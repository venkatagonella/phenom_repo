---
name: jira-story-rules
type: policy
description: "Story structure, template, and sign-off rules for Phenom Jira"
requires:
  - jira
always: false
triggers: [jira, phem, epic, story, stories, bug, ticket, sprint, backlog, issue, jql, task, defect]
---

## What Is a Story?

A Story is a simple narrative describing a deliverable the team can commit to within a **two-week sprint**. A series of related Stories makes up an Epic.

---

## Naming Convention

Format: `[Prefix] – [FE/BE] – [Story Title]`

Examples:
- `II – FE – Add transcript export option`
- `SCH – BE – Create calendar availability endpoint`
- `AE – FE – Display automation execution logs`
- `SCR – BE – Bulk reject via screening threshold`

For all product prefixes → see `jira-constants` policy.

---

## Core Rules

- Stories must be deliverable within a two-week sprint.
- Every Story must link to a parent Epic (no floating stories).
- One board, one team. Stories are created on the contributing team's board, linked back to the Epic.
- Naming: `[Prefix] – [FE/BE] – [Story Title]` — always use this format.
- Clear Acceptance Criteria. Use Given / When / Then (Gherkin) format. Aim for 3–5 criteria per Story.
- Stories marked `UX Required = YES` must pass Visual QA and UX sign-off before closing.

---

## Writing Style (lighter)

Stories should also be readable without prior project context. Full Epic clarity rules → `policies/jira-epic-rules.md` → "Writing Style / Clarity".

- Refer to the parent Epic by **full title + Jira key**, not cryptic labels (`E1`, `Phase A`).
- Avoid unexplained insider shorthand in the User Story or acceptance criteria.
- Do not put local filesystem / vault / prototype paths in the description — attach screenshots or link Figma instead.

---

## Cross-Team Story Questions

When a Story is part of a cross-team Epic, also confirm:

1. **Which Epic does this Story belong to?** Provide the Epic key (e.g., PHEM-123456).
2. **Does this Story's scope align with the Epic's dependency table?** The work described should match what the Epic says this team is responsible for.
3. **Are there dependencies on other teams' Stories?** If yes, list them and confirm sequencing.

---

## Quality Checklist

- [ ] Naming convention correct (`[Prefix] – [FE/BE] – [Title]`)
- [ ] Linked to a parent Epic (verify Epic key exists before creating)
- [ ] Has a clear User Story (Who, What, Why)
- [ ] Readable without cryptic labels — parent Epic referenced by title + key; no local asset paths
- [ ] Acceptance criteria are testable (Given / When / Then) — aim for 3–5 scenarios
- [ ] Dependencies identified and listed
- [ ] Out of Scope section filled in (reduces ambiguity)
- [ ] UX Required is set; if YES, Figma link is attached
- [ ] Open questions have owners assigned
- [ ] Product Experience / Product field is set (see `jira-constants` for values)
- [ ] Fix version matches the parent Epic's fix version

---

## Story Description Template

→ `policies/templates/story.md` — blank form, copy-paste ready.

Apply via the two-step pattern (see `jira-api` skill — create, then set the description as markdown via `editJiraIssue`).

---

## SA Product Stories (customer projects)

Product Stories raised by Solution Architects in customer / implementation projects follow their own template:

→ `skills/product-story-analyzer/templates/product-story-template.md`

Rules:
- **Search before creating.** Link to an existing Product Story or PHEM epic for the same need (any customer) instead of opening a new one.
- **One need = one Product Story.** Never split by team; Product breaks it into team stories in the PHEM epic.
- **No ETA on the Product Story.** ETAs are committed on the PHEM epic only.
- **Quality gate before decision:** Product rates Green / Amber / Red; only Green goes to the decision.
- **After approval, everything happens in PHEM.** Product fills section 11 (decision, owning PM, PHEM epic link). Requirements breakdown, team stories, the ETA and all delivery communication live on the PHEM epic, not on the Product Story.

To quality-check an SA Product Story, use the Product Story Analyzer (`skills/product-story-analyzer/SKILL.md`) (rating, duplicate check, team check, SA feedback).

---

## Before Creating a Story

Confirm:
1. Parent Epic key (required — verify it exists before creating)
2. Product Experience / Product (required custom field — see `jira-constants` for field IDs)
3. UX Required — YES / NO
4. FE or BE prefix (or both — create separate stories per team)
5. Fix Version — inherit from Epic unless different

If the user hasn't provided a user story statement or acceptance criteria, draft them and confirm before creating.

---

## UX Validation & Sign-Off

Stories marked `UX Required = YES` must follow this sign-off order:

1. **Dev** — completes implementation
2. **QA** — functional testing
3. **UX** — Visual QA and UX approval (required for any UI changes)
4. **PM** — final sign-off

Include design assets (Figma links, frame names) in the Story for smooth UX validation.
