---
name: Repo Structure
type: policy
description: Rules for modifying the copilot config repo filesystem
always: true
---

## Never create symlinks inside config folders

Do **not** create symlinks in `skills/`, `policies/`, `agents/`, or `knowledge/`.

In particular, never run commands like:

```bash
ln -s ../skills skills    # inside skills/ — creates infinite nesting
ln -s ../policies policies
ln -s ../agents agents
```

These folders are already wired into `CLAUDE.md` via `@skills/...`, `@policies/...`, and agent definitions. No extra linking is needed.

If you need to reference another file, use a markdown `@` import or a relative path in prose — not filesystem symlinks.

## Request-generated artifacts → `product-copilot/`

Store **all** files created from ad-hoc user requests (UI mocks, HTML placeholders, drafts, exports, one-off analyses, screenshots-derived mockups, etc.) under:

`product-copilot/`

Examples: `job-header-primary-title-placeholder.html`, `candidate-jobs-primary-title-placeholder.html`.

- Do **not** put these in `skills/`, `policies/`, `agents/`, `knowledge/`, `mcp/`, or the repo root
- Contents of `product-copilot/` are **gitignored** (see `.gitignore`) — never whitelist `!product-copilot/**`
- Create the folder if missing; keep filenames descriptive and kebab-case

## Allowed filesystem changes

- Add or edit `.md` / `.yaml` files directly in the correct folder
- Put request-generated working files only in `product-copilot/`
- Run `npm run check` from `mcp/` after structural changes to verify no bad symlinks exist
