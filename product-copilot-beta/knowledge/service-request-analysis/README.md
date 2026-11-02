# Service Request analysis — growing context

Teams **feed PE-specific context here**. The runnable workflow stays thin in [`skills/service-request-analysis/`](../../skills/service-request-analysis/SKILL.md).

## Layout

| Path | Purpose |
|------|---------|
| [`_shared/type-rules.md`](_shared/type-rules.md) | Cross-PE true-type signals (Service Request / Bug-Customer) |
| [`rx/`](rx/) | Recruiter Experience — areas, packages, label sheet |
| [`screening/`](screening/) | Screening — stub for that PE’s team to extend |
| [`interview-management/`](interview-management/) | Interview Management — stub |
| [`automations/`](automations/) | Automations — stub |
| [`_shared/taxonomy-guide.md`](_shared/taxonomy-guide.md) | How PMs/agent evolve categories |

## How a team expands this

1. Confirm exact ServiceNow `U_PRODUCT_EXPERIENCE` string in Snowflake.
2. Fill `areas.md` (full product-area names + remap rules).
3. Optionally add `packages.md` once true-SR themes stabilize.
4. Optionally add `label-sheet.md` when you have a human-labeled refinement Sheet for a contested slice.
5. Do **not** fork the skill workflow — run the same layers A–D.

## Label sheet role (read this)

A label sheet is **not** the demand population and **not** the metrics source.

It is a **human-refined label overlay** for a hard slice (e.g. RX Profile+Core) used mainly on **layer D** (and when scoring A/B tickets that appear in that slice). Snowflake still defines who is in A/B/C/D.

## Shared ops notes

- [`_shared/data-pull-efficiency.md`](_shared/data-pull-efficiency.md) — Snowflake partitions, stale COMMENT replica, live Jira JQL batches, Sheets write tips (saves tokens).
- [`_shared/details-format.md`](_shared/details-format.md) — Problem / Discussions / Solution for label-sheet `details`.
- [`_shared/review-clarity.md`](_shared/review-clarity.md) — clear vs needs_human_review for agent labels.
