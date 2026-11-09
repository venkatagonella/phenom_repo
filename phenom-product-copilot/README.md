# Phenom Product Copilot

Shared Cursor / Claude Code setup for Phenom PMs: skills, policies, agents, and a local MCP server (Google, Snowflake, Vanilla KB).

This repo is **private**. Ask a maintainer for collaborator access, then clone **this** git repo and open **this folder** as your Cursor workspace (the folder that contains `CLAUDE.md`).

```bash
git clone https://github.com/officiallybasti/phenom-product-copilot.git ~/Phenom\ -\ Product\ Copilot
cd ~/Phenom\ -\ Product\ Copilot
```

## Open Product OS

Product OS has two pages. Open both from here:

| | Product OS Local | Product OS Hosted |
|---|---|---|
| Open with | `/01_product-os` in Claude Code or Cursor, or `./01_product-os/onboarding/open.sh` | The "Open Product OS Hosted" button in Product OS Local (productos.phenom.pro once live) |
| Shows | Setup checks for this laptop, your own usage, commands to copy | Setup journey, skill catalog, what's new, team usage, how it works |
| Seen by | Only you, on this laptop | Every PM, the same page |

Keep Product OS Local running while you set up: Product OS Hosted reads it to tick off your steps.

Stay current with `/update-product-os` in Claude Code or Cursor (or `bash 01_product-os/skills/update-product-os/update.sh`): it pulls, relinks new skills, installs changed dependencies, rebuilds the skill catalog and tells you what is new. Skills and policies come from this repo. `02_personal-os/me.md` is gitignored — never commit it.

Two folders:

- **`01_product-os/`**: the shared layer every PM pulls (skills, policies, agents, knowledge, engineering index, MCP server, onboarding).
- **`02_personal-os/`**: your private vault (inbox, morning brief, meetings, 1:1s, your own context). Its folders and rules come with the repo; **everything you write there is gitignored and never pushed**. Add your starter files once, then say `set me up` in a chat:

```bash
bash 01_product-os/onboarding/setup-personal.sh
```

Maintainer / Cloud Run notes: [01_product-os/OWNERSHIP.md](01_product-os/OWNERSHIP.md).

---

## 1. Open the onboarding dashboard

```bash
./01_product-os/onboarding/open.sh
```

Opens [http://127.0.0.1:8787](http://127.0.0.1:8787): local readiness checks, optional engineering-clone status, and the skill catalog from `skills/`. While it runs, the PM OS site (productos.phenom.pro, or the local build) shows the same checks live in "Your setup". Keep the terminal process running while you use the page. It binds to `127.0.0.1` only.

Need Node.js 20+ and npm. For engineering clones later: Bitbucket SSH (`ssh -T git@bitbucket.org`).

---

## 2. Connect Copilot tools

The copilot server covers Snowflake and the help center (Vanilla KB) in both editors, and Google in Cursor. From the repo root:

```bash
cd 01_product-os/mcp && npm install && npm run setup
```

Setup talks to the Cloud Run backend (`https://product-copilot-backend-iarivxijkq-uc.a.run.app`). You sign in in the browser (Phenom Google). Vanilla KB tokens come from that backend — you do not paste a Vanilla API key or Google OAuth client secrets locally. Snowflake signs in with browser SSO: enter your Phenom email, the first query opens an Okta tab, and the login is cached after that. Existing PAT users: rerun `cd 01_product-os/mcp && npm install && npm run setup snowflake`. A PAT (`npm run setup snowflake -- --pat`) is only for headless jobs and only works if a Snowflake admin attached a network policy to your user (otherwise error 390432). Tokens land in `~/.copilot/tokens.json`.

There is no root `.env` / `.env.example` for PMs.

**Design system packages.** Prototypes that use the Phenom design system (`@phenom/react-ds`, Font Awesome Pro) install from Phenom's Nexus registry. Connect npm once (on the VPN):

```bash
bash 01_product-os/onboarding/setup-npm.sh                 # asks for the Nexus credential (hidden)
bash 01_product-os/onboarding/setup-npm.sh --from <path>   # or reuse the .npmrc of a Phenom UI repo you cloned
bash 01_product-os/onboarding/setup-npm.sh --check         # configured? does the registry answer?
```

It writes the registry and your credential to `~/.npmrc` (your user config). The credential never goes into this repo; `01_product-os/onboarding/npmrc.example` shows the lines without it.

---

## 3. Shared tools (Jira, Figma, Slack, Glean, design system)

The repo ships the tool list for both editors. Nobody pastes tokens: each tool opens a browser sign-in the first time.

| Tool | Required | Claude Code | Cursor |
|---|---|---|---|
| Copilot: Snowflake, help center | yes | `.mcp.json` | `.cursor/mcp.json` |
| Jira + Confluence | yes | Atlassian plugin (`.claude/settings.json`) | `.cursor/mcp.json` |
| Figma | yes | Figma plugin | `.cursor/mcp.json` |
| Slack | yes | Slack plugin | `.cursor/mcp.json` |
| Glean | yes | `.mcp.json` | `.cursor/mcp.json` |
| Phenom design system, Angular (Storybook) | yes | `.mcp.json` | `.cursor/mcp.json` |
| Phenom design system, React | yes | `setup-design-system.sh` (needs a key) | `setup-design-system.sh` |
| Google Drive, Docs, Sheets, Slides, Calendar, Gmail | yes | claude.ai connectors | Copilot (`npm run setup google`) |
| Miro, Granola | optional | add yourself | add yourself |

**Claude Code:** run `claude` in this folder. Approve the project's MCP servers and install the three plugins when asked, then `/mcp` → each tool → Authenticate. Connect Google once in claude.ai → Settings → Connectors. Claude Code uses those official connectors for Google, so the repo's `.mcp.json` turns the copilot server's Google tools off (`COPILOT_PROVIDERS`). The Slides scripts still use the copilot Google sign-in.

**Cursor:** open this folder, then Settings → MCP: turn on each server and click Connect.

**Design system (React):** the key comes from the design system team. Run once; it adds the server to both editors in your user config:

```bash
bash 01_product-os/onboarding/setup-design-system.sh           # asks for the key (hidden)
bash 01_product-os/onboarding/setup-design-system.sh --check
```

**Check it:** say `/01_product-os check connections`. The agent asks each tool who you are and lists anything still to sign in.

**One source per tool.** If `/mcp` (or Cursor's MCP list) shows a tool twice, for example Slack from the plugin and from an old manual entry, remove the manual one. Duplicates load every tool twice and confuse the agent. Your own extra tools (Mobbin, Perplexity, …) go in your user config, never in the repo.

The Slack server only connects after a Phenom Slack admin has approved it for the workspace.

For another repo, `@`-include this checkout's `CLAUDE.md`.

---

## 4. Your profile

Edit `02_personal-os/me.md` (gitignored, like everything you write in `02_personal-os/`). Cover role, products / Jira projects, default Drive folder, and working preferences. The onboarding agent can walk you through it.

---

## 5. Skills as slash commands

Every folder in `01_product-os/skills/` with a `SKILL.md` becomes a `/command` in Claude Code and Cursor once it is linked into `~/.claude/skills/`. Run once, and again after a pull that adds a skill:

```bash
bash 01_product-os/onboarding/link-skills.sh
uv tool install graphifyy==0.9.92   # only for /graphify
```

| Command | What it does | Source |
|---------|--------------|--------|
| `/humanizer` | Removes AI-writing tells from a draft without changing what it says | [blader/humanizer](https://github.com/blader/humanizer) (MIT) |
| `/design-taste-frontend` | Art direction and browser check for landing pages and marketing sites (not app UI — use Phenom Designer) | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) |
| `/caveman` | Terse replies to save tokens, until "stop caveman" | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (Apache-2.0) |
| `/graphify` | Builds a queryable knowledge graph of a folder or repo | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache-2.0) |
| `/phenom-slide-creator`, `/phenom-knowledge-base-creator`, `/product-story-analyzer`, `/service-request-analysis`, `/sr-triage` | Phenom workflows (see `CLAUDE.md`) | this repo |

Third-party skills are copied in unchanged with their licence. To update one, copy the new version over its folder.

---

## 6. Engineering code (required)

Every PM clones all registered Phenom repositories, read-only, so the agent answers feasibility questions from the real code (about 6 GB). Details: [`01_product-os/engineering/SETUP.md`](01_product-os/engineering/SETUP.md).

```bash
ssh -T git@bitbucket.org
./01_product-os/engineering/scripts/sync-repos.sh
```

**A clone fails with an access error?** Raise a DevOps ticket for read access: a Jira POS ticket of type "Bitbukcet-Access-Request" ([how it works](https://phenompeople.atlassian.net/wiki/spaces/DEVOPS/pages/57496830045)). This prints the ticket fields, with the repositories you still miss:

```bash
./01_product-os/engineering/scripts/access-request.sh
```

After DevOps approves it, run `./01_product-os/engineering/scripts/sync-repos.sh` again. Product OS Local shows "Engineering code" as done once every repository is cloned. Never edit, commit, or push `01_product-os/engineering/repos/`.

---

## What's in here

```
01_product-os/        Shared by every PM (tracked)
  skills/          Tool how-tos and slash commands
  policies/        Always-on rules (Jira, platform routing, …)
  agents/          Sub-agents (onboarding, ticket analyst, …)
  knowledge/       Product context and data definitions
  engineering/     Code index + clone script (repos/ is local, gitignored)
  mcp/             Local MCP server (Google, Snowflake, Vanilla KB)
  onboarding/      Product OS Local, catalog builder, setup scripts
  examples/        Real example outputs per skill
02_personal-os/       Your vault and profile (me.md): rules and folders tracked, your content gitignored
CLAUDE.md          Claude Code entry (routes to both folders)
```

Change shared files through a pull request (see .github/CONTRIBUTING.md); others get them with `/update-product-os`.

---

## Usage log (what gets recorded)

Opening this repo in Claude Code or Cursor turns on small hooks (`.claude/settings.json`, `.cursor/hooks.json`). They write one line per event to `~/.copilot/usage/events.jsonl` **on your laptop**: date, tool (Claude Code or Cursor), your work email, and the **name** of the skill, agent or slash command that ran. Prompts, arguments, files and answers are never recorded. Nothing leaves your laptop today.

- See yours: `node 01_product-os/onboarding/usage/report.mjs`, or the Usage page of the PM OS site while `./01_product-os/onboarding/open.sh` runs.
- Share a summary (counts only): `node 01_product-os/onboarding/usage/report.mjs --export`.
- Turn it off: `touch ~/.copilot/usage/OPT_OUT` (or set `PMOS_USAGE=off`).

