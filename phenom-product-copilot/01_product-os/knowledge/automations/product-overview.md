# RX Automations — Product Overview

Last enriched: 2026-09-25 (from CUSP + PHEM + Confluence; not yet a PM-reviewed source of truth)

## What Exists Today

**RX** = Recruiter Experience. **RX Automations** is the Platform pod that owns:

* **CRM Automations** — recipe builder: Trigger → Conditions → Actions in CRM (PO: Syed Naqvi)
* **Automation Engine (AE)** — Policy & Rule Engine, Workflow Builder, Developer Portal / Action Center (lead: Tulasi Pinnaka)

Goal: automate repetitive recruiter work (status changes, messaging, screening invites, forwarding, tagging, HVH FastTrack flows) without manual steps.

CUSP product field: `Product Experience : Product` = **CRM - Automation** (`customfield_15211`).

## Recipe model

Trigger → Conditions → Actions.

**Shipped actions / capabilities (with engineering evidence):**

| Capability | Evidence | Notes |
| --- | --- | --- |
| WhatsApp as a CRM recipe action ("WhatsApp Candidate", opt-in gated) | PHEM-1348379 Done, fixVersion 26.02 | CUSP-4981 still open; also linked to PHEM-605974 in PM Acceptance Queue — **verify GA before closing feedback** |
| Send Email to any recipient (non-candidate) — static address + field-driven | PHEM-2114070 / PHEM-2127654 Done (Aug 2026) | **Out of scope: role-based** (Hiring Manager, Recruiter, Interviewer on the req). Remaining gap kept on CUSP-5393 |
| Disposition/rejection reasons from master-list API | PHEM-2219937 Done | Distinct from "trigger on decline reason" (CUSP-7040) — verify overlap |
| FastTrack status as a native CRM Automations trigger | PHEM-305002 Done | PRD also listed as In Stg |
| Template Gallery (Events + Applicants templates) | Confluence Automation Template Gallery | |
| Temporal orchestration (Storm → Temporal) | PHEM-27515 Done | |

**Supported CRM actions (as quoted on FastTrack PRD / PHEM-305002):** Update Hiring Status, Send OWI Invite, Assign to Job, Email/SMS/Preferred Channel, Add to Campaign/TC, Modify fields, Forward profile, Invite Interview/Screening.

## Adjacent surfaces

* AE Developer Portal is where PODs build their own AE activities ([developer-portal.md](developer-portal.md)).
* Recruiter Hub is where recruiters see and override automation outcomes ([knowledge/recruiter-hub](../recruiter-hub/product-overview.md)).
* Screening, Scheduling, and HVH FastTrack consume recipe triggers/actions.
* Hiring Automations (Cassie Dunn) is adjacent, not this pod.

## Known Limitations

* Recipes are siloed: Profile→Profile, Project→Project, Job→Job (CUSP-7334).
* Add Tag exists as an action; Remove Tag does not (keeper CUSP-6399).
* Conditions are AND-only; no OR (keeper CUSP-5684).
* "Assigned to job" often ignores AI Discovery / lists / projects (keeper CUSP-5861).
* Analytics is aggregate, not per-recipe (keeper CUSP-7360).
* Failures are silent unless someone checks audit (keeper CUSP-6926).
* List / membership triggers only evaluate candidates added *after* the recipe is created — no bulk-apply for pre-existing list members (CUSP-7450).
* No Then action to Assign Candidate to Event after Assigned to Job (or similar); hiring-event applicants need manual event assignment today (CUSP-7543).
* Automation audit log has no export; customers must review in-product (CUSP-7565). Related: audit search-by-email (CUSP-6957) and per-recipe analytics (CUSP-7360) remain separate asks.
* Forward-to-HM sends all historical documents, not the current application (keeper CUSP-5184; epic PHEM-2125738).

## Context gaps (do not invent)

Call these out in any triage until a file exists and is PM-reviewed:

1. **No canonical inventory of current triggers / conditions / actions** in this repo or in Confluence (PM "Creating Trigger/Action/Condition" pages are stubs).
2. **No filled RX Automations roadmap page** — Confluence Product Discovery Roadmap is empty; Product Roadmap & Releases is a Google deck link only.
3. **No adoption / ROI benchmarks** in this repo (unlike Screening).
4. **WhatsApp GA is contradictory** — PHEM-1348379 Done vs PHEM-605974 still PM Acceptance Queue.
5. **`policies/platform-routing.md`** still has placeholder AE PM / Slack / docs (`_[AE PM]_`).
6. **~35 CUSP tickets** tagged CRM - Automation are actually bulk import/export/profile UX (mis-tags).
7. **"EC Trigger"** (CUSP-7454) — term not defined in this repo; confirm with CRM Automations before treating as recipe-builder vs Event Capture UX.

When a gap is closed, delete the matching bullet here and add the fact above.
