# Jira Ticket Classification: parents and children

Single source of truth for the recommended **sub-classification (child)**. Used by the SR triage agent, `sr_triage.py validate`, `child-tiers.py` and the SR Prevention dashboard. Rules for *choosing* are in [`../rulebook.md`](../rulebook.md) §5.

**Vocabulary.** These are the values the Jira field Ticket Classification (`customfield_18695`, a cascading select) actually uses on tickets (sheet columns `JIRA - Ticket Classification` / `jira_ticket_classification_child`, and the ServiceNow equivalent), checked on 2026-10-10. The live Jira option list has not been checked yet because the Atlassian connector was down. Recheck it with `getJiraIssueTypeMetaWithFields` (PHEM) when available.
- Values marked *(Confluence only)* are on the Confluence page "Ticket Classification – Global Field" but have not been seen on a ticket. Valid, but prefer the values used in Jira.
- Some options contain a comma but are **one** value: "Usability, Value KPIs missing" and "Library, Framework Dependency".
- Filed spelling fixes before comparing: Non-intutive → Non-intuitive; Localization → Localisation; Accesibility → Accessibility; Security-Related Issues → Code Issues › Security.

---

## Product & Knowledge Issues — it works as designed; the gap is knowledge, capability or self-service

| Child | Use when | Not when | Examples |
|---|---|---|---|
| **Documentation** | The answer existed; the customer needed an explanation, a how-to or a pointer (O-HOWTO) | They need a change done for them (→ Self-Service Missing) | CS0324550 Email changes; CS0322486 Proficiency-level answers in apply |
| **Non-intuitive Product Behaviour** | Expected behaviour that surprises users: the product did what it should, but it isn't obvious why | Behaviour is actually wrong (→ Code Issues) | CS0322832 Capital names; CS0326108 free slots shown as busy |
| **Self-Service Missing** | Support or Engineering did a one-off change the customer can't do themselves: data correction, deletion, purge, unmerge, closing jobs, adding a picklist value, enabling a field for export or filters, provisioning access (O-SELF-SERVICE) | A tenant setting was simply wrong (→ Configuration Issues) | CS0333936 Profile unmerge; CS0330087 list of automation failures; CS0322602 forward-candidate template |
| **Product Requirement** | The customer needs a capability the product doesn't have; a feature request or product feedback (O-CAPABILITY) | It existed and broke (→ Code Issues) | CS0331148 lead-to-application automation by traffic source; CS0344702 project stage from candidate fields |
| **Usability, Value KPIs missing** | The feature exists but is hard to use, or the customer can't see the value or metric they need | It is missing entirely (→ Product Requirement) | CS0320976 name mismatch between Phenom and Engage |
| **Inter Product Dependency** | The behaviour depends on another Phenom product's setup or data (e.g. Scheduling, Apply, Integrations) | A third-party system failed (→ External Dependency Issues) | — |

**Documentation vs Non-intuitive:** a how-to or "where is X" question is **Documentation**. "It worked as configured, but that surprised the customer" (Engineering or Support explains why) is **Non-intuitive Product Behaviour**.

## Configuration Issues — a tenant setting, flag, permission or mapping was wrong or missing

| Child | Use when | Not when |
|---|---|---|
| **Configuration Error** | A setting, flag, role permission, mapping or template configuration is wrong or missing in the tenant (O-FLAG, O-SEED, O-HOWTO-CHANGE) | The setting exists in staging but was never moved to production (→ Config Move Miss) |
| **Config Move Miss** | Configured in staging, missing or different in production; a promotion was missed (O-PROD-CONFIG) | Never configured anywhere (→ Configuration Error) |
| **Incorrect Discovery** | The requirement was captured wrongly during implementation or discovery, so the setup reflects the wrong need | A plain setting mistake (→ Configuration Error) |
| Configuration Missed *(Confluence only)* | A setting the customer needs was never configured. Jira files this as Configuration Error, so prefer that | It was configured in staging but not production (→ Config Move Miss) |
| Wrong Configuration *(Confluence only)* | A setting was configured with the wrong value. Jira files this as Configuration Error, so prefer that | The requirement itself was captured wrongly (→ Incorrect Discovery) |

Examples: CS0348347 scheduling automation shows no templates (Config Move Miss); CS0326819 automation did not trigger because of a filter setting (Configuration Error).

## Code Issues — supported behaviour fails and needs an engineering fix

| Child | Use when | Not when |
|---|---|---|
| **Functionality** | A feature doesn't do what it is designed to do: an action isn't performed, a button or control is missing after a deploy, a builder field is offered but doesn't work (O-UI-MISSING, O-BUILDER-FIELD) | It works as designed but surprises users (→ Product & Knowledge › Non-intuitive Product Behaviour) |
| **Data Quality** | The system created wrong, malformed, duplicate or junk data, or mishandles missing values in conditions and filters (O-NULL-FILTER) | The customer or the ATS sent the bad data (→ Configuration Issues or External Dependency Issues) |
| **Data Synchronization** | Data doesn't sync between Phenom services or with an external system, or events are processed out of order (O-SYNC-FAIL, O-AUTO-LATE without platform load) | The sync is slow because of infrastructure load (→ Ops › Infra Scaling) |
| **Data Pipeline** | Events or data never arrive in the next step: an ingestion or event pipeline drops them (e.g. notification events lost) | The events arrive but are processed wrongly (→ Functionality) |
| **Data Dependency** | The feature fails because data it depends on is missing or not ready upstream | The upstream system is a third party that failed (→ External Dependency Issues) |
| **Data Loss** | Data was deleted, overwritten or lost by the system | A user or a requested purge removed it (→ Product & Knowledge or Configuration) |
| **Performance** | A page or job is slow, times out or fails under load inside the application code | The cause is infrastructure capacity (→ Ops › Infra Scaling) |
| **API** | A Phenom API returns wrong results, wrong formats or errors to its caller | A third-party API failed (→ External Dependency › API Failure) |
| **Accessibility** | Content can't be opened or viewed (attachments, resumes or PDFs don't load), or an assistive-technology defect | The layout is merely awkward (→ User Experience › Layout) |
| **Customization** | A customer-specific customization or custom code stops working | The standard product behaviour fails for everyone (→ Functionality) |
| **Accuracy** | AI, matching, parsing or scoring output is wrong (e.g. fit score, resume parsing, recommendations) | The input data was wrong (→ Data Quality) |
| Localisation/I8n *(Confluence only)* | Translated text or locale handling breaks in code (wrong language served, locale not applied) | The translation wording is wrong (→ User Experience › Localisation / i18n) |
| Prompt *(Confluence only)* | An AI prompt produces wrong or unsafe output and the prompt must change | The model's matching or scoring is wrong (→ Accuracy) |
| Security *(Confluence only)* | Access control, data exposure or privacy defects in the product; also filed "Security-Related Issues" (Access Issue, Data Privacy Concern) | A role was simply configured wrongly (→ Configuration Error) |

## User Experience Issues — the UI itself is the problem

| Child | Use when | Not when |
|---|---|---|
| **Layout** | Elements are misplaced, overlapping, cut off or hard to scan on the screen | The element doesn't work (→ Code › Functionality) |
| **Navigation** | Users can't find where something lives or how to get there; menus, tabs or links lead to the wrong place | The page is missing because of permissions (→ Configuration or Role & Access) |
| **User Flow & Task Completion** | A multi-step task is confusing or takes too many steps, so users abandon it or do it wrong | A step fails with an error (→ Code › Functionality) |
| **Accessibility** | The UI is hard to use with a keyboard, screen reader or low vision (contrast, focus, labels) | Content fails to load (→ Code › Accessibility) |
| **Responsiveness** | The screen breaks or is unusable on smaller screens, mobile or zoom | It is slow (→ Code › Performance) |
| **Content & Microcopy** | Labels, help text, error messages or instructions are unclear, misleading or missing | The wording itself is fine but the customer needs to be told how it works (→ Product & Knowledge › Documentation) |
| **Localisation / i18n** | Translated UI text is missing, wrong or truncated in another language | The locale isn't applied at all because of a code defect (→ Code › Localisation/I8n) |

## External Dependency Issues — a third party failed

| Child | Use when | Not when |
|---|---|---|
| **API Failure** | A third-party API (ATS, HRIS, calendar, messaging provider) returned an error or was down | The Phenom API failed (→ Code › API) |
| **API Timeout** | A third-party API didn't respond in time | Phenom's own services were slow (→ Code › Performance or Ops) |
| **Invalid API Response** | A third party returned data in an unexpected shape or with wrong values (e.g. the ATS returned an error payload or bad field values) | Phenom mapped good data wrongly (→ Configuration Error) |
| **Library, Framework Dependency** | A third-party library or framework Phenom uses caused the failure (version change, deprecated component) | Our own code is at fault (→ Code Issues) |
| SFTP Issue *(Confluence only)* | A file transfer via SFTP failed (credentials, connection, file not delivered) | The file arrived but its content was wrong (→ Invalid API Response or Configuration) |
| Webhook Issue *(Confluence only)* | A third-party webhook didn't fire or reached Phenom malformed | Phenom's own event pipeline dropped it (→ Code › Data Pipeline) |

## Ops Issues — infrastructure

| Child | Use when | Not when |
|---|---|---|
| **Infra Scaling - Capacity planning** | Load, capacity or queue lag on the platform caused slowness, delays or failures (O-AUTO-LATE when platform load is named) | One feature's code is slow (→ Code › Performance) |
| **Incorrect Infra Configuration** | An environment, server, network or infrastructure setting was wrong (e.g. a service not deployed to a region, wrong environment variable) | A tenant setting in the product was wrong (→ Configuration Issues) |
| CI/CD Pipeline *(Confluence only)* | A build or deployment pipeline failure caused the issue (failed or partial release) | The released code itself is buggy (→ Code Issues) |

Jira often files Ops with no child; recommend one anyway.

---

## How the child is chosen (summary of rulebook §5)

1. **Inherit from Jira:** the recommended parent equals the Jira-filed parent and the Jira child is valid → take the Jira child. Source `jira`.
2. **Inherit from Support:** else, the recommended parent equals the ServiceNow-filed parent and that child is valid → take it. Source `support`.
3. **Rule-implied:** else, a rule id the agent recorded implies the child (table in §5). Source `rule <id>`.
4. **Agent:** else, the agent picks from this file with a one-line reason. Source `agent`. A doubt about the child alone is not a PM review reason.

When a PM corrects a child in review, add that ticket as an example above.
