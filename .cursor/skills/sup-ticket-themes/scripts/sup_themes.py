"""Classify SUP tickets into themes and associate non-SUP PHEM items with each theme.

Inputs (local JSON written from read-only Jira queries, see SKILL.md):
  sup-crm-*.json            SUP tickets per area, created on or after 2026-01-01
  phem-crm-*-2026.json      PHEM Initiative / Epic / Story per area, created on or after 2026-01-01
  phem-linked-from-sup.json PHEM Initiative / Epic / Story keys found in SUP issuelinks

Two association methods, reported separately:
  linked  - a SUP ticket in the theme has an issuelink to the PHEM item.
  title   - the PHEM item's title matches PHEM_RULES for the theme (same area pool);
            a Story with no direct match inherits its parent Epic's themes.
Done, Blocked and pre-2026 PHEM items are removed and counted. Engineering-only
items map only to ENGINEERING_EXEMPT themes.

CLI:
  python3 sup_themes.py --sup-dir <dir> [--dump-unclassified out.tsv]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "servicenow-service-requests" / "scripts"))

from sup_theme_rules import (  # noqa: E402
    AREA_OF_PRODUCT2, AREAS, ENGINEERING_EXEMPT, LINKED_FILE, PHEM_EXCLUDE, PHEM_FILES,
    PHEM_RULES, SUP_FILES, SUP_RULES, UNCLASSIFIED,
)
from theme_jira_map import is_engineering  # noqa: E402

CREATED_FROM = "2026-01-01"
DELIVERY_TYPES = {"Initiative", "Epic", "Story"}
_REDACTED = re.compile(r"\[(email|phone)\]")

_SUP = {a: [(t, [re.compile(p, re.I) for p in pats]) for t, pats in rules] for a, rules in SUP_RULES.items()}
_PHEM = {a: [(t, [re.compile(p, re.I) for p in pats]) for t, pats in rules.items()] for a, rules in PHEM_RULES.items()}


def classify(area: str, summary: str) -> tuple[str, str]:
    """Return (theme, matched text) from the SUP summary only.

    Descriptions are not used: on a sample of description-only matches most were wrong
    (boilerplate words such as "see", "status", "email" dominate free text).
    """
    text = _REDACTED.sub(" ", summary or "")
    for theme, pats in _SUP[area]:
        for p in pats:
            m = p.search(text)
            if m:
                return theme, m.group(0).strip()
    return UNCLASSIFIED, ""


def load_sup(sup_dir: Path, include_done: bool = False) -> tuple[dict[str, list[dict]], dict]:
    """Tickets per area; Done-category tickets (Done, Closed, In Prod) are dropped and counted unless include_done."""
    by_area: dict[str, list[dict]] = {a: [] for a in AREAS}
    meta = {"files": {}, "jql": {}, "fetched": Counter(), "done_removed": {a: Counter() for a in AREAS}}
    for area, files in SUP_FILES.items():
        seen = set()
        for name in files:
            d = json.loads((sup_dir / name).read_text())
            if d["count"] != d["expected"] or len(d["issues"]) != d["expected"]:
                sys.exit(f"{name}: {len(d['issues'])} issues, expected {d['expected']}")
            meta["files"][name] = d["count"]
            meta["jql"].setdefault(area, []).append(d["jql"])
            meta["fetched_on"] = d.get("fetched_on")
            for r in d["issues"]:
                if r["key"] in seen:
                    continue
                seen.add(r["key"])
                meta["fetched"][area] += 1
                if not include_done and r.get("statusCategory") == "Done":
                    meta["done_removed"][area][r.get("status") or "Done"] += 1
                    continue
                theme, ev = classify(area, r["summary"])
                by_area[area].append({**r, "theme": theme, "evidence": ev})
    return by_area, meta


def load_phem(sup_dir: Path) -> dict[str, dict[str, dict]]:
    pool: dict[str, dict[str, dict]] = {a: {} for a in AREAS}
    for name in PHEM_FILES:
        for it in json.loads((sup_dir / name).read_text())["issues"]:
            area = AREA_OF_PRODUCT2.get(it.get("area"))
            if area and it["type"] in DELIVERY_TYPES:
                pool[area][it["key"]] = it
    return pool


def load_linked(sup_dir: Path) -> dict[str, dict]:
    d = json.loads((sup_dir / LINKED_FILE).read_text())
    cols = d["fields"]
    return {row[0]: dict(zip(cols, row)) for row in d["issues"]}


def removed_reason(it: dict) -> str | None:
    if (it.get("created") or "")[:10] < CREATED_FROM:
        return "before"
    if (it.get("status") or "").lower() == "blocked":
        return "blocked"
    if it.get("statusCategory") == "Done":
        return "done"
    return None


def _allows(area: str, theme: str, it: dict) -> bool:
    if theme not in ENGINEERING_EXEMPT and is_engineering(it):
        return False
    ex = PHEM_EXCLUDE.get(area, {}).get(theme)
    return not (ex and re.search(ex, it["summary"], re.I))


def title_map(area: str, items: dict[str, dict]) -> dict[str, dict[str, dict]]:
    """{theme: {key: {"how": "direct"|"via epic", "evidence": str}}} for one area pool."""
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    direct: dict[str, dict[str, str]] = {}
    for k, it in items.items():
        hits = {}
        for theme, pats in _PHEM[area]:
            if not _allows(area, theme, it):
                continue
            for p in pats:
                m = p.search(it["summary"])
                if m:
                    hits[theme] = m.group(0).strip()
                    break
        if hits:
            direct[k] = hits
            for t, ev in hits.items():
                out[t][k] = {"how": "direct", "evidence": ev}
    for k, it in items.items():
        p = it.get("parent")
        if it["type"] != "Story" or k in direct or p not in direct or items[p]["type"] != "Epic":
            continue
        for t in direct[p]:
            if _allows(area, t, it):
                out[t][k] = {"how": "via epic", "evidence": items[p]["summary"]}
    return out


def analyse(sup_dir: Path, include_done: bool = False) -> dict:
    """Everything the HTML tab and the CLI need, per area."""
    for area in AREAS:
        diff = {t for t, _ in SUP_RULES[area]} ^ set(PHEM_RULES[area])
        if diff:
            sys.exit(f"{area}: SUP_RULES and PHEM_RULES themes differ: {sorted(diff)}")
    sup, meta = load_sup(sup_dir, include_done)
    pool_all = load_phem(sup_dir)
    linked_items = load_linked(sup_dir)
    areas = {}
    for area in AREAS:
        all_items = pool_all[area]
        removed = {k: r for k, it in all_items.items() if (r := removed_reason(it))}
        kept = {k: it for k, it in all_items.items() if k not in removed}
        mapped_all = title_map(area, all_items)
        mapped = title_map(area, kept)
        tickets = sup[area]
        themes = Counter(r["theme"] for r in tickets)
        linked: dict[str, dict[str, dict]] = defaultdict(dict)
        linked_removed: dict[str, Counter] = defaultdict(Counter)
        linked_other_types: dict[str, Counter] = defaultdict(Counter)
        for r in tickets:
            for l in r["links"]:
                if not l["key"].startswith("PHEM-"):
                    continue
                if l["issuetype"] not in DELIVERY_TYPES:
                    linked_other_types[r["theme"]][l["issuetype"]] += 1
                    continue
                it = linked_items.get(l["key"]) or {
                    "key": l["key"], "type": l["issuetype"], "status": l["status"],
                    "statusCategory": l["statusCategory"], "summary": l["summary"], "created": "",
                }
                reason = removed_reason(it)
                if reason:
                    linked_removed[r["theme"]][(reason, l["key"])] += 1
                    continue
                entry = linked[r["theme"]].setdefault(l["key"], {**it, "sup": [], "in_pool": l["key"] in all_items})
                entry["sup"].append((r["key"], l["rel"]))
        names = list(dict.fromkeys(name for name, _ in SUP_RULES[area]))
        order = sorted(
            (t for t in names + [UNCLASSIFIED] if themes[t]),
            key=lambda t: (t == UNCLASSIFIED, -themes[t]),
        )
        areas[area] = {
            "tickets": tickets,
            "themes": themes,
            "order": order,
            "empty": [name for name in names if not themes[name]],
            "pool_total": len(all_items),
            "pool_kept": kept,
            "removed": removed,
            "removed_counts": Counter(removed.values()),
            "mapped": mapped,
            "mapped_all": mapped_all,
            "linked": linked,
            "linked_removed": {t: Counter(reason for reason, _ in c) for t, c in linked_removed.items()},
            "linked_other_types": linked_other_types,
            "engineering": sum(1 for it in kept.values() if is_engineering(it)),
            "request_types": Counter(r.get("request_type") or "Not set" for r in tickets),
            "status": Counter(r.get("statusCategory") or "Not set" for r in tickets),
        }
    return {"areas": areas, "meta": meta}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sup-dir", required=True)
    ap.add_argument("--dump-unclassified", default="")
    ap.add_argument("--area", default="")
    ap.add_argument("--include-done", action="store_true", help="keep Done-category SUP tickets")
    args = ap.parse_args()
    res = analyse(Path(args.sup_dir), args.include_done)
    for area, a in res["areas"].items():
        if args.area and area != args.area:
            continue
        n = len(a["tickets"])
        unc = a["themes"][UNCLASSIFIED]
        done = dict(res["meta"]["done_removed"][area])
        print(f"\n== {area}: {n} open SUP tickets of {res['meta']['fetched'][area]} fetched "
              f"(Done removed: {done}), {unc} unclassified ({unc/n*100:.1f}%)")
        print(f"   PHEM pool {a['pool_total']}, open {len(a['pool_kept'])}, removed {dict(a['removed_counts'])}, engineering {a['engineering']}")
        for t in a["order"]:
            tm = a["mapped"].get(t, {})
            types = Counter(a["pool_kept"][k]["type"] for k in tm)
            print(f"  {a['themes'][t]:5d}  {t}  | title I{types['Initiative']} E{types['Epic']} S{types['Story']}"
                  f" | linked {len(a['linked'].get(t, {}))}")
    if args.dump_unclassified:
        with open(args.dump_unclassified, "w") as fh:
            for area, a in res["areas"].items():
                for r in a["tickets"]:
                    if r["theme"] == UNCLASSIFIED:
                        fh.write(f"{area}\t{r['key']}\t{r['summary']}\n")


if __name__ == "__main__":
    main()
