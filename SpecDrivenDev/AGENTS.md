# SpecDrivenDev — Agent Guide

This workspace is the **agent home** for creating **new** Functional Requirements Documents (FRDs / PRDs) for **Phenom CRM Core**. Users may say "PRD" or "functional spec" — treat as FRD.

**Primary deliverable:** a **new Google Doc** in Google Drive.  
**Optional local draft:** `specs/{initiative-slug}/frd.md`

---

## Agent role

You help product stakeholders:

1. **Understand** customer context from Jira entities (read-only)
2. **Break down** customer problems and what they are asking for
3. **Author** a segregated FRD with user stories and acceptance criteria
4. **Publish** a new Google Doc — without modifying any input Jira items or source documents

---

## Prerequisites (MCP)

| Integration | Required for | Setup |
|-------------|--------------|-------|
| **Atlassian MCP** | Jira fetch, Confluence read | Enabled in Cursor; `getAccessibleAtlassianResources` |
| **Google MCP** | Drive read (inputs) + Doc create (output) | Copilot MCP in `.cursor/mcp.json`; connect once via `../product-copilot-beta/mcp` (see below) |
| **Granola MCP** | Meeting context (optional) | When user references past calls |

### Google MCP setup (one-time)

Open **this folder** (`SpecDrivenDev`) as the Cursor workspace root, then connect Google:

```bash
cd ../product-copilot-beta/mcp
node bin/copilot-mcp.js google
```

Verify: `node bin/copilot-mcp.js status` → `✓ google`. Restart Cursor to load `.cursor/mcp.json`.

Tool reference: `../product-copilot-beta/skills/google.md`

If Google MCP is unavailable, complete local `frd.md` and document fallback (see **frd-google-drive** skill).

---

## Three-step workflow

Always start with **create-prd** skill. Do not skip steps.

```
Step 1  spec-from-jira     → Understand Jira entity context (read-only)
Step 2  spec-inputs        → Problem breakdown + Google Drive / other inputs (read-only)
Step 3  prd-authoring      → Draft FRD per templates/frd-template.md
        write-stories-from-problem → Derive Part B/C stories from Part A
        frd-google-drive    → Publish new Google Doc
```

**Read-only policy:** See **read-only-inputs** skill — never modify input Jira or source documents.

---

## Skills index

All skills live in `.cursor/skills/`:

| Skill | When to use |
|-------|-------------|
| [**create-prd**](.cursor/skills/create-prd/SKILL.md) | **Start here** — orchestrates the full three-step workflow |
| [**read-only-inputs**](.cursor/skills/read-only-inputs/SKILL.md) | Before any ingest — enforce no writes on inputs |
| [**spec-from-jira**](.cursor/skills/spec-from-jira/SKILL.md) | Step 1 — comma-separated Jira keys, any issue type |
| [**spec-inputs**](.cursor/skills/spec-inputs/SKILL.md) | Step 2 — Google Drive, Confluence, Granola, local files |
| [**write-stories-from-problem**](.cursor/skills/write-stories-from-problem/SKILL.md) | Step 3 — user stories + Part C blocks from Problem Breakdown |
| [**prd-authoring**](.cursor/skills/prd-authoring/SKILL.md) | Step 3 — FRD structure, segregation, review checklist |
| [**crm-core-product**](.cursor/skills/crm-core-product/SKILL.md) | Map problems to CRM Core scope; story prefix `Core` |
| [**frd-google-drive**](.cursor/skills/frd-google-drive/SKILL.md) | Step 3 — create **new** Google Doc; return URL |

---

## FRD structure (segregated)

Template: **`templates/frd-template.md`**  
Authority: **`../product-copilot-beta/policies/jira-story-rules.md`**

| Part | Content | Rule |
|------|---------|------|
| **A** | Source inputs, executive summary, customer issue, **problem breakdown**, goals | No solutions |
| **B** | Solution overview, user stories, functional requirements | No pain restatement |
| **C** | Story blocks: user story, Given/When/Then AC (3–5), out of scope | Trace to Part A |
| **D** | Dependencies, release plan, assumptions, appendix | Initiative wrap-up |

**Never mix** customer issue and proposed solution in the same section.

### Part A — Problem Breakdown (Step 2)

- **Related Problems** — connected sub-problems with sources
- **What the Customer Is Asking For** — stated asks vs inferred needs

---

## Folder layout

```
SpecDrivenDev/
├── AGENTS.md                          ← This file
├── .cursor/
│   ├── mcp.json                       ← Copilot MCP (Google Drive/Docs/Sheets)
│   ├── rules/spec-driven-dev.mdc      ← Always-on workspace rule
│   └── skills/                        ← Workflow skills (8 skills)
├── templates/
│   ├── frd-template.md                ← Canonical FRD template
│   ├── prd-template.md                ← Deprecated → frd-template
│   └── spec-template.md               ← Deprecated → frd-template
└── specs/
    └── {initiative-slug}/
        └── frd.md                     ← Local draft mirror
```

**Slug naming:** kebab-case; prefer customer or problem name (`acme-bulk-tagging`, `phem-45001-pipeline-visibility`).

---

## Input contract

User may provide (comma-separated where applicable):

| Input | Example |
|-------|---------|
| Jira keys | `PHEM-12345, PHEM-12346, PHEM-99001` |
| Google Doc/Sheet URL | `https://docs.google.com/document/d/...` |
| Google Drive search | "read my Google Drive docs on Acme tagging" |
| Confluence page | URL or page ID |
| Meeting context | "from the QBR with Acme last week" |
| Pasted ticket content | Support ticket body in prompt |

---

## Output contract

| Deliverable | Location |
|-------------|----------|
| **Primary** | New Google Doc: `FRD - [Initiative] - [Customer] - YYYY-MM-DD` |
| **Secondary** | `specs/{slug}/frd.md` with Google Doc link in metadata |
| **Status** | `Draft` until user reviews |

Confirm to user: inputs were read-only; only the new FRD was created.

---

## Example prompts

**Full workflow:**
> Understand PHEM-45001, PHEM-45002. Break down the customer problems, read my Google Drive docs on Acme bulk tagging, write stories from the customer problem, and create a new PRD in Google Drive.

**Jira only:**
> Create a PRD from PHEM-12345, PHEM-12346 — read only, don't update Jira.

**With Drive:**
> PHEM-12345 plus this Google Doc [URL]. New FRD in Drive please.

---

## External references

| Resource | Path |
|----------|------|
| FRD template | `templates/frd-template.md` |
| Story rules | `../product-copilot-beta/policies/jira-story-rules.md` |
| Story template | `../product-copilot-beta/policies/templates/story.md` |
| Epic template | `../product-copilot-beta/policies/templates/epic.md` |
| Jira constants (CRM Core) | `../product-copilot-beta/policies/jira-constants.md` |
| Google tools | `../product-copilot-beta/skills/google.md` |
| CRM customer KB | kb_id `3` in `../product-copilot-beta/skills/vanilla-kb.md` |
| Downstream PRD pipeline | `../product-copilot-beta/skills/prd.md` |

---

## What the agent must not do

- Modify or create **input** Jira issues or source documents
- Skip Step 2 problem breakdown before writing solutions
- Mix customer problem and solution in one section
- Invent customer quotes, metrics, or requirements unsupported by inputs
- Implement code in this workspace
- Publish to Confluence or create Jira tickets unless user **explicitly** asks (separate from PRD creation)

---

## Downstream (only when user explicitly requests)

```
LOCAL FRD → GOOGLE DRIVE → CONFLUENCE → JIRA EPIC → STORIES → DEVELOPMENT
```

Steps after Google Drive require explicit user instruction.
