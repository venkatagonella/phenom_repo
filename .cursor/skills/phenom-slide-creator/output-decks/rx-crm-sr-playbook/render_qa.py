#!/usr/bin/env python3
"""Render the PPTX to PNGs with real Poppins metrics so layout can be eyeballed."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN

EMU_PER_PX = 914400 * 0.0104166
SCALE = 1.0
W, H = 1280, 720
FONTS = {
    False: "/Library/Fonts/Poppins-Regular.ttf",
    True: "/Library/Fonts/Poppins-SemiBold.ttf",
}
_cache = {}


def font(px, bold):
    key = (round(px), bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[bold], int(round(px * SCALE)))
    return _cache[key]


def rgb(c):
    try:
        return "#" + str(c.rgb)
    except Exception:
        return "#000000"


def wrap(draw, text, fnt, max_w):
    out = []
    for hard in text.split("\n"):
        words, cur = hard.split(" "), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def render(prs, idx, slide, outdir):
    img = Image.new("RGB", (int(W * SCALE), int(H * SCALE)), "white")
    d = ImageDraw.Draw(img)
    overflow = []
    for shp in slide.shapes:
        x, y = shp.left / EMU_PER_PX * SCALE, shp.top / EMU_PER_PX * SCALE
        w, h = shp.width / EMU_PER_PX * SCALE, shp.height / EMU_PER_PX * SCALE
        if shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            fill = "#ffffff"
            try:
                fill = rgb(shp.fill.fore_color)
            except Exception:
                pass
            if "OVAL" in str(shp.auto_shape_type):
                d.ellipse([x, y, x + w, y + h], outline="#1a1c2e", width=2)
            else:
                r = min(14 * SCALE, h / 2) if "ROUNDED" in str(shp.auto_shape_type) else 0
                if r:
                    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill)
                else:
                    d.rectangle([x, y, x + w, y + h], fill=fill)
        if not shp.has_text_frame or not shp.text_frame.text.strip():
            continue
        cy = y
        for p in shp.text_frame.paragraphs:
            txt = "".join(r.text for r in p.runs)
            if not txt:
                continue
            r0 = p.runs[0]
            px = r0.font.size.pt / 0.75 if r0.font.size else 15
            bold = bool(r0.font.bold)
            fnt = font(px, bold)
            ls = p.line_spacing or 1.15
            lines = wrap(d, txt, fnt, w)
            for ln in lines:
                tx = x
                if p.alignment == PP_ALIGN.CENTER:
                    tx = x + (w - d.textlength(ln, font=fnt)) / 2
                d.text((tx, cy), ln, font=fnt, fill=rgb(r0.font.color))
                cy += px * ls * SCALE
            cy += (p.space_after.pt / 0.75 if p.space_after else 0) * SCALE
        if cy > y + h + 3 * SCALE:
            overflow.append((round((cy - y) / SCALE), round(h / SCALE),
                             shp.text_frame.text[:60]))
    img.save(outdir / f"slide-{idx:02d}.png")
    return overflow


def main():
    outdir = Path(__file__).with_name("qa-render")
    outdir.mkdir(exist_ok=True)
    prs = Presentation(Path(__file__).with_name("RX-CRM-Service-Request-Playbook.pptx"))
    total = 0
    for i, s in enumerate(prs.slides, start=1):
        for need, have, snip in render(prs, i, s, outdir):
            print(f"slide {i:>2}  text {need}px in {have}px box | {snip!r}")
            total += 1
    print(f"{total} overflow(s) · {outdir}")


if __name__ == "__main__":
    main()
