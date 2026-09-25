#!/usr/bin/env python3
"""Build RX Jira Yes vs No HTML theme report using rx_theme_rules classifier.

Playbook tab uses ticket-classification snapshot (option A): themes with ≥1 row
in each U_TICKET_CLASSIFICATION, existing reduce bullets only.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rx_theme_playbook import (  # noqa: E402
    AREA_BLURB,
    AREA_ORDER,
    PRIORITY_ORDER,
    THEME_AREA,
    THEME_PLAYBOOK,
)
from rx_theme_rules import UNCLASSIFIED, classify_theme_with_source  # noqa: E402

CLASS_FOCUS = [
    "Product & Knowledge Issues",
    "Code Issues",
    "Configuration Issues",
    "User Experience Issues",
]

CLASS_SLUG = {
    "Product & Knowledge Issues": "class-product-knowledge",
    "Configuration Issues": "class-configuration",
    "User Experience Issues": "class-user-experience",
    "Code Issues": "class-code",
}

AREA_SLUG = {
    "CRM Core": "area-crm-core",
    "CRM Profile": "area-crm-profile",
    "CRM Messaging": "area-crm-messaging",
    "CRM Automations": "area-crm-automations",
}


def g(r, k):
    return (r.get(k) or "").strip()


def esc(s):
    return html.escape(str(s))


def bar(pct, max_pct):
    w = min(100, round(100 * pct / max_pct, 1)) if max_pct else 0
    return f'<div class="bar"><span style="width:{w}%"></span></div>'


def table_rows(rows, headers):
    pct_idxs = [i for i, h in enumerate(headers) if h.startswith("%")]
    max_pct = max((r[pct_idxs[0]] for r in rows), default=1) if pct_idxs else 1
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = []
    for r in rows:
        cells = []
        for i, val in enumerate(r):
            hdr = headers[i]
            if hdr.startswith("%") and isinstance(val, (int, float)):
                cells.append(
                    f'<td class="num">{esc(f"{val:.1f}%")}'
                    f"{bar(val, max_pct) if i == pct_idxs[0] else ''}</td>"
                )
            elif hdr.startswith("Δ") and isinstance(val, (int, float)):
                cls = "up" if val > 0 else ("down" if val < 0 else "")
                cells.append(f'<td class="num {cls}">{esc(f"{val:+.1f} pp")}</td>')
            elif isinstance(val, int) and i > 0:
                cells.append(f'<td class="num">{esc(f"{val:,}")}</td>')
            else:
                cells.append(f"<td>{esc(val)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def analyze(subset):
    n = len(subset)
    themes = Counter()
    sources = Counter()
    pep = Counter()
    examples = defaultdict(list)
    for r in subset:
        theme, source = classify_theme_with_source(
            g(r, "SHORT_DESCRIPTION"), g(r, "DESCRIPTION")
        )
        themes[theme] += 1
        sources[source] += 1
        pep[g(r, "PRODUCT_EXPERIENCE_PRODUCT") or "(blank)"] += 1
        if len(examples[theme]) < 3:
            examples[theme].append(
                (
                    g(r, "CASE_NUMBER"),
                    g(r, "PRODUCT_EXPERIENCE_PRODUCT") or "(blank)",
                    g(r, "SHORT_DESCRIPTION")[:100],
                    source,
                )
            )
    return {
        "n": n,
        "themes": [(t, c, round(100 * c / n, 2)) for t, c in themes.most_common()],
        "sources": dict(sources),
        "pep": [(k, v, round(100 * v / n, 2)) for k, v in pep.most_common()],
        "examples": examples,
        "classified_pct": round(100 * (n - themes.get(UNCLASSIFIED, 0)) / n, 2),
    }


def theme_cards(block):
    max_p = block["themes"][0][2] if block["themes"] else 1
    cards = []
    for t, c, p in block["themes"]:
        ex = block["examples"].get(t, [])
        ex_html = "".join(
            f"<li><code>{esc(case)}</code> · {esc(pep)} · "
            f"<em>{esc(src)}</em> · {esc(title)}</li>"
            for case, pep, title, src in ex
        )
        cards.append(
            f"""<article class="theme-card">
          <div class="theme-head"><h3>{esc(t)}</h3>
          <div class="theme-nums"><b>{c:,}</b><span>{p:.1f}%</span></div></div>
          {bar(p, max_p)}<ul class="examples">{ex_html}</ul></article>"""
        )
    return "".join(cards)


def _reduce_block(theme: str) -> str:
    pb = THEME_PLAYBOOK.get(theme)
    if not pb:
        return "<p class='muted'>No reduce actions in playbook for this theme.</p>"
    reduce_items = pb.get("reduce") or []
    if isinstance(reduce_items, str):
        reduce_items = [reduce_items]
    reduce_html = "".join(f"<li>{esc(x)}</li>" for x in reduce_items)
    return (
        f"<dl class='pb'><dt>To reduce feedback %</dt>"
        f"<dd><ul class='reduce-list'>{reduce_html}</ul></dd></dl>"
    )


def reduce_only_card(
    theme: str,
    count_in_class: int,
    pct_of_class: float,
    theme_total: int,
    pct_of_theme: float,
    max_pct: float,
) -> str:
    """Theme card: counts from snapshot + existing playbook reduce bullets only."""
    pri = " priority" if theme in PRIORITY_ORDER else ""
    return f"""<article class="theme-card playbook-card{pri}">
  <div class="theme-head"><h3>{esc(theme)}</h3>
  <div class="theme-nums"><b>{count_in_class:,}</b>
  <span>{pct_of_class:.1f}% of this class</span></div></div>
  <div class="pack">Theme total in filter: {theme_total:,} ·
  {pct_of_theme:.1f}% of this theme’s filtered rows are in this class</div>
  {bar(pct_of_class, max_pct)}{_reduce_block(theme)}</article>"""


def product_area_card(
    theme: str, count: int, pct_of_filtered: float, max_pct: float
) -> str:
    """Theme card for CRM Core/Profile/Messaging/Automations grouping."""
    pri = " priority" if theme in PRIORITY_ORDER else ""
    return f"""<article class="theme-card playbook-card{pri}">
  <div class="theme-head"><h3>{esc(theme)}</h3>
  <div class="theme-nums"><b>{count:,}</b>
  <span>{pct_of_filtered:.1f}% of filtered</span></div></div>
  {bar(pct_of_filtered, max_pct)}{_reduce_block(theme)}</article>"""


def playbook_by_product_area(snapshot: dict) -> str:
    """CRM Core / Profile / Messaging / Automations — filtered theme totals."""
    n = snapshot["n_filtered"]
    by_area: dict[str, list] = {a: [] for a in AREA_ORDER}
    unmapped = []
    for row in snapshot.get("theme_totals") or []:
        theme = row["theme"]
        count = row["count"]
        pct = round(100 * count / n, 2) if n else 0.0
        area = THEME_AREA.get(theme)
        item = (theme, count, pct)
        if area in by_area:
            by_area[area].append(item)
        else:
            unmapped.append(item)

    sections = []
    for i, area in enumerate(AREA_ORDER):
        rows = by_area[area]
        if not rows:
            continue
        area_n = sum(c for _, c, _ in rows)
        area_pct = round(100 * area_n / n, 1) if n else 0.0
        max_pct = max((p for _, _, p in rows), default=1)
        cards = "".join(
            product_area_card(t, c, p, max_pct) for t, c, p in rows
        )
        aid = AREA_SLUG[area]
        open_attr = " open" if i == 0 else ""
        blurb = AREA_BLURB.get(area, "")
        sections.append(
            f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(area)}</span>
    <span class="area-stats"><b>{area_n:,}</b> SRs · {area_pct}% of filtered
    · {len(rows)} theme{"s" if len(rows) != 1 else ""}</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <p class="area-blurb">{esc(blurb)}</p>
    <div class="theme-grid playbook">{cards}</div>
  </div>
</details>"""
        )
    if unmapped:
        max_pct = max((p for _, _, p in unmapped), default=1)
        cards = "".join(
            product_area_card(t, c, p, max_pct) for t, c, p in unmapped
        )
        sections.append(
            f"""<details class="area-accordion" id="area-unmapped">
  <summary class="area-summary">
    <span class="area-title">Unmapped</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <div class="theme-grid playbook">{cards}</div>
  </div>
</details>"""
        )
    return "".join(sections)


def area_class_theme_card(
    theme: str,
    count_in_area_class: int,
    pct_of_area_class: float,
    theme_total_filtered: int,
    max_pct: float,
) -> str:
    pri = " priority" if theme in PRIORITY_ORDER else ""
    return f"""<article class="theme-card playbook-card{pri}">
  <div class="theme-head"><h3>{esc(theme)}</h3>
  <div class="theme-nums"><b>{count_in_area_class:,}</b>
  <span>{pct_of_area_class:.1f}% of this class in area</span></div></div>
  <div class="pack">Theme total in full filter: {theme_total_filtered:,}</div>
  {bar(pct_of_area_class, max_pct)}{_reduce_block(theme)}</article>"""


def playbook_by_area_nested(snapshot: dict) -> str:
    """CRM area accordion → classification % table → themes per class."""
    sections = []
    for i, area_block in enumerate(snapshot.get("by_area") or []):
        area = area_block["area"]
        area_n = area_block["count"]
        area_pct = area_block["pct_of_filtered"]
        aid = AREA_SLUG.get(area, "area-" + area.lower().replace(" ", "-"))
        open_attr = " open" if i == 0 else ""

        class_table_rows = [
            (c["classification"], c["count"], c["pct_of_area"])
            for c in area_block["classification_focus"]
        ]
        class_table = table_rows(
            class_table_rows,
            ["U_TICKET_CLASSIFICATION", "Rows", "% of area"],
        )
        other_bits = []
        for o in area_block.get("classification_other") or []:
            other_bits.append(
                f"{o['classification']} {o['count']} ({o['pct_of_area']:.1f}%)"
            )
        other_html = (
            f'<p class="area-blurb">Also in this area: {esc("; ".join(other_bits))}</p>'
            if other_bits
            else ""
        )

        nested = []
        for cblock in area_block["classification_focus"]:
            cls = cblock["classification"]
            c_n = cblock["count"]
            c_pct = cblock["pct_of_area"]
            themes = cblock.get("themes") or []
            if c_n == 0 and not themes:
                nested.append(
                    f"""<div class="nested-class empty">
  <h3>{esc(cls)} <span class="pill">0 · 0%</span></h3>
  <p class="muted">No filtered rows in this classification for {esc(area)}.</p>
</div>"""
                )
                continue
            max_pct = max((t["pct_of_area_class"] for t in themes), default=1)
            cards = "".join(
                area_class_theme_card(
                    t["theme"],
                    t["count_in_area_class"],
                    t["pct_of_area_class"],
                    t["theme_total_filtered"],
                    max_pct,
                )
                for t in themes
            )
            nested.append(
                f"""<div class="nested-class">
  <h3>{esc(cls)} <span class="pill pill-yes">{c_n:,} · {c_pct:.1f}% of area</span></h3>
  <div class="theme-grid playbook">{cards}</div>
</div>"""
            )

        sections.append(
            f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(area)}</span>
    <span class="area-stats"><b>{area_n:,}</b> SRs · {area_pct:.1f}% of filtered</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <h3 class="subhead">Feedback % by ticket classification — {esc(area)}</h3>
    {class_table}
    {other_html}
    {"".join(nested)}
  </div>
</details>"""
        )
    return "".join(sections)


def jira_yes_coverage_html(snapshot: dict) -> str:
    cov = snapshot.get("jira_yes_coverage")
    if not cov:
        return ""
    funnel = cov.get("funnel_unique_cases") or {}
    yes_n = cov.get("sheet_rx_jira_yes_rows", 0)
    uniq = cov.get("sheet_rx_jira_yes_unique_cases", 0)
    in_filter = funnel.get("in_playbook_filter", 0)
    found = funnel.get("found_in_all_fields", 0)
    not_sr = funnel.get("not_sr_or_defect", 0)
    pep_fail = funnel.get("pep_not_allowlist", 0)
    class_fail = funnel.get("class_not_allowed", 0)
    missing = funnel.get("missing_from_all_fields", 0)
    sheet_pep = cov.get("sheet_yes_with_crm_pep_allowlist", 0)
    sr_n = funnel.get("type_Service Request", 0)
    def_n = funnel.get("type_Defect", 0)
    pct_in = round(100 * in_filter / uniq, 1) if uniq else 0.0
    return f"""
  <div class="alert">
    <strong>Jira Yes coverage check (sheet RX · JIRA_CREATED=Yes):</strong>
    {yes_n:,} rows / {uniq:,} unique cases.
    In Playbook filter (Service Request + Defect): <b>{in_filter:,}</b> ({pct_in}% of unique Yes).
    Of those in filter: Service Request {sr_n:,}, Defect {def_n:,}.
    Not covered: {uniq - in_filter:,}.
    Breakdown of unique Yes: found in all-fields {found:,};
    not SR/Defect {not_sr:,}; classification not in allowlist {class_fail:,};
    PEP outside CRM Core/Profile/Automation/Messaging {pep_fail:,};
    missing from all-fields {missing:,}.
    Sheet Yes with CRM PEP allowlist alone (any issue type): {sheet_pep:,}.
    {esc(cov.get("note") or "")}
  </div>"""


def classification_pct_table(snapshot: dict) -> str:
    n = snapshot["n_filtered"]
    rows = [
        (x["classification"], x["count"], x["pct_of_filtered"])
        for x in snapshot["classification_focus"]
    ]
    other_note = ""
    if snapshot.get("classification_other"):
        bits = [
            f"{o['classification']} {o['count']} ({o['pct_of_filtered']:.1f}%)"
            for o in snapshot["classification_other"]
        ]
        other_note = (
            f'<p class="area-blurb">Also in filter (no area sub-section): '
            f'{esc("; ".join(bits))}. Ops Issues and Security-Related Issues: 0.</p>'
        )
    return (
        f"<h2>Overall feedback % by ticket classification "
        f"<span class='pill pill-yes'>n={n:,}</span></h2>"
        + table_rows(
            rows,
            ["U_TICKET_CLASSIFICATION", "Rows", "% of filtered"],
        )
        + other_note
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--csv",
        type=Path,
        required=True,
        help="Sheet CSV for Yes/No theme tabs",
    )
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--ticket-class-snapshot",
        type=Path,
        default=None,
        help="JSON from analyze_rx_ticket_classification.py (Playbook tab)",
    )
    args = ap.parse_args()

    with args.csv.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    rx = [
        r
        for r in rows
        if g(r, "PRODUCT_EXPERIENCE") == "Recruiter Experience (RX)"
        and g(r, "JIRA_CREATED") in ("Yes", "No")
    ]
    linked = sum(
        1
        for r in rows
        if g(r, "PRODUCT_EXPERIENCE") == "Recruiter Experience (RX)"
        and g(r, "JIRA_CREATED") == "Linked - key not found in JIRA"
    )
    yes = analyze([r for r in rx if g(r, "JIRA_CREATED") == "Yes"])
    no = analyze([r for r in rx if g(r, "JIRA_CREATED") == "No"])

    all_themes = []
    seen = set()
    for t, _, __ in yes["themes"] + no["themes"]:
        if t not in seen:
            seen.add(t)
            all_themes.append(t)
    ym = {t: (c, p) for t, c, p in yes["themes"]}
    nm = {t: (c, p) for t, c, p in no["themes"]}
    compare = []
    for t in all_themes:
        yc, yp = ym.get(t, (0, 0.0))
        nc, np_ = nm.get(t, (0, 0.0))
        compare.append((t, yc, yp, nc, np_, round(np_ - yp, 1)))

    snap_path = args.ticket_class_snapshot
    if snap_path is None:
        snap_path = args.out.parent / "snapshot-rx-ticket-classification.json"
    if not snap_path.exists():
        raise SystemExit(
            f"Missing ticket-class snapshot: {snap_path}\n"
            "Run analyze_rx_ticket_classification.py first."
        )
    snapshot = json.loads(snap_path.read_text())
    n_f = snapshot["n_filtered"]
    product_nav = "".join(
        f'<a href="#{AREA_SLUG[a]}" data-area="{AREA_SLUG[a]}">{esc(a)}</a>'
        for a in AREA_ORDER
        if any(b["area"] == a for b in snapshot.get("by_area") or [])
    )
    class_pct_html = classification_pct_table(snapshot)
    nested_accordions = playbook_by_area_nested(snapshot)

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RX themes — ticket classification + Jira Yes/No</title>
<style>
:root{{--bg:#f4f1ea;--ink:#1a1916;--muted:#5e594f;--card:#fffcf7;--line:#d9d2c4;--accent:#1f4d3a;--no:#7a3b2e}}
*{{box-sizing:border-box}}body{{margin:0;font-family:"IBM Plex Sans",system-ui,sans-serif;color:var(--ink);
background:radial-gradient(900px 500px at 0% 0%,#dde8e1,transparent 55%),var(--bg)}}
header{{max-width:1140px;margin:0 auto;padding:2rem 1.5rem 1rem}}
h1{{font-family:Georgia,serif;font-size:clamp(1.45rem,3vw,2rem);margin:0 0 .35rem}}
.sub{{color:var(--muted);max-width:78ch}}.stats{{display:flex;flex-wrap:wrap;gap:.65rem;margin-top:1rem}}
.stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.6rem .9rem}}
.stat b{{display:block;font-size:1.2rem;color:var(--accent)}}.stat.no b{{color:var(--no)}}
.stat span{{font-size:.75rem;color:var(--muted)}}
nav.tabs{{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:.35rem;padding:.5rem 1.5rem;
border-bottom:1px solid var(--line);background:color-mix(in srgb,var(--bg) 88%,white)}}
nav.tabs button{{border:1px solid var(--line);background:var(--card);border-radius:999px;padding:.3rem .8rem;
font:inherit;font-size:.85rem;cursor:pointer}}
nav.tabs button.active{{background:var(--accent);border-color:var(--accent);color:#fff}}
nav.tabs button.no-tab.active{{background:var(--no);border-color:var(--no)}}
main{{max-width:1140px;margin:0 auto;padding:1.1rem 1.5rem 3rem}}
section.panel{{display:none}}section.panel.active{{display:block}}
.note{{background:#fff7e6;border:1px solid #e5d2a6;border-radius:10px;padding:.75rem 1rem;margin-bottom:1rem;font-size:.9rem;color:#5a4824}}
.alert{{background:#f8ebe7;border:1px solid #e0b8ad;border-radius:10px;padding:.75rem 1rem;margin-bottom:1rem;color:#5c2f26}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:.84rem;margin-bottom:1rem}}
th,td{{padding:.4rem .55rem;border-bottom:1px solid var(--line);text-align:left}}th{{background:#efe9df}}
td.num{{white-space:nowrap}}td.up{{color:#1f4d3a}}td.down{{color:#7a3b2e}}
.bar{{height:7px;background:#e8e2d7;border-radius:99px;margin-top:4px;overflow:hidden}}
.bar span{{display:block;height:100%;background:var(--accent);border-radius:99px}}
.theme-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.65rem}}
.theme-grid.playbook{{grid-template-columns:1fr;gap:.85rem}}
.theme-card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:.75rem .9rem}}
.playbook-card.priority{{border-color:#8aab96;box-shadow:inset 3px 0 0 var(--accent)}}
.theme-head{{display:flex;justify-content:space-between;gap:.5rem}}.theme-nums{{text-align:right}}
.theme-nums b{{display:block;font-size:1.15rem;color:var(--accent)}}.theme-nums span{{font-size:.72rem;color:var(--muted)}}
.examples{{margin:.5rem 0 0;padding-left:1rem;color:var(--muted);font-size:.76rem}}
.pack{{font-size:.72rem;color:var(--muted);margin:.35rem 0 .15rem}}
.pb{{margin:.55rem 0 0;display:grid;gap:.45rem}}
.pb dt{{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--accent)}}
.pb dd{{margin:0;font-size:.86rem;line-height:1.45;color:var(--ink)}}
.reduce-list{{margin:.25rem 0 0;padding-left:1.15rem}}
.reduce-list li{{margin:.28rem 0;line-height:1.45}}
.pill{{display:inline-block;padding:.12rem .5rem;border-radius:999px;font-size:.72rem;font-weight:600;margin-left:.3rem}}
.pill-yes{{background:#dceae3;color:#1f4d3a}}.pill-no{{background:#f0ddd7;color:#7a3b2e}}
.area-toolbar{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
gap:.6rem;margin:0 0 .85rem}}
.area-nav{{display:flex;flex-wrap:wrap;gap:.4rem}}
.area-nav a,.area-actions button{{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:.28rem .75rem;font:inherit;font-size:.8rem;color:var(--ink);text-decoration:none;cursor:pointer}}
.area-nav a:hover,.area-actions button:hover{{border-color:var(--accent);color:var(--accent)}}
.area-actions{{display:flex;gap:.35rem}}
.area-accordion{{background:var(--card);border:1px solid var(--line);border-radius:12px;
margin:0 0 .65rem;overflow:hidden}}
.area-summary{{display:grid;grid-template-columns:minmax(0,1fr) auto auto;align-items:center;gap:.75rem;
padding:.85rem 1rem;cursor:pointer;list-style:none;user-select:none}}
.area-summary::-webkit-details-marker{{display:none}}
.area-summary:hover{{background:#f7f3eb}}
.area-title{{font-size:1.05rem;font-weight:700;color:var(--accent)}}
.area-stats{{font-size:.82rem;color:var(--muted);white-space:nowrap}}
.area-stats b{{color:var(--ink)}}
.area-chevron{{width:.55rem;height:.55rem;border-right:2px solid var(--muted);
border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .15s ease;
margin-right:.15rem;flex-shrink:0}}
.area-accordion[open] .area-chevron{{transform:rotate(225deg);margin-top:.2rem}}
.area-accordion[open] .area-summary{{border-bottom:1px solid var(--line);background:#f7f3eb}}
.area-body{{padding:.85rem 1rem 1.1rem}}
.area-blurb{{margin:0 0 .75rem;font-size:.88rem;color:var(--muted);max-width:85ch}}
.muted{{color:var(--muted);font-size:.86rem}}
.subhead{{font-size:.95rem;margin:0 0 .5rem;color:var(--ink)}}
.nested-class{{margin:1rem 0 1.25rem;padding-top:.5rem;border-top:1px solid var(--line)}}
.nested-class.empty{{opacity:.85}}
.nested-class h3{{display:flex;flex-wrap:wrap;align-items:center;gap:.4rem;margin:0 0 .55rem}}
footer{{max-width:1140px;margin:0 auto;padding:0 1.5rem 2rem;color:var(--muted);font-size:.75rem}}
h2{{font-size:1.1rem}}h3{{font-size:.95rem;margin:0}}
</style></head><body>
<header>
  <h1>RX themes — ticket classification + Jira Yes/No</h1>
  <p class="sub">Playbook tab: filtered all-fields CSV (Service Request + Defect · allowed ticket
  classifications · RX · CRM Core/Profile/Automation/Messaging exclusive) → n={n_f:,}.
  Themes via phrase rules; reduce bullets from existing playbook only.
  Other tabs: sheet Yes/No split (n={len(rx):,}).</p>
  <div class="stats">
    <div class="stat"><b>{n_f:,}</b><span>Filtered (Playbook)</span></div>
    <div class="stat"><b>{len(rx):,}</b><span>RX Yes+No (other tabs)</span></div>
    <div class="stat"><b>{yes['n']:,}</b><span>Jira Yes · {yes['classified_pct']:.1f}% classified</span></div>
    <div class="stat no"><b>{no['n']:,}</b><span>Jira No · {no['classified_pct']:.1f}% classified</span></div>
    <div class="stat"><b>{linked}</b><span>Linked key-not-found (excluded)</span></div>
  </div>
</header>
<nav class="tabs" id="tabs">
  <button data-tab="playbook" class="active">Playbook · ticket class</button>
  <button data-tab="compare">Yes vs No</button>
  <button data-tab="yes-themes">Yes · themes</button>
  <button data-tab="yes-products">Yes · products</button>
  <button data-tab="no-themes" class="no-tab">No · themes</button>
  <button data-tab="no-products" class="no-tab">No · products</button>
</nav>
<main>
<section class="panel active" id="playbook">
  <div class="note">Filters: <code>U_ISSUE_TYPE</code> ∈ {{Service Request, Defect}};
  <code>U_TICKET_CLASSIFICATION</code> in the 7 allowed values;
  <code>U_PRODUCT_EXPERIENCE</code> contains Recruiter Experience (RX);
  <code>PRODUCT_EXPERIENCE_PRODUCT</code> exclusive allowlist
  (CRM - Core, CRM - Profile, CRM - Automation, CRM - Messaging and Campaigns);
  area = first PEP token. Snapshot: <code>snapshot-rx-ticket-classification.json</code>.
  Reduce bullets from existing playbook only.</div>
  {class_pct_html}
  <h2>CRM areas → ticket classification → reduce feedback %</h2>
  <div class="area-toolbar">
    <nav class="area-nav" aria-label="Product areas">{product_nav}</nav>
    <div class="area-actions">
      <button type="button" id="expand-areas">Expand all</button>
      <button type="button" id="collapse-areas">Collapse all</button>
    </div>
  </div>
  <div class="area-accordions" id="area-accordions">
  {nested_accordions}
  </div>
</section>
<section class="panel" id="compare">
  <div class="note">Δ pp = No% − Yes%. Positive = more common when Jira was <em>not</em> created.
  Sources: base / cluster_v1 / unclassified. Population: sheet RX Yes+No (not the Playbook filter).</div>
  <h2>Theme comparison</h2>
  {table_rows(compare, ["Theme","Yes rows","% of Yes","No rows","% of No","Δ pp (No − Yes)"])}
  <h2>Match sources</h2>
  {table_rows([
    ("Jira Yes — base", yes["sources"].get("base",0), round(100*yes["sources"].get("base",0)/yes["n"],1)),
    ("Jira Yes — cluster_v1", yes["sources"].get("cluster_v1",0), round(100*yes["sources"].get("cluster_v1",0)/yes["n"],1)),
    ("Jira Yes — unclassified", yes["sources"].get("unclassified",0), round(100*yes["sources"].get("unclassified",0)/yes["n"],1)),
    ("Jira No — base", no["sources"].get("base",0), round(100*no["sources"].get("base",0)/no["n"],1)),
    ("Jira No — cluster_v1", no["sources"].get("cluster_v1",0), round(100*no["sources"].get("cluster_v1",0)/no["n"],1)),
    ("Jira No — unclassified", no["sources"].get("unclassified",0), round(100*no["sources"].get("unclassified",0)/no["n"],1)),
  ], ["Cohort / source","Rows","% of cohort"])}
  <div class="alert">For Jira No, <code>PRODUCT_EXPERIENCE_PRODUCT</code> is blank on essentially all rows (product label comes from Jira in the sheet SQL).</div>
</section>
<section class="panel" id="yes-themes">
  <h2>Key themes <span class="pill pill-yes">Jira Yes · n={yes['n']:,} · {yes['classified_pct']:.1f}% classified</span></h2>
  <div class="theme-grid">{theme_cards(yes)}</div>
</section>
<section class="panel" id="yes-products">
  <h2>PRODUCT_EXPERIENCE_PRODUCT <span class="pill pill-yes">Jira Yes</span></h2>
  {table_rows([(k,v,p) for k,v,p in yes["pep"]], ["PRODUCT_EXPERIENCE_PRODUCT","Rows","% of Yes"])}
</section>
<section class="panel" id="no-themes">
  <h2>Key themes <span class="pill pill-no">Jira No · n={no['n']:,} · {no['classified_pct']:.1f}% classified</span></h2>
  <div class="theme-grid">{theme_cards(no)}</div>
</section>
<section class="panel" id="no-products">
  <h2>PRODUCT_EXPERIENCE_PRODUCT <span class="pill pill-no">Jira No</span></h2>
  {table_rows([(k,v,p) for k,v,p in no["pep"]], ["PRODUCT_EXPERIENCE_PRODUCT","Rows","% of No"])}
</section>
</main>
<footer>
Classifier: scripts/rx_theme_rules.py. Playbook reduce: scripts/rx_theme_playbook.py.<br/>
Ticket-class filter: scripts/analyze_rx_ticket_classification.py → snapshot-rx-ticket-classification.json.<br/>
Sheet-only. No invented reduce actions or classifications.
</footer>
<script>
document.querySelectorAll('#tabs button').forEach(btn=>btn.addEventListener('click',()=>{{
  document.querySelectorAll('#tabs button').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('section.panel').forEach(p=>p.classList.remove('active'));
  btn.classList.add('active'); document.getElementById(btn.dataset.tab).classList.add('active');
}}));
const areaAccordions = () => [...document.querySelectorAll('#area-accordions details.area-accordion')];
document.getElementById('expand-areas')?.addEventListener('click', () => {{
  areaAccordions().forEach(d => {{ d.open = true; }});
}});
document.getElementById('collapse-areas')?.addEventListener('click', () => {{
  areaAccordions().forEach(d => {{ d.open = false; }});
}});
document.querySelectorAll('.area-nav a[data-area]').forEach(a => a.addEventListener('click', e => {{
  e.preventDefault();
  const id = a.dataset.area;
  const target = document.getElementById(id);
  if (!target) return;
  areaAccordions().forEach(d => {{ d.open = d === target; }});
  target.open = true;
  target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}));
</script></body></html>"""
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(doc)
    alt = args.out.parent / "jira-yes-keywords-product-areas.html"
    alt.write_text(doc)
    print(
        f"wrote {args.out} filtered={n_f} "
        f"yes_classified={yes['classified_pct']}% "
        f"no_classified={no['classified_pct']}%"
    )


if __name__ == "__main__":
    main()
