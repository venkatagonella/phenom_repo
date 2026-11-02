# Phenom Engineering — Local Code Context

Read-only clones of Phenom engineering repos, nested in **Phenom - Product Copilot** as `engineering/`. Organized by jobs-to-be-done so feasibility questions can be answered by reading code.

**First-time setup:** [`SETUP.md`](SETUP.md). Agent workflow: [`CLAUDE.md`](CLAUDE.md).

See `CLAUDE.md` for the full agent workflow. Quick orientation for humans:

## Pillars

1. **Product Experiences**
   - **Screening** — screening questions/flows, assessment integrations
   - **Candidate Engagement** — email/SMS campaigns, nurture, audience targeting, campaign analytics
   - **Interview Management** — scheduling, structured interviews, Interview Intelligence
2. **Recruiter Hub** — CRM platform + CRM UI shell
3. **Platform**
   - **Automations**
     - **Workflow** — Automation Engine (cross-pod recipes, triggers, pipeline state)
     - **CRM Automations** — CRM recipe runtime, Temporal workflows, automation UI, search
   - **Messaging** — notifications/communication platform
   - **Privacy & Compliance** — consent, retention, PII, audit

Full definitions and placement rules: `index/taxonomy.md`.

## Rollout status

**76 repos registered** in `scripts/repos.yaml`:

| Pillar / domain | Repos |
|---|---|
| **Recruiter Hub** (shell, config, candidates, jobs, hrm, storm, search, pipeline, projects, shared, dashboard) | 34 |
| **Interview Management** (scheduling + II) | 12 |
| **Candidate Engagement** (campaign stack + Storm confs) | 10 |
| **Platform → Automations** (Workflow + CRM Automations) | 10 |
| **Screening** (video/assessment) | 6 |
| **Platform → Messaging** | 4 |
| **Platform → Privacy & Compliance** | not started |

Live status per repo: `index/repo-catalog.md`. A pillar being listed means it has a working indexed set, not that every repo in that domain is captured — add more as feasibility questions surface gaps.

## Adding a repo

1. Add it to `scripts/repos.yaml` (name, git URL, target path under `repos/`, plus `branch:` if the default branch is a stub).
2. Run `./scripts/sync-repos.sh --only <name>` to clone it.
3. Add a row to `index/repo-catalog.md`.
4. Add a short manifest under `index/repos/<domain>/` and list it in that domain's `capability-index.md`.

## Rules

- **Read-only.** Never edit or commit into anything under `repos/` — those are live engineering repos, just cloned here for reference.
- `repos/` is gitignored in this folder — it's a local cache (~5.5 GB when fully synced), not something to version control here.
- Don't clone repos twice for cross-pillar use — note secondary consumers in `repo-catalog.md`'s "Also used by" column instead.
- Several repos need a **non-default branch** to contain real code (`crm-jobs-service` → `pre-develop`, `crm-commons` → `release`, Storm `*-conf` → `DEV`, …). These are pinned via `branch:` in `scripts/repos.yaml`; see `SETUP.md` for the full table.
