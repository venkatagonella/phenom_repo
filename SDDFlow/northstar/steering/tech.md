# Tech Steering — Stack, conventions, standards

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec and design.

## Stack

- **SDD kit:** Northstar kit v1.0.0 (installed via `curl -fsSL https://video-qa.phenompro.com/northstar/install.sh | sh -- --force` in this folder).
- **IDE adapters:** `.cursor/` (Cursor), `.kiro/` (Kiro) — generated bundles; do not hand-edit for kit changes (regenerate from upstream `.northstar/`).
- **Hooks:** `.cursor/hooks.json` wires `sessionStart` → `northstar-bootstrap.sh`, `subagentStop` → `northstar-review-advance.sh`.
- **Validation (when present):** `python3 scripts/northstar_check.py`, `python3 scripts/gen_index.py --check` (stdlib Python 3.8+).
- **Sibling app reference:** `../NorthStarCheck/` — TypeScript/Express/Vitest sample app with an existing `northstar/` tree.

## Conventions

- **Canonical SDD paths:** `northstar/steering/`, `northstar/specs/` only — not `docs/specs/` or other legacy folders.
- **Skills:** invoke `/northstar` to route; workflow skills are `ns-specify`, `ns-bug`, `ns-refactor`, `ns-steer`, `ns-implement`, `ns-finish`.
- **Rules:** `ns-constitution.mdc` (always on), `ns-spec-authoring.mdc` (scoped to `northstar/**`).
- **Hook scripts:** shell + `jq` where needed; must stay executable (`chmod +x`).

## Testing standards

- Application tests live in the target repo (e.g. `NorthStarCheck/tests/`), not in SDDFlow itself.
- Every implemented `REQ-ID` must have a passing test in the implementation repo.
- Bugs require a regression test (fails before fix, passes after).

## Constraints / banned patterns

- Do not rewrite shipped kit skill/agent files in `.cursor/` or `.kiro/` for one-off project needs — use steering, specs, or custom skills under `.cursor/skills/` that don't collide with kit names.
- Do not commit credentials; `scan-for-secrets.sh` (if wired) blocks obvious patterns in prompts.
- Installer requires git repo root or `--force` (SDDFlow is not the monorepo git root — use `--force` when re-installing here).
