# Phenom Engineering — Code Context

This repo holds **local clones of Phenom engineering repos**, organized by jobs-to-be-done, plus a curated index so feasibility questions can be answered by reading code instead of asking engineering first.

**This is a read-only reference layer.** Never edit, commit to, or push changes into anything under `repos/` — those are live engineering repos. Treat this folder as a research tool, not a place to build features.

## Structure

```
Phenom - Engineering/
├── index/                          ← START HERE for any feasibility question
│   ├── taxonomy.md                 ← pillar definitions and placement rules
│   ├── capability-map.md           ← platform-routing.md capability → pillar/repo
│   ├── repo-catalog.md             ← master list of every cloned repo
│   ├── repos/                      ← per-repo capability manifests
│   │   ├── _manifest-schema.md
│   │   ├── crm-automations/
│   │   ├── recruiter-hub/
│   │   ├── messaging/
│   │   ├── candidate-engagement/
│   │   ├── screening/
│   │   └── interview-management/
│   ├── product-experiences/
│   │   ├── screening.md
│   │   ├── candidate-engagement.md
│   │   └── interview-management.md
│   ├── recruiter-hub.md
│   └── platform/
│       ├── automations.md
│       ├── messaging.md
│       └── privacy-compliance.md
├── repos/                          ← actual git clones, mirrors index/ structure
│   ├── product-experiences/
│   │   ├── screening/
│   │   ├── candidate-engagement/
│   │   └── interview-management/
│   ├── recruiter-hub/
│   │   ├── shell/
│   │   ├── config/
│   │   ├── candidates/
│   │   ├── jobs/
│   │   └── …
│   └── platform/
│       ├── automations/
│       │   ├── workflow/
│       │   └── crm-automations/
│       ├── messaging/
│       └── privacy-compliance/
└── scripts/
    ├── repos.yaml                  ← list of repo name → git URL → target folder
    └── sync-repos.sh               ← clones missing repos / pulls existing ones
```

## Workflow for a feasibility question

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
5. Search/read the actual code under `repos/<pillar>/...` for the specific question — **max ~5 repos** unless the user asks for exhaustive coverage.
5. Answer with: the feasibility assessment, what would need to change, a confidence level, and which repos/entry points you based it on.
6. If the question spans pillars (common for automations/messaging/privacy), check every relevant domain file's "Platform dependencies" section.
7. Always caveat: this is a code-reading assessment, not a scoping estimate. Recommend validating with the owning team for effort, edge cases, and anything not visible in code (infra, data volume, org constraints).

## Keeping the index current

- New repo cloned → add a row to `repo-catalog.md`, then a short entry to the matching domain file.
- Repo used by multiple pillars → note it in "Also used by" in `repo-catalog.md` rather than cloning twice.
- Repo doesn't fit a pillar → log it in `repo-catalog.md`'s "Unassigned" section instead of guessing.
- Run `scripts/sync-repos.sh` periodically to pull latest on all cloned repos.

## Relationship to other repos in this workspace

- **`Phenom - Product Copilot/policies/platform-routing.md`** is the source of truth for *which team to contact*. This repo's `capability-map.md` mirrors that language but points to *where the code is*.
- Product knowledge (what a feature does, for whom) stays in `Phenom - Product Copilot/knowledge/`.
- Your feasibility conclusions from a specific project should be written back to `Personal - AI Product Leader/04_Projects/<project>/`, not stored here.
