#!/usr/bin/env bash
# Connects npm on this laptop to Phenom's package registry, so prototypes can install the design system
# (@phenom/react-ds) and Font Awesome Pro. Writes a marked block into ~/.npmrc (your user config).
# Credentials stay in ~/.npmrc: never in this repo, never printed.
#
#   bash 01_product-os/onboarding/setup-npm.sh                   # asks for the Nexus credential (hidden input)
#   bash 01_product-os/onboarding/setup-npm.sh --from <.npmrc>   # take the credentials from a .npmrc you already have,
#                                                             # e.g. in a cloned Phenom UI repo
#   bash 01_product-os/onboarding/setup-npm.sh --check           # is it configured? does the registry answer?
#
# Or set PHENOM_NEXUS_AUTH (and optionally FONTAWESOME_TOKEN) in the environment before running.
# The registry is only reachable on the Phenom VPN.

set -euo pipefail

NPMRC="${NPM_CONFIG_USERCONFIG:-$HOME/.npmrc}"
HOST="pie-nexus.phenompro.com"
REGISTRY="https://$HOST/repository/pie-npm-group/"
BEGIN="# >>> Product OS: Phenom registry (managed by 01_product-os/onboarding/setup-npm.sh)"
END="# <<< Product OS: Phenom registry"
MODE="write"
FROM=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) MODE="check" ;;
    --from) FROM="${2:?--from needs a path to a .npmrc}"; shift ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

configured() { [[ -f "$NPMRC" ]] && grep -q "^@phenom:registry=.*$HOST" "$NPMRC" && grep -q "^//$HOST/.*:_auth" "$NPMRC"; }

reachable() {
  # A version number back means the registry answered and accepted the credential.
  # perl's alarm is a hard 30 s cap: npm can hang far past its own fetch timeout when the registry is unreachable.
  (cd "${TMPDIR:-/tmp}" && perl -e 'alarm 30; exec @ARGV' npm view @phenom/react-ds version --fetch-timeout=15000 --fetch-retries=0 2>/dev/null) | tail -1
}

if [[ "$MODE" == "check" ]]; then
  if ! configured; then
    echo "MISSING ~/.npmrc has no Phenom registry entry: run bash 01_product-os/onboarding/setup-npm.sh"
    exit 1
  fi
  echo "ok      ~/.npmrc points @phenom packages to the Phenom registry"
  grep -q "^//npm.fontawesome.com/:_authToken" "$NPMRC" && echo "ok      Font Awesome Pro token present" || echo "INFO    no Font Awesome Pro token (only needed if a prototype uses @fortawesome/pro-*)"
  v="$(reachable || true)"
  if [[ -n "$v" ]]; then echo "ok      registry answers: @phenom/react-ds $v"; else echo "WARN    registry did not answer in 15 s: connect to the Phenom VPN, or the credential is wrong"; exit 1; fi
  exit 0
fi

nexus="${PHENOM_NEXUS_AUTH:-}"
fa="${FONTAWESOME_TOKEN:-}"
if [[ -n "$FROM" ]]; then
  [[ -f "$FROM" ]] || { echo "STOP $FROM not found"; exit 1; }
  nexus="$(sed -nE "s#^//$HOST/repository/:_auth=\"?([^\"]+)\"?.*#\1#p" "$FROM" | head -1)"
  fa="$(sed -nE 's#^//npm.fontawesome.com/:_authToken=\"?([^\"]+)\"?.*#\1#p' "$FROM" | head -1)"
  [[ -n "$nexus" ]] || { echo "STOP no //$HOST/repository/:_auth line in $FROM"; exit 1; }
fi
if [[ -z "$nexus" ]]; then
  echo "Paste the Phenom Nexus credential (the value after _auth=, without quotes). Input is hidden."
  read -rs nexus
  echo
fi
[[ -n "$nexus" ]] || { echo "STOP no credential given"; exit 1; }

touch "$NPMRC"
chmod 600 "$NPMRC"
cp -p "$NPMRC" "$NPMRC.bak-product-os"
# Drop our old block and any stray lines for the same registry, keep everything else.
awk -v b="$BEGIN" -v e="$END" -v host="$HOST" '
  $0 == b { skip = 1; next }
  $0 == e { skip = 0; next }
  skip { next }
  $0 ~ "^@phenom:registry=" || index($0, "//" host "/") == 1 { next }
  { print }' "$NPMRC.bak-product-os" >"$NPMRC"
{
  echo "$BEGIN"
  echo "legacy-peer-deps=true"
  echo "@phenom:registry=$REGISTRY"
  echo "//$HOST/repository/:_auth=\"$nexus\""
  if [[ -n "$fa" ]]; then
    echo "@fortawesome:registry=https://npm.fontawesome.com/"
    echo "@awesome.me:registry=https://npm.fontawesome.com/"
    echo "//npm.fontawesome.com/:_authToken=$fa"
  fi
  echo "$END"
} >>"$NPMRC"
chmod 600 "$NPMRC"

echo "ok      wrote the Phenom registry to $NPMRC (backup: $NPMRC.bak-product-os)"
[[ -z "$fa" ]] && echo "INFO    no Font Awesome Pro token added; only needed if a prototype uses @fortawesome/pro-*"
v="$(reachable || true)"
if [[ -n "$v" ]]; then echo "ok      registry answers: @phenom/react-ds $v"; else echo "WARN    registry did not answer in 15 s: connect to the Phenom VPN and run --check"; fi
