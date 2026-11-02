#!/usr/bin/env python3
"""
format_docs.py — Push local FRD markdown into Google Docs with REAL heading styles.

Why this exists
---------------
The Google MCP tools (`create_google_doc` / `update_google_doc`) only insert PLAIN
TEXT — they cannot apply Google Docs paragraph styles, so markdown like `#`, `##`,
`###` shows up as literal characters. This script bypasses that limitation by calling
the Google Docs API `batchUpdate` endpoint directly (the same endpoint + OAuth token
the MCP already uses), clearing each doc and re-applying native Heading 1/2/3 styles
and bullet lists from the local `specs/<slug>/frd.md` source files.

Source of truth = the local `specs/<slug>/frd.md` files. Edit those, then re-run
this script to sync the Google Docs.

Prerequisites
-------------
- The Google ("copilot") MCP must be connected in Cursor so a valid token exists at
  ~/.copilot/tokens.json (this script auto-refreshes it via the backend if near expiry).
- Network access to docs.googleapis.com (and the backend for refresh).

Usage
-----
    python3 tools/format_docs.py            # DRY RUN: parse + report, no changes
    python3 tools/format_docs.py --apply    # APPLY: clear + restyle all docs
    python3 tools/format_docs.py --apply --only my-jobs-role-filtering   # one spec

Markdown supported per line: `# / ## / ### / ####` headings, `- ` / `* ` bullets,
`> ` quotes (rendered as normal text), everything else = normal paragraph.
Inline `**bold**` / backticks are stripped (this MCP/script does not style inline runs).
Markdown tables are NOT supported — express tabular data as bullet lists.
"""
import json, os, sys, time, urllib.request, urllib.error

TOKENS = os.path.expanduser("~/.copilot/tokens.json")
BACKEND = "https://product-copilot-backend-iarivxijkq-uc.a.run.app"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(REPO, "specs", "{}", "frd.md")

# slug -> Google Doc ID. Keep in sync with specs/README.md.
DOCS = [
    ("recruiter-roles-data-model",    "1HQqfX4aR9kOPc8Z_ApH8bLSrkgP0FSK_c_Xm4lPvTEA"),
    ("hiring-team-role-assignment",   "1UrjQCiu5g1YrB9yduuVQvi3QXx81naLZw9-2MlD2uZU"),
    ("role-aware-notifications",      "1kU5MFejItwYW596qV4jnw_AgSjADWbV0kDTJl4KGJR8"),
    ("my-jobs-role-filtering",        "17g42IWQRGc80LNpq10RcsLnKfmHOpBHLy8QC35YL2zA"),
    ("per-role-analytics",            "1hp-8tITLRo7q6E9lvFFplxB568RNECNJ5SnbccLDi98"),
    ("role-aware-automation-recipes", "1k4q4KnczzpbJsmP0YuBXTiMNXaMyDHnJzrX2HEU93II"),
]

DRY = "--apply" not in sys.argv
ONLY = None
if "--only" in sys.argv:
    i = sys.argv.index("--only")
    if i + 1 < len(sys.argv):
        ONLY = sys.argv[i + 1]


def u16(s):
    """UTF-16 code-unit length (Google Docs indexes are UTF-16 offsets)."""
    return len(s.encode("utf-16-le")) // 2


def strip_inline(t):
    return t.replace("**", "").replace("__", "").replace("`", "")


def parse_md(md):
    paras = []  # (kind, text)
    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        s = line.lstrip()
        if s.startswith("#### "):
            paras.append(("HEADING_4", strip_inline(s[5:]).strip()))
        elif s.startswith("### "):
            paras.append(("HEADING_3", strip_inline(s[4:]).strip()))
        elif s.startswith("## "):
            paras.append(("HEADING_2", strip_inline(s[3:]).strip()))
        elif s.startswith("# "):
            paras.append(("HEADING_1", strip_inline(s[2:]).strip()))
        elif s.startswith("- ") or s.startswith("* "):
            paras.append(("BULLET", strip_inline(s[2:]).strip()))
        elif s.startswith("> "):
            paras.append(("NORMAL", strip_inline(s[2:]).strip()))
        else:
            paras.append(("NORMAL", strip_inline(s).strip()))
    return paras


def build_requests(paras):
    full = ""
    spans = []
    cursor = 1
    for kind, text in paras:
        start = cursor
        full += text + "\n"
        seg = u16(text)
        spans.append((start, start + seg + 1, kind))
        cursor += seg + 1
    reqs = [{"insertText": {"location": {"index": 1}, "text": full}}]
    for start, end, kind in spans:
        if kind.startswith("HEADING"):
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {"namedStyleType": kind},
                "fields": "namedStyleType"}})
        elif kind == "BULLET":
            reqs.append({"createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    return reqs, full


def get_token():
    d = json.load(open(TOKENS))
    g = d["google"]
    exp = g.get("token_expires_at")
    need = False
    if exp:
        try:
            t = time.strptime(exp.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            if time.mktime(t) - time.mktime(time.gmtime()) < 120:
                need = True
        except Exception:
            pass
    if need and d.get("backend_jwt"):
        try:
            req = urllib.request.Request(
                f"{BACKEND}/integrations/refresh/google", method="POST",
                headers={"Authorization": "Bearer " + d["backend_jwt"]})
            r = json.load(urllib.request.urlopen(req, timeout=30))
            g["access_token"] = r["access_token"]
            print("  (token refreshed)")
        except Exception as e:
            print("  (refresh failed, using existing token):", e)
    return g["access_token"]


def api(method, url, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def process(token, slug, doc_id):
    md = open(BASE.format(slug)).read()
    paras = parse_md(md)
    reqs, full = build_requests(paras)
    counts = {k: sum(1 for kk, _ in paras if kk == k) for k in
              ("HEADING_1", "HEADING_2", "HEADING_3", "BULLET")}
    print(f"[{slug}] paras={len(paras)} H1={counts['HEADING_1']} "
          f"H2={counts['HEADING_2']} H3={counts['HEADING_3']} "
          f"bullets={counts['BULLET']} chars={u16(full)}")
    if DRY:
        return
    doc = api("GET", f"https://docs.googleapis.com/v1/documents/{doc_id}", token)
    end = doc["body"]["content"][-1]["endIndex"]
    if end - 1 > 1:
        api("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", token,
            {"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end - 1}}}]})
    api("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", token,
        {"requests": reqs})
    print(f"  -> OK styled https://docs.google.com/document/d/{doc_id}/edit")


def main():
    targets = [(s, d) for s, d in DOCS if (ONLY is None or s == ONLY)]
    if not targets:
        print(f"No spec matches --only {ONLY}. Known: {[s for s,_ in DOCS]}")
        return
    token = None if DRY else get_token()
    for slug, doc_id in targets:
        try:
            process(token, slug, doc_id)
        except urllib.error.HTTPError as e:
            print(f"[{slug}] HTTP {e.code}: {e.read().decode()[:300]}")
        except Exception as e:
            print(f"[{slug}] ERROR: {e}")


if __name__ == "__main__":
    print("MODE:", "DRY-RUN (no changes)" if DRY else "APPLYING CHANGES")
    main()
