# Skill: Phenom CRM Automations

> **Area:** Automations (Recipes / triggers / conditions / actions)
> **Companion files:** `routing.yaml` (navigate to exact code), `graph.json` (connect the dots).
> **Scope:** Answer questions about how Phenom CRM Automations work, grounded in the
> cloned source under `MyLocalCRM/repos/`. This file tells you *what the area can do*
> and *how to answer without hallucinating*.

---

## GROUNDING CONTRACT (read first)

1. **Answer only from code.** Every factual claim about behavior must be backed by a
   `repo/path:line` reference from `routing.yaml`/`graph.json` or a direct read of the
   file. If you cannot find it in code, say **"not found in the cloned Automations
   repos"** — do not guess.
2. **Cite the location.** When you answer, name the repo and the symbol/line you relied
   on (e.g. `crm-automation-service AutomationController.java:104`).
3. **Multiple matches → list them all.** If a question maps to more than one repo or
   engine, answer per repo-area path and state what each one does. Never silently pick one.
4. **Respect provenance.** `routing.yaml` marks each reference `verified` (read this
   session) or `report` (from a sub-agent read pass). Prefer `verified`; if only `report`
   is available, say the line may need re-confirmation.
5. **Flag the shared library.** `TaskQueueConstants`, `CRMAutomationUtils.raiseAutomationEvent`,
   `TemporalClient`, `MongoDbUtils` live in `com.phenompeople.crm` (NOT cloned). Their
   internal behavior is **not grounded** — say so rather than describe it.
6. **crm-automation is NOT product code.** It is QA test automation. Never use it to
   answer product-behavior questions.

---

## WHAT THIS AREA IS

Phenom CRM Automations lets recruiters build **recipes**. A recipe =
**Trigger** (an entity/field change) + one or more **Control Statements** (condition
filters) + **Actions** (what to do). Recipes run automatically when matching CRM events occur.

**The five repos and their jobs:**

| Repo | Job | Language |
|---|---|---|
| `crm-automations-ui` | Recipe builder UI (MFE remote `crmAutomations`) | Angular 16 |
| `crm-automation-service` | Recipe CRUD, templates, analytics, metadata, jobs, Temporal action activities | Java/Spring Boot |
| `automation-search-service` | Trigger→recipe **matching** (Lucene + ES + validate) | Java/Spring Boot |
| `candidate-automation` | Action **execution** engine (Apache Storm, 24 actions) | Java/Storm |
| `crm-workflows` | LinkedIn CRM Connect integration (misnamed; not general automations) | Java/Spring Boot |

---

## LIFECYCLE (how a recipe runs) — the answer to "what happens when..."

1. **Author** — UI recipe builder (`crm-automations-ui` `edit-automation.component.ts`)
   saves via `AutomationsService.createRecipe` → `POST /crm-automation-service/recipe/create`.
2. **Persist** — `crm-automation-service` `AutomationController.createRecipe`
   (`AutomationController.java:104`) stores the recipe (Mongo `RecipeList`) and its
   projected filter (`MergedFilters`).
3. **Trigger event** — a CRM change publishes a Kafka trigger event
   (`cp_automation_online_trigger` / `cp_automation_trigger`, and the temporal variants).
4. **Match** — `automation-search-service` consumes the trigger
   (`KafkaConsumer.java:58/95`), finds candidate recipes via the Lucene projected-filter
   index (`LuceneSearchService.getProjectedFields`), fetches entity data from ES
   (`DataProviderService.getEntitiesData`), and evaluates the filters
   (`ValidatorService.validateFilters`, line 67). Result → which recipes fire.
5. **Execute** — two engines (see ambiguity note below):
   - **Storm** (`candidate-automation`): `Trigger → Filter → Action` bolts, then
     `ActionFactory.getInstance(actionId)` (`ActionFactory.java:24`) dispatches to one of
     24 action impls in `action/impl/`.
   - **Temporal** (`crm-automation-service`): `TemporalWorker` (`TemporalWorker.java:65`)
     runs a subset of actions as activities (forward-to-HM, video assessment, initiate
     screening, ODVA, invite-for-interview, notification, audit log).
6. **Downstream** — action impls call downstream services (email/SMS campaign, lists,
   tags, jobs, projects, screening, ODVA, etc.).

### ⚠️ Two-engine ambiguity (state this when relevant)
Actions can execute in **Storm** (`candidate-automation`) OR **Temporal**
(`crm-automation-service`). The path is data/feature-flag driven (e.g. the
`automationBatchWorkflow` flag checked in `automation-search-service`
`KafkaConsumer.java:69`). When asked "how is action X run", **check both engines**:
- `candidate-automation/.../action/impl/` for the Storm impl, and
- `crm-automation-service/.../temporal/activity/` for a Temporal activity.
Report whichever implement it, and say if both do.

---

## CAPABILITY CATALOG

### Recipe authoring & management (`crm-automation-service` `AutomationController`)
- Create `recipe/create:104`, update `recipe/update:264`, preview `recipe/preview:135`,
  enable/disable/delete `recipe/setAction:224`, detail `recipeDetail:312`,
  search `searchRecipesByCriteria:356`, history `searchRecipeHistory:324`,
  validate title `validateRecipeTitle:451`, system recipes `i/systemRecipe:484`,
  trigger frequency `trigger-frequency/{recipeId}:647`.

### Templates (`TemplateController`)
- List `template/list:45`, favourite `template/favourite:75`, detail
  `template/{refNum}/{locale}/{templateId}:108`, categories `template/{refNum}/category:139`,
  active check `active-template/{refNum}/{templateId}:167`.

### Analytics / ROI (`AnalyticsController`)
- Metrics `analytics:34`, set hourly rate `setHourlyRate:39`, get hourly rate
  `getHourlyRate/{refNum}:44`. UI: `automation-analytics.component.ts:29`.

### Metadata / configurable triggers & actions (`MetadataController`)
- V2 metadata `i/v2/metadata:41`, action config `i/get-action-config:52`,
  trigger config `i/get-trigger-config:62`.

### Internal jobs (`AutomationJobController`)
- Candidate job `i/CandidateAutomationJob:53`, delay job `i/AutomationDelayJob:86`,
  remove expired `i/removeExpiredRecipe:137`, invite recommendations
  `i/triggerInviteRecommendations:148`, metric generation `i/generate-*-metric:161-177`.

### Trigger→recipe matching (`automation-search-service`)
- Online/offline trigger consumers `KafkaConsumer.java:58/95`, ES fetch
  `DataProviderService.getEntitiesData:78`, filter validate
  `ValidatorService.validateFilters:67`, Lucene index
  `LuceneService.createProjectedFilterIndex:72` / `LuceneSearchService.getProjectedFields:93`.
- Admin/debug endpoints `AdminController` `/i/validate-filter:65`, `/i/getFilterStatus:84`,
  `/i/getLuceneData:105`.

### Action execution — Storm (`candidate-automation`)
- 24 actions dispatched by `ActionFactory.getInstance:24`. Full list in
  `routing.yaml → action_catalog`. Notable:
  - `SEND_EMAIL` / `SEND_SMS` / `CONTACT_CANDIDATE` (composite email+sms by preference)
  - `ADD_TO_LIST` / `REMOVE_FROM_LIST`, `ADD_TAG`, `ADD_TASK`
  - `ASSIGN_TO_JOB`, `ASSIGN_TO_PROJECT`, `CHANGE_HIRING_STATUS`, `CHANGE_PROJECT_STAGE`, `REMOVE_FROM_PROJECT`
  - `INITIATE_SCREENING`, `SEND_ODVA`, `FORWARD_PROFILE`, `FORWARD_CANDIDATE_TO_HIRING_MANAGER`, `FORWARD_VIDEO_ASSESSMENT_TO_HIRING_MANAGER`
  - `ADD_TO_CAMPAIGN` / `CAMPAIGN_OPT_OUT`, `ADD_TO_JTC`, `SIMILAR_JOB_SUBSCRIPTION`, `UPDATE_ADDITIONAL_FIELD`
  - `ADD_NOTE` → **stub, no-op** (`AddCandidateToNote` returns null); `DO_NOTHING` → no-op.

### Action execution — Temporal (`crm-automation-service`)
- Registered in `TemporalWorker.java:65-79`: ForwardCandidateToHRM, ForwardVideoAssessment(+interviewer),
  AuditLog, InitiateScreening, SendODVA, InviteForInterview, SendNotification, BatchAuditLog, RaiseKafkaEvent.

### LinkedIn integration (`crm-workflows`)
- Kafka fan-in `LKConsumer.java:31`; resume upload to LinkedIn `UploadResumeActivity.java:45`;
  action-type strategy dispatch `LinkedInFactory.getLinkedInService:14`.
- **Not** part of the recipe engine — separate integration triggered by CRM entity events.

---

## HANDLING CROSS-CUTTING QUESTIONS (map to multiple repos)

- **"How does automation send an email?"** →
  Storm: `candidate-automation SendEmail` (`ActionFactory.java:54`) → ecampaign.
  UI config: `crm-automations-ui automation-send-email.component.ts`.
  (SMS/WhatsApp/Notification are sibling actions/components.)
- **"How does a recipe decide to run?"** → matching is `automation-search-service`
  (filters/Lucene/ES); firing/execution is `candidate-automation` (Storm) or
  `crm-automation-service` (Temporal).
- **"Where are triggers/actions defined?"** → configurable metadata:
  `crm-automation-service MetadataController` (`/i/get-trigger-config`, `/i/get-action-config`).
  Executable action IDs: `candidate-automation ActionIdConstant.java`.
- **"Automation analytics / time saved"** → `crm-automation-service AnalyticsController`
  + UI `automation-analytics.component.ts`.

If a question is about **Messaging, Screening, Analytics, or Scheduling** specifically,
those are separate areas — note that the automation *action* touches them, but the
owning logic lives in that area's repos (see `../INDEX.md`; those areas are pending).

---

## KNOWN GAPS / CAVEATS (say these instead of guessing)
- **Shared lib not cloned** (`com.phenompeople.crm`): trigger fan-out
  (`CRMAutomationUtils.raiseAutomationEvent`), `TaskQueueConstants` values, `TemporalClient`.
- **Downstream endpoint line numbers** for each Storm action impl came from a sub-agent
  read pass (`report`); re-open the impl file to confirm exact lines before quoting them.
- **crm-workflows** endpoints/lines are `report` provenance.
- **Storm vs Temporal routing** for a specific action is feature-flag/data driven; confirm
  in code before asserting which engine runs a given production tenant's action.
- **No Scheduling repo** is cloned; automation actions like `INVITE_FOR_INTERVIEW`/`SEND_ODVA`
  reach scheduling via downstream calls, but scheduling internals are out of scope here.
