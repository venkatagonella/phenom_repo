---
name: jira
type: policy
description: "Jira routing, project constants, field IDs, and PM account IDs for Phenom's PHEM project"
requires:
  - jira
always: false
triggers: [jira, phem, epic, story, stories, bug, ticket, sprint, backlog, issue, jql, task, defect]
---

## Jira Skill Router

| Task | Refer to |
|------|----------|
| Creating or updating an **Epic** | `jira-epic-rules` policy + `jira-workflow` skill |
| Creating or updating a **Story** | `jira-story-rules` policy + `jira-workflow` skill |
| Making any API call (field IDs, two-step creation) | `jira-api` skill |
| Finding an existing Epic | `jira-workflow` skill → Epic Finder section |
| Updating an Epic from meeting notes | `jira-workflow` skill → Update from Meeting section |

---

## Project Constants

- **Workspace**: phenompeople.atlassian.net
- **Cloud ID**: `abbe3ee2-54f7-4096-a7a0-62a220d87814`
- **Project Key**: `PHEM`
- **Issue Types** (creatable in PHEM, verified 2026-10-03):

| Issue Type | ID |
|------------|----|
| Initiative | `10613` |
| Epic | `6` |
| Story | `7` |
| Task | `3` |
| Sub-task | `5` |
| Customer Bug | `10746` |
| Vulnerability | `10955` |
| Issues | `10934` |

> `Bug-Internal`, `Refactoring` and `Theme` no longer appear in PHEM create metadata — they may exist on old tickets but cannot be created via API.

---

## Epic Status Workflow

| Status | Meaning |
|--------|---------|
| **To Do** | Epic created, not yet started |
| **In Progress** | Work has begun (requirements, design, or dev) |
| **UX Queue** | Waiting for UX/design work |
| **Epic Grooming** | Being refined — requirements and scope under review |
| **Epic Ready** | Fully elaborated, ready for development |
| **Reopened** | Was ready/done but sent back for rework |
| **Done** | Completed and shipped |

For roadmap analysis, the relevant statuses are `To Do`, `In Progress`, `UX Queue`, `Epic Grooming`, `Epic Ready`, and `Reopened`. Exclude `Done` unless specifically requested.

---

## Field IDs — Quick Reference

> Pass custom fields in `createJiraIssue.additional_fields` / `editJiraIssue.fields`. Either string values `{"value": "…"}` or numeric IDs `{"id": "…"}` work; numeric IDs avoid `INVALID_INPUT` on cascading selects with special characters.

### Epic fields (issue type `6`)

| Field Name | Field ID | Type |
|------------|----------|------|
| Product Experience : Product | `customfield_15211` | cascadingselect |
| Priority | `customfield_15212` | select |
| Theme | `customfield_15215` | select |
| Initiative Type | `customfield_15216` | select |
| Release Note Candidate | `customfield_15217` | select |
| How to Enable | `customfield_15218` | select |
| PM Owner | `customfield_15223` | userpicker |
| UX Owner | `customfield_15222` | userpicker |
| UI Owner | `customfield_15552` | userpicker |
| KM Owner | `customfield_15522` | userpicker |
| UX Required | `customfield_14675` | multicheckboxes |
| UX Effort | `customfield_15431` | select |
| UX Link | `customfield_15074` | textarea |
| User Research Included | `customfield_15486` | multicheckboxes |
| Feature Flag Available | `customfield_15427` | select |
| Release Type | `customfield_15550` | select |
| Product Maturity | `customfield_15685` | select |
| Grooming Status | `customfield_15624` | select |
| Validation by QA before assigning to Customers | `customfield_15421` | select |
| Epic Name | `customfield_10113` | text |
| Epic Description | `customfield_15450` | textarea |
| Rank: Overall | `customfield_15213` | textarea |
| Customer(s) | `customfield_15214` | textarea |
| Client | `customfield_11213` | select (~1,300 values — look up, don't hardcode) |
| Customer Category | `customfield_14710` | select |
| Team Dependency | `customfield_14614` | multiselect |
| Parent Link (→ Initiative) | `customfield_12510` | jpo parent |
| Story Points | `customfield_10003` | float |
| Enablement Doc Link | `customfield_15551` | url |
| Link to Demo Video or Screenshots | `customfield_15717` | url |
| Link to the Google Drive | `customfield_15084` | url |
| SKU | `customfield_15699` | text |
| Team | `customfield_18551` | text |

### Story-only fields (issue type `7`)

Stories share most Epic fields (incl. `customfield_15211`, Priority, PM Owner). These are additional:

| Field Name | Field ID | Type |
|------------|----------|------|
| Epic Link | `customfield_10112` | gh-epic-link |
| Sprint | `customfield_10111` | gh-sprint |
| Story Description | `customfield_15451` | textarea |
| QA required | `customfield_15716` | multicheckboxes |
| QA Owner | `customfield_15224` | userpicker |
| DEV Owner | `customfield_15225` | userpicker |
| DEV ETA | `customfield_15541` | datepicker |
| Due Date | `customfield_13700` | datepicker |
| Release Notes Description | `customfield_14372` | textarea |
| KM Plan | `customfield_15734` | text |
| Team (Atlassian team) | `customfield_13000` | atlassian-team |

> ⚠️ `customfield_15213` is **Rank: Overall** (free text), not UX Required. UX Required is `customfield_14675`.
> ⚠️ `customfield_15256` (Product Experience, single select) is **not on the Epic or Story screens** — only Vulnerability/Alert. Use `customfield_15211` for Epics and Stories.

---

## Field Value IDs

### Product Experience : Product (`customfield_15211`)

All 18 experiences / 85 products live in Jira (synced 2026-10-03). String equivalent: `{"value": "<Experience>", "child": {"value": "<Product>"}}` — use the exact names below (note en-dashes in Career Site names).

#### Analytics — parent `20648`

| Product | Child ID | API format |
|---------|----------|------------|
| Talent Analytics | `20651` | `{id: "20648", child: {id: "20651"}}` |

#### Automation Engine — parent `32610`

| Product | Child ID | API format |
|---------|----------|------------|
| Automation Engine - Core | `32611` | `{id: "32610", child: {id: "32611"}}` |

#### Candidate Experience (CX) — parent `20644`

| Product | Child ID | API format |
|---------|----------|------------|
| Career Site – Platform Services | `27562` | `{id: "20644", child: {id: "27562"}}` |
| Career Site – Templates & Views | `27563` | `{id: "20644", child: {id: "27563"}}` |
| Chatbot | `52894` | `{id: "20644", child: {id: "52894"}}` |
| CMS | `20653` | `{id: "20644", child: {id: "20653"}}` |
| TXE | `51009` | `{id: "20644", child: {id: "51009"}}` |
| Video Hub | `49074` | `{id: "20644", child: {id: "49074"}}` |

#### Data — parent `20647`

| Product | Child ID | API format |
|---------|----------|------------|
| DEC | `28151` | `{id: "20647", child: {id: "28151"}}` |
| DNA | `28148` | `{id: "20647", child: {id: "28148"}}` |
| ETG | `20673` | `{id: "20647", child: {id: "20673"}}` |
| Ontologies | `53346` | `{id: "20647", child: {id: "53346"}}` |
| PUP | `28150` | `{id: "20647", child: {id: "28150"}}` |
| TDP | `30132` | `{id: "20647", child: {id: "30132"}}` |

#### Employee Experience (EX) — parent `20642`

| Product | Child ID | API format |
|---------|----------|------------|
| Alumni | `30024` | `{id: "20642", child: {id: "30024"}}` |
| Career Pathing | `20666` | `{id: "20642", child: {id: "20666"}}` |
| EX Platform (Other) | `30028` | `{id: "20642", child: {id: "30028"}}` |
| Internal Mobility | `30030` | `{id: "20642", child: {id: "30030"}}` |
| Learning | `30031` | `{id: "20642", child: {id: "30031"}}` |
| Mentoring | `30032` | `{id: "20642", child: {id: "30032"}}` |
| Projects/Gigs | `30029` | `{id: "20642", child: {id: "30029"}}` |
| Referrals | `30035` | `{id: "20642", child: {id: "30035"}}` |
| Edge - Pathfinder | `55939` | `{id: "20642", child: {id: "55939"}}` |
| Edge - Mobility | `55940` | `{id: "20642", child: {id: "55940"}}` |

#### Employee Onboarding Experience — parent `51312`

| Product | Child ID | API format |
|---------|----------|------------|
| Background Verification | `53928` | `{id: "51312", child: {id: "53928"}}` |
| Candidate Pre-boarding | `53927` | `{id: "51312", child: {id: "53927"}}` |
| Employee On-boarding | `51313` | `{id: "51312", child: {id: "51313"}}` |
| Tydy - Onboarding | `64135` | `{id: "51312", child: {id: "64135"}}` |

#### Hiring Automations — parent `28209`

| Product | Child ID | API format |
|---------|----------|------------|
| Hiring Automations - Assessments | `32327` | `{id: "28209", child: {id: "32327"}}` |
| Hiring Automations - Core | `28210` | `{id: "28209", child: {id: "28210"}}` |

#### Hiring Intelligence — parent `55311`

| Product | Child ID | API format |
|---------|----------|------------|
| Interview Intelligence | `55312` | `{id: "55311", child: {id: "55312"}}` |
| Scheduling | `55313` | `{id: "55311", child: {id: "55313"}}` |
| Voice Agent Screening | `58558` | `{id: "55311", child: {id: "58558"}}` |
| X+ Screening | `55314` | `{id: "55311", child: {id: "55314"}}` |

#### Integration Experience (IX) — parent `20641`

| Product | Child ID | API format |
|---------|----------|------------|
| FS Forms - Apply Platform | `32503` | `{id: "20641", child: {id: "32503"}}` |
| FS Forms - Config & Self-Serve | `32500` | `{id: "20641", child: {id: "32500"}}` |
| FS Forms - Simple Forms | `32501` | `{id: "20641", child: {id: "32501"}}` |
| FSI - App Integrations | `32506` | `{id: "20641", child: {id: "32506"}}` |
| FSI - Data Integrations | `32505` | `{id: "20641", child: {id: "32505"}}` |
| FSI - FlowStudio Onboarding | `52898` | `{id: "20641", child: {id: "52898"}}` |
| FSI - Hiring Status Int. | `20659` | `{id: "20641", child: {id: "20659"}}` |
| FSI - Integration Templates | `54611` | `{id: "20641", child: {id: "54611"}}` |
| FSI - Job Synch | `52900` | `{id: "20641", child: {id: "52900"}}` |
| FSI - Runtime Diagnostics | `32507` | `{id: "20641", child: {id: "32507"}}` |

#### Manager Experience (MX) — parent `20645`

| Product | Child ID | API format |
|---------|----------|------------|
| MX - Hiring | `27913` | `{id: "20645", child: {id: "27913"}}` |
| Req & Offer | `31156` | `{id: "20645", child: {id: "31156"}}` |
| MX - Mobile | `63523` | `{id: "20645", child: {id: "63523"}}` |

#### Other Products — parent `52882`

| Product | Child ID | API format |
|---------|----------|------------|
| Job Distribution | `52887` | `{id: "52882", child: {id: "52887"}}` |
| Phenom X+ | `52883` | `{id: "52882", child: {id: "52883"}}` |
| Swaasa | `52884` | `{id: "52882", child: {id: "52884"}}` |
| HRIS | `66690` | `{id: "52882", child: {id: "66690"}}` |

#### Phenomenal Tools — parent `30724`

| Product | Child ID | API format |
|---------|----------|------------|
| APM | `30725` | `{id: "30724", child: {id: "30725"}}` |
| Discovery & OnBoard X | `30727` | `{id: "30724", child: {id: "30727"}}` |
| HRIT | `52891` | `{id: "30724", child: {id: "52891"}}` |
| QA Hub | `30728` | `{id: "30724", child: {id: "30728"}}` |
| User Management | `52892` | `{id: "30724", child: {id: "52892"}}` |

#### Recruiter Experience (RX) — parent `20643`

| Product | Child ID | API format |
|---------|----------|------------|
| Compliance | `50732` | `{id: "20643", child: {id: "50732"}}` |
| CRM - Automation | `27560` | `{id: "20643", child: {id: "27560"}}` |
| CRM - Core | `20667` | `{id: "20643", child: {id: "20667"}}` |
| CRM - Events and University Recruiting | `20669` | `{id: "20643", child: {id: "20669"}}` |
| CRM - Google Chrome Extension | `28188` | `{id: "20643", child: {id: "28188"}}` |
| CRM - Messaging and Campaigns | `20668` | `{id: "20643", child: {id: "20668"}}` |
| CRM - Mobile | `28612` | `{id: "20643", child: {id: "28612"}}` |
| CRM - Profile | `27566` | `{id: "20643", child: {id: "27566"}}` |
| Direct Sourcing | `51524` | `{id: "20643", child: {id: "51524"}}` |
| CRM - Role & Access Management | _pending_ | ⚠️ No Jira ID yet — do not set it on Jira issues until an ID is added. Valid as a product name in SR triage / the label sheet. |


#### Search & Personalization — parent `20646`

| Product | Child ID | API format |
|---------|----------|------------|
| Fit Score | `20717` | `{id: "20646", child: {id: "20717"}}` |
| Job Parser | `22210` | `{id: "20646", child: {id: "22210"}}` |
| PX | `20672` | `{id: "20646", child: {id: "20672"}}` |
| Resume Parser | `20882` | `{id: "20646", child: {id: "20882"}}` |
| RX - Search | `20881` | `{id: "20646", child: {id: "20881"}}` |
| Search | `20671` | `{id: "20646", child: {id: "20671"}}` |
| SPX Sourcing | `25164` | `{id: "20646", child: {id: "25164"}}` |

#### Talent Management — parent `58549`

| Product | Child ID | API format |
|---------|----------|------------|
| Enterprise Talent Intelligence | `58552` | `{id: "58549", child: {id: "58552"}}` |
| Succession Planning | `58553` | `{id: "58549", child: {id: "58553"}}` |
| Performance Review | `58554` | `{id: "58549", child: {id: "58554"}}` |
| People Manager | `58555` | `{id: "58549", child: {id: "58555"}}` |
| ERM - Core | `58556` | `{id: "58549", child: {id: "58556"}}` |
| Resource Management | `58557` | `{id: "58549", child: {id: "58557"}}` |
| Development Plans | `60865` | `{id: "58549", child: {id: "60865"}}` |

#### Z - Ops Engineering (Not a Product) — parent `32534` ⚠️ do not use for product work

| Product | Child ID | API format |
|---------|----------|------------|
| Ops Engineering(DevOps/CloudOps) | `32536` | `{id: "32534", child: {id: "32536"}}` |
| Monitoring Team | `32537` | `{id: "32534", child: {id: "32537"}}` |
| Incident Response Engineering(IRE) | `32538` | `{id: "32534", child: {id: "32538"}}` |
| Metadata-daal | `62993` | `{id: "32534", child: {id: "62993"}}` |

#### Z - From Automation(Don't Use) — parent `55081` ⚠️ do not use for product work

| Product | Child ID | API format |
|---------|----------|------------|
| Use for Automations Only | `55082` | `{id: "55081", child: {id: "55082"}}` |

#### Z - Agents Experience (Don’t use) — parent `55815` ⚠️ do not use for product work

| Product | Child ID | API format |
|---------|----------|------------|
| Hiring Agents | `55816` | `{id: "55815", child: {id: "55816"}}` |

### Product Experience (`customfield_15256`) — Vulnerability / Alert only

| Value | ID |
|-------|----|
| Analytics | `{id: "28379"}` |
| Automation Engine | `{id: "32612"}` |
| Candidate Experience (CX) | `{id: "28380"}` |
| Data | `{id: "28382"}` |
| Employee Experience (EX) | `{id: "28383"}` |
| Hiring Automations | `{id: "28384"}` |
| Hiring Intelligence | `{id: "55320"}` |
| Integration Experience (IX) | `{id: "28385"}` |
| Manager Experience (MX) | `{id: "28386"}` |
| Other Products | `{id: "52902"}` |
| Phenomenal Tools | `{id: "31242"}` |
| Recruiter Experience (RX) | `{id: "28387"}` |
| Scheduling (legacy) | `{id: "28388"}` |
| Search & Personalization | `{id: "28389"}` |
| Talent Management | `{id: "58560"}` |
| Video Experience (VX) (legacy) | `{id: "28390"}` |
| Z - Agents Experience (Don't use) | `{id: "55906"}` |

> Not used for Epic/Story creation. Still used for JQL filtering in SUP/CUSP and on Vulnerability/Alert tickets.

### Priority (`customfield_15212`)

| Value | ID |
|-------|----|
| P0 | `{id: "20680"}` |
| P1 | `{id: "20681"}` |
| P2 | `{id: "20682"}` |
| P3 | `{id: "20683"}` |

### Theme (`customfield_15215`)

| Value | ID |
|-------|----|
| Revenue Bet | `{id: "50235"}` |
| Customer Retention Bet | `{id: "50234"}` |
| Delivery Enablement Bet | `{id: "50233"}` |
| Support Enablement Bet | `{id: "50232"}` |

### Initiative Type (`customfield_15216`)

| Value | ID |
|-------|----|
| New Feature | `{id: "20693"}` |
| Feature Enhancement | `{id: "50924"}` |
| Usability | `{id: "28208"}` |
| Customer Commit | `{id: "20691"}` |
| Customer Feedback | `{id: "28142"}` |
| Escalated Enhancement | `{id: "22166"}` |
| Compliance | `{id: "28777"}` |
| Data Quality | `{id: "28330"}` |
| Support Ticket Reduction | `{id: "20690"}` |
| Tech Debt | `{id: "20692"}` |

### Release Note Candidate (`customfield_15217`)

| Value | ID |
|-------|----|
| YES - Advertise Externally / All Customers | `{id: "20694"}` |
| Yes - Internal Only | `{id: "32377"}` |
| NO - Do Not Advertise / Specific Customers | `{id: "20695"}` |
| No - Do Not Advertise / Backend Change | `{id: "30064"}` |

### How to Enable (`customfield_15218`)

| Value | ID |
|-------|----|
| On By Default | `{id: "30072"}` |
| By Request - Support Ticket | `{id: "30073"}` |
| By Request - Paid Feature / AM Consult | `{id: "30074"}` |
| By Request - Product Maturing / CSM Consult | `{id: "30075"}` |
| None | `{id: "20696"}` |

### Feature Flag Available (`customfield_15427`)

| Value | ID |
|-------|----|
| YES | `{id: "27986"}` |
| NO | `{id: "27987"}` |
| NA | `{id: "27988"}` |

### UX Required (`customfield_14675`) — multicheckbox

| Value | ID |
|-------|----|
| Yes | `[{id: "17184"}]` (leave empty for No) |

### UX Effort (`customfield_15431`)

| Value | ID |
|-------|----|
| 1 | `{id: "28143"}` |
| 2 | `{id: "28144"}` |
| 3 | `{id: "28145"}` |
| 5 | `{id: "28146"}` |
| 8 | `{id: "28147"}` |

### User Research Included (`customfield_15486`) — multicheckbox

| Value | ID |
|-------|----|
| Yes | `[{id: "28611"}]` |

### Release Type (`customfield_15550`)

| Value | ID |
|-------|----|
| Full Release | `{id: "30065"}` |
| Limited Release | `{id: "30066"}` |
| Soft Release | `{id: "32244"}` |

### Product Maturity (`customfield_15685`)

| Value | ID |
|-------|----|
| General Availability (GA) | `{id: "31914"}` |
| Early Availability (EA) | `{id: "31913"}` |
| EA - Ramp Up | `{id: "63061"}` |
| EA - Incubation | `{id: "63062"}` |
| EA - Ideation | `{id: "63063"}` |

### Grooming Status (`customfield_15624`)

| Value | ID |
|-------|----|
| GROOMED | `{id: "30628"}` |
| NON-GROOMED | `{id: "30629"}` |

### Validation by QA before assigning to Customers (`customfield_15421`)

| Value | ID |
|-------|----|
| Yes | `{id: "27916"}` |
| No | `{id: "27917"}` |

### QA required (`customfield_15716`) — Story, multicheckbox

| Value | ID |
|-------|----|
| Yes | `[{id: "32254"}]` |
| No | `[{id: "32255"}]` |

### Fix Version

- Format: `YY.MM` e.g. `26.05`
- Unscheduled: `[{name: "Backlog"}]`

---

## JQL — Cascading Select Pattern

`customfield_15211` requires **two AND conditions** (one for parent, one for child):

```jql
project = PHEM AND "Product Experience : Product" = "Hiring Intelligence" AND "Product Experience : Product" = "Scheduling" AND type = Epic
```

Alternative using field ID alias: `cf[15211]` with the same two conditions.

For CUSP feedback (max 100 per request — paginate with date splits):
```jql
project = CUSP AND issuetype = "Product Feedback" AND "Product Experience : Product" = "Hiring Intelligence" AND "Product Experience : Product" = "Scheduling" AND created >= "2025-11-01" ORDER BY created DESC
```

---

## PM Account IDs

| PM | Account ID |
|----|------------|
| Sebastian Niewöhner | `6035546d8ff09800715a3137` |
| Markus Hertlein | `623c36be4a57610068e75ed9` |
| Timothy Moulton | `6231f5a3442e0e0069ed4fe1` |
| Jaydeep Gurujala | `712020:b80a30aa-dda4-47cc-86fb-5d85f3b6a3a8` |
| Syed Naqvi | `712020:9d76318c-04d0-42a6-a66f-867548fc314b` |
| Diksha Madhukar Rathod | `61e8ff1f6b1ad90069c5fcbc` |
| Sitaram Jonnalagedda | `712020:120c5b90-5d82-4e6c-a48a-900b342bd94d` |
| Guru Yerramilli | `712020:cf8f4c7e-13b7-4b40-968b-c766f1f14b32` |
| Katerina Bineva | `712020:f8241502-6461-4617-b016-606165272c40` |
| Tulasi Pinnaka | `64252c61b05b4e3e7dabedbf` |
| Mahendra Manohar Kamate | `6215cf2b7580350068348cdd` |
| Harshal Hanwantrao Chavhan | `712020:916856a4-1320-4ed1-a675-cf1480135ab4` |

> Last synced from Jira API: 2026-10-03 (field IDs + option IDs; PM account IDs not re-verified). To refresh `customfield_15211` values: call `getJiraIssueTypeMetaWithFields(cloudId, projectIdOrKey: "PHEM", issueTypeId: "6")` and look for `customfield_15211` → `allowedValues`.

---

## Product Prefixes (Story Naming)

Story format: `[Prefix] – [FE/BE] – [Story Title]`

| Product | Prefix | Note |
|---------|--------|------|
| Scheduling | `SCH` | |
| X+ Screening | `SCR` | |
| Interview Intelligence | `II` | |
| Voice Agent Screening | `VAS` | |
| Automation Engine | `AE` | |
| CRM - Core | `Core` | |
| CRM - Messaging and Campaigns | `MSG` | |
| CRM - Profile | `PROF` | |
| Hiring Agents | `AG` | ⚠️ Jira parent is `Z - Agents Experience (Don’t use)` |

---

## Naming Conventions

Examples:
- `II – FE – Add transcript export option`
- `SCH – BE – Create calendar availability endpoint`
- `AE – FE – Display automation execution logs`
- `SCR – BE – Bulk reject via screening threshold`

---

## Bug Reporting

When creating a **Customer Bug** or an internal bug ticket (`Bug-Internal` is no longer creatable in PHEM), always include:
- **Reproduction steps** (clear, numbered)
- **Environment** — Staging or Production? Ireland or US? Customer tenant or Phenom internal?
- **Links** — Job, candidate, logs, or any data needed to reproduce
- **Parent link** — Every bug must link to an Epic or Story (no floating bugs)
- **Priority** — P0 (blocker), P1 (critical), P2 (medium), P3 (low)

---

## Phase Management

- Phase 1 = Epic 1 with a clear scope boundary
- Phase 2 = a separate new Epic (never mix phases in one Epic)
- If scope creeps during development → move additions to a Phase 2 Epic
