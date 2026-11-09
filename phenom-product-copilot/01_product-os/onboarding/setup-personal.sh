#!/usr/bin/env bash
# Fills your Personal OS (02_personal-os/) with its starter files: context stubs, task lists, meeting routing.
# The folders, rules and templates come with the repo. The files this script adds are yours and are
# gitignored: they are never committed or pushed.
#
#   bash onboarding/setup-personal.sh            # add starter files that are missing (first run or after an update)
#   bash onboarding/setup-personal.sh --status   # say what would be added, change nothing
#
# Run from 01_product-os/ (or anywhere: paths are resolved from this script).
# It never overwrites a file, and a starter file you deleted is not brought back.
# The list of starter files already offered lives in 02_personal-os/99_System/.template-files.

set -euo pipefail

OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # 01_product-os/
ROOT="$(dirname "$OS_DIR")"
VAULT="$ROOT/02_personal-os"
STARTER="$VAULT/99_System/templates/vault"
SEEN="$VAULT/99_System/.template-files"
MODE="sync"

case "${1:-}" in
  --status) MODE="status" ;;
  "") ;;
  -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
  *) echo "unknown option: $1" >&2; exit 2 ;;
esac

[[ -d "$STARTER" ]] || { echo "STOP 02_personal-os/99_System/templates/vault/ not found: update the repo first (/update-product-os)"; exit 1; }

first_run=0
[[ -f "$VAULT/99_System/context/00-me.md" ]] || first_run=1
seen_list=""
[[ -f "$SEEN" ]] && seen_list="$(cat "$SEEN")"
offered=""
added=0

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  offered+="$rel"$'\n'
  if grep -qxF "$rel" <<<"$seen_list"; then continue; fi   # offered before: respect edits and deletions
  [[ -e "$VAULT/$rel" ]] && continue
  # Safety: only ever write files the repo ignores, so personal content can't be committed by accident.
  if ! git -C "$ROOT" check-ignore -q "02_personal-os/$rel" 2>/dev/null; then
    echo "SKIP $rel: it would be tracked by git (check .gitignore)"
    continue
  fi
  if [[ "$MODE" == "status" ]]; then
    echo "would add  $rel"
  else
    mkdir -p "$VAULT/$(dirname "$rel")"
    cp -p "$STARTER/$rel" "$VAULT/$rel"
  fi
  added=$((added + 1))
done < <(cd "$STARTER" && find . -type f ! -name '.DS_Store' | sed 's#^\./##' | LC_ALL=C sort)

if [[ "$MODE" == "status" ]]; then
  echo "$added starter file(s) to add"
  exit 0
fi

printf '%s%s\n' "$offered" "$seen_list" | grep -v '^$' | LC_ALL=C sort -u >"$SEEN"

# Belt and braces: nothing personal may be tracked.
tracked_personal="$(git -C "$ROOT" ls-files -ci --exclude-standard -- 02_personal-os 2>/dev/null || true)"
[[ -n "$tracked_personal" ]] && echo "WARN personal files are tracked by git; remove with: git rm --cached <file>" && printf '  %s\n' $tracked_personal

if [[ $first_run -eq 1 && $added -gt 0 ]]; then
  echo "created  $added starter files in 02_personal-os/ (gitignored: they stay on this laptop)"
  echo "Next: in a chat in this repo, say \"set me up\"."
elif [[ $added -gt 0 ]]; then
  echo "added    $added new starter file(s) to 02_personal-os/"
else
  echo "ok       02_personal-os/ has every starter file"
fi
