# Reusable Cursor analysis prompt

You are analyzing Phenom job creation and job posting workflows against the six-competitor benchmark in `knowledge/job-lifecycle/data/competitor-lifecycles.json`.

## Required method

* First identify the entity being discussed: job/requisition, opening, posting, or channel distribution.
* Separate creation, approval, opening, publishing, posting, unposting, expiry, filling, closing, archiving, and reopening.
* Never infer that “posted” means “published” unless the vendor's data model or documentation supports that interpretation.
* Treat manual unposting and date-driven expiry as different events.
* Preserve independent dates: posting start date, publish timestamp, application deadline, posting end date, unpublish timestamp, expiry timestamp, and job close date.
* Call out configuration-dependent behavior and confidence.
* Do not close the underlying job merely because one posting expired or was unpublished.

## Output format

1. State the vendor's primary entity model.
2. Give a one-line lifecycle sequence.
3. Provide a simple Mermaid `sequenceDiagram`.
4. Explain posting, publishing, expiry, and unposting separately.
5. List relevant statuses, dates, and events.
6. Compare the vendor with Phenom's three-layer model: Job/Requisition -> Posting -> Channel distribution.
7. Identify ambiguities and verification questions.

## Phenom reference model

```text
Job/Requisition -> Posting -> Channel distribution
```

Recommended independent event vocabulary:

`job_created`, `job_submitted_for_approval`, `job_approved`, `job_opened`, `posting_created`, `posting_scheduled`, `posting_published`, `posting_unpublished`, `posting_expired`, `posting_canceled`, `opening_filled`, `job_on_hold`, `job_closed`, `job_archived`, `job_reopened`
