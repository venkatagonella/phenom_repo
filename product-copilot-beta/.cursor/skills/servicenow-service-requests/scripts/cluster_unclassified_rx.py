#!/usr/bin/env python3
"""Cluster unclassified RX SRs (TF-IDF + MiniBatchKMeans), then report coverage
after applying base + cluster_v1 phrase rules.

Does not invent themes for residual clusters — only reports them for review.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rx_theme_rules import (  # noqa: E402
    BASE_THEME_RULES,
    CLUSTER_V1_THEME_RULES,
    UNCLASSIFIED,
    classify_theme,
    classify_theme_with_source,
)


def g(r, k):
    return (r.get(k) or "").strip()


def load_rx(csv_path: Path, jira_values=("Yes", "No")):
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [
        r
        for r in rows
        if g(r, "PRODUCT_EXPERIENCE") == "Recruiter Experience (RX)"
        and g(r, "JIRA_CREATED") in jira_values
    ]


def cluster_unclassified(rows, n_clusters=25, top_terms=8, examples_per=8):
    """Cluster rows that are unclassified under BASE rules only."""
    from rx_theme_rules import _compile

    base_compiled = _compile(BASE_THEME_RULES)

    def base_only(short, desc):
        for text in (short, f"{short}\n{desc}" if desc else short):
            if not text:
                continue
            for name, regs in base_compiled:
                for rgx in regs:
                    if rgx.search(text):
                        return name
        return UNCLASSIFIED

    unc = []
    for r in rows:
        theme = base_only(g(r, "SHORT_DESCRIPTION"), g(r, "DESCRIPTION"))
        if theme == UNCLASSIFIED:
            text = (g(r, "SHORT_DESCRIPTION") + "\n" + g(r, "DESCRIPTION")).strip()
            if text:
                unc.append((r, text))

    if len(unc) < n_clusters:
        n_clusters = max(2, len(unc) // 5) if len(unc) >= 10 else max(1, len(unc))

    texts = [t for _, t in unc]
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=12000,
        ngram_range=(1, 2),
        min_df=2,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(texts)
    km = MiniBatchKMeans(
        n_clusters=n_clusters, random_state=42, batch_size=512, n_init=10
    )
    labels = km.fit_predict(X)
    terms = vectorizer.get_feature_names_out()

    clusters = []
    for cid in range(n_clusters):
        idxs = [i for i, lab in enumerate(labels) if lab == cid]
        if not idxs:
            continue
        center = km.cluster_centers_[cid]
        top_idx = center.argsort()[::-1][:top_terms]
        top = [terms[j] for j in top_idx if center[j] > 0]
        examples = []
        for i in idxs[:examples_per]:
            r, _ = unc[i]
            examples.append(
                {
                    "CASE_NUMBER": g(r, "CASE_NUMBER"),
                    "JIRA_CREATED": g(r, "JIRA_CREATED"),
                    "SHORT_DESCRIPTION": g(r, "SHORT_DESCRIPTION")[:140],
                }
            )
        clusters.append(
            {
                "cluster_id": cid,
                "size": len(idxs),
                "share_of_unclassified": round(100 * len(idxs) / len(unc), 2),
                "top_terms": top,
                "examples": examples,
            }
        )
    clusters.sort(key=lambda c: -c["size"])
    return {
        "unclassified_under_base_only": len(unc),
        "n_clusters": n_clusters,
        "clusters": clusters,
    }


def coverage_report(rows):
    by_source = Counter()
    by_theme = Counter()
    by_jira_theme = defaultdict(Counter)
    for r in rows:
        theme, source = classify_theme_with_source(
            g(r, "SHORT_DESCRIPTION"), g(r, "DESCRIPTION")
        )
        by_source[source] += 1
        by_theme[theme] += 1
        by_jira_theme[g(r, "JIRA_CREATED")][theme] += 1
    n = len(rows)
    return {
        "n": n,
        "by_source": dict(by_source),
        "classified_pct": round(100 * (n - by_theme.get(UNCLASSIFIED, 0)) / n, 2),
        "unclassified_pct": round(100 * by_theme.get(UNCLASSIFIED, 0) / n, 2),
        "themes": by_theme.most_common(),
        "by_jira": {
            j: {"n": sum(c.values()), "themes": c.most_common()}
            for j, c in by_jira_theme.items()
        },
        "base_rule_count": sum(len(p) for _, p in BASE_THEME_RULES),
        "cluster_v1_rule_count": sum(len(p) for _, p in CLUSTER_V1_THEME_RULES),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--clusters", type=int, default=25)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write JSON report (clusters + coverage)",
    )
    args = ap.parse_args()
    rows = load_rx(args.csv)
    clusters = cluster_unclassified(rows, n_clusters=args.clusters)
    coverage = coverage_report(rows)
    report = {
        "method": (
            "1) Classify with base phrase rules. "
            "2) TF-IDF MiniBatchKMeans on residual unclassified (base-only). "
            "3) Human/agent derives high-confidence CLUSTER_V1 phrase rules from "
            "top clusters mapped to existing themes (or one new how-to theme). "
            "4) Re-classify with base + cluster_v1. Residual stays Unclassified."
        ),
        "clusters_of_base_unclassified": clusters,
        "coverage_after_base_plus_cluster_v1": coverage,
    }
    print(json.dumps(
        {
            "rx_n": coverage["n"],
            "classified_pct": coverage["classified_pct"],
            "unclassified_pct": coverage["unclassified_pct"],
            "by_source": coverage["by_source"],
            "top_themes": coverage["themes"][:12],
            "base_unclassified_clustered": clusters["unclassified_under_base_only"],
            "top_clusters": [
                {"id": c["cluster_id"], "size": c["size"], "terms": c["top_terms"][:6]}
                for c in clusters["clusters"][:10]
            ],
        },
        indent=2,
    ))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2))
        print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
