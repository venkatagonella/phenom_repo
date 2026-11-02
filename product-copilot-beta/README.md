# Phenom Product Copilot

Shared Cursor / Claude Code setup for Phenom PMs: skills, policies, agents, and a local MCP server (Google, Snowflake, Vanilla KB).

This repo is **private**. Ask a maintainer for collaborator access, then clone **this** git repo and open **this folder** as your Cursor workspace (the folder that contains `CLAUDE.md`).

```bash
git clone https://github.com/officiallybasti/phenom-product-copilot.git ~/Phenom\ -\ Product\ Copilot
cd ~/Phenom\ -\ Product\ Copilot
```

Stay current with `/update-product-os` in Claude Code or Cursor (or `bash skills/update-product-os/update.sh`): it pulls, relinks new skills, installs changed dependencies, rebuilds the skill catalog and tells you what is new. Skills and policies come from this repo. `me.md` is gitignored — never commit it.

Optional personal OS (inbox, briefs, your own context): GitHub template [phenom-personal-copilot](https://github.com/officiallybasti/phenom-personal-copilot) — Use this template, then add that clone as a second Cursor folder next to this one.

Maintainer / Cloud Run notes: [OWNERSHIP.md](OWNERSHIP.md).

---

## 1. Open the onboarding dashboard

```bash
./onboarding/open.sh
```

Opens [http://127.0.0.1:8787](http://127.0.0.1:8787): local readiness checks, optional engineering-clone status, and the skill catalog from `skills/`. While it runs, the PM OS site (productos.phenom.pro, or the local build) shows the same checks live in "Your setup". Keep the terminal process running while you use the page. It binds to `127.0.0.1` only.

Need Node.js 20+ and npm. For engineering clones later: Bitbucket SSH (`ssh -T git@bitbucket.org`).

---

## 2. Connect Copilot tools

From the repo root:

```bash
cd mcp && npm install && npm run setup
```

Setup talks to the Cloud Run backend (`https://product-copilot-backend-iarivxijkq-uc.a.run.app`). You sign in in the browser (Phenom Google). Vanilla KB tokens come from that backend — you do not paste a Vanilla API key or Google OAuth client secrets locally. Snowflake signs in with browser SSO: enter your Phenom email, the first query opens an Okta tab, and the login is cached after that. Existing PAT users: rerun `cd mcp && npm install && npm run setup snowflake`. A PAT (`npm run setup snowflake -- --pat`) is only for headless jobs and only works if a Snowflake admin attached a network policy to your user (otherwise error 390432). Tokens land in `~/.copilot/tokens.json`.

There is no root `.env` / `.env.example` for PMs.

---

## 3. Jira and Figma (personal tokens)

Jira/Confluence and Figma use official MCP servers. Put **your** tokens in `.cursor/mcp.json` next to the committed copilot server. Keep `${workspaceFolder}` — never commit machine-absolute paths.

```json
{
  "mcpServers": {
    "copilot": {
      "command": "node",
      "args": ["mcp/bin/copilot-mcp.js"],
      "env": { "COPILOT_CONFIG_DIR": "${workspaceFolder}" }
    },
    "atlassian": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-atlassian"],
      "env": {
        "ATLASSIAN_SITE_URL": "https://phenompeople.atlassian.net",
        "ATLASSIAN_USER_EMAIL": "your.name@phenom.com",
        "ATLASSIAN_API_TOKEN": "<your-api-token>"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_PERSONAL_ACCESS_TOKEN": "<your-pat>"
      }
    }
  }
}
```

- Atlassian token: [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- Figma token: Figma → Settings → Security → Personal access tokens

**Claude Code:** run `claude` from this repo. `CLAUDE.md` loads skills and policies. For another repo, `@`-include this checkout’s `CLAUDE.md`. Point `COPILOT_CONFIG_DIR` at this checkout (absolute path for `copilot-mcp.js` if needed).

---

## 4. Your profile

Edit `me.md` at the repo root (gitignored). Cover role, products / Jira projects, default Drive folder, and working preferences. The onboarding agent can walk you through it.

---

## 5. Skills as slash commands

Every folder in `skills/` with a `SKILL.md` becomes a `/command` in Claude Code and Cursor once it is linked into `~/.claude/skills/`. Run once, and again after a pull that adds a skill:

```bash
bash onboarding/link-skills.sh
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

## 6. Engineering clones (optional)

Do **not** clone all ~76 repos on day one. Details: [`engineering/SETUP.md`](engineering/SETUP.md).

```bash
ssh -T git@bitbucket.org
./engineering/scripts/sync-repos.sh --list
./engineering/scripts/sync-repos.sh --only interview    # example — pick your product
```

`--only` values include `recruiter-hub`, `hrm`, `interview`, `screening`, `candidate-engagement`, `automation`. Full sync is opt-in (~6 GB). Never edit, commit, or push `engineering/repos/`.

---

## What's in here

```
skills/         Tool how-tos
policies/       Always-on rules (Jira, platform routing, …)
agents/         Sub-agents (onboarding, ticket analyst, …)
mcp/            Local MCP (Google, Snowflake, Vanilla KB)
engineering/    Code index + clone script (`repos/` is local / gitignored)
onboarding/     Setup doctor + visual dashboard
CLAUDE.md       Claude Code entry
.cursor/rules/  Cursor entry
```

Edit shared files, push to the default branch; others `git pull`. Team experiments go on a branch and merge via PR.
