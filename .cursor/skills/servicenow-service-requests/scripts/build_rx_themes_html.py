#!/usr/bin/env python3
"""Build RX Jira Yes vs No HTML theme report using rx_theme_rules classifier."""

from __future__ import annotations

import argparse
import csv
import html
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


def playbook_cards(combined_themes, n_total, max_p=None):
    """Elaborated theme cards: meaning + phenom-knowledge + reduce actions."""
    if max_p is None:
        max_p = combined_themes[0][2] if combined_themes else 1
    cards = []
    for t, c, p in combined_themes:
        pb = THEME_PLAYBOOK.get(t)
        if not pb:
            body = (
                "<p class='muted'>No playbook entry yet — add to "
                "<code>rx_theme_playbook.py</code>.</p>"
            )
            pack = "—"
        else:
            pack = pb["pack"]
            reduce_items = pb.get("reduce") or []
            if isinstance(reduce_items, str):
                reduce_items = [reduce_items]
            reduce_html = "".join(f"<li>{esc(x)}</li>" for x in reduce_items)
            body = f"""
          <dl class="pb">
            <dt>What the theme is</dt><dd>{esc(pb['means'])}</dd>
            <dt>Phenom knowledge</dt><dd>{esc(pb['knowledge'])}</dd>
            <dt>To reduce feedback %</dt>
            <dd><ul class="reduce-list">{reduce_html}</ul></dd>
          </dl>"""
        pri = " priority" if t in PRIORITY_ORDER else ""
        cards.append(
            f"""<article class="theme-card playbook-card{pri}">
          <div class="theme-head"><h3>{esc(t)}</h3>
          <div class="theme-nums"><b>{c:,}</b><span>{p:.1f}% of RX</span></div></div>
          <div class="pack">Pack: {esc(pack)}</div>
          {bar(p, max_p)}{body}</article>"""
        )
    return "".join(cards)


def playbook_by_area(combined_themes, n_total):
    """Group elaborated themes into CRM Core / Profile / Messaging / Automations."""
    max_p = combined_themes[0][2] if combined_themes else 1
    by_area: dict[str, list] = {a: [] for a in AREA_ORDER}
    other = []
    for row in combined_themes:
        area = THEME_AREA.get(row[0])
        if area in by_area:
            by_area[area].append(row)
        else:
            other.append(row)

    sections = []
    for i, area in enumerate(AREA_ORDER):
        rows = by_area[area]
        if not rows:
            continue
        area_n = sum(c for _, c, _ in rows)
        area_pct = round(100 * area_n / n_total, 1) if n_total else 0
        blurb = AREA_BLURB.get(area, "")
        aid = "area-" + area.lower().replace(" ", "-")
        open_attr = " open" if i == 0 else ""
        sections.append(
            f"""<details class="area-accordion" id="{esc(aid)}"{open_attr}>
  <summary class="area-summary">
    <span class="area-title">{esc(area)}</span>
    <span class="area-stats"><b>{area_n:,}</b> SRs · {area_pct}% of RX
    · {len(rows)} theme{"s" if len(rows) != 1 else ""}</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <p class="area-blurb">{esc(blurb)}</p>
    <div class="theme-grid playbook">{playbook_cards(rows, n_total, max_p=max_p)}</div>
  </div>
</details>"""
        )
    if other:
        sections.append(
            f"""<details class="area-accordion">
  <summary class="area-summary">
    <span class="area-title">Unmapped</span>
    <span class="area-chevron" aria-hidden="true"></span>
  </summary>
  <div class="area-body">
    <div class="theme-grid playbook">{playbook_cards(other, n_total, max_p=max_p)}</div>
  </div>
</details>"""
        )
    return "".join(sections)


def combined_theme_counts(yes, no, n_total):
    counts = Counter()
    for t, c, _ in yes["themes"]:
        counts[t] += c
    for t, c, _ in no["themes"]:
        counts[t] += c
    return [
        (t, c, round(100 * c / n_total, 2)) for t, c in counts.most_common()
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
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

    # compare
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

    combined = combined_theme_counts(yes, no, len(rx))
    pri_html = "".join(
        f"<li><strong>{esc(t)}</strong> — "
        f"{next((f'{c:,} ({p:.1f}%)' for tt,c,p in combined if tt==t), '—')}"
        f"</li>"
        for t in PRIORITY_ORDER
        if any(tt == t for tt, _, __ in combined)
    )

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>RX themes — Jira Yes vs No (cluster_v1 high-confidence)</title>
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
.priority-list{{margin:.5rem 0 1rem;padding-left:1.2rem;font-size:.9rem}}
.area-toolbar{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
gap:.6rem;margin:0 0 .85rem}}
.area-nav{{display:flex;flex-wrap:wrap;gap:.4rem}}
.area-nav a,.area-actions button{{border:1px solid var(--line);background:var(--card);border-radius:999px;
padding:.28rem .75rem;font:inherit;font-size:.8rem;color:var(--ink);text-decoration:none;cursor:pointer}}
.area-nav a:hover,.area-actions button:hover{{border-color:var(--accent);color:var(--accent)}}
.area-actions{{display:flex;gap:.35rem}}
.area-accordion{{background:var(--card);border:1px solid var(--line);border-radius:12px;
margin:0 0 .65rem;overflow:hidden}}
.area-summary{{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:.75rem;
padding:.85rem 1rem;cursor:pointer;list-style:none;user-select:none}}
.area-summary::-webkit-details-marker{{display:none}}
.area-summary:hover{{background:#f7f3eb}}
.area-title{{font-size:1.05rem;font-weight:700;color:var(--accent)}}
.area-stats{{font-size:.82rem;color:var(--muted);white-space:nowrap}}
.area-stats b{{color:var(--ink)}}
.area-chevron{{width:.55rem;height:.55rem;border-right:2px solid var(--muted);
border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .15s ease;
margin-right:.15rem}}
.area-accordion[open] .area-chevron{{transform:rotate(225deg);margin-top:.2rem}}
.area-accordion[open] .area-summary{{border-bottom:1px solid var(--line);background:#f7f3eb}}
.area-body{{padding:.85rem 1rem 1.1rem}}
.area-blurb{{margin:0 0 .75rem;font-size:.88rem;color:var(--muted);max-width:85ch}}
footer{{max-width:1140px;margin:0 auto;padding:0 1.5rem 2rem;color:var(--muted);font-size:.75rem}}
h2{{font-size:1.1rem}}h3{{font-size:.95rem;margin:0}}
</style></head><body>
<header>
  <h1>RX themes — high-confidence (base + cluster_v1)</h1>
  <p class="sub">Method: phrase rules first; TF-IDF cluster residual unclassified; add high-confidence phrase rules from clusters.
  Residual stays Unclassified. Sheet title+body only (no comments). See <code>theme-methodology.md</code> and
  <code>theme-playbook.md</code> (phenom-knowledge grounded meaning + reduce-feedback actions).</p>
  <div class="stats">
    <div class="stat"><b>{len(rx):,}</b><span>RX Yes+No</span></div>
    <div class="stat"><b>{yes['n']:,}</b><span>Jira Yes · {yes['classified_pct']:.1f}% classified</span></div>
    <div class="stat no"><b>{no['n']:,}</b><span>Jira No · {no['classified_pct']:.1f}% classified</span></div>
    <div class="stat"><b>{linked}</b><span>Linked key-not-found (excluded)</span></div>
    <div class="stat"><b>{yes['sources'].get('cluster_v1',0)+no['sources'].get('cluster_v1',0):,}</b><span>Matched via cluster_v1 rules</span></div>
  </div>
</header>
<nav class="tabs" id="tabs">
  <button data-tab="playbook" class="active">Playbook · meaning &amp; reduce %</button>
  <button data-tab="compare">Yes vs No</button>
  <button data-tab="yes-themes">Yes · themes</button>
  <button data-tab="yes-products">Yes · products</button>
  <button data-tab="no-themes" class="no-tab">No · themes</button>
  <button data-tab="no-products" class="no-tab">No · products</button>
</nav>
<main>
<section class="panel active" id="playbook">
  <div class="note">Each theme: <strong>what it is</strong> (SR demand signal) ·
  <strong>phenom-knowledge</strong> grounding (Messaging / Automations / Screening — gaps called out) ·
  <strong>what to do to reduce feedback %</strong>. Counts = Yes+No combined (n={len(rx):,}).
  Actions are demand signals, not an approved roadmap. Source: <code>theme-playbook.md</code>.</div>
  <h2>Priority lens (highest volume, excl. Unclassified)</h2>
  <ol class="priority-list">{pri_html}</ol>
  <h2>Themes by product area</h2>
  <div class="area-toolbar">
    <nav class="area-nav" aria-label="Product areas">
      <a href="#area-crm-core" data-area="area-crm-core">CRM Core</a>
      <a href="#area-crm-profile" data-area="area-crm-profile">CRM Profile</a>
      <a href="#area-crm-messaging" data-area="area-crm-messaging">CRM Messaging</a>
      <a href="#area-crm-automations" data-area="area-crm-automations">CRM Automations</a>
    </nav>
    <div class="area-actions">
      <button type="button" id="expand-areas">Expand all</button>
      <button type="button" id="collapse-areas">Collapse all</button>
    </div>
  </div>
  <div class="area-accordions" id="area-accordions">
  {playbook_by_area(combined, len(rx))}
  </div>
</section>
<section class="panel" id="compare">
  <div class="note">Δ pp = No% − Yes%. Positive = more common when Jira was <em>not</em> created.
  Sources: base / cluster_v1 / unclassified.</div>
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
Classifier: .cursor/skills/servicenow-service-requests/scripts/rx_theme_rules.py (base + cluster_v1).<br/>
Playbook: theme-playbook.md + scripts/rx_theme_playbook.py (phenom-knowledge Messaging / Automations / Screening).<br/>
Methodology: product-copilot-beta/knowledge/servicenow-service-requests/theme-methodology.md.
Sheet-only. Residual clusters remain Unclassified by design.
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
    # mirror legacy filename
    alt = args.out.parent / "jira-yes-keywords-product-areas.html"
    alt.write_text(doc)
    print(
        f"wrote {args.out} yes_classified={yes['classified_pct']}% "
        f"no_classified={no['classified_pct']}%"
    )


if __name__ == "__main__":
    main()
