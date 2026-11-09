---
name: update-product-os
description: "Update this Product OS checkout: pull the latest shared repo, refresh slash-command links and dependencies, rebuild the skill catalog, run health checks, and tell the PM what is new for them. Use for /update-product-os, \"update product os\", \"pull the latest copilot\", \"what's new in the copilot\", or after someone says a new skill was shared."
metadata:
  owner: officiallybasti
  status: beta
  try: "/update-product-os"
  example: examples/update-product-os/check-run.md
---

# Update Product OS

One command instead of `git pull` plus four follow-up steps. The script does the mechanical work; you check its result and explain it.

## Run

From the repo root (the folder with `CLAUDE.md` and `skills/update-product-os/`):

```bash
bash skills/update-product-os/update.sh
```

Options, only when they apply:

| Flag | When |
|------|------|
| `--check` | The PM asks what is new without updating |
| `--autostash` | Exit code 2, and the PM said yes to keeping their edits on top of the update |
| `--extra <workspace>` | Maintainer: list that workspace's `.claude/` workflows in the catalog as "not shared yet" |
| `--site <dir>` | Maintainer: rebuild the PM OS site after the catalog |

## Exit codes

| Code | Meaning | What you do |
|------|---------|-------------|
| 0 | Updated (or already current) | Report, step 3 below |
| 2 | Local edits to tracked files block the pull | List the files. Ask once: keep them on top of the update (`--autostash`), or stop. Never discard, reset or check out over them |
| 3 | Branch and origin diverged | Explain in one line. Do not merge or rebase without an explicit yes |
| 4 | Fetch failed | Network or GitHub access; the PM needs collaborator access on `phenom-product-copilot` |

## Report (keep it under 15 lines)

1. **New for you.** From "What changed", list added and updated skills, policies and agents. Read `me.md` and put the ones that touch the PM's products or Jira projects first, each with its slash command or trigger phrase and one line on what it does (from its front matter).
2. **Do now.** Every `ACTION` and `WARN` line, as an instruction. Typical: start a new chat, run `cd mcp && npm run setup`, write `me.md`.
3. **Good to know.** `INFO` lines: engineering index changed (clones refresh only with `engineering/scripts/sync-repos.sh --only <pillar>`), local work not shared yet (offer to help open a pull request for it).

If nothing came in, say so in one line and only report `WARN` / `ACTION` items.

## Personal vault check (only if the PM has one)

The script adds new Personal OS starter files to `02_personal-os/` (never overwrites). Rule and template changes in `02_personal-os/` arrive with the pull itself. If the PM hasn't run `set me up` yet, offer it.

If `02_personal-os/` is set up (or `me.md` names another vault), and the update touched `knowledge/` or a glossary:

- Compare the changed shared entries with the PM's local context files.
- List contradictions. The shared version wins because it was reviewed.
- Propose the local edits. Apply them only after a yes.

## Rules

- Never commit, push or open a pull request from this skill.
- Never stage or copy the PM's own files from `02_personal-os/`: they are gitignored on purpose.
- Never edit anything under `engineering/repos/`.
- Do not run `engineering/scripts/sync-repos.sh` unless the PM asks.
- The catalog JSON in `onboarding/data/` is generated. Never edit it by hand.
