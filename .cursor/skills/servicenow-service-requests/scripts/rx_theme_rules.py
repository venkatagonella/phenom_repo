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

# High-confidence rules from DESCRIPTION review of residual unclassified
# (filtered RX + CRM PEP playbook population). Phrase matches only — no
# force-label by similarity. Maps leftover tickets into existing themes.
CLUSTER_V2_THEME_RULES: list[tuple[str, list[str]]] = [
    (
        "Email template content / hyperlinks / branding",
        [
            r'\b("?from"?\s+field|from\s+line)\b',
            r"\b(capitalize|sentence case|punctuat)\b.{0,40}\b(from|notification|email)\b",
            r"\b(white\s*label|white[- ]?labell?ing)\b",
            r"\bemail\b.{0,40}\b(white\s*label|white[- ]?labell?ing)\b",
            r"\bedit (the )?email copy\b",
            r"\bsharing (an )?event via email\b",
        ],
    ),
    (
        "Email not sending / not receiving / spam / bounce",
        [
            r"\bwhite[- ]?list\w*\b",
            r"\bblack[- ]?list\w*\b",
            r"\b(suppression list|block(ed)? email domains?)\b",
            r"\bregister(ing)? the domain\b",
            r"\bdomain\b.{0,40}\b(register|registered|dns|send emails?|validated)\b",
            r"\b(referral|incomplete apply|privacy notification)\s+emails?\b",
            r"\bemails?\b.{0,40}\b(not triggered|dropped|didn'?t (get|receive)|did not (get|receive)|blocked|thread visibility)\b",
            r"\b(candidate|cdd)\b.{0,40}\b(didn'?t get|did not get|didn'?t receive|blocked).{0,40}\b(email|message|response)\b",
            r"\bincomplete apply reminders?\b",
            r"\bphenom email (issue|thread)\b",
            r"\binbox (errors?|not showing|feature)\b",
            r"\bsubsequent email (response|reply)\b",
        ],
    ),
    (
        "SMS / WhatsApp",
        [
            r"\bno numbers? available\b",
            r"\b(area code|phone numbers? assigned|recruiter.{0,20}phone)\b",
        ],
    ),
    (
        "Candidate profile data / fields / tags / location / GDPR",
        [
            r"\b(profile source|candidate source|traffic source|applicant traffic source)\b",
            r"\b(vertical structure|hris mapping|org structure|nested job fields)\b",
            r"\b(country of residence|country codes?|capital names|job family)\b",
            r"\b(dropdown with search|source dropdown|hiring team dropdown)\b",
            r"\b(tagged|tagging)\b.{0,30}\bfollow\b",
            r"\b(privacy (process|requests?|list|notification|dashboard)|data removal|gdpr)\b",
            r"\b(candidate not deleting|delete a candidate|removing test data|cv removal|resume parsing|bulk resume upload|malicious content.{0,20}resume)\b",
            r"\b(attachments?|documents?)\b.{0,50}\b(missing|unable to see|automatic download|associate|associating|download)\b",
            r"\b(automatic download|missing|unable to see).{0,40}\b(attachments?|documents?)\b",
            r"\bmissing documents?\b",
            r"\b(associate|associating) (documents?|docs?) (with|to) jobs?\b",
            r"\b(test candidate|mctestface|testy\.mctestface|test data)\b",
            r"\bjsq\b.{0,40}\b(fields?|answers?|pdf)\b",
            r"\b(marketing emails?|event leads?).{0,40}\bprofiles?\b",
            r"\b(former|terminated|internal) (employee|candidates?)\b",
            r"\b(employee (data feed|records?|id)|profiles? converted to employee)\b",
            r"\b(dataset ingestion|field creation|bulk field)\b",
            r"\bupdate (to )?candidate source\b",
            r"\badding a profile source\b",
            r"\bopt[- ]?in (report|status)\b",
        ],
    ),
    (
        "Profile merge / unmerge / duplicates / disappeared",
        [
            r"\bnot merging (contacts|profiles|candidates)\b",
            r"\bassociating cand(idate)? id\b",
            r"\b(cand(idate)? id|ats id).{0,40}\b(profile|reassign|associated)\b",
            r"\bduplicat(e|ing)\b.{0,30}\b(job|draft|profile|candidate)\b",
        ],
    ),
    (
        "Hiring status / pipeline / stages / lead status",
        [
            r"\b(change status|no further transitions|moved.{0,20}to (decline|reject)|auto[- ]?knockout|auto disposition)\b",
            r"\b(new applicant|lead not showing|new leads)\b",
            r"\b(status|stage).{0,40}\b(moved|change|transition|decline|review)\b",
            r"\blead to application\b",
        ],
    ),
    (
        "Jobs / requisitions / applications / posting",
        [
            r"\b(unable to close|cannot close|can'?t close|close (the )?(job|project|phenom project)|unpublish|unable to publish|publish (tab|job))\b",
            r"\bwho (closed|cancelled) (this |the )?job\b",
            r"\b(visibility to jobs|see all jobs|limit.{0,20}jobs)\b",
            r"\b(candidate not adding to job|add(ing)? a candidate.{0,20}to a job|internal application)\b",
            r"\b(jobs? are duplicating|duplicating as draft)\b",
            r"\b(apm apply|apply errors|re[- ]?applied|re applied)\b",
            r"\b(showing as external|internally publish|career (site|website))\b",
            r"\b(job duration|deactivated|internally published)\b",
            r"\bemployee referral data\b",
            r"\breferral link\b",
        ],
    ),
    (
        "Forwarding / LinkedIn / ATS↔CRM sync",
        [
            r"\b(user/recruiter sync|recruiter sync|resync|re-sync|out of date)\b",
            r"\b(hm|hiring manager).{0,30}\b(crm|portal|sync)\b",
            r"\b(missing employee|employee.{0,20}crm|hire date)\b",
            r"\b(workday|taleo|successfactors|ats).{0,50}\b(phenom|crm|resume|eligibility)\b",
            r"\bdata integrity\b.{0,40}\b(crm|apps?)\b",
            r"\bforwarding candidates\b",
        ],
    ),
    (
        "Access / CRM not opening / permissions",
        [
            r"\bcrm not available\b",
            r"\b(do not have access|does not have access|cannot close jobs|recruiters do not have access)\b",
            r"\b(deactivated users|remove deactivated)\b",
            r"\b(user name change|users? email was updated)\b",
            r"\bonly (admins?|3 reqs)\b",
        ],
    ),
    (
        "Automation not triggering / failing / wrongly triggered",
        [
            r"\bautomation (request|center|is running|running to)\b",
            r'\b"email candidate" action\b',
            r"\bemail candidate.{0,20}automation\b",
            r"\b(what automation|auto knockout|custom automation)\b",
            r"\bautomation\b.{0,40}\b(not (being )?available|not available|partial apps?)\b",
        ],
    ),
    (
        "Events / university recruiting",
        [
            r"\bevent leads?\b",
            r"\b(marketing emails?).{0,30}\bevent\b",
            r"\bsharing (an )?event\b",
            r"\bhiring event\b",
        ],
    ),
    (
        "Activity / notes / UI display",
        [
            r"\b(remove|delete|need to remove) (one )?note\b",
            r"\bnote(s)? on candidate\b",
            r"\binbox not showing messages in order\b",
            r"\b(activity|emails?) tab\b",
            r"\b(lagging|freezing|system error)\b",
        ],
    ),
    (
        "How-to / configuration / enablement question",
        [
            r"\b(raise the concern|raise and not them|product enhancement|suggestion)\b",
            r"\b(what happened here|in reference to cs\d+)\b",
            r"\b(daylight saving|timezone|time zone|impact due to)\b",
            r"\b(enable|turn on|turning on).{0,40}\b(feature|associat)",
            r"\bdepartment (repurposed|name)\b",
            r"\bupdate org structure\b",
        ],
    ),
    (
        "Search / lists / filters / export / AI Discovery",
        [
            r"\b(extract(ing)? a report|report on phenom|requesting report)\b",
            r"\b(fields? are showing as|n/a|confidential job)\b",
        ],
    ),
    (
        "Screening / interview / scheduling / offer / notifications",
        [
            r"\b(jsq|knockout|auto disposition)\b",
            r"\bproactive notifications?\b",
            r"\bstatuspage\b",
        ],
    ),
    (
        "Campaigns / job alerts / subscriptions / spotlights",
        [
            r"\bjtc\b",
            r"\bjoin the community\b",
            r"\bmarketing emails?\b.{0,40}\b(profiles?|within their profiles?)\b",
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
    # later cluster rounds catch residual DESCRIPTION language.
    return BASE_THEME_RULES + CLUSTER_V1_THEME_RULES + CLUSTER_V2_THEME_RULES


def _compile(rules: Iterable[tuple[str, list[str]]]):
    return [(name, [re.compile(p, re.I | re.S) for p in pats]) for name, pats in rules]


_COMPILED = None


def compiled_rules():
    global _COMPILED
    if _COMPILED is None:
        _COMPILED = _compile(all_theme_rules())
    return _COMPILED


def reset_compiled_rules():
    """Clear cached compiled regexes after editing rule lists."""
    global _COMPILED
    _COMPILED = None


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
    # 3) Body-only pass (DESCRIPTION often has the real ask when title is a case ref)
    if desc:
        hit = _match_rules(desc, compiled, allow_title_only=False)
        if hit:
            return hit
    return UNCLASSIFIED


def classify_theme_with_source(short_description: str, description: str = "") -> Tuple[str, str]:
    """Return (theme, source) where source is base|cluster_v1|cluster_v2|unclassified."""
    short = short_description or ""
    desc = description or ""
    layers = [
        ("base", BASE_THEME_RULES),
        ("cluster_v1", CLUSTER_V1_THEME_RULES),
        ("cluster_v2", CLUSTER_V2_THEME_RULES),
    ]

    for label, rules in layers:
        compiled = _compile(rules)
        hit = _match_rules(short, compiled, allow_title_only=True)
        if hit:
            return hit, label
    if desc:
        combined = f"{short}\n{desc}"
        for label, rules in layers:
            compiled = _compile(rules)
            hit = _match_rules(combined, compiled, allow_title_only=False)
            if hit:
                return hit, label
        for label, rules in layers:
            compiled = _compile(rules)
            hit = _match_rules(desc, compiled, allow_title_only=False)
            if hit:
                return hit, label
    return UNCLASSIFIED, "unclassified"
