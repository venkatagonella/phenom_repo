---
name: spec-inputs
description: >-
  Read-only ingestion of Google Drive, Confluence, Granola meetings, support
  tickets, and local files for CRM Core PRD creation. Use in Step 2 of create-prd
  when gathering Google Drive docs or supplemental context beyond Jira.
---

# Spec Inputs

Collect and prioritize source material before FRD authoring. **Check existing context before asking the user to restate it.**

Section segregation follows **`../product-copilot-beta/policies/jira-story-rules.md`** — route gathered content to the correct FRD part (A–D) via **prd-authoring**.

## Input priority

| Source | When to use | Skill / tool |
|--------|-------------|--------------|
| Jira keys provided | User gives issue keys | **spec-from-jira** (Step 1) |
| **Google Drive** | User says "my Google Drive", provides Doc/Sheet URL, or PRD needs Drive context | See **Google Drive** section below (Step 2) |
| Meeting or "what we discussed" | Past customer/PM calls | Granola (below) |
| Confluence URL or page ID | Published spec, design doc | `getConfluencePage` |
| Unknown internal topic | Terminology, past decisions | Atlassian `search` or search-company-knowledge skill |
| Local workspace files | Prior drafts, notes | Read `specs/` or user-provided paths |
| User paste | Ad-hoc requirements | Use directly; flag gaps as Open Questions |

## Granola (meetings)

When the user mentions a meeting, decision, or person from a past conversation:

1. Read Granola MCP tool schema
2. Call `query_granola_meetings` with a focused query (customer name, feature, date range)
3. Preserve citation links from the response
4. Extract and route content:
   - **Part A** — customer statements, pain points, business impact, stated requirements
   - **Part B** — agreed solution direction, feature scope (if decided)
   - **Part C** — per-story AC, design notes, technical constraints
   - **Part D** — dependencies, timeline, open questions, assumptions

For upcoming meetings related to the topic, use `list_meetings` with a future date range.

If context likely continued on Slack/async, note the gap and offer to check connected tools.

## Google Drive (read-only — Step 2)

When the user references **Google Drive** or provides Doc/Sheet URLs as input for PRD creation:

Reference: `../product-copilot-beta/skills/google.md`

| Task | Tool |
|------|------|
| Find files by name or topic | `list_drive_files(query: "…", mime_type: optional)` |
| Read a Google Doc | `read_google_doc(document_id)` — URL or ID from `/d/…/` |
| Read a Google Sheet | `read_google_sheet(spreadsheet_id, sheet_name?, max_rows?)` |

### Workflow

1. If user gives specific URLs/IDs → `read_google_doc` / `read_google_sheet` for each
2. If user says "information in my Google Drive" → `list_drive_files` with customer name, feature, or initiative keywords; read all relevant hits
3. Extract content for **Problem Breakdown** in Part A:
   - Customer statements → **What the Customer Is Asking For**
   - Workflow pain → **Related Problems**
   - Constraints → Customer ask type `Constraint`
4. Add every file to **Source Inputs** with type `Google Doc` or `Google Sheet`

**Read-only:** Do not `update_google_doc` or `update_google_sheet` on source files. The **new** FRD is a separate Doc created by **frd-google-drive**.

## Confluence

When a Jira issue or user references a Confluence page:

```
getConfluencePage(
  cloudId: "<from getAccessibleAtlassianResources>",
  pageId: "<numeric ID or tiny-link from /wiki/x/ URL>",
  contentFormat: "markdown"
)
```

Resolve `cloudId` via `getAccessibleAtlassianResources` if not known.

When Confluence content mixes problem and solution, **split** into Part A vs. Part B during synthesis.

## Atlassian search

For broad discovery (no specific page or key):

```
search(query: "<customer name> <feature area>")
```

`cloudId` is derived automatically for Rovo Search. Use when you need related tickets, pages, or prior specs without a direct link.

For targeted Jira-only queries, use `searchJiraIssuesUsingJql`. For Confluence CQL, use `searchConfluenceUsingCql`.

The global **search-company-knowledge** skill covers parallel multi-source search patterns in depth.

## Local files

- Existing FRDs: `specs/{slug}/frd.md`
- Template: `templates/frd-template.md`
- Supporting notes: any file alongside the FRD in the initiative folder

Read relevant files before drafting updates.

## Synthesis handoff

After gathering inputs:

1. List sources in the FRD **Source Inputs** table (Part A)
2. Route customer pain to **Part A Customer Issue** and **Problem Breakdown** — never mix with solution
3. Populate **Related Problems** and **What the Customer Is Asking For** tables (Step 2)
4. Route solution direction to **Part B**; story detail to **Part C** via **write-stories-from-problem**
5. Note conflicts or gaps → Open Questions (per Part C block or Part D)
6. Follow **prd-authoring** to draft `specs/{slug}/frd.md` in Step 3

## Minimum context to collect

If inputs are thin, ask only for what's missing:

- Customer name and segment (if shareable)
- Source (CS call, QBR, support ticket, sales, internal)
- Affected personas (recruiter, sourcer, recruiting ops, hiring manager)
- Current workflow and where it breaks
- Desired outcome in the customer's words

## Read-only rule

Do **not** create or modify Confluence pages, Google Docs, Jira issues, or user-supplied reference files when gathering inputs. Read only. Output goes to a **new** FRD — see **create-prd** skill.

## Related skills

- **create-prd** — primary orchestrator
- **read-only-inputs** — no writes on source docs
- **spec-from-jira** — Step 1 Jira context
- **write-stories-from-problem** — Step 3 stories from Part A
- **prd-authoring** — Step 3 FRD structure
- **frd-google-drive** — Step 3 publish
