#!/usr/bin/env python3
"""Phenom PPTX — How ATS vendors address recruiter problems (sourced)."""
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
VENDORS = ["Workday", "SuccessFactors", "Greenhouse", "Ashby", "Workable", "Personio"]


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
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tf


def line(tf, text, px, color, bold=False, first=False, after=4, before=0,
         align=PP_ALIGN.LEFT, line_spacing=1.12):
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


def vendor_grid(s, y, rows, card_h=210):
    """rows: list of (fam, vendor, body) length 6 → 3x2."""
    cw, gap, rw = 373, 20, card_h
    for i, (fam, vendor, body) in enumerate(rows):
        col, row = i % 3, i // 3
        x = 56 + col * (cw + gap)
        yy = y + row * (rw + 16)
        rect(s, x, yy, cw, rw, FAM[fam]["50"], rounded=True, radius=0.06)
        tf = tbox(s, x + 20, yy + 16, cw - 40, rw - 32)
        line(tf, vendor, 16, INK, bold=True, first=True, after=8, line_spacing=1.0)
        line(tf, body, 12, INK2, after=0, line_spacing=1.2)


# ============================ 1 COVER =======================================
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 160, 1100, 36)
line(tf, "COMPETITIVE INTELLIGENCE  ·  RECRUITER EXPERIENCE", 13, FAM["mint"]["50"], bold=True, first=True, after=0)
tf = tbox(s, 72, 210, 1100, 180)
line(tf, "How ATS vendors address\nrecruiter problems today", 46, PAPER, bold=True, first=True, after=0, line_spacing=1.08)
tf = tbox(s, 72, 430, 1000, 80)
line(tf, "Workday  ·  SAP SuccessFactors  ·  Greenhouse  ·  Ashby  ·  Workable  ·  Personio", 16, FAM["mint"]["50"], first=True, after=8, line_spacing=1.3)
line(tf, "Mapped to the nine recruiter pressure points — sourced from vendor docs & Phenom Compete packs.", 15, "8a90b8", after=0, line_spacing=1.3)
tf = tbox(s, 72, 620, 700, 30)
line(tf, "Phenom  ·  Internal  ·  Sourced evidence only  ·  2026", 13, "8a90b8", first=True, after=0)

# ============================ 2 HOW TO READ =================================
s = slide()
header(s, "How to read this deck", "Documented mechanisms — not claims of solved")
cols = [
    ("mint", "What “addresses” means", "A product mechanism described in vendor help, admin guides, or Phenom Compete packs. Not a guarantee every tenant uses it."),
    ("peach", "Config warning", "Workday / SuccessFactors especially: security groups, operators, route maps, and templates vary by customer."),
    ("honey", "Evidence bar", "Only primary sources. Gaps marked honestly. Hypercell (Industry×Function×Role×Workflow×Geo) is Phenom framing — vendors don’t name it."),
]
cw, gap = 373, 24
for i, (fam, ttl, body) in enumerate(cols):
    x = 56 + i * (cw + gap)
    rect(s, x, 200, cw, 380, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 26, 240, cw - 52, 320)
    line(tf, ttl, 20, INK, bold=True, first=True, after=16, line_spacing=1.05)
    line(tf, body, 15, INK2, after=0, line_spacing=1.35)

# ============================ 3 NINE PROBLEMS ===============================
s = slide()
header(s, "Context", "Nine recruiter problems (from prior deck)")
items = [
    ("mint", "01", "Workload & ownership"),
    ("peach", "02", "Job setup & publish"),
    ("honey", "03", "Sourcing & discovery"),
    ("lilac", "04", "Screening velocity"),
    ("mint", "05", "HM & interview chase"),
    ("peach", "06", "Offer & fill risk"),
    ("honey", "07", "Data & identity"),
    ("lilac", "08", "Measurement gaps"),
    ("mint", "09", "Context / hypercell"),
]
cw, gap = 373, 20
for i, (fam, num, ttl) in enumerate(items):
    col, row = i % 3, i // 3
    x = 56 + col * (cw + gap)
    y = 190 + row * 150
    rect(s, x, y, cw, 130, FAM[fam]["50"], rounded=True, radius=0.06)
    circle_outline(s, x + cw - 52, y + 22, 34, INK)
    tf = tbox(s, x + cw - 52, y + 26, 34, 26, anchor=MSO_ANCHOR.MIDDLE)
    line(tf, num, 12, INK, bold=True, first=True, after=0, align=PP_ALIGN.CENTER)
    tf = tbox(s, x + 24, y + 48, cw - 90, 60)
    line(tf, ttl, 18, INK, bold=True, first=True, after=0, line_spacing=1.1)

# ============================ 4 SNAPSHOT ====================================
s = slide()
header(s, "At a glance", "Where documentation is strongest")
rows = [
    ("Workload / noise", "Workday Primary Recruiter + Hub; Greenhouse role-tasks; Ashby permissions automation; SF operators"),
    ("Publish vs close", "All six separate posting/visibility from job close (Compete lifecycle pack)"),
    ("Sourcing", "Workable Agent/AI search; GH/Ashby/WD/SF first-class Sourcer; Personio channel/external"),
    ("Feedback chase", "Greenhouse scorecard reminders + HM/coordinator tasks; Personio evaluation tasks"),
    ("Duplicates", "Workday Match/Merge + DMF; SF merge; GH tag/auto-merge; Ashby merge; Workable/Personio detect, no merge"),
    ("Context / volume", "Workday evergreen + self-schedule; Ashby dept-scoped auto-reject; Workable Agent ICP per job"),
]
y = 178
for i, (ttl, body) in enumerate(rows):
    fam = ["mint", "peach", "honey", "lilac", "mint", "peach"][i]
    rect(s, 56, y, 1168, 72, FAM[fam]["50"] if i % 2 == 0 else TILE, rounded=True, radius=0.05)
    tf = tbox(s, 78, y + 12, 280, 50)
    line(tf, ttl, 15, INK, bold=True, first=True, after=0, line_spacing=1.15)
    tf = tbox(s, 370, y + 12, 820, 50)
    line(tf, body, 13, INK2, first=True, after=0, line_spacing=1.2)
    y += 80

# ============================ 5 OWNERSHIP ===================================
s = slide()
header(s, "Problem 01", "Workload, ownership & notification noise")
vendor_grid(s, 178, [
    ("mint", "Workday", "Primary Recruiter → app notifications to one person. Recruiting Hub + Owned By Me role filters. Recruiter Overload Count on Manage Recruiter Workload. Roles: Recruiter, Primary Recruiter, Coordinator, Sourcer."),
    ("peach", "SuccessFactors", "Operators on the req: R Recruiter, W Second Recruiter, S Sourcer, T Coordinator, G HM. Drive route maps, field permissions, pipeline visibility, and status emails."),
    ("honey", "Greenhouse", "Hiring Team roles auto-assign tasks (My Tasks). Job notifications for pipeline events. Default role tasks cannot be edited. Filter jobs/candidates/reports by role."),
    ("lilac", "Ashby", "Hiring-team roles separate from access. Permissions Automation maps role → Job Access Role; grants/revokes on add/remove from team."),
    ("mint", "Workable", "Access levels + collaboration roles (Admin, Recruiter, HM, Contributor, Reviewer, External). Recruiters scoped to assigned jobs / dept / location."),
    ("peach", "Personio", "Custom recruiting roles with per-role notification settings; assign on the job hiring team."),
], card_h=230)

# ============================ 6 SETUP PUBLISH ===============================
s = slide()
header(s, "Problem 02", "Job setup & publishing")
vendor_grid(s, 178, [
    ("mint", "Workday", "Requisition-first. Draft → Approval → Open → Post. Separate internal/external postings + start/end dates. Freeze without close. Close ≠ unpost."),
    ("peach", "SuccessFactors", "Route-map approval before posting. Post/unpost with posting dates. Closed req can reopen (config-dependent)."),
    ("honey", "Greenhouse", "Job vs opening vs job post. Draft → Open → Publish. Unpublish post without closing job; close job unpublishes posts."),
    ("lilac", "Ashby", "Job / opening / posting. Open required before publish. Listed / Unlisted / Unpublished. Deadline can auto-unpublish."),
    ("mint", "Workable", "Requisition statuses + job visibility (Draft/Published/Internal/Confidential/Archived). Channel distribution to careers/boards."),
    ("peach", "Personio", "Draft → Publish. External promotion Scheduled/Running/Canceled/Expired with start/end. Cancel ≠ natural expiry."),
], card_h=230)

# ============================ 7 SOURCING ====================================
s = slide()
header(s, "Problem 03", "Sourcing & discovery")
vendor_grid(s, 178, [
    ("mint", "Workday", "Candidate pools; LinkedIn RSC; agency submissions; referrals; engagement campaigns."),
    ("peach", "SuccessFactors", "Searchable Candidate Profile; talent community / CRM pools; Source Tracker for ROI."),
    ("honey", "Greenhouse", "CRM prospect pools/campaigns; Chrome extension; LinkedIn RSC; Talent Finder (tier)."),
    ("lilac", "Ashby", "Sequences (LI Chrome, open/click/reply); Sourcing Dashboard; Sourcer on hiring team."),
    ("mint", "Workable", "Chrome extension + Agent AI sourcing/outreach; External Recruiter for agencies."),
    ("peach", "Personio", "Board multipost; LinkedIn sourcing extension (product); channel tagging. Counts vary by marketing page."),
], card_h=230)

# ============================ 8 SCREEN + CHASE ==============================
s = slide()
header(s, "Problems 04–05", "Screening velocity + HM / interview chase")
# left screening, right chase as two panels with vendor bullets
rect(s, 56, 178, 569, 460, FAM["mint"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 80, 198, 520, 420)
line(tf, "04  Screening", 18, INK, bold=True, first=True, after=12)
for t in [
    "Workday: Screen BP; questionnaires; auto-advance on min criteria; Hub stage cards.",
    "SF: Status pipeline / workbench; resume parsing (Best Practices); candidate search.",
    "Greenhouse: Stage alerts; advance/reject when scorecards in; template questions.",
    "Ashby: Auto-Reject on apply (posting or global/dept rules).",
    "Workable: Agent scores /100; auto-advance/disqualify; knockout + Automated Actions.",
    "Personio: Automated screening (disqualify + tag); optional AI screening criteria.",
]:
    line(tf, "•  " + t, 12, INK2, after=8, line_spacing=1.2)

rect(s, 655, 178, 569, 460, FAM["peach"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 679, 198, 520, 420)
line(tf, "05  HM & interview chase", 18, INK, bold=True, first=True, after=12)
for t in [
    "Workday: Interview BP + competency feedback; calendar; high-volume self-schedule.",
    "SF: Interview Central assessments; schedule or candidate self-schedule.",
    "Greenhouse: Scorecard due reminders (~1h default); Slack; HM review tasks.",
    "Ashby: Required feedback → automatic email reminders to interviewers.",
    "Workable: Kits/scorecards; evaluate reminders when interviews scheduled in-app.",
    "Personio: Evaluation forms; request feedback → email + Inbox task.",
]:
    line(tf, "•  " + t, 12, INK2, after=8, line_spacing=1.2)

# ============================ 9 OFFER CLOSE =================================
s = slide()
header(s, "Problem 06", "Offer, close & fill risk")
vendor_grid(s, 178, [
    ("mint", "Workday", "Offer BP: comp, approvals, e-sign, renegotiate; bulk offers; Candidate Home negotiate. Freeze/fill/close vs posting."),
    ("peach", "SuccessFactors", "Offer approval route then letter from template; mass offer approvals; Enable Offer Approval setting."),
    ("honey", "Greenhouse", "Offer document templates + tokens; generate/send; bulk generate. Job close vs post unpublish."),
    ("lilac", "Ashby", "Offer activity on Offer stage; PDF letter; Dropbox Sign; Offers dashboard metrics."),
    ("mint", "Workable", "Offer-stage e-sign; approval workflows before send (Premier/Enterprise); Hiring Plan ownership."),
    ("peach", "Personio", "Offer letter email templates with placeholders. E-sign on marketing pages — not verified in support."),
], card_h=230)

# ============================ 10 DATA + ANALYTICS ===========================
s = slide()
header(s, "Problems 07–08", "Data quality + measurement")
rect(s, 56, 178, 569, 460, FAM["honey"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 80, 198, 520, 420)
line(tf, "07  Duplicates & identity", 18, INK, bold=True, first=True, after=12)
for t in [
    "Workday: Match and Merge or Duplicate Management Framework; My Tasks duplicates; auto-merge settings.",
    "SF: Manage Duplicate Candidates; manual merge (no mass/API merge per KBA).",
    "Greenhouse: Duplicate tag + Auto-merge + manual merge + Show Potential Duplicates.",
    "Ashby: Duplicate detection + merge profiles documented.",
    "Workable: Email match per job; cannot merge profiles.",
    "Personio: Same-email warning across jobs; no merge feature documented.",
]:
    line(tf, "•  " + t, 12, INK2, after=8, line_spacing=1.2)

rect(s, 655, 178, 569, 460, FAM["lilac"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 679, 198, 520, 420)
line(tf, "08  Measurement visibility", 18, INK, bold=True, first=True, after=12)
for t in [
    "Workday: Recruiting report category; Time to Fill; Manage Recruiter Workload.",
    "SF: Source Tracker; Advanced Analytics; Career Site Builder channel ROI.",
    "Greenhouse: Custom reporting dashboards/widgets; hiring-team filters.",
    "Ashby: Core dashboards (Exec/Jobs/Sourcing/Interviews/Offers); custom alerts.",
    "Workable: Report Center — pipeline, TTH, sources, team productivity.",
    "Personio: Job metrics in product; full report catalog mostly marketing-only this pass.",
]:
    line(tf, "•  " + t, 12, INK2, after=8, line_spacing=1.2)

# ============================ 11 CONTEXT ====================================
s = slide()
header(s, "Problem 09", "Context mismatch — none ship Phenom Hypercell")
tf = tbox(s, 56, 178, 1168, 50)
line(tf, "No vendor publishes Industry × Function × Role × Workflow × Geography as a named matrix. Closest documented patterns:", 15, INK2, first=True, after=0, line_spacing=1.3)
dims = [
    ("mint", "Ashby", "Team/location jobs; dept-scoped auto-reject; Multiple Brands; report by area & geo."),
    ("peach", "Workday", "Evergreen reqs + self-schedule for volume; career pages by segment; posting templates."),
    ("honey", "SuccessFactors", "Multi-language Recruiting Posting; Career Site Builder; Position/EC context."),
    ("lilac", "Greenhouse", "Offer templates by office/dept/type; role-based tasks per job."),
    ("mint", "Workable", "Publish by dept/location; Agent ICP per job; language kits in automations."),
    ("peach", "Phenom angle", "Hypercell (Industry×Function×Role×Workflow×Geo) is still Phenom’s named differentiator."),
]
cw, gap = 373, 20
for i, (fam, ttl, body) in enumerate(dims):
    col, row = i % 3, i // 3
    x = 56 + col * (cw + gap)
    y = 250 + row * 190
    rect(s, x, y, cw, 170, FAM[fam]["50"], rounded=True, radius=0.06)
    tf = tbox(s, x + 20, y + 20, cw - 40, 130)
    line(tf, ttl, 16, INK, bold=True, first=True, after=10)
    line(tf, body, 13, INK2, after=0, line_spacing=1.25)

# ============================ 12 SOURCES ====================================
s = slide()
header(s, "Evidence", "Primary sources used")
rect(s, 56, 178, 569, 460, TILE, rounded=True, radius=0.06)
tf = tbox(s, 80, 198, 520, 420)
line(tf, "Vendor docs", 18, INK, bold=True, first=True, after=12)
for t in [
    "Workday Admin / Education (Primary Recruiter, Hub, Security)",
    "SAP Learning + Support KBAs (operators, route maps)",
    "Greenhouse Support (hiring team, tasks, duplicates)",
    "Ashby docs (permissions automation, analytics, fields)",
    "Workable Help (access levels, Agent, reporting)",
    "Personio Support (roles, evaluations, scheduling, agencies)",
]:
    line(tf, "•  " + t, 13, INK2, after=10, line_spacing=1.25)

rect(s, 655, 178, 569, 460, FAM["mint"]["50"], rounded=True, radius=0.06)
tf = tbox(s, 679, 198, 520, 420)
line(tf, "Phenom knowledge", 18, INK, bold=True, first=True, after=12)
for t in [
    "Compete/knowledge/personas-jtbd.md + lifecycle-comparison.md",
    "RX Job Page Revamp (Confluence) — Workable, Personio, Ashby (2026-05)",
    "Deep pass 2026-09-28: vendor help/docs matrix (sequences, DMF, Interview Central, Agent)",
    "Remaining gaps: Personio report catalog & e-sign offers (marketing-only)",
]:
    line(tf, "•  " + t, 13, INK2, after=12, line_spacing=1.25)

# ============================ 13 TAKEAWAYS ==================================
s = slide()
header(s, "Implications for Phenom", "Where to compete vs where to match")
takes = [
    ("01", "mint", "Match ownership clarity", "Primary/Secondary/Sourcer/Coordinator + one notification path — table stakes vs WD/GH/Ashby."),
    ("02", "peach", "Match publish ≠ close", "Requisition vs posting lifecycle is industry standard — keep Phenom model crisp."),
    ("03", "honey", "Differentiate Hypercell", "Vendors configure; they don’t sell Industry×Function×Role×Workflow×Geo playbooks."),
    ("04", "lilac", "Win on chase + trust", "Scorecard aging, incomplete-app truth, sync health, merge clarity — recruiter day-to-day pain."),
]
cw, gap = 280, 22
for i, (num, fam, ttl, desc) in enumerate(takes):
    x = 56 + i * (cw + gap)
    rect(s, x, 200, cw, 400, FAM[fam]["50"], rounded=True, radius=0.06)
    circle_outline(s, x + 24, 228, 42, INK)
    tf = tbox(s, x + 24, 236, 42, 28, anchor=MSO_ANCHOR.MIDDLE)
    line(tf, num, 13, INK, bold=True, first=True, after=0, align=PP_ALIGN.CENTER)
    tf = tbox(s, x + 24, 300, cw - 48, 270)
    line(tf, ttl, 18, INK, bold=True, first=True, after=14, line_spacing=1.05)
    line(tf, desc, 14, INK2, after=0, line_spacing=1.35)

# ============================ 14 CLOSE ======================================
s = slide()
rect(s, 0, 0, 1280, 720, NAVY)
tf = tbox(s, 72, 220, 1100, 140)
line(tf, "Competitors solve ownership with roles.\nPhenom can solve playbooks with Hypercells.", 34, PAPER, bold=True, first=True, after=0, line_spacing=1.2)
tf = tbox(s, 72, 420, 1000, 70)
line(tf, "Companion to: Current Problems Recruiters Face Today — sourced competitive response.", 16, FAM["mint"]["50"], first=True, after=0, line_spacing=1.35)
tf = tbox(s, 72, 620, 700, 30)
line(tf, "Phenom  ·  Recruiter Experience  ·  Compete", 13, "8a90b8", first=True, after=0)

out = "/Users/venkata.gonella/phenom-master-copilot/.cursor/skills/phenom-slide-creator/output-decks/recruiter-problems-vendor-response/ATS-Vendors-Address-Recruiter-Problems.pptx"
prs.save(out)
print(out)
