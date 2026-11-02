# Phenom Knowledge Framework — INDEX

A code-grounded knowledge base for answering questions about the Phenom application
**from real source code**, without hallucinating. It grows one product **area** at a time
and will eventually cover the entire Phenom stack.

## The 3-file convention (per area)

Each area lives in `phenom-knowledge/<area>/` with exactly three files:

| File | Purpose | Format |
|---|---|---|
| `routing.yaml` | **Navigate** — map an intent/question to the exact `repo/path:line` of the procedure, method, or endpoint. | YAML |
| `skill.md` | **Answer** — capability catalog + grounding contract (how to answer from code, never guess) + cross-area notes. | Markdown |
| `graph.json` | **Connect the dots** — nodes (repos, services, components, topics, stores, external systems) + edges (calls/consumes/produces/executes) for token-cheap traversal. | JSON |

### How to use when answering a question
1. Open `skill.md` for the area to understand scope and the grounding rules.
2. Use `routing.yaml` `intents:`/`action_catalog:` to jump to the exact code.
3. Use `graph.json` to trace cross-component/cross-repo flows.
4. **Cite `repo/path:line`.** If it isn't in the cloned code, say so — do not guess.
5. If a question spans multiple repos/areas, answer per repo-area path and list all.

### Provenance markers (in routing.yaml)
- `verified` — line read directly this session.
- `report` — read by a sub-agent pass; re-open to confirm exact line before quoting.
- `grounded: false` — referenced but source **not** cloned (e.g. shared libs). Never assert internals.

### Clone location
Source repos are shallow-cloned under:
`/Users/venkata.gonella/phenom_repo/MyLocalCRM/repos/<repo>`

---

## Area status

| Area | Status | Files | Notes |
|---|---|---|---|
| **Automations** | ✅ Built | `automations/{routing.yaml, skill.md, graph.json}` | 5 product repos analyzed from code. |
| **Messaging** | ✅ Built | `messaging/{routing.yaml, skill.md, graph.json}` | 8 repos (5 UI MFEs + platform monolith + lists + storm). |
| **Screening** | ✅ Built (partial) | `screening/{routing.yaml, skill.md, graph.json}` | Only `crm-video-assessment` accessible (ODVA lifecycle). Video capture/AI scoring + X+/Fitscore/Questionnaires not cloned. |
| **Analytics** | ✅ Built (partial) | `analytics/{routing.yaml, skill.md, graph.json}` | 3 repos (dashboard-service + 2 UIs). Snowflake analytics-pro KPI backend not cloned. |
| **Scheduling** | ⛔ Blocked (access) | — | No accessible repos with current SSH key. |

---

## Repo inventory by area

> Access status is from `git ls-remote` probes in prior sessions + this session's clones.
> "accessible" = SSH reachable. "cloned" = present under `MyLocalCRM/repos/`.

### Automations  — BUILT
| Repo | Language | Role | Status |
|---|---|---|---|
| `crm-automations-ui` | Angular 16 | Recipe builder UI (MFE `crmAutomations`) | cloned, analyzed |
| `crm-automation-service` | Java/Spring | Recipe CRUD, templates, analytics, metadata, jobs, Temporal actions | cloned, analyzed |
| `automation-search-service` | Java/Spring | Trigger→recipe matching (Lucene+ES+validate) | cloned, analyzed |
| `candidate-automation` | Java/Storm | Action execution engine (24 actions) | cloned, analyzed |
| `crm-workflows` | Java/Spring | LinkedIn CRM Connect integration (misnamed) | cloned, analyzed |
| `crm-automation` | Python/Robot/Playwright | **QA test automation — NOT product** | cloned, excluded |

### Messaging — BUILT
| Repo | Language | Role | Status |
|---|---|---|---|
| `crm-campaigns-ui` | Angular MFE | Campaign builder (email/SMS/WhatsApp), subscriptions | cloned (`development` branch), analyzed |
| `crm-templates-ui` | Angular MFE | Email/SMS template editor | cloned (`development` branch), analyzed |
| `crm-lists-ui` | Angular MFE | Lists + talent communities | cloned, analyzed |
| `crm-inbox-fe` | Angular MFE | Inbox/conversations, WhatsApp, Twilio voice | cloned, analyzed |
| `crm-notes-ui` | Angular MFE | Candidate notes | cloned, analyzed |
| `crm-messaging-platform` | Java (multi-module) | Backend: MGW gateway, email facade/api/analytics, text(SMS) api, campaign svcs | cloned, analyzed |
| `crm-candidate-lists` | Java (Play) | Lists backend | cloned, analyzed |
| `storm-campaign` | Java (Storm) | Campaign execution engine | cloned, analyzed |
> Not cloned: `notes-api` backend. Gateway prefix→module mapping (`/ecampaign`,`/sms-service`,`/messaging-campaign-service`) unverified.

### Screening — BUILT (partial)
| Repo | Language | Role | Status |
|---|---|---|---|
| `crm-video-assessment` | Java (Spring + Kafka Streams) | ODVA config, status lifecycle, notifications | cloned, analyzed |
> Not accessible/cloned: video capture + AI scoring (MCS/video hub), `crm-screening`, Fitscore,
> Questionnaires, Screening Agent. `INITIATE_SCREENING`/`SEND_ODVA` automations interact here.

### Analytics — BUILT (partial)
| Repo | Language | Role | Status |
|---|---|---|---|
| `crm-dashboard-service` | Java (Spring) | Recruiter dashboard backend (widgets; ES + Mongo userPreference) | cloned, analyzed |
| `crm-recruiter-dashboard` | Angular MFE | Recruiter dashboard UI (1:1 with dashboard-service) | cloned, analyzed |
| `crm-job-analytics` | Angular MFE | Job KPIs UI (calls Snowflake analytics-pro + facets2/ecampaign) | cloned, analyzed |
> Not accessible: `analytics-pro-ui-webpack`, `analytics-spring-boot-services` (Snowflake KPI backend),
> `custom-report-builder`, `analytics-helm-charts`.

### Scheduling — BLOCKED (access)
No `scheduling-*` repo was SSH-accessible with the current key. Documented primary MFE:
`scheduling-pluggable-frontend`; Jira `DEVOPS2-36927` lists many scheduling repos.
> Note: automation `INVITE_FOR_INTERVIEW` calls into this area via
> `crm-automation-service` Temporal `InviteForInterviewActivity`.

---

## Known cross-area seams (already visible from Automations)
- **Automations → Messaging**: send email/SMS/WhatsApp, add/opt-out campaign (via ecampaign/sms-service).
- **Automations → Screening**: initiate screening, send ODVA, forward video assessment.
- **Automations → Scheduling**: invite for interview.
- **Automations → Analytics**: automation ROI / time-saved metrics (`AnalyticsController`).

These seams are recorded in `automations/graph.json → cross_area_pointers` so future areas
link up cleanly.

---

## Pending / to fill in later
- Obtain access to Scheduling repos, then build its 3 files (only area still unbuilt).
- Deepen the partial areas: clone Screening's video-capture/AI-scoring + X+/Fitscore/Questionnaire
  repos, and Analytics' Snowflake KPI backend (`analytics-spring-boot-services`).
- Verify Messaging gateway prefix→module mapping and clone `notes-api`.
- Clone the shared library `phenompeople-crm-common` (`com.phenompeople.crm`) to ground
  trigger fan-out (`CRMAutomationUtils`), `TaskQueueConstants`, `TemporalClient`.
- Re-verify `report`-provenance line numbers in Automations before quoting them verbatim.
