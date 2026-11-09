---
name: messaging
type: index
description: "Domain index for Platform → Messaging repos — notifications/communication platform"
pillar: Platform
last_reviewed: 2026-07-12
status: onboarded (fully manifested)
---

# Platform → Messaging

## Scope

Email, SMS, and in-app notifications to candidates and users: templates, delivery, personalization, localization. Any feature that sends a communication should route through here.

## Repo manifests

**Use [`index/repos/messaging/capability-index.md`](../repos/messaging/capability-index.md) before grepping `repos/platform/messaging/`.** All 4 cloned repos have a curated manifest under `index/repos/messaging/` — purpose, capabilities, entry points, integrations, and search hints per repo. Two parallel stacks exist for email/SMS (legacy Play services vs. the newer `crm-messaging-platform` monorepo) — the capability index flags this; confirm which is authoritative with the Messaging team before giving a definitive answer.

## Key repos

See `index/repo-catalog.md` for full stack/status/"also used by" detail.

| Repo | Purpose | Start here |
|------|---------|------------|
| `candidates_email_microservice` | Legacy universal email send/trigger microservice — bot emails, HM-forward emails, career alerts, calendar invites (also embeds legacy SMS + campaign-job migration controllers) | `app/controllers/UniversalEmailController.java`, `EmailTriggerController.java` |
| `candidates-sms-services` | Primary SMS/WhatsApp delivery service for candidates — SMS config, number provisioning, WhatsApp, bot SMS campaigns, HRM integrations | `app/controllers/SMSController.java`, `WhatsAppController.java` |
| `crm-messaging-platform` | Modern multi-module messaging monorepo (20+ modules) — email API/facade/analytics, multi-vendor SMS/voice gateway + phenom inbox, transactional email, campaign-execution modules | `email-api-service/`, `email-facade-service/`, `messaging-gateway-service/` |
| `candidates-notifications` | In-app/recruiter notification service — notification feed, task spotlight, "follow candidate" alerts | `app/controllers/NotificationController.java` |

Note: `crm-messaging-platform` also contains `recruiter-campaign-service`, `sms-campaign-service`, and `system-campaign-service` modules that are campaign-**execution** (not definition/segmentation) flavored — see Candidate Engagement's domain file (`index/product-experiences/candidate-engagement.md`) and "Also used by" in `repo-catalog.md`.

## Common feasibility patterns

- "Can we send an SMS/email when X happens?" → template + delivery channel check; also check `crm-automation-service` (Platform → Automations) for an existing trigger/action before assuming new plumbing
- "Can we personalize this notification with Y data?" → check template variable/merge-field support
- "Why didn't a message get delivered?" → check suppression list / opt-in status (`crm-messaging-platform` `email-facade-service`/`email-analytics-service`, `candidates-sms-services` `PublicApiController`) before assuming a send-path bug

## Platform dependencies

- **Candidate Engagement** — campaign definition/audience/scheduling triggers sends here (see naming-overlap note above)
- **Automations** — send-email/send-sms/notification automation actions call into these repos
- **Recruiter Hub** — HRM forward/HM email orchestration in `hrm-profile-*` / `hrm-jobs-api` (delivery still Messaging); in-app notification surface mounted in CRM shell (`inbox` MFE)

## Eng contacts

_Fill in once known._
