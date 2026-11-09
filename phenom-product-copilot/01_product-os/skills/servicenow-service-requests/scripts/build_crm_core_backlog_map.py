"""Write the CRM Core backlog map from snapshot-crm-core-jira-areas.json.

Run crm_core_jira_areas.py first. Output:
01_product-os/knowledge/servicenow-service-requests/crm-core-backlog-map.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_crm_core_jira_html import area_forest  # noqa: E402
from crm_core_jira_areas import JQL, REPO, SNAPSHOT  # noqa: E402

OUT = SNAPSHOT.parent / "crm-core-backlog-map.md"


def plan_txt(n: dict) -> str:
    p = n.get("plan")
    if not p:
        return ""
    if p["state"] == "planned":
        return f'{p["target_version"]} (~{p["months"]:g} mo)'
    if p["state"] == "slipped":
        return f'{p["target_version"]} slipped'
    return "Backlog"


def roll_txt(n: dict) -> str:
    r = n.get("rollup")
    if not r or not r["items"]:
        return ""
    latest = f'latest {r["latest_version"]} (~{r["months"]:g} mo)' if r["latest_version"] else "no planned release"
    return f' — branch: {latest}; {r["planned"]} planned / {r["slipped"]} slipped / {r["unplanned"]} unplanned'


def line(snap: dict, key: str, area: str, depth: int) -> str:
    n = snap["nodes"][key]
    counted = key in snap["counted_keys_set"] and n["area"] == area
    note = "" if counted else (" _(context: outside filter)_" if n.get("context") else f' _(counted under {n["area"]})_')
    plan = plan_txt(n) if counted else ""
    plan = f" · {plan}" if plan else ""
    return f'{"  " * depth}- **{n["type"][0]}** {key} {n["summary"]} · {n["status"]}{plan}{roll_txt(n)}{note}'


def area_block(snap: dict, area: str) -> list[str]:
    roots, children = area_forest(snap, area)
    c = snap["area_counts"][area]
    t = snap["timeline"]["areas"][area]
    pm = t["pace_months"]
    out = [
        f"## {area}",
        "",
        f'{c["total"]} items (I {c["Initiative"]} · E {c["Epic"]} · S {c["Story"]}). '
        f'Planned {t["planned"]} · slipped {t["slipped"]} · unplanned {t["unplanned"]}. '
        f'Latest planned release: {t["latest_version"] or "none"}'
        + (f' (~{t["months"]:g} mo)' if t["months"] is not None else "")
        + (f'. Pace estimate: {pm["low"]:g}–{pm["high"]:g} team-months for {t["open_stories"]} open stories.' if t["open_stories"] else "."),
        "",
    ]
    if not roots:
        return out + ["No items.", ""]

    def rec(k: str, d: int):
        out.append(line(snap, k, area, d))
        for ch in children.get(k, []):
            rec(ch, d + 1)

    for r in roots:
        rec(r, 0)
    out.append("")
    return out


def main() -> None:
    snap = json.loads(SNAPSHOT.read_text())
    snap["counted_keys_set"] = set(snap["counted_keys"])
    lines = [
        "# CRM Core Jira backlog map (generated)",
        "",
        f'Generated from `snapshot-crm-core-jira-areas.json`, run date {snap["run_date"]}. '
        "Do not edit by hand; rerun `build_crm_core_backlog_map.py`.",
        "",
        f"JQL: `{JQL}`",
        "",
        "Legend: **I** Initiative, **E** Epic, **S** Story. After the status comes the item's Fix Version target "
        "(`~N mo` = months from the run date), `slipped` (release date passed, item still open) or `Backlog` (no release). "
        "`branch:` rolls up every counted item below a parent, across all areas.",
        "",
    ]
    for a in snap["areas"] + [snap["not_in_six"]]:
        lines += area_block(snap, a)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
