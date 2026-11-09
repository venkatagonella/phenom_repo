#!/usr/bin/env bash
# Prints the fields for a DevOps Bitbucket access ticket (Jira POS, type "Bitbukcet-Access-Request"),
# so a PM can paste them straight in. Lists the registered repos that are NOT cloned on this laptop;
# --all lists every registered repo. Process: https://phenompeople.atlassian.net/wiki/spaces/DEVOPS/pages/57496830045
#
#   ./engineering/scripts/access-request.sh          # repos you still miss
#   ./engineering/scripts/access-request.sh --all    # every repo in repos.yaml

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGISTRY="$SCRIPT_DIR/repos.yaml"
CLONES="$SCRIPT_DIR/../repos"
ALL=false
[[ "${1:-}" == "--all" ]] && ALL=true

slugs=()
name=""
while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]*-[[:space:]]name:[[:space:]]*(.+)$ ]]; then
    name="${BASH_REMATCH[1]//[\"\']/}"
  elif [[ "$line" =~ ^[[:space:]]+path:[[:space:]]*(.+)$ ]] && [[ -n "$name" ]]; then
    path="${BASH_REMATCH[1]//[\"\']/}"
    if $ALL || [[ ! -d "$CLONES/$path/.git" ]]; then slugs+=("$name"); fi
    name=""
  fi
done < "$REGISTRY"

email="${PMOS_USER_EMAIL:-$(python3 -c 'import json,os;print((json.load(open(os.path.expanduser("~/.claude.json"))).get("oauthAccount") or {}).get("emailAddress",""))' 2>/dev/null || true)}"
[[ -z "$email" ]] && email="$(git config user.email 2>/dev/null || true)"

if [[ ${#slugs[@]} -eq 0 ]]; then
  echo "Every registered repository is cloned. No ticket needed."
  exit 0
fi

cat <<OUT
Raise a Jira POS ticket of type "Bitbukcet-Access-Request" with these fields
(how it works: https://phenompeople.atlassian.net/wiki/spaces/DEVOPS/pages/57496830045):

Repositories: $(IFS=,; echo "${slugs[*]}" | sed 's/,/, /g')
User Emails:  ${email:-<your @phenom.com email>}
Access Level: read

Your manager approves it, DevOps moves it to "Approved Bitbucket", and access arrives within minutes.
Then run: ./engineering/scripts/sync-repos.sh
OUT
