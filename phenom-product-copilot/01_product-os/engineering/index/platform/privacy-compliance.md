---
name: privacy-compliance
type: index
description: "Domain index for Platform → Privacy & Compliance repos"
pillar: Platform
last_reviewed: 2026-07-10
status: not yet onboarded
---

# Platform → Privacy & Compliance

## Scope

Consent, data retention, PII handling, audit logs, GDPR-type concerns. Any feature that stores, exposes, or processes candidate/recruiter personal data should be checked against this domain.

## Key repos

Partly onboarded (2026-10-21): `crm-gdpr` only. Other privacy repos are still in the rollout queue (see `index/taxonomy.md`).

| Repo | Purpose | Start here |
|------|---------|------------|
| `crm-gdpr` (branch `prod`) | GDPR requests (view, delete, update), tenant GDPR settings, recruiter emails, internal reports | `conf/routes`, `controllers/GDPRUiController.java`, `services/GdprServices.java` |

### Tenant GDPR settings (Settings → GDPR in CRM)

- Stored on the tenant's document in `candidates.TenantConfigurations`: `gdprEnabled`, `GDPRFromEmail`, `gdpr_emails[]`, `gdprReportDisabled`, `configureGdprTemplates`. Saved by `GdprServices.updateGDPRConfig`; any save while the tenant is not yet GDPR-enabled sends an internal crypto-enable alert (`sendCryptoEnableAlert`).
- `gdprReportDisabled = true` stops the two recruiter emails sent to `gdpr_emails` from `GDPRFromEmail` (fallback `gdpr@phenompeople.com`): **GDPR_Notification** (open view/delete/video-delete requests) and **GDPR_Confirmation** (processed requests). `Utill.getOnlyGdprReportRefNums`, `JobController.processingEmail` / `confirmationEmail`.
- The internal daily and weekly reports (`/gdpr/dailyReport`, `/gdpr/weeklyReport`) go to the Phenom GDPR admin list for every GDPR-enabled tenant and ignore this flag.
- Job schedules are external (called over HTTP); cadence is not in the repo.

## Common feasibility patterns

- "Can we store/retain this data, and for how long?" → retention policy config
- "Who can see this field/record?" → consent + access control model
- "Does this need a new consent flow?" → check existing consent capture patterns before assuming greenfield work

## Eng contacts

_Fill in once onboarded._
