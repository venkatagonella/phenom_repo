#!/usr/bin/env python3
"""Heuristic overflow QA: estimate wrapped text height per textbox vs its frame."""
from pptx import Presentation
from pptx.util import Emu

PX = 914400 * 0.0104166  # EMU per authoring pixel
# Poppins average advance width as a fraction of font size, regular vs bold.
AVG = {False: 0.515, True: 0.545}

prs = Presentation("RX-CRM-Service-Request-Playbook.pptx")
problems = []
for i, s in enumerate(prs.slides, start=1):
    for shp in s.shapes:
        if not shp.has_text_frame or not shp.text_frame.text.strip():
            continue
        w_px = shp.width / PX
        h_px = shp.height / PX
        total = 0.0
        for p in shp.text_frame.paragraphs:
            txt = "".join(r.text for r in p.runs)
            if not txt:
                continue
            r0 = p.runs[0]
            fs = r0.font.size.pt / 0.75 if r0.font.size else 15
            bold = bool(r0.font.bold)
            ls = p.line_spacing or 1.15
            after = p.space_after.pt / 0.75 if p.space_after else 0
            chars_per_line = max(1, int(w_px / (fs * AVG[bold])))
            lines = 0
            for seg in txt.split("\n"):
                lines += max(1, -(-len(seg) // chars_per_line))
            total += lines * fs * ls + after
        if total > h_px + 2:
            problems.append((i, round(total), round(h_px), shp.text_frame.text[:70]))

for p in problems:
    print(f"slide {p[0]:>2}  need {p[1]}px  have {p[2]}px  | {p[3]!r}")
print(f"\n{len(problems)} potential overflows across {len(prs.slides._sldIdLst)} slides")
