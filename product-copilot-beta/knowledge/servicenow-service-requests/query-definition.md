# Query definition (from the sheet)

The workbook includes SQL that defines how Sheet1 was built. Below is the text **as returned by a Google Drive read of that spreadsheet** on 2026-09-23.

**Integrity note:** The Drive read truncated the SQL at the trailing predicate `WHERE t."NUMBER" IS NOT`. The remainder of the clause was not present in the tool output. Do not invent the missing characters. Do not execute this SQL against Snowflake under the **servicenow-service-requests** skill (sheet-only rule). The SQL is documentation of column semantics only.

```sql
WITH task_sn AS (
    SELECT "SYS_ID", "NUMBER", "SHORT_DESCRIPTION", "DESCRIPTION",
           "STATE", "OPENED_AT", "SYS_CREATED_ON"
    FROM fivetran_db.servicenow.task
    WHERE NOT _fivetran_deleted
      AND "SYS_CREATED_ON" >= '2026-01-01'   -- replaces {% condition date_filter %}
),
sn_case AS (
    SELECT "SYS_ID", "U_REQUEST_TYPE", "U_SUB_STATUS",
           "U_PRODUCT_EXPERIENCE", "U_JIRA_CASE", "ACCOUNT_VALUE"
    FROM fivetran_db.servicenow.sn_customerservice_case
    WHERE NOT _fivetran_deleted
      AND "U_REQUEST_TYPE" = 'Service Request'
),
/* sys_choice can carry one row per language per value. The QUALIFY keeps the
   lookups strictly 1:1 so they cannot multiply case rows. */
state_lookup AS (
    SELECT value, label
    FROM fivetran_db.servicenow.sys_choice
    WHERE element = 'state'
      AND name    = 'sn_customerservice_case'
      AND NOT _fivetran_deleted
    QUALIFY ROW_NUMBER() OVER (PARTITION BY value ORDER BY label) = 1
),
sub_status_lookup AS (
    SELECT value, label
    FROM fivetran_db.servicenow.sys_choice
    WHERE element = 'u_sub_status'
      AND name    = 'sn_customerservice_case'
      AND NOT _fivetran_deleted
    QUALIFY ROW_NUMBER() OVER (PARTITION BY value ORDER BY label) = 1
),
client AS (
    SELECT ca."SYS_ID" AS ca_sys_id, a."NAME" AS client_name
    FROM fivetran_db.servicenow.customer_account ca
    JOIN fivetran_db.salesforce_db.account a
      ON ca."U_SFDC_CORRELATION_ID" = a."ID"
    WHERE NOT ca._fivetran_deleted
      AND NOT a.is_deleted
),
-- U_JIRA_CASE holds 'ABC-1, ABC-2'; explode to one row per key
jira_keys AS (
    SELECT sc."SYS_ID" AS sc_sys_id, TRIM(j.value) AS jira_key
    FROM sn_case sc,
         LATERAL FLATTEN(input => SPLIT(sc."U_JIRA_CASE", ',')) j
    WHERE sc."U_JIRA_CASE" IS NOT NULL
      AND TRIM(sc."U_JIRA_CASE") <> ''
      AND TRIM(j.value) <> ''
),
-- AIRBYTE_ISSUE can hold several rows per key; keep the best one
jira_issue AS (
    SELECT key, id AS jira_issue_id
    FROM CID.JIRA_SCHEMA.AIRBYTE_ISSUE
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY key
        ORDER BY CASE WHEN status IS NOT NULL THEN 0 ELSE 1 END, id DESC
    ) = 1
),
-- customfield_15211 = Product Experience Product, latest value wins
product_experience_product AS (
    SELECT fh.ISSUE_ID, fo.NAME AS product_experience_product
    FROM CID.JIRA_SCHEMA.AIRBYTE_ISSUE_FIELD_HISTORY fh
    JOIN CID.JIRA_SCHEMA.AIRBYTE_FIELD_OPTION fo
      ON fh.VALUE = fo.ID::VARCHAR
    WHERE fh.FIELD_ID = 'customfield_15211'
      AND fh.VALUE IS NOT NULL
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY fh.ISSUE_ID ORDER BY fh.TIME DESC
    ) = 1
),
case_product AS (
    SELECT jk.sc_sys_id, pep.product_experience_product
    FROM jira_keys jk
    LEFT JOIN jira_issue ji                   ON jk.jira_key = ji.key
    LEFT JOIN product_experience_product pep  ON ji.jira_issue_id = pep.ISSUE_ID
),
/* One row per case: how many JIRA keys it carries and how many resolve.
   Aggregated, so this join cannot add row fan-out on top of case_product. */
jira_link AS (
    SELECT
        sc_sys_id,
        COUNT(*)                 AS jira_key_count,
        COUNT(jira_issue_id)     AS jira_resolved_count,
        LISTAGG(DISTINCT jira_key, '; ')
            WITHIN GROUP (ORDER BY jira_key) AS jira_case_keys
    FROM (
        SELECT jk.sc_sys_id, jk.jira_key, ji.jira_issue_id
        FROM jira_keys jk
        LEFT JOIN jira_issue ji ON jk.jira_key = ji.key
    ) k
    GROUP BY sc_sys_id
)
SELECT DISTINCT
    t."NUMBER"                                 AS case_number,
    t."SHORT_DESCRIPTION"                      AS short_description,
    t."DESCRIPTION"                            AS description,
    sl.label                                   AS status,
    t."STATE"                                  AS status_code,
    COALESCE(ssl.label, sc."U_SUB_STATUS")     AS sub_status,
    CASE
        WHEN jl.sc_sys_id IS NULL        THEN 'No'
        WHEN jl.jira_resolved_count = 0  THEN 'Linked - key not found in JIRA'
        ELSE 'Yes'
    END                                        AS jira_created,
    COALESCE(jl.jira_key_count, 0)             AS jira_key_count,
    jl.jira_case_keys,
    cp.product_experience_product,
    sc."U_PRODUCT_EXPERIENCE"                  AS product_experience,
    CONVERT_TIMEZONE('UTC', t."SYS_CREATED_ON")                            AS created_on_utc,
    CONVERT_TIMEZONE('Asia/Hong_Kong', t."SYS_CREATED_ON")::TIMESTAMP_NTZ  AS created_on_hkt,
    cl.client_name
FROM task_sn t
JOIN      sn_case sc            ON t."SYS_ID"          = sc."SYS_ID"
LEFT JOIN state_lookup sl       ON t."STATE"           = sl.value
LEFT JOIN sub_status_lookup ssl ON sc."U_SUB_STATUS"   = ssl.value
LEFT JOIN client cl             ON sc."ACCOUNT_VALUE"  = cl.ca_sys_id
LEFT JOIN case_product cp       ON sc."SYS_ID"         = cp.sc_sys_id
LEFT JOIN jira_link jl          ON sc."SYS_ID"         = jl.sc_sys_id
WHERE t."NUMBER" IS NOT
```

*(Truncated in source read — ends exactly as shown.)*
