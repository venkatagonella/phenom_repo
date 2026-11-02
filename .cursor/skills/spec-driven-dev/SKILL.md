---
name: spec-driven-dev
description: >-
  SpecDrivenDev guidelines for Phenom CRM Core FRD/PRD creation: read-only
  Jira and Drive inputs, problem-first breakdown, segregated Parts A–D, user
  stories with Given/When/Then AC, and a new Google Doc output. Use when
  creating a PRD, FRD, functional spec, or product requirements doc for CRM
  Core; when the user mentions SpecDrivenDev, create-prd, or problem breakdown.
---

# SpecDrivenDev — FRD/PRD Guidelines (orchestrator)

Canonical content lives under `SpecDrivenDev/`. Prefer the granular project skills for each step; this skill is the reusable guideline layer.

**Primary deliverable:** a **new** Google Doc  
**Optional local draft:** `SpecDrivenDev/specs/{initiative-slug}/frd.md`

## Hard rules

1. **Read-only inputs** — never create/edit input Jira issues, Confluence pages, or source Drive docs  
2. **Problem before solution** — complete Part A before Part B/C  
3. **Segregate** — never mix customer issue and proposed solution in the same section  
4. **Evidence only** — do not invent quotes, metrics, or requirements  
5. **Specs only** — do not implement product code in this workflow  
6. **No downstream publish** — Confluence/Jira create only when the user explicitly asks  

## Three-step workflow (do not skip)

| Step | Skill to load | Outcome |
|------|---------------|---------|
| 1 | **spec-from-jira** (+ **read-only-inputs**) | Jira context summary |
| 2 | **spec-inputs** + **write-stories-from-problem** | Part A problem breakdown |
| 3 | **prd-authoring** + **crm-core-product** + **frd-google-drive** | FRD Parts A–D → Google Doc |

Orchestrator entry: **create-prd**. Story format: **story-template**.  
Structure detail: [frd-structure.md](frd-structure.md) and `SpecDrivenDev/templates/frd-template.md`.

## Policy paths (structural authority)

- `product-copilot-beta/.cursor/policies/jira-story-rules.md`
- `product-copilot-beta/.cursor/policies/jira-epic-rules.md`
- `product-copilot-beta/.cursor/policies/templates/story.md`
- `product-copilot-beta/.cursor/policies/templates/epic.md`

## CRM Core story prefix

Use `Core` for CRM Core stories.

## Related

- Domain impact from a Jira key → **jira-domain-requirements**  
- Code feasibility → **phenom-engineering-context** / **phenom-knowledge**
