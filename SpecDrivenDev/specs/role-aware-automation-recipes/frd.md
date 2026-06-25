# Role-Aware CRM Automation Recipes

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core (with Automation Engine — NEW dependency)
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/1k4q4KnczzpbJsmP0YuBXTiMNXaMyDHnJzrX2HEU93II/edit
- Customer: Multiple (enabler for Allianz & Disney role-aware workflows)

# 1. Executive Summary

## 1.1 Overview

CRM Automation recipes can reference job-level role in conditions and actions, but only the three baseline roles are available. Once granular recruiter-family roles exist, role-targeting recipes (for example, "send email to recruiter") would resolve to an undifferentiated recruiter and could target the wrong person. This spec makes the four Phase-1 roles selectable in recipe conditions and role-targeting actions, while keeping legacy recipes working unchanged. Scope is Impact area H (CRM Automation Recipes), exposing the four Phase-1 roles in recipe conditions and role-targeting actions. It depends on the role data model (spec 1) and introduces no new permission enforcement.

## 1.2 Problem in One Line

CRM Automation recipes expose only three baseline roles, so role-targeting recipes cannot branch on or reach the new granular recruiter-family roles and risk mis-targeting once expanded roles are enabled.

## 1.3 Solution in One Line

Make the four Phase-1 roles selectable in recipe conditions and role-targeting actions, resolve actions to the correct granular role, and preserve legacy recipe behavior with the legacy "Recruiter" mapped to Primary Recruiter.

## 1.4 Key Outcomes

- Four Phase-1 roles selectable in recipe conditions and role-targeting actions (up from three baseline roles).
- Confirmed role-targeting actions resolve to the correct granular role (3 of 3 confirmed actions, plus the full inventory).
- Zero regression for legacy recipes with the feature flag OFF or ON.
- Full inventory of role-exposing recipe surfaces confirmed and covered.

## 1.5 Document Status & Version History

- v1.0 | 2026-06-16 | Generated from PHEM-2109151 (SpecDrivenDev) | Initial draft

# 2. Problem Statement

## 2.1 Background & Context

CRM Automation recipes drive workflow actions (emails, forwarding) and can branch on conditions including job-level role. Recipe conditions and actions today expose only the three baseline roles (Recruiter, Hiring Manager, Interviewer). Several role-targeting actions resolve "recruiter" as a single undifferentiated role. There is a NEW dependency on the Automation Engine; today only the three baseline roles are accessible in some recipe actions. The full inventory of recipe conditions and actions exposing job-level role is not yet confirmed (Open Question H4).

## 2.2 User Pain Points

- Recipes cannot condition on or target the new granular roles (only 3 baseline roles available).
- Role-targeting actions like "Send Email To Recruiter For Application Withdrawal" cannot distinguish Primary vs. Secondary Recruiter.
- Risk that legacy recipes break or mis-target when expanded roles are enabled.

## 2.3 Business Impact of the Problem

- Recruiting Ops / Automation Admin | Cannot build role-specific automations; risk of mis-targeted actions
- Recruiter / Sourcer | May receive or miss automated actions intended for a specific role

## 2.4 Opportunity

Exposing the four Phase-1 roles in recipe conditions and role-targeting actions lets automation admins build precise role-specific automations and ensures automated messages and forwards reach the intended person, while preserving all existing recipe behavior. This is the enabler for role-aware workflows for customers such as Allianz and Disney.

Related problems:

- 1 | Recipe conditions/actions expose only 3 baseline roles | New roles unusable in automation | PHEM-2109151 (H1)
- 2 | Role-targeting actions resolve "recruiter" ambiguously | Wrong recipient (e.g. secondary vs primary) | PHEM-2109151 (H2)
- 3 | Legacy recipes must not break on flag ON/OFF | Backward compatibility risk | PHEM-2109151 (H3)
- 4 | Full inventory of role-exposing recipe surfaces unknown | Can't guarantee complete coverage | PHEM-2109151 (H4)

What the customer is asking for:

- 1 | Make the 4 roles selectable in recipe conditions and actions | Stated requirement | Related problem 1 | epic H1
- 2 | Role-targeting actions resolve to the correct granular role | Stated requirement | Related problem 2 | epic H2
- 3 | Legacy recipes keep working (flag OFF and ON) | Constraint | Related problem 3 | epic H3

## 2.5 Assumptions

- Legacy "Recruiter" maps cleanly to Primary Recruiter across recipes.
- The three actions in H2 are confirmed; the full inventory is pending (H4).
- Three confirmed actions to update (H2): Send Email To Recruiter For Application Withdrawal, Forward Candidate To Hiring Manager, Forward Profile. This is not the complete list (H4).

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Enable role-aware automation as an enabler for customer role-aware workflows (e.g. Allianz, Disney).
- Resolve role-targeting actions to the correct granular role; preserve legacy recipe behavior.

## 3.2 User Goals

- Expose the four Phase-1 roles as values in recipe conditions and role-targeting actions.
- Allow automation admins to branch automations by granular job-level role and target the right person.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Roles available in recipe conditions/actions | 3 baseline | 4 Phase-1 roles | TBD | Automation Engine PM
- Confirmed role-targeting actions updated | 0/3 | 3/3 (plus full inventory) | TBD | Automation Engine PM
- Legacy recipes regressed | N/A | 0 | TBD | Automation Engine PM

## 3.4 Non-Goals (Out of Scope)

- Hiring Manager split resolution (Phase 2; confirm Forward Candidate To Hiring Manager still resolves correctly in Phase 1).
- New permission gating via recipes (Phase 2).

## 3.5 Guardrail Metrics

- Legacy recipes regressed | N/A | 0 | Regression test (flag ON/OFF) | Automation Engine PM

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Recruiting Ops / Automation Admin

- Persona: Recruiting Ops / Automation Admin
- Description: Builds and maintains CRM Automation recipes and their conditions and actions.
- Goals: Build role-specific automations; ensure automated actions reach the correct granular role.
- Pain Points: Cannot build role-specific automations; risk of mis-targeted actions; only three baseline roles available.

## 4.2 Secondary Personas

### Recruiter / Sourcer

- Persona: Recruiter / Sourcer
- Description: Recipient of automated recipe actions (emails, forwards) tied to job-level role.
- Goals: Receive automated actions intended for their role and avoid receiving actions intended for others.
- Pain Points: May receive or miss automated actions intended for a specific role.

## 4.3 Persona Journey Map

### Current State (As-Is)

- Recipe conditions and actions expose only the three baseline roles (Recruiter, Hiring Manager, Interviewer).
- Role-targeting actions resolve "recruiter" as a single undifferentiated role, so Primary vs. Secondary Recruiter cannot be distinguished.

### Future State (To-Be)

- All four Phase-1 roles (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) are selectable in recipe conditions and role-targeting actions.
- Role-targeting actions resolve to the chosen granular role; legacy recipes continue to work unchanged.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Expose roles in recipe conditions

- As an automation admin
- I want the four Phase-1 roles selectable in recipe conditions
- So that I can branch automations by granular job-level role (e.g. "if hiring-team role is Sourcer")

Acceptance Criteria:

- Given a recipe condition builder (flag ON) | When an admin builds a condition on job-level role | Then Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator are all selectable
- Given a recipe with condition "hiring-team role is Sourcer" | When the recipe runs on a job with a Sourcer | Then the condition matches the Sourcer member
- Given the flag is OFF | When building a role condition | Then only the three baseline roles are exposed

### US-2: Role-targeting actions resolve granular role

- As an automation admin
- I want role-targeting recipe actions to resolve to the correct granular role
- So that automated emails and forwards reach the intended person

Acceptance Criteria:

- Given the "Send Email To Recruiter For Application Withdrawal" action (flag ON) | When it runs on a job with a Primary and a Secondary Recruiter | Then it resolves to the intended granular role rather than an undifferentiated recruiter
- Given the "Forward Profile" action | When an admin configures it to forward to a selected job-level role | Then the profile is forwarded to the holder of that role
- Given the "Forward Candidate To Hiring Manager" action in Phase 1 (HM split is Phase 2) | When it runs | Then it still resolves to the correct Hiring Manager (no regression)

### US-3: Preserve legacy recipes

- As an existing tenant
- I want my legacy recipes built on the three baseline roles to keep working
- So that enabling expanded roles introduces no regression

Acceptance Criteria:

- Given a tenant with the flag OFF | When legacy recipes run | Then behavior is identical to today
- Given a legacy recipe referencing "Recruiter" and a tenant with the flag ON | When the recipe runs | Then "Recruiter" resolves to Primary Recruiter and the recipe does not break

### US-4: Inventory & cover all role-exposing surfaces

- As a product owner
- I want the full inventory of recipe conditions and actions that expose job-level role confirmed and updated
- So that coverage of the four roles is complete

Acceptance Criteria:

- Given the automation recipe catalog | When the inventory is compiled | Then every condition/action exposing job-level role is listed
- Given the confirmed inventory | When the work is complete | Then each listed surface offers the four Phase-1 roles

## 5.2 Use Cases / Scenarios

### Use Case 1: Branch automation by granular role

- Actor: Recruiting Ops / Automation Admin
- Precondition: Feature flag ON; role data model available
- Main Flow: Admin opens the recipe condition builder, selects job-level role, and chooses one of the four Phase-1 roles (e.g. Sourcer) as the condition value.
- Alternate Flows: Flag OFF — only the three baseline roles are exposed.
- Postcondition: Recipe condition matches the chosen granular role at runtime.

### Use Case 2: Target the correct recruiter for an action

- Actor: Recruiting Ops / Automation Admin
- Precondition: Feature flag ON; job has Primary and Secondary Recruiter assigned
- Main Flow: Admin configures a role-targeting action (e.g. Send Email To Recruiter For Application Withdrawal, Forward Profile) to a selected granular role; the action resolves to the holder of that role at runtime.
- Alternate Flows: Forward Candidate To Hiring Manager still resolves to the correct Hiring Manager (HM split deferred to Phase 2).
- Postcondition: Automated action reaches the intended granular role holder.

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Core

- FR-01 | Roles in conditions | The four Phase-1 roles are selectable in recipe conditions (epic H1). Suggested story: Core – BE – Conditions. Addresses related problem 1, customer ask 1, source PHEM-2109151 (H1).
- FR-02 | Role-targeting actions | Role-targeting actions resolve to the chosen granular role (epic H2). Confirmed actions: Send Email To Recruiter For Application Withdrawal, Forward Candidate To Hiring Manager, Forward Profile. Suggested story: Core – BE – Actions. Addresses related problem 2, customer ask 2, source PHEM-2109151 (H2).
- FR-03 | Legacy compatibility | Legacy "Recruiter" maps to Primary Recruiter; recipes unchanged with flag OFF and not broken with flag ON (epic H3). Suggested story: Core – BE – Compatibility. Addresses related problem 3, customer ask 3, source PHEM-2109151 (H3).

### 6.1.2 Admin / Configuration

- FR-04 | Surface inventory | Confirm and cover the full inventory of recipe conditions and actions that expose job-level role so coverage of the four roles is complete (epic H4). Suggested story: Core – BE – Coverage. Addresses related problem 4, customer ask 1, source PHEM-2109151 (H4).

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01 | N/A — no performance requirements specified in source.

### 6.2.2 Scalability

- NFR-02 | N/A — no scalability requirements specified in source.

### 6.2.3 Security & Compliance

- NFR-03 | No new permission enforcement via recipes in Phase 1 (permission gating is Phase 2).

### 6.2.4 Availability & Reliability

- NFR-04 | Compatibility: legacy recipes unchanged with flag OFF; no break with flag ON.
- NFR-05 | Coverage: all confirmed role-targeting actions updated.

### 6.2.5 Accessibility

- NFR-06 | N/A — automation backend/config; no UX accessibility requirements specified.

## 6.3 Technical Constraints

- No new permission enforcement via recipes (Phase 2).
- Automation Engine must own exposing roles in recipe conditions/actions (NEW dependency).
- Depends on the role data model (spec 1) for role resolution.

## 6.4 Data Requirements

- Role resolution relies on the role data model (spec 1); job-level role is the trigger/condition input and the target of role-targeting actions.
- Legacy "Recruiter" is mapped to Primary Recruiter for role resolution.
- The four Phase-1 roles are: Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator.

# 7. UX / Design

## 7.1 Design Principles

- N/A — automation backend/config; UX Required: No.

## 7.2 User Flows

### 7.2.1 Primary Flow

- Admin selects job-level role in a recipe condition or role-targeting action and chooses one of the four Phase-1 roles; the recipe evaluates or targets that granular role at runtime.

### 7.2.2 Error / Edge Case Flow

- Flag OFF: only the three baseline roles are exposed.
- Legacy recipe referencing "Recruiter" with flag ON: resolves to Primary Recruiter without breaking.

## 7.3 Wireframes & Mockups

- N/A — no mockups; automation backend/config.

## 7.4 Accessibility Requirements

- N/A — automation backend/config.

## 7.5 Localization & Internationalization

- N/A — not specified in source.

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

- The Automation Engine exposes job-level role values in recipe conditions and role-targeting actions. CRM Core provides role resolution from the role data model. A shared feature flag gates exposure of the expanded roles.

## 8.2 Technology Stack

- N/A — not specified in source.

## 8.3 API Design

- N/A | N/A | N/A | No API design specified in source.

## 8.4 Integrations & Dependencies

- Automation Engine must own exposing roles in recipe conditions/actions (NEW dependency).
- Depends on the role data model (spec 1) for role resolution.
- Platform Config provides the feature flag and enablement.

## 8.5 Data Model

- Job-level role serves as both a recipe condition input and the target of role-targeting actions.
- Legacy "Recruiter" maps to Primary Recruiter.
- Phase-1 roles: Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator.

## 8.6 Migration & Rollout Strategy

- Gated by feature flag hiring_team_expanded_roles (shared).
- Flag OFF preserves today's behavior with three baseline roles; flag ON exposes the four Phase-1 roles.
- No auto-migration of legacy recipes to the new roles.

## 8.7 Monitoring & Observability

- N/A — not specified in source; regression testing of legacy recipes (flag ON/OFF) is required.

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Roles in conditions, role-targeting action resolution, legacy compatibility, surface inventory | TBD | Automation Engine / CRM Core
- Phase 2 | HM-split targeting; permission gating via recipes | TBD | TBD

## 9.2 Key Milestones

- Expose four Phase-1 roles in recipe conditions (FR-01).
- Role-targeting actions resolve granular role (FR-02).
- Legacy compatibility verified under flag OFF and ON (FR-03).
- Full inventory of role-exposing surfaces confirmed and covered (FR-04).

## 9.3 Dependencies & Blockers

- Automation Engine | Expose roles in recipe conditions/actions (NEW) | Required by FR-01–FR-04 | Open
- CRM | Role resolution from data model | Required by FR-01, FR-02 | Open
- Platform Config | Feature flag + enablement | Required by all | Open

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: Full inventory of role-exposing recipe surfaces is unknown, so coverage may be incomplete | Likelihood: Medium | Impact: High | Mitigation: Compile and confirm the complete inventory (H4) before declaring coverage complete | Owner: Automation Engine PM

## 10.2 Product / UX Risks

- Risk: Role-targeting actions mis-target the wrong recruiter (Primary vs. Secondary) | Likelihood: Medium | Impact: High | Mitigation: Resolve actions to the chosen granular role and verify the three confirmed actions | Owner: Automation Engine PM

## 10.3 Business / Compliance Risks

- Risk: Legacy recipes break or mis-target when expanded roles are enabled | Likelihood: Medium | Impact: High | Mitigation: Map legacy "Recruiter" to Primary Recruiter; regression test with flag OFF and ON | Owner: Automation Engine PM

## 10.4 Schedule Risks

- Risk: NEW Automation Engine dependency and pending inventory (H4) may delay completion | Likelihood: Medium | Impact: Medium | Mitigation: Confirm dependency ownership early and prioritize the inventory work | Owner: Automation Engine PM

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Which recipe conditions currently expose job-level role (full inventory)? | Automation Engine PM | TBD | Open
- 2 | Full set of role-targeting actions beyond the 3 confirmed (H4) | Automation Engine PM | TBD | Open
- 3 | Any legacy recipe patterns that don't map cleanly to Primary Recruiter | Automation Engine PM | TBD | Open
- 4 | Confirm the complete inventory (H4) | Automation Engine PM | TBD | Open

## 11.2 Decisions Log

- 2026-06-16 | Map legacy "Recruiter" to Primary Recruiter | Preserve legacy recipe behavior with flag OFF and avoid breakage with flag ON | Alternatives considered: auto-migrate legacy recipes (out of scope) | Decided By: TBD
- 2026-06-16 | Defer Hiring Manager split resolution and permission gating to Phase 2 | Keep Phase 1 scoped to exposing the four roles and resolving confirmed actions | Alternatives considered: include HM split in Phase 1 | Decided By: TBD

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — The leading recruiter role for a job; legacy "Recruiter" maps to this role.
- Secondary Recruiter — A supporting recruiter role for a job, distinct from the Primary Recruiter.
- Sourcer — A recruiter-family role focused on sourcing candidates.
- Coordinator — A recruiter-family role focused on coordination of the hiring process.
- Leading role — The primary holder of a role responsibility on a job (e.g. Primary Recruiter).
- Supporting role — A secondary holder assisting the leading role (e.g. Secondary Recruiter).
- Automation recipe — A configurable CRM Automation workflow with conditions and actions (e.g. send email, forward profile).
- Feature flag — A toggle (hiring_team_expanded_roles) gating exposure of the expanded roles.
- ATS — Applicant Tracking System.
- CRM — Candidate Relationship Management (Phenom CRM Core).

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner | Reporter (Jira) | Reporter of Epic PHEM-2109151 | N/A
- Katerina Bineva | Assignee (Jira) | Assignee of Epic PHEM-2109151 | N/A
- CRM Core Pod | Owning pod | Role resolution from data model; recipe surface coverage | N/A
- Automation Engine Pod | Owning pod (NEW dependency) | Expose roles in recipe conditions/actions | N/A
- Platform Config | Supporting team | Feature flag + enablement | N/A

## 12.3 References & Related Documents

- PHEM-2109151 — Phase 1 - Recruiter-Family Roles, Notification Framework & Analytics (Epic, area H) — https://phenompeople.atlassian.net/browse/PHEM-2109151
- PHEM-1965641 — Automation Engine must expose new roles in recipe conditions & actions (Initiative) — https://phenompeople.atlassian.net/browse/PHEM-1965641
- Google Doc — https://docs.google.com/document/d/1k4q4KnczzpbJsmP0YuBXTiMNXaMyDHnJzrX2HEU93II/edit
- Confluence — Not published
- Related: role data model (spec 1)

## 12.4 Revision & Approval Sign-off

- N/A (Author: Generated from PHEM-2109151) | Author | pending — Draft
- N/A | Product Owner | pending — Draft
- N/A | Automation Engine PM | pending — Draft
