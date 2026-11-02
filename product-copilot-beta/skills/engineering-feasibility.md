---
name: engineering-feasibility
type: skill
description: Answer product feasibility and "where in the code" questions using the nested engineering index and local Bitbucket clones. Load when the user asks if something is possible, where a capability lives, how a service works, or mentions engineering/repos, JTBD pillars, or sync-repos.
always: false
triggers: [feasibility, where in the code, can we, engineering clone, sync-repos, departmentalization, recruiter-hub]
---

# Engineering feasibility

Follow `engineering/CLAUDE.md` and `policies/engineering-context.md`.

1. Confirm clones exist under `engineering/repos/` for the relevant pillar. If not, point at `engineering/SETUP.md` and `engineering/scripts/sync-repos.sh --only <filter>` — do not guess.
2. Route via `engineering/index/taxonomy.md` → `capability-map.md` → domain file → `index/repos/<domain>/capability-index.md`.
3. Read at most ~5 repos. Exclude tests when inferring production behavior.
4. Never edit `engineering/repos/`.
5. Cite paths, branch/commit if it matters, confidence level, and “validate with the owning team” using `policies/platform-routing.md` for *who* to contact.
