# RX — label sheet

**Sheet:** [RX - Service Request Analysis](https://docs.google.com/spreadsheets/d/1dTFPQUDCWflvrJ8xjfGm_21Ea_mGlFeZkIyjMCT8Sto)

## Role

Snowflake owns populations/metrics. This sheet owns recommendations plus `Summary` / `Details` narrative for human/agent triage. Prior rows are **not** human-reviewed unless their Recommendation Status is `reviewed`.

## Recommendation columns (2026-10-04)

One writer only: the `sr-triage` skill ([`skills/sr-triage/SKILL.md`](../../../skills/sr-triage/SKILL.md), rules in [`../rulebook.md`](../rulebook.md)). Service Sarah is retired.

| Header | Value |
|--------|-------|
| `Recommendation Ticket Type` | Service Request · Bug-Customer |
| `Recommendation Product Experience` / `Product Area` | Jira names from `policies/jira-constants.md` |
| `Recommendation JIRA - Ticket Classification` | Jira Ticket Classification parent |
| `Recommendation JIRA - Ticket Classification (Child)` | Child (sub-classification), rulebook §5; source in `matched_rules` as `child: jira / support / rule <id> / agent` |
| `Recommendation L1 - Category` / `L1 - Sub-Category` | Product Taxonomy tab (active or proposed rows) |
| `Recommendation Reasoning`, `Conficence Level`, `PM Review Required` | per rulebook §7–8 |
| `Recommendation Status` | `proposed`; only a PM sets `reviewed` (never overwritten) |
| `Recommendation Analysed By` / `On` | `SR Triage Agent` / run date |
| `matched_rules` | `rulebook <version>; <rule ids>` |

## Classification comparison (2026-10-05)

Three values per ticket, compared at **parent** level and, where the parents agree, at **child** level (the six Jira Ticket Classification parents in `../rulebook.md` §5):

| Source | Column | Notes |
|--------|--------|-------|
| Support filed | `SN - Classification` (child: `SN - Classification (Child)`) | as filed in ServiceNow |
| Jira filed | `JIRA - Ticket Classification` (child: `jira_ticket_classification_child`) | as filed in Jira; only escalated tickets |
| Recommended | `Recommendation JIRA - Ticket Classification` + `… (Child)` | parent by the SR triage agent; child inherited from Jira/Support when the parent matches, else rule or agent |

Filed values are normalised only when comparing (the sheet is never changed): `Non-intutive Product Behaviour` → `Non-intuitive Product Behaviour`, `Localization / i18n` → `Localisation / i18n`, `Security-Related Issues` → parent `Code Issues` (child Security). `Incorrect Discovery` and blank children keep their parent and count as "child not on the official list". A match = same parent. Filed children are shown as supporting detail only.

## Source columns

The `sr-triage` helper reads source fields by their live headers, including `Service Now ID`, `JIRA ID`,
`Summary`, `Details`, `SN - Component`, `SN - Sub-Component`, `SN - Request Category`,
`JIRA - Product Area`, `JIRA - Type of Issue/Request`, and `JIRA - Status`.
Do not reintroduce the retired snake_case label contract.

See **Legend** tab on the live sheet for fill instructions.

## `Details` shape

Always **Problem / Discussions / Solution** — summarized. `Problem:` and `Solution:` may be one line (`Problem: …`); Discussions stay as bullets. Full rules + example: [`_shared/details-format.md`](../_shared/details-format.md).

## `Summary` / `Details` fill rules (mandatory)

| Population | `Summary` | `Details` |
|------------|-----------|-----------|
| Layer B — no Jira ID | SN `TASK.SHORT_DESCRIPTION` | SN description + `SYS_JOURNAL_FIELD` work notes/comments (last ~8–10) |
| Layer C/D — has Jira | Jira summary (fallback SN short description) | Jira description + live comment thread (JQL batches); SN journal optional append |

**Never** leave SN-only rows with empty `Summary` / `Details` after a fill.

Mechanics: [`_shared/data-pull-efficiency.md`](../_shared/data-pull-efficiency.md).

## Process

1. Pull SN population + Jira links (Snowflake).
2. Fill narrative for **all** rows (SN first; Jira comments for escalations).
3. The `sr-triage` skill writes only Recommendation columns as `proposed`; only a human changes Recommendation Status to `reviewed`.
