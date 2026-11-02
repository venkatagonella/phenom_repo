# RX theme playbook — what each theme is & how to reduce SR volume

**Population:** Recruiter Experience (RX), `JIRA_CREATED` ∈ {Yes, No}, n = **4,379** (sheet CSV).  
**Classifier:** high-confidence phrase rules (`rx_theme_rules.py` base + cluster_v1).  
**%** = share of that RX population.

**How to read “To reduce feedback %”:** plain-language Phenom product fixes grounded in ticket SHORT_DESCRIPTION + DESCRIPTION. Unclassified is removed — every playbook theme is a named product area. Gaps in phenom-knowledge are called out in the knowledge row. These are demand signals, not an approved roadmap.

**Phenom Knowledge packs used:** `phenom-knowledge/messaging/`, `automations/`, `screening/` (+ `INDEX.md`, Engineering `capability-map.md` for routing only).

---

## Candidate profile data / fields / tags / location / GDPR — 463 (10.6%)

| | |
|--|--|
| **What customers report** | Wrong/missing profile fields, tags, location/address/phone, purge/GDPR/privacy, field add/rename/update failures. |
| **What the theme means in product terms** | Integrity and configurability of the **candidate record** in CRM (profile schema, tags, privacy/deletion). |
| **Phenom knowledge** | No dedicated “CRM Profile” area pack is built yet. Closest: Messaging **notes** (`crm-notes-ui`; `notes-api` **not cloned**). Recruiter Hub / profile services are pointed from Engineering capability-map but **not** in phenom-knowledge routing packs — do not assert internals. |
| **What to do in Phenom** | • Let admins manage sources, markets, tags, and custom fields in the product — not via ticket.<br>• Fix resume and attachment handling: blank parse, CVs that reappear, files missing versus ATS.<br>• Give customers a clear privacy / delete status they can check themselves.<br>• Correct employee versus external badges when someone is terminated — without Support.<br>• Stop phantom “follow” tags and other field changes with no recruiter action. |

---

## Screening / interview / scheduling / offer / notifications — 394 (9.0%)

| | |
|--|--|
| **What customers report** | Screening/questionnaire/assessment issues; interview/scheduling/calendar; offer letter; missing recruiter notifications. |
| **What it means** | Cross-area funnel: **Screening (ODVA)** + **Scheduling** + offer workflows + notification delivery. |
| **Problem** | Assessments overwrite, screening doesn’t send, interview booking is blocked, and notifies are missing. |
| **Phenom knowledge** | **Screening (partial):** ODVA config/status/notifications in `crm-video-assessment` (`VideoAssessmentConfigController`, `VideoAssessmentStatusController`, `VANotifyService` → Kafka `cp_automation_notification`). Video capture/AI scoring/X+/Fitscore/Questionnaires **not in cloned Screening repos**. **Scheduling:** area **blocked** (no accessible repos). **Automations** call into both via Temporal activities (`SEND_ODVA`, `INITIATE_SCREENING`, `INVITE_FOR_INTERVIEW` — see `automations/skill.md`). Notifications often land in **Messaging**. |
| **What to do in Phenom** | • Notify recruiters when video assessment or interview status changes.<br>• Make auto-knockout / JSQ disposition reliable and show why it did or didn’t run.<br>• Don’t commit to deep calendar / self-schedule fixes until Scheduling is grounded in knowledge.<br>• Finish Screening knowledge (questionnaires/assessments) before promising deep product changes there. |

---

## Campaigns / job alerts / subscriptions / spotlights — 370 (8.4%)

| | |
|--|--|
| **What customers report** | Campaigns not sending/wrong audience; job alerts/subscriptions; spotlights/dynamic lists; talent pool/nurture language. |
| **What it means** | Audience + outbound **campaign** lifecycle (author → schedule → send → track). |
| **Problem** | Campaigns “complete” with zero sent, wrong audiences, and broken spotlights or subscriptions. |
| **Phenom knowledge** | **Messaging:** `crm-campaigns-ui` (builder), `storm-campaign` (execution), `crm-lists-ui` / `crm-candidate-lists` (lists, opt-in/out), platform campaign controllers (`CampaignController`, `CampaignsController`). Lifecycle documented in `messaging/skill.md`. Gateway prefixes `/ecampaign/*` → exact backend module **unverified**. |
| **What to do in Phenom** | • Before send, show who will receive it and why it would fail.<br>• Align spotlight and dynamic-list filters with the list builder.<br>• Fix Join-the-Community / talent forms so registrations create a findable CRM record.<br>• Let customers control job alerts and see why an alert was sent. |

---

## Hiring status / pipeline / stages / lead status — 263 (6.0%)

| | |
|--|--|
| **What customers report** | Wrong/stuck hiring or lead status, pipeline/stage moves, disposition/reject reasons, ATS↔CRM status mismatch (also overlaps sync theme). |
| **What it means** | Pipeline state machine and status vocabularies on the candidate×job (or lead) entity. |
| **Problem** | Statuses get stuck, extra options appear, or candidates move with no explanation. |
| **Phenom knowledge** | **Not found** as a dedicated phenom-knowledge area pack. Automations often **trigger on** status/field changes (`automation-search-service` matching) and can **set** status via actions — see Automations lifecycle. Exact CRM status APIs: not grounded in current packs. |
| **What to do in Phenom** | • Show which status moves are allowed for each customer — stop “no further transitions” dead ends.<br>• When someone is auto-moved to Decline or Review, show the exact rule or form answer that caused it.<br>• If an automation changed status, show that on the candidate — unexplained moves become tickets.<br>• Let recruiters clear New Leads that aren’t tied to a job without calling Support. |

---

## Email template content / hyperlinks / branding — 245 (5.6%)

| | |
|--|--|
| **What customers report** | Broken links, footer/logo/branding, placeholders, edit/access to templates, language/locale issues. |
| **What it means** | Template authoring & rendering for recruiter/system email (and related SMS templates). |
| **Problem** | From-name, white-label, broken URLs, and locked default templates need tickets to fix. |
| **Phenom knowledge** | **Messaging:** `crm-templates-ui` (`template-page.component.ts`), `email-facade-service` `TemplateController`, gateway `TemplateAPIController`. Cross-link: campaigns pull templates before `storm-campaign` send. |
| **What to do in Phenom** | • Let customers set From-name casing and white-label / event-share copy in the product.<br>• Validate links and merge fields on save before a template can be used.<br>• Show branding preview (logo, footer) before send.<br>• Clarify who can edit company-default versus personal templates. |

---

## Jobs / requisitions / applications / posting — 242 (5.5%)

| | |
|--|--|
| **What customers report** | Jobs missing/duplicate/not posting; applications stuck/incomplete; internal vs external posting; req IDs. |
| **What it means** | Job ingest/posting and application capture into CRM. |
| **Problem** | Close, publish, unpublish, and apply flows fail or behave inconsistently. |
| **Phenom knowledge** | **Not in** messaging/automations/screening packs. Engineering capability-map points IX job sync (`crm-storm-job-pull`) and `crm-jobs-service` — **not cloned under phenom-knowledge**; do not assert internals. |
| **What to do in Phenom** | • Make close / publish / unpublish work for the right role, and say why Publish is disabled.<br>• Stop spontaneous duplicate draft jobs; show who closed or cancelled a job.<br>• Confirm when a candidate is added to a job (or show the error) — not a silent “added.”<br>• Surface job sync health so “missing job / wrong posting” is visible before a ticket. |

---

## Email not sending / not receiving / spam / bounce — 224 (5.1%)

| | |
|--|--|
| **What customers report** | Emails not delivered, bounce/spam, sender/from issues, whitelist, unsubscribe/opt-in email problems. |
| **What it means** | **Delivery path** after compose/campaign — providers, suppression, analytics webhooks. |
| **Problem** | Domains, whitelist, inbox, and blocked or dropped mail create delivery tickets. |
| **Phenom knowledge** | **Messaging:** send via SendGrid / SES / MGW (`SendEmailServices`, `AWSService`); tracking `email-analytics-service` `SendgridWebhookController`; suppression `SuppressionListController`; one-click unsubscribe; transactional `txn-email-service`. |
| **What to do in Phenom** | • Self-serve sending domains, whitelist/blacklist, and suppression — with a real reason (not “NA”).<br>• Fix inbox so messages appear and stay in order; keep Outlook reply threads on the candidate.<br>• Tell recruiters when a message was blocked or a reminder was dropped — and why.<br>• Separate “never sent” from “sent but bounced” so the right team owns the fix. |

---

## Forwarding / LinkedIn / ATS↔CRM sync — 180 (4.1%)

| | |
|--|--|
| **What customers report** | Forward resume/candidate failures; LinkedIn export/import; ATS/Workday/SuccessFactors sync gaps. |
| **What it means** | Integration edges into CRM + LinkedIn CRM Connect. |
| **Problem** | Forwarding fails, LinkedIn breaks, and ATS/HM data lags or never lands. |
| **Phenom knowledge** | **Automations:** `crm-workflows` = LinkedIn CRM Connect (misnamed repo). Temporal activity **forward-to-HM** in `crm-automation-service`. Full ATS job sync: capability-map IX path — **not in phenom-knowledge packs**. |
| **What to do in Phenom** | • Show sync freshness and last failure for ATS↔CRM and recruiter lists.<br>• When forward-to-HM fails, say why in plain language (for example, user not in the system).<br>• Surface LinkedIn Connect errors in product instead of a blank failure.<br>• When Hiring Managers can’t see recruiter notes or docs, show the portal sync error — not an empty panel. |

---

## SMS / WhatsApp — 178 (4.1%)

| | |
|--|--|
| **What customers report** | SMS/WhatsApp not sending/showing; opt-in; scheduling limits; column/status issues. |
| **What it means** | Text messaging channels + opt-in compliance. |
| **Problem** | Opt-in looks wrong, blasts fail, and numbers or area codes are missing or incorrect. |
| **Phenom knowledge** | **Messaging:** SMS `text-api-service` `SMSController` / `OptInController`; WhatsApp via `crm-inbox-fe` `whatsapp-management.service.ts` + Gupshup/Twilio webhooks; campaign SMS in `storm-campaign` / `sms-campaign-service`. |
| **What to do in Phenom** | • Show opt-in and sendability on the profile before send.<br>• Show which countries have numbers; let admins assign recruiter numbers / area codes.<br>• Surface the real provider error when a text fails.<br>• Make WhatsApp template approval status obvious before a blast. |

---

## Automation not triggering / failing / wrongly triggered — 170 (3.9%)

| | |
|--|--|
| **What customers report** | Recipes not firing, wrong fire, failures, screening/invite automations, run history gaps. |
| **What it means** | Recipe **match + execute** reliability (two engines: Storm + Temporal). |
| **Problem** | Recipes don’t fire, fire wrong, or partially fail with no explanation. |
| **Phenom knowledge** | **Automations:** UI `crm-automations-ui`; CRUD `AutomationController`; match `automation-search-service` (`KafkaConsumer`, Lucene + ES + `ValidatorService`); execute `candidate-automation` `ActionFactory` (24 actions) **and/or** Temporal activities in `crm-automation-service`. Shared lib `CRMAutomationUtils` **not cloned**. |
| **What to do in Phenom** | • Show a simple run history: what triggered → which recipe → what happened (or why it failed).<br>• Make Automation Center actions (for example Email Candidate) consistent between staging and production.<br>• Let customers preview filters before turning a recipe on.<br>• Alert when something should have matched but quietly did not. |

---

## Profile merge / unmerge / duplicates / disappeared — 141 (3.2%)

| | |
|--|--|
| **What customers report** | Duplicate profiles, merge/unmerge, “candidate disappeared,” resume disappears. |
| **What it means** | Identity resolution / merge tooling on candidate records. |
| **Problem** | Bad merges, duplicates, and IDs that don’t line up create urgent identity tickets. |
| **Phenom knowledge** | **Not found** in cloned Messaging/Automations/Screening packs. Treat as CRM Core/Profile gap until a pack exists. |
| **What to do in Phenom** | • Show a merge preview and easy undo before profiles are combined.<br>• Merge when a referral email differs from the application email — don’t create two contacts.<br>• Let admins re-associate the correct CAND / ATS ID in the UI.<br>• Keep a log of who merged or unmerged whom, and when.<br>• Dedupe on import so duplicate profiles aren’t created in the first place. |

---

## Access / CRM not opening / permissions — 141 (3.2%)

| | |
|--|--|
| **What customers report** | Cannot open CRM, role/permission missing, login/SSO, admin access to features (incl. templates). |
| **What it means** | AuthZ/authN and feature entitlements for recruiter users. |
| **Problem** | CRM won’t open, reqs vanish after an email change, and wrong people still appear in pickers. |
| **Phenom knowledge** | **Not found** as a dedicated pack. Capability-map: Recruiter Hub / identity — not grounded here. Messaging notes RBAC pain for template edit in SRs but auth service code is outside Messaging skill. |
| **What to do in Phenom** | • After a user email or name change, re-link their jobs automatically.<br>• Remove deactivated users from Hiring Team dropdowns.<br>• Say clearly whether Close / CRM access is blocked by role, license, or outage.<br>• Let customers see which role unlocks which action without opening a case. |

---

## Events / university recruiting — 87 (2.0%)

| | |
|--|--|
| **What customers report** | Event registration, campus/university recruiting, event forms/images/invites. |
| **What it means** | Event entities + campus recruiting flows (often tied to CRM Events product label). |
| **Problem** | Event leads and marketing-email flags still go through Support. |
| **Phenom knowledge** | Screening ODVA can attach to **Event** entities (`crm-video-assessment`). Broader Events/UR CRM features **not** covered by Messaging/Automations packs. |
| **What to do in Phenom** | • Let customers mark event leads as marketing-email eligible on the profile.<br>• Allow editing the default email when sharing an event.<br>• Show whether registrations synced successfully and when they last updated. |

---

## Activity / notes / UI display — 80 (1.8%)

| | |
|--|--|
| **What customers report** | UI not displaying, buttons/tabs blank, notes/activity not showing, logos. |
| **What it means** | Front-end shell / notes / activity timeline reliability. |
| **Problem** | Notes won’t delete, activity duplicates, and the UI goes blank or lags. |
| **Phenom knowledge** | **Messaging:** notes UI `crm-notes-ui` → `/notes-api/*` (**notes-api not cloned**). Inbox UI `crm-inbox-fe`. Recruiter dashboard: **Analytics** pack (`crm-recruiter-dashboard`, `crm-dashboard-service`) for widget display — only if SR is dashboard-specific. |
| **What to do in Phenom** | • Let admins delete notes they can see, or explain why delete is hidden.<br>• Stop duplicate outreach lines when the candidate was only emailed once.<br>• Replace blank or freezing screens with permission versus load-failure messages. |

---

## Search / lists / filters / export / AI Discovery — 75 (1.7%)

| | |
|--|--|
| **What customers report** | Search/filter broken; lists empty; export issues; AI Discovery / sourcing from CRM. |
| **What it means** | Candidate discovery + list membership + export. |
| **Problem** | Exports show blank or Confidential fields; lists are hard to download; Discovery can’t source CRM. |
| **Phenom knowledge** | **Messaging:** lists `crm-lists-ui` / `crm-candidate-lists` (FilterService). AI Discovery / CRM search engines: **not found** in cloned Messaging/Automations/Screening packs. |
| **What to do in Phenom** | • Explain why a report shows N/A or Confidential — permission versus data rule.<br>• Show export progress and columns before download.<br>• Keep filters consistent and explain zero-result searches. |

---

## How-to / configuration / enablement question — 50 (1.1%)

| | |
|--|--|
| **What customers report** | Title-level how/what/can-we / enable-feature questions (title-only classifier). |
| **What it means** | Enablement gap more than defect — often deflectable. |
| **Problem** | Feature flags and setup still need a ticket for common configuration asks. |
| **Phenom knowledge** | Cross-cutting; map each how-to to Messaging/Automations/Screening docs once topic is known. |
| **What to do in Phenom** | • Let customers turn safe features on themselves (for example, associate documents to jobs).<br>• Add short guided flows for common “how do I…?” questions.<br>• Publish plain impact notes for known platform changes so Support isn’t the only channel. |

---

## Priority lens (by SR share, excluding Unclassified)

Highest volume themes to attack first for RX feedback reduction:

1. **Candidate profile / fields / GDPR** (10.6%)  
2. **Screening / interview / scheduling / notifications** (9.0%)  
3. **Campaigns / job alerts / spotlights** (8.4%)  
4. **Hiring status / pipeline** (6.0%)  
5. **Email templates** (5.6%) + **Email deliverability** (5.1%) — treat as one messaging program  

Together with unclassified process work (cluster_v2), these dominate RX support load.

## Provenance

- Theme **counts/%**: sheet CSV + `rx_theme_rules.py` only.  
- **Capability / reduce actions:** grounded in phenom-knowledge skill packs where cited; otherwise marked not found / not cloned.  
- Do not treat “To reduce feedback %” bullets as committed roadmap items.
