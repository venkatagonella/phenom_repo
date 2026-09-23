# Snapshot — RX CRM theme split (sheet CSV only)

**Population:** `PRODUCT_EXPERIENCE` = Recruiter Experience (RX) **and** `JIRA_CREATED` = Yes **and** `PRODUCT_EXPERIENCE_PRODUCT` ∈ {CRM - Core, CRM - Messaging and Campaigns, CRM - Profile, CRM - Automation}

| Metric | Value |
|--------|-------|
| Rows | 1,580 |
| CRM - Core | 500 |
| CRM - Messaging and Campaigns | 459 |
| CRM - Profile | 455 |
| CRM - Automation | 166 |

**Method:** Exclusive first-match regex themes on `SHORT_DESCRIPTION`, then `SHORT_DESCRIPTION` + `DESCRIPTION` if no match. Theme labels paraphrase recurring ticket wording. **Unclassified / other** = no rule matched (not “no issue”). Percentages use the stated population as denominator (sums to 100% within each table).

**Source:** local CSV export of the canonical ServiceNow sheet only. No other documents.

## Overall (n = 1,580)

| Theme | Rows | % of feedback |
|-------|------|---------------|
| Unclassified / other | 426 | 27.0% |
| Candidate profile data / fields / tags / location / GDPR / purge | 166 | 10.5% |
| Campaigns / job alerts / subscriptions / spotlights | 142 | 9.0% |
| Screening / interview / scheduling / offer / notifications | 104 | 6.6% |
| Hiring status / pipeline / stages / lead status / progress status | 101 | 6.4% |
| Jobs / requisitions / applications / posting | 93 | 5.9% |
| Email not sending / not receiving / spam / sender / opt-in / bounce | 90 | 5.7% |
| Profile merge / unmerge / duplicates / candidate disappeared | 88 | 5.6% |
| SMS / WhatsApp | 88 | 5.6% |
| Automation not triggering / failing / wrongly triggered | 88 | 5.6% |
| Email template content / hyperlinks / branding / placeholders | 82 | 5.2% |
| Forwarding / LinkedIn / ATS↔CRM sync | 57 | 3.6% |
| Activity / notes / UI display issues | 30 | 1.9% |
| Search / lists / filters / export / AI Discovery | 13 | 0.8% |
| Access / CRM not opening / permissions | 12 | 0.8% |

## CRM - Core (n = 500)

| Theme | Rows | % |
|-------|------|---|
| Unclassified / other | 189 | 37.8% |
| Jobs / requisitions / applications / posting | 72 | 14.4% |
| Candidate profile data / fields / tags / location / GDPR / purge | 60 | 12.0% |
| Forwarding / LinkedIn / ATS↔CRM sync | 40 | 8.0% |
| Screening / interview / scheduling / offer / notifications | 38 | 7.6% |
| Hiring status / pipeline / stages / lead status / progress status | 28 | 5.6% |
| Campaigns / job alerts / subscriptions / spotlights | 22 | 4.4% |
| Activity / notes / UI display issues | 12 | 2.4% |
| Email template content / hyperlinks / branding / placeholders | 9 | 1.8% |
| Access / CRM not opening / permissions | 8 | 1.6% |
| Email not sending / not receiving / spam / sender / opt-in / bounce | 6 | 1.2% |
| Profile merge / unmerge / duplicates / candidate disappeared | 6 | 1.2% |
| SMS / WhatsApp | 5 | 1.0% |
| Search / lists / filters / export / AI Discovery | 3 | 0.6% |
| Automation not triggering / failing / wrongly triggered | 2 | 0.4% |

## CRM - Messaging and Campaigns (n = 459)

| Theme | Rows | % |
|-------|------|---|
| Campaigns / job alerts / subscriptions / spotlights | 107 | 23.3% |
| SMS / WhatsApp | 79 | 17.2% |
| Unclassified / other | 77 | 16.8% |
| Email not sending / not receiving / spam / sender / opt-in / bounce | 71 | 15.5% |
| Email template content / hyperlinks / branding / placeholders | 67 | 14.6% |
| Screening / interview / scheduling / offer / notifications | 26 | 5.7% |
| Candidate profile data / fields / tags / location / GDPR / purge | 11 | 2.4% |
| Automation not triggering / failing / wrongly triggered | 7 | 1.5% |
| Activity / notes / UI display issues | 6 | 1.3% |
| Hiring status / pipeline / stages / lead status / progress status | 3 | 0.7% |
| Search / lists / filters / export / AI Discovery | 2 | 0.4% |
| Forwarding / LinkedIn / ATS↔CRM sync | 1 | 0.2% |
| Jobs / requisitions / applications / posting | 1 | 0.2% |
| Access / CRM not opening / permissions | 1 | 0.2% |

## CRM - Profile (n = 455)

| Theme | Rows | % |
|-------|------|---|
| Unclassified / other | 138 | 30.3% |
| Candidate profile data / fields / tags / location / GDPR / purge | 86 | 18.9% |
| Profile merge / unmerge / duplicates / candidate disappeared | 80 | 17.6% |
| Hiring status / pipeline / stages / lead status / progress status | 57 | 12.5% |
| Screening / interview / scheduling / offer / notifications | 24 | 5.3% |
| Jobs / requisitions / applications / posting | 15 | 3.3% |
| Forwarding / LinkedIn / ATS↔CRM sync | 13 | 2.9% |
| Campaigns / job alerts / subscriptions / spotlights | 10 | 2.2% |
| Activity / notes / UI display issues | 9 | 2.0% |
| Email not sending / not receiving / spam / sender / opt-in / bounce | 7 | 1.5% |
| Automation not triggering / failing / wrongly triggered | 6 | 1.3% |
| Search / lists / filters / export / AI Discovery | 4 | 0.9% |
| Access / CRM not opening / permissions | 3 | 0.7% |
| SMS / WhatsApp | 2 | 0.4% |
| Email template content / hyperlinks / branding / placeholders | 1 | 0.2% |

## CRM - Automation (n = 166)

| Theme | Rows | % |
|-------|------|---|
| Automation not triggering / failing / wrongly triggered | 73 | 44.0% |
| Unclassified / other | 22 | 13.3% |
| Screening / interview / scheduling / offer / notifications | 16 | 9.6% |
| Hiring status / pipeline / stages / lead status / progress status | 13 | 7.8% |
| Candidate profile data / fields / tags / location / GDPR / purge | 9 | 5.4% |
| Email not sending / not receiving / spam / sender / opt-in / bounce | 6 | 3.6% |
| Jobs / requisitions / applications / posting | 5 | 3.0% |
| Email template content / hyperlinks / branding / placeholders | 5 | 3.0% |
| Search / lists / filters / export / AI Discovery | 4 | 2.4% |
| Activity / notes / UI display issues | 3 | 1.8% |
| Campaigns / job alerts / subscriptions / spotlights | 3 | 1.8% |
| Forwarding / LinkedIn / ATS↔CRM sync | 3 | 1.8% |
| Profile merge / unmerge / duplicates / candidate disappeared | 2 | 1.2% |
| SMS / WhatsApp | 2 | 1.2% |
