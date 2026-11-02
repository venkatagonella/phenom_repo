#!/usr/bin/env bash
# Extract a lightweight skeleton from a cloned repo for manifest authoring.
# Usage: ./extract-repo-manifest.sh <path-relative-to-repos/>
# Example: ./extract-repo-manifest.sh platform/automations/crm-automations/crm-automation-service

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOS_ROOT="$(dirname "$SCRIPT_DIR")/repos"
REL="${1:?Usage: $0 <path-relative-to-repos/>}"
TARGET="$REPOS_ROOT/$REL"
SLUG="$(basename "$TARGET")"

if [[ ! -d "$TARGET/.git" ]]; then
  echo "Not a git repo: $TARGET" >&2
  exit 1
fi

echo "# Auto-extracted skeleton: $SLUG"
echo "# Path: repos/$REL"
echo "# Generated: $(date +%Y-%m-%d)"
echo ""
echo "branch: $(git -C "$TARGET" branch --show-current 2>/dev/null || echo 'detached')"
echo "files: $(find "$TARGET" -type f ! -path '*/.git/*' ! -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')"
echo ""

# Stack detection
for f in pom.xml build.sbt package.json; do
  [[ -f "$TARGET/$f" ]] && echo "stack_marker: $f"
done

echo ""
echo "## Controllers (Java)"
find "$TARGET" -name "*Controller*.java" ! -path '*/test/*' ! -path '*/node_modules/*' 2>/dev/null \
  | sed "s|$TARGET/||" | head -20 || true

echo ""
echo "## Workflows / Activities (Java)"
find "$TARGET" \( -name "*Workflow*.java" -o -name "*Activity*.java" \) ! -path '*/test/*' 2>/dev/null \
  | sed "s|$TARGET/||" | head -20 || true

echo ""
echo "## Angular modules (if UI)"
find "$TARGET/src/app/modules" -maxdepth 1 -mindepth 1 -type d 2>/dev/null \
  | sed "s|.*/modules/||" | sort || true

echo ""
echo "## Test frameworks (if present)"
for marker in "*.robot" "*.spec.ts" "playwright.config.*"; do
  count=$(find "$TARGET" -name "$marker" ! -path '*/node_modules/*' 2>/dev/null | wc -l | tr -d ' ')
  [[ "$count" -gt 0 ]] && echo "$marker: $count files"
done

echo ""
echo "## Top-level dirs"
ls "$TARGET" 2>/dev/null | grep -v node_modules | head -20
