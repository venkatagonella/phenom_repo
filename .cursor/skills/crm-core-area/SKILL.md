---
name: crm-core-area
description: >-
  Reference for the Phenom CRM Core (Recruiter Experience RX - CRM - Core)
  product area: the six CRM Core areas (hiring status, jobs, ATS/LinkedIn sync,
  access, events, configuration), what customers raise in ServiceNow for each,
  which open 2026 Jira initiatives, epics and stories address them, their
  planned release timeline, and how to refresh the analysis. Use when asked
  what CRM Core is working on, which Jira items cover an area, when CRM Core
  work will ship, how SR demand maps to the CRM Core backlog, or to rebuild
  the CRM Core Jira areas HTML.
---

# CRM Core area reference

CRM Core is the Recruiter Experience (RX) pod that owns the recruiter's CRM: candidate pipeline and hiring status, jobs and requisitions, integrations into CRM (ATS, LinkedIn), access and roles, and admin configuration. Product scope, personas and FRD story naming live in **crm-core-product**. This skill adds what customers ask for in support tickets, what is open in Jira, and when it is planned to ship.

All numbers below come from the run on **2026-10-23**. Always quote the run date, and refresh the data (see "Refresh") before giving numbers for a later date.

## Hard rules

- Jira, ServiceNow and Drive are read-only inputs. Never create, edit, transition or comment on Jira (see **read-only-inputs**).
- Use only the data. If something is not in the snapshot or Jira, say it is not found. Do not invent dates, owners or scope.
- Support-ticket themes are demand signals, not roadmap commitments. Jira Fix Versions are plans, not ship guarantees.
- HTML output follows the Phenom Design System (PDS tokens, Poppins, no invented colours).

## The six CRM Core areas

Each area is a theme from the RX ServiceNow analysis (see **servicenow-service-requests**, `theme-playbook.md`). SR counts are from 4,379 RX service requests. Jira counts are the open 2026 CRM Core items placed in that area.

| Area | What it covers | RX SRs | Open Jira (I/E/S) | Latest planned release |
|------|----------------|-------:|------------------:|------------------------|
| Hiring status / pipeline / stages / lead status | Candidate × job status, pipeline stages, lead vs applicant status | 263 (6.0%) | 4 (0/1/3) | OffCycle-2026 (~2.3 mo) |
| Jobs / requisitions / applications / posting | Job record, req setup, publish/unpublish/expiry, career site, applications | 242 (5.5%) | 55 (2/16/37) | OffCycle-2026 (~2.3 mo) |
| Forwarding / LinkedIn / ATS↔CRM sync | LinkedIn CRM Connect, Workday/SuccessFactors/ATS sync, HRM, Indeed, ADP | 180 (4.1%) | 21 (2/9/10) | OffCycle-2026 (~2.3 mo) |
| Access / CRM not opening / permissions | Roles, RBAC, hiring-team roles, departmentalization, visibility, export restriction | 141 (3.2%) | 46 (0/8/38) | OffCycle-2026 (~2.3 mo) |
| Events / university recruiting | Event registration, campus recruiting | 87 (2.0%) | 0 | none |
| How-to / configuration / enablement question | Settings, feature flags, self-service errors, tenant setup | 50 (1.1%) | 17 (1/4/12) | OffCycle-2026 (~2.3 mo) |
| Not in the six areas | SDUI, performance, notes, spotlights, projects, agency, executive recruiting, localization, bugs | — | 135 (12/24/99) | 27.01 (~3.3 mo) |

The filter returned 308 items. 30 were removed because they mention metadata (see "Metadata exclusion" below), leaving 278: 17 initiatives, 62 epics and 199 stories. Status: 234 To Do, 17 Development, 9 In Progress, 6 Story Ready, 4 Story Grooming, 3 ON Hold, 5 other.

## What each area will improve

These summaries come from the item titles only.

**Hiring status / pipeline.** Hiring statuses are translated per recruiter language. With Hiring Pipeline on, leads and applicants get separate spotlights. "Latest job stage" becomes exportable, and lead and applicant counts show per agency. Key epic: PHEM-2136326 Translation Experience for Hiring Status (Backlog).

**Jobs / requisitions.** This area adds:
- Bulk-edit requisitions (PHEM-2260385, 26.11).
- Scheduled posting (PHEM-2186925).
- Private links for confidential jobs (PHEM-2199077).
- A job page overview tab (PHEM-1902635).
- A document viewer for attachments (PHEM-2180576).
- A job activity view (PHEM-1970578, PHEM-2281914).
- Translated job fields on the career site (PHEM-2491710, PHEM-2435084, 26.11).
- RedDot distribution (PHEM-1987584).
- Custom job statuses (PHEM-2391005).
- An application-centric list (PHEM-2252497).

**ATS / LinkedIn sync.** LinkedIn CRM Connect gets hardened and the broken pipeline fixed (PHEM-2341256, PHEM-2341415, 26.11; earlier PHEM-1957322 has slipped). Jobs follow their Workday lifecycle: create, publish and unpublish (PHEM-2267008), plus failure handling and manual retry (PHEM-2278041). The ATS job pull becomes role-aware (PHEM-2104059). The area also covers HRM <> CRM projects (PHEM-1957974), IX job workflow (PHEM-2278020), and Indeed native apply (PHEM-2007989).

**Access / permissions.** Job-level hiring-team roles cover the role UI, migration, auto-provisioning and role-based visibility (PHEM-2104062, 2104070, 2104079, 2104082). Their initiative and data-model epic were removed by the metadata exclusion, so these epics now sit at the top of the tree. Other work in this area:
- RBAC to restrict download and export (PHEM-2267012).
- Worker council lead access (PHEM-2492867).
- Departmentalized connections (PHEM-2178519).
- Hiding employee details when consent is No (PHEM-2079228).

**Events / university.** No open 2026 CRM Core item is in this area. The one events-related story, which restricts event candidate and report export, is counted under Access.

**Configuration / enablement.** Feature flags get reworked (PHEM-2262596). Error messages become specific enough for customers to fix problems themselves (PHEM-1970553, PHEM-1970555). The area also covers tenant-level notification settings (PHEM-2104076), tenant centralization (PHEM-1970183), regrouped searchable settings, and field management.

For the full initiative → epic → story tree with every item's plan, see [reference/backlog-map.md](reference/backlog-map.md).

## Timeline (as of 2026-10-23)

| Measure | Value |
|---------|-------|
| Items with a future release | 57 of 278 (OffCycle-2026: 36, 26.11: 20, 27.01: 1) |
| Slipped: release date passed, still open | 39 (mostly 26.05–26.10) |
| Unplanned (Fix Version = Backlog) | 182 |
| Latest planned release | 27.01 → about **3.3 months** |
| Pace: stories resolved Done per month | 12.3 (last 6 months), 9.3 (prior 6 months) |
| All 199 open stories at current pace | about **16.2–21.4 months** |

Answer "how long" with both numbers. The plan covers about 3 months, but only 21% of items have a future release. At today's pace, finishing every open story takes about 1.5–2 years. Per-area pace figures are team-months: the area's share of that total, not a separate finish date. See [reference/timeline-method.md](reference/timeline-method.md) for the rules and their limits.

## Answering common questions

| Question | How to answer |
|----------|---------------|
| "What is CRM Core doing about X?" | Find the area in the table above, then cite the epics in `backlog-map.md` with key, status and Fix Version. |
| "When will X ship?" | Give the item's Fix Version target and its state (planned, slipped or Backlog). For a parent, give the branch roll-up. Never promise a date. |
| "Is SR theme X covered by Jira?" | Compare the SR theme count with the area's open Jira items. Name the gaps; Events is currently uncovered. |
| "Which pod owns Y?" | Use **crm-core-product** (adjacent pods). The "Not in the six areas" items are still CRM Core work. |
| Live status of one item | Read it in Jira with `getJiraIssue` (read-only). The snapshot may be stale. |

## Data and Jira fields

- Jira site cloudId `abbe3ee2-54f7-4096-a7a0-62a220d87814`, project PHEM, browse `https://phenompeople.atlassian.net/browse/<KEY>`.
- Product field: `"Product Experience: Product2[Dropdown]" = "Recruiter Experience (RX) - CRM - Core"`.
- Planning fields: `fixVersions` (YY.MM release train, `OffCycle-2026`, `Backlog`), `duedate`, Sprint `customfield_10111` (2-week sprints), Story Points `customfield_10003`.
- `parent` and `fixVersions` only come back with `view: "full"` in `searchJiraIssuesUsingJql`.
- Scope JQL (open, created since 2026-01-01):

```
project = PHEM AND "Product Experience: Product2[Dropdown]" = "Recruiter Experience (RX) - CRM - Core"
AND type IN (Epic, Initiative, Story) AND created >= 2026-01-01
AND status NOT IN (Done, Blocked, "In QA", "PM Acceptance Queue")
```

## How items are placed in an area

Each item gets exactly one area, matched on its **title** (`crm_core_jira_areas.py`):
1. First, Jira-wording rules (`JIRA_V1_RULES`), in this order: sync, access, events, strong how-to, hiring status, jobs, weak how-to.
2. Then the ServiceNow theme phrases from `rx_theme_rules.py` for the six areas.
3. `BLOCK_RULES` stop known false matches, such as "candidate purge" counting as a job.
4. If nothing matches, the item takes its nearest classified parent's area. Otherwise it goes to "Not in the six areas".

Descriptions are not used, because Jira story templates contain boilerplate that causes false matches. Result: 133 items matched directly, 10 inherited and 135 matched nothing.

## Metadata exclusion

Before placing items, `exclude_metadata` removes every item whose title or description matches `\bmeta[\s-]?data` (case-insensitive). It also removes the descendants of items with metadata in the **title**, such as the three stories under PHEM-1974353, the PhenomHire metadata service and DAAL epic. Children of an item removed only for its description stay in and attach to their nearest remaining ancestor. In the 2026-10-23 run, this removed 7 items for their title, 20 for their description and 3 as children, leaving 278 of 308. The snapshot lists them under `excluded`, and the HTML header shows them in a collapsible note.

## Files

| File | Role |
|------|------|
| `product-copilot-beta/knowledge/servicenow-service-requests/data/crm-core-jira/page*.json` | Raw Jira pages (summary, type, status, parent) |
| `…/data/crm-core-jira/plan-page*.json` | Raw planning fields (Fix Versions, due date, sprint, story points) |
| `…/data/crm-core-jira/context-parents.json` | Parents outside the filter, shown greyed as context |
| `…/data/crm-core-jira/throughput.json` | Done-story counts used for pace, with their JQL |
| `…/snapshot-crm-core-jira-areas.json` | Classified nodes, counts, summaries and timeline |
| `…/crm-core-jira-areas.html` | Summary table with foldable hierarchy and timeline (open items created since 2026-01-01) |
| `…/crm-core-jira-areas-all.html` | Same six areas for every Initiative, Epic and Story in the product filter, any year and any status. Run 2026-10-26. Built by `build_crm_core_jira_all.py` from `data/crm-core-jira-all/` |
| `.cursor/skills/servicenow-service-requests/scripts/crm_core_jira_*.py` | Classifier, summaries, timeline |
| `…/scripts/build_crm_core_jira_html.py`, `build_crm_core_backlog_map.py` | HTML and `reference/backlog-map.md` |

## Refresh

1. Run the scope JQL with `searchJiraIssuesUsingJql`, `view: "full"`, and `maxResults: 100`, paging with `nextPageToken`.
   - Fields for `page*.json`: `summary, issuetype, status, parent, created, description`.
   - Fields for `plan-page*.json`: `fixVersions, duedate, customfield_10111, customfield_10003, description, status, issuetype`.
   - Large pages are saved to a file; copy it into `data/crm-core-jira/`.
2. Fetch any new parents outside the filter into `context-parents.json`.
3. Rerun the two Done-count JQLs in `throughput.json` for the new 6-month windows and update the counts.
4. Update `EXPECTED_TOTAL` in `crm_core_jira_areas.py`. If the area mix changed, rewrite the bullets in `crm_core_jira_summaries.py` from the titles.
5. From `.cursor/skills/servicenow-service-requests/scripts/`, run `python3 crm_core_jira_areas.py && python3 build_crm_core_jira_html.py && python3 build_crm_core_backlog_map.py`.
6. Check that the area counts sum to the total and that each counted key appears once in the HTML trees. Update the numbers in this file.

## Reference files

- [reference/backlog-map.md](reference/backlog-map.md): every area's initiative → epic → story tree, with Fix Version plans (generated).
- [reference/timeline-method.md](reference/timeline-method.md): how the planned and pace timelines are computed, and their limits.
- [reference/sr-themes.md](reference/sr-themes.md): what customers raise in ServiceNow for each of the six areas, and how Jira covers it.

## Related skills

- **crm-core-product**: scope, personas, adjacent pods, FRD story naming.
- **servicenow-service-requests**: SR sheet, theme rules, playbook.
- **release-calendar**: YY.MM release cadence and live schedule.
- **jira-api** / **read-only-inputs**: field IDs and the read-only policy.
- **create-prd** / **write-stories-from-problem**: turning an area gap into an FRD.
