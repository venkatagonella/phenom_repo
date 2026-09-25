#!/usr/bin/env python3
"""Filter all-fields ServiceNow CSV → theme × ticket-classification counts.

Also builds CRM product-area × classification nesting (by PRODUCT_EXPERIENCE_PRODUCT).
Optional --sheet-csv reports coverage of sheet RX Jira Yes cases.
Sheet-only. No invented themes or classifications.
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
from rx_theme_rules import classify_theme  # noqa: E402

CLASS_ALLOW = frozenset(
    {
        "Product & Knowledge Issues",
        "Configuration Issues",
        "User Experience Issues",
        "Code Issues",
        "External Dependency Issues",
        "Ops Issues",
        "Security-Related Issues",
    }
)

CLASS_FOCUS = [
    "Product & Knowledge Issues",
    "Code Issues",
    "Configuration Issues",
    "User Experience Issues",
]

PRODUCTS_ALLOW = frozenset(
    {
        "CRM - Core",
        "CRM - Profile",
        "CRM - Automation",
        "CRM - Messaging and Campaigns",
    }
)

# Playbook issue types (exact U_ISSUE_TYPE values)
ISSUE_TYPES_ALLOW = frozenset({"Service Request", "Defect"})

# PEP label → Playbook area name
PEP_TO_AREA = {
    "CRM - Core": "CRM Core",
    "CRM - Profile": "CRM Profile",
    "CRM - Automation": "CRM Automations",
    "CRM - Messaging and Campaigns": "CRM Messaging",
}

AREA_ORDER = [
    "CRM Core",
    "CRM Profile",
    "CRM Messaging",
    "CRM Automations",
]


def g(r, k):
    return (r.get(k) or "").strip()


def pep_parts(s: str) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in re.split(r"[;|]", s) if x.strip()]


def pep_only_allowed(s: str) -> bool:
    parts = pep_parts(s)
    return bool(parts) and all(x in PRODUCTS_ALLOW for x in parts)


def issue_type_ok(raw: str) -> bool:
    return (raw or "").strip() in ISSUE_TYPES_ALLOW


def area_from_pep(pep: str) -> str:
    """One area per row: first allowlisted PEP token (keeps sum = n_filtered)."""
    parts = pep_parts(pep)
    if not parts:
        return "Unmapped"
    return PEP_TO_AREA.get(parts[0], "Unmapped")


def analyze(csv_path: Path, sheet_csv: Path | None = None) -> dict:
    funnel = Counter()
    class_counts = Counter()
    pep_counts = Counter()
    theme_totals = Counter()
    theme_class: dict[str, Counter] = defaultdict(Counter)
    # area → class → count
    area_class_counts: dict[str, Counter] = defaultdict(Counter)
    # area → class → theme → count
    area_class_theme: dict[str, dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter)
    )
    area_totals: Counter = Counter()

    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            funnel["all"] += 1
            if not issue_type_ok(g(r, "U_ISSUE_TYPE")):
                continue
            funnel["issue_type"] += 1
            # track mix
            it = g(r, "U_ISSUE_TYPE")
            funnel[f"issue_type_{it}"] += 1
            cls = g(r, "U_TICKET_CLASSIFICATION")
            if cls not in CLASS_ALLOW:
                continue
            funnel["class_allow"] += 1
            if "Recruiter Experience (RX)" not in g(r, "U_PRODUCT_EXPERIENCE"):
                continue
            funnel["rx"] += 1
            pep = g(r, "PRODUCT_EXPERIENCE_PRODUCT")
            if not pep_only_allowed(pep):
                continue
            funnel["pep_only"] += 1
            funnel[f"pep_only_{it}"] += 1

            theme = classify_theme(g(r, "SHORT_DESCRIPTION"), g(r, "DESCRIPTION"))
            area = area_from_pep(pep)
            class_counts[cls] += 1
            pep_counts[pep] += 1
            theme_totals[theme] += 1
            theme_class[theme][cls] += 1
            area_totals[area] += 1
            area_class_counts[area][cls] += 1
            area_class_theme[area][cls][theme] += 1

    n = funnel["pep_only"]
    classification = []
    for c in CLASS_FOCUS:
        cnt = class_counts.get(c, 0)
        classification.append(
            {
                "classification": c,
                "count": cnt,
                "pct_of_filtered": round(100 * cnt / n, 2) if n else 0.0,
            }
        )
    other = []
    for c, cnt in class_counts.most_common():
        if c in CLASS_FOCUS:
            continue
        other.append(
            {
                "classification": c,
                "count": cnt,
                "pct_of_filtered": round(100 * cnt / n, 2) if n else 0.0,
            }
        )

    themes_by_class: dict[str, list] = {c: [] for c in CLASS_FOCUS}
    for theme, tot in theme_totals.most_common():
        ctr = theme_class[theme]
        for c in CLASS_FOCUS:
            in_class = ctr.get(c, 0)
            if in_class <= 0:
                continue
            class_n = class_counts.get(c, 0)
            themes_by_class[c].append(
                {
                    "theme": theme,
                    "count_in_class": in_class,
                    "pct_of_class": round(100 * in_class / class_n, 2)
                    if class_n
                    else 0.0,
                    "theme_total": tot,
                    "pct_of_theme": round(100 * in_class / tot, 2) if tot else 0.0,
                }
            )
    for c in CLASS_FOCUS:
        themes_by_class[c].sort(key=lambda x: (-x["count_in_class"], x["theme"]))

    # Nested: area → classification focus + themes
    by_area = []
    for area in AREA_ORDER:
        area_n = area_totals.get(area, 0)
        class_rows = []
        for c in CLASS_FOCUS:
            c_n = area_class_counts[area].get(c, 0)
            themes = []
            theme_ctr = area_class_theme[area].get(c, Counter())
            for theme, t_n in theme_ctr.most_common():
                themes.append(
                    {
                        "theme": theme,
                        "count_in_area_class": t_n,
                        "pct_of_area_class": round(100 * t_n / c_n, 2) if c_n else 0.0,
                        "theme_total_filtered": theme_totals[theme],
                    }
                )
            class_rows.append(
                {
                    "classification": c,
                    "count": c_n,
                    "pct_of_area": round(100 * c_n / area_n, 2) if area_n else 0.0,
                    "themes": themes,
                }
            )
        other_area = []
        for c, cnt in area_class_counts[area].most_common():
            if c in CLASS_FOCUS:
                continue
            other_area.append(
                {
                    "classification": c,
                    "count": cnt,
                    "pct_of_area": round(100 * cnt / area_n, 2) if area_n else 0.0,
                }
            )
        by_area.append(
            {
                "area": area,
                "count": area_n,
                "pct_of_filtered": round(100 * area_n / n, 2) if n else 0.0,
                "classification_focus": class_rows,
                "classification_other": other_area,
            }
        )

    coverage = None
    if sheet_csv and sheet_csv.exists():
        coverage = jira_yes_coverage(sheet_csv, csv_path)

    return {
        "source": str(csv_path),
        "filters": {
            "U_ISSUE_TYPE": "exact match in ['Service Request', 'Defect']",
            "U_TICKET_CLASSIFICATION": sorted(CLASS_ALLOW),
            "U_PRODUCT_EXPERIENCE": "contains 'Recruiter Experience (RX)'",
            "PRODUCT_EXPERIENCE_PRODUCT": (
                "exclusive allowlist (every ;-separated token in "
                + ", ".join(sorted(PRODUCTS_ALLOW))
                + "); area = first token"
            ),
        },
        "funnel": dict(funnel),
        "n_filtered": n,
        "classification_focus": classification,
        "classification_other": other,
        "pep_distribution": [
            {"product": k, "count": v} for k, v in pep_counts.most_common()
        ],
        "themes_by_class": themes_by_class,
        "theme_totals": [
            {"theme": t, "count": c} for t, c in theme_totals.most_common()
        ],
        "by_area": by_area,
        "jira_yes_coverage": coverage,
    }


def jira_yes_coverage(sheet_csv: Path, all_fields_csv: Path) -> dict:
    """How many sheet RX Jira Yes cases fall in the Playbook filter."""
    yes_cases: set[str] = set()
    yes_rows = 0
    sheet_pep_allow = 0
    with sheet_csv.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if g(r, "PRODUCT_EXPERIENCE") != "Recruiter Experience (RX)":
                continue
            if g(r, "JIRA_CREATED") != "Yes":
                continue
            yes_rows += 1
            yes_cases.add(g(r, "CASE_NUMBER"))
            if pep_only_allowed(g(r, "PRODUCT_EXPERIENCE_PRODUCT")):
                sheet_pep_allow += 1

    all_by_num: dict[str, dict] = {}
    with all_fields_csv.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            all_by_num[g(r, "NUMBER")] = r

    funnel = Counter()
    for cn in yes_cases:
        r = all_by_num.get(cn)
        if not r:
            funnel["missing_from_all_fields"] += 1
            continue
        funnel["found_in_all_fields"] += 1
        if not issue_type_ok(g(r, "U_ISSUE_TYPE")):
            funnel["not_sr_or_defect"] += 1
            continue
        funnel["sr_or_defect"] += 1
        funnel[f"type_{g(r, 'U_ISSUE_TYPE')}"] += 1
        if g(r, "U_TICKET_CLASSIFICATION") not in CLASS_ALLOW:
            funnel["class_not_allowed"] += 1
            continue
        funnel["class_ok"] += 1
        if "Recruiter Experience (RX)" not in g(r, "U_PRODUCT_EXPERIENCE"):
            funnel["not_rx_u_product_experience"] += 1
            continue
        funnel["rx_ok"] += 1
        if not pep_only_allowed(g(r, "PRODUCT_EXPERIENCE_PRODUCT")):
            funnel["pep_not_allowlist"] += 1
            continue
        funnel["in_playbook_filter"] += 1

    return {
        "sheet_rx_jira_yes_rows": yes_rows,
        "sheet_rx_jira_yes_unique_cases": len(yes_cases),
        "sheet_yes_with_crm_pep_allowlist": sheet_pep_allow,
        "funnel_unique_cases": dict(funnel),
        "note": (
            "Playbook n_filtered includes U_ISSUE_TYPE in {Service Request, Defect} "
            "with allowed ticket classification, RX, and CRM PEP allowlist "
            "(Jira Yes and No). Other issue types (Issue/Question, Change Request, …) "
            "remain outside this cut."
        ),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, required=True, help="All-fields CSV")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--sheet-csv",
        type=Path,
        default=None,
        help="Sheet export for RX Jira Yes coverage check",
    )
    args = ap.parse_args()
    data = analyze(args.csv, args.sheet_csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2))
    cov = data.get("jira_yes_coverage") or {}
    print(
        f"wrote {args.out} n_filtered={data['n_filtered']} "
        f"areas={len(data['by_area'])} "
        f"jira_yes_in_filter={cov.get('funnel_unique_cases', {}).get('in_playbook_filter', 'n/a')}"
    )


if __name__ == "__main__":
    main()
