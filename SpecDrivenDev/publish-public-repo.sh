#!/usr/bin/env bash
set -euo pipefail

# Publish SpecDrivenDev as a public GitHub repo (venkatagonella/SpecDrivenDev).
# Prerequisites: gh CLI installed and authenticated (`gh auth login`).

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRANCH="spec-driven-dev-public"
REMOTE="git@github.com:venkatagonella/SpecDrivenDev.git"

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: gh CLI not found. Install from https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Error: not logged in to GitHub. Run: gh auth login"
  exit 1
fi

cd "$REPO_ROOT"

if ! git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "Creating subtree branch $BRANCH..."
  git subtree split --prefix=SpecDrivenDev -b "$BRANCH"
fi

if gh repo view venkatagonella/SpecDrivenDev >/dev/null 2>&1; then
  VISIBILITY="$(gh repo view venkatagonella/SpecDrivenDev --json visibility -q .visibility)"
  echo "Repo exists (visibility: $VISIBILITY)"
  if [[ "$VISIBILITY" != "PUBLIC" ]]; then
    gh repo edit venkatagonella/SpecDrivenDev --visibility public --accept-visibility-change-consequences
    echo "Changed visibility to public."
  fi
else
  gh repo create venkatagonella/SpecDrivenDev \
    --public \
    --description "Spec-driven development workspace for Phenom CRM Core FRD/PRD authoring" \
    --source "$REPO_ROOT" \
    --remote spec-driven-dev-remote \
    --push=false
  echo "Created public repo."
fi

git push "$REMOTE" "$BRANCH:main" --force
echo "Pushed to https://github.com/venkatagonella/SpecDrivenDev"
