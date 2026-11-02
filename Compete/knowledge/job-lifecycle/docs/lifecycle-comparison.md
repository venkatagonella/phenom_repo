# Competitor Job Entity Lifecycle Comparison

## Executive summary

The six competitors use two broad patterns:

* Enterprise ATSs such as Workday and SAP SuccessFactors are requisition-first. Approval, requisition status, posting destination, and posting dates are distinct concerns.
* Modern ATSs such as Greenhouse and Ashby make the separation between job, opening, and posting especially visible. Workable and Personio combine job visibility and channel-distribution concepts differently.

Across all vendors, do not treat the following as synonyms:

* job/requisition status
* posting status
* published status
* channel distribution status
* expiry status
* closed/archived status

## Workday

### Simple sequence

`Draft requisition -> Approval -> Open/available -> Post -> Freeze/unpost or resume -> Fill/close -> Closed`

### Entity and state notes

* The requisition is the primary internal hiring record.
* A requisition can have separate internal and external postings.
* Posting start and end dates are explicit posting fields.
* A requisition can be frozen or unfrozen without being closed.
* Closing is stronger than unposting. A closed requisition is treated as terminal in this benchmark and should not be modeled as a simple pause.
* The posting may be removed or its end date changed while the requisition remains active.

### Lifecycle fields to benchmark

`requisition_status`, `posting_status`, `posting_start_date`, `posting_end_date`, `freeze_reason`, `closed_at`, `posting_destination`

## SAP SuccessFactors

### Simple sequence

`Pre-approved -> Approved -> Open -> Post requisition -> Unpost/expire -> Fill openings -> Closed or reopened`

### Entity and state notes

* The requisition progresses through workflow approval before posting eligibility.
* Internal and external posting records can have separate posting start and end dates.
* Posting is the platform's main candidate-visibility action; “publishing” is effectively represented by posting.
* A posting can be removed explicitly or can end through its posting end date.
* Changing posting dates may require removing the post and posting again.
* A closed requisition can return to a prior state when reopened, depending on configuration.

### Lifecycle fields to benchmark

`requisition_status`, `approval_status`, `posting_type`, `posting_start_date`, `posting_end_date`, `post_removed_at`, `closed_at`, `reopened_at`

## Greenhouse

### Simple sequence

`Create job -> Draft/approval -> Open -> Publish job post -> Edit/unpublish -> Close openings -> Close job/reopen`

### Entity and state notes

* Job, opening, and job post are separate concepts.
* The job remains Draft until approval and becomes Open after approval.
* A job may have multiple openings and multiple job posts.
* A job post has its own publish/unpublish behavior and candidate-facing content.
* Closing the job unpublishes its posts; unpublishing a post does not necessarily close the job.
* The benchmark treats opened, first-published, and closed timestamps as useful lifecycle signals.

### Lifecycle fields to benchmark

`job_status`, `opening_status`, `job_post_status`, `opened_at`, `first_published_at`, `closed_at`, `post_unpublished_at`, `application_deadline`

## Ashby

### Simple sequence

`Job draft -> Approval if configured -> Job open -> Publish posting -> Unpublish or deadline -> Fill openings -> Close job or return to draft`

### Entity and state notes

* Job, opening, and posting are separate entities.
* An Open job is required before a posting can be published.
* A posting can have its own deadline and can automatically unpublish after the deadline.
* Ashby distinguishes Listed, Unlisted, and Unpublished behavior.
* Listed means discoverable through normal listing surfaces.
* Unlisted hides the posting from normal listings but allows candidates with a direct link to apply.
* Unpublished makes the posting inaccessible for new applications.
* Closing the job removes its postings.

### Lifecycle fields to benchmark

`job_status`, `opening_status`, `posting_visibility`, `published_at`, `unpublished_at`, `application_deadline`, `opening_closed_at`, `job_closed_at`

## Workable

### Simple sequence

`Draft requisition/job -> Pending -> Approved -> Open requisition -> Publish -> Internal/on hold -> Reserved/filled or canceled -> Archived/unarchive`

### Entity and state notes

* Requisition statuses and job visibility statuses are separate but connected.
* Requisition statuses benchmarked: Draft, Pending, Approved, Open, Reserved, Filled, Canceled, and On hold.
* Job visibility statuses benchmarked: Draft, Published, Internal, Confidential, and Archived.
* Posting is mainly distribution to the careers page, free boards, premium boards, or external feeds.
* A job may enter an in-review state before becoming Published.
* There is no single universal job expiry equivalent to a posting deadline across all channels.
* Premium or featured placements may expire based on a purchased promotion period.
* Unpublishing removes candidate-facing visibility; archiving is stronger and limits further interaction.
* Unarchive can preserve the original publication date in the benchmarked behavior.

### Lifecycle fields to benchmark

`requisition_status`, `job_visibility_status`, `review_status`, `published_at`, `channel_status`, `promotion_end_at`, `on_hold_at`, `archived_at`, `unarchived_at`

## Personio

### Simple sequence

`Job draft -> Publish job -> Schedule posting -> Running -> Stopped/expired -> Opening filled -> Archive/reopen`

### Entity and state notes

* Job states benchmarked: Draft, Published, Promoted, and Archived.
* The Personio career-page job and external-board promotion are separate concerns.
* External postings can be Scheduled, Running, Canceled, or Expired.
* The posting start date controls when a channel placement becomes active.
* The posting end date controls when the channel placement becomes expired.
* Canceling/stopping a posting before its end date is different from natural expiry.
* Reopening an archived job returns it to Draft in the benchmarked behavior.
* Removing auto-postings from connected boards is an explicit unpublish-like action.

### Lifecycle fields to benchmark

`job_status`, `promotion_status`, `posting_start_date`, `posting_end_date`, `canceled_at`, `expired_at`, `opening_closed_at`, `archived_at`, `reopened_at`

## Cross-competitor comparison

| Dimension | Workday | SAP SuccessFactors | Greenhouse | Ashby | Workable | Personio |
|---|---|---|---|---|---|---|
| Primary internal entity | Requisition | Requisition | Job | Job | Requisition/job | Job |
| Separate posting object | Yes | Yes | Yes | Yes | Channel distribution model | External promotion/posting |
| Explicit posting dates | Yes | Yes | Partly/configuration-dependent | Deadline and publish timestamps | Channel-dependent | Yes for promotions |
| Separate publishing concept | Often represented by posting | Mostly represented by posting | Yes | Yes | Job visibility state | Career page publish plus promotion |
| Automatic expiry | Posting end date | Posting end date | Deadline or scheduled unpublish | Application deadline | Channel/promotion-dependent | Posting end date |
| Manual unposting | Yes | Remove Post | Unpublish | Unpublish | Unpublish | Cancel/remove promotion |
| Direct-link hidden mode | Not benchmarked | Not benchmarked | Not benchmarked | Unlisted | Not benchmarked | Not benchmarked |
| Reopen semantics | Closed treated as terminal | Can return to prior state | Reopen job | Return to draft/open behavior | Unarchive | Reopen as Draft |

## Product-management takeaway

The strongest common abstraction is a three-layer model:

`Job/Requisition -> Posting -> Channel distribution`

Each layer needs its own status and timestamps. Posting lifecycle must not implicitly close the underlying job unless a deliberate business rule says so.
