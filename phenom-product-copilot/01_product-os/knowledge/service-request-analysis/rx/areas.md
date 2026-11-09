# RX — product areas + remap rules

**PE label (Snowflake):** `Recruiter Experience (RX)` — confirm with `SELECT DISTINCT U_PRODUCT_EXPERIENCE` if unsure.

## Areas (full names only)

Names come **only** from `policies/jira-constants.md` (Product Experience : Product, parent `Recruiter Experience (RX)`). Which of them the SR Prevention tool shows lives in [`../scope.json`](../scope.json). This file holds routing rules only.

| Area (Jira product name) |
|------|
| CRM - Profile |
| CRM - Core |
| CRM - Messaging and Campaigns |
| CRM - Automation |
| CRM - Events and University Recruiting |
| Compliance |
| CRM - Role & Access Management |

## Suggested product-area remaps (locked)

| Signal | Suggested product area |
|--------|------------------------|
| Purge / retention / GDPR export / DSAR | Compliance |
| Role grants / permissions / access blockers | CRM - Role & Access Management |
| Data-storage consent, privacy opt-in / repermission, GDPR / CCPA consent | Compliance |
| Communication consent (email / SMS / WhatsApp) | CRM - Messaging and Campaigns |
| Suppression list add / remove / sync | CRM - Messaging and Campaigns |
| Else | Keep filing CRM area unless clearly misfiled |

Renamed 2026-10-04: `Platform - Privacy & Compliance` → `Compliance`, `Platform - Roles & Access Management` → `CRM - Role & Access Management` (Jira names). The full agent rulebook is [`../rulebook.md`](../rulebook.md).

Canonical type rules: [`../_shared/type-rules.md`](../_shared/type-rules.md).
