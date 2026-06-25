---
name: read-only-inputs
description: >-
  Enforces read-only handling of all Jira issues and source documents used as
  input for PRD/FRD creation. Use whenever ingesting Jira keys, Confluence,
  Google Drive docs, or support tickets — before and during create-prd workflow.
---

# Read-Only Inputs Policy

**No changes or creation of any items in the Jira issues or documents given as additional information for creating the functional specification or product requirement document (PRD).**

## Scope

Applies to **every input** the user provides for PRD creation:

- Jira entities (Epic, Story, Bug, Task, ticket, any issue type)
- Confluence pages
- Google Docs and Sheets used as reference
- Local files the user points to as source material
- Support ticket content

## Allowed (read)

| System | Read tools |
|--------|------------|
| Jira | `getJiraIssue`, `searchJiraIssuesUsingJql`, `search`, `getJiraIssueRemoteIssueLinks`, `getTransitionsForJiraIssue` (read status only) |
| Confluence | `getConfluencePage`, `searchConfluenceUsingCql`, `search` |
| Google Drive | `list_drive_files`, `read_google_doc`, `read_google_sheet` |
| Local | Read file contents |
| Granola | Query meeting tools (read) |

## Forbidden (write on inputs)

| System | Forbidden tools / actions |
|--------|---------------------------|
| Jira | `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, `createIssueLink`, `addWorklogToJiraIssue` |
| Confluence | `createConfluencePage`, `updateConfluencePage`, any comment create tools |
| Google (source docs) | `update_google_doc` / `update_google_sheet` on **input** files user provided |
| Local source files | Overwriting user-supplied reference files |

## Allowed outputs (create new only)

| Output | Action |
|--------|--------|
| `specs/{slug}/frd.md` | Create or update **new** local FRD draft in this workspace |
| Google Doc (FRD) | `create_google_doc` — **new** document via **frd-google-drive** |
| FRD revision | `update_google_doc` only on the **FRD Doc this workflow created**, not source inputs |

## If user asks to update Jira or source doc during PRD work

1. Decline the write during PRD authoring
2. Explain: this workflow produces a **new** FRD only
3. Offer: include suggested Jira story text or comments **inside the FRD** for manual copy-paste
4. Offer: separate task after PRD is approved (user must explicitly request)

## Confirmation to user

When delivering an FRD, state:

> All input Jira issues and source documents were read only. No input items were created or modified. The deliverable is [Google Doc URL / specs path].

## Related skills

- **create-prd** — primary workflow
- **spec-from-jira** — Jira read path
- **spec-inputs** — Drive, Confluence, meetings read path
