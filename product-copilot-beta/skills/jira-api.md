---
name: jira-api
type: skill
description: "PHEM-specific rules for creating/updating Jira issues via the official Atlassian MCP — two-step creation, required fields + defaults, common errors"
requires:
  - jira
always: false
triggers: [jira, phem, epic, story, stories, bug, ticket, sprint, backlog, issue, jql, task, defect]
---

Use the **official Atlassian MCP** (Claude: `Atlassian`, Cursor: `plugin-atlassian-atlassian`) for all Jira calls. There is no local Jira MCP. This skill only covers what the plugin can't know about PHEM. Field IDs and option values → `policies/jira-constants.md`.

| Task | Tool |
|------|------|
| Create | `createJiraIssue` (custom fields + fix version go in `additional_fields`) |
| Update fields / description | `editJiraIssue` (`fields`, `contentFormat: "markdown"`) |
| Read | `getJiraIssue` |
| Search | `searchJiraIssuesUsingJql` |
| Comment | `addOrEditJiraIssueComment` (`commentBody`) |
| Transition | Discover `listJiraIssueTransitions` → `transitionJiraIssue` |
| Link issues | Discover `createJiraIssueLink` and run it with `executeWrite` |
| Discover fields / allowed values | Discover `getJiraIssueTypeMetaWithFields`, then use `executeRead` (`requiredFieldsOnly: false`; Epic = `6`, Story = `7`) |

Cloud ID: `abbe3ee2-54f7-4096-a7a0-62a220d87814` · Project: `PHEM`

---

## Two-Step Creation (CRITICAL)

PHEM applies a default description template on create that **overwrites any description you send** — re-confirmed with the Atlassian plugin on 2026-10-04 (PHEM-2434013: markdown description sent on `createJiraIssue` was replaced by the Story template; `editJiraIssue` afterwards stuck). Always:

1. `createJiraIssue` — required fields only, **no description**
2. Wait ~1.5 s
3. `editJiraIssue` — `fields: {"description": "<markdown>"}`, `contentFormat: "markdown"` (Epics and Stories alike; no ADF needed)

---

## Required Fields + Defaults

Verified against PHEM create metadata 2026-10-03. Missing any → 400.

| Field | Field ID | Epic | Story | Default when user doesn't specify |
|-------|----------|------|-------|-----------------------------------|
| Product Experience : Product | `customfield_15211` | ✅ | ✅ | **Always ask** — `{"value": "<Experience>", "child": {"value": "<Product>"}}` |
| Priority | `customfield_15212` | ✅ | ✅ | `{"value": "P2"}` |
| Initiative Type | `customfield_15216` | ✅ | ✅ | **Always ask** — do not silently classify roadmap work |
| Release Note Candidate | `customfield_15217` | ✅ | ✅ | `{"value": "NO - Do Not Advertise / Specific Customers"}` |
| How to Enable | `customfield_15218` | ✅ | ✅ | `{"value": "None"}` |
| Feature Flag Available | `customfield_15427` | — | ✅ | `{"value": "NA"}` |
| Fix Version | `fixVersions` | ✅ | ✅ | `[{"name": "Backlog"}]` — or `YY.MM` |

- `customfield_15450` (Epic Description) / `customfield_15451` (Story Description) are flagged required but have defaults — omit them.
- Do **not** send `customfield_15256` (flat Product Experience) — not on Epic/Story screens.
- Commonly set when known: PM Owner `customfield_15223` (`{"accountId": "…"}`), UX Required `customfield_14675` (`[{"value": "Yes"}]`; omit for NO), Theme `customfield_15215`.
- Story → Epic: top-level `parent: "PHEM-…"`.

---

## Example (Story)

Field set confirmed working 2026-10-04 (PHEM-2434013).

```json
createJiraIssue({
  "cloudId": "abbe3ee2-54f7-4096-a7a0-62a220d87814",
  "projectKey": "PHEM",
  "issueType": "Story",
  "summary": "SCH – BE – <title>",
  "parent": "PHEM-1556813",
  "additional_fields": {
    "customfield_15211": {"value": "Hiring Intelligence", "child": {"value": "Scheduling"}},
    "customfield_15212": {"value": "P2"},
    "customfield_15216": {"value": "Usability"},
    "customfield_15217": {"value": "NO - Do Not Advertise / Specific Customers"},
    "customfield_15218": {"value": "None"},
    "customfield_15427": {"value": "NA"},
    "fixVersions": [{"name": "Backlog"}]
  }
})
```

Then wait ~1.5 s → `editJiraIssue(cloudId: "abbe3ee2-54f7-4096-a7a0-62a220d87814", issueIdOrKey: "<new key>", fields: {"description": "…"}, contentFormat: "markdown")`.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `INVALID_INPUT` / value not allowed | Wrong option string | Check `jira-constants`, or discover `getJiraIssueTypeMetaWithFields` and run it with `executeRead`; numeric `{"id": "…"}` also works |
| `Please fill the Product Experience: Product field` | Missing child in cascade | `{"value": "X", "child": {"value": "Y"}}` |
| `<Field> is required` | Required field missing | Add it from the table above |
| `Field 'customfield_…' cannot be set` | Field not on this issue type's screen (e.g. `15256`) | Drop it |
| Description shows default template | Sent description on create | Two-step: create, wait, then `editJiraIssue` |
| `401 Unauthorized` | Atlassian connector auth expired | Reconnect the Atlassian connector (claude.ai connector settings / `/mcp`; Cursor MCP settings) |
