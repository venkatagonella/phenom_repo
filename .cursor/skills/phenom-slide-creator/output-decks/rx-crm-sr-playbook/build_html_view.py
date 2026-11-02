#!/usr/bin/env python3
"""Emit a browser-viewable HTML deck from the rendered slides + the PPTX notes.

The slide images are the QA renders of the real .pptx, so the HTML is a
pixel-exact view of the deck rather than a reimplementation of it.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

from pptx import Presentation

HERE = Path(__file__).parent
PPTX = HERE / "RX-CRM-Service-Request-Playbook.pptx"
RENDERS = HERE / "qa-render-leadership"
OUT = HERE / "deck.html"

# leadership-editorial tokens
PAPER = "#F2F0EA"
NAVY = "#22224B"
KICKER = "#373775"
MAUVE = "#A67D8B"
MUTED = "#6B6B6B"

prs = Presentation(PPTX)
slides = []
for i, s in enumerate(prs.slides, start=1):
    img = RENDERS / f"slide-{i:02d}.png"
    if not img.exists():
        raise SystemExit(f"missing render: {img}")
    note = ""
    if s.has_notes_slide:
        note = s.notes_slide.notes_text_frame.text.strip()
    # first non-empty text line makes a usable thumbnail label
    title = ""
    for shp in s.shapes:
        if shp.has_text_frame:
            for ln in shp.text_frame.text.splitlines():
                if ln.strip():
                    title = ln.strip()
                    break
        if title:
            break
    slides.append({"n": i, "src": f"{RENDERS.name}/{img.name}",
                   "notes": note, "title": title})

data = json.dumps(slides, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e")

doc = f"""<!DOCTYPE html>
<meta charset="utf-8">
<title>RX CRM Service Request Playbook</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700&display=swap" rel="stylesheet">
<style>
  :root {{
    --paper: {PAPER}; --navy: {NAVY}; --kicker: {KICKER};
    --mauve: {MAUVE}; --muted: {MUTED};
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ height: 100%; margin: 0; }}
  body {{
    background: var(--navy);
    font-family: "DM Sans", system-ui, sans-serif;
    color: var(--paper);
    display: flex; flex-direction: column;
  }}
  header {{
    display: flex; align-items: center; gap: 20px;
    padding: 12px 22px; border-bottom: 1px solid rgba(242,240,234,.14);
    flex: 0 0 auto;
  }}
  h1 {{
    font-family: "Fraunces", Georgia, serif; font-weight: 600;
    font-size: 17px; margin: 0; letter-spacing: .1px;
  }}
  h1 em {{ color: var(--mauve); font-style: italic; }}
  .spacer {{ flex: 1; }}
  button {{
    font: inherit; font-size: 13px; color: var(--paper);
    background: transparent; border: 1px solid rgba(242,240,234,.3);
    border-radius: 999px; padding: 6px 14px; cursor: pointer;
  }}
  button:hover {{ background: rgba(242,240,234,.1); }}
  button[aria-pressed="true"] {{ background: var(--paper); color: var(--navy); border-color: var(--paper); }}
  #counter {{ font-variant-numeric: tabular-nums; font-size: 13px; color: rgba(242,240,234,.72); }}

  main {{ flex: 1; display: grid; place-items: center; padding: 22px; min-height: 0; }}
  #stage {{ max-width: 100%; max-height: 100%; display: flex; flex-direction: column; gap: 14px; }}
  #slide {{
    max-width: 100%; max-height: 100%; width: auto; height: auto;
    object-fit: contain; border-radius: 6px;
    box-shadow: 0 18px 50px rgba(0,0,0,.45);
    background: var(--paper);
  }}
  #notes {{
    display: none; background: rgba(242,240,234,.07);
    border-left: 3px solid var(--mauve); border-radius: 4px;
    padding: 13px 16px; font-size: 14px; line-height: 1.55;
    color: rgba(242,240,234,.9); max-width: 1100px;
  }}
  body.notes #notes {{ display: block; }}
  #notes:empty::after {{ content: "No speaker notes on this slide."; color: var(--muted); }}

  nav {{
    flex: 0 0 auto; display: flex; gap: 8px; overflow-x: auto;
    padding: 10px 16px; border-top: 1px solid rgba(242,240,234,.14);
    scrollbar-width: thin;
  }}
  nav img {{
    height: 62px; border-radius: 3px; cursor: pointer; flex: 0 0 auto;
    opacity: .45; border: 2px solid transparent; background: var(--paper);
    transition: opacity .12s;
  }}
  nav img:hover {{ opacity: .85; }}
  nav img.on {{ opacity: 1; border-color: var(--mauve); }}

  body.grid main {{ align-items: start; overflow: auto; }}
  body.grid #stage {{ display: none; }}
  #grid {{ display: none; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 18px; width: 100%; }}
  body.grid #grid {{ display: grid; }}
  body.grid nav {{ display: none; }}
  #grid figure {{ margin: 0; cursor: pointer; }}
  #grid img {{ width: 100%; border-radius: 4px; background: var(--paper); display: block; }}
  #grid figcaption {{ font-size: 12px; color: rgba(242,240,234,.66); padding-top: 6px; }}
</style>

<header>
  <h1>RX CRM Service Request Playbook <em>— as presented</em></h1>
  <span id="counter"></span>
  <span class="spacer"></span>
  <button id="btn-notes" aria-pressed="false">Speaker notes</button>
  <button id="btn-grid" aria-pressed="false">All slides</button>
</header>

<main>
  <div id="stage">
    <img id="slide" alt="">
    <div id="notes"></div>
  </div>
  <div id="grid"></div>
</main>

<nav id="strip"></nav>

<script>
const SLIDES = {data};
let i = 0;

const slide = document.getElementById('slide');
const notes = document.getElementById('notes');
const counter = document.getElementById('counter');
const strip = document.getElementById('strip');
const grid = document.getElementById('grid');

SLIDES.forEach((s, k) => {{
  const t = document.createElement('img');
  t.src = s.src; t.alt = 'Slide ' + s.n; t.loading = 'lazy';
  t.addEventListener('click', () => show(k));
  strip.appendChild(t);

  const fig = document.createElement('figure');
  const im = document.createElement('img');
  im.src = s.src; im.alt = 'Slide ' + s.n; im.loading = 'lazy';
  const cap = document.createElement('figcaption');
  cap.textContent = s.n + '. ' + (s.title || '');
  fig.append(im, cap);
  fig.addEventListener('click', () => {{ setGrid(false); show(k); }});
  grid.appendChild(fig);
}});

function show(k) {{
  i = Math.max(0, Math.min(SLIDES.length - 1, k));
  const s = SLIDES[i];
  slide.src = s.src;
  slide.alt = 'Slide ' + s.n + (s.title ? ': ' + s.title : '');
  notes.textContent = s.notes;
  counter.textContent = s.n + ' / ' + SLIDES.length;
  [...strip.children].forEach((el, j) => el.classList.toggle('on', j === i));
  strip.children[i].scrollIntoView({{ block: 'nearest', inline: 'center', behavior: 'smooth' }});
}}

function setGrid(on) {{
  document.body.classList.toggle('grid', on);
  document.getElementById('btn-grid').setAttribute('aria-pressed', on);
}}

document.getElementById('btn-notes').addEventListener('click', e => {{
  const on = !document.body.classList.contains('notes');
  document.body.classList.toggle('notes', on);
  e.currentTarget.setAttribute('aria-pressed', on);
}});
document.getElementById('btn-grid').addEventListener('click', () => {{
  setGrid(!document.body.classList.contains('grid'));
}});

addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{ show(i + 1); e.preventDefault(); }}
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{ show(i - 1); e.preventDefault(); }}
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(SLIDES.length - 1);
  else if (e.key === 'g') setGrid(!document.body.classList.contains('grid'));
  else if (e.key === 'n') document.getElementById('btn-notes').click();
  else if (e.key === 'Escape') setGrid(false);
}});
slide.addEventListener('click', () => show(i + 1));

show(0);
</script>
"""

OUT.write_text(doc, encoding="utf-8")
print(OUT, f"{len(slides)} slides")
