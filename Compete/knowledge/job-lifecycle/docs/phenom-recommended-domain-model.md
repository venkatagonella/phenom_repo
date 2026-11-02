# Phenom Recommended Job Lifecycle Domain Model

## Purpose

Use this as a benchmark model for job creation and posting workflows. It is intentionally vendor-neutral and preserves the differences observed across Workday, SAP SuccessFactors, Greenhouse, Ashby, Workable, and Personio.

## Entity hierarchy

```text
Job/Requisition
  ├── Opening 1..n
  ├── Posting 0..n
  │     └── Channel distribution 0..n
  └── Approval workflow 0..1
```

## Independent state machines

### Job/requisition state

`Draft -> Pending approval -> Approved -> Open -> On hold -> Filled/Cancelled -> Closed/Archived`

Possible transition: `Closed/Archived -> Reopened -> Draft or Open`, subject to business rules.

### Posting state

`Created -> Scheduled -> Published -> Unpublished/Paused -> Republished -> Expired/Canceled`

A posting can also transition directly from `Published -> Expired` when a date or deadline is reached.

### Channel distribution state

`Not distributed -> Queued/In review -> Live -> Removed/Failed/Expired`

Each channel can have its own status and timestamps. One channel may be live while another is removed or failed.

## Dates and timestamps

At minimum, model these separately:

* `created_at`
* `approved_at`
* `opened_at`
* `posting_start_date`
* `published_at`
* `application_deadline`
* `posting_end_date`
* `unpublished_at`
* `expired_at`
* `canceled_at`
* `opening_filled_at`
* `closed_at`
* `archived_at`
* `reopened_at`

Do not use `published_at` as a substitute for `posting_start_date`. A job can be configured today to start posting in the future.

## Recommended invariants

* A posting cannot be published unless its parent job is eligible for posting.
* A posting may be unpublished while its parent job remains open.
* Expiry is not the same event as manual unposting.
* A channel distribution can fail without changing the parent posting's business status.
* Closing a job may unpublish all active postings, but unpublishing one posting must not close the job.
* A posting end date should not silently rewrite the job close date.
* A direct-link or unlisted mode, if supported, must be distinct from unpublished.
* Reposting should preserve historical events and should not overwrite the original publication history.
* Reopening rules must be explicit: either restore the prior job state or return the job to Draft.
* Every status-changing action should capture actor, timestamp, reason, and source channel where relevant.

## Suggested status and reason fields

```json
{
  "job_status": "OPEN",
  "posting_status": "PUBLISHED",
  "posting_visibility": "LISTED",
  "channel_status": "LIVE",
  "posting_start_date": "2026-09-01",
  "posting_end_date": "2026-10-01",
  "application_deadline": null,
  "unpublish_reason": null,
  "expiry_reason": null,
  "close_reason": null
}
```

## Comparison questions for product discovery

* Is the user creating a job, a requisition, an opening, a posting, or a channel distribution?
* Can one job have multiple openings?
* Can one job have multiple postings with independent dates?
* Does publishing happen before or after approval?
* Can the user edit a posting after publishing?
* Is expiry automatic, manual, channel-specific, or deadline-driven?
* Does unposting preserve the posting record and history?
* Can a candidate with a direct link still apply after the listing is hidden?
* Does closing the job automatically unpublish every posting?
* Can a closed job be reopened, and to which state?
