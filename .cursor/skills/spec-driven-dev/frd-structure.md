# FRD Structure — Parts A–D

Use with the **spec-driven-dev** skill. When available, prefer the full template at:

`/Users/venkata.gonella/phenom-master-copilot/SpecDrivenDev/templates/frd-template.md`

Structural authority (when reachable):

- `product-copilot-beta/policies/jira-story-rules.md`
- `product-copilot-beta/policies/templates/story.md`
- `product-copilot-beta/policies/templates/epic.md`

---

## Metadata header

```markdown
# Functional Requirements Document: [Feature Name]

> **Status**: Draft | Review | Published
> **Author**: [Name]
> **Last Updated**: YYYY-MM-DD
> **Customer**: [Customer or "Multiple" / "Internal"]
> **CRM Pod**: Core
> **Google Doc**: [Link when created]
> **Confluence**: [Link when published]
> **Epic**: [PHEM-XXXXXX — primary Epic key]
```

---

## Part A — Initiative / Epic (no solutions)

### Source Inputs

| Source | Key / Link | Type | Summary |
|--------|------------|------|---------|
| … | PHEM-… | Epic / Story / Bug / Google Doc / … | One-line |

Include synthesis notes: conflicts, gaps, which item is the authoritative Epic.

### Executive Summary

2–4 sentences: who is affected, what problem, intended outcome. **No solution detail.**

### Customer Issue

- Background
- Pain Points (cite sources)
- Customer Requirements (as stated, customer language)
- Business Impact + persona impact table

### Problem Breakdown

**Related Problems** — sub-problems with connection + source (no solutions).

**What the Customer Is Asking For** — stated asks vs inferred needs; types:  
`Stated requirement` | `Explicit request` | `Inferred need` | `Constraint` | `Question`

### Goals & Success Metrics

Measurable outcomes tied to Part A problems (not feature laundry lists).

---

## Part B — What Should Be Done (no pain restatement)

- Solution Overview — addresses Part A only; reference problems by number
- User Stories table — title, persona, summary, traces to related problem # / ask #
- Functional Requirements list — what should be done, not why it hurts

Story naming: prefix with `Core` for CRM Core work.

---

## Part C — Requirement / Story Blocks

One block per story:

| Field | Guidance |
|-------|----------|
| User Story | Who / What / Why |
| Background | Brief context; do not restate Part A pain |
| Acceptance Criteria | **3–5** Given / When / Then scenarios |
| Out of Scope | Explicit exclusions |
| Design / Technical Notes | Optional; unknowns → Open Questions |
| Open Questions | Owner + decision needed |
| Traceability | Related problem # and customer ask # from Part A |

---

## Part D — Initiative Wrap-Up

- Cross-Team Dependencies
- Release Plan / phasing
- Assumptions (separated from confirmed facts)
- Appendix (links, glossary, discarded options)

---

## Review checklist

- [ ] Source Inputs lists all Jira keys and documents
- [ ] Part A Problem Breakdown complete (related problems + customer asks)
- [ ] Part A has no proposed solutions or features
- [ ] Part B has no customer pain restatement
- [ ] Each Part C block has Who/What/Why story
- [ ] Each Part C block has 3–5 Given/When/Then ACs
- [ ] Each Part C block has Out of Scope
- [ ] Stories trace to Part A problems/asks
- [ ] Success metrics in Part A are measurable
- [ ] Open questions have owners
- [ ] Dependencies and assumptions in Part D
- [ ] Status is `Draft` until user reviews

---

## Story derivation (from Part A → B/C)

For each related problem / customer ask cluster:

1. Name the persona and desired outcome (story)
2. Write only requirements that close that ask
3. Add AC that a tester can execute without reading Part A
4. Put anything not needed for that ask in Out of Scope or a later phase
