# Snapshot — structured key areas (from local CSV export)

**Source CSV:** `data/All Servicenow service requests from 2026-01-01 - Sheet1.csv`  
**Linked as:** `data/all-service-requests.csv`  
**Computed:** 2026-09-23 from sheet export only (no other sources).

## Population

| Metric | Value |
|--------|-------|
| Rows | 29,216 |
| Distinct `CASE_NUMBER` | 29,135 |
| Multi-row cases | 80 (81 extra rows) |
| `CREATED_ON_UTC` span | 2026-01-01 → 2026-09-23 |

### Rows by month (`CREATED_ON_UTC`)

| Month | Rows |
|-------|------|
| 2026-01 | 3,140 |
| 2026-02 | 3,125 |
| 2026-03 | 2,736 |
| 2026-04 | 3,047 |
| 2026-05 | 3,657 |
| 2026-06 | 3,595 |
| 2026-07 | 3,453 |
| 2026-08 | 3,830 |
| 2026-09 | 2,633 (partial month through 2026-09-23) |

## Key area 1 — `PRODUCT_EXPERIENCE` (all rows)

| PRODUCT_EXPERIENCE | Rows | Share |
|--------------------|------|-------|
| Integration Experience (IX) | 9,783 | 33.49% |
| Recruiter Experience (RX) | 4,399 | 15.06% |
| Candidate Experience (CX) | 3,324 | 11.38% |
| Hiring Intelligence | 2,552 | 8.73% |
| Employee Onboarding Experience | 2,422 | 8.29% |
| Phenomenal Tools | 1,985 | 6.79% |
| Analytics | 1,052 | 3.60% |
| Employee Experience (EX) | 1,035 | 3.54% |
| miscellaneous | 782 | 2.68% |
| Manager Experience (MX) | 771 | 2.64% |
| Search & Personalization | 335 | 1.15% |
| Other Products | 184 | 0.63% |
| (blank) | 168 | 0.58% |
| Data | 145 | 0.50% |
| Talent Management | 135 | 0.46% |
| Hiring Automations | 67 | 0.23% |
| Z - Ops Engineering (Not a Product) | 41 | 0.14% |
| Automation Engine | 18 | 0.06% |
| Customer Enablement [Not a Product] | 10 | 0.03% |
| Z - Agents Experience (Don’t use) | 4 | 0.01% |
| Candidates Experiences (CX) | 3 | 0.01% |
| HRIT Experience | 1 | 0.00% |

## Key area 2 — `PRODUCT_EXPERIENCE_PRODUCT`

- **Blank on 22,444 rows (76.82%)** — finer product is usually absent unless Jira linkage resolves a product field.
- Non-blank: **6,772 rows (23.18%)**.

### Top non-blank products (share of labeled / of all)

| PRODUCT_EXPERIENCE_PRODUCT | Labeled | % of labeled | % of all rows |
|----------------------------|---------|--------------|---------------|
| CRM - Core | 619 | 9.1% | 2.12% |
| CRM - Profile | 559 | 8.3% | 1.91% |
| FSI - Job Synch | 511 | 7.5% | 1.75% |
| CRM - Messaging and Campaigns | 510 | 7.5% | 1.75% |
| FS Forms - Life Cycle Mgmt | 508 | 7.5% | 1.74% |
| CMS | 423 | 6.2% | 1.45% |
| OnboardingX - Core | 401 | 5.9% | 1.37% |
| Career Site – Platform Services | 388 | 5.7% | 1.33% |
| Customer Analytics | 279 | 4.1% | 0.95% |
| Internal Mobility | 274 | 4.0% | 0.94% |
| MX - Hiring | 267 | 3.9% | 0.91% |
| Hiring Status | 235 | 3.5% | 0.80% |
| CRM - Automation | 185 | 2.7% | 0.63% |
| FS Integrations - Data Integration | 145 | 2.1% | 0.50% |
| CRM - Events and University Recruiting | 142 | 2.1% | 0.49% |

### Top PE × product combos (both non-blank)

| Rows | PRODUCT_EXPERIENCE | PRODUCT_EXPERIENCE_PRODUCT |
|------|--------------------|----------------------------|
| 500 | Recruiter Experience (RX) | CRM - Core |
| 478 | Integration Experience (IX) | FSI - Job Synch |
| 459 | Recruiter Experience (RX) | CRM - Messaging and Campaigns |
| 455 | Recruiter Experience (RX) | CRM - Profile |
| 438 | Integration Experience (IX) | FS Forms - Life Cycle Mgmt |
| 406 | Candidate Experience (CX) | CMS |
| 382 | Employee Onboarding Experience | OnboardingX - Core |
| 347 | Candidate Experience (CX) | Career Site – Platform Services |
| 270 | Analytics | Customer Analytics |
| 227 | Employee Experience (EX) | Internal Mobility |

## Status / Jira (context, not themes)

| Field | Notable values |
|-------|----------------|
| STATUS | Closed 23,263 (79.62%); Closed Auto Resolved 4,819 (16.49%); open-ish remainder &lt;4% |
| JIRA_CREATED | No 70.88%; Yes 28.70%; Linked - key not found 0.42% |
| SUB_STATUS Spam | 215 (0.74%) |
| SUB_STATUS Potential Future Enhancement | 2 |
| STATUS Product Request Review | 6 |

## Roadmap framing (sheet-only)

This snapshot is **volume of service requests by labeled areas**, not a committed product roadmap. Free-text theme mining of `SHORT_DESCRIPTION`/`DESCRIPTION` is not included here — run a separate filtered pass when asked.
