#!/usr/bin/env python3
"""Ingest one Jira MCP search JSON file into a meaningful slice directory."""
from __future__ import annotations

import json
import pathlib
import re
import sys


def opt(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get("value") or v.get("name") or v.get("displayName") or ""
    if isinstance(v, list):
        return ", ".join(x for x in (opt(i) for i in v) if x)
    return str(v)


def date(v):
    if not v:
        return ""
    s = str(v)
    return s[:10] if re.match(r"\d{4}-\d{2}-\d{2}", s) else s


def main():
    if len(sys.argv) < 4:
        print("usage: ingest_jira_page.py <src_json> <out_dir> <page_num> [expected]")
        return 2
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    page = int(sys.argv[3])
    expected = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(src.read_text())
    lines = []
    for raw in data.get("issues", []):
        f = raw["fields"]
        key = raw["key"]
        clients = [
            opt(f.get(k))
            for k in [
                "customfield_11213",
                "customfield_14805",
                "customfield_14396",
                "customfield_14523",
            ]
        ]
        lines.append(
            json.dumps(
                {
                    "key": key,
                    "summary": f.get("summary") or "",
                    "status": (f.get("status") or {}).get("name", ""),
                    "issuetype": (f.get("issuetype") or {}).get("name", ""),
                    "projectKey": (f.get("project") or {}).get("key", ""),
                    "eta": date(f.get("customfield_14383"))
                    or date(f.get("customfield_15541")),
                    "client": next((c for c in clients if c), ""),
                    "fixVersions": opt(f.get("fixVersions")),
                    "url": f"https://phenompeople.atlassian.net/browse/{key}",
                },
                ensure_ascii=False,
            )
        )
    path = out / f"page-{page:04d}.ndjson"
    path.write_text("\n".join(lines) + ("\n" if lines else ""))
    # recompute fetched
    keys = set()
    for p in out.glob("page-*.ndjson"):
        for line in p.open():
            if line.strip():
                keys.add(json.loads(line)["key"])
    meta = {
        "fetched": len(keys),
        "expected": expected or None,
        "nextPageToken": data.get("nextPageToken"),
        "isComplete": bool(data.get("isLast")) or not data.get("nextPageToken"),
        "lastPage": page,
        "pageCount": len(list(out.glob("page-*.ndjson"))),
    }
    (out / "progress.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta))
    if meta.get("nextPageToken"):
        print("TOKEN:" + meta["nextPageToken"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
