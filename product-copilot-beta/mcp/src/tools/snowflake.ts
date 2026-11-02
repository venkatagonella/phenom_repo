import snowflake from "snowflake-sdk";
import type { ToolCall, ToolDefinition, CredentialProvider } from "../types.js";
import { logger } from "./lib/logger.js";
import { renderSnowflakeLoginPage } from "./lib/snowflake-login-page.js";

// The MCP server talks over stdout, so the driver must never print there.
// Only errors go to stderr; everything else is dropped (no snowflake.log either).
const noop = () => {};
snowflake.configure({
  customLogger: {
    error: (msg: string) => console.error(`[snowflake-sdk] ${msg}`),
    warn: noop,
    info: noop,
    debug: noop,
    trace: noop,
  },
});

// ── Credential helper ─────────────────────────────────────────────────────────

interface SnowflakeCreds {
  /** sso = browser login (Okta) via the Node driver; pat/oauth = bearer token via the SQL REST API. */
  authMode: "oauth" | "pat" | "sso";
  accessToken: string;
  account: string;
  user?: string;
  warehouse?: string;
  role?: string;
}

async function getSnowflakeCredsFromProvider(credProvider: CredentialProvider): Promise<SnowflakeCreds | null> {
  const row = await credProvider.getCredentials("snowflake");
  if (!row?.access_token) return null;
  const meta = row.metadata as
    | { account?: string; user?: string; warehouse?: string; role?: string; authMode?: string }
    | null;
  if (!meta?.account) return null;
  const authMode = meta.authMode === "sso" ? "sso" : meta.authMode === "pat" ? "pat" : "oauth";
  if (authMode === "sso" && !meta.user) return null;
  return {
    authMode,
    accessToken: row.access_token,
    account: meta.account,
    user: meta.user,
    warehouse: meta.warehouse,
    role: meta.role,
  };
}

// ── Snowflake SQL REST API v2 ─────────────────────────────────────────────────

interface SnowflakeStatementResponse {
  statementHandle?: string;
  message?: string;
  code?: string;
  sqlState?: string;
  resultSetMetaData?: {
    rowType: Array<{ name: string; type: string }>;
    numRows: number;
  };
  data?: string[][];
}

function formatSnowflakeError(status: number, result: SnowflakeStatementResponse): string {
  if (result.code === "390432" || result.message?.includes("Network policy is required")) {
    return (
      `Snowflake rejected the access token (error 390432: network policy is required). ` +
      `Snowflake only accepts a PAT when a network policy is attached to your user, so connecting to VPN does not help. ` +
      `Switch to browser SSO with \`cd mcp && npm run setup snowflake\`, or ask a Snowflake admin to attach a network policy to your user.`
    );
  }
  return `Snowflake error (${status}): ${result.message ?? JSON.stringify(result)}`;
}

// ── Browser SSO (EXTERNALBROWSER) via the Node driver ────────────────────────

// One connection per MCP process. The first query opens a browser tab for Okta;
// later queries reuse the session, and the driver caches the login on disk.
let ssoConnection: Promise<snowflake.Connection> | null = null;

function getSsoConnection(creds: SnowflakeCreds): Promise<snowflake.Connection> {
  if (!ssoConnection) {
    const conn = snowflake.createConnection({
      account: creds.account,
      username: creds.user,
      authenticator: "EXTERNALBROWSER",
      clientStoreTemporaryCredential: true,
      clientSessionKeepAlive: true,
      browserResponseRenderer: renderSnowflakeLoginPage,
      ...(creds.warehouse ? { warehouse: creds.warehouse } : {}),
      ...(creds.role ? { role: creds.role } : {}),
    });
    ssoConnection = conn
      .connectAsync()
      .then(async (c) => {
        await executeSso(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 120");
        return c;
      })
      .catch((err) => {
        ssoConnection = null;
        throw err;
      });
  }
  return ssoConnection;
}

export async function closeSnowflakeConnection(): Promise<void> {
  if (!ssoConnection) return;
  const conn = await ssoConnection.catch(() => null);
  ssoConnection = null;
  if (conn?.isUp()) await new Promise<void>((resolve) => conn.destroy(() => resolve()));
}

function executeSso(
  conn: snowflake.Connection,
  sqlText: string
): Promise<{ columns: string[]; rows: Record<string, string>[] }> {
  return new Promise((resolve, reject) => {
    conn.execute({
      sqlText,
      // Match the REST API, which returns every value as a string.
      fetchAsString: ["Boolean", "Number", "Date", "JSON", "Buffer"],
      complete: (err, stmt, rows) => {
        if (err) return reject(err);
        const columns = stmt.getColumns()?.map((c) => c.getName()) ?? [];
        const out = (rows ?? []).map((row) => {
          const obj: Record<string, string> = {};
          for (const col of columns) obj[col] = row[col] ?? "";
          return obj;
        });
        resolve({ columns, rows: out });
      },
    });
  });
}

async function runStatementSso(
  creds: SnowflakeCreds,
  sql: string,
  warehouse?: string,
  database?: string,
  schema?: string
): Promise<{ columns: string[]; rows: Record<string, string>[]; rowCount: number }> {
  const run = async () => {
    const conn = await getSsoConnection(creds);
    if (warehouse) await executeSso(conn, `USE WAREHOUSE ${warehouse}`);
    if (database) await executeSso(conn, `USE DATABASE ${database}`);
    if (schema) await executeSso(conn, `USE SCHEMA ${schema}`);
    return executeSso(conn, sql);
  };

  let result;
  try {
    result = await run();
  } catch (err) {
    // Session dropped (laptop sleep, expiry): reconnect once, then give up.
    const conn = await ssoConnection?.catch(() => null);
    if (conn && conn.isUp()) throw err;
    ssoConnection = null;
    result = await run();
  }
  return { ...result, rowCount: result.rows.length };
}

// ── PAT / OAuth via the SQL REST API ─────────────────────────────────────────

async function runStatement(
  creds: SnowflakeCreds,
  sql: string,
  warehouse?: string,
  database?: string,
  schema?: string
): Promise<{ columns: string[]; rows: Record<string, string>[]; rowCount: number }> {
  const url = `https://${creds.account}.snowflakecomputing.com/api/v2/statements`;

  const body: Record<string, unknown> = {
    statement: sql,
    timeout: 120,
  };
  if (warehouse ?? creds.warehouse) body.warehouse = warehouse ?? creds.warehouse;
  if (creds.role) body.role = creds.role;
  if (database) body.database = database;
  if (schema) body.schema = schema;

  const tokenType = creds.authMode === "pat" ? "PROGRAMMATIC_ACCESS_TOKEN" : "OAUTH";

  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Authorization: `Bearer ${creds.accessToken}`,
      "X-Snowflake-Authorization-Token-Type": tokenType,
    },
    body: JSON.stringify(body),
  });

  const result = (await res.json()) as SnowflakeStatementResponse;

  if (!res.ok || (result.code && result.code !== "090001")) {
    throw new Error(formatSnowflakeError(res.status, result));
  }

  const columns = result.resultSetMetaData?.rowType.map((c) => c.name) ?? [];
  const rows = (result.data ?? []).map((row) => {
    const obj: Record<string, string> = {};
    columns.forEach((col, i) => {
      obj[col] = row[i] ?? "";
    });
    return obj;
  });

  return { columns, rows, rowCount: rows.length };
}

// ── Tool definitions ──────────────────────────────────────────────────────────

export const snowflakeToolDefinitions: ToolDefinition[] = [
  {
    name: "execute_snowflake_query",
    description:
      "Execute a SQL query against Snowflake and return results as JSON. " +
      "Use this to fetch ServiceNow tickets, support data, or any data stored in Snowflake. " +
      "Always include a LIMIT clause to avoid returning too many rows (max 500 recommended). " +
      "Results are capped at 500 rows regardless of query.",
    input_schema: {
      type: "object",
      properties: {
        sql: {
          type: "string",
          description:
            "The SQL SELECT statement to execute. Include a LIMIT clause. " +
            "Example: SELECT number, short_description, category, opened_at FROM SERVICENOW.PUBLIC.INCIDENT WHERE category = 'Scheduling' AND opened_at >= DATEADD('month', -3, CURRENT_TIMESTAMP()) LIMIT 500",
        },
        database: {
          type: "string",
          description: "Snowflake database to query. Leave blank to use the default from the config page.",
        },
        schema: {
          type: "string",
          description: "Snowflake schema to query. Leave blank to use the default from the config page.",
        },
        warehouse: {
          type: "string",
          description: "Snowflake warehouse to use. Defaults to the user's connected warehouse.",
        },
      },
      required: ["sql"],
    },
  },
];

export const snowflakeToolNames = new Set(snowflakeToolDefinitions.map((t) => t.name));

// ── Executor ──────────────────────────────────────────────────────────────────

export async function executeSnowflakeTool(
  _userId: string,
  call: ToolCall,
  credProvider: CredentialProvider
): Promise<string> {
  const creds = await getSnowflakeCredsFromProvider(credProvider);
  if (!creds) {
    return "Error: Snowflake is not connected. Run `npm run setup` and follow the Snowflake prompts.";
  }

  if (call.name === "execute_snowflake_query") {
    const { sql, database, schema, warehouse } = call.input as {
      sql: string;
      database?: string;
      schema?: string;
      warehouse?: string;
    };

    if (!sql?.trim()) return "Error: sql parameter is required.";

    try {
      logger.debug("snowflake", `executing: ${sql.slice(0, 160)}`);
      const run = creds.authMode === "sso" ? runStatementSso : runStatement;
      const { columns, rows, rowCount } = await run(creds, sql, warehouse, database, schema);

      if (rowCount === 0) return "Query returned 0 rows.";

      const capped = rows.slice(0, 500);
      const truncated = rowCount > 500 ? ` (showing first 500 of ${rowCount})` : "";

      return (
        `Query returned ${rowCount} rows${truncated}. Columns: ${columns.join(", ")}\n\n` +
        `Results:\n${JSON.stringify(capped, null, 2)}`
      );
    } catch (err) {
      logger.error("snowflake", `query error: ${err}`);
      let message = err instanceof Error ? err.message : String(err);
      if (!warehouse && !creds.warehouse) {
        message +=
          "\n\nAlso: no default warehouse is configured. Run `cd mcp && npm run setup snowflake` and provide your warehouse.";
      }
      return `Error executing query: ${message}`;
    }
  }

  return `Unknown tool: ${call.name}`;
}
