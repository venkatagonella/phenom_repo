#!/usr/bin/env python3
"""Simplified RX CRM SR playbook — clean two-column Theme | Jira ID tables.

Reads theme-jira-rows.json (board 1091 open 2026+ mappings). Unmapped → TBD.
Visual: white canvas, navy title, light gray table header, Poppins, 16:9.
"""
from __future__ import annotations

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

OUT_DIR = Path(__file__).resolve().parent
# …/phenom-master-copilot/.cursor/skills/phenom-slide-creator/output-decks/rx-crm-sr-playbook
ROOT = OUT_DIR.parents[4]
KB = ROOT / "product-copilot-beta/knowledge/servicenow-service-requests"
ROWS = json.loads((OUT_DIR / "theme-jira-rows.json").read_text())

# Phenom corporate tokens (clean)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PAPER = RGBColor(0xF7, 0xF8, 0xFA)
INK = RGBColor(0x1A, 0x1A, 0x2E)
BODY = RGBColor(0x33, 0x33, 0x33)
MUTED = RGBColor(0x66, 0x66, 0x66)
NAVY = RGBColor(0x00, 0x2A, 0x5C)
MINT = RGBColor(0x00, 0xC1, 0xB5)
LINE = RGBColor(0xE2, 0xE5, 0xEB)
HEADER_BG = RGBColor(0xEE, 0xF1, 0xF6)
TBD = RGBColor(0x99, 0x99, 0x99)

SANS = "Poppins"
ROWS_PER_SLIDE = 9
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def set_run(run, text, size=14, bold=False, color=BODY, font=SANS):
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    # East Asian / complex script name for PowerPoint consistency
    rPr = run._r.get_or_add_rPr()
    for tag in ("latin", "ea", "cs"):
        el = rPr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{tag}"))
        el.set("typeface", font)


def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def solid_bg(slide, color=WHITE):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def title_block(slide, title, subtitle=None):
    box = add_textbox(slide, Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.55))
    p = box.text_frame.paragraphs[0]
    p.clear()
    set_run(p.add_run(), title, size=26, bold=True, color=NAVY)
    if subtitle:
        sub = add_textbox(slide, Inches(0.6), Inches(0.85), Inches(12.1), Inches(0.35))
        sp = sub.text_frame.paragraphs[0]
        sp.clear()
        set_run(sp.add_run(), subtitle, size=12, bold=False, color=MUTED)


def footer(slide, page, total):
    box = add_textbox(slide, Inches(0.6), Inches(7.05), Inches(10), Inches(0.3))
    p = box.text_frame.paragraphs[0]
    p.clear()
    set_run(p.add_run(), "RX CRM · Service Request themes → Jira mapping", size=10, color=MUTED)
    num = add_textbox(slide, Inches(11.5), Inches(7.05), Inches(1.2), Inches(0.3))
    np = num.text_frame.paragraphs[0]
    np.alignment = PP_ALIGN.RIGHT
    np.clear()
    set_run(np.add_run(), f"{page} / {total}", size=10, color=MUTED)


def rgb_hex(color: RGBColor) -> str:
    return f"{int(color[0]):02X}{int(color[1]):02X}{int(color[2]):02X}"


def set_cell_shading(cell, color: RGBColor):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag == qn("a:solidFill"):
            tcPr.remove(child)
    solid = etree.SubElement(tcPr, qn("a:solidFill"))
    srgb = etree.SubElement(solid, qn("a:srgbClr"))
    srgb.set("val", rgb_hex(color))


def fill_cell(cell, text, size=12, bold=False, color=BODY, align=PP_ALIGN.LEFT):
    cell.text = ""
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    p.clear()
    set_run(p.add_run(), text, size=size, bold=bold, color=color)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def add_two_col_table(slide, rows, left=0.6, top=1.35, width=12.1, height=5.4):
    """rows: list of (theme, jira). Includes header."""
    n = len(rows) + 1
    table_shape = slide.shapes.add_table(n, 2, Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table
    table.columns[0].width = Inches(width * 0.48)
    table.columns[1].width = Inches(width * 0.52)

    fill_cell(table.cell(0, 0), "SR theme", size=12, bold=True, color=NAVY)
    fill_cell(table.cell(0, 1), "Initiative / Epic / Story", size=12, bold=True, color=NAVY)
    set_cell_shading(table.cell(0, 0), HEADER_BG)
    set_cell_shading(table.cell(0, 1), HEADER_BG)

    for i, (theme, jira) in enumerate(rows, start=1):
        fill_cell(table.cell(i, 0), theme, size=12, bold=False, color=BODY)
        is_tbd = (jira == "TBD")
        fill_cell(
            table.cell(i, 1),
            jira,
            size=11,
            bold=False,
            color=TBD if is_tbd else BODY,
        )
        bg = WHITE if i % 2 else PAPER
        set_cell_shading(table.cell(i, 0), bg)
        set_cell_shading(table.cell(i, 1), bg)

    # tighten row heights roughly evenly
    row_h = int(Inches(height) / n)
    for row in table.rows:
        row.height = row_h
    return table


def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]

    slides_meta = []  # (builder_fn args) collected then rendered with page numbers

    # --- plan slides ---
    plan = []

    def cover():
        return ("cover", None)

    plan.append(("cover", None))
    plan.append(("method", None))
    plan.append(("summary", None))
    for area in ROWS["areas"]:
        plan.append(("section", area))
        pairs = [(r["theme"], r["jira"]) for r in area["rows"]]
        chunks = list(chunk(pairs, ROWS_PER_SLIDE))
        for idx, ch in enumerate(chunks):
            plan.append(("table", (area, ch, idx + 1, len(chunks))))
    plan.append(("close", None))

    total = len(plan)

    for page, (kind, payload) in enumerate(plan, start=1):
        slide = prs.slides.add_slide(blank)
        solid_bg(slide, WHITE)

        if kind == "cover":
            # accent bar
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.12))
            bar.fill.solid()
            bar.fill.fore_color.rgb = MINT
            bar.line.fill.background()
            t = add_textbox(slide, Inches(0.8), Inches(2.4), Inches(11.5), Inches(1.2))
            p = t.text_frame.paragraphs[0]
            p.clear()
            set_run(p.add_run(), "RX CRM Service Request themes", size=36, bold=True, color=NAVY)
            s = add_textbox(slide, Inches(0.8), Inches(3.5), Inches(11.5), Inches(0.8))
            sp = s.text_frame.paragraphs[0]
            sp.clear()
            set_run(
                sp.add_run(),
                "Mapped to open 2026 Initiative / Epic / Story IDs · Unmapped themes marked TBD",
                size=16,
                color=BODY,
            )
            m = add_textbox(slide, Inches(0.8), Inches(4.5), Inches(11.5), Inches(0.5))
            mp = m.text_frame.paragraphs[0]
            mp.clear()
            set_run(mp.add_run(), "CRM Core · Profile · Messaging · Automations", size=14, color=MUTED)

        elif kind == "method":
            title_block(slide, "How to read this deck", "One table pattern on every content slide")
            rows = [
                ("SR theme", "Customer-reported theme from the Service Request analysis"),
                ("Initiative / Epic / Story", "Open PHEM IDs on the CRM board, created on or after 1 Jan 2026"),
                ("TBD", "No open Initiative, Epic, or Story mapped to this theme yet"),
            ]
            add_two_col_table(slide, rows, top=1.5, height=2.6)
            note = add_textbox(slide, Inches(0.6), Inches(4.5), Inches(12.1), Inches(1.5))
            tf = note.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.clear()
            set_run(
                p.add_run(),
                "Done and Blocked items are excluded. Mapping is title-based against the CRM board "
                "(same rules as the SR themes HTML report). IDs are listed as Init / Epic / Story.",
                size=13,
                color=MUTED,
            )

        elif kind == "summary":
            title_block(slide, "Coverage at a glance", ROWS["source"])
            # Custom header labels for this slide
            pairs = [
                (
                    a["label"],
                    f"{a['mapped']} of {a['total']} themes mapped · {a['total'] - a['mapped']} TBD",
                )
                for a in ROWS["areas"]
            ]
            table_shape = slide.shapes.add_table(
                len(pairs) + 1, 2, Inches(0.6), Inches(1.5), Inches(12.1), Inches(3.2)
            )
            table = table_shape.table
            table.columns[0].width = Inches(12.1 * 0.48)
            table.columns[1].width = Inches(12.1 * 0.52)
            fill_cell(table.cell(0, 0), "Area", size=12, bold=True, color=NAVY)
            fill_cell(table.cell(0, 1), "Mapped themes", size=12, bold=True, color=NAVY)
            set_cell_shading(table.cell(0, 0), HEADER_BG)
            set_cell_shading(table.cell(0, 1), HEADER_BG)
            for i, (area, cov) in enumerate(pairs, start=1):
                fill_cell(table.cell(i, 0), area, size=12, color=BODY)
                fill_cell(table.cell(i, 1), cov, size=12, color=BODY)
                bg = WHITE if i % 2 else PAPER
                set_cell_shading(table.cell(i, 0), bg)
                set_cell_shading(table.cell(i, 1), bg)

        elif kind == "section":
            area = payload
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.12))
            bar.fill.solid()
            bar.fill.fore_color.rgb = MINT
            bar.line.fill.background()
            t = add_textbox(slide, Inches(0.8), Inches(2.8), Inches(11.5), Inches(1.0))
            p = t.text_frame.paragraphs[0]
            p.clear()
            set_run(p.add_run(), area["label"], size=40, bold=True, color=NAVY)
            s = add_textbox(slide, Inches(0.8), Inches(3.9), Inches(11.5), Inches(0.6))
            sp = s.text_frame.paragraphs[0]
            sp.clear()
            set_run(
                sp.add_run(),
                f"{area['mapped']} of {area['total']} themes have an open Jira mapping",
                size=18,
                color=BODY,
            )

        elif kind == "table":
            area, ch, part, parts = payload
            subtitle = area["label"] if parts == 1 else f"{area['label']} · {part} of {parts}"
            title_block(slide, "SR theme → Jira", subtitle)
            add_two_col_table(slide, ch, top=1.35, height=5.4)

        elif kind == "close":
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.12))
            bar.fill.solid()
            bar.fill.fore_color.rgb = MINT
            bar.line.fill.background()
            t = add_textbox(slide, Inches(0.8), Inches(2.6), Inches(11.5), Inches(1.0))
            p = t.text_frame.paragraphs[0]
            p.clear()
            set_run(p.add_run(), "Next step: replace every TBD", size=32, bold=True, color=NAVY)
            s = add_textbox(slide, Inches(0.8), Inches(3.7), Inches(11.5), Inches(1.2))
            tf = s.text_frame
            tf.word_wrap = True
            sp = tf.paragraphs[0]
            sp.clear()
            set_run(
                sp.add_run(),
                "Themes marked TBD have open Service Request volume but no open 2026 Initiative, "
                "Epic, or Story on the CRM board. Use them to seed backlog coverage.",
                size=16,
                color=BODY,
            )

        if kind not in ("cover", "section", "close"):
            footer(slide, page, total)
        else:
            # still number cover/section/close lightly
            num = add_textbox(slide, Inches(11.5), Inches(7.05), Inches(1.2), Inches(0.3))
            np = num.text_frame.paragraphs[0]
            np.alignment = PP_ALIGN.RIGHT
            np.clear()
            set_run(np.add_run(), f"{page} / {total}", size=10, color=MUTED)

    out1 = OUT_DIR / "RX-CRM-Service-Request-Playbook.pptx"
    out2 = KB / "RX-CRM-Service-Request-Playbook.pptx"
    prs.save(out1)
    prs.save(out2)
    print(f"slides={total} wrote {out1}")
    print(f"wrote {out2}")


if __name__ == "__main__":
    build()
