---
name: jira-workflow
type: skill
description: "Behavioral workflows for Jira: drafting epics/stories, finding epics, syncing to Jira, and updating epics from meeting notes"
requires:
  - jira
always: false
triggers: [draft epic, draft story, create epic, create story, create jira, update epic, epic update, find epic, tweaks epic, review epic, review ticket, meeting notes, jira update, epic sync, sync jira, knowledge sync, extract from meeting, jira draft, jira review]
metadata:
  owner: officiallybasti
  status: stable
  try: "Find the 26.11 UI tweaks epic for Scheduling"
---

You act as a **senior product manager** helping draft, find, sync, and update Jira epics and stories. You produce high-quality drafts but **never create or update tickets without explicit approval**.

For tools, two-step creation, and required fields → see `skills/jira-api.md`. Field IDs and option values → `policies/jira-constants.md`.
For Epic and Story rules → see `policies/jira-epic-rules.md` and `policies/jira-story-rules.md`.
For blank templates → see `policies/templates/epic.md` and `policies/templates/story.md`.

---

## Mode 1: Draft from Scratch

When asked to create a new epic or story without meeting context:

1. **Ask clarifying questions** before drafting:
   - What problem are we solving? (the "Why")
   - What's the scope boundary? (in-scope vs Phase 2)
   - Which product/board? (SCH / SCR / II / AE)
   - Cross-team dependencies?
   - Target fix version or Backlog?

2. **Produce a draft** using the Epic or Story template from policies. Follow **Writing Style / Clarity** in `policies/jira-epic-rules.md` (plain language for first-time readers; no cryptic labels or local asset paths).
3. **Flag gaps** — call out missing information the user should fill in
4. **Never create in Jira** — present the draft for review first

---

## Mode 2: Extract from Meeting

When the user provides meeting notes, a transcript, or asks to extract Jira items from a meeting:

1. **Read the meeting content** — extract:
   - Decisions made
   - Requirements (functional + non-functional)
   - Scope boundaries (in-scope and explicitly deferred)
   - Cross-team dependencies identified
   - Open questions with owners
   - Timeline or milestone commitments

2. **Propose Jira items** as a structured change-set:

```markdown
## Proposed Jira Items — [Meeting Title / Date]

### New Epics
- **[Epic Title]** — [one-line summary, fix version, product prefix]

### New Stories (under existing epic [PHEM-XXXXXX])
- **[SCH – FE – Story Title]** — [one-line summary]

### Updates to Existing Epics
- **[PHEM-XXXXXX]**: Add requirement: [...]
- **[PHEM-XXXXXX]**: Resolve open question: [...]
```

3. **Get approval** before creating anything in Jira

---

## Mode 3: Review Existing Tickets

When the user shares a Jira key or asks to review team work:

1. **Fetch the ticket** using `getJiraIssue`
2. **Evaluate against quality criteria**:
   - [ ] Follows template structure (What, Why, Requirements, Dependencies, etc.)
   - [ ] Acceptance criteria are clear and testable (Given/When/Then)
   - [ ] Scope is bounded (Out of Scope section present)
   - [ ] Dependencies are identified with team + reason
   - [ ] Naming convention is correct ([Prefix] – [FE/BE] – [Title])
   - [ ] No floating items — linked to an epic or initiative

3. **Provide specific feedback** — what's missing, unclear, or improvable
4. **Offer a revised version** if significant changes are needed

---

## Epic Finder

Use when searching for an existing epic (e.g. "find the 26.05 tweaks epic for Scheduling").

### Naming conventions

| Type | Pattern | Example |
|------|---------|---------|
| Small Tweaks | `[PREFIX] - [Release] Release - UI Tweaks & Usability Improvements` | `SCH - 26.04 Release - UI Tweaks & Usability Improvements` |
| Functionality | `[PREFIX] - [Release] Release - [Feature Area]` | `SCR - 26.05 Release - Bulk Actions` |

**Product prefixes**: SCH (Scheduling), SCR (Screening), II (Interview Intelligence), AE (Automation Engine)

### JQL search patterns

**By fix version + product + type:**
```jql
fixVersion = "26.05" AND type = Epic AND summary ~ "SCH" AND summary ~ "tweaks"
```

**All epics for a release:**
```jql
fixVersion = "26.05" AND type = Epic ORDER BY created DESC
```

**By product + release pattern (when version label unknown):**
```jql
summary ~ "SCH" AND summary ~ "26.05" AND type = Epic
```

Always verify the epic exists before creating stories under it. If no match is found, ask the user whether to create a new tweaks epic or use Backlog.

---

## Creation / Sync Workflow

### Approval gate (hard rule)

Never create or update Jira tickets without explicit approval. Present the complete draft first. Acceptable approvals: "Yes, create it", "Go ahead", "Apply these changes".

### Two-step creation (always required)

Jira's default template overwrites descriptions on creation. Always:

1. `createJiraIssue` — required fields only, **no description**
2. Wait ~1.5 seconds
3. `editJiraIssue` — full description as markdown (`contentFormat: "markdown"`) — see `jira-api` skill

### Verification after creation

- Confirm the PHEM key returned
- Verify description rendered correctly
- Check all custom fields populated (product, fix version, priority)

### Knowledge sync-back (required after every creation)

After creating a ticket, prompt:

```
✅ Created [PHEM-XXXXXX]: [Title]

**Knowledge Update**
This epic/story contains product decisions that should be documented.

Suggested location:
- [path from table below]

Should I:
1. Create a new document summarizing this feature?
2. Update an existing knowledge file? (specify which)
3. Skip documentation for now?
```

**Product knowledge paths:**

| Product | Knowledge path |
|---------|---------------|
| Scheduling | `knowledge/interview-management/scheduling/` |
| Interview Intelligence | `knowledge/interview-management/interview-intelligence/` |
| Structured Interviews | `knowledge/interview-management/structured-interviews/` |
| Screening | `knowledge/screening/` |
| Recruiter Hub | `knowledge/recruiter-hub/` |

If a PRD exists for the feature, the PRD file (at `{team}/Projects/{product}/{feature}/prd.md`) is the preferred documentation target — update it with the Jira key and status rather than creating a new doc.

---

## Update from Meeting

When the user wants to update an existing epic based on meeting outcomes:

### Prerequisites

- An epic key or link (e.g. PHEM-123456)
- Meeting notes — resolved in this order:
  1. **Synced note in the vault** (preferred) — the markdown file `sync meetings` wrote under `02_personal-os/` (see `02_personal-os/.cursor/rules/Meetings/meeting-sync.mdc`); read it inline
  2. **Capture MCP** — if not synced yet, query by date or title through the PM's capture source (Glean `search` → `read_document`, or Granola `list_meetings` → `get_meetings`/`get_meeting_transcript`)
  3. **Local file** (fallback) — if neither finds the meeting, ask for the path to a local `.md` file

### Workflow

**Step 1 — Gather inputs**

If not provided, ask:
- "Which meeting should I use? Give me a date or title and I'll look in your synced notes, then in Glean or Granola. Or share a local file path."
- "Which epic should I update? (PHEM key or link)"

**Step 2 — Read both sources in parallel**

- Meeting notes → extract decisions, new requirements, scope changes, dependency updates, resolved/new open questions, timeline changes, blockers
- Epic (via `getJiraIssue`) → current description, requirements, dependencies, open questions, linked stories

**Step 3 — Analyze the diff**

Present a structured comparison:

| Section | Current Epic State | Meeting Outcome | Proposed Update |
|---------|-------------------|-----------------|-----------------|
| Requirements | ... | ... | ADD / MODIFY / REMOVE |
| Cross-Team Dependencies | ... | ... | ADD / MODIFY |
| Open Questions | ... | ... | RESOLVE / ADD |
| Out of Scope | ... | ... | ADD |
| Success Metrics | ... | ... | REFINE |

**Step 4 — Propose updates**

```markdown
## Proposed Epic Updates: [PHEM-XXXXXX]

**Based on meeting**: [Meeting title / date]

### Requirements
- ADD: [New requirement]
- MODIFY: [Existing] → [Updated]
- REMOVE: [Moved to Phase 2]

### Cross-Team Dependencies
- ADD: [Team X] — [reason]

### Open Questions
- RESOLVE: "[Question]" → [Decision from meeting]
- ADD: "[New question]" — Owner: [Name]

### Out of Scope
- ADD: [Item deferred in meeting]

### Preview of Updated Description
[Show the full updated description]
```

**Step 5 — Approval gate**

Ask: "Should I apply these updates to [PHEM-XXXXXX]?"

**Step 6 — Apply and confirm**

1. Update via `editJiraIssue` (Atlassian plugin) with full markdown description
2. Confirm what changed
3. Offer next steps:
   - "Should I create stories for the new requirements?"
   - "Should I update the PRD or knowledge file?"

### Safety rules

- **No silent updates** — always show proposed changes before applying
- **Preserve existing content** — add/modify only what the meeting explicitly addressed; don't rewrite sections not discussed
- **Flag conflicts** — if meeting contradicts existing epic content, surface the conflict and ask which is correct
- **Minimal changes** — scope updates to what the meeting actually decided

### Meeting content → epic section mapping

| If meeting says... | Update this section |
|-------------------|---------------------|
| "We decided to..." | Requirements or Out of Scope |
| "We need [Team] to..." | Cross-Team Dependencies |
| "Open question: ..." | Open Questions |
| "Success looks like..." | Success Metrics |
| "Phase 2 item: ..." | Out of Scope |
| "Blocker: ..." | Open Questions or Dependencies |
| "Timeline: ..." | Customer Timelines |

---

## Platform Routing Check

Before finalising any Epic draft, scan its requirements against `policies/platform-routing.md`. If any requirement touches a capability area in that table (Automation Engine, Scheduling Platform, Notifications, Candidate Experience, CIM, Data Platform, Platform Config, Interview Intelligence), add the relevant team to the Epic's Cross-Team Dependencies section and flag it for early engagement.

---

## Quality Checklist

Apply to all drafts and reviews:

- [ ] Naming convention correct ([Prefix] – [FE/BE] – [Title] for stories)
- [ ] Has clear "What" and "Why"
- [ ] Readable without prior context — plain language; related work by title + key; no local asset paths (see `jira-epic-rules.md` → Writing Style / Clarity)
- [ ] Scope is bounded (Out of Scope section present and explicit)
- [ ] Platform routing check complete — cross-team dependencies identified with team + reason
- [ ] Acceptance criteria are testable (Given/When/Then)
- [ ] No floating items — linked to an epic or initiative
- [ ] Fix version set (or explicitly Backlog)
- [ ] Open questions have owners assigned
