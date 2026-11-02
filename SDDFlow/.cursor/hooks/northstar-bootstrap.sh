#!/bin/sh
# Cursor sessionStart hook (self-contained) — injects the SDD pointer.
# reads its bundled context file next to this script, so it needs nothing in the repo.
# Fail-open: emit {} on any problem so a session can never be blocked.
DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SNIP="$DIR/northstar-bootstrap-context.md"
cat > /dev/null   # drain stdin (unused)
[ -f "$SNIP" ] || { printf '{}'; exit 0; }
PY="$(command -v python3 || command -v python || true)"
[ -z "$PY" ] && { printf '{}'; exit 0; }
NORTHSTAR_SNIP="$SNIP" "$PY" - <<'EOF'
import json, os
try:
    with open(os.environ["NORTHSTAR_SNIP"], encoding="utf-8") as f:
        print(json.dumps({"additional_context": f.read().strip()}))
except Exception:
    print("{}")
EOF
