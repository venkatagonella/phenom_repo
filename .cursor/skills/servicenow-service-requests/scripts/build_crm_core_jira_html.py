"""Build crm-core-jira-areas.html from snapshot-crm-core-jira-areas.json.

Run crm_core_jira_areas.py first. The HTML is self-contained: PDS tokens are
inlined from DesignSystem/styles/pds-tokens.css.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from crm_core_jira_areas import REPO, SNAPSHOT  # noqa: E402

OUT = SNAPSHOT.parent / "crm-core-jira-areas.html"
PDS_TOKENS = REPO / "DesignSystem/styles/pds-tokens.css"
BROWSE = "https://phenompeople.atlassian.net/browse/"
TYPE_ORDER = {"Initiative": 0, "Epic": 1, "Story": 2}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _key_num(k: str) -> int:
    return int(k.split("-")[1])


def area_forest(snap: dict, area: str) -> tuple[list[str], dict[str, list[str]]]:
    """Roots and child lists for every in-area item plus its ancestors."""
    nodes = snap["nodes"]
    counted = set(snap["counted_keys"])
    members = [k for k in counted if nodes[k]["area"] == area]
    keep: set[str] = set()
    for k in members:
        cur = k
        while cur and cur in nodes and cur not in keep:
            keep.add(cur)
            cur = nodes[cur].get("parent")
    children: dict[str, list[str]] = {k: [] for k in keep}
    roots = []
    for k in keep:
        p = nodes[k].get("parent")
        if p in keep:
            children[p].append(k)
        else:
            roots.append(k)

    def order(ks):
        return sorted(ks, key=lambda k: (TYPE_ORDER.get(nodes[k]["type"], 9), -_key_num(k)))

    return order(roots), {k: order(v) for k, v in children.items()}


def months_txt(m) -> str:
    return "—" if m is None else f"~{m:g} mo"


def plan_badge(p: dict) -> str:
    v = esc(", ".join(p["versions"]) or "none")
    if p["state"] == "planned":
        label = f'{esc(p["target_version"])} · {months_txt(p["months"])}'
        tip = f'Fix Version {v}; target {p["target"]} ({p["basis"]})'
    elif p["state"] == "slipped":
        label = f'{esc(p["target_version"])} · slipped'
        tip = f'Fix Version {v}; target {p["target"]} has passed and the item is still open'
    else:
        label = "Backlog · unplanned"
        tip = "Fix Version Backlog: no release planned"
    extra = ""
    if p.get("active_sprint"):
        extra += f'<span class="sprint" title="In the active sprint">{esc(p["active_sprint"])}</span>'
    if p.get("due"):
        extra += f'<span class="sprint" title="Jira due date">due {esc(p["due"])}</span>'
    return f'<span class="plan p-{p["state"]}" title="{esc(tip)}">{label}</span>{extra}'


def rollup_badge(r: dict) -> str:
    latest = (
        f'finishes {esc(r["latest_version"])} ({months_txt(r["months"])})'
        if r["latest_version"] else "no planned release"
    )
    return (
        f'<span class="rollup" title="Whole branch below this item, all areas: planned / slipped / unplanned">'
        f'branch: {latest} · {r["planned"]} planned · {r["slipped"]} slipped · {r["unplanned"]} unplanned</span>'
    )


def node_line(snap: dict, key: str, area: str) -> str:
    n = snap["nodes"][key]
    in_area = key in set(snap["counted_keys"]) and n["area"] == area
    if n.get("context"):
        tag = '<span class="ctx-tag">outside filter · context</span>'
    elif not in_area:
        tag = f'<span class="ctx-tag">counted under {esc(n["area"])}</span>'
    else:
        tag = ""
    how = ""
    if in_area and n["source"] == "inherited":
        how = f'<span class="how" title="No area phrase in the title; area taken from parent">inherited {esc(n["pattern"])}</span>'
    plan = plan_badge(n["plan"]) if "plan" in n else ""
    roll = rollup_badge(n["rollup"]) if n.get("rollup") and n["rollup"]["items"] else ""
    cls = "node" + ("" if in_area else " context")
    return (
        f'<div class="{cls}">'
        f'<span class="type t-{n["type"].lower()}">{esc(n["type"])}</span>'
        f'<a class="key" href="{BROWSE}{esc(key)}" target="_blank" rel="noopener">{esc(key)}</a>'
        f'<span class="summary">{esc(n["summary"])}</span>'
        f'<span class="status">{esc(n["status"])}</span>{plan}{roll}{how}{tag}</div>'
    )


def render_tree(snap: dict, area: str) -> str:
    roots, children = area_forest(snap, area)
    if not roots:
        return '<p class="empty">No items in this area.</p>'

    def rec(k: str) -> str:
        line = node_line(snap, k, area)
        kids = children.get(k, [])
        if not kids:
            return f"<li>{line}</li>"
        inner = "".join(rec(c) for c in kids)
        t = snap["nodes"][k]["type"].lower()
        return f'<li><details data-type="{t}"><summary>{line}</summary><ul>{inner}</ul></details></li>'

    return '<ul class="tree">' + "".join(rec(r) for r in roots) + "</ul>"


LEVELS = [("initiative", "Initiatives"), ("epic", "Epics"), ("story", "Stories")]


def level_buttons(scope: str) -> str:
    btns = "".join(
        f'<button type="button" onclick="setLevel({scope},\'{lv}\')">{label}</button>' for lv, label in LEVELS
    )
    return f'<span class="levels"><span>Show down to:</span>{btns}</span>'


def timeline_cell(t: dict) -> str:
    latest = (
        f'<b>{esc(t["latest_version"])}</b> {months_txt(t["months"])}' if t["latest_version"] else "<b>No planned release</b>"
    )
    pm = t["pace_months"]
    pace = f'{pm["low"]:g}–{pm["high"]:g} team-months' if t["open_stories"] else "—"
    return (
        f'<div class="tl">Latest planned: {latest}</div>'
        f'<div class="chips"><span class="plan p-planned">{t["planned"]} planned</span>'
        f'<span class="plan p-slipped">{t["slipped"]} slipped</span>'
        f'<span class="plan p-unplanned">{t["unplanned"]} unplanned</span></div>'
        f'<div class="tl muted">At current pace: {pace}</div>'
    )


def summary_table(snap: dict) -> str:
    rows = []
    tl = snap["timeline"]["areas"]
    rest = snap["not_in_six"]
    for a in snap["areas"] + [rest]:
        c = snap["area_counts"][a]
        is_rest = a == rest
        if is_rest:
            what = (
                "Platform, performance, SDUI, notes, spotlights, executive reports, surveys, agency and "
                "messaging-template work whose titles do not match any of the six areas."
            )
        else:
            what = '<ul class="bullets">' + "".join(f"<li>{esc(b)}</li>" for b in snap["summaries"][a]) + "</ul>"
        sid = slug(a)
        rows.append(
            f'<tr class="area-row{" muted-row" if is_rest else ""}" id="{sid}"><td class="area">{esc(a)}</td>'
            f'<td class="num">{c["Initiative"]}</td><td class="num">{c["Epic"]}</td>'
            f'<td class="num">{c["Story"]}</td><td class="num total">{c["total"]}</td>'
            f"<td class=\"tlcell\">{timeline_cell(tl[a])}</td><td>{what}</td></tr>"
        )
        tree = render_tree(snap, a)
        controls = level_buttons(f"'{sid}-tree'") if c["total"] else ""
        rows.append(
            f'<tr class="tree-row"><td colspan="7"><details class="tree-wrap" id="{sid}-tree">'
            f'<summary>Hierarchy for {esc(a)} · {c["Initiative"]} initiatives · {c["Epic"]} epics · {c["Story"]} stories</summary>'
            f'<div class="tree-body">{controls}{tree}</div></details></td></tr>'
        )
    return (
        '<table class="summary"><thead><tr><th>CRM Core area</th><th>Initiatives</th><th>Epics</th>'
        "<th>Stories</th><th>Total</th><th>Planned timeline</th><th>What will improve (from the item titles)</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def timeline_section(snap: dict) -> str:
    tl = snap["timeline"]
    o = tl["overall"]
    pace = tl["pace"]["windows"]
    pace_txt = "; ".join(
        f'{w["label"]} ({w["from"]} to {w["to"]}): {w["stories_done"]} stories done, {w["stories_per_month"]:g} per month'
        for w in pace
    )
    vers = " · ".join(f"{esc(v)} {n}" for v, n in tl["target_version_counts"].items())
    rows = []
    for a in snap["areas"] + [snap["not_in_six"]]:
        t = tl["areas"][a]
        pm = t["pace_months"]
        pace_cell = f'{pm["low"]:g}–{pm["high"]:g}' if t["open_stories"] else "—"
        muted = ' class="muted-row"' if a == snap["not_in_six"] else ""
        rows.append(
            f'<tr{muted}><td class="area">{esc(a)}</td>'
            f'<td class="num">{t["planned"]}</td><td class="num">{t["slipped"]}</td><td class="num">{t["unplanned"]}</td>'
            f'<td>{esc(t["latest_version"] or "—")}</td><td class="num">{months_txt(t["months"])}</td>'
            f'<td class="num">{t["open_stories"]}</td><td class="num">{pace_cell}</td></tr>'
        )
    opm = o["pace_months"]
    rows.append(
        f'<tr class="total-row"><td class="area">All {snap["total"]} items</td><td class="num">{o["planned"]}</td>'
        f'<td class="num">{o["slipped"]}</td><td class="num">{o["unplanned"]}</td><td>{esc(o["latest_version"] or "—")}</td>'
        f'<td class="num">{months_txt(o["months"])}</td><td class="num">{o["open_stories"]}</td>'
        f'<td class="num">{opm["low"]:g}–{opm["high"]:g}</td></tr>'
    )
    return f"""
<div class="stats">
<div class="stat"><b>{months_txt(o["months"])}</b><span>to the latest planned release ({esc(o["latest_version"])})</span></div>
<div class="stat"><b>{opm["low"]:g}–{opm["high"]:g} mo</b><span>to finish all {o["open_stories"]} open stories at current pace</span></div>
<div class="stat"><b>{o["planned"]}</b><span>items with a future release</span></div>
<div class="stat"><b>{o["slipped"]}</b><span>items whose release date has passed</span></div>
<div class="stat"><b>{o["unplanned"]}</b><span>items in Backlog (no release)</span></div>
</div>
<table class="summary tl-table"><thead><tr><th>CRM Core area</th><th>Planned</th><th>Slipped</th><th>Unplanned</th>
<th>Latest planned release</th><th>Months to it</th><th>Open stories</th><th>Team-months at current pace</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>
<div class="note"><b>How the timeline was estimated (as of {esc(tl["as_of"])}).</b>
<b>Planned timeline</b> uses only each item's Jira Fix Version: the version's release date if Jira has one, otherwise the end of the YY.MM month (27.01 = 31 Jan 2027), and 31 Dec 2026 for OffCycle-2026. <i>Planned</i> means the item has a release on or after today. <i>Slipped</i> means every release on the item is already past but the item is still open, so it needs re-planning. <i>Unplanned</i> means Fix Version is Backlog.
<b>Current pace</b> divides open stories by the number of CRM Core stories Jira shows as resolved Done ({pace_txt}). Per-area figures are team-months: the time if the whole CRM Core team worked only on that area. Areas run in parallel, so the per-area figures add up to the all-items figure rather than each being a separate finish date.
Limits: only {tl["with_story_points"]} of {snap["total"]} items have story points and {tl["with_due_date"]} have a due date, so story size is not weighted. Epics and initiatives with no open child stories add work this count does not see. {tl["in_active_sprint"]} items are in the active sprint.
Target versions across all items: {vers}.</div>
"""


CSS = """
body{margin:0;font-family:var(--font-family-body,Poppins),system-ui,sans-serif;color:var(--pds-text);background:var(--pds-surface-muted)}
header,main{max-width:1180px;margin:0 auto;padding:1.5rem}
header{padding-bottom:.5rem}
h1{font-size:1.6rem;font-weight:600;margin:0 0 .3rem}
h2{font-size:1.15rem;font-weight:600;margin:1.6rem 0 .6rem}
.sub{color:var(--pds-text-muted);font-size:.9rem;max-width:90ch;line-height:1.5}
code{font-size:.78rem;background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);padding:.4rem .6rem;display:block;white-space:pre-wrap;word-break:break-word;margin:.5rem 0}
.stats{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:.9rem}
.stat{background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);box-shadow:var(--pds-shadow-sm);padding:.55rem .9rem;min-width:8.5rem}
.stat b{display:block;font-size:1.25rem;font-weight:600;color:var(--pds-brand-teal);font-variant-numeric:tabular-nums}
.stat span{font-size:.75rem;color:var(--pds-text-muted)}
.note{background:var(--pds-surface);border:1px solid var(--pds-border);border-left:3px solid var(--pds-warning);border-radius:var(--pds-radius-md);padding:.7rem 1rem;font-size:.85rem;line-height:1.5;color:var(--pds-text-muted);margin:.8rem 0}
table.summary{width:100%;border-collapse:collapse;background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);overflow:hidden;font-size:.86rem}
table.summary th,table.summary td{padding:.6rem .7rem;border-bottom:1px solid var(--pds-border);text-align:left;vertical-align:top}
table.summary th{background:var(--pds-surface-muted);font-weight:600;font-size:.78rem;color:var(--pds-text-muted)}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.total{font-weight:600;color:var(--pds-brand-teal)}
td.area{font-weight:600;width:15rem}
td.area a{color:var(--pds-text);text-decoration:none}td.area a:hover{color:var(--pds-brand)}
tr.muted-row td{color:var(--pds-text-muted)}
ul.bullets{margin:0;padding-left:1.1rem;line-height:1.5}ul.bullets li{margin:.15rem 0}
details.area-block{background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);box-shadow:var(--pds-shadow-sm);margin:.75rem 0}
details.area-block>summary{cursor:pointer;padding:.8rem 1rem;display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;list-style:none}
details.area-block>summary::-webkit-details-marker{display:none}
details.area-block>summary::before{content:"\\25B8";color:var(--pds-text-muted);transition:transform .15s}
details.area-block[open]>summary::before{transform:rotate(90deg)}
.area-title{font-weight:600;font-size:1rem}
.pill{font-size:.75rem;color:var(--pds-brand-teal);border:1px solid var(--pds-border);border-radius:999px;padding:.1rem .6rem;font-variant-numeric:tabular-nums}
.area-body{padding:0 1rem 1rem}
.area-body>ul.bullets{background:var(--pds-surface-muted);border-radius:var(--pds-radius-md);padding:.6rem .6rem .6rem 1.6rem;margin-bottom:.8rem;font-size:.88rem}
ul.tree,ul.tree ul{list-style:none;margin:0;padding-left:1.2rem}
ul.tree{padding-left:0}
ul.tree ul{border-left:1px dashed var(--pds-border);margin-left:.45rem}
ul.tree li{margin:.2rem 0}
ul.tree details>summary{cursor:pointer;list-style:none}
ul.tree details>summary::-webkit-details-marker{display:none}
.node{display:flex;flex-wrap:wrap;gap:.45rem;align-items:baseline;font-size:.84rem;padding:.2rem .3rem;border-radius:6px}
.node:hover{background:var(--pds-surface-muted)}
.node.context{opacity:.6}
.type{font-size:.66rem;font-weight:600;text-transform:uppercase;letter-spacing:.03em;border-radius:4px;padding:.05rem .35rem;border:1px solid var(--pds-border)}
.t-initiative{color:var(--pds-brand);border-color:var(--pds-brand)}
.t-epic{color:var(--pds-brand-teal);border-color:var(--pds-brand-teal)}
.t-story{color:var(--pds-text-muted)}
.key{font-weight:600;color:var(--pds-brand);text-decoration:none;font-variant-numeric:tabular-nums}
.key:hover{text-decoration:underline}
.summary{flex:1 1 22rem}
.status{font-size:.72rem;color:var(--pds-text-muted);background:var(--pds-surface-muted);border-radius:999px;padding:.05rem .5rem}
.how,.ctx-tag{font-size:.7rem;color:var(--pds-text-muted);font-style:italic}
.empty{color:var(--pds-text-muted);font-size:.86rem;font-style:italic}
tr.tree-row>td{padding:0 .7rem .6rem;background:var(--pds-surface)}
tr.area-row>td{border-bottom:none}
details.tree-wrap>summary{cursor:pointer;font-size:.8rem;font-weight:500;color:var(--pds-brand);padding:.35rem 0;list-style:none}
details.tree-wrap>summary::-webkit-details-marker{display:none}
details.tree-wrap>summary::before,ul.tree details>summary .node::before{content:"\\25B8";display:inline-block;margin-right:.35rem;color:var(--pds-text-muted);transition:transform .15s}
details.tree-wrap[open]>summary::before,ul.tree details[open]>summary .node::before{transform:rotate(90deg)}
.tree-body{border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);padding:.6rem .8rem;background:var(--pds-surface-muted)}
.tree-body .node:hover{background:var(--pds-surface)}
.levels{display:flex;flex-wrap:wrap;gap:.35rem;align-items:center;font-size:.75rem;color:var(--pds-text-muted);margin-bottom:.5rem}
.levels button{font:inherit;font-weight:500;color:var(--pds-brand);background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:999px;padding:.15rem .7rem;cursor:pointer}
.levels button:hover{border-color:var(--pds-brand)}
.toolbar{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;margin-bottom:.5rem}
.plan{font-size:.7rem;font-weight:500;border-radius:999px;padding:.05rem .5rem;border:1px solid currentColor;white-space:nowrap}
.p-planned{color:var(--pds-success)}.p-slipped{color:var(--pds-error)}.p-unplanned{color:var(--pds-text-muted)}
.sprint,.rollup{font-size:.7rem;color:var(--pds-text-muted)}
.rollup{border-left:2px solid var(--pds-brand-teal);padding-left:.4rem}
td.tlcell{width:13rem;font-size:.8rem}
.tl{margin:.1rem 0}.tl.muted{color:var(--pds-text-muted)}
.chips{display:flex;flex-wrap:wrap;gap:.25rem;margin:.3rem 0}
tr.total-row td{font-weight:600;background:var(--pds-surface-muted)}
.tl-table{margin-top:.8rem}
footer{max-width:1180px;margin:0 auto;padding:0 1.5rem 2rem;font-size:.78rem;color:var(--pds-text-muted)}
"""


def excluded_note(snap: dict) -> str:
    ex = snap.get("excluded") or []
    if not ex:
        return ""
    rows = "".join(
        f'<li><span class="type t-{e["type"].lower()}">{esc(e["type"])}</span> '
        f'<a class="key" href="{BROWSE}{esc(e["key"])}" target="_blank" rel="noopener">{esc(e["key"])}</a> '
        f'{esc(e["summary"])} <span class="how">{esc(e["reason"])}</span></li>'
        for e in ex
    )
    return (
        f'<details class="note"><summary><b>{len(ex)} items removed</b> because their title or description '
        "mentions metadata, plus the child stories of a removed metadata-titled item. They are left out of "
        "every count, tree and timeline below. Children of an item removed only for its description stay in "
        f'and attach to their nearest remaining parent.</summary><ul class="excluded">{rows}</ul></details>'
    )


def build(snap: dict) -> str:
    in_six = sum(snap["area_counts"][a]["total"] for a in snap["areas"])
    rest = snap["area_counts"][snap["not_in_six"]]["total"]
    if in_six + rest != snap["total"]:
        raise SystemExit("Area counts do not sum to the item total")
    t = snap["type_totals"]
    src = snap["source_counts"]
    tokens = PDS_TOKENS.read_text() if PDS_TOKENS.exists() else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(snap["title"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{tokens}</style><style>{CSS}</style></head><body>
<header>
<h1>{esc(snap["title"])}</h1>
<p class="sub">Open CRM Core initiatives, epics and stories created since 1 Jan 2026, grouped into six areas. Each area shows a three-point summary of what will improve, its planned timeline from Jira Fix Versions, and a foldable initiative → epic → story hierarchy. Jira was read only. Run date {esc(snap["run_date"])}.</p>
<code>{esc(snap["jql"])}</code>
<div class="stats">
<div class="stat"><b>{snap.get("filter_total", snap["total"])}</b><span>Jira items in the filter</span></div>
<div class="stat"><b>{len(snap.get("excluded", []))}</b><span>removed (metadata)</span></div>
<div class="stat"><b>{snap["total"]}</b><span>items analysed</span></div>
<div class="stat"><b>{in_six}</b><span>in the six areas</span></div>
<div class="stat"><b>{rest}</b><span>not in the six areas</span></div>
<div class="stat"><b>{t.get("Initiative", 0)}</b><span>initiatives</span></div>
<div class="stat"><b>{t.get("Epic", 0)}</b><span>epics</span></div>
<div class="stat"><b>{t.get("Story", 0)}</b><span>stories</span></div>
</div>
<div class="note">How items were placed: each item gets exactly one area, matched on its <b>title</b>. Descriptions were not used because Jira story templates carry boilerplate (for example "Out of scope: Permissions") that causes false matches. {src.get("jira_v1", 0)} items matched an area phrase directly. {src.get("inherited", 0)} items had no area phrase and took their parent's area. {src.get("unmatched", 0)} items matched nothing and are listed under "Not in the six areas". Greyed rows in a tree are parents shown for context: they are outside the filter or counted in a different area.</div>
{excluded_note(snap)}
</header>
<main>
<h2>Summary by area</h2>
<div class="toolbar"><span class="sub">Open "Hierarchy" under an area to see its initiatives, epics and stories. Each initiative and epic folds. The buttons set how deep the tree opens.</span>
<span class="levels"><span>All areas:</span><button type="button" onclick="setLevel(null,'area')">Areas only</button><button type="button" onclick="setLevel(null,'initiative')">Initiatives</button><button type="button" onclick="setLevel(null,'epic')">Epics</button><button type="button" onclick="setLevel(null,'story')">Stories</button></span></div>
{summary_table(snap)}
<h2>Estimated timeline</h2>
{timeline_section(snap)}
</main>
<footer>Source: Jira PHEM (read-only) · snapshot-crm-core-jira-areas.json · built by build_crm_core_jira_html.py</footer>
<script>
function setLevel(scopeId, level) {{
  const wraps = scopeId ? [document.getElementById(scopeId)] : [...document.querySelectorAll('details.tree-wrap')];
  wraps.forEach(w => {{
    w.open = level !== 'area';
    w.querySelectorAll('details[data-type]').forEach(d => {{
      const t = d.dataset.type;
      d.open = level === 'story' || (level === 'epic' && t === 'initiative');
    }});
  }});
}}
</script>
</body></html>
"""


def main() -> None:
    snap = json.loads(SNAPSHOT.read_text())
    OUT.write_text(build(snap))
    print(f"Wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
