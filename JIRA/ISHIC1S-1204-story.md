# Story: Career site translations for 2 system job fields

**Source:** [ISHIC1S-1204](https://phenompeople.atlassian.net/browse/ISHIC1S-1204)  
**Customer:** Siemens Healthineers (`SHDSHWUS`)  
**ServiceNow:** CS0345853  
**Related (out of scope for this story):** [ISHIC1S-1044](https://phenompeople.atlassian.net/browse/ISHIC1S-1044) — translations for 4 additional job fields (track separately; do not block that work on this story)

---

## Problem (from source ticket)

On the **internal and external career site**, filter options and job requisition field values for **two system job fields** stay in English. There is also **no option to provide translations** for them. This is called out as a legal compliance need for fully translated sites (e.g. France, Germany).

Fields called out as not translated (example: German locale):

1. **Location** — countries, states, and cities show English only  
2. **Job type** — English only  

---

## User Story

User Story: As a job seeker on the Siemens Healthineers internal or external career site, I want Location and Job type values (in filters and on the job requisition) shown in my selected locale language so that the career site meets legal translation requirements and I can understand job filters and details in my language.

Acceptance Criteria:

Scenario: Location values appear in the selected locale on filters and job details  
Given: the career site (internal or external) is viewed in a locale listed under Locales in scope  
When: I open location filters or view location fields on a job requisition  
Then: country, state, and city values are shown in that locale language (not English-only)

Scenario: Job type values appear in the selected locale on filters and job details  
Given: the career site (internal or external) is viewed in a locale listed under Locales in scope  
When: I open job type filters or view the job type field on a job requisition  
Then: job type values are shown in that locale language (not English-only)

Scenario: Ability to supply translations for these system fields  
Given: translations are needed for Location and Job type system job fields  
When: an authorized admin or configuration path is used to manage translations for these fields  
Then: there is a supported way to provide and maintain translations for Location and Job type (the ticket states there is currently no option to provide translations)

Scenario: Critical locales (already live — legal compliance)  
Given: the site locale is German (Germany) or French (France)  
When: I use Location or Job type filters, or view those fields on a job  
Then: values are translated for that locale

Scenario: Urgent locales (already live)  
Given: the site locale is French (Global) or Spanish (Spain)  
When: I use Location or Job type filters, or view those fields on a job  
Then: values are translated for that locale

Scenario: Important locales (go-live scheduled for 2026-11-26)  
Given: the site locale is Japanese (Japan), Italian (Italy), Slovak (Slovakia), Korean (South Korea), or Portuguese (Brazil)  
When: I use Location or Job type filters, or view those fields on a job  
Then: values are translated for that locale in time for the 2026-11-26 go-live

Considerations:

1. Localization  
   This story is localization work. Location (country/state/city) and Job type must be translated for all locales listed in scope below. User-facing filter labels and field values on both internal and external career sites must match the selected locale.

2. Analytics / Data Storage  
   N/A for new analytics events based on the source ticket — the ask is translated display of existing system field values and a way to provide those translations. Persist translations in the product’s existing translation / configuration store for system job fields so they are available on career site filters and job requisition display. No new Snowflake/reporting requirement is stated in ISHIC1S-1204.

---

## Locales in scope (from source ticket)

| Priority | Locales | Notes from ticket |
|----------|---------|-------------------|
| Critical | German (Germany), French (France) | Already live; legal compliance |
| Urgent | French (Global), Spanish (Spain) | Already live |
| Important | Japanese (Japan), Italian (Italy), Slovak (Slovakia), Korean (South Korea), Portuguese (Brazil) | Go-live scheduled for **2026-11-26** |

---

## Scope boundaries (from source ticket only)

**In scope**

- Internal career site and external career site  
- System fields: **Location** (countries, states, cities) and **Job type**  
- Display in filters and on job requisition fields  
- Providing a way to supply translations for these two system fields  

**Out of scope for this story**

- The **4 additional job fields** tracked in ISHIC1S-1044 (keep separate so that work is not delayed if this story takes longer — per comment on ISHIC1S-1204)

---

## Open items from source (not invented)

- Ticket asks for an **ETA** (not provided in the ticket body).  
- Exact translation content / glossary is not attached in the ticket text; delivery depends on approved translations for the listed locales.
