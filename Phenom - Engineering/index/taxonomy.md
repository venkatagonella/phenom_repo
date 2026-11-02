---
name: taxonomy
type: index
description: "Source of truth for how Phenom engineering repos are grouped in this workspace"
last_reviewed: 2026-07-20
---

# Engineering Taxonomy

This is the canonical grouping for everything under `repos/`. It's organized by **jobs-to-be-done**, not by engineering org chart — optimized for feasibility and product questions, not for how eng teams are staffed.

Every repo gets exactly **one primary home** below. If a repo is used by multiple pillars, note that in `index/repo-catalog.md` under "Also used by" rather than duplicating the clone.

## Pillars

### 1. Product Experiences
Everything around the candidate- and recruiter-facing job to be done of getting someone hired.

- **Screening** (`repos/product-experiences/screening/`) — screening questions/flows, assessment integrations. Everything before a candidate is scheduled for an interview (excluding campaigns — see Candidate Engagement).
- **Candidate Engagement** (`repos/product-experiences/candidate-engagement/`) — email/SMS campaigns, nurture, audience targeting, campaign execution and analytics (including campaign Storm topologies + `*-conf` deploy configs).
- **Interview Management** (`repos/product-experiences/interview-management/`) — interview scheduling, structured interviews (guides, scorecards), Interview Intelligence (recording, transcription, debrief).

### 2. Recruiter Hub
The CRM platform and CRM UI — the shared recruiter-facing shell that many other teams plug features into (job workspace, candidate profile, pipelines, navigation). If a feature question is "where does the recruiter see/configure this," start here.

  - Sub-folders under `repos/recruiter-hub/` (RX platform domains):
  - **`shell/`** — CRM host app (`cp_ui_app_2.0`)
  - **`config/`** — tenant config, feature flags
  - **`candidates/`** — candidate profile/list APIs + UI MFEs
  - **`jobs/`** — job workspace APIs + UI MFEs (+ **`crm-storm-job-pull`**: IX → CRM job ingest)
  - **`hrm/`** — Hiring Manager experience (jobs/profile APIs, accounts, gigs; HM email orchestration)
  - **`dashboard/`** — recruiter dashboard MFE
  - **`search/`**, **`pipeline/`**, **`projects/`** — Tier B
  - **`shared/`** — shared Maven libraries (`crm-commons`: departmentalization, Mongo/ES clients)
  - **`storm/`** — CRM Apache Storm libraries (candidate event processing, signals/score/automation confs)

### 3. Platform
Shared capabilities that other pillars build on top of. Not a product surface on its own.

- **Automations** (`repos/platform/automations/`) — two sub-folders:
  - **`workflow/`** — Automation Engine: cross-pod triggers, recipes, conditions, actions, pipeline state machine
  - **`crm-automations/`** — CRM-native automations: recipe runtime, Temporal workflows, CRM automation UI, recipe search
- **Messaging** (`repos/platform/messaging/`) — all notification/communication platform components: email, SMS, in-app, templates, delivery.
- **Privacy & Compliance** (`repos/platform/privacy-compliance/`) — consent, data retention, PII handling, audit, GDPR-type concerns.

## Placement rules

1. **One primary home per repo.** Pick by who owns the domain logic, not who renders the UI.
2. **UI shells that mount pod features → Recruiter Hub**, even if the feature logic lives in a pod repo (e.g. screening builder UI may live in `screening`, but the CRM shell that hosts it is Recruiter Hub).
3. **Cross-cutting infra (config, feature flags, integrations, analytics) → not yet assigned.** Default to `platform/` and flag in `repo-catalog.md` as "needs pillar decision" rather than guessing.
4. When unsure, log the repo under the closest pillar in `repo-catalog.md` with a note — don't block cloning on a perfect taxonomy fit.

## Rollout order

Repos are being onboarded in this order (see `repo-catalog.md` for live status):

1. Recruiter Hub (CRM repos)
2. 🚧 **Interview Management** (scheduling + II) — **12 repos cloned** (see `repo-catalog.md`)
3. 🚧 **Screening** — **6 repos cloned** (assessment/video)
4. 🚧 **Candidate Engagement** — **5 repos cloned** (campaign stack)
5. Everything else, as feasibility questions come up
