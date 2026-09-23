# Schema — columns on the data tab

Source: header row of Sheet1 in spreadsheet `1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8`.

| Column | Meaning (from sheet header + SQL tab on the same workbook) |
|--------|-------------------------------------------------------------|
| `CASE_NUMBER` | ServiceNow task/case number (e.g. `CS0293199`) |
| `SHORT_DESCRIPTION` | Short description from the task |
| `DESCRIPTION` | Full description / body |
| `STATUS` | Human-readable case state label |
| `STATUS_CODE` | Numeric state code on the task |
| `SUB_STATUS` | Sub-status label (or raw value if label missing) |
| `JIRA_CREATED` | Whether linked Jira keys resolve in Jira: values defined in the sheet SQL as `No`, `Yes`, or `Linked - key not found in JIRA` |
| `JIRA_KEY_COUNT` | Count of Jira keys on the case |
| `JIRA_CASE_KEYS` | Distinct Jira keys aggregated (semicolon-separated in the SQL) |
| `PRODUCT_EXPERIENCE_PRODUCT` | Product label from linked Jira custom field when present; often blank when no resolvable Jira link |
| `PRODUCT_EXPERIENCE` | Product experience on the ServiceNow case (`U_PRODUCT_EXPERIENCE`) |
| `CREATED_ON_UTC` | Created timestamp in UTC |
| `CREATED_ON_HKT` | Same created timestamp in Asia/Hong_Kong |
| `CLIENT_NAME` | Client/account name |

## Row grain

One row per service-request case (SQL uses `SELECT DISTINCT` over the joined case).

## Filters baked into the extract (from SQL tab)

As written on the sheet’s SQL tab (do not add extra filters when describing “what the sheet is”):

- Task `SYS_CREATED_ON` ≥ `2026-01-01`
- Case `U_REQUEST_TYPE` = `Service Request`
- Non-deleted Fivetran rows for the listed source tables

## Primary “key area” fields for roadmap-style questions

Use these **before** inventing free-text themes:

1. `PRODUCT_EXPERIENCE`
2. `PRODUCT_EXPERIENCE_PRODUCT` (report blank rate; do not impute)

Free-text themes may only come from `SHORT_DESCRIPTION` and `DESCRIPTION` with an explicit method and case citations.
