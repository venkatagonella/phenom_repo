---
spec_id: 001-secondary-recruiter-role-enforcement
summary: "Secondary Recruiter role with recruiter-equivalent create permissions and Primary-only delete/close enforcement on job lifecycle actions"
type: feature
status: implemented
approval_state: approved
owners: [venkatagonella]
reviewers: [venkatagonella]
ticket_ids: [PHEM-2109151]
risk: medium
blast_radius: "Incorrect enforcement blocks legitimate Primary Recruiter job lifecycle actions or allows Secondary Recruiter to delete/close jobs"
touches: ["src/roles/**", "src/jobs/**", "src/permissions/**", "src/ui/**", "tests/**"]
amends: []
supersedes_reqs: []
compliance_tags: []
northstar_version: 0.1
originating_ide: cursor
last_validated_at: "2026-06-24"
---

# Secondary Recruiter Role & Job Lifecycle Permission Enforcement

## 1. Summary

Introduce a **Secondary Recruiter** job-level hiring-team role that inherits standard recruiter capabilities—including creating jobs from a template, a blank template, or by cloning an existing job—while **enforcing** that only a **Primary Recruiter** on a job's hiring team may delete or close that job. Secondary Recruiters are always denied delete and close, regardless of who created the job. The change ships behind the per-tenant `hiring_team_expanded_roles` feature flag with zero behavior change when the flag is off.

This increment delivers a reference implementation in the NorthStarCheck repository, modeling the permission-enforcement slice called out as Phase 2 in PHEM-2109151 while building on the recruiter-family role registry defined in Functional Spec 1.

## 2. Context discovered (Phase 0)

- **Steering reviewed:** No `northstar/steering/` files exist yet (greenfield repo). Product context from PHEM-2109151 Functional Spec 1 and `SpecDrivenDev/specs/recruiter-roles-data-model/frd.md`: CRM today collapses all recruiting-function members into a single undifferentiated "Recruiter" job-level role; platform RBAC (Admin, Recruiter, HM, Interviewer) exists but does not distinguish Primary vs Secondary at the job level.
- **Existing specs that overlap (`touches`):** None in `northstar/specs/`. Conceptual overlap with PHEM-2109151 Spec 1 (role registry, feature flag, permission seam). Related downstream specs (assignment, notifications, My Jobs, analytics, automation) are out of scope for this increment.
- **Requirements this change amends/supersedes:** None — net new northstar spec. Extends beyond official Phase 1 FRD scope by implementing permission enforcement (officially Phase 2).
- **Relevant code paths:** Greenfield — no prior implementation. Reference material: Recruiter Hub product overview (`product-copilot-beta/knowledge/recruiter-hub/product-overview.md`).
- **Current behavior:** All users on a job's hiring team labeled "Recruiter" are treated identically; any recruiter assigned to a job can perform lifecycle actions including delete and close. No Primary/Secondary distinction exists.
- **Human-confirmed scope decisions:**
  - **Enforcement scope:** Phase 2 permission enforcement (not design-only seam).
  - **Delete/close rule (B):** Only Primary Recruiter may delete or close a job; Secondary Recruiter may never delete or close any job.

## 3. Requirements (EARS)

- **REQ-001** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a service requests the job-level recruiter-family role registry, THE SYSTEM SHALL return at minimum **Primary Recruiter** and **Secondary Recruiter**, each with a stable `roleId`, display name, `hierarchyPriority`, and `category` (`Leading` for Primary, `Supporting` for Secondary).
  - *Acceptance:* Integration test requests the registry with flag ON and asserts both roles are present with the correct categories and stable IDs across repeated calls.

- **REQ-002** — WHEN the `hiring_team_expanded_roles` feature flag is ON AND a hiring-team membership carries the legacy role value `Recruiter`, THE SYSTEM SHALL resolve that membership to **Primary Recruiter** without changing the customer-visible display label for the legacy role.
  - *Acceptance:* Given a membership with legacy role `Recruiter`, role resolution returns Primary Recruiter while the legacy display field remains `Recruiter`.

- **REQ-003** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a user holds **Secondary Recruiter** on a job's hiring team (or holds Secondary Recruiter as their effective job-level recruiting role for a job-scoped action) AND the user attempts to **create a job** via template, blank template, or clone of an existing job, THE SYSTEM SHALL permit the action with the same outcome as a standard recruiter today (a new job record is created and the actor is recorded on the hiring team).
  - *Acceptance:* Three tests—create-from-template, create-blank, create-clone—each with a Secondary Recruiter actor succeed and produce a persisted job with the actor on the hiring team.

- **REQ-004** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a user holds **Secondary Recruiter** on a job's hiring team AND the user attempts to **delete** that job, THE SYSTEM SHALL reject the request with an authorization failure and SHALL NOT mutate or remove the job record.
  - *Acceptance:* Delete attempt by Secondary Recruiter returns HTTP 403 (or equivalent authorization error code) and the job record remains unchanged in storage.

- **REQ-005** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a user holds **Secondary Recruiter** on a job's hiring team AND the user attempts to **close** that job, THE SYSTEM SHALL reject the request with an authorization failure and SHALL NOT change the job's status to closed.
  - *Acceptance:* Close attempt by Secondary Recruiter returns HTTP 403 (or equivalent) and the job status field remains its pre-request value.

- **REQ-006** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a user holds **Primary Recruiter** on a job's hiring team AND the user attempts to **delete** or **close** that job, THE SYSTEM SHALL permit the action (subject to any pre-existing business rules unrelated to Primary/Secondary distinction, such as job state guards).
  - *Acceptance:* Delete and close attempts by Primary Recruiter on the same job each succeed when no unrelated business rule blocks the action.

- **REQ-007** — WHEN the `hiring_team_expanded_roles` feature flag is OFF for a tenant, THE SYSTEM SHALL preserve legacy recruiter behavior for delete, close, and create actions and SHALL NOT apply Primary/Secondary enforcement rules.
  - *Acceptance:* With flag OFF, a user with legacy `Recruiter` hiring-team membership can delete and close jobs as today; expanded role fields are not read for authorization.

- **REQ-008** — WHERE a user interface exposes delete or close controls for a job, IF the authenticated user holds **Secondary Recruiter** (and not Primary Recruiter) on that job's hiring team AND the feature flag is ON, THEN THE SYSTEM SHALL disable or hide those controls and SHALL still enforce REQ-004 and REQ-005 on the server for any direct API call.
  - *Acceptance:* UI test shows delete/close controls disabled or absent for Secondary Recruiter; a direct API call without UI still returns 403 per REQ-004/REQ-005.

- **REQ-009** — WHEN the `hiring_team_expanded_roles` feature flag is ON for a tenant AND a user holds both **Primary Recruiter** and **Secondary Recruiter** on the same job (duplicate or conflicting assignments), THE SYSTEM SHALL treat the user as **Primary Recruiter** for delete/close authorization decisions by selecting the role with the highest `hierarchyPriority` value (Leading / Primary wins over Supporting / Secondary).
  - *Acceptance:* User with both roles on one job can delete/close that job; a unit test asserts Primary Recruiter is selected when `hierarchyPriority(Primary) > hierarchyPriority(Secondary)`.

- **REQ-010** — WHEN a job lifecycle authorization check runs for delete or close AND the feature flag is ON, THE SYSTEM SHALL evaluate the actor's **job-level hiring-team role** (Primary vs Secondary) and SHALL NOT use job `createdBy` or job creator identity as the authorization criterion.
  - *Acceptance:* A Secondary Recruiter who created the job is still denied delete/close; a Primary Recruiter who did not create the job is permitted delete/close when assigned as Primary on the hiring team.

## 4. Non-functional requirements

- **NFR-001 (security):** Delete and close authorization checks SHALL execute on the server for every API entry point; client-side UI gating alone is insufficient. Unauthorized attempts SHALL return HTTP 403 (or equivalent) with no side effects on the job record.
- **NFR-002 (security):** Authorization decisions SHALL use the authenticated user identity and the persisted hiring-team membership for the target job; requests without a valid session SHALL receive HTTP 401 (or equivalent).
- **NFR-003 (perf):** The incremental latency added by the job-level role lookup on delete/close requests SHALL be ≤ 5 ms at p95 in the reference implementation's integration test harness (single-process, in-memory or local DB).
- **NFR-004 (reliability):** With `hiring_team_expanded_roles` OFF, regression tests SHALL demonstrate zero change in delete/close/create outcomes compared to the legacy code path baseline captured before this feature lands.

## 5. Out of scope

- Sourcer and Coordinator permission matrices (registry may list them for extensibility, but no enforcement rules in this increment).
- ATS job-pull role mapping and provisioning-source population.
- Role-aware notifications, My Jobs filtering, per-role analytics, and automation recipes (PHEM-2109151 specs 2–6).
- Custom-role builder / tenant-named roles.
- Global user-level role vs job-level role precedence beyond the same-job duplicate-role tiebreaker (REQ-009).
- Platform Admin override of delete/close restrictions.
- Assignment history / audit persistence (desirable follow-on; not required to prove delete/close enforcement).
- Production deployment to Phenom CRM services (this repo is a reference implementation).

## 6. Open questions

-

## Changelog

- v0.1.0 — 2026-06-24 — implemented — NorthStarCheck reference service
