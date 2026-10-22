#!/usr/bin/env python3
"""Render the leadership-editorial PPTX to PNGs with real Fraunces / DM Sans metrics.

Adapted from render_qa.py (the corporate-template QA harness). Differences:
per-run fonts and italics, letter-spacing, pictures with python-pptx cropping,
the 1920x1080 authoring grid, and a contact sheet.

Fraunces and DM Sans are not system-installed here, so the variable TTFs are
fetched once into qa-fonts/ (gitignored scratch, same category as qa-render/).

Usage: python3 render_qa_leadership.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN

HERE = Path(__file__).parent
DECK = HERE / "RX-CRM-Service-Request-Playbook.pptx"
OUT = HERE / "qa-render-leadership"
FONTDIR = HERE / "qa-fonts"
W, H = 1920, 1080
EMU_PER_PX = 914400 * (13.3333333 / W)
SCALE = 1.0       # render 1:1 — rounding the font size at any other scale
                  # shifts wrap points and invents overflow that is not there

GF = "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl"
SOURCES = {
    "Fraunces.ttf": f"{GF}/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf",
    "Fraunces-Italic.ttf": f"{GF}/fraunces/Fraunces-Italic%5BSOFT,WONK,opsz,wght%5D.ttf",
    "DMSans.ttf": f"{GF}/dmsans/DMSans%5Bopsz,wght%5D.ttf",
    "DMSans-Italic.ttf": f"{GF}/dmsans/DMSans-Italic%5Bopsz,wght%5D.ttf",
}
# (file, named instance) per (family, bold, italic)
PICK = {
    ("Fraunces", True, False): ("Fraunces.ttf", "SemiBold"),
    ("Fraunces", True, True): ("Fraunces-Italic.ttf", "SemiBold Italic"),
    ("Fraunces", False, False): ("Fraunces.ttf", "Regular"),
    ("Fraunces", False, True): ("Fraunces-Italic.ttf", "Italic"),
    ("DM Sans", False, False): ("DMSans.ttf", "Regular"),
    ("DM Sans", True, False): ("DMSans.ttf", "Bold"),
    ("DM Sans", False, True): ("DMSans-Italic.ttf", "Italic"),
    ("DM Sans", True, True): ("DMSans-Italic.ttf", "Bold Italic"),
}


def ensure_fonts():
    FONTDIR.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        f = FONTDIR / name
        if f.exists() and f.stat().st_size > 50_000:
            continue
        print(f"fetching {name}")
        subprocess.run(["curl", "-sS", "--max-time", "60", "-o", str(f), url],
                       check=True)


_cache: dict = {}


def font(px, family, bold, italic):
    key = (round(px * SCALE), family, bold, italic)
    if key not in _cache:
        fname, inst = PICK.get((family, bool(bold), bool(italic)),
                               ("DMSans.ttf", "Regular"))
        f = ImageFont.truetype(str(FONTDIR / fname), max(1, int(round(px * SCALE))))
        try:
            f.set_variation_by_name(inst)
        except Exception:
            pass
        _cache[key] = f
    return _cache[key]


def rgb(c, default="#000000"):
    try:
        return "#" + str(c.rgb)
    except Exception:
        return default


def spc_px(run):
    try:
        v = run.font._rPr.get("spc")
        return (int(v) / 100) * 2 if v else 0.0        # 1/100 pt -> authoring px
    except Exception:
        return 0.0


def tokens(para):
    """Flatten a paragraph into word tokens; <a:br/> becomes a hard break."""
    from pptx.oxml.ns import qn
    from pptx.text.text import _Run
    out = []
    for el in para._p:
        if el.tag == qn("a:br"):
            out.append({"br": True})
            continue
        if el.tag != qn("a:r"):
            continue
        r = _Run(el, para)
        if not r.text:
            continue
        px = r.font.size.pt * 2 if r.font.size else 24
        fam = r.font.name or "DM Sans"
        f = font(px, fam, r.font.bold, r.font.italic)
        col = rgb(r.font.color)
        sp = spc_px(r) * SCALE
        for w in r.text.split(" "):
            if w:
                out.append({"t": w, "f": f, "c": col, "sp": sp, "px": px})
    return out


def measure(tok):
    base = tok["f"].getlength(tok["t"])
    return base + tok["sp"] * len(tok["t"])


def draw_token(d, x, y, tok):
    if tok["sp"]:
        for ch in tok["t"]:
            d.text((x, y), ch, font=tok["f"], fill=tok["c"], anchor="la")
            x += tok["f"].getlength(ch) + tok["sp"]
        return x
    d.text((x, y), tok["t"], font=tok["f"], fill=tok["c"], anchor="la")
    return x + tok["f"].getlength(tok["t"])


def render(idx, slide):
    img = Image.new("RGB", (int(W * SCALE), int(H * SCALE)), "#FFFFFF")
    d = ImageDraw.Draw(img)
    issues = []
    for shp in slide.shapes:
        x, y = shp.left / EMU_PER_PX * SCALE, shp.top / EMU_PER_PX * SCALE
        w, h = shp.width / EMU_PER_PX * SCALE, shp.height / EMU_PER_PX * SCALE
        if shp.shape_type == MSO_SHAPE_TYPE.PICTURE:
            try:
                im = Image.open(shp.image.blob and __import__("io").BytesIO(
                    shp.image.blob)).convert("RGB")
            except Exception:
                continue
            cl, cr = shp.crop_left or 0, shp.crop_right or 0
            ct, cb = shp.crop_top or 0, shp.crop_bottom or 0
            iw, ih = im.size
            im = im.crop((int(iw * cl), int(ih * ct),
                          int(iw * (1 - cr)), int(ih * (1 - cb))))
            img.paste(im.resize((max(1, int(w)), max(1, int(h)))),
                      (int(x), int(y)))
            continue
        if shp.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            fill = rgb(shp.fill.fore_color, "#FFFFFF")
            kind = str(shp.auto_shape_type)
            if "OVAL" in kind:
                d.ellipse([x, y, x + w, y + h], fill=fill)
            elif "ROUNDED" in kind:
                try:
                    r = shp.adjustments[0] * min(w, h)
                except Exception:
                    r = 0
                d.rounded_rectangle([x, y, x + w, y + h],
                                    radius=max(0, min(r, min(w, h) / 2)), fill=fill)
            else:
                d.rectangle([x, y, x + w, y + h], fill=fill)
        if not shp.has_text_frame or not shp.text_frame.text.strip():
            continue
        cy = y
        paras = [p for p in shp.text_frame.paragraphs
                 if any(not t.get("br") for t in tokens(p))]
        for pi, p in enumerate(paras):
            toks = tokens(p)
            words = [t for t in toks if not t.get("br")]
            px = max(t["px"] for t in words) * SCALE
            ls = p.line_spacing or 1.3
            lh = px * ls
            lines, cur, cw = [], [], 0.0
            space = words[0]["f"].getlength(" ")
            for t in toks:
                if t.get("br"):
                    lines.append((cur, cw))
                    cur, cw = [], 0.0
                    continue
                tw = measure(t)
                if cur and cw + space + tw > w:
                    lines.append((cur, cw))
                    cur, cw = [t], tw
                else:
                    cw = cw + (space + tw if cur else tw)
                    cur.append(t)
            if cur:
                lines.append((cur, cw))
            for ln, lw in lines:
                tx = x
                if p.alignment == PP_ALIGN.CENTER:
                    tx = x + (w - lw) / 2
                ty = cy + (lh - px) / 2
                for t in ln:
                    tx = draw_token(d, tx, ty, t) + space
                cy += lh
            if pi < len(paras) - 1:
                cy += (p.space_after.pt * 2 if p.space_after else 0) * SCALE
        if cy > y + h + 4 * SCALE:
            issues.append(("overflow", round((cy - y) / SCALE),
                           round(h / SCALE), shp.text_frame.text[:70]))
    img.save(OUT / f"slide-{idx:02d}.png")
    return issues


def contact_sheet(paths, out, cols=3):
    ims = [Image.open(p) for p in paths]
    tw, th = 640, 360
    rows = (len(ims) + cols - 1) // cols
    pad, label = 14, 26
    sheet = Image.new("RGB", (cols * (tw + pad) + pad,
                              rows * (th + pad + label) + pad), "#2A2A2E")
    d = ImageDraw.Draw(sheet)
    f = font(28, "DM Sans", True, False)
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        x = pad + c * (tw + pad)
        y = pad + r * (th + pad + label)
        sheet.paste(im.resize((tw, th)), (x, y + label))
        d.text((x + 2, y + 2), f"{i + 1:02d}  {paths[i].stem}", font=f,
               fill="#FFFFFF", anchor="la")
    sheet.save(out)
    return out


def main():
    ensure_fonts()
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    prs = Presentation(DECK)
    total = 0
    for i, s in enumerate(prs.slides, start=1):
        for kind, need, have, snip in render(i, s):
            print(f"slide {i:>2}  {kind}: text {need}px in {have}px box | {snip!r}")
            total += 1
    paths = sorted(OUT.glob("slide-*.png"))
    sheet = contact_sheet(paths, OUT / "contact-sheet.png")
    print(f"{total} overflow(s) across {len(paths)} slides")
    print(f"sheet: {sheet}")


if __name__ == "__main__":
    sys.exit(main())
