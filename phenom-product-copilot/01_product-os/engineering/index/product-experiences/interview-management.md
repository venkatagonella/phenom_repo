---
name: interview-management
type: index
description: "Domain index for Interview Management repos — scheduling, structured interviews, Interview Intelligence"
pillar: Product Experiences
last_reviewed: 2026-07-27
---

# Interview Management

## Scope

Everything from "candidate passed screening" through "interview is evaluated":
- Interview scheduling (calendar integration, availability, invites, timezone handling, rescheduling)
- Structured interviews (interview guides, scorecards, evaluation forms)
- Interview Intelligence (recording, transcription, conversation intelligence, debrief summaries)

Not in scope: pre-interview screening (→ Screening), recruiter-facing interview list/pipeline views that just surface this data (→ Recruiter Hub).

## Key repos

See `index/repo-catalog.md` for full stack/status/"also used by" detail. Curated per-repo manifests + a reverse capability index (all 12 repos) are at [`index/repos/interview-management/capability-index.md`](../repos/interview-management/capability-index.md) — use that before grepping code.

### Scheduling (Bitbucket project: SCHEDULING)

| Repo | Purpose | Start here |
|------|---------|------------|
| `scheduling-main-app` | Core scheduling app — schedule requests, event scheduling, invites, webhooks, Temporal worker activities | `SchedulingApplication.java`, `controller/SchedulesController.java`, `controller/eventscheduling/EventSchedulingController.java` |
| `phenom-internal-calendar` | Calendar & availability — slot generation, conference rooms, scheduling teams | `CalendarApplication.java`, `controllers/SlotGenerationController.java` |
| `scheduling-orchestration` | Temporal workflow orchestration — schedule execution, bulk signals, workflow config | `SchedulingOrchestrationApplication.java`, `controller/WorkflowExecutionController.java` |
| `scheduling-rule-parser` | RRule / recurrence parsing for scheduling patterns | `controllers/rules_controller.py` (`POST /rules`) |
| `scheduling-messaging-service` | Scheduling notifications — **confirmed stub** (2 files, `README.md` only, no code); actual trigger logic lives in `scheduling-main-app` (`NotificationController`) | `README.md` only — do not scan |
| `scheduling-meeting-links` | Legacy meeting links — **confirmed stale stub** (2022, `.gitignore` only); superseded by `scheduling-main-app` (`MeetingLinkController`, `LiveLinkController`) | Do not scan |

**Suggested feasibility flow for scheduling questions:** `scheduling-main-app` (business logic + API) → `phenom-internal-calendar` (availability/slots) → `scheduling-orchestration` (workflow execution) → `scheduling-rule-parser` (recurrence rules) → Platform → Messaging for actual email/SMS delivery.

### Structured interview & Interview Intelligence (Bitbucket project: II)

| Repo | Purpose | Start here |
|------|---------|------------|
| `interview-management-service` | Core IMS backend — meetings, guides, evaluations, consent, question libraries | `controllers/MeetingsController.java`, `InterviewguideController.java`, `EvaluationController.java` |
| `interview-management-ui` | II/IM UI MFE — scheduling panels, guides, evaluation views | `src/imBootstrapper.js`, `src/iiBootstrapper.js` |
| `evaluation-service` | Evaluation & scorecard service — summaries, comparisons, downloads | `EvaluationsApplication.java`, `controller/ScorecardsController.java`, `controller/EvaluationsController.java` |
| `meeting-bot-orchestrator` | Virtual meeting recording bots (Zoom/Teams/GMeet/Webex) | `API_DOCUMENTATION.md`, `src/app.module.ts` |
| `ii-phone-recordings-service` | Phone interview recording (Twilio) | `TwiliopocApplication.java` |
| `speaker-identification` | Speaker ID for transcripts — **confirmed empty stub** (`.gitignore` only); `ii-phone-recordings-service` already has its own `SpeakerDetailsService` — check there first | `master` only — do not scan |

**Suggested feasibility flow for II/recording questions:** `interview-management-ui` (surface) → `interview-management-service` (meetings, guides, consent) → `meeting-bot-orchestrator` or `ii-phone-recordings-service` (capture) → `evaluation-service` (scorecards/evaluations) → `speaker-identification`/`ii-phone-recordings-service` (if diarization needed — see stub note).

## Common feasibility patterns

- **New scheduling rule / conflict handling** → `phenom-internal-calendar` (slots/availability) + `scheduling-rule-parser` (recurrence) + `scheduling-orchestration` (workflow).
- **Reschedule / cancel / invite notification** → `scheduling-main-app` for trigger logic → Platform → Messaging for delivery (not `scheduling-messaging-service` until confirmed active).
- **New scorecard field or interview guide type** → `interview-management-service` (`InterviewguideController`, `QuestionLibraryController`) + `evaluation-service` (`ScorecardsController`).
- **Record virtual interview** → `meeting-bot-orchestrator` (+ platform-specific `bot-recording-*` repos not yet cloned).
- **Record phone interview** → `ii-phone-recordings-service`.
- **Auto-send reminder before interview** → Platform → Automations for trigger + Platform → Messaging for delivery; scheduling event source in `scheduling-main-app`.
- **Recording consent / retention** → `interview-management-service` (`CandidateConsentController`) + Platform → Privacy & Compliance.
- **Roles / permissions / who can view a recording / departmentalization** → **`index/cross-cutting/access-control.md`** — II is audited, don't re-scan code.

## Access control (audited 2026-07-27)

Full detail in [`index/cross-cutting/access-control.md`](../cross-cutting/access-control.md). The short version, because it's counter-intuitive and comes up often:

- **II owns almost no permission data.** One Mongo collection, `permissionsForRole` in the `interviewmanagement` DB, mapping access tier (`ADMIN`/`EDIT`/`VIEW`) → capability flags. The authority for identity and grants is the central **User Management** service (`validateTokenAndPermissions`).
- **Which tier a user gets is hardcoded in Java**, not configured — `TokenUtils.getPermissionsForRole()` maps Recruiter-in-CRM → ADMIN, invited Hiring Manager-in-HRM → EDIT, invited Interviewer-in-HRM → VIEW.
- **Visibility is membership-based, not role-based.** Access to a specific recording comes from `meetings.forwardedList[]`, `meetings.panel.required/optional[]`, or a live CRM `hiringTeamList` lookup.
- **Departmentalization adoption is inconsistent**: `evaluation-service` actively scope-filters via the shared `departmentalization-commons` library; `interview-management-service` has it **hardcoded off** and doesn't pull the library at all. Scope filtering on meetings/recordings can't be enabled by a tenant flag today.
- **Don't mistake `recruiterDetails` for a user/permission table** — it's Twilio phone verification for `ii-phone-recordings-service`.

## Mongo databases (II sub-domain)

All four II services share two databases — useful context before assuming a collection is service-private:

| DB | Services |
|----|----------|
| `interviewmanagement` | `interview-management-service`, `evaluation-service` (read), `meeting-bot-orchestrator`, `ii-phone-recordings-service` |
| `InterviewEvaluations` | `evaluation-service` (primary), `interview-management-service` (pending evaluations, scorecards) |

## Platform dependencies

- **Automations** — reminders, auto-follow-ups, scheduled re-checks
- **Messaging** — interview invites, reminders, confirmation notifications (delivery layer; scheduling trigger logic is in scheduling repos)
- **Recruiter Hub** — interview pipeline views, scheduling panel embedded in CRM UI via `interview-management-ui`
- **Privacy & Compliance** — recording consent, retention of interview recordings/transcripts

## Eng contacts

_Fill in once known — Scheduling team + Interview Intelligence team, Slack channels._
