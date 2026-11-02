---
name: create-prd
description: >-
  Create a new PRD/FRD for Phenom CRM Core in three steps: (1) understand
  context from Jira entities, (2) break down customer problems and what they are
  asking for, (3) author a new FRD from Jira + Google Drive inputs using
  frd-template.md and publish to Google Drive. Read-only on all input Jira
  items and source documents — never modify inputs.
---

# Create PRD — Three-Step Workflow

Orchestrates creation of a **new** Functional Requirements Document (FRD / PRD) for **Phenom CRM Core**. Follow these three steps in order. Do not skip ahead.

```
Step 1 → Understand context from Jira entities
Step 2 → Break down customer problems & what customer is asking for
Step 3 → Create new FRD/PRD from all inputs → publish to Google Drive
```

**Template:** `templates/frd-template.md` (Parts A–D, segregated per `jira-story-rules.md`)

**Read-only rule:** No changes or creation of any Jira issues or source documents used as input. Only create **new** FRD output (local draft + new Google Doc).

---

## Step 1 — Understand context from Jira entities

**Goal:** Build a complete picture of the problem from every Jira entity the user provides.

### Inputs

- One or more Jira keys, comma-separated: `PHEM-12345, PHEM-12346, PHEM-99001`
- **Any Jira entity type:** Epic, Story, Task, Bug, Sub-task, Initiative, Support/JSM ticket, or other issue type

### Actions (read-only)

Follow **spec-from-jira**:

1. Parse and deduplicate keys
2. `getAccessibleAtlassianResources` → `cloudId`
3. `getJiraIssue` for **each** key — `fields` including `"comment"`, `responseContentFormat: "markdown"`
4. Enrich context when thin:
   - Epic → fetch child stories via JQL (`parent = KEY` or `"Epic Link" = KEY`)
   - Story → fetch parent Epic
   - Bug/ticket → fetch linked issues, duplicates, blocks/relates-to
   - `getJiraIssueRemoteIssueLinks` for external links

### What to extract per entity

| Field | Use for |
|-------|---------|
| Issue type | How this entity fits (Epic vs Story vs Bug) |
| Summary | One-line context |
| Description | Problem detail, requirements, acceptance criteria |
| Status / priority | Urgency and lifecycle |
| Comments | Customer voice, PM/CS clarifications, decisions |
| Labels / components | Product area mapping |
| Parent / children / links | Scope and relationships |

### Step 1 output (internal summary before writing FRD)

Produce a short **Jira Context Summary** covering:

- Which entity is the primary Epic or initiative anchor
- How entities relate (parent/child, blocks, duplicates)
- Key facts vs open questions from Jira alone
- Gaps that need Google Drive or other inputs

Do **not** edit any Jira entity.

---

## Step 2 — Break down customer problems

**Goal:** Decompose the customer situation into related problems and clearly state what the customer is asking for — before writing any solution.

Also ingest **Google Drive** reference material in this step (read-only). Follow **spec-inputs** → Google Drive section.

### Problem breakdown structure

Document in FRD **Part A** under dedicated subsections (see `frd-template.md`):

#### Related Problems

Break the overall situation into **related but distinct** problem clusters:

| # | Related problem | How it connects to the main issue | Source |
|---|-----------------|-------------------------------------|--------|
| 1 | [Sub-problem A] | [Cause/effect or dependency] | PHEM-XXXXX |
| 2 | [Sub-problem B] | [Cause/effect or dependency] | Drive doc / ticket |

Rules:

- Each row is a **problem**, not a solution
- Show how sub-problems relate (upstream/downstream, root cause vs symptom)
- Cite Jira key or Google Drive document for each

#### What the Customer Is Asking For

Separate **stated asks** from **underlying needs**:

| # | Customer ask (their words) | Type | Related problem # | Source |
|---|---------------------------|------|-------------------|--------|
| 1 | "[Quote or paraphrase]" | Stated requirement | 1 | PHEM-XXXXX |
| 2 | "[Quote or paraphrase]" | Inferred need | 2 | Google Doc |

Types: `Stated requirement` | `Explicit request` | `Inferred need` | `Constraint` | `Question`

Rules:

- Use customer language where possible
- Flag when an ask maps to multiple related problems
- Flag conflicts between asks or between Jira entities
- **No solutions, features, or CRM changes in this subsection**

### Google Drive inputs (read-only)

Gather **all** relevant information from the user's Google Drive:

| Tool | When |
|------|------|
| `list_drive_files` | User says "my Google Drive" or gives a search term / folder context |
| `read_google_doc` | User provides Doc URL/ID, or search finds relevant docs |
| `read_google_sheet` | Requirements matrices, customer data in Sheets |

- Read every user-specified Doc/Sheet and any files found by search relevant to the initiative
- Add each to **Source Inputs** table with type `Google Doc` or `Google Sheet`
- Do **not** `update_google_doc` on source files — only read

Combine Jira context (Step 1) + Google Drive + any Confluence/Granola inputs into the problem breakdown.

### Step 2 output

Before drafting Part B/C, confirm:

- [ ] Related problems listed with connections
- [ ] Customer asks table complete with sources
- [ ] All Google Drive reference docs read and cited
- [ ] No solutions written yet

---

## Step 3 — Create new FRD/PRD → Google Drive

**Goal:** Author a **new** FRD synthesizing Step 1 + Step 2, following `templates/frd-template.md`, and publish to Google Drive.

### Draft locally first

1. Copy structure from `templates/frd-template.md`
2. Write `specs/{initiative-slug}/frd.md` with status `Draft`
3. Fill all parts:

| Part | Content |
|------|---------|
| **A** | Source Inputs, Executive Summary, Customer Issue, **Problem Breakdown** (Step 2), Goals |
| **B** | Solution Overview, User Stories, Functional Requirements — addresses Part A only |
| **C** | One block per story: User Story, AC (Given/When/Then), Out of Scope, etc. |
| **D** | Dependencies, Release Plan, Assumptions, Appendix |

4. Every story in Part B/C must trace to Step 2 **Related Problems** and **Customer Asks** — follow **write-stories-from-problem**
5. Map capabilities with **crm-core-product**; follow **prd-authoring** review checklist

### Publish to Google Drive

Follow **frd-google-drive**:

```
create_google_doc({
  title: "FRD - [Initiative] - [Customer] - YYYY-MM-DD",
  content: "<full FRD from local draft>"
})
```

Return the **Google Doc URL** as the primary deliverable. Update `frd.md` metadata with the Drive link.

### Step 3 constraints

- **Create new** Google Doc only — do not overwrite source Docs from Step 2
- Do not create or edit Jira issues
- Confirm to user: inputs were read-only; only the new FRD was created

---

## End-to-end checklist

```
- [ ] Step 1: All Jira entities fetched and context understood
- [ ] Step 2: Related problems + customer asks documented; Google Drive read
- [ ] Step 3: FRD drafted per frd-template.md (Parts A–D)
- [ ] Step 3: Stories trace to Step 2 problems/asks
- [ ] Step 3: New Google Doc created; URL returned
- [ ] No input Jira items or source documents modified
```

## Example prompt

> Understand PHEM-45001, PHEM-45002, PHEM-45003. Break down the customer problems, read my Google Drive docs on Acme bulk tagging, and create a new PRD in Google Drive.

## Related skills

| Skill | Step |
|-------|------|
| **read-only-inputs** | All steps — enforce no writes on inputs |
| **spec-from-jira** | Step 1 — Jira entity context (read-only) |
| **spec-inputs** | Step 2 — Google Drive, Confluence, meetings (read-only) |
| **write-stories-from-problem** | Step 3 — derive stories from Part A breakdown |
| **crm-core-product** | Step 3 — CRM Core scope mapping |
| **prd-authoring** | Step 3 — FRD structure, segregation, review |
| **frd-google-drive** | Step 3 — publish new Google Doc |

## What not to do

- Do not skip Step 2 problem breakdown before writing solutions
- Do not modify Jira entities or source Google Docs/Sheets
- Do not mix customer problem and solution in the same section
- Do not invent customer asks not supported by Jira or Drive inputs
