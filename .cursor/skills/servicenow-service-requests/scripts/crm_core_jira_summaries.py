"""Three plain-language bullets per CRM Core area: what will improve once the
open 2026 Jira items in that area ship. Written only from the titles of the
items classified into the area (see crm_core_jira_areas.py)."""

from crm_core_jira_areas_names import ACC, EVT, HOW, HS, JOB, SYNC

AREA_SUMMARIES: dict[str, list[str]] = {
    HS: [
        "Hiring statuses will show in each recruiter's language, and status updates move to the new data layer (DAAL).",
        "With Hiring Pipeline on, leads and applicants get separate spotlights, so each tab only counts its own candidates.",
        "Recruiters can export a candidate's latest job stage and see lead and applicant counts for each agency.",
    ],
    JOB: [
        "Recruiters can bulk-edit job requisitions, schedule when a job publishes or expires, and share confidential jobs through private links.",
        "The job page gets a cleaner overview and edit layout, an in-app document viewer, attachments that copy over when a job is duplicated, and a full activity and audit history.",
        "Jobs go out more completely: translated job fields reach the career site, jobs can be distributed through RedDot, custom job statuses are supported, and applications get their own searchable list.",
    ],
    SYNC: [
        "The LinkedIn CRM connection is hardened: the broken pipeline gets fixed, and LinkedIn InMail contacts become filled-in CRM profiles.",
        "Jobs sync to Workday across create, publish and unpublish, and recruiters can see each job's sync status and retry failures themselves.",
        "Other integrations get stronger too: hiring-team roles come over from SuccessFactors and Workday, HRM projects, activities and languages stay in step with CRM, and ADP, ERM and Indeed (native apply) connections improve.",
    ],
    ACC: [
        "Each job gets defined hiring-team roles (for example sourcer and associate interviewer), and the role decides what a person sees, which notifications they get and how they are set up.",
        "Admins can stop recruiters from downloading or exporting candidate data in CRM, Events and Onboarding, and can limit who creates or manages tags.",
        "Departments and special roles control visibility: worker council users can't see leads on departmentalized jobs, employee details stay hidden when consent is No, and forced logout moves from 8 to 12 hours.",
    ],
    EVT: [
        "No open 2026 CRM Core initiative, epic or story matches this area.",
        "The only events-related item (restricting event candidate and report export) is counted under Access / permissions.",
        "Events and university recruiting work is not in the CRM Core backlog selected by this filter.",
    ],
    HOW: [
        "Admins get regrouped CRM settings with search, and feature flags are reworked so features are easier to switch on per customer.",
        "Error messages become specific enough for customers to fix common problems themselves instead of raising a ticket.",
        "More setup becomes self-service: tenant-level notification settings, field management, agency bulk-upload setup, survey forms and NPS reminders, plus cleaner tenant setup and centralization.",
    ],
}
