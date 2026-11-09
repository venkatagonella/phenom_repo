# Core Entities

**Database:** CID    **Schema:** RAW_SCHEMA    **Last updated:** 2026-02-10

Cross-pod foundational tables used by multiple experience pods. Always included as Tier 1 context in Product Copilot LLM calls.

## RB_APPLICATIONS

Job applications submitted by candidates.

| Column | Type | Description |
| --- | --- | --- |
| APPLICATION_ID | VARCHAR | Unique application identifier |
| REFNUM | VARCHAR | Customer identifier — join to SALESFORCE_SCHEMA.ACCOUNT |
| APPLIED_DATE | TIMESTAMP | When the application was submitted |
| HIRING_STATUS_CODE | VARCHAR | Current hiring status |
| JOB_ID | VARCHAR | Job posting identifier |

## RB_APPLICATIONS_DETAILS

Extended application data. **Each row = one hiring status change for an application.**

**WARNING: Rows can be duplicated** — the same status change (same APPLICATION_ID + HIRING_STATUS_UPDATED_DATE + HIRING_STATUS_STEP) may appear multiple times. Always use `COUNT(DISTINCT HIRING_STATUS_UPDATED_DATE)` when counting status changes, NOT `COUNT(*)`.

| Column | Type | Description |
| --- | --- | --- |
| APPLICATION_ID | VARCHAR | Unique application identifier |
| ATS_ID | VARCHAR | ATS candidate ID. Format: CANDIDATE-3-XXXXX. Does NOT match RB_VIDEO_SCREENS candidate ID. |
| USER_ID | VARCHAR | Hash-style candidate user ID. Joins to RB_VIDEO_SCREENS.VIDEOSCREENCANDIDATE_CANDIDATEID for screening linkage. |
| REFNUM | VARCHAR | Customer identifier |
| JOB_ID | VARCHAR | Job posting identifier |
| JOB_TITLE | VARCHAR | Job title (e.g., "Quality Specialist") |
| JOB_CATEGORY | VARCHAR | Job family/category (e.g., "Quality", "Stores & Distribution"). Use to filter by job family. |
| APPLIED_JOB_LOCATION | VARCHAR | Job location as displayed to applicant. Primary field for geographic analysis. Three inconsistent formats — see parsing notes below. |
| APPLIED_DATE | TIMESTAMP | When the application was submitted |
| HIRING_STATUS_CODE | VARCHAR | Hiring status code |
| HIRING_STATUS_STEP | VARCHAR | Human-readable step (e.g., "New Candidate", "Interview", "Offer", "Ready for Hire") |
| HIRING_STATUS_VALUE | VARCHAR | Normalized status value. See Hiring Pipeline section. Values: Lead, REVIEW, SCREEN, INTERVIEW, OFFER, HIRED, REJECTED |
| HIRING_STATUS_UPDATED_DATE | TIMESTAMP | When this status change occurred. Use with COUNT(DISTINCT) — rows may be duplicated. |
| HIRING_STATUS_PREVIOUS_STEP | VARCHAR | Previous step. NULL for first status. Use IS NOT NULL to filter to meaningful changes. |
| HIRING_STATUS_PREVIOUS_VALUE | VARCHAR | Previous status value |
| IS_REJECTED | BOOLEAN | Whether the candidate was rejected |
| REJECTION_REASON | VARCHAR | Reason for rejection |
| FIRST_SOURCE_CHANNEL | VARCHAR | First source channel (e.g., "direct / not_set") |
| LAST_SOURCE_CHANNEL | VARCHAR | Most recent source channel (e.g., "Internal Applicant / not_set") |
| APPLIED_SITE_TYPE | VARCHAR | Site type where application was submitted (e.g., "external", "internal") |

### Location Parsing Notes (APPLIED_JOB_LOCATION)

Three inconsistent formats exist:

1. `United States - California - San Diego` — Country - State - City (US jobs with state)
2. `India - Mumbai` — Country - City (non-US jobs, no state)
3. `Norway > Oslo : Kjelsasveien 161` — Country > City : Address (older format)

Trailing whitespace may exist. Always use `TRIM()`.

```sql
-- Extract country (handles both formats)
CASE WHEN CONTAINS(job_location, ' > ') THEN SPLIT_PART(job_location, ' > ', 1)
     ELSE TRIM(SPLIT_PART(job_location, ' - ', 1)) END AS country

-- Extract US state (only for US jobs with 3-part format)
CASE WHEN TRIM(SPLIT_PART(job_location, ' - ', 1)) = 'United States'
          AND TRIM(SPLIT_PART(job_location, ' - ', 3)) != ''
     THEN TRIM(SPLIT_PART(job_location, ' - ', 2)) ELSE NULL END AS us_state
```

### Common Joins

```sql
-- Link applications to scheduled interviews (coverage ~15% for some customers)
JOIN CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST sr
  ON APPLICATION_ID = sr.CANDIDATE_ATS_APPLICATION_ID

-- Link applications to screenings (requires both USER_ID and JOB_ID match)
JOIN CID.RAW_SCHEMA.RB_VIDEO_SCREENS vs
  ON USER_ID = vs.VIDEOSCREENCANDIDATE_CANDIDATEID AND JOB_ID = vs.INTERVIEWDETAILS_ENTITYVALUE

-- Get customer account name
JOIN CID.SALESFORCE_SCHEMA.ACCOUNT a ON REFNUM = a.REFNUM_C
```

## RB_JOBS

Job posting master record. **Each row = one job × one locale variant.** A single req typically has 1–24 rows (one per language the job is translated into). Always `GROUP BY JOB_ID` or `QUALIFY ROW_NUMBER() OVER (PARTITION BY JOB_ID ORDER BY JOB_LOCALE) = 1` before counting unique reqs.

| Column | Type | Description |
| --- | --- | --- |
| JOBS_OBJECT_ID | VARCHAR | Internal object ID |
| REFNUM | VARCHAR | Customer identifier |
| JOB_ID | VARCHAR | Req identifier — shared across all locale rows for the same req |
| JOB_LOCALE | VARCHAR | Language-site variant this row represents (e.g. `de_DE`, `en_GB`, `en_US`) |
| JOB_LOCATION | VARCHAR | Free-text location string. Format varies by customer — see parsing note below. **Prefer custom fields for structured location (see RB_JOBS_CUSTOM_FIELDS).** |
| COUNTRY | VARCHAR | Country field — **sparse for most customers; check fill rate before using.** |
| CONTINENT | VARCHAR | Continent — sparse, case-inconsistent. |
| STANDARDISED_TIMEZONE | VARCHAR | UTC offset (e.g. `+05:30 UTC`). Good country proxy when COUNTRY is empty. |
| COMPANY | VARCHAR | Operating-company code. First 2 chars are typically the ISO country code (e.g. `IN0025` = India, `DE1464` = Germany). |
| COMPANY_NAME | VARCHAR | Display name of the employing company |
| POSTING_STATUS | VARCHAR | `Posted` or `Not Posted` |
| STATUS | VARCHAR | Job status |
| IS_DELETED | BOOLEAN | Soft-delete flag — always filter `IS_DELETED = FALSE` |
| SITE_TYPE | VARCHAR | `external` (public career site) or `internal` (internal mobility) |
| VISIBILITY_TYPE | VARCHAR | `External`, `Internal`, or `Internal/External` |
| VISIBILITY_LOCALE | ARRAY | Array of locale codes the job is visible to. Flatten with `LATERAL FLATTEN`. Cannot be cast to VARCHAR — use `LATERAL FLATTEN` only. |
| JOB_TITLE | VARCHAR | Job title |
| JOB_CATEGORY | VARCHAR | Job family / category |
| JOB_FAMILY | VARCHAR | Job family (alternative to JOB_CATEGORY) |
| JOB_TYPE | VARCHAR | Employment type |
| JOB_ZONE | VARCHAR | Job zone / level |
| DEPARTMENT | VARCHAR | Department — may embed country tokens for some customers |
| POSTED_DATE | TIMESTAMP_LTZ | When the job was posted |
| CREATED_DATE | TIMESTAMP_LTZ | When the job was created |
| EXPIRY_DATE | TIMESTAMP_LTZ | When the job expires |
| ENABLE_REMOTE | BOOLEAN | Remote work flag |

### Location Parsing Note (JOB_LOCATION)

Format varies by customer. Common pattern: `City, [State,] Country[, ZIP]`.

```sql
-- Extract country from JOB_LOCATION (reverse-split, skip trailing ZIP if numeric)
CASE
  WHEN REGEXP_LIKE(TRIM(SPLIT_PART(JOB_LOCATION, ',', -1)), '.*[0-9].*')
    THEN TRIM(SPLIT_PART(JOB_LOCATION, ',', -2))
  ELSE TRIM(SPLIT_PART(JOB_LOCATION, ',', -1))
END AS country
```

**Prefer `RB_JOBS_CUSTOM_FIELDS` over free-text parsing** when the customer uses ATS custom fields (see below).

### Important caveats

- `RB_JOBS_INFORMATION` exists in schema but is **empty for many customers** — check `COUNT(*)` before using it.
- `RB_JOBS_MULTI_LOCATION` is empty for customers that do not use Phenom's multi-location feature.
- The `VISIBILITY_LOCALE` column is `ARRAY(VARCHAR)` — it cannot be cast directly to string. Use `LATERAL FLATTEN`.

## RB_JOBS_HIRING_TEAM

Recruiter / hiring-manager / interviewer assignments per job. One row per person × job assignment event — contains duplicates (same person can appear multiple times for the same job as events are replayed). Always deduplicate with `GROUP BY ID, JOB_ID` or `QUALIFY ROW_NUMBER()`.

| Column | Type | Description |
| --- | --- | --- |
| JOBS_OBJECT_ID | VARCHAR | Links to RB_JOBS |
| REFNUM | VARCHAR | Customer identifier |
| JOB_ID | VARCHAR | Job identifier |
| ID | VARCHAR | Person identifier (user ID) — use for attribution; join to RB_RECRUITER_ACTIVITY.RECRUITER_USER_ID |
| NAME | VARCHAR | Full name of the person |
| EMAIL_ID | VARCHAR | Email address |
| ROLE | VARCHAR | `Recruiter`, `Hiring Manager`, or `Interviewer` |
| TYPE | VARCHAR | Usually empty string `''` for system users; `'recruiter'` or `'employee'` for external/non-system rows. Filter `COALESCE(TYPE,'') = ''` for the main recruiter universe. |
| CREATED_DATE | TIMESTAMP_LTZ | When this person was added to the hiring team |

### Common query pattern

```sql
-- Distinct (recruiter, job) pairs for a customer — always deduplicate
SELECT DISTINCT ID AS recruiter_id, MAX(NAME) AS name, MAX(EMAIL_ID) AS email, JOB_ID
FROM CID.RAW_SCHEMA.RB_JOBS_HIRING_TEAM
WHERE REFNUM = '{customer}' AND ROLE = 'Recruiter' AND COALESCE(TYPE,'') = ''
  AND ID IS NOT NULL AND ID != ''
GROUP BY ID, JOB_ID
```

## RB_JOBS_CUSTOM_FIELDS

ATS-sourced custom fields per job. **One row per job × FIELD_ID × locale variant.** This is the primary source of structured job metadata for customers that pass ATS custom fields — including location, region, entity, and career-site visibility signals that may be absent from `RB_JOBS` columns.

| Column | Type | Description |
| --- | --- | --- |
| REFNUM | VARCHAR | Customer identifier |
| JOB_ID | VARCHAR | Job identifier |
| FIELD_ID | VARCHAR | Custom field name (customer-defined) |
| FIELD_VALUE | VARCHAR | Custom field value |
| JOB_SEQ_NUM | VARCHAR | Contains locale/site type context for the row |
| CREATED_EVENT_AT | TIMESTAMP_LTZ | Event timestamp |
| UPDATED_EVENT_AT | TIMESTAMP_LTZ | Last update timestamp |

### Location-related FIELD_IDs (Allianz example — REFNUM = 'AISAIPGB')

Different customers use different FIELD_IDs. Always run `SELECT DISTINCT FIELD_ID FROM RB_JOBS_CUSTOM_FIELDS WHERE REFNUM = '{customer}' LIMIT 200` to discover the field map for a new customer.

| FIELD_ID | Description |
| --- | --- |
| `jobCountry` | **Primary country field** — clean country names (e.g. "Germany", "India"). 100% coverage for Allianz. Prefer over free-text parsing of JOB_LOCATION. |
| `countryName` | Display version of country |
| `cityName` | City |
| `state` / `stateName` | State or region |
| `zipCode` | Postal code |
| `custRegion` | Allianz regional cluster: `APAC`, `ROE`, `DEU`, `CEE`, `NA`, `MEA`, `SA` |
| `custOperatingEntity` | Allianz subsidiary name (e.g. "Allianz Australia - P&C", "Allianz Germany") |
| `employingEntity` | Employing legal entity code |
| `postedLocales` | JSON array of career-site locale codes the job is published to |
| `corporatePosting` | `'true'`/`'false'` — whether job is on corporate external career site |
| `intranetPosting` | `'true'`/`'false'` — whether job is on internal mobility site |
| `remote` | Remote/hybrid/on-site flag |

### Query pattern

```sql
-- Get clean country for each unique job (Allianz)
SELECT DISTINCT JOB_ID, FIELD_VALUE AS country
FROM CID.RAW_SCHEMA.RB_JOBS_CUSTOM_FIELDS
WHERE REFNUM = 'AISAIPGB' AND FIELD_ID = 'jobCountry'
  AND NULLIF(TRIM(FIELD_VALUE), '') IS NOT NULL

-- Discover what custom fields a customer has
SELECT FIELD_ID, COUNT(DISTINCT JOB_ID) AS jobs, COUNT(DISTINCT FIELD_VALUE) AS distinct_vals
FROM CID.RAW_SCHEMA.RB_JOBS_CUSTOM_FIELDS
WHERE REFNUM = '{customer}'
GROUP BY FIELD_ID
ORDER BY jobs DESC
LIMIT 100
```

### Performance note

`RB_JOBS_CUSTOM_FIELDS` is very large (179M+ rows for Allianz). Avoid CTEs that join it to other large tables in a single pass. Preferred pattern: filter to a specific `FIELD_ID` first, then join the result to other tables.

## RB_CANDIDATES

Candidate profile information.

| Column | Type | Description |
| --- | --- | --- |
| CANDIDATE_ID | VARCHAR | Unique candidate identifier |
| USER_ID | VARCHAR | Hash-style user ID — joins to RB_APPLICATIONS_DETAILS.USER_ID |

## RB_RECRUITER_ACTIVITY

Domain-level recruiter actions in CRM. One row per recruiter action. Tracks status changes, email, SMS, notes, tags, scheduling actions, rejections, and bulk operations. Does NOT include UI clickstream — see note below.

| Column | Type | Description |
| --- | --- | --- |
| RECRUITER_ACTIVITY_OBJECT_ID | VARCHAR | Primary key — unique activity row identifier |
| REFNUM | VARCHAR | Customer identifier |
| ACTION_TYPE | VARCHAR | Type of recruiter action (see action types below) |
| ACTION_VALUE | VARCHAR | Optional value or detail for the action |
| CREATED_DATE | TIMESTAMP_LTZ | When the action occurred (prefer for filtering/ordering) |
| CREATED_EVENT_AT | TIMESTAMP_LTZ | Event timestamp (alternative to CREATED_DATE) |
| RECRUITER_USER_ID | VARCHAR | Recruiter who performed the action — use for attribution |
| CANDIDATE_ID | VARCHAR | Candidate (hash-style). Joins to RB_APPLICATIONS_DETAILS.USER_ID for same job. |
| JOB_ID | VARCHAR | Job posting. Join with CANDIDATE_ID to link activity to an application. |
| ENTITY_ID | VARCHAR | Often unpopulated — prefer (CANDIDATE_ID, JOB_ID) for application join |
| PREVIOUS_STATUS | VARCHAR | Prior hiring status (for status-change actions) |
| CURRENT_STATUS | VARCHAR | New hiring status (for status-change actions) |

### Action Types

| Category | Values |
| --- | --- |
| Status & Pipeline | `CHANGEDJOBSTATUS` |
| Communication | `SENDEMAIL`, `SENDEMAIL_ANALYTICS`, `SENDSMS`, `EMAIL_OPT_IN`, `SMS_OPT_IN` |
| Notes & Tags | `NOTEADDED`, `TAGADD`, `ATTACHMENTADDED` |
| Scheduling | `SCHEDULEDINTERVIEW`, `UPDATEDINTERVIEWSTATUS` |
| Rejection | `REJECTEDPROFILE` |
| Bulk & Apply | `UPLOADRESUME`, `BULKIMPORT`, `JOBAPPLIEDBYRECRUITER` |
| Feedback | `INTERVIEW_FEEDBACK` |

### Common Joins

```sql
-- Match recruiter activity to applications (same candidate, same job)
JOIN CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS app
  ON CANDIDATE_ID = app.USER_ID
 AND RB_RECRUITER_ACTIVITY.JOB_ID = app.JOB_ID

-- Get customer account name
JOIN CID.SALESFORCE_SCHEMA.ACCOUNT a ON REFNUM = a.REFNUM_C
```

### Coverage Notes

* UI clickstream (e.g. "opened candidate profile", "opened Interviews tab") is in `FACT_CRM_OVERALL_ACTIONS` or `RB_USER_ACTIVITIES` / `RB_USER_ACTIVITY_PAGE_STATES`, not here.
* `FACT_CRM_OVERALL_ACTIONS` uses `RECRUITER_SKEY` as the recruiter identifier, which does NOT directly join to `RECRUITER_USER_ID`. A bridge between SKEY and USER_ID is needed to correlate CRM UI behavior with RB_RECRUITER_ACTIVITY.
* Check % of rows with non-null (CANDIDATE_ID, JOB_ID) to see how much activity can be tied to applications.

## Hiring Pipeline (HIRING_STATUS_VALUE Stages)

Ordered pipeline tracked via `HIRING_STATUS_VALUE` in RB_APPLICATIONS_DETAILS.

| Order | HIRING_STATUS_VALUE | HIRING_STATUS_STEP | Meaning |
| --- | --- | --- | --- |
| 1 | Lead | (none) | Initial status assigned automatically. Ignore for meaningful activity — HIRING_STATUS_PREVIOUS_STEP is NULL. |
| 2 | REVIEW | New Candidate | Application received and ready for recruiter review |
| 3 | SCREEN | Screen / Meets Minimum Qualifications OR Qualify / Meets Preferred Qualifications | Candidate passed initial screen. May have multiple SCREEN steps. |
| 4 | INTERVIEW | Interview | Candidate moved to interview stage. May appear multiple times for multiple rounds. |
| 5 | OFFER | Offer | Offer extended to candidate |
| 6 | HIRED | Ready for Hire | Candidate accepted and marked as hired |
| — | REJECTED | Position filled (or other) | Can occur at any stage. Check REJECTION_REASON for details. |

**Important notes:** Pipeline is NOT strictly linear — candidates can skip stages. REJECTED can appear at any point. Rows in RB_APPLICATIONS_DETAILS can be duplicated — always use `COUNT(DISTINCT HIRING_STATUS_UPDATED_DATE)`.
