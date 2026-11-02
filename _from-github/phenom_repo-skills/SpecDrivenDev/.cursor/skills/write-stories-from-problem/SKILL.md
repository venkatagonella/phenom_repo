---
name: write-stories-from-problem
description: >-
  Derives user stories and Part C requirement blocks from customer problems
  documented in FRD Part A (Problem Breakdown). Use in Step 3 of create-prd
  after Related Problems and Customer Asks are complete — before or while
  filling Part B and Part C of the FRD.
---

# Write Stories from Customer Problem

Convert **Part A Problem Breakdown** into sprint-sized **user stories** and **Part C blocks** — each story must trace to a related problem and customer ask. Do not write stories before Step 2 is complete.

## Triggers

- Part A Problem Breakdown tables are filled
- User asks to "write stories", "break into stories", or "define acceptance criteria"
- Step 3 of **create-prd** after Jira + Google Drive ingestion

## Prerequisites

- **Related Problems** table complete (with source citations)
- **What the Customer Is Asking For** table complete
- No solutions in Part A

## Derivation rules

### 1. Map problems → stories

| Related problem # | Customer ask # | Story needed? | Rationale |
|-------------------|----------------|---------------|-----------|
| 1 | 1, 2 | Yes | [Why one or more stories] |
| 2 | 3 | Maybe phased | [MVP vs later] |

- One story per **sprint-sized** deliverable (two-week rule per `jira-story-rules`)
- Large asks → split into multiple stories or Phase 1 / Phase 2 in Part D
- Multiple asks → one story only if they ship together atomically

### 2. User story format

Per `../product-copilot-beta/policies/templates/story.md`:

```
As a [type of user], I want [goal] so that [customer outcome from Part A].
```

| Field | Source |
|-------|--------|
| **Persona** | Recruiter, sourcer, recruiting ops, CRM admin — from Part A impact table |
| **Goal** | What they need to do — from Part B scope, not Part A pain |
| **So that** | Ties to **customer ask** or **success metric** from Part A — never generic |

### 3. Suggested story title (FRD only — do not create in Jira)

```
Core – [FE|BE] – [Short action-oriented title]
```

CRM Core prefix: **`Core`** (`../product-copilot-beta/policies/jira-constants.md`)

Examples:
- `Core – FE – Bulk apply tags to selected candidates`
- `Core – BE – Validate tag rules on pipeline stage change`

### 4. Part C block per story

For each story, write a full Part C section in `frd-template.md`:

1. **User Story** — Who / What / Why
2. **Addresses** — Related problem # + Customer ask # (one line)
3. **Background / Context** — Optional; link input Jira key if story mirrors existing ticket (read-only reference)
4. **Acceptance Criteria** — 3–5 scenarios, Given / When / Then
5. **Out of Scope**
6. **Design / Mockups** — If UX; note UX Required YES/NO
7. **Technical Notes** — If BE or integration
8. **Open Questions** — Table with owner

### 5. Acceptance criteria quality

Per `jira-story-rules`:

- Testable, specific, observable
- 3–5 scenarios per story
- Name each scenario briefly
- Cover happy path, edge case, and permission/error case where relevant

**Scenario template:**

```
**Scenario N: [Brief name]**
- Given [precondition]
- When [action]
- Then [expected result]
```

## Traceability matrix (include in Part B or Part D)

| Story / FR | Related problem # | Customer ask # | Source input |
|------------|-------------------|----------------|--------------|
| FR1 | 1 | 1 | PHEM-12345 |
| FR2 | 1, 2 | 2 | Google Doc |

## What not to do

- Do not write stories without a Part A problem breakdown
- Do not restate full customer pain in Part C — reference Part A
- Do not create or edit Jira stories — output lives in the FRD only
- Do not invent acceptance criteria unsupported by inputs
- Do not combine unrelated customer asks into one story without noting tradeoff

## Related skills

- **create-prd** — orchestrator (Step 3)
- **prd-authoring** — FRD structure and review checklist
- **crm-core-product** — map stories to CRM Core capabilities
