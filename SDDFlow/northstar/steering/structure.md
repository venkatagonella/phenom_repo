# Structure Steering — How the codebase is organized

> **Layer 1 / living context.** Keep this current; the agent uses it for Phase-0 discovery and file placement.

## Directory layout

```
SDDFlow/
├── AGENTS.md                 # Agent entry guide for this workspace
├── .cursor/                  # Cursor adapter (kit v1.0.0)
│   ├── agents/               # ns-implementer + 4 reviewers
│   ├── hooks/                # northstar-bootstrap, review-advance, custom guards
│   ├── hooks.json            # sessionStart, subagentStop wiring
│   ├── rules/                # ns-constitution, ns-spec-authoring, custom rules
│   └── skills/               # /northstar, /ns-*, practice skills, pr-review
├── .kiro/                    # Kiro adapter (same skills/agents + steering pointers)
├── northstar/
│   ├── steering/             # Layer 1 — product.md, tech.md, structure.md (this file)
│   └── specs/                # Layer 2 — increment specs + INDEX.md
└── scripts/                  # northstar_check.py, gen_index.py (add when available from kit)
```

**Monorepo context:** git root is `../` (`phenom_repo/`). Sibling folders include `NorthStarCheck/` (reference TS app), `SpecDrivenDev/` (FRD workflow).

## Module boundary rules

- **SDDFlow** holds process/tooling only — no `src/` application code here unless a spec explicitly adds it.
- **Implementation** for product features targets sibling repos; specs in `northstar/specs/` should set `touches:` globs pointing at real code paths (e.g. `../NorthStarCheck/src/**`).
- **Kit files** under `.cursor/` and `.kiro/` are overwritten on kit reinstall (`.bak` backups saved).

## Where things go

| Change type | Where |
|-------------|--------|
| New increment spec | `northstar/specs/NNN-slug/spec.md` (+ `design.md`/`tasks.md` for Full tier) |
| Living context update | `northstar/steering/*.md` |
| Custom agent skill | `.cursor/skills/<name>/SKILL.md` (avoid clashing with `ns-*` kit skills) |
| Custom always-on rule | `.cursor/rules/<name>.mdc` |
| CI validation scripts | `scripts/` (when shipped by kit maintainer) |

Refresh `northstar/specs/INDEX.md` when adding specs (`/ns-finish` or `gen_index.py`).
