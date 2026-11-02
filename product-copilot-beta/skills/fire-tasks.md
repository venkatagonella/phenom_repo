---
name: fire-tasks
type: skill
description: "Manages weekly FIRE project tasks in Jira. Handles weekly planning (review, create, update, close tasks), enforces CW-prefixed naming, and ensures each task has a clear definition of done. Load when the user mentions FIRE tasks, planning their week, CW week numbers, or asks to review/create/close weekly tasks."
always: false
triggers: [FIRE, fire tasks, plan my week, weekly tasks, CW, calendar week, week planning, close tasks]
---

# FIRE Task Management

The FIRE project (`project = FIRE` in Jira) is a personal weekly task tracker. Each task represents a discrete deliverable for a given calendar week.

---

## Task Format

### Title
```
CW{N} - {Topic} - {Specific Outcome}
```
- `CW{N}` = ISO calendar week number (e.g. `CW19`)
- Multi-week tasks: `CW18 - CW19 - {Topic} - {Outcome}`
- Title must describe the **outcome**, not the activity

**Examples:**
- `CW19 - Lokalise POC - Final Review of Project Documentation`
- `CW19 - Group Interviews - Mock Up of Next Phase Handed Off to Product/Dev Team for Planning`
- `CW18 - CW19 - Skills Based Interviewing - Framework Alignment Completed and Handed to UX`

### Body (Definition of Done)
Every task must have a description listing what "done" looks like. Use a checklist:

```
Definition of Done:
- [ ] [Specific, verifiable deliverable]
- [ ] [Specific, verifiable deliverable]
- [ ] [Outcome handed off / decision made / artifact produced]
```

Each item must be a concrete, verifiable outcome — not a vague activity.

**Example body:**
```
Definition of Done:
- [ ] All Lokalise POC documentation reviewed and comments resolved
- [ ] Final go/no-go recommendation documented and shared with stakeholders
- [ ] Any open questions escalated or closed
```

### Issue Type
- Use **Task** for most FIRE items (default)
- Use **Story** only if it's an OKR-tracked deliverable that needs sprint visibility

---

## Weekly Planning Workflow

When the user says "plan my week" or asks to review FIRE tasks:

### Step 1 — Fetch current open tasks
Query: `project = FIRE AND assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`

### Step 2 — Identify stale tasks
Any task with a CW prefix **earlier than the current week** is stale. For each stale task, ask:
> "[FIRE-XXXX] {summary} — from CW{N}. Close it, carry it forward to CW{current}, or update the scope?"

Wait for the user's answer before making any changes.

### Step 3 — Reconcile with the user's plan
Compare the user's stated priorities for the week against open tasks:
- **Match found** → Rename to `CW{current}` if still on an old CW, confirm the DoD is still accurate
- **No match** → Create a new task (see creation below)
- **Open task not in the plan** → Flag it and ask whether to close or keep

### Step 4 — Execute changes
After the user confirms the plan, in one batch:
- **Update** summaries for carried-forward tasks (CW prefix + any scope changes)
- **Close** stale tasks no longer needed (transition id `111` → Done)
- **Create** new tasks for new priorities

Always confirm the final state by listing the resulting open tasks.

---

## Creating a New Task

```json
{
  "project": {"key": "FIRE"},
  "summary": "CW{N} - {Topic} - {Outcome}",
  "issuetype": {"name": "Task"},
  "priority": {"name": "Major"}
}
```

After creation, update the description (two-step — FIRE project may apply a template):
1. Create the issue
2. Wait ~1s, then PATCH/PUT the description with the Definition of Done checklist

---

## Closing a Task

Use transition id `111` (Done):
```json
POST /rest/api/3/issue/{key}/transitions
{"transition": {"id": "111"}}
```

---

## Current Week Helper

Today's ISO week: calculate from the current date. In 2026, CW19 = May 4–10.

Always confirm the ISO week number before labeling tasks, especially near year boundaries.
