# Maintainer notes — ownership and access

This file is for whoever runs the shared Copilot git repo. It is not required reading for day-to-day PM use. PMs follow [README.md](README.md).

## GitHub

- **Repo:** [officiallybasti/phenom-product-copilot](https://github.com/officiallybasti/phenom-product-copilot) (private). Clone: `https://github.com/officiallybasti/phenom-product-copilot.git`
- Add PMs as collaborators (pull); maintainers need push.
- We are **not** creating a second Copilot git repo.
- We are **not** committing Bitbucket engineering clones. `engineering/repos/` is a local cache.
- Personal vaults live in `02_personal-os/`, but only the template (rules, scripts, starter files, empty folders) is tracked. Everything a PM writes there is gitignored and never pushed.

## Backend credentials (not PM onboarding)

Google OAuth client secrets and the Vanilla API key live on Tim’s Cloud Run backend (`https://product-copilot-backend-iarivxijkq-uc.a.run.app`). PMs sign in via `cd mcp && npm run setup` in the browser; they do not need 1Password or a root `.env`.

1Password (`hi-copilot OAuth Apps`, `hi-copilot API Keys`) is a **maintainer / backend** vault for rotating those Cloud Run secrets — not a step in the PM README.

## How PMs get new skills

You commit to the default branch and push. They `git pull`. Engineering **index** updates ride the same pull. Engineering **code** refreshes only when they run `engineering/scripts/sync-repos.sh`.

## Bitbucket

Clones use SSH to `phenompeople/*`. Every PM clones all registered repositories during onboarding (a required step in Product OS). Missing access is fixed with a DevOps POS ticket ("Bitbukcet-Access-Request"); `engineering/scripts/access-request.sh` prints the fields. Process: https://phenompeople.atlassian.net/wiki/spaces/DEVOPS/pages/57496830045
