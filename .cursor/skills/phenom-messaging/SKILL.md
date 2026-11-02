---
name: phenom-messaging
description: >-
  Code-grounded navigation for Phenom Messaging (email, SMS, WhatsApp, voice,
  campaigns, templates, lists, inbox, notes). Use when building or designing
  messaging features, tracing send/delivery paths, finding controllers/methods,
  checking vendor integrations (SendGrid, SES, Twilio, Gupshup, ADNOC, IMI), or
  when the user mentions messaging APIs, MGW, phenom inbox, campaigns, or
  candidate outreach channels.
---

# Phenom Messaging — Agent Reference

Personal skill that loads the grounded Messaging knowledge pack so any agent can
jump to the right **repo → module → controller/method** before designing or
building new functionality.

## Source of truth (read in this order)

| Priority | Path | Use for |
|---|---|---|
| 1 | `/Users/venkata.gonella/phenom-master-copilot/phenom-knowledge/messaging/skill.md` | Scope, grounding contract, capability catalog, lifecycles |
| 2 | `/Users/venkata.gonella/phenom-master-copilot/phenom-knowledge/messaging/routing.yaml` | Intent → `repo/path:line` (methods, controllers, UI services) |
| 3 | `/Users/venkata.gonella/phenom-master-copilot/phenom-knowledge/messaging/graph.json` | Cross-repo call graph (UI → platform → providers) |
| 4 | This skill’s [integrations.md](integrations.md) | Vendor + internal caller cheat sheet |
| 5 | `/Users/venkata.gonella/phenom-master-copilot/Phenom - Engineering/index/repos/messaging/capability-index.md` | Dual-stack feasibility (legacy vs modern) |

**Clone root for source:**  
`/Users/venkata.gonella/phenom_repo/MyLocalCRM/repos/<repo>`

## Workflow (required)

1. Read `phenom-knowledge/messaging/skill.md` (grounding contract first).
2. Match the user’s intent in `routing.yaml` → `intents:` and open the cited `at:` path under the clone root.
3. If the flow spans UI → backend → vendor, traverse `graph.json` edges.
4. **Cite `repo/path:line`.** If it isn’t in the cloned Messaging repos, say **"not found in cloned Messaging repos"** — do not invent APIs.
5. Prefer existing send/template/opt-out paths over new parallel plumbing. Confirm with Messaging which stack is live for the tenant/channel (legacy Play vs `crm-messaging-platform`).

## Quick capability → start here

| Need | Start at (verify line in clone) |
|---|---|
| Candidate email send | `crm-messaging-platform/.../email-api-service/.../CandidateController.java` |
| Transactional email | `.../txn-email-service/.../TxnEmailServiceRestController.java` |
| Email templates / schedule / suppression | `.../email-facade-service/.../TemplateController`, `EmailSchedulerRestController`, `SuppressionListController` |
| SMS send / opt-in | `.../text-api-service/.../SMSController`, `OptInController` |
| Inbox / conversations | `.../messaging-gateway-service/.../phenomInbox/InboxController` + UI `crm-inbox-fe/.../inbox.service.ts` |
| WhatsApp | UI `crm-inbox-fe/.../whatsapp-management.service.ts`; webhooks `GupshupWebhookController`, `TwilioWebhookController` |
| Voice | `.../phenomInbox/VoiceCallController` + UI `twilio-voice.service.ts` |
| Campaign authoring | UI `crm-campaigns-ui` campaign-page; facade `CampaignController` |
| Campaign execution | `storm-campaign` topologies + `CampaignServices` |
| Lists / talent communities | UI `crm-lists-ui`; backend `crm-candidate-lists` |
| Delivery analytics / unsubscribe | `email-analytics-service` `SendgridWebhookController`, `OneClickUnsubscribeWebhookController` |

## Hard rules

1. Answer from code under the clone root; cite paths.
2. Do not assert gateway-prefix → module mapping for `/ecampaign/`, `/sms-service/`, `/messaging-campaign-service/` unless verified — UI calls are known; exact module may be gateway config.
3. Campaign **definition/segmentation** vs **send execution** are different repos — see Candidate Engagement / `storm-campaign` notes in the pack.
4. Automations actions `SEND_EMAIL` / `SEND_SMS` / `SEND_WHATSAPP` land here — check `phenom-knowledge/automations/` when the feature is trigger-driven.
5. Never edit live engineering clones under `MyLocalCRM/repos/` or `Phenom - Engineering/repos/` from a research/reference workflow unless the user explicitly opens that product repo to implement.

## How to invoke from another agent / chat

- Say: **“use phenom-messaging”** or **“load Phenom Messaging knowledge”**
- Or ask a capability question (send SMS, inbox, campaign drip, SendGrid webhook) — this skill should auto-apply from the description.
- For any Phenom area (not only Messaging), use the companion skill **phenom-knowledge**.
