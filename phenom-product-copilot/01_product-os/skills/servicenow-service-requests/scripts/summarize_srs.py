#!/usr/bin/env python3
"""Summarize ServiceNow service requests CSV exported from the canonical sheet.

Sheet-only: reads local CSV; prints distributions. Does not call external APIs.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = [
    "CASE_NUMBER",
    "SHORT_DESCRIPTION",
    "DESCRIPTION",
    "STATUS",
    "STATUS_CODE",
    "SUB_STATUS",
    "JIRA_CREATED",
    "JIRA_KEY_COUNT",
    "JIRA_CASE_KEYS",
    "PRODUCT_EXPERIENCE_PRODUCT",
    "PRODUCT_EXPERIENCE",
    "CREATED_ON_UTC",
    "CREATED_ON_HKT",
    "CLIENT_NAME",
]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise SystemExit(f"No header row in {path}")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise SystemExit(
                f"CSV missing expected columns {missing}. Found: {list(reader.fieldnames)}"
            )
        return [{k: (row.get(k) or "").strip() for k in REQUIRED_COLUMNS} for row in reader]


def blank(v: str) -> str:
    return v if v else "(blank)"


def print_counter(title: str, counter: Counter, total: int, limit: int | None = None) -> None:
    print(f"\n## {title}")
    items = counter.most_common(limit)
    for key, n in items:
        pct = (100.0 * n / total) if total else 0.0
        print(f"{n:7d}  {pct:6.2f}%  {key}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        required=True,
        help="Path to all-service-requests.csv exported from the canonical sheet",
    )
    parser.add_argument(
        "--product-experience",
        default=None,
        help="Optional exact filter on PRODUCT_EXPERIENCE",
    )
    parser.add_argument(
        "--product-experience-product-prefix",
        default=None,
        help="Optional prefix filter on PRODUCT_EXPERIENCE_PRODUCT (e.g. 'CRM -')",
    )
    parser.add_argument("--top", type=int, default=40, help="Max rows per frequency table")
    args = parser.parse_args()

    if not args.csv.exists():
        print(
            f"Missing CSV: {args.csv}\n"
            "Export the canonical sheet (File → Download → CSV) to this path. "
            "See 01_product-os/knowledge/servicenow-service-requests/data/README.md",
            file=sys.stderr,
        )
        return 1

    rows = load_rows(args.csv)
    if args.product_experience is not None:
        rows = [r for r in rows if r["PRODUCT_EXPERIENCE"] == args.product_experience]
    if args.product_experience_product_prefix is not None:
        prefix = args.product_experience_product_prefix
        rows = [r for r in rows if r["PRODUCT_EXPERIENCE_PRODUCT"].startswith(prefix)]

    total = len(rows)
    dates = [r["CREATED_ON_UTC"][:10] for r in rows if r["CREATED_ON_UTC"][:10]]
    cases = [r["CASE_NUMBER"] for r in rows if r["CASE_NUMBER"]]

    print("# Service request summary (sheet CSV only)")
    print(f"file: {args.csv}")
    print(f"rows: {total}")
    print(f"distinct CASE_NUMBER: {len(set(cases))}")
    if dates:
        print(f"CREATED_ON_UTC date span: {min(dates)} → {max(dates)}")
    else:
        print("CREATED_ON_UTC date span: (none)")
    if args.product_experience is not None:
        print(f"filter PRODUCT_EXPERIENCE == {args.product_experience!r}")
    if args.product_experience_product_prefix is not None:
        print(
            f"filter PRODUCT_EXPERIENCE_PRODUCT startswith "
            f"{args.product_experience_product_prefix!r}"
        )

    print_counter(
        "PRODUCT_EXPERIENCE",
        Counter(blank(r["PRODUCT_EXPERIENCE"]) for r in rows),
        total,
        args.top,
    )
    print_counter(
        "PRODUCT_EXPERIENCE_PRODUCT",
        Counter(blank(r["PRODUCT_EXPERIENCE_PRODUCT"]) for r in rows),
        total,
        args.top,
    )
    print_counter("STATUS", Counter(blank(r["STATUS"]) for r in rows), total, args.top)
    print_counter("SUB_STATUS", Counter(blank(r["SUB_STATUS"]) for r in rows), total, args.top)
    print_counter(
        "JIRA_CREATED", Counter(blank(r["JIRA_CREATED"]) for r in rows), total, args.top
    )
    print_counter(
        "CLIENT_NAME (top)",
        Counter(blank(r["CLIENT_NAME"]) for r in rows),
        total,
        min(args.top, 25),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
