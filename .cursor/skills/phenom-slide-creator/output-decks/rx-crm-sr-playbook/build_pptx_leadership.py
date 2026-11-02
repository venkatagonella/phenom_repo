#!/usr/bin/env python3
"""Phenom PPTX — RX CRM Service Request playbook, `leadership-editorial` style.

Style source of truth (read, not approximated):
  product-copilot-beta/skills/phenom-slide-creator/references/styles/leadership-editorial/STYLE.md
  product-copilot-beta/skills/phenom-slide-creator/assets/artifact-slides/leadership-editorial/build_deck.py

Tokens, type scale, paddings, radii and layout structures below are transcribed from
that builder's `STYLES["leadership-editorial"]` dict and its layout methods, on the
same 1920x1080 authoring canvas. Creativity level 1: catalog layouts only
(cover, divider, cards, compare, rows, chain, stats, numbers, table, takeaway).

Every number and sentence is read from the same two sources that generate
rx-jira-yes-themes.html:
  * snapshot-rx-crm-areas-jira-yn.json  (counts, Jira Yes/No splits)
  * rx_theme_playbook.py                (area blurbs, means, problem, reduce bullets)
No content is authored here.

Fonts: Fraunces (titles, numerals) + DM Sans (everything else). If they are not
installed locally PowerPoint substitutes silently; the font names are still written
correctly so the file renders properly once they are installed.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path("/Users/venkata.gonella/phenom-master-copilot")
KB = ROOT / "product-copilot-beta/knowledge/servicenow-service-requests"
SKILL = ROOT / "product-copilot-beta/skills/phenom-slide-creator"
IMAGERY = SKILL / "assets/imagery"
ARTIFACT = SKILL / "assets/artifact-slides/leadership-editorial"

sys.path.insert(0, str(ROOT / ".cursor/skills/servicenow-service-requests/scripts"))
from rx_theme_playbook import (  # noqa: E402
    AREA_BLURB,
    AREA_ORDER,
    PRIORITY_ORDER,
    THEME_AREA,
    THEME_PLAYBOOK,
)

# ------------------------------------------------------------------ the data
SNAP = json.loads((KB / "snapshot-rx-crm-areas-jira-yn.json").read_text())
AREAS = {a["area"]: a for a in SNAP["areas"]}
FUNNEL = SNAP["funnel"]
N = SNAP["n_filtered"]
# funnel's jira_Yes / jira_No count every RX Service Request *before* theme
# classification (555 / 842 over 1,397). The split inside the classified 1,164
# is the sum over areas.
JY = sum(a["jira_yes"] for a in SNAP["areas"])
JN = sum(a["jira_no"] for a in SNAP["areas"])
assert JY + JN == N, (JY, JN, N)
N_THEMES = sum(len(a["themes"]) for a in SNAP["areas"])
EXCLUDED = FUNNEL["rx"] - N
NO_JIRA_VALUE = FUNNEL["rx"] - FUNNEL["jira_yes_or_no"]

# ------------------------------------------------- tokens (build_deck.py)
PAPER = "F2F0EA"
CARD = "FFFFFF"
INK = "141416"
BODY = "414241"
MUTED = "6B6B6B"        # STYLE.md muted, darker of the two listed values
NAVY = "22224B"
KICKER = "373775"
BLACK = "141416"
MAUVE = "A67D8B"
RULE = "D6D3CB"
TINTS = ["EDE0C3", "EEDDD9", "DDDDEA", "FFFFFF", "DDE3D5"]
STRONG = ["CEA667", "C9A49A", "77779F", "8A9A7B"]
ON_DARK = "FFFFFF"
ON_DARK_SOFT = "DDDDEA"
STATEMENT_LABEL = "BBBBC8"

SERIF = "Fraunces"
SANS = "DM Sans"

# ------------------------------------------------------------ canvas / units
CW, CH = 1920, 1080                       # authoring canvas, as in build_deck.py
K = 13.3333333 / CW                       # inches per authoring px
PAD_T, PAD_R, PAD_B, PAD_L = 72, 96, 72, 128   # section padding, rail off
X0, X1 = PAD_L, CW - PAD_R
Y0, Y1 = PAD_T, CH - PAD_B
INNER_W = X1 - X0                         # 1696
INNER_H = Y1 - Y0                         # 936
GAP = 40                                  # default flex gap

# Exact per-character advance widths (fraction of font size) for the five faces
# this deck uses, written by gen_font_metrics.py from the real Fraunces / DM Sans
# TTFs. Wrapping is therefore exact and deterministic without the fonts installed.
METRICS = json.loads((Path(__file__).with_name("font-metrics.json")).read_text())
SAFETY = 1.004                            # kerning headroom
# Fraunces has no U+2194 / U+2192; DM Sans does. Serif text is asserted clean.
SERIF_GAPS = "\u2194\u2192"


def E(px: float) -> int:
    return Inches(px * K)


def PT(px: float) -> Pt:
    return Pt(px * 0.5)


def C(h: str) -> RGBColor:
    return RGBColor.from_string(h)


# ------------------------------------------------------------- text metrics
def text_w(text: str, px: float, face: str, spc: float = 0.0) -> float:
    """Advance width of a string, in authoring px."""
    m = METRICS[face]
    w, avg = m["w"], m["avg"]
    return (sum(w.get(c, avg) for c in str(text)) * px
            + spc * len(str(text))) * SAFETY


def wrap_lines(text: str, px: float, face: str, max_w: float, spc: float = 0.0) -> int:
    """Greedy word wrap, measured with the real per-character advance widths."""
    space = text_w(" ", px, face, spc)
    total = 0
    for hard in str(text).split("\n"):
        words = hard.split(" ")
        words = [w for w in words if w] or [""]
        lines, cur = 1, 0.0
        for w in words:
            ww = text_w(w, px, face, spc)
            if cur > 0 and cur + space + ww > max_w:
                lines += 1
                cur = ww
            else:
                cur += (space + ww) if cur else ww
        total += lines
    return total


def text_h(text: str, px: float, face: str, max_w: float, ls: float = 1.3,
           spc: float = 0.0) -> float:
    return wrap_lines(text, px, face, max_w, spc) * px * ls


# ------------------------------------------------------------------- deck
prs = Presentation()
prs.slide_width = Inches(13.3333333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
PLAN: list[tuple[int, str, str]] = []     # (index, layout, title) for the report


def rect(s, x, y, w, h, fill, radius=0.0):
    """Rectangle; radius in authoring px (0 = square corners)."""
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        E(x), E(y), E(w), E(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = C(fill)
    shp.line.fill.background()
    shp.shadow.inherit = False
    if radius:
        try:
            shp.adjustments[0] = min(0.5, radius / min(w, h))
        except Exception:
            pass
    return shp


def band(s, x, y, w, h, fill, radius=0.0, top=True, bottom=True):
    """Rounded band with selectable rounded corners (squares off the rest)."""
    if not radius or (top and bottom):
        return rect(s, x, y, w, h, fill, radius)
    rect(s, x, y, w, h, fill, radius)
    if not top:
        rect(s, x, y, w, min(radius, h), fill)
    if not bottom:
        rect(s, x, y + h - min(radius, h), w, min(radius, h), fill)


def picture(s, path: Path, x, y, w, h):
    """Place an image, cropped centre to fill the box (object-fit: cover)."""
    pic = s.shapes.add_picture(str(path), E(x), E(y), E(w), E(h))
    native = pic.image.size
    want, have = w / h, native[0] / native[1]
    if abs(want - have) > 0.001:
        if have > want:                    # image wider: crop left/right
            frac = (1 - want / have) / 2
            pic.crop_left = pic.crop_right = frac
        else:                              # image taller: crop top/bottom
            frac = (1 - have / want) / 2
            pic.crop_top = pic.crop_bottom = frac
        pic.left, pic.top, pic.width, pic.height = E(x), E(y), E(w), E(h)
    return pic


def tbox(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


FACE_FONT = {"sans400": (SANS, False, False), "sans500": (SANS, False, False),
             "sans700": (SANS, True, False), "serif600": (SERIF, True, False),
             "serif600i": (SERIF, True, True)}


def _br(p):
    """<a:br/> — a hard line break inside a paragraph."""
    from pptx.oxml.ns import qn
    p._p.append(p._p.makeelement(qn("a:br"), {}))


def _run(p, text, px, face, color, spc=0.0, italic=None):
    first = True
    for seg in str(text).split("\n"):
        if not first:
            _br(p)
        first = False
        if seg:
            r = _one_run(p, seg, px, face, color, spc, italic)
    return r


def _one_run(p, text, px, face, color, spc=0.0, italic=None):
    r = p.add_run()
    r.text = text
    name, bold, ital = FACE_FONT[face]
    f = r.font
    f.name = name
    f.size = PT(px)
    f.bold = bold
    f.italic = ital if italic is None else italic
    f.color.rgb = C(color)
    if spc:
        f._rPr.set("spc", str(int(round(spc * 0.5 * 100))))
    return r


def line(tf, text, px, face, color, *, first=False, after=0.0, ls=1.3,
         align=PP_ALIGN.LEFT, spc=0.0, upper=False, rich=False):
    """One paragraph. `rich` splits *italic* spans into their own runs."""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(0)
    p.space_after = PT(after)
    p.line_spacing = ls
    txt = str(text).upper() if upper else str(text)
    if rich and "*" in txt:
        ital_face = "serif600i" if face == "serif600" else face
        for i, chunk in enumerate(txt.split("*")):
            if chunk:
                _run(p, chunk, px, ital_face if i % 2 else face, color, spc,
                     italic=bool(i % 2) if face != "serif600" else None)
    else:
        _run(p, txt, px, face, color, spc)
    return p


def plain(text) -> str:
    return str(text).replace("*", "")


def notes(s, text):
    s.notes_slide.notes_text_frame.text = " ".join(text.split())


def slide(layout, title):
    s = prs.slides.add_slide(BLANK)
    PLAN.append((len(prs.slides.__iter__.__self__._sldIdLst), layout, plain(title)))
    return s


# ------------------------------------------------------------------- chrome
def chrome(s, dark=False):
    logo = ARTIFACT / ("logo-light.png" if dark else "logo-dark.png")
    s.shapes.add_picture(str(logo), E(48), E(996), E(33), E(42))


def section(s, dark=False, bg=None):
    rect(s, 0, 0, CW, CH, bg or (BLACK if dark else PAPER))


def head_h(kicker, title, sub, size=60, max_w=INNER_W) -> float:
    h = 0.0
    if kicker:
        h += text_h(kicker, 24, "sans700", max_w, 1.3, spc=1) + 8
    if title:
        h += text_h(plain(title), size, "serif600", max_w, 1.1) + 8
    if sub:
        h += text_h(sub, 30, "sans400", max_w, 1.3) + 8
    return max(0.0, h - 8)


def head(s, y, kicker, title, sub, size=60, dark=False, max_w=INNER_W,
         x=X0, align=PP_ALIGN.LEFT) -> float:
    """Chrome header: kicker, Fraunces title, 30px subtitle. Returns bottom y."""
    if kicker:
        h = text_h(kicker, 24, "sans700", max_w, 1.3, spc=1)
        tf = tbox(s, x, y, max_w, h)
        line(tf, kicker, 24, "sans700", ON_DARK_SOFT if dark else KICKER,
             first=True, ls=1.3, spc=1, upper=True, align=align)
        y += h + 8
    if title:
        h = text_h(plain(title), size, "serif600", max_w, 1.1)
        tf = tbox(s, x, y, max_w, h)
        line(tf, title, size, "serif600", ON_DARK if dark else INK,
             first=True, ls=1.1, rich=True, align=align)
        y += h + 8
    if sub:
        h = text_h(sub, 30, "sans400", max_w, 1.3)
        tf = tbox(s, x, y, max_w, h)
        line(tf, sub, 30, "sans400", ON_DARK_SOFT if dark else BODY,
             first=True, ls=1.3, rich=True, align=align)
        y += h + 8
    return y - 8


def foot_h(callout=None, source=None) -> float:
    h = 0.0
    if callout:
        label, text = callout
        inner = INNER_W - 64
        body = (label + "  " if label else "") + plain(text)
        h += text_h(body, 26, "sans400", inner, 1.35) + 40
    if source:
        if h:
            h += GAP
        h += text_h(source, 24, "sans400", INNER_W, 1.3)
    return h


def foot(s, callout=None, source=None, tone="navy"):
    """Bottom callout bar + source line, pinned to the content box bottom."""
    y = Y1
    if source:
        h = text_h(source, 24, "sans400", INNER_W, 1.3)
        y -= h
        tf = tbox(s, X0, y, INNER_W, h)
        line(tf, source, 24, "sans400", MUTED, first=True, ls=1.3)
        y -= GAP
    if callout:
        label, text = callout
        inner = INNER_W - 64
        bg, fg = (NAVY, ON_DARK) if tone == "navy" else (
            TINTS[{"honey": 0, "rose": 1, "lilac": 2}.get(tone, 0)], INK)
        body = (label + "  " if label else "") + plain(text)
        h = text_h(body, 26, "sans400", inner, 1.35) + 40
        y -= h
        rect(s, X0, y, INNER_W, h, bg, radius=20)
        tf = tbox(s, X0 + 32, y + 20, inner, h - 40)
        p = tf.paragraphs[0]
        p.line_spacing = 1.35
        p.space_after = Pt(0)
        if label:
            _run(p, label + "  ", 26, "sans700", fg)
        for i, chunk in enumerate(str(text).split("*")):
            if chunk:
                _run(p, chunk, 26, "sans400", fg, italic=bool(i % 2))
    return y


# ============================================================== layouts
def L_cover(image, title, sub, size=88, nts=""):
    s = slide("cover", title)
    section(s, dark=True, bg=NAVY)
    picture(s, image, 0, 0, CW, CH)
    chrome(s, dark=True)
    max_w = CW - 520                                   # padding 72px 260px
    th = text_h(plain(title), size, "serif600", max_w, 1.08)
    sh = text_h(sub, 30, "sans400", max_w, 1.3) if sub else 0
    block = th + (20 + sh if sub else 0)
    y = Y0 + (INNER_H - block) / 2
    tf = tbox(s, 260, y, max_w, th)
    line(tf, title, size, "serif600", ON_DARK, first=True, ls=1.08,
         align=PP_ALIGN.CENTER, rich=True)
    if sub:
        tf = tbox(s, 260, y + th + 20, max_w, sh)
        line(tf, sub, 30, "sans400", ON_DARK_SOFT, first=True, ls=1.3,
             align=PP_ALIGN.CENTER)
    notes(s, nts)
    return s


def L_divider(image, number, kicker, title, sub, mode="bottom", nts=""):
    s = slide("divider", title)
    section(s, dark=True)
    picture(s, image, 0, 0, CW, CH)
    chrome(s, dark=True)
    num_h = 160 if number else 0
    hh = head_h(kicker, title, sub, 84)
    block = num_h + (24 if number else 0) + hh
    if mode == "top":
        y = Y0
    elif mode == "band":
        y = Y0 + (INNER_H - block) / 2
    else:
        y = Y1 - 72 - block
    if number:
        tf = tbox(s, X0, y, INNER_W, num_h)
        line(tf, number, 160, "serif600", ON_DARK, first=True, ls=1.0)
        y += num_h + 24
    head(s, y, kicker, title, sub, 84, dark=True)
    notes(s, nts)
    return s


def L_cards(kicker, title, sub, items, callout=None, source=None, nts=""):
    """3 or 4 tinted cards in a row; tints rotate honey > rose > lilac > white."""
    s = slide("cards", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    top = y + GAP
    avail = Y1 - fh - GAP - top
    n = len(items)
    gap = 24
    cw = (INNER_W - gap * (n - 1)) / n
    inner = cw - 80                                    # padding 36px 40px
    for i, it in enumerate(items):
        navy = it.get("navy", False)
        bg = NAVY if navy else TINTS[i % len(TINTS)]
        fg = ON_DARK if navy else INK
        fb = ON_DARK_SOFT if navy else BODY
        x = X0 + i * (cw + gap)
        rect(s, x, top, cw, avail, bg, radius=40)
        ty = top + 36
        if it.get("tag"):
            h = text_h(it["tag"], 24, "sans700", inner, 1.3, spc=1)
            tf = tbox(s, x + 40, ty, inner, h)
            line(tf, it["tag"], 24, "sans700", ON_DARK_SOFT if navy else KICKER,
                 first=True, ls=1.3, spc=1, upper=True)
            ty += h + 12
        h = text_h(it["title"], 30, "sans700", inner, 1.2)
        tf = tbox(s, x + 40, ty, inner, h)
        line(tf, it["title"], 30, "sans700", fg, first=True, ls=1.2)
        ty += h + 12
        h = text_h(it["body"], 26, "sans400", inner, 1.35)
        tf = tbox(s, x + 40, ty, inner, h)
        line(tf, it["body"], 26, "sans400", fb, first=True, ls=1.35)
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_numbers(kicker, title, sub, items, closing=None, source=None, size=104,
              callout=None, nts=""):
    """Two to four giant Fraunces numbers in a row; the last one in the accent."""
    s = slide("numbers", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    n = len(items)
    gap = 40
    cw = (INNER_W - gap * (n - 1)) / n
    bh = max(text_h(it["body"], 26, "sans400", cw, 1.35) for it in items)
    block = size + 12 + bh
    ch_ = (text_h(closing, 30, "sans700", INNER_W, 1.3) + GAP) if closing else 0
    top = y + GAP + max(0.0, (Y1 - fh - ch_ - GAP - (y + GAP) - block) / 2)
    for i, it in enumerate(items):
        x = X0 + i * (cw + gap)
        col = MAUVE if it.get("accent", i == n - 1) else INK
        tf = tbox(s, x, top, cw, size)
        line(tf, it["big"], size, "serif600", col, first=True, ls=1.0)
        tf = tbox(s, x, top + size + 12, cw, bh)
        line(tf, it["body"], 26, "sans400", BODY, first=True, ls=1.35)
    if closing:
        h = text_h(closing, 30, "sans700", INNER_W, 1.3)
        tf = tbox(s, X0, Y1 - fh - GAP - h, INNER_W, h)
        line(tf, closing, 30, "sans700", INK, first=True, ls=1.3, rich=True)
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_stats(kicker, title, sub, tiles, cards, callout=None, source=None, nts=""):
    """4 stat tiles above 3 explainer cards (STYLE.md `stats`, AI 2.0 s56)."""
    s = slide("stats", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    gap = 20
    tw = (INNER_W - gap * (len(tiles) - 1)) / len(tiles)
    ti = tw - 64                                       # padding 28px 32px
    lab_h = max(text_h(t["label"], 24, "sans700", ti, 1.3) for t in tiles)
    sub_h = max(text_h(t["sub"], 24, "sans400", ti, 1.3) for t in tiles)
    th = 56 + lab_h + 6 + 64 + 6 + sub_h
    cw = (INNER_W - gap * (len(cards) - 1)) / len(cards)
    ci = cw - 64
    cth = max(text_h(c["title"], 28, "sans700", ci, 1.2) for c in cards)
    cbh = max(text_h(c["body"], 24, "sans400", ci, 1.35) for c in cards)
    chh = 56 + cth + 8 + cbh
    top = y + GAP + max(0.0, (Y1 - fh - GAP - (y + GAP) - th - gap - chh) / 2)
    for i, t in enumerate(tiles):
        x = X0 + i * (tw + gap)
        rect(s, x, top, tw, th, CARD, radius=24)
        ty = top + 28
        tf = tbox(s, x + 32, ty, ti, lab_h)
        line(tf, t["label"], 24, "sans700", KICKER, first=True, ls=1.3, upper=True)
        ty += lab_h + 6
        tf = tbox(s, x + 32, ty, ti, 64)
        line(tf, t["big"], 64, "serif600", INK, first=True, ls=1.0)
        ty += 64 + 6
        tf = tbox(s, x + 32, ty, ti, sub_h)
        line(tf, t["sub"], 24, "sans400", BODY, first=True, ls=1.3)
    cy = top + th + gap
    for i, c in enumerate(cards):
        x = X0 + i * (cw + gap)
        rect(s, x, cy, cw, chh, TINTS[i % len(TINTS)], radius=24)
        tf = tbox(s, x + 32, cy + 28, ci, cth)
        line(tf, c["title"], 28, "sans700", INK, first=True, ls=1.2)
        tf = tbox(s, x + 32, cy + 28 + cth + 8, ci, cbh)
        line(tf, c["body"], 24, "sans400", BODY, first=True, ls=1.35)
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_compare(kicker, title, sub, columns, callout=None, source=None, nts=""):
    """Two columns, light honey card vs navy card (STYLE.md `compare`)."""
    s = slide("compare", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    top = y + GAP
    avail = Y1 - fh - GAP - top
    gap = 24
    cw = (INNER_W - gap) / 2

    def measure(pad, inner_gap, kw):
        """Tallest column at this padding / gutter, including the key column."""
        iw = cw - pad * 2
        worst = 0.0
        for c in columns:
            t = pad * 2
            t += text_h(c["tag"], 24, "sans700", iw, 1.3, spc=1) + inner_gap
            t += text_h(plain(c["title"]), 40, "serif600", iw, 1.15) + inner_gap
            for k, v in c["rows"]:
                t += max(text_h(v, 24, "sans400", iw - kw - 20, 1.35),
                         56 if c.get("stats") else
                         text_h(k, 24, "sans700", kw, 1.35)) + inner_gap
            worst = max(worst, t - inner_gap)
        return worst

    pad, inner_gap, kw = 40, 20, 200
    for pad, inner_gap, kw in ((40, 20, 200), (40, 20, 170), (36, 16, 170),
                               (32, 14, 150)):
        if measure(pad, inner_gap, kw) <= avail:
            break
    need = measure(pad, inner_gap, kw)
    assert need <= avail + 1, (
        f"compare does not fit: needs {need:.0f}px in {avail:.0f}px "
        f"(title {plain(title)!r})")
    inner = cw - pad * 2
    for i, c in enumerate(columns):
        navy = c.get("navy", i == 1)
        bg = NAVY if navy else TINTS[0]
        fg = ON_DARK if navy else INK
        fb = ON_DARK_SOFT if navy else BODY
        strong = STRONG[0] if navy else KICKER
        x = X0 + i * (cw + gap)
        rect(s, x, top, cw, avail, bg, radius=32)
        ty = top + pad
        h = text_h(c["tag"], 24, "sans700", inner, 1.3, spc=1)
        tf = tbox(s, x + pad, ty, inner, h)
        line(tf, c["tag"], 24, "sans700", strong, first=True, ls=1.3, spc=1,
             upper=True)
        ty += h + inner_gap
        h = text_h(plain(c["title"]), 40, "serif600", inner, 1.15)
        tf = tbox(s, x + pad, ty, inner, h)
        line(tf, c["title"], 40, "serif600", fg, first=True, ls=1.15, rich=True)
        ty += h + inner_gap
        for k, v in c["rows"]:
            vw = inner - kw - 20
            if c.get("stats"):
                h = max(text_h(v, 24, "sans400", vw, 1.35), 56)
                tf = tbox(s, x + pad, ty, kw, 56)
                line(tf, k, 56, "serif600", fg, first=True, ls=1.0)
            else:
                h = max(text_h(v, 24, "sans400", vw, 1.35),
                        text_h(k, 24, "sans700", kw, 1.35))
                tf = tbox(s, x + pad, ty, kw, h)
                line(tf, k, 24, "sans700", strong, first=True, ls=1.35)
            tf = tbox(s, x + pad + kw + 20, ty, vw, h)
            line(tf, v, 24, "sans400", fb, first=True, ls=1.35)
            ty += h + inner_gap
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_rows(kicker, title, sub, items, callout=None, source=None, nts=""):
    """Worksheet rows: bold label left, body right, tints rotate (AI 2.0 s43)."""
    s = slide("rows", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    top = y + GAP
    gap = 14
    lab_w = 420
    body_w = INNER_W - 64 - lab_w - 32
    heights = []
    for it in items:
        lh = text_h(it["label"], 28, "sans700", lab_w, 1.2)
        if it.get("meta"):
            lh += 6 + text_h(it["meta"], 24, "sans400", lab_w, 1.25)
        bh = sum(text_h(b, 24, "sans400", body_w, 1.35) + 8
                 for b in it["body"]) - 8
        heights.append(max(lh, bh) + 44)
    total = sum(heights) + gap * (len(items) - 1)
    avail = Y1 - fh - GAP - top
    if total > avail:                                  # distribute the squeeze
        scale = (avail - gap * (len(items) - 1)) / (total - gap * (len(items) - 1))
        heights = [h * scale for h in heights]
        total = sum(heights) + gap * (len(items) - 1)
    ry = top + max(0.0, (avail - total) / 2)
    for i, it in enumerate(items):
        h = heights[i]
        navy = it.get("navy", i == len(items) - 1)
        bg = NAVY if navy else TINTS[i % len(TINTS)]
        fg = ON_DARK if navy else INK
        fb = ON_DARK_SOFT if navy else BODY
        rect(s, X0, ry, INNER_W, h, bg, radius=20)
        lh = text_h(it["label"], 28, "sans700", lab_w, 1.2)
        mh = (6 + text_h(it["meta"], 24, "sans400", lab_w, 1.25)) if it.get("meta") else 0
        ly = ry + (h - lh - mh) / 2
        tf = tbox(s, X0 + 32, ly, lab_w, lh)
        line(tf, it["label"], 28, "sans700", fg, first=True, ls=1.2)
        if it.get("meta"):
            tf = tbox(s, X0 + 32, ly + lh + 6, lab_w, mh - 6)
            line(tf, it["meta"], 24, "sans400", ON_DARK_SOFT if navy else BODY,
                 first=True, ls=1.25)
        bh = sum(text_h(b, 24, "sans400", body_w, 1.35) + 8 for b in it["body"]) - 8
        tf = tbox(s, X0 + 32 + lab_w + 32, ry + (h - bh) / 2, body_w, bh)
        for bi, b in enumerate(it["body"]):
            line(tf, b, 24, "sans400", fb, first=(bi == 0), after=8, ls=1.35)
        ry += h + gap
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_chain(kicker, title, sub, items, closing=None, callout=None, source=None,
            nts=""):
    """Columns with a thin coloured top rule, numbered (speed-of-AI s07/s12/s50)."""
    s = slide("chain", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    ch_ = (text_h(closing, 30, "sans700", INNER_W, 1.3) + GAP) if closing else 0
    top = y + GAP
    gap = 32
    cw = (INNER_W - gap * (len(items) - 1)) / len(items)
    for i, it in enumerate(items):
        x = X0 + i * (cw + gap)
        rect(s, x, top, cw, 4, STRONG[i % len(STRONG)])
        ty = top + 4 + 20
        h = text_h(it["num"], 24, "sans700", cw, 1.3)
        tf = tbox(s, x, ty, cw, h)
        line(tf, it["num"], 24, "sans700", KICKER, first=True, ls=1.3)
        ty += h + 10
        h = text_h(it["title"], 34, "serif600", cw, 1.15)
        tf = tbox(s, x, ty, cw, h)
        line(tf, it["title"], 34, "serif600", INK, first=True, ls=1.15)
        ty += h + 10
        bh = sum(text_h(b, 24, "sans400", cw, 1.35) + 10 for b in it["body"]) - 10
        tf = tbox(s, x, ty, cw, bh)
        for bi, b in enumerate(it["body"]):
            line(tf, b, 24, "sans400", BODY, first=(bi == 0), after=10, ls=1.35)
    if closing:
        h = text_h(closing, 30, "sans700", INNER_W, 1.3)
        tf = tbox(s, X0, Y1 - fh - GAP - h, INNER_W, h)
        line(tf, closing, 30, "sans700", INK, first=True, ls=1.3, rich=True)
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_table(kicker, title, sub, columns, widths, rows, callout=None, source=None,
            font=24, nts=""):
    """Navy header row, white body, lilac alternating rows (AI 2.0 s32/s50)."""
    s = slide("table", title)
    section(s)
    chrome(s)
    y = head(s, Y0, kicker, title, sub)
    fh = foot_h(callout, source)
    top = y + GAP
    avail = Y1 - fh - GAP - top
    pad_x, pad_y = 20, 12
    colw = [INNER_W * w / 100 for w in widths]

    def row_h(cells, face):
        return max(text_h(c, font, face, colw[j] - pad_x * 2, 1.35)
                   for j, c in enumerate(cells)) + pad_y * 2

    hh = row_h(columns, "sans700")
    rh = [max(text_h(c, font, "sans700" if j == 0 else "sans400",
                     colw[j] - pad_x * 2, 1.35) for j, c in enumerate(r)) + pad_y * 2
          for r in rows]
    total = hh + sum(rh)
    while total > avail and font > 24:                 # shrink, then re-measure
        font -= 0.5
        hh = row_h(columns, "sans700")
        rh = [max(text_h(c, font, "sans700" if j == 0 else "sans400",
                         colw[j] - pad_x * 2, 1.35)
                  for j, c in enumerate(r)) + pad_y * 2 for r in rows]
        total = hh + sum(rh)
    band(s, X0, top, INNER_W, hh, NAVY, radius=24, bottom=False)
    cx = X0
    for j, c in enumerate(columns):
        tf = tbox(s, cx + pad_x, top + pad_y, colw[j] - pad_x * 2, hh - pad_y * 2)
        line(tf, c, font, "sans700", ON_DARK, first=True, ls=1.35)
        cx += colw[j]
    ry = top + hh
    for i, r in enumerate(rows):
        last = i == len(rows) - 1
        if i % 2:
            band(s, X0, ry, INNER_W, rh[i], TINTS[2], radius=24, top=False,
                 bottom=last)
        else:
            band(s, X0, ry, INNER_W, rh[i], CARD, radius=24, top=False,
                 bottom=last)
        cx = X0
        for j, c in enumerate(r):
            tf = tbox(s, cx + pad_x, ry + pad_y, colw[j] - pad_x * 2,
                      rh[i] - pad_y * 2)
            line(tf, c, font, "sans700" if j == 0 else "sans400", INK,
                 first=True, ls=1.35)
            cx += colw[j]
        ry += rh[i]
    foot(s, callout, source)
    notes(s, nts)
    return s


def L_takeaway(kicker, title, items, closing=None, nts=""):
    """Black slide, three cards, one closing line (AI 2.0 s57)."""
    s = slide("takeaway", title)
    section(s, dark=True)
    chrome(s, dark=True)
    y = head(s, Y0, kicker, title, None, dark=True)
    gap = 24
    cw = (INNER_W - gap * (len(items) - 1)) / len(items)
    inner = cw - 72                                    # padding 36px
    cth = max(text_h(c["title"], 30, "sans700", inner, 1.2) for c in items)
    cbh = max(text_h(c["body"], 24, "sans400", inner, 1.35) for c in items)
    chh = 72 + cth + 10 + cbh
    ch_ = text_h(closing, 30, "sans400", INNER_W, 1.3) if closing else 0
    top = y + GAP + max(0.0, (Y1 - (y + GAP) - chh - (ch_ + GAP if closing else 0)) / 2)
    for i, c in enumerate(items):
        x = X0 + i * (cw + gap)
        rect(s, x, top, cw, chh, STRONG[0] if i == len(items) - 1 else CARD,
             radius=24)
        tf = tbox(s, x + 36, top + 36, inner, cth)
        line(tf, c["title"], 30, "sans700", INK, first=True, ls=1.2)
        tf = tbox(s, x + 36, top + 36 + cth + 10, inner, cbh)
        line(tf, c["body"], 24, "sans400",
             INK if i == len(items) - 1 else BODY, first=True, ls=1.35)
    if closing:
        tf = tbox(s, X0, top + chh + GAP, INNER_W, ch_)
        line(tf, closing, 30, "sans400", ON_DARK_SOFT, first=True, ls=1.3,
             align=PP_ALIGN.CENTER)
    notes(s, nts)
    return s


# ============================================================ derived facts
WORD = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def word(n: int) -> str:
    """Spell small counts out — titles are sentences, not data labels."""
    return WORD[n] if n < len(WORD) else f"{n:,}"


def pct(a, b, nd=1):
    v = round(a / b * 100, nd)
    return f"{v:g}%"


def meta(t):
    return f"{t['count']} SRs  ·  Jira Yes {t['jira_yes']} / No {t['jira_no']}"


def tag(t):
    return f"{t['count']} SRs  ·  JIRA YES {t['jira_yes']} / NO {t['jira_no']}"


THEMES = {a: AREAS[a]["themes"] for a in AREA_ORDER}
SRC = "Source: ServiceNow Service Request export (Recruiter Experience), snapshot-rx-crm-areas-jira-yn.json."
BY_COUNT = sorted(AREA_ORDER, key=lambda a: -AREAS[a]["count"])
PRI = sorted(
    ((THEME_AREA[th], next(t for t in AREAS[THEME_AREA[th]]["themes"]
                           if t["theme"] == th)) for th in PRIORITY_ORDER),
    key=lambda r: -r[1]["count"])
PRI_TOTAL = sum(t["count"] for _, t in PRI)
BIGGER = sorted((t for a in SNAP["areas"] for t in a["themes"]
                 if t["theme"] not in PRIORITY_ORDER), key=lambda t: -t["count"])[:2]
MOST_NO = max(AREA_ORDER, key=lambda a: AREAS[a]["jira_no"] / AREAS[a]["count"])
BIGGEST_NO = max(AREA_ORDER, key=lambda a: AREAS[a]["jira_no"])
YES_OVER_NO = [a for a in AREA_ORDER if AREAS[a]["jira_yes"] > AREAS[a]["jira_no"]]
assert len(YES_OVER_NO) == 1, YES_OVER_NO
TOP2_SHARE = round(sum(AREAS[a]["pct_of_filtered"] for a in BY_COUNT[:2]), 1)

# ================================================================== 1 cover
L_cover(
    IMAGERY / "rocket-cover-full.jpg",
    "What recruiters keep asking\nPhenom *to fix in CRM.*",
    f"{N:,} Service Requests  ·  {N_THEMES} themes",
    nts=f"This deck is a direct read-out of the ServiceNow Service Request export for "
        f"Recruiter Experience. {N:,} Service Requests were classified into "
        f"{N_THEMES} themes across four CRM areas. {JY} have a Jira created against "
        f"them and {JN} do not. Nothing here is inferred: every count, problem "
        f"statement and action comes from the same analysis that produces the RX "
        f"themes HTML report.")

# ========================================================== 2 cards · method
L_cards(
    "Method | How to read this deck",
    f"One export, four CRM areas, *{word(N_THEMES)} themes.*",
    "Every count in this deck is read straight from the export; nothing is estimated.",
    [
        {"tag": "01 | Scope", "title": "What is in scope",
         "body": "ServiceNow rows where Issue Type contains “Service Request” and "
                 "Product Experience contains “Recruiter Experience (RX)”. Both "
                 "Jira-created (Yes) and non-Jira (No) tickets are counted."},
        {"tag": "02 | Method", "title": "How themes are assigned",
         "body": f"Each ticket is matched once, by phrase rules run over its Short "
                 f"Description and Description. First match wins, so no ticket is "
                 f"counted twice. The {FUNNEL['unclassified']} tickets that match no "
                 f"rule are excluded rather than forced into a theme."},
        {"tag": "03 | Wording", "title": "What the wording means",
         "body": "“What the tickets say” summarises the recurring wording in those "
                 "Service Requests. “What to do in Phenom” is the product change "
                 "those tickets point to. No vendor claims, benchmarks or outside "
                 "sources are used.",
         "navy": True},
    ],
    callout=("Read this way", f"A theme belongs to exactly one CRM area, and a ticket "
                              f"to exactly one theme — so the four areas sum to {N:,}."),
    source="Source: all-service-requests.csv, filtered on Issue Type and Product "
           "Experience; theme rules in rx_theme_rules.py.",
    nts="Set expectations before any numbers land. The audience should know the "
        "filter, the one-ticket-one-theme rule, and that unclassified tickets were "
        "dropped rather than redistributed. The third card is the honesty card: no "
        "outside benchmarks appear anywhere in this deck.")

# ========================================================= 3 numbers · funnel
L_numbers(
    "The data | The funnel",
    f"From {FUNNEL['all']:,} rows to *{N:,} Service Requests.*",
    None,
    [
        {"big": f"{FUNNEL['all']:,}", "body": "rows in the ServiceNow export",
         "accent": False},
        {"big": f"{FUNNEL['service_request']:,}",
         "body": "Issue Type contains Service Request", "accent": False},
        {"big": f"{FUNNEL['rx']:,}",
         "body": "Product Experience is Recruiter Experience (RX)", "accent": False},
        {"big": f"{N:,}", "body": f"matched one of the {N_THEMES} CRM themes",
         "accent": True},
    ],
    closing=f"{EXCLUDED} RX Service Requests are excluded: "
            f"{FUNNEL['unclassified']} matched no theme rule, {NO_JIRA_VALUE} carry no "
            f"Jira Yes/No value.",
    source=SRC,
    nts=f"The funnel explains why {N:,} is the denominator for every percentage that "
        f"follows. Each step is a filter on the previous one, not a new query. The "
        f"{EXCLUDED} excluded tickets are named so nobody has to guess where the gap "
        f"between {FUNNEL['rx']:,} and {N:,} went.")

# ======================================================= 4 stats · at a glance
L_stats(
    "At a glance | Where the 1,164 land",
    f"{BY_COUNT[0].replace('CRM ', '')} and {BY_COUNT[1].replace('CRM ', '')} carry "
    f"*{TOP2_SHARE}% of the load.*",
    "Four CRM areas, in descending Service Request volume.",
    [{"label": a, "big": f"{AREAS[a]['count']}",
      "sub": f"{AREAS[a]['pct_of_filtered']}%  ·  Yes {AREAS[a]['jira_yes']} / "
             f"No {AREAS[a]['jira_no']}"} for a in BY_COUNT],
    [
        {"title": "The two largest areas",
         "body": f"{BY_COUNT[0]} ({AREAS[BY_COUNT[0]]['count']}) and {BY_COUNT[1]} "
                 f"({AREAS[BY_COUNT[1]]['count']}) together are {TOP2_SHARE}% of all "
                 f"CRM Service Requests."},
        {"title": f"{MOST_NO.replace('CRM ', '')} is the most non-Jira",
         "body": f"{AREAS[MOST_NO]['jira_no']} of its {AREAS[MOST_NO]['count']} "
                 f"Service Requests have no Jira created — "
                 f"{pct(AREAS[MOST_NO]['jira_no'], AREAS[MOST_NO]['count'])}, the "
                 f"highest share of any area."},
        {"title": f"{YES_OVER_NO[0].replace('CRM ', '')} is the exception",
         "body": f"It is the only area where Jira Yes "
                 f"({AREAS[YES_OVER_NO[0]]['jira_yes']}) outweighs Jira No "
                 f"({AREAS[YES_OVER_NO[0]]['jira_no']})."},
    ],
    callout=("The shape", f"Three of the four areas close more Service Requests "
                          f"without a Jira than with one."),
    source="Source: snapshot areas[].count and areas[].jira_yes / jira_no.",
    nts="Four numbers to remember: "
        + ", ".join("{} {}".format(a.replace("CRM ", ""), AREAS[a]["count"])
                    for a in BY_COUNT)
        + ". The three cards underneath are arithmetic on those same counts, not "
        f"interpretation of outside data. The shape matters more than any single "
        f"number: outbound messaging and the candidate record are where recruiters "
        f"hit Phenom hardest.")

# ====================================================== 5 compare · Jira split
L_compare(
    "The Jira split | Inside the 1,164",
    f"Just under half of this demand *reaches Jira.*",
    f"Summed across the four CRM areas. The funnel's {FUNNEL['jira_Yes']} / "
    f"{FUNNEL['jira_No']} are pre-classification figures for all "
    f"{FUNNEL['jira_yes_or_no']:,} RX Service Requests that carry a Jira value.",
    [
        {"tag": "Jira created · Yes", "title": "Reaches engineering", "stats": True,
         "rows": [(f"{JY}", f"Service Requests with a Jira created — "
                            f"{pct(JY, N)} of the {N:,}"),
                  (f"{AREAS[YES_OVER_NO[0]]['jira_yes']}",
                   f"of them are {YES_OVER_NO[0]}, the only area where Yes "
                   f"outweighs No")]},
        {"tag": "No Jira · No", "title": "Closed in Support", "stats": True,
         "navy": True,
         "rows": [(f"{JN}", f"Service Requests with no Jira — {pct(JN, N)} of the "
                            f"{N:,}"),
                  (f"{AREAS[BIGGEST_NO]['jira_no']}",
                   f"of them are {BIGGEST_NO}, the largest non-Jira block of any "
                   f"area")]},
    ],
    callout=("Why it matters", f"The {JN} Service Requests with no Jira do not appear "
                               f"anywhere in Jira."),
    source=f"Source: sum of snapshot areas[].jira_yes / jira_no ({JY} + {JN} = "
           f"{N:,}); funnel.jira_Yes {FUNNEL['jira_Yes']} and funnel.jira_No "
           f"{FUNNEL['jira_No']} cover all {FUNNEL['jira_yes_or_no']:,} RX Service "
           f"Requests before theme classification.",
    nts=f"This is the correction slide. The funnel's {FUNNEL['jira_Yes']} / "
        f"{FUNNEL['jira_No']} count every RX Service Request before theme "
        f"classification and sum to {FUNNEL['jira_yes_or_no']:,}, not {N:,}. The true "
        f"split inside the classified set is {JY} Yes and {JN} No, summed across "
        f"areas, and the build asserts that those two add to {N:,}. Say the "
        f"{pct(JN, N)} out loud — it is the reason this deck exists.")

# ============================================================ 6 divider · 01
L_divider(
    IMAGERY / "clouds-black-full.jpg", "01", "Part 1 | The tickets",
    "What the Service Requests *actually say.*",
    f"Four CRM areas, {word(N_THEMES)} themes, each area in descending volume.",
    mode="top",
    nts="Act break. Everything before this slide was method and shape; everything "
        "after is the tickets' own wording. Two slides per group: what the tickets "
        "say, then what to do in Phenom.")

# ==================================================== 7-18 the four CRM areas
def say_cards(area, idx, chunk, chunk_i, n_chunks, blurb):
    a = AREAS[area]
    covered = sum(t["count"] for t in chunk)
    top = max(chunk, key=lambda t: t["count"])
    if n_chunks == 1:
        title = f"{word(len(chunk)).capitalize()} themes, *{covered} of the {a['count']}.*"
    elif chunk_i == 0:
        title = f"Three themes carry *{covered} of the {a['count']}.*"
    else:
        title = f"The other {word(len(chunk))} carry *{covered}.*"
    L_cards(
        f"{area} | Area {idx} of 4", title, blurb,
        [{"tag": tag(t), "title": t["theme"],
          "body": THEME_PLAYBOOK[t["theme"]]["problem"],
          "navy": i == len(chunk) - 1 and chunk_i == n_chunks - 1}
         for i, t in enumerate(chunk)],
        callout=("The point", f"{top['theme']} is the largest theme here: "
                              f"{top['count']} Service Requests, {top['jira_no']} of "
                              f"them without a Jira."),
        source=SRC,
        nts=f"{area}: {a['count']} Service Requests, Jira Yes {a['jira_yes']} and "
            f"Jira No {a['jira_no']}. Each card is one theme; the paragraph is the "
            f"recurring wording in those tickets, not a summary written for this "
            f"deck. Read the largest card aloud and let the others be reference.")


def say_compare(area, idx, themes, blurb=None):
    a = AREAS[area]
    if area == BY_COUNT[-1]:
        title = f"Smallest area. *Highest share without a Jira.*"
    else:
        top = max(themes, key=lambda t: t["count"])
        title = f"Two themes. *{top['count']} of the {a['count']} are one of them.*"
    L_compare(
        f"{area} | Area {idx} of 4", title, blurb,
        [{"tag": tag(t), "title": t["theme"], "navy": i == 1,
          "rows": [("What it covers", THEME_PLAYBOOK[t["theme"]]["means"]),
                   ("What the tickets say", THEME_PLAYBOOK[t["theme"]]["problem"])]}
         for i, t in enumerate(themes)],
        callout=("The point", f"{max(themes, key=lambda t: t['count'])['theme']} alone "
                              f"is {max(t['count'] for t in themes)} of the area's "
                              f"{a['count']} Service Requests."),
        source=SRC,
        nts=f"{area} has only {len(themes)} themes, so both fit side by side with what "
            f"each one covers and what the tickets say. Area totals: {a['count']} "
            f"Service Requests, Jira Yes {a['jira_yes']} and Jira No {a['jira_no']}. "
            f"The navy column is the smaller theme, not the less important one.")


def do_rows(area, idx, chunk, chunk_i, n_chunks, offset, sub=None):
    a = AREAS[area]
    covered = sum(t["count"] for t in chunk)
    which = (" *Both themes.*" if n_chunks == 1 else
             (" *The top three.*" if chunk_i == 0 else " *The other three.*"))
    L_rows(
        f"{area} | What to do", f"What to do in Phenom.{which}", sub,
        [{"label": t["theme"], "meta": meta(t),
          "body": THEME_PLAYBOOK[t["theme"]]["reduce"]} for t in chunk],
        callout=("For Phenom",
                 f"Both themes, all {covered} of {area}'s Service Requests."
                 if covered == a["count"] else
                 f"These {len(chunk)} themes are {covered} of {area}'s "
                 f"{a['count']} Service Requests — {pct(covered, a['count'])}."),
        source=SRC,
        nts=f"{area} — actions for "
            f"{', '.join(t['theme'] for t in chunk)}. These {len(chunk)} themes "
            f"account for {covered} of the area's {a['count']} Service Requests. "
            f"Every bullet is the product change the tickets in that theme are "
            f"asking for; none of it is a roadmap commitment.")


def do_chain(area, idx, chunk, offset):
    a = AREAS[area]
    covered = sum(t["count"] for t in chunk)
    L_chain(
        f"{area} | What to do", "What to do in Phenom. *The other three.*", None,
        [{"num": f"{offset + i + 1:02d}", "title": t["theme"],
          "body": THEME_PLAYBOOK[t["theme"]]["reduce"]} for i, t in enumerate(chunk)],
        callout=("For Phenom", f"These {len(chunk)} themes are {covered} of "
                               f"{area}'s {a['count']} Service Requests — "
                               f"{pct(covered, a['count'])}."),
        source=SRC,
        nts=f"{area} — the long tail. {', '.join(t['theme'] for t in chunk)} are "
            f"{covered} of the area's {a['count']} Service Requests between them. "
            f"The numbering continues the area's descending-volume order, so 0"
            f"{offset + 1} is the fourth-largest theme. Skip quickly unless someone "
            f"asks.")


for idx, area in enumerate(AREA_ORDER, start=1):
    themes = THEMES[area]
    blurb = AREA_BLURB[area]
    if len(themes) <= 2:
        # the area blurb rides on the action slide here: the compare columns need
        # the vertical room the 3-line subtitle would take
        say_compare(area, idx, themes)
        do_rows(area, idx, themes, 0, 1, 0, sub=blurb)
    else:
        chunks = [themes[i:i + 3] for i in range(0, len(themes), 3)]
        for ci, chunk in enumerate(chunks):
            say_cards(area, idx, chunk, ci, len(chunks), blurb if ci == 0 else None)
            if ci == 0:
                do_rows(area, idx, chunk, ci, len(chunks), 0)
            else:
                do_chain(area, idx, chunk, ci * 3)

# =========================================================== 19 divider · 02
L_divider(
    IMAGERY / "sunset-band-full.jpg", "02", "Part 2 | Where to start",
    f"{word(len(PRI)).capitalize()} priority themes.",
    "Ranked by Service Request volume.",
    mode="band",
    nts=f"Second act break. The priority list is PRIORITY_ORDER from "
        f"rx_theme_playbook.py — it is carried over, not derived from volume, which "
        f"is why the next slide has to say what it is not.")

# =============================================================== 20 table
L_table(
    "Where to start | The priority list",
    f"The {word(len(PRI))} priority themes, *by Service Request volume.*",
    f"Not the {word(len(PRI))} largest: "
    + " and ".join(f"{b['theme']} ({b['count']})" for b in BIGGER)
    + " are bigger but sit outside the priority list.",
    ["Theme", "Area", f"SRs  ·  % of {N:,}", "Jira Yes / No"],
    [45, 19, 20, 16],
    [[t["theme"], area,
      f"{t['count']}  ·  {t['pct_of_filtered']}%",
      f"{t['jira_yes']} / {t['jira_no']}"] for area, t in PRI],
    callout=("For Phenom", f"Together the {word(len(PRI))} are {PRI_TOTAL} of the {N:,} "
                           f"Service Requests — {pct(PRI_TOTAL, N)}."),
    source="Source: PRIORITY_ORDER in rx_theme_playbook.py; counts from the snapshot.",
    nts=f"These are the {word(len(PRI))} priority themes carried over from the RX theme "
        f"playbook, shown in descending ticket volume. They are deliberately not the "
        f"{word(len(PRI))} largest themes — "
        + " and ".join(f"{b['theme']} ({b['count']})" for b in BIGGER)
        + f" are larger but sit outside the priority list. Together the {word(len(PRI))} "
          f"cover {PRI_TOTAL} of the {N:,} Service Requests.")

# ============================================================= 21 takeaway
L_takeaway(
    "The takeaway",
    "More than half of this demand *never becomes a Jira ticket.*",
    [
        {"title": f"{JN} of {N:,}",
         "body": f"CRM Service Requests have no Jira created against them — "
                 f"{pct(JN, N)} of the total."},
        {"title": f"{PRI_TOTAL} of {N:,}",
         "body": f"are covered by the {word(len(PRI))} priority themes — "
                 f"{pct(PRI_TOTAL, N)} of the total."},
        {"title": f"{word(N_THEMES).capitalize()} themes, four areas",
         "body": f"One ticket matches one theme. {FUNNEL['unclassified']} "
                 f"unclassified tickets were excluded, not redistributed."},
    ],
    closing="Source: ServiceNow Service Request export, Recruiter Experience, "
            "Jira Yes and No.",
    nts=f"Close on the Jira No number. These {JN} Service Requests were handled by "
        f"Support without an engineering ticket, so the demand they represent does "
        f"not appear in Jira. The priority-theme figure is the sum of the six themes "
        f"on the previous slide. Nothing on this slide is new — it is the same "
        f"arithmetic, said once more.")

# ------------------------------------------------------------------- checks
def _serif_strings():
    """Every string this build renders in Fraunces, for the glyph assertion."""
    out = []
    for i, s in enumerate(prs.slides, start=1):
        for shp in s.shapes:
            if not shp.has_text_frame:
                continue
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name == SERIF:
                        out.append((i, r.text))
    return out


bad = [(i, t) for i, t in _serif_strings() if any(c in t for c in SERIF_GAPS)]
assert not bad, f"Fraunces has no glyph for {SERIF_GAPS!r}: {bad}"

out = Path(__file__).with_name("RX-CRM-Service-Request-Playbook.pptx")
prs.save(out)
print(f"{len(prs.slides.__iter__.__self__._sldIdLst)} slides -> {out}")
for i, layout, title in PLAN:
    print(f"  {i:>2}  {layout:<9}  {title}")
