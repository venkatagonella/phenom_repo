# Functional Requirements Document: [Feature Name]

> **Status**: Draft | Review | Published
> **Author**: [Name]
> **Last Updated**: YYYY-MM-DD
> **Customer**: [Customer name or "Multiple" / "Internal"]
> **CRM Pod**: Core
> **Google Doc**: [Link when created in Drive]
> **Confluence**: [Link when published]
> **Epic**: [PHEM-XXXXXX — primary Epic key]

**Structural authority**: Section segregation follows [`../product-copilot-beta/policies/jira-story-rules.md`](../product-copilot-beta/policies/jira-story-rules.md), [`../product-copilot-beta/policies/templates/story.md`](../product-copilot-beta/policies/templates/story.md), and [`../product-copilot-beta/policies/templates/epic.md`](../product-copilot-beta/policies/templates/epic.md).

> **Segregation rule**: Never mix customer issue and proposed solution in the same section. Epic content → Part A; solution overview and FR list → Part B; story-sized detail blocks → Part C.

---

# Part A — Initiative / Epic

## Source Inputs

Document every input used to author this FRD. Cite keys and links so reviewers can trace requirements.

| Source | Key / Link | Type | Summary |
|--------|------------|------|---------|
| [PHEM-12345](https://…) | PHEM-12345 | Epic | [One-line summary] |
| [PHEM-12346](https://…) | PHEM-12346 | Story | [One-line summary] |
| | [Support ticket ref] | Support ticket | [One-line summary] |
| | [Confluence page] | Document | [One-line summary] |
| | [Google Doc title] | Google Doc | [One-line summary] |
| | [Google Sheet title] | Google Sheet | [One-line summary] |

### Input synthesis notes

- [Conflicts, gaps, or ambiguities found across inputs]
- [Which item is the authoritative Epic vs. supporting Stories/Bugs]

---

## Executive Summary

[2–4 sentences: who is affected, what customer problem this initiative addresses, and the intended outcome. **No solution detail** — reference Part B for approach.]

---

## Customer Issue

> **Segregation rule**: Document only the customer problem, current state, stated asks, and impact. **Do not propose solutions, features, or CRM Core changes in this section.**

### Background

[Who is the customer, what is their recruiting model, and why this matters now?]

### Pain Points

- [Pain point 1 — cite source key if from Jira/ticket]
- [Pain point 2]

### Customer Requirements (as stated)

- [Requirement or ask 1 — in customer language; cite source key]
- [Requirement or ask 2]

### Business Impact

[Revenue, retention, efficiency, compliance, or competitive risk if known.]

| Persona | Impact |
|---------|--------|
| Recruiter / Sourcer | |
| Recruiting Ops | |
| Candidate / HM | |

---

## Problem Breakdown

> **Segregation rule**: Decompose the customer situation into related problems and stated asks. **No solutions.** Complete this section during Step 2 of the PRD workflow before writing Part B.

### Related Problems

Break the overall customer situation into distinct but connected problem clusters:

| # | Related problem | How it connects to the main issue | Source |
|---|-----------------|-----------------------------------|--------|
| 1 | [Sub-problem — describe the problem, not the fix] | [Root cause, symptom, upstream/downstream link] | [PHEM-XXXXX / Google Doc] |
| 2 | [Sub-problem] | [Connection] | [Source] |

### What the Customer Is Asking For

| # | Customer ask (their words) | Type | Related problem # | Source |
|---|---------------------------|------|-------------------|--------|
| 1 | "[Quote or paraphrase]" | Stated requirement | 1 | [PHEM-XXXXX] |
| 2 | "[Quote or paraphrase]" | Explicit request / Inferred need / Constraint | 2 | [Google Doc / ticket] |

**Types:** Stated requirement | Explicit request | Inferred need | Constraint | Question

### Breakdown notes

- [Conflicts or tensions between related problems or asks]
- [Gaps requiring Open Questions in Part D]

---

## Goals & Success Metrics

### Goals

1. [Primary goal aligned to the customer problem above]
2. [Secondary goal]

### Success Metrics

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| [Metric 1] | | | |

### Non-Goals

- [What this initiative will explicitly not address at the Epic level]

---

# Part B — What Should Be Done

> **Segregation rule**: Document the proposed CRM Core response at initiative level. **Do not restate customer pain here** — reference Part A instead.

## Solution Overview

[Brief overview of what CRM Core should accomplish to address Part A. High-level only — detailed requirements and acceptance criteria go in Part C.]

### Existing vs. New

| Need | Exists in CRM Core today? | Gap |
|------|---------------------------|-----|
| [Need 1] | Yes / Partial / No | [What's missing] |

---

## User Stories

One user story per deliverable (maps to a Jira Story). Use the format from `story.md`:

| # | Jira Key | Deliverable | User Story |
|---|----------|-------------|------------|
| 1 | PHEM-XXXXX | [Short title] | As a [type of user], I want [goal] so that [reason]. |
| 2 | PHEM-XXXXX | [Short title] | As a [type of user], I want [goal] so that [reason]. |

---

## Functional Requirements

> Each FR states **only what should be done** — not the customer problem. Link to Part C for story-sized detail blocks.

| FR | Name | Summary | Jira Story |
|----|------|---------|------------|
| FR1 | [Requirement name] | [Role] can [action] from [location] | PHEM-XXXXX |
| FR2 | [Requirement name] | System [does something] when [condition] | PHEM-XXXXX |

### Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Performance | [Response time, throughput] |
| Security / Permissions | [Auth, data protection] |
| Scale | |
| Localization | |
| Accessibility | [Keyboard, screen reader if applicable] |

### Platform Considerations

- [Capability area] must use the [Platform Team] service, not custom logic.

### Constraints

[Boundaries engineering needs to know upfront — e.g. must use existing service, no new infrastructure.]

---

# Part C — Requirement / Story Blocks

> Repeat this block for **each** functional requirement or story-sized deliverable. Structure and quality checklist per [`jira-story-rules`](../product-copilot-beta/policies/jira-story-rules.md) and [`story.md`](../product-copilot-beta/policies/templates/story.md).

---

## FR1: [Requirement Name] — PHEM-XXXXX

### User Story

As a [type of user], I want [goal] so that [reason].

### Addresses (traceability)

- **Related problem #**: [from Part A Problem Breakdown]
- **Customer ask #**: [from What the Customer Is Asking For]
- **Source input**: [PHEM-XXXXX / Google Doc]

### Background / Context

*(optional)*

[Relevant product, technical, or business context. Link to designs, research, related Epics or bugs.]

This is part of [Epic PHEM-XXXXXX].

### Acceptance Criteria

**Scenario 1: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

**Scenario 2: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

**Scenario 3: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

### Out of Scope

[What this requirement does NOT cover. Reference other Stories/Epics if applicable.]

### Design / Mockups

*(if UX Required = YES)*

- **UX Required**: Yes / No
- [Figma link → Frame: "Frame Name v1"]

### Technical Notes

*(if applicable)*

- [Backend/frontend considerations]
- [API endpoints affected]
- [Data model notes]

### Open Questions

| Question | Owner | Status |
|----------|-------|--------|
| | | Open |

---

## FR2: [Requirement Name] — PHEM-XXXXX

### User Story

As a [type of user], I want [goal] so that [reason].

### Addresses (traceability)

- **Related problem #**:
- **Customer ask #**:
- **Source input**:

### Background / Context

*(optional)*

### Acceptance Criteria

**Scenario 1: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

**Scenario 2: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

**Scenario 3: [Brief name]**

- Given [precondition]
- When [action]
- Then [expected result]

### Out of Scope

### Design / Mockups

### Technical Notes

### Open Questions

| Question | Owner | Status |
|----------|-------|--------|
| | | Open |

---

# Part D — Initiative Wrap-Up

## Cross-Team Dependencies

| Team | Dependency | Required By | Story / Status |
|------|------------|-------------|----------------|
| CRM - Messaging | | | Open |
| CRM - Profile | | | Open |
| CRM - Automation | | | Open |
| Scheduling | | | Open |
| Automation Engine | | | Open |
| Platform | | | Open |

---

## Release Plan

### Phases

1. **Phase 1 (MVP)**: [Minimum scope to address core pain]
2. **Phase 2**: [Additional scope]

### Feature Flags

- **Flag Name**: [name]
- **Rollout Strategy**: [Percentage, customer list]

---

## Assumptions

- [Assumption 1 — distinguish from confirmed facts in Jira/tickets/docs]

---

## Appendix / References

### Customer Quotes / Notes

> [Optional verbatim or paraphrased quotes from customer conversations or ticket comments]

### References

- [Jira keys, Confluence pages, meeting notes, related FRDs]

### Story Quality Checklist

Per `jira-story-rules` — verify for each Part C block before stakeholder review:

- [ ] Naming convention correct (`[Prefix] – [FE/BE] – [Title]`)
- [ ] Linked to parent Epic
- [ ] Clear User Story (Who, What, Why)
- [ ] Acceptance criteria testable (Given / When / Then) — 3–5 scenarios
- [ ] Dependencies identified
- [ ] Out of Scope filled in
- [ ] UX Required set; Figma link if YES
- [ ] Open questions have owners
