#!/usr/bin/env bash
# Opens the local Product Copilot onboarding dashboard.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PHENOM_COPILOT_PORT:-8787}"
URL="http://127.0.0.1:${PORT}"
LOG_FILE="${TMPDIR:-/tmp}/phenom-copilot-onboarding.log"
PID_FILE="${TMPDIR:-/tmp}/phenom-copilot-onboarding.pid"

open_url() {
  if command -v open >/dev/null 2>&1; then
    open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL"
  else
    python3 -c "import webbrowser; webbrowser.open('$URL')"
  fi
}

if curl --silent --fail --max-time 1 "$URL/api/status" >/dev/null 2>&1; then
  open_url
  echo "Product Copilot onboarding is open at $URL"
  exit 0
fi

nohup python3 "$SCRIPT_DIR/server.py" --port "$PORT" --no-open >"$LOG_FILE" 2>&1 &
echo $! >"$PID_FILE"

for _ in {1..30}; do
  if curl --silent --fail --max-time 1 "$URL/api/status" >/dev/null 2>&1; then
    open_url
    echo "Product Copilot onboarding is open at $URL"
    echo "Local server PID: $(cat "$PID_FILE")"
    exit 0
  fi
  sleep 0.1
done

echo "Dashboard did not start. See $LOG_FILE" >&2
exit 1
