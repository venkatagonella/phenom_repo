# Domain Requirements: PHEM-2190578

**Story:** [CRM Core: Creation of Job Expiry Field in Job creation - Core](https://phenompeople.atlassian.net/browse/PHEM-2190578)  
**Parent Epic:** [PHEM-2117038 — UnPost Job based on Job expiry, Job Status and Hired count](https://phenompeople.atlassian.net/browse/PHEM-2117038)  
**Status:** In Progress | **Priority:** Major | **Fix Version:** 26.08  
**Customers:** Disney (IDPMV-427), Calgary Catholic SD (ICCSD-387) — Go-Live 27 July 2026

## Source summary

As a platform engineer on the CRM Core team, jobs with a configured **Job Expiry** date must be **unposted within ~1 hour** after expiry to meet compliance (customers reported jobs staying posted >1 day). The expiry field is optional; only portal visibility changes — no other job entity attributes are modified.

---

## CRM

**Impact:** High  
**Source:** PHEM-2190578 requirements 1, 3, 4, 5

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-CRM-001 | WHEN a recruiter creates a job via blank, copy-job, or template-based flows THE SYSTEM SHALL display an optional **Job Expiry** date field on the job creation form. | PHEM-2190578, req 1 |
| REQ-CRM-002 | WHEN a job is created from an HRM Req template flow THE SYSTEM SHALL display the same optional **Job Expiry** date field. | PHEM-2190578, req 1 |
| REQ-CRM-003 | WHEN a recruiter views or edits any existing job for the tenant THE SYSTEM SHALL show the **Job Expiry** field as optional (editable, not required). | PHEM-2190578, req 4 |
| REQ-CRM-004 | WHEN the **Job Expiry** field is empty THE SYSTEM SHALL persist the job without an expiry and SHALL NOT schedule automatic unpost for that job. | PHEM-2190578, req 3, 5 |
| REQ-CRM-005 | WHEN a recruiter sets **Job Expiry** THE SYSTEM SHALL persist the date on the job record; the UI SHALL NOT display a time component (date only). | PHEM-2190578, req 2 |
| REQ-CRM-006 | WHEN **Job Expiry** is saved THE SYSTEM SHALL store sufficient metadata to resolve expiry execution in the job-posting timezone (derived from job location / country / state). | PHEM-2190578, req 2 |

### Acceptance criteria

- [ ] Job Expiry appears on blank, copy, template, and HRM Req template creation flows.
- [ ] Job can be saved with Job Expiry blank; no validation error.
- [ ] Existing jobs show Job Expiry; field is editable and optional.
- [ ] Date picker shows date only (no timestamp in UI).
- [ ] Copy-job and template flows copy or default Job Expiry per existing copy-field rules (confirm with product if blank vs copied).

### Dependencies / open questions

- Confirm copy-job behavior: should expiry copy from source job or reset to blank?
- Confirm HRM Req template: field placement and whether template can pre-populate expiry.

---

## Integrations

**Impact:** High  
**Source:** PHEM-2190578 requirements 2, 7; AC 1

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-INT-001 | WHEN a job passes its **Job Expiry** instant (23:59:59 in the job-posting timezone on the configured date) THE SYSTEM SHALL unpost the job on all portals where it is visible. | PHEM-2190578, req 2, 7 |
| REQ-INT-002 | WHEN a job is unposted due to expiry THE SYSTEM SHALL remove portal visibility only; THE SYSTEM SHALL NOT alter other job entity attributes (status, hiring team, applications, etc.). | PHEM-2190578, req 7; AC 1 |
| REQ-INT-003 | WHEN a job is unposted due to expiry THE SYSTEM SHALL prevent new candidate applications on affected portals after unpost completes. | PHEM-2190578, req 7; AC 1 |
| REQ-INT-004 | IF unpost is delayed THE SYSTEM SHALL complete unpost within one hour of the expiry instant to satisfy compliance SLA. | PHEM-2190578, user story |

### Acceptance criteria

- [ ] After expiry + processing window, job no longer appears on career portal(s).
- [ ] CRM job record retains prior field values except publish/visibility state.
- [ ] Apply flow is unavailable for expired-unposted jobs on portal.
- [ ] Unpost completes within 1 hour of 23:59:59 on expiry date in posting timezone.

### Dependencies / open questions

- Which integration services own portal unpost API — confirm with Integrations pod.
- Multi-portal jobs: unpost all portals atomically or per-portal (define failure partial state).

---

## Analytics

**Impact:** Medium  
**Source:** Implied by compliance reporting and Phenom story standards (not explicit in ticket)

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-ANL-001 | WHEN **Job Expiry** is created or updated THE SYSTEM SHALL emit a CRM job-field change event including jobId, tenantId, expiryDate, and actor. | ASSUMPTION — observability |
| REQ-ANL-002 | WHEN a job is unposted due to expiry THE SYSTEM SHALL emit an event including jobId, tenantId, expiryDate, unpostTimestamp, triggerSource (`expiry_automation`), and portals affected. | ASSUMPTION — compliance audit |
| REQ-ANL-003 | WHEN expiry-driven unpost events are emitted THE SYSTEM SHALL land them in the tenant analytics store (e.g. Snowflake) for compliance and operations reporting. | ASSUMPTION — Phenom standard |

### Acceptance criteria

- [ ] Field-change and unpost events are queryable by jobId and tenantId.
- [ ] Unpost event timestamp allows SLA verification (expiry instant vs actual unpost).

### Dependencies / open questions

- Confirm event schema with Analytics pod; align with existing job publish/unpublish events.
- Ticket does not mandate recruiter notifications — no messaging analytics required.

---

## Messaging

**Impact:** None  
**Source:** No notification requirements in PHEM-2190578

### Requirements

No requirements — the story does not specify recruiter or candidate notifications on expiry or unpost.

### Recommendations (out of scope unless product confirms)

- Optional future REQ: notify Primary Recruiter when auto-unpost executes (not in current ticket).

---

## Screening

**Impact:** Medium  
**Source:** PHEM-2190578 req 7; AC 1

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-SCR-001 | WHEN a job has been unposted due to expiry THE SYSTEM SHALL block new application submissions for that job on candidate-facing channels. | PHEM-2190578, AC 1 |
| REQ-SCR-002 | WHILE a job is past expiry but not yet unposted THE SYSTEM SHALL define consistent apply eligibility (recommend: block apply at expiry instant, not at unpost completion). | ASSUMPTION — gap in ticket |

### Acceptance criteria

- [ ] Candidate cannot complete a new application on an expired-unposted job.
- [ ] In-flight applications started before expiry are unaffected (confirm with product).

### Dependencies / open questions

- **Gap:** Ticket does not state behavior for applications in progress at expiry.
- **Gap:** Deep-link / SEO cached job pages — confirm Screening + Integrations handling.

---

## Scheduling

**Impact:** High  
**Source:** PHEM-2190578 req 2, user story (<1 hour SLA)

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-SCH-001 | THE SYSTEM SHALL run a scheduled job (cron) at a configurable interval to process jobs whose **Job Expiry** has passed. | PHEM-2190578, req 2 |
| REQ-SCH-002 | THE SYSTEM SHALL support configurable cron intervals of at least **30 minutes** and **1 hour**. | PHEM-2190578, req 2 |
| REQ-SCH-003 | WHEN evaluating expiry THE SYSTEM SHALL treat the expiry instant as **23:59:59** on the configured date in the timezone derived from job posting location (country/state). | PHEM-2190578, req 2 |
| REQ-SCH-004 | WHEN the cron runs after the expiry instant THE SYSTEM SHALL enqueue or execute unpost within the compliance window (≤1 hour after expiry). | PHEM-2190578, user story |
| REQ-SCH-005 | IF a job has no **Job Expiry** value THE SCHEDULER SHALL exclude that job from expiry processing. | PHEM-2190578, req 5 |

### Acceptance criteria

- [ ] Cron interval is tenant- or environment-configurable (30 min / 1 hr).
- [ ] Job with expiry 2026-07-08 in posting TZ is eligible for unpost after 2026-07-08 23:59:59 local.
- [ ] Jobs without expiry are never picked up by expiry cron.
- [ ] Worst-case unpost latency ≤ 1 hour after expiry instant given configured interval.

### Dependencies / open questions

- **Gap:** Ticket mentions "timezone closest to UTC" in one revision and "job posting timezone" in another — **resolve to posting-location timezone** per latest description bullet 2.
- Confirm whether DST transitions affect 23:59:59 boundary.

---

## Automations

**Impact:** High  
**Source:** PHEM-2190578 req 6

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-AUT-001 | THE Automations flow SHALL scan all jobs for each customer across associated tenants to identify jobs past **Job Expiry** with the field populated. | PHEM-2190578, req 6 |
| REQ-AUT-002 | WHEN a scanned job is past expiry THE Automations flow SHALL trigger unpost (portal visibility removal) per Integrations requirements. | PHEM-2190578, req 6, 7 |
| REQ-AUT-003 | WHEN **Job Expiry** is not populated THE Automations flow SHALL skip the job (no unpost). | PHEM-2190578, req 5 |
| REQ-AUT-004 | THE Automations flow SHALL be idempotent for jobs already unposted (no duplicate side effects). | ASSUMPTION — operational safety |

### Acceptance criteria

- [ ] Tenant scan processes all jobs with expiry populated across associated tenants.
- [ ] Unpost action invoked only when expiry instant has passed and job is still posted.
- [ ] Re-running scan on already-unposted job is a no-op.
- [ ] Automations and Scheduling cron do not double-unpost or conflict (define single owner or coordination).

### Dependencies / open questions

- **Gap:** Relationship between **Scheduling cron** and **Automations flow** — ticket mentions both; clarify single execution path or layered design (Scheduling triggers Automations).
- Confirm per-customer enablement for Disney and Calgary Catholic SD before go-live.

---

## Cross-domain summary

| Area | Impact | REQ count |
|------|--------|-----------|
| CRM | High | 6 |
| Integrations | High | 4 |
| Analytics | Medium | 3 (assumptions) |
| Messaging | None | 0 |
| Screening | Medium | 2 |
| Scheduling | High | 5 |
| Automations | High | 4 |

## Gaps & risks

1. **Scheduling vs Automations overlap** — req 2 describes cron; req 6 describes Automations scan. Clarify architecture to avoid duplicate processing or missed jobs.
2. **Timezone wording conflict** — "timezone closest to UTC" vs "timezone where job is posted" in description; engineering should standardize on posting-location TZ.
3. **Apply eligibility during unpost lag** — up to 1 hour between expiry and unpost; define whether apply is blocked at expiry or at unpost.
4. **Copy-job / template expiry defaults** — not specified in ticket.
5. **Analytics not in ticket** — recommend explicit analytics AC in Jira before go-live for compliance audit (Disney, Calgary Catholic SD).

## Suggested child tickets

| Area | Suggested ticket |
|------|------------------|
| CRM | Job Expiry field — UI, persistence, and HRM Req template support |
| Scheduling | Configurable expiry cron (30 min / 1 hr) with posting-TZ evaluation |
| Automations | Tenant-wide expiry scan and unpost orchestration |
| Integrations | Portal unpost on expiry — visibility-only, multi-portal |
| Screening | Block new applications on expired / unposted jobs |
| Analytics | Expiry field change and auto-unpost event schema + Snowflake pipeline |

---

*Generated from PHEM-2190578 via `jira-domain-requirements` skill.*
