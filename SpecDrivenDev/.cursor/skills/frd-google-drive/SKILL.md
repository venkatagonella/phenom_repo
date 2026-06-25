---
name: frd-google-drive
description: >-
  Publish a Functional Requirements Document (FRD) to Google Drive as a Google Doc.
  Use after drafting FRD content locally, when the user asks for Drive output,
  or as the final step of any FRD authoring workflow.
---

# FRD → Google Drive

The **primary deliverable** for SpecDrivenDev is a **Functional Requirements Document (FRD)** published as a **Google Doc** in the user's Google Drive. Users may say "PRD" — treat that as an alias for FRD.

Preserve the segregated Part A / B / C / D structure from `templates/frd-template.md` when publishing.

## When to use

- Final step after drafting `specs/{initiative-slug}/frd.md`
- User asks to "put it in Drive", "create a Google Doc", or "publish the FRD"
- Any FRD workflow (`spec-from-jira`, `prd-authoring`) ends here unless the user explicitly wants local-only

## Google MCP tools

Tools are provided by the **product-copilot-beta Google MCP** (`requires: google`). Read tool schemas before calling.

Reference: `../product-copilot-beta/skills/google.md`

| Task | Tool | Key parameters |
|------|------|----------------|
| Create FRD Google Doc | `create_google_doc` | `title` (required), `content` (optional — plain text or markdown-like) |
| Update existing Doc | `update_google_doc` | `document_id`, `content`, `mode`: `replace` or `append` |
| Find existing FRDs | `list_drive_files` | `query`, `mime_type`: `application/vnd.google-apps.document` |
| Read existing Doc | `read_google_doc` | `document_id` (URL or ID) |

**Auth**: Uses the connected user's OAuth token. If Google is not connected, follow the fallback below.

**Folder placement**: `create_google_doc` does not accept a parent folder ID — new Docs land in the user's Drive root. After creation, tell the user to move the Doc into their team folder if needed, or share the Doc link for them to organize.

## Document naming

Use this convention unless the user specifies otherwise:

```
FRD - [Initiative] - [Customer/Feature] - YYYY-MM-DD
```

Examples:

- `FRD - Bulk Tagging - Acme Corp - 2026-06-15`
- `FRD - Pipeline Visibility - Internal - 2026-06-15`

Derive `[Initiative]` from the Epic title or primary feature. Use today's date for `[YYYY-MM-DD]`.

## Workflow

```
Task Progress:
- [ ] Confirm local draft is complete (specs/{slug}/frd.md)
- [ ] Build Google Doc title per naming convention
- [ ] Create Google Doc with full FRD content
- [ ] Return Doc URL to user; update local draft metadata with Drive link
- [ ] (Optional) User moves Doc to team folder
```

### 1. Prepare content

Read `specs/{slug}/frd.md`. Strip or adapt markdown that won't render well if needed — headings and bullet lists work as plain text in `create_google_doc`.

For very long FRDs (> ~50k characters), create the Doc with a title and executive summary first, then `update_google_doc` with `mode: "append"` in sections.

### 2. Create the Google Doc

```
create_google_doc({
  title: "FRD - [Initiative] - [Customer/Feature] - YYYY-MM-DD",
  content: "<full FRD body from local draft>"
})
```

The tool returns `documentId`, `title`, and `url`. Share the **url** with the user as the primary deliverable.

### 3. Update local draft metadata

Add or update the **Google Drive** line at the top of `specs/{slug}/frd.md` with the Doc URL. Keep the local file as a draft mirror for iteration.

### 4. Revisions

When the user updates requirements:

1. Edit `specs/{slug}/frd.md` locally
2. `update_google_doc({ document_id: "<url>", content: "<updated body>", mode: "replace" })`
3. Confirm the change with the user

## User inputs (optional)

Ask only when missing and relevant:

| Input | When needed |
|-------|-------------|
| Customer / feature name | For Doc title when not clear from Jira |
| Preferred Drive folder | Cannot set via MCP today — user moves Doc after creation |
| Existing Doc URL | When updating instead of creating |
| Shared drive | Not supported by current MCP — note in response |

## Fallback when Google MCP is unavailable

If Google tools are not connected or calls fail:

1. **Complete the local draft** at `specs/{initiative-slug}/frd.md`
2. Tell the user:
   - The FRD is ready locally at that path
   - Google Drive was not available: `[error message]`
   - To connect: from `../product-copilot-beta/mcp`, run `node bin/copilot-mcp.js google`, then restart Cursor with `SpecDrivenDev` as the workspace root
3. Manual upload options:
   - **Google Docs**: File → Open → Upload → select `frd.md`, or paste content into a new Doc
   - **Drive**: Upload `frd.md` to the desired folder, then open with Google Docs
4. Use the naming convention above when they create the Doc manually

Do not block delivery on Google — always produce the local draft first.

## Related skills

- **create-prd** — orchestrator
- **read-only-inputs** — do not update source Docs; only create new FRD Doc
- **prd-authoring** — FRD content before publish
- **write-stories-from-problem** — Part C content
