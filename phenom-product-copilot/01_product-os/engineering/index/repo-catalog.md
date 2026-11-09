---
name: repo-catalog
type: index
description: "Master list of cloned engineering repos — one row per repo. Update whenever a repo is added or its purpose changes."
last_reviewed: 2026-07-20
---

# Repo Catalog

Status legend: 🟢 cloned & indexed · 🟡 cloned, not yet indexed · ⚪ planned, not cloned yet

## Recruiter Hub

Sub-folders: `shell/`, `config/`, `candidates/`, `jobs/`, `hrm/`, `dashboard/` (+ Tier B: `search/`, `pipeline/`, `projects/`, `shared/`, `storm/`). Manifests under [`index/repos/recruiter-hub/`](repos/recruiter-hub/capability-index.md) — use that capability index before grepping code.

| Repo | Path | Status | Purpose | Stack | Start here | Also used by |
|------|------|--------|---------|-------|------------|---------------|
| cp_ui_app_2.0 | `shell/` | 🟢 | RX shell — Angular host app that loads every `crm-*-ui` MFE via module federation (candidates, jobs, lists, filters, projects, automations, campaigns, scheduling, requisition, onboarding, offer, BGV, eSign, etc.), plus global nav, login bootstrap, shared design system | Angular 19, TypeScript, `@angular-architects/module-federation`, webpack | `src/app/app.module.ts`, `src/environments/mfe.config.ts` (MFE registry), `src/app/crm-mfe/app-mfe.module.ts` | Nearly every Product Experiences feature (UI host) |
| crm-config-service | `config/` | 🟢 | Multi-module CRM config backend — feature/engineering flags, hiring **pipeline stage definitions** (template, not candidate movement), career-events/university-program config | Java, Spring Boot 2.7.1, Maven (multi-module: config-application/core/events/flags/hiringstatus) | `config-flags/.../FeatureFlagController.java`, `config-hiringstatus/.../PipelineController.java`, `config-events/.../EventTypeController.java` | Platform (feature flags); `crm-hiring-status-service` (stage lookups); most pillars read tenant config |
| crm-recruiter-dashboard | `dashboard/` | 🟢 | Recruiter landing/home dashboard MFE — presentation only, widgets pull data from owning domain services | Angular 19.2, TypeScript, module federation | `src/app/modules/recruiter-dashboard/recruiter-dashboard.module.ts` | — |
| crm-candidate-lists | `candidates/` | 🟢 | Candidate lists (talent pools/saved lists) backend — list CRUD, filtering, templates, dashboards, count aggregation, export, public list API | Java (Play Framework, Scala 2.13.14, sbt) | `app/controllers/ListController.java`, `FilterController.java` | Candidate Engagement (campaign audience targeting); automations (list-triggered recipes) |
| crm-candidates-ui | `candidates/` | 🟢 | Candidate profile MFE — profile view/edit, detail panel, list/table, import flows (manual/resume/bulk), talent communities, template editor | Angular 19.2, TypeScript, module federation | `src/app/modules/candidates/profile/candidates-routing.module.ts`, `src/app/modules/candidates/list-table/candidate-table.module.ts` | — |
| candidates-api | `candidates/` | 🟢 | **Core candidate backend** — CRUD, resume parsing, LinkedIn import, file upload, facets/filters, hiring-status link, tag/note association endpoints, automation triggers, webhooks | Java (Play Framework, Scala 2.13.8, sbt) | `app/controllers/com/phenompeople/CandidateController.java`, `ParseResumeController.java`, `FacetsController.java` | Screening, Interview Management, `crm-candidates-ui`, `candidates-microservice`, automations |
| candidates-microservice | `candidates/` | 🟢 | Edit-profile/merge/bulk-ops backend complementing `candidates-api` — anonymous merge, bulk cleanup, availability, LinkedIn sync, OpenAPI gateway for external integrations (hub path: `microservice-api`) | Java (Play Framework, Scala 2.13.8, sbt) | `app/controllers/CandidateOperationsController.java`, `AnonymousMergeController.java`, `openapi/gateway/controller/GatewayController.java` | External integrations (OpenAPI gateway) |
| crm-jobs-ui | `jobs/` | 🟢 | Job workspace MFE — job list, job detail, requisition-adjacent template editing | Angular 19.2, TypeScript, module federation | `src/app/modules/jobs/jobs-routing.module.ts`, `job-detail.module.ts` | — |
| crm-jobs-service | `jobs/` | 🟢 | Jobs/requisitions backend — req creation/status, postings, org hierarchy, hiring team, compensation, screening questionnaires, activity log (hub path: `jobs-api`) | Java, Spring Boot (pom reads 4.0.2 on `pre-develop` — verify with eng), Maven, MongoDB + Postgres via DALL SDK | `basicRequisitions/controller/ReqCreationController.java`, `reqpostings/controller/ReqPostingController.java` — branch **`pre-develop`** (`main`/`development` are stubs) | `crm-domain-search-service`/`crm-profile-search-service` (job search), automations (assign-to-job) |
| crm-storm-job-pull | `jobs/` | 🟢 | **IX → CRM job ingest** Storm runtime — delta/bulk scrape sync into Mongo+ES, hiring-team/HM assignment, scrape ack to IX | Java, Apache Storm, Kafka, Mongo, ES, Redis | `topology/JobPullTopology.java`, `HiringTeam.java` — branch **`release_25_02`** (`master` is stub) | IX / job-pull-service; Hiring Team Roles |
| crm-storm-job-pull-conf | `jobs/` | 🟢 | Env config for job-pull Storm topologies (IX Kafka topics, endpoints) | `.properties` | `JobPullTopology/application.properties` — env branches **DEV**/STG/PROD | pairs with `crm-storm-job-pull` |
| hrm-jobs-api | `hrm/` | 🟢 | **HRM jobs edge (Play)** — HM workflows + **emails to hiring managers** (forward profile, get feedback); digest data APIs | Java, Play, Scala 3.3.1, Mongo, ES | `SendEmailServices.java`, `HRMJobSeekerService.java`, `conf/routes` | Messaging (`crm-emailservice`); sibling of `hrm-jobs-service` |
| hrm-jobs-service | `hrm/` | 🟢 | **HRM jobs Spring** — task submit, manager approval, hiring-status; emails/Kafka to **recruiters** after HM actions | Java 21, Spring Boot 3.5, Maven | `PostUpdateActionsService.java`, `CandidateOperationController.java` | Migrating from `hrm-jobs-api` |
| hrm-profile-api | `hrm/` | 🟢 | **HRM profile edge (Play)** — forward-to-HM, ODVA, interview feedback, Workday, validations; proxies to profile-service when `enableNewHiringPipeline` | Java, Play, Scala 3.3.1, Kafka, Temporal | `ForwardProfileService.java`, `ProfileServiceRedirection.java`, `conf/routes` | Interview Management; `crm-automation-service` |
| hrm-profile-service | `hrm/` | 🟢 | **HRM profile orchestration (Spring)** — new hiring pipeline forward/HM/task/merge/approval core | Java 21, Spring Boot, Maven | `ForwardProfileController.java`, `ForwardCandidatesService.java` | Called by `hrm-profile-api` |
| hrm-accounts-api | `hrm/` | 🟢 | HRM identity — Keycloak, auto-provision HM users, permissions, user search | Java 21, Spring Boot 3, Keycloak, Mongo, Redis | `AutoProvisionController.java`, `UserController.java` | Auth dependency for all HRM runtimes |
| hrm-gigs-api | `hrm/` | 🟢 | HRM gigs API — gig CRUD/lifecycle + **manager gig emails** (HRM deep links) | Java, Play, Scala 3.3.1, Mongo, ES | `GigServices.java`, `SendEmailServices.java` | Messaging (`crm-emailservice`) |
| storm-candidates | `storm/` | 🟢 | Multi-topology Storm monolith — hub profiles, apply tracking, ATS, GDPR, resume parse, legacy jobpull trigger | Java, Apache Storm, Kafka, Mongo, Redis | `topology/KafkaTopology.java`, `EventProcessorBolt.java` | Candidate Engagement (campaign events); Automations (triggers) |
| storm-candidates-conf | `storm/` | 🟢 | Env config for `storm-candidates` topologies | `.properties` | `KafkaTopology-TOPIC_hub_profiles_Topology/config.properties` — **DEV**+ | — |
| storm-candsignals-conf | `storm/` | 🟢 | Config for talent **signals** topologies (candidate/job/ETG) — runtime JAR not cloned | `.properties` | `CandidateSignalTopology-*/config.properties` — **DEV** | `cp-facet-2.0` (reads signals) |
| storm-candauto-conf | `storm/` | 🟢 | Config for **CandidateAutomation** Storm lane — runtime JAR not cloned | `.properties` | `CandidateAutomation/application.properties` — **DEV** (`master` stub) | Platform → Automations |
| storm-candidatescore-conf | `storm/` | 🟢 | Config for ML **fit-score** CandidateScore topology — runtime JAR not cloned | `.properties` + `application.conf` | `CandidateScore/crm-cand-score.properties` — **DEV** | PUP / facets2 scoring |
| storm-integrations | `storm/` | 🟡 | **Empty stub** (README only) — listed on Storm Libraries sheet; no code | — | Do not scan | — |
| crm-hiring-status-service | `pipeline/` | 🟢 | Candidate hiring status / pipeline **movement** — stage transitions, application moves, rejection reasons, import/export, ATS sync, multistage field config (vs. `crm-config-service`, which owns the stage template) | Java, Spring Boot 2.7.7, Maven | `contollers/HiringStatusController.java` *(sic — package is misspelled `contollers`)*, `ApplicationMoveController.java`, `ATSSyncController.java` | `candidates-api`, automations (change-hiring-status action), `crm-candidates-ui` |
| crm-profile-search-service | `search/` | 🟢 | Candidate-profile-specific search — PUP/X-Plus search, spotlight/intelligent-sourcing facets, agentic/boolean/AI-assisted search | Java, Spring Boot 3.5.7, Maven | `spx/PUPSearchController.java`, `pupfilters/xplus/controllers/XplusSearchController.java`, `agents/controllers/AgenticSearchController.java` | `crm-candidates-ui`/`cp_ui_app_2.0` global search MFEs |
| crm-domain-search-service | `search/` | 🟢 | Generic CRM domain/metadata search — cross-entity field search, field mapping/dropdown metadata, spotlight filters, count aggregation (hub path: `crm-search-service`) | Java, Spring Boot 3.4.5, Maven | `controller/AllFieldsController.java`, `MetadataCountController.java`, `DropdownController.java` | `crm-filters-ui`, `cp_ui_app_2.0` (`filters`, `globalSearch`) |
| crm-filters-ui | `search/` | 🟢 | Filters/facets panel MFE used across candidate/job search and list views | Angular 19.2, TypeScript, module federation | `src/app/modules/filters/filters.module.ts` | Embedded in `crm-candidates-ui` / `crm-jobs-ui` search surfaces |
| cp-facet-2.0 | `search/` | 🟢 | **Legacy-but-live search/facet execution monolith** behind hub path **`facets2`** — candidate/job/global/boolean search, spotlight, dashboard widgets, tags/notes search, SMS inbox, gigs, projects, segments. Directly queries Elasticsearch/MongoDB. Distinct from `crm-search-service` hub path (= `crm-domain-search-service`) | Java (Play Framework, Scala 2.13.8, sbt) | `app/controllers/FacetsController.java`, `conf/routes` — branch **`release-patch`** (`master` is stale, last real commit 2023) | `cp_ui_app_2.0` (`FacetSearchService`, ~70 call sites), `crm-filters-ui`; calls `candidates-api`, `crm-jobs-service`, `hrm-profile-api`, `crm-automation-service` |
| crm-lists-ui | `candidates/` | 🟢 | Candidate lists MFE — list view/management, talent communities (pairs with `crm-candidate-lists` backend) | Angular 19.2, TypeScript, module federation | `src/app/modules/lists/list.module.ts`, `list-routing.module.ts` | — |
| crm-settings-service | `config/` | 🟢 | CRM tenant settings — custom job statuses, additional/custom fields, company watchlist, notes *settings* (not content), job groups, CSV import/export, audit log | Java, Spring Boot 2.7.12, Maven | `controllers/TenantConfigController.java`, `AdditionalFieldsController.java`, `CustomJobStatusesController.java` | `crm-jobs-service` (custom job statuses); `crm-candidates-ui`/`crm-lists-ui` (additional fields, watchlists) |
| notes-service | `candidates/` | 🟢 | Candidate notes backend — candidate note CRUD, "feature notes" on non-candidate entities (hub path: `notes-api`; UI counterpart `crm-notes-ui` not cloned) | Java, Spring Boot 2.7.5, Maven | `controllers/CandidateNoteController.java`, `FeatureNoteController.java` | `candidates-api` (note association endpoints), `crm-candidates-ui` |
| tags-service | `candidates/` | 🟢 | Candidate tags backend — tag CRUD, tag-to-candidate association (UI mounted inside `crm-candidates-ui`, not a separate MFE) | Java, Spring Boot 3.1.1, Maven | `controllers/TagsController.java`, `candidatetags/controllers/CandidateTagController.java` — branch **`master`** (`main` is stub-only) | `candidates-api`, `crm-candidates-ui`, `crm-automation-service` (add-tags action) |
| crm-projects-ui | `projects/` | 🟢 | Recruiting projects MFE — project-based view over jobs/candidates, template editing. **No dedicated projects backend cloned** — likely reads `crm-jobs-service`/`candidates-api`/`crm-workflows` (LinkedIn project sync), unconfirmed in code | Angular 19.2, TypeScript, module federation | `src/app/modules/projects/projects.module.ts`, `projects-routing.module.ts` | Backend integration unconfirmed — validate with owning team before feasibility calls |
| crm-commons | `shared/` | 🟢 | **Shared RX library** (Maven multi-module, not a service) — departmentalization/scope ACL (`scopeAttr`), ES/Mongo scope filters, hiring-team job visibility (`jobsHiringTeam`), CBAC/consent, plus Mongo/ES client commons. Branch **`release`** (v12.8) | Java 8, Maven modules: `crm-departmentalization`, `crm-mongo-commons`, `crm-es-commons`, `crm-core-commons`, `apm-alerts` | `crm-departmentalization/.../DepartmentalizationManagerV2.java`, `ScopeBuilder.java`, `DepartmentalizationConstants.java` | Consumed by many CRM backends (search, candidates, jobs, scheduling — confirm per `pom`); Platform → Privacy (CBAC/consent) |

## Product Experiences → Interview Management

Manifests: [`index/repos/interview-management/capability-index.md`](repos/interview-management/capability-index.md) — all 12 repos manifested (9 active + 3 confirmed stubs).

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| scheduling-main-app | 🟢 | Core scheduling application — schedule requests, event scheduling, invites, meeting/live links, message & interview templates, notification prefs, webhooks, Temporal worker + Kafka listener activities (58 controllers — largest repo in the sub-domain) | Java, Spring Boot, Temporal, Kafka | `SchedulingApplication.java` (+ `SchedulingWorkerApplication.java`, `SchedulingListenerApplication.java`), `controller/SchedulesController.java`, `controller/eventscheduling/EventSchedulingController.java`, `controller/MeetingLinkController.java` | Platform → Messaging (notification delivery) |
| phenom-internal-calendar | 🟢 | Internal calendar service — availability slots, conference rooms, scheduling teams, personal calendar connect (Google/Outlook), calendar sync, GDPR | Java 17, Spring Boot (reactive/WebFlux), MongoDB Reactive, Redis Reactive | `CalendarApplication.java`, `controllers/SlotGenerationController.java`, `controllers/CalendarConnectController.java` | — |
| scheduling-orchestration | 🟢 | Scheduling workflow orchestration layer — Temporal workflow execution, bulk signals, workflow config, Kafka workflow events | Java, Spring Boot, Temporal SDK, MongoDB, Redis | `SchedulingOrchestrationApplication.java`, `controller/WorkflowExecutionController.java`, `BulkSignalWorkflowController.java` | — |
| scheduling-rule-parser | 🟢 | Recurrence rule (RRule) parsing microservice for scheduling patterns — rule parsing + intersection checks | Python, Flask | `app.py`, `controllers/rules_controller.py` (`/rules`, `/rules/intersection` endpoints) | — |
| scheduling-messaging-service | 🟡 | Scheduling-specific messaging — **confirmed empty stub** on `main` (2 files: `.gitignore` + boilerplate `README.md`, no code). Actual trigger logic lives in `scheduling-main-app` (`NotificationController`, `MessageTemplateController`); delivery is Platform → Messaging | — (no code) | `README.md` only — do not scan for feasibility | Platform → Messaging |
| scheduling-meeting-links | 🟡 | Meeting link generation — **confirmed legacy stub** (last updated 2022, single `.gitignore` file on `master`, no code). Superseded by `scheduling-main-app` (`MeetingLinkController`, `LiveLinkController`) | — (no code) | Do not scan for feasibility | — |
| interview-management-service | 🟢 | Core Interview Management / II backend — meetings, interview guides, question/attribute libraries, scorecards (lightweight), candidate consent, onboarding, bulk import, scheduling integration, X-Plus/CRM, GPT-assisted content | Java (Play Framework, sbt), MongoDB, Kafka, AWS S3, MS Graph | `controllers/MeetingsController.java`, `InterviewguideController.java`, `QuestionLibraryController.java`, `CandidateConsentController.java`, `SchedulingIntegrationsController.java` | Recruiter Hub (II UI host) |
| interview-management-ui | 🟢 | Interview Management & II UI — video playback panel, unassigned-interview panel (MFE/bootstrapper; **Vue 2.x**, not Angular/React). Note: `package.json` name is `"video-content"`, not the repo slug | JavaScript/TypeScript, Vue 2.x, webpack | `src/imBootstrapper.js`, `src/iiBootstrapper.js`, `src/redesign_imBootstrapper.js` (confirm which bootstrapper is live) | Recruiter Hub (mounted in CRM shell) |
| evaluation-service | 🟢 | Structured interview evaluations & scorecards — evaluation summaries, candidate comparison, config, PDF/bulk downloads, reacts to CRM `ApplicationMoveEvent` | Java, Spring Boot 3.2.4, Gradle | `EvaluationsApplication.java`, `controller/EvaluationsController.java`, `controller/ScorecardsController.java`, `CrmApiController.java` | Recruiter Hub (pipeline-move events) |
| meeting-bot-orchestrator | 🟢 | Virtual meeting bot orchestrator — dispatches Recall.ai recording bots to Zoom/Teams/Webex/GMeet, manages bot lifecycle, ingests Recall webhooks, tenant-scoped via `x-ph-refnum` header | Node.js, NestJS, TypeScript, MongoDB | `src/app.module.ts`, `API_DOCUMENTATION.md` (`GET /v1/meetings`, bot management), `src/shared/services/recall/recall.service.ts` | Platform → Privacy & Compliance (recording retention) |
| ii-phone-recordings-service | 🟢 | Phone interview recording service — Twilio-based inbound/outbound call handling + recording, speaker/recruiter detail lookups. ⚠️ internal package name `twiliopoc` despite being production | Java, Spring Boot 3.2.2, Gradle, Twilio SDK | `TwiliopocApplication.java`, `controllers/IncomingCall.java`, `OutboundCall.java`, `service/SpeakerDetailsService.java` | — |
| speaker-identification | 🟡 | Speaker diarization / identification for interview transcripts — **confirmed empty stub** on `master` (`.gitignore` only, no code). `ii-phone-recordings-service` already has its own `SpeakerDetailsService` — check there and with II team before assuming this capability is unbuilt | — (no code) | `master` only — do not scan for feasibility | — |

> **Repo name corrections:** User-provided `Ii-phone-recording-service` → Bitbucket slug **`ii-phone-recordings-service`** (plural). `Speaker-Identification` → **`speaker-identification`** (lowercase).
>
> **Stub confirmation (2026-07-12 skim):** `scheduling-messaging-service` (2 files), `scheduling-meeting-links` (1 file), and `speaker-identification` (1 file) contain no production code — manifests marked `role: stub`, `scan_priority: skip-for-feasibility`. See `index/repos/interview-management/capability-index.md` for where the equivalent capability actually lives.

## Product Experiences → Candidate Engagement

Manifests: [`index/repos/candidate-engagement/capability-index.md`](repos/candidate-engagement/capability-index.md).

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| candidates-email-campaign | 🟢 | **v1** campaign management API — defines/sends email + SMS campaigns, templates, analytics, CMS campaign config (Maven/build artifact: `candidates_email_campaign`) | Java (Play Framework, sbt) | `app/controllers/CampaignController.java` | Platform → Messaging (delivery layer) |
| storm-campaign | 🟢 | Real-time campaign event tracking (opens/clicks) + autoresponder/drip campaign scheduling via Apache Storm topology (Maven artifact: `storm-emailcamp`) | Java, Apache Storm | `src/jvm/com/phenompeople/tracker/topology/EmailCampaignsTopology.java` | — |
| storm-campaign-conf | 🟢 | Env config for campaign Storm topologies (+ bundled CandidateAutomation/CandidateScore folders) | `.properties` | `EmailCampaign/camp-storm-config.properties` — **DEV**+ | pairs with `storm-campaign` |
| storm-sms-campaign-conf | 🟡 | **Empty stub** — SMS config lives in `storm-campaign-conf` / topology in `storm-campaign` | — | Do not scan | — |
| storm-hob-campaign | 🟡 | **Empty stub** — HOB lane uses `storm-campaign` JAR | — | Do not scan | — |
| storm-hob-campaign-conf | 🟢 | Env config for HOB EmailCampaign deployment lane (acronym undocumented in code) | `.properties` | `HobEmailCampaign/camp-storm-config.properties` | `storm-campaign` |
| crm-campaigns-v2 | 🟢 | **v2** campaign engine — audience segmentation (facet-sql-builder), fair scheduling (fairscheduler), CDC, REST API (Spark/Livy/K8s job orchestration), Spark/Kafka streaming jobs. ⚠️ Naming note: internal packages/artifacts are named `messagingv2` (e.g. `com.phenom.messagingv2.*`) despite the repo being "campaigns-v2" — legacy carry-over, not evidence it belongs in Platform → Messaging; validate with owning team if it matters for a specific decision | Java, Apache Spark, Kafka, Iceberg, REST, Maven multi-module | `restapi/src/main/java/com/phenom/messagingv2/RestMain.java`, `facet-sql-builder/` | Platform → Messaging (naming overlap — verify) |
| crm-storm-transactions | 🟢 | Real-time campaign transaction/stats processing via Storm — email campaign analytics stat bolts, transactional email/SMS, recruiter digest, plus one GDPR-specific bolt | Java, Apache Storm, Maven | `src/jvm/com/phenompeople/StormTransactions/topology/CRMTransactionsTopology.java`, `bolt/EmailCampaignAnalyticsStatsBolt/` | Platform → Privacy & Compliance (dedicated GDPR bolt) |
| crm-storm-transactions-conf | 🟢 | Env config for `CRMTransactions` topology | `.properties` | `CRMTransactions/storm-transactions-config.properties` — **DEV**+ | pairs with `crm-storm-transactions` |
| campaign-execution-service | 🟢 | Executes candidate outreach campaigns; injects video context (Kaltura) into campaign content | Java (Play Framework, Scala 2.13.1, sbt), MongoDB, Redis | `app/com/phenompeople/mcs/campaignexecution/controllers/CampaignExecutionController.java` | — |

## Product Experiences → Screening

Manifests: [`index/repos/screening/capability-index.md`](repos/screening/capability-index.md).

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| assessment-management-service | 🟢 | Core assessment CRUD — create assessments, look up by candidate/job/email, configured-assessments per job | Java (Play Framework, sbt) | `app/com/phenompeople/controllers/AssessmentController.java` (branch: `release_2.2`, 2026-04-22 — master is an empty stub, see note below) | — |
| assessment-streaming-service | 🟢 | Normalizes and streams assessment results from third-party providers (eSkill, Talogy, Buplas, Otomeyt) via Kafka; syncs assessment status + job-pull events | Java (Play Framework, sbt) | `app/com/phenom/assessmentstreaming/services/kafka/AssessmentStatusUpdateEventsListener.java` (branch: `release_1.0`, 2026-04-22 — master is a stub) | — |
| video-assessment-ats | 🟢 | Processes video assessment events and syncs results into the ATS/CRM by job application ID | Java (Play Framework, sbt) | `app/.../controllers/TestController.java` (`processVideoAssessmentEvents` — despite the "Test" name, this is production event processing on this branch) (branch: `fun_stg_deployment`, 2026-05-20 — master is a stub) | Recruiter Hub (candidate profile / video review) |
| video-assessment-gdpr | 🟢 | Candidate-facing video assessment info API (`VideoAssessmentController`) **plus** privacy/compliance — scheduled auto-purge, compliance events, data migration, S3/Mongo utilities. Naming undersells scope — validate before assuming GDPR-only | Java (Play Framework, sbt) | `app/.../controllers/VideoAssessmentController.java` (`assessmentInfoByCandidateId`), `GdprTestController.java` (branch: `func_24_02_phApplicationId`, 2026-07-07 — master is a stub) | Platform → Privacy & Compliance |
| video-hub | 🟢 | API gateway / auth-proxy in front of video assessment services — routes and authorizes requests to underlying video services (VX plugin integration) | Java (Play Framework, sbt) | `app/com/phenompeople/videohub/controllers/ApiController.java` (branch: `feat_common_may_2026`, 2026-07-09 — master is a stub) | Recruiter Hub, Interview Management (check before building separate video-proxy) |
| odva-transcription-app | 🟢 | Transcribes video/audio recordings (assessments) via AWS Transcribe (established path) **and** AssemblyAI (in-progress integration on current branch); publishes results via Kafka/SQS, stores in MongoDB/S3; also calls Candidate Engagement's `campaign-execution-service` for video-context | Java, Spring, Gradle, AWS SDK v2 | `src/main/java/com/phenom/transcription/services/TranscribeJob.java`, `AssemblyAiOrchestrationService.java` (branch: `func_1.1_PHEM-2098529_assembly_ai_integration`, 2026-06-12 — master is a stub) | Interview Management (check before assuming a separate interview-recording transcription build is needed); Candidate Engagement (`campaign-execution-service`) |

> **Master-branch stub warning:** `assessment-management-service`, `assessment-streaming-service`, `video-assessment-ats`, `video-assessment-gdpr`, and `video-hub` all have an empty `master` (single "Initial commit" with just config files) — real code lives on feature/release branches. Each has been checked out locally to its most-recently-updated branch as of 2026-07-10 (noted above). `sync-repos.sh` only runs `pull --ff-only` on whatever branch is currently checked out, so it won't auto-advance to a newer branch — re-check `git branch -r` periodically for anything more recent.

## Platform → Automations — Workflow

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| automation-ui-2 | 🟢 | Automation Engine main UI — workflow builder, recipe editor, automation central | React 18, Vite, TypeScript, @phenom/react-ds | `src/routes/definitions.tsx`, `src/pages/WorkflowDashboard` | Recruiter Hub (mounted in CRM shell) |
| automation-service-2 | 🟢 | AE backend — workflow config CRUD, triggers, actions, versioning, analytics | Java 8, Spring Boot 2.7, MongoDB | `AutomationServiceApplication.java`, `controllers/AsyncWorkFlowController.java` | Screening, Interview Management, Candidate Engagement (recipe consumers) |
| automation-engine-mfes | 🟢 | MFE monorepo — action center, policy engine, fraud product UIs | pnpm, Turbo, React | `apps/`, `ARCHITECTURE.md` — branch **`develop`** (`main` is README-only) | Recruiter Hub |
| action-centre | 🟢 | Action center backend — multi-module Spring service | Java, Spring, Maven | `ActionCentreApplication.java`, `ae-action-centre-domain/` — branch **`action-center-dev-2`** | Recruiter Hub |
| ae_statesmith | 🟡 | Hiring pipeline state machine backend | Java, Spring Boot | `StatesmithApplication.java`, `controllers/` — branch **`auto-transitions`** (`main` is README-only) | Screening, Interview Management |

## Platform → Automations — CRM Automations

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| crm-automation-service | 🟢 | Core CRM automation backend — recipe CRUD, templates, reminder jobs, Temporal activity workers (screening, notifications, interview invite, HRM forward, audit) | Java, Spring Boot, Temporal, Maven | `CrmAutomationServiceApplication.java`, `controllers/AutomationController.java`, `temporal/activity/` | Platform → Messaging (notification actions), Screening, Interview Management |
| crm-workflows | 🟢 | CRM Temporal workflow definitions — LinkedIn project sync, resume sync, Kafka workflow broker | Java, Spring Boot, Temporal, Kafka | `CrmWorkflowsApplication.java`, `linkedin/`, `helpers/WorkflowUtils.java` | — |
| crm-automations-ui | 🟢 | CRM Automations Angular UI — recipe builder/config surfaces | Angular 16, TypeScript | `src/app/`, `angular.json` | Recruiter Hub (mounted in CRM shell) |
| automation-search-service | 🟢 | Automation recipe/filter search — Lucene indexing, filter config cache, Temporal filter activities, Kafka consumer | Java, Spring Boot, Lucene, Temporal | `AutomationSearchService.java`, `lucene/LuceneSearchService.java`, `controller/AdminController.java` | `crm-automation-service` (recipe lookup) |
| crm-automation | 🟢 | **QA / E2E test harness** for CRM — Playwright + Robot Framework (~1.7k `.robot` files). **Not the production backend** — that is `crm-automation-service`. Cloned for test-coverage questions only; skip for feasibility routing | Playwright, Robot Framework, Python | `RF_Automation_CRM/`, `PlayWright_TestAutomation/` | — |

## Platform → Messaging

Manifests: [`index/repos/messaging/capability-index.md`](repos/messaging/capability-index.md).

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| candidates_email_microservice | 🟢 | Legacy email sending/delivery microservice — universal email sending, triggers, bot emails, admin tools (also embeds legacy SMS + campaign-job migration controllers) | Java (Play Framework, Scala 2.13.14, sbt), Java 17 | `app/controllers/UniversalEmailController.java`, `EmailTriggerController.java` | Candidate Engagement (campaign email triggers) |
| candidates-sms-services | 🟢 | Primary SMS/WhatsApp delivery service for candidates — SMS config, number provisioning, WhatsApp, bot SMS campaigns, HRM/bot integrations | Java (Play Framework, Scala 2.13.14), Gradle+sbt, Java 17 | `app/controllers/SMSController.java`, `WhatsAppController.java` | — |
| crm-messaging-platform | 🟢 | Modern multi-service messaging platform (monorepo, 20+ modules) — email API/facade/analytics, multi-vendor SMS/voice gateway + phenom inbox, transactional email, campaign-execution modules | Java 17, Spring Boot 3.5.13, Maven (multi-module) | `email-api-service/`, `email-facade-service/`, `messaging-gateway-service/` | Candidate Engagement (`recruiter-campaign-service`, `sms-campaign-service`, `system-campaign-service` modules are campaign-execution-flavored, not the segmentation engine) |
| candidates-notifications | 🟢 | In-app/recruiter notification service — notification feed, task spotlight, "follow candidate" alerts | Java (Play Framework, Scala 2.13.14) | `app/controllers/NotificationController.java` | Recruiter Hub (notification surface in CRM UI) |

## Platform → Privacy & Compliance

| Repo | Status | Purpose | Stack | Start here | Also used by |
|------|--------|---------|-------|------------|---------------|
| crm-gdpr | 🟢 | CRM GDPR service: candidate view/delete/update requests and their jobs, tenant GDPR settings (`getGDPRConfig` / `updateGDPRConfig`, the live backend of Settings → GDPR), recruiter notification and confirmation emails, internal daily/weekly reports. Branch **`prod`** (master is stale, Jan 2025) | Java (Play Framework, sbt), MongoDB | `conf/routes`, `controllers/GDPRUiController.java`, `controllers/JobController.java`, `services/GdprServices.java`, `services/GdprEmail.java` | Recruiter Hub (`cp_ui_app_2.0` Settings → GDPR; `candidates-api` holds an older copy of the config endpoints with routes commented out) |

## Unassigned / needs pillar decision

Repos that don't cleanly fit a pillar yet (e.g. Career Site/CIM, Talent Analytics, Integration Experience/ATS connectors). Log here instead of guessing.

| Repo | Purpose | Candidate pillar(s) | Notes |
|------|---------|----------------------|-------|
| | | | |

---

## How to add a repo

1. Clone it into the right `repos/<pillar>/<sub-domain>/` folder (see `taxonomy.md`).
2. Add a row above with status 🟡.
3. Skim the repo for its purpose, stack, and a good "start here" entry point (main service class, top-level API router, etc.).
4. Flip status to 🟢 and add a short entry to the matching domain file in `index/`.
5. If other pillars consume this repo, note it in "Also used by" instead of cloning twice.
