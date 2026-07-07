# Product Steering — What we build & why

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec.

## What this product is

SDDFlow is a **Spec-Driven Development (SDD) workspace** inside the `phenom_repo` monorepo. It hosts the **Northstar kit** (Cursor/Kiro adapters, hooks, skills, agents) and the canonical SDD document tree (`northstar/steering/`, `northstar/specs/`). It is not an application runtime — it is the process and tooling layer for spec-before-code workflows on Phenom engineering work.

## Who uses it (roles)

- **Engineer** — runs `/northstar` and `/ns-*` flows, authors and approves specs, implements approved changes (often in sibling repos such as `NorthStarCheck/`).
- **Reviewer** — approves requirements/design/tasks gates; uses subagent reviews and `pr-review` skill at PR time.
- **Kit maintainer** — updates the Northstar kit via the installer; regenerates adapters from `.northstar/` in the upstream kit repo.

## Problems it solves / boundaries

- **In scope:** SDD routing, steering context, increment specs, IDE hooks/skills/agents, agent onboarding (`AGENTS.md`).
- **Out of scope:** Application business logic (lives in target repos, e.g. `NorthStarCheck/`); FRD authoring for CRM Core (see `SpecDrivenDev/`).

## Compliance & policy obligations

- No secrets in specs, steering, or committed hook scripts.
- Increment specs are immutable except Changelog; behavior changes get new specs with `amends` / `supersedes_reqs` linkage.
- Match ceremony to risk (constitution §7): exempt trivial edits; full flow for features and migrations.

## Non-functional defaults

- Phase-0 discovery reads `northstar/steering/*` and `northstar/specs/INDEX.md` before every non-exempt change.
- Specs use EARS requirements with stable `REQ-ID`s and testable acceptance criteria.
