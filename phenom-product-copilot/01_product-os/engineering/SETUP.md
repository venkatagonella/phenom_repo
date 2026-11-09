# Setup — Engineering code context

This folder lets you answer engineering feasibility questions ("can we do X?", "where does Y actually happen?") by **reading Phenom's real code** in Cursor, instead of pinging engineering first and waiting a day.

It lives **inside Phenom - Product Copilot** as `engineering/`. Two pieces:

1. **`index/`** — a curated map of ~76 Phenom repos: what each one does, what it explicitly does *not* do, and which file to open first. Committed to git; `git pull` on Copilot updates it.
2. **`scripts/`** — a registry plus one script that clones those repos onto your machine under `engineering/repos/` (gitignored, ~6 GB for a full sync).

---

## Before you start

**You need Bitbucket read access to `phenompeople/*` over SSH.** Check it now:

```bash
ssh -T git@bitbucket.org
```

You want to see `logged in as <you>`. If you get a permission error, or a clone later fails with an access error, raise a DevOps ticket: a Jira POS ticket of type "Bitbukcet-Access-Request" with read access ([how it works](https://phenompeople.atlassian.net/wiki/spaces/DEVOPS/pages/57496830045)). `./scripts/access-request.sh` prints the fields to paste, including the repositories you still miss.

You'll also want **~6 GB of free disk** for a full sync, and git plus Cursor installed.

You do **not** need a Bitbucket API token for normal use. The optional `.env` file is only for the audit script in `scripts/`.

---

## 1. You already have the folder

If you cloned **Phenom - Product Copilot**, `engineering/` is already there. Open **this Copilot repo** as your Cursor workspace (not a parent mega-folder). Confirm the agent can see `engineering/CLAUDE.md` and `policies/engineering-context.md`.

## 2. Clone the repos

`repos/` is **empty on a fresh clone** — it's about 5.5 GB of live engineering code and it's gitignored. You clone it locally.

Start with just the area you actually work on rather than pulling all 76 repos on your first day:

```bash
cd engineering/scripts

./sync-repos.sh --list                 # see what's registered
./sync-repos.sh --dry-run              # see what would happen, change nothing

./sync-repos.sh --only recruiter-hub   # the CRM/RX platform
./sync-repos.sh --only hrm             # hiring-manager experience
./sync-repos.sh --only interview       # scheduling + Interview Intelligence
./sync-repos.sh --only screening
./sync-repos.sh --only candidate-engagement
```

When you're ready for everything (expect a long run):

```bash
./sync-repos.sh
```

The script is safe to re-run. It clones what's missing, fast-forwards what's already there, and **one failing repo no longer kills the whole run** — failures are collected and printed at the end. Missing Bitbucket access is expected for some repos; request access and re-run `--only <name>`.

## 3. Verify it worked

```bash
# something real should exist on disk
ls "../repos/recruiter-hub/candidates/candidates-api"

# branch pinning worked (this must say pre-develop, not main)
git -C "../repos/recruiter-hub/jobs/crm-jobs-service" rev-parse --abbrev-ref HEAD
```

Then ask your agent something that requires the index, for example: *"Using engineering/, where is departmentalization / job visibility enforced?"* A good answer names `crm-commons` and `DepartmentalizationManagerV2.java`. If instead it starts grepping all of `repos/` blindly, the engineering context rule isn't loading.

---

## Branch pinning — why several repos need it

For a number of Phenom repos, the **default branch is a stub or years stale**. Clone the default and you'll read an empty repo and conclude a capability doesn't exist.

`scripts/repos.yaml` pins the correct branch, and `sync-repos.sh` checks it out for you:

| Repo | Pinned branch | Default branch is |
|---|---|---|
| `crm-jobs-service` | `pre-develop` | `main` / `development` are stubs |
| `crm-commons` | `release` | matches the published artifact |
| `crm-storm-job-pull` | `release_25_02` | `master` is README only |
| `cp-facet-2.0` | `release-patch` | `master` stale since 2023 |
| `tags-service` | `master` | `main` is stub only |
| `crm-storm-job-pull-conf`, `storm-*-conf`, `crm-storm-transactions-conf` | `DEV` | `master` has no real config |

If the script reports `branch 'X' not found — cloned default branch instead`, the branch was renamed upstream. Confirm the current one with the owning team and update `branch:` in `repos.yaml`.

---

## How to actually use this

Don't grep `repos/` directly — 5.5 GB of Java will bury you. Follow the funnel:

```
index/taxonomy.md          which pillar owns this?
   -> index/capability-map.md      product language -> repo folder
   -> index/<domain>.md            scope + entry points
   -> index/repos/<domain>/capability-index.md    which repos to scan
   -> repos/...                    read the code
```

Rules of the road:

- **Never edit, commit, or push anything under `repos/`.** Those are live engineering repos, cloned for reading.
- **Which team to contact** is still owned by `policies/platform-routing.md` (one level up). `index/capability-map.md` maps the same language to *code locations*, not team ownership.

## Adding a repo

1. Add an entry to `scripts/repos.yaml` (`name`, `url`, `path`, and `branch` if the default isn't right)
2. `./sync-repos.sh --only <name>`
3. Add a row to `index/repo-catalog.md`
4. Add a short manifest under `index/repos/<domain>/` and list it in that domain's `capability-index.md`

Steps 3 and 4 are what keep this useful for everyone else. A cloned repo nobody indexed is just disk usage. Commit the index/script changes to Copilot so other PMs get them on `git pull`.

## Troubleshooting

**Every clone fails.** Bitbucket access. Re-run `ssh -T git@bitbucket.org`.

**Some clones fail, most work.** Per-repo access. The run finishes and lists them at the end; request access, then `./sync-repos.sh --only <name>`.

**It looks frozen.** The script runs SSH in batch mode so it fails fast instead of silently waiting on a passphrase prompt. A genuinely long pause is usually a large repo (`cp_ui_app_2.0`, `scheduling-main-app`). Use `--only` to work in smaller batches.

**A repo looks empty.** Check the branch table above — you're probably on a stub default branch.

**`pull failed` on a repo you didn't touch.** Something diverged locally. Since nothing here should ever be edited, the safe fix is to delete that folder under `repos/` and re-clone it.

## Day-2 updates

```bash
# New skills, policies, and index maps
git pull

# Fresher engineering code (only repos you already cloned, plus any new matches)
./engineering/scripts/sync-repos.sh
```
