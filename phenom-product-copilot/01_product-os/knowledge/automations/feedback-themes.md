# RX Automations — CUSP feedback themes

Last enriched: 2026-11-02. Triage only — do not comment/close CUSP unless Sebastian asks.

Filter: `project = CUSP AND issuetype = "Product Feedback" AND "Product Experience : Product" = "CRM - Automation" AND statusCategory != Done`

## Keepers (close the rest as Duplicate of the keeper)

| Theme | Keep | Close as duplicate |
| --- | --- | --- |
| Remove Tag as a Then action | CUSP-6399 | CUSP-7222, CUSP-6599, CUSP-6674 |
| OR in conditions | CUSP-5684 | CUSP-6771 |
| AI Discovery / lists / projects fire "assigned to job" | CUSP-5861 | CUSP-5857, CUSP-6023 |
| Notify when an automation fails | CUSP-6926 | CUSP-6556, CUSP-6121 |
| Email HM / recruiter / interviewer by **role** | CUSP-5393 | CUSP-7488, CUSP-7227, CUSP-4912, CUSP-392, CUSP-336, CUSP-4642, CUSP-4697, CUSP-1130, CUSP-7053, CUSP-7191, CUSP-4713 |
| Forward to HM = this application's docs only | CUSP-5184 | CUSP-5231, CUSP-4621, CUSP-4952 |
| Request screening eval as a hiring-status action | CUSP-7383 | CUSP-7289, CUSP-6517 |
| Per-recipe analytics | CUSP-7360 | CUSP-6689, CUSP-6463, CUSP-4913 |
| FitScore in recipes | CUSP-5295 | CUSP-5984 |
| Trigger from an evaluation-form response | CUSP-4673 | CUSP-936 |
| Send only in business hours | CUSP-6381 | CUSP-7026 |
| Run / sync recipe against pre-existing list members on activate | CUSP-7450 | |
| Assign Candidate to Event (Then action) | CUSP-7543 | |
| Export Automation Audit Log | CUSP-7565 | |

CUSP-7289 is the same Healius action as CUSP-7383 plus "only after recruiter eval" — if closed, that gate belongs on 7383.

## Related, not duplicates (leave open)

CUSP-7060 auto-retry · CUSP-6957 audit search by email (related to CUSP-7565 export, not a dupe) · CUSP-5992 which recipe fired · CUSP-6734 business days · CUSP-7334 / CUSP-5804 cross-entity / projects


## Newer tickets — keep open / note duplicates

* **CUSP-7696** (created 2026-10-21, Ayyappan Chaganti) — "Automated Synchronization between Project Stage and Candidate Hiring Status". **Duplicate of CUSP-4606** (project status from hiring status, Prioritise to Backlog); overlaps CUSP-7616 (action to update project stage/status); closed CUSP-5686 was Potential Future Enhancement. 2026-10-29: assigned to Syed Naqvi; Benjamin Badilla added Cisco context (FYI Andrew Foley) — when a candidate is Hired on any job, CRM project stage should move to Hired so nurture stops; gap is job-level trigger with no project-level action; says other customers ask too (not named). Asks: workaround today, feedback route, roadmap. **Missing context:** no published roadmap item or PHEM found for a project-stage action, and no documented workaround in local docs. Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7565** (created 2026-09-24 evening IST / after 2026-09-24 morning triage) — "Automation Audit Log Export" (Baylor Scott & White; reviewed with Automations Product Team / Syed). Want export of automation audit log for analytics review + troubleshooting. **New theme / keep open.** Related to CUSP-6957 (audit *search* by email) and adjacent to CUSP-7360 (per-recipe analytics) but not duplicates — export ≠ search ≠ recipe analytics. No matching open CRM-recipe PHEM for audit-log export found (title/text hits are MSG/OnboardX/Gig/skills/AWS noise). 2026-10-29: assigned to Syed Naqvi (by Eric Archuleta). Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7543** (created 2026-09-23) — "Automated Assignment of Candidates to Events". Want When: Assigned to Job → Then: Assign Candidate to Event (hiring-event job apps currently need manual event assignment). **New theme / keep open.** No other open CRM-Automation CUSP with matching text. No matching open PHEM for a CRM recipe "Assign to Event" action found by title/text search (Events PHEM hits are HRM/Events staff notifications, not this Then action). Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7488** (created 2026-09-16) — "More Email to options in Automations" (Email Recruiter / Hiring Manager). **Obvious duplicate of keeper CUSP-5393** (role-based email); do not open a new theme. Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7450** — recipes only fire for candidates added to a list *after* the automation exists; want bulk-apply / sync for members already on the list. No obvious dupe in open CRM-Automation CUSP; no matching open PHEM found by title search.
* **CUSP-7454** — "EC Trigger" CTA stays enabled after success; unclear UX (once-only). **Missing context:** no local/Confluence definition of "EC Trigger" in automations docs — may be Event Capture / a specific recipe trigger surface; do not close or retag without Syed confirmation.

## Shipped-but-still-open (verify, don't auto-close)

* CUSP-4981 WhatsApp — PHEM-1348379 Done vs PHEM-605974 PM Acceptance Queue
* Role-based email cluster — static/field email shipped (PHEM-2114070); role-based did not
* CUSP-7040 decline-reason triggers — may overlap PHEM-2219937 / PHEM-2267013; confirm before closing

* **CUSP-7209** (Jeremy Hamilton, To Do, unassigned) — automatic posting + unposting of job reqs (promised unpost 06-22, post in Aug; unpost not working in staging; CS0315621). **Likely shipped match (2026-11-02):** PHEM-2278048 (custom automation to unpost on expiry: hourly schedule + hour-level relative date operators in the Builder) and PHEM-2278097 (Job Post action + Kafka events) both moved **Done 2026-11-01**; PHEM-2278098 API/Kafka contract Done. Still open: system-automation unpost PHEM-2219929 (Development), settings page PHEM-2221509 (PM Acceptance Queue), epic PHEM-2117038 In Progress, stories carry fixVersion "Backlog". **Missing:** release/GA version and staging/prod availability for this tenant — confirm with the AE/automations team before telling the customer or closing.

## Gaps in this file (2026-10-30)

* After the Product OS move to `01_product-os/` (commit 4d2be85, 2026-10-21) this file lacks entries filed by earlier triage runs for CUSP-7616, CUSP-7625, CUSP-7685 ("Weekday only Automation", likely near CUSP-6734 business days) and CUSP-5684 (OR operator, Capgemini). Backfill from Jira on a quieter run.
* CUSP-4662 (DHL career-site job advert URL back to recruiters, Prioritise to Backlog): DHL asked for status for their monthly enhancement review (Patrik Magitteri, 2026-10-19); Syed replied 2026-10-29 he will review with the team. No roadmap date known.

## Delta 2026-11-02

* **CUSP-5147** (HM app attachment overload, fast-track; Allianz/BSW cluster) moved **Done 2026-10-30** by Akanksha Janna: job-specific attachments for Hiring Managers delivered in **26.08**, self-service config, KB0014809. Open bucket count 127 → 126.
* **CUSP-5231** (Yale; forward to HM sends all resumes) stays open (Prioritise to Backlog, Syed). On 2026-10-30 Akanksha **removed** its "resolved by PHEM-873435" link (HRM resume mapping epic, now Done) — so the HRM/attachment work is *not* treated as resolving it; the remaining tracker is PHEM-2125738 (configurable document scope for Forward Candidate, CRM Automations). Keeper for the theme is still CUSP-5184.
* Jira currently returns Syed Naqvi's account as `active: false` on CUSP assignee fields. **Missing context:** whether Syed has left / changed role and who now owns CRM Automations CUSP — confirm before routing.
