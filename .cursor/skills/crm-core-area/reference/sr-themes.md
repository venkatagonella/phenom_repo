# ServiceNow demand vs CRM Core Jira, by area

SR side: RX population of 4,379 service requests (Jira-created Yes or No). Source: `product-copilot-beta/knowledge/servicenow-service-requests/theme-playbook.md`, which classifies with the `rx_theme_rules.py` base and cluster_v1 rules. The "what to do" bullets there are demand signals, not roadmap.

Jira side: the open 2026 CRM Core items (see `backlog-map.md`), as of 2026-10-23.

## Hiring status / pipeline / stages / lead status

- **SRs:** 263 (6.0%). Customers report wrong or stuck hiring and lead statuses, unexplained stage moves, disposition and reject reasons, and ATS↔CRM status mismatches.
- **Jira:** 5 items. Translated hiring statuses (PHEM-2136326), status APIs moving to DAAL, separate lead and applicant spotlights, an exportable latest job stage, and agency lead counts.
- **Gap:** no Jira item addresses allowed-transition rules, explaining auto-moves, or showing automation-driven status changes. Those come from the playbook's "what to do" list.

## Jobs / requisitions / applications / posting

- **SRs:** 242 (5.5%). Customers report jobs that are missing, duplicated or not posting, applications that are stuck, internal vs external posting problems, and req ID issues.
- **Jira:** 64 items. Bulk edit, scheduled posting, private links, the job page redesign, document viewer, attachment copy, activity and audit, translated fields, RedDot, custom statuses and the application list.
- **Gap:** the playbook's asks to explain why Publish is disabled and to stop duplicate drafts have no matching Jira title.

## Forwarding / LinkedIn / ATS↔CRM sync

- **SRs:** 180 (4.1%). Customers report forwarding failures, LinkedIn export and import problems, and Workday/SuccessFactors sync gaps.
- **Jira:** 22 items. LinkedIn CRM Connect hardening and the broken pipeline, Workday job lifecycle sync with retry, role-aware ATS pull, HRM projects, IX workflow, and Indeed native apply.
- **Gap:** forward-to-HM failure messaging has no matching Jira title.

## Access / CRM not opening / permissions

- **SRs:** 141 (3.2%). Customers report that CRM won't open, missing roles, login/SSO problems, and admin access to features.
- **Jira:** 53 items. Job-level hiring-team roles (initiative PHEM-1965641), export RBAC, worker council access, departmentalization, and consent-based visibility.
- **Gap:** re-linking jobs after a user's email changes and removing deactivated users from pickers have no matching Jira title.

## Events / university recruiting

- **SRs:** 87 (2.0%). Customers report problems with event registration, campus recruiting, and event forms and invites.
- **Jira:** 0 items. This area is fully uncovered in the open 2026 CRM Core backlog. The work may sit in another pod's backlog; check before claiming it is a gap.

## How-to / configuration / enablement question

- **SRs:** 50 (1.1%). Customers ask how-to, can-we and enable-feature questions (matched on title only).
- **Jira:** 18 items. Feature flag revamp, self-service error messages, tenant notification settings, tenant centralization, and settings regrouping.
- **Gap:** guided "how do I" flows have no matching Jira title.

"No matching Jira title" means only that no title in this filter matches. It does not prove the work is absent elsewhere.
