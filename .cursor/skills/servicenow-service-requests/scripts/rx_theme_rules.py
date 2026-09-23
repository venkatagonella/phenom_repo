"""RX theme phrase rules + classifier (sheet text only).

Classification is exclusive first-match on SHORT_DESCRIPTION, then
SHORT_DESCRIPTION + DESCRIPTION. Unclassified stays unclassified unless a
high-confidence phrase rule matches.

Cluster-derived rules (added after TF-IDF clustering of unclassified RX rows)
are marked with source=cluster_v1 in RULE_META.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional, Tuple

# (theme_name, list_of_regex_patterns)
# Order matters: first match wins.

BASE_THEME_RULES: list[tuple[str, list[str]]] = [
    (
        "Automation not triggering / failing / wrongly triggered",
        [
            r"\bautomations?\b.{0,60}\b(not\s+)?(trigger|triggering|triggered|fail|failed|failing|failure|wrongly|incorrectly|broken)\b",
            r"\b(not\s+)?(trigger|triggering|triggered|fail|failed|failing)\b.{0,60}\bautomations?\b",
            r"\bautomation\s+(failed|failing|failure|issue|broken)\b",
            r"\bmultiple automations?\b",
            r"\bscreening automation\b",
            r"\bautomation\b.{0,40}\b(run history|not properly)\b",
        ],
    ),
    (
        "SMS / WhatsApp",
        [r"\bsms\b", r"\bwhatsapp\b", r"\bwhats\s*app\b"],
    ),
    (
        "Email template content / hyperlinks / branding",
        [
            r"\bemail templates?\b",
            r"\btemplates? in the crm\b",
            r"\bdefault templates?\b",
            r"\btemplates?\b.{0,60}\b(hyperlink|footer|button|color|language|placeholder|edit|editing|branding|image|from.?field)\b",
            r"\b(hyperlink|hyperlinks)\b",
            r"\breferral template\b",
            r"\bplaceholder",
        ],
    ),
    (
        "Email not sending / not receiving / spam / bounce",
        [
            r"\b(unable to send|not receiving|not being sent|not sent|go to spam|email whitelist|sender email|bounced|bounce)\b",
            r"\bemails?\b.{0,50}\b(not\s+(being\s+)?sent|not\s+receiving|unable|spam|whitelist|deliver|sender|bounc)\b",
            r"\b(not|unable).{0,30}\b(send|sending|sent|receive|receiving|deliver|delivered).{0,30}\bemails?\b",
            r"\bbulk email\b",
            r"\brejection email\b",
            r"\bapplication email\b",
            r"\bopt[- ]?in email\b",
            r"\bno-reply\b",
            r"\bunsubscribe page\b",
            r"\bcandidate messaging within phenom\b",
            r"\bnote emails?\b",
        ],
    ),
    (
        "Campaigns / job alerts / subscriptions / spotlights",
        [
            r"\bcampaigns?\b",
            r"\bjob alerts?\b",
            r"\bjobalert",
            r"\bsubscriptions?\b",
            r"\bspotlights?\b",
            r"\bdynamic list\b",
        ],
    ),
    (
        "Profile merge / unmerge / duplicates / disappeared",
        [
            r"\bunmerg",
            r"\bmerg(e|ed|ing)\b.{0,50}\b(profile|candidate|duplicate)",
            r"\b(profile|candidate).{0,50}\bmerg(e|ed|ing)\b",
            r"\bduplicate (candidate|profile|merging|feature)\b",
            r"\bcandidate disappeared\b",
            r"\bdisappeared\b",
            r"\bprofile merge\b",
            r"\bresume disappears\b",
            r"\btwo records for same candidate\b",
        ],
    ),
    (
        "Candidate profile data / fields / tags / location / GDPR",
        [
            r"\bcandidate profile\b",
            r"\bcandidate field",
            r"\breorder candidate fields\b",
            r"\bmissing employee email\b",
            r"\bcandidate email\b",
            r"\bcandidate address\b",
            r"\b(missing|incorrect|inconsistent|appearing incorrect).{0,40}\b(email|location|field|fields|city|state|data|address)\b",
            r"\blocation appearing incorrect\b",
            r"\bgdpr\b",
            r"\bprivacy view\b",
            r"\b(candidate )?purge\b",
            r"\bprofile deletion\b",
            r"\btags?\b",
            r"\btagged as\b",
            r"\bimported_from_ats\b",
            r"\bchange an email on a candidate\b",
        ],
    ),
    (
        "Hiring status / pipeline / stages / lead status",
        [
            r"\bhiring status",
            r"\blead status",
            r"\bhiring pipeline\b",
            r"\bpipeline\b",
            r"\bproject stage\b",
            r"\btransition status",
            r"\brecruiter reject\b",
            r"\bcandidate status\b",
            r"\bnext status\b",
            r"\bprogressed to the next status\b",
            r"\bstatus(es)?\b.{0,50}\b(crm|ats|inconsistent|incorrect|change|showing|rejected|declined|progress)",
        ],
    ),
    (
        "Forwarding / LinkedIn / ATS↔CRM sync",
        [
            r"\blinkedin\b",
            r"\bforward(ing)?\b.{0,40}\b(candidate|resume)\b",
            r"\bunable to forward\b",
            r"\buser not in the system\b",
            r"\bworkday\b.{0,50}\bphenom\b",
            r"\brecruiter export to phenom\b",
            r"\bhiring statuses are not consistent between ats and crm\b",
        ],
    ),
    (
        "Jobs / requisitions / applications / posting",
        [
            r"\bapplications? submitted\b",
            r"\bjob requisitions?\b",
            r"\bmy jobs\b",
            r"\bdelete jobs\b",
            r"\bremove job from crm\b",
            r"\bclosed job\b",
            r"\bjob approval\b",
            r"\bposting options\b",
            r"\binvite to apply\b",
            r"\b(jr\d{5,})",
            r"\brequisition",
            r"\bwrong req\b",
            r"\bjobs?\b.{0,40}\b(export|post|posted|posting|delete|approval|career site)\b",
            r"\bapplication(s)?\b.{0,40}\b(without resume|email|record)\b",
        ],
    ),
    (
        "Search / lists / filters / export / AI Discovery",
        [
            r"\bai discovery\b",
            r"\bexport(ing)? candidates?\b",
            r"\bexport of\b",
            r"\bread versus unread\b",
            r"\blist doesnt filter\b",
            r"\bsource candidates from crm\b",
            r"\bcreate list\b",
            r"\bprojects/lists\b",
        ],
    ),
    (
        "Access / CRM not opening / permissions",
        [
            r"\bcrm is not opening\b",
            r"\bunable to (add a candidate|access the candidate)\b",
            r"\bdoes not have access\b",
            r"\bapi key\b",
            r"\bpermission",
        ],
    ),
    (
        "Screening / interview / scheduling / offer / notifications",
        [
            r"\bscreening\b",
            r"\binterview\b",
            r"\bscheduling\b",
            r"\binterviewer\b",
            r"\bvideo screening\b",
            r"\binvite to interview\b",
            r"\btake action link\b",
            r"\boffer letter\b",
            r"\bnotifications?\b.{0,40}\b(not|missing|sent)",
            r"\bmissing notifications\b",
        ],
    ),
    (
        "Activity / notes / UI display",
        [
            r"\bactivity not showing\b",
            r"\bactivity log\b",
            r"\bfront-end not displaying\b",
            r"\bdl app\b",
            r"\blogo\b",
        ],
    ),
    (
        "Events / university recruiting",
        [
            r"\bevents?\b.{0,40}\b(crm|recruit|university|campus)",
            r"\buniversity recruit",
            r"\bcampus\b",
            r"\bevent (update|email|invite)",
        ],
    ),
]

# High-confidence rules derived from TF-IDF clusters of previously unclassified RX SRs.
# Only patterns that clearly map to an existing theme (or a new named theme with
# consistent cluster language) are included. Leave residual clusters unclassified.
CLUSTER_V1_THEME_RULES: list[tuple[str, list[str]]] = [
    (
        "Candidate profile data / fields / tags / location / GDPR",
        [
            r"\b(add|adding|update|updating|change|changing|remove|removing|rename|renaming)\b.{0,40}\b(field|fields|column|columns)\b",
            r"\bfield(s)?\b.{0,40}\b(not|missing|blank|empty|incorrect|wrong|null)\b",
            r"\b(custom field|system field|profile field)\b",
            r"\b(phone|mobile|address|location|city|state|country|zip)\b.{0,40}\b(field|profile|candidate|missing|incorrect|blank)\b",
            r"\bcandidate (data|details|information)\b",
            r"\b(pii|personal data|data subject|right to be forgotten|dsar)\b",
            r"\bdelete (the )?candidate\b",
            r"\bcandidate (record|records)\b.{0,30}\b(delete|deletion|remove)\b",
        ],
    ),
    (
        "Email not sending / not receiving / spam / bounce",
        [
            r"\bemails?\b.{0,40}\b(bounce|bouncing|bounced|undeliver|undeliverable|blocked|quarantine)\b",
            r"\b(not|never)\b.{0,20}\b(got|getting|received|receiving)\b.{0,20}\b(the )?email",
            r"\bmail(s)? (not|never) (going|going out|delivered)\b",
            r"\bdeliverability\b",
            r"\bdkim\b|\bdmarc\b|\bspf\b",
            r"\bfrom address\b",
            r"\bsender (id|address|name)\b",
        ],
    ),
    (
        "Email template content / hyperlinks / branding",
        [
            r"\b(template|templates)\b.{0,40}\b(broken|incorrect|wrong|update|edit|copy|clone|duplicate|create)\b",
            r"\b(broken|incorrect|wrong|dead)\b.{0,20}\b(link|links|url|urls)\b",
            r"\b(cta|call to action)\b",
            r"\bemail (header|footer|banner|branding|logo)\b",
            r"\b(html|body)\b.{0,30}\b(email|template)\b",
        ],
    ),
    (
        "Campaigns / job alerts / subscriptions / spotlights",
        [
            r"\b(talent pool|talentpool)\b",
            r"\b(nurture|drip)\b.{0,20}\b(campaign|email)\b",
            r"\balert(s)?\b.{0,30}\b(job|jobs|internal|employee)\b",
            r"\b(subscribe|unsubscribe|subscription)\b",
            r"\bsaved search\b",
            r"\bdynamic (audience|segment|list)\b",
        ],
    ),
    (
        "Hiring status / pipeline / stages / lead status",
        [
            r"\b(stage|stages)\b.{0,40}\b(change|changing|move|moved|moving|wrong|incorrect|stuck)\b",
            r"\b(move|moved|moving)\b.{0,30}\b(candidate|candidates)\b.{0,30}\b(stage|status|pipeline)\b",
            r"\bdisposition\b",
            r"\breject(ed|ion)?\b.{0,30}\b(status|stage|reason)\b",
            r"\boffer stage\b",
            r"\bpipeline (view|stage|stages)\b",
        ],
    ),
    (
        "Jobs / requisitions / applications / posting",
        [
            r"\b(job|jobs|req|reqs)\b.{0,40}\b(not (showing|visible|appearing|posting|posted)|missing|duplicate)\b",
            r"\b(post|posted|posting|unpost|unposted)\b.{0,30}\b(job|jobs|req|requisition)\b",
            r"\bapplication(s)?\b.{0,40}\b(stuck|incomplete|missing|not (received|showing|visible))\b",
            r"\binternal (job|jobs|posting|portal)\b",
            r"\bexternal (job|jobs|posting)\b",
            r"\breq(uisition)? (id|number|#)\b",
        ],
    ),
    (
        "Screening / interview / scheduling / offer / notifications",
        [
            r"\b(calendar|outlook|teams|zoom|meet)\b.{0,40}\b(invite|interview|scheduling|sync)\b",
            r"\b(reschedule|rescheduling|cancel(led)? interview)\b",
            r"\bpanel interview\b",
            r"\bscorecard\b",
            r"\b(self[- ]?schedule|self[- ]?scheduling)\b",
            r"\boffer (letter|approval|workflow)\b",
            r"\bquestionnaire\b",
            r"\bassessment\b",
        ],
    ),
    (
        "Search / lists / filters / export / AI Discovery",
        [
            r"\b(search|searches|searching)\b.{0,40}\b(candidate|candidates|crm|not|wrong|incorrect|empty|no result)\b",
            r"\b(filter|filters|filtering)\b.{0,40}\b(not|broken|wrong|incorrect|missing)\b",
            r"\b(boolean|keyword) search\b",
            r"\b(list|lists)\b.{0,40}\b(not|broken|empty|missing|cannot|can't|unable)\b",
            r"\bexport\b.{0,40}\b(csv|excel|candidates|list|data)\b",
            r"\bbulk (select|action|actions|edit|update)\b",
        ],
    ),
    (
        "Access / CRM not opening / permissions",
        [
            r"\b(role|roles|permission|permissions|access)\b.{0,40}\b(missing|denied|unable|cannot|can't|not|grant|remove|add)\b",
            r"\b(login|log[- ]?in|sso|okta|cannot access|can't access|unable to access)\b",
            r"\b(user|users|recruiter)\b.{0,40}\b(deactivat|activat|provision|access|permission|role)\b",
            r"\bcrm\b.{0,30}\b(down|unavailable|not (loading|opening|working)|blank|error)\b",
            r"\b(master )?admin\b.{0,30}\b(access|permission|role)\b",
        ],
    ),
    (
        "Forwarding / LinkedIn / ATS↔CRM sync",
        [
            r"\b(sync|synced|syncing|synchron)\b.{0,40}\b(ats|crm|candidate|job|application|workday|successfactor)\b",
            r"\b(ats|workday|successfactors|success factor|taleo)\b.{0,40}\b(sync|not (in|showing)|missing|crm|phenom)\b",
            r"\blinkedin (recruiter|export|import|rsc)\b",
            r"\b(import|imported|importing)\b.{0,30}\b(candidate|candidates|resume|csv)\b",
        ],
    ),
    (
        "Automation not triggering / failing / wrongly triggered",
        [
            r"\b(workflow|workflows|rule|rules)\b.{0,40}\b(not|fail|trigger|automat)\b",
            r"\bautomat(ic|ed|ion)\b.{0,40}\b(email|invite|reject|status|stage)\b",
            r"\bscheduled (job|action|automation)\b",
        ],
    ),
    (
        "Events / university recruiting",
        [
            r"\b(career fair|campus event|recruiting event|event registration)\b",
            r"\bevent\b.{0,40}\b(candidate|registration|invite|qr|check[- ]?in)\b",
            r"\buniversity\b",
            r"\bcampus recruit",
        ],
    ),
    (
        "Activity / notes / UI display",
        [
            r"\b(ui|page|screen|button|tab|modal|widget)\b.{0,40}\b(not|broken|missing|blank|incorrect|display|showing|load)\b",
            r"\b(note|notes|comment|comments)\b.{0,40}\b(not|missing|showing|display|save)\b",
            r"\b(dashboard|homepage|landing)\b.{0,30}\b(not|blank|broken|load)\b",
            r"\berror message\b",
            r"\bconsole error\b",
        ],
    ),
    # How-to: title-only patterns (see classify_theme — body boilerplate often
# contains "how can you help", which is not a how-to theme).
    (
        "How-to / configuration / enablement question",
        [
            r"^(how (do|can|to)|where (do|can|to)|what (is|does|are)|can we |can you (explain|clarify|confirm))",
            r"\b(need|requesting) (clarity|clarification|explanation|documentation|guidance)\b",
            r"\b(enable|disable|turn on|turn off|configure|configuration|setup|set up)\b.{0,40}\b(feature|setting|option|toggle)\b",
            r"\bis (it|there) (possible|a way)\b",
            r"\bbest practice\b",
            r"\bwhat is [a-z0-9]",
        ],
    ),
]

# Themes matched only against SHORT_DESCRIPTION (high-confidence title signal).
TITLE_ONLY_THEMES = frozenset(
    {
        "How-to / configuration / enablement question",
    }
)

UNCLASSIFIED = "Unclassified / other"


def all_theme_rules() -> list[tuple[str, list[str]]]:
    # Cluster rules run after base rules so exact base phrases still win;
    # cluster rules mainly catch previously unclassified residual language.
    return BASE_THEME_RULES + CLUSTER_V1_THEME_RULES


def _compile(rules: Iterable[tuple[str, list[str]]]):
    return [(name, [re.compile(p, re.I | re.S) for p in pats]) for name, pats in rules]


_COMPILED = None


def compiled_rules():
    global _COMPILED
    if _COMPILED is None:
        _COMPILED = _compile(all_theme_rules())
    return _COMPILED


def _match_rules(text: str, compiled, *, allow_title_only: bool) -> Optional[str]:
    if not text:
        return None
    for name, regs in compiled:
        if name in TITLE_ONLY_THEMES and not allow_title_only:
            continue
        for rgx in regs:
            if rgx.search(text):
                return name
    return None


def classify_theme(short_description: str, description: str = "") -> str:
    short = short_description or ""
    desc = description or ""
    compiled = compiled_rules()
    # 1) Title first (includes title-only themes)
    hit = _match_rules(short, compiled, allow_title_only=True)
    if hit:
        return hit
    # 2) Title+body for non-title-only themes
    if desc:
        hit = _match_rules(f"{short}\n{desc}", compiled, allow_title_only=False)
        if hit:
            return hit
    return UNCLASSIFIED


def classify_theme_with_source(short_description: str, description: str = "") -> Tuple[str, str]:
    """Return (theme, source) where source is base|cluster_v1|unclassified."""
    short = short_description or ""
    desc = description or ""
    base = _compile(BASE_THEME_RULES)
    cluster = _compile(CLUSTER_V1_THEME_RULES)

    hit = _match_rules(short, base, allow_title_only=True)
    if hit:
        return hit, "base"
    hit = _match_rules(short, cluster, allow_title_only=True)
    if hit:
        return hit, "cluster_v1"
    if desc:
        combined = f"{short}\n{desc}"
        hit = _match_rules(combined, base, allow_title_only=False)
        if hit:
            return hit, "base"
        hit = _match_rules(combined, cluster, allow_title_only=False)
        if hit:
            return hit, "cluster_v1"
    return UNCLASSIFIED, "unclassified"
