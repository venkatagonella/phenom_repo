# SR triage rulebook

**Version:** v7 · 2026-10-10 · used by `skills/sr-triage/SKILL.md`
**Owner:** Sebastian Niewöhner (RX). Changes bump the version; the agent stamps the version on every row it writes.

One rulebook, one agent, one recommendation per ticket. It replaces the Service Sarah keyword rules and the ad-hoc Claude rubrics. It consolidates what already existed — it does not invent new policy:

| Topic | Source this rulebook draws on |
|---|---|
| Decision procedure, locked overrides | Support Ticket Triage Classification Specification v1.0 (§6, §7, §10) |
| Service request vs defect | `_shared/type-rules.md`, sheet Legend ("Question retired") |
| Product experience and product **names** | `policies/jira-constants.md` (Product Experience : Product) — the only source |
| Product **routing** (which product a ticket belongs to) | `rx/areas.md` |
| Products shown in the SR Prevention tool | `scope.json` |
| Jira Ticket Classification | Confluence "Ticket Classification – Global Field" (page 56466505741) + sheet Legend |
| Level 1 / level 2 categories | Sheet **Product Taxonomy** tab (read live each run); L1 definitions on the sheet Constants tab |
| Confidence and PM review | `_shared/review-clarity.md` |

## 1. What the agent produces (sheet columns)

One object per ticket. Column names are the sheet headers; the writer finds them by name.

| Field | Sheet column | Allowed values |
|---|---|---|
| `type` | Recommendation Ticket Type | `Service Request` · `Bug-Customer` |
| `product_experience` | Recommendation Product Experience | any experience in `jira-constants.md` |
| `product` | Recommendation Product Area | a product under that experience in `jira-constants.md` |
| `jira_classification` | Recommendation JIRA - Ticket Classification | `Code Issues` · `User Experience Issues` · `Product & Knowledge Issues` · `Configuration Issues` · `External Dependency Issues` · `Ops Issues` |
| `l1` | Recommendation L1 - Category | one of the 10 L1 categories |
| `l2` | Recommendation L1 - Sub-Category | an `active` or `proposed` L2 of that product + L1 on the Product Taxonomy tab |
| `reasoning` | Recommendation Reasoning | 1–2 sentences (see §8) |
| `confidence` | Recommendation Conficence Level | `high` · `medium` · `low` |
| `pm_review` | Recommendation PM Review Required | `TRUE` · `FALSE` |
| — | Recommendation Status | always `proposed` (only a PM sets `reviewed`) |
| — | Recommendation Analysed By / On | `SR Triage Agent` / run date |
| — | matched_rules | current version + the rule ids applied, e.g. `rulebook v6; O-AUTOMATION; R-ROUTE-PRIVACY` |

The Jira classification **child** is deferred (stage 2).

## 2. Decision procedure (in this order)

1. **Requested outcome.** Write privately: "The customer wants Phenom to …". Never classify from the symptom or title alone ("email not received" can be a defect, suppression, configuration, a provider issue or expected behaviour).
2. **Working as designed?** Use the full Details: problem, discussions, solution, RCA, engineering fix. Evidence order: customer outcome → observed behaviour → Support investigation/resolution → engineering RCA/fix → native SN/Jira fields → component → title. Native fields are weak signals.
3. **Who did or must do the work?** Support-only routine work or a Support data/config correction → Service Request. Product, code or platform fix → Bug-Customer.
4. **Type** (§3) → **product** (§4) → **Jira classification** (§5) → **L1/L2** (§6) → **confidence and review** (§7).

## 3. Type: Service Request vs Bug-Customer

- **Bug-Customer** = supported behaviour fails and needs an engineering code/data fix: regression after deploy, wrong system result, wrong automation action, expected notification not sent, UI control missing after deploy, systemic data corruption.
- **Engineering corrected the system's own wrong result → Bug-Customer.** A code fix, patch, hotfix, or engineering repair of system-created bad data is Bug-Customer even when Support closed the case as a request. One-off fulfillment routed through Engineering can still be a Service Request under O-UNMERGE or O-SELF-SERVICE.
- **Classify by the final resolution**, not the opening ask: an enablement request that turns into a confirmed defect is Bug-Customer; a reported bug that turns out to be configuration or expected behaviour is a Service Request.
- **Service Request** = it works as designed, or the work is Support/ops fulfilment. Includes how-to and clarification (Question is retired — it is a Service Request), configuration and admin tasks, data corrections Support can make, feature enablement, managed-service and no-cost MSR work, and requests for capabilities the product does not have.

Locked overrides (spec §7, `type-rules.md`):

| Id | Pattern | Result |
|---|---|---|
| O-UNMERGE | Unmerge incorrectly merged profiles | Service Request · CRM - Profile (a systemic bad-merge pattern is a separate defect) |
| O-UI-MISSING | UI control missing after a deploy | Bug-Customer · Code Issues |
| O-FLAG | Tenant feature-flag enablement | Service Request · Configuration Issues |
| O-HOWTO | How-to / "is this possible?" with nothing broken | Service Request · Product & Knowledge Issues |
| O-HOWTO-CHANGE | Question followed by an explicit change request | Service Request · Configuration Issues |
| O-SYNC-MANUAL | ATS↔CRM sync gap Support can correct | Service Request |
| O-SYNC-FAIL | Sync gap Support cannot correct, integration failure | Bug-Customer · Code Issues |
| O-SEED | Support seeds/maps fields, filters, watchlists, hiring statuses | Service Request · Configuration Issues |
| O-AUTOMATION | Automation not firing / wrong action / expected email not sent | Bug-Customer · CRM - Automation — **except** when expected behaviour, invalid customer configuration, suppression or consent rule, external provider failure, or unsupported use case → Service Request |
| O-CONTENT | Support updates template, branding, logo or copy | Service Request · route to the template owner under R-ROUTE-OWNER — **except** sent output differs from configured content → Bug-Customer |

PM decisions from the CRM Automation review (2026-10-05, rulebook v5):

| Id | Pattern | Result |
|---|---|---|
| O-AUTO-LATE | The event (status, field change, ATS update) reached the automation after it had already evaluated, so it did not fire or fired late | Bug-Customer · Code Issues (Ops Issues when the details name platform load, queue lag or capacity). Only when the details prove the ATS sent the events in that order is it a Service Request · External Dependency Issues |
| O-NULL-FILTER | A missing, blank or malformed value breaks a condition or filter: a blank opt-in treated as a match, a location without coordinates, a status with a trailing space | Bug-Customer · Code Issues. The product must handle missing values safely. **Scope (v6):** conditions and filters only. A missing value elsewhere (placeholder, locale, template field) is not a general pattern: defect when the product claims to support the case and fails, O-CAPABILITY when it does not; set `pm_review = TRUE` when the details don't say which |
| O-BUILDER-FIELD | The automation builder offers a field (e.g. a derived field such as "Hiring Stage and Status") that does not work in conditions or filters | Bug-Customer · Code Issues, even when Engineering calls the field unsupported: offering it is the defect (PM decision v6) |
| O-JIRA-OPEN | The Jira is in any open status (Open, Eng Triage, In Development, In QA, Reporter Review, Confirm Resolution — anything but Done / Closed / Resolved; v6) but the evidence so far points to configuration or expected behaviour | Classify on the evidence so far, set `pm_review = TRUE`, and say "re-check when Jira closes" in the reasoning. The nightly run re-classifies the ticket once the Jira is closed |
| O-CAPABILITY | The customer needs something the product does not offer (an action missing on a trigger, a template setting that does not exist, an export column that does not show the needed value, sender name customisation) | Service Request · Product & Knowledge Issues (child: Product Requirement). It is a new feature request, not a defect |
| O-PROD-CONFIG | A setting, branding or database configuration is missing in production (e.g. configured only in staging) | Configuration Issues. Service Request if it was never set up in production; Bug-Customer if it worked before and broke (regression) |

## 4. Product experience and product

Names come **only** from `policies/jira-constants.md`. Start from the filed product (ServiceNow component or Jira product area, translated to the Jira name), then move it only when a routing rule or the ticket content clearly says it belongs elsewhere.

Routing rules (`rx/areas.md`, spec §8):

| Id | Signal | Product |
|---|---|---|
| R-ROUTE-PRIVACY | GDPR, CCPA, DSAR, erasure, purge, retention, privacy export, data-storage consent, privacy pipeline failure — the ticket content must be about privacy; a GDPR sub-component alone is not enough | Recruiter Experience (RX) · Compliance |
| R-ROUTE-ACCESS | Roles, permissions, RBAC, SSO, user accounts, allowlisting, scopes/departmentalization, record visibility blocked by role or hiring team | Recruiter Experience (RX) · CRM - Role & Access Management (L2s: Custom roles & permissions · Scopes & departmentalization · Record visibility · User accounts & SSO · Access audits & user reports · Access feature settings). Profile visibility driven by candidate consent stays CRM - Profile ("Profile access & visibility") |
| R-ROUTE-MSG | SMS/WhatsApp/email consent, unsubscribe, suppression, sender identity, delivery, campaigns, communication templates, campaign analytics | Recruiter Experience (RX) · CRM - Messaging and Campaigns |
| R-ROUTE-PROFILE | Candidate identity, profile data, merge/unmerge, profile source, resumes, attachments, profile sync | Recruiter Experience (RX) · CRM - Profile |
| R-ROUTE-CORE | Jobs, fields, filters, watchlists, hiring-status pipeline/settings configuration and manual status changes, projects, lifecycle operations, core CRM configuration | Recruiter Experience (RX) · CRM - Core |
| R-ROUTE-STATUS-SYNC | Hiring status mismatches, unmapped or unchangeable statuses driven by ATS/apply events on a candidate | Recruiter Experience (RX) · CRM - Profile ("Hiring status sync on profile") |
| R-ROUTE-AUTO | Triggers, conditions, actions, recipes, execution, automation-driven status/tag changes and notifications | Recruiter Experience (RX) · CRM - Automation |
| R-ROUTE-EVENTS | Events, event registration/forms, university recruiting | Recruiter Experience (RX) · CRM - Events and University Recruiting |
| R-ROUTE-HI | Interview scheduling, interview intelligence, X+ screening, voice agent screening | Hiring Intelligence · the matching product |
| R-ROUTE-OUT | Clearly another experience (e.g. assessments → Hiring Automations · Hiring Automations - Assessments; requisitions/offers → Manager Experience (MX) · Req & Offer; ATS integrations → Integration Experience (IX); career site → Candidate Experience (CX)) | that experience and product from `jira-constants.md` |

**R-ROUTE-EXPORT (v6):** candidate and data exports, one-off pulls and report extracts stay in CRM - Automation › Data & records › Exports & data extracts — the Automation pod owns exports. This wins over R-ROUTE-OWNER and R-ROUTE-CORE for exports.

**R-ROUTE-ACCESS wins (v6):** every RX access question — module access (e.g. Automation Center), roles, permissions, feature access — goes to CRM - Role & Access Management, even when the product has its own access L2 (those are retired). Profile visibility driven by candidate consent stays CRM - Profile.

**Routing decisions (2026-10-05):** PhenomHire requisition form, fields and status → Manager Experience (MX) · Req & Offer. High-volume hiring (HVH) apply/workflow questions → Hiring Automations · Hiring Automations - Core (for now). Restricting exports by role → CRM - Role & Access Management (who may export, not the export). Duplicate or wrong interviewer records and interview data that differs between candidate, interviewer and calendar → Hiring Intelligence · Scheduling › Data & records › Interview discrepancies. Agency portal and vendor submissions → CRM - Core › Experience surfaces › Agency Portal. Job-specific / application field answers not shown on the profile → CRM - Profile › Experience surfaces › Job & application field display. Security and compliance questionnaires (BYOK, RTO/RPO, backup evidence) → Compliance › Insights & reporting › Compliance Questionnaires.

**R-ROUTE-OWNER (2026-10-05):** a ticket goes to the product whose feature has to change, not the product where the symptom showed up. Automations often surface other products' features: sender identity, consent and opt-out reports → CRM - Messaging and Campaigns; scheduling and interview templates → Hiring Intelligence · Scheduling; an interview invite triggered by a CRM automation that fails, shows no rounds or templates, or sends late → Hiring Intelligence · Scheduling › Workflows & automations › Automation-triggered invites (v6); email template content → the template owner (O-CONTENT). Only behaviour of the automation itself (trigger, condition, action, run history) stays CRM - Automation.

**Moving a ticket to another product** needs the customer's ask to be about that product's feature, not just where the symptom surfaced (a screening email with broken placeholders stays with the product that owns the template). When the SN component and Jira product area disagree, the Jira product area is the filed product.

Products outside `scope.json` are valid recommendations; they are simply not shown in the SR Prevention tool. Products with no level 2 categories (currently CRM - Events and University Recruiting, Interview Intelligence, Hiring Automations - Assessments) get an empty `l2` and no PM review for that reason.

## 5. Jira Ticket Classification (parent › child)

The recommendation is **parent › child** (PM decision 2026-10-10). The parent goes in `Recommendation JIRA - Ticket Classification`, the child in `Recommendation JIRA - Ticket Classification (Child)`, and the child's source in `matched_rules` as `child: <source>`. Allowed children, definitions and examples: [`_shared/ticket-classification.md`](_shared/ticket-classification.md). It is the only vocabulary and prefers values Jira actually uses.

**How the child is chosen (in this order):**
1. **Jira:** recommended parent = Jira-filed parent and the Jira child is valid → take it (`child: jira`). Jira is filed after Engineering looked at the ticket.
2. **Support:** else recommended parent = ServiceNow-filed parent and that child is valid → take it (`child: support`).
3. **Rule:** else a recorded rule implies it (`child: rule <id>`): O-CAPABILITY → Product Requirement · O-SELF-SERVICE → Self-Service Missing · O-HOWTO → Documentation · O-PROD-CONFIG → Config Move Miss · O-FLAG / O-SEED / O-HOWTO-CHANGE → Configuration Error · O-BUILDER-FIELD / O-UI-MISSING → Functionality · O-SYNC-FAIL → Data Synchronization · O-NULL-FILTER → Data Quality · O-AUTO-LATE → Data Synchronization (Code) or Infra Scaling - Capacity planning (Ops).
4. **Agent:** else the agent picks from the dictionary with a one-line reason (`child: agent`). A doubt about the child alone is **not** a PM review reason.

Steps 1–3 run without the agent (`product-copilot/sr-prevention/child-tiers.py`). The agent may override an inherited child only with a written reason. A PM correction of a child becomes an example in the dictionary.

Confluence reference list (some values are not used in Jira — see the dictionary):

Reference children (Confluence "Ticket Classification – Global Field"):
- Code Issues: Functionality, Performance, Accesibility, API, Data Pipeline, Customization, Localisation/I8n, Data Quality, Data Dependency, Data Loss, Data Synchronization, Accuracy, Prompt, Security
- User Experience Issues: Layout, Navigation, User Flow & Task Completion, Accessibility, Localisation / i18n, Responsiveness, Content & Microcopy
- Product & Knowledge Issues: Product Requirement, Documentation, Non-intuitive Product Behaviour, Inter Product Dependency, Self-Service Missing, Usability, Value KPIs missing
- External Dependency Issues: API Timeout, API Failure, Invalid API Response, SFTP Issue, Webhook Issue, Library, Framework Dependency
- Ops Issues: Infra Scaling - Capacity planning, Incorrect Infra Configuration, CI/CD Pipeline
- Configuration Issues: Configuration Error, Config Move Miss, Configuration Missed, Wrong Configuration


| Parent | Use when |
|---|---|
| Code Issues | Does not work as designed: functionality, performance, API, data quality/sync/loss, accuracy, accessibility, localisation, security |
| User Experience Issues | UI bucket: layout, navigation, responsiveness, unclear labels/error text/instructions, broken flow |
| Product & Knowledge Issues | Works as designed, or the gap is documentation, a missing self-service, non-intuitive behaviour, a missing product requirement, or an inter-product dependency |
| Configuration Issues | Wrong, missed or unmigrated setting, parameter or feature configuration |
| External Dependency Issues | Third-party API, SFTP, webhook, library or framework failure |
| Ops Issues | Infrastructure capacity, infrastructure misconfiguration, CI/CD |

Pairing rules:
- **O-SELF-SERVICE** — one-off change done by Support or Engineering on the customer's request — data correction, deletion or purge, unmerge, bulk tag clean-up, backend status change (e.g. closing jobs), adding a picklist value, provisioning API access, enabling a field for export or filters (v6: wins over O-SEED, because it often needs Engineering and is not self-service) → **Product & Knowledge Issues** (child: Self-Service Missing): the customer needed us because they cannot do it themselves (PM decision 2026-10-05). Exception: if the bad data was created by the system, it is **Code Issues**.
- A tenant setting, feature flag or role permission that was wrong, missing or not migrated → **Configuration Issues**. How-to, expected behaviour, missing capability → **Product & Knowledge Issues**. A feature-flag request is Configuration (L1 Configuration & setup), even when the flag controls access or visibility.
- A Service Request caused by the customer's ATS or another third party (their API returned an error, vendor behaviour) → **External Dependency Issues**; this pairing is valid.
- Bug-Customer normally pairs with Code, User Experience, External Dependency or Ops; Service Request with Product & Knowledge, Configuration or External Dependency. Bug-Customer + Configuration is valid for a production config regression (O-PROD-CONFIG) and needs no review for the pairing alone. Any other pairing must be explained and sets `pm_review = TRUE`.

## 6. Level 1 / level 2

- L1 is one of: Access & permissions · Data & records · Configuration & setup · Workflows & automations · Communications · Integrations & sync · Experience surfaces · Insights & reporting · Content & localization · Reliability & performance.
- L2 must be an `active` or `proposed` row on the Product Taxonomy tab for the chosen product and L1. If the product has L2 rows but none fits, pick the closest, set `pm_review = TRUE`, and name the missing theme in the reasoning ("Suggest new L2: …"). Never invent an L2 value.
- `Triage quality / Wrongly assigned product area` is retired for new runs: re-route the ticket instead (§4).
- Job record edits that don't save (job fields, postal code on a posted job, job data reverting) → CRM - Core › Configuration & setup › **Job configuration** (PM decision 2026-10-05; no separate L2).
- Retired L2s (status `retired` on the tab) are never used. CRM - Core › "Roles & access management" was retired on 2026-10-04 → use CRM - Role & Access Management and pick one of its L2s.

## 7. Confidence and PM review

- **high** — a locked override or unambiguous fulfilment applies, the Details show what was asked, and the product is the filed one or a locked route.
- **medium** — the evidence points one way but the resolution is thin or a second reading is plausible.
- **low** — empty/boilerplate Details, contradictory evidence, or a guess.
- **E-THIN (PM decision 2026-10-05):** when the only doubt is that the Details are empty, boilerplate or too thin to judge, keep the best call with confidence `low`, add `E-THIN` to `rules`, start the reasoning with "Insufficient evidence —", and set `pm_review = FALSE`. A PM cannot add anything there, and flagging these makes the review queue too long. If there is a real second doubt (type fork, product move, security), flag it as usual.
- **Not review reasons on their own (PM decision 2026-10-05):** a Jira that is still open (O-JIRA-OPEN — write "re-check when Jira closes"; the ticket is re-classified once the Jira closes) and a move to another product experience that a routing rule requires. Flag only when a real doubt remains.
- `pm_review = TRUE` when any of: confidence low (except E-THIN) · type fork (defect vs service request plausible) · product moved to another experience · security or data loss · no fitting L2 on a product that has L2s · incoherent type/classification pair. Privacy, access and consent tickets are no longer flagged automatically — only when one of the other reasons applies.

## 8. Reasoning format

One or two sentences: **decision → signal → product**. Example: "Bug-Customer — automation audit shows a project-stage update that never happened; supported behaviour failed (O-AUTOMATION). CRM - Automation (filed)." Do not restate the whole problem.

## 9. Worked examples

| Ticket | Result | Why |
|---|---|---|
| Unmerge two incorrectly merged profiles | Service Request · RX/CRM - Profile · Product & Knowledge Issues · Data & records › Merge, unmerge & duplicate profiles | O-UNMERGE; one-off change on request = Self-Service Missing (2026-10-05) |
| Control disappeared after a release | Bug-Customer · component product · Code Issues | O-UI-MISSING |
| Conditions met but automation never executes | Bug-Customer · RX/CRM - Automation · Code Issues · Workflows & automations › Trigger & execution failures | O-AUTOMATION (no exception in the details) |
| Automation "failed" but audit shows the condition was not met | Service Request · RX/CRM - Automation · Product & Knowledge Issues | O-AUTOMATION exception: expected behaviour |
| Enable a packaged tenant feature | Service Request · Configuration Issues · Configuration & setup | O-FLAG |
| Candidate in ATS missing from CRM, Support cannot fix | Bug-Customer · Code Issues · Integrations & sync | O-SYNC-FAIL |
| "How does X work?" then "please configure fields" | Service Request · Configuration Issues | O-HOWTO-CHANGE |

**Classification decisions from the PM review of 2026-10-05** (71 reviewed rows, compared with the Jira-filed parent):

| Pattern | Example tickets | Jira filed | Decision |
|---|---|---|---|
| Support deletes, purges or corrects data, closes jobs, adds a source value or provisions API access on request | CS0323467, CS0333008, CS0335827, CS0323056, CS0337211, CS0349201, CS0347576, CS0323422 | mixed | Product & Knowledge Issues (Self-Service Missing) |
| Junk tags created by the system, cleaned up by Support | CS0343612 | Code Issues | Code Issues: the system created the bad data |
| Works as designed; only an explanation was needed | CS0329024, CS0332140, CS0343578, CS0344293, CS0343056, CS0333000 | Code / UX / Config / Ops | Product & Knowledge Issues |
| Engineering fixed code (edits not saving, tags orphaned in search, empty hiring team from an API) | CS0326297, CS0326351, CS0328172, CS0328239 | Ops / Config / Product & Knowledge | Code Issues |
| A tenant setting, feature flag or role permission was missing | CS0325734, CS0326437, CS0328484 | Product & Knowledge | Configuration Issues, valid with Bug-Customer when Engineering made the fix |
| Infrastructure capacity: stage overloaded, database cluster upgrade | CS0328074, CS0346357 | Product & Knowledge / Code › Performance | Ops Issues |
| Customer's ATS API returned an error | CS0345454 | Product & Knowledge › Inter Product Dependency | External Dependency Issues |
| Integration config not carried to production | CS0331473 | Configuration › Config Move Miss | Configuration Issues |
| Purge not propagated from CRM to the Apply database | CS0335022 | Configuration | Code Issues (data synchronization) |
| Engineering confirmed the value is expected | CS0340723 | Product & Knowledge | Product & Knowledge Issues |

## 10. Quality gate

The gold set is the **RX - Service Request Analysis** Google Sheet itself: every row a PM has marked `Recommendation Status = reviewed`. Local files (e.g. anything in a Downloads folder) are never used as a benchmark or input.

Before a rulebook version goes live: run it on the reviewed rows and target ≥ 85 % agreement on type and on product. Report defect precision and recall separately — false defects create engineering load, missed defects hide quality problems.
