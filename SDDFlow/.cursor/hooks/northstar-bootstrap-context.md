This repository uses **Spec-Driven Development (SDD)**. For any non-trivial change:

- Start with **`/northstar`** (the router skill) — it classifies the change and hands off to the right flow.
- The non-negotiable rules are loaded as the **SDD constitution** rule. Project context lives in `northstar/steering/*` — create it with `/ns-steer` if it's missing.
- Specs live in `northstar/specs/NNN-slug/`; the catalog is `northstar/specs/INDEX.md`. Do **Phase-0 context discovery** (read steering, scan the index, read overlapping specs, inspect code) before drafting.

Trivial/exempt changes (typos, comments, formatting, dep bumps) don't need a spec — see the constitution's ceremony tiers.
