# RX Automations — CUSP feedback themes

Last enriched: 2026-09-25. Triage only — do not comment/close CUSP unless Sebastian asks.

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

* **CUSP-7565** (created 2026-09-24 evening IST / after 2026-09-24 morning triage) — "Automation Audit Log Export" (Baylor Scott & White; reviewed with Automations Product Team / Syed). Want export of automation audit log for analytics review + troubleshooting. **New theme / keep open.** Related to CUSP-6957 (audit *search* by email) and adjacent to CUSP-7360 (per-recipe analytics) but not duplicates — export ≠ search ≠ recipe analytics. No matching open CRM-recipe PHEM for audit-log export found (title/text hits are MSG/OnboardX/Gig/skills/AWS noise). Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7543** (created 2026-09-23) — "Automated Assignment of Candidates to Events". Want When: Assigned to Job → Then: Assign Candidate to Event (hiring-event job apps currently need manual event assignment). **New theme / keep open.** No other open CRM-Automation CUSP with matching text. No matching open PHEM for a CRM recipe "Assign to Event" action found by title/text search (Events PHEM hits are HRM/Events staff notifications, not this Then action). Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7488** (created 2026-09-16) — "More Email to options in Automations" (Email Recruiter / Hiring Manager). **Obvious duplicate of keeper CUSP-5393** (role-based email); do not open a new theme. Triage-only — do not close/comment unless Sebastian asks.
* **CUSP-7450** — recipes only fire for candidates added to a list *after* the automation exists; want bulk-apply / sync for members already on the list. No obvious dupe in open CRM-Automation CUSP; no matching open PHEM found by title search.
* **CUSP-7454** — "EC Trigger" CTA stays enabled after success; unclear UX (once-only). **Missing context:** no local/Confluence definition of "EC Trigger" in automations docs — may be Event Capture / a specific recipe trigger surface; do not close or retag without Syed confirmation.

## Shipped-but-still-open (verify, don't auto-close)

* CUSP-4981 WhatsApp — PHEM-1348379 Done vs PHEM-605974 PM Acceptance Queue
* Role-based email cluster — static/field email shipped (PHEM-2114070); role-based did not
* CUSP-7040 decline-reason triggers — may overlap PHEM-2219937 / PHEM-2267013; confirm before closing
