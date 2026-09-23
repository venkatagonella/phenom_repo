# Detailed breakup — Jira-created service requests (sheet only)

## Scope and limits (no hallucination)

- **Filter:** `JIRA_CREATED` = `Yes`
- **Rows:** 8,384
- **Source:** local CSV export of spreadsheet `1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8` only
- **Product areas:** taken from sheet columns `PRODUCT_EXPERIENCE` and `PRODUCT_EXPERIENCE_PRODUCT` (not inferred from free text)
- **Customer wording:** taken from `SHORT_DESCRIPTION` (SR title) and `DESCRIPTION` (SR body)
- **Comments:** **not available** — the sheet has no comments / work-notes column. Nothing below claims to use comments.
- **Keyword %:** share of these Jira-Yes rows where the title and/or description contains that token/phrase at least once

---

## 1. Product areas on the SR (sheet columns)

### 1a. `PRODUCT_EXPERIENCE`

| PRODUCT_EXPERIENCE | Rows | % of Jira-Yes |
|--------------------|------|---------------|
| Recruiter Experience (RX) | 1,949 | 23.25% |
| Integration Experience (IX) | 1,500 | 17.89% |
| Candidate Experience (CX) | 1,066 | 12.71% |
| Employee Onboarding Experience | 957 | 11.41% |
| Hiring Intelligence | 949 | 11.32% |
| Employee Experience (EX) | 549 | 6.55% |
| Manager Experience (MX) | 373 | 4.45% |
| Analytics | 300 | 3.58% |
| Search & Personalization | 201 | 2.40% |
| Phenomenal Tools | 152 | 1.81% |
| Talent Management | 108 | 1.29% |
| Data | 108 | 1.29% |
| Other Products | 66 | 0.79% |
| Hiring Automations | 51 | 0.61% |
| Z - Ops Engineering (Not a Product) | 22 | 0.26% |
| Automation Engine | 16 | 0.19% |
| (blank) | 7 | 0.08% |
| miscellaneous | 5 | 0.06% |
| Z - Agents Experience (Don’t use) | 4 | 0.05% |
| Customer Enablement [Not a Product] | 1 | 0.01% |

### 1b. `PRODUCT_EXPERIENCE_PRODUCT`

| PRODUCT_EXPERIENCE_PRODUCT | Rows | % of Jira-Yes |
|---------------------------|------|---------------|
| (blank) | 1,612 | 19.23% |
| CRM - Core | 619 | 7.38% |
| CRM - Profile | 559 | 6.67% |
| FSI - Job Synch | 511 | 6.09% |
| CRM - Messaging and Campaigns | 510 | 6.08% |
| FS Forms - Life Cycle Mgmt | 508 | 6.06% |
| CMS | 423 | 5.05% |
| OnboardingX - Core | 401 | 4.78% |
| Career Site – Platform Services | 388 | 4.63% |
| Customer Analytics | 279 | 3.33% |
| Internal Mobility | 274 | 3.27% |
| MX - Hiring | 267 | 3.18% |
| Hiring Status | 235 | 2.80% |
| CRM - Automation | 185 | 2.21% |
| FS Integrations - Data Integration | 145 | 1.73% |
| CRM - Events and University Recruiting | 142 | 1.69% |
| Req & Offer | 130 | 1.55% |
| Career Site – Templates & Views | 121 | 1.44% |
| User Management | 101 | 1.20% |
| EX Platform (Other) | 94 | 1.12% |
| Chatbot | 90 | 1.07% |
| TDP | 67 | 0.80% |
| Default Configuration Scheme for Software Requirements | 58 | 0.69% |
| Search | 54 | 0.64% |
| FS Integrations - App Integration | 52 | 0.62% |
| Referrals | 45 | 0.54% |
| RX - Search | 44 | 0.52% |
| Projects/Gigs | 43 | 0.51% |
| Learning | 42 | 0.50% |
| Job Distribution | 37 | 0.44% |
| HVH - Core | 31 | 0.37% |
| FS Forms - Core Platform | 26 | 0.31% |
| Career Pathing | 24 | 0.29% |
| Mentoring | 20 | 0.24% |
| HVH - Assessments | 19 | 0.23% |
| Ops Engineering(DevOps/CloudOps) | 18 | 0.21% |
| FS Forms - Forms/Apps | 16 | 0.19% |
| Recruiter Experience (RX) | 14 | 0.17% |
| APM | 14 | 0.17% |
| Cross Team Dependency | 13 | 0.16% |
| Automation Engine - Core | 13 | 0.16% |
| Universal Graph | 11 | 0.13% |
| Phenom X+ | 11 | 0.13% |
| Compliance | 11 | 0.13% |
| Integration Experience (IX) | 10 | 0.12% |
| Direct Sourcing | 9 | 0.11% |
| Resume Parser | 8 | 0.10% |
| Employee Onboarding Experience | 8 | 0.10% |
| Video Hub | 7 | 0.08% |
| Employee Experience (EX) | 7 | 0.08% |
| Alumni | 7 | 0.08% |
| Other Products | 6 | 0.07% |
| CRM - Mobile | 6 | 0.07% |
| Candidate Experience (CX) | 5 | 0.06% |
| PX | 5 | 0.06% |
| Manager Experience (MX) | 4 | 0.05% |
| DNA Services | 4 | 0.05% |
| CRM - Google Chrome Extension | 3 | 0.04% |
| ETG | 3 | 0.04% |
| FS Integrations - Life Cycle Mgmt | 3 | 0.04% |
| People Manager | 2 | 0.02% |
| TXE | 2 | 0.02% |
| Default Configuration Scheme for Prospect Client | 2 | 0.02% |
| DEC | 1 | 0.01% |
| Employee Feed | 1 | 0.01% |
| PUP | 1 | 0.01% |
| QA Hub | 1 | 0.01% |
| HRIT - Core | 1 | 0.01% |
| High Volume Hiring (HVH) | 1 | 0.01% |

### 1c. Top PE × product combinations

| PRODUCT_EXPERIENCE | PRODUCT_EXPERIENCE_PRODUCT | Rows | % |
|--------------------|---------------------------|------|---|
| Hiring Intelligence | (blank) | 810 | 9.66% |
| Employee Onboarding Experience | (blank) | 551 | 6.57% |
| Recruiter Experience (RX) | CRM - Core | 500 | 5.96% |
| Integration Experience (IX) | FSI - Job Synch | 478 | 5.70% |
| Recruiter Experience (RX) | CRM - Messaging and Campaigns | 459 | 5.47% |
| Recruiter Experience (RX) | CRM - Profile | 455 | 5.43% |
| Integration Experience (IX) | FS Forms - Life Cycle Mgmt | 438 | 5.22% |
| Candidate Experience (CX) | CMS | 406 | 4.84% |
| Employee Onboarding Experience | OnboardingX - Core | 382 | 4.56% |
| Candidate Experience (CX) | Career Site – Platform Services | 347 | 4.14% |
| Analytics | Customer Analytics | 270 | 3.22% |
| Employee Experience (EX) | Internal Mobility | 227 | 2.71% |
| Integration Experience (IX) | Hiring Status | 205 | 2.45% |
| Manager Experience (MX) | MX - Hiring | 196 | 2.34% |
| Recruiter Experience (RX) | CRM - Automation | 166 | 1.98% |
| Recruiter Experience (RX) | CRM - Events and University Recruiting | 132 | 1.57% |
| Integration Experience (IX) | FS Integrations - Data Integration | 128 | 1.53% |
| Manager Experience (MX) | Req & Offer | 112 | 1.34% |
| Candidate Experience (CX) | Career Site – Templates & Views | 105 | 1.25% |
| Phenomenal Tools | User Management | 94 | 1.12% |
| Candidate Experience (CX) | Chatbot | 75 | 0.89% |
| Talent Management | (blank) | 73 | 0.87% |
| Employee Experience (EX) | EX Platform (Other) | 69 | 0.82% |
| Data | TDP | 59 | 0.70% |
| Recruiter Experience (RX) | (blank) | 53 | 0.63% |
| Search & Personalization | Default Configuration Scheme for Software Requirements | 50 | 0.60% |
| Integration Experience (IX) | FS Integrations - App Integration | 45 | 0.54% |
| Employee Experience (EX) | Referrals | 44 | 0.52% |
| Search & Personalization | Search | 38 | 0.45% |
| Employee Experience (EX) | Learning | 36 | 0.43% |
| Integration Experience (IX) | (blank) | 35 | 0.42% |
| Hiring Intelligence | MX - Hiring | 35 | 0.42% |
| Integration Experience (IX) | CRM - Profile | 35 | 0.42% |
| Employee Experience (EX) | Projects/Gigs | 33 | 0.39% |
| Candidate Experience (CX) | FS Forms - Life Cycle Mgmt | 33 | 0.39% |
| Search & Personalization | RX - Search | 32 | 0.38% |
| Other Products | Job Distribution | 32 | 0.38% |
| Hiring Intelligence | CRM - Core | 31 | 0.37% |
| Integration Experience (IX) | CRM - Core | 27 | 0.32% |
| Data | CRM - Profile | 27 | 0.32% |

---

## 2. Keywords in SR title (`SHORT_DESCRIPTION`)

| Keyword | SRs with keyword in title | % of Jira-Yes |
|---------|---------------------------|---------------|
| candidate | 907 | 10.82% |
| job | 733 | 8.74% |
| phenom | 595 | 7.10% |
| email | 416 | 4.96% |
| crm | 366 | 4.37% |
| candidates | 346 | 4.13% |
| interview | 344 | 4.10% |
| status | 333 | 3.97% |
| missing | 291 | 3.47% |
| site | 288 | 3.44% |
| hiring | 274 | 3.27% |
| profile | 270 | 3.22% |
| update | 268 | 3.20% |
| career | 264 | 3.15% |
| jobs | 243 | 2.90% |
| showing | 241 | 2.87% |
| page | 237 | 2.83% |
| application | 229 | 2.73% |
| apply | 219 | 2.61% |
| data | 218 | 2.60% |
| internal | 214 | 2.55% |
| report | 211 | 2.52% |
| error | 193 | 2.30% |
| scheduling | 190 | 2.27% |
| employee | 180 | 2.15% |
| recruiter | 166 | 1.98% |
| change | 163 | 1.94% |
| external | 161 | 1.92% |
| manager | 151 | 1.80% |
| add | 143 | 1.71% |
| incorrect | 139 | 1.66% |
| automation | 139 | 1.66% |
| screening | 134 | 1.60% |
| emails | 134 | 1.60% |
| workday | 131 | 1.56% |
| access | 130 | 1.55% |
| tydy | 128 | 1.53% |
| form | 126 | 1.50% |
| event | 122 | 1.46% |
| link | 122 | 1.46% |
| onboarding | 120 | 1.43% |
| offer | 120 | 1.43% |
| search | 119 | 1.42% |
| field | 117 | 1.40% |
| staging | 115 | 1.37% |
| remove | 114 | 1.36% |
| integration | 113 | 1.35% |
| calendar | 110 | 1.31% |
| location | 110 | 1.31% |
| widget | 108 | 1.29% |
| req | 108 | 1.29% |
| template | 104 | 1.24% |
| visible | 102 | 1.22% |
| requisition | 101 | 1.20% |
| text | 98 | 1.17% |
| user | 98 | 1.17% |
| re-push | 97 | 1.16% |
| templates | 95 | 1.13% |
| cannot | 95 | 1.13% |
| referral | 94 | 1.12% |
| profiles | 93 | 1.11% |
| name | 92 | 1.10% |
| required | 91 | 1.09% |
| ats | 88 | 1.05% |
| interviews | 86 | 1.03% |
| sent | 85 | 1.01% |
| prof | 85 | 1.01% |
| available | 84 | 1.00% |
| updated | 81 | 0.97% |
| questions | 81 | 0.97% |
| time | 81 | 0.97% |
| fields | 81 | 0.97% |
| posting | 80 | 0.95% |
| upload | 78 | 0.93% |
| campaign | 78 | 0.93% |
| careers | 77 | 0.92% |
| prod | 76 | 0.91% |
| list | 76 | 0.91% |
| evaluation | 75 | 0.89% |
| ind | 75 | 0.89% |
| filter | 74 | 0.88% |
| invite | 74 | 0.88% |
| question | 74 | 0.88% |
| sms | 73 | 0.87% |
| applications | 73 | 0.87% |
| receiving | 73 | 0.87% |
| resume | 72 | 0.86% |
| source | 71 | 0.85% |
| date | 71 | 0.85% |
| production | 71 | 0.85% |
| multiple | 70 | 0.83% |
| button | 69 | 0.82% |
| section | 67 | 0.80% |
| analytics | 67 | 0.80% |
| reflecting | 67 | 0.80% |
| view | 66 | 0.79% |
| role | 66 | 0.79% |
| option | 65 | 0.78% |
| test | 65 | 0.78% |
| language | 65 | 0.78% |

### Title bigrams

| Bigram | SRs | % |
|--------|-----|---|
| career site | 180 | 2.15% |
| hiring manager | 111 | 1.32% |
| candidate profile | 105 | 1.25% |
| hiring status | 86 | 1.03% |
| interview scheduling | 46 | 0.55% |
| careers site | 43 | 0.51% |
| job posting | 43 | 0.51% |
| voice agent | 43 | 0.51% |
| offer letter | 42 | 0.50% |
| job pull | 40 | 0.48% |
| external career | 37 | 0.44% |
| fit score | 37 | 0.44% |
| apply flow | 33 | 0.39% |
| talent community | 30 | 0.36% |
| email templates | 30 | 0.36% |
| job alert | 29 | 0.35% |
| candidate profiles | 29 | 0.35% |
| pending worker | 29 | 0.35% |
| email address | 27 | 0.32% |
| job description | 26 | 0.31% |
| internal mobility | 25 | 0.30% |
| candidate status | 23 | 0.27% |
| phenom crm | 23 | 0.27% |
| shs testing | 23 | 0.27% |
| internal candidate | 22 | 0.26% |
| interview invite | 22 | 0.26% |
| email template | 21 | 0.25% |
| job search | 21 | 0.25% |
| job title | 21 | 0.25% |
| report builder | 21 | 0.25% |
| apply errors | 21 | 0.25% |
| scheduling link | 20 | 0.24% |
| usage report | 20 | 0.24% |
| status updated | 20 | 0.24% |
| employee feed | 19 | 0.23% |
| job alerts | 19 | 0.23% |
| job requisition | 19 | 0.23% |
| job page | 19 | 0.23% |
| job category | 19 | 0.23% |
| crm connect | 19 | 0.23% |
| hiring managers | 19 | 0.23% |
| candidate application | 19 | 0.23% |
| apm apply | 18 | 0.21% |
| phenom workday | 18 | 0.21% |
| internal career | 18 | 0.21% |
| high priority | 18 | 0.21% |
| crm usage | 18 | 0.21% |
| home page | 17 | 0.20% |
| requisition realignment | 17 | 0.20% |
| job application | 16 | 0.19% |
| automation triggering | 16 | 0.19% |
| internal candidates | 16 | 0.19% |
| matching criteria | 16 | 0.19% |
| status change | 16 | 0.19% |
| employee profile | 16 | 0.19% |
| showing phenom | 16 | 0.19% |
| career sites | 15 | 0.18% |
| job postings | 15 | 0.18% |
| staging environment | 15 | 0.18% |
| job sync | 15 | 0.18% |

---

## 3. Keywords in SR description (`DESCRIPTION`)

| Keyword | SRs with keyword in description | % of Jira-Yes |
|---------|--------------------------------|---------------|
| candidate | 2,497 | 29.78% |
| phenom | 2,106 | 25.12% |
| job | 1,800 | 21.47% |
| email | 1,454 | 17.34% |
| candidates | 1,328 | 15.84% |
| crm | 899 | 10.72% |
| name | 827 | 9.86% |
| profile | 823 | 9.82% |
| status | 785 | 9.36% |
| showing | 757 | 9.03% |
| interview | 755 | 9.01% |
| page | 732 | 8.73% |
| jobs | 730 | 8.71% |
| recruiter | 722 | 8.61% |
| site | 700 | 8.35% |
| hiring | 676 | 8.06% |
| data | 666 | 7.94% |
| currently | 634 | 7.56% |
| application | 614 | 7.32% |
| update | 613 | 7.31% |
| req | 594 | 7.08% |
| example | 587 | 7.00% |
| received | 585 | 6.98% |
| review | 585 | 6.98% |
| sent | 584 | 6.97% |
| time | 572 | 6.82% |
| internal | 562 | 6.70% |
| error | 557 | 6.64% |
| out | 553 | 6.60% |
| system | 551 | 6.57% |
| career | 537 | 6.41% |
| change | 536 | 6.39% |
| support | 536 | 6.39% |
| employee | 532 | 6.35% |
| manager | 517 | 6.17% |
| workday | 517 | 6.17% |
| apply | 513 | 6.12% |
| user | 507 | 6.05% |
| now | 488 | 5.82% |
| link | 488 | 5.82% |
| available | 488 | 5.82% |
| add | 482 | 5.75% |
| investigate | 474 | 5.65% |
| through | 474 | 5.65% |
| updated | 471 | 5.62% |
| process | 465 | 5.55% |
| both | 464 | 5.53% |
| report | 463 | 5.52% |
| confirm | 456 | 5.44% |
| reference | 452 | 5.39% |
| within | 436 | 5.20% |
| screenshots | 436 | 5.20% |
| requisition | 435 | 5.19% |
| look | 426 | 5.08% |
| list | 424 | 5.06% |
| correct | 412 | 4.91% |
| required | 401 | 4.78% |
| number | 399 | 4.76% |
| appears | 396 | 4.72% |
| expected | 395 | 4.71% |
| her | 393 | 4.69% |
| added | 393 | 4.69% |
| provide | 391 | 4.66% |
| date | 388 | 4.63% |
| created | 383 | 4.57% |
| screen | 383 | 4.57% |
| access | 383 | 4.57% |
| open | 379 | 4.52% |
| option | 374 | 4.46% |
| first | 373 | 4.45% |
| while | 370 | 4.41% |
| possible | 368 | 4.39% |
| address | 367 | 4.38% |
| show | 363 | 4.33% |
| cannot | 362 | 4.32% |
| emails | 361 | 4.31% |
| field | 357 | 4.26% |
| ats | 354 | 4.22% |
| shows | 354 | 4.22% |
| applied | 353 | 4.21% |
| careers | 353 | 4.21% |
| test | 348 | 4.15% |
| questions | 346 | 4.13% |
| find | 346 | 4.13% |
| completed | 344 | 4.10% |
| since | 340 | 4.06% |
| set | 339 | 4.04% |
| different | 338 | 4.03% |
| noticed | 337 | 4.02% |
| correctly | 335 | 4.00% |
| view | 331 | 3.95% |
| end | 330 | 3.94% |
| current | 329 | 3.92% |
| production | 328 | 3.91% |
| staging | 328 | 3.91% |
| understand | 326 | 3.89% |
| changes | 326 | 3.89% |
| multiple | 323 | 3.85% |
| trying | 323 | 3.85% |
| visible | 322 | 3.84% |

### Description bigrams

| Bigram | SRs | % |
|--------|-----|---|
| career site | 383 | 4.57% |
| candidate profile | 293 | 3.49% |
| hiring manager | 280 | 3.34% |
| candidate name | 261 | 3.11% |
| email address | 233 | 2.78% |
| hiring status | 188 | 2.24% |
| candidate email | 132 | 1.57% |
| phenom support | 130 | 1.55% |
| job req | 123 | 1.47% |
| careers site | 114 | 1.36% |
| hiring managers | 107 | 1.28% |
| candidate profiles | 103 | 1.23% |
| expected behavior | 102 | 1.22% |
| phenom crm | 101 | 1.20% |
| job requisition | 94 | 1.12% |
| job posting | 93 | 1.11% |
| confirm whether | 92 | 1.10% |
| interview scheduling | 88 | 1.05% |
| root cause | 86 | 1.03% |
| staging environment | 84 | 1.00% |
| offer letter | 84 | 1.00% |
| candidate candidate | 83 | 0.99% |
| job title | 82 | 0.98% |
| email sent | 80 | 0.95% |
| reach out | 73 | 0.87% |
| phone number | 73 | 0.87% |
| screen recording | 72 | 0.86% |
| soon possible | 71 | 0.85% |
| received email | 70 | 0.83% |
| start date | 70 | 0.83% |
| first name | 69 | 0.82% |
| within phenom | 68 | 0.81% |
| candidate experience | 68 | 0.81% |
| external career | 67 | 0.80% |
| job description | 63 | 0.75% |
| job pull | 63 | 0.75% |
| candidate applied | 62 | 0.74% |
| screen shot | 62 | 0.74% |
| talent community | 62 | 0.74% |
| applied job | 60 | 0.72% |
| screenshots reference | 60 | 0.72% |
| workday phenom | 60 | 0.72% |
| through phenom | 59 | 0.70% |
| phenom candidate | 59 | 0.70% |
| interview scheduled | 58 | 0.69% |
| screen shots | 58 | 0.69% |
| employee profile | 57 | 0.68% |
| production environment | 56 | 0.67% |
| name email | 56 | 0.67% |
| last name | 56 | 0.67% |
| internal candidate | 55 | 0.66% |
| schedule interview | 55 | 0.66% |
| job application | 55 | 0.66% |
| full name | 55 | 0.66% |
| last week | 55 | 0.66% |
| internal number | 55 | 0.66% |
| example candidate | 54 | 0.64% |
| job category | 54 | 0.64% |
| candidate status | 52 | 0.62% |
| phenom side | 52 | 0.62% |

---

## 4. Keywords in title **or** description (combined)

| Keyword | SRs | % of Jira-Yes |
|---------|-----|---------------|
| candidate | 2,629 | 31.36% |
| phenom | 2,228 | 26.57% |
| job | 1,927 | 22.98% |
| email | 1,510 | 18.01% |
| candidates | 1,393 | 16.61% |
| crm | 989 | 11.80% |
| profile | 867 | 10.34% |
| showing | 859 | 10.25% |
| status | 846 | 10.09% |
| name | 835 | 9.96% |
| interview | 817 | 9.74% |
| page | 791 | 9.43% |
| jobs | 781 | 9.32% |
| site | 777 | 9.27% |
| recruiter | 764 | 9.11% |
| update | 732 | 8.73% |
| hiring | 726 | 8.66% |
| data | 721 | 8.60% |
| application | 667 | 7.96% |
| currently | 636 | 7.59% |
| req | 620 | 7.40% |
| internal | 616 | 7.35% |
| sent | 615 | 7.34% |
| career | 613 | 7.31% |
| change | 603 | 7.19% |
| error | 603 | 7.19% |
| received | 597 | 7.12% |
| review | 596 | 7.11% |
| example | 587 | 7.00% |
| time | 586 | 6.99% |
| system | 575 | 6.86% |
| employee | 570 | 6.80% |
| out | 568 | 6.77% |
| apply | 565 | 6.74% |
| manager | 547 | 6.52% |
| support | 547 | 6.52% |
| user | 534 | 6.37% |
| workday | 534 | 6.37% |
| available | 527 | 6.29% |
| add | 524 | 6.25% |
| link | 513 | 6.12% |
| updated | 505 | 6.02% |
| now | 491 | 5.86% |
| through | 487 | 5.81% |
| investigate | 481 | 5.74% |
| process | 481 | 5.74% |
| report | 477 | 5.69% |
| missing | 474 | 5.65% |
| both | 472 | 5.63% |
| reference | 471 | 5.62% |
| requisition | 464 | 5.53% |
| required | 461 | 5.50% |
| confirm | 458 | 5.46% |
| within | 446 | 5.32% |
| list | 442 | 5.27% |
| screenshots | 436 | 5.20% |
| correct | 428 | 5.10% |
| look | 428 | 5.10% |
| cannot | 414 | 4.94% |
| number | 411 | 4.90% |
| access | 410 | 4.89% |
| expected | 410 | 4.89% |
| added | 405 | 4.83% |
| appears | 403 | 4.81% |
| emails | 402 | 4.79% |
| date | 399 | 4.76% |
| provide | 397 | 4.74% |
| screen | 396 | 4.72% |
| created | 395 | 4.71% |
| her | 393 | 4.69% |
| open | 392 | 4.68% |
| field | 389 | 4.64% |
| option | 388 | 4.63% |
| external | 387 | 4.62% |
| while | 381 | 4.54% |
| scheduling | 380 | 4.53% |
| show | 377 | 4.50% |
| ats | 377 | 4.50% |
| possible | 377 | 4.50% |
| first | 374 | 4.46% |
| address | 372 | 4.44% |
| shows | 371 | 4.43% |
| questions | 370 | 4.41% |
| careers | 367 | 4.38% |
| correctly | 366 | 4.37% |
| test | 365 | 4.35% |
| applied | 359 | 4.28% |
| find | 358 | 4.27% |
| visible | 357 | 4.26% |
| different | 357 | 4.26% |
| completed | 354 | 4.22% |
| view | 353 | 4.21% |
| multiple | 351 | 4.19% |
| staging | 350 | 4.17% |
| set | 348 | 4.15% |
| production | 348 | 4.15% |
| changes | 348 | 4.15% |
| since | 341 | 4.07% |
| noticed | 338 | 4.03% |
| integration | 337 | 4.02% |
| end | 337 | 4.02% |
| section | 334 | 3.98% |
| profiles | 333 | 3.97% |
| current | 332 | 3.96% |
| users | 331 | 3.95% |
| search | 329 | 3.92% |
| trying | 328 | 3.91% |
| understand | 327 | 3.90% |
| appear | 324 | 3.86% |
| ensure | 322 | 3.84% |
| want | 317 | 3.78% |
| text | 310 | 3.70% |
| remove | 309 | 3.69% |
| receive | 309 | 3.69% |
| advise | 308 | 3.67% |
| offer | 305 | 3.64% |
| recruiters | 304 | 3.63% |
| between | 303 | 3.61% |
| last | 298 | 3.55% |
| testing | 298 | 3.55% |

### Combined bigrams

| Bigram | SRs | % |
|--------|-----|---|
| career site | 438 | 5.22% |
| candidate profile | 333 | 3.97% |
| hiring manager | 306 | 3.65% |
| candidate name | 263 | 3.14% |
| email address | 235 | 2.80% |
| hiring status | 220 | 2.62% |
| candidate email | 140 | 1.67% |
| phenom support | 130 | 1.55% |
| careers site | 129 | 1.54% |
| job req | 129 | 1.54% |
| candidate profiles | 118 | 1.41% |
| job posting | 115 | 1.37% |
| interview scheduling | 115 | 1.37% |
| hiring managers | 113 | 1.35% |
| phenom crm | 108 | 1.29% |
| job requisition | 107 | 1.28% |
| expected behavior | 102 | 1.22% |
| offer letter | 100 | 1.19% |
| confirm whether | 93 | 1.11% |
| staging environment | 91 | 1.09% |
| candidate candidate | 90 | 1.07% |
| email sent | 88 | 1.05% |
| job title | 87 | 1.04% |
| root cause | 86 | 1.03% |
| job pull | 82 | 0.98% |
| external career | 79 | 0.94% |
| phone number | 75 | 0.89% |
| phenom candidate | 73 | 0.87% |
| reach out | 73 | 0.87% |
| screen recording | 72 | 0.86% |
| job description | 72 | 0.86% |
| talent community | 71 | 0.85% |
| soon possible | 71 | 0.85% |
| received email | 71 | 0.85% |
| candidate experience | 70 | 0.83% |
| start date | 70 | 0.83% |
| within phenom | 69 | 0.82% |
| first name | 69 | 0.82% |
| candidate applied | 66 | 0.79% |
| internal candidate | 66 | 0.79% |
| candidate status | 64 | 0.76% |
| workday phenom | 64 | 0.76% |
| job application | 63 | 0.75% |
| screen shot | 62 | 0.74% |
| through phenom | 62 | 0.74% |
| job category | 62 | 0.74% |
| interview scheduled | 61 | 0.73% |
| apply flow | 61 | 0.73% |
| employee profile | 60 | 0.72% |
| applied job | 60 | 0.72% |
| screenshots reference | 60 | 0.72% |
| production environment | 58 | 0.69% |
| schedule interview | 58 | 0.69% |
| screen shots | 58 | 0.69% |
| voice agent | 58 | 0.69% |
| email candidate | 57 | 0.68% |
| last name | 57 | 0.68% |
| internal mobility | 56 | 0.67% |
| name email | 56 | 0.67% |
| search results | 56 | 0.67% |
| status updated | 55 | 0.66% |
| full name | 55 | 0.66% |
| last week | 55 | 0.66% |
| internal number | 55 | 0.66% |
| email template | 54 | 0.64% |
| example candidate | 54 | 0.64% |
| showing phenom | 54 | 0.64% |
| interview invite | 54 | 0.64% |
| crm candidate | 53 | 0.63% |
| phenom side | 53 | 0.63% |
| home page | 52 | 0.62% |
| email templates | 52 | 0.62% |
| job postings | 51 | 0.61% |
| fit score | 51 | 0.61% |
| candidate application | 51 | 0.61% |
| job search | 50 | 0.60% |
| community phenom | 49 | 0.58% |
| emails sent | 49 | 0.58% |
| hrit hub | 49 | 0.58% |
| drop down | 49 | 0.58% |

---

## 5. Phrase presence (title vs description vs either)

Includes high-frequency customer bigrams plus sheet product-label strings that appear in free text. Rows with 0 hits omitted.

| Phrase | % title | % description | % title or description | # SRs (either) |
|--------|---------|---------------|------------------------|----------------|
| candidate | 14.91% | 38.90% | 40.03% | 3,356 |
| job | 11.65% | 26.91% | 28.20% | 2,364 |
| email | 6.55% | 19.68% | 20.13% | 1,688 |
| candidates | 4.16% | 16.41% | 17.19% | 1,441 |
| profile | 4.38% | 11.93% | 12.43% | 1,042 |
| interview | 6.11% | 11.58% | 12.05% | 1,010 |
| crm | 4.48% | 10.90% | 11.99% | 1,005 |
| recruiter | 2.47% | 11.30% | 11.71% | 982 |
| status | 4.58% | 10.01% | 10.68% | 895 |
| application | 3.60% | 9.27% | 9.97% | 836 |
| jobs | 2.93% | 9.34% | 9.94% | 833 |
| data | 2.72% | 8.71% | 9.34% | 783 |
| employee | 2.83% | 8.22% | 8.62% | 723 |
| apply | 3.02% | 7.45% | 8.15% | 683 |
| manager | 2.17% | 7.59% | 7.90% | 662 |
| requisition | 1.55% | 6.50% | 6.81% | 571 |
| workday | 1.62% | 6.32% | 6.52% | 547 |
| event | 2.09% | 5.80% | 5.93% | 497 |
| career site | 2.34% | 4.72% | 5.46% | 458 |
| ats | 1.37% | 5.07% | 5.45% | 457 |
| search | 1.57% | 5.14% | 5.36% | 449 |
| emails | 1.63% | 4.37% | 4.87% | 408 |
| scheduling | 2.42% | 4.08% | 4.81% | 403 |
| template | 2.40% | 4.37% | 4.64% | 389 |
| candidate profile | 1.54% | 3.88% | 4.40% | 369 |
| hiring manager | 1.63% | 4.13% | 4.39% | 368 |
| screening | 1.84% | 3.47% | 3.70% | 310 |
| automation | 2.14% | 3.46% | 3.58% | 300 |
| sso | 0.47% | 3.44% | 3.55% | 298 |
| filter | 1.44% | 3.27% | 3.39% | 284 |
| feed | 1.12% | 3.07% | 3.32% | 278 |
| job req | 0.62% | 3.01% | 3.23% | 271 |
| email address | 0.41% | 3.16% | 3.20% | 268 |
| posting | 1.25% | 2.72% | 3.12% | 262 |
| notification | 1.30% | 2.76% | 3.07% | 257 |
| onboarding | 1.54% | 2.64% | 3.01% | 252 |
| hiring status | 1.23% | 2.53% | 2.91% | 244 |
| candidate name | 0.13% | 2.79% | 2.87% | 241 |
| dec | 0.49% | 2.56% | 2.62% | 220 |
| campaign | 1.32% | 2.45% | 2.54% | 213 |
| resume | 1.01% | 2.31% | 2.39% | 200 |
| templates | 1.13% | 2.21% | 2.37% | 199 |
| merge | 1.37% | 2.21% | 2.36% | 198 |
| referral | 1.47% | 2.05% | 2.28% | 191 |
| analytics | 0.83% | 1.88% | 2.14% | 179 |
| recording | 0.16% | 2.00% | 2.05% | 172 |
| events | 0.70% | 1.87% | 2.00% | 168 |
| cms | 0.43% | 1.84% | 1.96% | 164 |
| duplicate | 0.89% | 1.59% | 1.96% | 164 |
| job posting | 0.70% | 1.50% | 1.81% | 152 |
| job requisition | 0.31% | 1.43% | 1.59% | 133 |
| linkedin | 0.78% | 1.50% | 1.59% | 133 |
| careers site | 0.55% | 1.38% | 1.57% | 132 |
| phenom support | 0.01% | 1.50% | 1.50% | 126 |
| pipeline | 0.16% | 1.47% | 1.49% | 125 |
| mobile | 0.61% | 1.41% | 1.48% | 124 |
| successfactors | 0.27% | 1.42% | 1.46% | 122 |
| sms | 0.89% | 1.32% | 1.44% | 121 |
| hiring managers | 0.25% | 1.35% | 1.43% | 120 |
| screen shot | 0.00% | 1.42% | 1.42% | 119 |
| candidate profiles | 0.35% | 1.16% | 1.34% | 112 |
| interview scheduling | 0.54% | 1.01% | 1.32% | 111 |
| questionnaire | 0.68% | 1.23% | 1.32% | 111 |
| expected behavior | 0.00% | 1.29% | 1.29% | 108 |
| chatbot | 0.82% | 1.19% | 1.29% | 108 |
| forms | 0.35% | 1.15% | 1.28% | 107 |
| offer letter | 0.58% | 1.04% | 1.23% | 103 |
| job title | 0.36% | 1.17% | 1.23% | 103 |
| phenom crm | 0.27% | 1.13% | 1.20% | 101 |
| internal candidate | 0.47% | 1.05% | 1.20% | 101 |
| export | 0.45% | 1.17% | 1.19% | 100 |
| candidate email | 0.13% | 1.06% | 1.17% | 98 |
| staging environment | 0.19% | 1.05% | 1.15% | 96 |
| email template | 0.60% | 0.97% | 1.15% | 96 |
| nifi | 0.07% | 1.11% | 1.13% | 95 |
| external career | 0.50% | 0.95% | 1.11% | 93 |
| phone number | 0.23% | 1.03% | 1.06% | 89 |
| root cause | 0.02% | 1.04% | 1.04% | 87 |
| assessment | 0.57% | 0.93% | 1.04% | 87 |
| job description | 0.37% | 0.91% | 1.03% | 86 |
| login | 0.36% | 0.91% | 1.03% | 86 |
| confirm whether | 0.01% | 1.00% | 1.01% | 85 |
| job pull | 0.51% | 0.79% | 1.01% | 85 |
| compliance | 0.14% | 0.91% | 1.00% | 84 |
| job application | 0.20% | 0.87% | 0.95% | 80 |
| screen recording | 0.01% | 0.92% | 0.92% | 77 |
| employee profile | 0.23% | 0.81% | 0.89% | 75 |
| candidate experience | 0.04% | 0.86% | 0.88% | 74 |
| reach out | 0.00% | 0.87% | 0.87% | 73 |
| talent community | 0.36% | 0.75% | 0.86% | 72 |
| start date | 0.05% | 0.85% | 0.85% | 71 |
| interview invite | 0.35% | 0.61% | 0.85% | 71 |
| learning | 0.49% | 0.69% | 0.83% | 70 |
| inbox | 0.17% | 0.82% | 0.83% | 70 |
| first name | 0.08% | 0.82% | 0.82% | 69 |
| job alert | 0.58% | 0.75% | 0.82% | 69 |
| internal career | 0.26% | 0.73% | 0.81% | 68 |
| apply flow | 0.47% | 0.66% | 0.80% | 67 |
| domain | 0.26% | 0.76% | 0.79% | 66 |
| production environment | 0.05% | 0.75% | 0.78% | 65 |
| job category | 0.24% | 0.64% | 0.74% | 62 |
| referrals | 0.29% | 0.61% | 0.73% | 61 |
| hsi | 0.31% | 0.64% | 0.73% | 61 |
| full name | 0.00% | 0.72% | 0.72% | 60 |
| screen shots | 0.00% | 0.70% | 0.70% | 59 |
| voice agent | 0.52% | 0.47% | 0.70% | 59 |
| landing page | 0.23% | 0.62% | 0.70% | 59 |
| last week | 0.01% | 0.69% | 0.69% | 58 |
| last name | 0.05% | 0.67% | 0.68% | 57 |
| taleo | 0.14% | 0.64% | 0.68% | 57 |
| internal mobility | 0.30% | 0.52% | 0.67% | 56 |
| schedule interview | 0.24% | 0.52% | 0.66% | 55 |
| search results | 0.13% | 0.58% | 0.66% | 55 |
| home page | 0.21% | 0.60% | 0.66% | 55 |
| email templates | 0.36% | 0.52% | 0.64% | 54 |
| fit score | 0.47% | 0.57% | 0.64% | 54 |
| within phenom | 0.04% | 0.62% | 0.63% | 53 |
| candidate status | 0.33% | 0.35% | 0.61% | 51 |
| phenom side | 0.01% | 0.60% | 0.61% | 51 |
| job postings | 0.18% | 0.50% | 0.61% | 51 |

### Sheet product-label strings that customers also typed in title/description

These are exact lowercase matches of `PRODUCT_EXPERIENCE` / `PRODUCT_EXPERIENCE_PRODUCT` label text appearing inside free text (often rare — labels live in columns, not in prose).

| Label string in free text | % of Jira-Yes | # SRs |
|--------------------------|---------------|-------|
| data | 9.34% | 783 |
| search | 5.36% | 449 |
| hiring status | 2.91% | 244 |
| dec | 2.62% | 220 |
| analytics | 2.14% | 179 |
| cms | 1.96% | 164 |
| chatbot | 1.29% | 108 |
| compliance | 1.00% | 84 |
| learning | 0.83% | 70 |
| referrals | 0.73% | 61 |
| internal mobility | 0.67% | 56 |
| apm | 0.61% | 51 |
| employee feed | 0.48% | 40 |
| pup | 0.18% | 15 |
| mentoring | 0.16% | 13 |
| alumni | 0.16% | 13 |
| people manager | 0.16% | 13 |
| tdp | 0.14% | 12 |
| talent management | 0.07% | 6 |
| hiring automations | 0.07% | 6 |
| automation engine | 0.07% | 6 |
| job distribution | 0.07% | 6 |
| video hub | 0.07% | 6 |
| career pathing | 0.06% | 5 |
| miscellaneous | 0.05% | 4 |
| direct sourcing | 0.05% | 4 |
| etg | 0.04% | 3 |
| mx - hiring | 0.01% | 1 |
| phenom x+ | 0.01% | 1 |
| resume parser | 0.01% | 1 |
| high volume hiring (hvh) | 0.01% | 1 |

---

## 6. Top customer keywords **within** each `PRODUCT_EXPERIENCE`

Denominator for % in this section = rows in that product experience (still Jira-Yes only).

### Recruiter Experience (RX) (n=1,949, 23.25% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| candidate | 778 | 39.92% |
| phenom | 591 | 30.32% |
| email | 560 | 28.73% |
| candidates | 457 | 23.45% |
| crm | 414 | 21.24% |
| job | 399 | 20.47% |
| profile | 351 | 18.01% |
| recruiter | 266 | 13.65% |
| status | 254 | 13.03% |
| emails | 216 | 11.08% |
| showing | 204 | 10.47% |
| hiring | 200 | 10.26% |
| sent | 198 | 10.16% |
| name | 186 | 9.54% |
| system | 177 | 9.08% |
| out | 176 | 9.03% |
| automation | 173 | 8.88% |
| event | 173 | 8.88% |
| data | 161 | 8.26% |
| received | 161 | 8.26% |
| example | 158 | 8.11% |
| list | 158 | 8.11% |
| review | 153 | 7.85% |
| jobs | 153 | 7.85% |
| update | 150 | 7.70% |
| internal | 150 | 7.70% |
| template | 145 | 7.44% |
| profiles | 145 | 7.44% |
| now | 143 | 7.34% |
| application | 142 | 7.29% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| candidate profile | 167 | 8.57% |
| hiring status | 95 | 4.87% |
| email address | 83 | 4.26% |
| hiring manager | 56 | 2.87% |
| candidate profiles | 55 | 2.82% |
| career site | 43 | 2.21% |
| email template | 40 | 2.05% |
| phenom crm | 40 | 2.05% |
| email sent | 35 | 1.80% |
| phone number | 34 | 1.74% |
| candidate name | 34 | 1.74% |
| candidate email | 32 | 1.64% |
| job req | 30 | 1.54% |
| email templates | 30 | 1.54% |
| candidate status | 29 | 1.49% |
| staging environment | 28 | 1.44% |
| job requisition | 26 | 1.33% |
| phenom candidate | 26 | 1.33% |
| receive email | 26 | 1.33% |
| profile phenom | 25 | 1.28% |

### Integration Experience (IX) (n=1,500, 17.89% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| phenom | 648 | 43.20% |
| job | 612 | 40.80% |
| candidate | 408 | 27.20% |
| workday | 317 | 21.13% |
| candidates | 299 | 19.93% |
| application | 290 | 19.33% |
| apply | 263 | 17.53% |
| jobs | 236 | 15.73% |
| crm | 236 | 15.73% |
| showing | 229 | 15.27% |
| status | 226 | 15.07% |
| site | 225 | 15.00% |
| req | 204 | 13.60% |
| ats | 188 | 12.53% |
| career | 187 | 12.47% |
| data | 172 | 11.47% |
| integration | 169 | 11.27% |
| email | 164 | 10.93% |
| update | 160 | 10.67% |
| internal | 157 | 10.47% |
| error | 157 | 10.47% |
| hiring | 153 | 10.20% |
| posted | 151 | 10.07% |
| requisition | 148 | 9.87% |
| open | 137 | 9.13% |
| external | 132 | 8.80% |
| change | 129 | 8.60% |
| currently | 127 | 8.47% |
| example | 127 | 8.47% |
| field | 127 | 8.47% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| career site | 146 | 9.73% |
| hiring status | 72 | 4.80% |
| job pull | 70 | 4.67% |
| job posting | 57 | 3.80% |
| job req | 49 | 3.27% |
| job requisition | 47 | 3.13% |
| careers site | 44 | 2.93% |
| email address | 43 | 2.87% |
| apply flow | 40 | 2.67% |
| workday phenom | 39 | 2.60% |
| phenom crm | 39 | 2.60% |
| job application | 37 | 2.47% |
| candidate profile | 37 | 2.47% |
| hiring manager | 37 | 2.47% |
| phenom side | 36 | 2.40% |
| showing phenom | 35 | 2.33% |
| open phenom | 34 | 2.27% |
| external career | 34 | 2.27% |
| staging environment | 33 | 2.20% |
| phenom job | 30 | 2.00% |

### Candidate Experience (CX) (n=1,066, 12.71% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| page | 379 | 35.55% |
| site | 307 | 28.80% |
| job | 292 | 27.39% |
| career | 203 | 19.04% |
| widget | 164 | 15.38% |
| phenom | 162 | 15.20% |
| careers | 161 | 15.10% |
| jobs | 156 | 14.63% |
| pages | 156 | 14.63% |
| text | 140 | 13.13% |
| change | 135 | 12.66% |
| search | 133 | 12.48% |
| update | 115 | 10.79% |
| cms | 114 | 10.69% |
| link | 112 | 10.51% |
| candidate | 100 | 9.38% |
| currently | 96 | 9.01% |
| button | 96 | 9.01% |
| add | 93 | 8.72% |
| apply | 92 | 8.63% |
| showing | 91 | 8.54% |
| video | 80 | 7.50% |
| reference | 78 | 7.32% |
| chatbot | 74 | 6.94% |
| content | 72 | 6.75% |
| font | 71 | 6.66% |
| mobile | 71 | 6.66% |
| changes | 71 | 6.66% |
| appears | 71 | 6.66% |
| email | 70 | 6.57% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| career site | 159 | 14.92% |
| careers site | 49 | 4.60% |
| home page | 32 | 3.00% |
| talent community | 30 | 2.81% |
| job page | 30 | 2.81% |
| external career | 29 | 2.72% |
| job description | 29 | 2.72% |
| search results | 28 | 2.63% |
| design studio | 24 | 2.25% |
| landing page | 23 | 2.16% |
| job search | 22 | 2.06% |
| job posting | 22 | 2.06% |
| job pages | 20 | 1.88% |
| screen recording | 20 | 1.88% |
| job alert | 19 | 1.78% |
| job category | 19 | 1.78% |
| mobile view | 18 | 1.69% |
| phenom support | 18 | 1.69% |
| user experience | 17 | 1.59% |
| join talent | 16 | 1.50% |

### Employee Onboarding Experience (n=957, 11.41% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| candidate | 454 | 47.44% |
| tydy | 263 | 27.48% |
| name | 235 | 24.56% |
| email | 232 | 24.24% |
| onboarding | 193 | 20.17% |
| hire | 164 | 17.14% |
| status | 149 | 15.57% |
| required | 127 | 13.27% |
| offer | 123 | 12.85% |
| phenom | 115 | 12.02% |
| employee | 113 | 11.81% |
| form | 106 | 11.08% |
| re-push | 102 | 10.66% |
| date | 97 | 10.14% |
| support | 94 | 9.82% |
| update | 94 | 9.82% |
| candidates | 93 | 9.72% |
| earliest | 90 | 9.40% |
| cases | 88 | 9.20% |
| requisition | 88 | 9.20% |
| updated | 86 | 8.99% |
| sent | 85 | 8.88% |
| reflecting | 85 | 8.88% |
| type | 85 | 8.88% |
| vignesh | 85 | 8.88% |
| confirm | 83 | 8.67% |
| process | 80 | 8.36% |
| error | 79 | 8.25% |
| section | 79 | 8.25% |
| bgc | 77 | 8.05% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| candidate name | 121 | 12.64% |
| candidate candidate | 52 | 5.43% |
| com/disclaimer html | 48 | 5.02% |
| disclaimer visit | 48 | 5.02% |
| asianpaints com/disclaimer | 48 | 5.02% |
| email disclaimer | 48 | 5.02% |
| candidate email | 48 | 5.02% |
| visit asianpaints | 46 | 4.81% |
| html email | 46 | 4.81% |
| start date | 46 | 4.81% |
| offer letter | 41 | 4.28% |
| candidate full | 37 | 3.87% |
| type hire | 35 | 3.66% |
| full name | 34 | 3.55% |
| resolve earliest | 33 | 3.45% |
| hire type | 32 | 3.34% |
| pending worker | 31 | 3.24% |
| tydy portal | 29 | 3.03% |
| asianpaints subject | 28 | 2.93% |
| phenom support | 28 | 2.93% |

### Hiring Intelligence (n=949, 11.32% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| interview | 516 | 54.37% |
| candidate | 445 | 46.89% |
| scheduling | 267 | 28.13% |
| phenom | 245 | 25.82% |
| email | 226 | 23.81% |
| candidates | 204 | 21.50% |
| recruiter | 204 | 21.50% |
| interviews | 191 | 20.13% |
| calendar | 179 | 18.86% |
| time | 177 | 18.65% |
| job | 165 | 17.39% |
| sent | 160 | 16.86% |
| scheduled | 157 | 16.54% |
| interviewer | 151 | 15.91% |
| invite | 141 | 14.86% |
| schedule | 136 | 14.33% |
| meeting | 135 | 14.23% |
| received | 131 | 13.80% |
| link | 131 | 13.80% |
| req | 121 | 12.75% |
| screening | 118 | 12.43% |
| showing | 104 | 10.96% |
| hiring | 102 | 10.75% |
| available | 98 | 10.33% |
| out | 98 | 10.33% |
| error | 96 | 10.12% |
| manager | 95 | 10.01% |
| her | 92 | 9.69% |
| name | 92 | 9.69% |
| interviewers | 91 | 9.59% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| interview scheduling | 83 | 8.75% |
| hiring manager | 70 | 7.38% |
| candidate name | 57 | 6.01% |
| interview scheduled | 42 | 4.43% |
| interview invite | 42 | 4.43% |
| schedule interview | 41 | 4.32% |
| voice agent | 40 | 4.21% |
| scheduling link | 35 | 3.69% |
| scheduled interview | 35 | 3.69% |
| candidate profile | 35 | 3.69% |
| schedule interviews | 34 | 3.58% |
| time slots | 30 | 3.16% |
| candidate email | 29 | 3.06% |
| time zone | 27 | 2.85% |
| confirmation email | 25 | 2.63% |
| received email | 25 | 2.63% |
| sap myally | 23 | 2.42% |
| job req | 23 | 2.42% |
| email address | 23 | 2.42% |
| email sent | 22 | 2.32% |

### Employee Experience (EX) (n=549, 6.55% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| employee | 147 | 26.78% |
| internal | 107 | 19.49% |
| job | 103 | 18.76% |
| profile | 100 | 18.21% |
| phenom | 94 | 17.12% |
| page | 78 | 14.21% |
| email | 78 | 14.21% |
| career | 73 | 13.30% |
| change | 73 | 13.30% |
| site | 72 | 13.11% |
| employees | 69 | 12.57% |
| referral | 69 | 12.57% |
| candidate | 64 | 11.66% |
| update | 60 | 10.93% |
| manager | 55 | 10.02% |
| add | 52 | 9.47% |
| user | 49 | 8.93% |
| remove | 48 | 8.74% |
| skills | 46 | 8.38% |
| link | 44 | 8.01% |
| currently | 42 | 7.65% |
| name | 42 | 7.65% |
| users | 39 | 7.10% |
| crm | 39 | 7.10% |
| jobs | 38 | 6.92% |
| text | 38 | 6.92% |
| data | 37 | 6.74% |
| updated | 37 | 6.74% |
| erm | 36 | 6.56% |
| want | 36 | 6.56% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| career site | 37 | 6.74% |
| internal mobility | 32 | 5.83% |
| internal career | 24 | 4.37% |
| employee profile | 21 | 3.83% |
| employee feed | 19 | 3.46% |
| kind sofia | 12 | 2.19% |
| job title | 12 | 2.19% |
| email address | 12 | 2.19% |
| referred candidate | 12 | 2.19% |
| nitish sadaiya | 12 | 2.19% |
| mobility site | 10 | 1.82% |
| colella nitish | 10 | 1.82% |
| employee referral | 10 | 1.82% |
| mentor profile | 9 | 1.64% |
| internal employees | 9 | 1.64% |
| employee experience | 9 | 1.64% |
| career path | 9 | 1.64% |
| internal employee | 9 | 1.64% |
| development plan | 8 | 1.46% |
| access internal | 8 | 1.46% |

### Manager Experience (MX) (n=373, 4.45% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| hiring | 139 | 37.27% |
| candidate | 138 | 37.00% |
| manager | 120 | 32.17% |
| candidates | 79 | 21.18% |
| phenom | 74 | 19.84% |
| job | 71 | 19.03% |
| offer | 63 | 16.89% |
| interview | 60 | 16.09% |
| profile | 60 | 16.09% |
| email | 54 | 14.48% |
| managers | 54 | 14.48% |
| req | 53 | 14.21% |
| recruiter | 51 | 13.67% |
| evaluation | 45 | 12.06% |
| view | 44 | 11.80% |
| hrm | 42 | 11.26% |
| received | 40 | 10.72% |
| review | 38 | 10.19% |
| crm | 38 | 10.19% |
| letter | 38 | 10.19% |
| sent | 37 | 9.92% |
| access | 36 | 9.65% |
| interviewer | 33 | 8.85% |
| status | 32 | 8.58% |
| visible | 31 | 8.31% |
| receiving | 30 | 8.04% |
| user | 30 | 8.04% |
| form | 29 | 7.77% |
| notifications | 29 | 7.77% |
| support | 28 | 7.51% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| hiring manager | 103 | 27.61% |
| hiring managers | 51 | 13.67% |
| offer letter | 35 | 9.38% |
| candidate profile | 30 | 8.04% |
| manager portal | 12 | 3.22% |
| manager view | 12 | 3.22% |
| internal number | 10 | 2.68% |
| confirm whether | 10 | 2.68% |
| phenom hiring | 9 | 2.41% |
| hiring status | 8 | 2.14% |
| signed offer | 8 | 2.14% |
| service hub | 7 | 1.88% |
| interview feedback | 7 | 1.88% |
| access candidate | 7 | 1.88% |
| evaluation form | 7 | 1.88% |
| manager access | 7 | 1.88% |
| hiring leader | 7 | 1.88% |
| interview evaluation | 7 | 1.88% |
| visible hiring | 7 | 1.88% |
| expected behavior | 7 | 1.88% |

### Analytics (n=300, 3.58% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| report | 196 | 65.33% |
| data | 124 | 41.33% |
| analytics | 112 | 37.33% |
| phenom | 88 | 29.33% |
| job | 72 | 24.00% |
| candidate | 60 | 20.00% |
| crm | 60 | 20.00% |
| reporting | 55 | 18.33% |
| candidates | 53 | 17.67% |
| showing | 46 | 15.33% |
| reports | 45 | 15.00% |
| jobs | 44 | 14.67% |
| time | 43 | 14.33% |
| date | 38 | 12.67% |
| builder | 38 | 12.67% |
| shows | 37 | 12.33% |
| status | 37 | 12.33% |
| recruiter | 36 | 12.00% |
| pull | 34 | 11.33% |
| number | 34 | 11.33% |
| hiring | 33 | 11.00% |
| source | 32 | 10.67% |
| example | 32 | 10.67% |
| apply | 31 | 10.33% |
| noticed | 31 | 10.33% |
| each | 30 | 10.00% |
| usage | 30 | 10.00% |
| review | 29 | 9.67% |
| missing | 28 | 9.33% |
| email | 28 | 9.33% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| report builder | 34 | 11.33% |
| usage report | 24 | 8.00% |
| crm usage | 22 | 7.33% |
| analytics report | 16 | 5.33% |
| date range | 16 | 5.33% |
| report report | 15 | 5.00% |
| traffic source | 15 | 5.00% |
| phenom analytics | 14 | 4.67% |
| report shows | 14 | 4.67% |
| career site | 13 | 4.33% |
| hiring status | 11 | 3.67% |
| report analytics | 10 | 3.33% |
| source report | 10 | 3.33% |
| page views | 10 | 3.33% |
| job category | 10 | 3.33% |
| talent analytics | 10 | 3.33% |
| applies report | 9 | 3.00% |
| hiring funnel | 9 | 3.00% |
| report job | 9 | 3.00% |
| jobs report | 8 | 2.67% |

### Search & Personalization (n=201, 2.40% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| job | 84 | 41.79% |
| candidate | 59 | 29.35% |
| candidates | 55 | 27.36% |
| phenom | 50 | 24.88% |
| jobs | 45 | 22.39% |
| search | 42 | 20.90% |
| filter | 36 | 17.91% |
| fit | 36 | 17.91% |
| crm | 35 | 17.41% |
| showing | 35 | 17.41% |
| score | 32 | 15.92% |
| results | 29 | 14.43% |
| criteria | 28 | 13.93% |
| matching | 26 | 12.94% |
| skills | 26 | 12.94% |
| site | 26 | 12.94% |
| filters | 23 | 11.44% |
| experience | 23 | 11.44% |
| example | 23 | 11.44% |
| feature | 22 | 10.95% |
| result | 21 | 10.45% |
| location | 21 | 10.45% |
| currently | 20 | 9.95% |
| profile | 20 | 9.95% |
| career | 20 | 9.95% |
| list | 19 | 9.45% |
| expected | 19 | 9.45% |
| support | 19 | 9.45% |
| while | 18 | 8.96% |
| functionality | 18 | 8.96% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| fit score | 30 | 14.93% |
| career site | 17 | 8.46% |
| matching criteria | 16 | 7.96% |
| job search | 11 | 5.47% |
| search results | 11 | 5.47% |
| candidate profile | 9 | 4.48% |
| hiring status | 9 | 4.48% |
| candidate profiles | 8 | 3.98% |
| search bar | 7 | 3.48% |
| phenom support | 7 | 3.48% |
| job titles | 7 | 3.48% |
| job title | 7 | 3.48% |
| job description | 7 | 3.48% |
| search functionality | 6 | 2.99% |
| expected behavior | 6 | 2.99% |
| location search | 6 | 2.99% |
| ideal candidates | 5 | 2.49% |
| phenom crm | 5 | 2.49% |
| job req | 5 | 2.49% |
| user experience | 5 | 2.49% |

### Phenomenal Tools (n=152, 1.81% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| phenom | 59 | 38.82% |
| access | 54 | 35.53% |
| users | 40 | 26.32% |
| user | 39 | 25.66% |
| hub | 27 | 17.76% |
| process | 24 | 15.79% |
| error | 23 | 15.13% |
| email | 22 | 14.47% |
| hrit | 22 | 14.47% |
| crm | 21 | 13.82% |
| account | 21 | 13.82% |
| support | 20 | 13.16% |
| data | 20 | 13.16% |
| login | 19 | 12.50% |
| hiring | 17 | 11.18% |
| currently | 17 | 11.18% |
| name | 17 | 11.18% |
| service | 16 | 10.53% |
| sso | 16 | 10.53% |
| manager | 16 | 10.53% |
| both | 15 | 9.87% |
| log | 15 | 9.87% |
| time | 14 | 9.21% |
| update | 14 | 9.21% |
| role | 14 | 9.21% |
| certificate | 13 | 8.55% |
| roles | 13 | 8.55% |
| well | 13 | 8.55% |
| remove | 13 | 8.55% |
| complete | 12 | 7.89% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| hrit hub | 14 | 9.21% |
| service hub | 11 | 7.24% |
| hiring manager | 10 | 6.58% |
| phenom support | 7 | 4.61% |
| career site | 7 | 4.61% |
| user access | 7 | 4.61% |
| hiring managers | 6 | 3.95% |
| access phenom | 6 | 3.95% |
| access denied | 6 | 3.95% |
| data deletion | 6 | 3.95% |
| churn process | 5 | 3.29% |
| email address | 5 | 3.29% |
| account name | 5 | 3.29% |
| auto provisioning | 4 | 2.63% |
| access crm | 4 | 2.63% |
| phenom phans | 4 | 2.63% |
| error messages | 4 | 2.63% |
| screen shot | 4 | 2.63% |
| her access | 4 | 2.63% |
| login phenom | 4 | 2.63% |

### Talent Management (n=108, 1.29% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| erm | 59 | 54.63% |
| employees | 26 | 24.07% |
| skills | 25 | 23.15% |
| employee | 23 | 21.30% |
| phenom | 19 | 17.59% |
| role | 18 | 16.67% |
| kind | 17 | 15.74% |
| skill | 17 | 15.74% |
| add | 17 | 15.74% |
| user | 16 | 14.81% |
| diana | 15 | 13.89% |
| received | 13 | 12.04% |
| manager | 13 | 12.04% |
| view | 13 | 12.04% |
| available | 12 | 11.11% |
| roles | 12 | 11.11% |
| missing | 12 | 11.11% |
| possible | 12 | 11.11% |
| job | 12 | 11.11% |
| visible | 11 | 10.19% |
| tab | 11 | 10.19% |
| learning | 10 | 9.26% |
| field | 10 | 9.26% |
| report | 10 | 9.26% |
| now | 10 | 9.26% |
| talent | 9 | 8.33% |
| comment | 9 | 8.33% |
| email | 9 | 8.33% |
| users | 9 | 8.33% |
| plan | 9 | 8.33% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| kind diana | 15 | 13.89% |
| comment user | 8 | 7.41% |
| received comment | 8 | 7.41% |
| erm skills | 7 | 6.48% |
| add skills | 5 | 4.63% |
| find reported | 4 | 3.70% |
| career path | 4 | 3.70% |
| erm employee | 4 | 3.70% |
| proficiency level | 4 | 3.70% |
| advanced search | 4 | 3.70% |
| skills uat | 4 | 3.70% |
| gbs learning | 3 | 2.78% |
| dev plans | 3 | 2.78% |
| development plans | 3 | 2.78% |
| available erm | 3 | 2.78% |
| roles report | 3 | 2.78% |
| employee feed | 3 | 2.78% |
| learning plan | 3 | 2.78% |
| employee search | 3 | 2.78% |
| while testing | 3 | 2.78% |

### Data (n=108, 1.29% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| candidate | 67 | 62.04% |
| profile | 58 | 53.70% |
| profiles | 55 | 50.93% |
| merged | 49 | 45.37% |
| phenom | 42 | 38.89% |
| candidates | 40 | 37.04% |
| email | 37 | 34.26% |
| merge | 33 | 30.56% |
| job | 26 | 24.07% |
| ats | 26 | 24.07% |
| crm | 25 | 23.15% |
| name | 21 | 19.44% |
| address | 21 | 19.44% |
| unmerge | 20 | 18.52% |
| different | 18 | 16.67% |
| data | 17 | 15.74% |
| applied | 16 | 14.81% |
| internal | 16 | 14.81% |
| number | 14 | 12.96% |
| merging | 14 | 12.96% |
| records | 14 | 12.96% |
| system | 13 | 12.04% |
| separate | 13 | 12.04% |
| appears | 12 | 11.11% |
| application | 12 | 11.11% |
| hiring | 11 | 10.19% |
| review | 11 | 10.19% |
| find | 11 | 10.19% |
| employee | 11 | 10.19% |
| her | 11 | 10.19% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| candidate profiles | 23 | 21.30% |
| candidate profile | 20 | 18.52% |
| email address | 16 | 14.81% |
| profiles merged | 14 | 12.96% |
| merged candidate | 11 | 10.19% |
| profile merge | 11 | 10.19% |
| candidate name | 8 | 7.41% |
| unmerge profiles | 8 | 7.41% |
| hiring status | 7 | 6.48% |
| phone number | 7 | 6.48% |
| incorrectly merged | 7 | 6.48% |
| candidate email | 6 | 5.56% |
| merged phenom | 6 | 5.56% |
| applied job | 6 | 5.56% |
| profile merged | 6 | 5.56% |
| phone numbers | 6 | 5.56% |
| unmerge candidate | 5 | 4.63% |
| phenom merged | 5 | 4.63% |
| merged profiles | 5 | 4.63% |
| phenom candidate | 5 | 4.63% |

### Other Products (n=66, 0.79% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| job | 39 | 59.09% |
| jobs | 23 | 34.85% |
| phenom | 21 | 31.82% |
| feed | 18 | 27.27% |
| candidates | 14 | 21.21% |
| xml | 14 | 21.21% |
| posting | 11 | 16.67% |
| candidate | 11 | 16.67% |
| available | 10 | 15.15% |
| site | 10 | 15.15% |
| example | 9 | 13.64% |
| out | 9 | 13.64% |
| provide | 9 | 13.64% |
| email | 9 | 13.64% |
| linkedin | 9 | 13.64% |
| set | 8 | 12.12% |
| open | 8 | 12.12% |
| data | 8 | 12.12% |
| expected | 8 | 12.12% |
| update | 8 | 12.12% |
| career | 8 | 12.12% |
| included | 8 | 12.12% |
| system | 8 | 12.12% |
| missing | 7 | 10.61% |
| cannot | 7 | 10.61% |
| because | 7 | 10.61% |
| questions | 7 | 10.61% |
| review | 7 | 10.61% |
| level | 7 | 10.61% |
| feature | 7 | 10.61% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| xml feed | 13 | 19.70% |
| job feed | 7 | 10.61% |
| career site | 7 | 10.61% |
| job postings | 6 | 9.09% |
| job posting | 5 | 7.58% |
| job board | 4 | 6.06% |
| reach out | 4 | 6.06% |
| job description | 3 | 4.55% |
| high level | 3 | 4.55% |
| number jobs | 3 | 4.55% |
| job level | 3 | 4.55% |
| configuration support | 3 | 4.55% |
| feature expected | 3 | 4.55% |
| enabled features | 3 | 4.55% |
| gen features | 3 | 4.55% |
| job candidate | 3 | 4.55% |
| feed phenom | 3 | 4.55% |
| jobboards-ir phenommarket | 3 | 4.55% |
| linkedin feed | 3 | 4.55% |
| seek job | 2 | 3.03% |

### Hiring Automations (n=51, 0.61% of Jira-Yes)

| Keyword | SRs in this PE | % of this PE |
|---------|----------------|--------------|
| candidate | 27 | 52.94% |
| hvh | 19 | 37.25% |
| job | 13 | 25.49% |
| apply | 12 | 23.53% |
| candidates | 12 | 23.53% |
| questions | 11 | 21.57% |
| assessment | 11 | 21.57% |
| interview | 11 | 21.57% |
| fast | 10 | 19.61% |
| example | 10 | 19.61% |
| application | 9 | 17.65% |
| flow | 9 | 17.65% |
| schedule | 9 | 17.65% |
| workflow | 9 | 17.65% |
| track | 8 | 15.69% |
| hiring | 8 | 15.69% |
| completed | 8 | 15.69% |
| update | 7 | 13.73% |
| recruiter | 7 | 13.73% |
| question | 7 | 13.73% |
| screening | 7 | 13.73% |
| applied | 7 | 13.73% |
| email | 7 | 13.73% |
| status | 7 | 13.73% |
| once | 6 | 11.76% |
| within | 6 | 11.76% |
| sent | 6 | 11.76% |
| assessments | 6 | 11.76% |
| chatbot | 6 | 11.76% |
| phone | 6 | 11.76% |

| Bigram | SRs | % of this PE |
|--------|-----|--------------|
| fast track | 8 | 15.69% |
| hvh workflow | 5 | 9.80% |
| question hvh | 3 | 5.88% |
| example candidate | 3 | 5.88% |
| apply flow | 3 | 5.88% |
| phone screen | 3 | 5.88% |
| track status | 3 | 5.88% |
| high volume | 3 | 5.88% |
| candidates fast | 3 | 5.88% |
| fast tracked | 3 | 5.88% |
| bon secours | 2 | 3.92% |
| within hvh | 2 | 3.92% |
| hvh process | 2 | 3.92% |
| hiring automation | 2 | 3.92% |
| screening questions | 2 | 3.92% |
| both candidates | 2 | 3.92% |
| hiring manager | 2 | 3.92% |
| disney-stg phenompro | 2 | 3.92% |
| phenompro com/waltdisneyworld/global/en/job/twntwdusp102186waltdisneyworldenglobal/lifeguard-walt-disney-world-availability-check | 2 | 3.92% |
| ever employed | 2 | 3.92% |

---

## 7. Top customer keywords **within** each major `PRODUCT_EXPERIENCE_PRODUCT` (n≥80, non-blank)

### CRM - Core (n=619, 7.38% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| job | 205 | 33.12% |
| phenom | 201 | 32.47% |
| candidate | 192 | 31.02% |
| crm | 138 | 22.29% |
| recruiter | 122 | 19.71% |
| candidates | 117 | 18.90% |
| jobs | 87 | 14.05% |
| profile | 74 | 11.95% |
| email | 73 | 11.79% |
| req | 69 | 11.15% |
| showing | 64 | 10.34% |
| hiring | 63 | 10.18% |
| status | 58 | 9.37% |
| requisition | 57 | 9.21% |
| list | 55 | 8.89% |
| open | 55 | 8.89% |
| system | 54 | 8.72% |
| currently | 54 | 8.72% |
| user | 53 | 8.56% |
| recruiters | 53 | 8.56% |
| data | 53 | 8.56% |
| within | 52 | 8.40% |
| example | 50 | 8.08% |
| add | 50 | 8.08% |
| field | 47 | 7.59% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| candidate profile | 37 | 5.98% |
| crm connect | 21 | 3.39% |
| phenom crm | 20 | 3.23% |
| hiring manager | 20 | 3.23% |
| job req | 19 | 3.07% |
| career site | 19 | 3.07% |
| linkedin crm | 18 | 2.91% |
| job requisition | 17 | 2.75% |
| candidate profiles | 16 | 2.58% |
| hiring status | 16 | 2.58% |
| email address | 14 | 2.26% |
| job posting | 13 | 2.10% |
| job fields | 12 | 1.94% |
| within phenom | 12 | 1.94% |
| open jobs | 12 | 1.94% |

### CRM - Profile (n=559, 6.67% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| candidate | 313 | 55.99% |
| profile | 219 | 39.18% |
| phenom | 191 | 34.17% |
| candidates | 155 | 27.73% |
| crm | 148 | 26.48% |
| email | 136 | 24.33% |
| job | 103 | 18.43% |
| status | 102 | 18.25% |
| profiles | 102 | 18.25% |
| application | 81 | 14.49% |
| employee | 70 | 12.52% |
| showing | 70 | 12.52% |
| hiring | 70 | 12.52% |
| merged | 69 | 12.34% |
| recruiter | 66 | 11.81% |
| ats | 65 | 11.63% |
| name | 63 | 11.27% |
| applied | 62 | 11.09% |
| internal | 61 | 10.91% |
| review | 57 | 10.20% |
| data | 56 | 10.02% |
| address | 56 | 10.02% |
| system | 55 | 9.84% |
| workday | 51 | 9.12% |
| merge | 48 | 8.59% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| candidate profile | 94 | 16.82% |
| email address | 49 | 8.77% |
| hiring status | 43 | 7.69% |
| candidate profiles | 34 | 6.08% |
| profile phenom | 21 | 3.76% |
| phenom candidate | 20 | 3.58% |
| candidate name | 19 | 3.40% |
| phone number | 17 | 3.04% |
| profile crm | 16 | 2.86% |
| profiles merged | 16 | 2.86% |
| crm profile | 16 | 2.86% |
| candidate applied | 16 | 2.86% |
| hiring manager | 15 | 2.68% |
| candidate email | 14 | 2.50% |
| status candidate | 13 | 2.33% |

### FSI - Job Synch (n=511, 6.09% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| job | 349 | 68.30% |
| phenom | 239 | 46.77% |
| jobs | 165 | 32.29% |
| site | 146 | 28.57% |
| posted | 128 | 25.05% |
| showing | 123 | 24.07% |
| workday | 119 | 23.29% |
| career | 115 | 22.50% |
| open | 98 | 19.18% |
| crm | 98 | 19.18% |
| posting | 88 | 17.22% |
| req | 82 | 16.05% |
| pull | 78 | 15.26% |
| requisition | 75 | 14.68% |
| closed | 71 | 13.89% |
| integration | 64 | 12.52% |
| careers | 61 | 11.94% |
| currently | 61 | 11.94% |
| ats | 60 | 11.74% |
| requisitions | 57 | 11.15% |
| recruiter | 56 | 10.96% |
| external | 50 | 9.78% |
| investigate | 49 | 9.59% |
| status | 48 | 9.39% |
| example | 47 | 9.20% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| career site | 96 | 18.79% |
| job pull | 59 | 11.55% |
| job posting | 47 | 9.20% |
| careers site | 33 | 6.46% |
| job req | 29 | 5.68% |
| open phenom | 26 | 5.09% |
| jobs posted | 24 | 4.70% |
| job requisition | 23 | 4.50% |
| job posted | 22 | 4.31% |
| job postings | 22 | 4.31% |
| phenom job | 22 | 4.31% |
| external career | 21 | 4.11% |
| site job | 20 | 3.91% |
| job sync | 19 | 3.72% |
| showing phenom | 19 | 3.72% |

### CRM - Messaging and Campaigns (n=510, 6.08% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| email | 286 | 56.08% |
| candidate | 174 | 34.12% |
| emails | 149 | 29.22% |
| phenom | 132 | 25.88% |
| candidates | 117 | 22.94% |
| sent | 102 | 20.00% |
| template | 97 | 19.02% |
| campaign | 84 | 16.47% |
| crm | 84 | 16.47% |
| received | 82 | 16.08% |
| send | 75 | 14.71% |
| templates | 68 | 13.33% |
| recruiter | 66 | 12.94% |
| job | 65 | 12.75% |
| sms | 64 | 12.55% |
| out | 63 | 12.35% |
| receiving | 59 | 11.57% |
| name | 58 | 11.37% |
| sending | 56 | 10.98% |
| receive | 56 | 10.98% |
| system | 52 | 10.20% |
| campaigns | 50 | 9.80% |
| profile | 48 | 9.41% |
| example | 47 | 9.22% |
| error | 47 | 9.22% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| email templates | 30 | 5.88% |
| email template | 27 | 5.29% |
| email address | 24 | 4.71% |
| candidate profile | 24 | 4.71% |
| receive email | 19 | 3.73% |
| email sent | 19 | 3.73% |
| hiring manager | 18 | 3.53% |
| emails sent | 17 | 3.33% |
| job alert | 16 | 3.14% |
| receiving emails | 16 | 3.14% |
| job alerts | 15 | 2.94% |
| email activity | 14 | 2.75% |
| email campaign | 14 | 2.75% |
| phone number | 14 | 2.75% |
| received email | 14 | 2.75% |

### FS Forms - Life Cycle Mgmt (n=508, 6.06% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| apply | 211 | 41.54% |
| application | 204 | 40.16% |
| candidate | 195 | 38.39% |
| phenom | 146 | 28.74% |
| job | 139 | 27.36% |
| candidates | 124 | 24.41% |
| email | 96 | 18.90% |
| applications | 82 | 16.14% |
| error | 75 | 14.76% |
| workday | 75 | 14.76% |
| site | 67 | 13.19% |
| internal | 67 | 13.19% |
| field | 65 | 12.80% |
| flow | 64 | 12.60% |
| applied | 61 | 12.01% |
| page | 59 | 11.61% |
| data | 57 | 11.22% |
| name | 56 | 11.02% |
| external | 56 | 11.02% |
| career | 55 | 10.83% |
| update | 55 | 10.83% |
| required | 52 | 10.24% |
| submit | 49 | 9.65% |
| req | 49 | 9.65% |
| profile | 48 | 9.45% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| apply flow | 43 | 8.46% |
| career site | 39 | 7.68% |
| email address | 27 | 5.31% |
| submit application | 24 | 4.72% |
| hosted apply | 21 | 4.13% |
| candidate profile | 20 | 3.94% |
| job application | 20 | 3.94% |
| candidate applied | 17 | 3.35% |
| first name | 16 | 3.15% |
| apply errors | 16 | 3.15% |
| internal candidate | 15 | 2.95% |
| apply job | 13 | 2.56% |
| phenom side | 13 | 2.56% |
| crm candidate | 12 | 2.36% |
| applied job | 12 | 2.36% |

### CMS (n=423, 5.05% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| page | 185 | 43.74% |
| site | 107 | 25.30% |
| widget | 107 | 25.30% |
| job | 103 | 24.35% |
| pages | 79 | 18.68% |
| cms | 77 | 18.20% |
| jobs | 70 | 16.55% |
| careers | 69 | 16.31% |
| career | 66 | 15.60% |
| text | 65 | 15.37% |
| change | 55 | 13.00% |
| phenom | 54 | 12.77% |
| update | 52 | 12.29% |
| mobile | 46 | 10.87% |
| video | 44 | 10.40% |
| currently | 43 | 10.17% |
| button | 43 | 10.17% |
| search | 43 | 10.17% |
| font | 42 | 9.93% |
| link | 41 | 9.69% |
| reference | 40 | 9.46% |
| showing | 39 | 9.22% |
| view | 37 | 8.75% |
| correctly | 37 | 8.75% |
| design | 37 | 8.75% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| career site | 52 | 12.29% |
| home page | 19 | 4.49% |
| design studio | 17 | 4.02% |
| careers site | 15 | 3.55% |
| screen recording | 14 | 3.31% |
| landing page | 14 | 3.31% |
| job page | 14 | 3.31% |
| mobile view | 12 | 2.84% |
| talent community | 12 | 2.84% |
| desktop view | 11 | 2.60% |
| job description | 11 | 2.60% |
| live site | 10 | 2.36% |
| job pages | 9 | 2.13% |
| jobs widget | 9 | 2.13% |
| search results | 8 | 1.89% |

### OnboardingX - Core (n=401, 4.78% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| candidate | 162 | 40.40% |
| onboarding | 150 | 37.41% |
| hire | 118 | 29.43% |
| re-push | 86 | 21.45% |
| email | 79 | 19.70% |
| offer | 79 | 19.70% |
| name | 76 | 18.95% |
| phenom | 70 | 17.46% |
| type | 63 | 15.71% |
| requisition | 56 | 13.97% |
| employee | 54 | 13.47% |
| date | 52 | 12.97% |
| start | 46 | 11.47% |
| sent | 45 | 11.22% |
| transfer | 45 | 11.22% |
| hcm | 42 | 10.47% |
| signed | 41 | 10.22% |
| req | 40 | 9.98% |
| full | 37 | 9.23% |
| tydy | 36 | 8.98% |
| letter | 36 | 8.98% |
| candidates | 35 | 8.73% |
| form | 35 | 8.73% |
| integration | 32 | 7.98% |
| status | 31 | 7.73% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| start date | 36 | 8.98% |
| offer letter | 35 | 8.73% |
| candidate full | 35 | 8.73% |
| type hire | 33 | 8.23% |
| full name | 31 | 7.73% |
| candidate email | 26 | 6.48% |
| candidate name | 24 | 5.99% |
| hire type | 23 | 5.74% |
| email address | 20 | 4.99% |
| hcm integration | 18 | 4.49% |
| signed offer | 16 | 3.99% |
| onboarding form | 15 | 3.74% |
| offer signed | 15 | 3.74% |
| phenom onboarding | 13 | 3.24% |
| candidate ats | 13 | 3.24% |

### Career Site – Platform Services (n=388, 4.63% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| site | 146 | 37.63% |
| job | 139 | 35.82% |
| page | 129 | 33.25% |
| career | 96 | 24.74% |
| careers | 68 | 17.53% |
| phenom | 66 | 17.01% |
| jobs | 65 | 16.75% |
| search | 64 | 16.49% |
| change | 53 | 13.66% |
| pages | 53 | 13.66% |
| text | 47 | 12.11% |
| link | 46 | 11.86% |
| candidate | 45 | 11.60% |
| update | 39 | 10.05% |
| apply | 38 | 9.79% |
| button | 36 | 9.28% |
| widget | 35 | 9.02% |
| currently | 34 | 8.76% |
| website | 33 | 8.51% |
| links | 32 | 8.25% |
| showing | 32 | 8.25% |
| external | 31 | 7.99% |
| user | 31 | 7.99% |
| email | 30 | 7.73% |
| add | 30 | 7.73% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| career site | 76 | 19.59% |
| careers site | 29 | 7.47% |
| external career | 18 | 4.64% |
| job posting | 15 | 3.87% |
| talent community | 14 | 3.61% |
| job page | 14 | 3.61% |
| search results | 13 | 3.35% |
| job search | 11 | 2.84% |
| job description | 11 | 2.84% |
| job alerts | 10 | 2.58% |
| search bar | 9 | 2.32% |
| job pages | 9 | 2.32% |
| job alert | 9 | 2.32% |
| home page | 8 | 2.06% |
| career website | 8 | 2.06% |

### Customer Analytics (n=279, 3.33% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| report | 186 | 66.67% |
| data | 118 | 42.29% |
| analytics | 105 | 37.63% |
| phenom | 82 | 29.39% |
| job | 66 | 23.66% |
| crm | 59 | 21.15% |
| candidates | 51 | 18.28% |
| reporting | 51 | 18.28% |
| candidate | 50 | 17.92% |
| showing | 44 | 15.77% |
| time | 42 | 15.05% |
| jobs | 42 | 15.05% |
| reports | 39 | 13.98% |
| date | 36 | 12.90% |
| builder | 36 | 12.90% |
| status | 35 | 12.54% |
| shows | 34 | 12.19% |
| pull | 34 | 12.19% |
| recruiter | 33 | 11.83% |
| number | 33 | 11.83% |
| hiring | 31 | 11.11% |
| example | 30 | 10.75% |
| noticed | 29 | 10.39% |
| source | 29 | 10.39% |
| usage | 29 | 10.39% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| report builder | 33 | 11.83% |
| usage report | 24 | 8.60% |
| crm usage | 22 | 7.89% |
| report report | 16 | 5.73% |
| analytics report | 16 | 5.73% |
| date range | 16 | 5.73% |
| traffic source | 13 | 4.66% |
| phenom analytics | 13 | 4.66% |
| report shows | 13 | 4.66% |
| applies report | 10 | 3.58% |
| career site | 10 | 3.58% |
| talent analytics | 10 | 3.58% |
| report analytics | 9 | 3.23% |
| job category | 9 | 3.23% |
| hiring funnel | 9 | 3.23% |

### Internal Mobility (n=274, 3.27% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| internal | 79 | 28.83% |
| employee | 74 | 27.01% |
| profile | 57 | 20.80% |
| job | 54 | 19.71% |
| site | 54 | 19.71% |
| phenom | 51 | 18.61% |
| career | 46 | 16.79% |
| employees | 40 | 14.60% |
| email | 37 | 13.50% |
| candidate | 37 | 13.50% |
| page | 36 | 13.14% |
| change | 32 | 11.68% |
| user | 29 | 10.58% |
| crm | 25 | 9.12% |
| remove | 24 | 8.76% |
| referral | 24 | 8.76% |
| access | 24 | 8.76% |
| currently | 23 | 8.39% |
| name | 23 | 8.39% |
| link | 23 | 8.39% |
| mobility | 22 | 8.03% |
| data | 22 | 8.03% |
| jobs | 22 | 8.03% |
| updated | 21 | 7.66% |
| feed | 21 | 7.66% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| career site | 28 | 10.22% |
| internal mobility | 22 | 8.03% |
| internal career | 20 | 7.30% |
| employee feed | 13 | 4.74% |
| employee profile | 11 | 4.01% |
| email address | 8 | 2.92% |
| mobility site | 8 | 2.92% |
| access internal | 8 | 2.92% |
| candidate profile | 8 | 2.92% |
| internal careers | 8 | 2.92% |
| hiring manager | 7 | 2.55% |
| internal candidate | 6 | 2.19% |
| job title | 6 | 2.19% |
| employee file | 6 | 2.19% |
| internal site | 6 | 2.19% |

### MX - Hiring (n=267, 3.18% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| hiring | 139 | 52.06% |
| manager | 120 | 44.94% |
| candidate | 119 | 44.57% |
| candidates | 76 | 28.46% |
| interview | 74 | 27.72% |
| evaluation | 61 | 22.85% |
| phenom | 59 | 22.10% |
| managers | 57 | 21.35% |
| job | 51 | 19.10% |
| profile | 50 | 18.73% |
| hrm | 49 | 18.35% |
| recruiter | 48 | 17.98% |
| email | 47 | 17.60% |
| req | 39 | 14.61% |
| interviewer | 38 | 14.23% |
| user | 38 | 14.23% |
| view | 37 | 13.86% |
| access | 36 | 13.48% |
| crm | 34 | 12.73% |
| sent | 33 | 12.36% |
| evaluations | 32 | 11.99% |
| review | 32 | 11.99% |
| received | 31 | 11.61% |
| completed | 29 | 10.86% |
| system | 29 | 10.86% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| hiring manager | 105 | 39.33% |
| hiring managers | 53 | 19.85% |
| candidate profile | 28 | 10.49% |
| manager portal | 14 | 5.24% |
| evaluation form | 11 | 4.12% |
| candidate name | 9 | 3.37% |
| interview feedback | 9 | 3.37% |
| manager view | 9 | 3.37% |
| internal number | 9 | 3.37% |
| confirm whether | 9 | 3.37% |
| manager dashboard | 8 | 3.00% |
| hiring leader | 8 | 3.00% |
| interview evaluation | 8 | 3.00% |
| email notification | 7 | 2.62% |
| hrm app | 7 | 2.62% |

### Hiring Status (n=235, 2.80% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| status | 125 | 53.19% |
| candidate | 123 | 52.34% |
| phenom | 120 | 51.06% |
| hiring | 81 | 34.47% |
| candidates | 81 | 34.47% |
| crm | 71 | 30.21% |
| workday | 66 | 28.09% |
| job | 61 | 25.96% |
| application | 48 | 20.43% |
| review | 44 | 18.72% |
| ats | 44 | 18.72% |
| req | 37 | 15.74% |
| error | 34 | 14.47% |
| showing | 33 | 14.04% |
| update | 33 | 14.04% |
| statuses | 33 | 14.04% |
| change | 32 | 13.62% |
| hsi | 32 | 13.62% |
| applied | 30 | 12.77% |
| integration | 30 | 12.77% |
| screen | 29 | 12.34% |
| recruiter | 29 | 12.34% |
| move | 28 | 11.91% |
| interview | 28 | 11.91% |
| between | 24 | 10.21% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| hiring status | 69 | 29.36% |
| candidate status | 18 | 7.66% |
| job application | 12 | 5.11% |
| hiring statuses | 12 | 5.11% |
| status change | 12 | 5.11% |
| phenom candidate | 10 | 4.26% |
| phenom crm | 10 | 4.26% |
| status phenom | 10 | 4.26% |
| candidate name | 9 | 3.83% |
| workday phenom | 9 | 3.83% |
| candidate profile | 9 | 3.83% |
| status changes | 9 | 3.83% |
| hiring manager | 9 | 3.83% |
| showing phenom | 9 | 3.83% |
| status hiring | 8 | 3.40% |

### CRM - Automation (n=185, 2.21% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| automation | 124 | 67.03% |
| candidate | 97 | 52.43% |
| candidates | 70 | 37.84% |
| status | 63 | 34.05% |
| email | 52 | 28.11% |
| automations | 48 | 25.95% |
| hiring | 47 | 25.41% |
| phenom | 43 | 23.24% |
| triggered | 39 | 21.08% |
| job | 37 | 20.00% |
| triggering | 35 | 18.92% |
| trigger | 32 | 17.30% |
| interview | 31 | 16.76% |
| sent | 28 | 15.14% |
| crm | 27 | 14.59% |
| out | 26 | 14.05% |
| recruiter | 25 | 13.51% |
| review | 24 | 12.97% |
| name | 24 | 12.97% |
| set | 23 | 12.43% |
| screening | 22 | 11.89% |
| moved | 22 | 11.89% |
| failed | 22 | 11.89% |
| send | 21 | 11.35% |
| change | 21 | 11.35% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| hiring status | 31 | 16.76% |
| automation triggering | 19 | 10.27% |
| automation triggered | 14 | 7.57% |
| hiring manager | 13 | 7.03% |
| automation failed | 12 | 6.49% |
| audit history | 10 | 5.41% |
| status change | 9 | 4.86% |
| candidate hiring | 9 | 4.86% |
| candidate profile | 9 | 4.86% |
| automation trigger | 8 | 4.32% |
| candidates moved | 8 | 4.32% |
| automation name | 8 | 4.32% |
| status changed | 7 | 3.78% |
| created automation | 7 | 3.78% |
| automation set | 7 | 3.78% |

### FS Integrations - Data Integration (n=145, 1.73% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| phenom | 87 | 60.00% |
| job | 41 | 28.28% |
| candidate | 35 | 24.14% |
| workday | 34 | 23.45% |
| data | 34 | 23.45% |
| integration | 33 | 22.76% |
| employee | 31 | 21.38% |
| update | 30 | 20.69% |
| candidates | 28 | 19.31% |
| email | 24 | 16.55% |
| profile | 21 | 14.48% |
| internal | 21 | 14.48% |
| api | 20 | 13.79% |
| support | 19 | 13.10% |
| updated | 18 | 12.41% |
| jobs | 18 | 12.41% |
| ats | 17 | 11.72% |
| crm | 17 | 11.72% |
| production | 17 | 11.72% |
| example | 16 | 11.03% |
| environment | 16 | 11.03% |
| ensure | 15 | 10.34% |
| out | 15 | 10.34% |
| showing | 15 | 10.34% |
| change | 15 | 10.34% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| candidate profile | 7 | 4.83% |
| email address | 7 | 4.83% |
| employee profile | 6 | 4.14% |
| staging environment | 6 | 4.14% |
| employee feed | 6 | 4.14% |
| phenom support | 6 | 4.14% |
| career site | 5 | 3.45% |
| job requisition | 5 | 3.45% |
| phenom api | 4 | 2.76% |
| api calls | 4 | 2.76% |
| phenom crm | 4 | 2.76% |
| internal mobility | 4 | 2.76% |
| between phenom | 4 | 2.76% |
| phenom integration | 4 | 2.76% |
| reach out | 4 | 2.76% |

### CRM - Events and University Recruiting (n=142, 1.69% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| event | 112 | 78.87% |
| events | 64 | 45.07% |
| candidates | 39 | 27.46% |
| registration | 37 | 26.06% |
| candidate | 32 | 22.54% |
| phenom | 32 | 22.54% |
| email | 30 | 21.13% |
| registered | 25 | 17.61% |
| sent | 23 | 16.20% |
| page | 21 | 14.79% |
| crm | 21 | 14.79% |
| showing | 21 | 14.79% |
| created | 20 | 14.08% |
| add | 19 | 13.38% |
| form | 17 | 11.97% |
| test | 17 | 11.97% |
| option | 16 | 11.27% |
| link | 16 | 11.27% |
| through | 15 | 10.56% |
| available | 15 | 10.56% |
| out | 15 | 10.56% |
| time | 14 | 9.86% |
| possible | 14 | 9.86% |
| career | 14 | 9.86% |
| missing | 14 | 9.86% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| event registration | 16 | 11.27% |
| registration form | 11 | 7.75% |
| event page | 11 | 7.75% |
| event organizer | 6 | 4.23% |
| registered event | 6 | 4.23% |
| candidates event | 6 | 4.23% |
| career site | 6 | 4.23% |
| events page | 5 | 3.52% |
| event candidates | 5 | 3.52% |
| create event | 5 | 3.52% |
| event name | 5 | 3.52% |
| event crm | 5 | 3.52% |
| event templates | 5 | 3.52% |
| sent candidates | 5 | 3.52% |
| registered candidates | 5 | 3.52% |

### Req & Offer (n=130, 1.55% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| offer | 56 | 43.08% |
| candidate | 35 | 26.92% |
| letter | 35 | 26.92% |
| job | 26 | 20.00% |
| req | 17 | 13.08% |
| phenom | 17 | 13.08% |
| template | 16 | 12.31% |
| field | 15 | 11.54% |
| fields | 14 | 10.77% |
| page | 13 | 10.00% |
| received | 12 | 9.23% |
| templates | 12 | 9.23% |
| available | 12 | 9.23% |
| update | 12 | 9.23% |
| hiring | 12 | 9.23% |
| signed | 12 | 9.23% |
| report | 11 | 8.46% |
| out | 11 | 8.46% |
| manager | 11 | 8.46% |
| add | 10 | 7.69% |
| status | 10 | 7.69% |
| email | 10 | 7.69% |
| api | 10 | 7.69% |
| option | 10 | 7.69% |
| change | 10 | 7.69% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| offer letter | 32 | 24.62% |
| offer letters | 7 | 5.38% |
| hiring manager | 7 | 5.38% |
| vertical api | 6 | 4.62% |
| signed offer | 6 | 4.62% |
| demand report | 5 | 3.85% |
| letter template | 5 | 3.85% |
| refresh vertical | 5 | 3.85% |
| drop down | 5 | 3.85% |
| umm edu | 5 | 3.85% |
| api refresh | 4 | 3.08% |
| candidate profile | 4 | 3.08% |
| vertical structure | 4 | 3.08% |
| offer template | 4 | 3.08% |
| e-signature document | 3 | 2.31% |

### Career Site – Templates & Views (n=121, 1.44% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| page | 44 | 36.36% |
| job | 35 | 28.93% |
| site | 32 | 26.45% |
| career | 24 | 19.83% |
| pages | 18 | 14.88% |
| search | 18 | 14.88% |
| email | 18 | 14.88% |
| candidate | 17 | 14.05% |
| careers | 17 | 14.05% |
| apply | 17 | 14.05% |
| widget | 16 | 13.22% |
| jobs | 15 | 12.40% |
| link | 12 | 9.92% |
| update | 12 | 9.92% |
| text | 12 | 9.92% |
| first | 12 | 9.92% |
| phenom | 12 | 9.92% |
| set | 11 | 9.09% |
| button | 11 | 9.09% |
| add | 11 | 9.09% |
| appears | 10 | 8.26% |
| change | 10 | 8.26% |
| section | 10 | 8.26% |
| changes | 10 | 8.26% |
| video | 9 | 7.44% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| career site | 18 | 14.88% |
| job alert | 6 | 4.96% |
| job category | 5 | 4.13% |
| job alerts | 5 | 4.13% |
| job description | 4 | 3.31% |
| home page | 4 | 3.31% |
| search results | 4 | 3.31% |
| landing page | 4 | 3.31% |
| apply job | 4 | 3.31% |
| job postings | 4 | 3.31% |
| page careers | 4 | 3.31% |
| apply flow | 4 | 3.31% |
| careers site | 4 | 3.31% |
| expected behavior | 3 | 2.48% |
| category pages | 3 | 2.48% |

### User Management (n=101, 1.20% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| phenom | 39 | 38.61% |
| access | 38 | 37.62% |
| user | 30 | 29.70% |
| users | 28 | 27.72% |
| hub | 21 | 20.79% |
| data | 18 | 17.82% |
| process | 15 | 14.85% |
| service | 15 | 14.85% |
| account | 15 | 14.85% |
| error | 14 | 13.86% |
| crm | 14 | 13.86% |
| email | 12 | 11.88% |
| hrit | 12 | 11.88% |
| client | 12 | 11.88% |
| update | 11 | 10.89% |
| name | 11 | 10.89% |
| hiring | 10 | 9.90% |
| time | 10 | 9.90% |
| cannot | 10 | 9.90% |
| currently | 10 | 9.90% |
| remove | 10 | 9.90% |
| roles | 9 | 8.91% |
| now | 9 | 8.91% |
| log | 9 | 8.91% |
| support | 8 | 7.92% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| service hub | 10 | 9.90% |
| hrit hub | 9 | 8.91% |
| data deletion | 6 | 5.94% |
| hiring manager | 6 | 5.94% |
| user access | 6 | 5.94% |
| hiring managers | 5 | 4.95% |
| churn process | 5 | 4.95% |
| data extraction | 5 | 4.95% |
| account name | 5 | 4.95% |
| access crm | 4 | 3.96% |
| phenom phans | 4 | 3.96% |
| access phenom | 4 | 3.96% |
| deletion date | 4 | 3.96% |
| contract end | 4 | 3.96% |
| date data | 4 | 3.96% |

### EX Platform (Other) (n=94, 1.12% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| employee | 34 | 36.17% |
| phenom | 34 | 36.17% |
| erm | 27 | 28.72% |
| manager | 25 | 26.60% |
| job | 19 | 20.21% |
| profile | 19 | 20.21% |
| employees | 18 | 19.15% |
| skills | 16 | 17.02% |
| email | 15 | 15.96% |
| role | 14 | 14.89% |
| skill | 14 | 14.89% |
| nitish | 14 | 14.89% |
| add | 13 | 13.83% |
| data | 12 | 12.77% |
| change | 11 | 11.70% |
| system | 10 | 10.64% |
| people | 10 | 10.64% |
| colella | 10 | 10.64% |
| through | 9 | 9.57% |
| find | 9 | 9.57% |
| name | 9 | 9.57% |
| file | 9 | 9.57% |
| stefania | 9 | 9.57% |
| report | 9 | 9.57% |
| sadaiya | 9 | 9.57% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| colella nitish | 10 | 10.64% |
| nitish sadaiya | 9 | 9.57% |
| people manager | 8 | 8.51% |
| stefania colella | 7 | 7.45% |
| phenom contacts | 7 | 7.45% |
| employee profile | 7 | 7.45% |
| phenom contact | 5 | 5.32% |
| employee feed | 5 | 5.32% |
| relevant skills | 4 | 4.26% |
| nitish sadayia | 4 | 4.26% |
| data phenom | 4 | 4.26% |
| contacts stefania | 4 | 4.26% |
| manager view | 4 | 4.26% |
| job title | 4 | 4.26% |
| kind diana | 3 | 3.19% |

### Chatbot (n=90, 1.07% of Jira-Yes)

| Keyword | SRs | % of this product |
|---------|-----|-------------------|
| chatbot | 67 | 74.44% |
| questions | 23 | 25.56% |
| job | 18 | 20.00% |
| bot | 17 | 18.89% |
| chat | 17 | 18.89% |
| question | 16 | 17.78% |
| site | 16 | 17.78% |
| staging | 16 | 17.78% |
| career | 16 | 17.78% |
| phenom | 15 | 16.67% |
| jobs | 11 | 12.22% |
| apply | 11 | 12.22% |
| change | 10 | 11.11% |
| provide | 9 | 10.00% |
| understand | 9 | 10.00% |
| data | 9 | 10.00% |
| response | 9 | 10.00% |
| website | 9 | 10.00% |
| external | 9 | 10.00% |
| internal | 9 | 10.00% |
| talent | 9 | 10.00% |
| currently | 9 | 10.00% |
| answer | 9 | 10.00% |
| candidate | 9 | 10.00% |
| page | 9 | 10.00% |

| Bigram | SRs | % of this product |
|--------|-----|-------------------|
| chat bot | 13 | 14.44% |
| career site | 11 | 12.22% |
| talent companion | 7 | 7.78% |
| something went | 4 | 4.44% |
| went wrong | 4 | 4.44% |
| external career | 4 | 4.44% |
| ask question | 4 | 4.44% |
| chatbot answering | 4 | 4.44% |
| staging environment | 4 | 4.44% |
| within chatbot | 4 | 4.44% |
| phenom support | 4 | 4.44% |
| phenom chatbot | 4 | 4.44% |
| chatbot questions | 3 | 3.33% |
| unanswered question | 3 | 3.33% |
| unanswered questions | 3 | 3.33% |
