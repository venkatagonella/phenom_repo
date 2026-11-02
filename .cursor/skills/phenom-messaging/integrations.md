# Messaging integrations cheat sheet

Companion to `phenom-knowledge/messaging/`. Vendors confirmed via
`MGWVendorNames` / webhook controllers in `messaging-gateway-service`.

## Channels

| Channel | Constant / surface |
|---|---|
| SMS | `sms` |
| WhatsApp | `whatsapp` |
| Email | `email` |
| Voice | `voice-call` |
| In-app (CRM bell) | `candidates-notifications` (legacy Play; also see Engineering messaging index) |

## External vendors (MGW)

| Vendor | Key | Typical use |
|---|---|---|
| SendGrid | `sendgrid` | Email send + delivery/reply webhooks |
| AWS SES | `ses` | Email (also storm-campaign `AWSService`) |
| Twilio | `twilio` | SMS, WhatsApp, voice, number provisioning |
| Gupshup | `gupshup` | WhatsApp templates + webhooks |
| ADNOC | `adnoc` | Regional messaging webhooks/replies |
| IMI | `imi` | SMS webhooks |

## Internal callers of messaging APIs

| Caller | Uses messaging for |
|---|---|
| Candidate Engagement / `storm-campaign` | Campaign email/SMS execution |
| CRM Automations | `SEND_EMAIL` / `SEND_SMS` / `SEND_WHATSAPP` / campaign opt actions |
| Recruiter Hub / HRM | HM forward, interview feedback emails; HRM SMS |
| CRM UI MFEs | Campaigns, templates, lists, inbox, notes |
| Bots | Bot email / bot SMS keyword paths (legacy SMS services) |

## Dual stack note

Modern: `crm-messaging-platform` (+ UI MFEs above).  
Legacy still indexed under Engineering: `candidates_email_microservice`,
`candidates-sms-services`, `candidates-notifications`.  
Confirm with Messaging which path is authoritative per tenant/channel.
