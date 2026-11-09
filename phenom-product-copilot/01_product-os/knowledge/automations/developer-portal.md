# Automation Engine — Platform Capabilities and the Developer Portal

Last enriched: 2026-10-29 (code read of `automation-service-2` master `2081b5a8`, `automation-ui-2` master `782802679`, `automation-engine-mfes` develop `96262c9` + feature branches; AE Activity Studio Coach for the intended process). Not yet reviewed by the AE team. Code paths are relative to `engineering/repos/platform/automations/workflow/`.

## What Exists Today

The **Automation Engine (AE)** is Phenom's horizontal orchestration layer: a **workflow** is a trigger (an event on an entity) plus a graph of **activities** that run when the event fires. Customers reach it through products (Screening, HVH, CRM, onboarding); it is not sold on its own. The **Developer Portal** (Developer Hub) is the authoring area inside AE where product teams define activities and triggers that later appear in the **Workflow Builder** for HRIT, admins and business partners.

Three code bases:

| Repo | What it is | Role |
| --- | --- | --- |
| `automation-service-2` | Spring backend | Stores and publishes definitions (activities, triggers, events, workflows, endpoint specs), serves dropdown data, exposes execution logs and KPIs. **Does not execute workflows**: runtime is the separate `automation-engine-core` library (`pom.xml:160`), no Temporal code here |
| `automation-ui-2` | React host app | Workflow Builder, Developer Portal, Trigger Library, templates, settings. Hosts the MFEs below |
| `automation-engine-mfes` | Module-federated micro-frontends | List Management (`FraudDetection`), job-level Policy overrides (`PolicyEmbeddings`), Action Center; on branches: Policy Library, Action Registry, Pipelines + Pipeline Builder (`ae_statesmith`). Pages are being extracted from `automation-ui-2` one by one (`apps/policies/README.md:3`) |

### AE workflow vs CRM recipe

| | AE workflow | CRM recipe |
| --- | --- | --- |
| Built by | HRIT, admins, business partners | Recruiters |
| Shape | Multi-step map with branches, loops, waits | When / If / Then |
| Authoring of steps | Product teams in the Developer Portal | CRM Automations pod in code |
| Tool | Automation Engine | CRM Automations ([product-overview.md](product-overview.md)) |

## What the platform provides vs what a product team builds

| Capability | Platform provides (no product work) | Product team must supply |
| --- | --- | --- |
| **Activity definition** | Form builder (visual + JSON), 10 field types, side-panel tabs, branches, icon, preview, JSON-schema generation, storage in `ui_activity_definitions` | Name, description, fields, Automation Type, category, product; ask AE to add the activity to the automation type's `allowedActivities` / `developerActivities` (no UI for this) |
| **Dropdown data** | Gateway `/proxy/{service}/{proxyId}` with per-service Keycloak client-credentials tokens, JsonPath mapping of response to label/value, 9 built-in filter entities | Its own search endpoint, registered as an **endpoint specification** (needs `meta:write`; AE does this today). No endpoint-spec page in the UI |
| **Execution flow** | Visual canvas with loop (for/while over a list), fixed and dated waits, decision, parallel/serial groups, sub-flows, API call, Temporal call to any task queue, retries, continue-on-failure | The flow itself, and either (a) a Temporal worker on the product's own task queue, or (b) an HTTP endpoint the API step can call |
| **Triggers & events** | Event definitions (Kafka topic, criteria, entity paths), Trigger Library UI, event routing | The Kafka event from the product's service; `EVENT:all` / `TRIGGER:all` permissions, held by AE today |
| **Placement rules** | Logic tab: count, position, sequence, branch, saved to `/v1/validations` | The rules. **Enforced in the Workflow Builder front end only**; no backend check found |
| **Publish / promote** | Workflow publish/unpublish, versioning, export/import between environments, template promotion | Nothing, but see "Known limitations": the activity-level Publish button is not wired |
| **Observability** | Per-tenant executions, KPIs, logs, errors (`/v1/workflows/{refNum}/executions|kpi|logs|errors`, Doris-backed), analytics meta, dashboards | Nothing |
| **Audience / tenant** | Audience validation (bloom filters at publish), tenant scoping by `refNum`, per-tenant automation types | Nothing |
| **Auth** | JWT or app token, entity:scope permissions mapped per role in DB | Role mapping rows (DB), set by AE |
| **Lists** | List Management MFE: list definitions, records, templates, bulk import (`/v1/automation-lists/*`) | List contents |
| **Policies** | Policy Library (GUARDRAIL / ROUTING / action / GLOBAL rules, AI extraction from a document), job-level overrides, evaluated by `orchestration-ai-engine` | Product config (`productKey`, business functions, entities, outcomes), registered in DB |
| **Action Center** | Task inbox with server-driven widgets (markdown, key-value, table, attachments, timeline) and invokable actions | Registration as a "rendering application" (`appKey`) and the task/action backend |
| **Pipelines** | Hiring pipeline state machine (`ae_statesmith`): stages, substages, statuses (system / ATS / custom), reasons, transitions, auto-assignment rules | Pipeline configuration. No auto-transition UI yet; machines carry `postActions` |
| **MFE hosting** | Host loads `*PluginInit.js` and calls `initPluginBootstrapper({containerId, appKey, siteData.refNum, authorization, proxyConfig, permissionMapping})` | Nothing today: only AE's own apps are mounted; another pod cannot mount its UI inside AE |

## Developer Portal: what you configure

Entry: settings gear → **Developer Hub** (`config:all` permission) → `/developer/activity-library`. Sidebar: Activity Library, Trigger Library, Entity & Event Management, Custom Activities, Realtime Subflows.

### Creating an activity

* Type: **Single** only. Group and Internal are shown but "Coming Soon" (`automation-ui-2/src/pages/developer/ActivityLibrary/ActivityTypeSelection.tsx:26-44`).
* Build method: **Visual Components** or **JSON Code**; a toggle in the Builder switches between the form editor and a Monaco JSON editor.
* Setup progress tracks 8 steps across the four tabs.

### Settings tab

| Sub-tab | Fields | Source |
| --- | --- | --- |
| Details | Name (locked after first save; slug becomes the id, must be unique), map-card description, Activity Type (Default / Trigger / Condition, icon palette only), Automation Type (multi), Activity Category (= `groupName`, groups the palette), Product Experience, Product | Types/categories/PE/products are **fetched from `/v1/automation-types` and `/v1/automation-options/*`**, i.e. DB values, not code |
| Side Panel | Tabs Configuration (always on), Advanced, User Interface (adds predefined candidate-facing fields); side-panel description; Help icon | |
| Branches | One / Limited (named outcomes) / Unlimited | Limited stores `multipathOutcomes`; One and Unlimited both store `hasMultiPathOutcomes=false`, so Unlimited reloads as One (`Branches.tsx:15-21,43`) |

Guideline from the AE coach (not enforced in code): activity name ≤ 34 characters, Verb + object; side-panel description ≈ 84 chars for two lines.

### Builder tab: field types

| Type | Settings (`automation-service-2/…/models/activity_builder/`) |
| --- | --- |
| String | text / textarea / richText; min, max length |
| Number | min, max |
| Dropdown | **Static** options or **Dynamic** (API); Single or **Multi** (min/max items); `apiConfig` {method, endpoint, service, headers, body, abstractConfig} or `specConfig` {service, proxyId, entity} |
| Checkbox group | layout; static or dynamic; min/max items |
| Radio group | layout; options |
| Boolean (toggle) | can fetch options dynamically; **can create a branch on the field** (`triggersFollowUp`, `followUpBranchLabel`) |
| Media | png/jpg/mp4/txt/pdf/doc; max size; multiple; max files |
| Group | nested fields; layout; style |
| Divider, Description text, Widget | display only (Widget = "User Interface Radio") |

Per field: required, tooltip, hint, locked, tab, and **field actions** (show/hide another field when a value equals X or exists). `date` and `code` exist as types but are not offered in the menu; there is **no JSON / list-of-objects field**. The generated JSON schema is stored in `validations`; **no server-side validation of submitted values was found**.

### Dynamic dropdown wiring

Dialog "Dynamic selection API configuration" (Basic / Advanced / Mapping):

1. Method (GET/POST/PATCH/PUT/DELETE), **Service** (fetched from `/v1/workflow/dashboard/services-list`, i.e. the registered endpoint specs), endpoint path, optional headers and body with value sources CONTEXT / EVENT / STATIC / NESTED.
2. "Abstract Data" = `{labelPath, valuePath}` JsonPath into the response.
3. "Execute Configuration" calls `POST /v1/filters/spec` and shows raw vs transformed values.
4. Save generates a spec via `/v1/activity-builder/activities/generate-spec`.

Behind it: `FieldFiltersService` entity `dynamic-spec` looks up the endpoint spec, fills params from context, calls the target through the proxy, and maps the response (`services/filters/SpecHelpers.java:435-474`). If the service holds a `serviceAuthorization` with provider `KEY_CLOAK`, the platform fetches and caches a client-credentials token (`SpecHelpers.java:561-600`). "No data fetched" means the service is not registered or the path/mapping is wrong.

Built-in filter entities (no endpoint spec needed): `job`, `job-attr`, `candidate-attr`, `onboarding-job-attr`, `onboarding-placeholders`, `trigger_locales`, `trigger_siteTypes`, `candidate_tags`, `dynamic-spec` (`services/filters/FieldFiltersService.java:129-469`). There is **no projects and no email-template entity**.

### Logic tab

Count (Unlimited / Exact / Range), Position (none, first after trigger, last), Sequence (allowed or excluded previous/next activities, any vs immediate), Branch (Unlimited / Exact / Range). Saved to `/v1/validations`. The backend has `allowedPreviousActivity` / `allowedNextActivity` fields but nothing reads them (`models/ProductActivity.java:56-59`); enforcement is front-end only.

### Execution tab

Each execution flow is a SUBFLOW workflow bound to the activity (`nodeType=featureId`), with name, Automation Type, Channel and an Execution Criteria JSON. The editor is the same React Flow canvas as the Workflow Builder; the palette is fetched (`/v1/product/ui/activities/automation-type/list` filtered by `developerActivities`, plus an Async group from `/v1/product/async/activities/list`). No role gating on the editor.

Step types the publisher emits (`models/workflow_actions/ActionConfig.java:23-32`, `services/PublishUtils.java:141-193`):

| UI node | Published step | Notes |
| --- | --- | --- |
| config | context_update | set context values |
| decision / uiDecision / condition | decision / condition | rule tree (AND/OR) |
| **for_loop / while_loop** | **loop** | `iterationSource` = list in context, `maxIteration`, `breakRules` (`ActivityLoopConfig.java:19-28`) |
| waitBy / waitedDecision | fixed_wait / dated_wait | SECOND…YEAR, or a date from context with offset |
| multi_action | multi_action | SERIAL or PARALLEL |
| miniflow | sub_flow | |
| async / asyncCustom | base | Temporal activity: `executionConfig.TASK_QUEUE` + `NAME`, arguments, retry options (3 attempts, 1 m → 10 m back-off, 60 m timeout), `continueExecutionOnFailure` (`PublishUtils.java:963-1007`) |
| uiApiCall | api item in a generic activity | `ApiCallItem` {method, endpoint, headers, body}, values from CONTEXT / EVENT / STATIC / PREVIOUS_OUTPUT, JSON or multipart (`models/workflow/ApiCallItem.java:14-52`) |
| go_back / go_to, resetter, exit / terminate | same | |

`wait_until_event` is a constant with no builder. `#firstName`-style string templating was **not found**; values are mapped by source + path.

### Trigger Library and events

* Trigger: name, description, scope Global vs Tenant, entity, event, operator, single/multi value, advanced filters; model `AutomationTrigger` {entity, event, filters, automationTypeId, scope}. Save needs `TRIGGER:all`.
* Event: `AutomationEventDefinition` {handle, Kafka `topicName`, mode DEFAULT/BATCH, `eventCriteria`, `primaryEntity`, tenant/entity paths, projections}. CRUD needs `EVENT:all`.
* Entity & Event Management page: entities with a domain and a static or dynamic schema.
* No hard-coded "AE only" check: whoever's role maps to these permissions in the DB `AccessMapping` can register (`utils/AuthHandler.java:193-219`).

## Publish and promote

| Object | What works | Permission |
| --- | --- | --- |
| Workflow | Publish / unpublish (`/v1/publish/workflow`), versions (new version per change), statuses PUBLISHED / UNPUBLISHED / PAUSED / IN_PROGRESS (shown as Live / Pending / Paused / Publishing), **Promote to {env}** via `/v1/ui/workflow/export` + `/v1/configs/import` | `ui_workflow:publish`, `config:publish`, promote `ui_workflow:create` |
| Activity (Developer Portal) | `publishStatus` DRAFT / PUBLISHED and `version` are stored, but **no code changes them**; the Publish button has no handler, Duplicate / Version Control only log to console (`DeveloperActivityDashboard.tsx:184-188`) | — |
| Environment copy | `/v1/configs/export/{entity}/{id}/{env}` covers `workflows` and runtime `activities` (ui/async/generic/custom), **not activity-builder definitions** (`services/ConfigPublishService.java:145-221`) | import is token-only |
| Templates | `/v1/ui/template/import|export|instances`, versioned | |

Process as the AE team describes it today: Draft → Request to publish → AE reviews and publishes → POD tests in INTQA → AE promotes. Given the code above, "publish" and "promote" of an activity are manual AE steps, not buttons.

## Hard-coded first-party activities (not built in the Portal)

Side-panel forms in `automation-ui-2/src/pages/VerticalEditor/ConfigContent/forms/`: Add Tag, Async, Async Task, BGV rule check / verification, Candidate Details (v1, v2), Check Availability, Delay, Execution, Exit, Forms / Forms Approval, Generic Decision, Job Card, Journey, Locale, Loop / Loop check-in, Media, Mini-flow, Multi-action, Q&A, Redirect, Screen, Status, UI API call, Update Field, Waited Decision, Workflow Lobby; plus Scheduling, One-Way Interview, Assessment, Hosted Apply, Promote to Applicant, HCM Integration, I-9 Section 1, Document Push, Email, Pre-Qualification Questionnaire, Time Trigger. Hard-coded condition/trigger node types: filter, condition, followup_condition, waitedCondition, uiDecision, trigger, timeTrigger.

A Developer Portal activity is recognised by `meta.groupType` + `meta.iconKey`, rendered as `feature_activity`, and its side panel is built from `tabs` + `renderingSchema` (`FeatureActivityContent.tsx:15-68`).

## Decision guide for a product team

| Situation | Do this |
| --- | --- |
| The step is specific to your product journey | Build it as a Developer Portal activity |
| Many pods need the same step (e.g. Condition, Check consent as a generic rule) | Enhance the shared platform activity with AE |
| Options in a dropdown come from your service | Register an endpoint spec (AE), then use Dynamic + Abstract Data; prefer paging-capable endpoints |
| The step must call your backend at runtime | Simplest: HTTP API step in the execution flow via the proxy. Heavier or long-running: a Temporal worker on your task queue, registered in `async_activities` |
| The step must act on each item of a multi-select | Use a `for_loop` over the context list; the called endpoint can stay single-item |
| The step must wait | `waitBy` (fixed) or `waitedDecision` (until date / event) |
| You need a new trigger | Define the Kafka event + trigger with AE (`EVENT:all`, `TRIGGER:all`) |
| You need a new Automation Type, category or product value | DB change, AE team |
| You need to show your own UI inside AE | Not possible today; propose an MFE in `automation-engine-mfes` |

## Known limitations

* Activity-level Publish, Duplicate and Version Control are not implemented; Group and Internal activity types are "Coming Soon".
* Logic rules are enforced only in the Workflow Builder front end.
* No server-side validation of author input against the generated schema.
* No `date`, `code` or JSON-list field in the Builder menu.
* Dropdown data sources need an endpoint spec, which has no UI and no update path (an existing service is never overwritten, `EndpointSpecificationCrud.java:49-60`).
* Activity Library metrics are placeholders (Published and Usage always 0); status dot compares `'Published'` against `'PUBLISHED'`.
* Environment export/import does not cover activity-builder definitions.
* Workflow Builder palette groups by category only, not by product or automation type.
* Another pod cannot mount its own UI inside AE.
* Execution logs and KPIs require Doris to be configured.

## Context gaps (do not invent)

1. Automation Types, categories, product experiences and products are DB values; no list in code or in this repo.
2. Registered endpoint specifications (which services already have a proxy) are DB only.
3. Which roles hold `meta:write`, `EVENT:all`, `TRIGGER:all`, `activity_builder` is DB only.
4. The runtime (`automation-engine-core`) is not cloned; retry, idempotency and loop semantics at run time are inferred from the published config only.
5. The `orchestration-ai-engine` (policies, action registry) and the Action Center backend are not cloned.
6. AE team contacts and Slack channel: see `policies/platform-routing.md` (still placeholders).
