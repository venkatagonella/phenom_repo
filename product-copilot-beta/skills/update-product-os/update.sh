#!/usr/bin/env bash
# Brings this Product OS checkout up to date and re-runs everything that depends on it:
# pull, dependency install when mcp/ changed, slash-command links, the catalog, health checks.
# The /update-product-os skill runs this and explains the result.
#
#   bash skills/update-product-os/update.sh                # pull and refresh
#   bash skills/update-product-os/update.sh --check        # show what would come in, change nothing
#   bash skills/update-product-os/update.sh --autostash    # pull although tracked files have local edits
#   bash skills/update-product-os/update.sh --extra <dir>  # maintainer: also list <dir>/.claude workflows in the catalog
#   bash skills/update-product-os/update.sh --site <dir>   # maintainer: rebuild the PM OS site afterwards
#
# Exit codes: 0 ok · 2 local edits block the pull · 3 branch has diverged from origin · 4 fetch failed

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"

CHECK=0 AUTOSTASH="" EXTRA="" SITE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK=1 ;;
    --autostash) AUTOSTASH="--autostash" ;;
    --extra) EXTRA="$2"; shift ;;
    --site) SITE="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 64 ;;
  esac
  shift
done

section() { printf '\n## %s\n' "$1"; }
note() { printf -- '- %s\n' "$1"; }

section "Repo"
branch="$(git branch --show-current)"
note "branch: $branch"
old="$(git rev-parse HEAD)"

if ! git fetch --quiet origin; then
  note "STOP fetch failed: check network and GitHub access (collaborator on phenom-product-copilot)"
  exit 4
fi
upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [[ -z "$upstream" ]]; then
  # A local feature branch: never pull into it. Compare with origin/main so the PM still sees what is new.
  upstream="origin/main"
  PULL=0
  note "ACTION $branch has no upstream, so nothing is pulled into it; switch to main to update (git switch main)"
else
  PULL=1
  [[ "$branch" == "main" ]] || note "WARN not on main: updating $branch from $upstream"
fi
incoming="$(git rev-list --count HEAD.."$upstream")"
ahead="$(git rev-list --count "$upstream"..HEAD)"
note "commits on $upstream you don't have: $incoming"
[[ "$PULL" -eq 1 && "$ahead" -gt 0 ]] && note "WARN $ahead local commit(s) not pushed"

if [[ "$CHECK" -eq 1 || "$PULL" -eq 0 ]]; then
  section "On $upstream, not here"
  git log --no-merges --date=short --format='- %ad %s' HEAD.."$upstream" || true
  [[ "$CHECK" -eq 1 ]] && exit 0
fi

if [[ "$PULL" -eq 1 && "$incoming" -gt 0 ]]; then
  dirty="$(git status --porcelain --untracked-files=no)"
  if [[ -n "$dirty" && -z "$AUTOSTASH" ]]; then
    section "Blocked"
    note "STOP local edits to tracked files; nothing was pulled:"
    printf '%s\n' "$dirty" | sed 's/^/  /'
    exit 2
  fi
  if ! git pull --ff-only --quiet $AUTOSTASH; then
    section "Blocked"
    note "STOP your branch and origin have diverged; nothing was merged"
    exit 3
  fi
fi
new="$(git rev-parse HEAD)"

section "What changed"
if [[ "$old" == "$new" ]]; then
  note "already up to date"
  changed=""
else
  git log --no-merges --date=short --format='- %ad %s' "$old..$new"
  changed="$(git diff --name-status "$old" "$new")"
  printf '%s\n' "$changed" | awk -F'\t' '
    { p = $NF; s = ($1 ~ /^A/) ? "added" : ($1 ~ /^D/) ? "removed" : "updated" }
    p ~ /^skills\/[^/]+\/SKILL\.md$/ { split(p, a, "/"); print "  skill " s ": /" a[2]; next }
    p ~ /^skills\/[^/]+\.mdc?$/      { sub(/^skills\//, "", p); sub(/\.mdc?$/, "", p); print "  skill " s ": " p; next }
    p ~ /^policies\/[^/]+\.md$/      { sub(/^policies\//, "", p); sub(/\.md$/, "", p); print "  policy " s ": " p; next }
    p ~ /^agents\//                  { sub(/^agents\//, "", p); sub(/\.yaml$/, "", p); print "  agent " s ": " p; next }
    p ~ /^knowledge\//               { split(p, a, "/"); k["  knowledge updated: " a[2]] = 1; next }
    p ~ /^engineering\/index\//      { k["  engineering index updated"] = 1; next }
    p == "CLAUDE.md"                 { k["  CLAUDE.md updated"] = 1; next }
    END { for (x in k) print x }'
fi

touched() { printf '%s\n' "$changed" | grep -qE "$1"; }

section "Dependencies"
if [[ -n "$changed" ]] && touched $'\tmcp/package(-lock)?\\.json$'; then
  if (cd mcp && npm install --no-audit --no-fund --silent); then note "mcp: npm install done"; else note "WARN mcp: npm install failed"; fi
else
  note "mcp: no change"
fi

section "Slash commands"
links="$(bash onboarding/link-skills.sh 2>&1 | grep -vE '^(ok |$|Done\.)' || true)"
if [[ -n "$links" ]]; then printf '%s\n' "$links" | sed 's/^/  /'; else note "all skill links current"; fi

section "Catalog"
node onboarding/build-catalog.mjs ${EXTRA:+--extra "$EXTRA"} | sed 's/^/  /'

section "Health"
nodev="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
[[ "$nodev" -ge 20 ]] && note "node $nodev ok" || note "WARN node 20+ needed (found $nodev)"
[[ -f me.md ]] && note "me.md present" || note "WARN me.md missing: the onboarding agent can write it with you"
[[ -f "$HOME/.copilot/tokens.json" ]] && note "copilot tokens present" || note "WARN no ~/.copilot/tokens.json: run cd mcp && npm run setup"
[[ -d mcp/node_modules ]] || note "WARN mcp/node_modules missing: run cd mcp && npm install"
if [[ -n "$changed" ]] && touched $'\tskills/[^/]+/'; then
  (cd mcp && npm run --silent check >/dev/null 2>&1) && note "repo health check ok" || note "WARN repo health check failed: run cd mcp && npm run check"
fi
[[ -n "$changed" ]] && touched $'\tCLAUDE\\.md$' && note "ACTION start a new chat: CLAUDE.md changed"
[[ -n "$changed" ]] && touched $'\tskills/' && note "ACTION start a new chat to load new or changed skills"
[[ -n "$changed" ]] && touched $'\tengineering/index/' && note "INFO engineering index changed; code clones refresh only with engineering/scripts/sync-repos.sh"
unshared="$(git status --porcelain --untracked-files=all -- skills policies agents knowledge | awk '{print $2}' | cut -d/ -f1-2 | sort -u)"
if [[ -n "$unshared" ]]; then
  note "INFO local changes not in the shared repo yet:"
  printf '%s\n' "$unshared" | sed 's/^/    /'
fi

if [[ -n "$SITE" ]]; then
  section "PM OS site"
  if (cd "$SITE" && npm run --silent build); then note "site rebuilt in $SITE/dist"; else note "WARN site build failed"; fi
fi

section "Result"
note "ok: $(git log -1 --date=short --format='%h %ad %s')"
