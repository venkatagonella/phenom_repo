#!/bin/sh
# Cursor subagentStop hook (OPTIONAL accelerator) — when one of the SDD review subagents
# (ns-spec-reviewer / ns-tasks-reviewer / ns-spec-compliance-reviewer / ns-code-quality-reviewer)
# finishes WITHOUT an approval, auto-continue the parent to address the issues before proceeding.
# For any other subagent, or an approved verdict, it does nothing.
#
# This only accelerates Cursor's review loops; the portable baseline is the prose loop the
# /ns-implement and /ns-specify prompts already drive (Kiro relies on that, since Kiro hooks
# do not fire inside subagents). Fail-open and bounded by loop_limit in hooks.json.
ROOT="${CURSOR_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || { printf '{}'; exit 0; }
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then cat > /dev/null; printf '{}'; exit 0; fi

# Capture the hook JSON from stdin BEFORE running python via heredoc (heredoc owns python's
# stdin), then hand it to python through the environment.
NORTHSTAR_IN="$(cat)"
NORTHSTAR_IN="$NORTHSTAR_IN" "$PY" - <<'EOF'
import json, os, re
try:
    data = json.loads(os.environ.get("NORTHSTAR_IN", "") or "{}")
except Exception:
    print("{}"); raise SystemExit

summary = data.get("summary") or ""
status = data.get("status") or ""
headers = ("## Spec Review", "## Tasks Review",
           "## Spec-Compliance Review", "## Code-Quality Review")

# Only act on a completed SDD review (recognizable by its output header).
if status != "completed" or not any(h in summary for h in headers):
    print("{}"); raise SystemExit

m = re.search(r"\*\*Status:\*\*\s*(.+)", summary)
verdict = (m.group(1).strip().lower() if m else "")
if verdict.startswith(("approved", "spec compliant")):
    print("{}"); raise SystemExit

print(json.dumps({"followup_message":
    "The SDD review subagent reported issues (not an approval). Address every issue it listed, "
    "then re-run the same review and proceed only when it returns Approved / Spec compliant."}))
EOF
