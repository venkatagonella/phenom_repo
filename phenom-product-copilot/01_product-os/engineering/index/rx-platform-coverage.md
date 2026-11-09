---
name: rx-platform-coverage
type: index
description: "RX (Recruiter Experience) platform scope — what the CRM shell integrates, what's cloned, and priority gaps"
last_reviewed: 2026-07-13
---

# RX Platform Coverage

**RX (Recruiter Experience)** is the recruiter-facing CRM product. In engineering terms it is **`cp_ui_app_2.0`** (shell) plus **MFE repos** (`crm-*-ui`) and **hub API services** routed through `crm-hub`. Sub-experiences (Automations, Messaging, Campaigns, Scheduling, II) live in other taxonomy pillars but mount into RX — that split is intentional.

## Audit tooling

Refresh clone vs Bitbucket status:

```bash
cd engineering
set -a && source .env && set +a
python3 scripts/bitbucket-rx-audit.py
python3 scripts/bitbucket-rx-audit.py --json > /tmp/rx-audit.json
```

Source: Bitbucket workspace `phenompeople` (API), cross-checked against `cp_ui_app_2.0` hub routes + `mfe.config.ts`.

## What's cloned today (RX-relevant)

Layout: `repos/recruiter-hub/{shell,config,candidates,jobs,dashboard,search,pipeline,projects}/`.

| Repo | Path | Role in RX |
|------|------|------------|
| `cp_ui_app_2.0` | `shell/` | CRM shell — hosts all MFEs, routing, shared services |
| `crm-config-service` | `config/` | Feature flags, hiring pipeline config |
| `crm-recruiter-dashboard` | `dashboard/` | Dashboard MFE |
| `crm-candidate-lists` | `candidates/` | Lists backend (hub path: `/lists/`) |
| `crm-candidates-ui` | `candidates/` | Profile MFE _(Tier A — cloned)_ |
| `candidates-api` | `candidates/` | Core candidate backend _(Tier A — cloned)_ |
| `candidates-microservice` | `candidates/` | Edit profile, merge, bulk ops _(Tier A — cloned)_ |
| `hrm-profile-api` | `hrm/` | HRM profile edge _(moved from candidates/; + `hrm-profile-service`, jobs/accounts/gigs)_ |
| `crm-jobs-ui` | `jobs/` | Job workspace MFE _(Tier A — cloned)_ |
| `crm-jobs-service` | `jobs/` | Jobs backend _(Tier A — cloned; checkout **`pre-develop`**, not `main`)_ |

| `crm-hiring-status-service` | `pipeline/` | Hiring status / pipeline _(Tier B — cloned)_ |
| `crm-profile-search-service` | `search/` | Profile search _(Tier B — cloned)_ |
| `crm-domain-search-service` | `search/` | Domain search backend _(Tier B — cloned)_ |
| `crm-filters-ui` | `search/` | Filters MFE _(Tier B — cloned)_ |
| `cp-facet-2.0` | `search/` | Legacy `facets2` search/facet execution monolith — candidate/job/global/boolean search, spotlight, dashboard widgets, tags/notes search, gigs, projects, segments _(cloned 2026-07-13; checkout **`release-patch`**, not `master`)_ |
| `crm-lists-ui` | `candidates/` | Lists MFE _(Tier B — cloned)_ |
| `crm-settings-service` | `config/` | CRM settings API _(Tier B — cloned)_ |
| `notes-service` | `candidates/` | Notes API _(Tier B — cloned)_ |
| `tags-service` | `candidates/` | Tags API _(Tier B — cloned; checkout **`master`**, not `main`)_ |
| `crm-projects-ui` | `projects/` | Projects MFE _(Tier B — cloned)_ |


**Integrated sub-experiences (cloned elsewhere):** `crm-automations-ui`, `crm-messaging-platform`, `candidates-notifications`, campaign stack, scheduling/II MFEs, etc.

## Hub path → Bitbucket slug (non-obvious mappings)

| Hub path (in shell) | Bitbucket repo |
|---------------------|----------------|
| `jobs-api` | `crm-jobs-service` |
| `microservice-api` | `candidates-microservice` |
| `notes-api` | `notes-service` (UI: `crm-notes-ui`) |
| `crm-search-service` | `crm-domain-search-service` |
| `facets2` | `cp-facet-2.0` |
| `lists` | `crm-candidate-lists` |

## Priority clones for RX platform coverage

### Tier A — core candidate + job domain (clone first)

| Slug | Why |
|------|-----|
| `crm-candidates-ui` | Profile, edit profile, candidate list/table MFE |
| `candidates-api` | Core candidate backend |
| `crm-jobs-ui` | Job workspace MFE |
| `crm-jobs-service` | Jobs backend |
| `hrm-profile-api` | HRM profile edge (+ suite under `hrm/`) |
| `candidates-microservice` | Edit profile, merge, bulk tag ops |

### Tier B — search, pipeline, lists UI, settings ✅ cloned 2026-07-12

| Slug | Why |
|------|-----|
| `crm-hiring-status-service` | Pipeline / hiring status |
| `crm-profile-search-service` | Profile search |
| `crm-domain-search-service` | CRM search backend |
| `crm-filters-ui` | Filters/facets UI |
| `crm-lists-ui` | Lists UI (pairs with `crm-candidate-lists`) |
| `crm-settings-service` | CRM settings |
| `notes-service` | Notes API |
| `tags-service` | Tags |
| `crm-projects-ui` | Projects |

### Tier C — supporting / cross-cutting

| Slug | Why |
|------|-----|
| `crm-gdpr` | Privacy in CRM |
| `crm-global-search-ui` | Global search MFE |
| `crm-data-access-layer` | Shared data access |

## RX-named Bitbucket repos (different concern)

Repos with `rx` in the name are mostly **search/analytics/data** infrastructure, not the CRM UI shell:

- `rx-search-monorepo`, `rx-data-sync`, `rx-commons`, `spx-rx-search-utils`, etc.

Use these for search/metrics feasibility — not for profile UI or candidate CRUD.

## RX integration map (conceptual)

```
cp_ui_app_2.0 (shell)
├── MFEs: crm-candidates-ui, crm-jobs-ui, crm-lists-ui, crm-automations-ui, …
├── Hub APIs: candidates-api, crm-jobs-service, crm-config-service, …
└── Sub-experiences (other pillars, mounted in RX):
    ├── Platform → Automations (crm-automation-service, crm-automations-ui)
    ├── Platform → Messaging (crm-messaging-platform, notifications)
    ├── Candidate Engagement (campaigns UI/API)
    └── Interview Management (scheduling/II MFEs)
```

## Next steps

1. ~~Add Tier A repos to `scripts/repos.yaml` under `recruiter-hub/` sub-folders~~ ✅
2. ~~Run `./scripts/sync-repos.sh` for Tier A~~ ✅ (6 repos cloned; audit confirms 0 Tier A gaps)
3. ~~Tier B — add to `repos.yaml` and clone (`search/`, `pipeline/`, `projects/`, settings, notes, tags)~~ ✅ (9 repos cloned 2026-07-12)
4. ~~**`crm-jobs-service`:** checkout integration branch~~ ✅ local branch **`pre-develop`** (863 files; `main` = 3 files, `development` = skeleton)
5. ~~**Manifests deferred:** build Recruiter Hub manifests (`index/repos/recruiter-hub/`) after Tier B skim — same pattern as CRM Automations pilot~~ ✅ 19 repo manifests + `capability-index.md` built 2026-07-12
6. Index Tier A + Tier B in `repo-catalog.md` — 🟡 rows added; promote → 🟢 after deeper pass
7. **`tags-service`:** keep **`master`** checked out locally (`main` is stub-only)
