---
name: screening
type: index
description: "Domain index for Screening repos — screening questions/flows, assessment integrations"
pillar: Product Experiences
last_reviewed: 2026-07-27
---

# Screening

## Scope

Everything before a candidate is scheduled for an interview:
- Screening questions, flows, knockout logic, routing
- Assessment integrations (third-party assessment providers, scoring)

Not in scope:
- Campaigns / candidate nurture (→ Candidate Engagement — `index/product-experiences/candidate-engagement.md`)
- Interview scheduling or evaluation (→ Interview Management)
- Recruiter-facing configuration UI that just hosts screening features (→ Recruiter Hub)

## Repo manifests

**Use [`index/repos/screening/capability-index.md`](../repos/screening/capability-index.md) before grepping `repos/product-experiences/screening/`.** All 6 cloned repos have a curated manifest under `index/repos/screening/` — purpose, capabilities, entry points, integrations, and search hints per repo, plus the branch checked out for each (all six have an empty `master`/`main`).

## Key repos

See `index/repo-catalog.md` for full stack/status/"also used by" detail.

### Assessment integrations (video assessment + transcription)

| Repo | Purpose | Start here |
|------|---------|------------|
| `assessment-management-service` | Core assessment CRUD — create assessments, look up by candidate/job/email, configured-assessments per job | `app/com/phenompeople/controllers/AssessmentController.java` |
| `assessment-streaming-service` | Normalizes and streams assessment results from third-party providers (eSkill, Talogy, Buplas, Otomeyt) via Kafka | `app/com/phenom/assessmentstreaming/services/kafka/AssessmentStatusUpdateEventsListener.java` |
| `video-hub` | **Start here for video assessment questions** — API gateway/auth-proxy in front of the video assessment services | `app/com/phenompeople/videohub/controllers/ApiController.java` |
| `video-assessment-ats` | Processes video assessment events, syncs results into the ATS/CRM by job application ID | `app/.../controllers/TestController.java` (`processVideoAssessmentEvents`) |
| `video-assessment-gdpr` | Candidate-facing video assessment info API **plus** privacy/compliance (scheduled auto-purge, compliance events, migration, S3/Mongo utilities) — naming undersells its scope, see manifest | `app/.../controllers/VideoAssessmentController.java` (`assessmentInfoByCandidateId`), `GdprTestController.java` |
| `odva-transcription-app` | Transcribes video/audio assessment recordings — AWS Transcribe (established) + AssemblyAI (in progress on current branch); publishes via Kafka/SQS, stores in MongoDB/S3 | `src/main/java/com/phenom/transcription/services/TranscribeJob.java`, `AssemblyAiOrchestrationService.java` |

**Note:** all six have an empty `master`/`main` (real code lives on feature/release branches). Each is checked out locally to its most-recently-updated branch — see `index/repo-catalog.md` for exact branch names and dates, and re-check `git branch -r` periodically since `sync-repos.sh` won't auto-advance to a newer branch on its own.

**Suggested feasibility flow for video assessment questions:** `video-hub` (entry/auth) → `video-assessment-ats` (event processing / ATS sync) → `assessment-streaming-service` or `assessment-management-service` (assessment data) → `odva-transcription-app` (if transcript/content is involved) → `video-assessment-gdpr` (if retention/consent is involved).

## Common feasibility patterns

- **New screening question type** → check this pillar's flow/question-config code first, then Recruiter Hub for where it's configured in the UI.
- **Auto-advance/auto-reject on screening result** → Platform → Automations owns the trigger logic; this pillar owns the score/result event.
- **Notify candidate or recruiter on screening completion** → Platform → Messaging.
- **New assessment provider integration** → check for an existing provider adapter pattern before assuming greenfield work.
- **Roles / permissions / tenant entitlements / who can view or modify a questionnaire** → **`index/cross-cutting/access-control.md`** — Screening is audited, don't re-scan code.

## Access control (audited 2026-07-27)

Full detail and the Interview Intelligence comparison in [`index/cross-cutting/access-control.md`](../cross-cutting/access-control.md). Short version:

- **`video-hub` is the only repo in this pillar that authorizes anything.** The other five have no authorization code and are assumed reachable only through it — that assumption is the first thing to confirm with the team.
- It calls central **User Management** through the *same* mechanism as Interview Management: Redis DDO `validateAuthLoginToken`, headers `Authorization` + `PhenomSource: VX`, payload `{ applicationName }`.
- **It enforces tenant entitlements, which II does not** — `entitlements[]` must contain `ALL` or the request `refNum`, and `childRefnums[]` gets narrowed to entitled tenants. This is the strongest per-user check found in either product.
- Permissions are typed (`ODVAEntityPermissions`: `view`/`modify`/`duplicate` × `My`/`All` Questionnaires) and arrive on the token prefixed `ODVA_`. `video-hub` also handles the `II_` prefix — **it fronts both products**.
- **Zero access-control data in Mongo**, and **no departmentalization anywhere** in the pillar (no `crm-commons` in any build file).
- Enforcement is edge-only; `ApiService` writes permissions into the API response, so the allow/deny decision is handed to the calling UI.

## Mongo estate (Screening)

Separate from Interview Management's. All five Play services share **one** DB — `mongo.db` = `mongo_ngcc_dev` in dev (confirm the prod name). `odva-transcription-app` is Spring Boot with three URIs (`default`, `offline`, `vxim`). ⚠️ The `conf/*.conf` files contain plaintext non-prod credentials; don't lift config snippets from these repos.

## Platform dependencies

- **Automations** — auto-advance/reject rules triggered by screening outcomes
- **Messaging** — completion notifications, reminders
- **Recruiter Hub** — screening setup/config UI, results shown on candidate profile
- **Privacy & Compliance** — assessment data retention, candidate consent for screening

## Eng contacts

_Fill in once known — team name, PM, Slack channel._
