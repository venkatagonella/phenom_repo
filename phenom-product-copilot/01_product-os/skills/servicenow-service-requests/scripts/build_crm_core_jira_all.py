"""Build the all-items CRM Core area page.

Reads slice-*.json written from the Jira filter (any year, any status):
  project = PHEM AND Product2 = Recruiter Experience (RX) - CRM - Core
  AND type IN (Epic, Initiative, Story)

Does not modify the 2026-open snapshot or crm-core-jira-areas.html.
Jira is read-only; this script only reads local JSON.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_crm_core_jira_html import (  # noqa: E402
    CSS,
    PDS_TOKENS,
    esc,
    excluded_note,
    level_buttons,
    months_txt,
    render_tree,
    slug,
)
from crm_core_jira_areas import (  # noqa: E402
    AREAS,
    EXCLUDE_RX,
    NOT_IN_SIX,
    classify_all,
)
from crm_core_jira_timeline import months_between, version_target  # noqa: E402

REPO = SCRIPT_DIR.parents[3]  # repo root
# 01_product-os/knowledge/servicenow-service-requests (scripts live in 01_product-os/skills/<skill>/scripts)
KNOW = SCRIPT_DIR.parents[2] / "knowledge" / "servicenow-service-requests"
DATA = KNOW / "data/crm-core-jira-all"
OUT = KNOW / "crm-core-jira-areas-all.html"
SNAPSHOT = DATA / "snapshot-crm-core-jira-areas-all.json"

JQL = (
    'project = PHEM AND "Product Experience: Product2[Dropdown]" = '
    '"Recruiter Experience (RX) - CRM - Core" AND type IN (Epic, Initiative, Story)'
)
EXPECTED_TOTAL = 3078
AS_OF = date(2026, 10, 26)

# Hand-written area summaries. Filled after the first classification pass
# when the top initiative titles are known. Auto bullets are used until then.
SUMMARY_OVERRIDES: dict[str, list[str]] = {
    "Hiring status / pipeline / stages / lead status": [
        "No initiative sits in this area. Seven epics and 150 stories are about hiring status, the pipeline, leads and applicants. 60 are Done and 97 are still open.",
        "The Done work is mostly the action-items widgets for new applicants, new leads and AI-recommended leads.",
        "Still open: the hiring-pipeline backlog, and translating hiring status into the recruiter’s language (PHEM-2136326, Backlog).",
    ],
    "Jobs / requisitions / applications / posting": [
        "Five initiatives, 64 epics and 518 stories cover the job record, requisitions, posting and applications. 287 are Done and 300 are still open.",
        "Done initiatives include hiring-stage visibility on the jobs list. Large Done epics include the job-list workflow and the create-job page.",
        "Still open: job analytics and recommendations, the job activity view, RedDot distribution, linking projects and jobs, and job-details improvements.",
    ],
    "Forwarding / LinkedIn / ATS↔CRM sync": [
        "Two initiatives and 17 epics cover LinkedIn CRM Connect, Workday job sync and ATS job pull. 78 items are Done and 69 are still open.",
        "The open initiatives are LinkedIn CRM Connect (past its release, still To Do) and LinkedIn CRM Connectivity & Enhancements (a future release).",
        "Open epics also cover the IX job workflow, a role-aware ATS job pull, Workday create/publish/unpublish, and failure handling with manual retry.",
    ],
    "Access / CRM not opening / permissions": [
        "Two initiatives are Done: Departmentalization 2.0 and consent-based access. The area also has 36 epics and 160 stories. 89 items are Done and 109 are still open.",
        "Done work includes departmentalization customer commits, EEO data restriction, and an autoprovisioned events-user access fix.",
        "Still open: role-based visibility, RBAC limits on download and export, departmentalization, role-aware auto-provisioning, and worker-council lead access.",
    ],
    "Events / university recruiting": [
        "There is no initiative or epic for university or campus recruiting in this filter.",
        "Five stories matched the word event. Three are Done: a note-tag event, dashboard tracking events, and project-workflow events.",
        "Two are still open: renaming the candidate-list column to Event Registration Status, and selecting an Events block inside an automation.",
    ],
    "How-to / configuration / enablement question": [
        "Three initiatives, 22 epics and 137 stories cover feature flags, field management, settings and tenant setup. 86 are Done and 76 are still open.",
        "Done work includes partner-enablement feature flags, the CRM configuration service, and field management in RX.",
        "Still open: a common data model for field management, self-service error messages, the feature-flag revamp, and tenant centralization.",
    ],
}


def load_slices() -> dict[str, dict]:
    files = sorted(DATA.glob("slice-*.json"))
    if not files:
        raise SystemExit(f"No slice files in {DATA}")
    items: dict[str, dict] = {}
    for page in files:
        d = json.loads(page.read_text())
        for i in d["issues"]:
            items[i["key"]] = {
                "key": i["key"],
                "type": i["type"],
                "status": i["status"],
                "statusCategory": i.get("statusCategory") or "",
                "summary": " ".join((i.get("summary") or "").split()),
                "created": (i.get("created") or "")[:10],
                "parent": i.get("parent") or None,
                "versions": i.get("versions") or [],
            }
        print(f"  {page.name}: file count {d.get('count')} loaded keys so far {len(items)}")
    return items


def load_context() -> dict[str, dict]:
    path = DATA / "context-parents.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text())["issues"]
    return {
        k: {
            "key": k,
            "type": v["type"],
            "status": v["status"],
            "statusCategory": v.get("statusCategory") or "",
            "summary": " ".join(v["summary"].split()),
            "parent": v.get("parent"),
            "versions": v.get("versions") or [],
            "context": True,
        }
        for k, v in raw.items()
    }


def load_metadata_keys() -> set[str]:
    path = DATA / "metadata-keys.json"
    if not path.exists():
        return set()
    return set(json.loads(path.read_text())["keys"])


def exclude_metadata(items: dict, meta_keys: set[str]) -> list[dict]:
    reason: dict[str, str] = {}
    for k, n in items.items():
        if EXCLUDE_RX.search(n["summary"]):
            reason[k] = "metadata in title"
        elif k in meta_keys:
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

    parent_of = {k: n.get("parent") for k, n in items.items()}

    def kept_ancestor(p):
        seen = set()
        while p and p in reason and p not in seen:
            seen.add(p)
            p = parent_of.get(p)
        return p

    removed = []
    for k in list(reason):
        if k not in items:
            continue
        n = items.pop(k)
        n["parent"] = kept_ancestor(n.get("parent"))
        removed.append({
            "key": k, "type": n["type"], "status": n["status"],
            "summary": n["summary"], "reason": reason[k],
        })
    for n in items.values():
        n["parent"] = kept_ancestor(n.get("parent"))
    return sorted(removed, key=lambda r: (r["reason"].startswith("under"), r["key"]))


def is_done(n: dict) -> bool:
    return n.get("statusCategory") == "done" or n.get("status") == "Done"


def item_plan(n: dict) -> dict:
    versions = n.get("versions") or []
    names = [v.get("name") or "" for v in versions]
    targets = []
    for v in versions:
        t, basis = version_target(v.get("name") or "", v.get("release_date"))
        if t:
            targets.append((t, v.get("name") or "", basis))
    base = {
        "versions": names,
        "due": None,
        "story_points": None,
        "active_sprint": None,
    }
    if is_done(n):
        if targets:
            t, name, basis = max(targets)
            target, target_version, basis = t.isoformat(), name, basis
        else:
            target, target_version, basis = None, (names[0] if names else "Backlog"), "done"
        return {
            **base, "state": "done", "target": target, "target_version": target_version,
            "basis": basis, "months": None,
        }
    future = [x for x in targets if x[0] >= AS_OF]
    if future:
        t, name, basis = max(future)
        state, target, months = "planned", t.isoformat(), months_between(AS_OF, t)
    elif targets:
        t, name, basis = max(targets)
        state, target, months = "slipped", t.isoformat(), None
    else:
        name, basis, state, target, months = "Backlog", "backlog", "unplanned", None, None
    return {
        **base, "state": state, "target": target, "target_version": name,
        "basis": basis, "months": months,
    }


def rollup(plans: list[dict]) -> dict:
    counts = {"planned": 0, "slipped": 0, "unplanned": 0, "done": 0}
    latest = None
    for t in plans:
        counts[t["state"]] = counts.get(t["state"], 0) + 1
        if t["state"] == "planned" and t.get("target"):
            d = date.fromisoformat(t["target"])
            if latest is None or d > latest[0]:
                latest = (d, t["target_version"])
    return {
        **counts,
        "items": len(plans),
        "latest_target": latest[0].isoformat() if latest else None,
        "latest_version": latest[1] if latest else None,
        "months": months_between(AS_OF, latest[0]) if latest else None,
    }


def pace_range(stories: int, pace: dict) -> dict:
    rates = [w["stories_per_month"] for w in pace["windows"] if w["stories_per_month"]]
    if not rates or not stories:
        return {"low": 0.0, "high": 0.0}
    return {"low": round(stories / max(rates), 1), "high": round(stories / min(rates), 1)}


def _children_index(nodes: dict) -> dict[str, list[str]]:
    children: dict[str, list[str]] = {k: [] for k in nodes}
    for k, n in nodes.items():
        p = n.get("parent")
        if p in children:
            children[p].append(k)
    return children


def subtree_plans(k: str, children: dict, nodes: dict, seen: set) -> list[dict]:
    out = [nodes[k]["plan"]] if "plan" in nodes.get(k, {}) else []
    for c in children.get(k, []):
        if c not in seen:
            seen.add(c)
            out += subtree_plans(c, children, nodes, seen)
    return out


def auto_bullets(area: str, nodes: dict, counted: list[str], children: dict) -> list[str]:
    members = [nodes[k] for k in counted if nodes[k]["area"] == area]
    c = Counter(n["type"] for n in members)
    done = sum(1 for n in members if n["plan"]["state"] == "done")
    open_n = len(members) - done

    def weight(k: str) -> int:
        return sum(1 for p in subtree_plans(k, children, nodes, {k}) if True)

    def titles(kind: str, only_open: bool) -> list[str]:
        rows = []
        for n in members:
            if n["type"] != kind:
                continue
            if only_open and n["plan"]["state"] == "done":
                continue
            rows.append((weight(n["key"]), n["summary"]))
        rows.sort(key=lambda r: -r[0])
        return [s for _, s in rows[:3]]

    leaders = titles("Initiative", False) or titles("Epic", False)
    still = titles("Initiative", True) or titles("Epic", True)
    lead = "; ".join(leaders) if leaders else "No initiative or epic title in this area"
    open_lead = "; ".join(still) if still else "No open initiative or epic in this area"
    return [
        f"{c.get('Initiative', 0)} initiatives, {c.get('Epic', 0)} epics and {c.get('Story', 0)} stories. {done} are Done and {open_n} are still open.",
        f"Largest items: {lead}.",
        f"Still open: {open_lead}.",
    ]


def build_snapshot() -> dict:
    items = load_slices()
    if len(items) != EXPECTED_TOTAL:
        raise SystemExit(f"Expected {EXPECTED_TOTAL} Jira items, loaded {len(items)}")
    meta_keys = load_metadata_keys()
    excluded = exclude_metadata(items, meta_keys)
    context = {k: v for k, v in load_context().items() if k not in items}
    nodes = classify_all(items, context)
    children = _children_index(nodes)
    for n in nodes.values():
        if not n.get("context"):
            n["plan"] = item_plan(n)
    for k, n in nodes.items():
        if children[k]:
            n["rollup"] = rollup(subtree_plans(k, children, nodes, {k}))

    counted = [nodes[k] for k in items]
    by_area = {a: Counter() for a in AREAS + [NOT_IN_SIX]}
    for n in counted:
        by_area[n["area"]][n["type"]] += 1

    pace = json.loads((DATA / "throughput.json").read_text())
    per_area = {}
    for a in AREAS + [NOT_IN_SIX]:
        members = [nodes[k] for k in items if nodes[k]["area"] == a]
        plans = [m["plan"] for m in members]
        stories = [m for m in members if m["type"] == "Story" and m["plan"]["state"] != "done"]
        per_area[a] = {
            **rollup(plans),
            "open_stories": len(stories),
            "pace_months": pace_range(len(stories), pace),
        }
    all_plans = [nodes[k]["plan"] for k in items]
    open_stories = sum(1 for k in items if nodes[k]["type"] == "Story" and nodes[k]["plan"]["state"] != "done")
    overall = {**rollup(all_plans), "open_stories": open_stories, "pace_months": pace_range(open_stories, pace)}

    summaries = {}
    for a in AREAS:
        summaries[a] = SUMMARY_OVERRIDES.get(a) or auto_bullets(a, nodes, list(items), children)
        if len(summaries[a]) != 3:
            raise SystemExit(f"Need 3 summary bullets for {a}")

    missing_parents = sorted({
        n["parent"] for n in items.values()
        if n.get("parent") and n["parent"] not in nodes
    })
    (DATA / "missing-parents.json").write_text(json.dumps(missing_parents, indent=1))

    snap = {
        "title": "CRM Core Jira items by area",
        "jql": JQL,
        "run_date": AS_OF.isoformat(),
        "filter_total": EXPECTED_TOTAL,
        "excluded": excluded,
        "total": len(items),
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
                "done": per_area[a]["done"],
                "open": per_area[a]["planned"] + per_area[a]["slipped"] + per_area[a]["unplanned"],
            }
            for a, c in by_area.items()
        },
        "source_counts": dict(Counter(n["source"] for n in counted)),
        "summaries": summaries,
        "nodes": nodes,
        "counted_keys": list(items),
        "timeline": {
            "as_of": AS_OF.isoformat(),
            "pace": pace,
            "areas": per_area,
            "overall": overall,
        },
        "missing_parent_count": len(missing_parents),
    }
    return snap


def timeline_cell(t: dict) -> str:
    latest = (
        f'<b>{esc(t["latest_version"])}</b> {months_txt(t["months"])}'
        if t["latest_version"] else "<b>No future release</b>"
    )
    pm = t["pace_months"]
    pace = f'{pm["low"]:g}–{pm["high"]:g} team-months' if t["open_stories"] else "—"
    return (
        f'<div class="tl">{t["done"]} done · {t["open_stories"]} open stories</div>'
        f'<div class="tl">Latest open release: {latest}</div>'
        f'<div class="chips"><span class="plan p-planned">{t["planned"]} planned</span>'
        f'<span class="plan p-slipped">{t["slipped"]} slipped</span>'
        f'<span class="plan p-unplanned">{t["unplanned"]} unplanned</span></div>'
        f'<div class="tl muted">Open stories at current pace: {pace}</div>'
    )


def summary_table(snap: dict) -> str:
    rows = []
    tl = snap["timeline"]["areas"]
    rest = snap["not_in_six"]
    for a in snap["areas"] + [rest]:
        c = snap["area_counts"][a]
        sid = slug(a)
        if a == rest:
            what = (
                "Titles that match none of the six areas. The largest initiatives are the CRM homepage, "
                "ad hoc quarterly work, RX adoption, the projects revamp, schema-driven UI, page-load performance "
                "and CRM personalisation. Greyed parents above a row sit outside the filter and are not counted."
            )
        else:
            what = '<ul class="bullets">' + "".join(f"<li>{esc(b)}</li>" for b in snap["summaries"][a]) + "</ul>"
        rows.append(
            f'<tr class="area-row{" muted-row" if a == rest else ""}" id="{sid}">'
            f'<td class="area">{esc(a)}</td>'
            f'<td class="num">{c["Initiative"]}</td><td class="num">{c["Epic"]}</td>'
            f'<td class="num">{c["Story"]}</td><td class="num total">{c["total"]}</td>'
            f'<td class="num">{c["done"]}</td><td class="num">{c["open"]}</td>'
            f'<td class="tlcell">{timeline_cell(tl[a])}</td><td>{what}</td></tr>'
        )
        tree = render_tree(snap, a)
        controls = level_buttons(f"'{sid}-tree'") if c["total"] else ""
        rows.append(
            f'<tr class="tree-row"><td colspan="9"><details class="tree-wrap" id="{sid}-tree">'
            f'<summary>Hierarchy for {esc(a)} · {c["Initiative"]} initiatives · '
            f'{c["Epic"]} epics · {c["Story"]} stories</summary>'
            f'<div class="tree-body">{controls}'
            f'<label class="filter">Find <input type="search" placeholder="Key or title" '
            f'oninput="filterTree(\'{sid}-tree\', this.value)"></label>'
            f'{tree}</div></details></td></tr>'
        )
    return (
        '<table class="summary"><thead><tr><th>CRM Core area</th><th>Initiatives</th><th>Epics</th>'
        '<th>Stories</th><th>Total</th><th>Done</th><th>Open</th>'
        '<th>Timeline for what is still open</th><th>What the items cover</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


def build_html(snap: dict) -> str:
    in_six = sum(snap["area_counts"][a]["total"] for a in snap["areas"])
    rest = snap["area_counts"][snap["not_in_six"]]["total"]
    if in_six + rest != snap["total"]:
        raise SystemExit("Area counts do not sum to the item total")
    t = snap["type_totals"]
    src = snap["source_counts"]
    o = snap["timeline"]["overall"]
    pm = o["pace_months"]
    pace = snap["timeline"]["pace"]["windows"]
    pace_txt = "; ".join(
        f'{w["label"]} ({w["from"]} to {w["to"]}): {w["stories_done"]} stories done, {w["stories_per_month"]:g} per month'
        for w in pace
    )
    tokens = PDS_TOKENS.read_text() if PDS_TOKENS.exists() else ""
    statuses = ", ".join(f"{n} {name}" for name, n in list(snap["status_totals"].items())[:8])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(snap["title"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{tokens}</style><style>{CSS}
.filter{{display:flex;gap:.4rem;align-items:center;font-size:.75rem;color:var(--pds-text-muted);margin:.2rem 0 .6rem}}
.filter input{{font:inherit;color:var(--pds-text);background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);padding:.25rem .55rem;min-width:16rem}}
li.is-hidden{{display:none}}
</style></head><body>
<header>
<h1>{esc(snap["title"])}</h1>
<p class="sub">Every CRM Core initiative, epic and story in the Jira filter, any year and any status. Each area has a short summary and a hierarchy you can fold at the initiative, epic or story. Open a hierarchy, then use “Show down to” to stop at the level you want. Jira was read only. Run date {esc(snap["run_date"])}.</p>
<code>{esc(snap["jql"])}</code>
<div class="stats">
<div class="stat"><b>{snap["filter_total"]}</b><span>Jira items in the filter</span></div>
<div class="stat"><b>{len(snap.get("excluded", []))}</b><span>removed (metadata)</span></div>
<div class="stat"><b>{snap["total"]}</b><span>items in the trees</span></div>
<div class="stat"><b>{in_six}</b><span>in the six areas</span></div>
<div class="stat"><b>{rest}</b><span>not in the six areas</span></div>
<div class="stat"><b>{t.get("Initiative", 0)}</b><span>initiatives</span></div>
<div class="stat"><b>{t.get("Epic", 0)}</b><span>epics</span></div>
<div class="stat"><b>{t.get("Story", 0)}</b><span>stories</span></div>
<div class="stat"><b>{o["done"]}</b><span>Done</span></div>
<div class="stat"><b>{o["planned"] + o["slipped"] + o["unplanned"]}</b><span>still open</span></div>
</div>
<div class="note">How items were placed: each item gets exactly one area, matched on its <b>title</b>. {src.get("jira_v1", 0)} items matched an area phrase directly. {src.get("inherited", 0)} items had no area phrase and took their parent's area. {src.get("unmatched", 0)} items matched nothing and sit under “Not in the six areas”. Greyed rows are parents kept for context, or items counted in another area. Status mix (top): {esc(statuses)}.</div>
<div class="note"><b>Timeline, as of {esc(snap["run_date"])}.</b> Done items are closed and are not treated as slipped. For everything else, <i>planned</i> means a Fix Version on or after today, <i>slipped</i> means every Fix Version is already past, and <i>unplanned</i> means Backlog. Open-story pace uses stories Jira shows as resolved Done ({pace_txt}). At that pace the {o["open_stories"]} open stories would take {pm["low"]:g}–{pm["high"]:g} team-months. Per-area figures are that same team working only on the area, so they add up to the total. The latest planned Fix Version still on an open item is {esc(o["latest_version"] or "none")} ({months_txt(o["months"])}). Fix Versions are a plan, not a ship date.</div>
{excluded_note(snap)}
</header>
<main>
<h2>Summary by area</h2>
<div class="toolbar"><span class="sub">Open “Hierarchy” under an area. Each initiative and epic folds. The buttons set how deep that tree opens.</span>
<span class="levels"><span>All areas:</span><button type="button" onclick="setLevel(null,'area')">Areas only</button><button type="button" onclick="setLevel(null,'initiative')">Initiatives</button><button type="button" onclick="setLevel(null,'epic')">Epics</button><button type="button" onclick="setLevel(null,'story')">Stories</button></span></div>
{summary_table(snap)}
</main>
<footer>Source: Jira PHEM, read only · {snap["missing_parent_count"]} parents sit outside the filter and are shown only when their record was fetched · crm-core-jira-areas-all.html</footer>
<script>
function setLevel(scopeId, level) {{
  const wraps = scopeId ? [document.getElementById(scopeId)] : [...document.querySelectorAll('details.tree-wrap')];
  wraps.forEach(w => {{
    if (!w) return;
    w.open = level !== 'area';
    w.querySelectorAll('details[data-type]').forEach(d => {{
      const t = d.dataset.type;
      d.open = level === 'story' || (level === 'epic' && t === 'initiative');
    }});
  }});
}}
function filterTree(scopeId, q) {{
  const root = document.getElementById(scopeId);
  if (!root) return;
  q = q.trim().toLowerCase();
  const items = [...root.querySelectorAll('ul.tree li')];
  items.forEach(li => li.classList.remove('is-hidden'));
  if (!q) return;
  items.forEach(li => {{
    const node = li.querySelector(':scope > .node, :scope > details > summary .node');
    const self = node && node.textContent.toLowerCase().includes(q);
    const kid = [...li.querySelectorAll(':scope ul .node')].some(n => n.textContent.toLowerCase().includes(q));
    li.classList.toggle('is-hidden', !(self || kid));
    const det = li.querySelector(':scope > details');
    if (det && kid) det.open = true;
  }});
  root.open = true;
}}
</script>
</body></html>
"""


def main() -> None:
    snap = build_snapshot()
    SNAPSHOT.write_text(json.dumps(snap, ensure_ascii=False))
    OUT.write_text(build_html(snap))
    print(f"Wrote {OUT.relative_to(REPO)}  total={snap['total']} excluded={len(snap['excluded'])}")
    print(f"  missing parents outside the filter: {snap['missing_parent_count']}")
    for a in AREAS + [NOT_IN_SIX]:
        c = snap["area_counts"][a]
        print(f"  {c['total']:>4}  I{c['Initiative']:>3} E{c['Epic']:>4} S{c['Story']:>4}  done {c['done']:>4} open {c['open']:>4}  {a}")
        if a in snap["summaries"]:
            for b in snap["summaries"][a]:
                print(f"      - {b[:180]}")


if __name__ == "__main__":
    main()
