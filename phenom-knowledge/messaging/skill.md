# Skill: Phenom CRM Messaging

> **Area:** Messaging — Email, SMS, WhatsApp, Voice, Campaigns, Templates, Lists,
> Talent Communities, Inbox/Conversations, Notes.
> **Companion files:** `routing.yaml`, `graph.json`. **Framework/contract:** `../INDEX.md`.

---

## GROUNDING CONTRACT (read first)
1. Answer only from code; cite `repo/path:line` from `routing.yaml`/`graph.json`.
2. If a fact isn't in the cloned Messaging repos, say **"not found in cloned Messaging repos"** — don't guess.
3. Multiple matches → list all repo-area paths.
4. Respect provenance: `verified` (read this session) vs `report` (sub-agent pass; re-open to confirm exact line).
5. **API-gateway prefix → backend-module mapping is NOT verified** (it's gateway config). When a UI calls `/ecampaign/*`, `/sms-service/*`, or `/messaging-campaign-service/*`, say which UI method it is (verified) but flag the exact backend module as unconfirmed unless the prefix is one of the verified ones (`/messaging-gateway-service/`, `/email-facade-service/`, `/email-analytics-service/`, `/lists/`, `/voice-call-service/`).

---

## WHAT THIS AREA IS
The Messaging area covers how recruiters communicate with candidates and manage audiences:
send **email / SMS / WhatsApp / voice**, build & run **campaigns** (one-off, drip,
autoresponder/subscription), author **templates**, manage **lists / talent communities**,
work the unified **inbox**, and keep **notes**.

### Repos
| Repo | Layer | Job |
|---|---|---|
| `crm-campaigns-ui` | UI (MFE) | Email/SMS/WhatsApp campaign builder, subscriptions |
| `crm-templates-ui` | UI (MFE) | Email + SMS template editor/library |
| `crm-lists-ui` | UI (MFE) | Lists (static/dynamic) + talent communities |
| `crm-inbox-fe` | UI (MFE) | Inbox/conversations, WhatsApp campaigns, Twilio voice, "messaging everywhere" |
| `crm-notes-ui` | UI (MFE) | Candidate notes |
| `crm-messaging-platform` | Backend (multi-module) | Gateway (MGW), email facade/api, email analytics/webhooks, text(SMS) api, campaign services, txn email, ops |
| `crm-candidate-lists` | Backend (Play) | List CRUD/membership/targeting, opt-in/out |
| `storm-campaign` | Backend (Storm) | Campaign execution: schedule & send touches (drip/bulk/autoresponder) |

### `crm-messaging-platform` modules (backend map)
`messaging-gateway-service` (24 controllers — inbox, Twilio/Gupshup/IMI/SendGrid webhooks, voice, templates, analytics),
`email-facade-service` (8 — inbox, scheduler, templates, campaigns, suppression),
`email-api-service` (candidate/transactional email send), `txn-email-service` (transactional email),
`email-analytics-service` (SendGrid webhook events, one-click unsubscribe, reply tracking),
`text-api-service` (SMS send, opt-in, validation), `system-campaign-service` (system campaigns, status, dry-run count),
`recruiter-campaign-service`, `sms-campaign-service`, `ops-api-service`.

---

## LIFECYCLE: how a campaign sends
1. **Author** — `crm-campaigns-ui` campaign builder (`campaign-page.component.ts:63`) saves via
   `EmailManagementService` (`/ecampaign/*`) or WhatsApp via `whatsapp-management.service.ts`.
2. **Persist/config** — backend campaign controllers (`email-facade-service CampaignController:46`,
   `system-campaign-service CampaignsController:44`) store campaign + occurrences (Mongo `Campaigns`).
3. **Schedule/execute** — `storm-campaign` topologies consume Kafka campaign topics and run bolts:
   schedule bolts (`*ScheduleBolt`) → batch bolts (`CrmCampaignBatchWiseProcessingBolt:127`) →
   processing bolts (`RecruiterCampaignProcessingBolt:102`) that actually send.
4. **Send** — via providers: SendGrid (`SendEmailServices.java:183`), AWS SES
   (`AWSService.java:424`), MGW, or SMS REST (`CampaignServices.java:6863`).
5. **Track** — delivery events (open/click/bounce/spam) ingested by `storm-campaign`
   `CampaignEventsProcessorBolt:81` and platform `email-analytics-service SendgridWebhookController:38`.

## LIFECYCLE: how the inbox works
Inbound SMS/WhatsApp/email arrives at platform webhooks (`TwilioWebhookController:42`,
`GupshupWebhookController:40`, `IMISMSWebhookController:41`, `SendGridWebhookController:29`) →
stored → surfaced via `messaging-gateway-service InboxController` → UI `crm-inbox-fe`
(`inbox.service.ts:26` `/messaging-gateway-service/v1.0/inbox/getConversations`).

---

## CAPABILITY CATALOG (see routing.yaml `intents` for exact targets)
- **Email send** → platform `email-api-service CandidateController:78`, `txn-email-service TxnEmailServiceRestController:77`.
- **SMS send** → platform `text-api-service SMSController:60`; UI `sms.service.ts:104`; execution `storm-campaign CampaignServices.java:6627`.
- **WhatsApp** → UI `whatsapp-management.service.ts:44`; providers Gupshup/Twilio webhooks.
- **Voice** → platform `VoiceCallController:22`; UI `twilio-voice.service.ts:544`.
- **Campaigns** → UI `campaign-page.component.ts:63`; backend `CampaignController:46`/`CampaignsController:44`; execution `storm-campaign` topologies.
- **Templates** → UI `crm-templates-ui template-page.component.ts:50`; backend `email-facade-service TemplateController`.
- **Lists / talent communities** → UI `crm-lists-ui list.service.ts`; backend `crm-candidate-lists` FilterService (13 controllers).
- **Opt-in/out / unsubscribe / suppression** → platform `OneClickUnsubscribeWebhookController:32`, `SuppressionListController`, `OptInController:50`; `crm-candidate-lists PublicApiService`.
- **Delivery events / analytics** → platform `SendgridWebhookController:38`; `storm-campaign CampaignEventsProcessorBolt:81`.
- **Notes** → UI `crm-notes-ui notes-service.ts` → `/notes-api/*` (backend `notes-api` NOT cloned).

## PROVIDERS
Email: SendGrid, AWS SES v2, MGW. SMS: Twilio, IMI Mobile, internal SMS REST.
WhatsApp: Gupshup, Twilio. Voice: Twilio.

---

## CROSS-AREA
- **Automations → Messaging**: automation actions `SEND_EMAIL`/`SEND_SMS`/`SEND_WHATSAPP`/`ADD_TO_CAMPAIGN`/`CAMPAIGN_OPT_OUT` execute here (see `../automations`).
- **Messaging → Scheduling**: UIs call `/scheduling-api-gateway/*` (Scheduling area, not cloned).

## KNOWN GAPS / CAVEATS
- **`notes-api` backend not cloned** — notes UI endpoints are known, backend impl is not grounded.
- **`/ecampaign/`, `/sms-service/`, `/messaging-campaign-service/` prefix → module mapping unverified.** The UI calls are verified; the exact backend module behind these gateway prefixes is not confirmed from code. Do not assert it.
- **Topic names are mostly property-bound** in `storm-campaign` (e.g. `recruiter.campaigns.topic`); only some have literal fallbacks. Don't state a literal unless it's the fallback shown in `routing.yaml`.
- **crm-campaigns-ui / crm-templates-ui source is on the `development` branch** (default branch empty) — note this if regenerating.
- Controller **base paths are constant references** (e.g. `WARestConstants.MGW`); resolve the constant for the literal URL before quoting a full path.
