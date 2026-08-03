#!/bin/bash
set -euo pipefail
ROOT="/Users/venkata.gonella/phenom_repo/Disney/exports"
cd "$ROOT"
while true; do
  python3 merge_all_slices.py >/tmp/rx-merge-meta.json
  python3 - <<'PY'
import json, pathlib
meta=json.load(open('/tmp/rx-merge-meta.json'))
slices=pathlib.Path('slices')
prog=[]
for p in sorted(slices.glob('*/progress.json')):
    try:
        d=json.loads(p.read_text())
        prog.append(f"{p.parent.name}:{d.get('fetched',0)}/{d.get('expected','?')} complete={d.get('isComplete')}")
    except Exception as e:
        prog.append(f"{p.parent.name}:err")
print(meta.get('exportedCount'), '/', meta.get('expectedTotal'), f"({meta.get('coveragePct')}%)")
print(' | '.join(prog[:20]))
PY
  # stop if coverage >= 99.5%
  cov=$(python3 -c "import json; print(json.load(open('/tmp/rx-merge-meta.json')).get('coveragePct',0))")
  python3 - <<PY
cov=float("$cov")
raise SystemExit(0 if cov >= 99.5 else 1)
PY && break
  sleep 60
done
echo "DONE"
cat /tmp/rx-merge-meta.json
