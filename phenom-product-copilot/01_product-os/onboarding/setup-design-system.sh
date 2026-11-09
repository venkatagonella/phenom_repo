#!/usr/bin/env bash
# Connects the Phenom React design system MCP (components, props, usage for @phenom/react-ds) to Claude Code
# and Cursor on this laptop. It needs a key, so it can't sit in the repo's shared tool list: this script adds it
# to your user config (~/.claude.json via `claude mcp`, and ~/.cursor/mcp.json). The key is never printed.
# The Angular Storybook MCP needs no key and is already in the repo's .mcp.json and .cursor/mcp.json.
#
#   bash 01_product-os/onboarding/setup-design-system.sh           # asks for the key (hidden input)
#   bash 01_product-os/onboarding/setup-design-system.sh --check   # is it connected in Claude Code and Cursor?
#
# Or set PHENOM_DS_MCP_KEY in the environment before running. Ask the design system team for the key.

set -euo pipefail

NAME="phenom-react-ds-mcp"
URL="https://ph-ds-mcp-poc.phdcpoc.workers.dev/mcp"
HOST="ph-ds-mcp-poc.phdcpoc.workers.dev"
CURSOR_MCP="$HOME/.cursor/mcp.json"
MODE="write"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) MODE="check" ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

# Prints where the React DS server is registered (any server name, matched by URL): "claude", "cursor", both or nothing.
registered() {
  python3 - "$HOST" "$CURSOR_MCP" <<'EOF'
import json, os, sys
host, cursor_path = sys.argv[1], sys.argv[2]
def has(servers):
    return any(host in (s.get("url") or "") for s in (servers or {}).values() if isinstance(s, dict))
found = []
try:
    d = json.load(open(os.path.expanduser("~/.claude.json")))
    if has(d.get("mcpServers")) or any(has(p.get("mcpServers")) for p in d.get("projects", {}).values()):
        found.append("claude")
except Exception:
    pass
try:
    if has(json.load(open(cursor_path)).get("mcpServers")):
        found.append("cursor")
except Exception:
    pass
print(" ".join(found))
EOF
}

if [[ "$MODE" == "check" ]]; then
  where="$(registered)"
  [[ "$where" == *claude* ]] && echo "ok      Claude Code has the React design system MCP" || echo "MISSING Claude Code: run bash 01_product-os/onboarding/setup-design-system.sh"
  [[ "$where" == *cursor* ]] && echo "ok      Cursor has the React design system MCP" || echo "MISSING Cursor: run bash 01_product-os/onboarding/setup-design-system.sh"
  [[ -n "$where" ]]
  exit $?
fi

key="${PHENOM_DS_MCP_KEY:-}"
if [[ -z "$key" ]]; then
  read -rsp "Phenom design system MCP key (ask the design system team): " key
  echo
fi
key="${key#Bearer }"
[[ -n "$key" ]] || { echo "STOP no key given"; exit 1; }

code="$(curl -s -o /dev/null -w '%{http_code}' -m 10 -X POST "$URL" \
  -H "Authorization: Bearer $key" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"01_product-os","version":"1"}}}' || true)"
case "$code" in
  200) echo "ok      key accepted" ;;
  401|403) echo "STOP the server refused this key (HTTP $code)"; exit 1 ;;
  *) echo "WARN    the server did not answer as expected (HTTP ${code:-none}); saving the key anyway" ;;
esac

if command -v claude >/dev/null 2>&1; then
  claude mcp remove "$NAME" -s user >/dev/null 2>&1 || true
  claude mcp add --scope user --transport http "$NAME" "$URL" --header "Authorization: Bearer $key" >/dev/null
  echo "ok      Claude Code: added $NAME (user scope)"
else
  echo "SKIP    Claude Code not installed"
fi

if [[ -d "$HOME/.cursor" ]]; then
  PHENOM_DS_MCP_KEY="$key" python3 - "$CURSOR_MCP" "$NAME" "$URL" <<'EOF'
import json, os, sys
path, name, url = sys.argv[1:4]
try:
    data = json.load(open(path))
except FileNotFoundError:
    data = {}
servers = data.setdefault("mcpServers", {})
# One entry per server: drop copies of the same URL under another name.
for other in [k for k, s in servers.items() if k != name and isinstance(s, dict) and s.get("url") == url]:
    del servers[other]
servers[name] = {"url": url, "headers": {"Authorization": "Bearer " + os.environ["PHENOM_DS_MCP_KEY"]}}
tmp = path + ".tmp"
with open(tmp, "w") as f:
    json.dump(data, f, indent=2)
os.chmod(tmp, 0o600)
os.replace(tmp, path)
EOF
  echo "ok      Cursor: added $NAME to ~/.cursor/mcp.json"
else
  echo "SKIP    Cursor not installed"
fi

echo "Restart Claude Code and Cursor to load it."
