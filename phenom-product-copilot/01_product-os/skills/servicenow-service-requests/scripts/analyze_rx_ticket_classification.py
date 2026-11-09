#!/usr/bin/env python3
"""Filter all-fields ServiceNow CSV → theme × ticket-classification counts.

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

# Accordion sections (focus four). Order preserved for HTML.
CLASS_FOCUS = [
    "Product & Knowledge Issues",
    "Configuration Issues",
    "User Experience Issues",
    "Code Issues",
]

PRODUCTS_ALLOW = frozenset(
    {
        "CRM - Core",
        "CRM - Profile",
        "CRM - Automation",
        "CRM - Messaging and Campaigns",
    }
)


def g(r, k):
    return (r.get(k) or "").strip()


def pep_parts(s: str) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in re.split(r"[;|]", s) if x.strip()]


def pep_only_allowed(s: str) -> bool:
    parts = pep_parts(s)
    return bool(parts) and all(x in PRODUCTS_ALLOW for x in parts)


def analyze(csv_path: Path) -> dict:
    funnel = Counter()
    class_counts = Counter()
    pep_counts = Counter()
    theme_totals = Counter()
    theme_class: dict[str, Counter] = defaultdict(Counter)

    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            funnel["all"] += 1
            if "Service Request" not in g(r, "U_ISSUE_TYPE"):
                continue
            funnel["issue_type"] += 1
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

            theme = classify_theme(g(r, "SHORT_DESCRIPTION"), g(r, "DESCRIPTION"))
            if theme == "Unclassified / other":
                funnel["unclassified_excluded"] += 1
                continue
            funnel["classified"] += 1

            class_counts[cls] += 1
            pep_counts[pep] += 1
            theme_totals[theme] += 1
            theme_class[theme][cls] += 1

    n = funnel["classified"]
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
                    "pct_of_class": round(100 * in_class / class_n, 2) if class_n else 0.0,
                    "theme_total": tot,
                    "pct_of_theme": round(100 * in_class / tot, 2) if tot else 0.0,
                }
            )
    for c in CLASS_FOCUS:
        themes_by_class[c].sort(key=lambda x: (-x["count_in_class"], x["theme"]))

    return {
        "source": str(csv_path),
        "filters": {
            "U_ISSUE_TYPE": "contains 'Service Request'",
            "U_TICKET_CLASSIFICATION": sorted(CLASS_ALLOW),
            "U_PRODUCT_EXPERIENCE": "contains 'Recruiter Experience (RX)'",
            "PRODUCT_EXPERIENCE_PRODUCT": (
                "exclusive allowlist (every ;-separated token in "
                + ", ".join(sorted(PRODUCTS_ALLOW))
                + ")"
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
        f"themes={len(data['theme_totals'])}"
    )


if __name__ == "__main__":
    main()
