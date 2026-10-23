# CRM Core timeline method

Code: `.cursor/skills/servicenow-service-requests/scripts/crm_core_jira_timeline.py`. As-of date = snapshot `run_date`.

## 1. Plan-based timeline (from Fix Versions)

Each Fix Version on an item becomes a target date:

| Fix Version | Target date |
|-------------|-------------|
| Has a Jira release date | That date (e.g. 26.11 → 2026-11-30, 26.10 → 2026-10-05) |
| `YY.MM` with no release date | Last day of that month (27.01 → 2027-01-31) |
| `OffCycle-<year>` | 31 Dec of that year (OffCycle-2026 → 2026-12-31) |
| `Backlog` | None |

Item state:

- **planned**: at least one target is on or after the as-of date. The latest future target wins.
- **slipped**: every target is before the as-of date, but the item is still open. It needs re-planning; do not use its date as a finish date.
- **unplanned**: Fix Version is Backlog only.

Months = (target − as-of) / 30.44 days, to one decimal place.

Roll-ups:
- **Parent (epic or initiative) branch roll-up**: covers every counted item below it, across all areas. It gives the latest planned target and the planned, slipped and unplanned counts.
- **Area roll-up**: covers the counted items in that area.

## 2. Pace-based estimate (from delivery history)

`throughput.json` holds the CRM Core stories resolved Done in two 6-month windows (the JQL is stored with the counts). On 2026-10-23 these were 74 stories in the last 6 months (12.3 a month) and 56 in the prior 6 months (9.3 a month). CRM Core also closed 12 epics in the last 6 months.

Estimate = open stories ÷ stories per month, reported as a range across the two windows.

- All 218 open stories: 17.7–23.4 months.
- Per area: team-months, meaning the time if the whole CRM Core team worked only on that area. Areas run in parallel, so the per-area values add up to the overall figure and are not separate finish dates.

## Limits

State these limits whenever you quote a timeline:

- **Low coverage.** Only 71 of 308 items (23%) have a future release. 196 are Backlog and 41 have slipped. So the plan-based "~3.3 months" covers a minority of the work.
- **No sizing.** Only 71 items have story points and 4 have a due date, so the pace estimate counts stories without weighting them by size.
- **Missing work.** Epics and initiatives with no open child stories in the filter add work that the story count does not include.
- **Partial scope.** Items in In QA or PM Acceptance Queue are outside the filter, so near-done work is not counted.
- **Not a promise.** Fix Versions are plans. Check the live schedule in **release-calendar** before quoting dates externally.

## How to phrase an answer

> As of 2026-10-23, CRM Core's planned releases run to 27.01, about 3.3 months away. That plan covers only 71 of the 308 open items: 196 are in Backlog and 41 have passed their release date. At the pace of the last year, 9–12 stories a month, the 218 open stories would take about 18–23 months.
