# Epic Template

> Copy this into a Jira Epic description via `editJiraIssue` (Atlassian plugin, markdown).
> Full rules and quality checklist → `policies/jira-epic-rules.md`
> Field IDs and PM account IDs → `policies/jira-constants.md`
>
> **Style:** Write for a first-time reader — full feature names (not `E1`/`UC3`), expand unfamiliar abbreviations on first use, explain insider terms in-line, cross-ref related work by title + Jira key, and never put local/vault/prototype file paths in the description (attach wireframes instead). See `jira-epic-rules.md` → "Writing Style / Clarity".

---

## What

What is this feature?
Provide a brief overview of what this feature will accomplish.

---

## Why

Why should this feature be worked on?
What business problem does it solve? What value will Phenom, the customer, and/or the user realise?

---

## Success Metrics

- What metric does this feature look to impact?
- What determines success? Make it measurable and quantifiable.
- Why is this Epic worth prioritising over others?

---

## Requirements

### Functional Requirements

> **Separate functional requirements by impact area** — one labelled sub-section per workstream the change touches (e.g. Data Model, Assignment/UI, Integration Experience, Migration, Notifications, Talent Analytics, Automation Engine), annotated with the owning pod. Write each requirement precisely (observable, testable). Each impact area should map to a Story and to a row in Cross-Team Dependencies. See `jira-epic-rules.md` → "Requirements: Separate by Impact Area".

#### [Impact area A] *(owning pod)*

A1. [Role] can [action] from [location in the product]
A2. System [does something] when [condition]

#### [Impact area B] *(owning pod)*

B1. [Role] can [action] from [location in the product]

### Non-Functional Requirements

- Response time: [action] completes within [N] seconds
- Language support: Supports 13+ languages
- Accessibility: All interactive elements reachable via keyboard
- Scale: Handles up to [N] concurrent users / records

### Platform Considerations

- [Capability area] must use the [Platform Team] service, not custom logic.
  Contact: [PM name]. Docs: [link].

### Constraints

[Boundaries engineering needs to know upfront — e.g. must use existing service, no new infrastructure, specific security requirements.]

---

## Cross-Team Dependencies

> List the **delivery pods** required. Do **not** add a UX/Design row — UX is needed on nearly every Epic; capture it via the `UX Required` field instead. Use canonical pod names: **Integration Experience** (ATS/connectors), **Talent Analytics** (reporting/report builder), **Notifications / Messaging Platform**, **Automation Engine**, **Platform Config**, **CRM**, **Scheduling**, **Interview Intelligence**.

| Pod | Required (Yes / tbd) | Why? | Story |
|-----|----------------------|------|-------|
| CRM | | | |
| Platform Config | | | |
| Integration Experience | | | |
| Talent Analytics | | | |
| Automation Engine | | | |
| _(add additional pods)_ | | | |

---

## Out of Scope

What will **not** be worked on as part of this feature?
What belongs to a future iteration?

---

## Open Questions

| Question | Owner | Status |
|----------|-------|--------|
| | | Open |

---

## Customer Timelines (optional)

| Customer | Start of UAT (Staging) | Go-Live Date (Production) |
|----------|------------------------|---------------------------|
| | | |

---

## Documentation

- **Visual QA**: [Link]
- **Release Documentation**: [Link after release]
