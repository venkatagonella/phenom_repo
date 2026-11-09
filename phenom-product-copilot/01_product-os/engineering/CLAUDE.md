# Phenom Engineering — Code Context

This folder (`engineering/` inside **Phenom - Product Copilot**) holds **local clones of Phenom engineering repos**, organized by jobs-to-be-done, plus a curated index so feasibility questions can be answered by reading code instead of asking engineering first.

**This is a read-only reference layer.** Never edit, commit to, or push changes into anything under `repos/` — those are live engineering repos. Treat this folder as a research tool, not a place to build features. The clone cache is gitignored; only the index and scripts live in the Copilot repo.

## Structure

```
engineering/
├── index/                          ← START HERE for any feasibility question
│   ├── taxonomy.md                 ← pillar definitions and placement rules
│   ├── capability-map.md           ← platform-routing.md capability → pillar/repo
│   ├── repo-catalog.md             ← master list of every cloned repo
│   ├── repos/                      ← per-repo capability manifests (committed)
│   ├── cross-cutting/
│   ├── product-experiences/
│   ├── recruiter-hub.md
│   └── platform/
├── repos/                          ← actual git clones (LOCAL ONLY, gitignored)
└── scripts/
    ├── repos.yaml                  ← list of repo name → git URL → target folder
    └── sync-repos.sh               ← clones missing repos / pulls existing ones
```

## Workflow for a feasibility question

0. **Is it a cross-cutting question?** If it's about roles, permissions, access control, scopes/departmentalization, or "who is allowed to see this" → read `index/cross-cutting/access-control.md` **first**. Audited domains are answered there without a code scan. Only scan code if the domain is marked not-yet-audited, the question is about one specific endpoint's enforcement, or `last_reviewed` is stale relative to the repo's current branch.
1. Read `index/taxonomy.md` if you don't already know which pillar the question belongs to.
2. Read `index/capability-map.md` to translate product/Jira language into a pillar + repo folder.
3. **If manifests exist for that domain**, use them to pick which repos to scan — do not grep all repos in the folder. Check manifests first, before grepping:
   - `index/repos/recruiter-hub/capability-index.md`
   - `index/repos/crm-automations/capability-index.md`
   - `index/repos/messaging/capability-index.md`
   - `index/repos/candidate-engagement/capability-index.md`
   - `index/repos/screening/capability-index.md`
   - `index/repos/interview-management/capability-index.md`
4. Read the matching domain file under `index/` (e.g. `index/product-experiences/screening.md`) for scope, known entry points, and platform dependencies.
5. Search/read the actual code under `repos/<pillar>/...` for the specific question — **max ~5 repos** unless the user asks for exhaustive coverage. **Exclude test files** (`--glob '!*test*'`) when inferring production behavior — several repos have test trees referencing collections and methods that don't reflect production config.
6. Answer with: the feasibility assessment, what would need to change, a confidence level, and which repos/entry points you based it on.
7. If the question spans pillars (common for automations/messaging/privacy), check every relevant domain file's "Platform dependencies" section.
8. Always caveat: this is a code-reading assessment, not a scoping estimate. Recommend validating with the owning team for effort, edge cases, and anything not visible in code (infra, data volume, org constraints).
9. **Confirm the branch.** Several repos have stale or empty default branches (see `scripts/repos.yaml` `branch:` pins). State which commit/branch you read when the answer will be shared outside this workspace.

## Keeping the index current

- New repo cloned → add a row to `repo-catalog.md`, then a short entry to the matching domain file.
- Repo used by multiple pillars → note it in "Also used by" in `repo-catalog.md` rather than cloning twice.
- Repo doesn't fit a pillar → log it in `repo-catalog.md`'s "Unassigned" section instead of guessing.
- Run `scripts/sync-repos.sh` periodically to pull latest on all cloned repos.
- **A question forced a multi-pillar code scan that the index couldn't route** → that's a signal it's cross-cutting. Write the answer into `index/cross-cutting/` and link it from the affected domain files + `capability-map.md`.

## Relationship to the rest of this repo

- **`../policies/platform-routing.md`** is the source of truth for *which team to contact*. This folder's `index/capability-map.md` mirrors that language but points to *where the code is*.
- Product knowledge (what a feature does, for whom) stays in `../knowledge/`.
- Do not store personal project decisions here. Shared index updates (new manifests, corrected branch pins) belong in this folder and should be committed to Copilot so other PMs get them on `git pull`.
