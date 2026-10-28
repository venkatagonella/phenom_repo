"""Phenom-knowledge-grounded RX theme elaborations.

`problem` = human summary from SHORT_DESCRIPTION + DESCRIPTION
(Jira Yes and No Service Requests). `reduce` = what to do in Phenom.
"""

from __future__ import annotations

PRIORITY_ORDER = [
    'Candidate profile data / fields / tags / location / GDPR',
    'Email not sending / not receiving / spam / bounce',
    'Jobs / requisitions / applications / posting',
    'Hiring status / pipeline / stages / lead status',
    'Automation not triggering / failing / wrongly triggered',
    'Campaigns / job alerts / subscriptions / spotlights',
]

THEME_PLAYBOOK: dict[str, dict] = {
    'Candidate profile data / fields / tags / location / GDPR': {
        "means": ('Integrity and configurability of the candidate record: wrong/missing fields, tags, location/phone/email, GDPR/purge/privacy, field add/rename failures, sources, attachments/resumes.'),
        "problem": 'Largest theme across Yes and No: wrong/missing fields and sources, internal badge missing, attachments auto-download or go missing, privacy delete without a CRM path, and profile edits that save in list view but not on the profile.',
        "knowledge": ('No dedicated CRM Profile pack. Closest: Messaging notes UI (crm-notes-ui; notes-api not cloned). Recruiter Hub/profile services appear on Engineering capability-map but are not in phenom-knowledge routing packs — do not assert internals.'),
        "reduce": [
            'Let admins manage sources, markets, tags, and field order in the product.',
            'Fix resume/attachment open, parse, and ATS mismatches.',
            'Give a clear privacy / delete path and status in CRM.',
            'Make profile edits that work in list view also save on the profile.',
            'Keep internal vs external badges accurate after hire/terminate.',
        ],
        "pack": 'gap (Profile)',
    },
    'Screening / interview / scheduling / offer / notifications': {
        "means": ('Funnel friction across Screening (ODVA/questionnaire), interview/scheduling/calendar, offer letters, and missing recruiter notifications.'),
        "problem": 'Tagged-note and screening notifies never fire; assessments overwrite or land on the wrong tab; interview override/busy-slot booking fails; invite-to-interview templates empty in Automation Center — Jira No volume is high.',
        "knowledge": ('Screening (partial): ODVA config/status/notify in crm-video-assessment (VideoAssessmentConfigController, VideoAssessmentStatusController, VANotifyService → Kafka cp_automation_notification). Video capture/AI scoring/X+/Fitscore/Questionnaires not in cloned Screening repos. Scheduling area blocked (no accessible repos). Automations Temporal activities: SEND_ODVA, INITIATE_SCREENING, INVITE_FOR_INTERVIEW. Notify path often lands in Messaging.'),
        "reduce": [
            'Notify when tagged notes, screening sends, or interview status change — and show failures.',
            'Stop assessments overwriting valid results inside the retention window.',
            'Fix interview override/busy-slot booking and empty invite templates in Automation Center.',
            'Show why a candidate landed on the wrong screening/assessment tab.',
        ],
        "pack": 'screening + automations (+ scheduling blocked)',
    },
    'Campaigns / job alerts / subscriptions / spotlights': {
        "means": ('Audience + outbound campaign lifecycle: campaigns not sending/wrong audience, job alerts/subscriptions, spotlights/dynamic lists, talent-pool/nurture language, join-the-community (JTC) forms.'),
        "problem": 'Campaigns mark complete with 0 sent; subscription/job-alert templates and headers do not update; spotlights will not save; staging alerts leak into prod mailboxes — heavy on both Yes and No.',
        "knowledge": ('Messaging: crm-campaigns-ui (builder), storm-campaign (execution), crm-lists-ui / crm-candidate-lists (lists, opt-in/out), platform CampaignController / CampaignsController. Gateway /ecampaign/* → exact backend module unverified.'),
        "reduce": [
            'Before send, show who will receive it and why a campaign would complete with 0 sent.',
            'Keep subscription / job-alert template headers and bodies in sync after edits.',
            'Fix spotlight save and remove staging alerts leaking into production inboxes.',
            'Let customers create and update subscription campaigns without Phenom-admin-only blocks where safe.',
        ],
        "pack": 'messaging',
    },
    'Hiring status / pipeline / stages / lead status': {
        "means": ('Pipeline state machine and status vocabularies: stuck/wrong hiring or lead status, stage moves, disposition/reject reasons, ATS↔CRM mismatch.'),
        "problem": 'Recruiters cannot change lead or hiring status (dropdown empty, “no further transitions”), pipeline does not update after HM forward, and allowed moves differ for similar candidates — on both Jira Yes and No tickets.',
        "knowledge": ('Not a dedicated phenom-knowledge pack. Automations often trigger on status/field changes (automation-search-service) and can set status via actions — exact CRM status APIs not grounded in current packs.'),
        "reduce": [
            'Show which status moves are allowed for each customer — stop empty dropdowns and “no further transitions.”',
            'When status should update after HM forward or automation, show it immediately or show why it did not.',
            'If an automation changed status, show that on the candidate.',
            'Let recruiters clear stuck leads without calling Support.',
        ],
        "pack": 'gap (pipeline) · automations adjacent',
    },
    'Email template content / hyperlinks / branding': {
        "means": ('Template authoring & rendering: broken links, footer/logo/branding, From-name casing, white-label copy, placeholders, locale.'),
        "problem": 'Default templates locked or missing in prod; placeholders like first name / job category stay blank; From-name casing and white-label still need tickets; Jira No is mostly template enable/edit asks.',
        "knowledge": ('Messaging: crm-templates-ui (template-page.component.ts), email-facade-service TemplateController, gateway TemplateAPIController. Campaigns pull templates before storm-campaign send.'),
        "reduce": [
            'Let Master Admins manage default templates in prod the same way as staging.',
            'Validate placeholders (name, job category, links) on save before send.',
            'Allow From-name casing and white-label edits in product.',
            'Export or list all templates so customers can audit without a ticket.',
        ],
        "pack": 'messaging',
    },
    'Jobs / requisitions / applications / posting': {
        "means": ('Job ingest/posting and application capture: close/publish/unpublish failures, duplicate draft jobs, internal vs external visibility, referral data, incomplete apply.'),
        "problem": 'Close/publish/unpublish fails, pay rate and posting dates disagree with the careers site, candidates do not land on the right req, and HMs lose visibility when a job is unposted — common on both Jira-linked and non-Jira SRs.',
        "knowledge": ('Not in messaging/automations/screening packs. Capability-map points IX job sync (crm-storm-job-pull) and crm-jobs-service — not cloned under phenom-knowledge.'),
        "reduce": [
            'Make close / publish / unpublish work for the assigned recruiter and say why the action is blocked.',
            'Keep careers-site pay rate and post dates in sync with the job record.',
            'Confirm candidates land on the right req (or show the transfer error).',
            'Keep unposted jobs visible to HMs for review when customers need that.',
        ],
        "pack": 'gap (jobs / IX)',
    },
    'Email not sending / not receiving / spam / bounce': {
        "means": ('Delivery path after compose/campaign: not delivered, bounce/spam, domain registration, whitelist/blacklist/suppression, inbox gaps, referral and incomplete-apply reminder emails.'),
        "problem": 'Inbox shows unread with nothing inside; domains need registering; whitelist/blacklist is ticket-only (especially Jira No UAT); tagged-note and incomplete-apply emails go missing or fire after the app is complete.',
        "knowledge": ('Messaging: SendGrid/SES/MGW (SendEmailServices, AWSService); email-analytics-service SendgridWebhookController; SuppressionListController; one-click unsubscribe; txn-email-service.'),
        "reduce": [
            'Self-serve domain register, whitelist/blacklist, and suppression with a real reason (not “NA”).',
            'Fix inbox so unread counts match visible messages and threads stay in order.',
            'Stop incomplete-apply reminders after the application is already complete.',
            'Tell recruiters when tagged-note or candidate mail was blocked — and why.',
        ],
        "pack": 'messaging',
    },
    'Forwarding / LinkedIn / ATS↔CRM sync': {
        "means": ('Integration edges: forward resume/candidate failures, LinkedIn export/import, ATS/Workday/SuccessFactors/HM-portal sync gaps, stale recruiter lists.'),
        "problem": 'Forward-to-HM fails with “user not in the system,” Workday/ATS applies never appear on the Phenom req, LinkedIn CRM Connect export or Edge recommendations break, and recruiter/HM emails stay out of date.',
        "knowledge": ('Automations: crm-workflows = LinkedIn CRM Connect; Temporal forward-to-HM in crm-automation-service. Full ATS job sync (IX) not in phenom-knowledge packs.'),
        "reduce": [
            'When forward-to-HM fails, say why in plain language (for example, user not in the system).',
            'Show ATS/Workday sync freshness and push missing applies onto the Phenom req.',
            'Fix LinkedIn CRM Connect export and Edge recommendations with visible errors.',
            'Keep recruiter and HM email lists current after people changes.',
        ],
        "pack": 'automations (+ IX gap)',
    },
    'SMS / WhatsApp': {
        "means": ('Text channels + opt-in: SMS/WhatsApp not sending/showing, opt-in, local numbers / area codes, “no numbers available.”'),
        "problem": 'Opt-in wrong or missing on profile, blasts fail or lack AM slots/numbers (NZ/AU/area codes), WhatsApp templates reject, and STOP consent behavior is unclear — Yes and No alike.',
        "knowledge": ('Messaging: text-api-service SMSController / OptInController; WhatsApp via crm-inbox-fe whatsapp-management.service.ts + Gupshup/Twilio webhooks; campaign SMS in storm-campaign / sms-campaign-service.'),
        "reduce": [
            'Show accurate SMS opt-in on the profile (including IQA/Workday sources).',
            'Provide numbers for required countries/area codes and clearer “no number available” guidance.',
            'Surface real send errors for blasts and WhatsApp template rejection reasons.',
            'Document STOP behavior on 1:1 SMS so consent updates are predictable.',
        ],
        "pack": 'messaging',
    },
    'Automation not triggering / failing / wrongly triggered': {
        "means": ('Recipe match + execute reliability: not firing, wrong fire, failures, missing Automation Center actions (e.g. Email Candidate), run-history gaps.'),
        "problem": 'Recipes do not fire for matching candidates, fire too often, work in staging but fail in prod, or send rejection mail customers want paused — with no clear run history on either Jira Yes or No.',
        "knowledge": ('Automations: crm-automations-ui; AutomationController CRUD; automation-search-service match (KafkaConsumer, Lucene+ES, ValidatorService); execute via candidate-automation ActionFactory (24 actions) and/or Temporal activities in crm-automation-service. CRMAutomationUtils shared lib not cloned.'),
        "reduce": [
            'Show run history: trigger → recipe → result (or why it failed) for Yes and No cases.',
            'Make staging and production recipe behavior match, or show the config gap.',
            'Let customers pause or exclude candidates from a rejection automation quickly.',
            'Alert when a candidate matches conditions but the recipe never fires.',
        ],
        "pack": 'automations',
    },
    'Profile merge / unmerge / duplicates / disappeared': {
        "means": ('Identity resolution: duplicates, merge/unmerge, CAND/ATS ID reassignment, referral email mismatches that create two contacts.'),
        "problem": 'Wrong merges and unmerges dominate Jira Yes; Jira No adds duplicate profiles on re-apply/agency upload with no duplicate check, merge status customers cannot see, and profiles that disappear.',
        "knowledge": ('Not found in Messaging/Automations/Screening packs — CRM Core/Profile gap until a pack exists.'),
        "reduce": [
            'Show merge preview and easy undo; block wrong merges that mix documents.',
            'Run duplicate checks on apply and agency upload — not only on manual add.',
            'Show merge status on the profile so customers do not have to ask Support.',
            'Keep a findable trail when a profile is soft-deleted or “disappears.”',
        ],
        "pack": 'gap (merge / identity)',
    },
    'Access / CRM not opening / permissions': {
        "means": ('AuthZ/authN and entitlements: cannot open CRM, role/permission missing, email/name changes breaking req visibility, deactivated users still in hiring-team pickers.'),
        "problem": 'CRM will not open or loads a 401, Apps dropdown is empty despite access, email changes drop req visibility, and feature flags (Chrome extension, Create Job, forms) still need a ticket to turn on.',
        "knowledge": ('No dedicated pack. Capability-map: Recruiter Hub / identity — not grounded here. Messaging SRs mention template RBAC; auth service code is outside Messaging skill.'),
        "reduce": [
            'When CRM will not open, say whether it is role, license, or outage — not a blank spin or 401.',
            'After email/name change, re-link jobs automatically.',
            'Let admins turn safe feature flags on themselves (extension, Create Job limits, forms).',
            'Remove deactivated users from Hiring Team and similar pickers.',
        ],
        "pack": 'gap (identity / access)',
    },
    'Events / university recruiting': {
        "means": ('Event entities + campus recruiting: registration, marketing-email flags on event leads, event share email copy.'),
        "problem": 'Event marketing-email flags and registration copy still go through Support; campus reps cannot log into the event app; invite-to-event and Early Talent access are unclear.',
        "knowledge": ('Screening ODVA can attach to Event entities (crm-video-assessment). Broader Events/UR CRM features not covered by Messaging/Automations packs.'),
        "reduce": [
            'Let customers mark event leads as marketing-email eligible without a spreadsheet ticket.',
            'Allow editing event registration confirmation copy in product.',
            'Make invite-to-event and Early Talent access self-explanatory for the right roles.',
        ],
        "pack": 'screening (partial) · Events gap',
    },
    'Activity / notes / UI display': {
        "means": ('Front-end shell / notes / activity timeline: notes delete, duplicate activity lines, lagging/freezing UI, inbox ordering.'),
        "problem": 'Counts on screen disagree with buckets, notes cannot be deleted even as Master Admin, activity shows triple outreach, dashboards stay blank, and texting shows “Failed to fetch conversations.”',
        "knowledge": ('Messaging: crm-notes-ui → /notes-api/* (notes-api not cloned); crm-inbox-fe. Dashboard widgets: Analytics pack (crm-recruiter-dashboard, crm-dashboard-service) only if SR is dashboard-specific.'),
        "reduce": [
            'Align bucket counts with what the UI shows.',
            'Let Master Admins delete notes or explain why delete is hidden.',
            'Stop duplicate outreach lines on the activity tab.',
            'Replace blank dashboards and “Failed to fetch conversations” with a clear retry/error.',
        ],
        "pack": 'messaging (+ analytics if dashboard)',
    },
    'Search / lists / filters / export / AI Discovery': {
        "means": ('Candidate discovery + list membership + export: search/filter broken, lists empty, report/export columns blank or confidential.'),
        "problem": 'List build returns empty mid-filter; exports show N/A or Confidential; phone/preferred fields missing from export; AI Discovery cannot source CRM or external candidates.',
        "knowledge": ('Messaging: lists crm-lists-ui / crm-candidate-lists (FilterService). AI Discovery / CRM search engines not found in cloned Messaging/Automations/Screening packs.'),
        "reduce": [
            'Keep list filters working through Apply & View Results — no empty mid-build.',
            'Explain N/A / Confidential on exports and include phone when configured.',
            'Fix AI Discovery sourcing from CRM and expected external candidates.',
        ],
        "pack": 'messaging (lists) · Discovery gap',
    },
    'How-to / configuration / enablement question': {
        "means": ('Enablement gap more than defect — how/what/can-we, enable-feature, org/department rename, impact questions (e.g. timezone changes).'),
        "problem": 'Admins ask Support to enable flags (calendar, docs-to-jobs, incomplete-apply reminders, preferred name), rename departments, change time zones/area codes, and recover deleted candidates.',
        "knowledge": ('Cross-cutting; map each how-to to Messaging/Automations/Screening docs once the topic is known.'),
        "reduce": [
            'Let customers enable common flags themselves (docs-to-jobs, incomplete-apply reminders, preferred name).',
            'Short guided flows for department rename, time zone, and area-code changes.',
            'Show how to recover a soft-deleted candidate without a ticket.',
        ],
        "pack": 'cross-cutting',
    },
}

AREA_ORDER = [
    'CRM Core',
    'CRM Profile',
    'CRM Messaging',
    'CRM Automations',
]

THEME_AREA: dict[str, str] = {
    'Hiring status / pipeline / stages / lead status': 'CRM Core',
    'Jobs / requisitions / applications / posting': 'CRM Core',
    'Forwarding / LinkedIn / ATS↔CRM sync': 'CRM Core',
    'Access / CRM not opening / permissions': 'CRM Core',
    'Events / university recruiting': 'CRM Core',
    'How-to / configuration / enablement question': 'CRM Core',
    'Candidate profile data / fields / tags / location / GDPR': 'CRM Profile',
    'Profile merge / unmerge / duplicates / disappeared': 'CRM Profile',
    'Campaigns / job alerts / subscriptions / spotlights': 'CRM Messaging',
    'Email template content / hyperlinks / branding': 'CRM Messaging',
    'Email not sending / not receiving / spam / bounce': 'CRM Messaging',
    'SMS / WhatsApp': 'CRM Messaging',
    'Activity / notes / UI display': 'CRM Messaging',
    'Search / lists / filters / export / AI Discovery': 'CRM Messaging',
    'Automation not triggering / failing / wrongly triggered': 'CRM Automations',
    'Screening / interview / scheduling / offer / notifications': 'CRM Automations',
}

AREA_BLURB: dict[str, str] = {
    'CRM Core': ('Across Jira Yes and No Service Requests, Core pain is status moves that will not stick, jobs that will not close or post correctly, ATS/LinkedIn/forwarding breaks, and access that disappears after email or role changes. Recruiters cannot self-serve these — they open tickets.'),
    'CRM Profile': ('Profile holds the single largest theme in the data — candidate profile data — and it is the only area where Jira-created Service Requests outnumber non-Jira ones. Tickets show field/source/privacy work still done by Support, resumes and attachments that misbehave, and merges/duplicates/disappeared profiles — especially wrong merges on Jira Yes and silent duplicates on Jira No.'),
    'CRM Messaging': ('Messaging is the largest area overall (Yes + No). Campaigns complete with zero sends, job-alert/subscription templates drift, email delivery and whitelist stay ticket-driven, and SMS/WhatsApp opt-in and numbers fail. Template/placeholder edits dominate Jira No.'),
    'CRM Automations': ('Smaller share but noisy: screening/interview notifies and calendar booking fail silently, and Automation Center recipes miss, double-fire, or differ between staging and production — on both Jira-updated and non-Jira Service Requests.'),
}
