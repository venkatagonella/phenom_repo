---
name: Repo Structure
type: policy
description: Rules for modifying the copilot config repo filesystem
always: true
metadata:
  owner: nikhilsharma-phenom
  status: stable
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

## Request-generated artifacts → `02_personal-os/outputs/`

Store **all** files created from ad-hoc user requests (UI mocks, HTML placeholders, drafts, exports, one-off analyses, screenshots-derived mockups, etc.) under:

`02_personal-os/outputs/` (at the repo root, next to `01_product-os/`)

Examples: `job-header-primary-title-placeholder.html`, `candidate-jobs-primary-title-placeholder.html`.

- Do **not** put these in `01_product-os/` (skills, policies, agents, knowledge, mcp) or the repo root
- Everything you write in `02_personal-os/` is **gitignored** — never add a `!` rule for it in `.gitignore`
- Create the folder if missing; keep filenames descriptive and kebab-case

## Allowed filesystem changes

- Add or edit `.md` / `.yaml` files directly in the correct folder
- Put request-generated working files only in `02_personal-os/outputs/`
- Run `npm run check` from `mcp/` after structural changes to verify no bad symlinks exist
