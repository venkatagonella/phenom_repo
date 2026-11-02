---
name: inbox meetings
type: skill
description: "Post-sync inbox meeting triage — 5-day rule, action extraction, filing consumed notes. Load after Granola sync or when processing meeting notes in the vault inbox."
always: false
triggers: [inbox meetings, triage inbox, process inbox, process meetings, meeting inbox, extract actions from meetings, 5-day rule, consume meeting notes]
---

# Inbox & Meetings (Personal OS)

## When to Use This Rule

This rule activates when the user says (or similar):
- "triage my inbox meetings" / "process inbox meetings"
- "extract actions from meetings"
- "apply the 5-day rule" / "archive old inbox meetings"
- "consume meeting notes" / "file this meeting note"

**Not for fetching from Granola** — use `@skills/granola-sync.md` first (`sync my Granola`, `Granola sync`).

## Prerequisites

1. Meeting notes already in the vault (via `@skills/granola-sync.md`, or manually placed).
2. **`{vault_root}` resolved** — same as Granola sync Execution contract §1:
   - Read `@me.md` → `## Granola vault`
   - Else discover `99_System/granola/routing.json` in workspace
   - Else ask the user

All paths below are under `{vault_root}/`. Create folders/files on first use if missing.

## Skill split (vs Granola sync)

| Task | Skill |
|------|-------|
| Fetch from Granola MCP, write markdown, update tracking, auto-route on sync | `@skills/granola-sync.md` |
| Process inbox after sync: extract actions, manual filing, 5-day archive, mark consumed | **This skill** |

Auto-routing rules on sync (product, miscellaneous) live in `@skills/granola-sync.md` and `{vault_root}/99_System/granola/routing.json`. This skill handles **post-sync inbox workflow**.

## Inbox rules

- **Inbox is flat:** `{vault_root}/00_Inbox/Meetings/` has **no subfolders** (no separate Granola folder). Unrouted meetings land here directly.
- **New topics or ideas** (non-meeting) → save to `{vault_root}/00_Inbox/`.
- **5-day rule:** Only meetings from the **last 5 days** (by date in filename `YYYY-MM-DD_HHMM_*.md`, else file mtime) stay in Inbox. Anything **older than 5 days** still in Inbox → move to `{vault_root}/90_Archives/Meetings/`.
- When a meeting is **consumed** (actions extracted, filed to project/person), move the note to the relevant area or to `{vault_root}/90_Archives/Meetings/`.
- **Extracted actions** → append to `{vault_root}/01_Tasks/Tasks.md` (create file if missing).

## Paths (under `{vault_root}`)

| Purpose | Path |
|---------|------|
| Inbox (last 5 days, flat) | `00_Inbox/Meetings/` |
| General inbox (ideas/topics) | `00_Inbox/` |
| Product meetings | `05_Areas/Product/Meetings/` |
| Miscellaneous meetings | `05_Areas/Miscellaneous/Meetings/` |
| Archive (older untriaged or consumed) | `90_Archives/Meetings/` |
| Task list | `01_Tasks/Tasks.md` |

If `{vault_root}/99_System/granola/routing.json` exists, prefer path keys from config (`paths.inbox`, `paths.archive`, etc.) — same as `@skills/granola-sync.md`.

## Execution steps

### 1. Resolve vault and list inbox

1. Resolve `{vault_root}` (see Prerequisites).
2. List `.md` files in `{vault_root}/00_Inbox/Meetings/` (exclude `README.md`).

### 2. Apply 5-day rule

For each inbox meeting file older than **5 days** (filename date or mtime):
- Move to `{vault_root}/90_Archives/Meetings/` (keep filename).
- Report moved files.

### 3. Process remaining inbox (user-directed)

For each meeting the user wants to process (or all if asked):
1. Read the note (summary + transcript sections).
2. Extract action items, decisions, and follow-ups.
3. Append actions to `{vault_root}/01_Tasks/Tasks.md` with meeting title and date as context.
4. **File the note:**
   - Product-related → move to `05_Areas/Product/Meetings/`
   - Other → move to `05_Areas/Miscellaneous/Meetings/` or `90_Archives/Meetings/` once consumed
5. Confirm what was extracted and where the file was moved.

### 4. Report summary

Provide:
- Files archived (5-day rule)
- Files processed (actions extracted, destination)
- Remaining inbox count

## Important notes

- **Granola sync first:** If inbox is empty but user expects new meetings, run `@skills/granola-sync.md` before this skill.
- **No duplicate archive on sync:** Granola sync also archives old untriaged inbox files (step 6). Either skill may perform the move — skip if already archived.
- **Vault root:** Set in `me.md` under `## Granola vault`; never hardcode user-specific paths.

---
**Last Updated**: 2026-07-08
