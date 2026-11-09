"""Map CRM Jira items (board 1091, CRM Core Board) to the service-request themes.

Input: slice-*.json written from the board's filter, restricted to
Initiative / Epic / Story:
  project = PHEM AND "Product Experience : Product" = "CRM - Core"
and metadata-keys.json (items whose summary or description mentions metadata).
Jira is read-only; this module only reads local JSON.

Matching is title-only and non-exclusive: an item maps to every theme in an
area whose Jira phrase rules match its summary, and the matched text is kept as
evidence. A story with no direct match in an area inherits its parent epic's
themes for that area ("via epic"). Initiatives and epics never inherit.
Engineering-only items (ENGINEERING_RX on the item or its parent's title) map
only to ENGINEERING_EXEMPT themes; JIRA_EXCLUDE drops known false positives.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

JIRA_BROWSE = "https://phenompeople.atlassian.net/browse/"
SLICES = ["pre2023", "2023", "2024", "2025", "2026"]
META_RX = re.compile(r"\bmeta[\s-]?data|\bmetatdata", re.I)

AUTOMATION_NOISE = r"(?<!qa backlog )(?<!data migration )"

# Engineering-only work (tooling, observability, refactors, framework upgrades, test
# plumbing) does not address a customer-reported theme, except where the theme itself
# is technical (ENGINEERING_EXEMPT).
ENGINEERING_RX = re.compile(
    r"swagger|open ?tele?metry|jococo|jacoco|\bapm\b|sonar|checkstyle|config[- ]?jar|"
    r"config-commons|core commons|\bmfes?\b|module fed|refactor|unit test|test coverage|"
    r"rf-automation|zz test|\bsdui\b|page ?schema|list schema|build/deploy|deploy pipeline|"
    r"bitbucket|migration script|migrate (process|post process) flow|header in|"
    r"ui automation|script to automate|engineering flag|automation of the story|"
    r"utilization ?:|velocity ?:|usage report|automations metrics|slack alerts for data migration|"
    r"compare the ff|business review|\blooker\b|"
    r"graphite|signoz|kafka|mongo ?db|\bupgrade|\bcdn\b|redis|auth[- ]adapter|auth-utils|"
    r"sidecar|\bbff\b|regression test|integration testing|sanity testing|"
    r"technical documentation|cognitive complexity|garbage collector|play framework|"
    r"logger jar|shared lib|openreplay|tree ?shak|constant files|tech debt|spring boot|"
    r"\bjar\b|\bdoris\b|\bpolly\b|api gateway|\bqa automation|\bpds\b|design system",
    re.I,
)
ENGINEERING_EXEMPT = {
    "Security, compliance & data-privacy requests",
    "Performance, outages & UI errors",
}

JIRA_RULES: dict[str, dict[str, list[str]]] = {
    "CRM Core": {
        "LinkedIn integration (CRM Connect, Recommendations, sharing)": [
            r"linked ?in", r"crm connect", r"\binmail",
        ],
        "EC Trigger issues": [r"\bec trigger"],
        "Security, compliance & data-privacy requests": [
            r"fedramp", r"vulnerab", r"\bsecurity\b", r"\bsecure\b", r"\bpii\b", r"obfuscat",
            r"soc ?2", r"pen ?test", r"encrypt", r"compliance", r"sensitive data", r"\bvault\b",
            r"data privacy", r"eeo data", r"\bdpa\b",
        ],
        "Audit trail & 'who changed it' questions": [
            r"\baudit", r"job activity", r"activity (log|view|tab|timeline)", r"change history",
            r"last updated", r"\bhistory of\b", r"who (changed|created|closed|updated)",
        ],
        "Feature enablement & feature-flag requests": [
            r"feature[- ]?flag", r"\bffs?\b", r"feature enablement", r"feature version tracking",
        ],
        "Performance, outages & UI errors": [
            r"performance", r"latency", r"\bp99\b", r"load(ing)? (time|performance)", r"page load",
            r"\blcp\b", r"\bslow", r"bundle size", r"lazy load", r"outage", r"\bstabili",
            r"\b5xx\b", r"something went wrong", r"error (messages?|improvements?|handling)",
            r"self-servicing errors", r"rage clicks", r"too much time", r"crm loader", r"\bcrash",
            r"service availability",
        ],
        "Access, roles, permissions & login": [
            r"\brbac\b", r"\bcbac\b", r"permission", r"\baccess\b", r"restrict",
            r"dep(a)?r(t)?(e)?m(e)?n(a)?t(a)?li[sz]", r"worker council|works council|work council",
            r"auto-?provision", r"\blog ?in\b", r"\bsso\b", r"logout", r"authori[sz]ation",
            r"\bauthz?\b", r"user ?management", r"\blicen[sc]e", r"consent based access",
            r"\broles?\b(?!.*\b(job-level|hiring team)\b)", r"fencing",
        ],
        "Interview scheduling, calendars, evaluations & scorecards": [
            r"interview", r"calendar", r"scorecard", r"evaluation", r"intake meeting",
            r"\bmeetings?\b", r"scheduling flow", r"\bscheduler\b",
            r"scheduling dependency", r"hiring manager feedback",
        ],
        "Assessments & video screening": [
            r"assessment", r"\bvideo\b", r"screening", r"questionnaire", r"knockout",
        ],
        "Invite to Apply & Recruiter Initiated Apply": [
            r"invite to apply", r"recruiter[- ]initiated apply", r"\bria\b",
        ],
        "Offer letters & pre-onboarding": [
            r"\boffer", r"pre-?onboarding", r"preboarding", r"\be-?sign",
        ],
        "Fit Score & AI features (AI Discovery, X+, Voice Agent, Intelligent Sourcing)": [
            r"fit ?score", r"\bai\b", r"ai discovery", r"matching criteria", r"intelligent",
            r"\bx\+", r"voice agent", r"gen ?ai", r"fit criteria", r"ai recommended",
        ],
        "Agency portal": [r"\bagenc(y|ies)\b"],
        "Projects": [r"\bprojects?\b", r"hiring initiatives"],
        "Bulk upload, import, export, documents & reports": [
            r"\bbulk\b", r"\bimports?\b", r"\bexports?\b", r"\bcsv\b", r"\bupload", r"download",
            r"\breports?\b", r"attachment", r"document viewer", r"\bresumes?\b", r"extract",
        ],
        "Duplicate & merged profiles (logged under CRM Core)": [
            r"\bmerg(e|ed|ing)\b", r"unmerg", r"duplicate (candidate|profile)s?", r"dedup",
        ],
        "Email, notifications & Talent Community (logged under CRM Core)": [
            r"\bemails?\b", r"notification", r"\bnotify\b", r"talent community", r"\bsms\b",
            r"campaign", r"\binbox\b", r"slack", r"announcement",
        ],
        "Automation items (logged under CRM Core)": [
            AUTOMATION_NOISE + r"\bautomations?\b(?! stability)", r"rule engine",
            r"lifecycle automations", r"auto(matic)? job closure", r"auto assignment",
        ],
        "Events & university recruiting": [
            r"events (2025|users?|module|registration|pro)\b", r"\ball events\b", r"\bin events\b",
            r"event registration", r"career fair", r"university", r"campus",
        ],
        "Spotlights, filters, search & lists": [
            r"spotlight", r"\bfilter", r"\bsearch", r"\blists?\b", r"manage columns", r"\bcolumns\b",
            r"\bsort(ing)?\b", r"\bviews\b",
        ],
        "Tags & notes": [r"\btags?\b", r"\bnotes?\b", r"hash-?tag"],
        "Job posting, publishing, closing & career-site visibility": [
            r"\bpost(ing)? (to )?(a )?jobs?\b", r"job ?posting", r"\bposted\b", r"job board",
            r"\bunpost", r"publish", r"\bjobs?\b.{0,15}\bclos(e|ed|ing|ure)\b",
            r"\bclos(e|ed|ing|ure)\b.{0,15}\bjobs?\b", r"re-?open.{0,15}\bjobs?\b",
            r"career ?site", r"private (job|link)",
            r"confidential jobs?", r"job status", r"job statuses", r"expir", r"job bundling",
        ],
        "Job & requisition access, assignment and hiring team": [
            r"hiring team", r"job-level", r"assign(ed|ment|s)? .{0,20}\bjobs?\b",
            r"\bjobs?\b.{0,20}assign", r"job visibility", r"unassign", r"coordinator",
            r"recruiter-family roles", r"role-aware",
        ],
        "Job fields, dropdowns, locations & translations": [
            r"\bfields?\b", r"dropdown|drop-down|drop down", r"\blocations?\b", r"translat",
            r"locali[sz]", r"\blanguage", r"locales?", r"job description", r"job zone",
            r"lokalise", r"job categor",
        ],
        "Hiring status, lead/applicant pipeline & workflow": [
            r"hiring status", r"candidate status", r"application status", r"lead status",
            r"\bpipeline\b", r"hiring stages?", r"workflow stages?", r"\bstages?\b",
            r"disposition", r"\bworkflows?\b(?! automation)", r"new (leads|applicants)",
        ],
        "ATS / HRIS sync & integrations (Workday, SF, UKG, API, Chrome extension)": [
            r"workday", r"successfactors|\bsap sf\b|\bsf\b", r"\bukg\b", r"\bats\b",
            r"job ?sync", r"\bindeed\b", r"beeline", r"reddot", r"chrome extension|browser extension",
            r"job pull", r"\bhrm\b", r"\bix\b", r"naukri", r"phenom hire", r"\bhris\b", r"\bhrit\b",
            r"\badp\b", r"crm integrations?", r"integrating crm with", r"downstream data integration",
            r"integration config", r"integrated fields",
        ],
        "Job & requisition records (missing, creation, editing, discrepancies)": [
            r"job (creation|create|edit|duplicate|details?|page|data|record|entity)",
            r"create (new )?job", r"requisition", r"\breqs?\b", r"bulk edit job",
            r"positions\b", r"opportunity id",
        ],
        "Candidate profile & data (logged under CRM Core)": [
            r"candidate profile", r"\bprofiles?\b", r"candidate data", r"jobseeker data",
            r"\bemployee\b", r"preferred (first )?name", r"work experience", r"\bconsent\b",
            r"reconsent", r"candidate (additional |system )?fields?",
        ],
    },
    "Profile": {
        "Profile merge, unmerge & duplicate profiles": [
            r"\bmerg(e|ed|ing)\b", r"unmerg", r"duplicate (candidate|profile)s?", r"dedup",
        ],
        "Privacy, GDPR, deletion, purge & consent": [
            r"\bgdpr\b", r"privacy", r"\bpurg", r"delet(e|ion) (candidate|profile)", r"anonymi",
            r"\bconsent\b", r"reconsent", r"retention", r"\bdpa\b", r"eeo data",
        ],
        "Profile / traffic source & referral attribution": [
            r"(profile|candidate|project|first|traffic) source", r"source (on|of) candidate",
            r"source is being", r"system and source", r"traffic", r"\butm\b", r"\breferral",
        ],
        "Resumes, documents & resume parsing": [
            r"\bresumes?\b", r"\bcvs?\b", r"\bdocuments\b", r"attachment", r"\bpars(e|er|ing)\b",
            r"document (viewer|preview|upload|deletion|section|template|handling)",
        ],
        "Hiring status changes & mismatches": [
            r"hiring status", r"candidate status", r"application status", r"disposition",
            r"hiring stages?",
        ],
        "Employee vs. candidate classification (internal, alumni, terminated)": [
            r"\bemployees?\b", r"internal (candidate|applicant|mobility)", r"alumni",
        ],
        "Candidates, applications or data missing / not syncing with ATS": [
            r"(candidate|applicant|application)s? (data )?(sync|missing|not (showing|syncing|visible))\b",
            r"(sync|pull)(ing)? (of )?(candidates?|applicants?|applications?)\b",
            r"(candidates?|applicants?|applications?) (from|to|into) (workday|successfactors|taleo|the ats|ats|hrm)\b",
            r"not sent to (taleo|workday|successfactors|the ats|ats)\b", r"missing candidates?",
        ],
        "Candidate profile data, fields & contact details": [
            r"candidate profile", r"\bprofile\b", r"preferred (first )?name", r"jobseeker data",
            r"candidate data", r"work experience", r"contact details", r"phone", r"email address",
        ],
        "Applications & candidate-to-job association": [
            r"application (records?|viewer|creation|consent|search|-centric|centric|id)",
            r"application-centric", r"candidate-job links", r"move application", r"withdraw",
            r"job application", r"apply (form|flow)", r"application questions",
            r"candidate job association", r"assign a candidate to a job",
            r"candidates? to (a )?jobs?", r"add candidates?\b", r"leads to jobs",
        ],
        "Interview, screening & offer details on profile": [
            r"\b(interview|screening|offer|evaluation|assessment)s?\b.{0,60}\b(profile|candidate|applicant|jobseeker)",
            r"\b(profile|candidate|applicant|jobseeker).{0,60}\b(interview|screening|offer|evaluation|assessment)s?\b",
        ],
        "Forwarding candidates & hiring-manager view": [
            r"\bforward", r"share candidate profiles?", r"hiring manager (feedback|view|dashboard|review)",
            r"hrm dashboard",
        ],
        "Activity log & profile audit history": [
            r"activity (log|tab|timeline)", r"candidate activity", r"job seeker activity",
            r"\baudit.{0,40}(candidate|profile|application)", r"(candidate|profile).{0,40}\baudit",
        ],
        "Search, filters & lists": [
            r"(candidate|profile|applicant|lead|talent)s?\b.{0,40}\b(search|filter|lists?\b)",
            r"\b(search|filter|lists?\b).{0,40}(candidate|profile|applicant|lead)s?\b",
        ],
        "Access, login & user accounts": [
            r"\blog ?in\b", r"logout", r"user ?management", r"auto-?provision", r"\bsso\b",
            r"user onboarding", r"user access", r"cannot access", r"unauthori[sz]ed",
            r"(candidate|profile|lead)s?\b.{0,40}(access|visibility)",
        ],
        "Automation & Talent Community items (logged under Profile)": [
            AUTOMATION_NOISE + r"\bautomations?\b(?! stability)", r"talent community",
        ],
    },
    "Messaging": {
        "Staging / UAT: email whitelisting & test-environment messaging": [
            r"(email|domain).{0,20}white ?list", r"white ?list.{0,20}(email|domain)",
            r"\bstaging\b.*\b(email|messag)", r"\buat\b.{0,30}(email|messag|sms)",
            r"(email|messag|sms).{0,30}\buat\b", r"test emails?",
        ],
        "WhatsApp messaging": [r"what'?s ?app"],
        "SMS: sending, numbers, inbox & opt-in": [r"\bsms\b", r"text messag", r"twilio"],
        "Template placeholders & tokens not resolving": [
            r"placeholders? for messaging templates", r"entities & placeholders", r"template tokens?",
            r"(email|messag|sms)\w* (template )?(placeholders?|tokens?)",
        ],
        "Job alerts, subscriptions, Talent Community & incomplete-apply reminders": [
            r"job ?alerts?", r"subscri", r"talent community", r"incomplete apply", r"unsubscribe",
        ],
        "Email campaigns & drip / always-on campaigns": [r"campaign", r"\bdrip\b", r"always[- ]on"],
        "Recruiter / hiring-manager system notifications": [
            r"notification", r"\bnotify\b", r"reminder", r"\bslack\b", r"teams notifications",
            r"inactivity emails", r"announcement email",
        ],
        "Recruiter inbox & candidate replies (Phenom / Outlook)": [
            r"\binbox\b", r"\brepl(y|ies)\b", r"outlook",
        ],
        "Email deliverability: not received, bounced, spam, blocked, suppressed": [
            r"deliverab", r"bounce", r"\bspam\b", r"(email|sms|messag)\w*.{0,30}suppress",
            r"suppress\w*.{0,30}(email|sms|messag)", r"sendgrid", r"\bdkim\b",
        ],
        "Candidate system emails not sending or wrong (apply thank-you, confirmation, rejection, referral)": [
            r"thank[- ]you (email|message)", r"confirmation (email|message)", r"rejection (email|message)",
            r"system emails?", r"apply emails?",
        ],
        "Screening & interview invitation emails": [
            r"(screening|interview) (invite|invitation|email)s?", r"invite to (screen|interview)",
        ],
        "Email templates: branding, footer, links, editing & default templates": [
            r"(email|message|messaging|communication|mail) templates?", r"templates? (for|in) (email|messag)",
            r"email (branding|footer|signature)",
        ],
        "Messaging automations not triggering": [
            r"(email|messag|sms).{0,40}automation", r"automation.{0,40}(email|messag|sms)",
        ],
        "Opt-in, opt-out & consent": [
            r"\bopt[- ]?(in|out)\b",
            r"(email|sms|messag|communication|marketing|whatsapp|text).{0,30}consent",
            r"consent.{0,30}(email|sms|messag|communication|marketing|whatsapp)",
        ],
        "1:1 email sending & email activity visibility": [
            r"\b1:1\b", r"send(ing)? emails?", r"email activity", r"emails? (on|in) (the )?(candidate|profile)",
            r"inbox conversations to the candidate profile", r"emails and notes",
        ],
        "Access, roles & permissions": [
            r"(messag|email|notification).{0,40}(roles?|permission|access|scope)",
            r"(roles?|permission|access|scope).{0,40}(messag|email|notification)",
        ],
        "Lists (static & dynamic)": [r"(static|dynamic) lists?", r"\brx lists\b"],
        "Event communications": [
            r"\bevents?\b.{0,30}(email|communication|message)",
            r"(email|communication)s?\b.{0,30}\bevents?\b",
        ],
        "Messaging reporting & analytics": [
            r"(email|messag|campaign|sms).{0,40}(report|analytic|metric)",
            r"(report|analytic|metric).{0,40}(email|messag|campaign|sms)",
        ],
    },
    "Automations": {
        "Run history, audit log & trigger-count visibility": [
            r"automation.{0,40}(history|audit|logs?\b|\bcounts?\b)", r"run history", r"policy execution",
        ],
        "Export, bulk upload & candidate data": [
            r"automation.{0,40}(export|bulk|import)", r"(export|bulk|import).{0,40}automation",
        ],
        "Wrong, duplicate or unexpected automation actions": [
            r"automation.{0,40}(duplicate|wrong|incorrect|twice|unexpected)",
        ],
        "Automation not triggering / failing": [
            r"automation.{0,40}(fail|not trigger|not working|error|retry|retrigger)",
        ],
        "Screening, interview & Voice Agent automations": [
            r"(automation|automated|auto[- ]assign\w*|automatic assignment).{0,40}(screen|interview|knockout)",
            r"(screen|interview).{0,40}automation", r"voice agent",
        ],
        "Automation setup, configuration questions & feature requests": [
            AUTOMATION_NOISE + r"\bautomations?\b(?! stability)", r"rule engine", r"recipe",
            r"workflow automation", r"auto(matic)? job closure", r"automated population",
        ],
        "Hiring status & stage movement": [
            r"automat.{0,60}(hiring status|\bstages?\b)", r"(hiring status|\bstages?\b).{0,60}automat",
        ],
        "Automated email / template content": [
            r"automat.{0,40}(email|template|notification|message)", r"inactivity emails",
        ],
        "Access, environments & ATS/HRM sync": [
            r"automation.{0,40}(access|staging|sync|hrm)", r"(access|staging|sync|hrm).{0,40}automation",
        ],
        "Jobs, offers, events & other records (logged under Automations)": [
            r"automations? (from|for|on) (the )?(jobs?|job details|offers?|events?|projects?)\b",
            r"(jobs?|offers?|events?|projects?|tags?|notes?) (from|via|by) automations?\b",
            r"automation \| leads added to jobs", r"job lifecycle automations",
            r"auto(matic)? job closure", r"unposting automation",
        ],
    },
}

JIRA_EXCLUDE: dict[str, dict[str, str]] = {
    "CRM Core": {
        "Access, roles, permissions & login": (
            r"\biam role|aws access|looker access|access for crm in qa|s3 access|access keys|"
            r"write access|ease of access|quick access|naming restriction|restriction for character"
        ),
        "Fit Score & AI features (AI Discovery, X+, Voice Agent, Intelligent Sourcing)": r"concert ai",
        "Audit trail & 'who changed it' questions": r"partner enablement|second cluster",
        "Hiring status, lead/applicant pipeline & workflow": (
            r"project|stage (urls?|in url|environments?|and prod)|\bstage \d|home ?page"
        ),
        "ATS / HRIS sync & integrations (Workday, SF, UKG, API, Chrome extension)": r"linked ?in",
        "Spotlights, filters, search & lists": r"\blist of\b",
        "Job fields, dropdowns, locations & translations": (
            r"^(?!.*\bjobs?\b).*\b(candidate|employee)\b.*\bfields?\b|event registration"
        ),
        "Candidate profile & data (logged under CRM Core)": (
            r"user profile|ai profiles|customer commits|metrics|job profile"
        ),
    },
    "Profile": {
        "Candidates, applications or data missing / not syncing with ATS": r"linked ?in",
        "Candidate profile data, fields & contact details": (
            r"user profile|ai profiles|customer commits|metrics|job profile"
        ),
        "Interview, screening & offer details on profile": r"unpost",
        "Activity log & profile audit history": r"job fields",
    },
    "Messaging": {
        "Event communications": r"events are raised",
        "Job alerts, subscriptions, Talent Community & incomplete-apply reminders": r"onpush|leads to jobs",
    },
}

_COMPILED = {
    area: [(t, [re.compile(p, re.I) for p in pats]) for t, pats in rules.items()]
    for area, rules in JIRA_RULES.items()
}


def is_engineering(item: dict) -> bool:
    return bool(ENGINEERING_RX.search(item["summary"]) or ENGINEERING_RX.search(item.get("parent_summary") or ""))


def theme_allows(area: str, theme: str, item: dict) -> bool:
    if theme not in ENGINEERING_EXEMPT and is_engineering(item):
        return False
    ex = JIRA_EXCLUDE.get(area, {}).get(theme)
    return not (ex and re.search(ex, item["summary"], re.I))


def load_items(data_dir: Path) -> tuple[dict[str, dict], dict]:
    items: dict[str, dict] = {}
    for s in SLICES:
        for it in json.loads((data_dir / f"slice-{s}.json").read_text())["issues"]:
            items[it["key"]] = it
    meta = json.loads((data_dir / "metadata-keys.json").read_text())
    meta_keys = {m["key"] for m in meta["items"]}
    title_hits = {k for k in meta_keys if k in items and META_RX.search(items[k]["summary"])}
    excluded = set(meta_keys)
    children = defaultdict(list)
    for k, it in items.items():
        if it.get("parent"):
            children[it["parent"]].append(k)
    stack = list(title_hits)
    while stack:
        k = stack.pop()
        for c in children.get(k, []):
            if c not in excluded:
                excluded.add(c)
                stack.append(c)
    kept = {k: v for k, v in items.items() if k not in excluded}
    stats = {
        "fetched": len(items),
        "metadata_matches": len(meta_keys),
        "metadata_title_matches": len(title_hits),
        "excluded": len(excluded & set(items)),
        "kept": len(kept),
    }
    return kept, stats


CREATED_FROM = "2026-01-01"


def created_before(item: dict, cutoff: str = CREATED_FROM) -> bool:
    return (item.get("created") or "")[:10] < cutoff


def keys_created_before(data_dir: Path, cutoff: str = CREATED_FROM) -> set[str]:
    """Every board item created before the cutoff, including metadata-excluded ones."""
    keys = set()
    for s in SLICES:
        for it in json.loads((data_dir / f"slice-{s}.json").read_text())["issues"]:
            if created_before(it, cutoff):
                keys.add(it["key"])
    return keys


def split_done(items: dict[str, dict]) -> tuple[dict[str, dict], set[str], set[str], set[str]]:
    """Drop Done, Blocked, and items created before 2026-01-01.

    Returns (kept, done keys, blocked keys, created-before keys).
    """
    done = {k for k, it in items.items() if it["statusCategory"] == "Done"}
    blocked = {k for k, it in items.items() if (it.get("status") or "").lower() == "blocked"}
    before = {k for k, it in items.items() if created_before(it)}
    removed = done | blocked | before
    return {k: v for k, v in items.items() if k not in removed}, done, blocked, before


def direct_matches(area: str, item: dict) -> dict[str, str]:
    hits = {}
    for theme, pats in _COMPILED[area]:
        if not theme_allows(area, theme, item):
            continue
        for p in pats:
            m = p.search(item["summary"])
            if m:
                hits[theme] = m.group(0).strip()
                break
    return hits


def map_items(items: dict[str, dict]) -> dict[str, dict[str, dict[str, dict]]]:
    """Return {area: {theme: {key: {"how": "direct"|"via epic", "evidence": str}}}}."""
    out: dict[str, dict[str, dict[str, dict]]] = {a: defaultdict(dict) for a in JIRA_RULES}
    direct: dict[str, dict[str, dict[str, str]]] = {a: {} for a in JIRA_RULES}
    for area in JIRA_RULES:
        for k, it in items.items():
            hits = direct_matches(area, it)
            if hits:
                direct[area][k] = hits
                for t, ev in hits.items():
                    out[area][t][k] = {"how": "direct", "evidence": ev}
        for k, it in items.items():
            if it["type"] != "Story" or k in direct[area]:
                continue
            p = it.get("parent")
            if p in items and items[p]["type"] == "Epic" and p in direct[area]:
                for t in direct[area][p]:
                    if theme_allows(area, t, it):
                        out[area][t][k] = {"how": "via epic", "evidence": items[p]["summary"]}
    return out


def build_tree(
    items: dict[str, dict],
    mapped: dict[str, dict],
    hidden_done: set[str] = frozenset(),
    hidden_blocked: set[str] = frozenset(),
    hidden_before: set[str] = frozenset(),
    outside_label: str = "Initiative not visible (epic is not on the CRM Core Board)",
) -> list[dict]:
    """Group mapped items as Initiative -> Epic -> Story, adding unmapped ancestors as context.

    Ancestors removed from `items` (created before 2026-01-01, Blocked, or Done) are a generic label, not a key.
    """
    inits: dict[str, dict] = {}

    def hidden_pair(key: str) -> tuple[tuple[str, str], tuple[str, str]] | None:
        if key in hidden_before:
            return (("_before", "Parent initiative was created before 2026-01-01 (not shown)"),
                    ("_before", "Parent epic was created before 2026-01-01 (not shown)"))
        if key in hidden_blocked:
            return (("_blocked", "Parent initiative is Blocked (not shown)"),
                    ("_blocked", "Parent epic is Blocked (not shown)"))
        if key in hidden_done:
            return (("_done", "Parent initiative is Done (not shown)"),
                    ("_done", "Parent epic is Done (not shown)"))
        return None

    def init_node(key, summary, status, on_board):
        if key not in inits:
            inits[key] = {"key": key, "summary": summary, "status": status, "on_board": on_board,
                          "mapped": mapped.get(key), "epics": {}, "stories": []}
        return inits[key]

    def epic_node(parent_init, key, summary, status, on_board):
        eps = parent_init["epics"]
        if key not in eps:
            eps[key] = {"key": key, "summary": summary, "status": status, "on_board": on_board,
                        "mapped": mapped.get(key), "stories": []}
        return eps[key]

    def resolve_epic(epic_key, fallback_summary):
        if epic_key in items:
            e = items[epic_key]
            ip = e.get("parent")
            if ip:
                if ip in items:
                    i = items[ip]
                    inode = init_node(ip, i["summary"], i["statusCategory"], True)
                elif (pair := hidden_pair(ip)):
                    inode = init_node(*pair[0], None, True)
                else:
                    inode = init_node(ip, e.get("parent_summary") or "", None, False)
            else:
                inode = init_node("_none", "No parent initiative", None, True)
            return epic_node(inode, epic_key, e["summary"], e["statusCategory"], True)
        if (pair := hidden_pair(epic_key)):
            return epic_node(init_node(*pair[0], None, True), *pair[1], None, True)
        inode = init_node("_unknown", outside_label, None, False)
        return epic_node(inode, epic_key, fallback_summary or "", None, False)

    for k in mapped:
        it = items[k]
        t = it["type"]
        if t == "Initiative":
            init_node(k, it["summary"], it["statusCategory"], True)
        elif t == "Epic":
            resolve_epic(k, it["summary"])
        else:
            p = it.get("parent")
            if p and (it.get("parent_type") == "Epic" or (p in items and items[p]["type"] == "Epic")):
                resolve_epic(p, it.get("parent_summary"))["stories"].append(k)
            elif p and (it.get("parent_type") == "Initiative" or (p in items and items[p]["type"] == "Initiative")):
                if p in items:
                    inode = init_node(p, items[p]["summary"], items[p]["statusCategory"], True)
                elif (pair := hidden_pair(p)):
                    inode = init_node(*pair[0], None, True)
                else:
                    inode = init_node(p, it.get("parent_summary") or "", None, False)
                inode["stories"].append(k)
            else:
                inode = init_node("_none", "No parent initiative", None, True)
                epic_node(inode, "_none", "No parent epic", None, True)["stories"].append(k)

    def weight(node):
        return (1 if node.get("mapped") else 0) + len(node.get("stories", [])) + sum(
            weight(e) for e in node.get("epics", {}).values())

    ordered = sorted(inits.values(), key=lambda n: (n["key"].startswith("_"), -weight(n)))
    for n in ordered:
        n["epics"] = sorted(n["epics"].values(), key=lambda e: (e["key"].startswith("_"), -weight(e)))
    return ordered
