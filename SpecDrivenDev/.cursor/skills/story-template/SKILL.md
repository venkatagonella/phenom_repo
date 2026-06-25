---
name: story-template
description: >-
  Write user stories with acceptance criteria and considerations in the Phenom
  Jira-ready story format (User Story / Acceptance Criteria as Scenario +
  Given/When/Then / Considerations for Localization and Analytics/Data Storage).
  Use when authoring user stories for a functional specification, breaking an epic
  into stories, populating Section 5 of a PRD/FRD, or producing stories that can be
  pasted into Jira. Always include the Localization and Analytics / Data Storage
  considerations for every story.
---

# Phenom Story Template

Use this exact structure for every user story. It is Jira-ready: a story is the
User Story line, its Acceptance Criteria (one or more Scenario blocks written as
Given / When / Then), and its Considerations (always Localization + Analytics /
Data Storage). Do not drop the Considerations — they exist so localization and
data-storage needs are designed in, not bolted on later.

## Template (verbatim)

```
User Story: As a [type of user], I want [an action] so that [a benefit/a value].
Acceptance Criteria:
Scenario: <Brief description of the scenario or user action> Given: <Preconditions or context before the action takes place> When: <Specific action or event taken by the user/system> Then: <Expected outcome or result from the action/event>
Scenario: (Add multiple scenarios as needed) Given: When: Then:
Considerations:
1. Localization <Languages: Our Product today supports over 13 languages. Make sure to call out in your user story that your feature should support those languages to provide a consistent experience.>
2. Analytics / Data Storage <Snowflake or Data Storage of Choice: It is critical to call out any data storage requirements within the acceptance criteria so that it is not an afterthought.>
```

## How to fill it

- **User Story** — one sentence: `As a [persona], I want [action] so that [value]`. Keep the persona concrete (e.g. "Primary Recruiter", "Recruiting Ops admin"), not "user".
- **Acceptance Criteria** — one or more `Scenario:` blocks. Each scenario is testable and uses `Given:` (preconditions/context) → `When:` (the action/event) → `Then:` (the observable outcome). Add as many scenarios as the story needs (happy path, edge cases, flag-OFF/regression).
- **Considerations** — always both items, written for *this* story:
  1. **Localization** — state whether the story introduces user-facing strings (labels, role names, notification copy, filter/report values). If yes, call out that they must support the 13+ languages the product supports. If the story is backend-only, say so explicitly and note any strings that surface in UI elsewhere must remain localizable.
  2. **Analytics / Data Storage** — call out concrete storage/analytics needs in the acceptance criteria: what is persisted, where (e.g. Snowflake / chosen data store), event emission, audit/history, retention. Never leave this as an afterthought.

## Rules

- Every story MUST include both Considerations. Do not omit them even when a value is "N/A" — write the N/A and why.
- Keep scenarios outcome-focused and verifiable; avoid implementation detail in `Then:`.
- Trace each story back to its source (epic impact area, customer ticket) where a spec calls for references.
- This is the format expected for stories that will be added to Jira; do not invent a different structure.

## Example

```
User Story: As a Primary Recruiter, I want to assign Secondary Recruiter, Sourcer, and Coordinator on a job's Hiring Team so that each contributor is tracked in their actual role.
Acceptance Criteria:
Scenario: Assign a support role manually
Given: the expanded-roles feature flag is ON and I am the Primary Recruiter on a job
When: I open the Hiring Team section and assign a colleague as Sourcer
Then: the colleague is shown as Sourcer with a "manual" provisioning indicator and the assignment is recorded with its time window
Scenario: Flag-OFF regression
Given: the feature flag is OFF for the tenant
When: I open the Hiring Team section
Then: only the legacy three roles are shown and behavior is unchanged
Considerations:
1. Localization: Role display names and the provisioning-source indicator are user-facing and must be translated across the 13+ supported languages for a consistent experience.
2. Analytics / Data Storage: Each assignment persists roleId, provisioningSource, and the assignment time window (role history) to the system of record and is emitted as a per-role CRM event to Snowflake so role attribution is reportable.
```
