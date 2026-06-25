---
name: prd-authoring
description: >-
  Authors CRM Core PRDs and functional specs using problem-first framing.
  Use when writing a PRD, product requirements document, functional spec,
  feature spec, or iterating on specs in the SpecDrivenDev workspace.
---

# PRD Authoring — CRM Core

Author review-ready **Functional Requirements Documents (FRDs)** for **Phenom CRM Core**. Users may say "PRD" — treat as FRD alias.

## Structural authority

Section segregation follows **`../product-copilot-beta/policies/jira-story-rules.md`** (quality checklist and AC rules) and **`../product-copilot-beta/policies/templates/story.md`** (per-story block structure). Epic-level content aligns with **`../product-copilot-beta/policies/templates/epic.md`**.

| Part | Content | Segregation rule |
|------|---------|------------------|
| **Part A — Initiative / Epic** | Source Inputs, Executive Summary, Customer Issue, **Problem Breakdown**, Goals & Success Metrics | **No proposed solutions** |
| **Part B — What Should Be Done** | Solution Overview, User Stories table, Functional Requirements list | **No customer pain restatement** — reference Part A |
| **Part C — Requirement / Story Blocks** | One block per FR/story: User Story, Background, AC (Given/When/Then), Out of Scope, Design, Technical Notes, Open Questions | **What + how to verify** — not customer problem |
| **Part D — Initiative Wrap-Up** | Cross-Team Dependencies, Release Plan, Assumptions, Appendix | Initiative-level only |

**Never mix customer issue and proposed solution in the same section.**

## Output

| Item | Location |
|------|----------|
| Template | `templates/frd-template.md` |
| Output file | `specs/{initiative-slug}/frd.md` |
| Status | `Draft` until reviewed |

**Slug rules:** kebab-case; prefer customer or problem name over solution name (e.g. `globalco-bulk-tagging`).

## CRM Core scope

Primary capabilities — map Part B requirements here before proposing net-new work:

| Area | Examples |
|------|----------|
| Pipeline | Stage config, pipeline views, candidate movement |
| Sourcing | Talent pools, search, re-engagement |
| Requisitions | Job linkage, req setup, hiring team context |
| Communication | Outreach and messaging from CRM |
| Organization | Tags, filters, saved views, list management |
| Automation | CRM-side rules and triggers |
| Evaluation | Scorecards and evaluation access |

Adjacent pods (Messaging, Profile, Automation) and products (Scheduling, Screening) are **dependencies**, not primary scope unless the customer problem requires them.

## Authoring workflow

```
Task Progress:
- [ ] Gather inputs (spec-inputs or spec-from-jira if applicable)
- [ ] Copy segregated structure from templates/frd-template.md
- [ ] Fill Part A (customer issue only), then Part B (solution only)
- [ ] Write one Part C block per FR/story deliverable
- [ ] Complete Part D wrap-up
- [ ] Mark status Draft; run review checklist
```

### Writing standards

- **Segregate strictly** — Part A = problem; Part B = solution summary; Part C = testable story blocks; Part D = initiative wrap-up
- **Be specific** — name roles, screens, workflows; avoid vague "improve UX"
- **Preserve customer voice** — quote or paraphrase in Part A Customer Requirements (as stated)
- **Quantify when possible** — volume, frequency, time lost, deal impact
- **Flag uncertainty** — Open Questions in Part C blocks and Part D, not guesses
- **Stay scoped** — one problem per FRD; split large asks into phased specs

### Review checklist

Before presenting as stakeholder-ready:

- [ ] Source Inputs table lists all Jira keys and documents used
- [ ] Part A Problem Breakdown lists related problems and customer asks (Step 2)
- [ ] Part A contains no proposed solutions or feature descriptions
- [ ] Part B contains no customer pain restatement (references Part A instead)
- [ ] Part B Functional Requirements state only what should be done
- [ ] Each Part C block has a User Story (Who / What / Why)
- [ ] Each Part C block has 3–5 Given/When/Then scenarios per `jira-story-rules`
- [ ] Each Part C block has Out of Scope filled in
- [ ] Measurable success metrics in Part A Goals & Success Metrics
- [ ] Open questions with owners (per Part C block and initiative-level in Part D)
- [ ] Cross-team dependencies identified in Part D
- [ ] Assumptions separated from confirmed facts in Part D

## Downstream pipeline (when requested)

```
LOCAL FRD → CONFLUENCE → JIRA EPIC → STORIES → DEVELOPMENT
```

| Need | Location |
|------|----------|
| Story structure & AC rules | `../product-copilot-beta/policies/jira-story-rules.md` |
| Story template | `../product-copilot-beta/policies/templates/story.md` |
| Epic template | `../product-copilot-beta/policies/templates/epic.md` |
| Full PRD format & pipeline | `../product-copilot-beta/skills/prd.md` |
| Jira team mapping (CRM - Core) | `../product-copilot-beta/policies/jira-constants.md` |

**Do not** publish to Confluence or create Jira tickets unless the user explicitly asks.

## What not to do

- Do not implement features in this workspace — specs only
- Do not conflate CRM Core with the full Phenom suite without cause
- Do not invent customer quotes, metrics, or commitments
- Do not mix customer issue and solution in one section
- Do not restate customer pain inside Part B FRs or Part C blocks

## Related skills

- **create-prd** — orchestrator
- **read-only-inputs** — input policy
- **write-stories-from-problem** — derive Part C from Part A
- **crm-core-product** — scope and `Core` prefix
- **spec-from-jira** / **spec-inputs** — ingestion (read-only)
- **frd-google-drive** — publish new Google Doc
