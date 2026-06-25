---
name: spec-from-jira
description: >-
  Step 1 of PRD creation: read-only fetch and understand context from Jira
  entities (Epic, Story, Bug, Task, ticket, or any issue type). Use when the
  user provides comma-separated Jira keys to create a spec/PRD.
---

# Spec from Jira — Step 1: Understand Context

**Step 1** of the **create-prd** workflow. Read and understand context from Jira entities before problem breakdown or FRD drafting.

Turn one or more Jira issues into contextual understanding for a review-ready FRD.

## Structural authority

Map Jira content into segregated FRD parts per **`../product-copilot-beta/policies/jira-story-rules.md`** and **`../product-copilot-beta/policies/templates/story.md`**. Never mix customer issue with proposed solution in the same section.

| Jira type | FRD mapping |
|-----------|-------------|
| **Epic** | Part A — Customer Issue, Goals & Success Metrics |
| **Epic "What" / requirements** | Part B — Solution Overview, Functional Requirements list |
| **Story** | Part B User Stories table + Part C requirement block (full `story.md` structure) |

## Triggers

- User provides Jira keys: `PHEM-12345`, `PHEM-111, PHEM-222`
- "Create spec from Jira", "PRD from ticket", "draft from epic"
- Any issue type: Epic, Story, Task, Bug, Initiative

## Workflow

```
Task Progress:
- [ ] Parse issue keys from user input
- [ ] Resolve cloudId
- [ ] Fetch each issue (with comments)
- [ ] Fetch linked/parent issues if context is thin
- [ ] Produce Jira Context Summary (see create-prd Step 1)
- [ ] Hand off to spec-inputs (Step 2) — do not draft FRD yet
```

### 1. Parse keys

Extract comma- or space-separated keys (e.g. `PHEM-12345, PHEM-67890`). Normalize to uppercase. Deduplicate.

### 2. Resolve cloudId

Read the Atlassian MCP tool schema, then call `getAccessibleAtlassianResources` (no args). Use the returned `cloudId` for subsequent calls.

If the user pasted a Jira URL, try the site hostname as `cloudId` first; fall back to `getAccessibleAtlassianResources`.

### 3. Fetch issues

For **each** key, call `getJiraIssue`:

| Parameter | Value |
|-----------|-------|
| `cloudId` | From step 2 |
| `issueIdOrKey` | Issue key (e.g. `PHEM-12345`) |
| `fields` | `["summary", "description", "status", "issuetype", "priority", "labels", "components", "parent", "subtasks", "comment"]` — include `"comment"` |
| `responseContentFormat` | `"markdown"` |

Fetch in parallel when multiple keys are provided.

### 4. Enrich context (when needed)

- **Epic with thin description** → fetch child stories via `searchJiraIssuesUsingJql` (`parent = PHEM-XXXX`) or linked issues from `getJiraIssueRemoteIssueLinks`
- **Story under Epic** → also fetch parent Epic for scope and goals
- **Confluence link in description** → use `getConfluencePage` (see spec-inputs skill)
- **Ambiguous product area** → use Atlassian `search` tool for related tickets

### 5. Synthesize — segregated mapping

When Jira descriptions mix problem and solution, **split them** into the correct FRD part:

| Jira source | FRD section | Part |
|-------------|-------------|------|
| Epic "Why", customer pain, business value | Customer Issue — Background, Pain Points, Business Impact | **A** |
| Customer asks, CS/PM comments | Customer Requirements (as stated) | **A** |
| Epic Success Metrics | Goals & Success Metrics | **A** |
| Epic "What", feature overview | Solution Overview | **B** |
| Epic functional/non-functional requirements | Functional Requirements table (what only) | **B** |
| Story user story block | User Stories table + Part C User Story | **B + C** |
| Story acceptance criteria | Part C Acceptance Criteria (Given/When/Then, 3–5 scenarios) | **C** |
| Story Out of Scope | Part C Out of Scope | **C** |
| Design links, UX Required | Part C Design / Mockups | **C** |
| Technical notes | Part C Technical Notes | **C** |
| Open questions in comments | Part C Open Questions (per story) + Part D if initiative-wide | **C / D** |
| Epic cross-team dependencies | Cross-Team Dependencies | **D** |
| Labels, components, epic name | CRM Core capability mapping | **B** |
| Linked bugs/support tickets | Pain Points, Customer Context | **A** |

**Separate facts from inference.** Mark gaps as Open Questions. Do not invent customer quotes or metrics.

### 6. Hand off

Return **Jira Context Summary** to Step 2 (**spec-inputs** / **create-prd**). FRD drafting happens in Step 3 only.

When ready to draft, map content per table in §5 and **write-stories-from-problem** for Part C blocks.

## MCP reference

Always read tool schemas under the Atlassian MCP server before calling.

| Tool | When |
|------|------|
| `getAccessibleAtlassianResources` | First call — obtain `cloudId` |
| `getJiraIssue` | Per issue key; always request comments + markdown |
| `searchJiraIssuesUsingJql` | Epic children, related issues |
| `search` | Broad discovery across Jira + Confluence |
| `getConfluencePage` | Linked Confluence pages in issue body |

**Do not** create, edit, comment on, or transition Jira issues when gathering inputs for PRD creation. Jira is **read-only** in this workflow — see **create-prd** skill. Only create Jira items if the user explicitly asks outside of PRD authoring.

## Example

**Input:** "Draft an FRD from PHEM-45001, PHEM-45002"

**Actions:**
1. `getAccessibleAtlassianResources` → `cloudId`
2. Parallel `getJiraIssue` for both keys with `fields` including `"comment"`, `responseContentFormat: "markdown"`
3. If PHEM-45001 is Epic, JQL fetch children → one Part C block per child Story
4. Draft `specs/bulk-tagging-candidates/frd.md` via `prd-authoring`
5. Publish Google Doc via `frd-google-drive`; return URL

## Related skills

- **create-prd** — primary orchestrator
- **read-only-inputs** — no writes on Jira
- **spec-inputs** — Step 2 problem breakdown + Google Drive
- **write-stories-from-problem** — Step 3 story derivation
- **prd-authoring** — Step 3 FRD draft
- **frd-google-drive** — Step 3 publish
