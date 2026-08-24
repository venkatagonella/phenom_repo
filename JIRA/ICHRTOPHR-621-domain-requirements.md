# ICHRTOPHR-621 — Requirements Story (by system)

**Jira:** [ICHRTOPHR-621](https://phenompeople.atlassian.net/browse/ICHRTOPHR-621)  
**Epic:** ICHRTOPHR-517 (Horizon 2 CVS)  
**Summary:** Unpost Workday job when Phenom applicant reaches Offer stage  
**Status:** Story Elaboration  
**Product area:** Recruiter Experience (RX) — CRM Core  
**Customer go-live (from Slack):** 29 Sept 2026 · Target planning: 26.09 / 26-17 sprint  
**Miro (Angad):** https://miro.com/app/board/uXjVH42NCZo=/  
**Diagram attachment:** `image-20260730-021216.png`

---

## User story

As a CVS recruiter hiring through Phenom (Horizon 2),  
when a finalist reaches the Offer path on a Phenom job that was also created in Workday,  
I need Phenom to unpost that job on the career site and unpost/close the linked Workday job,  
so candidates stop applying and both systems stay aligned without creating a new Workday job.

---

## Flow from the attached diagram

The attachment is a segment of the CVS hire / offer flowchart. Relevant path:

```text
… → Hire reason & date
      → Phenom Sends Offer Documents to Candidate
        (+ Put Custom Object Call for WOTC)
      → Docs sent
      → Finalist Accepts Offer?
            ├─ NO  → Offer Declined (end)
            └─ YES → Unpost Job
                      → Unposted
                      → Candidate Uploads Required Documents
                      → Docs uploaded
                      → Candidate Completes Background Check
                      → Check submitted
                      → Background Check Result? …
```

**What this means for ICHRTOPHR-621**

| Diagram step | Meaning for this story |
|---|---|
| Offer documents sent / Offer path | Candidate is on the Offer journey in Phenom |
| **Finalist Accepts Offer? = YES** | Diagram places **Unpost Job** only after acceptance |
| **Unpost Job → Unposted** | Job must leave active posted state (career site + linked ATS/Workday job) |
| Later steps (docs, BGC) | **Out of scope** for this story |

**Trigger ambiguity (must resolve)**

| Source | Trigger |
|---|---|
| Ticket AC1 | Candidate **reaches Offer stage** |
| Diagram | **After finalist accepts offer** |
| Angad (Slack/Jira) | Applicant **selected for / reaches offer**; CRM listens to hiring status |

**ASSUMPTION until PM confirms:** treat trigger as **candidate hiring status moves to Offer (or Offer Accepted)** on a Phenom job that has a stored Workday job ID. Confirm whether unpost is on **Offer stage entry** or **Offer accepted**.

---

## End-to-end intended architecture (ticket + Angad)

```text
Candidate hiring status → Offer (or Offer Accepted)
        │
        ▼
   CRM detects status change
        │
        ├─ Unpost Phenom job / career-site visibility (must not be blocked by Workday failure)
        │
        ▼
   Automations orchestrates unpost sync
        │
        ▼
   IX / Job Sync calls Workday with stored Workday job ID
        │
        ├─ success → status: Unposted in Workday (+ timestamps)
        └─ failure → retry up to 3× → Unpost Failed / Retry Pending
                     (recruiter visibility in CRM; notify TBD — see gaps)
        │
        ▼
   Workday may send Job closure notification
        │
        ▼
   Phenom acknowledges and updates sync records
```

CRM is the owning product area. Angad’s split: **(1) Automations orchestrates**, **(2) IX executes Workday call**.

---

## What each system must do

### 1. CRM (owner) — Impact: High

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-CRM-001 | WHEN a candidate’s hiring status on a Phenom job moves to the agreed Offer trigger (Offer stage / Offer Accepted — TBD) THE SYSTEM SHALL initiate the job unpost path for that Phenom job. | AC1, diagram, Angad Slack |
| REQ-CRM-002 | WHEN unpost is initiated THE SYSTEM SHALL use the Workday job ID already stored on the Phenom job and SHALL NOT create a new Workday job. | AC1 |
| REQ-CRM-003 | WHEN Workday unpost sync state changes THE SYSTEM SHALL persist and show on the job in CRM one of: `Unpost In Progress`, `Unposted in Workday`, `Unpost Failed`, `Retry Pending`, with timestamp and failure details. | AC2 |
| REQ-CRM-004 | IF Workday unpost fails THE SYSTEM SHALL still allow the Phenom job to be unposted (Workday failure must not block Phenom unpost). | AC3 |
| REQ-CRM-005 | WHEN sync status is `Unpost Failed` or `Retry Pending` after automatic retries THE SYSTEM SHALL allow an authorized user to manually retry (permissions TBD). | Dependencies |

**Acceptance criteria**

- [ ] Offer-path candidate on a linked Phenom↔Workday job triggers unpost only when Workday job ID is present.
- [ ] CRM job UI shows required sync statuses + timestamp + last error.
- [ ] Phenom job unpost succeeds even if Workday call fails.

**Dependencies / open questions**

- Confirm CRM field placement for sync status.
- Confirm exact hiring-status value(s) that fire the trigger.
- Confirm manual retry roles/permissions.

---

### 2. Automations — Impact: High

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-AUTO-001 | WHEN the agreed Offer hiring-status condition is met on a job with a stored Workday job ID THE SYSTEM SHALL orchestrate the Workday unpost sync workflow. | Angad Jira comment |
| REQ-AUTO-002 | IF the Workday unpost call fails and retries remain THE SYSTEM SHALL set status to `Retry Pending` and re-invoke IX up to 3 automatic attempts. | AC3 |
| REQ-AUTO-003 | WHEN automatic retries are exhausted THE SYSTEM SHALL set status to `Unpost Failed` (or leave `Retry Pending` per final design) without rolling back Phenom unpost. | AC3 |

**Acceptance criteria**

- [ ] Automation recipe/rule exists for Offer-trigger → Workday unpost orchestration.
- [ ] Exactly 3 automatic retries; then terminal failed/retry-pending state.
- [ ] Sync status field usable as automation condition/trigger for follow-on rules (recommended; explicit in sibling ICHRTOPHR-798).

**Dependencies**

- CRM emits reliable hiring-status / job events Automations can consume.
- IX exposes a callable unpost/close Workday job action.

---

### 3. Integrations (IX / FSI Job Sync / Workday) — Impact: High

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-INT-001 | WHEN invoked for Workday unpost THE SYSTEM SHALL call the confirmed Workday API to unpost/close the existing job identified by the stored Workday job ID. | AC1, Dependencies |
| REQ-INT-002 | WHEN the Workday call succeeds THE SYSTEM SHALL return success so CRM can set `Unposted in Workday`. | AC2 |
| REQ-INT-003 | WHEN the Workday call fails THE SYSTEM SHALL return error details suitable for CRM persistence and retry. | AC2, AC3 |
| REQ-INT-004 | WHEN Workday sends a Job closure notification THE SYSTEM SHALL acknowledge it and update Phenom sync records accordingly. | AC4 |
| REQ-INT-005 | WHEN unposting THE SYSTEM SHALL also ensure career-site / portal posted visibility is removed for the Phenom job (unpost on career site + ATS). | Angad Slack |

**Acceptance criteria**

- [ ] Existing Workday job is unposted/closed; no duplicate job created.
- [ ] Closure notification is acknowledged and reflected in sync status.
- [ ] Career site no longer shows the job as actively posted after Phenom unpost.

**Dependencies / risks**

- Confirm Workday API method (unpost vs close vs status update).
- Confirm inbound Job closure notification format/ack contract.
- Linked [ICHRTOPHR-798](https://phenompeople.atlassian.net/browse/ICHRTOPHR-798) (close Workday when Phenom job closed) has an FSI comment of “no feasibility” — treat as related but **different trigger**; do not assume 798 delivers 621.

**Out of scope (Integrations)**

- Creating/editing Workday jobs  
- Candidate sync beyond this trigger  
- Inbound Workday updates except closure acknowledgment  

---

### 4. Workday (customer ATS) — Impact: High (external)

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-WD-001 | WHEN Phenom sends unpost/close for a known job ID THE SYSTEM SHALL unpost/close that existing job (customer/Workday config dependency). | AC1 |
| REQ-WD-002 | WHEN the job is closed/unposted THE SYSTEM SHALL emit the Job closure notification Phenom will acknowledge. | AC4 |

Customer/config confirmation required; not a Phenom code deliverable alone.

---

### 5. Messaging — Impact: Contested

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-MSG-001 | IF automatic retries are exhausted THE SYSTEM SHALL notify the assigned recruiter on the job. | AC3 |

**Conflict:** ticket **Out of Scope** lists “Failure notification workflows.”  
**Decision needed:** keep AC3 notify as in-scope Messaging work, or drop notify and rely on CRM status + manual retry only.

---

### 6. Analytics — Impact: Low (recommended)

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-ANA-001 | WHEN unpost sync status, timestamps, failure details, or Workday job reference change THE SYSTEM SHALL make them available for reporting. | Sibling 798 AC12; recommended for 621 |

No hard analytics AC on 621 today — recommend emitting events for ops/SLA.

---

### 7. Screening — Impact: None (indirect)

No requirements — apply eligibility changes only as a side effect of job unpost/portal visibility (owned by Integrations/CRM unpost), not a new screening feature.

---

### 8. Scheduling — Impact: Low–Medium

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-SCH-001 | WHEN a Workday unpost retry is scheduled THE SYSTEM SHALL execute retries according to the agreed backoff/interval until 3 attempts are exhausted. | AC3 |

Retry clock/interval TBD with Automations/IX.

---

## Cross-domain summary

| Area | Impact | REQ count |
|------|--------|-----------|
| CRM | High | 5 |
| Automations | High | 3 |
| Integrations | High | 5 |
| Workday (external) | High | 2 |
| Messaging | Contested | 1 |
| Analytics | Low (rec.) | 1 |
| Scheduling | Low–Med | 1 |
| Screening | None | 0 |

---

## Gaps & risks

1. **Trigger mismatch:** Offer stage (ticket) vs Offer Accepted (diagram) vs “selected for offer” (Slack).
2. **Notify vs out-of-scope:** AC3 recruiter notify vs “Failure notification workflows” out of scope.
3. **Workday API + closure notification contract** still listed as dependencies on the ticket.
4. **FSI feasibility** for related close-on-Phenom-close (798) — clarify whether Offer-stage unpost uses a different/supported API path.
5. **Workday job ID prerequisite** — must already be stored from Intake Agent / Put Job integration before this story can fire.
6. Cross-team session still needed (CRM + IX PM + Automations PM) — noted in Slack 31 Jul.

---

## Suggested child tickets

1. **[CRM]** Offer-status trigger, Phenom job unpost, sync status fields, manual retry UI  
2. **[Automations]** Orchestration recipe: Offer trigger → IX Workday unpost + 3 retries  
3. **[IX / Job Sync]** Workday unpost/close API + closure notification acknowledgment  
4. **[Messaging — optional]** Recruiter notify after exhausted retries (only if AC3 wins over OOS)  

---

## Explicit out of scope (from ticket)

- Creating or editing Workday jobs  
- Candidate sync beyond Offer-stage unpost trigger  
- Inbound Workday updates except Job closure acknowledgment  
- Failure notification workflows *(conflicts with AC3 — resolve)*  
- Diagram steps after Unpost (document upload, background check)  
