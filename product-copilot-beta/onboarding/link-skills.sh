#!/usr/bin/env bash
# Links every skill folder in skills/ (one with a SKILL.md) into ~/.claude/skills/,
# so it gets a /command in Claude Code. Cursor reads ~/.claude/skills/ too.
#
# Links, not copies: `git pull` updates every linked skill in place.
# Run it again after a pull that adds a new skill folder.
#
#   bash onboarding/link-skills.sh               # link all skills
#   bash onboarding/link-skills.sh --uninstall   # remove links that point into this repo

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../skills" && pwd)"
TARGET_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
GRAPHIFY_VERSION="0.9.92"   # keep in step with skills/graphify/SKILL.md

mkdir -p "$TARGET_DIR"

# Remove our links whose skill folder no longer exists (or all of them on --uninstall).
for link in "$TARGET_DIR"/*; do
  [[ -L "$link" ]] || continue
  dest="$(readlink "$link")"
  [[ "$dest" == "$SKILLS_DIR"/* ]] || continue
  if [[ "${1:-}" == "--uninstall" || ! -f "$dest/SKILL.md" ]]; then
    rm "$link"
    echo "removed  $(basename "$link")"
  fi
done
[[ "${1:-}" == "--uninstall" ]] && exit 0

for src in "$SKILLS_DIR"/*/; do
  src="${src%/}"
  [[ -f "$src/SKILL.md" ]] || continue
  name="$(basename "$src")"
  dst="$TARGET_DIR/$name"

  if [[ -L "$dst" ]]; then
    if [[ "$(readlink "$dst")" == "$src" ]]; then
      echo "ok       $name"
      continue
    fi
    rm "$dst"
    ln -s "$src" "$dst"
    echo "relinked $name"
  elif [[ -e "$dst" ]]; then
    echo "skipped  $name  ($dst is your own copy; delete it to use the Product OS version)"
  else
    ln -s "$src" "$dst"
    echo "linked   $name"
  fi
done

if [[ -f "$SKILLS_DIR/graphify/SKILL.md" ]] && ! command -v graphify >/dev/null 2>&1; then
  echo
  echo "graphify needs its CLI:  uv tool install graphifyy==$GRAPHIFY_VERSION"
fi

echo
echo "Done. Start a new Claude Code or Cursor chat to pick up new skills."
