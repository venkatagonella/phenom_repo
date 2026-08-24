# Skill: Phenom CRM Screening (On-Demand Video Assessment)

> **Area:** Screening — currently only the **On-Demand Video Assessment (ODVA)** lifecycle.
> **Companion files:** `routing.yaml`, `graph.json`. **Framework/contract:** `../INDEX.md`.

---

## GROUNDING CONTRACT (read first)
1. Answer only from code; cite `repo/path:line`.
2. **Only `crm-video-assessment` is cloned.** It covers ODVA config, status lifecycle,
   candidate screening context, and recruiter notifications. It does **NOT** contain video
   capture, AI evaluation/scoring, X+ Screening, Fitscore, Questionnaires, or the Screening
   Agent. If asked about those, say **"not available in the cloned Screening repos."**
3. Multiple matches → list all repo-area paths.
4. Provenance: `verified` (controllers/endpoints read this session) vs `report` (services, sub-agent pass).

---

## WHAT THIS AREA IS (as cloned)
`crm-video-assessment` is a Spring Boot + Kafka Streams service that manages the **state and
notifications** of On-Demand Video Assessments (ODVA), for both **Job** and **Event** entities.

### What it does
- **Config**: enable ODVA and set the required count on a job/event
  (`VideoAssessmentConfigController.java:31` → `VideoAssessmentConfigServiceImpl.setVideoAssessmentConfig:101`).
- **Status lifecycle**: update the candidate's screening status — `invite failed`,
  `pending evaluation`, `evaluated`, `disqualified`, `video deleted`
  (`VideoAssessmentStatusController.java:67` → `VideoAssessmentStatusServiceImpl.updateEntityStatus:126`).
  Status is stored in an `onDemandInterviewScreening` sub-document on the entity and mirrored to Elasticsearch.
- **Candidate context**: return per-candidate ODVA context
  (`CandidateContextController.java:43` → `CandidateContextServiceImpl.getCandidateContext:49`).
- **Recruiter notifications**: on status changes, dispatch notifications via `VANotifyService`
  (abstract) + 4 subclasses (Submitted/Evaluated/Failed/Disqualified), emitting to Kafka topic
  `cp_automation_notification` through the LightSaber gateway.
- **Event ingestion**: a Kafka Streams topology (`InterviewProcessor.java:55`) consumes
  `MCS_VIDEO_SCREEN` and `candidate_initiated_screening`, logs raw events to Mongo
  `OndemandInterviewRawEvent`, and drives `updateEntityStatus`.

### How a video assessment result flows (lifecycle)
1. Candidate completes a video screen in the MCS/video-hub (not in this repo).
2. MCS publishes an event to Kafka `MCS_VIDEO_SCREEN`.
3. `InterviewProcessor.processEvent:119` consumes it → `updateEntityStatus:126`.
4. Status sub-doc updated in Mongo (`OnDemandInterviewScreenings` + entity collection) and ES.
5. `getNotifyServiceFromCurrentStatus:310` selects the right `VANotifyService` subclass →
   builds `InterviewNotificationDto` → calls VX/MCS for email substitutions → emits
   `cp_automation_notification` via LightSaber → recruiter is notified.

---

## CAPABILITY CATALOG (see routing.yaml `intents`)
- **Enable/config ODVA** → `VideoAssessmentConfigController:31`.
- **Update screening status** → `VideoAssessmentStatusController:67` / `updateEntityStatus:126`.
- **Delete a video assessment** → `VideoAssessmentStatusServiceImpl.deleteVideoAssessment:458`.
- **Candidate screening context** → `CandidateContextController:43`.
- **Recruiter notifications** → `VANotifyService` (+ 4 subclasses).
- **Event ingestion** → `InterviewProcessor:119`.

## EXTERNAL SYSTEMS
LightSaber (Kafka gateway), Email service (`/crm/interviewSchedule`), VX/MCS campaign-execution
(email substitutions), crm-events (OWI checklist), Slack (alerts), Elasticsearch.

## DATA STORES
Mongo (`{refNum}_candidates` DB): `OnDemandInterviewScreenings`, `JobSeekerActivity`,
`EventRegistrations`, `JobsList`, `EventsSchedule`, `CandidatesList`, `OndemandInterviewRawEvent`,
`TenantConfigurations`. Redis (tenant/recruiter config). Elasticsearch (entity index per tenant).

---

## CROSS-AREA
- **Automations → Screening**: actions `INITIATE_SCREENING`, `SEND_ODVA`,
  `FORWARD_VIDEO_ASSESSMENT_TO_HIRING_MANAGER` relate here (see `../automations`).
- **Screening → Messaging**: notifications/emails go out through the Messaging stack.

## KNOWN GAPS / CAVEATS
- **This repo is lifecycle+notifications only.** Video capture, playback, AI scoring/evaluation
  are produced upstream (MCS/video hub) — not cloned. Don't describe their internals.
- **X+ Screening, Fitscore, Questionnaires, Screening Agent**: repos not accessible with the
  current SSH key. Answer "not available in cloned Screening repos."
- Uses raw BSON `Document`s (no JPA entities); "models" are request/DTO POJOs.
- Service line numbers are `report` provenance — re-open the file to confirm before quoting verbatim.
