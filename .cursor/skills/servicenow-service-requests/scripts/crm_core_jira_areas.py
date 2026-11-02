"""Map CRM Core Jira items (Initiative / Epic / Story) to the six CRM Core areas.

Input: raw Jira search pages saved under
product-copilot-beta/knowledge/servicenow-service-requests/data/crm-core-jira/
(page*.json from searchJiraIssuesUsingJql, context-parents.json for parents
outside the filter). Jira is read-only; nothing here writes to Jira.

Classification is exclusive and title-only:
  1. jira_v1 phrases (Jira feature wording) in AREA order
  2. the six areas' ServiceNow phrase rules from rx_theme_rules (base,
     cluster_v1, cluster_v2) in AREA order
  3. if still unmatched, inherit the nearest classified ancestor's area
  4. otherwise "Not in the six areas"
Descriptions are not matched: Jira story templates carry boilerplate
("Out of scope: Permissions…", "Considerations: Localization…") that
produces false hits.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from rx_theme_rules import all_theme_rules  # noqa: E402
from crm_core_jira_summaries import AREA_SUMMARIES  # noqa: E402
from crm_core_jira_timeline import annotate as annotate_timeline  # noqa: E402

REPO = SCRIPT_DIR.parents[3]
KNOW = REPO / "product-copilot-beta/knowledge/servicenow-service-requests"
DATA = KNOW / "data/crm-core-jira"
SNAPSHOT = KNOW / "snapshot-crm-core-jira-areas.json"

JQL = (
    'project = PHEM AND "Product Experience: Product2[Dropdown]" = '
    '"Recruiter Experience (RX) - CRM - Core" AND type IN (Epic, Initiative, Story) '
    'AND created >= 2026-01-01 AND status NOT IN (Done, Blocked, "In QA", '
    '"PM Acceptance Queue")'
)
EXPECTED_TOTAL = 308

# Items whose title or description mentions metadata are removed from the
# analysis, together with every descendant of a title match.
EXCLUDE_RX = re.compile(r"\bmeta[\s-]?data", re.I)

from crm_core_jira_areas_names import (  # noqa: E402
    ACC,
    AREAS,
    EVT,
    HOW,
    HS,
    JOB,
    NOT_IN_SIX,
    SYNC,
)

# Jira feature wording. Evaluated in this list order (not AREAS order) so that
# integration, access and enablement wording wins over generic "job" titles.
JIRA_V1_RULES: list[tuple[str, list[str]]] = [
    (
        SYNC,
        [
            r"\blinkedin\b",
            r"\binmail\b",
            r"\bworkday\b",
            r"\bsuccessfactors\b",
            r"\bats\b",
            r"\bjob sync\b",
            r"\bsync(ed|ing)?\b",
            r"\bhrm\s*(<>|↔|and|to)\s*crm\b",
            r"\bcrm\s*(<>|↔|and|to)\s*hrm\b",
            r"\bix and crm\b",
            r"\b(adp|hcm|erm)\b",
            r"\bindeed integration\b",
        ],
    ),
    (
        ACC,
        [
            r"\brbac\b",
            r"\bcbac\b",
            r"\broles?\b",
            r"\bpermissions?\b",
            r"\brestrict",
            r"\baccess\b",
            r"\bdep(a)?r(t)?(e)?m(e)?n(a)?t(a)?li[sz]ation\b",
            r"\bdepartmentali[sz]ed\b",
            r"\bauto-provisioning\b",
            r"\bforced logout\b",
            r"\bworker council\b",
            r"\blead visibility\b",
            r"\bvisibility\b.{0,40}\bconsent\b",
            r"\bprivacy segmentation\b",
            r"\bauthorization\b",
        ],
    ),
    (
        EVT,
        [
            r"\bevents? (module|candidate|registration)\b",
            r"\bcareer fair\b",
            r"\buniversity\b",
            r"\bcampus\b",
        ],
    ),
    (
        HOW,
        [
            r"\bfeature flag\b",
            r"\bself-servic",
            r"\berror (messages?|improvements?)\b",
            r"\btenant (provisioning|centralization)\b",
            r"\bprovisioning flow\b",
        ],
    ),
    (
        HS,
        [
            r"\bhiring status",
            r"\bhiring pipeline\b",
            r"\bleads?\b",
            r"\bapplicants?\b",
            r"\bjob stage\b",
        ],
    ),
    (
        JOB,
        [
            r"\bjobs?\b",
            r"\bjob(details|postings?)\b",
            r"\brequisitions?\b",
            r"\breq templates?\b",
            r"\bposting\b",
            r"\bposted\b",
            r"\b(un)?publish(ing)?\b",
            r"\bexpir(y|ing|e)\b",
            r"\bcareer site\b",
            r"\bapplications?\b",
            r"\bintake\b",
            r"\breddot\b",
        ],
    ),
    (
        HOW,
        [
            r"\bsettings?\b",
            r"\bfield management\b",
            r"\bconfigur(e|ation|ations)\b",
        ],
    ),
]

# (area, pattern): a title matching the pattern may not take that area from
# any rule. Guards against generic words used in a non-recruiting sense.
BLOCK_RULES: list[tuple[str, str]] = [
    (HS, r"\bvalidation pipeline\b"),
    (JOB, r"\bjob executive presentation\b"),
    (JOB, r"\bapplication constant\b"),
    (JOB, r"\bcandidate purge\b"),
    (JOB, r"\bsdui\b"),
    (JOB, r"^publish draft$"),
    (JOB, r"\bfilter notes\b"),
    (SYNC, r"\bcustom job statuses\b"),
    (HOW, r"\bremote\b"),
    (HOW, r"\bwidgets and custom blocks\b"),
]


def _compile(rules):
    return [(a, [re.compile(p, re.I) for p in pats]) for a, pats in rules]


_JIRA_V1 = _compile(JIRA_V1_RULES)
_SR_SIX = sorted(
    _compile([(t, p) for t, p in all_theme_rules() if t in AREAS]),
    key=lambda x: AREAS.index(x[0]),
)
_BLOCK = [(a, re.compile(p, re.I)) for a, p in BLOCK_RULES]


def _blocked(area: str, title: str) -> bool:
    return any(a == area and rx.search(title) for a, rx in _BLOCK)


def classify_title(title: str) -> tuple[str | None, str, str]:
    """Return (area or None, source, matched pattern)."""
    for source, layer in (("jira_v1", _JIRA_V1), ("servicenow_rules", _SR_SIX)):
        for area, regs in layer:
            if _blocked(area, title):
                continue
            for rx in regs:
                if rx.search(title):
                    return area, source, rx.pattern
    return None, "", ""


def _type_letter(t: str) -> str:
    return {"Initiative": "I", "Epic": "E", "Story": "S"}.get(t, t[:1])


def load_items() -> tuple[dict, dict]:
    items: dict[str, dict] = {}
    for page in sorted(DATA.glob("page*.json")):
        d = json.loads(page.read_text())
        d = d.get("data", d)
        for i in d["issues"]:
            f = i["fields"]
            par = f.get("parent") or {}
            items[i["key"]] = {
                "key": i["key"],
                "type": f["issuetype"]["name"],
                "status": f["status"]["name"],
                "summary": " ".join(f["summary"].split()),
                "created": (f.get("created") or "")[:10],
                "parent": par.get("key"),
                "_description": f.get("description") or "",
            }
    ctx_raw = json.loads((DATA / "context-parents.json").read_text())["issues"]
    context = {
        k: {
            "key": k,
            "type": v["type"],
            "status": v["status"],
            "summary": " ".join(v["summary"].split()),
            "parent": v.get("parent"),
            "context": True,
        }
        for k, v in ctx_raw.items()
        if k not in items
    }
    return items, context


def exclude_metadata(items: dict, context: dict) -> list[dict]:
    """Drop metadata items from `items` in place; return what was removed.

    Kept items whose parent was removed are re-attached to their nearest
    remaining ancestor, so trees and area inheritance skip removed items.
    """
    reason: dict[str, str] = {}
    for k, n in items.items():
        if EXCLUDE_RX.search(n["summary"]):
            reason[k] = "metadata in title"
        elif EXCLUDE_RX.search(n["_description"]):
            reason[k] = "metadata in description"

    title_hits = {k for k, r in reason.items() if r == "metadata in title"}
    changed = True
    while changed:
        changed = False
        for k, n in items.items():
            p = n.get("parent")
            if k not in reason and p in reason and (p in title_hits or reason[p].startswith("under ")):
                reason[k] = f"under {p}"
                changed = True

    nodes = {**context, **items}

    def kept_ancestor(p):
        while p in reason:
            p = nodes[p].get("parent")
        return p

    removed = []
    for k in list(items):
        if k in reason:
            n = items.pop(k)
            removed.append({"key": k, "type": n["type"], "status": n["status"],
                            "summary": n["summary"], "reason": reason[k]})
    for n in items.values():
        n["parent"] = kept_ancestor(n.get("parent"))
        n.pop("_description", None)
    return sorted(removed, key=lambda r: (r["reason"].startswith("under"), r["key"]))


def classify_all(items: dict, context: dict) -> dict:
    nodes = {**context, **items}
    direct = {k: classify_title(n["summary"]) for k, n in nodes.items()}

    def inherited(key: str, seen: set) -> tuple[str | None, str]:
        p = nodes.get(key, {}).get("parent")
        while p and p in nodes and p not in seen:
            seen.add(p)
            area = direct[p][0]
            if area:
                return area, p
            p = nodes[p].get("parent")
        return None, ""

    for k, n in nodes.items():
        area, source, pattern = direct[k]
        if area:
            n.update(area=area, source=source, pattern=pattern)
            continue
        area, via = inherited(k, {k})
        if area:
            n.update(area=area, source="inherited", pattern=f"from {via}")
        else:
            n.update(area=NOT_IN_SIX, source="unmatched", pattern="")
    return nodes


def build_snapshot() -> dict:
    items, context = load_items()
    if len(items) != EXPECTED_TOTAL:
        raise SystemExit(f"Expected {EXPECTED_TOTAL} Jira items, loaded {len(items)}")
    excluded = exclude_metadata(items, context)
    nodes = classify_all(items, context)
    counted = [nodes[k] for k in items]
    total = len(counted)
    if total + len(excluded) != EXPECTED_TOTAL:
        raise SystemExit("Kept + excluded items do not add up to the filter total")

    by_area = {a: Counter() for a in AREAS + [NOT_IN_SIX]}
    for n in counted:
        by_area[n["area"]][n["type"]] += 1
    if sum(sum(c.values()) for c in by_area.values()) != total:
        raise SystemExit("Area counts do not sum to the item total")

    missing = [a for a in AREAS if len(AREA_SUMMARIES.get(a, [])) != 3]
    if missing:
        raise SystemExit(f"Need exactly 3 summary bullets for: {missing}")

    snap = {
        "title": "CRM Core Jira items mapped to the six CRM Core areas",
        "jql": JQL,
        "run_date": date.today().isoformat(),
        "filter_total": EXPECTED_TOTAL,
        "excluded": excluded,
        "total": total,
        "type_totals": dict(Counter(n["type"] for n in counted)),
        "status_totals": dict(Counter(n["status"] for n in counted).most_common()),
        "areas": AREAS,
        "not_in_six": NOT_IN_SIX,
        "area_counts": {
            a: {
                "total": sum(c.values()),
                "Initiative": c.get("Initiative", 0),
                "Epic": c.get("Epic", 0),
                "Story": c.get("Story", 0),
            }
            for a, c in by_area.items()
        },
        "source_counts": dict(Counter(n["source"] for n in counted)),
        "summaries": {a: AREA_SUMMARIES.get(a, []) for a in AREAS},
        "nodes": nodes,
        "counted_keys": list(items),
    }
    annotate_timeline(snap, DATA, AREAS + [NOT_IN_SIX])
    return snap


def main() -> None:
    snap = build_snapshot()
    SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False, indent=1))
    print(f"Wrote {SNAPSHOT.relative_to(REPO)}  total={snap['total']}")
    for a in AREAS + [NOT_IN_SIX]:
        c = snap["area_counts"][a]
        print(f"  {c['total']:>3}  I{c['Initiative']:>2} E{c['Epic']:>3} S{c['Story']:>3}  {a}")
    print("  sources:", snap["source_counts"])
    tl = snap["timeline"]
    print(f"  timeline as of {tl['as_of']}  pace: "
          + ", ".join(f"{w['label']} {w['stories_per_month']}/mo" for w in tl["pace"]["windows"]))
    for a in AREAS + [NOT_IN_SIX, "overall"]:
        t = tl["overall"] if a == "overall" else tl["areas"][a]
        print(f"  P{t['planned']:>3} Sl{t['slipped']:>3} U{t['unplanned']:>3}  latest {t['latest_version'] or '-':>13} "
              f"({t['months'] if t['months'] is not None else '-'} mo)  stories {t['open_stories']:>3} "
              f"pace {t['pace_months']['low']}-{t['pace_months']['high']} mo  {a}")
    print("  target versions:", tl["target_version_counts"])
    if "--list" in sys.argv:
        for k in snap["counted_keys"]:
            n = snap["nodes"][k]
            print(f"{n['area'][:12]:12} | {n['source'][:9]:9} | {_type_letter(n['type'])} | {k} | {n['summary'][:90]} | {n['pattern'][:40]}")


if __name__ == "__main__":
    main()
