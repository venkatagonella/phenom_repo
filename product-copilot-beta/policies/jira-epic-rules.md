---
name: jira-epic-rules
type: policy
description: "Epic structure, template, and management rules for Phenom Jira"
requires:
  - jira
always: false
triggers: [jira, phem, epic, story, stories, bug, ticket, sprint, backlog, issue, jql, task, defect]
---

## What Is an Epic?

An Epic is a body of work grouping all tasks needed to build a **releasable functionality**. It normally spans multiple sprints, allows end-to-end testing, and communicates release timelines internally.

---

## Core Rules

- **One Epic = one shippable increment.** Never mix phases or unrelated features. If it can't be released independently, it shouldn't be a separate Epic.
- **One owner** = a single PM accountable for the Epic end-to-end.
- **Team-specific Stories.** Each contributing team creates Stories on their own board, linked to the same Epic.
- **One Fix Version.** The Epic-level fix version indicates the target release month for all teams.
- Epic closes only when all Stories across all teams are complete and end-to-end testing passes.
- Phase 2 work = a new Epic. Never extend an existing Epic's scope.

**Cross-team epics:**
- The Epic owner creates the Epic on their board.
- Other teams create Stories on their own boards but link them to the shared Epic.

---

## Phase Management

- **Phase 1** = Epic 1 with a clear scope boundary.
- **Phase 2** = a **new** Epic (future-dated). Never mix phases in one Epic.
- If scope creeps during elaboration or development, move the new items into a Phase 2 Epic.

---

## Cross-Team Dependency Questions

Before an Epic is considered ready for elaboration, confirm answers to all of the following:

1. **Which teams are required?** List every team that must contribute work for this functionality to ship end-to-end.
2. **Is this ONE Epic?** Confirm that a single Epic groups all work across teams.
3. **Does each team have a Story?** For every team in the Cross-Team Dependencies table, is there (or will there be) a dedicated Story on that team's board?
4. **Are platform / shared components considered?** If this feature requires building or modifying shared components (APIs, data models, config services), is the platform team involved?
5. **Is UX required?** If yes, is the design link attached and has UX been involved in the kick-off?
6. **Are there upstream or downstream dependencies?** Does this Epic depend on another Epic being completed first? Will another team's work be blocked until this ships?
7. **Are open questions documented?** Every unresolved question must have an owner before elaboration begins.

**If the Epic involves multiple teams, also confirm:**

8. **Has a kick-off call been scheduled?** Multi-team Epics require early alignment with Product, UX & Engineering.
9. **Is the communication owner clear?** The Epic owner maintains weekly progress tracking until production deployment.
10. **Is the fix version aligned across teams?** All contributing teams must be able to deliver within the same release window.

---

## Platform Awareness Check

Before finalising requirements, scan the Epic against `policies/platform-routing.md`. If the Epic involves any capability area below, engage that platform team **before** finalising scope.

| If requirements mention… | Flag this platform area |
|--------------------------|------------------------|
| Candidate portal, apply flow, candidate status, candidate-facing UI | Unified Candidate Experience |
| Job page, career site, CIM, widgets, SEO | CIM / Career Site |
| Auto-advance, auto-reject, triggers, workflows, scheduled tasks, reminders | Automation Engine |
| Calendar, availability, time zones, scheduling invitations | Scheduling Platform |
| Interview recording, playback, transcription, evaluation, debrief | Interview Intelligence |
| Email, SMS, in-app notifications to candidates or users | Notifications / Messaging Platform |
| Dashboards, reports, analytics, exports, data warehouse, report builder | Talent Analytics |
| ATS job pull, integration sync, connectors (SuccessFactors, Workday, etc.) | Integration Experience |
| Tenant settings, feature flags, configuration, toggles | Platform Config |

> **Naming convention:** always refer to the analytics team/capability as **Talent Analytics** (not "Data Platform / BI" or "Analytics team"), and the ATS/integration team/capability as **Integration Experience** (not "ATS / Integrations" or "Connectors").

---

## Writing Style / Clarity

Write every Epic so a **first-time reader** (no prior chat, meeting, or project context) can understand it.

- Prefer **full product/feature names** over internal labels (`E1`, `E2`, `Phase A`, `UC3`) unless those labels already exist as official Jira Epic titles — and even then, **spell out the title on first mention**.
- Expand abbreviations on first use when not universally known in Phenom Jira (e.g. Elasticsearch (ES), then ES). Common Phenom product names already standard in `jira-constants` (CRM, RX, etc.) can stay; do not invent new shorthand.
- Avoid cryptic insider language ("the Brandon lock", "v0.5 Apps tab") without a plain-English explanation in the same sentence.
- Cross-references: use **full Epic/Story titles + Jira keys** (e.g. Application Fields Configuration & Grouping (PHEM-2252490)), not "see E1".
- **Assets / attachments:** Do not put local filesystem paths, vault paths, or internal prototype repo paths in Jira descriptions. Say wireframes / screenshots will be attached to this ticket (or attach them). Describe design options and current UX in words; screenshots are attachments, not path references.
- Clarity does not mean vague — keep impact-area structure and precise, observable, testable requirements (see below).

---

## Requirements: Separate by Impact Area

Functional requirements must **always be separated by impact area** — the distinct workstreams (and the pods that own them) the change touches. Typical impact areas: Data Model, Assignment/UI, Integration Experience, Migration & Feature Flag, Notifications, Workspace Views/Filters, Talent Analytics, Automation Engine.

Rules:

- Group functional requirements under a labelled heading **per impact area**, and annotate each area with its owning **pod**.
- Write each requirement **precisely** — observable, testable statements (who can do what, when, where), not lean single-paragraph prose. Avoid vague verbs ("improve", "better", "enhance").
- The Epic must give a **full overview of every Story it implies**: a reader should be able to see all the workstreams the Epic spans. Each impact area should map to a Story on the owning pod's board, and each should have a matching row in the Cross-Team Dependencies table (and vice versa).
- Do not list UX/Design as a separate dependency row — it is required across virtually every Epic. Capture it via the `UX Required` field instead, and call out the **delivery pods** in the dependency list.

---

## Quality Checklist

Before an Epic is approved for development:

- [ ] Follows the template structure (What, Why, Success Metrics, Requirements, Dependencies, Out of Scope, Open Questions)
- [ ] Has a clear "What" and "Why"
- [ ] Scope is bounded (Out of Scope section filled in)
- [ ] **Readable without prior context** — plain language; no cryptic abbreviations or insider shorthand; related work referenced by full title + Jira key (see "Writing Style / Clarity")
- [ ] **No local asset paths** in the description — wireframes/screenshots attached (or noted as attachments), not vault/filesystem/prototype paths
- [ ] **Functional requirements are separated by impact area**, each precise enough to map to a Story, giving a full overview of the Stories the Epic implies (see "Requirements: Separate by Impact Area")
- [ ] Requirements are also structured: Functional, Non-Functional, Platform Considerations, Constraints
- [ ] **Platform Awareness Check completed** — relevant platform teams engaged and added to dependencies
- [ ] Cross-Team Dependencies table complete — all contributing teams listed with reason
- [ ] Open Questions all have owners
- [ ] Success metrics are measurable and quantifiable
- [ ] Fix version is set (or explicitly `Backlog`)
- [ ] UX Required is set; if YES, design link is attached
- [ ] Not floating — linked to an Initiative or Theme if applicable

---

## Epic Description Template

→ `policies/templates/epic.md` — blank form, copy-paste ready.

Apply via `editJiraIssue` (Atlassian plugin) with markdown — no ADF needed (see `jira-api` skill).

---

## Before Creating an Epic

Ask the user to confirm:
1. Product Experience / Product (required — see `jira-constants` for field IDs and values)
2. Fix Version — specific month (`YY.MM`, e.g., `26.05`) or `Backlog` if unscheduled
3. UX Required — YES / NO
4. Any cross-team dependencies to document upfront
5. If a kick-off call with UX and Engineering is needed before work starts
6. Platform awareness check — any capability areas from the routing table involved?
