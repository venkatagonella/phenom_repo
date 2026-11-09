# Job audit trail — field inclusion (sourced)

Prototype: [`index.html`](./index.html)  
Scope: **job entity field edits only** (Diff / “Job Details Updated” pattern). Not lifecycle events.

## Column model

| Column | Why |
| --- | --- |
| Edited by | PHEM-887168: WHO — filter via PDS AutoComplete (search + dropdown) |
| Date & time | PHEM-887168: WHEN in viewer timezone — sortable asc/desc |
| Field(s) changed | Single edit: one field (regular weight). Bulk edit: list of all fields in that `bulkOpId` instance ([PHEM-2260385](https://phenompeople.atlassian.net/browse/PHEM-2260385)) |
| Source | Single-job edit vs bulk edit activity ([PHEM-2260385](https://phenompeople.atlassian.net/browse/PHEM-2260385) Audit / activities log) |

Previous / New value columns are not shown in the table; bulk rows can still open a modal with per-field diffs.

## Interaction model

| Behavior | Spec |
| --- | --- |
| Edited by combobox | Type to filter or open list and select (PDS AutoComplete) |
| Date sort | Header toggle ascending ↔ descending; normal font weight |
| Bulk edit row | One activity row per bulk op; chips list every field; modal shows full per-field diffs |

## Included fields

### Standard CRM job fields (Jobpull ↔ CRM mapping)

Source: [Phenom Hire Jobpull Implementation](https://phenompeople.atlassian.net/wiki/spaces/OGD/pages/56606523442) (updated 2025-12-05).

| Field (CRM label) | Mapping note | Audit importance |
| --- | --- | --- |
| Job Title | `title` → Job Title | Candidate-facing identity; highest-churn edit |
| Job Description | `jobRequirements` → Job Description (CRM-editable mapping) | Content change drives posting accuracy / compliance |
| Job Location | `primaryWorkLocation` + `additionalLocations` | Affects search, scheduling, and compliance geography |
| Job Category | `category` | Classification / reporting |
| Job Type | `type` → Job Type | Employment type; hiring workflow branching |
| Hiring Team | `hiringTeamList` / `recruiterdata` | Access, notifications, ownership |
| Languages / Publish | `languageCode` / `countryCode` / locale + siteType | Visibility on career site |

Also:

| Field | Source | Why |
| --- | --- | --- |
| Primary Job Title | [PHEM-2202538](https://phenompeople.atlassian.net/browse/PHEM-2202538) | Distinct from posting title; recruiters need audit when primary vs posting diverge |

### Disney job-level fields (customer list)

Source: attachment **image-20260814-161356.png** on [PHEM-2260385](https://phenompeople.atlassian.net/browse/PHEM-2260385) (“Fields relevant for Disney”).

| Field | Type (from attachment) | Why auditable |
| --- | --- | --- |
| Recruiting Instructions | single-select | Process guidance for recruiters |
| Requisition Notes | text field | Operational notes; support / dispute context |
| Job Family Group | single-select | Org classification (listed on Disney sheet) |
| Recruitment Group | single-select | Routing / ownership |
| Recruitment Subgroup | single-select | Finer routing |
| Recruitment Type | single-select | Hire type decisions |
| Source Type | single-select | Mass Volume Placement |
| Process Team | single-select | Mass Volume Placement |
| Recruitment Status | single-select | Mass Volume Placement status |
| Recruitment Status Date | date | Mass Volume Placement timing |

Compensation and Static qualification fields are omitted from this prototype view (product request).

### Additional job fields (class, not a hard-coded list)

Source: [Job level - Additional fields](https://phenompeople.atlassian.net/wiki/spaces/CAN/pages/54252605663).

Any tenant field with `groupType: "Job"` can appear in the Field column when edited. Labels are tenant-configured — do not invent a universal list beyond the Disney attachment and standard mapping above.

## Explicitly out of scope for this page

| Event / data | Why excluded |
| --- | --- |
| Create / publish / unpublish / close job | Lifecycle MVP on [PHEM-887168](https://phenompeople.atlassian.net/browse/PHEM-887168); not field diffs |
| Candidate moves / candidate actions | Out of MVP and not job-field edits |
| Job field *definition* changes (admin catalog add/edit/delete) | Separate ask: [PHEM-322165](https://phenompeople.atlassian.net/browse/PHEM-322165) |

## UI references used

- Design system skill + local tokens: `skills/design-system.md`, `knowledge/design-system/phenom-ds-code.md`
- PDS Table page: [Figma DS V2 Table](https://www.figma.com/design/6Vd1BU48fnhA5F0eg8d57S/Phenom-Design-System-V2--UI-Shell----Master?node-id=6392-64730)
- Bulk-edit CRM shell / tokens: Jira attachment `bulk-edit-job-requisitions.html` on PHEM-2260385
- Job entity enhancements Figma: [Co6dDI7rsZmHM7NLT8WjSg](https://www.figma.com/design/Co6dDI7rsZmHM7NLT8WjSg/Job-entity-enhancements?node-id=9679-13654) (wireframe board; “Bulk update summary” section label at `10054-37238`)

## Not claimed

- Exact production Activity tab placement is still an open IA question on [PHEM-1863370](https://phenompeople.atlassian.net/browse/PHEM-1863370); this prototype uses an **Activity** tab as the placement assumed by PHEM-887168’s “findable job history” requirement.
- Sample editor names / old→new values are illustrative for UI density only; they are not production audit data.
