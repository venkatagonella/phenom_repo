"""Classify CRM Core / Profile / Messaging / Automations service requests into
themes from SHORT_DESCRIPTION verbatims and render a tabular HTML report.

Source of truth: the "All Servicenow service requests from 2026-01-01" sheet
export only. Area comes from structured case fields; theme comes from
exclusive first-match phrase rules on SHORT_DESCRIPTION. No match stays
"Unclassified".
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme_jira_map import (  # noqa: E402
    JIRA_BROWSE, JIRA_RULES, build_tree, is_engineering, keys_created_before, load_items, map_items, split_done,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "sup-ticket-themes" / "scripts"))
from sup_theme_rules import PRODUCT2  # noqa: E402
from sup_themes import analyse as analyse_sup  # noqa: E402

csv.field_size_limit(sys.maxsize)

AREAS = ["CRM Core", "Profile", "Messaging", "Automations"]
AREA_TONE = {"CRM Core": "core", "Profile": "profile", "Messaging": "messaging", "Automations": "automations"}

SUB_PRODUCT_MAP = {
    "CRM - Core": "CRM Core",
    "CRM - Profile": "Profile",
    "CRM - Messaging and Campaigns": "Messaging",
    "CRM - Automation": "Automations",
}
COMPONENT_MAP = {
    "CRM - Core": "CRM Core",
    "CRM - Profile Service": "Profile",
    "CRM - Messaging": "Messaging",
    "CRM - Automation": "Automations",
}

EXCLUDED_SUB_STATUS = {"Spam", "Duplicate"}
UNCLASSIFIED = "Unclassified"

NON_ACTIONABLE = (
    "Non-actionable (auto-created / external / test / case reference only)",
    [
        r"^\[external\]\s*$",
        r"^\[external\]\s*(resume|hello|question:?)\s*$",
        r"inf ticket created",
        r"golden opportunity|domain for sale|ai quotient awards|target foodservice|intent signals"
        r"|the ai behind fifa|managing safety\. are you managing risk|pop ups on your website",
        r"\btest(ing)?[ _]case\b|test support case|do not action|please ignore|^test$",
        r"scheduled maintenance",
        r"^(re:|fw:|recall:)?\s*(cs|hrc|inc)\d+\s*$",
        r"^recall:",
        r"^(re-?open(ing)?|follow[- ]?up|folllow up|fu|continuation|in reference to|past case|reopening)\b[^a-z]*(of |to |from |on |up )?(case |ticket )?(cs\d+|previous case|question for case cs\d+)",
        r"^(follow[- ]?up|folllow up) (to|on|from)?:?\s*(case )?cs\d+\s*$",
        r"^(re: )?\[external\] (fw: )?\[external\] your requests have been complete",
        r"^ask a question$|^question answer$|^i need short instruction$",
    ],
)

RULES: dict[str, list[tuple[str, list[str]]]] = {
    "Automations": [
        NON_ACTIONABLE,
        (
            "Run history, audit log & trigger-count visibility",
            [
                r"audit", r"run history", r"trigger counts?", r"logging",
                r"triggered column", r"trigger number", r"saying failed but",
                r"list of automation failures", r"notified if automation fails",
                r"failure notice", r"why (the )?automation did not run",
                r"why candidate .* did not trigger", r"understanding why automation failed",
                r"automations failed --- why", r"clarification on automation email trigger count",
                r"retrigger", r"\bre-?triggered\b",
            ],
        ),
        (
            "Export, bulk upload & candidate data",
            [r"export", r"bulk", r"upload", r"import", r"download", r"\bcvs?\b", r"resume"],
        ),
        (
            "Wrong, duplicate or unexpected automation actions",
            [
                r"wrongly", r"incorrect(ly)?", r"twice", r"duplicat", r"\b2x\b",
                r"erroneous", r"prematurely", r"all requisitions", r"excluded",
                r"wrong req", r"not selecting the correct", r"extra message",
                r"deleted but still", r"enabled by accident", r"contacting rejected",
                r"moved to manager review", r"automatically rejected",
                r"triggered not correctly", r"not firing correctly",
            ],
        ),
        (
            "Automation not triggering / failing",
            [
                r"not trigger", r"did not trigger", r"didn'?t trigger", r"doesn'?t seem to trigger",
                r"not firing", r"fail", r"broken", r"not working", r"won'?t run",
                r"don'?t seem to run", r"did not run", r"not (being )?sent", r"not sending",
                r"not (being )?delivered", r"error", r"outage", r"not properly", r"significant delay",
                r"not consistently", r"does not work", r"not running", r"disappeared",
                r"unable to load", r"not getting triggered", r"not updating", r"not added",
                r"tags? missing", r"descrepency|discrepancy", r"didn'?t send", r"did not follow",
                r"not moving", r"not being moved", r"not shown", r"not appearing", r"spam", r"not sharing",
            ],
        ),
        (
            "Screening, interview & Voice Agent automations",
            [r"screen", r"interview", r"voice agent", r"questionnaire", r"\bowi\b", r"knockout"],
        ),
        (
            "Automation setup, configuration questions & feature requests",
            [
                r"\badd(ing)?\b", r"enabl", r"filter", r"condition", r"request", r"set ?up",
                r"recipe", r"feasibility", r"help", r"question", r"logic", r"review",
                r"not available", r"\boption\b", r"how (to|can|did|do)", r"\bcan (i|we|the)\b",
                r"pause", r"\bstop\b", r"\bdelay\b", r"exclude", r"workflow", r"automation\b",
            ],
        ),
        (
            "Hiring status & stage movement",
            [r"hiring status", r"status", r"stage from|previous stage|job stage", r"step"],
        ),
        (
            "Automated email / template content",
            [r"email", r"template", r"placeholder", r"sender", r"notification", r"reminders?", r"\bsms\b"],
        ),
        (
            "Access, environments & ATS/HRM sync",
            [r"access", r"log ?in", r"staging", r"sandbox", r"mirroring", r"\bsync", r"\bhrm\b", r"\bsf\b", r"redirected", r"retention"],
        ),
        (
            "Jobs, offers, events & other records (logged under Automations)",
            [r"\bjobs?\b", r"offer", r"requisition", r"event", r"project", r"categor", r"notes", r"candidate page", r"forward", r"source", r"tags?\b"],
        ),
    ],
    "Profile": [
        NON_ACTIONABLE,
        (
            "Profile merge, unmerge & duplicate profiles",
            [
                r"merg", r"duplicat", r"two profiles", r"appears twice", r"double profiles",
                r"same email", r"\b\d+ profiles\b", r"appears \d+ times", r"two (separate|identical)",
                r"two candidates", r"data of 2 different", r"de-?link", r"linking directly to",
                r"multiple (agency )?candidate profiles", r"duplicate management",
                r"multople agency", r"two records",
            ],
        ),
        (
            "Privacy, GDPR, deletion, purge & consent",
            [
                r"gdpr", r"rgpd", r"privacy", r"purg", r"\bdelet\w*\b(?!.*\b(attach|document|resume))",
                r"anonymi", r"erasure", r"retention", r"consent", r"opt[- ]?in", r"opted out",
                r"\bremov(e|al)\b(?!.*\b(document|cv|resume|location|attach))(?=.*(candidate|profile|application))",
                r"right to delete", r"data protection", r"suppress", r"anonymous", r"delatea", r"eliminated",
                r"candidate removal", r"removing test data", r"what is shown to candidates",
            ],
        ),
        (
            "Profile / traffic source & referral attribution",
            [
                r"source", r"traffic", r"\butm\b", r"\breferr", r"tracking", r"imported_from_ats", r"tagged as ats apply",
                r"track candidates", r"how .*profile was created", r"lead entered",
            ],
        ),
        (
            "Resumes, documents & resume parsing",
            [
                r"resume(?! review)", r"\bcvs?\b", r"\bcv's\b", r"document", r"attachment", r"\bpars(e|ed|er|ing)\b|parcing", r"\bword\b",
                r"\.pdf|\bpdf\b", r"upload", r"zip file", r"jsq", r"certifications",
            ],
        ),
        (
            "Hiring status changes & mismatches",
            [
                r"hiring status", r"status", r"statues", r"disposition", r"reject", r"declin", r"pipeline",
                r"workflow", r"\b(hiring|offer|interview|first|ready to offer) stages?\b", r"stage change", r"stage visibility",
                r"post[- ]apply", r"pre[- ]apply",
            ],
        ),
        (
            "Employee vs. candidate classification (internal, alumni, terminated)",
            [
                r"employee", r"internal", r"alumni", r"terminated", r"termed", r"former",
                r"prior workers?", r"contingent", r"purple ring", r"blue circle",
            ],
        ),
        (
            "Candidates, applications or data missing / not syncing with ATS",
            [
                r"missing", r"not (visible|showing|found|searchable|flowing|fed|feeding|transferred)",
                r"disappeared", r"\bsync", r"workday", r"\bwd\b", r"\bsf\b", r"successfactors",
                r"\bats\b", r"ukg", r"\borc\b", r"\bsap\b", r"not .* in phenom", r"flown to crm",
                r"unable to (find|see)", r"cannot (find|see)", r"\blag(ging)?\b", r"\bdelay\b(?! notifications)",
            ],
        ),
        (
            "Candidate profile data, fields & contact details",
            [
                r"email", r"phone", r"location", r"address", r"\bname\b", r"names", r"field",
                r"language", r"salary", r"country", r"city", r"skills", r"tags?\b", r"category",
                r"profile summary", r"ai generated", r"evaluations?", r"assessment", r"\bdata\b",
                r"profile creation", r"getting created", r"linkedin", r"fraud", r"candidate id", r"mismatch", r"inaccurate",
                r"incorrect", r"special characters", r"distance", r"graduation", r"fit ?score",
                r"contact", r"profile doesnt make sense", r"update candidate profiles", r"tagging",
                r"\bcrm profiles?\b", r"candidate profile\b", r"wrong tab",
            ],
        ),
        (
            "Applications & candidate-to-job association",
            [
                r"application", r"appl(y|ied|ying)", r"\bjobs?\b", r"\bjr\b|jr#", r"requisition", r"\breqs?\b",
                r"moving applicants", r"candidate adding", r"add(ing)? (new )?candidates?", r"\bleads?\b",
                r"invited to apply", r"\bria\b", r"recommended jobs", r"similar candidate",
            ],
        ),
        (
            "Interview, screening & offer details on profile",
            [
                r"interview", r"screen", r"offer", r"onboarding", r"recording", r"availability",
                r"calendar", r"i-9", r"e-?sign", r"questionnaire", r"\bscheduling\b",
            ],
        ),
        (
            "Forwarding candidates & hiring-manager view",
            [r"forward", r"hiring manager", r"\bhm\b", r"interviewer"],
        ),
        (
            "Activity log & profile audit history",
            [r"activity", r"audit", r"\blog\b", r"who (rejected|added)", r"changes made", r"who .* listed"],
        ),
        (
            "Search, filters & lists",
            [r"search", r"filter", r"\blists?\b", r"read versus unread", r"column"],
        ),
        (
            "Access, login & user accounts",
            [r"access", r"log ?in", r"\buser", r"provisioning", r"role groups", r"test system"],
        ),
        (
            "Automation & Talent Community items (logged under Profile)",
            [r"automation", r"trigger", r"talent community", r"job alerts", r"campaign", r"\bsms\b"],
        ),
    ],
    "Messaging": [
        NON_ACTIONABLE,
        (
            "Staging / UAT: email whitelisting & test-environment messaging",
            [r"white ?list", r"whitelisting", r"\bstag(ing|ging)\b", r"\bstg\b", r"\buat\b", r"in test\b", r"test sends?", r"testing in"],
        ),
        (
            "WhatsApp messaging",
            [r"what'?s ?app"],
        ),
        (
            "SMS: sending, numbers, inbox & opt-in",
            [
                r"\bsms\b", r"\btext(s|ing)\b", r"\btext messag", r"area code", r"short code",
                r"call forwarding", r"phone number", r"handset", r"no numbers? available",
                r"twilio", r"phenom number",
            ],
        ),
        (
            "Template placeholders & tokens not resolving",
            [
                r"placeholder", r"token", r"\[\[\[", r"#firstname", r"#employeename",
                r"first name", r"preferred name", r"tag not loading", r"tags? in email",
                r"not pulling (in )?(employee )?names?",
            ],
        ),
        (
            "Job alerts, subscriptions, Talent Community & incomplete-apply reminders",
            [
                r"job ?alert", r"\balerts\b", r"subs?cri", r"job widget", r"\bjtc\b", r"talent community", r"incomplete",
                r"partial[/ ](incomplete )?apply", r"finish your application", r"complete your application",
                r"unsubscribe", r"similar jobs?",
            ],
        ),
        (
            "Email campaigns & drip / always-on campaigns",
            [r"campa", r"drip", r"always[- ]on", r"\bblast", r"newsletter"],
        ),
        (
            "Recruiter / hiring-manager system notifications",
            [
                r"notif", r"notiication", r"tagged", r"reminder", r"evaluation", r"evaluators", r"approval emails?",
                r"alert emails", r"email alerts",
            ],
        ),
        (
            "Recruiter inbox & candidate replies (Phenom / Outlook)",
            [
                r"repl(y|ies)", r"inbox", r"outlook", r"thread", r"response", r"returning email",
                r"responding", r"\booo\b|out of office",
            ],
        ),
        (
            "Email deliverability: not received, bounced, spam, blocked, suppressed",
            [
                r"spam", r"junk", r"bounc", r"blocked", r"suppress", r"undeliver", r"dropped",
                r"drop rate", r"not (being )?(received|receiving|delivered|delivering)",
                r"not getting delivered", r"did(n'?t| not) (get|receive)", r"no-?reply",
                r"sendgrid", r"dkim", r"domain", r"\bip addresses\b", r"invalid email",
                r"delivery", r"fatal error", r"quarantine", r"focused", r"malicious",
                r"proofpoint", r"unable to send", r"not able to send", r"send(ing)? fail",
                r"not functioning", r"cannot (email|send)", r"emails? not (going|working)",
                r"not going through", r"not reaching", r"unable to receive", r"stuck on .?sending",
            ],
        ),
        (
            "Candidate system emails not sending or wrong (apply thank-you, confirmation, rejection, referral)",
            [
                r"thank you", r"thanks for applying", r"confirmation", r"acknowledg", r"reject", r"declin", r"disposition",
                r"referral", r"welcome", r"job filled", r"status update", r"comms when status",
                r"password", r"\botp\b", r"registration",
            ],
        ),
        (
            "Screening & interview invitation emails",
            [r"screening", r"interview", r"voice agent", r"invite", r"scheduling", r"x\+"],
        ),
        (
            "Email templates: branding, footer, links, editing & default templates",
            [
                r"template", r"footer", r"logo", r"banner", r"header", r"button", r"font",
                r"colou?r", r"brand", r"\blinks?\b", r"sender", r"signature", r"image",
                r"translation", r"language", r"\burl", r"copyright", r"icon", r"html",
                r"from name", r"from\" field|\"from\"", r"white label",
            ],
        ),
        (
            "Messaging automations not triggering",
            [r"automation", r"pre-set", r"\btrigger"],
        ),
        (
            "Opt-in, opt-out & consent",
            [r"\bopt(ed|ing)?[- ]?(in|out|back)", r"consent", r"unwanted emails"],
        ),
        (
            "1:1 email sending & email activity visibility",
            [
                r"1:1|1 on 1", r"email activity", r"send(ing)? emails?", r"send mail", r"emails? in crm",
                r"emails? not showing", r"subject", r"emailing", r"sending address", r"email address",
                r"who sent", r"viewing an email", r"candidate emails?\b", r"email issue", r"spell check",
                r"\bemails?\b.*\b(issue|struggles)", r"scheduled email", r"recruiter not getting emails",
                r"deleting emails", r"email setting", r"email configuration", r"media not loading",
                r"sent via email", r"secondary email", r"document received",
            ],
        ),
        (
            "Access, roles & permissions",
            [r"access", r"\broles?\b", r"permission"],
        ),
        (
            "Lists (static & dynamic)",
            [r"\blists?\b", r"filter"],
        ),
        (
            "Event communications",
            [r"event"],
        ),
        (
            "Messaging reporting & analytics",
            [r"\bdata\b", r"report", r"metric", r"analytic", r"\bcount\b", r"performance", r"export"],
        ),
    ],
    "CRM Core": [
        NON_ACTIONABLE,
        (
            "LinkedIn integration (CRM Connect, Recommendations, sharing)",
            [r"linked ?in", r"crm connect", r"linkeidn", r"linkendin", r"\bli (crm|profile)\b", r"inmail"],
        ),
        (
            "EC Trigger issues",
            [r"\bec trigger"],
        ),
        (
            "Security, compliance & data-privacy requests",
            [
                r"soc ?2", r"pentest", r"vulnerab", r"itdr", r"data privacy", r"security review",
                r"dns records", r"work(s|ers)? council", r"encryption", r"\bcmk\b", r"legal (queries|inquiry)",
                r"compliance",
            ],
        ),
        (
            "Audit trail & 'who changed it' questions",
            [
                r"audit", r"who (closed|cancelled|created|schedule)", r"activity log",
                r"who added", r"how was the hiring team added",
            ],
        ),
        (
            "Feature enablement & feature-flag requests",
            [r"feature flag", r"\benabl", r"turn (on|off)", r"\bdisable"],
        ),
        (
            "Performance, outages & UI errors",
            [
                r"slow", r"\blag(ging)?\b", r"latenc", r"(?<!drop )\bdown\b", r"not loading", r"glitch", r"spinning",
                r"wheel of doom", r"session expires", r"buffering", r"error loading",
                r"crm (is )?not (available|opening)", r"not opening", r"not working correctly", r"front[- ]end", r"rendering",
                r"load time", r"something went wrong", r"system latncy", r"typing cursor",
                r"screen re-setting", r"weird system", r"screen size", r"error 409",
                r"not accessible", r"appears down", r"staging is not working", r"screens not loading",
                r"dashboard", r"\bicon\b", r"menu", r"\bui\b", r"mobile app", r"browser",
                r"px width", r"need to refresh", r"error messages?", r"undefined", r"time stamps",
                r"page (not loading|error)", r"phenom app", r"recruiter app\b",
            ],
        ),
        (
            "Access, roles, permissions & login",
            [
                r"access", r"\b(custom|user|crm|hrit|recruiter|works council|admin) roles?\b", r"\broles? (and|&|list|details|required|creation|changes|for (users|recruiters))\b",
                r"users or roles", r"roles in crm", r"permission", r"log ?in", r"scope", r"departmentali",
                r"provision", r"\bsso\b", r"cookie", r"users? (not|unable|error)",
                r"proxy", r"license", r"left the company", r"users leave", r"restricted views",
                r"cannot access", r"unable to access", r"gear icon",
            ],
        ),
        (
            "Interview scheduling, calendars, evaluations & scorecards",
            [
                r"interview", r"calendar", r"schedul(ing|er)\b", r"scorecard", r"evaluation", r"meeting",
                r"outlook", r"transcript", r"recording", r"time ?zones?", r"availability",
            ],
        ),
        (
            "Assessments & video screening",
            [
                r"assessment", r"otome?yt|otomyte", r"talogy", r"video", r"hirevue|modern hire",
                r"screening questionnaire", r"screening enabled", r"\bhogan\b", r"clinical delay",
            ],
        ),
        (
            "Invite to Apply & Recruiter Initiated Apply",
            [r"invite to apply", r"\bria\b", r"recruiter initiated apply"],
        ),
        (
            "Offer letters & pre-onboarding",
            [r"offer", r"onboarding", r"preboarding", r"bank and nominee", r"\be-?sign", r"\bbgv\b"],
        ),
        (
            "Fit Score & AI features (AI Discovery, X+, Voice Agent, Intelligent Sourcing)",
            [
                r"fit ?score", r"\bai\b", r"x\+", r"voice agent", r"intelligent sourcing",
                r"\bia discovery\b", r"framework \d", r"matching criteria", r"gen.ai", r"chatbot", r"\bbot\b",
            ],
        ),
        (
            "Agency portal",
            [r"agency"],
        ),
        (
            "Projects",
            [r"project"],
        ),
        (
            "Bulk upload, import, export, documents & reports",
            [
                r"bulk", r"import", r"upload", r"export", r"report", r"extract", r"download",
                r"migration", r"historical", r"attach", r"document", r"\bjsq", r"resume", r"raw data",
            ],
        ),
        (
            "Duplicate & merged profiles (logged under CRM Core)",
            [r"duplica", r"merg", r"created multiple times", r"multiple (candidate profiles|emails)"],
        ),
        (
            "Email, notifications & Talent Community (logged under CRM Core)",
            [
                r"\bemails?\b(?!.*\b(address|id)\b)", r"notification", r"talent community", r"\bsms\b", r"campaign", r"thank you",
                r"\bjtc\b", r"subscri", r"opt-in", r"placeholder", r"whitelist", r"\btc\b",
                r"apply_thank_you", r"delivered",
            ],
        ),
        (
            "Automation items (logged under CRM Core)",
            [r"automation"],
        ),
        (
            "Events & university recruiting",
            [r"\bevents?\b", r"university", r"campus", r"career fair"],
        ),
        (
            "Spotlights, filters, search & lists",
            [r"spotlight", r"filter", r"search", r"\blists?\b", r"columns?", r"sort"],
        ),
        (
            "Tags & notes",
            [r"\btag", r"\bnotes?\b"],
        ),
        (
            "Job posting, publishing, closing & career-site visibility",
            [
                r"\bpost(ed|ing)?\b(?![- ]?(apply|application|hire))", r"publish", r"unpost", r"\bclos(e|ed|ing)\b", r"reopen|re-open",
                r"career ?site", r"website", r"expir", r"open jobs", r"private job", r"job link",
                r"preview (of|link)|previewing|job preview", r"draft", r"\bactive\b", r"\bfilled\b", r"approv", r"cancel a req",
                r"delete job", r"job req deletion",
            ],
        ),
        (
            "Job & requisition access, assignment and hiring team",
            [
                r"confidential", r"recruiter", r"hiring manager", r"hiring team", r"coordinator",
                r"assign", r"supervisor", r"can'?t see|cannot see|not able to see|unable to view|not seeing",
                r"visib", r"collaborat", r"restrict",
            ],
        ),
        (
            "Job fields, dropdowns, locations & translations",
            [
                r"field", r"dropdown|drop down", r"location", r"channel partner", r"bridgecare",
                r"vertical structure", r"categor", r"department", r"translat", r"language",
                r"job (code|level|family|description|details|data)", r"\bjd\b", r"facility",
                r"rejection reasons", r"classification", r"days open", r"\bdates?\b", r"template",
                r"org structure", r"benefits", r"pay rate", r"salary", r"spelling",
            ],
        ),
        (
            "Hiring status, lead/applicant pipeline & workflow",
            [
                r"hiring status", r"status", r"pipeline", r"workflow", r"(?<!\[)\bstages?\b(?! environment)", r"\bwf\b", r"step",
                r"\bleads?\b", r"disposition", r"move application", r"another req",
            ],
        ),
        (
            "ATS / HRIS sync & integrations (Workday, SF, UKG, API, Chrome extension)",
            [
                r"workday", r"\bsf\b", r"success ?factor", r"ukg", r"\bapi\b", r"chrome extension",
                r"integration", r"\bsync", r"\bhsi\b", r"\bats\b", r"\bfeed\b", r"naukri",
                r"seek", r"indeed", r"\binfor\b", r"\bmapping\b", r"not flowing", r"pull",
                r"not reflecting", r"\bicst?_|ics_sit|reflect",
            ],
        ),
        (
            "Job & requisition records (missing, creation, editing, discrepancies)",
            [r"\bjobs?\b", r"\breqs?\b|req's", r"requisition", r"\bp-\d+", r"positions?\b", r"advert", r"# of openings"],
        ),
        (
            "Candidate profile & data (logged under CRM Core)",
            [
                r"\bprofiles?\b", r"candidates? (not|incorrectly|unable)", r"missing candidates?",
                r"\bemployee", r"work experience", r"\bskills\b", r"consent", r"purged", r"anonymi",
                r"data (retention|storage|update)", r"internal (application|profile)", r"country code",
                r"user'?s data", r"(candidate|candidate experience|new joiner|application) data",
                r"duplicity", r"new submission",
            ],
        ),
    ],
}

_COMPILED = {
    area: [(name, [re.compile(p, re.I) for p in pats]) for name, pats in rules]
    for area, rules in RULES.items()
}


def assign_area(row: dict) -> str | None:
    return (
        SUB_PRODUCT_MAP.get(row.get("U_SUB_PRODUCT", ""))
        or COMPONENT_MAP.get(row.get("U_COMPONENT", ""))
        or SUB_PRODUCT_MAP.get(row.get("PRODUCT_EXPERIENCE_PRODUCT", ""))
    )


def area_source(row: dict) -> str:
    if row.get("U_SUB_PRODUCT", "") in SUB_PRODUCT_MAP:
        return "U_SUB_PRODUCT"
    if row.get("U_COMPONENT", "") in COMPONENT_MAP:
        return "U_COMPONENT"
    return "PRODUCT_EXPERIENCE_PRODUCT"


def classify(area: str, short_description: str) -> tuple[str, str]:
    text = (short_description or "").strip()
    for name, regs in _COMPILED[area]:
        for rgx in regs:
            if rgx.search(text):
                return name, rgx.pattern
    return UNCLASSIFIED, ""


def load(csv_path: str, start: str, end: str) -> tuple[list[dict], dict]:
    rows, stats = [], Counter()
    with open(csv_path, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            day = r["CREATED_ON_UTC"][:10]
            if not (start <= day <= end):
                continue
            stats["in_date_range"] += 1
            area = assign_area(r)
            if not area:
                continue
            stats["in_scope_areas"] += 1
            if r.get("SUB_STATUS_LABEL", "") in EXCLUDED_SUB_STATUS:
                stats[f"excluded_{r['SUB_STATUS_LABEL'].lower()}"] += 1
                continue
            theme, pattern = classify(area, r["SHORT_DESCRIPTION"])
            rows.append(
                {
                    "case": r["NUMBER"],
                    "created": day,
                    "area": area,
                    "area_source": area_source(r),
                    "theme": theme,
                    "pattern": pattern,
                    "verbatim": " ".join(r["SHORT_DESCRIPTION"].split()),
                    "client": r.get("CLIENT_NAME", ""),
                    "status": r.get("STATUS", ""),
                    "jira": r.get("JIRA_CREATED", ""),
                }
            )
    return rows, stats


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


CSS = """
:root{
  --pds-brand:#1a73e8;--pds-brand-hover:#174ea6;--pds-brand-teal:#188038;
  --pds-text:#202124;--pds-text-muted:#5f6368;--pds-surface:#fff;--pds-surface-muted:#f8f9fa;
  --pds-border:#dadce0;--pds-success:#188038;--pds-error:#d93025;
  --pds-radius-md:8px;--font-family-body:Arial,Helvetica,sans-serif;
  --tabbar:56px;
}
*{box-sizing:border-box}
html,body,button,input,textarea,select{font-family:Arial,Helvetica,sans-serif}
body{color:var(--pds-text);background:var(--pds-surface-muted);margin:0;line-height:1.5}
.page{max-width:1200px;margin:0 auto;padding:28px 24px 48px}
h1{font-size:22px;font-weight:400;margin:0 0 4px}
.lede{color:var(--pds-text-muted);margin:0 0 12px;font-size:14px}
p.meta{color:var(--pds-text-muted);margin:8px 0;font-size:13px}
details.about{background:var(--pds-surface);border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);padding:8px 14px;margin:0 0 16px}
details.about>summary{font-size:13px;font-weight:600}
table{border-collapse:collapse;width:100%;margin:8px 0 16px;font-size:13px;background:var(--pds-surface)}
th,td{border-bottom:1px solid var(--pds-border);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--pds-surface-muted);font-weight:600;position:sticky;top:var(--tabbar);z-index:1}
td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:0}
ul.v{margin:0;padding-left:18px}
ul.v li{margin:2px 0}
.case{color:var(--pds-text-muted);font-family:Arial,Helvetica,sans-serif;font-size:12px}
input#q{width:100%;padding:10px 12px;font:inherit;font-size:14px;border:1px solid var(--pds-border);border-radius:var(--pds-radius-md);margin:8px 0 12px;background:var(--pds-surface)}
input#q:focus{outline:2px solid var(--pds-brand);outline-offset:1px}
details{margin:4px 0}
summary{cursor:pointer;color:#1a73e8;font-weight:600}
details.area{background:var(--pds-surface);border:1px solid var(--pds-border);border-left-width:4px;border-radius:var(--pds-radius-md);margin:12px 0;padding:0 16px}
details.area>summary{font-size:16px;font-weight:600;padding:14px 0}
details.area>summary .sub{display:block;font-size:12px;font-weight:500;color:inherit;opacity:.8;margin:2px 0 0}
details.area[data-tone="core"]{border-left-color:#1a73e8}
details.area[data-tone="core"]>summary{color:#1a73e8}
details.area[data-tone="profile"]{border-left-color:#188038}
details.area[data-tone="profile"]>summary{color:#188038}
details.area[data-tone="messaging"]{border-left-color:#e37400}
details.area[data-tone="messaging"]>summary{color:#e37400}
details.area[data-tone="automations"]{border-left-color:#d93025}
details.area[data-tone="automations"]>summary{color:#d93025}
details.area[open]>summary{border-bottom:1px solid var(--pds-border);margin-bottom:12px}
h3{font-size:14px;margin:14px 0 6px}
ol.themes{columns:2;column-gap:32px;margin:0 0 12px;padding-left:20px;font-size:13px}
ol.themes li{break-inside:avoid;margin:3px 0}
.muted{color:var(--pds-text-muted)}
.toolbar{margin:8px 0}
.toolbar button{font:inherit;font-size:13px;font-weight:500;padding:6px 12px;margin-right:8px;border:1px solid var(--pds-border);background:var(--pds-surface);color:var(--pds-text);border-radius:var(--pds-radius-md);cursor:pointer}
.toolbar button:hover{background:#f1f3f4}
.tabs{position:sticky;top:0;z-index:3;display:flex;gap:6px;margin:0 -24px 8px;padding:10px 24px;background:var(--pds-surface-muted);border-bottom:1px solid var(--pds-border)}
.tabs button{font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:500;padding:8px 16px;border:1px solid transparent;background:transparent;color:var(--pds-text-muted);border-radius:20px;cursor:pointer}
.tabs button:hover{background:#f1f3f4;color:var(--pds-text)}
.tabs button:focus-visible{outline:2px solid var(--pds-brand);outline-offset:2px}
.tabs button.active{background:var(--pds-brand);color:#fff;border-color:var(--pds-brand);font-weight:600}
.tabs button.active:hover{background:var(--pds-brand-hover);border-color:var(--pds-brand-hover);color:#fff}
.tab{display:none;padding-top:8px}
.tab.active{display:block}
td.areacell{background:var(--pds-surface-muted);width:16%}
td.areacell b{font-size:15px}
td.areacell div{margin:4px 0;font-size:12px}
td.themecell{width:22%}
td.verbcell{width:26%}
td.themecell .tn{font-weight:600}
.lvl{display:inline-block;font-size:10px;font-weight:600;padding:1px 5px;border-radius:4px;margin-right:6px;color:#fff;vertical-align:1px}
.lvl.I{background:#1a73e8}.lvl.E{background:#188038}.lvl.S{background:#e37400}
ul.tree{list-style:none;padding-left:14px;margin:4px 0}
ul.tree li{margin:3px 0}
details.node>summary{font-weight:500}
.st{font-size:11px;font-weight:500;padding:1px 8px;border-radius:999px;border:1px solid var(--pds-border);color:var(--pds-text-muted);margin-left:6px;white-space:nowrap}
.st.In-Progress{background:color-mix(in srgb,var(--pds-brand) 10%,#fff);color:var(--pds-brand);border-color:transparent}
.ev{font-size:12px;color:var(--pds-text-muted);margin-left:6px}
.ctx{color:var(--pds-text-muted)}
a.k{font-family:Arial,Helvetica,sans-serif;font-size:13px;color:var(--pds-brand);text-decoration:none}
a.k:hover{text-decoration:underline}
a{color:var(--pds-brand)}
.none{color:var(--pds-error);font-weight:600}
.sec{font-size:12px;font-weight:600;color:var(--pds-text-muted);margin:8px 0 2px}
.sec:first-child{margin-top:0}
td.supcell{width:40%}
code{font-family:Arial,Helvetica,sans-serif;font-size:12px;background:var(--pds-surface-muted);border:1px solid var(--pds-border);border-radius:4px;padding:0 4px}
"""

JS = """
function f(){var q=document.getElementById('q').value.toLowerCase();
document.querySelectorAll('#all tbody tr').forEach(function(tr){
tr.style.display=tr.textContent.toLowerCase().indexOf(q)>-1?'':'none';});}
function toggleAreas(open,sel){document.querySelectorAll(sel||'details.area[data-area]').forEach(function(d){d.open=open;});}
function showTab(id){
document.querySelectorAll('.tab').forEach(function(t){var on=t.id===id;t.classList.toggle('active',on);t.hidden=!on;});
document.querySelectorAll('.tabs button').forEach(function(b){var on=b.dataset.tab===id;b.classList.toggle('active',on);b.setAttribute('aria-selected',on?'true':'false');});}
function openHash(){var el=location.hash&&document.getElementById(location.hash.slice(1));
if(!el)return;var tab=el.classList.contains('tab')?el:el.closest('.tab');if(tab)showTab(tab.id);
if(el===tab){window.scrollTo(0,0);return;}if(el.tagName==='DETAILS')el.open=true;el.scrollIntoView();}
function goArea(id){showTab('themes');var el=document.getElementById(id);el.open=true;el.scrollIntoView();
history.replaceState(null,'','#'+id);return false;}
window.addEventListener('hashchange',openHash);window.addEventListener('load',openHash);
"""


LEVEL_NAME = {"I": "Initiative", "E": "Epic", "S": "Story"}


def pick_examples(members: list[dict], examples: int) -> list[dict]:
    seen, ex = set(), []
    for r in sorted(members, key=lambda r: r["created"], reverse=True):
        key = r["verbatim"].lower()
        if key in seen or len(r["verbatim"]) < 6:
            continue
        seen.add(key)
        ex.append(r)
        if len(ex) == examples:
            break
    return ex


EMAIL_RX = re.compile(r"[A-Za-z0-9._%+-]*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+")
PHONE_RX = re.compile(r"(?<!req )(?<!req)(?<!\w)\+?\(?\d[\d\s().-]{8,}\d", re.I)


MASK = "xxxxxx"


def redact(s: str) -> str:
    """Mask emails, phone-like runs of 10+ digits and stored [email]/[phone] placeholders in displayed text."""
    s = EMAIL_RX.sub(MASK, s or "").replace("[email]", MASK).replace("[phone]", MASK)
    return PHONE_RX.sub(lambda m: MASK if sum(c.isdigit() for c in m.group(0)) >= 10 else m.group(0), s)


def verbatim_li(r: dict) -> str:
    return f"<li>&ldquo;{esc(redact(r['verbatim'])[:180])}&rdquo; <span class='case'>{r['case']}</span></li>"


def jira_line(level: str, key: str, summary: str, status: str | None, info: dict | None, on_board: bool,
              off_label: str = "not on CRM Core Board") -> str:
    tag = f"<span class='lvl {level}' title='{LEVEL_NAME[level]}'>{level}</span>"
    if key.startswith("_"):
        return f"{tag}<span class='ctx'>{esc(summary)}</span>"
    link = f"<a class='k' href='{JIRA_BROWSE}{key}' target='_blank' rel='noopener'>{key}</a>"
    st = f"<span class='st {status.replace(' ', '-')}'>{esc(status)}</span>" if status else ""
    if info and info["how"] == "direct":
        return f"{tag}{link} {esc(summary)}{st}<span class='ev'>matched &ldquo;{esc(info['evidence'])}&rdquo;</span>"
    if info:
        return f"{tag}{link} {esc(summary)}{st}<span class='ev'>via parent epic</span>"
    where = "context only" if on_board else f"context only, {off_label}"
    return f"{tag}{link} <span class='ctx'>{esc(summary)}</span>{st}<span class='ev'>{where}</span>"


def omitted_note(n_done: int, n_blocked: int, n_before: int, lead: str = "") -> str:
    parts = []
    if n_before:
        parts.append(f"{n_before} created before 2026-01-01")
    if n_done:
        parts.append(f"{n_done} Done")
    if n_blocked:
        parts.append(f"{n_blocked} Blocked")
    if not parts:
        return ""
    if len(parts) == 1:
        body = parts[0]
    else:
        body = ", ".join(parts[:-1]) + ", and " + parts[-1]
    return f"{lead}{body} items not shown"


def render_jira_tree(
    items: dict[str, dict], mapped: dict[str, dict],
    hidden_done: set[str], hidden_blocked: set[str], hidden_before: set[str],
    n_done: int, n_blocked: int, n_before: int,
    none_msg: str = "No open matching Initiative, Epic or Story on board 1091.",
    none_hint: str = "Listed in the Themes without Jira mapping tab.",
    off_label: str = "not on CRM Core Board",
    outside_label: str = "Initiative not visible (epic is not on the CRM Core Board)",
) -> str:
    if not mapped:
        note = omitted_note(n_done, n_blocked, n_before, " ")
        note = f"{note}." if note else ""
        return f"<span class='none'>{esc(none_msg)}</span> <span class='muted'>{note} {esc(none_hint)}</span>"
    types = Counter(items[k]["type"] for k in mapped)
    direct = sum(1 for v in mapped.values() if v["how"] == "direct")

    def story_li(k: str) -> str:
        it = items[k]
        return f"<li>{jira_line('S', k, it['summary'], it['statusCategory'], mapped[k], True, off_label)}</li>"

    parts = []
    for ini in build_tree(items, mapped, hidden_done, hidden_blocked, hidden_before, outside_label):
        inner = []
        for ep in ini["epics"]:
            head = jira_line("E", ep["key"], ep["summary"], ep["status"], ep["mapped"], ep["on_board"], off_label)
            if ep["stories"]:
                stories = "".join(story_li(k) for k in ep["stories"])
                inner.append(f"<li><details class='node'><summary>{head} <span class='muted'>"
                             f"({len(ep['stories'])} stories)</span></summary><ul class='tree'>{stories}</ul></details></li>")
            else:
                inner.append(f"<li>{head}</li>")
        inner.extend(story_li(k) for k in ini["stories"])
        head = jira_line("I", ini["key"], ini["summary"], ini["status"], ini["mapped"], ini["on_board"], off_label)
        if not inner:
            parts.append(f"<li>{head}</li>")
            continue
        n_ep = sum(1 for e in ini["epics"] if e["mapped"] or e["stories"])
        n_st = len(ini["stories"]) + sum(len(e["stories"]) for e in ini["epics"])
        parts.append(f"<li><details class='node'><summary>{head} <span class='muted'>({n_ep} epics, "
                     f"{n_st} stories)</span></summary><ul class='tree'>{''.join(inner)}</ul></details></li>")
    omitted = omitted_note(n_done, n_blocked, n_before, ", ")
    return (f"<details><summary>{types['Initiative']} initiatives &middot; {types['Epic']} epics &middot; "
            f"{types['Story']} stories open <span class='muted'>({direct} by title match, "
            f"{len(mapped) - direct} via parent epic{omitted})</span></summary><ul class='tree'>{''.join(parts)}</ul></details>")


LEVEL_OF_TYPE = {"Initiative": "I", "Epic": "E", "Story": "S"}
REMOVED_LABEL = {"done": "Done", "blocked": "Blocked", "before": "created before 2026-01-01"}


def sup_li(r: dict) -> str:
    return (f"<li><a class='k' href='{JIRA_BROWSE}{r['key']}' target='_blank' rel='noopener'>{r['key']}</a> "
            f"{esc(redact(r['summary'])[:160])} <span class='case'>{r['created']} &middot; {esc(r.get('request_type') or 'Type not set')}</span></li>")


def render_sup_linked(linked: dict[str, dict], removed: Counter, other_types: Counter) -> str:
    notes = []
    if removed:
        notes.append(", ".join(f"{n} {REMOVED_LABEL[k]}" for k, n in sorted(removed.items())))
    if other_types:
        notes.append(", ".join(f"{n} of type {t}" for t, n in other_types.most_common()) + " (not Initiative, Epic or Story)")
    note = f"<div class='muted'>Linked items not shown: {esc('; '.join(notes))}.</div>" if notes else ""
    if not linked:
        return f"<div class='muted'>No open Initiative, Epic or Story is linked from these SUP tickets.</div>{note}"
    lines = []
    for k, it in sorted(linked.items(), key=lambda kv: (-len(kv[1]["sup"]), kv[0])):
        lvl = LEVEL_OF_TYPE[it["type"]]
        tag = f"<span class='lvl {lvl}' title='{it['type']}'>{lvl}</span>"
        link = f"<a class='k' href='{JIRA_BROWSE}{k}' target='_blank' rel='noopener'>{k}</a>"
        st = f"<span class='st {it['statusCategory'].replace(' ', '-')}'>{esc(it['statusCategory'])}</span>"
        sups = ", ".join(f"{s} ({esc(rel)})" for s, rel in it["sup"][:3])
        more = f" +{len(it['sup']) - 3} more" if len(it["sup"]) > 3 else ""
        lines.append(f"<li>{tag}{link} {esc(it['summary'][:140])}{st}<span class='ev'>linked from {sups}{more}</span></li>")
    return f"<ul class='tree'>{''.join(lines)}</ul>{note}"


def render_sup_tab(sup: dict, examples: int) -> list[str]:
    areas, meta = sup["areas"], sup["meta"]
    total = sum(len(a["tickets"]) for a in areas.values())
    fetched = sum(meta["fetched"].values())
    done_all = Counter()
    for c in meta["done_removed"].values():
        done_all.update(c)
    done_txt = ", ".join(f"{n:,} {s}" for s, n in done_all.most_common())
    out = ["<div class='tab' id='sup'>"]
    out.append(
        f"<p class='meta'>{total:,} open SUP (support) tickets created from 2026-01-01 to {meta.get('fetched_on')} whose "
        f"Product Experience is one of the four CRM areas. {fetched - total:,} of the {fetched:,} fetched tickets are in "
        f"Jira's Done status category ({done_txt}) and are not shown or counted. Each area shows its open SUP ticket "
        "count, the themes found in the ticket titles, and the non-SUP Jira Initiatives, Epics and Stories associated "
        "with each theme.</p>"
    )
    jql = "".join(f"<li><b>{esc(a)}</b>: <code>{esc(q)}</code></li>" for a, qs in meta["jql"].items() for q in qs)
    out.append(
        "<details class='about'><summary>How this tab was built</summary><ul class='v'>"
        "<li>Source: Jira project SUP, read only, fetched on "
        f"{esc(meta.get('fetched_on') or '')}. Queries (results were paged and the stored count equals the Jira total for each query):<ul class='v'>{jql}</ul></li>"
        "<li>SUP tickets in Jira's Done status category (statuses Done, In Prod and Closed) are removed before "
        "classification. Open tickets in To Do or In Progress statuses, including Confirm Resolution and Reporter "
        "Review, are kept. Jira links are taken from open tickets only.</li>"
        "<li>Theme: the first matching phrase rule on the SUP ticket <em>title</em> (skill "
        "<code>01_product-os/skills/sup-ticket-themes</code>). Descriptions are not used: on a sample, most description-only "
        "matches were wrong. A title with no matching phrase stays Unclassified; no label is forced.</li>"
        "<li>Associated Jira items (non-SUP), two methods shown separately: <b>Linked from SUP</b> lists PHEM Initiatives, "
        "Epics and Stories that a SUP ticket in the theme links to in Jira; <b>Matched by title</b> lists PHEM "
        "Initiatives, Epics and Stories with the same Product Experience value, created on or after 2026-01-01, whose title "
        "contains one of the theme's phrases (a Story with no match inherits its parent Epic's themes).</li>"
        "<li>Done items, Blocked items and items created before 2026-01-01 are removed from both methods and counted. "
        "Engineering-only items (tooling, refactors, upgrades, test plumbing) are not matched by title, except to the "
        "performance and security themes.</li>"
        "<li>Email addresses and phone numbers in titles are shown as xxxxxx. Ticket descriptions, "
        "reporters and assignees are not shown.</li>"
        "<li>Limits: title matching misses Jira items worded differently from the theme phrases, and few SUP tickets carry "
        "a Jira link, so an empty cell means no evidence was found, not that no work exists.</li>"
        "</ul></details>"
    )
    out.append("<div class='toolbar'><button onclick=\"toggleAreas(true,'details.area[data-sup]')\">Expand all areas</button>"
               "<button onclick=\"toggleAreas(false,'details.area[data-sup]')\">Collapse all areas</button></div>")
    for area in AREAS:
        a = areas[area]
        tickets, themes, order = a["tickets"], a["themes"], a["order"]
        n = len(tickets)
        unc = themes[UNCLASSIFIED]
        named = [t for t in order if t != UNCLASSIFIED]
        has_jira = [t for t in named if a["linked"].get(t) or a["mapped"].get(t)]
        rt = " &middot; ".join(f"{c} {esc(k)}" for k, c in a["request_types"].most_common())
        st = " &middot; ".join(f"{c} {esc(k)}" for k, c in a["status"].most_common())
        rc = a["removed_counts"]
        n_done = sum(meta["done_removed"][area].values())
        done_s = ", ".join(f"{c} {s}" for s, c in meta["done_removed"][area].most_common())
        out.append(
            f"<details class='area' data-sup data-tone='{AREA_TONE[area]}' id='sup-{area.replace(' ', '-')}'><summary>{area}"
            f"<span class='sub'>{n:,} open SUP tickets &middot; {n_done:,} Done removed &middot; {len(named)} themes &middot; "
            f"{unc} unclassified &middot; {len(has_jira)} of {len(named)} themes with associated Jira items</span></summary>"
        )
        area_cell = (
            f"<b>{area}</b><div class='muted'>{esc(PRODUCT2[area])}</div>"
            f"<div><b>{n:,}</b> open SUP tickets since 2026-01-01</div>"
            f"<div class='muted'>{n_done:,} Done-category tickets removed ({esc(done_s)}) of {meta['fetched'][area]:,} fetched</div>"
            f"<div>{len(named)} themes &middot; {unc} unclassified ({unc/n*100:.1f}%)</div>"
            f"<div class='muted'>Type: {rt}</div><div class='muted'>Status: {st}</div>"
            f"<div>{len(has_jira)} of {len(named)} themes have associated Jira items</div>"
            f"<div class='muted'>Jira pool: {a['pool_total']} PHEM Initiative/Epic/Story items created since 2026-01-01; "
            f"{rc['done']} Done and {rc['blocked']} Blocked removed; {len(a['pool_kept'])} open used.</div>"
        )
        out.append("<table><thead><tr><th>Area &amp; SUP tickets</th><th>Themes in SUP tickets</th>"
                   "<th>Associated Jira items (non-SUP): Initiative &rsaquo; Epic &rsaquo; Story</th></tr></thead><tbody>")
        done_keys = {k for k, r in a["removed"].items() if r == "done"}
        blocked_keys = {k for k, r in a["removed"].items() if r == "blocked"}
        for i, t in enumerate(order):
            members = sorted((r for r in tickets if r["theme"] == t), key=lambda r: (r["created"], r["key"]), reverse=True)
            c = len(members)
            bugs = sum(1 for r in members if r.get("request_type") == "Bug-Customer")
            ex = members[:examples]
            rest = members[examples:]
            more = (f"<details><summary>All {c} tickets</summary><ul class='v'>{''.join(sup_li(r) for r in rest)}</ul></details>"
                    if rest else "")
            theme_cell = (
                f"<div class='tn'>{esc(t)}</div>"
                f"<div class='muted'>{c} tickets &middot; {c/n*100:.1f}% of area &middot; {bugs} Bug-Customer</div>"
                f"<ul class='v'>{''.join(sup_li(r) for r in ex)}</ul>{more}"
            )
            if t == UNCLASSIFIED:
                jira_cell = "<span class='muted'>No theme, so no Jira association. Most of these titles are case references or too general to classify.</span>"
            else:
                mapped = a["mapped"].get(t, {})
                linked = a["linked"].get(t, {})
                mall = a["mapped_all"].get(t, {})
                tree = render_jira_tree(
                    a["pool_kept"], mapped, done_keys, blocked_keys, set(),
                    sum(1 for k in mall if k in done_keys), sum(1 for k in mall if k in blocked_keys), 0,
                    none_msg="", none_hint="",
                    off_label=f"outside the 2026 {area} set",
                    outside_label=f"Initiative not visible (parent epic is outside the 2026 {area} set)",
                ) if mapped else ""
                if not mapped:
                    n_d = sum(1 for k in mall if k in done_keys)
                    n_b = sum(1 for k in mall if k in blocked_keys)
                    note = omitted_note(n_d, n_b, 0, " ")
                    tree = f"<div class='muted'>No open 2026 {area} Initiative, Epic or Story matches this theme by title.{note + '.' if note else ''}</div>"
                lead = "" if (mapped or linked) else "<div class='none'>No associated non-SUP Jira item found.</div>"
                jira_cell = (
                    f"{lead}<div class='sec'>Linked from SUP tickets ({len(linked)})</div>"
                    f"{render_sup_linked(linked, a['linked_removed'].get(t, Counter()), a['linked_other_types'].get(t, Counter()))}"
                    f"<div class='sec'>Matched by title</div>{tree}"
                )
            first = f"<td class='areacell' rowspan='{len(order)}'>{area_cell}</td>" if i == 0 else ""
            out.append(f"<tr>{first}<td class='themecell supcell'>{theme_cell}</td><td>{jira_cell}</td></tr>")
        out.append("</tbody></table></details>")
    out.append("</div>")
    return out


def render(rows: list[dict], stats: dict, start: str, end: str, examples: int, jira: dict, sup: dict | None = None) -> str:
    by_area = defaultdict(list)
    for r in rows:
        by_area[r["area"]].append(r)
    jitems, jmap, jstats, jeng = jira["items"], jira["mapped"], jira["stats"], jira["engineering"]
    jdone, jblocked, jbefore, jmap_all = jira["done"], jira["blocked"], jira["before"], jira["mapped_with_done"]

    def removed_count(area: str, theme: str, keys: set[str]) -> int:
        return sum(1 for k in jmap_all[area].get(theme, {}) if k in keys)

    out = [
        "<!doctype html><html><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>CRM service request themes - Jan to Aug 2026</title>",
        f"<style>{CSS}</style></head><body><div class='page'>",
        "<h1>CRM service request themes</h1>",
        f"<p class='lede'>{len(rows):,} cases from {start} to {end} across CRM Core, Profile, Messaging, and Automations. "
        f"Jira mapping uses {jstats['open']:,} open board items created on or after 2026-01-01.</p>",
        "<details class='about'><summary>How this report was built</summary>",
        f"<p class='meta'>Source: Google Sheet <em>All Servicenow service requests from 2026-01-01</em> "
        "(ID 1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8). No other sources used. "
        f"Cases in the window: {stats['in_date_range']:,}. In the four areas: {stats['in_scope_areas']:,}. "
        f"Excluded as Spam ({stats.get('excluded_spam',0)}) or Duplicate ({stats.get('excluded_duplicate',0)}).</p>",
        "<p class='meta'>Area comes from U_SUB_PRODUCT, then U_COMPONENT, then PRODUCT_EXPERIENCE_PRODUCT. "
        "Theme is the first matching phrase on the Short description. No match stays Unclassified.</p>",
        "<p class='meta'>Jira is the CRM Core Board (board 1091), read-only. "
        f"{jstats['fetched']:,} Initiative, Epic, and Story items. Metadata excluded: {jstats['excluded']}. "
        f"Done removed: {jstats['done']:,}. Blocked removed: {jstats['blocked']}. "
        f"Created before 2026-01-01 removed: {jstats['before']:,}. "
        "The board holds CRM - Core work only.</p></details>",
    ]

    def theme_order(area: str, themes: Counter) -> list[str]:
        names = list(dict.fromkeys([name for name, _ in RULES[area]] + list(themes)))
        return sorted(names, key=lambda t: (t == UNCLASSIFIED, t.startswith("Non-actionable"), -themes[t]))

    def is_theme(t: str) -> bool:
        return t != UNCLASSIFIED and not t.startswith("Non-actionable")

    unmapped = [
        (area, t) for area in AREAS
        for t in theme_order(area, Counter(r["theme"] for r in by_area[area]))
        if is_theme(t) and any(r["theme"] == t for r in by_area[area]) and not jmap[area].get(t)
    ]
    out.append(
        "<div class='tabs' role='tablist' aria-label='Report sections'>"
        "<button type='button' role='tab' class='active' aria-selected='true' data-tab='summary' onclick=\"showTab('summary')\">Summary</button>"
        "<button type='button' role='tab' aria-selected='false' data-tab='themes' onclick=\"showTab('themes')\">Themes mapped to JIRA</button>"
        f"<button type='button' role='tab' aria-selected='false' data-tab='unmapped' onclick=\"showTab('unmapped')\">Themes not mapped to Jira ({len(unmapped)})</button>"
        + (f"<button type='button' role='tab' aria-selected='false' data-tab='sup' onclick=\"showTab('sup')\">"
           f"SUP ticket themes ({sum(len(a['tickets']) for a in sup['areas'].values()):,})</button>" if sup else "")
        + f"<button type='button' role='tab' aria-selected='false' data-tab='cases' onclick=\"showTab('cases')\">All cases ({len(rows):,})</button></div>"
    )

    summary = ["<div class='tab active' id='summary'>"]
    summary.append(f"<p class='meta'>{len(rows):,} cases analysed across {len(AREAS)} areas. "
                   "Expand an area to see every theme identified in it.</p>")
    summary.append("<div class='toolbar'><button onclick=\"toggleAreas(true,'details.area[data-sum]')\">Expand all</button>"
                   "<button onclick=\"toggleAreas(false,'details.area[data-sum]')\">Collapse all</button></div>")
    for area in AREAS:
        items = by_area[area]
        n = len(items)
        themes = Counter(r["theme"] for r in items)
        unc = themes[UNCLASSIFIED]
        jira = sum(1 for r in items if r["jira"] == "Yes")
        order = theme_order(area, themes)
        aid = area.replace(" ", "-")
        theme_s = "".join(
            f"<li{'' if is_theme(t) else ' class=muted'}>{esc(t)} &mdash; {themes[t]} ({themes[t]/n*100:.1f}%)</li>"
            for t in order
        )
        summary.append(
            f"<details class='area' data-sum data-tone='{AREA_TONE[area]}' id='sum-{aid}'><summary>{area}"
            f"<span class='sub'>{n:,} cases &middot; {n/len(rows)*100:.1f}% of analysed &middot; "
            f"{(n-unc)/n*100:.1f}% classified &middot; {unc} unclassified &middot; {jira} Jira linked &middot; "
            f"{sum(1 for t in order if is_theme(t))} themes</span></summary>"
            "<table><thead><tr><th>Cases</th><th>% of analysed</th><th>Classified</th><th>Unclassified</th>"
            "<th>Jira linked (Yes)</th></tr></thead><tbody>"
            f"<tr><td class='num'>{n:,}</td><td class='num'>{n/len(rows)*100:.1f}%</td>"
            f"<td class='num'>{(n-unc)/n*100:.1f}%</td><td class='num'>{unc}</td><td class='num'>{jira}</td></tr>"
            "</tbody></table>"
            f"<h3>All themes identified in {area}</h3><ol class='themes'>{theme_s}</ol>"
            f"<p><a href='#{aid}' onclick=\"return goArea('{aid}')\">Open {area} theme details with example verbatims</a></p>"
            "</details>"
        )
    summary.append("</div>")

    out.append("<div class='tab' id='themes'>")
    out.append(
        "<details><summary>How Jira items were mapped to themes</summary><ul class='v'>"
        "<li>Each theme has its own phrase list. An Initiative, Epic or Story maps to a theme when its title contains "
        "one of those phrases; the matched phrase is shown next to the item. One item can map to more than one theme.</li>"
        "<li>A Story whose own title does not match inherits its parent Epic's themes (shown as <em>via parent epic</em>).</li>"
        "<li>Unmatched parents are shown as <em>context only</em> so the Initiative &rsaquo; Epic &rsaquo; Story path stays visible.</li>"
        f"<li>Engineering-only and internal-analytics items (tooling, observability, refactors, tech debt, framework upgrades, "
        f"test plumbing, business-review metrics), judged by the item's or its parent epic's title ({jeng} items), are not "
        "mapped, except to the Performance and Security themes.</li>"
        "<li>Done items, Blocked items, and items created before 2026-01-01 are removed. A 2026 Story or Epic whose parent "
        "was removed sits under a label naming that reason, and Stories do not inherit themes from a removed Epic.</li>"
        "<li>Metadata items are excluded (see the header). Non-actionable cases are not mapped; Unclassified cases are shown as a count only.</li>"
        "</ul></details>"
    )
    out.append("<div class='toolbar'><button onclick='toggleAreas(true)'>Expand all areas</button>"
               "<button onclick='toggleAreas(false)'>Collapse all areas</button></div>")
    for area in AREAS:
        items = by_area[area]
        n = len(items)
        themes = Counter(r["theme"] for r in items)
        order = [t for t in theme_order(area, themes) if is_theme(t) and themes[t]]
        empty = [t for t in theme_order(area, themes) if is_theme(t) and not themes[t]]
        non_act = sum(c for t, c in themes.items() if t.startswith("Non-actionable"))
        n_mapped = sum(1 for t in order if jmap[area].get(t))
        out.append(
            f"<details class='area' data-area data-tone='{AREA_TONE[area]}' id='{area.replace(' ','-')}'><summary>{area}"
            f"<span class='sub'>{n:,} cases &middot; {len(order)} themes &middot; {themes[UNCLASSIFIED]} unclassified "
            f"&middot; {n_mapped} of {len(order)} themes mapped to Jira</span></summary>"
        )
        area_cell = (
            f"<b>{area}</b><div>{n:,} service requests</div><div>{len(order)} themes</div>"
            f"<div>{themes[UNCLASSIFIED]} unclassified</div>"
            f"<div class='muted'>{non_act} non-actionable (not mapped)</div>"
            f"<div>{n_mapped} of {len(order)} themes mapped to Jira</div>"
            f"<div class='{'none' if n_mapped < len(order) else 'muted'}'>{len(order) - n_mapped} themes without a Jira mapping</div>"
        )
        if empty:
            area_cell += f"<div class='muted'>No cases this window: {esc('; '.join(empty))}</div>"
        out.append("<table><thead><tr><th>Area</th><th>Themes identified (service requests)</th>"
                   "<th>Example verbatims</th>"
                   "<th>Mapped Jira items: Initiative &rsaquo; Epic &rsaquo; Story (board 1091)</th></tr></thead><tbody>")
        for i, t in enumerate(order):
            members = [r for r in items if r["theme"] == t]
            c = len(members)
            linked = sum(1 for r in members if r["jira"] == "Yes")
            ex = pick_examples(members, examples)
            rest = "".join(verbatim_li(r) for r in sorted(members, key=lambda r: r["verbatim"].lower()) if r not in ex)
            more = f"<details><summary>All {c} verbatims</summary><ul class='v'>{rest}</ul></details>" if rest else ""
            theme_cell = (
                f"<div class='tn'>{esc(t)}</div>"
                f"<div class='muted'>{c} cases &middot; {c/n*100:.1f}% of area &middot; {linked} with a Jira link in ServiceNow</div>"
            )
            verb_cell = f"<ul class='v'>{''.join(verbatim_li(r) for r in ex)}</ul>{more}"
            first = f"<td class='areacell' rowspan='{len(order)}'>{area_cell}</td>" if i == 0 else ""
            out.append(f"<tr>{first}<td class='themecell'>{theme_cell}</td><td class='verbcell'>{verb_cell}</td>"
                       f"<td>{render_jira_tree(jitems, jmap[area].get(t, {}), jdone, jblocked, jbefore, removed_count(area, t, jdone), removed_count(area, t, jblocked), removed_count(area, t, jbefore))}</td></tr>")
        out.append("</tbody></table></details>")
    out.append("</div>")

    out.append("<div class='tab' id='unmapped'>")
    out.append(
        f"<p class='meta'>{len(unmapped)} themes have service requests in this window but no Initiative, "
        "Epic or Story on the CRM Core Board (board 1091) that was created on or after 2026-01-01, is not Done, and is not Blocked, "
        "whose title matches the theme's phrases. These need new Jira items. "
        "Where matching items exist but were created before 2026-01-01, or are Done or Blocked, the counts are shown; those items are not listed. "
        "The board holds CRM - Core work only, so Jira work tracked on other boards is not visible here.</p>"
    )
    out.append("<table><thead><tr><th>Area</th><th>Theme</th><th>Cases</th><th>% of area</th>"
               "<th>With a Jira link in ServiceNow</th><th>Example verbatims (Short description, as written)</th>"
               "<th>Created before 2026-01-01 (not shown)</th>"
               "<th>Done items matched (not shown)</th><th>Blocked items matched (not shown)</th>"
               "<th>Jira status</th></tr></thead><tbody>")
    for area, t in unmapped:
        members = [r for r in by_area[area] if r["theme"] == t]
        c = len(members)
        ex = pick_examples(members, examples)
        rest = "".join(verbatim_li(r) for r in sorted(members, key=lambda r: r["verbatim"].lower()) if r not in ex)
        more = f"<details><summary>All {c} verbatims</summary><ul class='v'>{rest}</ul></details>" if rest else ""
        out.append(
            f"<tr><td>{area}</td><td>{esc(t)}</td><td class='num'>{c}</td>"
            f"<td class='num'>{c/len(by_area[area])*100:.1f}%</td>"
            f"<td class='num'>{sum(1 for r in members if r['jira'] == 'Yes')}</td>"
            f"<td><ul class='v'>{''.join(verbatim_li(r) for r in ex)}</ul>{more}</td>"
            f"<td class='num'>{removed_count(area, t, jbefore)}</td>"
            f"<td class='num'>{removed_count(area, t, jdone)}</td>"
            f"<td class='num'>{removed_count(area, t, jblocked)}</td>"
            "<td class='none'>No open mapping. Jira item needs to be created.</td></tr>"
        )
    out.append("</tbody></table></div>")
    out.extend(summary)
    if sup:
        out.extend(render_sup_tab(sup, examples))
    out.append("<div class='tab' id='cases'>")
    out.append("<input id='q' onkeyup='f()' placeholder='Filter by case, area, theme, client or text...'>")
    out.append("<table id='all'><thead><tr><th>Case</th><th>Created (UTC)</th><th>Area</th><th>Theme</th>"
               "<th>Short description (verbatim)</th><th>Client</th><th>Status</th><th>Jira</th></tr></thead><tbody>")
    for r in sorted(rows, key=lambda r: (AREAS.index(r["area"]), r["theme"], r["created"])):
        out.append(
            f"<tr><td class='case'>{r['case']}</td><td>{r['created']}</td><td>{r['area']}</td><td>{esc(r['theme'])}</td>"
            f"<td>{esc(redact(r['verbatim']))}</td><td>{esc(r['client'])}</td><td>{esc(r['status'])}</td><td>{esc(r['jira'])}</td></tr>"
        )
    out.append(f"</tbody></table></div></div><script>{JS}</script></body></html>")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", default="2026-01-01")
    ap.add_argument("--end", default="2026-08-31")
    ap.add_argument("--examples", type=int, default=6)
    ap.add_argument("--dump-unclassified", default="")
    ap.add_argument("--jira-dir", default="", help="board 1091 export; default <csv dir>/crm-board-1091")
    ap.add_argument("--sup-dir", default="", help="SUP + PHEM export; default <csv dir>/sup-2026; 'none' to skip")
    args = ap.parse_args()

    for area in AREAS:
        defined = {name for name, _ in RULES[area] if not name.startswith("Non-actionable")}
        if defined != set(JIRA_RULES[area]):
            sys.exit(f"{area}: Jira rules out of sync with themes: {sorted(defined ^ set(JIRA_RULES[area]))}")

    rows, stats = load(args.csv, args.start, args.end)
    jira_dir = Path(args.jira_dir) if args.jira_dir else Path(args.csv).resolve().parent / "crm-board-1091"
    all_items, jstats = load_items(jira_dir)
    jitems, done, blocked, before = split_done(all_items)
    hidden_before = before | keys_created_before(jira_dir)
    jstats["done"], jstats["blocked"], jstats["before"], jstats["open"] = len(done), len(blocked), len(before), len(jitems)
    before = hidden_before
    jira = {
        "items": jitems,
        "done": done,
        "blocked": blocked,
        "before": before,
        "mapped": map_items(jitems),
        "mapped_with_done": map_items(all_items),
        "stats": jstats,
        "engineering": sum(1 for it in jitems.values() if is_engineering(it)),
    }
    sup = None
    if args.sup_dir != "none":
        sup = analyse_sup(Path(args.sup_dir) if args.sup_dir else Path(args.csv).resolve().parent / "sup-2026")
    page = render(rows, stats, args.start, args.end, args.examples, jira, sup)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("jira", jstats)

    print(dict(stats), "analysed", len(rows))
    for area in AREAS:
        items = [r for r in rows if r["area"] == area]
        c = Counter(r["theme"] for r in items)
        print(f"\n== {area} ({len(items)})")
        for t, n in c.most_common():
            print(f"  {n:5d}  {t}")
    if args.dump_unclassified:
        with open(args.dump_unclassified, "w") as fh:
            for r in rows:
                if r["theme"] == UNCLASSIFIED:
                    fh.write(f"{r['area']}\t{r['case']}\t{r['verbatim']}\n")


if __name__ == "__main__":
    main()
