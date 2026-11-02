#!/usr/bin/env python3
"""Phenom Community (Vanilla) KB helper — read articles and stage DRAFTS only.

Deliberately has no publish path. This tool cannot create a live article,
edit a live article, or change article status. Publishing is a human step
performed inside Vanilla after review.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://community.phenom.com/api/v2"
SITE = "https://community.phenom.com"
# Cloudflare rejects bare API clients with error 1010 without a browser UA.
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Any request outside this allowlist is refused before it leaves the process,
# so a prompt-injected or mistaken instruction still cannot publish.
ALLOWED = (
    ("GET", "/search"),
    ("GET", "/articles/"),
    ("GET", "/knowledge-bases"),
    ("GET", "/knowledge-categories"),
    ("GET", "/drafts"),
    ("POST", "/drafts"),
    ("DELETE", "/drafts/"),
)


def token() -> str:
    path = Path.home() / ".copilot" / "tokens.json"
    try:
        return json.loads(path.read_text())["vanilla"]["access_token"]
    except FileNotFoundError:
        sys.exit(f"No token file at {path}. Authenticate the Vanilla integration first.")
    except KeyError:
        sys.exit(f"No vanilla.access_token in {path}.")


def guard(method: str, path: str) -> None:
    if method in ("PATCH", "PUT"):
        sys.exit(f"REFUSED: {method} is never allowed. This tool cannot modify live articles.")
    if path.startswith("/articles") and method != "GET":
        sys.exit(
            "REFUSED: writing to /articles would create or change a live article. "
            "Stage a draft instead and publish manually in Vanilla."
        )
    if not any(method == m and path.startswith(p) for m, p in ALLOWED):
        sys.exit(f"REFUSED: {method} {path} is not an allowed operation.")


def call(method: str, path: str, params: dict | None = None, payload: dict | None = None):
    guard(method, path)
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token()}",
            "User-Agent": UA,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()[:900]
        sys.exit(f"HTTP {exc.code} on {method} {path}\n{body}")


def to_markdown(html: str) -> str:
    try:
        import html2text
    except ImportError:
        sys.exit("Install html2text first:  python3 -m pip install --user html2text")
    conv = html2text.HTML2Text()
    conv.body_width = 0
    conv.protect_links = True
    return conv.handle(html or "").strip()


# ── read commands ────────────────────────────────────────────────────────────

def cmd_kbs(args):
    for kb in call("GET", "/knowledge-bases", {"limit": 100}):
        print(f"{kb.get('knowledgeBaseID'):>4}  {kb.get('name')}")


def cmd_categories(args):
    cats, page = [], 1
    while page <= 20:
        batch = call("GET", "/knowledge-categories",
                     {"limit": 100, "page": page, "expand": "knowledgeBase"})
        if not batch:
            break
        cats.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    def kb_of(cat):
        return (cat.get("knowledgeBase") or {}).get("knowledgeBaseID") or cat.get("knowledgeBaseID")

    if args.kb:
        cats = [c for c in cats if kb_of(c) == args.kb]
    by_id = {c["knowledgeCategoryID"]: c for c in cats}

    def crumb(cat):
        parts, parent, seen = [cat.get("name")], cat.get("parentID"), set()
        while parent and parent not in (-1, 0) and parent in by_id and parent not in seen:
            seen.add(parent)
            parts.append(by_id[parent].get("name"))
            parent = by_id[parent].get("parentID")
        return " > ".join(reversed(parts))

    for cat in sorted(cats, key=crumb):
        print(f"{cat['knowledgeCategoryID']:>5}  kb={kb_of(cat)}  {crumb(cat)}")


def cmd_search(args):
    params = {"query": args.query, "recordTypes[]": "article", "limit": args.limit}
    if args.kb:
        params["knowledgeBaseID"] = args.kb
    results = call("GET", "/search", params)
    results = results if isinstance(results, list) else results.get("results", [])
    if not results:
        print("No articles found.")
        return
    for item in results:
        aid = item.get("articleID") or item.get("recordID")
        print(f"{aid:>6}  {item.get('name')}")
        print(f"        {(item.get('url') or '').split('?')[0]}")


def cmd_get(args):
    art = call("GET", f"/articles/{args.article_id}")
    body = to_markdown(art.get("body") or art.get("bodyRendered") or "")
    doc = (
        f"# {art.get('name')}\n\n"
        f"- Article ID: {art.get('articleID')}\n"
        f"- URL: {(art.get('url') or '').split('?')[0]}\n"
        f"- Knowledge base / category: {art.get('knowledgeBaseID')} / {art.get('knowledgeCategoryID')}\n"
        f"- Status: {art.get('status')}\n"
        f"- Last updated: {art.get('dateUpdated')}\n\n---\n\n{body}\n"
    )
    if args.out:
        Path(args.out).write_text(doc)
        print(f"Wrote {args.out} ({len(doc)} chars)")
    else:
        print(doc)


def cmd_drafts(args):
    drafts = call("GET", "/drafts", {"limit": 50, "recordType": "article"})
    if not drafts:
        print("No article drafts.")
        return
    for d in drafts:
        attrs = d.get("attributes") or {}
        print(f"draftID={d.get('draftID')}  status={d.get('draftStatus')}  "
              f"article={d.get('recordID')}  {attrs.get('name')!r}")
        print(f"        {d.get('editUrl') or d.get('permaLink') or ''}")


# ── draft commands ───────────────────────────────────────────────────────────

PLACEHOLDERS = ("[SCREENSHOT NEEDED]", "[VIDEO NEEDED]", "TODO (verify)")


def scan_placeholders(body: str):
    """Return (line_number, marker, line) for every unresolved review marker."""
    hits = []
    for num, line in enumerate(body.splitlines(), 1):
        for marker in PLACEHOLDERS:
            if marker in line:
                hits.append((num, marker, line.strip()))
    return hits


def cmd_check(args):
    hits = scan_placeholders(Path(args.file).read_text())
    if not hits:
        print(f"{args.file}: clean — no unresolved media callouts or TODOs.")
        return
    print(f"{args.file}: {len(hits)} unresolved marker(s)\n")
    for num, marker, line in hits:
        print(f"  line {num:>4}  {marker}")
        print(f"            {line[:140]}")
    print("\nResolve these before staging, or pass --allow-placeholders to stage anyway.")


def read_body(path: str, allow_placeholders: bool = False) -> str:
    body = Path(path).read_text().strip()
    if not body:
        sys.exit(f"{path} is empty; Vanilla requires a non-empty body.")
    hits = scan_placeholders(body)
    if hits and not allow_placeholders:
        summary = "\n".join(f"  line {n}: {m}" for n, m, _ in hits)
        sys.exit(
            f"BLOCKED: {path} still has {len(hits)} unresolved review marker(s):\n{summary}\n\n"
            "Add the screenshots/video and resolve the TODOs, or re-run with "
            "--allow-placeholders to stage anyway (e.g. when adding visuals in the Vanilla editor)."
        )
    if hits:
        print(f"WARNING: staging with {len(hits)} unresolved marker(s) still in the body.")
    return body


def report(draft, article_id=None):
    draft_id = draft.get("draftID")
    url = draft.get("editUrl")
    if not url:
        url = (f"{SITE}/kb/articles/{article_id}/editor?draftID={draft_id}"
               if article_id else f"{SITE}/kb/articles/add?draftID={draft_id}")
    print(f"Draft staged. draftID={draft_id}  status={draft.get('draftStatus')}")
    print(f"Review and publish here: {url}")
    print("Nothing is live. This tool cannot publish — publish manually in Vanilla after review.")


def cmd_draft_new(args):
    attrs = {
        "name": args.title,
        "body": read_body(args.file, args.allow_placeholders),
        "format": args.format,
        "knowledgeCategoryID": args.category_id,
    }
    if args.kb:
        attrs["knowledgeBaseID"] = args.kb
    report(call("POST", "/drafts", payload={"recordType": "article", "attributes": attrs}))


def cmd_draft_update(args):
    live = call("GET", f"/articles/{args.article_id}")
    attrs = {
        "name": args.title or live.get("name"),
        "body": read_body(args.file, args.allow_placeholders),
        "format": args.format,
        "knowledgeCategoryID": args.category_id or live.get("knowledgeCategoryID"),
        "knowledgeBaseID": live.get("knowledgeBaseID"),
    }
    draft = call("POST", "/drafts", payload={
        "recordType": "article",
        "recordID": args.article_id,
        "attributes": attrs,
    })
    report(draft, args.article_id)


def cmd_delete_draft(args):
    call("DELETE", f"/drafts/{args.draft_id}")
    print(f"Deleted draft {args.draft_id}.")


# ── cli ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("kbs", help="list knowledge bases").set_defaults(func=cmd_kbs)

    p = sub.add_parser("categories", help="list categories with IDs")
    p.add_argument("--kb", type=int)
    p.set_defaults(func=cmd_categories)

    p = sub.add_parser("search", help="search articles")
    p.add_argument("query")
    p.add_argument("--kb", type=int)
    p.add_argument("--limit", type=int, default=15)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("get", help="fetch a live article as markdown")
    p.add_argument("article_id", type=int)
    p.add_argument("--out")
    p.set_defaults(func=cmd_get)

    sub.add_parser("drafts", help="list your article drafts").set_defaults(func=cmd_drafts)

    p = sub.add_parser("check", help="lint a review draft for unresolved callouts and TODOs")
    p.add_argument("file")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("draft-new", help="stage a brand-new article as a draft")
    p.add_argument("--title", required=True)
    p.add_argument("--category-id", type=int, required=True)
    p.add_argument("--file", required=True, help="markdown file holding the body")
    p.add_argument("--kb", type=int)
    p.add_argument("--format", default="markdown", choices=["markdown", "html", "rich2", "text"])
    p.add_argument("--allow-placeholders", action="store_true",
                   help="stage even with unresolved media callouts or TODOs")
    p.set_defaults(func=cmd_draft_new)

    p = sub.add_parser("draft-update", help="stage a new version of an existing article")
    p.add_argument("article_id", type=int)
    p.add_argument("--file", required=True, help="markdown file holding the new body")
    p.add_argument("--title")
    p.add_argument("--category-id", type=int)
    p.add_argument("--format", default="markdown", choices=["markdown", "html", "rich2", "text"])
    p.add_argument("--allow-placeholders", action="store_true",
                   help="stage even with unresolved media callouts or TODOs")
    p.set_defaults(func=cmd_draft_update)

    p = sub.add_parser("delete-draft", help="remove a draft you staged")
    p.add_argument("draft_id", type=int)
    p.set_defaults(func=cmd_delete_draft)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
