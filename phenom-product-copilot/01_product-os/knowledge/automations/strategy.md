# RX Automations — Strategy

Last enriched: 2026-11-02 (CUSP morning triage; inferred from open PHEM — not a published half plan). Treat as a working map until Syed/Tulasi confirm.

## Pod Vision

Automate repetitive recruiter work in CRM so status changes, messaging, screening invites, forwarding, and tagging happen without manual steps — via recipes today and a broader Automation Engine (policy/rules + workflow builder) over time.

North star (inferred, not sourced from a vision doc): _if a recruiter does the same Then every time a When happens, it should be a recipe — including cross-entity, role-based, and observable runs._

## In-flight / planned (PHEM)

| Item | Status | Source |
| --- | --- | --- |
| Unpost job on hired-count / expiry / terminal job status; Job Post action | Epic PHEM-2117038 In Progress. **Done 2026-11-01:** PHEM-2278048 (custom unpost automation — hourly schedule + hour-level relative date operators in Builder), PHEM-2278097 (Job Post action + Kafka events), PHEM-2278098 (API + Kafka contract). Still open: PHEM-2219929 system-automation unpost (Development), PHEM-2221509 settings page (PM Acceptance Queue). FixVersion "Backlog" — **release/GA version missing**. Likely match for CUSP-7209. | PHEM-2117038 (Disney/Calgary) |
| Configurable document scope for Forward Candidate to HM (All vs Application-Specific) | To Do | PHEM-2125738 (Allianz/Yale; CUSP-5184 cluster). **Do not close CUSP-5184** on PHEM-2267042 / PHEM-2300936 Done — those are HRM “share/forward without task”, not document-scope. |
| Multi-job hiring conditions — Any vs All | Epic Grooming | PHEM-1939903 `[26.05]` |
| Disposition reasons — admin UI, capture, visibility, analytics | To Do, `deferred` | PHEM-2263200 `(26.10)` |
| DHL application deletion automation (GDPR/retention) | Epic Ready | PHEM-1991257 |
| AE Policy & Rule Engine + Workflow Builder UI | Active AE shape | RX Onboarding Guide §2.4 — **no dated initiative list in Confluence** |

## Feedback themes to keep as one item each

See [feedback-themes.md](feedback-themes.md). Do not open a second CUSP for an existing keeper.

## Success metrics

**Missing.** No targets in this repo. Do not invent.

## Context gaps

* No PM-authored strategy.md equivalent (this file is a triage-derived stub).
* No published current-half priorities or success metrics.
* Unify Automation Products POV (FIRE-5244) is Done as a story — outcome not copied here.
