---
name: recruiter-hub
type: index
description: "Domain index for Recruiter Hub repos — the CRM platform and CRM UI shell"
pillar: Recruiter Hub
last_reviewed: 2026-07-20
---

# Recruiter Hub

## Scope

The CRM platform and CRM UI — the shared recruiter-facing shell (RX) that most other pods mount features into:
- Job workspace, candidate profile, pipelines
- Navigation, search, filters, shared list/table components
- Core CRM domain services (jobs, candidates, applications, users) that other pillars read from or write to
- Shared libraries (departmentalization / scope ACL, Mongo/ES clients)

This is usually the **first place to check** for "where does the recruiter see/configure this" questions, even if the underlying feature logic lives in a pod repo (Screening, Interview Management, etc.).

## Repo manifests

**Use [`index/repos/recruiter-hub/capability-index.md`](repos/recruiter-hub/capability-index.md) before grepping `repos/recruiter-hub/`.** Cloned repos have curated manifests under `index/repos/recruiter-hub/` — purpose, capabilities, entry points, integrations, and search hints per repo, grouped by sub-folder (shell, config, candidates, jobs, **hrm**, dashboard, search, pipeline, projects, shared, storm).

## Folder layout (`repos/recruiter-hub/`)

| Sub-folder | Repos | Notes |
|------------|-------|-------|
| **`shell/`** | `cp_ui_app_2.0` | RX host — MFE federation |
| **`config/`** | `crm-config-service`, `crm-settings-service` | Feature flags, tenant config, CRM settings API |
| **`candidates/`** | `crm-candidates-ui`, `candidates-api`, `candidates-microservice`, `crm-candidate-lists`, `crm-lists-ui`, `notes-service`, `tags-service` | Profile, lists, notes, tags |
| **`jobs/`** | `crm-jobs-ui`, `crm-jobs-service`, `crm-storm-job-pull` (+ conf) | Job workspace + IX job ingest |
| **`hrm/`** | `hrm-jobs-api`, `hrm-jobs-service`, `hrm-profile-api`, `hrm-profile-service`, `hrm-accounts-api`, `hrm-gigs-api` | Hiring Manager experience; HM email orchestration |
| **`dashboard/`** | `crm-recruiter-dashboard` | Landing MFE |
| **`search/`** | `crm-profile-search-service`, `crm-domain-search-service`, `crm-filters-ui`, `cp-facet-2.0` | Profile/domain search, filters MFE, legacy `facets2` search monolith |
| **`pipeline/`** | `crm-hiring-status-service` | Hiring status / pipeline config |
| **`projects/`** | `crm-projects-ui` | Projects MFE |
| **`shared/`** | `crm-commons` | Shared Maven libraries (departmentalization, Mongo/ES clients) — not a deployable service |
| **`storm/`** | `storm-candidates`, `*-conf`, `storm-integrations` | CRM Apache Storm (candidate events, signals/score/automation confs) |

Mounted in RX but cloned elsewhere: **Automations** → `platform/automations/crm-automations/`, **Messaging** → `platform/messaging/`, **Campaigns** → `product-experiences/candidate-engagement/`.

## Key repos

See `index/repo-catalog.md` for full stack/status/"also used by" detail.

| Repo | Purpose | Start here |
|------|---------|------------|
| `cp_ui_app_2.0` | CRM UI shell — hosts micro-frontends | `src/app/app.module.ts`, `src/app/crm-mfe/` |
| `crm-config-service` | Tenant configuration, feature flags | `config-application` module |
| `crm-candidates-ui` | Candidate profile MFE | `src/app/modules/candidates/profile/` |
| `candidates-api` | Candidate CRUD API | `CandidateController.java`, `CandidateOperationsController.java` |
| `candidates-microservice` | Merge, bulk ops | `CandidateOperationsController.java` |
| `crm-jobs-ui` / `crm-jobs-service` | Job workspace UI + backend | `jobs-routing.module.ts` / `ReqCreationController.java` on **`pre-develop`** |
| `crm-storm-job-pull` | **IX → CRM job ingest** + hiring-team sync | `JobPullTopology.java` on **`release_25_02`** |
| `hrm-jobs-api` / `hrm-jobs-service` | HRM jobs (Play edge + Spring) — **emails to HMs** live primarily in jobs-api / profile-* | `SendEmailServices.java` / `PostUpdateActionsService.java` |
| `hrm-profile-api` / `hrm-profile-service` | HRM forward-to-HM + profile orchestration (edge → service when new pipeline) | `ForwardProfileService.java` / `ForwardCandidatesService.java` |
| `hrm-accounts-api` | HRM identity / auto-provision | `AutoProvisionController.java` |
| `hrm-gigs-api` | HRM gigs + manager gig emails | `GigServices.java`, `SendEmailServices.java` |
| `storm-candidates` | Hub profiles / apply / ATS Storm monolith | `KafkaTopology.java`, `EventProcessorBolt.java` |
| `crm-candidate-lists` | List/filter/export backend | `ListController.java`, `FilterController.java` |
| `crm-recruiter-dashboard` | Recruiter dashboard MFE | `src/app/modules/recruiter-dashboard/` |
| `crm-commons` | Shared RX lib — **departmentalization / scope / CBAC**, Mongo+ES clients | `DepartmentalizationManagerV2.java`, `ScopeBuilder.java` — branch **`release`** |

## Common feasibility patterns

- **Add a field to the candidate/job profile** → start here (data model + UI), then check which pod owns the underlying data if it's not native CRM data.
- **New recruiter-facing setting or toggle** → check for an existing settings/config pattern before assuming new plumbing is needed.
- **Feature X should show up in the CRM UI** → find the mount point / extension pattern other pods use (e.g. how Screening or Interview Management panels are embedded) rather than building a new integration point.
- **Permissions / role-based visibility** → Recruiter Hub usually owns the role model; confirm before assuming a pod repo needs its own permission logic.
- **Why can't this recruiter see this job/candidate?** → start with **`crm-commons`** (departmentalization `scopeAttr`, CBAC, `jobsHiringTeam` visibility), then the search consumer (`cp-facet-2.0` / domain-search) and job hiring team on `crm-jobs-service`.
- **How do IX jobs land in CRM / hiring team get populated on ingest?** → **`crm-storm-job-pull`** (`release_*`) + `crm-storm-job-pull-conf`; not the legacy `storm-candidates` `JobpullTopology`.
- **Emails to hiring managers (forward profile, get feedback)?** → **`hrm-jobs-api`** + **`hrm-profile-api`/`hrm-profile-service`** (new pipeline); transport via Messaging (`crm-emailservice`). Gig manager emails → `hrm-gigs-api`.
- **Hub profile / apply / ATS event processing** → **`storm-candidates`** (+ conf); signals/fit-score/automation Storm lanes → corresponding `*-conf` until runtime JARs are cloned.

## Platform dependencies

- **Automations** — recipes configured/triggered from CRM UI
- **Messaging** — notification preferences UI, in-app notification surface
- **Privacy & Compliance** — access controls, audit logging of recruiter actions
- Consumed by nearly every Product Experiences feature as the UI host

## Eng contacts

_Fill in once known — team name, PM, Slack channel. Note: many teams contribute to this shell, so there may be multiple contacts depending on the module._
