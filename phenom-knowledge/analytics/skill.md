# Skill: Phenom CRM Analytics

> **Area:** Analytics — Recruiter Dashboard widgets + Job Analytics KPIs.
> **Companion files:** `routing.yaml`, `graph.json`. **Framework/contract:** `../INDEX.md`.

---

## GROUNDING CONTRACT (read first)
1. Answer only from code; cite `repo/path:line`.
2. Three repos cloned: `crm-dashboard-service` (backend), `crm-recruiter-dashboard` (UI),
   `crm-job-analytics` (UI). The **Snowflake analytics-pro backend** that computes job KPIs is
   **NOT cloned** — do not assert its internals; say "not available in cloned Analytics repos."
3. Multiple matches → list all repo-area paths.
4. Provenance: `verified` (backend controllers/endpoints read this session) vs `report` (UI services, sub-agent pass).

---

## WHAT THIS AREA IS
Two distinct analytics surfaces:

### 1. Recruiter Dashboard (`crm-recruiter-dashboard` UI → `crm-dashboard-service` backend)
Widget-based recruiter home. The UI `DashboardService` (`dashboard.service.ts:12`, base
`{crmHub}/dashboard-service/`) is a **1:1 bridge** to the backend's 9 business endpoints:

| Widget / capability | Backend endpoint | at |
|---|---|---|
| Overview / account-level | `GET /overview`, `GET /account-level` | `OverviewController.java:50,71` |
| New leads | `GET /new-leads/data` | `NewLeadsController.java:41` |
| New applicants | `GET /new-applicants/data` | `NewApplicantsController.java:42` |
| My jobs | `POST /myJobs` | `MyJobsWidgetController.java:28` |
| Recent activity | `GET /dashboard/recent-activity/{userId}` | `RecentActivityController.java:46` |
| Discover | `POST /discover` | `DiscoverWidgetController.java:41` |
| Widget ordering / persona | `GET /persona`, `GET /widget-order/{recruiterUserId}` | `WidgetOrderingController.java:38,52` |
| Widget done | `POST /{widgetType}/done` | `WidgetDoneRequestController.java:33` |

Backend data comes from **Elasticsearch (multi-index)** + **Mongo `userPreference` DB** (widget
order/persona) + upstream **list-service** and **email-facade-service**. It consumes Kafka
`crm.recent.activity.topic`. **No direct Snowflake/SQL** in this service.

### 2. Job Analytics (`crm-job-analytics` UI → Snowflake analytics-pro)
Job-level KPIs/funnel. `JobAnalyticsService` calls a **separate Snowflake analytics-pro backend**
(`qa-snowflake-analyticspro.phenompro.com`, GET KPI endpoints) plus CRM Hub `facets2/` and
`ecampaign/` (POST) for candidate/campaign data. **It does NOT call `crm-dashboard-service`.**
The KPI computation backend is not cloned.

---

## MFE
Both Angular repos are **Module Federation remotes** (no `remotes:{}` host block):
- `crm-recruiter-dashboard` → remote `recruiter-dashboard`, exposes `./RecruiterDashboard`.
- `crm-job-analytics` → remote `job-analytics`, exposes `./JobAnalyticsPageComponent`.

---

## CROSS-AREA
- **Analytics ↔ Messaging**: `crm-dashboard-service` pulls from `email-facade-service`;
  `crm-job-analytics` calls `ecampaign/` (Messaging area).
- **Automations analytics are elsewhere**: automation ROI / time-saved metrics live in
  `crm-automation-service AnalyticsController` (see `../automations`), **not** in this area.

## KNOWN GAPS / CAVEATS
- **Snowflake analytics-pro backend not cloned** (`analytics-pro-ui-webpack`,
  `analytics-spring-boot-services`, `custom-report-builder`, `analytics-helm-charts` not
  accessible). Job-analytics KPI internals are not grounded.
- UI service line numbers are `report` provenance; backend endpoints are `verified`.
- `crm-dashboard-service` uses ES as the analytics store, not a data warehouse.
