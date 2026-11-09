---
name: MCP Connectivity Checks
type: policy
description: Keep MCP auth and connection checks minimal — never dump full tool catalogs for status
always: true
metadata:
  owner: nikhilsharma-phenom
  status: stable
---

# MCP Connectivity & Auth — Token Budget

For MCP **auth**, **connection**, or **status** checks, use the smallest possible call. Do not treat these as discovery tasks.

## Happy path (1 call)

Call the server's lightweight status/identity tool only, e.g.:

- Atlassian → `atlassianUserInfo`
- Other servers → `whoami`, `get_account_info`, or equivalent

If it succeeds, report status and **stop**.

## Auth needed (2 calls max)

1. Status/identity tool fails or returns not connected
2. Call `mcp_auth` **once**
3. Re-check with the status/identity tool

Do not retry auth in a loop. Do not probe multiple server aliases unless the first known-good server fails.

## Forbidden for status checks

- Full-server `GetMcpTools` (no `toolName`) — dumps every schema
- Broad `GetMcpTools` pattern searches across a product's tool catalog
- Catalog listing of all MCP servers when checking one connection
- Dual-probing `user-*` and `plugin-*` variants of the same product in parallel for a simple "are you connected?" ask

## When full tool schemas are allowed

Use `GetMcpTools` with **`server` + `toolName`** only when you are about to **invoke** that tool and need its input schema. Prefer one tool at a time.

## Budget rule of thumb

| Ask | Max tool calls | Catalog dumps |
|-----|----------------|---------------|
| "Connect / auth / are you connected?" | 1–2 | **0** |
| Implementing a new MCP integration | As needed | Prefer single-tool lookups |
