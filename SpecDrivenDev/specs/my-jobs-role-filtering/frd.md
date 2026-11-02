# "My Jobs" Role Filtering, Spotlights & Workspace Views

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/17g42IWQRGc80LNpq10RcsLnKfmHOpBHLy8QC35YL2zA/edit
- Customer: Allianz (primary driver) — applies to all tenants

# 1. Executive Summary

## 1.1 Overview

A recruiter assigned to many jobs as a supporting recruiter sees all of them mixed together in "My Jobs," making it hard to focus on the jobs they actually lead. Allianz wants a user's default view to surface jobs where they hold the leading (Primary Recruiter) role, with supporting-role jobs grouped separately, and the new roles available as filter/spotlight conditions across the CRM. This spec scopes "My Jobs" filtering and role conditions in CRM filter/spotlight surfaces.

This is spec 4 of 6, covering Impact area F (Workspace Views, Filters & Spotlights). It resolves Allianz's "show me jobs where I'm the primary recruiter" ask. It depends on the role data model (spec 1) — specifically hierarchyPriority and the Leading/Supporting category.

## 1.2 Problem in One Line

"My Jobs" mixes jobs a user leads with jobs they merely support, and the granular roles are not available as filter or spotlight conditions, so users cannot focus on the jobs they actually lead.

## 1.3 Solution in One Line

Add job-level role as a filter dimension to "My Jobs" with a default view that surfaces Leading-role jobs and groups Supporting-role jobs separately, and expose the four Phase-1 roles as condition values across CRM filters and spotlights.

## 1.4 Key Outcomes

- Users can filter "My Jobs" by their job-level role and focus on jobs where they are the primary recruiter.
- The default "My Jobs" view surfaces jobs the user leads and groups supporting-role jobs separately.
- The four Phase-1 roles (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) become selectable values in filters and spotlights CRM-wide.
- A deterministic hierarchy tiebreaker places mixed-role jobs in the correct group.

## 1.5 Document Status & Version History

- v1.0 | 2026-06-16 | Generated from PHEM-2109151 (SpecDrivenDev) | Initial draft

# 2. Problem Statement

## 2.1 Background & Context

"My Jobs" today lists every job a user is assigned to as a recruiter, with no distinction between jobs they lead and jobs they merely support. Filters and Spotlights expose only the three baseline roles as condition values. The Allianz comment (Katerina Bineva) suggests solving this via a default filter / Spotlight view / hyperpersonalization flag rather than a hard system restriction — Phase 1 does not restrict access, only scopes the default view.

## 2.2 User Pain Points

- A user sees all jobs they are assigned to under "My Jobs," including ones where they are not the leading recruiter (ASRM-1570).
- There is no way to filter to "jobs where I am the primary recruiter."
- The new granular roles cannot be used as filter or spotlight condition values.

## 2.3 Business Impact of the Problem

- Recruiter (leading) | Time lost scanning irrelevant supporting-role jobs.
- Secondary Recruiter / Sourcer | Cluttered default view; slower to reach role-relevant work.
- Recruiting Ops | Cannot build saved views/spotlights on granular roles.

## 2.4 Opportunity

Related problems that connect to the main issue:

- 1 | "My Jobs" cannot filter by job-level role | Blocks Allianz's "jobs I lead" view | Source: PHEM-2109151 (F1), ASRM-1570
- 2 | No default scoping to Leading-role jobs | Supporting-role jobs clutter the default view | Source: PHEM-2109151 (F1)
- 3 | Mixed Leading + Supporting roles on one job need a placement rule | Ambiguous which group a job belongs to | Source: PHEM-2109151 (F2)
- 4 | New roles not selectable in filters/spotlights CRM-wide | Only 3 baseline roles exposed today | Source: PHEM-2109151 (F3)

What the customer is asking for:

- 1 | Filter "My Jobs" to jobs where I'm primary recruiter | Stated requirement | Related problem 1, 2 | Source: ASRM-1570
- 2 | Default view surfaces jobs I lead; supporting jobs grouped separately | Explicit request | Related problem 2, 3 | Source: epic F1
- 3 | New roles selectable in filter & spotlight conditions across CRM | Stated requirement | Related problem 4 | Source: epic F3

Customer requirements (as stated):

- "Jobs filters to show jobs where user is primary recruiter." (ASRM-1570, 25 March Allianz call)
- "Default should show jobs I'm the main recruiter of." (epic F1 paraphrase of Allianz)

The opportunity is to reduce click-path to role-relevant work (an Initiative KR in PHEM-1965641) by scoping a user's default workspace to the jobs they lead, while making the granular roles reusable across all CRM filter and spotlight surfaces. Solve via default filter / Spotlight, not a hard access restriction (Allianz scoping comment; Phase 1 has no permission enforcement).

## 2.5 Assumptions

- The default-view scoping is acceptable as a filter/grouping rather than a hard restriction (Allianz aligned).
- hierarchyPriority and the Leading/Supporting category from the role data model (spec 1) are available to drive default scoping and the tiebreaker.

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Let users filter "My Jobs" by job-level role and default to jobs where they hold a Leading role.
- Make the four Phase-1 roles selectable as condition values in filters and spotlights CRM-wide.
- Reduce the click-path from login to role-relevant work (Initiative click-path-reduction KR, PHEM-1965641).

## 3.2 User Goals

- A recruiter can focus on jobs they lead without scanning irrelevant supporting-role jobs.
- A supporting recruiter, sourcer, or coordinator can reach role-relevant work faster.
- A recruiting ops user can build saved views and spotlights on the granular roles.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Clicks from login to a role-relevant action (Secondary Recruiter) | Baseline: ~6 | Target: -20% (~4) | Timeline: Phase 1 | Owner: CRM PM (funnel instrumentation must be owned)
- Default "My Jobs" excludes non-leading jobs | Baseline: No | Target: Yes | Timeline: Phase 1 | Owner: CRM PM
- Roles available as filter/spotlight values | Baseline: 3 | Target: 4 (Phase-1 set) | Timeline: Phase 1 | Owner: CRM PM

## 3.4 Non-Goals (Out of Scope)

- Hard access restriction by role (Phase 2 visibility enforcement).
- Redesign of the "My Jobs" widget beyond role filter/grouping.

## 3.5 Guardrail Metrics

- Flag-OFF tenants see unchanged "My Jobs" and 3-role filters.
- Filtering performs at parity with the existing "My Jobs" load (no regression).

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Recruiter (Leading)

- Persona: Recruiter holding the Primary Recruiter (Leading) role on jobs.
- Description: Leads one or more jobs and also appears as a supporting recruiter on others.
- Goals: Focus on the jobs they lead; quickly reach the work that matters.
- Pain Points: Time lost scanning irrelevant supporting-role jobs in a mixed "My Jobs" list.

### Secondary Recruiter / Sourcer

- Persona: Supporting recruiter, sourcer, or coordinator on jobs.
- Description: Performs supporting recruiting work across several jobs.
- Goals: Reach role-relevant work without wading through an unscoped default view.
- Pain Points: Cluttered default view; slower to reach role-relevant work.

## 4.2 Secondary Personas

### Recruiting Ops

- Persona: Recruiting operations / admin building saved views and spotlights.
- Description: Configures filter and spotlight conditions for teams across the CRM.
- Goals: Build saved views and spotlights based on the granular roles anywhere conditions are built.
- Pain Points: Only the three baseline roles are exposed as condition values today.

## 4.3 Persona Journey Map

### Current State (As-Is)

- A recruiter opens "My Jobs" and sees every job they are assigned to, leading and supporting, mixed together.
- There is no way to filter to "jobs where I am the primary recruiter."
- When building a filter or spotlight, only the three baseline roles are available as condition values.

### Future State (To-Be)

- The default "My Jobs" view surfaces jobs the user leads, with supporting-role jobs grouped separately.
- The user can filter "My Jobs" by any of the four Phase-1 roles.
- Mixed-role jobs are placed deterministically using hierarchyPriority.
- The four Phase-1 roles are selectable as condition values across CRM filters and spotlights.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Filter "My Jobs" by job-level role

- As a recruiter
- I want to filter "My Jobs" by my job-level role
- So that I can focus on the jobs where I am the primary recruiter

Traceability: Related problem 1; Customer ask 1; Source: PHEM-2109151 (F1), ASRM-1570. Background: Part of Epic PHEM-2109151. Allianz wants this as a filter, not an access restriction. UX Required: Yes.

Acceptance Criteria:

- Scenario 1 (Filter to primary): Given a user assigned as Primary Recruiter on some jobs and Secondary Recruiter on others (flag ON), When they filter "My Jobs" to Primary Recruiter, Then only jobs where they are Primary Recruiter are listed.
- Scenario 2 (Filter to a supporting role): Given the same user, When they filter to Sourcer, Then only jobs where they are Sourcer are listed.
- Scenario 3 (Flag OFF unchanged): Given the flag is OFF, When the user opens "My Jobs," Then the legacy unfiltered behavior is unchanged.

Out of Scope: Restricting which jobs the user can access (Phase 2).

### US-2: Default leading-role view with grouping

- As a recruiter
- I want my default "My Jobs" view to surface jobs where I hold a Leading role and group Supporting-role jobs separately
- So that the jobs I lead are front and center

Traceability: Related problem 2, 3; Customer ask 2; Source: PHEM-2109151 (F1). UX Required: Yes.

Acceptance Criteria:

- Scenario 1 (Default surfaces leading jobs): Given a user with leading and supporting jobs (flag ON), When they open "My Jobs" with no filter applied, Then jobs where they are Primary Recruiter are surfaced and supporting-role jobs are grouped separately.
- Scenario 2 (Supporting jobs still reachable): Given the grouped supporting section, When the user expands/selects it, Then they can view their supporting-role jobs.

Out of Scope: Hiding supporting jobs entirely (they are grouped, not removed).

### US-3: Hierarchy tiebreaker for mixed roles

- As a recruiter on a job where I hold both a Leading and a Supporting role
- I want deterministic placement
- So that the job appears in the correct group

Traceability: Related problem 3; Customer ask 2; Source: PHEM-2109151 (F2). Technical note: Uses hierarchyPriority from the role registry (spec 1).

Acceptance Criteria:

- Scenario 1 (Mixed categories to leading): Given a user is Primary Recruiter and Coordinator on the same job (flag ON), When "My Jobs" groups the job, Then hierarchyPriority places it in the Leading group.
- Scenario 2 (Single category to no tiebreak): Given a user holds only supporting roles on a job, When the job is grouped, Then no tiebreaker is applied and it appears under Supporting.

Out of Scope: Tiebreaking across different jobs.

### US-4: New roles in filters and spotlights CRM-wide

- As a recruiting ops user
- I want the four Phase-1 roles selectable in filter and spotlight conditions across the CRM
- So that I can build role-based views anywhere, not just in "My Jobs"

Traceability: Related problem 4; Customer ask 3; Source: PHEM-2109151 (F3). UX Required: Yes.

Acceptance Criteria:

- Scenario 1 (Roles as filter values): Given a saved filter or list view condition builder (flag ON), When a user builds a condition on job-level role, Then Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator are all available as values.
- Scenario 2 (Roles in spotlights): Given a Spotlight condition on job-level role, When configuring it, Then the four Phase-1 roles are selectable.
- Scenario 3 (Flag OFF shows 3 roles): Given the flag is OFF, When building a role condition, Then only the three baseline roles are exposed.

Out of Scope: Adding roles to surfaces that do not build conditions on job-level role.

## 5.2 Use Cases / Scenarios

### Use Case 1: Recruiter focuses on jobs they lead

- Actor: Recruiter (Leading)
- Precondition: Feature flag ON; user holds Primary Recruiter on some jobs and supporting roles on others.
- Main Flow: The user opens "My Jobs"; the default view surfaces jobs where they are Primary Recruiter and groups supporting-role jobs separately; the user optionally filters to a specific role.
- Alternate Flows: If the flag is OFF, the legacy unfiltered "My Jobs" behavior is shown; if the user has no leading jobs, the leading group is empty and supporting jobs remain reachable.
- Postcondition: The user sees the jobs they lead front and center, with supporting jobs grouped and still accessible.

### Use Case 2: Recruiting ops builds a role-based spotlight

- Actor: Recruiting Ops user
- Precondition: Feature flag ON; the user is configuring a filter or spotlight that builds conditions on job-level role.
- Main Flow: The user opens the condition builder, selects job-level role, and chooses one of the four Phase-1 roles as the condition value.
- Alternate Flows: If the flag is OFF, only the three baseline roles are available; surfaces that do not build job-level-role conditions are unaffected.
- Postcondition: A saved view or spotlight scoped to a granular role is created.

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Core

- FR-01 (My Jobs role filter): "My Jobs" is filterable by job-level role. Suggested story: Core – FE – My Jobs filter. Addresses related problem 1; customer ask 1.
- FR-02 (Default leading view + grouping): The default view surfaces Leading jobs; Supporting jobs are grouped separately. Suggested story: Core – FE – Default view. Addresses related problem 2, 3; customer ask 2.
- FR-03 (Hierarchy tiebreaker): hierarchyPriority resolves placement when roles span categories. Suggested story: Core – BE/FE – Tiebreaker. Addresses related problem 3; customer ask 2.
- FR-04 (Roles in filters/spotlights): The 4 Phase-1 roles are selectable across CRM condition builders. Suggested story: Core – FE – Filter values. Addresses related problem 4; customer ask 3.

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01 (Performance): Filtering performs at parity with the existing "My Jobs" load.

### 6.2.2 Scalability

- NFR-02: N/A (no specific scalability target stated).

### 6.2.3 Security & Compliance

- NFR-03: N/A (no permission enforcement in Phase 1; visibility enforcement is Phase 2).

### 6.2.4 Availability & Reliability

- NFR-04 (Compatibility): Flag-OFF tenants see unchanged "My Jobs" and 3-role filters.

### 6.2.5 Accessibility

- NFR-05 (Accessibility): Filter controls are keyboard- and screen-reader-accessible.

## 6.3 Technical Constraints

- No hard access restriction (visibility enforcement is Phase 2).
- Depends on the role data model (spec 1) for hierarchyPriority and the Leading/Supporting category.
- Confirm the full inventory of filter/spotlight surfaces that build job-level-role conditions (Open Question F3).

## 6.4 Data Requirements

- Job-level role (the four Phase-1 roles) must be available as a filter/grouping dimension on "My Jobs" and across filter/spotlight condition builders.
- hierarchyPriority and the Leading/Supporting category (from spec 1) drive default scoping and the mixed-role placement tiebreaker.

# 7. UX / Design

## 7.1 Design Principles

- Scope, do not restrict: the default view focuses attention without removing access to supporting-role jobs.
- Consistency: the granular roles behave the same wherever filter and spotlight conditions are built.
- No disruption: flag-OFF tenants experience the unchanged legacy view.

## 7.2 User Flows

### 7.2.1 Primary Flow

- The user opens "My Jobs"; the default view surfaces Leading-role (Primary Recruiter) jobs and groups Supporting-role jobs separately; the user can apply a role filter to narrow to a specific role.

### 7.2.2 Error / Edge Case Flow

- A user holding both a Leading and a Supporting role on the same job has the job placed by hierarchyPriority into the Leading group; a user with no leading jobs sees an empty leading group with supporting jobs still reachable.

## 7.3 Wireframes & Mockups

- UX Required: Yes (My Jobs filter, default grouping, and filter/spotlight condition values). Specific wireframes/mockups: TBD; exact default grouping and labels for Leading vs Supporting to be defined by CRM Design.

## 7.4 Accessibility Requirements

- Filter and grouping controls must be keyboard navigable and screen-reader-accessible.

## 7.5 Localization & Internationalization

- N/A (no specific localization requirement stated; new role labels follow existing localization standards).

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

Add job-level role as a filter dimension to "My Jobs," with the default view surfacing Leading-role (Primary Recruiter) jobs and grouping Supporting-role jobs (Secondary Recruiter / Sourcer / Coordinator) separately. Use hierarchyPriority as the tiebreaker when a user holds both Leading and Supporting roles on a job. Expose the four Phase-1 roles as condition values everywhere filters and spotlights build conditions on job-level role.

Existing vs. new capabilities:

- "My Jobs" view | Exists today | Gap: no role filter or grouping.
- Filter/spotlight conditions on job-level role | Partial today (3 roles) | Gap: new roles not exposed.
- Default scoping to leading-role jobs | Does not exist today | Gap: new.

## 8.2 Technology Stack

- N/A (specific technology stack not specified; CRM workspace views, filters, and spotlights owned by the CRM Core pod).

## 8.3 API Design

- N/A | N/A | N/A | API design not specified in source.

## 8.4 Integrations & Dependencies

- CRM: "My Jobs" widget, filters, and spotlights.
- CRM (data model): hierarchyPriority and the Leading/Supporting category from the registry (spec 1).
- Platform Config: feature flag and per-tenant enablement.
- CRM Design: "My Jobs" and filter UX.

## 8.5 Data Model

- Relies on the role data model (spec 1): job-level role, hierarchyPriority, and the Leading/Supporting category.
- No new persistent entities introduced by this spec beyond consuming the registry/membership model.

## 8.6 Migration & Rollout Strategy

- Gated by the feature flag hiring_team_expanded_roles (shared). Note: epic F1 also references a possible hyperpersonalization flag for the default view — confirm.
- Flag OFF: unchanged "My Jobs" and 3-role filters.
- Flag ON: role filter, default leading-role grouping, mixed-role tiebreaker, and the four roles in filter/spotlight conditions are active.

## 8.7 Monitoring & Observability

- Funnel instrumentation for clicks from login to a role-relevant action (must be owned) to validate the click-path-reduction KPI.
- Functional verification that the default view excludes non-leading jobs and that the four roles appear as filter/spotlight values.

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Role filter, default leading-role grouping, tiebreaker, roles in filter/spotlight conditions | Target Date: TBD | Owner: Core
- Phase 2 | Visibility enforcement / role-based access restriction | Target Date: TBD | Owner: TBD

## 9.2 Key Milestones

- Confirm hierarchyPriority ordering for the four roles (Engineering).
- Confirm the full inventory of filter/spotlight surfaces that build job-level-role conditions (CRM PM).
- "My Jobs" role filter and default leading-role grouping delivered.
- Roles available as values across CRM filters and spotlights.

## 9.3 Dependencies & Blockers

- CRM | "My Jobs" widget, filters, spotlights | Required by FR-01 to FR-04 | Status: Open
- CRM (data model) | hierarchyPriority, category from registry | Required by FR-02, FR-03 | Status: Open
- Platform Config | Feature flag + enablement | Required by all | Status: Open
- CRM Design | "My Jobs" + filter UX | Required by FR-01, FR-02, FR-04 | Status: Open (UX Required: Yes)

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: hierarchyPriority ordering for the four roles is not yet confirmed, risking incorrect mixed-role placement | Likelihood: Medium | Impact: Medium | Mitigation: Confirm ordering with Engineering before implementing the tiebreaker | Owner: Engineering
- Risk: Full inventory of filter/spotlight surfaces is unknown, risking incomplete coverage | Likelihood: Medium | Impact: Medium | Mitigation: Inventory the surfaces that build job-level-role conditions (F3) | Owner: CRM PM

## 10.2 Product / UX Risks

- Risk: Default grouping/labels for Leading vs Supporting may not match user expectations | Likelihood: Medium | Impact: Medium | Mitigation: Define grouping and labels with CRM Design; validate with Allianz | Owner: CRM Design
- Risk: Ambiguity on whether the filter is a saved default or a per-session toggle | Likelihood: Medium | Impact: Low | Mitigation: Decide filter persistence model with CRM PM | Owner: CRM PM

## 10.3 Business / Compliance Risks

- Risk: Scoping the default view could be perceived as restricting access | Likelihood: Low | Impact: Medium | Mitigation: Keep Phase 1 as filter/grouping only (no hard restriction); communicate clearly | Owner: CRM PM

## 10.4 Schedule Risks

- Risk: Click-path-reduction KPI requires funnel instrumentation that is not yet owned | Likelihood: Medium | Impact: Low | Mitigation: Assign ownership for funnel instrumentation early | Owner: CRM PM

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Is the filter a saved default or a per-session toggle? | Owner: CRM PM | Due Date: TBD | Status: Open
- 2 | Exact default grouping/labels for Leading vs Supporting | Owner: CRM Design | Due Date: TBD | Status: Open
- 3 | Confirm hierarchyPriority ordering for the 4 roles | Owner: Engineering | Due Date: TBD | Status: Open
- 4 | Confirm the full inventory of filter/spotlight surfaces that build job-level-role conditions (F3) | Owner: CRM PM | Due Date: TBD | Status: Open
- 5 | Does the default view use the shared flag or a separate hyperpersonalization flag (epic F1)? | Owner: CRM PM + Platform Config | Due Date: TBD | Status: Open

## 11.2 Decisions Log

- 2026-03-25 | Solve "jobs where I'm primary recruiter" via default filter / Spotlight, not a hard access restriction | Phase 1 has no permission enforcement; Allianz aligned on scoping the default view | Alternatives Considered: Hard role-based access restriction (deferred to Phase 2) | Decided By: Allianz call (Katerina Bineva) / CRM PM

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — The lead recruiter role on a job (a Phase-1 job-level hiring-team role); the Leading role for "My Jobs" default scoping.
- Secondary Recruiter — A supporting recruiter role on a job (a Phase-1 job-level hiring-team role).
- Sourcer — A dedicated sourcing role on a job (a Phase-1 job-level hiring-team role).
- Coordinator — A coordinating role on a job (a Phase-1 job-level hiring-team role).
- Leading role — The primary/lead role driving a job (e.g., Primary Recruiter); jobs in this category are surfaced in the default "My Jobs" view.
- Supporting role — A secondary/assisting role on a job (e.g., Secondary Recruiter, Sourcer, Coordinator); grouped separately in the default view.
- hierarchyPriority — A role-registry attribute (spec 1) used as the tiebreaker when a user holds both a Leading and a Supporting role on the same job.
- Spotlight — A CRM surface that builds conditions (including on job-level role) to highlight or scope records.
- Feature flag — Toggle (hiring_team_expanded_roles, shared) gating the behavior; OFF preserves the legacy "My Jobs" and 3-role filters.
- ATS — Applicant Tracking System.
- CRM — Candidate Relationship Management (Phenom CRM Core).

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner | Reporter (Jira) | Reported / originated the epic context | Contact: N/A
- Katerina Bineva | Assignee (Jira) | Accountable for epic delivery; Allianz scoping input | Contact: N/A
- CRM / Core Pod | Owning pod (CRM Core) | "My Jobs" widget, filters, spotlights | Contact: N/A
- CRM Design | Supporting team | "My Jobs" and filter/grouping UX | Contact: N/A
- Platform Config | Supporting team | Feature flag + enablement | Contact: N/A

## 12.3 References & Related Documents

- PHEM-2109151 (Epic — Phase 1 - Recruiter-Family Roles, Notification Framework & Analytics; area F) — https://phenompeople.atlassian.net/browse/PHEM-2109151
- ASRM-1570 (Product Story — Allianz: "My Jobs" should show jobs where I'm the primary recruiter) — https://phenompeople.atlassian.net/browse/ASRM-1570
- PHEM-1965641 (Initiative — click-path reduction KR; "jobs I lead" filtering) — https://phenompeople.atlassian.net/browse/PHEM-1965641
- Spec 1 (role data model; hierarchyPriority and Leading/Supporting category) — referenced dependency.

## 12.4 Revision & Approval Sign-off

- N/A (Author) | Author | Sign-off Date: pending — Draft
- N/A | Reviewer | Sign-off Date: pending — Draft
- N/A | Approver | Sign-off Date: pending — Draft
