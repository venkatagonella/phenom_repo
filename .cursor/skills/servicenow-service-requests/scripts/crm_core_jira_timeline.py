"""Planned timeline for the CRM Core Jira items, from Jira planning fields only.

Input (under data/crm-core-jira/):
  plan-page*.json   searchJiraIssuesUsingJql pages with fixVersions, duedate,
                    Sprint (customfield_10111), Story Points (customfield_10003)
  throughput.json   CRM Core stories/epics resolved Done per 6-month window

Two estimates, never mixed:
  1. Plan-based: each Fix Version becomes a target date.
       release date on the version  -> that date
       YY.MM name without a date    -> last day of that month (monthly release train)
       OffCycle-<year>              -> 31 Dec of that year
       Backlog                      -> no date (unplanned)
     planned  = at least one target on or after the as-of date (latest one wins)
     slipped  = only targets before the as-of date while the item is still open
     unplanned = Backlog only
  2. Pace-based: open stories / stories closed per month in the throughput
     windows. Reported as a range across the windows, in team-months (the
     whole CRM Core team working only on that set of stories).
"""

from __future__ import annotations

import calendar
import json
import re
from datetime import date
from pathlib import Path

DAYS_PER_MONTH = 30.44
_YYMM = re.compile(r"^(\d{2})\.(\d{2})$")
_OFFCYCLE = re.compile(r"^OffCycle-(\d{4})$", re.I)


def months_between(start: date, end: date) -> float:
    return round((end - start).days / DAYS_PER_MONTH, 1)


def version_target(name: str, release_date: str | None) -> tuple[date | None, str]:
    if release_date:
        return date.fromisoformat(release_date), "release date"
    m = _YYMM.match(name)
    if m:
        y, mo = 2000 + int(m.group(1)), int(m.group(2))
        return date(y, mo, calendar.monthrange(y, mo)[1]), "end of release month"
    m = _OFFCYCLE.match(name)
    if m:
        return date(int(m.group(1)), 12, 31), "end of off-cycle year"
    return None, "backlog"


def load_plan(data_dir: Path) -> dict[str, dict]:
    plan: dict[str, dict] = {}
    for page in sorted(data_dir.glob("plan-page*.json")):
        d = json.loads(page.read_text())
        d = d.get("data", d)
        for i in d["issues"]:
            f = i["fields"]
            cf = f.get("customFields") or {}
            sprints = (cf.get("Sprint") or {}).get("value") or []
            plan[i["key"]] = {
                "versions": [
                    {"name": v["name"], "release_date": v.get("releaseDate")}
                    for v in f.get("fixVersions") or []
                ],
                "due": f.get("duedate"),
                "story_points": (cf.get("Story Points") or {}).get("value"),
                "sprints": [
                    {"name": s["name"], "state": s["state"], "end": (s.get("endDate") or "")[:10]}
                    for s in sprints
                ],
            }
    return plan


def item_timeline(p: dict, as_of: date) -> dict:
    targets = []
    for v in p["versions"]:
        t, basis = version_target(v["name"], v["release_date"])
        if t:
            targets.append((t, v["name"], basis))
    future = [x for x in targets if x[0] >= as_of]
    if future:
        t, name, basis = max(future)
        state = "planned"
    elif targets:
        t, name, basis = max(targets)
        state = "slipped"
    else:
        t, name, basis = None, "Backlog", "backlog"
        state = "unplanned"
    active = [s["name"] for s in p["sprints"] if s["state"] == "active"]
    return {
        "versions": [v["name"] for v in p["versions"]],
        "state": state,
        "target": t.isoformat() if t else None,
        "target_version": name,
        "basis": basis,
        "months": months_between(as_of, t) if t and state == "planned" else None,
        "due": p["due"],
        "story_points": p["story_points"],
        "active_sprint": active[0] if active else None,
    }


def _rollup(items: list[dict], as_of: date) -> dict:
    counts = {"planned": 0, "slipped": 0, "unplanned": 0}
    latest = None
    for t in items:
        counts[t["state"]] += 1
        if t["state"] == "planned":
            d = date.fromisoformat(t["target"])
            if latest is None or d > latest[0]:
                latest = (d, t["target_version"])
    return {
        **counts,
        "items": len(items),
        "latest_target": latest[0].isoformat() if latest else None,
        "latest_version": latest[1] if latest else None,
        "months": months_between(as_of, latest[0]) if latest else None,
    }


def load_pace(data_dir: Path) -> dict:
    raw = json.loads((data_dir / "throughput.json").read_text())
    windows = [
        {**w, "stories_per_month": round(w["stories_done"] / w["months"], 1)}
        for w in raw["windows"]
    ]
    return {"as_of": raw["as_of"], "windows": windows}


def pace_range(stories: int, pace: dict) -> dict:
    rates = [w["stories_per_month"] for w in pace["windows"] if w["stories_per_month"]]
    if not rates or not stories:
        return {"low": 0.0, "high": 0.0}
    return {"low": round(stories / max(rates), 1), "high": round(stories / min(rates), 1)}


def annotate(snap: dict, data_dir: Path, areas_with_rest: list[str]) -> None:
    """Add per-item plan, per-node rollups and per-area timeline to snap."""
    as_of = date.fromisoformat(snap["run_date"])
    plan = load_plan(data_dir)
    counted = snap["counted_keys"]
    missing = [k for k in counted if k not in plan]
    if missing:
        raise SystemExit(f"No planning fields for {len(missing)} items, e.g. {missing[:3]}")

    nodes = snap["nodes"]
    for k in counted:
        nodes[k]["plan"] = item_timeline(plan[k], as_of)

    children: dict[str, list[str]] = {k: [] for k in nodes}
    for k, n in nodes.items():
        if n.get("parent") in children:
            children[n["parent"]].append(k)

    def subtree(k: str, seen: set) -> list[dict]:
        out = [nodes[k]["plan"]] if "plan" in nodes[k] else []
        for c in children[k]:
            if c not in seen:
                seen.add(c)
                out += subtree(c, seen)
        return out

    for k, n in nodes.items():
        if children[k]:
            n["rollup"] = _rollup(subtree(k, {k}), as_of)

    pace = load_pace(data_dir)
    per_area = {}
    for a in areas_with_rest:
        members = [nodes[k] for k in counted if nodes[k]["area"] == a]
        roll = _rollup([m["plan"] for m in members], as_of)
        stories = [m for m in members if m["type"] == "Story"]
        per_area[a] = {
            **roll,
            "open_stories": len(stories),
            "unplanned_stories": sum(1 for m in stories if m["plan"]["state"] == "unplanned"),
            "pace_months": pace_range(len(stories), pace),
        }
    all_plans = [nodes[k]["plan"] for k in counted]
    all_stories = sum(1 for k in counted if nodes[k]["type"] == "Story")
    overall = {
        **_rollup(all_plans, as_of),
        "open_stories": all_stories,
        "pace_months": pace_range(all_stories, pace),
    }
    version_counts: dict[str, int] = {}
    for p in all_plans:
        v = p["target_version"]
        version_counts[v] = version_counts.get(v, 0) + 1
    snap["timeline"] = {
        "as_of": as_of.isoformat(),
        "pace": pace,
        "areas": per_area,
        "overall": overall,
        "target_version_counts": dict(sorted(version_counts.items(), key=lambda x: -x[1])),
        "with_due_date": sum(1 for p in all_plans if p["due"]),
        "in_active_sprint": sum(1 for p in all_plans if p["active_sprint"]),
        "with_story_points": sum(1 for p in all_plans if p["story_points"] is not None),
    }
