#!/usr/bin/env python3
"""Ingest one MCP searchJiraIssuesUsingJql JSON response into refresh-2026."""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def opt(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return (
            v.get("displayName")
            or v.get("value")
            or v.get("name")
            or ""
        )
    if isinstance(v, list):
        return ", ".join(x for x in (opt(i) for i in v) if x)
    return str(v)


def date(v):
    if not v:
        return ""
    s = str(v)
    return s[:10] if re.match(r"\d{4}-\d{2}-\d{2}", s) else s


def main():
    if len(sys.argv) < 2:
        print("usage: ingest_page.py <src_json> [page_num]")
        return 2
    src = pathlib.Path(sys.argv[1])
    data = json.loads(src.read_text(encoding="utf-8"))
    # tolerate MCP wrapper text before JSON
    if not isinstance(data, dict) or "issues" not in data:
        text = src.read_text(encoding="utf-8")
        data = json.loads(text[text.find("{") :])

    progress = json.loads((ROOT / "progress.json").read_text(encoding="utf-8"))
    page = int(sys.argv[2]) if len(sys.argv) > 2 else int(progress.get("lastPage", 0)) + 1

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
                "pmOwner": opt(f.get("customfield_15223")),
                "url": f"https://phenompeople.atlassian.net/browse/{key}",
            }
        )

    out = ROOT / f"page-{page:04d}.ndjson"
    out.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in lines)
        + ("\n" if lines else ""),
        encoding="utf-8",
    )
    # also keep raw for debugging
    (ROOT / f"raw-{page:04d}.json").write_text(
        json.dumps(data, ensure_ascii=False), encoding="utf-8"
    )

    keys = set()
    for p in ROOT.glob("page-*.ndjson"):
        for line in p.open(encoding="utf-8"):
            if line.strip():
                keys.add(json.loads(line)["key"])

    progress.update(
        {
            "fetched": len(keys),
            "nextPageToken": data.get("nextPageToken"),
            "isComplete": bool(data.get("isLast")) or not data.get("nextPageToken"),
            "lastPage": page,
            "pageCount": len(list(ROOT.glob("page-*.ndjson"))),
        }
    )
    (ROOT / "progress.json").write_text(json.dumps(progress, indent=2), encoding="utf-8")
    print(json.dumps({
        "page": page,
        "pageRows": len(lines),
        "fetched": progress["fetched"],
        "expected": progress.get("expected"),
        "isComplete": progress["isComplete"],
        "hasToken": bool(progress.get("nextPageToken")),
    }))
    if progress.get("nextPageToken"):
        print("TOKEN:" + progress["nextPageToken"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
