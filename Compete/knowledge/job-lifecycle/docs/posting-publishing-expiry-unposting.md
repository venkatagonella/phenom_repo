# Posting, Publishing, Expiry, and Unposting

## Definitions

### Posting

A posting is the candidate-facing listing or channel-specific placement created from a job/requisition. A single job can have multiple postings for internal, external, regional, branded, or third-party destinations.

### Publishing

Publishing is the visibility transition that makes a job or posting available to candidates. Publishing may be a separate action from creating the posting. Some platforms use “post” as the name of the publish action, so the UI label is not enough to infer the data model.

### Expiry

Expiry is an automatic or date-driven end condition. It is normally triggered by a posting end date, application deadline, paid placement period, or channel rule. Expiry should record why and when the listing stopped being available.

### Unposting or unpublishing

Unposting is an explicit removal action. It can happen before the planned end date, at the user's request, because of a policy decision, or because the underlying job is closed. It should be distinguishable from natural expiry.

### Closing and archiving

Closing or archiving applies to the underlying job/requisition. It is stronger than removing one posting. A closed or archived job may prevent new applications, new postings, or further edits, depending on the platform.

## Differences by competitor

### Workday

* Posting is a requisition-level child, often split by internal and external destination.
* Publishing is normally represented by posting the eligible requisition.
* Expiry is driven by the posting end date.
* Unposting can remove an individual posting while the requisition remains active.

### SAP SuccessFactors

* Posting is a posting-type record with start and end dates.
* Publishing is effectively the Post Job action.
* Expiry occurs when the posting end date is reached.
* Remove Post is the explicit unposting action; date changes may require remove and repost.

### Greenhouse

* Posting is a job post separate from the job and openings.
* Publishing activates the job post on a selected channel.
* Expiry is commonly represented by scheduled unpublish or an application deadline.
* Unpublishing stops candidate-facing availability while preserving the job and recruiting data.

### Ashby

* Posting is a distinct listing attached to an Open job.
* Publishing makes the posting live; visibility can be Listed or Unlisted.
* Expiry can be driven by the application deadline and can automatically unpublish the posting.
* Unpublished is not the same as Unlisted: Unlisted can still accept applications through a direct link, while Unpublished prevents new applications.

### Workable

* Posting is primarily channel distribution from the job to career pages, boards, or feeds.
* Publishing changes candidate-facing job visibility and may include an in-review step.
* Expiry is not one universal job state; it can depend on the channel or promotion period.
* Unpublishing removes public visibility; archiving is the stronger administrative state.

### Personio

* Posting is external promotion of a published job through selected boards.
* Publishing makes the job visible on the career page; promotion distributes it to external channels.
* Expiry occurs when an external posting's end date is reached.
* Cancellation or removal before that date is an explicit stop action and should not be labeled natural expiry.

## Recommended event vocabulary for Phenom

Use explicit event names instead of overloading one status field:

* `job_created`
* `job_submitted_for_approval`
* `job_approved`
* `job_opened`
* `posting_created`
* `posting_scheduled`
* `posting_published`
* `posting_unpublished`
* `posting_expired`
* `posting_canceled`
* `opening_filled`
* `job_on_hold`
* `job_closed`
* `job_archived`
* `job_reopened`

## Required distinction

For every lifecycle report, answer these separately:

1. Is the underlying job/requisition open?
2. Does a posting record exist?
3. Is the posting published or merely created?
4. Is it listed, unlisted, or unpublished?
5. Has it expired by date, or was it manually unpublished?
6. Is the job itself filled, closed, canceled, or archived?
