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
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)

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
    "Configuration Issues",
    "User Experience Issues",
    "Code Issues",
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


def product_experience(r) -> str:
    """All-fields export uses U_PRODUCT_EXPERIENCE; older sheet used PRODUCT_EXPERIENCE."""
    return g(r, "PRODUCT_EXPERIENCE") or g(r, "U_PRODUCT_EXPERIENCE")


def is_rx(r) -> bool:
    return "Recruiter Experience (RX)" in product_experience(r)


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


def theme_slug(theme: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-")
    return s or "theme"


def _reduce_block(theme: str, count: int = 0, slug: str = "") -> str:
    pb = THEME_PLAYBOOK.get(theme)
    if not pb:
        return "<p class='muted'>No reduce actions in playbook for this theme.</p>"
    problem = (pb.get("problem") or "").strip()
    reduce_items = pb.get("reduce") or []
    if isinstance(reduce_items, str):
        reduce_items = [reduce_items]
    slug = slug or theme_slug(theme)
    parts = []
    if problem:
        parts.append(
            f"<p class='theme-problem'><span class='lbl'>Problem</span> {esc(problem)}</p>"
        )
    if reduce_items:
        count_link = (
            f'<a class="sr-count-link" href="#playbook-srs" data-theme-slug="{esc(slug)}" '
            f'data-theme="{esc(theme)}" title="Open {count:,} Service Requests '
            f'(Jira Yes + No) for this theme">'
            f"{count:,} SRs</a>"
            if count
            else ""
        )
        lis = []
        for x in reduce_items:
            if count_link:
                lis.append(
                    f"<li><span class='reduce-text'>{esc(x)}</span> "
                    f"<span class='sr-count'>{count_link}</span></li>"
                )
            else:
                lis.append(f"<li>{esc(x)}</li>")
        reduce_html = "".join(lis)
        parts.append(
            "<dl class='pb'><dt>What to do in Phenom "
            f"{count_link}</dt>"
            f"<dd><ul class='reduce-list'>{reduce_html}</ul></dd></dl>"
        )
    return "".join(parts) or "<p class='muted'>No actions listed.</p>"


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
  {bar(pct_of_class, max_pct)}{_reduce_block(theme, theme_total)}</article>"""


def product_area_card(
    theme: str,
    count: int,
    pct_of_filtered: float,
    jira_yes: int,
    jira_no: int,
    max_pct: float,
    slug: str = "",
) -> str:
    """Theme card for CRM Core/Profile/Messaging/Automations grouping."""
    pri = " priority" if theme in PRIORITY_ORDER else ""
    slug = slug or theme_slug(theme)
    return f"""<article class="theme-card playbook-card{pri}" id="theme-{esc(slug)}">
  <div class="theme-head"><h3>{esc(theme)}</h3>
  <div class="theme-nums"><b>{count:,}</b>
  <span>{pct_of_filtered:.1f}% of CRM-area SRs</span></div></div>
  <div class="pack">Jira Yes {jira_yes:,} · Jira No {jira_no:,}
  (Service Requests with / without a Jira update)</div>
  {bar(pct_of_filtered, max_pct)}{_reduce_block(theme, count, slug)}</article>"""


def playbook_by_product_area(snapshot: dict) -> str:
    """CRM Core / Profile / Messaging / Automations — Jira Yes + No."""
    n = snapshot["n_filtered"]
    # Prefer structured areas[] from analyze_rx_crm_areas_jira_yn.py
    if snapshot.get("areas"):
        sections = []
        for i, area_row in enumerate(snapshot["areas"]):
            area = area_row["area"]
            rows = area_row.get("themes") or []
            if not rows:
                continue
            area_n = area_row["count"]
            area_pct = area_row.get("pct_of_filtered") or (
                round(100 * area_n / n, 1) if n else 0.0
            )
            y = area_row.get("jira_yes", 0)
            no = area_row.get("jira_no", 0)
            max_pct = max((r["pct_of_filtered"] for r in rows), default=1)
            cards = "".join(
                product_area_card(
                    r["theme"],
                    r["count"],
                    r["pct_of_filtered"],
                    r.get("jira_yes", 0),
                    r.get("jira_no", 0),
                    max_pct,
                    r.get("theme_slug") or theme_slug(r["theme"]),
                )
                for r in rows
                if r["theme"] in THEME_PLAYBOOK
            )
            aid = AREA_SLUG[area]
            open_attr = " open" if i == 0 else ""
            blurb = AREA_BLURB.get(area, "")
            sections.append(
                f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(area)}</span>
    <span class="area-stats"><b>{area_n:,}</b> SRs · {area_pct:.1f}% ·
    Jira Yes {y:,} / No {no:,} · {len(rows)} theme{"s" if len(rows) != 1 else ""}</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <p class="area-blurb">{esc(blurb)}</p>
    <div class="theme-grid playbook">{cards}</div>
  </div>
</details>"""
            )
        return "".join(sections)

    # Fallback: older theme_totals + THEME_AREA map
    by_area: dict[str, list] = {a: [] for a in AREA_ORDER}
    for row in snapshot.get("theme_totals") or []:
        theme = row["theme"]
        if theme == "Unclassified / other" or theme not in THEME_PLAYBOOK:
            continue
        count = row["count"]
        pct = round(100 * count / n, 2) if n else 0.0
        area = THEME_AREA.get(theme)
        if area in by_area:
            by_area[area].append(
                {
                    "theme": theme,
                    "count": count,
                    "pct": pct,
                    "jira_yes": row.get("jira_yes", 0),
                    "jira_no": row.get("jira_no", 0),
                }
            )
    sections = []
    for i, area in enumerate(AREA_ORDER):
        rows = by_area[area]
        if not rows:
            continue
        area_n = sum(r["count"] for r in rows)
        area_pct = round(100 * area_n / n, 1) if n else 0.0
        y = sum(r["jira_yes"] for r in rows)
        no = sum(r["jira_no"] for r in rows)
        max_pct = max((r["pct"] for r in rows), default=1)
        cards = "".join(
            product_area_card(
                r["theme"],
                r["count"],
                r["pct"],
                r["jira_yes"],
                r["jira_no"],
                max_pct,
                theme_slug(r["theme"]),
            )
            for r in rows
        )
        aid = AREA_SLUG[area]
        open_attr = " open" if i == 0 else ""
        blurb = AREA_BLURB.get(area, "")
        sections.append(
            f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(area)}</span>
    <span class="area-stats"><b>{area_n:,}</b> SRs · {area_pct}% ·
    Jira Yes {y:,} / No {no:,} · {len(rows)} theme{"s" if len(rows) != 1 else ""}</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <p class="area-blurb">{esc(blurb)}</p>
    <div class="theme-grid playbook">{cards}</div>
  </div>
</details>"""
        )
    return "".join(sections)


def playbook_by_classification(snapshot: dict) -> str:
    """Four ticket-classification accordions (option A)."""
    focus_meta = {x["classification"]: x for x in snapshot["classification_focus"]}
    by_class = snapshot["themes_by_class"]
    sections = []
    for i, cls in enumerate(CLASS_FOCUS):
        meta = focus_meta.get(cls, {"count": 0, "pct_of_filtered": 0.0})
        rows = [
            r
            for r in (by_class.get(cls) or [])
            if r["theme"] != "Unclassified / other" and r["theme"] in THEME_PLAYBOOK
        ]
        max_pct = max((r["pct_of_class"] for r in rows), default=1)
        cards = "".join(
            reduce_only_card(
                r["theme"],
                r["count_in_class"],
                r["pct_of_class"],
                r["theme_total"],
                r["pct_of_theme"],
                max_pct,
            )
            for r in rows
        )
        aid = CLASS_SLUG[cls]
        open_attr = " open" if i == 0 else ""
        sections.append(
            f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(cls)}</span>
    <span class="area-stats"><b>{meta['count']:,}</b> SRs ·
    {meta['pct_of_filtered']:.1f}% of filtered · {len(rows)} theme{"s" if len(rows) != 1 else ""}</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <p class="area-blurb">Themes with ≥1 filtered row in this classification.
    Reduce bullets are from the existing playbook only — not invented for this cut.
    A theme may also appear under other classifications.</p>
    <div class="theme-grid playbook">{cards}</div>
  </div>
</details>"""
        )
    return "".join(sections)


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
            f'<p class="area-blurb">Also in filter (no accordion): '
            f'{esc("; ".join(bits))}. Ops Issues and Security-Related Issues: 0.</p>'
        )
    return (
        f"<h2>Feedback % by ticket classification "
        f"<span class='pill pill-yes'>n={n:,}</span></h2>"
        + table_rows(
            rows,
            ["U_TICKET_CLASSIFICATION", "Rows", "% of filtered"],
        )
        + other_note
    )


def playbook_srs_panel(crm_snapshot: dict) -> str:
    """New tab: all Service Requests used in the CRM-area playbook (Yes + No)."""
    srs = crm_snapshot.get("service_requests") or []
    n = len(srs)
    y = sum(1 for s in srs if s.get("jira_created") == "Yes")
    no = sum(1 for s in srs if s.get("jira_created") == "No")
    # Themes per area (preserve AREA_ORDER; themes sorted by count desc then name)
    theme_meta: dict[str, dict] = {}
    for s in srs:
        slug = s.get("theme_slug") or theme_slug(s["theme"])
        if slug not in theme_meta:
            theme_meta[slug] = {
                "theme": s["theme"],
                "slug": slug,
                "area": s["area"],
                "count": 0,
            }
        theme_meta[slug]["count"] += 1
    themes_by_area: dict[str, list] = {a: [] for a in AREA_ORDER}
    for meta in theme_meta.values():
        if meta["area"] in themes_by_area:
            themes_by_area[meta["area"]].append(meta)
    for a in AREA_ORDER:
        themes_by_area[a].sort(key=lambda x: (-x["count"], x["theme"]))

    areas = [a for a in AREA_ORDER if themes_by_area.get(a)]
    area_opts = "".join(f'<option value="{esc(a)}">{esc(a)}</option>' for a in areas)
    # All theme options with data-area for client-side filtering
    theme_opts_parts = []
    for a in AREA_ORDER:
        for meta in themes_by_area.get(a) or []:
            theme_opts_parts.append(
                f'<option value="{esc(meta["slug"])}" data-area="{esc(meta["area"])}">'
                f'{esc(meta["theme"])} ({meta["count"]})</option>'
            )
    theme_opts = "".join(theme_opts_parts)
    area_theme_map = {
        a: [{"slug": m["slug"], "theme": m["theme"], "count": m["count"]} for m in themes_by_area[a]]
        for a in AREA_ORDER
        if themes_by_area.get(a)
    }
    area_theme_json = json.dumps(area_theme_map, ensure_ascii=False).replace(
        "<", "\\u003c"
    ).replace(">", "\\u003e")
    payload = json.dumps(srs, ensure_ascii=False)
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e")
    return f"""
  <div class="note">All Service Requests in the CRM-area Playbook
  (Jira Yes <b>{y:,}</b> + Jira No <b>{no:,}</b> = <b>{n:,}</b>).
  Choose an <b>Area</b> first — the Theme list shows only themes in that area.
  Click an SR count on a “What to do in Phenom” bullet to jump here filtered to that theme.</div>
  <div class="sr-toolbar">
    <label>Area
      <select id="sr-filter-area"><option value="">All areas</option>{area_opts}</select>
    </label>
    <label>Theme
      <select id="sr-filter-theme"><option value="">All themes</option>{theme_opts}</select>
    </label>
    <label>Jira
      <select id="sr-filter-jira">
        <option value="">Yes + No</option>
        <option value="Yes">Jira Yes only</option>
        <option value="No">Jira No only</option>
      </select>
    </label>
    <label class="sr-search">Search
      <input id="sr-filter-q" type="search" placeholder="ID, title, or description…" />
    </label>
    <span class="sr-showing" id="sr-showing">Showing {n:,} of {n:,}</span>
  </div>
  <div class="sr-table-wrap">
    <table class="sr-table" id="sr-table">
      <thead>
        <tr>
          <th>SR ID</th>
          <th>Jira</th>
          <th>Area</th>
          <th>Theme</th>
          <th>Short description</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody id="sr-tbody"></tbody>
    </table>
  </div>
  <script type="application/json" id="playbook-srs-data">{payload}</script>
  <script type="application/json" id="playbook-area-themes">{area_theme_json}</script>
"""


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
        help="JSON from analyze_rx_ticket_classification.py (classification % table)",
    )
    ap.add_argument(
        "--crm-areas-snapshot",
        type=Path,
        default=None,
        help="JSON from analyze_rx_crm_areas_jira_yn.py (Playbook CRM areas, Yes+No)",
    )
    args = ap.parse_args()

    with args.csv.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    rx = [
        r
        for r in rows
        if is_rx(r) and g(r, "JIRA_CREATED") in ("Yes", "No")
    ]
    linked = sum(
        1
        for r in rows
        if is_rx(r) and g(r, "JIRA_CREATED") == "Linked - key not found in JIRA"
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

    class_snap_path = args.ticket_class_snapshot
    if class_snap_path is None:
        class_snap_path = args.out.parent / "snapshot-rx-ticket-classification.json"
    if not class_snap_path.exists():
        raise SystemExit(
            f"Missing ticket-class snapshot: {class_snap_path}\n"
            "Run analyze_rx_ticket_classification.py first."
        )
    class_snapshot = json.loads(class_snap_path.read_text())
    class_pct_html = classification_pct_table(class_snapshot)

    crm_snap_path = args.crm_areas_snapshot
    if crm_snap_path is None:
        crm_snap_path = args.out.parent / "snapshot-rx-crm-areas-jira-yn.json"
    if not crm_snap_path.exists():
        raise SystemExit(
            f"Missing CRM-areas snapshot: {crm_snap_path}\n"
            "Run analyze_rx_crm_areas_jira_yn.py first."
        )
    crm_snapshot = json.loads(crm_snap_path.read_text())
    n_f = crm_snapshot["n_filtered"]
    # Header Jira split = the split *inside* the classified population, summed from
    # areas[]. funnel.jira_Yes/No count every RX Yes/No SR before theme classification,
    # so they do not add up to n_filtered and must not be shown as its split.
    area_rows = crm_snapshot.get("areas") or []
    n_yes = sum(a.get("jira_yes", 0) for a in area_rows)
    n_no = sum(a.get("jira_no", 0) for a in area_rows)
    if n_yes + n_no != n_f:
        raise SystemExit(
            f"Jira split from areas[] ({n_yes} Yes + {n_no} No = {n_yes + n_no}) "
            f"does not match n_filtered={n_f} in {crm_snap_path}"
        )
    funnel = crm_snapshot.get("funnel") or {}
    f_yes = funnel.get("jira_Yes", 0)
    f_no = funnel.get("jira_No", 0)
    f_yn = funnel.get("jira_yes_or_no", f_yes + f_no)
    product_accordions = playbook_by_product_area(crm_snapshot)
    playbook_srs_html = playbook_srs_panel(crm_snapshot)
    product_nav = "".join(
        f'<a href="#{AREA_SLUG[a]}" data-area="{AREA_SLUG[a]}">{esc(a)}</a>'
        for a in AREA_ORDER
    )

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
.reduce-list li{{margin:.28rem 0;line-height:1.45;display:flex;flex-wrap:wrap;align-items:baseline;gap:.45rem}}
.reduce-list .reduce-text{{flex:1 1 18rem}}
.sr-count{{flex:0 0 auto}}
.sr-count-link{{display:inline-block;font-size:.78rem;font-weight:700;color:var(--accent);
background:#dceae3;border-radius:999px;padding:.12rem .55rem;text-decoration:none;
border:1px solid #b7d0c3;white-space:nowrap}}
.sr-count-link:hover{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.pb dt .sr-count-link{{margin-left:.45rem;vertical-align:middle}}
.sr-toolbar{{display:flex;flex-wrap:wrap;gap:.65rem;align-items:end;margin:0 0 .85rem}}
.sr-toolbar label{{display:grid;gap:.2rem;font-size:.75rem;color:var(--muted);font-weight:600}}
.sr-toolbar select,.sr-toolbar input{{font:inherit;font-size:.85rem;padding:.35rem .5rem;
border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);min-width:10rem}}
.sr-search{{flex:1 1 14rem}}.sr-search input{{width:100%}}
.sr-showing{{font-size:.82rem;color:var(--muted);padding-bottom:.35rem}}
.sr-table-wrap{{overflow:auto;max-height:70vh;border:1px solid var(--line);border-radius:12px;background:var(--card)}}
.sr-table{{margin:0;font-size:.8rem}}.sr-table th{{position:sticky;top:0;z-index:1}}
.sr-table td.desc{{max-width:36rem;white-space:normal;line-height:1.4;color:var(--muted)}}
.sr-table td.short{{max-width:18rem;white-space:normal}}
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
.area-blurb{{margin:0 0 .75rem;font-size:.88rem;color:var(--ink);max-width:90ch;line-height:1.45}}
.theme-problem{{margin:.55rem 0 0;font-size:.88rem;line-height:1.45;color:var(--ink)}}
.theme-problem .lbl{{display:inline-block;font-size:.72rem;font-weight:700;text-transform:uppercase;
letter-spacing:.03em;color:var(--no);margin-right:.35rem}}
.muted{{color:var(--muted);font-size:.86rem}}
footer{{max-width:1140px;margin:0 auto;padding:0 1.5rem 2rem;color:var(--muted);font-size:.75rem}}
h2{{font-size:1.1rem}}h3{{font-size:.95rem;margin:0}}
</style></head><body>
<header>
  <h1>RX themes — ticket classification + Jira Yes/No</h1>
  <p class="sub">Playbook CRM areas: full all-fields CSV · Service Request · RX ·
  <b>Jira Yes and Jira No</b> · themes classified into Core / Profile / Messaging /
  Automations → n={n_f:,}, of which <b>{n_yes:,}</b> are Jira Yes and
  <b>{n_no:,}</b> are Jira No. Before theme classification there were {f_yn:,}
  RX Yes/No SRs ({f_yes:,} Yes / {f_no:,} No); {f_yn - n_f:,} stayed unclassified
  and are not in the four areas below.
  Each theme shows a Problem summary from SHORT_DESCRIPTION + DESCRIPTION and
  clear What to do in Phenom actions. Other tabs: sheet Yes/No theme compare
  (n={len(rx):,}).</p>
  <div class="stats">
    <div class="stat"><b>{n_f:,}</b><span>CRM-area SRs (Yes+No)</span></div>
    <div class="stat"><b>{n_yes:,}</b><span>Jira Yes · of the {n_f:,} classified</span></div>
    <div class="stat no"><b>{n_no:,}</b><span>Jira No · of the {n_f:,} classified</span></div>
    <div class="stat"><b>{f_yn:,}</b><span>RX SRs before classification ({f_yes:,} Yes / {f_no:,} No)</span></div>
    <div class="stat"><b>{len(rx):,}</b><span>RX Yes+No (other tabs)</span></div>
    <div class="stat"><b>{yes['n']:,}</b><span>Jira Yes · {yes['classified_pct']:.1f}% classified</span></div>
    <div class="stat no"><b>{no['n']:,}</b><span>Jira No · {no['classified_pct']:.1f}% classified</span></div>
    <div class="stat"><b>{linked}</b><span>Linked key-not-found (excluded)</span></div>
  </div>
</header>
<nav class="tabs" id="tabs">
  <button data-tab="playbook" class="active">Playbook · product areas</button>
  <button data-tab="playbook-srs">Playbook · Service Requests</button>
  <button data-tab="compare">Yes vs No</button>
  <button data-tab="yes-themes">Yes · themes</button>
  <button data-tab="yes-products">Yes · products</button>
  <button data-tab="no-themes" class="no-tab">No · themes</button>
  <button data-tab="no-products" class="no-tab">No · products</button>
</nav>
<main>
<section class="panel active" id="playbook">
  <div class="note">CRM-area Playbook population: <code>U_ISSUE_TYPE</code> contains Service Request;
  <code>U_PRODUCT_EXPERIENCE</code> contains Recruiter Experience (RX);
  <code>JIRA_CREATED</code> = <b>Yes</b> (Jira updated) or <b>No</b> (not updated);
  theme matched by phrase rules into Core / Profile / Messaging / Automations
  (Unclassified excluded from these four sections).
  Each theme card shows volume, Jira Yes/No split, a plain-language <b>Problem</b>
  from DESCRIPTION wording, and <b>What to do in Phenom</b>.
  Snapshot: <code>snapshot-rx-crm-areas-jira-yn.json</code>.
  Ticket-classification % table below still uses the narrower CRM PEP allowlist cut.</div>
  {class_pct_html}
  <h2>All themes — elaborated by product area</h2>
  <div class="area-toolbar">
    <nav class="area-nav" aria-label="Product areas">{product_nav}</nav>
    <div class="area-actions">
      <button type="button" id="expand-areas">Expand all</button>
      <button type="button" id="collapse-areas">Collapse all</button>
    </div>
  </div>
  <div class="area-accordions" id="area-accordions">
  {product_accordions}
  </div>
</section>
<section class="panel" id="playbook-srs">
  <h2>Playbook Service Requests
  <span class="pill pill-yes">n={n_f:,}</span>
  <span class="pill pill-yes">Jira Yes</span>
  <span class="pill pill-no">Jira No</span></h2>
  {playbook_srs_html}
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

function activateTab(tabId) {{
  document.querySelectorAll('#tabs button').forEach(b => {{
    b.classList.toggle('active', b.dataset.tab === tabId);
  }});
  document.querySelectorAll('section.panel').forEach(p => {{
    p.classList.toggle('active', p.id === tabId);
  }});
}}

const srDataEl = document.getElementById('playbook-srs-data');
const srAll = srDataEl ? JSON.parse(srDataEl.textContent) : [];
const areaThemesEl = document.getElementById('playbook-area-themes');
const areaThemes = areaThemesEl ? JSON.parse(areaThemesEl.textContent) : {{}};
const srTbody = document.getElementById('sr-tbody');
const srShowing = document.getElementById('sr-showing');
const srArea = document.getElementById('sr-filter-area');
const srTheme = document.getElementById('sr-filter-theme');
const srJira = document.getElementById('sr-filter-jira');
const srQ = document.getElementById('sr-filter-q');

function escHtml(s) {{
  return String(s ?? '').replace(/[&<>"']/g, c => ({{
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }})[c]);
}}

function rebuildThemeOptions(preferredSlug) {{
  if (!srTheme) return;
  const area = srArea?.value || '';
  const prev = preferredSlug || srTheme.value || '';
  let list = [];
  if (area && areaThemes[area]) {{
    list = areaThemes[area];
  }} else {{
    Object.values(areaThemes).forEach(arr => {{ list = list.concat(arr); }});
  }}
  const opts = ['<option value="">All themes in ' + (area || 'all areas') + '</option>']
    .concat(list.map(t =>
      `<option value="${{escHtml(t.slug)}}" data-area="${{escHtml(area || '')}}">${{escHtml(t.theme)}} (${{t.count}})</option>`
    ));
  srTheme.innerHTML = opts.join('');
  if (prev && [...srTheme.options].some(o => o.value === prev)) {{
    srTheme.value = prev;
  }} else {{
    srTheme.value = '';
  }}
}}

function renderSrs(rows) {{
  if (!srTbody) return;
  const html = rows.map(r => `
    <tr data-theme-slug="${{escHtml(r.theme_slug)}}" data-area="${{escHtml(r.area)}}" data-jira="${{escHtml(r.jira_created)}}">
      <td><code>${{escHtml(r.number)}}</code></td>
      <td>${{r.jira_created === 'Yes'
        ? '<span class="pill pill-yes">Yes</span>'
        : '<span class="pill pill-no">No</span>'}}</td>
      <td>${{escHtml(r.area)}}</td>
      <td>${{escHtml(r.theme)}}</td>
      <td class="short">${{escHtml(r.short_description)}}</td>
      <td class="desc">${{escHtml(r.description)}}</td>
    </tr>`).join('');
  srTbody.innerHTML = html || '<tr><td colspan="6" class="muted">No Service Requests match these filters.</td></tr>';
  if (srShowing) srShowing.textContent = `Showing ${{rows.length.toLocaleString()}} of ${{srAll.length.toLocaleString()}}`;
}}

function filterSrs() {{
  const area = srArea?.value || '';
  const theme = srTheme?.value || '';
  const jira = srJira?.value || '';
  const q = (srQ?.value || '').trim().toLowerCase();
  const rows = srAll.filter(r => {{
    if (area && r.area !== area) return false;
    if (theme && r.theme_slug !== theme) return false;
    if (jira && r.jira_created !== jira) return false;
    if (q) {{
      const blob = `${{r.number}} ${{r.short_description}} ${{r.description}} ${{r.theme}}`.toLowerCase();
      if (!blob.includes(q)) return false;
    }}
    return true;
  }});
  renderSrs(rows);
}}

srArea?.addEventListener('change', () => {{
  rebuildThemeOptions('');
  filterSrs();
}});
srTheme?.addEventListener('change', filterSrs);
srJira?.addEventListener('change', filterSrs);
srQ?.addEventListener('input', filterSrs);
rebuildThemeOptions('');
filterSrs();

document.querySelectorAll('.sr-count-link').forEach(a => a.addEventListener('click', e => {{
  e.preventDefault();
  const slug = a.dataset.themeSlug || '';
  const themeName = a.dataset.theme || '';
  const match = srAll.find(r => r.theme_slug === slug || r.theme === themeName);
  activateTab('playbook-srs');
  if (srArea && match) srArea.value = match.area || '';
  rebuildThemeOptions(slug);
  if (srTheme) srTheme.value = slug;
  if (srJira) srJira.value = '';
  if (srQ) srQ.value = '';
  filterSrs();
  document.getElementById('playbook-srs')?.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
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
