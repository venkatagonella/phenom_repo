# Phenom Master Copilot

Unified Cursor workspace for Phenom product, design, competitive, engineering, and spec workflows.

Moved from `~/phenom_repo` (Cursor-linked packs). Engineering code clones for CRM apps remain under `~/phenom_repo/MyLocalCRM/repos/`.

## Quick start

1. Open this folder as the Cursor workspace root.
2. Unsure which skill? Load **phenom-master-router**.
3. Project skills live in `.cursor/skills/`; rules in `.cursor/rules/`.

## Area folders

| Folder | Purpose |
|--------|---------|
| `DesignSystem/` | Phenom Design System references, tokens, templates |
| `Compete/` | Competitive intelligence + job lifecycle packs |
| `JIRA/` | Domain-requirements skill + saved outputs |
| `SpecDrivenDev/` | CRM Core FRD/PRD workflow + specs |
| `SDDFlow/` | Northstar / SDD kit (reference; ns-* also personal) |
| `Phenom - Engineering/` | Read-only eng index (+ clones under `repos/` if present) |
| `phenom-knowledge/` | Code-grounded area packs (routing.yaml / skill.md / graph.json) |
| `product-copilot-beta/` | Phenom Product Copilot (synced from [officiallybasti/phenom-product-copilot](https://github.com/officiallybasti/phenom-product-copilot); see `.upstream-sync.md`) |
| `PhenomDeckTemplate/` | Phenom slide creator assets |
| `my_agents/` | Misc agent notes |

## Project skills (`.cursor/skills/`)

| Skill | Area |
|-------|------|
| `phenom-master-router` | Cross-area routing |
| `phenom-design-system` | PDS UI |
| `competitor-job-lifecycle` | Compete |
| `hypercell` | Hypercell matrix (Industry × Function × Role × Workflow × Geography) |
| `jira-domain-requirements` | Jira → domains |
| `jira-workflow` / `jira-api` | Jira PM workflows |
| `spec-driven-dev` / `create-prd` + step skills | FRD/PRD |
| `phenom-engineering-context` | Feasibility from eng index |
| `phenom-knowledge` / `phenom-messaging` | Code-grounded CRM maps |
| `phenom-slide-creator` | Decks |
| `google` / `vanilla-kb` / `product-context` / `snowflake-data-context` / `release-calendar` | Product copilot MCPs |
| `pr-review` | PR review |

Northstar `ns-*` flows stay in personal `~/.cursor/skills/` (not duplicated).

## Left in `phenom_repo`

`MyLocalCRM`, `SampleCode`, `NorthStarCheck`, `Disney`, `Snowflake Integration`, empty UI experience folders.
