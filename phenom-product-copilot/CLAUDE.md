# Copilot Configuration

This repo has two folders:

- **`01_product-os/`** — the shared layer every PM pulls: `skills/`, `policies/`, `agents/`, `knowledge/`, `engineering/`, `mcp/`, `onboarding/`, `examples/`. Paths written inside these files (`skills/jira-api.md`, `onboarding/open.sh` …) are relative to `01_product-os/`.
- **`02_personal-os/`** — your private vault: inbox, context, meetings, 1:1s, tasks, `outputs/`. Paths inside its rules (`00_Inbox/`, `99_System/` …) are relative to `02_personal-os/`. Only its system files (rules, scripts, templates, empty folders) are tracked; **everything you write there stays on this laptop. Never stage, commit or copy it into `01_product-os/`.**

Run scripts from the repo root with the folder prefix, e.g. `./01_product-os/onboarding/open.sh`.

<!-- Personal profile — who I am and how I work -->
@02_personal-os/me.md

<!-- Policies — always active -->
@01_product-os/policies/planning.md
@01_product-os/policies/repo-structure.md
@01_product-os/policies/mcp-connectivity.md
@01_product-os/policies/jira-constants.md
@01_product-os/policies/jira-epic-rules.md
@01_product-os/policies/jira-story-rules.md
@01_product-os/policies/platform-routing.md
@01_product-os/policies/engineering-context.md
@01_product-os/skills/token-guard.md

<!-- Engineering code context (index-first; clones are local/gitignored) -->
@01_product-os/engineering/CLAUDE.md

<!-- Skills — loaded when relevant -->
@01_product-os/skills/jira-api.md
@01_product-os/skills/jira-workflow.md
@01_product-os/skills/snowflake-data-context.md
@01_product-os/skills/service-request-analysis/SKILL.md
@01_product-os/skills/google.md
@01_product-os/skills/vanilla-kb.md
@01_product-os/skills/prd.md
@01_product-os/skills/release-calendar.md
@01_product-os/skills/fire-tasks.md
@01_product-os/skills/product-feedback.md
@01_product-os/skills/product-story-analyzer/SKILL.md
@01_product-os/skills/phenom-slide-creator/SKILL.md
@01_product-os/skills/engineering-feasibility.md
@01_product-os/skills/design-system.md

## Tools

The shared tool list ships with the repo (`.mcp.json` for Claude Code, `.cursor/mcp.json` for Cursor, plugins in `.claude/settings.json`). One source per tool; full table in README §3.

- **Snowflake, Vanilla Knowledge Base** — local copilot MCP server (both editors)
- **Google** (Drive, Docs, Sheets, Slides, Calendar, Gmail) — Claude Code: official claude.ai connectors; Cursor: copilot server. Tool names per editor: `skills/google.md`
- **Jira + Confluence, Figma, Slack** — official servers (Claude Code plugins; Cursor remote servers)
- **Glean** — `glean_default`
- **Phenom design system** — `phenom-ds-storybook` (Angular, in the repo) and `phenom-react-ds-mcp` (React, added by `onboarding/setup-design-system.sh`)

A PM asks whether their tools work → `/01_product-os check connections`.

## Agents

The following agents are available:

- **Customer Adoption Report** [manual]: Analyzes customer platform adoption and produces a Google Slides deck
- **Support Ticket Analyst** [auto]: Classifies a single ticket or processes a full batch for a team
- **Issue Clustering** [manual]: Groups classified tickets into existing or new high-level issues
- **Community Answer Analyzer** [manual]: Matches open Community discussions to existing KB articles and identifies content gaps (read-only)
- **Onboarding** [manual]: Walks new users through repo setup, MCP servers, and their personal profile
- **Phenom Designer** [manual]: Builds prototypes following Phenom DS V2 — **local** (HTML/React) or **Figma (MCP)**. Asks which mode first. References: `skills/phenom-designer.md`, `skills/phenom-ds-figma.mdc`, `knowledge/design-system/phenom-ds-code.md`
- **Phenom Slide Creator** [manual, `/phenom-slide-creator`]: Builds any Phenom deck from notes, docs or a conversation. Picks a **style** from the style library (`leadership-editorial` = the 2026 leadership decks, Fraunces + DM Sans, warm paper; `corporate-template` = Poppins, Mint/Peach/Honey/Lilac) and a **route**: Claude Slides artifact (default, exports to Google Slides), HTML, or Google template fill. Can learn a new style from any deck you share. References: `skills/phenom-slide-creator/SKILL.md`, `references/styles/`, `references/decks.md`, `assets/artifact-slides/leadership-editorial/build_deck.py`
- **Writing and design utilities** [manual, `/humanizer`, `/design-taste-frontend`, `/caveman`, `/graphify`]: third-party skills in `skills/`, not `@`-imported here. They become slash commands via `onboarding/link-skills.sh` (README §5).
- **Product OS** [manual, `/01_product-os`]: opens Product OS Local (`./01_product-os/onboarding/open.sh`, http://127.0.0.1:8787: setup checks, own usage) and links Product OS Hosted (catalog, what's new, team usage). When a PM asks how to start, what is installed, or where the catalog is, run it. Reference: `skills/01_product-os/SKILL.md`
- **Update Product OS** [manual, `/update-product-os`]: pulls the shared repo, relinks skills, rebuilds the catalog (`onboarding/build-catalog.mjs` → `onboarding/data/`), runs health checks and reports what is new. Use it instead of a bare `git pull`. Reference: `skills/update-product-os/SKILL.md`
- **Skill feedback** [manual, `/skill-feedback`]: sends feedback on any skill, agent or policy to its owner as a GitHub issue, or makes the change on a branch and opens a pull request. Every item has an owner and a status (sandbox → beta → stable → retired) in its front matter; rules in `.github/CONTRIBUTING.md`. Reference: `skills/skill-feedback/SKILL.md`
- **Onboarding** also covers the required **engineering clones** (`engineering/SETUP.md`) after MCP and `02_personal-os/me.md`. A clone that fails for access → help the PM raise a DevOps POS ticket with `./engineering/scripts/access-request.sh`.

## Personal OS (`02_personal-os/`)

Every PM's private vault. On first use, `bash 01_product-os/onboarding/setup-personal.sh` fills in the starter files from `02_personal-os/99_System/templates/vault/` (also run by `/update-product-os`; it never overwrites). Shared facts move up only through `promote context`, as a pull request. Read `02_personal-os/AGENTS.md` before personal work. If `02_personal-os/99_System/context/00-me.md` is missing, offer to run the setup script.

| Say | Rule |
|---|---|
| `set me up` | `02_personal-os/.cursor/rules/System/set-me-up.mdc` |
| `morning brief` | `02_personal-os/.cursor/rules/Daily/morning-brief.mdc` |
| `sync meetings`, `sync my Glean`, `sync my Granola` | `02_personal-os/.cursor/rules/Meetings/meeting-sync.mdc` (asks Glean or Granola first; Granola also saves screenshots) |
| `triage my inbox meetings` | `02_personal-os/.cursor/rules/Meetings/inbox-meetings.mdc` |
| `plan my week`, `weekly review` | `02_personal-os/.cursor/rules/Weekly/weekly-review.mdc` |
| `1:1 prep`, `1:1 review` | `02_personal-os/.cursor/rules/Meetings/1o1-prep.mdc`, `1o1-review.mdc` |
| `promote context` | `02_personal-os/.cursor/rules/System/context-promotion.mdc` |

The vault's rules and starter files are shared and reach every PM through `/update-product-os`. To change them, edit them in `02_personal-os/` and open a pull request; never put names, meetings or goals in a tracked file.
