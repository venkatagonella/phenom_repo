#!/usr/bin/env python3
"""Build a rich, editable Phenom PPTX for PHEM-2109151 MVP deck.
Reconstructs the HTML template layouts natively using Phenom design tokens
(phenom-tokens.css) so the deck is editable in Google Slides and on-brand.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---- Phenom tokens ---------------------------------------------------------
INK="1a1c2e"; INK2="434343"; INK3="6b6b73"; PAPER="ffffff"; TILE="f2f2f3"; RULE="e4e4e8"
NAVY="131a4a"
FAM={
 "mint":  {"50":"daf3f2","strong":"64a39c","ink":"203634"},
 "peach": {"50":"f6e2d5","strong":"d36238","ink":"46210c"},
 "honey": {"50":"faedd7","strong":"dda04a","ink":"493614"},
 "lilac": {"50":"e9e6f9","strong":"7172da","ink":"0a0d37"},
}
FONT="Poppins"
K=0.0104166  # px -> inch on a 13.333in (1280px) stage

def E(px):            # geometry px -> Inches
    return Inches(px*K)
def PT(px):           # css px font -> pt (0.75)
    return Pt(px*0.75)
def C(hexs):
    return RGBColor.from_string(hexs)

prs=Presentation()
prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]

def slide():
    return prs.slides.add_slide(BLANK)

def rect(s,x,y,w,h,fill,rounded=False,radius=0.08):
    shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                           E(x),E(y),E(w),E(h))
    shp.fill.solid(); shp.fill.fore_color.rgb=C(fill); shp.line.fill.background()
    shp.shadow.inherit=False
    if rounded:
        try:
            shp.adjustments[0]=radius
        except Exception:
            pass
    return shp

def circle_outline(s,x,y,d,color):
    shp=s.shapes.add_shape(MSO_SHAPE.OVAL,E(x),E(y),E(d),E(d))
    shp.fill.background(); shp.line.color.rgb=C(color); shp.line.width=Pt(1.5)
    shp.shadow.inherit=False
    return shp

def tbox(s,x,y,w,h,anchor=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(E(x),E(y),E(w),E(h)); tf=tb.text_frame
    tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    return tf

def line(tf,text,px,color,bold=False,first=False,after=6,before=0,align=PP_ALIGN.LEFT,line_spacing=1.15):
    p=tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment=align; p.space_after=Pt(after); p.space_before=Pt(before)
    p.line_spacing=line_spacing
    r=p.add_run(); r.text=text
    f=r.font; f.name=FONT; f.size=PT(px); f.bold=bold; f.color.rgb=C(color)
    return p

def header(s,kicker,title):
    tf=tbox(s,56,40,1180,24); line(tf,kicker,15,INK,bold=True,first=True,after=0)
    tf=tbox(s,56,66,1190,116); line(tf,title,40,INK,bold=True,first=True,after=0,line_spacing=1.05)
    rect(s,56,184,1168,2,RULE)

def panel(s,x,y,w,h,bg,title,items,strong):
    rect(s,x,y,w,h,bg,rounded=True,radius=0.06)
    tf=tbox(s,x+26,y+24,w-52,h-40)
    line(tf,title,18,INK,bold=True,first=True,after=12)
    for it in items:
        p=line(tf,it,15,INK2,after=9,line_spacing=1.2)

def bullet_items(items):
    return ["•  "+t for t in items]

# ============================ SLIDE 1 =======================================
s=slide()
header(s,"The Business Challenge","Every recruiter on a job looks the same — and it's costing teams time")
tf=tbox(s,56,196,1160,92)
line(tf,("Enterprise talent teams staff a job with several kinds of recruiters — a lead recruiter, "
         "supporting recruiters, sourcers, and coordinators. Today the platform collapses them all into "
         "one \u201cRecruiter\u201d role, so notifications, workspace views, and ATS sync can't tell them apart."),
     15,INK2,first=True,after=0,line_spacing=1.3)
panel(s,56,300,569,300,TILE,"The problem today",bullet_items([
    "Notification fatigue & duplicates — a person with two roles on a job is notified twice.",
    "Undifferentiated \u201cMy Jobs\u201d — supporting-role jobs clutter the jobs a user actually leads.",
    "Lost ATS fidelity — sourcers & secondary recruiters get flattened into \u201cRecruiter\u201d.",
]),FAM["mint"]["strong"])
panel(s,655,300,569,300,FAM["mint"]["50"],"What the business is asking for",bullet_items([
    "Recognise distinct recruiter-family roles on the hiring team.",
    "Route notifications by role and send exactly one alert per event.",
    "Focus \u201cMy Jobs\u201d and filters on the role that matters to each user.",
    "Preserve the ATS's granular roles when a job is pulled in.",
]),FAM["mint"]["strong"])

# ============================ SLIDE 2 =======================================
s=slide()
header(s,"MVP \u00b7 Roles","New recruiter-family roles")
tf=tbox(s,56,196,1160,74)
line(tf,("Phase 1 adds recruiter-family roles, each switched on per tenant by admin configuration. "
         "Sourcer and Recruiting Coordinator become new top-level roles; Secondary Recruiter sits under Recruiter."),
     15,INK2,first=True,after=0,line_spacing=1.3)
cards=[
 ("peach","Leading","Primary Recruiter","Today's Recruiter. Owns the job; \u201cMy Jobs\u201d keeps showing only where the user is Primary Recruiter."),
 ("honey","Supporting","Secondary Recruiter","A child role under Recruiter for additional recruiters on the same requisition."),
 ("lilac","Supporting","Sourcer","New top-level role for sourcing specialists, with its own job spotlight."),
 ("mint","Supporting","Recruiting Coordinator","New top-level role for scheduling and coordination on the job."),
]
cw=274; gap=24
for i,(fam,tag,ttl,desc) in enumerate(cards):
    x=56+i*(cw+gap)
    rect(s,x,300,cw,300,FAM[fam]["50"],rounded=True,radius=0.06)
    circle_outline(s,x+cw-64,324,40,INK)
    tf=tbox(s,x+24,352,cw-48,230)
    line(tf,tag.upper(),11,FAM[fam]["strong"],bold=True,first=True,after=6)
    line(tf,ttl,22,INK,bold=True,after=10,line_spacing=1.0)
    line(tf,desc,15,INK2,after=0,line_spacing=1.25)

# ============================ SLIDE 3 =======================================
s=slide()
header(s,"MVP \u00b7 Configuration & CRM","Admin-controlled, role-aware CRM")
panel(s,56,216,569,336,FAM["honey"]["50"],"Configuration & assignment",bullet_items([
    "Each role is enabled or disabled per tenant by an admin — separately for Secondary Recruiter, Sourcer & Coordinator.",
    "Roles can be associated to a job before it is published.",
    "Only the Primary Recruiter adds users to these roles; assignments stay editable after publish.",
]),FAM["honey"]["strong"])
panel(s,655,216,569,336,TILE,"Views, spotlights & ATS",bullet_items([
    "Each enabled role gets its own spotlight (\u201cSourcer Jobs\u201d, etc.); \u201cMy Jobs\u201d still lists Recruiter jobs.",
    "Existing filters and advanced filters work as-is for the new roles.",
    "Roles configured in the ATS create placeholders in CRM, filled manually in MVP.",
]),FAM["honey"]["strong"])
tf=tbox(s,56,576,1160,40)
p=tf.paragraphs[0]; p.line_spacing=1.2
r=p.add_run(); r.text="Guardrail: "; r.font.name=FONT; r.font.size=PT(13); r.font.bold=True; r.font.color.rgb=C(INK2)
r=p.add_run(); r.text="once a job has a user assigned to one of these roles, that role's setting can no longer be turned off."
r.font.name=FONT; r.font.size=PT(13); r.font.color.rgb=C(INK3)

# ============================ SLIDE 4 =======================================
s=slide()
header(s,"MVP \u00b7 Notifications","One person, one notification")
ncards=[
 ("lilac","Exactly one email","Even when a user holds multiple roles on the same job, only one email notification is sent per event."),
 ("peach","Last-held-role context","Notifications reflect the most recent role — a Recruiter later made Sourcer receives Sourcer notifications, not Recruiter."),
 ("honey","Inherited settings","Notification preferences are inherited directly from recruiter-level settings."),
]
cw=373; gap=24
for i,(fam,ttl,desc) in enumerate(ncards):
    x=56+i*(cw+gap)
    rect(s,x,232,cw,318,FAM[fam]["50"],rounded=True,radius=0.06)
    circle_outline(s,x+cw-64,256,40,INK)
    tf=tbox(s,x+26,320,cw-52,210)
    line(tf,ttl,22,INK,bold=True,first=True,after=12,line_spacing=1.0)
    line(tf,desc,15,INK2,after=0,line_spacing=1.3)
tf=tbox(s,56,576,1160,40)
p=tf.paragraphs[0]; p.line_spacing=1.2
r=p.add_run(); r.text="Not in MVP: "; r.font.name=FONT; r.font.size=PT(13); r.font.bold=True; r.font.color.rgb=C(INK2)
r=p.add_run(); r.text="SMS / WhatsApp delivery and per-role personalization."
r.font.name=FONT; r.font.size=PT(13); r.font.color.rgb=C(INK3)

# ============================ SLIDE 5 =======================================
s=slide()
header(s,"MVP \u00b7 Reports & Analytics","Visibility into every role's contribution")
panel(s,56,236,569,300,FAM["mint"]["50"],"What's planned",bullet_items([
    "Reporting is enabled per the roles a user holds on jobs, so their activity can be analysed by role.",
    "Primary Recruiter reporting capabilities are cloned for Secondary Recruiter, Sourcer & Coordinator.",
]),FAM["mint"]["strong"])
panel(s,655,236,569,300,TILE,"In practice",bullet_items([
    "A user who is both Secondary Recruiter and Sourcer can be reported on separately for each role.",
    "Leaders gain a clear view of each role's contribution to a requisition.",
]),FAM["mint"]["strong"])

# ============================ SLIDE 6 =======================================
s=slide()
header(s,"MVP \u00b7 Delivery","When Phenom can deliver the MVP")
rect(s,56,360,1168,3,RULE)
stops=[
 ("Now","Grooming & Design","Scope, UX and cross-team effort being finalised.","honey",False,"down"),
 ("TBD","Build","Engineering across CRM, Integration & Messaging.","peach",True,"up"),
 ("TBD","UAT — Staging","Customer validation on the agreed rollout tenants.","lilac",True,"down"),
 ("TBD","Go-Live — Production","Enabled per tenant after ATS role mapping is validated.","mint",True,"up"),
]
centers=[202,494,786,1078]
for cx,(yr,et,desc,fam,tbd,pos) in zip(centers,stops):
    pill=rect(s,cx-70,343,140,38,(TILE if tbd else FAM[fam]["50"]),rounded=True,radius=0.5)
    tf=pill.text_frame; tf.word_wrap=True
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    line(tf,yr,15,(INK3 if tbd else INK),bold=True,first=True,after=0,align=PP_ALIGN.CENTER)
    if pos=="up":
        tf=tbox(s,cx-140,250,280,86,anchor=MSO_ANCHOR.BOTTOM)
    else:
        tf=tbox(s,cx-140,392,280,90)
    line(tf,et,13,INK,bold=True,first=True,after=4,align=PP_ALIGN.CENTER,line_spacing=1.05)
    line(tf,desc,13,INK2,after=0,align=PP_ALIGN.CENTER,line_spacing=1.2)
tf=tbox(s,56,636,900,30)
line(tf,"Dates to be confirmed — the epic is currently in grooming.",13,INK3,first=True,after=0)

out="PHEM-2109151-MVP-Executive-Deck/PHEM-2109151-MVP-Executive-Deck.pptx"
prs.save(out)
print("Saved",out,"slides:",len(prs.slides._sldIdLst))
