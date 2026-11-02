#!/usr/bin/env python3
"""Phenom PPTX — Current Problems Recruiters Face (importable to Google Slides)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

INK = "1a1c2e"
INK2 = "434343"
INK3 = "6b6b73"
PAPER = "ffffff"
TILE = "f2f2f3"
RULE = "e4e4e8"
NAVY = "131a4a"
FAM = {
    "mint": {"50": "daf3f2", "strong": "64a39c", "ink": "203634"},
    "peach": {"50": "f6e2d5", "strong": "d36238", "ink": "46210c"},
    "honey": {"50": "faedd7", "strong": "dda04a", "ink": "493614"},
    "lilac": {"50": "e9e6f9", "strong": "7172da", "ink": "0a0d37"},
}
FONT = "Poppins"
K = 0.0104166


def E(px):
    return Inches(px * K)


def PT(px):
    return Pt(px * 0.75)


def C(hexs):
    return RGBColor.from_string(hexs)


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def rect(s, x, y, w, h, fill, rounded=False, radius=0.08):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        E(x),
        E(y),
        E(w),
        E(h),
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
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tf


def line(
    tf,
    text,
    px,
    color,
    bold=False,
    first=False,
    after=6,
    before=0,
    align=PP_ALIGN.LEFT,
    line_spacing=1.15,
):
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


def header(s, kicker, title, title_px=36):
    tf = tbox(s, 56, 40, 1180, 24)
    line(tf, kicker, 15, INK, bold=True, first=True, after=0)
    tf = tbox(s, 56, 66, 1190, 100)
    line(tf, title, title_px, INK, bold=True, first=True, after=0, line_spacing=1.05)
    rect(s, 56, 172, 1168, 2, RULE)


def card(s, x, y, w, h, fam, num, title, body):
    rect(s, x, y, w, h, FAM[fam]["50"], rounded=True, radius=0.06)
    circle_outline(s, x + w - 56, y + 20, 36, INK)
    tf = tbox(s, x + w - 56, y + 24, 36, 28, anchor=MSO_ANCHOR.MIDDLE)
    line(tf, num, 14, INK, bold=True, first=True, after=0, align=PP_ALIGN.CENTER)
    tf = tbox(s, x + 22, y + 22, w - 90, 200)
    line(tf, title, 18, INK, bold=True, first=True, after=10, line_spacing=1.05)
    line(tf, body, 13, INK2, after=0, line_spacing=1.25)


# ============================ 1 COVER =======================================
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 180, 1100, 40)
line(tf, "RECRUITER EXPERIENCE", 14, FAM["mint"]["50"], bold=True, first=True, after=0)
tf = tbox(s, 72, 230, 1100, 160)
line(
    tf,
    "Current problems\nrecruiters face today",
    52,
    PAPER,
    bold=True,
    first=True,
    after=0,
    line_spacing=1.05,
)
tf = tbox(s, 72, 460, 900, 80)
line(
    tf,
    "Nine pressure points from approved job → hire — grouped for product & strategy conversations.",
    18,
    FAM["mint"]["50"],
    first=True,
    after=0,
    line_spacing=1.35,
)
tf = tbox(s, 72, 620, 600, 30)
line(tf, "Phenom  ·  Internal  ·  2026", 14, "8a90b8", first=True, after=0)

# ============================ 2 BOTTOM LINE =================================
s = slide()
header(s, "The core problem", "Process owners — stuck in noise")
rect(s, 56, 210, 1168, 200, FAM["mint"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 88, 250, 1100, 130)
line(
    tf,
    "Recruiters own approved job → hire, but spend most of their day on notifications, sync gaps, chase, and duplicates — not on screening quality and closing offers.",
    24,
    INK,
    bold=True,
    first=True,
    after=0,
    line_spacing=1.35,
)
cols = [
    ("peach", "Noise", "Alerts, cluttered My Jobs, unclear ownership"),
    ("honey", "Friction", "Slow setup, HM chase, stuck stages"),
    ("lilac", "Mismatch", "One playbook for every role cell & geo"),
]
cw, gap = 370, 28
for i, (fam, ttl, desc) in enumerate(cols):
    x = 56 + i * (cw + gap)
    rect(s, x, 450, cw, 180, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 28, 480, cw - 56, 130)
    line(tf, ttl, 22, INK, bold=True, first=True, after=12, line_spacing=1.0)
    line(tf, desc, 15, INK2, after=0, line_spacing=1.3)

# ============================ 3 MAP 1–5 =====================================
s = slide()
header(s, "Problem map  ·  1 of 2", "Where recruiters feel the pressure")
items = [
    ("mint", "01", "Workload & portfolio", "Unclear ownership; My Jobs noise; no clear “act today” queue"),
    ("peach", "02", "Job setup & publish", "Slow create; sync gaps; geo/compliance rules easy to miss"),
    ("honey", "03", "Sourcing & discovery", "Weak CRM search; thin handoffs; channel mismatch"),
    ("lilac", "04", "Screening velocity", "Manual piles; incomplete apps; ATS↔CRM status fights"),
    ("mint", "05", "HM & interview chase", "Slow feedback; fragile scheduling; recruiter as reminder bot"),
]
cw, gap = 220, 18
for i, (fam, num, ttl, body) in enumerate(items):
    x = 56 + i * (cw + gap)
    card(s, x, 220, cw, 420, fam, num, ttl, body)

# ============================ 4 MAP 6–9 =====================================
s = slide()
header(s, "Problem map  ·  2 of 2", "Close, data & context gaps")
items = [
    ("peach", "06", "Offer & fill risk", "Slow approvals; acceptance drop; unpost vs close confusion"),
    ("honey", "07", "Data & identity", "Duplicates, bad merges, stale profiles break Fit trust"),
    ("lilac", "08", "Measurement blind spots", "Aging causes hidden; weak source→hire attribution"),
    ("mint", "09", "Hypercell mismatch", "Volume ≠ professional; geo changes rules; agents ignore cells"),
]
cw, gap = 280, 22
for i, (fam, num, ttl, body) in enumerate(items):
    x = 56 + i * (cw + gap)
    card(s, x, 220, cw, 420, fam, num, ttl, body)

# ============================ 5 OPS DETAIL ==================================
s = slide()
header(s, "Operations", "Workload, setup & publishing")
left = [
    "Too many open reqs; Primary / Secondary / Sourcer / Coordinator blurred",
    "Everyone treated as full Recruiter → notification fatigue",
    "Hard to separate “act now” vs quietly aging jobs",
    "Admin time crowds out hiring decisions",
]
right = [
    "Job/req create is slow and incomplete",
    "One global playbook fails across industry, role, geo, volume",
    "Publish / compliance rules differ by market",
    "Jobs missing or duplicated across ATS ↔ CRM",
]
rect(s, 56, 210, 569, 420, FAM["peach"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 84, 240, 510, 360)
line(tf, "01  Workload & portfolio chaos", 20, INK, bold=True, first=True, after=18)
for it in left:
    line(tf, "•  " + it, 15, INK2, after=12, line_spacing=1.25)
rect(s, 655, 210, 569, 420, FAM["honey"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 683, 240, 510, 360)
line(tf, "02  Job setup & publishing", 20, INK, bold=True, first=True, after=18)
for it in right:
    line(tf, "•  " + it, 15, INK2, after=12, line_spacing=1.25)

# ============================ 6 PIPELINE ====================================
s = slide()
header(s, "Pipeline", "Source → screen → chase")
panels = [
    (
        "mint",
        "03  Sourcing gaps",
        [
            "Hard filters (certs, radius, schedule) hard to apply",
            "Sourcer ↔ recruiter handoffs weak or empty",
            "Outreach channel doesn’t match labor market",
            "Volume roles drown; scarce roles stall",
        ],
    ),
    (
        "peach",
        "04  Screening velocity",
        [
            "Manual screen of large piles",
            "Incomplete apps stall without “what’s missing”",
            "Status maps confuse allowed moves",
            "Silent automations move candidates unexplained",
        ],
    ),
    (
        "lilac",
        "05  HM & interviews",
        [
            "Slow HM / interviewer feedback kills velocity",
            "Stacked scheduling is fragile",
            "Recruiters become human reminders",
            "Hard to know stuck vs waiting",
        ],
    ),
]
cw, gap = 373, 24
for i, (fam, ttl, items) in enumerate(panels):
    x = 56 + i * (cw + gap)
    rect(s, x, 210, cw, 420, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 26, 240, cw - 52, 360)
    line(tf, ttl, 18, INK, bold=True, first=True, after=16)
    for it in items:
        line(tf, "•  " + it, 14, INK2, after=12, line_spacing=1.25)

# ============================ 7 CLOSE + DATA ================================
s = slide()
header(s, "Close & trust", "Offers, identity & visibility")
panels = [
    (
        "honey",
        "06  Offer & fill risk",
        [
            "Draft / approval / follow-up drag cycle time",
            "Acceptance drops without tight chase",
            "Unpost vs close vs reopen leaves wrong state",
            "Fill credit unclear with multi-recruiter touch",
        ],
    ),
    (
        "lilac",
        "07  Data & identity",
        [
            "Duplicates and bad merges break CRM trust",
            "Stale profiles waste screen time",
            "Import sync creates cleanup work",
            "“Disappeared” candidates = support fire drills",
        ],
    ),
    (
        "mint",
        "08  Measurement gaps",
        [
            "Aging cause not visible at stage level",
            "Leads lack clean workload / ownership views",
            "Uneven load and late escalations",
            "Source → hire attribution stays anecdotal",
        ],
    ),
]
cw, gap = 373, 24
for i, (fam, ttl, items) in enumerate(panels):
    x = 56 + i * (cw + gap)
    rect(s, x, 210, cw, 420, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 26, 240, cw - 52, 360)
    line(tf, ttl, 18, INK, bold=True, first=True, after=16)
    for it in items:
        line(tf, "•  " + it, 14, INK2, after=12, line_spacing=1.25)

# ============================ 8 HYPERCELL ===================================
s = slide()
header(s, "Context", "09  Why one playbook fails")
tf = tbox(s, 56, 200, 1160, 50)
line(
    tf,
    "Hiring automation must differ by Industry × Function × Role × Workflow × Geography.",
    18,
    INK2,
    first=True,
    after=0,
    line_spacing=1.3,
)
dims = [
    ("mint", "Industry", "Regulated vs retail vs logistics"),
    ("peach", "Function", "QA, ops, R&D, campus…"),
    ("honey", "Role", "Job family cluster being hired"),
    ("lilac", "Workflow", "Volume/speed vs precision"),
    ("mint", "Geography", "Compliance, language, channels"),
]
cw, gap = 220, 18
for i, (fam, ttl, desc) in enumerate(dims):
    x = 56 + i * (cw + gap)
    rect(s, x, 280, cw, 200, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 20, 310, cw - 40, 150)
    line(tf, ttl, 18, INK, bold=True, first=True, after=12)
    line(tf, desc, 14, INK2, after=0, line_spacing=1.3)
rect(s, 56, 520, 1168, 120, TILE, rounded=True, radius=0.06)
tf = tbox(s, 88, 548, 1100, 70)
line(
    tf,
    "Agents and automations that ignore the cell create more cleanup than lift — frontline high-volume ≠ professional precision hiring.",
    16,
    INK,
    bold=True,
    first=True,
    after=0,
    line_spacing=1.35,
)

# ============================ 9 TAKEAWAYS ===================================
s = slide()
header(s, "Summary", "What this means for product")
takes = [
    ("01", "mint", "Cut noise first", "Role-aware ownership, My Jobs, and one notification per event"),
    ("02", "peach", "Make context explicit", "Hypercell-aware setup, knockouts, publish, and chase SLAs"),
    ("03", "honey", "Unstick the funnel", "Surface incomplete apps, status truth, and HM feedback aging"),
    ("04", "lilac", "Protect trust", "Sync health, identity/merge clarity, source→hire attribution"),
]
cw, gap = 280, 22
for i, (num, fam, ttl, desc) in enumerate(takes):
    x = 56 + i * (cw + gap)
    rect(s, x, 220, cw, 380, FAM[fam]["50"], rounded=True, radius=0.06)
    circle_outline(s, x + 24, 248, 44, INK)
    tf = tbox(s, x + 24, 256, 44, 28, anchor=MSO_ANCHOR.MIDDLE)
    line(tf, num, 14, INK, bold=True, first=True, after=0, align=PP_ALIGN.CENTER)
    tf = tbox(s, x + 24, 320, cw - 48, 240)
    line(tf, ttl, 22, INK, bold=True, first=True, after=14, line_spacing=1.05)
    line(tf, desc, 15, INK2, after=0, line_spacing=1.35)

# ============================ 10 CLOSE ======================================
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 240, 1100, 120)
line(
    tf,
    "Recruiters don’t need more work.\nThey need less noise and the right playbook.",
    36,
    PAPER,
    bold=True,
    first=True,
    after=0,
    line_spacing=1.2,
)
tf = tbox(s, 72, 420, 900, 60)
line(
    tf,
    "Nine problems. One through-line: ownership clarity × cell context × funnel truth.",
    18,
    FAM["mint"]["50"],
    first=True,
    after=0,
    line_spacing=1.35,
)
tf = tbox(s, 72, 620, 600, 30)
line(tf, "Phenom  ·  Recruiter Experience", 14, "8a90b8", first=True, after=0)

out = "/Users/venkata.gonella/phenom-master-copilot/.cursor/skills/phenom-slide-creator/output-decks/recruiter-problems-today/Current-Problems-Recruiters-Face.pptx"
prs.save(out)
print(out)
