#!/usr/bin/env python3
"""Build CRM-area theme snapshot from all-fields CSV (Jira Yes + No).

Population (sheet-only):
  - U_ISSUE_TYPE contains 'Service Request'
  - U_PRODUCT_EXPERIENCE (or PRODUCT_EXPERIENCE) contains Recruiter Experience (RX)
  - JIRA_CREATED in {Yes, No}
  - Theme classifies into a CRM Core/Profile/Messaging/Automations area

Includes full playbook SR list (number, short/description, jira, theme, area)
for the HTML Playbook SRs tab. Does not invent themes.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rx_theme_playbook import AREA_ORDER, THEME_AREA  # noqa: E402
from rx_theme_rules import UNCLASSIFIED, classify_theme  # noqa: E402


def g(r, k):
    return (r.get(k) or "").strip()


def product_experience(r) -> str:
    return g(r, "PRODUCT_EXPERIENCE") or g(r, "U_PRODUCT_EXPERIENCE")


def clean_text(t: str, limit: int = 600) -> str:
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = re.sub(r"&nbsp;", " ", t, flags=re.I)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > limit:
        return t[: limit - 1].rstrip() + "…"
    return t


def theme_slug(theme: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-")
    return s or "theme"


def analyze(csv_path: Path) -> dict:
    funnel = Counter()
    theme_totals = Counter()
    theme_jira: dict[str, Counter] = defaultdict(Counter)
    area_totals = Counter()
    area_jira: dict[str, Counter] = defaultdict(Counter)
    service_requests: list[dict] = []

    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            funnel["all"] += 1
            if "Service Request" not in g(r, "U_ISSUE_TYPE"):
                continue
            funnel["service_request"] += 1
            if "Recruiter Experience (RX)" not in product_experience(r):
                continue
            funnel["rx"] += 1
            jira = g(r, "JIRA_CREATED")
            if jira not in ("Yes", "No"):
                continue
            funnel[f"jira_{jira}"] += 1
            funnel["jira_yes_or_no"] += 1

            short = g(r, "SHORT_DESCRIPTION")
            desc = g(r, "DESCRIPTION")
            theme = classify_theme(short, desc)
            if theme == UNCLASSIFIED:
                funnel["unclassified"] += 1
                continue
            area = THEME_AREA.get(theme)
            if not area:
                funnel["classified_outside_crm_areas"] += 1
                continue

            funnel["classified_in_crm_areas"] += 1
            theme_totals[theme] += 1
            theme_jira[theme][jira] += 1
            area_totals[area] += 1
            area_jira[area][jira] += 1

            number = g(r, "NUMBER") or g(r, "CASE_NUMBER")
            service_requests.append(
                {
                    "number": number,
                    "short_description": short,
                    "description": clean_text(desc, 600),
                    "jira_created": jira,
                    "ticket_class": g(r, "U_TICKET_CLASSIFICATION"),
                    "pep": g(r, "PRODUCT_EXPERIENCE_PRODUCT"),
                    "theme": theme,
                    "theme_slug": theme_slug(theme),
                    "area": area,
                }
            )

    # Stable order: area order, then theme count desc, then number
    area_rank = {a: i for i, a in enumerate(AREA_ORDER)}
    service_requests.sort(
        key=lambda x: (
            area_rank.get(x["area"], 99),
            -theme_totals[x["theme"]],
            x["theme"],
            x["number"],
        )
    )

    n = funnel["classified_in_crm_areas"]
    themes_by_area: dict[str, list] = {a: [] for a in AREA_ORDER}
    for theme, tot in theme_totals.most_common():
        area = THEME_AREA[theme]
        y = theme_jira[theme].get("Yes", 0)
        no = theme_jira[theme].get("No", 0)
        themes_by_area[area].append(
            {
                "theme": theme,
                "theme_slug": theme_slug(theme),
                "count": tot,
                "pct_of_filtered": round(100 * tot / n, 2) if n else 0.0,
                "jira_yes": y,
                "jira_no": no,
            }
        )
    for a in AREA_ORDER:
        themes_by_area[a].sort(key=lambda x: (-x["count"], x["theme"]))

    areas = []
    for a in AREA_ORDER:
        tot = area_totals.get(a, 0)
        areas.append(
            {
                "area": a,
                "count": tot,
                "pct_of_filtered": round(100 * tot / n, 2) if n else 0.0,
                "jira_yes": area_jira[a].get("Yes", 0),
                "jira_no": area_jira[a].get("No", 0),
                "themes": themes_by_area[a],
            }
        )

    return {
        "source": str(csv_path),
        "filters": {
            "U_ISSUE_TYPE": "contains 'Service Request'",
            "U_PRODUCT_EXPERIENCE|PRODUCT_EXPERIENCE": "contains 'Recruiter Experience (RX)'",
            "JIRA_CREATED": ["Yes", "No"],
            "theme": "classified into CRM Core/Profile/Messaging/Automations via phrase rules",
        },
        "funnel": dict(funnel),
        "n_filtered": n,
        "areas": areas,
        "theme_totals": [
            {
                "theme": t,
                "theme_slug": theme_slug(t),
                "count": c,
                "jira_yes": theme_jira[t].get("Yes", 0),
                "jira_no": theme_jira[t].get("No", 0),
                "area": THEME_AREA[t],
            }
            for t, c in theme_totals.most_common()
        ],
        "service_requests": service_requests,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    data = analyze(args.csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2))
    print(
        f"wrote {args.out} n_filtered={data['n_filtered']} "
        f"srs={len(data['service_requests'])} "
        f"yes={data['funnel'].get('jira_Yes', 0)} "
        f"no={data['funnel'].get('jira_No', 0)} "
        f"unc={data['funnel'].get('unclassified', 0)}"
    )


if __name__ == "__main__":
    main()
