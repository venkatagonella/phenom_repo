# SDDFlow — Agent Guide

This workspace is the **Northstar SDD home** for spec-driven development tooling and project context. Application code for features typically lives in sibling repos (e.g. `../NorthStarCheck/`).

**Start here:** type **`/northstar`** and describe the change. The router classifies it and hands off to the right `/ns-*` flow.

---

## SDD quick reference

| Flow | Use when |
|------|----------|
| `/northstar` | Any change — routes to the right flow and ceremony tier |
| `/ns-steer` | First run or stale steering — writes `northstar/steering/*` |
| `/ns-specify` | Feature, migration, greenfield (Full tier: spec → design → tasks) |
| `/ns-bug` | Defect — `bugfix.md` + regression test plan |
| `/ns-refactor` | Behavior-preserving restructure — invariant matrix |
| `/ns-implement` | Build an **approved** spec |
| `/ns-finish` | Tests green → update living layer → PR |

**Living context:** `northstar/steering/product.md`, `tech.md`, `structure.md`  
**Increment specs:** `northstar/specs/NNN-slug/` — catalog in `northstar/specs/INDEX.md`

**Constitution:** loaded via `.cursor/rules/ns-constitution.mdc` (always on).

---

## Installed kit (v1.0.0)

- **Cursor:** `.cursor/skills/`, `.cursor/agents/`, `.cursor/hooks/`
- **Kiro:** `.kiro/` (mirror of skills/agents)
- **Reinstall:** from this folder: `curl -fsSL https://video-qa.phenompro.com/northstar/install.sh | sh -s -- --force`

---

## Local checks

When `scripts/` is present:

```bash
python3 scripts/northstar_check.py
python3 scripts/gen_index.py --check
```

---

## Monorepo siblings

| Path | Purpose |
|------|---------|
| `../NorthStarCheck/` | Reference TypeScript app with existing `northstar/specs/` |
| `../SpecDrivenDev/` | FRD/PRD authoring for Phenom CRM Core |

---

## First-time setup checklist

1. Trust this workspace in Cursor (hooks need execute permission).
2. Confirm `/northstar` responds in chat.
3. Run `/ns-steer` if steering needs refresh after major repo changes.
4. Add validation scripts to `scripts/` when provided by the kit release.
