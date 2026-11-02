# Per-Role Analytics, CRM Events & Report Builder

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core (with Talent Analytics — NEW dependency)
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/1hp-8tITLRo7q6E9lvFFplxB568RNECNJ5SnbccLDi98/edit
- Customer: Disney (primary driver), ThermoFisher (sourcing attribution)

# 1. Executive Summary

## 1.1 Overview

Because all recruiters on a job share one role, analytics collapses every person's activity into "recruiter," so a sourcer's or coordinator's distinct contribution cannot be measured. Disney needs each role tracked as a separate dimension with CRM events emitted per role and pullable in the report builder at parity with how "recruiter" is reported today; ThermoFisher needs the same for sourcing attribution. This spec defines per-role CRM events, the analytics dimension, and report-builder support, using role assignment history for accurate attribution over time.

This spec covers Impact area G (Analytics & Reporting) of the Phase 1 epic. It resolves Disney's per-role tracking ask and ThermoFisher's sourcing attribution. It depends on the role data model (spec 1), especially role assignment history (FR4 of spec 1).

## 1.2 Problem in One Line

All recruiter-family members on a job share one "recruiter" role, so analytics cannot separate or attribute each role's distinct activity.

## 1.3 Solution in One Line

Emit CRM events tagged with the actor's job-level role, expose each role as a distinct analytics dimension and report-builder field at recruiter parity, and attribute activity using role assignment history.

## 1.4 Key Outcomes

- Each Phase-1 role (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) becomes a distinct analytics dimension instead of "recruiter" only.
- CRM events are emitted per job-level role so role activity is separable downstream.
- The new roles are pullable in the report builder at parity with the current "recruiter" reporting.
- Attribution stays correct across mid-requisition role changes by using role assignment history.

## 1.5 Document Status & Version History

- v1.0 | 2026-06-16 | Generated from PHEM-2109151 (SpecDrivenDev) | Initial draft

# 2. Problem Statement

## 2.1 Background & Context

CRM emits events that flow to analytics keyed to the single "recruiter" role. The report builder lets customers report on recruiter activity, but there is no dimension for the granular recruiter-family roles. As a result, the report builder can report on recruiter activity in aggregate but cannot break it down by the specific role a member holds on a job.

## 2.2 User Pain Points

- A sourcer's or secondary recruiter's workload is collapsed into "recruiter," so per-role effort is not measurable (IDPRP-467).
- ThermoFisher cannot attribute sourcing activity to a dedicated Sourcer role.
- Attribution is lost when a member's role changes mid-requisition.

## 2.3 Business Impact of the Problem

- Recruiting Ops / Analyst | Cannot measure who is actually doing what on a job; no role-level reports.
- Sourcer / Secondary Recruiter | Contribution is invisible in reporting.
- Leadership | Cannot evaluate staffing effectiveness per role.

## 2.4 Opportunity

Related problems that connect to the main issue:

- 1 | CRM events keyed only to "recruiter"; no per-role dimension | Root cause — role activity not separable | Source: PHEM-2109151 (G1), IDPRP-467
- 2 | Report builder lacks role dimension at recruiter parity | Customers can't self-serve role-level reports | Source: PHEM-2109151 (G2)
- 3 | Attribution breaks when role changes mid-requisition | Reports become inaccurate over time | Source: PHEM-2109151 (G3)
- 4 | Unclear whether analytics keys on system-level vs job-level role today | Must confirm before emitting per-role events | Source: ASRM-1570 (analytics question)

What the customer is asking for:

- 1 | Track each role separately in analytics like "recruiter" today | Stated requirement | Related problem 1 | Source: IDPRP-467
- 2 | Pull the new roles in the report builder at recruiter parity | Stated requirement | Related problem 2 | Source: IDPRP-467
- 3 | Sourcing attribution to a dedicated Sourcer role | Stated requirement | Related problem 1 | Source: ThermoFisher (epic)
- 4 | Accurate attribution as teams change | Inferred need | Related problem 3 | Source: epic G3

Customer requirements (as stated):

- "Each role should have the ability to [be] tracked separately within analytics in the same manner that the Phenom default 'recruiter' role is tracked now." (IDPRP-467)
- "Analytics to consume those different roles." (ASRM-1570)
- ThermoFisher: dedicated Sourcer role for sourcing-attribution analytics (epic Why / initiative table).

## 2.5 Assumptions

- Current recruiter analytics keys on the job-level hiring-team role (to be confirmed).
- Report-builder parity is achievable in the Phase-1 window (Analytics effort unconfirmed).
- Report-builder parity within the Phase-1 window is an open question for the Analytics PM.

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Represent each Phase-1 role as a distinct analytics dimension and emit CRM events per role.
- Make the roles pullable in the report builder at parity with "recruiter."
- Use role assignment history so attribution stays correct as roles change.

## 3.2 User Goals

- Recruiting ops analysts can build role-level reports without engineering involvement.
- Data consumers can see each role's activity instead of a single collapsed "recruiter" value.
- Analysts get attribution that stays accurate when team members change roles.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Roles reportable as a distinct dimension | Baseline: "recruiter" only | Target: 4 Phase-1 roles | Timeline: Phase 1 | Owner: Talent Analytics PM
- Per-role CRM events emitted | Baseline: No | Target: Yes | Timeline: Phase 1 | Owner: Talent Analytics / CRM
- Attribution accuracy across mid-req role changes | Baseline: N/A | Target: Correct per history | Timeline: Phase 1 | Owner: Analytics + Engineering

## 3.4 Non-Goals (Out of Scope)

- New analytics visualizations beyond report-builder parity.
- System-level user-role reporting changes (this is job-level role reporting).
- New report templates or visualizations.
- Net-new metrics not tracked for "recruiter" today.
- New event types beyond tagging existing events with role.
- Retroactive re-attribution beyond what history supports.

## 3.5 Guardrail Metrics

- Flag-OFF tenants: no change to current recruiter analytics behavior.
- Events correctly attributed across role changes (no attribution loss or double counting).

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Recruiting Ops Analyst

- Persona: Recruiting Ops / Analyst
- Description: Builds and consumes recruiting reports; owns role-level reporting self-service.
- Goals: Build role-level reports without engineering; measure who is doing what on a job.
- Pain Points: Cannot measure who is actually doing what on a job; no role-level reports.

### Sourcer / Secondary Recruiter

- Persona: Sourcer / Secondary Recruiter
- Description: Performs sourcing or secondary recruiting work on a job alongside the primary recruiter.
- Goals: Have their distinct contribution reflected in reporting.
- Pain Points: Contribution is invisible because it is collapsed into "recruiter."

### Analytics / Data Consumer

- Persona: Analytics consumer / data engineer
- Description: Consumes CRM-sourced analytics datasets and dimensions.
- Goals: Query each Phase-1 role as a distinct dimension; emit and consume per-role events.
- Pain Points: Role activity collapsed into "recruiter"; no per-role dimension.

## 4.2 Secondary Personas

### Leadership

- Persona: Leadership
- Description: Evaluates staffing effectiveness and team performance.
- Goals: Evaluate staffing effectiveness per role.
- Pain Points: Cannot evaluate staffing effectiveness per role.

## 4.3 Persona Journey Map

### Current State (As-Is)

- All recruiter-family members share one "recruiter" role.
- CRM events and analytics collapse every person's activity into "recruiter."
- The report builder can report recruiter activity but cannot segment by granular role.
- Attribution is lost when a member's role changes mid-requisition.

### Future State (To-Be)

- CRM events are tagged with the actor's job-level role.
- Each Phase-1 role is a distinct analytics dimension.
- Analysts pull the new roles in the report builder at recruiter parity.
- Activity is attributed to the role held at the time of the event using assignment history.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Emit CRM events per job-level role

- As an analytics engineer
- I want CRM events tagged with the actor's job-level role
- So that each role's activity can be tracked separately downstream

Traceability: Related problem 1, 4; Customer ask 1, 3; Source: PHEM-2109151 (G1), IDPRP-467. Background: Part of Epic PHEM-2109151. Confirm whether current events key on system-level or job-level role.

Acceptance Criteria:

- Scenario 1 (Event tagged with role): Given a Sourcer performs a tracked CRM action on a job (flag ON), When the CRM event is emitted, Then it carries the Sourcer roleId for that job.
- Scenario 2 (Distinct from recruiter): Given a Secondary Recruiter and a Primary Recruiter each act on the same job, When events are emitted, Then each event is tagged with its respective role, not collapsed into one "recruiter."
- Scenario 3 (Flag OFF unchanged): Given the flag is OFF, When events are emitted, Then current recruiter event behavior is unchanged.

Out of Scope: New event types beyond tagging existing events with role.

### US-2: Analytics role dimension

- As a data consumer
- I want each Phase-1 role represented as a distinct dimension in analytics
- So that a sourcer's or secondary recruiter's activity is not collapsed into "recruiter"

Traceability: Related problem 1; Customer ask 1; Source: PHEM-2109151 (G1), IDPRP-467, ThermoFisher.

Acceptance Criteria:

- Scenario 1 (Role as a dimension): Given per-role events flowing to analytics (flag ON), When the dataset is queried, Then Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator are each available as dimension values.
- Scenario 2 (Parity with recruiter metrics): Given existing recruiter metrics, When the new roles are added as a dimension, Then the same metrics are computable per role.

Out of Scope: Net-new metrics not tracked for recruiter today.

### US-3: Roles in report builder

- As a recruiting ops analyst
- I want to pull the new roles in the report builder at parity with the default recruiter role
- So that I can build role-level reports without engineering involvement

Traceability: Related problem 2; Customer ask 2; Source: PHEM-2109151 (G2), IDPRP-467. UX Required: Yes (report builder surface).

Acceptance Criteria:

- Scenario 1 (Build a per-role report): Given the report builder (flag ON), When an analyst selects job-level role as a field, Then they can build a report segmented by the four Phase-1 roles.
- Scenario 2 (Parity behavior): Given a report built on "recruiter" today, When built on Sourcer instead, Then the builder offers the same capabilities and metrics.

Out of Scope: New report templates or visualizations.

### US-4: History-based attribution

- As an analyst
- I want activity attributed to the role a member held at the time of the event
- So that reports stay accurate when a member's role changes mid-requisition

Traceability: Related problem 3; Customer ask 4; Source: PHEM-2109151 (G3), spec 1 FR4. Technical note: Consumes role assignment history (spec 1, FR4).

Acceptance Criteria:

- Scenario 1 (Attribution before a role change): Given a member was Secondary Recruiter, then became Primary Recruiter (history recorded), When reporting on activity from before the change, Then that activity is attributed to Secondary Recruiter.
- Scenario 2 (Attribution after a role change): Given the same member, When reporting on activity after the change, Then it is attributed to Primary Recruiter.
- Scenario 3 (Window spanning a change): Given a reporting window spanning the role change, When the report runs, Then activity is split between the two roles per the history time windows.

Out of Scope: Retroactive re-attribution beyond what history supports.

## 5.2 Use Cases / Scenarios

### Use Case 1: Build a per-role activity report

- Actor: Recruiting ops analyst
- Precondition: Feature flag ON; per-role events flowing to analytics; report builder exposes job-level role.
- Main Flow: Analyst opens report builder, selects job-level role as a field, builds a report segmented by the four Phase-1 roles, and runs it.
- Alternate Flows: If a role has no activity in the window, it shows zero/no rows; if flag OFF, only "recruiter" is available.
- Postcondition: Analyst has a role-level report at parity with the recruiter report.

### Use Case 2: Attribute activity across a mid-requisition role change

- Actor: Analyst / data consumer
- Precondition: A member's role changed mid-requisition and the change is recorded in role assignment history.
- Main Flow: Analyst runs a report over a window spanning the change; the system attributes activity to the role held at each event time using history windows.
- Alternate Flows: Window entirely before the change attributes all to the prior role; window entirely after attributes all to the new role.
- Postcondition: Activity is correctly split or attributed per the assignment history.

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Core

- FR-01 (Per-role CRM events): CRM emits events tagged with the actor's job-level role. Suggested story: Core – BE – Per-role events. Addresses related problem 1, 4; customer ask 1, 3.
- FR-02 (Analytics role dimension): Each Phase-1 role is a distinct analytics field/dimension. Suggested story: Core – BE – Analytics dimension. Addresses related problem 1; customer ask 1.
- FR-03 (Report-builder parity): Roles are pullable in the report builder like "recruiter." Suggested story: Core – FE – Report builder. Addresses related problem 2; customer ask 2.
- FR-04 (History-based attribution): Attribution uses role assignment history. Suggested story: Core – BE – Attribution. Addresses related problem 3; customer ask 4.

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01: N/A (no specific performance target stated; report-builder behavior expected at parity with current recruiter reporting).

### 6.2.2 Scalability

- NFR-02: N/A (no specific scalability target stated).

### 6.2.3 Security & Compliance

- NFR-03: N/A (no specific security/compliance requirement stated).

### 6.2.4 Availability & Reliability

- NFR-04 (Data integrity): Events are correctly attributed across role changes (no loss or double counting).
- NFR-05 (Compatibility): Flag-OFF tenants see no change to current recruiter analytics.

### 6.2.5 Accessibility

- NFR-06: N/A (report builder surface; standard product accessibility applies, no specific requirement stated).

Additional parity requirement:

- NFR-07 (Parity): Role-level reporting is delivered at parity with current recruiter reporting.

## 6.3 Technical Constraints

- Confirm current analytics keys on job-level (not system-level) role before emitting per-role events.
- Talent Analytics must own per-role CRM events and the report-builder dimension. NEW dependency; pod not yet engaged.
- Depends on assignment history (spec 1).

## 6.4 Data Requirements

- CRM events must carry the actor's job-level roleId for the job.
- Each Phase-1 role (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) must be representable as a distinct analytics dimension value.
- Role assignment history (spec 1, FR4) is the attribution source; attribution is resolved to the role held at the time of each event using history time windows.

# 7. UX / Design

## 7.1 Design Principles

- Parity: role-level reporting should match existing recruiter reporting capabilities and metrics.
- No disruption: flag-OFF tenants experience no change.

## 7.2 User Flows

### 7.2.1 Primary Flow

- Analyst selects job-level role as a field in the report builder and builds a report segmented by the four Phase-1 roles, at parity with a recruiter-based report.

### 7.2.2 Error / Edge Case Flow

- A role with no activity in the selected window returns zero/no rows; reporting windows spanning a role change split activity per assignment-history time windows.

## 7.3 Wireframes & Mockups

- UX Required: Yes (report builder surface). Specific wireframes/mockups: TBD.

## 7.4 Accessibility Requirements

- N/A (no specific accessibility requirement stated; standard product accessibility applies).

## 7.5 Localization & Internationalization

- N/A (no specific localization requirement stated).

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

Emit CRM events tagged with the actor's job-level role so each Phase-1 role becomes a distinct data field/dimension in analytics. Expose those roles in the report builder at parity with the default recruiter role. Resolve attribution using the role assignment history (spec 1, FR4) so activity is credited to the role that applied at the time of the event.

Existing vs. new capabilities:

- CRM events to analytics | Exists today (recruiter) | Gap: not tagged per granular role.
- Analytics role dimension | Partial today (recruiter) | Gap: new roles missing.
- Report-builder role pull | Exists today (recruiter) | Gap: new roles not pullable.
- History-based attribution | Does not exist today | Gap: new.

## 8.2 Technology Stack

- N/A (specific technology stack not specified; CRM event pipeline, analytics platform, and report builder owned across CRM and Talent Analytics pods).

## 8.3 API Design

- N/A | N/A | N/A | API design not specified in source.

## 8.4 Integrations & Dependencies

- Talent Analytics: per-role CRM events, analytics dimension, report builder (NEW, not yet engaged).
- CRM: tag events with job-level role; expose assignment history.
- Platform Config: feature flag + enablement.
- Spec 1 (role data model): role assignment history (FR4 of spec 1).

## 8.5 Data Model

- Analytics dimension keyed on the job-level hiring-team role (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator).
- Role assignment history used as the attribution source, with time windows mapping events to the role held at the time.

## 8.6 Migration & Rollout Strategy

- Gated by feature flag hiring_team_expanded_roles (shared).
- Flag OFF: current recruiter analytics and events behavior unchanged.
- Flag ON: per-role events, analytics dimension, report-builder parity, and history-based attribution active.

## 8.7 Monitoring & Observability

- Event pipeline validation to confirm per-role CRM events are emitted.
- Reporting tests against assignment history to validate attribution accuracy.
- Report builder verification (Disney) that roles are reportable as a distinct dimension.

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Per-role events, analytics dimension, report-builder parity, history-based attribution | Target Date: TBD | Owner: Core + Talent Analytics
- Phase 2 / Future | Advanced role analytics, custom-role reporting | Target Date: TBD | Owner: TBD

## 9.2 Key Milestones

- Confirm whether current analytics keys on system-level vs job-level role (gating decision).
- Talent Analytics pod engaged on per-role events and report-builder dimension.
- Per-role CRM events emitted and validated.
- Report-builder parity verified with Disney.

## 9.3 Dependencies & Blockers

- Talent Analytics | Per-role CRM events, analytics dimension, report builder (NEW, not yet engaged) | Required by FR-01 to FR-04 | Status: Open
- CRM | Tag events with job-level role; expose assignment history | Required by FR-01, FR-04 | Status: Open
- Platform Config | Feature flag + enablement | Required by all | Status: Open

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: Current analytics may key on system-level user role rather than job-level role | Likelihood: Medium | Impact: High | Mitigation: Confirm keying with Analytics PM before emitting per-role events | Owner: Analytics PM (Sai/Ashish)
- Risk: Role assignment history granularity insufficient for required attribution windows | Likelihood: Medium | Impact: High | Mitigation: Validate history granularity against attribution requirements | Owner: Analytics + Engineering

## 10.2 Product / UX Risks

- Risk: Report-builder parity may not be achievable within the Phase-1 window | Likelihood: Medium | Impact: Medium | Mitigation: Confirm scope and effort with Talent Analytics PM; descope to parity-only | Owner: Talent Analytics PM

## 10.3 Business / Compliance Risks

- Risk: Talent Analytics is a NEW dependency not yet engaged, risking delivery | Likelihood: Medium | Impact: High | Mitigation: Engage Talent Analytics pod early and confirm ownership | Owner: Core PM / Talent Analytics PM

## 10.4 Schedule Risks

- Risk: Analytics effort to emit per-role events and add the report-builder dimension is unconfirmed | Likelihood: Medium | Impact: Medium | Mitigation: Obtain effort estimate; sequence against Phase-1 window | Owner: Talent Analytics PM

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Is current recruiter analytics tracked on system-level user role or job-level hiring-team role? | Owner: Analytics PM (Sai/Ashish) | Due Date: TBD | Status: Open
- 2 | Effort to emit per-role events + add report-builder dimension; achievable in Phase-1 window? | Owner: Talent Analytics PM (TBD) | Due Date: TBD | Status: Open
- 3 | Is report-builder parity achievable within the Phase-1 window? | Owner: Talent Analytics PM | Due Date: TBD | Status: Open
- 4 | Is history granularity sufficient for the required attribution windows? | Owner: Analytics + Engineering | Due Date: TBD | Status: Open

## 11.2 Decisions Log

- N/A | No decisions recorded yet | N/A | N/A | N/A

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — The lead recruiter role on a job (a Phase-1 job-level hiring-team role).
- Secondary Recruiter — A supporting recruiter role on a job (a Phase-1 job-level hiring-team role).
- Sourcer — A dedicated sourcing role on a job; needed by ThermoFisher for sourcing attribution.
- Coordinator — A coordinating role on a job (a Phase-1 job-level hiring-team role).
- Leading role — The primary/lead role driving a job (e.g., Primary Recruiter).
- Supporting role — A secondary/assisting role on a job (e.g., Secondary Recruiter, Sourcer, Coordinator).
- Assignment history (role assignment history) — Time-windowed record of which role a member held on a job; used as the attribution source (spec 1, FR4).
- Feature flag — Toggle (hiring_team_expanded_roles, shared) gating the per-role behavior; OFF preserves current recruiter behavior.
- ATS — Applicant Tracking System.
- CRM — Candidate Relationship Management (Phenom CRM Core), which emits the events that flow to analytics.

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner | Reporter (Jira) | Reported / originated the epic context | Contact: N/A
- Katerina Bineva | Assignee (Jira) | Accountable for epic delivery | Contact: N/A
- Talent Analytics PM | Owning pod (Talent Analytics) | Responsible for per-role CRM events, analytics dimension, report builder | Contact: N/A
- Analytics PM (Sai/Ashish) | Analytics PM | Confirm analytics role keying (system-level vs job-level) | Contact: N/A
- CRM / Core Pod | Owning pod (CRM Core) | Tag events with job-level role; expose assignment history | Contact: N/A
- Platform Config | Supporting team | Feature flag + enablement | Contact: N/A

## 12.3 References & Related Documents

- PHEM-2109151 (Epic — Phase 1 - Recruiter-Family Roles, Notification Framework & Analytics) — https://phenompeople.atlassian.net/browse/PHEM-2109151
- IDPRP-467 (Product Story — Disney: track each role separately in analytics; report-builder parity) — https://phenompeople.atlassian.net/browse/IDPRP-467
- PHEM-1965641 (Initiative — Analytics separability KR; ThermoFisher sourcing attribution) — https://phenompeople.atlassian.net/browse/PHEM-1965641
- ASRM-1570 (Product Story — Allianz: analytics to consume the different roles) — https://phenompeople.atlassian.net/browse/ASRM-1570
- ThermoFisher (epic narrative — dedicated Sourcer role for sourcing attribution).
- Spec 1 (role data model; role assignment history FR4) — referenced dependency.

## 12.4 Revision & Approval Sign-off

- N/A (Author) | Author | Sign-off Date: pending — Draft
- N/A | Reviewer | Sign-off Date: pending — Draft
- N/A | Approver | Sign-off Date: pending — Draft
