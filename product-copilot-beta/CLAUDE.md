# Copilot Configuration

<!-- Personal profile — who I am and how I work -->
@me.md

<!-- Policies — always active -->
@policies/planning.md
@policies/repo-structure.md
@policies/mcp-connectivity.md
@policies/jira-constants.md
@policies/jira-epic-rules.md
@policies/jira-story-rules.md
@policies/platform-routing.md
@policies/engineering-context.md
@skills/token-guard.md

<!-- Engineering code context (index-first; clones are local/gitignored) -->
@engineering/CLAUDE.md

<!-- Skills — loaded when relevant -->
@skills/jira-api.md
@skills/jira-workflow.md
@skills/snowflake-data-context.md
@skills/service-request-analysis/SKILL.md
@skills/google.md
@skills/vanilla-kb.md
@skills/prd.md
@skills/release-calendar.md
@skills/fire-tasks.md
@skills/product-feedback.md
@skills/product-story-analyzer/SKILL.md
@skills/phenom-slide-creator/SKILL.md
@skills/engineering-feasibility.md
@skills/granola-sync.md
@skills/inbox-meetings.md
@skills/design-system.md

## Tools

The following tools are available via MCP servers configured in `.cursor/mcp.json`:

- **Google** (Drive, Docs, Sheets, Slides, Calendar) — local copilot MCP server
- **Snowflake** — local copilot MCP server
- **Vanilla Knowledge Base** — local copilot MCP server
- **Jira + Confluence** — official Atlassian MCP server
- **Figma** — official Figma MCP server

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
- **Update Product OS** [manual, `/update-product-os`]: pulls the shared repo, relinks skills, rebuilds the catalog (`onboarding/build-catalog.mjs` → `onboarding/data/`), runs health checks and reports what is new. Use it instead of a bare `git pull`. Reference: `skills/update-product-os/SKILL.md`
- **Onboarding** also covers optional **engineering clones** (`engineering/SETUP.md`) after MCP and `me.md`.
