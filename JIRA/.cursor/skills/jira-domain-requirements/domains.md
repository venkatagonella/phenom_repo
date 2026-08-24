# Phenom Platform Domain Areas

Reference for mapping Jira stories to the correct product area. When in doubt, assign to the area that **owns the code path** that must change.

## CRM

**Scope:** Recruiter-facing CRM — job and candidate records, job creation/edit flows (blank, copy, template), job details, hiring team, internal job status, CRM-native fields and validation.

**Signals in tickets:** "job creation page", "job entity", "recruiter", "HRM Req template", "existing jobs", "field visible", "non-mandatory field".

**Out of scope:** External portal rendering (Integrations), notification delivery (Messaging), workflow engine scans (Automations).

## Integrations

**Scope:** ATS/HRM job pull and push, portal publish/unpublish to career sites, Workday/SuccessFactors/legacy connectors, multi-portal visibility, sync between CRM and external systems.

**Signals:** "portal", "unpost", "unpublish", "visibility", "posted to", "ATS", "job pull", "HRM".

**Out of scope:** CRM UI field placement (CRM), cron timing (Scheduling).

## Analytics

**Scope:** Snowflake (or tenant data warehouse) event emission, Beacon/user-activity tracking, audit logs, reporting dimensions, historical retention for compliance reporting.

**Signals:** "report", "Snowflake", "metrics", "track", "audit", "data storage", "Beacon".

**Default:** If the ticket omits analytics, note what **should** be emitted for observability (unpost events, expiry field changes) as recommendations, not hard requirements.

## Messaging

**Scope:** Email, SMS, in-app, and push notifications; templates; recruiter/candidate notification triggers.

**Signals:** "notify", "email", "alert", "reminder", "message template".

**When absent:** State "No requirements" — do not invent notification flows unless compliance or UX clearly needs them.

## Screening

**Scope:** Candidate application eligibility, apply-button behavior, application submission gates, post-apply flows affected by job state.

**Signals:** "candidate cannot apply", "application", "apply after", "screening", "eligibility".

**Related to this epic:** Expired/unposted jobs must block new applications on portals.

## Scheduling

**Scope:** Cron jobs, scheduled tasks, interval configuration, timezone-aware execution windows, job-queue timing.

**Signals:** "cron", "scheduled interval", "hourly", "30 minutes", "23:59:59", "timezone", "expiry date execution".

**Out of scope:** Business-rule definition of *what* to do (Automations) vs *when* to run (Scheduling).

## Automations

**Scope:** Phenom Automations / workflow engine — tenant-wide scans, rule evaluation, bulk actions across jobs per customer, automation recipes.

**Signals:** "Automations flow", "scan through all jobs", "per customer", "associated tenants", "workflow".

**Distinction from Scheduling:** Scheduling owns the clock; Automations owns the scan-and-act business logic across tenants.
