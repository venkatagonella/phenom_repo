---
name: automations
type: index
description: "Domain index for Platform → Automations — Automation Engine (workflow) and CRM Automations"
pillar: Platform
last_reviewed: 2026-07-10
---

# Platform → Automations

## Scope

Two related but distinct automation stacks under `repos/platform/automations/`:

| Sub-folder | What it is | When to start here |
|------------|------------|-------------------|
| **`workflow/`** | Automation Engine (AE) — cross-pod workflow builder, recipes, triggers, actions, pipeline state machine | "Can we auto-advance when X?", workflow builder UI, pod trigger/action registration |
| **`crm-automations/`** | CRM-native automations — recipe execution, Temporal workflows, CRM automation UI, recipe search/filter | CRM-specific automation recipes, templates, reminder jobs, LinkedIn/resume sync workflows |

Both share Platform dependencies (Messaging for send actions, Recruiter Hub for UI mount points). For cross-pod AE questions, start in **`workflow/`**; for CRM recipe runtime/UI, start in **`crm-automations/`**.

---

## Automation Engine — Workflow (`workflow/`)

Cross-pod Automation Engine: triggers, recipes, conditions, actions, scheduled tasks, hiring pipeline state transitions.

| Repo | Purpose | Start here |
|------|---------|------------|
| `automation-ui-2` | Main AE UI — workflow builder, recipe editor, automation central, developer portal | `src/routes/definitions.tsx` → `src/pages/WorkflowDashboard`, `src/pages/VerticalEditor/` |
| `automation-service-2` | Backend for workflow config, triggers, actions, versioning, audience validation, analytics | `AutomationServiceApplication.java`, `controllers/AsyncWorkFlowController.java`, `controllers/AutomationEntityController.java` |
| `automation-engine-mfes` | MFE monorepo (action center, policy engine) — **use `develop` branch** | `apps/`, `packages/`, `ARCHITECTURE.md` |
| `action-centre` | Action center backend — **use `action-center-dev-2` branch** | `ActionCentreApplication.java`, `ae-action-centre-domain/` |
| `ae_statesmith` | Hiring pipeline state machine — **use `auto-transitions` branch** | `StatesmithApplication.java`, `controllers/ApplicationController.java` |

### Common feasibility patterns (Workflow)

- "Can we auto-advance/auto-reject when X happens?" → `automation-service-2` (`controllers/AutomationEventController.java`, `controllers/AutomationEntityController.java`)
- "Can we schedule a follow-up N days later?" → scheduled task pattern in workflow definitions (`models/` + `services/` in `automation-service-2`)
- "Where is the workflow builder UI?" → `automation-ui-2` (`src/pages/VerticalEditor/`, `src/pages/WorkflowDashboard`)
- "How do pods register triggers/actions?" → `automation-service-2/controllers/AutomationFeaturesController.java`, `AutomationListDefinitionController.java`

---

## CRM Automations (`crm-automations/`)

CRM-native automation runtime: recipe CRUD, Temporal workflow execution, automation templates, recipe search/filter, CRM automation UI.

| Repo | Purpose | Start here |
|------|---------|------------|
| `crm-automation-service` | Core CRM automation backend — recipe CRUD, templates, reminder jobs, Temporal activity workers (screening, notifications, interview invite, HRM forward, audit log) | `CrmAutomationServiceApplication.java`, `controllers/AutomationController.java`, `controllers/TemplateController.java`, `temporal/activity/` |
| `crm-workflows` | CRM Temporal workflow definitions — LinkedIn project sync, resume sync, Kafka-driven workflow broker | `CrmWorkflowsApplication.java`, `linkedin/`, `helpers/WorkflowUtils.java` |
| `crm-automations-ui` | CRM Automations Angular UI (recipe builder/config surfaces) | `src/app/`, `angular.json` |
| `automation-search-service` | Recipe/filter search service — Lucene indexing, filter config cache, Temporal filter activities, Kafka consumer | `AutomationSearchService.java`, `lucene/LuceneSearchService.java`, `controller/AdminController.java` |
| `crm-automation` | **QA / E2E only** — not the production backend (`crm-automation-service`). Playwright + Robot Framework test suites | `RF_Automation_CRM/`, `PlayWright_TestAutomation/` |

### Common feasibility patterns (CRM Automations)

- "How does a CRM automation recipe execute?" → `crm-automation-service` (`controllers/AutomationController.java`, `temporal/activity/`)
- "Where is the CRM automation UI?" → `crm-automations-ui`
- "How are automation recipes searched/filtered?" → `automation-search-service` (`lucene/`, `temporal/AutomationFilterActivityImpl.java`)
- "LinkedIn / resume sync automation workflows" → `crm-workflows`
- "E2E test coverage for CRM automations" → `crm-automation` (QA repo only — see manifest)

> **Naming trap:** `crm-automation` (QA tests) vs `crm-automation-service` (production backend). For any feasibility question, start with **`crm-automation-service`**. Full manifests: `index/repos/crm-automations/`.

---

## Platform dependencies

- **Messaging** — automation actions that send email/SMS route through Platform → Messaging repos
- **Recruiter Hub** — AE UI and CRM Automations UI mounted inside the CRM shell (`cp_ui_app_2.0`)
- **Product Experiences pods** — recipe consumers (Screening, Interview Management, Candidate Engagement) triggered via Workflow or CRM automation activities

## Eng contacts

_Fill in once confirmed with Automation Engine / CRM Automations team._
