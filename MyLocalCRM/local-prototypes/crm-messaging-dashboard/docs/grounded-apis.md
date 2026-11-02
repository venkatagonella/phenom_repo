# Grounded APIs — crm-messaging-dashboard local prototype

Maps this local UI/stub to real Phenom Messaging code.
Knowledge pack: `/Users/venkata.gonella/phenom_repo/phenom-knowledge/messaging/`
Skill: `phenom-messaging`

## UI pattern

| Local | Source |
|---|---|
| `prototypes/messaging-dashboard.html` | Visual chrome from `DesignSystem/templates/html/jobs-dashboard.html` + `styles/jobs-dashboard.css` |
| PDS tokens | Symlink → `DesignSystem/styles/pds-tokens.css` |

## Repo shape (mirrors `crm-inbox-fe`)

| Local path | Real Phenom counterpart |
|---|---|
| `webpack.config.js` exposes `./inbox` | `crm-inbox-fe/webpack.config.js` → `./inbox` |
| `src/app/inbox/inbox.module.ts` | `crm-inbox-fe/src/app/inbox/` |
| `src/app/inbox/inbox-page/` | `inbox-page.component.ts` |
| `src/app/inbox/services/inbox.service.ts` | `inbox/services/inbox.service.ts` |
| `src/app/core/service/messaging-api.constants.ts` | path strings from InboxService + routing.yaml |

## Backend calls (verified in clones)

| Capability | Method / path | Repo |
|---|---|---|
| List conversations | `POST messaging-gateway-service/v1.0/inbox/getConversations` | `crm-inbox-fe` InboxService → `crm-messaging-platform` messaging-gateway-service InboxController |
| Chat history | `POST .../v1.0/inbox/getCandidateChat` | same |
| Unread count | `POST .../v1.0/inbox/totalUnreadCount` | same |
| Read/unread | `POST .../v1.0/inbox/changeReadConversationStatus` | same |
| Archive | `POST .../v1.0/inbox/changeArchiveConversationStatus` | same |
| Search | `POST email-facade-service/v1.0/inbox/search` | email-facade-service |

## Vendors shown in prototype columns

From `MGWVendorNames` / gateway webhooks: Twilio, Gupshup, SendGrid (+ SES, ADNOC, IMI in platform).

## Related MFEs (nav targets, not cloned into this prototype)

- `crm-campaigns-ui` — Campaigns
- `crm-templates-ui` — Templates
- `crm-lists-ui` — Lists
- `crm-notes-ui` — Notes

## Unverified

Gateway prefixes `/sms-service/`, `/messaging-campaign-service/`, `/ecampaign/` → exact platform module mapping is gateway config (see phenom-knowledge messaging skill caveats).
