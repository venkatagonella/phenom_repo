
---
name: granola sync
type: skill
description: "Sync Granola meeting notes to local markdown. Triggers on sync/update/latest Granola meetings. MCP + vault files only — read"
always: false
triggers: [granola sync]
---

# Granola Meeting Notes Sync

## When to Use This Rule

This rule activates when the user says (or similar):
- "sync my Granola" / "sync Granola meetings" / "Granola sync"
- "update my Granola files" / "update my Granola meetings"
- "get my latest meetings" / "sync my latest granola meetings"
- "sync according to my syncing rules" / "run granola sync"

## Execution contract (follow every time — no shortcuts)

1. **Resolve `{vault_root}`** — before any vault file I/O. **Never hardcode a user-specific absolute path.**

   Resolve in this order (first match wins):

   1. **`me.md`** — read `@me.md` for a `## Granola vault` section with the absolute path to the vault folder (each user sets this once; file is gitignored).
   2. **Discover in workspace** — search open workspace folder(s) for `99_System/granola/routing.json`. The vault root is the directory that contains `99_System/` (strip `/99_System/granola/routing.json` from the found path).
   3. **Ask the user** — if still unknown, ask for the vault folder path once and suggest adding it to `me.md` under `## Granola vault`.

   Do **not** read `routing.json` to bootstrap `{vault_root}` — the file lives at `{vault_root}/99_System/granola/routing.json`, so its location depends on `{vault_root}` already being known (from steps 1–3 above).

2. **Load config** (only after `{vault_root}` is resolved):

   - Read `{vault_root}/99_System/granola/routing.json` — **single source of truth** for paths, `product.title_keywords`, and `default_bucket`
   - Read `{vault_root}/99_System/granola/backup_tracking.json` — skip IDs in `backed_up_meeting_ids`

   `{vault_root}` is fixed after step 1 — do **not** change it based on fields inside `routing.json`. That file configures routing only; vault location comes exclusively from step 1 (me.md, workspace discovery, or user prompt).

   All paths below are relative to `{vault_root}`. Combine with `config.paths.base` from routing.json (e.g. `{vault_root}/{base}/00_Inbox/Meetings/`).

3. **Sync method:** Granola MCP server **`user-granola sync`** only (`list_meetings` → `get_meetings` → `get_meeting_transcript` per meeting) + **Write** markdown into the vault. **Do not** create or run Python/shell sync scripts, subagents, or `/tmp` automation — the rule + MCP is the implementation.

4. **Routing:** Apply the priority table below using **only** names/keywords from `routing.json` — never invent folders or hardcode people lists in code.

5. **After sync:** Update `backup_tracking.json`, then archive Inbox files older than 5 days per config.

For post-sync inbox processing (action extraction, filing consumed notes, manual triage), see `@skills/inbox-meetings.md`.

## Target Locations (from routing config)

All paths are defined in **`{vault_root}/99_System/granola/routing.json`**. When resolving paths, use `{vault_root}` + `config.paths.base` + path key (e.g. `config.paths.product`). If the config is missing, save to `{vault_root}/00_Inbox/Meetings/` (flat).

| Bucket | Config path key | Resolved path (example) |
|--------|-----------------|--------------------------|
| **Product** | `paths.product` | `{base}/05_Areas/Product/Meetings/` |
| **Miscellaneous (default)** | `paths.miscellaneous` | `{base}/05_Areas/Miscellaneous/Meetings/` |
| **Inbox (manual triage)** | `paths.inbox` | `{base}/00_Inbox/Meetings/` — flat, last 5 days only; not used by auto-routing on sync |
| **Archive** | `paths.archive` | `{base}/90_Archives/Meetings/` (old untriaged Inbox files) |

**Routing config** (`99_System/granola/routing.json`) contains: `product.title_keywords`, `default_bucket` (usually `"miscellaneous"`), and `paths`.

## File Naming Convention

Use this exact format: `YYYY-MM-DD_HHMM_Meeting_Title.md`

Examples:
- `2026-01-15_0504_Focus_on_POV.md`
- `2026-01-14_0905_Guru_Sebastian.md`

Rules for title conversion:
- Replace spaces with underscores `_`
- Replace `/` with `_`
- Replace `<>` with nothing (remove them)
- Keep `&` as is
- Remove any other special characters

## Routing (before creating each file)

After calling `get_meetings(meeting_ids)` or equivalent to get metadata (title, attendees) for a new meeting:

1. **Resolve `{vault_root}`** (see Execution contract §1), then **load config** from `{vault_root}/99_System/granola/routing.json`. If missing, save to `{vault_root}/00_Inbox/Meetings/` (flat).
2. **Decide bucket** using meeting **title** (case-insensitive). Apply in this order; first match wins.

| Priority | Rule | Condition | Save path (use config) |
|----------|------|-----------|------------------------|
| 1 | **Product** | Title contains any of `config.product.title_keywords` | `{base}/{paths.product}/` |
| 2 | **Default** | No product keyword match | `{base}/{paths[config.default_bucket]}/` (typically `paths.miscellaneous`) |

3. **Resolve save path:** `config.paths.base` + `/` + the bucket path from the table. Create the meeting file in that folder (same filename and content format as below).

Edit `product.title_keywords` in `routing.json` as your team and meeting naming conventions change.

## Granola MCP (Cursor)

When calling Granola from Cursor, use **MCP server name `user-granola sync`** (note the space). Cursor derives this from your `mcp.json` key — e.g. `"granola sync"` becomes `user-granola sync`. Do **not** use `Granola`, `granola`, or `user-granola` (no space). Tool names: `list_meetings`, `get_meetings`, `get_meeting_transcript`, `query_granola_meetings`. Always use server **`user-granola sync`** with these tools.

## Execution Steps

### 1. Find New Meetings

Call the Granola MCP with server **`user-granola sync`**, tool **`list_meetings`**, and `time_range: "this_week"` (or `"last_30_days"` for a longer window).

### 2. Check Tracking File

Read the tracking file at `{vault_root}/99_System/granola/backup_tracking.json`.

This file contains `backed_up_meeting_ids` — skip any meeting ID already in this list. If the file does not exist, create it on first sync.

### 3. Get Meeting Content

For each NEW meeting (not in tracking file), using MCP server **`user-granola sync`**:
1. Call **`get_meetings`** with the meeting IDs (max 10 per call; batch if needed) to get metadata (title, attendees, date) and the **AI-generated summary**.
2. For **each** meeting, call **`get_meeting_transcript`** with that meeting's `meeting_id` to get the **full verbatim transcript**. (One call per meeting.)
3. Run the **Routing** logic above to get the save path for this meeting.
4. Create the file using both the summary (from `get_meetings`) and the full transcript (from `get_meeting_transcript`). If `get_meeting_transcript` returns no content, still create the file and add "*Full transcript not available.*" under the Full Transcript section.

### 4. Create Meeting Files

For each meeting, create the markdown file **in the path returned by Routing** with this structure:

```markdown
# [Meeting Title]

**Meeting ID:** [uuid]
**Date:** [YYYY-MM-DD HH:MM]
**Type:** meeting
**Participants:** list participants

---

## Meeting Notes

[AI summary from get_meetings — preserve structure and formatting]

---

## Full Transcript

[Verbatim transcript from get_meeting_transcript — include full content. If unavailable, add: *Full transcript not available.*]

---

**Chat with meeting transcript:** [link if available]

*Synced from Granola on [today's date]*
```

### 5. Update Tracking File

After creating all files, update the tracking file at `{vault_root}/99_System/granola/backup_tracking.json`:
- Add all new meeting IDs to `backed_up_meeting_ids` array
- Update `last_updated` timestamp to current datetime

### 6. Archive Old Untriaged Files (Inbox only)

After updating the tracking file, move any meeting files **still in the Inbox** that are older than 5 days to Archive:

- **Scope:** Only `.md` files directly in the Inbox folder (`{base}/{paths.inbox}/`). Exclude `README.md`.
- **Age:** Use the date from the filename when it matches `YYYY-MM-DD_HHMM_*.md`; otherwise use the file's modification date. If that date is more than **5 days** before today, the file is considered old.
- **Action:** Move each such file to `{base}/{paths.archive}/` (keep the same filename).
- Only files that were **not** auto-routed to Product or Miscellaneous remain in Inbox; those are the only candidates for archive. Auto-routed files are never in Inbox, so they are never moved to Archive by this step.

### 7. Report Summary

After completion, provide a summary table showing:
- Date
- Meeting name
- File created (filename)
- Folder (e.g. `05_Areas/Product/Meetings`, `05_Areas/Miscellaneous/Meetings`, `00_Inbox/Meetings`)

If any files were moved to Archive in step 6, list them (e.g. "Archived to {paths.archive}: file1.md, file2.md").

## Important Notes

- **Duplicate prevention:** The tracking file prevents re-importing meetings, even if the file was moved or deleted.
- **Inbox is flat:** `00_Inbox/Meetings/` is for **manual triage** only — meetings placed here by hand or moved during inbox processing. Auto-routed sync does **not** land here.
- **Auto-triage:** Product keyword matches (WBR, Scrum, Recruiter Hub, etc.) → `05_Areas/Product/Meetings/`. Everything else → `05_Areas/Miscellaneous/Meetings/` per `default_bucket`.
- **Archive:** Only untriaged meetings that stayed in Inbox and are older than 5 days are moved to the archive path from config.
- **Vault root:** Set once in `me.md` under `## Granola vault` (absolute path). Example: `~/Documents/Cursor/Product Co-Pilots/Personal - AI Product Leader`. Resolved only via Execution contract §1 — never from `routing.json`.
- **Config:** Edit `{vault_root}/99_System/granola/routing.json` to add/remove keywords in `product.title_keywords`, change `default_bucket`, or adjust paths in `paths`. Tracking: `{vault_root}/99_System/granola/backup_tracking.json`.
- **Preserve formatting:** Keep bullet points, headers, and structure from Granola's notes.
- **Full transcript:** For each meeting, call **`get_meeting_transcript`** (server `user-granola sync`) and include the result in a **Full Transcript** section so the file contains the verbatim transcript, not only the summary.
- **Include transcript links:** If the meeting has a transcript link, include it at the bottom.

## Error Handling

- If Granola MCP returns no results, try `time_range: "last_30_days"` or ensure server **`user-granola sync`** is used (not `Granola`, `granola`, or `user-granola`).
- If a meeting has no documents or no transcript, still create the file with basic metadata and summary; use "*Full transcript not available.*" if transcript is missing.
- If tracking file doesn't exist, create it fresh.
- If routing config doesn't exist, save all meetings to Inbox (flat).

---
**Last Updated**: 2026-07-08
