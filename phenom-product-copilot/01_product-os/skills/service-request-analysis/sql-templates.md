# SQL templates — Service Request analysis

Fully qualify tables. Prefer aggregations; use `LIMIT` on detail pulls (max 500) except **label-sheet population pulls** (full window, no LIMIT).

Always exclude deleted Fivetran rows: `COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE` (and same on `TASK` / bridge when joined).

## Population + escalation (distinct cases)

```sql
WITH links AS (
  SELECT
    U_CASE_NUMBER_VALUE AS CASE_SYS_ID,
    COUNT_IF(U_JIRA_KEY IS NOT NULL) AS LINK_COUNT,
    COUNT_IF(U_JIRA_KEY ILIKE 'SUP-%') AS SUP_LINK_COUNT
  FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_JIRA_TASK
  WHERE COALESCE(_FIVETRAN_DELETED, FALSE) = FALSE
  GROUP BY 1
)
SELECT
  COUNT(DISTINCT c.SYS_ID) AS sn_srs,
  COUNT(DISTINCT CASE WHEN COALESCE(j.LINK_COUNT, 0) > 0 THEN c.SYS_ID END) AS any_jira,
  COUNT(DISTINCT CASE WHEN COALESCE(j.SUP_LINK_COUNT, 0) > 0 THEN c.SYS_ID END) AS sup_only,
  COUNT(DISTINCT CASE WHEN COALESCE(j.LINK_COUNT, 0) = 0 THEN c.SYS_ID END) AS never_escalated
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
LEFT JOIN links j ON c.SYS_ID = j.CASE_SYS_ID
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'  -- swap PE label
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
  -- optional area filter via U_COMPONENT / U_SUBCOMPONENT when analyzing one CRM/Platform area
;
```

## Monthly volume

```sql
SELECT
  DATE_TRUNC('month', c.SYS_CREATED_ON) AS month,
  COUNT(DISTINCT c.SYS_ID) AS sn_srs
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
GROUP BY 1
ORDER BY 1
;
```

## Component / subcomponent mix (top areas)

```sql
SELECT
  c.U_COMPONENT,
  c.U_SUBCOMPONENT,
  COUNT(DISTINCT c.SYS_ID) AS sn_srs
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
GROUP BY 1, 2
ORDER BY sn_srs DESC
LIMIT 30
;
```

## SN request category mix (Support subcategory)

```sql
SELECT
  c.U_REQUEST_CATEGORY,
  COUNT(DISTINCT c.SYS_ID) AS sn_srs
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
GROUP BY 1
ORDER BY sn_srs DESC
;
```

Normalize common slugs when writing the sheet: `admin_task` → Admin Tasks/ EIS Tasks, `adoption` → Adoption,
`issue_question` → Service Request - Issue/Question; keep pretty labels as-is. See
[`sn-request-category.md`](../../knowledge/service-request-analysis/_shared/sn-request-category.md).

## Label-sheet case pull (REQUIRED columns)

Use this (or a superset) whenever refreshing the Tickets population. Join `TASK` for CS number + state. **No LIMIT** for the full window.

```sql
SELECT
  t.NUMBER AS SN_NUMBER,
  c.SYS_ID AS SN_SYS_ID,
  c.SYS_CREATED_ON AS SN_CREATED,
  t.SHORT_DESCRIPTION,
  t.DESCRIPTION,
  t.STATE AS SN_STATE,
  c.U_REQUEST_TYPE,
  c.U_PRODUCT_EXPERIENCE,
  c.U_COMPONENT,                    -- → SN - Component
  c.U_SUBCOMPONENT,                 -- → SN - Sub-Component
  c.U_REQUEST_CATEGORY,             -- → SN - Request Category (normalize slugs)
  c.U_TICKET_CLASSIFICATION,        -- → SN - Classification
  c.U_TICKET_CLASSIFICATION_CHILD,  -- → SN - Classification (Child)
  c.ACCOUNT_VALUE,
  c.U_JIRA_CASE AS CASE_JIRA_HINT
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
JOIN FIVETRAN_DB.SERVICENOW.TASK t
  ON t.SYS_ID = c.SYS_ID
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND COALESCE(t._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
;
```

Second query: Jira links via `SN_CUSTOMERSERVICE_JIRA_TASK` (`U_CASE_NUMBER_VALUE` = case `SYS_ID` → `U_JIRA_KEY`). Merge in Node; primary key heuristic: prefer `SUP-%`, else first linked key, else `CASE.U_JIRA_CASE`.

Sheet mapping (metadata — do **not** overwrite triage `category` / `subcategory`):

| Snowflake | Sheet column |
|-----------|--------------|
| `U_COMPONENT` | `SN - Component` |
| `U_SUBCOMPONENT` | `SN - Sub-Component` |
| `U_REQUEST_CATEGORY` (normalized) | `SN - Request Category` |
| `U_TICKET_CLASSIFICATION` | `SN - Classification` |
| `U_TICKET_CLASSIFICATION_CHILD` | `SN - Classification (Child)` |

## Layer B candidate set (never escalated)

```sql
SELECT
  t.NUMBER AS SN_NUMBER,
  c.SYS_ID,
  c.SYS_CREATED_ON,
  c.ACCOUNT_VALUE,
  c.U_COMPONENT,
  c.U_SUBCOMPONENT,
  c.U_REQUEST_CATEGORY,
  c.U_TICKET_CLASSIFICATION,
  c.U_TICKET_CLASSIFICATION_CHILD,
  c.U_ISSUE_TYPE,
  t.STATE
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
JOIN FIVETRAN_DB.SERVICENOW.TASK t ON t.SYS_ID = c.SYS_ID
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND COALESCE(t._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
  AND NOT EXISTS (
    SELECT 1
    FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_JIRA_TASK j
    WHERE j.U_CASE_NUMBER_VALUE = c.SYS_ID
      AND j.U_JIRA_KEY IS NOT NULL
      AND COALESCE(j._FIVETRAN_DELETED, FALSE) = FALSE
  )
ORDER BY c.SYS_CREATED_ON DESC
LIMIT 500
;
```

## Layer C/D — escalations with SUP key

```sql
SELECT
  t.NUMBER AS SN_NUMBER,
  c.SYS_ID,
  c.SYS_CREATED_ON,
  c.U_COMPONENT,
  c.U_SUBCOMPONENT,
  c.U_REQUEST_CATEGORY,
  c.U_TICKET_CLASSIFICATION,
  c.U_TICKET_CLASSIFICATION_CHILD,
  j.U_JIRA_KEY
FROM FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE c
JOIN FIVETRAN_DB.SERVICENOW.TASK t ON t.SYS_ID = c.SYS_ID
INNER JOIN FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_JIRA_TASK j
  ON c.SYS_ID = j.U_CASE_NUMBER_VALUE
WHERE c.U_PRODUCT_EXPERIENCE = 'Recruiter Experience (RX)'
  AND c.U_REQUEST_TYPE = 'Service Request'
  AND COALESCE(c._FIVETRAN_DELETED, FALSE) = FALSE
  AND COALESCE(t._FIVETRAN_DELETED, FALSE) = FALSE
  AND c.SYS_CREATED_ON >= '2026-05-01'
  AND COALESCE(j._FIVETRAN_DELETED, FALSE) = FALSE
  AND j.U_JIRA_KEY ILIKE 'SUP-%'
ORDER BY t.SYS_CREATED_ON DESC
LIMIT 500
;
```

## Jira live fields (REQUIRED for escalated rows — not in Snowflake)

`SPX_DB.JIRA_REPLICA_V2.ISSUE` has **no** Ticket Classification / custom Component. For every linked Jira key, batch via Atlassian `searchJiraIssuesUsingJql`:

- JQL: `key in (KEY1, KEY2, …)` — **~40 keys / call**
- `fields`: `["summary","description","status","comment","components","customfield_15126","customfield_14807","customfield_18695","customfield_15211"]`
  - Include `comment` only when filling `details`; can omit on a metadata-only refresh
- Cache: `~/Downloads/rx-jira-component-classification.json`

| Sheet column | Jira field |
|--------------|------------|
| `JIRA - Ticket Classification` | `customfield_18695`.value |
| `jira_ticket_classification_child` | `customfield_18695`.child.value |
| `JIRA - Product Area` | `customfield_15211.child.value` (Product Experience : Product) |

Keep Component (`customfield_15126`) and Sub-Component (`customfield_14807`) in the local cache; the live Tickets tab has no destination columns for them.

Do not invent issue fields. See [`data-pull-efficiency.md`](../../knowledge/service-request-analysis/_shared/data-pull-efficiency.md).
