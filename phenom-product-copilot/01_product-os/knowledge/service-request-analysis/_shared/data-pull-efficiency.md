# Data pull efficiency (token + time savers)

Learned while filling the RX label sheet (2026-09-19). Prefer these patterns over rediscovery.

## Principles

1. **Snowflake bulk first** for populations, joins, descriptions, escalation rates.
2. **Never 1:1 Jira MCP/API per ticket** when a search/JQL batch or Snowflake replica can cover many keys.
3. **Cache pulls locally** (`~/Downloads/rx-label-sheet-sn-pull.json`, `rx-jira-issues-by-key.json`, `rx-jira-comments-by-key.json`) and reuse within a session.
4. **Label sheet ≠ metrics** — write populations to Summary from Snowflake; sheet is for recommendations + `Details` enrichment.

## Snowflake SQL API (Node on Mac)

Auth: `~/.copilot/tokens.json` → `snowflake` PAT; header `X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN`.

### Partition pagination (required)

First response often returns only partition 0 (~300 rows). `partitionInfo` lists more.

- Fetch remaining with: `GET .../statements/{handle}?partition={n}` (query param form).
- Path form `/partitions/{n}` often returns **empty body** — avoid.
- Set `dns.setDefaultResultOrder('ipv4first')` to reduce connect timeouts (VPN/IPv6).

### SN case pull (locked objects)

| Object | Role |
|--------|------|
| `FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE` | Primary (`SYS_ID`, `U_*`, `SYS_CREATED_ON`, `ACCOUNT_VALUE`) |
| `FIVETRAN_DB.SERVICENOW.TASK` | `NUMBER`, `STATE`, `SHORT_DESCRIPTION`, `DESCRIPTION` (STATE is **not** on CASE) |
| `FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_JIRA_TASK` | Bridge: `U_CASE_NUMBER_VALUE` = case `SYS_ID` → `U_JIRA_KEY` |

**Required CASE columns on every label-sheet / population pull** (do not drop these from SELECT):

- `U_COMPONENT`, `U_SUBCOMPONENT` → sheet `SN - Component` / `SN - Sub-Component`
- `U_REQUEST_CATEGORY` → sheet `SN - Request Category` (normalize slugs; see [`sn-request-category.md`](sn-request-category.md))
- `U_TICKET_CLASSIFICATION`, `U_TICKET_CLASSIFICATION_CHILD` → sheet `SN - Classification` / `SN - Classification (Child)`
- `U_REQUEST_TYPE`, `U_PRODUCT_EXPERIENCE`

Prefer **two queries** (cases + links) over heavy `LISTAGG` in one statement when debugging; merge in Node. Canonical SELECT: [`sql-templates.md` → Label-sheet case pull](../../../skills/service-request-analysis/sql-templates.md).

Primary Jira key heuristic: prefer `SUP-%`, else first linked key, else `CASE.U_JIRA_CASE`.

### Jira issue fields in Snowflake

`SPX_DB.JIRA_REPLICA_V2.ISSUE` has a **small** column set (~33): `KEY`, `SUMMARY`, `STATUS`, `DESCRIPTION`, `CREATED`, `ID`, etc.

- **No** `CUSTOMFIELD_*` product-area fields here — get filed product area from Jira API or prior sheet, not this table.
- Chunk `KEY IN (...)` lists (~400 keys) for description/summary/status.

## Comments — critical freshness trap

| Source | Join | Usable for May 2026+ RX SUP? |
|--------|------|------------------------------|
| `SPX_DB.JIRA_REPLICA_V2.COMMENT` | `COMMENT.ISSUE_ID = ISSUE.ID` | **No** — `ISSUE_ID` max ~3.1M; recent SUP issue IDs are ~4.7M+ |
| `SPX_DB.JIRA_AIRBYTE_SCHEMA_LATEST.ISSUE_COMMENTS` | `ISSUEID` is the **issue key string** (e.g. `SUP-68462`), not numeric id | Stale / empty for `SUP-12xxxx` in practice |
| Live Jira | Atlassian `searchJiraIssuesUsingJql` | **Yes** — use this for `Details` comment threads |

### Efficient live Jira pull (comments + metadata)

- Tool: `searchJiraIssuesUsingJql`, `responseContentFormat: "markdown"`.
- JQL batches: `key in (SUP-1, SUP-2, …)` — **~40–50 keys per call**, `maxResults: 100`.
- **Always** request these fields on escalated-key batches (add `comment` when filling `details`):
  `summary`, `description`, `status`, `components`, `customfield_15126` (Component), `customfield_14807` (Sub Component), `customfield_18695` (Ticket Classification), `customfield_15211` (Product Experience : Product).
- ~1,100 keys ≈ ~25 API calls, not 1,100 `getJiraIssue` calls.
- Cache: `~/Downloads/rx-jira-issues-by-key.json` and/or `rx-jira-component-classification.json`.
- Map classification to the live sheet headers; keep Jira component metadata in the local cache (see section below).

### Pitfalls that wasted tokens

- Filtering `COALESCE(IS_PUBLIC, TRUE) = TRUE` when `IS_PUBLIC` is string `'true'`/`'false'` → zero rows.
- Assuming `ILIKE 'SUP-12%'` means “2026 SUP-12xxxx” — also matches ancient `SUP-12009`, etc.
- Rewriting the whole Sheets grid without expanding `rowCount` first → `Range exceeds grid limits`.
- Google refresh over IPv6 → connect timeout; force IPv4 first + longer abort.

## Google Sheet writes

- Spreadsheet: RX label sheet `1dTFPQUDCWflvrJ8xjfGm_21Ea_mGlFeZkIyjMCT8Sto`.
- Refresh Google token via product-copilot-backend `/integrations/refresh/google` + `backend_jwt` before Sheets API.
- Before large writes: `updateSheetProperties.gridProperties.rowCount` (≥ row count + buffer).
- Chunk value puts (~80–150 rows); smaller chunks when `details` cells are large.
- Do **not** treat prior heuristic/`prior-label-sheet` rows as human-reviewed unless Sebastian says so.

## Suggested agent order for a full fill

1. Ask PE / area / window (skill intake).
2. SN cases + Jira links from Snowflake → local JSON — **must include** `U_COMPONENT`, `U_SUBCOMPONENT`, `U_REQUEST_CATEGORY`, `U_TICKET_CLASSIFICATION`, `U_TICKET_CLASSIFICATION_CHILD` (see label-sheet case pull in [`sql-templates.md`](../../../skills/service-request-analysis/sql-templates.md)).
3. ISSUE summary/description/status from Snowflake (chunked).
4. **All SN rows:** `SHORT_DESCRIPTION` + description + `SYS_JOURNAL_FIELD` → `Summary` / `Details` (covers Layer B).
5. Escalated keys only: **live Jira JQL batches** with fields including `components`, `customfield_15126`, `customfield_14807`, `customfield_18695` (+ `comment` when filling `Details`); write classification fields and keep component metadata in the local cache.
6. Merge into Tickets + Summary metrics; leave label columns `proposed` until human review.
7. **Verify** no blank `Summary` / `Details` (especially SN-only rows) **and** SN metadata columns populated from Snowflake; Jira metadata populated for rows with a Jira ID.

## Layer B / SN-only narrative (do not skip)

**Mistake (2026-09-19):** filled `Summary` / `Details` only from Jira → ~1.3k never-escalated rows stayed blank.

For **every** in-scope SN row (especially Layer B with no Jira ID):

| Sheet field | Snowflake source |
|-------------|------------------|
| `Summary` | `TASK.SHORT_DESCRIPTION` (join `TASK.SYS_ID = CASE.SYS_ID`) |
| `Details` | `TASK.DESCRIPTION` + journal threads |

### Journal / work notes

- Table: `FIVETRAN_DB.SERVICENOW.SYS_JOURNAL_FIELD`
- Join: `ELEMENT_ID = CASE.SYS_ID` (not `SYS_ID` of the journal row)
- Useful `ELEMENT` values: `work_notes`, `comments`, `additional_comments`, `close_notes`
- Fallback if journal empty: `TASK.WORK_NOTES`, `TASK.COMMENTS`, `TASK.CLOSE_NOTES`, `TASK.COMMENTS_AND_WORK_NOTES`

Chunk `ELEMENT_ID IN (...)` (~400 ids). Put last ~8–10 journal lines into `Details` after Description.

### Layer C/D (has Jira)

- `Summary` / description / comments: live Jira JQL batches (see above)
- If Jira summary blank, backfill `Summary` from `TASK.SHORT_DESCRIPTION`

**Rule:** after any label-sheet fill, assert `Summary` and `Details` are non-empty for **all** rows (SN-only and escalated). Zero blank narrative rows is a success criterion.

## `details` writing

After pulling text, **rewrite** `Details` into Problem / Discussions / Solution — see [`details-format.md`](details-format.md). Never leave raw description + numbered comment dumps on the sheet.

## SN request category (Support subcategory)

Field: `SN_CUSTOMERSERVICE_CASE.U_REQUEST_CATEGORY` (join `TASK.NUMBER` for CS id).

Formal Service Request subcategories (normalize slugs → display labels):

| Raw (common) | Display |
|--------------|---------|
| `admin_task` | Admin Tasks/ EIS Tasks — routine admin / enable-disable |
| `adoption` | Adoption — help using documented functionality |
| `Functionality Clarification` | Functionality Clarification — how the feature technically works |
| `Feature Clarification` | Feature Clarification — what a feature does / why it exists |
| `issue_question` | Service Request - Issue/Question — holding value only; never recommend as the corrected destination |

Also useful (not Support request category): `U_TICKET_CLASSIFICATION` + `U_TICKET_CLASSIFICATION_CHILD` (e.g. Product & Knowledge Issues → Documentation).

Sheet columns: `SN - Request Category`, `SN - Classification`, `SN - Classification (Child)`. Never overwrite `Recommendation …` columns during a source-data refresh.

## Jira Component / Ticket Classification (live API)

Snowflake `JIRA_REPLICA_V2.ISSUE` has **no** these custom fields. Pull via Atlassian `searchJiraIssuesUsingJql` in key batches (~40).

| Sheet column | Jira field |
|--------------|------------|
| `JIRA - Ticket Classification` | `customfield_18695`.value |
| `jira_ticket_classification_child` | `customfield_18695`.child.value |

Keep Component (`customfield_15126`) and Sub-Component (`customfield_14807`) in
`~/Downloads/rx-jira-component-classification.json`; the live Tickets tab has no destination columns for them.

