-- CRM_EVENTS distinct-user trends
-- Metric: COUNT(DISTINCT EMAIL)  (users, not jobs)
-- Filters: PHENOM_REFNUM = CRM_EVENTS, STATUS_C = Customer, exclude %phenom% emails
-- Run in Snowsight on account that has CID.RAW_SCHEMA access

-- ---------------------------------------------------------------------------
-- A) Rolling windows: last 1 week / last 6 weeks / last 1 year
-- ---------------------------------------------------------------------------
WITH filtered AS (
  SELECT A.EMAIL, A.TIME_STAMP AS ts
  FROM CID.RAW_SCHEMA.BEACON_CLICK_STREAM_DATA A
  JOIN CID.RAW_SCHEMA.DIM_CUSTOMER_INFO_SF_LOOKER B
    ON A.REFNUM = B.REFNUM
  WHERE A.PHENOM_REFNUM = 'CRM_EVENTS'
    AND A.TIME_STAMP >= DATEADD('year', -1, CURRENT_DATE())
    AND A.EMAIL IS NOT NULL
    AND A.EMAIL NOT ILIKE '%phenom%'
    AND B.STATUS_C = 'Customer'
)
SELECT period, users, users_thousands
FROM (
  SELECT
    'last_1_week' AS period,
    1 AS sort_key,
    COUNT(DISTINCT EMAIL) AS users,
    ROUND(COUNT(DISTINCT EMAIL) / 1000.0, 2) AS users_thousands
  FROM filtered
  WHERE ts >= DATEADD('week', -1, CURRENT_TIMESTAMP())

  UNION ALL

  SELECT
    'last_6_weeks',
    2,
    COUNT(DISTINCT EMAIL),
    ROUND(COUNT(DISTINCT EMAIL) / 1000.0, 2)
  FROM filtered
  WHERE ts >= DATEADD('week', -6, CURRENT_TIMESTAMP())

  UNION ALL

  SELECT
    'last_1_year',
    3,
    COUNT(DISTINCT EMAIL),
    ROUND(COUNT(DISTINCT EMAIL) / 1000.0, 2)
  FROM filtered
)
ORDER BY sort_key;

-- ---------------------------------------------------------------------------
-- B) Weekly trend — last 6 weeks (good for a line chart)
-- ---------------------------------------------------------------------------
SELECT
  DATE_TRUNC('week', A.TIME_STAMP)::DATE AS week_start,
  COUNT(DISTINCT A.EMAIL) AS users,
  ROUND(COUNT(DISTINCT A.EMAIL) / 1000.0, 2) AS users_thousands
FROM CID.RAW_SCHEMA.BEACON_CLICK_STREAM_DATA A
JOIN CID.RAW_SCHEMA.DIM_CUSTOMER_INFO_SF_LOOKER B
  ON A.REFNUM = B.REFNUM
WHERE A.PHENOM_REFNUM = 'CRM_EVENTS'
  AND A.TIME_STAMP >= DATEADD('week', -6, DATE_TRUNC('week', CURRENT_DATE()))
  AND A.TIME_STAMP < DATEADD('week', 1, DATE_TRUNC('week', CURRENT_DATE()))
  AND A.EMAIL IS NOT NULL
  AND A.EMAIL NOT ILIKE '%phenom%'
  AND B.STATUS_C = 'Customer'
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------------
-- C) Weekly trend — last 1 year
-- ---------------------------------------------------------------------------
SELECT
  DATE_TRUNC('week', A.TIME_STAMP)::DATE AS week_start,
  COUNT(DISTINCT A.EMAIL) AS users,
  ROUND(COUNT(DISTINCT A.EMAIL) / 1000.0, 2) AS users_thousands
FROM CID.RAW_SCHEMA.BEACON_CLICK_STREAM_DATA A
JOIN CID.RAW_SCHEMA.DIM_CUSTOMER_INFO_SF_LOOKER B
  ON A.REFNUM = B.REFNUM
WHERE A.PHENOM_REFNUM = 'CRM_EVENTS'
  AND A.TIME_STAMP >= DATEADD('year', -1, CURRENT_DATE())
  AND A.EMAIL IS NOT NULL
  AND A.EMAIL NOT ILIKE '%phenom%'
  AND B.STATUS_C = 'Customer'
GROUP BY 1
ORDER BY 1;

-- ---------------------------------------------------------------------------
-- Optional: monthly trend for calendar 2026 (closer to your original shape,
-- but users instead of jobs)
-- ---------------------------------------------------------------------------
SELECT
  DATE_TRUNC('month', A.TIME_STAMP)::DATE AS month_start,
  A.REFNUM,
  B.CUSTOMER_TIER_SF,
  COUNT(DISTINCT A.EMAIL) AS users,
  ROUND(COUNT(DISTINCT A.EMAIL) / 1000.0, 2) AS users_thousands
FROM CID.RAW_SCHEMA.BEACON_CLICK_STREAM_DATA A
JOIN CID.RAW_SCHEMA.DIM_CUSTOMER_INFO_SF_LOOKER B
  ON A.REFNUM = B.REFNUM
WHERE A.PHENOM_REFNUM = 'CRM_EVENTS'
  AND YEAR(A.TIME_STAMP) = 2026
  AND A.EMAIL IS NOT NULL
  AND A.EMAIL NOT ILIKE '%phenom%'
  AND B.STATUS_C = 'Customer'
GROUP BY 1, 2, 3
HAVING COUNT(DISTINCT A.EMAIL) > 0
ORDER BY 1, 2;
