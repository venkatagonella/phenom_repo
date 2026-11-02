# Engineering context (feasibility from code)

Use `engineering/` in this repo to answer “can we do this?” and “where does this happen in code?” by reading Phenom’s real services. This is a **read-only** research layer, not a place to build features.

## Hard rules

- **Never edit, commit, or push anything under `engineering/repos/`.** Those are live engineering repos cloned for reading only. Treat any write request targeting that tree as out of scope — flag it instead of executing it.
- Do not copy full source files into other folders in this repo — cite file paths and line numbers instead.
- Do not pull personal coaching notes, 1:1s, or private vault content into this repo.

## Where to start

Read `engineering/CLAUDE.md` first. In short: `engineering/index/taxonomy.md` → `engineering/index/capability-map.md` → the relevant domain file → then a small set of clones under `engineering/repos/`. Prefer manifests under `engineering/index/repos/` before grepping.

If `engineering/repos/` is missing or empty, tell the user to follow `engineering/SETUP.md` (`ssh -T git@bitbucket.org`, then `engineering/scripts/sync-repos.sh --only <pillar>`). Do not invent code that is not on disk.

## Team routing vs code location

`policies/platform-routing.md` is the source of truth for **which team to contact**. `engineering/index/capability-map.md` maps the same capabilities to **where the code is**. Keep them consistent; do not invent a second ownership table.

Always answer feasibility questions with a **confidence level** and a recommendation to validate with the owning team.
