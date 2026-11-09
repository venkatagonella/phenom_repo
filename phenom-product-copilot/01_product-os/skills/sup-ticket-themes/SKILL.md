---
name: sup-ticket-themes
description: >-
  Classifies Jira SUP (support) tickets for Recruiter Experience CRM Core, CRM Profile,
  CRM Messaging and CRM Automations into themes, and associates each theme with non-SUP
  PHEM Initiatives, Epics and Stories (explicit SUP links + title phrase matches).
  Use when the user asks about SUP tickets, support-ticket themes, support demand by CRM
  area, or which Jira work addresses support themes. Jira is read-only; never invent themes.
metadata:
  owner: gvsrk
  status: sandbox
---

# SUP ticket themes (CRM Core, Profile, Messaging, Automations)

## Source of truth (only)

Jira, read-only, via the Atlassian MCP (`searchJiraIssuesUsingJql`, cloudId `abbe3ee2-54f7-4096-a7a0-62a220d87814`).

| Area | `Product Experience: Product2` value |
|------|--------------------------------------|
| CRM Core | `Recruiter Experience (RX) - CRM - Core` |
| Profile | `Recruiter Experience (RX) - CRM - Profile` |
| Messaging | `Recruiter Experience (RX) - CRM - Messaging and Campaigns` |
| Automations | `Recruiter Experience (RX) - CRM - Automation` |

SUP tickets, one query per area:

```
project = SUP AND created >= "2026-01-01" AND "Product Experience: Product2[Dropdown]" = "<value>"
```

Non-SUP Jira pool, same four values:

```
project = PHEM AND Product2 in (<4 values>) AND issuetype in (Initiative, Epic, Story) AND created >= "2026-01-01"
```

PHEM Initiative / Epic / Story keys found in SUP issuelinks are fetched with `key in (...)` to get
their status and created date.

Local exports: `01_product-os/knowledge/servicenow-service-requests/data/sup-2026/`

| File | Content |
|------|---------|
| `sup-crm-core.json` | SUP, CRM Core |
| `sup-crm-profile-a.json`, `sup-crm-profile-b.json` | SUP, Profile (created before / from 2026-06-01) |
| `sup-crm-messaging-a.json`, `sup-crm-messaging-b.json` | SUP, Messaging (two pages of the same query) |
| `sup-crm-automation.json` | SUP, Automations |
| `phem-crm-core-2026.json`, `phem-crm-profile-messaging-automation-2026.json` | PHEM pool |
| `phem-linked-from-sup.json` | PHEM items linked from SUP tickets |

Each SUP file stores `jql`, `expected` (Jira total) and `count`; the loader exits if they differ.

## Hard rules

1. Jira is **read-only**. Never call createJiraIssue, editJiraIssue, transitionJiraIssue,
   addCommentToJiraIssue, createIssueLink or addWorklogToJiraIssue. See `read-only-inputs`.
2. Use only the exports above as evidence. Do not add themes, counts or Jira items from
   memory, Glean, Confluence or other documents.
3. Classify on the SUP **summary only**. Descriptions were tested as a fallback and most
   description-only matches were wrong, so they are not used.
4. Never force a label. A summary with no matching phrase stays `Unclassified`.
5. PII: store summaries with emails as `[email]` and phones as `[phone]` (classification
   strips these placeholders); the report shows both as `xxxxxx`. Do not display
   descriptions, reporters, assignees or client names. Do not commit the exports.
6. Every number you report must state its filter (area value, created date range) and count.
7. Only open SUP tickets are analysed by default: tickets in Jira's Done status category
   (Done, In Prod, Closed) are removed and counted. Pass `--include-done` to the CLI to keep them.

## Method

- `scripts/sup_theme_rules.py`
  - `SUP_RULES[area]`: ordered `(theme, [regex])`; first match wins. A theme may appear twice
    so specific phrases win early and broad phrases late (e.g. CRM Core performance).
  - `PHEM_RULES[area][theme]`: title phrases for PHEM items; one item may match several themes.
  - `PHEM_EXCLUDE`: known false positives per theme (e.g. "Post-MVP", "call forwarding").
  - `ENGINEERING_EXEMPT`: themes that may match engineering-only items (performance, security).
  - Every theme in `SUP_RULES` must have a `PHEM_RULES` entry; the loader exits otherwise.
- `scripts/sup_themes.py`
  - Loads and classifies SUP tickets, loads the PHEM pool, builds two associations per theme:
    - **Linked from SUP**: PHEM Initiative / Epic / Story linked from a SUP ticket in the theme.
      Links to Tasks, Sub-tasks and other types are counted, not shown.
    - **Matched by title**: PHEM items in the same area pool whose title matches the theme
      phrases; a Story with no direct match inherits its parent Epic's themes.
  - Removes Done, Blocked and pre-2026 items from both methods and counts them.
  - Reuses `is_engineering` and `build_tree` from `servicenow-service-requests/scripts/theme_jira_map.py`.

## Scripts

```bash
# Theme counts, coverage and Jira association counts per area
python3 01_product-os/skills/sup-ticket-themes/scripts/sup_themes.py \
  --sup-dir 01_product-os/knowledge/servicenow-service-requests/data/sup-2026 \
  --dump-unclassified /tmp/sup-unclassified.tsv

# Rebuild the HTML report; adds the "SUP ticket themes" tab (default --sup-dir <csv dir>/sup-2026)
python3 01_product-os/skills/servicenow-service-requests/scripts/build_crm4_area_themes_html.py \
  --csv 01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --out 01_product-os/knowledge/servicenow-service-requests/crm-4-areas-sr-themes-jan-aug-2026.html
```

## Refreshing the data

1. Run each SUP JQL with `searchResultMode: count` to get the total; store it as `expected`.
2. Page with `maxResults` 100 and `nextPageToken`; keep `key, summary, created, status,
   statusCategory, Type of Issue/Request (customfield_16835), components, labels, issuelinks`.
3. Redact emails and phones in summaries before writing. Write `count` and verify it equals `expected`.
4. Re-run the PHEM pool query and the linked-key query; then rerun the scripts above.
5. Read the `--dump-unclassified` output; add phrases only when several titles share wording.
   Spot-check samples per theme before publishing.

## Limits to state in answers

- Title matching misses Jira work worded differently from the theme phrases.
- Few SUP tickets link to PHEM Initiatives, Epics or Stories, so "no associated item" means no
  evidence found in these exports, not that no work exists.
- First-match ordering means a ticket that touches two themes is counted once, under the earlier theme.
