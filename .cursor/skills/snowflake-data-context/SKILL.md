---
name: snowflake-data-context
description: >-
  Looks up Phenom product data schemas from local knowledge files and queries them via Snowflake. Use when asking for usage metrics, counts, trends, SQL, or analytics data questions.
---

When a user asks a data question about product usage, customer behavior, scheduling activity,
or any operational metric — use this workflow to find the right tables and query them.

## Step 1 — Load the right data context file

Use the table below to load the correct local knowledge file. Do NOT search or guess.

| Area | Local File |
|---|---|
| Platform (shared entities: candidates, applications, accounts, recruiter activity) | `product-copilot-beta/knowledge/platform/core-entities.md` |
| Platform (REFNUM → account name resolution) | `product-copilot-beta/knowledge/platform/account-tenant-mapping.md` |
| Platform (cross-pod joins, time-to-offer, interview round counting, job activity) | `product-copilot-beta/knowledge/platform/cross-pod-join-patterns.md` |
| Interview Management (scheduling requests, meetings, II recording, evaluations) | `product-copilot-beta/knowledge/interview-management/data-context.md` |
| Scheduling (detailed schema + query patterns) | `product-copilot-beta/knowledge/interview-management/scheduling/data-context.md` |
| Interview Intelligence (detailed schema + query patterns) | `product-copilot-beta/knowledge/interview-management/interview-intelligence/data-context.md` |
| Screening | `product-copilot-beta/knowledge/screening/data-context.md` |

For questions spanning multiple areas, read both the pod-specific file AND the relevant Platform file.

If unsure which area applies, default to loading `product-copilot-beta/knowledge/interview-management/data-context.md` for Interview Management questions, or `product-copilot-beta/knowledge/screening/data-context.md` for screening questions.

## Step 2 — Read the file to understand the schema

Load the file identified above. Extract:

- **Database** and **Schema** — listed at the top of every file (e.g. `Database: CID`, `Schema: RAW_SCHEMA`)
- **Table names and columns** — each table section lists columns with type and description
- **Common filters** — pre-written WHERE conditions for typical queries
- **Common joins** — how tables link to each other and to platform tables

Never skip this step. Never guess table or column names.

## Step 3 — Query Snowflake

Call `execute_snowflake_query` with a SELECT built from what you read.

Rules:
- Fully qualify every table: `{Database}.{Schema}.{TableName}` (e.g. `CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST`)
- Always include a LIMIT clause (max 500 rows for detail queries; aggregations don't need it)
- Use `REFNUM` to filter by customer when the question is customer-specific
- Use `DATEADD('MONTH', -N, CURRENT_DATE())` or explicit date literals for date ranges
- For account/customer names, join to `SALESFORCE_SCHEMA.ACCOUNT` on `REFNUM = REFNUM_C`

## Step 4 — Interpret and summarize

Return a clear, human-readable answer. Include:
- The specific numbers or trends the user asked about
- What filters were applied (date range, customer, etc.)
- An offer to drill deeper or break down by dimension

## Notes

- Snowflake table and column names are case-sensitive — use them exactly as shown in the file.
- If Snowflake returns "does not exist or not authorized", re-read the file and verify the
  Database and Schema values — do not guess alternatives.
- `product-copilot-beta/knowledge/platform/core-entities.md` covers entities shared across all pods. Check it
  if a table you need is not found in the pod-specific file.
- For complex cross-pod queries (e.g. application → scheduling join, time-to-hire), always
  load `product-copilot-beta/knowledge/platform/cross-pod-join-patterns.md` which has pre-built query patterns.
