# Cross-Pod Join Patterns

Documented join paths and analysis patterns that span multiple pods or require combining pod-specific tables with platform entity tables. This is the highest-value data context document for complex cross-pod queries — the LLM uses these to construct accurate Snowflake queries without hallucinating column names or join keys.

## Counting Interview Rounds

Two approaches exist — they measure different things and give different numbers. Present both when possible.

### Approach 1: Hiring Status Changes (Universal Coverage)

| Attribute | Value |
| --- | --- |
| Table | CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS |
| What it measures | Pipeline stage transitions to INTERVIEW status — how many times candidate was moved to/through Interview status |
| Typical values | ~1.1–1.6 per offered candidate |
| Pro | Available for all candidates. High coverage. |
| Con | Undercounts actual interviews — one status change may represent multiple interview events. |

```sql
SELECT APPLICATION_ID,
    COUNT(DISTINCT HIRING_STATUS_UPDATED_DATE) AS interview_status_changes
FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
WHERE REFNUM = '{customer}' AND HIRING_STATUS_VALUE = 'INTERVIEW'
GROUP BY APPLICATION_ID
```

### Approach 2: Scheduling Requests (More Accurate, Limited Coverage)

| Attribute | Value |
| --- | --- |
| Table | CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST |
| What it measures | Actual interview scheduling events through Phenom scheduling product |
| Typical values | ~1.5–2.2 per offered candidate (where data exists) |
| Pro | Each scheduling request = one interview event. More accurate count. |
| Con | Only covers candidates who used Phenom scheduling. Coverage varies widely (~15% for some customers). |

```sql
SELECT sr.CANDIDATE_ATS_APPLICATION_ID AS APPLICATION_ID,
    COUNT(DISTINCT sr.SCHEDULE_REQUEST_OBJECT_ID) AS scheduled_interviews
FROM CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST sr
WHERE sr.REFNUM = '{customer}'
GROUP BY sr.CANDIDATE_ATS_APPLICATION_ID
```

**Recommendation:** Present both approaches when possible. The gap between them reveals Phenom scheduling adoption rate for the customer.

## Time to Offer / Time to Hire

Standard pattern for calculating time through the hiring funnel for candidates who received an offer.

**Definition:** Time to Offer = days from APPLIED_DATE to first HIRING_STATUS_UPDATED_DATE where HIRING_STATUS_VALUE = 'OFFER'. Scope to candidates who received at least one OFFER.

**Key dimensions:** JOB_CATEGORY, APPLIED_JOB_LOCATION, JOB_ID

```sql
WITH offered_apps AS (
    SELECT DISTINCT APPLICATION_ID
    FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
    WHERE REFNUM = '{customer}' AND JOB_CATEGORY = '{job_family}'
      AND HIRING_STATUS_VALUE = 'OFFER' AND APPLICATION_ID IS NOT NULL
),
app_base AS (
    SELECT d.APPLICATION_ID,
        MIN(d.APPLIED_DATE) AS applied_date,
        MAX(d.APPLIED_JOB_LOCATION) AS job_location
    FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS d
    JOIN offered_apps oa ON d.APPLICATION_ID = oa.APPLICATION_ID
    WHERE d.REFNUM = '{customer}' AND d.JOB_CATEGORY = '{job_family}'
    GROUP BY d.APPLICATION_ID
),
first_offer AS (
    SELECT APPLICATION_ID, MIN(HIRING_STATUS_UPDATED_DATE) AS first_offer_date
    FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS d
    JOIN offered_apps oa USING (APPLICATION_ID)
    WHERE d.REFNUM = '{customer}' AND d.HIRING_STATUS_VALUE = 'OFFER'
    GROUP BY APPLICATION_ID
)
SELECT
    CASE WHEN CONTAINS(ab.job_location, ' > ') THEN SPLIT_PART(ab.job_location, ' > ', 1)
         ELSE TRIM(SPLIT_PART(ab.job_location, ' - ', 1)) END AS country,
    COUNT(*) AS offers,
    ROUND(AVG(DATEDIFF('day', ab.applied_date, fo.first_offer_date)), 1) AS avg_days_to_offer,
    ROUND(MEDIAN(DATEDIFF('day', ab.applied_date, fo.first_offer_date)), 1) AS med_days_to_offer
FROM app_base ab
JOIN first_offer fo ON ab.APPLICATION_ID = fo.APPLICATION_ID
GROUP BY country
ORDER BY offers DESC
```

**Notes:** Filter to offered candidates first, then look backward at their journey. Use LEFT JOIN for screen/interview CTEs, INNER JOIN for offer CTE. Negative days_to_offer values indicate data quality issues.

## Application → Interview Scheduling Join

Links an application to its scheduled interviews via Phenom scheduling. Coverage varies by customer (~15% for some).

```sql
JOIN CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST sr
  ON app.APPLICATION_ID = sr.CANDIDATE_ATS_APPLICATION_ID
-- Result: one row per scheduling request linked to this application
```

## Application → Screening Join

Links an application to its video screening assessment. Requires both USER_ID and JOB_ID to match. Coverage can be very low for some job families.

```sql
JOIN CID.RAW_SCHEMA.RB_VIDEO_SCREENS vs
  ON app.USER_ID = vs.VIDEOSCREENCANDIDATE_CANDIDATEID
 AND app.JOB_ID = vs.INTERVIEWDETAILS_ENTITYVALUE
-- Note: ATS_ID does NOT match RB_VIDEO_SCREENS candidate ID — use USER_ID instead
```

## Scheduling WoW Trend by Customer

Standard pattern for week-over-week scheduling volume analysis with customer segmentation:

```sql
SELECT
    a.NAME AS account_name,
    DATE_TRUNC('week', sr.CREATED_DATE) AS week,
    COUNT(DISTINCT sr.SCHEDULE_REQUEST_OBJECT_ID) AS scheduling_requests
FROM CID.RAW_SCHEMA.RB_SCHEDULING_SCHEDULE_REQUEST sr
JOIN CID.SALESFORCE_SCHEMA.ACCOUNT a ON sr.REFNUM = a.REFNUM_C
WHERE sr.CREATED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
GROUP BY 1, 2
ORDER BY 1, 2
```

## Job Activity: Is a Job Active?

Three approaches for determining if a job has meaningful activity. Use alone or combine.

### Approach 1: Application Count

Job has N+ applications created in a time period.

```sql
SELECT JOB_ID, REFNUM, COUNT(DISTINCT APPLICATION_ID) AS app_count
FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
WHERE REFNUM = '{customer}' AND APPLIED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
GROUP BY JOB_ID, REFNUM
HAVING app_count >= 1
```

### Approach 2: Hiring Status Changes

Job has N+ hiring status changes (recruiter/candidate activity beyond apply).

```sql
SELECT JOB_ID, REFNUM, COUNT(*) AS status_change_count
FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
WHERE REFNUM = '{customer}' AND HIRING_STATUS_UPDATED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
GROUP BY JOB_ID, REFNUM
HAVING status_change_count >= 1
```

### Approach 3: Meaningful Status Changes Only

Exclude the initial LEAD status assigned at apply time — only count recruiter-driven pipeline movement.

```sql
SELECT JOB_ID, REFNUM, COUNT(*) AS meaningful_change_count
FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
WHERE REFNUM = '{customer}'
  AND HIRING_STATUS_UPDATED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
  AND COALESCE(HIRING_STATUS_STEP, '') != 'LEAD'
  AND HIRING_STATUS_PREVIOUS_STEP IS NOT NULL
GROUP BY JOB_ID, REFNUM
HAVING meaningful_change_count >= 1
```

### Combined (recommended)

```sql
WITH active_by_apps AS (
  SELECT JOB_ID, REFNUM FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
  WHERE REFNUM = '{customer}' AND APPLIED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
  GROUP BY JOB_ID, REFNUM HAVING COUNT(DISTINCT APPLICATION_ID) >= 1
),
active_by_changes AS (
  SELECT JOB_ID, REFNUM FROM CID.RAW_SCHEMA.RB_APPLICATIONS_DETAILS
  WHERE REFNUM = '{customer}' AND HIRING_STATUS_UPDATED_DATE >= DATEADD('MONTH', -3, CURRENT_DATE())
    AND COALESCE(HIRING_STATUS_STEP, '') != 'LEAD' AND HIRING_STATUS_PREVIOUS_STEP IS NOT NULL
  GROUP BY JOB_ID, REFNUM HAVING COUNT(*) >= 1
)
SELECT DISTINCT JOB_ID, REFNUM FROM active_by_apps
UNION
SELECT DISTINCT JOB_ID, REFNUM FROM active_by_changes
```

**Note:** `RB_APPLICATIONS_DETAILS` has both `APPLIED_DATE` and `HIRING_STATUS_UPDATED_DATE` — one table covers both application counts and status change analysis.

## Job Country / Location Lookup

### Approach 1: ATS Custom Fields (preferred when available)

Customers that sync ATS custom fields expose structured location data in `RB_JOBS_CUSTOM_FIELDS`. No parsing required. Always check what `FIELD_ID`s a customer has before defaulting to free-text.

```sql
-- Discover location-related custom fields for a customer
SELECT FIELD_ID, COUNT(DISTINCT JOB_ID) AS jobs, COUNT(DISTINCT FIELD_VALUE) AS vals
FROM CID.RAW_SCHEMA.RB_JOBS_CUSTOM_FIELDS
WHERE REFNUM = '{customer}'
  AND (LOWER(FIELD_ID) LIKE '%countr%' OR LOWER(FIELD_ID) LIKE '%locat%'
    OR LOWER(FIELD_ID) LIKE '%city%' OR LOWER(FIELD_ID) LIKE '%region%'
    OR LOWER(FIELD_ID) LIKE '%entity%' OR LOWER(FIELD_ID) LIKE '%site%')
GROUP BY FIELD_ID ORDER BY jobs DESC

-- Get clean country per job (example: Allianz uses FIELD_ID = 'jobCountry')
SELECT DISTINCT JOB_ID, FIELD_VALUE AS country
FROM CID.RAW_SCHEMA.RB_JOBS_CUSTOM_FIELDS
WHERE REFNUM = '{customer}' AND FIELD_ID = 'jobCountry'
  AND NULLIF(TRIM(FIELD_VALUE), '') IS NOT NULL
```

**Allianz (AISAIPGB) field map:** `jobCountry`, `cityName`, `state`, `zipCode`, `custRegion` (APAC/ROE/DEU/CEE/NA/MEA/SA), `custOperatingEntity` (subsidiary name), `postedLocales` (JSON array of career-site locale codes), `corporatePosting`, `intranetPosting`, `remote`.

**Performance:** Filter to a specific `FIELD_ID` first — the table is very large (179M+ rows for Allianz). Avoid joining it to other large tables inside a CTE.

### Approach 2: RB_JOBS.JOB_LOCATION free-text parsing (fallback)

Use when custom fields are not populated. Format is `City, [State,] Country[, ZIP]`. See `core-entities.md > RB_JOBS > Location Parsing Note` for the CASE expression.

### Approach 3: RB_JOBS.COMPANY prefix

The `COMPANY` code's first 2 chars are the ISO country code for most customers (e.g. `IN0025` = India, `DE1464` = Germany, `FR1741` = France, `GB0281` = UK). Fast and ~99% populated, but requires knowing the convention holds for the customer.

### Which approach to use

| Situation | Use |
| --- | --- |
| Customer has `jobCountry` or similar custom field | Custom fields (Approach 1) |
| Custom fields empty / not available | JOB_LOCATION parsing (Approach 2) |
| Need a quick proxy without parsing | COMPANY prefix (Approach 3) |
| Need multiple location dimensions (city, state, region, entity) | Custom fields always win |

### Tables to avoid

- `RB_JOBS.COUNTRY` — sparse for most customers (12.8% for Allianz). Check fill rate before using.
- `RB_JOBS_INFORMATION` — rich schema but **empty for many customers** (confirmed empty for Allianz). Always `COUNT(*)` before using.
- `RB_JOBS_MULTI_LOCATION` — only populated for customers using Phenom's multi-location feature. Empty for most.

---

## Recruiter → Job Country Cross-Reference

Pattern for analysing how many countries a recruiter covers, or which recruiters span multiple countries.

```sql
-- Step 1: get distinct (recruiter, job) pairs for currently-posted jobs
WITH recruiter_jobs AS (
  SELECT DISTINCT ht.ID AS recruiter_id,
    MAX(ht.NAME) AS name,
    MAX(ht.EMAIL_ID) AS email,
    ht.JOB_ID
  FROM CID.RAW_SCHEMA.RB_JOBS_HIRING_TEAM ht
  JOIN CID.RAW_SCHEMA.RB_JOBS j ON ht.JOB_ID = j.JOB_ID AND j.REFNUM = ht.REFNUM
  WHERE ht.REFNUM = '{customer}'
    AND ht.ROLE = 'Recruiter'
    AND COALESCE(ht.TYPE, '') = ''     -- exclude external/agency rows
    AND ht.ID IS NOT NULL AND ht.ID != ''
    AND j.IS_DELETED = FALSE
    AND j.POSTING_STATUS = 'Posted'    -- scope to live jobs only
  GROUP BY ht.ID, ht.JOB_ID
),
-- Step 2: join to country — use custom fields when available (faster than parsing JOB_LOCATION)
recruiter_country AS (
  SELECT rj.recruiter_id, MAX(rj.name) AS name, MAX(rj.email) AS email,
    COUNT(DISTINCT rj.JOB_ID) AS posted_jobs,
    COUNT(DISTINCT cf.FIELD_VALUE) AS countries
  FROM recruiter_jobs rj
  JOIN CID.RAW_SCHEMA.RB_JOBS_CUSTOM_FIELDS cf
    ON rj.JOB_ID = cf.JOB_ID AND cf.REFNUM = '{customer}'
    AND cf.FIELD_ID = 'jobCountry'    -- adjust FIELD_ID per customer
    AND NULLIF(TRIM(cf.FIELD_VALUE), '') IS NOT NULL
  GROUP BY rj.recruiter_id
)
SELECT countries, COUNT(*) AS recruiters
FROM recruiter_country
GROUP BY countries ORDER BY countries
```

**Performance note:** The 3-way join (hiring team × jobs × custom fields) on the full table can time out. The pattern above is faster because Step 1 pre-filters hiring team + jobs first, then the Step 2 join hits a much smaller row set. Do not combine all three tables in a single CTE without pre-filtering.

**Interpretation note:** Recruiters with very high country counts (14+) often reflect an org configuration pattern where a shared TA/HR-Ops pool is added en-bloc to every global req — not individual sourcing breadth. Validate with CSM before citing as product engagement depth.

---

## Job Locale / Career-Site Visibility

Pattern for understanding which career sites or language sites a job is published on.

```sql
-- Which locale-sites does a job appear on? (Allianz: each job has 20-24 JOB_LOCALE rows)
SELECT JOB_ID, JOB_LOCALE, SITE_TYPE, VISIBILITY_TYPE
FROM CID.RAW_SCHEMA.RB_JOBS
WHERE REFNUM = '{customer}' AND JOB_ID = '{job_id}' AND IS_DELETED = FALSE

-- Flatten VISIBILITY_LOCALE array (locale codes the job is visible to)
SELECT j.JOB_ID, f.value::string AS visible_to_locale
FROM CID.RAW_SCHEMA.RB_JOBS j,
  LATERAL FLATTEN(input => j.VISIBILITY_LOCALE) f
WHERE j.REFNUM = '{customer}' AND j.IS_DELETED = FALSE
-- Note: VISIBILITY_LOCALE is ARRAY(VARCHAR) — cannot cast directly; LATERAL FLATTEN only.

-- Career-site type breakdown per customer
SELECT SITE_TYPE, VISIBILITY_TYPE, COUNT(DISTINCT JOB_ID) AS jobs
FROM CID.RAW_SCHEMA.RB_JOBS
WHERE REFNUM = '{customer}' AND IS_DELETED = FALSE AND POSTING_STATUS = 'Posted'
GROUP BY 1, 2 ORDER BY 3 DESC
```

**Allianz pattern:** All 2,655 currently-posted reqs are published in 20–24 language variants each. `SITE_TYPE = 'external'` covers 9,722 unique jobs; `'internal'` covers 1,877. The `postedLocales` custom field (JSON array) is Allianz's own record of which career-site locale codes a job is published to.

## Adding New Patterns

When you discover a reliable cross-pod join pattern, document it here with: the two tables being joined, the join key, coverage notes, and a query example.
