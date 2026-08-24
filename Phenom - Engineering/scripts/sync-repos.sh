#!/usr/bin/env bash
# Clones any repo in repos.yaml that isn't present yet, and updates any that
# already exist. Read-only usage assumption: this workspace never pushes back
# to these repos.
#
# Usage:
#   ./sync-repos.sh                  # sync everything in repos.yaml
#   ./sync-repos.sh --only hrm       # only entries whose name/path matches "hrm"
#   ./sync-repos.sh --dry-run        # show what would happen, change nothing
#   ./sync-repos.sh --list           # list registered repos and exit
#
# A single repo failing (no access, bad branch, network) is reported and
# skipped — it does not abort the rest of the run.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINEERING_ROOT="$(dirname "$SCRIPT_DIR")"
REPOS_ROOT="$ENGINEERING_ROOT/repos"
CONFIG_FILE="$SCRIPT_DIR/repos.yaml"

# Fail fast instead of blocking on a passphrase or host-key prompt — an
# interactive prompt in a 79-repo loop looks like a hang.
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes -o ConnectTimeout=15}"

ONLY_FILTER=""
DRY_RUN=false
LIST_ONLY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --only)    ONLY_FILTER="${2:-}"; shift 2 ;;
    --only=*)  ONLY_FILTER="${1#*=}"; shift ;;
    --dry-run) DRY_RUN=true; shift ;;
    --list)    LIST_ONLY=true; shift ;;
    -h|--help)
      sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *)
      echo "Unknown option: $1 (try --help)" >&2
      exit 2 ;;
  esac
done

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "No repos.yaml found at $CONFIG_FILE" >&2
  exit 1
fi

cloned=0 updated=0 skipped=0 failed=0
declare -a FAILED_REPOS=()

# Minimal parser for the constrained repos.yaml format (list of
# name/url/path/branch entries). Not a general YAML parser.
name="" url="" path="" branch=""

reset_entry() { name="" url="" path="" branch=""; }

# Make sure an existing clone is on the branch repos.yaml asks for.
ensure_branch() {
  local target="$1" want="$2" label="$3"
  local current
  current="$(git -C "$target" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  if [[ "$current" == "$want" ]]; then
    return 0
  fi
  echo "    branch: $current -> $want"
  if ! git -C "$target" fetch origin "$want" --quiet 2>/dev/null; then
    echo "    ! could not fetch branch '$want'"
    return 1
  fi
  git -C "$target" checkout -B "$want" "origin/$want" --quiet 2>/dev/null
}

process_entry() {
  [[ -n "$name" && -n "$url" && -n "$path" ]] || return 0

  if [[ -n "$ONLY_FILTER" && "$name" != *"$ONLY_FILTER"* && "$path" != *"$ONLY_FILTER"* ]]; then
    return 0
  fi

  if [[ "$LIST_ONLY" == true ]]; then
    printf '  %-32s %s%s\n' "$name" "$path" "${branch:+  (branch: $branch)}"
    return 0
  fi

  local target="$REPOS_ROOT/$path"

  if [[ "$DRY_RUN" == true ]]; then
    if [[ -d "$target/.git" ]]; then
      echo "would update  $name${branch:+  [$branch]}"
    else
      echo "would clone   $name -> $path${branch:+  [$branch]}"
    fi
    return 0
  fi

  if [[ -d "$target/.git" ]]; then
    echo "-> Updating $name ($path)"
    if [[ -n "$branch" ]]; then
      if ! ensure_branch "$target" "$branch" "$name"; then
        FAILED_REPOS+=("$name (branch $branch)")
        failed=$((failed + 1))
        return 0
      fi
    fi
    if git -C "$target" pull --ff-only --quiet 2>/dev/null; then
      updated=$((updated + 1))
    else
      echo "    ! pull failed (local changes, diverged, or no access) — left as is"
      FAILED_REPOS+=("$name (pull)")
      failed=$((failed + 1))
    fi
  else
    echo "-> Cloning $name into $path${branch:+  [$branch]}"
    mkdir -p "$(dirname "$target")"
    local -a clone_args=(clone --quiet)
    [[ -n "$branch" ]] && clone_args+=(--branch "$branch")
    if git "${clone_args[@]}" "$url" "$target" 2>/dev/null; then
      cloned=$((cloned + 1))
    else
      # Retry without --branch: the pinned branch may have been renamed.
      if [[ -n "$branch" ]] && git clone --quiet "$url" "$target" 2>/dev/null; then
        echo "    ! branch '$branch' not found — cloned default branch instead"
        FAILED_REPOS+=("$name (branch '$branch' missing, on default)")
        failed=$((failed + 1))
      else
        echo "    ! clone failed — check Bitbucket access for $name"
        rm -rf "$target" 2>/dev/null
        FAILED_REPOS+=("$name (clone)")
        failed=$((failed + 1))
      fi
    fi
  fi
}

if [[ "$LIST_ONLY" == true ]]; then
  echo "Registered repos${ONLY_FILTER:+ matching \"$ONLY_FILTER\"}:"
fi

while IFS= read -r line; do
  trimmed="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  case "$trimmed" in
    "- name:"*)
      process_entry
      reset_entry
      name="$(echo "${trimmed#- name:}" | sed -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//')"
      ;;
    "url:"*)
      url="$(echo "${trimmed#url:}" | sed -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//')"
      ;;
    "path:"*)
      path="$(echo "${trimmed#path:}" | sed -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//')"
      ;;
    "branch:"*)
      branch="$(echo "${trimmed#branch:}" | sed -e 's/^[[:space:]]*//' -e 's/^"//' -e 's/"$//')"
      ;;
  esac
done < "$CONFIG_FILE"
process_entry

[[ "$LIST_ONLY" == true || "$DRY_RUN" == true ]] && exit 0

total=$((cloned + updated + failed))
if [[ "$total" -eq 0 ]]; then
  echo "Nothing matched${ONLY_FILTER:+ filter \"$ONLY_FILTER\"}. Add entries to $CONFIG_FILE or check the filter."
  exit 0
fi

echo ""
echo "Done. $cloned cloned, $updated updated, $failed failed."
if [[ "$failed" -gt 0 ]]; then
  echo ""
  echo "Needs attention:"
  for r in "${FAILED_REPOS[@]}"; do
    echo "  - $r"
  done
  echo ""
  echo "Most common cause is missing Bitbucket access. Ask in #rx-eng for read"
  echo "access to the repos above, then re-run: ./sync-repos.sh --only <name>"
fi
echo ""
echo "Reminder: use index/ (taxonomy -> capability-map -> domain file) to pick"
echo "which repos to read. Never edit anything under repos/."
