"""Phenom-knowledge-grounded RX theme elaborations (meaning + reduce-feedback actions).

Counts/% live in the sheet classifier report — not here.
Capabilities cite phenom-knowledge packs; gaps are explicit.
`reduce` is a list of short, human-readable actions.
"""

from __future__ import annotations

# Keys must match theme names in rx_theme_rules.py exactly.
THEME_PLAYBOOK: dict[str, dict] = {
    "Unclassified / other": {
        "means": (
            "SRs that did not match a high-confidence phrase rule — mixed issues, "
            "sparse titles, or residual cluster language. Not a product capability."
        ),
        "knowledge": (
            "Methodology residual (theme-methodology.md). No phenom-knowledge area."
        ),
        "reduce": [
            "Review the leftover tickets again and add clear phrase rules only where the wording is obvious — do not force a weak label.",
            "Ask support to write clearer case titles for how-to questions so the next round classifies (and deflects) better.",
        ],
        "pack": "—",
    },
    "Candidate profile data / fields / tags / location / GDPR": {
        "means": (
            "Integrity and configurability of the candidate record: wrong/missing "
            "fields, tags, location/phone/email, GDPR/purge/privacy, field "
            "add/rename failures."
        ),
        "knowledge": (
            "No dedicated CRM Profile pack. Closest: Messaging notes UI "
            "(crm-notes-ui; notes-api not cloned). Recruiter Hub/profile services "
            "appear on Engineering capability-map but are not in phenom-knowledge "
            "routing packs — do not assert internals."
        ),
        "reduce": [
            "Make sure phone, email, and location stay correct when a candidate applies or is imported — catch bad data before it lands on the profile.",
            "Give admins a simpler way to add, rename, and manage custom fields and tags without opening a ticket.",
            "Publish clear timelines for GDPR / data-purge requests, and let customers check status themselves instead of chasing Support.",
            "Add short in-product help for “how do I change this field?” so those questions never become SRs.",
        ],
        "pack": "gap (Profile)",
    },
    "Screening / interview / scheduling / offer / notifications": {
        "means": (
            "Funnel friction across Screening (ODVA/questionnaire), interview/"
            "scheduling/calendar, offer letters, and missing recruiter notifications."
        ),
        "knowledge": (
            "Screening (partial): ODVA config/status/notify in crm-video-assessment "
            "(VideoAssessmentConfigController, VideoAssessmentStatusController, "
            "VANotifyService → Kafka cp_automation_notification). Video capture/"
            "AI scoring/X+/Fitscore/Questionnaires not in cloned Screening repos. "
            "Scheduling area blocked (no accessible repos). Automations Temporal "
            "activities: SEND_ODVA, INITIATE_SCREENING, INVITE_FOR_INTERVIEW. "
            "Notify path often lands in Messaging."
        ),
        "reduce": [
            "Fix the path so invites and status changes reliably notify the recruiter — many tickets are “I never got notified.”",
            "Ship ready-made automation recipes for “invite to interview” and “send video assessment,” and show a clear history when a recipe fails.",
            "Calendar and self-schedule bugs need Scheduling code access first — treat that as a prerequisite before promising product fixes.",
            "For questionnaires and assessments, finish Screening knowledge packs before committing to deep engineering work.",
        ],
        "pack": "screening + automations (+ scheduling blocked)",
    },
    "Campaigns / job alerts / subscriptions / spotlights": {
        "means": (
            "Audience + outbound campaign lifecycle: campaigns not sending/wrong "
            "audience, job alerts/subscriptions, spotlights/dynamic lists, "
            "talent-pool/nurture language."
        ),
        "knowledge": (
            "Messaging: crm-campaigns-ui (builder), storm-campaign (execution), "
            "crm-lists-ui / crm-candidate-lists (lists, opt-in/out), platform "
            "CampaignController / CampaignsController. Gateway /ecampaign/* → "
            "exact backend module unverified."
        ),
        "reduce": [
            "Before a campaign sends, show who will receive it and why it would fail — so recruiters catch wrong audiences and bad setups themselves.",
            "Make spotlights and dynamic lists use the same filters as the list builder — mismatches drive a lot of “wrong people got this” tickets.",
            "Let customers control job-alert subscriptions (internal vs external) and see a simple audit of why an alert went out.",
            "Give CS and Product a live view of bounce and send failures so chronic delivery problems are fixed before they pile up as tickets.",
        ],
        "pack": "messaging",
    },
    "Hiring status / pipeline / stages / lead status": {
        "means": (
            "Pipeline state machine and status vocabularies: stuck/wrong hiring or "
            "lead status, stage moves, disposition/reject reasons, ATS↔CRM mismatch."
        ),
        "knowledge": (
            "Not a dedicated phenom-knowledge pack. Automations often trigger on "
            "status/field changes (automation-search-service) and can set status "
            "via actions — exact CRM status APIs not grounded in current packs."
        ),
        "reduce": [
            "Show each customer which hiring/lead statuses they can use and which moves are allowed — cuts “what statuses exist?” and stuck-pipeline tickets.",
            "When ATS and CRM disagree on status, show both values side by side so Support (and the customer) can see the gap immediately.",
            "If an automation moved a candidate’s status, let the recruiter see that in the run history — unexplained status changes create SRs.",
            "Stop silent auto-reject recipes: require confirmation or a clear warning before candidates are rejected automatically.",
        ],
        "pack": "gap (pipeline) · automations adjacent",
    },
    "Email template content / hyperlinks / branding": {
        "means": (
            "Template authoring & rendering: broken links, footer/logo/branding, "
            "placeholders, edit/access, language/locale."
        ),
        "knowledge": (
            "Messaging: crm-templates-ui (template-page.component.ts), "
            "email-facade-service TemplateController, gateway TemplateAPIController. "
            "Campaigns pull templates before storm-campaign send."
        ),
        "reduce": [
            "When someone saves a template, check links and merge fields and flag broken ones before they go live.",
            "Preview how logo, footer, and brand styling will look so customers are not surprised after send.",
            "Make it obvious who can edit company-default templates vs their own account templates — many tickets are access confusion, not bugs.",
            "When cloning a template into another language, keep placeholders and layout intact so locale copies do not break.",
        ],
        "pack": "messaging",
    },
    "Jobs / requisitions / applications / posting": {
        "means": (
            "Job ingest/posting and application capture: missing/duplicate jobs, "
            "stuck/incomplete applications, internal vs external posting, req IDs."
        ),
        "knowledge": (
            "Not in messaging/automations/screening packs. Capability-map points "
            "IX job sync (crm-storm-job-pull) and crm-jobs-service — not cloned "
            "under phenom-knowledge."
        ),
        "reduce": [
            "Show customers when job sync last succeeded or failed — “job is missing” tickets drop when sync health is visible.",
            "Explain in the UI what makes an application incomplete, so recruiters fix it without opening a case.",
            "Stop duplicate jobs/requisitions from being created on import.",
            "Build a Jobs knowledge pack so deeper fixes are grounded in real code, not guesses.",
        ],
        "pack": "gap (jobs / IX)",
    },
    "Email not sending / not receiving / spam / bounce": {
        "means": (
            "Delivery path after compose/campaign: not delivered, bounce/spam, "
            "sender/from issues, whitelist, unsubscribe/opt-in email problems."
        ),
        "knowledge": (
            "Messaging: SendGrid/SES/MGW (SendEmailServices, AWSService); "
            "email-analytics-service SendgridWebhookController; "
            "SuppressionListController; one-click unsubscribe; txn-email-service."
        ),
        "reduce": [
            "Give Product and CS a simple deliverability view per customer (bounce and spam rates) so problems are fixed before tickets pile up.",
            "Tell the recruiter clearly when a candidate is unsubscribed or suppressed — instead of a silent “email didn’t send.”",
            "Equip Support with a short sender-authentication checklist (SPF / DKIM / DMARC) for “landing in spam” cases.",
            "In triage, separate “automation never fired” from “email was sent but bounced” — those need different owners and fixes.",
        ],
        "pack": "messaging",
    },
    "Forwarding / LinkedIn / ATS↔CRM sync": {
        "means": (
            "Integration edges: forward resume/candidate failures, LinkedIn "
            "export/import, ATS/Workday/SuccessFactors sync gaps."
        ),
        "knowledge": (
            "Automations: crm-workflows = LinkedIn CRM Connect; Temporal "
            "forward-to-HM in crm-automation-service. Full ATS job sync (IX) "
            "not in phenom-knowledge packs."
        ),
        "reduce": [
            "Show LinkedIn Connect errors in the product UI instead of a blank failure that becomes an SR.",
            "When “forward to hiring manager” fails, say why (e.g. user not in the system) in plain language.",
            "Show how fresh ATS↔CRM sync is, and when it last failed, so customers know if the gap is lag vs a real break.",
            "Document the ATS sync path in a knowledge pack before promising deep engineering fixes.",
        ],
        "pack": "automations (+ IX gap)",
    },
    "SMS / WhatsApp": {
        "means": (
            "Text channels + opt-in: SMS/WhatsApp not sending/showing, opt-in, "
            "scheduling limits, column/status issues."
        ),
        "knowledge": (
            "Messaging: text-api-service SMSController / OptInController; "
            "WhatsApp via crm-inbox-fe whatsapp-management.service.ts + "
            "Gupshup/Twilio webhooks; campaign SMS in storm-campaign / "
            "sms-campaign-service."
        ),
        "reduce": [
            "Show opt-in status on the candidate profile and whether they are eligible for an SMS/WhatsApp campaign before send.",
            "Surface provider error messages (why the text failed) for recruiters and CS — not just “send failed.”",
            "Make WhatsApp template approval status obvious so customers know when a message can go out.",
            "Offer a small test/preview send before a large SMS or WhatsApp blast.",
        ],
        "pack": "messaging",
    },
    "Automation not triggering / failing / wrongly triggered": {
        "means": (
            "Recipe match + execute reliability: not firing, wrong fire, failures, "
            "screening/invite automations, run-history gaps."
        ),
        "knowledge": (
            "Automations: crm-automations-ui; AutomationController CRUD; "
            "automation-search-service match (KafkaConsumer, Lucene+ES, "
            "ValidatorService); execute via candidate-automation ActionFactory "
            "(24 actions) and/or Temporal activities in crm-automation-service. "
            "CRMAutomationUtils shared lib not cloned."
        ),
        "reduce": [
            "Let customers see a simple run history: what triggered, which recipe matched, and what the action did (or why it failed).",
            "Let them preview and validate filters before turning a recipe on — fewer “it fired on the wrong people” tickets.",
            "Alert when a recipe should have matched but quietly did not — silent misses create mystery SRs.",
            "For Support, document which actions run on which engine so debugging is faster and handoffs are clearer.",
        ],
        "pack": "automations",
    },
    "Profile merge / unmerge / duplicates / disappeared": {
        "means": (
            "Identity resolution: duplicates, merge/unmerge, “candidate "
            "disappeared,” resume disappears."
        ),
        "knowledge": (
            "Not found in Messaging/Automations/Screening packs — CRM Core/"
            "Profile gap until a pack exists."
        ),
        "reduce": [
            "Show a clear merge preview and an easy undo — so merge mistakes do not become urgent tickets.",
            "Keep an audit log of who merged or unmerged whom, and when.",
            "When a profile is soft-deleted, keep it findable (with context) so candidates do not “disappear” with no explanation.",
            "Deduplicate on import before creating a new profile.",
        ],
        "pack": "gap (merge / identity)",
    },
    "Access / CRM not opening / permissions": {
        "means": (
            "AuthZ/authN and entitlements: cannot open CRM, role/permission "
            "missing, login/SSO, admin access to features (incl. templates)."
        ),
        "knowledge": (
            "No dedicated pack. Capability-map: Recruiter Hub / identity — not "
            "grounded here. Messaging SRs mention template RBAC; auth service "
            "code is outside Messaging skill."
        ),
        "reduce": [
            "Show in-product which role unlocks which feature — so “I can’t open X” is self-diagnosable.",
            "Let customers request access themselves, with a clear reason when access is denied.",
            "Give Support a short SSO troubleshooting checklist for login failures.",
            "Error messages should say whether a feature is turned off vs the user lacks permission — those are different fixes.",
        ],
        "pack": "gap (identity / access)",
    },
    "Events / university recruiting": {
        "means": (
            "Event entities + campus recruiting: registration, campus/university "
            "flows, event forms/images/invites."
        ),
        "knowledge": (
            "Screening ODVA can attach to Event entities (crm-video-assessment). "
            "Broader Events/UR CRM features not covered by Messaging/Automations packs."
        ),
        "reduce": [
            "Make event forms and field setup easier so campus/event teams configure without Support.",
            "Show whether registrations synced successfully and when they last updated.",
            "Build an Events product knowledge pack before committing to deep code fixes.",
        ],
        "pack": "screening (partial) · Events gap",
    },
    "Activity / notes / UI display": {
        "means": (
            "Front-end shell / notes / activity timeline: UI not displaying, "
            "blank buttons/tabs, notes/activity missing, logos."
        ),
        "knowledge": (
            "Messaging: crm-notes-ui → /notes-api/* (notes-api not cloned); "
            "crm-inbox-fe. Dashboard widgets: Analytics pack "
            "(crm-recruiter-dashboard, crm-dashboard-service) only if SR is "
            "dashboard-specific."
        ),
        "reduce": [
            "Ground the notes backend in knowledge packs so blank notes/activity screens can be fixed with confidence.",
            "Replace blank screens with a clear message: “you don’t have permission” vs “this failed to load — try again.”",
            "Show when the activity feed was last refreshed so recruiters know if data is stale.",
        ],
        "pack": "messaging (+ analytics if dashboard)",
    },
    "Search / lists / filters / export / AI Discovery": {
        "means": (
            "Candidate discovery + list membership + export: search/filter broken, "
            "lists empty, export issues, AI Discovery / sourcing from CRM."
        ),
        "knowledge": (
            "Messaging: lists crm-lists-ui / crm-candidate-lists (FilterService). "
            "AI Discovery / CRM search engines not found in cloned Messaging/"
            "Automations/Screening packs."
        ),
        "reduce": [
            "Keep list filters consistent everywhere, and explain why a search returned zero results instead of a blank list.",
            "Show export progress/status and document which columns come out — “export broke / wrong columns” is a top ask.",
            "Build a Search / AI Discovery knowledge pack before promising deeper product changes.",
        ],
        "pack": "messaging (lists) · Discovery gap",
    },
    "How-to / configuration / enablement question": {
        "means": (
            "Enablement gap more than defect — title-level how/what/can-we / "
            "enable-feature questions (title-only classifier)."
        ),
        "knowledge": (
            "Cross-cutting; map each how-to to Messaging/Automations/Screening "
            "docs once the topic is known."
        ),
        "reduce": [
            "Add short guided setups in the product for the most common “how do I…?” questions.",
            "Give CS ready-made answer macros mapped to these themes so how-to cases close without engineering.",
            "Where it is safe, let customers turn features on themselves instead of waiting for a ticket to enable them.",
        ],
        "pack": "cross-cutting",
    },
}


PRIORITY_ORDER = [
    "Candidate profile data / fields / tags / location / GDPR",
    "Screening / interview / scheduling / offer / notifications",
    "Campaigns / job alerts / subscriptions / spotlights",
    "Hiring status / pipeline / stages / lead status",
    "Email template content / hyperlinks / branding",
    "Email not sending / not receiving / spam / bounce",
]

# Product-area buckets for the HTML Playbook tab (order preserved).
AREA_ORDER = [
    "CRM Core",
    "CRM Profile",
    "CRM Messaging",
    "CRM Automations",
]

THEME_AREA: dict[str, str] = {
    # CRM Core — jobs, pipeline, access, events, residual/how-to
    "Hiring status / pipeline / stages / lead status": "CRM Core",
    "Jobs / requisitions / applications / posting": "CRM Core",
    "Forwarding / LinkedIn / ATS↔CRM sync": "CRM Core",
    "Access / CRM not opening / permissions": "CRM Core",
    "Events / university recruiting": "CRM Core",
    "How-to / configuration / enablement question": "CRM Core",
    "Unclassified / other": "CRM Core",
    # CRM Profile
    "Candidate profile data / fields / tags / location / GDPR": "CRM Profile",
    "Profile merge / unmerge / duplicates / disappeared": "CRM Profile",
    # CRM Messaging
    "Campaigns / job alerts / subscriptions / spotlights": "CRM Messaging",
    "Email template content / hyperlinks / branding": "CRM Messaging",
    "Email not sending / not receiving / spam / bounce": "CRM Messaging",
    "SMS / WhatsApp": "CRM Messaging",
    "Activity / notes / UI display": "CRM Messaging",
    "Search / lists / filters / export / AI Discovery": "CRM Messaging",
    # CRM Automations (+ screening/invite funnel often driven by recipes)
    "Automation not triggering / failing / wrongly triggered": "CRM Automations",
    "Screening / interview / scheduling / offer / notifications": "CRM Automations",
}

AREA_BLURB: dict[str, str] = {
    "CRM Core": (
        "Jobs, pipeline/status, access, events, ATS/LinkedIn sync, "
        "and residual/how-to tickets that sit on the CRM platform."
    ),
    "CRM Profile": (
        "Candidate record integrity — fields, tags, location, GDPR/purge, "
        "merge/duplicates, and disappeared profiles."
    ),
    "CRM Messaging": (
        "Outbound and channel messaging — campaigns, templates, email delivery, "
        "SMS/WhatsApp, notes/activity UI, and lists/search/export."
    ),
    "CRM Automations": (
        "Recipe reliability plus screening/interview/invite/notification flows "
        "that automations commonly drive."
    ),
}

