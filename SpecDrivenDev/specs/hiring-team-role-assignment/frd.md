# Hiring Team Role Assignment UI & ATS Role Mapping

- Status: Draft
- Author: Generated from PHEM-2109151 (SpecDrivenDev)
- Date: June 16, 2026
- Team / CRM Pod: Core
- Epic: PHEM-2109151
- Google Doc: https://docs.google.com/document/d/1UrjQCiu5g1YrB9yduuVQvi3QXx81naLZw9-2MlD2uZU/edit
- Customer: Multiple (Allianz on SuccessFactors, Disney on Workday)

# 1. Executive Summary

## 1.1 Overview

Customers need to assign granular recruiter-family roles to the people on a job — both manually in the CRM and automatically from the ATS where the distinction already exists in the payload. Disney's Primary Recruiter assigns Secondary Recruiter, Sourcer, and Coordinator by hand for both Workday and CRM-native jobs; Allianz needs the SuccessFactors primary/secondary recruiter distinction to flow through on job pull. This spec covers the Hiring Team assignment experience and the extension of existing ATS role mapping.

This is spec 2 of 6, covering impact areas B (Role Assignment & Hiring Team UI) and C (ATS Integration & Role Mapping). It depends on the role data model (spec 1). Sourcer and Coordinator are manual-only in Phase 1 (no ATS mapping).

## 1.2 Problem in One Line

Recruiting teams cannot assign the four granular recruiter-family roles on a job, and ATS job pull collapses the primary/secondary recruiter distinction that already exists in SF/WD payloads.

## 1.3 Solution in One Line

Surface granular role plus a provisioning-source indicator in the Hiring Team widget, allow manual assignment of all four roles on the job and during job creation, and extend the existing ATS job-pull mapping so SF/WD primary vs. secondary recruiter resolves to the new CRM roles.

## 1.4 Key Outcomes

- A Primary Recruiter or admin can assign and change all four Phase-1 roles on any job (created in CRM or pulled from ATS).
- Existing ATS job-pull mapping is extended so SF/WD primary vs. secondary recruiter resolves to distinct CRM roles.
- Manual assignment is available for all four Phase-1 roles on day one (up from three roles today).
- SF/WD primary vs. secondary recruiter is correctly mapped on pull instead of collapsing to a single recruiter.

## 1.5 Document Status & Version History

- v1.0 | 2026-06-16 | Generated from PHEM-2109151 (SpecDrivenDev) | Initial draft

# 2. Problem Statement

## 2.1 Background & Context

The CRM Hiring Team section on the Job Details page shows members under the legacy 3-role model. Some customers (Phenom Hire, no ATS feed) assign everyone manually; others (Allianz on SF, Disney on WD) receive hiring-team data via job pull but it collapses to a single "Recruiter."

A job-pull capability that maps ATS fields to CRM already exists; Phase 1 must identify and extend it, not build greenfield (epic area C preamble). Per the Allianz comment (Gustavo Denes): "For SFs and WD, they already have this concept of primary recruiter and additional recruiting team members."

## 2.2 User Pain Points

- A Primary Recruiter cannot assign or change Secondary Recruiter / Sourcer / Coordinator on a job (IDPRP-467).
- ATS job pull does not preserve the primary vs. additional recruiting-team distinction that already exists in SF/WD payloads (ASRM-1570).
- Phenom Hire customers with no ATS feed have no mechanism to assign the new roles at all.

Customer requirements (as stated):

- "A Primary Recruiter will assign these people in the CRM to the correct role as part of the hiring team for both workday and CRM jobs." (IDPRP-467)
- "Consume hiring team with different roles from job Pull." (ASRM-1570)

## 2.3 Business Impact of the Problem

- Recruiter / Sourcer | Cannot be placed in the correct function on a job
- Recruiting Ops | Manual workarounds; inconsistent team data across ATS and CRM jobs
- Candidate / Hiring Manager | Indirect

## 2.4 Opportunity

The customer is asking for:

- Primary Recruiter manually assigns support roles on WD & CRM jobs (stated requirement; addresses related problems 1, 2; source IDPRP-467).
- Consume hiring team with different roles from job pull (stated requirement; addresses related problem 3; source ASRM-1570).
- Show each member's role plus provisioning source (ATS vs manual) (explicit request; addresses related problem 1; source PHEM-2109151 B1).

Related problems driving the opportunity:

- 1 | No UI to assign/change the new roles on a job | Blocks Disney's manual assignment flow | PHEM-2109151 (B1, B2), IDPRP-467
- 2 | New roles not assignable during CRM Job Creation | Phenom Hire (no ATS) cannot staff a job | PHEM-2109151 (B3)
- 3 | Existing ATS job-pull mapping collapses primary/secondary | Allianz's SF distinction is lost | PHEM-2109151 (C1), ASRM-1570
- 4 | Sourcer/Coordinator have no ATS source field | Must be manual-only in Phase 1 | PHEM-2109151 (B4, C3)
- 5 | Per-customer enablement of mapping is unclear | Need to define how mapping turns on for Allianz/Disney | PHEM-2109151 (C2)

## 2.5 Assumptions

- The existing mapping engine can be extended without a rebuild.
- SF/WD payloads carry a usable primary vs. additional recruiter distinction for Allianz and Disney.
- ATS mapping in Phase 1 covers recruiter to Primary and recruiterTeam to Secondary for SF and WD only; Sourcer/Coordinator stay manual.

# 3. Goals & Success Metrics

## 3.1 Business Goals

- Let a Primary Recruiter or admin assign and change the four Phase-1 roles on any job (created in CRM or pulled from ATS).
- Extend existing ATS job-pull mapping so SF/WD primary vs. secondary recruiter resolves to the new CRM roles.

## 3.2 User Goals

- A recruiter can see each hiring-team member's granular role and how they were assigned (ATS vs manual).
- A Primary Recruiter can keep the hiring team accurate by assigning and changing support roles at any time.
- A Phenom Hire recruiter with no ATS feed can staff a job with all four roles during job creation.

## 3.3 Key Performance Indicators (KPIs) & Success Metrics

- Manual assignment available for all 4 Phase-1 roles | 3 roles | 4 roles, day one | At GA | CRM PM
- SF/WD primary vs secondary correctly mapped on pull | Collapsed to single recruiter | Distinct primary/secondary | At GA | Integration Experience PM

## 3.4 Non-Goals (Out of Scope)

- Auto-provisioning changes beyond existing job-pull mapping (Phase 2).
- ATS mapping for Sourcer/Coordinator.

## 3.5 Guardrail Metrics

- When the feature flag is OFF, the Hiring Team section continues to show the legacy 3-role display with no provisioning indicator (no regression).
- New role labels respect existing localization standards.
- Widget controls remain keyboard- and screen-reader-accessible.

# 4. User Personas & Target Audience

## 4.1 Primary Personas

### Persona: Primary Recruiter

- Description: Owns a job and the hiring team working it; assigns support roles for both ATS-fed and CRM-native jobs.
- Goals: Place the right people in the right function; keep the hiring team accurate over time.
- Pain Points: Cannot assign or change Secondary Recruiter / Sourcer / Coordinator on a job today.

### Persona: Recruiter / Sourcer

- Description: Member of the hiring team performing a specific recruiting function.
- Goals: Be placed in the correct function on a job and have it reflected in the CRM.
- Pain Points: Cannot be placed in the correct function on a job under the legacy 3-role model.

### Persona: Phenom Hire Recruiter (no ATS feed)

- Description: Recruiter at a customer with no ATS integration who creates CRM-native jobs.
- Goals: Staff the hiring team with all four roles during job creation without depending on an ATS pull.
- Pain Points: No mechanism to assign the new roles at all today.

## 4.2 Secondary Personas

### Persona: Recruiting Ops

- Description: Operations function maintaining consistent team data across ATS and CRM jobs.
- Goals: Eliminate manual workarounds and inconsistent team data.
- Pain Points: Manual workarounds; inconsistent team data across ATS and CRM jobs.

### Persona: Integration Engineer

- Description: Owns extending the ATS job-pull role mapping for SF/WD.
- Goals: Ensure primary vs. secondary recruiter resolves to the correct CRM roles on pull.
- Pain Points: Existing mapping collapses the primary/secondary distinction.

### Persona: Candidate / Hiring Manager

- Description: Downstream stakeholders affected indirectly.
- Goals: N/A (indirect).
- Pain Points: Indirect.

## 4.3 Persona Journey Map

### Current State (As-Is)

- The Hiring Team section shows members under the legacy 3-role model.
- ATS-fed customers (Allianz on SF, Disney on WD) receive hiring-team data on job pull, but it collapses to a single "Recruiter."
- A Primary Recruiter cannot assign or change support roles; Phenom Hire customers cannot assign the new roles at all.

### Future State (To-Be)

- The Hiring Team section shows each member's granular role plus a provisioning-source indicator (ATS vs manual).
- A Primary Recruiter or admin assigns and changes all four roles on the job and during job creation.
- ATS job pull preserves the primary vs. secondary recruiter distinction for SF/WD, mapping to the new CRM roles.

# 5. User Stories & Use Cases

## 5.1 User Stories

### US-1: Hiring Team role display + provisioning indicator

- As a recruiter
- I want to see each hiring-team member's granular role and whether it came from ATS or manual
- So that I know who does what and how they were assigned

Addresses (traceability): Related problem 1; Customer ask 3; Source PHEM-2109151 (B1). Relies on provisioningSource from the data-model spec.

Acceptance Criteria:

- Scenario 1 — Granular role shown: Given a job with members holding Primary Recruiter, Sourcer, and Coordinator roles (flag ON), When a user views the Hiring Team section, Then each member's granular role label is displayed.
- Scenario 2 — Provisioning indicator: Given a member assigned via ATS pull and another assigned manually, When the Hiring Team section renders, Then each shows an indicator distinguishing ATS-sourced from manually-assigned.
- Scenario 3 — Flag OFF unchanged: Given the flag is OFF, When the Hiring Team section renders, Then it shows the legacy 3-role display with no provisioning indicator.

Out of scope: Redesigning the Hiring Team widget layout beyond adding role + indicator.

### US-2: Manual assign / change support roles

- As a Primary Recruiter or admin
- I want to assign and change Secondary Recruiter, Sourcer, and Coordinator on a job's Hiring Team
- So that the team composition reflects who is actually working the job

Addresses (traceability): Related problem 1; Customer ask 1; Source PHEM-2109151 (B2, B4), IDPRP-467.

Acceptance Criteria:

- Scenario 1 — Assign a support role: Given a Primary Recruiter on a job (flag ON), When they add a user and select Sourcer, Then the user is saved as Sourcer with provisioningSource = manual and an assignment-history record opens.
- Scenario 2 — Change a role: Given a member currently assigned Secondary Recruiter, When the Primary Recruiter changes them to Coordinator, Then the role updates and history closes the prior window and opens a new one.
- Scenario 3 — All four roles available: Given the assignment control, When opening the role selector, Then Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator are all selectable.

Out of scope: Restricting which actions a role can take on the job (Phase 2 permissions).

### US-3: Assign roles in CRM Job Creation

- As a Phenom Hire recruiter with no ATS feed
- I want to assign all four Phase-1 roles while creating a job
- So that I can staff the hiring team without depending on an ATS pull

Addresses (traceability): Related problem 2; Customer ask 1; Source PHEM-2109151 (B3).

Acceptance Criteria:

- Scenario 1 — Assign during creation: Given a recruiter creating a CRM-native job (flag ON), When they reach the Hiring Team step, Then they can assign users to all four roles before the job is saved.
- Scenario 2 — Post-creation parity: Given a job created in CRM, When opened later, Then the same four roles can be assigned/changed via the Hiring Team widget.

Out of scope: ATS-fed jobs (handled by mapping, see US-4 / FR4).

### US-4: Extend ATS job-pull role mapping

- As an integration engineer
- I want the existing ATS job-pull role mapping extended
- So that the primary vs. secondary recruiter distinction already present in SF/WD payloads resolves to the new CRM roles

Addresses (traceability): Related problems 3, 4, 5; Customer ask 2; Source PHEM-2109151 (C1, C2, C3), ASRM-1570. Confirm current job-pull mapping behavior before scoping; mapping must reuse the existing engine.

Acceptance Criteria:

- Scenario 1 — SF primary/secondary mapping: Given an Allianz SF job pull with a recruiter and recruiterTeam members (flag ON, mapping enabled), When the job is pulled, Then recruiter maps to Primary Recruiter and recruiterTeam members map to Secondary Recruiter in CRM, each with provisioningSource = ats-auto.
- Scenario 2 — Workday equivalent: Given a Disney WD job pull distinguishing primary vs. additional recruiting team members, When the job is pulled, Then the distinction maps to Primary vs. Secondary Recruiter in CRM.
- Scenario 3 — Sourcer/Coordinator not mapped: Given any Phase-1 ATS pull, When the job is pulled, Then no member is auto-assigned Sourcer or Coordinator (manual only).
- Scenario 4 — Per-customer enablement: Given mapping is configured for a specific Phase-1 tenant, When that tenant's flag is ON and mapping enabled, Then the extended mapping applies only to that tenant per the defined enablement model.

Out of scope: Sourcer/Coordinator ATS mapping; role-aware auto-provisioning beyond job pull (Phase 2).

## 5.2 Use Cases / Scenarios

### Use Case 1: Disney Primary Recruiter staffs a Workday job

- Actor: Primary Recruiter
- Precondition: Flag ON; job pulled from Workday or created in CRM
- Main Flow: Primary Recruiter opens the Hiring Team widget, adds users, and assigns Secondary Recruiter, Sourcer, and Coordinator as needed.
- Alternate Flows: A member's role is changed; assignment history closes the prior window and opens a new one.
- Postcondition: The hiring team reflects the correct granular roles with manual provisioning source.

### Use Case 2: Allianz SuccessFactors job pull

- Actor: Integration Engine / Integration Engineer
- Precondition: Flag ON and mapping enabled for the Allianz tenant
- Main Flow: SF job pull delivers recruiter and recruiterTeam members; mapping resolves recruiter to Primary Recruiter and recruiterTeam to Secondary Recruiter with provisioningSource = ats-auto.
- Alternate Flows: No member is auto-assigned Sourcer or Coordinator.
- Postcondition: The CRM hiring team reflects the SF primary/secondary distinction.

### Use Case 3: Phenom Hire recruiter creates a CRM-native job

- Actor: Phenom Hire Recruiter (no ATS feed)
- Precondition: Flag ON; no ATS integration
- Main Flow: Recruiter creates a CRM-native job, reaches the Hiring Team step, and assigns all four roles before saving.
- Alternate Flows: Roles are assigned or changed later via the Hiring Team widget (post-creation parity).
- Postcondition: The job is staffed with all four roles without an ATS pull.

# 6. Requirements

## 6.1 Functional Requirements

### 6.1.1 Hiring Team UI (Role Assignment & Display)

- FR-01 | Role + provisioning display: The Hiring Team section shows each member's granular role and an ATS/manual provisioning indicator. (US-1; Core – FE – Hiring Team display)
- FR-02 | Manual assign/change: A Primary Recruiter or admin can assign and change the four roles post-creation, with assignment-history records. (US-2; Core – FE – Assignment UI)
- FR-03 | Assign in Job Creation: All four roles are assignable during CRM job creation, with post-creation parity. (US-3; Core – FE – Job Creation)

### 6.1.2 ATS Integration & Role Mapping

- FR-04 | Extend ATS mapping: Map SF recruiter to Primary Recruiter and recruiterTeam to Secondary Recruiter (and the Workday equivalent), with provisioningSource = ats-auto. (US-4; Core – BE – ATS mapping)
- FR-05 | Per-customer enablement: Define how mapping is enabled for Allianz (SF) and Disney (WD), applying only to the configured tenant. (US-4; Core – BE – ATS mapping)

## 6.2 Non-Functional Requirements

### 6.2.1 Performance

- NFR-01 | N/A in source; no specific performance targets stated for Phase 1.

### 6.2.2 Scalability

- NFR-02 | Per-customer enablement must apply mapping only to the configured tenant (no cross-tenant leakage).

### 6.2.3 Security & Compliance

- NFR-03 | Assignment available to Primary Recruiter or admin (no other gating in Phase 1).

### 6.2.4 Availability & Reliability

- NFR-04 | N/A in source.

### 6.2.5 Accessibility

- NFR-05 | Widget controls must be keyboard- and screen-reader-accessible.

Additional: New role labels respect existing localization standards.

## 6.3 Technical Constraints

- Sourcer/Coordinator: manual only in Phase 1.
- Depends on the role data model (spec 1) for roleId and provisioningSource.
- Reuse the existing ATS mapping engine; do not build a greenfield mapping engine.
- Integration Experience / Connectors owns the ATS job-pull mapping extension (ownership is an Open Question).

## 6.4 Data Requirements

- roleId and provisioningSource come from the role data-model spec (spec 1).
- provisioningSource values: manual (manual assignment) and ats-auto (ATS pull).
- Assignment-history records track role assignment windows (open on assign, close prior window and open new on change).

# 7. UX / Design

## 7.1 Design Principles

- Surface the granular role and provisioning source clearly within the existing Hiring Team widget without a broad redesign.
- Preserve the legacy 3-role experience when the feature flag is OFF.

## 7.2 User Flows

### 7.2.1 Primary Flow

- View Hiring Team: A recruiter views the Job Details Hiring Team section and sees each member's granular role and provisioning indicator.
- Assign / change: A Primary Recruiter assigns or changes Secondary Recruiter, Sourcer, or Coordinator via the assignment control, with all four roles selectable.
- Create with roles: A Phenom Hire recruiter assigns all four roles during the Hiring Team step of CRM job creation.

### 7.2.2 Error / Edge Case Flow

- Flag OFF: The Hiring Team section shows the legacy 3-role display with no provisioning indicator.
- Sourcer/Coordinator on ATS pull: No member is auto-assigned Sourcer or Coordinator; these remain manual only.

## 7.3 Wireframes & Mockups

- UX Required: Yes (FR-01, FR-02, FR-03).
- Figma link: TBD; the epic references a prototype image.

## 7.4 Accessibility Requirements

- Widget controls must be keyboard- and screen-reader-accessible.

## 7.5 Localization & Internationalization

- New role labels respect existing localization standards.

# 8. Architecture & Technical Approach

## 8.1 High-Level Architecture

Surface the granular role and a provisioning-source indicator in the Hiring Team widget on Job Details, allow assignment/change of the four roles there and in the CRM Job Creation flow, and extend the existing ATS job-pull role mapping so SF recruiter/recruiterTeam and the Workday equivalent resolve to Primary/Secondary Recruiter.

Existing vs. New:

- Hiring Team widget on Job Details | Exists today | Gap: shows only legacy roles; no provisioning indicator
- Manual role assignment | Partial today | Gap: only 3 roles; no Sourcer/Coordinator
- Assignment in Job Creation flow | Partial today | Gap: new roles not selectable
- ATS job-pull role mapping | Exists today | Gap: collapses primary/secondary; needs extension

## 8.2 Technology Stack

- N/A — not specified in source. CRM Core front-end (Hiring Team widget, Job Creation flow) and back-end ATS job-pull mapping engine.

## 8.3 API Design

- N/A — no API contract specified in source.

## 8.4 Integrations & Dependencies

- ATS job pull from SuccessFactors (Allianz) and Workday (Disney).
- Integration Experience / Connectors owns the ATS job-pull mapping extension (ownership is an Open Question).
- Depends on the role data model (spec 1) for roleId and provisioningSource.

## 8.5 Data Model

- roleId and provisioningSource provided by the role data-model spec (spec 1).
- Phase-1 roles: Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator.
- ATS mapping (Phase 1): SF recruiter to Primary, recruiterTeam to Secondary; Workday equivalent for primary vs. additional recruiting team members.

## 8.6 Migration & Rollout Strategy

- Gated by feature flag hiring_team_expanded_roles (shared with the data-model spec).
- Per-customer enablement defines how mapping turns on for Allianz (SF) and Disney (WD), applying only to the configured tenant.
- Phase 1: Manual assignment (all 4 roles), Job Creation assignment, SF/WD primary-secondary mapping, provisioning display.
- Phase 2: Role-aware auto-provisioning; Sourcer/Coordinator ATS mapping if source fields emerge.

## 8.7 Monitoring & Observability

- N/A — not specified in source.

# 9. Milestones & Timeline

## 9.1 Project Phases

- Phase 1 (this spec) | Manual assignment (all 4 roles), Job Creation assignment, SF/WD primary-secondary mapping, provisioning display | TBD | CRM / Integration Experience
- Phase 2 | Role-aware auto-provisioning; Sourcer/Coordinator ATS mapping if source fields emerge | TBD | TBD

## 9.2 Key Milestones

- Hiring Team UI (FR-01 to FR-03) delivered by CRM. | TBD
- ATS job-pull mapping extension (FR-04 to FR-05) delivered by Integration Experience. | TBD
- Flag + per-tenant enablement delivered by Platform Config. | TBD

## 9.3 Dependencies & Blockers

- CRM | Hiring Team widget, Job Creation flow | FR-01 to FR-03 | Open
- Integration Experience | Extend ATS job-pull mapping (SF/WD) | FR-04 to FR-05 | Open
- Platform Config | Flag + per-tenant enablement | All | Open
- CRM Design | Hiring Team / Job Creation UX | FR-01 to FR-03 | Open (UX Required: Yes)
- Role data model (spec 1) | roleId and provisioningSource | All | Dependency

# 10. Risks & Mitigations

## 10.1 Technical Risks

- Risk: The existing mapping engine cannot be extended without a rebuild | Likelihood: Medium | Impact: High | Mitigation: Confirm current job-pull mapping behavior before scoping; reuse the existing engine | Owner: Integration Experience / Connectors PM
- Risk: SF/WD payloads do not reliably distinguish primary vs. secondary for target tenants | Likelihood: Medium | Impact: High | Mitigation: Validate Allianz (SF) and Disney (WD) payloads before build | Owner: Integration Experience PM

## 10.2 Product / UX Risks

- Risk: Visual treatment of the provisioning indicator is undefined | Likelihood: Medium | Impact: Medium | Mitigation: Resolve CRM Design open question before implementation | Owner: CRM Design
- Risk: Ambiguity on single vs. multiple Primary Recruiters per job | Likelihood: Medium | Impact: Medium | Mitigation: Resolve open question with Basti + CRM PM | Owner: CRM PM

## 10.3 Business / Compliance Risks

- Risk: Per-customer enablement model unclear, delaying Allianz/Disney activation | Likelihood: Medium | Impact: Medium | Mitigation: Define enablement model as part of FR-05 | Owner: CRM PM / Integration Experience PM

## 10.4 Schedule Risks

- Risk: Cross-team dependencies (CRM, Integration Experience, Platform Config, CRM Design) all open | Likelihood: Medium | Impact: Medium | Mitigation: Sequence work and confirm ownership early | Owner: CRM PM

# 11. Open Questions & Decisions Log

## 11.1 Open Questions

- 1 | Visual treatment of the provisioning indicator | CRM Design | TBD | Open
- 2 | Can a job have multiple Primary Recruiters or exactly one? | Basti + CRM PM | TBD | Open
- 3 | Is role assignment mandatory or optional at creation? | CRM PM | TBD | Open
- 4 | What does the existing job-pull role mapping do per ATS (SF, WD)? On-by-default or manual? | Integration Experience / Connectors PM | TBD | Open
- 5 | Who owns the ATS to CRM role mapping? | Basti + Eng | TBD | Open
- 6 | Do SF (Allianz) and WD (Disney) payloads reliably distinguish primary vs. secondary? | Integration Experience PM | TBD | Open

## 11.2 Decisions Log

- 2026-06-16 | Sourcer and Coordinator are manual-only in Phase 1 (no ATS mapping) | No reliable ATS source field exists for these roles | Map Sourcer/Coordinator from ATS | SpecDrivenDev (from PHEM-2109151)
- 2026-06-16 | Phase 1 ATS mapping covers recruiter to Primary and recruiterTeam to Secondary for SF and WD only | This is the distinction that already exists in SF/WD payloads | Broader ATS mapping in Phase 1 | SpecDrivenDev (from PHEM-2109151)
- 2026-06-16 | Reuse the existing ATS mapping engine; do not build greenfield | A job-pull capability mapping ATS fields to CRM already exists | Build a new mapping engine | SpecDrivenDev (epic area C preamble)

# 12. Appendix

## 12.1 Glossary

- Primary Recruiter — Recruiter-family role that owns the job and the hiring team; can assign support roles.
- Secondary Recruiter — Supporting recruiter-family role assigned alongside the Primary Recruiter.
- Sourcer — Recruiter-family role focused on sourcing; manual-only in Phase 1.
- Coordinator — Recruiter-family role focused on coordination; manual-only in Phase 1.
- Leading — Designation for the primary/owning role on the hiring team.
- Supporting — Designation for additional (non-primary) recruiting-team roles.
- provisioningSource — Field indicating how a member was assigned: manual or ats-auto (ATS pull).
- Feature flag — hiring_team_expanded_roles; gates the expanded-roles experience (shared with the data-model spec).
- ATS — Applicant Tracking System.
- CRM — Customer Relationship Management (Phenom CRM Core).
- SF — SuccessFactors (Allianz's ATS).
- WD — Workday (Disney's ATS).

## 12.2 Stakeholders & RACI

- Sebastian Niewöhner (Basti) | Reporter / CRM PM | Accountable for product decisions (e.g., Primary Recruiter cardinality, mapping ownership) | N/A
- Katerina Bineva | Assignee | Responsible for epic delivery (PHEM-2109151) | N/A
- CRM Pod (Core) | Owning team | Responsible for Hiring Team UI and Job Creation (FR-01 to FR-03) | N/A
- Integration Experience / Connectors | Owning team | Responsible for ATS job-pull mapping extension (FR-04 to FR-05) | N/A
- Platform Config | Supporting team | Responsible for flag + per-tenant enablement | N/A
- CRM Design | Supporting team | Responsible for Hiring Team / Job Creation UX | N/A
- Gustavo Denes | Allianz contact | Provided SF/WD primary vs. additional recruiter context | N/A

## 12.3 References & Related Documents

- PHEM-2109151 (Epic — Phase 1, areas B, C): https://phenompeople.atlassian.net/browse/PHEM-2109151
- PHEM-1965641 (Initiative — strategic container): https://phenompeople.atlassian.net/browse/PHEM-1965641
- ASRM-1570 (Product Story — Allianz, consume hiring team roles from job pull on SF): https://phenompeople.atlassian.net/browse/ASRM-1570
- IDPRP-467 (Product Story — Disney, Primary Recruiter manually assigns support roles on WD + CRM jobs): https://phenompeople.atlassian.net/browse/IDPRP-467
- Disney process board (Miro) and scoping sheet linked from IDPRP-467.

## 12.4 Revision & Approval Sign-off

- Sebastian Niewöhner (Basti), CRM PM | Product Approver | Draft / pending
- Katerina Bineva, Epic Assignee | Delivery Owner | Draft / pending
- CRM Pod (Core) Lead | Engineering Approver | Draft / pending
- Integration Experience / Connectors Lead | Integration Approver | Draft / pending
