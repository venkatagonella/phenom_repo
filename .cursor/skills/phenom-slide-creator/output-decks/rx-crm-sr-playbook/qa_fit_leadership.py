#!/usr/bin/env python3
"""Structural QA for the leadership-editorial deck — the checks a render can't make.

Extends qa_fit.py (the corporate-template overflow harness, now covered by
render_qa_leadership.py's exact-metric renderer) with the style's own rules:
locked fonts, the 24px type floor, token-only colours, text contrast against the
shape actually behind it, placeholder text, glyph coverage, slides where a layout
repeats back to back, and speaker notes on every slide.

Usage: python3 qa_fit_leadership.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

HERE = Path(__file__).parent
DECK = HERE / "RX-CRM-Service-Request-Playbook.pptx"
PX = 914400 * (13.3333333 / 1920)
CANVAS = (1920, 1080)

TOKENS = {
    "F2F0EA", "FFFFFF", "141416", "414241", "8A8A8A", "22224B", "373775",
    "A67D8B", "D6D3CB", "EDE0C3", "EEDDD9", "DDDDEA", "DDE3D5", "6B6B6B",
    "CEA667", "C9A49A", "77779F", "8A9A7B",
}
FONTS = {"Fraunces", "DM Sans"}
MIN_PX = 24                      # STYLE.md: "Never below 24px"
PLACEHOLDER = re.compile(r"\[[A-Za-z ]+\]|lorem|ipsum|TODO|TBD|XXX|\{\{", re.I)
METRICS = json.loads((HERE / "font-metrics.json").read_text())
COVERED = set(METRICS["serif600"]["w"]) | set(METRICS["sans400"]["w"])
SERIF_GAPS = set("\u2194\u2192")

problems: list[str] = []


def lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgb(c):
    try:
        return str(c.rgb).upper()
    except Exception:
        return None


def boxes(slide):
    """Filled shapes and pictures, in paint order, as (x, y, w, h, fill)."""
    out = []
    for shp in slide.shapes:
        g = (shp.left / PX, shp.top / PX, shp.width / PX, shp.height / PX)
        if shp.shape_type == MSO_SHAPE_TYPE.PICTURE:
            out.append(g + ("PICTURE",))
        elif shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            out.append(g + (rgb(shp.fill.fore_color) or "FFFFFF",))
    return out


def behind(bgs, x, y, w, h):
    """Topmost filled shape fully containing the text box."""
    hit = None
    for bx, by, bw, bh, fill in bgs:
        if bx - 1 <= x and by - 1 <= y and bx + bw + 1 >= x + w and by + bh + 1 >= y + h:
            hit = fill
    return hit


def main():
    prs = Presentation(DECK)
    n_slides = len(prs.slides._sldIdLst)
    layouts: list[str] = []
    for i, s in enumerate(prs.slides, start=1):
        bgs = boxes(s)
        if not s.has_notes_slide or len(s.notes_slide.notes_text_frame.text.split()) < 20:
            problems.append(f"slide {i}: speaker notes missing or under 20 words")
        for shp in s.shapes:
            if not shp.has_text_frame or not shp.text_frame.text.strip():
                continue
            x, y = shp.left / PX, shp.top / PX
            w, h = shp.width / PX, shp.height / PX
            if x < -1 or y < -1 or x + w > CANVAS[0] + 1 or y + h > CANVAS[1] + 1:
                problems.append(
                    f"slide {i}: text box outside the canvas at "
                    f"({x:.0f},{y:.0f},{w:.0f},{h:.0f}): "
                    f"{shp.text_frame.text[:40]!r}")
            bg = behind(bgs, x, y, w, h)
            if PLACEHOLDER.search(shp.text_frame.text):
                problems.append(
                    f"slide {i}: placeholder text {shp.text_frame.text[:50]!r}")
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if not r.text.strip():
                        continue
                    name = r.font.name
                    if name not in FONTS:
                        problems.append(f"slide {i}: font {name!r} is not in {FONTS}")
                    px = r.font.size.pt * 2 if r.font.size else 0
                    if px < MIN_PX:
                        problems.append(
                            f"slide {i}: {px:.0f}px text is under the {MIN_PX}px "
                            f"floor: {r.text[:40]!r}")
                    col = rgb(r.font.color)
                    if col and col not in TOKENS:
                        problems.append(f"slide {i}: off-token colour #{col}")
                    missing = {c for c in r.text if c not in COVERED and c != " "}
                    if missing:
                        problems.append(
                            f"slide {i}: no metric/glyph for {sorted(missing)!r}")
                    if name == "Fraunces" and SERIF_GAPS & set(r.text):
                        problems.append(
                            f"slide {i}: Fraunces lacks a glyph for "
                            f"{sorted(SERIF_GAPS & set(r.text))!r}")
                    if col and bg and bg != "PICTURE":
                        c = contrast(col, bg)
                        floor = 3.0 if px >= 48 else 4.4
                        if c < floor:
                            problems.append(
                                f"slide {i}: contrast {c:.1f}:1 for #{col} on #{bg} "
                                f"({r.text[:34]!r})")
        # layout fingerprint: the shape-kind sequence, for repeat detection
        geom = tuple(sorted((round(sh.left / PX / 8), round(sh.top / PX / 8),
                             round(sh.width / PX / 8), round(sh.height / PX / 8))
                            for sh in s.shapes))
        layouts.append(geom)
    for i in range(1, len(layouts)):
        if layouts[i] == layouts[i - 1]:
            problems.append(f"slides {i} and {i + 1}: identical layout geometry")

    for p in problems:
        print(p)
    print(f"\n{len(problems)} issue(s) across {n_slides} slides")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
