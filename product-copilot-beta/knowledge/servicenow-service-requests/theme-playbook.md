# RX theme playbook — what each theme is & how to reduce SR volume

**Population:** Recruiter Experience (RX), `JIRA_CREATED` ∈ {Yes, No}, n = **4,379** (sheet CSV).  
**Classifier:** high-confidence phrase rules (`rx_theme_rules.py` base + cluster_v1).  
**%** = share of that RX population.

**How to read “To reduce feedback %”:** plain-language actions that address the *kinds of tickets* in that theme — product reliability, clearer UX, enablement, or ops hygiene. These are **demand signals from SRs**, not an approved roadmap. Where Phenom Knowledge has cloned code, capabilities are cited; where not, that is stated explicitly.

**Phenom Knowledge packs used:** `phenom-knowledge/messaging/`, `automations/`, `screening/` (+ `INDEX.md`, Engineering `capability-map.md` for routing only).

---

## Unclassified / other — 1,076 (24.6%)

| | |
|--|--|
| **What it is** | SRs that did not match a high-confidence phrase rule. Includes mixed issues, sparse titles, and residual clusters (e.g. generic “candidate / email / team” language). |
| **Phenom knowledge** | Not a product capability — methodology residual (`theme-methodology.md`). |
| **To reduce feedback %** | • Review the leftover tickets again and add clear phrase rules only where the wording is obvious — do not force a weak label.<br>• Ask support to write clearer case titles for how-to questions so the next round classifies (and deflects) better. |

---

## Candidate profile data / fields / tags / location / GDPR — 463 (10.6%)

| | |
|--|--|
| **What customers report** | Wrong/missing profile fields, tags, location/address/phone, purge/GDPR/privacy, field add/rename/update failures. |
| **What the theme means in product terms** | Integrity and configurability of the **candidate record** in CRM (profile schema, tags, privacy/deletion). |
| **Phenom knowledge** | No dedicated “CRM Profile” area pack is built yet. Closest: Messaging **notes** (`crm-notes-ui`; `notes-api` **not cloned**). Recruiter Hub / profile services are pointed from Engineering capability-map but **not** in phenom-knowledge routing packs — do not assert internals. |
| **To reduce feedback %** | • Make sure phone, email, and location stay correct when a candidate applies or is imported — catch bad data before it lands on the profile.<br>• Give admins a simpler way to add, rename, and manage custom fields and tags without opening a ticket.<br>• Publish clear timelines for GDPR / data-purge requests, and let customers check status themselves instead of chasing Support.<br>• Add short in-product help for “how do I change this field?” so those questions never become SRs. |

---

## Screening / interview / scheduling / offer / notifications — 394 (9.0%)

| | |
|--|--|
| **What customers report** | Screening/questionnaire/assessment issues; interview/scheduling/calendar; offer letter; missing recruiter notifications. |
| **What it means** | Cross-area funnel: **Screening (ODVA)** + **Scheduling** + offer workflows + notification delivery. |
| **Phenom knowledge** | **Screening (partial):** ODVA config/status/notifications in `crm-video-assessment` (`VideoAssessmentConfigController`, `VideoAssessmentStatusController`, `VANotifyService` → Kafka `cp_automation_notification`). Video capture/AI scoring/X+/Fitscore/Questionnaires **not in cloned Screening repos**. **Scheduling:** area **blocked** (no accessible repos). **Automations** call into both via Temporal activities (`SEND_ODVA`, `INITIATE_SCREENING`, `INVITE_FOR_INTERVIEW` — see `automations/skill.md`). Notifications often land in **Messaging**. |
| **To reduce feedback %** | • Fix the path so invites and status changes reliably notify the recruiter — many tickets are “I never got notified.”<br>• Ship ready-made automation recipes for “invite to interview” and “send video assessment,” and show a clear history when a recipe fails.<br>• Calendar and self-schedule bugs need Scheduling code access first — treat that as a prerequisite before promising product fixes.<br>• For questionnaires and assessments, finish Screening knowledge packs before committing to deep engineering work. |

---

## Campaigns / job alerts / subscriptions / spotlights — 370 (8.4%)

| | |
|--|--|
| **What customers report** | Campaigns not sending/wrong audience; job alerts/subscriptions; spotlights/dynamic lists; talent pool/nurture language. |
| **What it means** | Audience + outbound **campaign** lifecycle (author → schedule → send → track). |
| **Phenom knowledge** | **Messaging:** `crm-campaigns-ui` (builder), `storm-campaign` (execution), `crm-lists-ui` / `crm-candidate-lists` (lists, opt-in/out), platform campaign controllers (`CampaignController`, `CampaignsController`). Lifecycle documented in `messaging/skill.md`. Gateway prefixes `/ecampaign/*` → exact backend module **unverified**. |
| **To reduce feedback %** | • Before a campaign sends, show who will receive it and why it would fail — so recruiters catch wrong audiences and bad setups themselves.<br>• Make spotlights and dynamic lists use the same filters as the list builder — mismatches drive a lot of “wrong people got this” tickets.<br>• Let customers control job-alert subscriptions (internal vs external) and see a simple audit of why an alert went out.<br>• Give CS and Product a live view of bounce and send failures so chronic delivery problems are fixed before they pile up as tickets. |

---

## Hiring status / pipeline / stages / lead status — 263 (6.0%)

| | |
|--|--|
| **What customers report** | Wrong/stuck hiring or lead status, pipeline/stage moves, disposition/reject reasons, ATS↔CRM status mismatch (also overlaps sync theme). |
| **What it means** | Pipeline state machine and status vocabularies on the candidate×job (or lead) entity. |
| **Phenom knowledge** | **Not found** as a dedicated phenom-knowledge area pack. Automations often **trigger on** status/field changes (`automation-search-service` matching) and can **set** status via actions — see Automations lifecycle. Exact CRM status APIs: not grounded in current packs. |
| **To reduce feedback %** | • Show each customer which hiring/lead statuses they can use and which moves are allowed — cuts “what statuses exist?” and stuck-pipeline tickets.<br>• When ATS and CRM disagree on status, show both values side by side so Support (and the customer) can see the gap immediately.<br>• If an automation moved a candidate’s status, let the recruiter see that in the run history — unexplained status changes create SRs.<br>• Stop silent auto-reject recipes: require confirmation or a clear warning before candidates are rejected automatically. |

---

## Email template content / hyperlinks / branding — 245 (5.6%)

| | |
|--|--|
| **What customers report** | Broken links, footer/logo/branding, placeholders, edit/access to templates, language/locale issues. |
| **What it means** | Template authoring & rendering for recruiter/system email (and related SMS templates). |
| **Phenom knowledge** | **Messaging:** `crm-templates-ui` (`template-page.component.ts`), `email-facade-service` `TemplateController`, gateway `TemplateAPIController`. Cross-link: campaigns pull templates before `storm-campaign` send. |
| **To reduce feedback %** | • When someone saves a template, check links and merge fields and flag broken ones before they go live.<br>• Preview how logo, footer, and brand styling will look so customers are not surprised after send.<br>• Make it obvious who can edit company-default templates vs their own account templates — many tickets are access confusion, not bugs.<br>• When cloning a template into another language, keep placeholders and layout intact so locale copies do not break. |

---

## Jobs / requisitions / applications / posting — 242 (5.5%)

| | |
|--|--|
| **What customers report** | Jobs missing/duplicate/not posting; applications stuck/incomplete; internal vs external posting; req IDs. |
| **What it means** | Job ingest/posting and application capture into CRM. |
| **Phenom knowledge** | **Not in** messaging/automations/screening packs. Engineering capability-map points IX job sync (`crm-storm-job-pull`) and `crm-jobs-service` — **not cloned under phenom-knowledge**; do not assert internals. |
| **To reduce feedback %** | • Show customers when job sync last succeeded or failed — “job is missing” tickets drop when sync health is visible.<br>• Explain in the UI what makes an application incomplete, so recruiters fix it without opening a case.<br>• Stop duplicate jobs/requisitions from being created on import.<br>• Build a Jobs knowledge pack so deeper fixes are grounded in real code, not guesses. |

---

## Email not sending / not receiving / spam / bounce — 224 (5.1%)

| | |
|--|--|
| **What customers report** | Emails not delivered, bounce/spam, sender/from issues, whitelist, unsubscribe/opt-in email problems. |
| **What it means** | **Delivery path** after compose/campaign — providers, suppression, analytics webhooks. |
| **Phenom knowledge** | **Messaging:** send via SendGrid / SES / MGW (`SendEmailServices`, `AWSService`); tracking `email-analytics-service` `SendgridWebhookController`; suppression `SuppressionListController`; one-click unsubscribe; transactional `txn-email-service`. |
| **To reduce feedback %** | • Give Product and CS a simple deliverability view per customer (bounce and spam rates) so problems are fixed before tickets pile up.<br>• Tell the recruiter clearly when a candidate is unsubscribed or suppressed — instead of a silent “email didn’t send.”<br>• Equip Support with a short sender-authentication checklist (SPF / DKIM / DMARC) for “landing in spam” cases.<br>• In triage, separate “automation never fired” from “email was sent but bounced” — those need different owners and fixes. |

---

## Forwarding / LinkedIn / ATS↔CRM sync — 180 (4.1%)

| | |
|--|--|
| **What customers report** | Forward resume/candidate failures; LinkedIn export/import; ATS/Workday/SuccessFactors sync gaps. |
| **What it means** | Integration edges into CRM + LinkedIn CRM Connect. |
| **Phenom knowledge** | **Automations:** `crm-workflows` = LinkedIn CRM Connect (misnamed repo). Temporal activity **forward-to-HM** in `crm-automation-service`. Full ATS job sync: capability-map IX path — **not in phenom-knowledge packs**. |
| **To reduce feedback %** | • Show LinkedIn Connect errors in the product UI instead of a blank failure that becomes an SR.<br>• When “forward to hiring manager” fails, say why (e.g. user not in the system) in plain language.<br>• Show how fresh ATS↔CRM sync is, and when it last failed, so customers know if the gap is lag vs a real break.<br>• Document the ATS sync path in a knowledge pack before promising deep engineering fixes. |

---

## SMS / WhatsApp — 178 (4.1%)

| | |
|--|--|
| **What customers report** | SMS/WhatsApp not sending/showing; opt-in; scheduling limits; column/status issues. |
| **What it means** | Text messaging channels + opt-in compliance. |
| **Phenom knowledge** | **Messaging:** SMS `text-api-service` `SMSController` / `OptInController`; WhatsApp via `crm-inbox-fe` `whatsapp-management.service.ts` + Gupshup/Twilio webhooks; campaign SMS in `storm-campaign` / `sms-campaign-service`. |
| **To reduce feedback %** | • Show opt-in status on the candidate profile and whether they are eligible for an SMS/WhatsApp campaign before send.<br>• Surface provider error messages (why the text failed) for recruiters and CS — not just “send failed.”<br>• Make WhatsApp template approval status obvious so customers know when a message can go out.<br>• Offer a small test/preview send before a large SMS or WhatsApp blast. |

---

## Automation not triggering / failing / wrongly triggered — 170 (3.9%)

| | |
|--|--|
| **What customers report** | Recipes not firing, wrong fire, failures, screening/invite automations, run history gaps. |
| **What it means** | Recipe **match + execute** reliability (two engines: Storm + Temporal). |
| **Phenom knowledge** | **Automations:** UI `crm-automations-ui`; CRUD `AutomationController`; match `automation-search-service` (`KafkaConsumer`, Lucene + ES + `ValidatorService`); execute `candidate-automation` `ActionFactory` (24 actions) **and/or** Temporal activities in `crm-automation-service`. Shared lib `CRMAutomationUtils` **not cloned**. |
| **To reduce feedback %** | • Let customers see a simple run history: what triggered, which recipe matched, and what the action did (or why it failed).<br>• Let them preview and validate filters before turning a recipe on — fewer “it fired on the wrong people” tickets.<br>• Alert when a recipe should have matched but quietly did not — silent misses create mystery SRs.<br>• For Support, document which actions run on which engine so debugging is faster and handoffs are clearer. |

---

## Profile merge / unmerge / duplicates / disappeared — 141 (3.2%)

| | |
|--|--|
| **What customers report** | Duplicate profiles, merge/unmerge, “candidate disappeared,” resume disappears. |
| **What it means** | Identity resolution / merge tooling on candidate records. |
| **Phenom knowledge** | **Not found** in cloned Messaging/Automations/Screening packs. Treat as CRM Core/Profile gap until a pack exists. |
| **To reduce feedback %** | • Show a clear merge preview and an easy undo — so merge mistakes do not become urgent tickets.<br>• Keep an audit log of who merged or unmerged whom, and when.<br>• When a profile is soft-deleted, keep it findable (with context) so candidates do not “disappear” with no explanation.<br>• Deduplicate on import before creating a new profile. |

---

## Access / CRM not opening / permissions — 141 (3.2%)

| | |
|--|--|
| **What customers report** | Cannot open CRM, role/permission missing, login/SSO, admin access to features (incl. templates). |
| **What it means** | AuthZ/authN and feature entitlements for recruiter users. |
| **Phenom knowledge** | **Not found** as a dedicated pack. Capability-map: Recruiter Hub / identity — not grounded here. Messaging notes RBAC pain for template edit in SRs but auth service code is outside Messaging skill. |
| **To reduce feedback %** | • Show in-product which role unlocks which feature — so “I can’t open X” is self-diagnosable.<br>• Let customers request access themselves, with a clear reason when access is denied.<br>• Give Support a short SSO troubleshooting checklist for login failures.<br>• Error messages should say whether a feature is turned off vs the user lacks permission — those are different fixes. |

---

## Events / university recruiting — 87 (2.0%)

| | |
|--|--|
| **What customers report** | Event registration, campus/university recruiting, event forms/images/invites. |
| **What it means** | Event entities + campus recruiting flows (often tied to CRM Events product label). |
| **Phenom knowledge** | Screening ODVA can attach to **Event** entities (`crm-video-assessment`). Broader Events/UR CRM features **not** covered by Messaging/Automations packs. |
| **To reduce feedback %** | • Make event forms and field setup easier so campus/event teams configure without Support.<br>• Show whether registrations synced successfully and when they last updated.<br>• Build an Events product knowledge pack before committing to deep code fixes. |

---

## Activity / notes / UI display — 80 (1.8%)

| | |
|--|--|
| **What customers report** | UI not displaying, buttons/tabs blank, notes/activity not showing, logos. |
| **What it means** | Front-end shell / notes / activity timeline reliability. |
| **Phenom knowledge** | **Messaging:** notes UI `crm-notes-ui` → `/notes-api/*` (**notes-api not cloned**). Inbox UI `crm-inbox-fe`. Recruiter dashboard: **Analytics** pack (`crm-recruiter-dashboard`, `crm-dashboard-service`) for widget display — only if SR is dashboard-specific. |
| **To reduce feedback %** | • Ground the notes backend in knowledge packs so blank notes/activity screens can be fixed with confidence.<br>• Replace blank screens with a clear message: “you don’t have permission” vs “this failed to load — try again.”<br>• Show when the activity feed was last refreshed so recruiters know if data is stale. |

---

## Search / lists / filters / export / AI Discovery — 75 (1.7%)

| | |
|--|--|
| **What customers report** | Search/filter broken; lists empty; export issues; AI Discovery / sourcing from CRM. |
| **What it means** | Candidate discovery + list membership + export. |
| **Phenom knowledge** | **Messaging:** lists `crm-lists-ui` / `crm-candidate-lists` (FilterService). AI Discovery / CRM search engines: **not found** in cloned Messaging/Automations/Screening packs. |
| **To reduce feedback %** | • Keep list filters consistent everywhere, and explain why a search returned zero results instead of a blank list.<br>• Show export progress/status and document which columns come out — “export broke / wrong columns” is a top ask.<br>• Build a Search / AI Discovery knowledge pack before promising deeper product changes. |

---

## How-to / configuration / enablement question — 50 (1.1%)

| | |
|--|--|
| **What customers report** | Title-level how/what/can-we / enable-feature questions (title-only classifier). |
| **What it means** | Enablement gap more than defect — often deflectable. |
| **Phenom knowledge** | Cross-cutting; map each how-to to Messaging/Automations/Screening docs once topic is known. |
| **To reduce feedback %** | • Add short guided setups in the product for the most common “how do I…?” questions.<br>• Give CS ready-made answer macros mapped to these themes so how-to cases close without engineering.<br>• Where it is safe, let customers turn features on themselves instead of waiting for a ticket to enable them. |

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
