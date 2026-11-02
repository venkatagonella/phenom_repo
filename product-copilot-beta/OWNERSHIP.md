# Maintainer notes — ownership and access

This file is for whoever runs the shared Copilot git repo. It is not required reading for day-to-day PM use. PMs follow [README.md](README.md).

## GitHub

- **Repo:** [officiallybasti/phenom-product-copilot](https://github.com/officiallybasti/phenom-product-copilot) (private). Clone: `https://github.com/officiallybasti/phenom-product-copilot.git`
- Add PMs as collaborators (pull); maintainers need push.
- We are **not** creating a second Copilot git repo.
- We are **not** committing Bitbucket engineering clones. `engineering/repos/` is a local cache.
- We are **not** putting personal vaults (`Personal - AI Product Leader`) in this repo.

## Backend credentials (not PM onboarding)

Google OAuth client secrets and the Vanilla API key live on Tim’s Cloud Run backend (`https://product-copilot-backend-iarivxijkq-uc.a.run.app`). PMs sign in via `cd mcp && npm run setup` in the browser; they do not need 1Password or a root `.env`.

1Password (`hi-copilot OAuth Apps`, `hi-copilot API Keys`) is a **maintainer / backend** vault for rotating those Cloud Run secrets — not a step in the PM README.

## How PMs get new skills

You commit to the default branch and push. They `git pull`. Engineering **index** updates ride the same pull. Engineering **code** refreshes only when they run `engineering/scripts/sync-repos.sh`.

## Bitbucket

Clones use SSH to `phenompeople/*`. Partial failure on first sync is success. Do not require a full 76-repo clone for onboarding.
