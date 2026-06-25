---
name: crm-core-product
description: >-
  Phenom CRM Core product scope, personas, and capability mapping for PRD/FRD
  authoring. Use when mapping customer problems to CRM Core features, deciding
  in-scope vs dependency, or naming story prefixes for Recruiter Experience CRM.
---

# CRM Core Product Context

Reference when authoring FRDs for **Phenom CRM Core** (Recruiter Experience / CRM - Core). Helps map customer problems to product capabilities without conflating adjacent pods.

## Product identity

| Field | Value |
|-------|-------|
| Jira team | Recruiter Experience (RX) / CRM - Core |
| Story prefix | `Core` |
| Jira product field | `CRM - Core` |
| Customer KB | kb_id `3` — see `../product-copilot-beta/skills/vanilla-kb.md` |

## Primary scope (in-scope for this workspace)

| Capability area | What it covers | Example customer problems |
|-----------------|----------------|----------------------------|
| **Pipeline** | Stages, views, candidate movement, pipeline config | "Can't see all candidates in a stage", "Stage rules wrong" |
| **Sourcing** | Talent pools, search, re-engagement, contact management | "Can't find past applicants", "Pool is stale" |
| **Requisitions** | Job linkage, req setup, hiring team on req | "CRM not linked to right job", "Wrong req on candidate" |
| **Communication** | Outreach initiated from CRM (not full messaging platform) | "Can't email from pipeline view" |
| **Organization** | Tags, filters, saved views, lists, bulk actions | "Can't tag in bulk", "Filter doesn't save" |
| **Automation** | CRM-side rules and triggers | "Auto-move on tag not working" |
| **Evaluation** | Scorecards and evaluation access within CRM | "Can't see HM scorecard in CRM" |

## Adjacent areas (dependencies — not primary unless problem requires)

| Pod | When it appears in FRD |
|-----|------------------------|
| CRM - Messaging | Campaigns, templates, send infrastructure beyond CRM-initiated outreach |
| CRM - Profile | Candidate profile UI, unified profile data |
| CRM - Automation | Cross-product automation engine integration |
| Scheduling | Interview scheduling from CRM context |
| Screening | Screening stage handoff from CRM |
| Automation Engine | Platform-wide automation vs CRM-local rules |
| Platform | Auth, permissions, APIs, shared services |

List these in **Part D Cross-Team Dependencies**, not as CRM Core scope unless the customer problem is explicitly in that pod.

## Personas

| Persona | Typical goals in CRM Core FRDs |
|---------|-------------------------------|
| **Recruiter** | Pipeline management, candidate communication, evaluation |
| **Sourcer** | Search, pools, tagging, re-engagement |
| **Recruiting Ops** | Configuration, automation rules, reporting on pipeline health |
| **CRM Admin** | Stage config, permissions, org-wide tags/filters |
| **Hiring Manager** | Limited — usually dependency on Profile/Evaluation pods |

## Mapping customer problem → capability

When writing Part B:

1. Identify which **capability area** addresses each related problem
2. Check **Existing vs. New** table — does CRM Core already partially solve this?
3. If gap is in adjacent pod → Part D dependency, not Part B CRM Core feature
4. Use `search_kb` (kb_id `3`) for customer-facing behavior when unsure what exists today

## Story naming

```
Core – FE – [UI/workflow change]
Core – BE – [API/service/data change]
```

Create separate FE and BE stories when both are needed (`jira-story-rules`).

## What not to do

- Do not label Scheduling/Screening bugs as CRM Core scope without analysis
- Do not propose net-new platform infrastructure in CRM Core FRD without Platform dependency
- Do not assume feature exists — verify via inputs or KB search

## Related skills

- **prd-authoring** — FRD structure
- **write-stories-from-problem** — story derivation from Part A
- **create-prd** — full workflow
