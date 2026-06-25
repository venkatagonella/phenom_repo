# Role-Aware Notification Framework

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core (with Notifications / Messaging Platform — NEW dependency)
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/1kU5MFejItwYW596qV4jnw_AgSjADWbV0kDTJl4KGJR8/edit
- Customer: Allianz (primary driver) — applies to all tenants

# 1. Executive Summary

## 1.1 Overview

Every person sharing a role on a job receives the same notifications, and a person holding two roles on a job can receive duplicate or inconsistent notifications. Allianz wants notifications routed to the primary recruiter only (or a configured role set) and zero duplicates for multi-role users. This spec adds a role dimension to the notification framework so triggers route by the recipient's job-level role, with most-permissive de-duplication and curated per-role default profiles — delivering routing and defaults without a new settings screen. The spec covers Impact area E (Role-Aware Notifications) of the Phase 1 epic, resolves Allianz's "primary recruiter only" ask and the duplicate-notification issue (SUP-107507), and depends on the role data model (spec 1). Routing plus role default profiles only — no new settings UI (deferred to Phase 2).

## 1.2 Problem in One Line

Notifications have no role dimension, so all hiring-team members are over-notified and multi-role users receive duplicate alerts.

## 1.3 Solution in One Line

Add a role dimension to the notification framework that routes triggers by job-level role, de-duplicates to exactly one notification per trigger (most permissive wins), and ships curated per-role default profiles — with no new settings UI.

## 1.4 Key Outcomes

- Route notification triggers by the recipient's job-level role (primary vs. supporting).
- Guarantee exactly one notification per trigger per user, regardless of how many roles they hold on the job.
- Eliminate duplicate notifications for multi-role users (target: 0; baseline: occurs per SUP-107507).
- Support triggers reaching the primary recruiter only when configured (not possible today).
- Ship curated per-role default profiles with no new settings UI.
- Preserve notification volume/behavior for flag-OFF tenants (unchanged).

## 1.5 Document Status & Version History

- v1.0 | June 16, 2026 | Generated from PHEM-2109151 (SpecDrivenDev) | Initial draft reformatted into PRD template

# 2. Problem Statement

## 2.1 Background & Context

The notification framework delivers triggers to all hiring-team members of a job regardless of their function, and notification settings are per-trigger at the tenant level with no role awareness. The global → tenant → user cascade exists today; tenants customize via Phenom support. Today notification overrides are per-trigger for the whole tenant, with no role awareness. The epic specifies model B: Phenom ships curated default trigger profiles per role; no self-service admin UI in Phase 1. This is a NEW dependency on the Notifications / Messaging Platform team, not yet engaged.

## 2.2 User Pain Points

- Too many people on a job receive the same alerts; supporting recruiters get notification fatigue (ASRM-1570).
- A user holding two roles on the same job receives duplicate notifications for a single trigger (SUP-107507).
- There is no way to send a trigger to the primary recruiter only.

## 2.3 Business Impact of the Problem

- Recruiter / Sourcer | Notification fatigue; missed signal among noise
- Recruiting Ops | Support tickets to suppress duplicates; manual tenant tuning
- Candidate / HM | Indirect — delayed action on relevant alerts

## 2.4 Opportunity

Adding a role dimension to the notification framework resolves Allianz's "primary recruiter only" ask and the duplicate-notification issue while establishing a reusable, role-aware routing capability across all tenants. It reduces notification fatigue, removes support-driven manual tuning, and lays the schema groundwork for a future Digest state and self-service settings (Phase 2) without rework.

## 2.5 Assumptions

- Most-permissive dedup is the accepted rule pending formal PM sign-off.
- The Messaging Platform can add a role dimension within the ~6-week Phase-1 window (effort unconfirmed).
- "Most permissive wins" is the agreed dedup rule (narrative-confirmed in the epic; still flagged Open with Notifications PM + Basti).
- Schema should accommodate a future Digest state without migration; the Digest engine is not built here.

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Resolve Allianz's request to route notifications to the primary recruiter only.
- Eliminate duplicate notifications for multi-role users (SUP-107507).
- Reduce notification fatigue and support-driven manual tenant tuning across all tenants.

## 3.2 User Goals

- Primary recruiters receive the configured triggers; supporting roles receive only their curated subset.
- Multi-role users receive exactly one notification per trigger, never double-alerted or missed.
- Tenants get sensible per-role defaults with no configuration required.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Duplicate notifications for multi-role users on a job | Occurs (SUP-107507) | 0 | Phase 1 | Notifications / Messaging Platform (via notification logs / Allianz validation)
- Triggers reaching primary recruiter only (when configured) | Not possible | Supported | Phase 1 | CRM Core (via functional test)
- Notification volume/behavior for flag-OFF tenants | Baseline | Unchanged | Phase 1 | Notifications / Messaging Platform (via regression monitoring)
- Action rate on support-role notifications (initiative KR) | Baseline | +25% | TBD | TBD — owner must be assigned (via funnel instrumentation)

## 3.4 Non-Goals (Out of Scope)

- Redesigned self-service notification settings UI (Phase 2).
- Digest delivery engine (Phase 2; schema accommodates only).
- Per-role admin override matrix with user override (Phase 2, model B to C).
- Cross-job notification aggregation.

## 3.5 Guardrail Metrics

- No increase in dispatch latency or volume for flag-OFF tenants.
- Tenants with support-set customizations retain them with no regression.
- Zero misses: a trigger Off for all of a user's roles produces no notification and no error or duplicate.

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Persona: Primary Recruiter

- Persona: Primary Recruiter (Leading role on a job)
- Description: Owns the requisition and is the leading recruiter on the job.
- Goals: Receive the full configured set of relevant triggers for owned jobs; act quickly on relevant signal.
- Pain Points: Signal lost among noise when all hiring-team members get the same alerts.

### Persona: Supporting Recruiter / Sourcer / Coordinator

- Persona: Secondary Recruiter, Sourcer, Coordinator (Supporting roles on a job)
- Description: Supporting hiring-team members who collaborate on the job alongside the primary recruiter.
- Goals: Receive only the curated subset of triggers relevant to their function.
- Pain Points: Notification fatigue from receiving the full firehose by default.

### Persona: Multi-Role User

- Persona: User holding two or more roles on the same job
- Description: A person who simultaneously holds multiple roles (e.g., Primary Recruiter and Coordinator) on a single job.
- Goals: Receive exactly one notification per trigger, never double-alerted or missed.
- Pain Points: Duplicate notifications for a single trigger (SUP-107507).

## 4.2 Secondary Personas

### Persona: Recruiting Ops / Tenant Admin

- Persona: Recruiting Operations / Tenant Administrator
- Description: Manages tenant-level notification settings, today via Phenom support.
- Goals: Sensible per-role defaults without configuration; retain existing customizations with no regression.
- Pain Points: Support tickets to suppress duplicates; manual tenant tuning.

### Persona: Messaging Platform Engineer

- Persona: Notifications / Messaging Platform Engineer
- Description: Owns the notification framework that must add the role dimension, routing, and dedup.
- Goals: Map triggers per role with delivery states (Instant/Off) so routing can differ by job-level role.
- Pain Points: NEW dependency, team not yet engaged; effort and Phase-1 fit unconfirmed.

## 4.3 Persona Journey Map

### Current State (As-Is)

A trigger fires on a job and is delivered to all hiring-team members regardless of function. Notification settings are per-trigger at the tenant level with no role awareness. A user holding two roles on the same job receives duplicate notifications for a single trigger. There is no way to send a trigger to the primary recruiter only. Supporting recruiters experience notification fatigue, and Recruiting Ops file support tickets and manually tune tenant settings.

### Future State (To-Be)

A trigger fires and the dispatch engine resolves the recipient's job-level role(s) and applies the configured routing. Primary recruiters receive the configured triggers; supporting roles receive only their curated subset. Multi-role users receive exactly one notification per trigger using the most-permissive setting across their roles. Curated per-role default profiles apply with no configuration. The existing global to tenant to user cascade and personal per-trigger control continue to work.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Role dimension in notification framework

- As a Messaging Platform engineer
- I want notification triggers to be mappable per job-level role with delivery states Instant or Off
- So that routing can differ by role

Acceptance Criteria:

- Given the framework with the role dimension (flag ON) | When a trigger is configured for Primary Recruiter = Instant and Secondary Recruiter = Off | Then the configuration persists per role
- Given the delivery-state schema | When configuring a trigger | Then only Instant and Off are selectable; Digest exists in schema but is not offered
- Given the flag is OFF | When triggers are evaluated | Then per-trigger tenant-wide behavior is unchanged

### US-2: Role-aware dispatch routing

- As a primary recruiter
- I want to receive the configured triggers while Secondary Recruiter / Sourcer / Coordinator receive only their curated subset
- So that the right people get the right alerts

Acceptance Criteria:

- Given a trigger configured Instant for Primary Recruiter and Off for supporting roles (flag ON) | When the trigger fires on a job | Then only the Primary Recruiter receives it
- Given a Sourcer's curated profile allows a specific trigger | When that trigger fires | Then the Sourcer receives only triggers in their subset, not the full set
- Given a user's role differs across two jobs | When a trigger fires on each | Then routing uses the user's role on that specific job

### US-3: Most-permissive de-duplication

- As a user holding multiple roles on the same job
- I want exactly one notification per trigger
- So that I am never double-alerted or missed

Acceptance Criteria:

- Given a user is both Primary Recruiter and Coordinator on a job (flag ON) | When a trigger fires that both roles would receive | Then the user receives exactly one notification
- Given a trigger is Instant for one of the user's roles and Off for another | When the trigger fires | Then the user receives the notification (Instant wins)
- Given a trigger is Off for all of a user's roles | When it fires | Then the user receives no notification and no error/duplicate is generated

### US-4: Curated per-role default profiles

- As a tenant
- I want Phenom-curated default trigger sets per Phase-1 role
- So that supporting roles aren't flooded and no configuration is required

Acceptance Criteria:

- Given a tenant with the flag ON and no custom settings | When a user holds a given role on a job | Then they inherit the curated default profile for that role (Primary = full; supporting = curated subset)
- Given a user is Primary Recruiter on job A and Sourcer on job B | When triggers fire | Then they inherit the Primary profile for A and the Sourcer profile for B

### US-5: Preserve cascade & personal control

- As an existing tenant
- I want the global to tenant to user notification cascade and my support-set customizations to keep working
- So that role-aware routing introduces no regression

Acceptance Criteria:

- Given a tenant with custom notification settings via Phenom support | When the role dimension ships | Then those customizations are retained with no regression
- Given a user adjusts a per-trigger setting in personal Settings | When triggers fire | Then their personal control still applies within the role-aware model

## 5.2 Use Cases / Scenarios

### Use Case 1: Notify primary recruiter only

- Actor: Primary Recruiter
- Precondition: Flag ON; trigger configured Instant for Primary Recruiter and Off for supporting roles
- Main Flow: Trigger fires on a job; dispatch resolves job-level roles; routing delivers to Primary Recruiter only
- Alternate Flows: If supporting role's curated profile allows the trigger, that role also receives it within its subset
- Postcondition: Only the configured role(s) receive the notification; supporting roles are not over-notified

### Use Case 2: Single notification for a multi-role user

- Actor: User holding two roles on one job (e.g., Primary Recruiter and Coordinator)
- Precondition: Flag ON; trigger applies to more than one of the user's roles
- Main Flow: Trigger fires; dedup applies most-permissive setting across the user's roles; exactly one notification is delivered
- Alternate Flows: Trigger is Off for all of the user's roles -> no notification, no error or duplicate
- Postcondition: User receives at most one notification per trigger, never duplicated or missed

### Use Case 3: Default profiles applied without configuration

- Actor: Tenant / Recruiting Ops
- Precondition: Flag ON; tenant has no custom settings
- Main Flow: A user holds a role on a job; the curated default profile for that role is inherited (Primary = full; supporting = curated subset)
- Alternate Flows: User holds different roles across jobs -> profile inherited per job role
- Postcondition: Sensible per-role defaults apply with no setup; supporting roles are not flooded

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Core

- FR-01 Role dimension: Triggers mappable per role; states Instant/Off (Digest reserved in schema). Maps to US-1; addresses related problem 1, customer ask 1; source PHEM-2109151 (E1).
- FR-02 Role-aware routing: Dispatch routes by the recipient's job-level role; role is resolved from the specific job. Maps to US-2; addresses related problem 1, customer ask 1; source PHEM-2109151 (E2), ASRM-1570.
- FR-05 Cascade preservation: global to tenant to user cascade and personal per-trigger control remain intact with no regression. Maps to US-5; addresses related problem 4, customer ask 4; source PHEM-2109151 (E4).

### 6.1.2 Defaults

- FR-04 Role default profiles: Curated default trigger set per Phase-1 role (model B); inherited by job role (Primary = full; supporting = curated subset). Maps to US-4; addresses related problem 3, customer ask 3; source PHEM-2109151 (E5).

### 6.1.3 Notifications & Alerts

- FR-03 Most-permissive dedup: Exactly one notification per trigger per user; the most-permissive setting wins across the user's roles; Off for all roles yields no notification and no error/duplicate. Maps to US-3; addresses related problem 2, customer ask 2; source PHEM-2109151 (E3), SUP-107507.

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01 Performance: No increase in dispatch latency or volume for flag-OFF tenants.

### 6.2.2 Scalability

- NFR-02 Extensibility / Scalability: Schema accommodates a future Digest state without migration.

### 6.2.3 Security & Compliance

- NFR-03 Security & Compliance: N/A — no new security or compliance requirements identified in source.

### 6.2.4 Availability & Reliability

- NFR-04 Compatibility / Reliability: Tenants with support-set customizations retain them with no regression.

### 6.2.5 Accessibility

- NFR-05 Accessibility: N/A — no new UI in Phase 1.

## 6.3 Technical Constraints

- No new settings UI in Phase 1 (routing + defaults only).
- Per-role trigger lists are a business decision still open.
- Notifications / Messaging Platform must own the role-aware routing change — do not build custom routing logic in CRM. NEW dependency; team not yet engaged.
- Depends on job-level role resolution from the data-model spec.

## 6.4 Data Requirements

- Trigger-to-role mapping with delivery states: Instant, Off (Digest reserved in schema, not active).
- Curated default trigger profiles per Phase-1 role.
- Job-level role assignments (resolved from the role data model) to determine routing per job.
- Existing global to tenant to user cascade settings and personal per-trigger overrides must be preserved.

# 7. UX / Design

## 7.1 Design Principles

- No new settings UI in Phase 1; deliver routing and defaults transparently. Detailed design principles N/A for this backend-focused phase.

## 7.2 User Flows

### 7.2.1 Primary Flow

A trigger fires on a job. The dispatch engine resolves the recipient's job-level role(s), applies the configured per-role routing, de-duplicates to exactly one notification per trigger using the most-permissive setting, and delivers. No user-facing configuration screen is involved in Phase 1.

### 7.2.2 Error / Edge Case Flow

A trigger that is Off for all of a user's roles fires: the user receives no notification and no error or duplicate is generated. A multi-role user with conflicting per-role states (Instant vs Off) receives a single notification (Instant wins).

## 7.3 Wireframes & Mockups

- N/A — no UI in Phase 1.

## 7.4 Accessibility Requirements

- N/A — no UI in Phase 1.

## 7.5 Localization & Internationalization

- N/A — not specified in source.

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

Add a role dimension to the notification framework so a trigger can be mapped per role with delivery states Instant or Off (schema reserves Digest). The dispatch engine resolves the recipient's job-level role(s) and applies the configured routing, then de-duplicates so each trigger yields exactly one notification using the most-permissive setting across the user's roles. Phenom ships curated default profiles per Phase-1 role. The existing global to tenant to user cascade and personal per-trigger control continue to work. The role-aware routing change is owned by the Notifications / Messaging Platform team.

## 8.2 Technology Stack

- N/A — specific stack not defined in source. Role-aware routing implemented within the existing Notifications / Messaging Platform.

## 8.3 API Design

- N/A | N/A | N/A | API surface not defined in source

## 8.4 Integrations & Dependencies

- Notifications / Messaging Platform: owns the role dimension, routing, and dedup (NEW dependency, not yet engaged).
- CRM Core: provides job-level role resolution from the role data model (spec 1).
- Platform Config: feature flag and enablement.

## 8.5 Data Model

- Per-role trigger mapping with delivery states (Instant/Off; Digest reserved without migration).
- Curated default trigger profiles per Phase-1 role.
- Job-level role assignments used to resolve routing per job.
- Existing cascade and personal override structures preserved.

## 8.6 Migration & Rollout Strategy

- Gated by feature flag hiring_team_expanded_roles (shared).
- Flag OFF: per-trigger tenant-wide behavior unchanged (no regression).
- Schema accommodates future Digest state without migration.
- Forward-only: no new self-service UI in Phase 1; Phase 2 introduces UI, admin default matrix + user override, Digest, and association dimension (model B to C).

## 8.7 Monitoring & Observability

- Notification logs to validate zero duplicates for multi-role users (Allianz validation).
- Regression monitoring for flag-OFF tenants (volume/behavior unchanged).
- Funnel instrumentation for action rate on support-role notifications (owner must be assigned).

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Role dimension, role-aware routing, most-permissive dedup, curated default profiles; no UI | TBD (~6-week Phase-1 window) | Notifications / Messaging Platform + CRM Core
- Phase 2 | Self-service role-aware settings UI, admin default matrix + user override, Digest state, association dimension (model B to C) | TBD | TBD

## 9.2 Key Milestones

- Notifications / Messaging Platform engaged and effort confirmed for the Phase-1 window — TBD.
- Per-role curated trigger lists decided (Basti + customers) — TBD.
- Most-permissive dedup rule formally signed off (Notifications PM + Basti) — TBD.

## 9.3 Dependencies & Blockers

- Notifications / Messaging Platform: own role dimension, routing, dedup (NEW, not yet engaged) | Required by FR-01 to FR-05 | Open
- CRM: job-level role resolution from data model | Required by FR-02, FR-03 | Open
- Platform Config: feature flag + enablement | Required by all | Open

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: Messaging Platform cannot add the role dimension within the ~6-week Phase-1 window | Likelihood: Medium | Impact: High | Mitigation: Engage Notifications team early; confirm effort; descope if needed | Owner: Notifications PM (TBD)
- Risk: Job-level role resolution dependency (data-model spec) slips | Likelihood: Medium | Impact: High | Mitigation: Sequence behind spec 1; track cross-spec dependency | Owner: CRM Core

## 10.2 Product / UX Risks

- Risk: Per-role curated trigger lists undecided, blocking default profiles | Likelihood: Medium | Impact: Medium | Mitigation: Drive decision with Basti + customers; provide sensible interim defaults | Owner: Basti

## 10.3 Business / Compliance Risks

- Risk: Regression in existing tenant customizations or cascade | Likelihood: Low | Impact: High | Mitigation: Preserve cascade (FR-05); regression monitoring for flag-OFF tenants | Owner: Notifications / Messaging Platform

## 10.4 Schedule Risks

- Risk: Forward-only rollout with no self-service UI means no in-product remediation if defaults are wrong | Likelihood: Low | Impact: Medium | Mitigation: Validate defaults with Allianz before broad enablement; gate via feature flag | Owner: CRM Core

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Effort for Messaging team to add a role dimension; can it land in the Phase-1 window? | Notifications PM (TBD) | TBD | Open
- 2 | For each Phase-1 role, which triggers stay ON vs OFF? | Basti + customers | TBD | Open
- 3 | Confirm rule = one notification using most-permissive setting across roles | Notifications PM + Basti | TBD | Open (narrative-confirmed)
- 4 | Exact curated trigger list per role | Basti + customers | TBD | Open
- 5 | Interaction order between role defaults and personal overrides | Notifications PM | TBD | Open

## 11.2 Decisions Log

- June 16, 2026 | Adopt model B (Phenom ships curated default trigger profiles per role; no self-service admin UI in Phase 1) | Avoids building settings UI while delivering role-aware routing and sensible defaults | Model C (admin override matrix + user override) deferred to Phase 2 | Epic PHEM-2109151
- June 16, 2026 | Reserve a Digest delivery state in schema without building the engine | Allows future Digest without migration | Build Digest now (rejected for Phase 1 scope) | Epic PHEM-2109151
- TBD | Most-permissive wins as the dedup rule | One notification per trigger; never double-alert or miss | Other dedup orderings | Pending formal sign-off (narrative-confirmed)

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — Leading recruiter role on a job; owns the requisition and receives the full configured trigger set.
- Secondary Recruiter — Supporting recruiter role on a job; receives a curated subset of triggers.
- Sourcer — Supporting role focused on sourcing; receives a curated subset of triggers.
- Coordinator — Supporting role focused on coordination; receives a curated subset of triggers.
- Leading role — A job-level role designation (e.g., Primary Recruiter) that receives the full configured set.
- Supporting role — A job-level role designation (e.g., Secondary Recruiter, Sourcer, Coordinator) that receives only a curated subset.
- provisioningSource — Field indicating the source/origin of a role or notification provisioning. N/A — not detailed in source.
- Feature flag — hiring_team_expanded_roles (shared); gates role-aware notification behavior; OFF preserves existing per-trigger tenant-wide behavior.
- ATS — Applicant Tracking System; system of record for requisitions and candidates.
- CRM — Candidate Relationship Management; Phenom CRM Core, the recruiter experience platform in scope.

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner (Basti) | Reporter / Product (PHEM-2109151) | Responsible for per-role trigger decisions and dedup rule sign-off | N/A
- Katerina Bineva | Assignee (PHEM-2109151) | Accountable for epic delivery | N/A
- Notifications / Messaging Platform | Owning pod | Own role dimension, routing, and dedup | N/A
- CRM Core Pod | Owning pod | Job-level role resolution; spec ownership | N/A
- Platform Config | Supporting pod | Feature flag and enablement | N/A
- Notifications PM | Product | Confirm Messaging effort; dedup rule sign-off; defaults/override interaction | TBD

## 12.3 References & Related Documents

- PHEM-2109151 (Epic — Phase 1 anchor, area E): https://phenompeople.atlassian.net/browse/PHEM-2109151
- ASRM-1570 (Product Story — Allianz notifications to primary recruiter only; duplicate notifications): https://phenompeople.atlassian.net/browse/ASRM-1570
- PHEM-1965641 (Initiative — Notification framework needs a role dimension): https://phenompeople.atlassian.net/browse/PHEM-1965641
- SUP-107507 (Support ticket — Allianz duplicate-notification issue; referenced, not directly readable)
- Notification-Structure-Options.md (source doc — Phase 2 options reference)
- Google Doc: https://docs.google.com/document/d/1kU5MFejItwYW596qV4jnw_AgSjADWbV0kDTJl4KGJR8/edit

## 12.4 Revision & Approval Sign-off

- Sebastian Niewöhner, Product | Reporter / Product approver | Draft / pending
- Katerina Bineva, Epic Assignee | Delivery approver | Draft / pending
- Notifications PM, Product | Platform approver | Draft / pending
