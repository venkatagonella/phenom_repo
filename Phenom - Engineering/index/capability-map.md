---
name: capability-map
type: index
description: "Bridges product/Jira capability language (from platform-routing.md) to this workspace's engineering pillars and repos"
last_reviewed: 2026-07-10
---

# Capability Map

`Phenom - Product Copilot/policies/platform-routing.md` is the source of truth for **which platform team to contact**. This file maps those same capabilities to **where the code lives in this workspace**, so feasibility questions can go straight to the right repos.

| Capability (platform-routing.md) | Engineering pillar / sub-domain | Repo folder |
|-----------------------------------|----------------------------------|-------------|
| Automation Engine | Platform → Automations → Workflow | `repos/platform/automations/workflow/` — start with `automation-service-2` (backend), `automation-ui-2` (UI) |
| Notifications / Messaging Platform | Platform → Messaging | `repos/platform/messaging/` — start with `crm-messaging-platform` (modern multi-service platform), `candidates_email_microservice`, `candidates-sms-services`, `candidates-notifications` |
| Scheduling Platform | Product Experiences → Interview Management | `repos/product-experiences/interview-management/` — start with `scheduling-main-app` (core API), `phenom-internal-calendar` (availability), `scheduling-orchestration` (Temporal workflows), `scheduling-rule-parser` (RRule) |
| Interview Intelligence | Product Experiences → Interview Management | `repos/product-experiences/interview-management/` — start with `interview-management-service` (core IMS), `evaluation-service` (scorecards), `meeting-bot-orchestrator` (virtual recording), `interview-management-ui` (MFE) |
| Unified Candidate Experience | Product Experiences (Screening and/or Interview Management, depending on funnel stage) | `repos/product-experiences/` |
| CIM / Career Site | Not yet cloned — closest fit is Product Experiences → Screening (pre-CRM, candidate-facing) | _unassigned_ |
| Talent Analytics | Not yet cloned — see `repo-catalog.md` unassigned section | _unassigned_ |
| Integration Experience | Not yet cloned — likely Platform (shared connector layer) | _unassigned_ |
| Platform Config | Platform (feature flags, tenant settings) — may warrant its own sub-domain once repos are added | `repos/platform/` |

## Not in platform-routing.md yet

| Capability | Engineering pillar / sub-domain | Repo folder |
|------------|----------------------------------|-------------|
| CRM platform / CRM UI shell | Recruiter Hub | `repos/recruiter-hub/` |
| Screening questions, knockout logic, assessment integrations | Product Experiences → Screening | `repos/product-experiences/screening/` |
| Campaigns / candidate nurture | Product Experiences → Candidate Engagement | `repos/product-experiences/candidate-engagement/` — start with `candidates-email-campaign` (campaign API), `crm-campaigns-v2` (v2 engine: segmentation, scheduling, Spark/Kafka), `storm-campaign`/`crm-storm-transactions` (+ `*-conf`) for event tracking & analytics |
| IX job sync into CRM / hiring team on ingest | Recruiter Hub → jobs | `crm-storm-job-pull` (**`release_*`**) + `crm-storm-job-pull-conf`; job APIs still `crm-jobs-service` |
| Hub profile / apply / ATS streaming | Recruiter Hub → storm | `storm-candidates` + `storm-candidates-conf`; signals/fit-score/automation → matching `*-conf` until runtimes cloned |
| Hiring Manager experience / emails to HMs | Recruiter Hub → hrm | `hrm-jobs-api` + `hrm-profile-api`/`hrm-profile-service` (forward/feedback); `hrm-gigs-api` (gig manager emails); `hrm-accounts-api` (identity); delivery via Messaging |
| CRM automations / recipe runtime | Platform → Automations → CRM Automations | `repos/platform/automations/crm-automations/` — start with `crm-automation-service` (recipe CRUD + Temporal activities), `crm-automations-ui` (UI), `automation-search-service` (recipe search) |
| Structured interview guides / scorecards | Product Experiences → Interview Management | `repos/product-experiences/interview-management/` — `interview-management-service` (guides), `evaluation-service` (scorecards/evaluations) |
| Privacy, consent, retention, PII, audit | Platform → Privacy & Compliance | `repos/platform/privacy-compliance/` |

## How to use this for a feasibility question

1. Identify the capability keyword(s) in the question.
2. Look it up here to find the primary repo folder(s).
3. Read the matching domain file in `index/` (e.g. `index/product-experiences/screening.md`) for entry points before searching code.
4. If it spans pillars (e.g. "notify recruiter when auto-screening completes"), check every matching row — most cross-pillar features touch **Automations** and/or **Messaging**.
5. If nothing matches, add it to `repo-catalog.md` → "Unassigned" rather than guessing a home.
