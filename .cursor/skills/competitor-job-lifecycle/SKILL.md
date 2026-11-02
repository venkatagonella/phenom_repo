---
name: competitor-job-lifecycle
description: Analyzes job creation, requisition, posting, publishing, expiry, unposting, closure, and reopening workflows across ATS competitors for Phenom. Use when comparing Phenom with Workday, SAP SuccessFactors, Greenhouse, Ashby, Workable, or Personio, or when discussing job/requisition/posting lifecycle.
---

# Competitor Job Lifecycle Research Skill

Use this skill whenever the task involves comparing Phenom's job creation or job posting workflow with Workday, SAP SuccessFactors, Greenhouse, Ashby, Workable, or Personio.

## Core model

Always distinguish:

* Job/requisition — internal hiring demand.
* Opening — headcount slot.
* Posting — candidate-facing listing.
* Channel distribution — destination-specific delivery.
* Publishing — visibility transition.
* Expiry — automatic/date-driven end.
* Unposting — explicit removal.
* Closing/archiving — stronger action on the underlying job.

Use the reference data file `knowledge/job-lifecycle/data/competitor-lifecycles.json` when available. Also read `knowledge/job-lifecycle/docs/` and `knowledge/job-lifecycle/diagrams/job-lifecycles.mmd` before answering.

## Workflow

1. Identify the vendor and the primary entity.
2. Separate job/requisition states from posting and channel states.
3. Map creation, approval, open, posting, publishing, unposting, expiry, fill, close, archive, and reopen transitions.
4. Preserve all independent dates and timestamps.
5. Explain whether posting end dates, application deadlines, or paid promotion periods trigger expiry.
6. Explain whether unposting is reversible and whether the job remains open.
7. State configuration-dependent behavior and confidence.
8. Produce a concise sequence and, when useful, a Mermaid `sequenceDiagram`.

## Output contract

Return:

* Primary entity model.
* One-line lifecycle sequence.
* Separate definitions of posting, publishing, expiry, and unposting.
* Statuses and lifecycle dates.
* Mermaid sequence diagram when requested.
* Comparison with Phenom's model: `Job/Requisition -> Posting -> Channel distribution`.
* Open verification questions.

## Guardrails

* Do not treat posting and publishing as synonyms without evidence.
* Do not treat expiry and manual unposting as the same event.
* Do not close a job merely because one posting is removed.
* Do not erase original publication history when a posting is republished.
* Do not claim vendor behavior is universal; call out configuration and edition differences.
* If source evidence is unavailable, mark the conclusion as a working benchmark and recommend verification.
