# PRD: Recruiter-Family Role Data Model, Registry, Migration & Feature Flag

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/1HQqfX4aR9kOPc8Z_ApH8bLSrkgP0FSK_c_Xm4lPvTEA/edit
- Customer: Multiple (Allianz, Disney, ThermoFisher)

# 1. Executive Summary

## 1.1 Overview

Phenom CRM models a job's hiring team with three undifferentiated job-level roles (Recruiter, Hiring Manager, Interviewer). Because two people sharing the "Recruiter" role on a job are treated identically, the platform cannot route notifications, scope "My Jobs" views, or attribute analytics by the real recruiting function a person performs. Allianz, Disney, and ThermoFisher are blocked by this single undifferentiated model. This initiative's foundation is a role data model capable of representing granular recruiter-family roles with the metadata, assignment history, and feature-flagged migration required for every downstream capability to become role-aware without a future data migration.

This document covers the foundational role data model — impact areas A (Role Data Model & Registry) and D (Data Model Changes, Migration & Feature Flag) of PHEM-2109151. It is the prerequisite for the notifications, "My Jobs" filtering, analytics, assignment, and automation specs (spec 1 of 6). Permission/visibility enforcement is out of scope (Phase 2); Phase 1 designs the seam only.

## 1.2 Problem in One Line

The CRM collapses every recruiting-function person on a job into a single undifferentiated "Recruiter" role, so the platform cannot route, scope, or attribute work by the actual role a person performs.

## 1.3 Solution in One Line

Introduce a predefined recruiter-family role registry plus expanded hiring-team membership, assignment history, and a design-only permission seam, all gated behind a per-tenant feature flag with full backward compatibility.

## 1.4 Key Outcomes

- A role registry and hiring-team data model representing the four Phase-1 recruiter-family roles with stable IDs, hierarchy, category, provisioning source, and assignment history.
- A model extensible to future predefined and custom roles and to permission/visibility associations — without a Phase-2 data migration.
- Zero regression for flag-off tenants; expanded roles ship behind a per-tenant feature flag.
- Phase-1 roles representable with full metadata (target: 4 roles with roleId/hierarchy/category/source/history vs. 3 roles, no metadata today).
- Phase-2 permission enforcement requires 0 data migrations because the seam is designed in Phase 1.

## 1.5 Document Status & Version History

- v1.0 | 2026-06-16 | Generated from PHEM-2109151 | Initial draft

# 2. Problem Statement

## 2.1 Background & Context

CRM job-level hiring team roles are currently limited to a small hardcoded set (Recruiter, Hiring Manager, Interviewer). Enterprise customers staff a job with multiple recruiting-function people — a leading recruiter plus supporting secondary recruiters, sourcers, and coordinators — but the CRM collapses all of them into a single "Recruiter" label. Because two people sharing the "Recruiter" role on a job are treated identically, every downstream behavior (notifications, views, analytics, automation) keys off this undifferentiated model.

Authoritative anchor: Epic PHEM-2109151 (Phase 1). PHEM-1965641 is the parent Initiative and provides the long-term role model and the "design the permission seam now, enforce later" decision. ThermoFisher's Sourcer/analytics ask is captured in the Epic/Initiative narrative; no separate readable ticket was provided. IDPRP-467 / PHEM-2014766 reference a customer-configurable / custom-role direction; Phase 1 ships a registry of predefined roles only — the custom-role builder is explicitly not built now.

## 2.2 User Pain Points

- All users added as "Recruiter" on a job are indistinguishable, so there is no way to mark who leads the job vs. who supports it (ASRM-1570).
- The shared role causes duplicate / inconsistent behavior when one person holds two roles on the same job (root of the Allianz duplicate-notification issue, SUP-107507) — a symptom of the data model, not just the notification engine.
- Disney cannot measure effort per role: a sourcer's or coordinator's workload is collapsed into "recruiter," so role-specific activity is not attributable (IDPRP-467).
- The hardcoded role set forces customers to fit their org structure into Phenom rather than the reverse (PHEM-2014766).

Customer requirements as stated:

- "In the CRM everyone has the same Role (Recruiter) — There's no way to differentiate between primary and secondary recruiters." (ASRM-1570)
- "Add the following roles as options within the hiring team … Secondary Recruiter, Sourcer, Coordinator … Keep the Phenom recruiter default role [as] the Disney primary recruiter on a job." (IDPRP-467)
- "Each role should have the ability to [be] tracked separately within analytics in the same manner that the Phenom default 'recruiter' role is tracked now." (IDPRP-467)

## 2.3 Business Impact of the Problem

- Recruiter / Sourcer — Cannot be assigned or recognized for the actual function they perform on a job.
- Recruiting Ops — Cannot report on or manage staffing of supporting roles; attribution is lost when teams change.
- Candidate / Hiring Manager — Indirect impact: mis-routed notifications and unclear ownership.

## 2.4 Opportunity

What the customer is asking for (the basis for this initiative):

- Differentiate Primary vs Secondary recruiter on a job (stated requirement; ASRM-1570).
- Add Secondary Recruiter, Sourcer, Coordinator as assignable roles; keep "Recruiter" as Primary (stated requirement; IDPRP-467).
- Track each role separately in analytics "the same manner … recruiter is tracked now" (stated requirement; IDPRP-467).
- Roles must eventually carry permission/visibility, e.g. Allianz RecView view-only (inferred need / constraint; PHEM-1965641).
- No regression for tenants not yet enabled (constraint; PHEM-2109151 D2).

Delivering a granular, metadata-rich role model unblocks notifications, "My Jobs" scoping, per-role analytics, assignment, and automation across multiple enterprise customers from a single foundational change.

## 2.5 Assumptions

- Field names expandedRole / provisioningSource / hierarchyPriority are illustrative pending Engineering confirmation (D1).
- Legacy "Recruiter" maps cleanly to Primary Recruiter for all tenants.
- Ask #4 (permission/visibility) is explicitly design-only in Phase 1 — the model must carry the seam but apply no enforcement.
- The "no rollback / forward-only" constraint (D4) tensions with the "no regression" goal: regression safety is achieved by the flag-off path, not by reverting an enabled tenant.

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Provide a role registry and hiring-team data model that represents the four Phase-1 recruiter-family roles with stable IDs, hierarchy, category, provisioning source, and assignment history.
- Make the model extensible to future predefined and custom roles and to permission/visibility associations — without a Phase-2 data migration.
- Ship behind a per-tenant feature flag with zero regression for flag-off tenants.

## 3.2 User Goals

- Recruiting Ops can staff, manage, and report on leading vs. supporting recruiter-family roles on a job.
- Recruiters and Sourcers are recognized and assignable for the actual function they perform.
- Analysts can attribute activity to the correct role even as teams change mid-requisition.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Regression for flag-OFF tenants on legacy 3-role behavior | Baseline: n/a | Target: 0 regressions | Timeline: Phase 1 GA | Owner: CRM / QA
- Phase-1 roles representable with full metadata | Baseline: 3 roles, no metadata | Target: 4 roles with roleId/hierarchy/category/source/history | Timeline: Phase 1 | Owner: CRM Engineering
- Phase-2 permission enforcement requiring data migration | Baseline: — | Target: 0 (seam designed in Phase 1) | Timeline: Phase 1 architecture sign-off | Owner: CRM Architect
- Measurement methods: regression test suite + tenant monitoring; schema review + data validation; architecture review sign-off.

## 3.4 Non-Goals (Out of Scope)

- Custom-role builder / tenant-named roles (Future; PHEM-2014766).
- Any permission or visibility enforcement (Phase 2).
- Hiring Manager split, Associate Interviewer, Resource Manager roles (Phase 2 / Future).

## 3.5 Guardrail Metrics

- Flag-off tenants must show zero behavior change (no regression to the legacy 3-role model).
- Schema changes must deploy without downtime.
- Legacy role/source fields must remain populated and readable while the flag is ON.

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Persona: Recruiter / Sourcer

- Description: A recruiting-function team member assigned to a job (leading or supporting capacity).
- Goals: Be assigned and recognized for the actual function performed on a job.
- Pain Points: Collapsed into a single "Recruiter" label; cannot be distinguished as primary, secondary, sourcer, or coordinator.

### Persona: Recruiting Ops Analyst

- Description: Owns staffing and reporting across hiring teams.
- Goals: Report on and manage staffing of supporting roles; keep attribution correct as teams change.
- Pain Points: Cannot report per role; attribution is lost when team membership or roles change.

### Persona: CRM Platform Engineer / Architect

- Description: Owns the hiring-team data model, registry, and the permission seam.
- Goals: A consistent, extensible role model that downstream surfaces can resolve and that avoids future data migrations.
- Pain Points: A metadata-only model would ignore the future permission/visibility seam and force a costly Phase-2 migration.

## 4.2 Secondary Personas

### Persona: Platform Admin

- Description: Controls per-tenant enablement and feature flags.
- Goals: Enable expanded roles per tenant with zero change for non-enabled tenants.
- Pain Points: Needs controlled, forward-only enablement without regressing live tenants.

### Persona: Candidate / Hiring Manager

- Description: Indirect consumers of hiring-team behavior.
- Goals: Correct routing and clear ownership.
- Pain Points: Mis-routed notifications and unclear ownership due to the undifferentiated model.

## 4.3 Persona Journey Map

### Current State (As-Is)

- A job's hiring team supports only Recruiter, Hiring Manager, Interviewer.
- Multiple recruiting-function people are all labeled "Recruiter."
- No leading vs. supporting distinction; no per-role attribution; no record of who held which role and when; no record of how an assignment was made.

### Future State (To-Be)

- A registry exposes Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator with stable metadata.
- Each membership carries expanded role, provisioning source, and hierarchy.
- Assignment history records role time windows; analytics attribution survives team changes.
- A design-only permission/visibility seam is carried in the model for Phase 2; all gated behind a per-tenant flag with legacy fields preserved.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Predefined recruiter-family role registry

- As a CRM platform engineer
- I want a registry of predefined job-level roles with stable metadata
- So that every product surface (notifications, filters, analytics, automation) can resolve and reason about granular roles consistently

Addresses: Related problem 1, 2; Customer ask 1, 2; Source PHEM-2109151 (A1, A2, A3), IDPRP-467, ASRM-1570. Background: Phase 1 registry holds exactly four roles — Primary Recruiter (= today's "Recruiter" default, preserved and not renamed), Secondary Recruiter, Sourcer, Coordinator. The schema must later hold additional predefined roles and tenant custom roles without rework.

Acceptance Criteria:

- Given the hiring_team_expanded_roles flag is ON for a tenant, When a service requests the job-level role registry, Then it returns Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator, each with a stable roleId, display name, hierarchyPriority, and category.
- Given a job whose legacy hiring team lists a "Recruiter", When the registry resolves that membership under the flag, Then the legacy "Recruiter" resolves to Primary Recruiter with no change to display for the customer.
- Given the registry, When a consumer reads a role's category, Then Primary Recruiter = Leading and Secondary Recruiter / Sourcer / Coordinator = Supporting.
- Given the registry schema, When a new predefined role definition is added in a future phase, Then it can be stored without altering the table structure, and no custom-role authoring UI exists in Phase 1.

Out of scope: Custom-role creation UI / tenant-named roles (PHEM-2014766, Future); Hiring Manager family, Interviewer family, Resource Manager.

### US-2: Extend hiring-team membership with role metadata

- As a CRM platform engineer
- I want each hiring-team membership to carry the expanded role, provisioning source, and hierarchy
- So that downstream features can route, filter, and report by the real function a person performs

Addresses: Related problem 1, 4; Customer ask 2; Source PHEM-2109151 (A3, A4, D1).

Acceptance Criteria:

- Given a member assigned as Sourcer on a job under the flag, When the membership is persisted, Then it stores the Sourcer roleId alongside the preserved legacy role field.
- Given a membership created manually, When it is saved, Then provisioningSource = manual; for an ATS-pulled membership, provisioningSource = ats-auto.
- Given Phase 1, When any membership is created, Then interview-invite-auto is never written (reserved for a later phase).

Out of scope: Producing interview-invite-auto assignments (later phase); Sourcer/Coordinator ATS mapping (manual only in Phase 1 — see ATS spec).

### US-3: Role assignment history / audit

- As a recruiting ops analyst
- I want the system to record who held which role on a job and the time window of that assignment
- So that attribution and reporting remain accurate as teams change

Addresses: Related problem 3; Customer ask 3; Source PHEM-2109151 (A5), IDPRP-467.

Acceptance Criteria:

- Given a user is assigned Secondary Recruiter on a job, When the assignment is saved, Then a history record captures user, roleId, job, and start timestamp.
- Given a user's role on a job changes from Secondary Recruiter to Primary Recruiter, When the change is saved, Then the prior record's end timestamp is set and a new record opens.
- Given analytics requests attribution for a reporting window, When a member's role changed mid-window, Then the history exposes which role applied during which sub-window.

Out of scope: The analytics report-builder dimension itself (see Per-Role Analytics spec); this story provides the underlying history only.

### US-4: Permission / visibility seam (design-only)

- As a CRM architect
- I want the model to associate permission and visibility attributes with a role and to express the global-to-job-level relationship
- So that Phase 2 can enforce gating without a data migration

Addresses: Related problem 5; Customer ask 4; Source PHEM-2109151 (A6, constraints), PHEM-1965641 (Architectural Background).

Acceptance Criteria:

- Given the flag is ON, When a role with associated permission/visibility attributes is read, Then the attributes are stored and retrievable but no action or visibility restriction is applied anywhere in Phase 1.
- Given a user with a global user-level role and a job-level role, When the relationship is recorded, Then the model can represent both layers and their association without defining a precedence rule (precedence is Phase 2).

Out of scope: Any enforcement of permissions or visibility (Phase 2 core); defining the precedence rule between global and job-level roles (Phase 2).

### US-5: Feature flag, backward-compatible schema & enablement

- As a platform admin
- I want expanded roles gated by a per-tenant feature flag with legacy fields preserved
- So that tenants not yet enabled experience zero change and enablement is controlled

Addresses: Related problem 6; Customer ask 5; Source PHEM-2109151 (D2, D3, D4), constraints.

Acceptance Criteria:

- Given hiring_team_expanded_roles is OFF for a tenant, When any hiring-team-dependent feature runs, Then the legacy 3-role behavior is unchanged and no expanded fields are read.
- Given the flag is ON for a tenant whose ATS mapping is ready, When the hiring team is read, Then expanded roles and metadata are active while legacy fields remain populated.
- Given a tenant has been enabled, When considering rollback, Then the rollout plan documents that there is no supported revert to the 3-role model.
- Given existing recruiter records on an enabling tenant, When the tenant is enabled, Then Primary/Secondary assignment is set either by a one-time backfill or by the next scheduled job-pull re-fetch (decision recorded with Engineering — D3).

Out of scope: Destructive cleanup of legacy fields (post-GA, Phase 2); the ATS mapping logic itself (see Assignment & ATS Mapping spec).

## 5.2 Use Cases / Scenarios

### Use Case 1: Assign a Sourcer to a job under the flag

- Actor: Recruiting Ops Analyst
- Precondition: hiring_team_expanded_roles is ON for the tenant.
- Main Flow: Analyst adds a user to the hiring team as Sourcer; the membership stores the Sourcer roleId with provisioningSource = manual; a history record opens with a start timestamp.
- Alternate Flows: If the membership is created via ATS pull, provisioningSource = ats-auto.
- Postcondition: The Sourcer is distinctly represented, attributable in analytics, and recorded in assignment history.

### Use Case 2: Enable a tenant with existing recruiter records

- Actor: Platform Admin
- Precondition: Tenant's ATS mapping is ready; flag is about to be turned ON.
- Main Flow: Admin enables the flag; legacy "Recruiter" memberships resolve to Primary Recruiter; Primary/Secondary assignment is set by one-time backfill or next job-pull re-fetch.
- Alternate Flows: If backfill is deemed unnecessary, normal job-pull cycles re-apply mapping (D3).
- Postcondition: Expanded roles active, legacy fields preserved; enablement is forward-only with no supported revert.

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Core — Role Registry & Model

- FR-01: Role registry — System provides a registry of predefined roles (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) with a flexible schema. (Story: Core – BE – Role registry)
- FR-02: Role metadata — Each role carries roleId, display name, hierarchyPriority, and category (Leading/Supporting). (Story: Core – BE – Role registry)
- FR-03: Membership expansion — Each hiring-team membership stores expanded role + provisioningSource (ats-auto / manual / interview-invite-auto reserved). (Story: Core – BE – Membership model)
- FR-04: Assignment history — System records role assignment time windows per member per job. (Story: Core – BE – Assignment history)
- FR-05: Permission seam (design-only) — Model can associate permission/visibility attributes and express the global-to-job-level relationship; no enforcement. (Story: Core – BE – Permission seam)

### 6.1.2 Admin / Configuration

- FR-06: Feature flag & backward compatibility — hiring_team_expanded_roles gates reads; legacy role/source preserved; per-tenant, forward-only. (Story: Core – BE – Flag + migration)
- FR-07: Enablement & backfill decision — Define per-tenant enablement; decide backfill vs. next job-pull re-fetch. (Story: Core – BE – Flag + migration)

### 6.1.3 Notifications & Alerts

- N/A in Phase 1. Notification routing is enabled by the role model produced here but is specified in a separate downstream spec.

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01: Schema changes deploy without downtime.

### 6.2.2 Scalability

- NFR-02: The registry must accommodate future predefined and custom roles without altering table structure.

### 6.2.3 Security & Compliance

- NFR-03: Permission/visibility attributes are stored but not enforced in Phase 1.

### 6.2.4 Availability & Reliability

- NFR-04: Backward compatibility — legacy role/source fields preserved; flag-off equals no behavior change (no regression for non-enabled tenants).

### 6.2.5 Accessibility

- N/A — backend / data-model foundation with no UX surface in Phase 1.

## 6.3 Technical Constraints

- Backward-compatible migration only; no destructive changes in Phase 1 (legacy field cleanup is post-GA Phase 2).
- No permission/visibility enforcement in Phase 1.
- Per-tenant enablement is forward-only — no supported rollback (D4).
- Field names (expandedRole, provisioningSource, hierarchyPriority) are a working assumption and must be confirmed against the current data model with Engineering before being treated as final (D1).

## 6.4 Data Requirements

- Role registry entries: roleId, display name, hierarchyPriority, category (Leading/Supporting).
- Hiring-team membership: expanded roleId, preserved legacy role field, provisioningSource (ats-auto / manual / interview-invite-auto reserved).
- Assignment history records: user, roleId, job, start timestamp, end timestamp (time window per member per job).
- Permission/visibility associations and the global-to-job-level relationship structure (stored, not enforced).
- hierarchyPriority is the tiebreaker used by the "My Jobs" filter spec when a user holds both Leading and Supporting roles on one job.

# 7. UX / Design

## 7.1 Design Principles

- N/A for Phase 1 — this is a backend / data-model foundation with no net-new UX. Legacy "Recruiter" display must remain unchanged for customers under the flag.

## 7.2 User Flows

### 7.2.1 Primary Flow

- N/A — no user-facing UI flow in Phase 1. The functional flow is system-level (registry resolution, membership persistence, history capture), covered in Section 5.2.

### 7.2.2 Error / Edge Case Flow

- Edge case: a user holds both a Leading and a Supporting role on one job — resolved by hierarchyPriority tiebreaker (consumed by the downstream "My Jobs" filter spec).
- Edge case: legacy "Recruiter" membership under the flag must resolve to Primary Recruiter with no display change.

## 7.3 Wireframes & Mockups

- N/A — no UX deliverable in Phase 1.

## 7.4 Accessibility Requirements

- N/A — no UX surface in Phase 1.

## 7.5 Localization & Internationalization

- TBD — role display names may require localization in later phases; not in scope for Phase 1.

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

Replace the hardcoded 3-role list with a predefined role registry and extend the hiring-team membership model to store each member's granular role plus its metadata. Persist role-assignment history so attribution survives team changes. Carry permission/visibility association structure and the global-to-job-level relationship in the schema (design-only). Gate all reads behind the hiring_team_expanded_roles feature flag with legacy fields preserved for backward compatibility, enabled per tenant and forward-only.

Existing vs. new:

- Job-level hiring team roles — Exists today partially (3 hardcoded); gap: no registry, no granular recruiter-family roles.
- Role metadata (hierarchy, category, provisioning source) — Does not exist today; new.
- Role assignment history / audit — Does not exist today; new.
- Permission/visibility association on a role — Does not exist today; new structure (design-only, no enforcement).
- Feature-flagged, backward-compatible schema — Partial today; new flag + dual-write of legacy + expanded fields.

## 8.2 Technology Stack

- N/A / TBD — implementation stack owned by CRM Core and Platform Config engineering; not specified in the source.

## 8.3 API Design

- N/A — internal service/registry resolution; no external API surface specified in Phase 1.
- Method: N/A | Endpoint: N/A | Auth: N/A | Description: Job-level role registry is consumed via internal services; concrete API contract TBD with Engineering.

## 8.4 Integrations & Dependencies

- CRM — Owns hiring-team data model and registry; foundation for all Phase-1 specs. Status: Open.
- Platform Config — Owns hiring_team_expanded_roles flag, schema, and per-tenant enablement; required before any tenant enablement. Status: Open.
- Integration Experience — Populates provisioningSource = ats-auto and primary/secondary on job pull; ATS mapping spec. Status: Open.
- Talent Analytics — Consumes assignment history (FR-04) for attribution; analytics spec. Status: Open.

## 8.5 Data Model

- Predefined role registry with roleId, display name, hierarchyPriority, category (Leading/Supporting).
- Hiring-team membership extended with expanded roleId + provisioningSource, retaining legacy role/source fields (dual-write).
- Assignment-history records with user, roleId, job, start/end timestamps.
- Permission/visibility associations and global-to-job-level relationship carried in schema (no enforcement).
- Field names expandedRole / provisioningSource / hierarchyPriority are a working assumption pending Engineering confirmation (D1).

## 8.6 Migration & Rollout Strategy

- Backward-compatible migration only; no destructive changes in Phase 1.
- Gate reads behind hiring_team_expanded_roles; legacy fields preserved.
- Per-tenant enablement, enabled once that tenant's ATS mapping is ready (Allianz on SuccessFactors, Disney on Workday, ThermoFisher considered). Forward-only — no supported rollback (D4).
- Backfill decision: Primary/Secondary assignment set by a one-time backfill or by the next scheduled job-pull re-fetch (D3); D3 is 2nd priority and likely unnecessary if job-pull cycles re-apply mapping — confirm with Engineering.

## 8.7 Monitoring & Observability

- Regression test suite plus tenant monitoring to verify flag-off tenants show zero behavior change.
- Schema review and data validation to verify the four roles are representable with full metadata.

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Deliverables: registry, membership expansion, assignment history, permission seam (design-only), flag + backward-compatible schema | Target Date: TBD | Owner: CRM Core
- Phase 2 | Deliverables: permission/visibility enforcement, precedence rule, legacy-field cleanup | Target Date: TBD | Owner: CRM Core / Platform

## 9.2 Key Milestones

- Architecture review sign-off confirming Phase-2 enforcement needs no data migration. (Target: TBD)
- Schema deployed without downtime; four roles representable with full metadata. (Target: TBD)
- First tenant enabled once ATS mapping is ready. (Target: TBD)

## 9.3 Dependencies & Blockers

- Platform Config flag, schema, and tenant enablement required before any tenant enablement (Open).
- Integration Experience ATS mapping required before enabling a tenant whose roles depend on job-pull provisioning (Open).
- Confirmation of current hiring-team data model and final field naming (D1, Open) blocks finalizing the schema.

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: Working-assumption field names (expandedRole, provisioningSource, hierarchyPriority) diverge from the live data model | Likelihood: Medium | Impact: Medium | Mitigation: Confirm naming/structure against current model with Engineering before finalizing (D1) | Owner: CRM Engineering
- Risk: Schema migration causes downtime or regresses existing 3-role tenants | Likelihood: Low | Impact: High | Mitigation: Backward-compatible, non-destructive migration; dual-write legacy + expanded fields; regression suite | Owner: CRM Engineering / QA

## 10.2 Product / UX Risks

- Risk: Legacy "Recruiter" does not map cleanly to Primary Recruiter for some tenant | Likelihood: Low | Impact: Medium | Mitigation: Validate mapping assumption per tenant during enablement | Owner: CRM PM
- Risk: Stakeholders expect a custom-role builder in Phase 1 | Likelihood: Medium | Impact: Low | Mitigation: Explicit non-goal; registry of predefined roles only; communicate scope | Owner: CRM PM

## 10.3 Business / Compliance Risks

- Risk: Permission/visibility seam carried but not enforced is mistaken for active enforcement | Likelihood: Low | Impact: Medium | Mitigation: Document design-only status; no action/visibility restriction applied in Phase 1 | Owner: CRM Architect

## 10.4 Schedule Risks

- Risk: Forward-only enablement (no supported rollback) increases pressure on enablement validation | Likelihood: Medium | Impact: High | Mitigation: Regression safety via flag-off path; define enablement validation owner; stage per-tenant rollout (D4) | Owner: Platform PM
- Risk: Backfill-vs-job-pull decision (D3) unresolved delays enablement | Likelihood: Medium | Impact: Medium | Mitigation: Confirm with Engineering early; default to job-pull re-fetch if backfill unnecessary | Owner: Engineering + Platform PM

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Confirm current hiring-team data model and final field naming/structure (D1) | Owner: Engineering | Due Date: TBD | Status: Open
- 2 | Phase-1 role set confirmed = Primary/Secondary Recruiter, Sourcer, Coordinator? | Owner: Basti | Due Date: TBD | Status: Open (Initiative marked Closed/Yes)
- 3 | Final membership field names validated against live model | Owner: Engineering | Due Date: TBD | Status: Open
- 4 | Retention period / granularity of history records | Owner: Engineering + Analytics | Due Date: TBD | Status: Open
- 5 | Dedicated backfill vs. normal job-pull cycles (D3)? Who owns enablement validation given forward-only? | Owner: Engineering + Platform PM | Due Date: TBD | Status: Open

## 11.2 Decisions Log

- 2026-06-16 | Phase 1 ships a registry of predefined roles only; no custom-role builder | Rationale: Scope foundation now, defer configurability | Alternatives Considered: Customer-configurable / custom-role builder (PHEM-2014766) | Decided By: Initiative PHEM-1965641
- 2026-06-16 | Precedence rule between global and job-level roles deferred to Phase 2 | Rationale: Model can represent both layers without defining precedence now | Alternatives Considered: Define precedence in Phase 1 | Decided By: Basti + Platform PM
- 2026-06-16 | Permission/visibility is design-only in Phase 1 (seam carried, no enforcement) | Rationale: Avoid a costly Phase-2 data migration | Alternatives Considered: Metadata-only model with no seam | Decided By: PHEM-1965641 (Architectural Background)
- 2026-06-16 | Per-tenant enablement is forward-only with no supported rollback (D4) | Rationale: Regression safety achieved by flag-off path, not by reverting enabled tenants | Alternatives Considered: Reversible enablement | Decided By: Epic PHEM-2109151

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — The leading recruiter on a job; equals today's default "Recruiter" role, preserved and not renamed. Category: Leading.
- Secondary Recruiter — A supporting recruiter on a job, distinct from the primary. Category: Supporting.
- Sourcer — A recruiting-function role focused on sourcing candidates; assignable and separately attributable. Category: Supporting.
- Coordinator — A recruiting-function role handling coordination on a job; assignable and separately attributable. Category: Supporting.
- Leading — Role category indicating the person who leads the job (Primary Recruiter).
- Supporting — Role category indicating supporting roles (Secondary Recruiter, Sourcer, Coordinator).
- provisioningSource — Metadata on a membership recording how the assignment was made: ats-auto (from ATS job pull), manual (manually assigned), interview-invite-auto (reserved for a later phase, never written in Phase 1).
- hierarchyPriority — A numeric tiebreaker on a role used to resolve which role applies when a user holds both Leading and Supporting roles on one job (consumed by the "My Jobs" filter spec).
- Feature flag (hiring_team_expanded_roles) — Per-tenant, forward-only flag gating expanded-role reads; flag-off preserves legacy 3-role behavior.
- Assignment history — Records of who held which role on a job and the time window (start/end), enabling attribution as teams change.
- Permission/visibility seam — Schema structure that can associate permission/visibility attributes with a role and express the global-to-job-level relationship; stored but not enforced in Phase 1.
- ATS — Applicant Tracking System (e.g. SuccessFactors, Workday) from which hiring-team data is pulled.
- CRM — Phenom Candidate Relationship Management product; the platform whose hiring-team role model this spec changes.

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner (Basti) | Role/Title: Reporter (PHEM-2109151) / Product | Responsibility: Accountable — initiative scope and role-set decisions | Contact: N/A
- Katerina Bineva | Role/Title: Assignee (PHEM-2109151) | Responsibility: Responsible — delivery of Phase-1 data model work | Contact: N/A
- CRM Core Pod | Role/Title: Owning engineering pod | Responsibility: Responsible — hiring-team data model, registry, assignment history | Contact: N/A
- Platform Config | Role/Title: Owning pod | Responsibility: Responsible — feature flag, schema, per-tenant enablement | Contact: N/A
- Integration Experience | Role/Title: Dependency pod | Responsibility: Consulted — ATS mapping / provisioningSource population | Contact: N/A
- Talent Analytics | Role/Title: Dependency pod | Responsibility: Consulted — consumes assignment history for attribution | Contact: N/A

## 12.3 References & Related Documents

- PHEM-2109151 (Epic — Phase 1 Recruiter-Family Roles, Notification Framework & Analytics): https://phenompeople.atlassian.net/browse/PHEM-2109151
- PHEM-1965641 (Initiative — Job-Level Hiring Team Member Roles): https://phenompeople.atlassian.net/browse/PHEM-1965641
- ASRM-1570 (Allianz — Additional Recruiter Role in CRM): https://phenompeople.atlassian.net/browse/ASRM-1570
- IDPRP-467 (Disney — Custom Hiring Team Roles in the CRM): https://phenompeople.atlassian.net/browse/IDPRP-467
- CUSP-5947 (Product Feedback — Additional Recruiter Role in CRM): https://phenompeople.atlassian.net/browse/CUSP-5947
- CUSP-6045 (Product Feedback — Distinguish recruiter permission sets): https://phenompeople.atlassian.net/browse/CUSP-6045
- PHEM-2014766 (Story — Customer-configurable job-level hiring team roles): https://phenompeople.atlassian.net/browse/PHEM-2014766
- SUP-107507 (Support ticket — Allianz duplicate-notification issue; referenced in epic, not directly readable)
- Notification-Structure-Options.md (referenced by epic; Phase 2 notification config)
- Structural authority: ../product-copilot-beta/policies/jira-story-rules.md, story.md, epic.md

## 12.4 Revision & Approval Sign-off

- Sebastian Niewöhner, Product (Reporter) | Role: Approver | Sign-off Date: Draft / pending
- Katerina Bineva, Assignee | Role: Delivery Owner | Sign-off Date: Draft / pending
- CRM Core Pod Lead | Role: Engineering Approver | Sign-off Date: Draft / pending
- Platform Config Lead | Role: Enablement Approver | Sign-off Date: Draft / pending
