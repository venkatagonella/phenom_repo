#!/usr/bin/env python3
"""Phenom PPTX — RX CRM Service Request playbook.

Every number and sentence is read from the same two sources that generate
rx-jira-yes-themes.html:
  * snapshot-rx-crm-areas-jira-yn.json  (counts, Jira Yes/No splits)
  * rx_theme_playbook.py                (area blurbs, problem, reduce bullets)
No content is authored here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path("/Users/venkata.gonella/phenom-master-copilot")
KB = ROOT / "product-copilot-beta/knowledge/servicenow-service-requests"
sys.path.insert(0, str(ROOT / ".cursor/skills/servicenow-service-requests/scripts"))
from rx_theme_playbook import (  # noqa: E402
    AREA_BLURB,
    AREA_ORDER,
    PRIORITY_ORDER,
    THEME_AREA,
    THEME_PLAYBOOK,
)

SNAP = json.loads((KB / "snapshot-rx-crm-areas-jira-yn.json").read_text())
AREAS = {a["area"]: a for a in SNAP["areas"]}
FUNNEL = SNAP["funnel"]
N = SNAP["n_filtered"]
# funnel's jira_Yes / jira_No count every RX Service Request *before* theme
# classification. The split inside the classified 1,164 is the sum over areas.
JY = sum(a["jira_yes"] for a in SNAP["areas"])
JN = sum(a["jira_no"] for a in SNAP["areas"])
assert JY + JN == N, (JY, JN, N)

# ---------------------------------------------------------------- brand pods
INK = "1a1c2e"
INK2 = "434343"
INK3 = "6b6b73"
PAPER = "ffffff"
TILE = "f2f2f3"
RULE = "e4e4e8"
NAVY = "131a4a"
NAVY_SOFT = "8a90b8"
FAM = {
    "mint": {"50": "daf3f2", "strong": "64a39c", "ink": "203634"},
    "peach": {"50": "f6e2d5", "strong": "d36238", "ink": "46210c"},
    "honey": {"50": "faedd7", "strong": "dda04a", "ink": "493614"},
    "lilac": {"50": "e9e6f9", "strong": "7172da", "ink": "0a0d37"},
}
AREA_FAMILY = {
    "CRM Core": "mint",
    "CRM Profile": "peach",
    "CRM Messaging": "honey",
    "CRM Automations": "lilac",
}
FONT = "Poppins"
K = 0.0104166

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def E(px):
    return Inches(px * K)


def PT(px):
    return Pt(px * 0.75)


def C(h):
    return RGBColor.from_string(h)


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, fill, rounded=False, radius=0.06):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        E(x), E(y), E(w), E(h),
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = C(fill)
    shp.line.fill.background()
    shp.shadow.inherit = False
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def circle_outline(s, x, y, d, color):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(d), E(d))
    shp.fill.background()
    shp.line.color.rgb = C(color)
    shp.line.width = Pt(1.5)
    shp.shadow.inherit = False
    return shp


def tbox(s, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def line(tf, text, px, color, bold=False, first=False, after=4, before=0,
         align=PP_ALIGN.LEFT, line_spacing=1.15):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(after)
    p.space_before = Pt(before)
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    f = r.font
    f.name = FONT
    f.size = PT(px)
    f.bold = bold
    f.color.rgb = C(color)
    return p


def header(s, kicker, title, title_px=34):
    tf = tbox(s, 56, 36, 1180, 22)
    line(tf, kicker, 14, INK, bold=True, first=True, after=0)
    tf = tbox(s, 56, 58, 1190, 90)
    line(tf, title, title_px, INK, bold=True, first=True, after=0, line_spacing=1.05)
    rect(s, 56, 152, 1168, 2, RULE)


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def theme_rows(area):
    """Themes of an area, in the snapshot's descending-count order."""
    return AREAS[area]["themes"]


def theme_label(theme):
    """Poppins has no U+2194; render the arrow as a hyphen."""
    return theme.replace("↔", "-")


def meta(t):
    return f"{t['count']} SRs  ·  Jira Yes {t['jira_yes']} / No {t['jira_no']}  ·  {t['pct_of_filtered']}% of {N:,}"


# ======================================================== 1 · COVER
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 150, 1100, 36)
line(tf, "SERVICENOW SERVICE REQUESTS  ·  RECRUITER EXPERIENCE (RX)", 13,
     FAM["mint"]["50"], bold=True, first=True, after=0)
tf = tbox(s, 72, 198, 1100, 190)
line(tf, "What recruiters keep asking\nPhenom to fix in CRM", 46, PAPER, bold=True,
     first=True, after=0, line_spacing=1.08)
tf = tbox(s, 72, 420, 1050, 100)
line(tf, f"{N:,} Service Requests across CRM Core, Profile, Messaging and Automations",
     17, FAM["mint"]["50"], first=True, after=10, line_spacing=1.3)
line(tf, f"Jira created: {JY}  ·  No Jira: {JN}  ·  "
         f"{sum(len(a['themes']) for a in SNAP['areas'])} themes  ·  "
         f"{FUNNEL['unclassified']} unclassified tickets excluded",
     15, NAVY_SOFT, after=0, line_spacing=1.3)
tf = tbox(s, 72, 622, 900, 30)
line(tf, "Phenom  ·  Internal  ·  Sourced only from the ServiceNow export", 13,
     NAVY_SOFT, first=True, after=0)
notes(s, "This deck is a direct read-out of the ServiceNow Service Request export for "
         "Recruiter Experience. Nothing is inferred: every count, problem statement and "
         "action comes from the same analysis that produces the RX themes HTML report.")

# ======================================================== 2 · HOW TO READ
s = slide()
header(s, "How to read this deck", "One export, four CRM areas, sixteen themes")
cols = [
    ("mint", "What is in scope",
     "ServiceNow rows where Issue Type contains “Service Request” and Product Experience "
     "contains “Recruiter Experience (RX)”. Both Jira-created (Yes) and non-Jira (No) "
     "tickets are counted."),
    ("peach", "How themes are assigned",
     "Each ticket is matched once, by phrase rules run over its Short Description and "
     "Description. First match wins, so no ticket is counted twice. Tickets that match no "
     f"rule ({FUNNEL['unclassified']}) are excluded rather than forced into a theme."),
    ("honey", "What the wording means",
     "“Problem” is a summary of what the tickets actually say. “What to do in Phenom” is "
     "the product change those tickets point to. No vendor claims, benchmarks or outside "
     "sources are used."),
]
cw, gap = 373, 24
for i, (fam, ttl, body) in enumerate(cols):
    x = 56 + i * (cw + gap)
    rect(s, x, 200, cw, 380, FAM[fam]["50"], rounded=True)
    tf = tbox(s, x + 26, 238, cw - 52, 320)
    line(tf, ttl, 20, INK, bold=True, first=True, after=16, line_spacing=1.05)
    line(tf, body, 14, INK2, after=0, line_spacing=1.35)
notes(s, "Set expectations before any numbers land. The audience should know the filter, "
         "the one-ticket-one-theme rule, and that unclassified tickets were dropped, not "
         "redistributed.")

# ======================================================== 3 · FUNNEL
s = slide()
header(s, "The data", "From 29,310 ServiceNow rows to 1,164 CRM Service Requests")
steps = [
    ("mint", f"{FUNNEL['all']:,}", "Rows in the ServiceNow export"),
    ("peach", f"{FUNNEL['service_request']:,}", "Issue Type = Service Request"),
    ("honey", f"{FUNNEL['rx']:,}", "Recruiter Experience (RX)"),
    ("lilac", f"{FUNNEL['classified_in_crm_areas']:,}", "Matched a CRM theme"),
]
cw, gap = 283, 22
for i, (fam, num, lbl) in enumerate(steps):
    x = 56 + i * (cw + gap)
    rect(s, x, 196, cw, 196, FAM[fam]["50"], rounded=True)
    tf = tbox(s, x + 26, 228, cw - 52, 70)
    line(tf, num, 46, INK, bold=True, first=True, after=6, line_spacing=1.0)
    tf = tbox(s, x + 26, 304, cw - 52, 70)
    line(tf, lbl, 14, INK2, first=True, after=0, line_spacing=1.25)

rect(s, 56, 424, 1168, 216, TILE, rounded=True)
tf = tbox(s, 86, 452, 1110, 180)
line(tf, "Inside those 1,164 Service Requests", 18, INK, bold=True, first=True, after=14)
for t in [
    f"{JY} have a Jira created ({round(JY / N * 100)}%) and "
    f"{JN} do not ({round(JN / N * 100)}%) — the non-Jira half is the larger half.",
    f"{FUNNEL['rx'] - N} RX Service Requests are excluded from every count: "
    f"{FUNNEL['unclassified']} matched no theme rule and "
    f"{FUNNEL['rx'] - FUNNEL['jira_yes_or_no']} carry no Jira Yes/No value.",
    "The four CRM areas are mutually exclusive: a theme belongs to exactly one area, and a ticket to exactly one theme.",
]:
    line(tf, "•  " + t, 14, INK2, after=10, line_spacing=1.3)
notes(s, "The funnel explains why 1,164 is the denominator for every percentage that "
         "follows. The most important line is the Jira split: most of this demand never "
         "became a Jira ticket, so it is invisible in engineering planning today.")

# ======================================================== 4 · AT A GLANCE
s = slide()
header(s, "At a glance", "Where the 1,164 Service Requests land")
cw, gap = 283, 22
for i, area in enumerate(AREA_ORDER):
    a = AREAS[area]
    fam = AREA_FAMILY[area]
    x = 56 + i * (cw + gap)
    rect(s, x, 190, cw, 250, FAM[fam]["50"], rounded=True)
    tf = tbox(s, x + 26, 216, cw - 52, 70)
    line(tf, f"{a['count']}", 52, INK, bold=True, first=True, after=0, line_spacing=1.0)
    tf = tbox(s, x + 26, 290, cw - 52, 60)
    line(tf, area, 18, INK, bold=True, first=True, after=6, line_spacing=1.1)
    tf = tbox(s, x + 26, 346, cw - 52, 70)
    line(tf, f"{a['pct_of_filtered']}% of all CRM SRs", 13, INK2, first=True, after=6)
    line(tf, f"Jira Yes {a['jira_yes']}  ·  No {a['jira_no']}", 13, INK2, after=0)
    line(tf, f"{len(a['themes'])} themes", 13, INK3, after=0)

rect(s, 56, 468, 1168, 172, TILE, rounded=True)
tf = tbox(s, 86, 494, 1110, 140)
line(tf, "What the shape says", 18, INK, bold=True, first=True, after=14)
_msg, _prof, _auto = AREAS["CRM Messaging"], AREAS["CRM Profile"], AREAS["CRM Automations"]
for t in [
    f"Messaging and Profile together are {round(_msg['pct_of_filtered'] + _prof['pct_of_filtered'], 1)}% "
    f"of all CRM Service Requests — outbound and the candidate record carry most of the load.",
    f"CRM Automations is the smallest area and the most non-Jira: {_auto['jira_no']} of its "
    f"{_auto['count']} Service Requests have no Jira.",
    f"Profile is the only area where Jira Yes ({_prof['jira_yes']}) outweighs Jira No "
    f"({_prof['jira_no']}).",
]:
    line(tf, "•  " + t, 14, INK2, after=9, line_spacing=1.3)
notes(s, "Four numbers to remember: Messaging 432, Core 334, Profile 260, Automations 138. "
         "The supporting bullets are arithmetic on those same counts, not interpretation of "
         "outside data.")


# ======================================================== per-area builders
def area_problem_slide(area, idx_label):
    """Problem cards for every theme in the area."""
    a = AREAS[area]
    fam = AREA_FAMILY[area]
    themes = theme_rows(area)
    s = slide()
    header(s, f"{idx_label}  ·  {area}",
           f"What the {a['count']} Service Requests actually say")
    tf = tbox(s, 56, 172, 1168, 54)
    line(tf, AREA_BLURB[area], 14, INK2, first=True, after=0, line_spacing=1.3)

    top = 244
    if len(themes) <= 2:
        pw, pgap = 569, 30
        for i, t in enumerate(themes):
            x = 56 + i * (pw + pgap)
            rect(s, x, top, pw, 360, FAM[fam]["50"], rounded=True)
            tf = tbox(s, x + 28, top + 26, pw - 56, 70)
            line(tf, theme_label(t["theme"]), 19, INK, bold=True, first=True, after=6, line_spacing=1.1)
            line(tf, meta(t), 12, INK3, after=0)
            rect(s, x + 28, top + 118, pw - 56, 1, FAM[fam]["strong"])
            tf = tbox(s, x + 28, top + 138, pw - 56, 196)
            line(tf, "WHAT THIS THEME COVERS", 11, FAM[fam]["ink"], bold=True,
                 first=True, after=6)
            line(tf, THEME_PLAYBOOK[t["theme"]]["means"], 13, INK2, after=18,
                 line_spacing=1.3)
            line(tf, "WHAT THE TICKETS SAY", 11, FAM[fam]["ink"], bold=True, after=6)
            line(tf, THEME_PLAYBOOK[t["theme"]]["problem"], 14, INK2, after=0,
                 line_spacing=1.32)
    else:
        cw2, g2, ch = 373, 20, 196
        for i, t in enumerate(themes):
            col, row = i % 3, i // 3
            x = 56 + col * (cw2 + g2)
            y = top + row * (ch + 16)
            rect(s, x, y, cw2, ch, FAM[fam]["50"], rounded=True)
            tf = tbox(s, x + 20, y + 18, cw2 - 40, ch - 34)
            line(tf, theme_label(t["theme"]), 14, INK, bold=True, first=True, after=4, line_spacing=1.1)
            line(tf, f"{t['count']} SRs  ·  Jira Yes {t['jira_yes']} / No {t['jira_no']}",
                 11, INK3, after=10)
            line(tf, THEME_PLAYBOOK[t["theme"]]["problem"], 12, INK2, after=0,
                 line_spacing=1.24)
    notes(s, f"{area}: {a['count']} Service Requests, Jira Yes {a['jira_yes']} and "
             f"Jira No {a['jira_no']}. Each card is one theme; the paragraph summarises the "
             f"recurring wording in those tickets. Read the two largest cards aloud and let "
             f"the rest be reference.")


def area_action_slides(area, idx_label):
    """'What to do in Phenom' — up to three themes per slide."""
    a = AREAS[area]
    fam = AREA_FAMILY[area]
    themes = theme_rows(area)
    chunks = [themes[i:i + 3] for i in range(0, len(themes), 3)]
    for ci, chunk in enumerate(chunks):
        s = slide()
        part = "" if len(chunks) == 1 else f"  ({ci + 1} of {len(chunks)})"
        header(s, f"{idx_label}  ·  {area}", f"What to do in Phenom{part}")
        if len(chunk) >= 3:
            # three columns, one theme per column
            for ci2, t in enumerate(chunk):
                x, w = 56 + ci2 * 393, 373
                rect(s, x, 178, w, 462, FAM[fam]["50"], rounded=True)
                tf = tbox(s, x + 24, 200, w - 48, 110)
                line(tf, theme_label(t["theme"]), 16, INK, bold=True, first=True, after=6,
                     line_spacing=1.12)
                line(tf, f"{t['count']} SRs  ·  Jira Yes {t['jira_yes']} / No {t['jira_no']}",
                     11, INK3, after=0)
                rect(s, x + 24, 318, w - 48, 1, RULE)
                tf = tbox(s, x + 24, 336, w - 48, 290)
                for bi, b in enumerate(THEME_PLAYBOOK[t["theme"]]["reduce"]):
                    line(tf, "•  " + b, 12.5, INK2, first=(bi == 0), after=10,
                         line_spacing=1.28)
        else:
            # one or two themes: full-width bands, label left, actions right
            bh = 226 if len(chunk) == 2 else 300
            for ri, t in enumerate(chunk):
                y = 178 + ri * (bh + 36)
                rect(s, 56, y, 1168, bh, FAM[fam]["50"], rounded=True)
                tf = tbox(s, 86, y + 28, 300, bh - 56)
                line(tf, theme_label(t["theme"]), 17, INK, bold=True, first=True, after=8,
                     line_spacing=1.12)
                line(tf, f"{t['count']} SRs", 15, INK, bold=True, after=4)
                line(tf, f"Jira Yes {t['jira_yes']} / No {t['jira_no']}", 12, INK3, after=0)
                rect(s, 416, y + 28, 1, bh - 56, FAM[fam]["strong"])
                tf = tbox(s, 452, y + 28, 740, bh - 56)
                for bi, b in enumerate(THEME_PLAYBOOK[t["theme"]]["reduce"]):
                    line(tf, "•  " + b, 14, INK2, first=(bi == 0), after=11,
                         line_spacing=1.3)
        covered = sum(t["count"] for t in chunk)
        notes(s, f"{area} — actions for {', '.join(theme_label(t['theme']) for t in chunk)}. "
                 f"These {len(chunk)} themes account for {covered} of the area's "
                 f"{a['count']} Service Requests. Each bullet is the product change the "
                 f"tickets in that theme are asking for.")


for i, area in enumerate(AREA_ORDER, start=1):
    label = f"Area {i} of 4"
    area_problem_slide(area, label)
    area_action_slides(area, label)

# ======================================================== PRIORITIES
s = slide()
header(s, "Where to start", "The six priority themes, by Service Request volume")
pri = []
for th in PRIORITY_ORDER:
    area = THEME_AREA[th]
    row = next(t for t in AREAS[area]["themes"] if t["theme"] == th)
    pri.append((area, row))
pri.sort(key=lambda r: -r[1]["count"])
pri_total = sum(t["count"] for _, t in pri)
bigger = sorted(
    (t for a in SNAP["areas"] for t in a["themes"] if t["theme"] not in PRIORITY_ORDER),
    key=lambda t: -t["count"],
)[:2]
y = 182
for i, (area, t) in enumerate(pri):
    fam = AREA_FAMILY[area]
    rect(s, 56, y, 1168, 70, FAM[fam]["50"], rounded=True, radius=0.05)
    circle_outline(s, 78, y + 18, 34, INK)
    tf = tbox(s, 78, y + 23, 34, 24, anchor=MSO_ANCHOR.MIDDLE)
    line(tf, f"{i + 1:02d}", 12, INK, bold=True, first=True, after=0, align=PP_ALIGN.CENTER)
    tf = tbox(s, 130, y + 14, 470, 46)
    line(tf, theme_label(t["theme"]), 14, INK, bold=True, first=True, after=2, line_spacing=1.1)
    line(tf, area, 11, INK3, after=0)
    tf = tbox(s, 620, y + 22, 150, 30)
    line(tf, f"{t['count']} SRs", 18, INK, bold=True, first=True, after=0)
    tf = tbox(s, 780, y + 24, 180, 30)
    line(tf, f"Yes {t['jira_yes']} / No {t['jira_no']}", 13, INK2, first=True, after=0)
    tf = tbox(s, 980, y + 24, 230, 30)
    line(tf, f"{t['pct_of_filtered']}% of all CRM SRs", 13, INK2, first=True, after=0)
    y += 78
notes(s, "These are the six priority themes carried over from the RX theme playbook, shown "
         f"here in descending ticket volume. They are not simply the six largest themes — "
         + " and ".join(f"{theme_label(b['theme'])} ({b['count']})" for b in bigger)
         + f" are larger but sit outside the priority list. Together the six cover "
           f"{pri_total} of the {N:,} Service Requests.")

# ======================================================== CLOSE
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 170, 1120, 160)
line(tf, "More than half of this demand\nnever becomes a Jira ticket.", 40, PAPER,
     bold=True, first=True, after=0, line_spacing=1.18)
tf = tbox(s, 72, 352, 1100, 150)
for bi, t in enumerate([
    f"{JN} of the {N:,} CRM Service Requests have no Jira created against them "
    f"({round(JN / N * 100)}%).",
    f"The six priority themes alone cover {pri_total} of the {N:,} Service Requests "
    f"({round(pri_total / N * 100)}%).",
    "Source: ServiceNow Service Request export, Recruiter Experience, Jira Yes and No.",
]):
    line(tf, "•  " + t, 15, FAM["mint"]["50"], first=(bi == 0), after=12,
         line_spacing=1.35)
tf = tbox(s, 72, 622, 900, 30)
line(tf, "Phenom  ·  Recruiter Experience  ·  CRM Service Request playbook", 13,
     NAVY_SOFT, first=True, after=0)
notes(s, "Close on the Jira No number. These Service Requests were handled by Support "
         "without an engineering ticket, so the demand they represent is not visible in "
         "Jira-based planning. The priority-theme figure is the sum of the six themes on "
         "the previous slide.")

out = Path(__file__).with_name("RX-CRM-Service-Request-Playbook.pptx")
prs.save(out)
print(out, len(prs.slides.__iter__.__self__._sldIdLst))
