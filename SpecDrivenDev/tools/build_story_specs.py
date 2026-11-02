#!/usr/bin/env python3
"""
build_story_specs.py — Publish plain-language functional specs to Google Docs.

Each of the 6 PHEM-2109151 themes becomes one Google Doc with:
  - Background: a short, plain explanation of the customer problem.
  - How It Works: a simple step-by-step workflow (where one exists).
  - User Stories: each in the Phenom Jira-ready story template
    (User Story / Acceptance Criteria as Scenario + Given/When/Then /
     Considerations: 1. Localization, 2. Analytics / Data Storage).

Content is written for humans (no placeholders / "random words to fill in") and is
grounded in: PHEM-2109151, ASRM-1570, CUSP-5947, ASRM-1477, and the Allianz
"Support Recruiter" reference doc.

The doc body text lives in this file (DOC_MD). No markdown files are written.

Usage
-----
    python3 tools/build_story_specs.py            # DRY RUN: parse + report only
    python3 tools/build_story_specs.py --apply    # update the 6 existing docs in place
    python3 tools/build_story_specs.py --apply --only role-aware-notifications
    python3 tools/build_story_specs.py --apply --create   # make NEW docs instead

Requirements: ~/.copilot/tokens.json with `google` + top-level `backend_jwt`
(the Google/copilot MCP connected). Docs scope for edit; Drive scope for the
optional folder move (skipped with a note if missing).
"""
import json, os, sys, time, urllib.request, urllib.error

TOKENS = os.path.expanduser("~/.copilot/tokens.json")
BACKEND = "https://product-copilot-backend-iarivxijkq-uc.a.run.app"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_ID = "12y7JmKa0uNhO7Glbc8Q_GLrGaCwoOne-"

DRY = "--apply" not in sys.argv
CREATE = "--create" in sys.argv
ONLY = None
if "--only" in sys.argv:
    i = sys.argv.index("--only")
    if i + 1 < len(sys.argv):
        ONLY = sys.argv[i + 1]

TITLES = {
    "recruiter-roles-data-model":    "Functional Spec - 1. Recruiter-Family Role Data Model, Registry, Migration & Feature Flag - PHEM-2109151",
    "hiring-team-role-assignment":   "Functional Spec - 2. Hiring Team Role Assignment & ATS Role Mapping - PHEM-2109151",
    "role-aware-notifications":      "Functional Spec - 3. Role-Aware Notification Framework - PHEM-2109151",
    "my-jobs-role-filtering":        "Functional Spec - 4. My Jobs Role Filtering, Spotlights & Workspace Views - PHEM-2109151",
    "per-role-analytics":            "Functional Spec - 5. Per-Role Analytics, CRM Events & Report Builder - PHEM-2109151",
    "role-aware-automation-recipes": "Functional Spec - 6. Role-Aware CRM Automation Recipes - PHEM-2109151",
}

UPDATE_IDS = {
    "recruiter-roles-data-model":    "13MyVk8NywDj8GI4TQIloE3dK5CuPMfCrGZdMORTirsM",
    "hiring-team-role-assignment":   "1iWkK6ngNsyxKC-Ehn35NTZKsjANezcNNPEkhT6Zvszw",
    "role-aware-notifications":      "14F8PursKnzFl2-VxzQ0y-7KAUglsdiDHClC6lohNi54",
    "my-jobs-role-filtering":        "1yWT0ZZXxexoR9eYjAFBSBmpgH_SoUg7r-jzm9-GSj1A",
    "per-role-analytics":            "18IkcgFGC9KqfIKgrknybORXxdKInfweZ1jUGYqOk_A0",
    "role-aware-automation-recipes": "1pUTGOIGHzSU0g4qydeeFkajzG53p8PKRpN3m_3byloU",
}

# ---------------------------------------------------------------------------
# Doc bodies (markdown). Headings: "# " H1, "## " H2; "- " bullets; other = text.
# ---------------------------------------------------------------------------
DOC_MD = {

"recruiter-roles-data-model": """# Background

Today in the Phenom CRM, everyone on a job's hiring team has the same role: "Recruiter." There is no way to tell the lead recruiter apart from the people helping out. Allianz hit this directly — they added all of their SuccessFactors recruiters into the CRM, and because everyone looks the same, the system can't route notifications, filter jobs, or report on who actually did the work (ASRM-1570, CUSP-5947).

This spec is the foundation that fixes that: it lets the CRM store a small set of clear job roles — Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator — and remember how each person got their role and for how long. It is built so more roles (and a future "view vs. act" access level, like SuccessFactors' Rec_View / Rec_Action) can be added later without rebuilding the data (ASRM-1477).

# How It Works

- Step 1: A job is created in the CRM, or pulled in from the ATS (SuccessFactors / Workday).
- Step 2: Each hiring-team member is given a job role: Primary Recruiter, Secondary Recruiter, Sourcer, or Coordinator.
- Step 3: The CRM saves the role, how it was set (from the ATS or by hand), and the dates the person held it.
- Step 4: A per-customer switch ("expanded roles") turns this on. When it is off, the customer keeps today's single-recruiter behavior with no change.

# User Stories

## Story 1: A clear list of recruiter roles
User Story:
As a CRM product owner, I want a defined list of job-level recruiter roles (Primary Recruiter, Secondary Recruiter, Sourcer, Coordinator) so that the team can tell the lead recruiter apart from supporting members on a job.
Acceptance Criteria:
Scenario: The four roles are available
Given: a customer has expanded roles turned on
When: someone assigns roles on a job
Then: Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator are all available to choose
Scenario: Room to grow later
Given: the role list
When: a new role needs to be added in the future
Then: it can be added without changing the data model or migrating existing data
Considerations:
1. Localization
Role names appear in the CRM, so they must be translatable into the 13+ languages Phenom supports.
2. Analytics / Data Storage
Each role is stored with a stable ID and whether it is a "leading" role (Primary Recruiter) or a "supporting" role (the other three). This ID is what later lets analytics report activity by role.

## Story 2: Remember each person's role and how they got it
User Story:
As a CRM engineer, I want each hiring-team member's record to store their role and how it was assigned (from the ATS or by hand) so that the rest of the product can act on the role reliably.
Acceptance Criteria:
Scenario: Role and source are saved
Given: expanded roles are on
When: a person is added to a job's hiring team
Then: the CRM saves their role and marks whether it came from the ATS or was set manually
Scenario: Nothing breaks for existing customers
Given: a customer who has not turned this on
When: their jobs are read
Then: the old single-recruiter behavior works exactly as before
Considerations:
1. Localization
No new customer-facing text in this story; role names shown elsewhere stay translatable.
2. Analytics / Data Storage
The role and its source are saved on the membership record alongside the existing fields, so nothing is lost and old data still works.

## Story 3: Keep a history of who held which role and when
User Story:
As an analyst, I want the CRM to remember who held which role on a job and during what dates so that reports stay accurate even when the team changes mid-hire.
Acceptance Criteria:
Scenario: Changes are recorded
Given: expanded roles are on
When: a person is added, changed, or removed from a role
Then: the CRM records the role, the person, and the start/end dates
Scenario: Reports use the role held at the time
Given: a member changed roles part-way through a job
When: an analyst runs a report over a date range
Then: each activity is credited to the role that person held at the time it happened
Considerations:
1. Localization
No customer-facing text in this story.
2. Analytics / Data Storage
Role history is kept as an add-only record (it is never overwritten) and stored long enough to support reporting — this is required for accurate per-role analytics (Disney).

## Story 4: Leave room for "view vs. act" access (design only)
User Story:
As a platform architect, I want the role model to be able to carry an access level later (for example, view-only vs. full-action, like SuccessFactors' Rec_View and Rec_Action) so that a future phase can restrict actions without a data migration.
Acceptance Criteria:
Scenario: The structure exists but does nothing yet
Given: expanded roles are on
When: a role is defined
Then: the model can hold view/action access settings, but Phase 1 applies no restrictions
Scenario: No behavior change in Phase 1
Given: any role
When: a person works on a job
Then: nothing they can do today is blocked in Phase 1
Considerations:
1. Localization
No customer-facing text in this story.
2. Analytics / Data Storage
The access-level structure is saved but inactive; no permission decisions are recorded in Phase 1.

## Story 5: Turn it on safely, one customer at a time
User Story:
As a Platform Config admin, I want to switch expanded roles on per customer so that customers who are ready get the new roles and everyone else is untouched.
Acceptance Criteria:
Scenario: Off by default
Given: a customer who is not enabled
When: their hiring-team data is read
Then: today's single-recruiter behavior applies with no change
Scenario: On, and forward-only
Given: a customer is enabled
When: the switch is on
Then: the expanded roles are active, and this is treated as a one-way change (no supported rollback to the old model)
Considerations:
1. Localization
No customer-facing text in this story.
2. Analytics / Data Storage
The on/off state is stored per customer; the old role/source fields are preserved so nothing is destroyed. A re-pull of jobs can fill in Primary vs. Secondary, so a separate backfill is usually not needed.
""",

"hiring-team-role-assignment": """# Background

People need a simple way to set and see who is the Primary recruiter versus a Secondary recruiter on a job. Good news: for Allianz (SuccessFactors) and Disney (Workday), the ATS already separates the lead recruiter from the "additional recruiting team members," so the CRM can read that split automatically when it pulls a job. Sourcer and Coordinator have no ATS equivalent yet, so they are set by hand. If the ATS doesn't say who the primary is, the CRM needs a sensible default (for example, the first recruiter listed) (ASRM-1570, CUSP-5947).

# How It Works

- Step 1: A job is pulled from the ATS. The CRM maps the ATS lead recruiter to Primary Recruiter and the additional recruiting team members to Secondary Recruiter.
- Step 2: If the ATS doesn't mark a primary, the CRM makes the first recruiter listed the Primary Recruiter (to be confirmed with the team).
- Step 3: On the job's Hiring Team, the Primary Recruiter or an admin can add or change Secondary Recruiter, Sourcer, and Coordinator by hand.
- Step 4: Each member shows their role and a small tag for how it was set (from the ATS or manually).
- Step 5: Customers with no ATS feed set every role by hand while creating the job.

# User Stories

## Story 1: See who holds which role on the job
User Story:
As a recruiter, I want the Hiring Team area on the Job Details page to show each member's role and how it was set so that I can see at a glance who the lead and supporting recruiters are.
Acceptance Criteria:
Scenario: Roles and source are visible
Given: expanded roles are on
When: I open the Hiring Team area on a job
Then: each member shows their role and a tag showing it came from the ATS or was set by hand
Scenario: Unchanged for non-enabled customers
Given: a customer who has not turned this on
When: I open the Hiring Team area
Then: I see today's recruiter list, unchanged
Considerations:
1. Localization
Role names and the "from ATS / manual" tag are shown to users and must be translated into the 13+ supported languages.
2. Analytics / Data Storage
This screen only reads the role and source already stored on each member; it adds no new data.

## Story 2: Assign and change supporting roles by hand
User Story:
As a Primary Recruiter or admin, I want to assign and change the Secondary Recruiter, Sourcer, and Coordinator on a job so that everyone helping is recorded in their real role (this is Disney's flow for both Workday and CRM jobs).
Acceptance Criteria:
Scenario: Add a supporting recruiter
Given: expanded roles are on and I am the Primary Recruiter
When: I add a colleague as Sourcer
Then: they appear as Sourcer with a "manual" tag and the change is saved with its date
Scenario: Change someone's role
Given: an existing member
When: I change them from Coordinator to Secondary Recruiter
Then: the new role applies and the old one is closed off in the role history
Considerations:
1. Localization
The assignment screens (role pickers, confirmations) must be translated into the 13+ supported languages.
2. Analytics / Data Storage
Each change is saved with the role, "manual" as the source, and the date, and is sent on as a per-role activity event for reporting.

## Story 3: Set roles while creating a job (no-ATS customers)
User Story:
As a recruiter at a customer with no ATS feed, I want to assign all four roles while creating a job in the CRM so that the Hiring Team area is a complete way to set up the team by hand.
Acceptance Criteria:
Scenario: Assign during creation
Given: expanded roles are on and the customer has no ATS feed
When: I create a job
Then: I can assign Primary Recruiter, Secondary Recruiter, Sourcer, and Coordinator during creation and afterwards
Scenario: All four roles work by hand
Given: Sourcer and Coordinator never come from the ATS
When: I assign them
Then: manual assignment works for all four roles from day one
Considerations:
1. Localization
The job-creation Hiring Team screens must be translated into the 13+ supported languages.
2. Analytics / Data Storage
Manual assignments are saved with "manual" as the source and sent on as per-role activity events.

## Story 4: Read Primary vs. Secondary from the ATS on job pull
User Story:
As an integrations engineer, I want the job pull to map the ATS lead recruiter to Primary Recruiter and the additional recruiting team to Secondary Recruiter for SuccessFactors (Allianz) and Workday (Disney) so that primary and secondary are set automatically wherever the ATS already separates them.
Acceptance Criteria:
Scenario: Map the ATS team
Given: the existing job pull with expanded roles on
When: a job is pulled
Then: the ATS lead recruiter becomes Primary Recruiter and additional recruiting team members become Secondary Recruiter
Scenario: Default the primary if missing
Given: a pulled job where the ATS does not mark a primary
When: the job is mapped
Then: the first recruiter listed is made Primary Recruiter (to be confirmed), and Sourcer/Coordinator are not set from the ATS
Considerations:
1. Localization
No customer-facing text in this story (integration logic only).
2. Analytics / Data Storage
ATS-set assignments are saved with "from ATS" as the source; the per-customer mapping is stored so it can be turned on for Allianz and Disney.
""",

"role-aware-notifications": """# Background

Right now, every recruiter on a job gets every notification, and someone who holds two roles on the same job can get the same alert twice. This is exactly Allianz's complaint: because everyone is just "Recruiter," all of them are notified when, say, a screening is completed (ASRM-1570, CUSP-5947, SUP-107507).

Allianz wants two things: alerts should go to the Primary recruiter only, and a Support (Secondary) recruiter should be able to choose which extra alerts they get for the jobs they support — on top of the alerts for jobs they personally lead. Their reference doc also asks that some alerts that don't exist today be added (for example, when a Hiring Manager submits a screening evaluation). And a person with more than one role on a job should get exactly one alert, never a duplicate.

# How It Works

- Step 1: Something happens on a job (for example, a screening is completed).
- Step 2: The CRM checks each recipient's role on that job.
- Step 3: It applies the notification settings for that role — Primary gets the full set; Support gets the smaller set they chose or were given.
- Step 4: If a person holds more than one role on the job, the CRM uses the most generous setting and sends just one alert.
- Step 5: If the alert is turned off for all of that person's roles, nothing is sent.

# User Stories

## Story 1: Set notifications per job role
User Story:
As a recruiting admin, I want notifications to be set per job role (on or off) so that the Primary recruiter and supporting recruiters can receive different alerts.
Acceptance Criteria:
Scenario: Different setting per role
Given: expanded roles are on
When: an alert is set to On for Primary Recruiter and Off for Secondary Recruiter
Then: the setting is saved separately for each role
Scenario: Cover the missing alerts too
Given: an alert that does not exist today (for example, "Hiring Manager submitted a screening evaluation")
When: notification options are set up
Then: that alert is available to select, as Allianz requested
Considerations:
1. Localization
Notification text shown to users must be translated into the 13+ supported languages.
2. Analytics / Data Storage
The per-role notification settings are saved in the notification system; the design also leaves room for a future "digest" option without a data change.

## Story 2: Send to the Primary recruiter only
User Story:
As a Primary recruiter, I want certain alerts to come to me only so that supporting recruiters are not flooded with notifications they don't need.
Acceptance Criteria:
Scenario: Primary only
Given: an alert set to On for Primary Recruiter and Off for supporting roles
When: the alert fires on a job
Then: only the Primary recruiter is notified
Scenario: Right role per job
Given: a person who is Primary on one job and Secondary on another
When: an alert fires on each
Then: each notification follows the role that person holds on that specific job
Considerations:
1. Localization
Delivered notification text stays translated into the 13+ supported languages.
2. Analytics / Data Storage
Routing reads the job roles set in the foundation spec; what was sent is logged so we can confirm the behavior.

## Story 3: Support recruiters choose their extra alerts
User Story:
As a Support (Secondary) recruiter, I want to choose which alerts I get for the jobs I support so that I stay informed on those jobs without losing the alerts for the jobs I personally lead.
Acceptance Criteria:
Scenario: Separate selection for supported jobs
Given: I am a Secondary recruiter on some jobs
When: I open my notification settings
Then: I can pick the alerts I want for jobs I support, in addition to my Primary-role alerts
Scenario: Defaults are sensible
Given: I have not changed anything
When: alerts fire on jobs I support
Then: I receive a sensible default set, not every alert
Considerations:
1. Localization
The notification settings screen and options must be translated into the 13+ supported languages.
2. Analytics / Data Storage
Each person's choices and the per-role default sets are saved; the exact default list per role is still being finalized with the customer.

## Story 4: One alert per event, even with multiple roles
User Story:
As a recruiter who holds more than one role on a job, I want to get exactly one alert per event so that I am never notified twice for the same thing.
Acceptance Criteria:
Scenario: No duplicates
Given: I am both Primary Recruiter and Coordinator on a job
When: an alert fires that both roles would receive
Then: I get exactly one notification
Scenario: Most generous setting wins, and silence means silence
Given: an alert is On for one of my roles and Off for another
When: it fires
Then: I receive it (On wins); and if it is Off for all my roles, I get nothing and no error
Considerations:
1. Localization
No new customer-facing text in this story.
2. Analytics / Data Storage
The de-duplication decision is logged so we can prove there are zero duplicates for multi-role users (this resolves SUP-107507).

## Story 5: Don't break what works today
User Story:
As an existing customer, I want my current notification settings to keep working so that turning on roles introduces no surprises.
Acceptance Criteria:
Scenario: Existing settings kept
Given: a customer with custom notification settings set up through Phenom support
When: role-aware notifications ship
Then: those settings still work, unchanged
Scenario: Off means no change
Given: a customer who has not turned this on
When: alerts fire
Then: the volume and behavior of notifications are exactly as they are today
Considerations:
1. Localization
No new customer-facing text in this story.
2. Analytics / Data Storage
Existing global, customer, and personal settings are preserved; non-enabled customers see no change.
""",

"my-jobs-role-filtering": """# Background

Allianz recruiters see every job they are attached to in "My Jobs," even jobs where they are only helping out. They want their default view to show only the jobs where they are the Primary (Main) recruiter, with a separate place for the jobs they support. The same idea applies to meetings, email/SMS campaigns, and leads. They also need to filter by role across the CRM — for example, a Spotlight that finds all jobs where a specific colleague is the main recruiter (ASRM-1570, CUSP-5947, and the Allianz "Support Recruiter" reference doc).

One important note from the customer: showing everything to everyone breaks the "need-to-know" principle and can expose candidates that a person shouldn't see, so the default views must respect each person's role.

# How It Works

- Step 1: A recruiter opens My Jobs.
- Step 2: By default they see the jobs where they are the Primary recruiter.
- Step 3: Jobs where they are a Secondary/Support recruiter appear in a separate tab or group.
- Step 4: They can change the filter to also see jobs they support, or their colleagues' jobs.
- Step 5: The same role filter is available in Spotlights and saved filters across the CRM (for example, filter by the main recruiter's email).

# User Stories

## Story 1: Filter My Jobs by role
User Story:
As a recruiter, I want to filter "My Jobs" by my role on the job so that I can focus on the jobs where I am the lead recruiter.
Acceptance Criteria:
Scenario: Show only my lead jobs
Given: expanded roles are on and I hold different roles across jobs
When: I filter "My Jobs" to Primary Recruiter
Then: I see only the jobs where I am the Primary recruiter
Scenario: Unchanged for non-enabled customers
Given: a customer who has not turned this on
When: I open "My Jobs"
Then: today's behavior and role choices are unchanged
Considerations:
1. Localization
Filter labels and role names must be translated into the 13+ supported languages.
2. Analytics / Data Storage
The filter reads the job roles from the foundation spec; it stores no new data.

## Story 2: Default view = my lead jobs, support jobs separate
User Story:
As a Support (Secondary) recruiter, I want my default "My Jobs" view to show the jobs I lead and to keep the jobs I support in a separate tab so that my own jobs are not buried under the ones I only help with.
Acceptance Criteria:
Scenario: Lead jobs by default
Given: expanded roles are on
When: I open "My Jobs" with no filter set
Then: I see the jobs where I am the Primary recruiter, and jobs I support are in a separate tab
Scenario: Respect need-to-know
Given: jobs and candidates I am not entitled to see
When: any default view loads
Then: I am not shown jobs, meetings, or candidates outside my role
Considerations:
1. Localization
Tab names and view labels (for example, "Lead", "Supporting") must be translated into the 13+ supported languages.
2. Analytics / Data Storage
The view reads each person's role and assignments; the click-to-relevant-action path is measured to confirm the time-saving goal.

## Story 3: Decide placement when someone is both lead and support
User Story:
As a recruiter who is both a lead and a supporting recruiter on the same job, I want the job to show up in the most relevant place so that the view is not confusing.
Acceptance Criteria:
Scenario: Lead wins when both apply
Given: I hold both a leading and a supporting role on one job
When: my default view is built
Then: the job is placed using role priority (the leading role wins)
Scenario: No tiebreak needed
Given: all of my roles on a job are the same type
When: the view is built
Then: the job simply appears in that group
Considerations:
1. Localization
No new customer-facing text in this story.
2. Analytics / Data Storage
Placement uses the role priority from the foundation spec; it stores no new data.

## Story 4: Filter by role across the CRM (Spotlights and saved filters)
User Story:
As a CRM user, I want the four roles available wherever I can filter by job role so that role-based views are consistent across the whole CRM, not just in "My Jobs."
Acceptance Criteria:
Scenario: Roles available everywhere a role filter exists
Given: expanded roles are on
When: I build a Spotlight, saved filter, or list view that filters by job role
Then: all four roles are available as choices, where only the old single recruiter was before
Scenario: Find a colleague's jobs
Given: I support a colleague's jobs
When: I filter for jobs where that colleague is the main recruiter (for example, by their email)
Then: I get exactly those jobs
Considerations:
1. Localization
Role values in every filter and Spotlight must be translated into the 13+ supported languages.
2. Analytics / Data Storage
Filters read the stored job roles; they store no new data.

## Story 5: Apply the same default to meetings, campaigns, and leads
User Story:
As a recruiter, I want my dashboard (meetings, email and SMS campaigns, and new leads) to default to my lead jobs, with supported jobs available separately, so that my whole workspace reflects what I lead.
Acceptance Criteria:
Scenario: Meetings default to my lead jobs
Given: expanded roles are on
When: I open my meetings
Then: I see meetings for the jobs I lead and the meetings where I am an interviewer, with a separate tab for jobs I support
Scenario: Campaigns and leads follow the same rule
Given: Overview, My Email Campaigns, My SMS Campaigns, and Discover New Leads
When: I open them
Then: each defaults to the work I lead or set up, with the option to switch to colleagues' work
Considerations:
1. Localization
All view and tab labels must be translated into the 13+ supported languages.
2. Analytics / Data Storage
These views read role and assignment data; they must respect candidate visibility (need-to-know) and store no new data.
""",

"per-role-analytics": """# Background

Because everyone on a job is just "Recruiter," Allianz and Disney cannot measure who actually drove the hiring. A Sourcer's or a Secondary recruiter's work is lumped in with everyone else's. This spec tags each tracked action with the person's job role, so each role's activity can be reported separately — the same way "recruiter" is reported today. Disney needs this to measure their support roles, and ThermoFisher needs it for sourcing credit (PHEM-2109151, ASRM-1570).

# How It Works

- Step 1: A recruiter does something that gets tracked on a job (for example, screens a candidate).
- Step 2: The CRM records the action together with the person's role on that job.
- Step 3: The data lands in the analytics store (Snowflake) with the role attached.
- Step 4: In the report builder, customers can report by role, using the role each person held at the time the action happened.

# User Stories

## Story 1: Tag each tracked action with the person's role
User Story:
As an analytics engineer, I want each tracked action to carry the person's job role so that a Sourcer's or Secondary recruiter's work is counted separately instead of being lumped into "recruiter."
Acceptance Criteria:
Scenario: Role is attached to the activity
Given: expanded roles are on
When: a hiring-team member does a tracked action on a job
Then: the recorded activity includes that person's role on the job
Scenario: Roles stay separate
Given: a Sourcer and a Primary recruiter both act on the same job
When: their activity is recorded
Then: each is counted under its own role, not merged
Considerations:
1. Localization
No customer-facing text in this story; role names shown in reports stay translatable.
2. Analytics / Data Storage
Activity is stored in Snowflake (the analytics store) keyed by role so it can be queried by role — this is the core data requirement of this spec.

## Story 2: Make role a reporting dimension
User Story:
As a data analyst, I want each role available as a reporting dimension so that I can slice activity by role.
Acceptance Criteria:
Scenario: Role available to query
Given: role-tagged activity is flowing in
When: I query the analytics data
Then: job role is available as its own field to group and filter by
Scenario: On par with "recruiter"
Given: how "recruiter" is tracked today
When: I compare
Then: the new roles are modeled the same way, at the same level of detail
Considerations:
1. Localization
Any role labels shown to users must be translated into the 13+ supported languages.
2. Analytics / Data Storage
The role dimension is built in Snowflake and supports the four roles today and more later.

## Story 3: Report by role without engineering help
User Story:
As a customer report author, I want the new roles available in the report builder so that I can build role-level reports myself.
Acceptance Criteria:
Scenario: Self-serve role report
Given: expanded roles are on and the role dimension exists
When: I build a report
Then: I can pull the four roles as fields or filters
Scenario: Same experience as recruiter reporting
Given: how recruiter reports work today
When: I build a role report
Then: the experience matches today's recruiter reporting
Considerations:
1. Localization
Report builder field labels and role values must be translated into the 13+ supported languages.
2. Analytics / Data Storage
The report builder reads the role dimension from Snowflake; matching today's experience inside the Phase-1 timeline is still being confirmed with the analytics team.

## Story 4: Keep credit correct when roles change
User Story:
As a report consumer, I want reports to use role history so that activity is credited correctly even when someone's role changed during a job.
Acceptance Criteria:
Scenario: Credit by the role at the time
Given: a person changed roles part-way through a job
When: I run a role report over a date range
Then: each activity is credited to the role that person held when it happened
Scenario: The past is not rewritten
Given: a role change today
When: I report on earlier activity
Then: the earlier credit does not change
Considerations:
1. Localization
No customer-facing text in this story.
2. Analytics / Data Storage
Reports join activity to the role history from the foundation spec; that history must be kept for the reporting period.
""",

"role-aware-automation-recipes": """# Background

CRM Automations ("recipes") can only target the old single "Recruiter." Now that there is a Primary recruiter and supporting recruiters, automations need to target the right one — for example, email the Primary recruiter when an application is withdrawn, not every recruiter on the job. Old recipes built on the single recruiter must keep working (PHEM-2109151).

# How It Works

- Step 1: An automation runs (for example, "email the recruiter when an application is withdrawn").
- Step 2: The automation figures out the correct role on that job (for example, Primary Recruiter).
- Step 3: It sends to or acts on the right person for that role.

# User Stories

## Story 1: Use the new roles in recipe conditions
User Story:
As an automation author, I want the four roles available in recipe conditions so that I can build automations that branch on a person's role on the job.
Acceptance Criteria:
Scenario: Roles available in conditions
Given: expanded roles are on
When: I build a condition on job role (for example, "if the hiring-team role is Sourcer")
Then: all four roles are available to choose
Scenario: Unchanged when off
Given: a customer who has not turned this on
When: I build a condition
Then: only today's roles are available and nothing changes
Considerations:
1. Localization
Role names shown in the recipe builder must be translated into the 13+ supported languages.
2. Analytics / Data Storage
Conditions read the stored job roles; automation runs are logged as they are today.

## Story 2: Send actions to the right role
User Story:
As an automation author, I want role-targeting actions to resolve "recruiter" to the correct role so that emails and hand-offs reach the right person.
Acceptance Criteria:
Scenario: Resolve to the right recruiter
Given: expanded roles are on
When: an action like "email the recruiter on application withdrawal" or "forward profile" runs
Then: it goes to the correct role (for example, the Primary recruiter), not to every recruiter
Scenario: Hiring Manager action still works
Given: the "forward candidate to Hiring Manager" action in Phase 1
When: it runs
Then: it still reaches the right person (the Hiring Manager split comes in a later phase)
Considerations:
1. Localization
Any customer-facing output (for example, email templates) must support the 13+ supported languages.
2. Analytics / Data Storage
Actions read the stored job roles; they may record per-role activity for reporting.

## Story 3: Keep existing recipes working
User Story:
As an existing customer, I want my current recipes to keep working so that enabling roles does not break my automations.
Acceptance Criteria:
Scenario: Off means no change
Given: recipes built on today's single recruiter
When: the customer has not turned this on
Then: they keep working exactly as before
Scenario: On maps the old recruiter to Primary
Given: expanded roles are on
When: an old recipe refers to "Recruiter"
Then: it maps to the Primary recruiter and does not break
Considerations:
1. Localization
No new customer-facing text in this story.
2. Analytics / Data Storage
The old role information is preserved so existing recipes still resolve correctly.

## Story 4: Find and update every place roles are used
User Story:
As the automation product owner, I want every recipe condition and action that uses job role identified and updated so that roles work consistently across all automations.
Acceptance Criteria:
Scenario: Full list updated
Given: the review of all role-using conditions and actions
When: the list is complete
Then: each one is updated to offer the four roles
Scenario: Known actions covered
Given: the three known actions (email recruiter on application withdrawal, forward candidate to Hiring Manager, forward profile)
When: the update ships
Then: all three are confirmed updated
Considerations:
1. Localization
Role values across all updated actions must be translated into the 13+ supported languages.
2. Analytics / Data Storage
No new data is stored; these actions read the existing job roles.
""",
}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def strip_inline(t):
    return t.replace("**", "").replace("__", "").replace("`", "")


def parse_md(md):
    paras = []
    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        s = line.lstrip()
        if s.startswith("#### "):
            paras.append(("HEADING_4", strip_inline(s[5:]).strip()))
        elif s.startswith("### "):
            paras.append(("HEADING_3", strip_inline(s[4:]).strip()))
        elif s.startswith("## "):
            paras.append(("HEADING_2", strip_inline(s[3:]).strip()))
        elif s.startswith("# "):
            paras.append(("HEADING_1", strip_inline(s[2:]).strip()))
        elif s.startswith("- ") or s.startswith("* "):
            paras.append(("BULLET", strip_inline(s[2:]).strip()))
        elif s.startswith("> "):
            paras.append(("NORMAL", strip_inline(s[2:]).strip()))
        else:
            paras.append(("NORMAL", strip_inline(s).strip()))
    return paras


def build_requests(paras):
    full = ""
    spans = []
    cursor = 1
    for kind, text in paras:
        start = cursor
        full += text + "\n"
        seg = u16(text)
        spans.append((start, start + seg + 1, kind))
        cursor += seg + 1
    reqs = [{"insertText": {"location": {"index": 1}, "text": full}}]
    for start, end, kind in spans:
        if kind.startswith("HEADING"):
            reqs.append({"updateParagraphStyle": {
                "range": {"startIndex": start, "endIndex": end},
                "paragraphStyle": {"namedStyleType": kind},
                "fields": "namedStyleType"}})
        elif kind == "BULLET":
            reqs.append({"createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    return reqs, full


def get_token():
    d = json.load(open(TOKENS))
    g = d["google"]
    exp = g.get("token_expires_at")
    need = True
    if exp:
        try:
            t = time.strptime(exp.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            if time.mktime(t) - time.mktime(time.gmtime()) > 120:
                need = False
        except Exception:
            pass
    if need and d.get("backend_jwt"):
        try:
            req = urllib.request.Request(
                f"{BACKEND}/integrations/refresh/google", method="POST",
                headers={"Authorization": "Bearer " + d["backend_jwt"]})
            r = json.load(urllib.request.urlopen(req, timeout=30))
            g["access_token"] = r["access_token"]
            print("  (token refreshed)")
        except Exception as e:
            print("  (refresh failed, using existing token):", e)
    return g["access_token"]


def api(method, url, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def move_to_folder(token, doc_id):
    try:
        meta = api("GET",
                   f"https://www.googleapis.com/drive/v3/files/{doc_id}?fields=parents&supportsAllDrives=true",
                   token)
        parents = ",".join(meta.get("parents", []))
        url = (f"https://www.googleapis.com/drive/v3/files/{doc_id}"
               f"?addParents={FOLDER_ID}&removeParents={parents}&fields=id,parents&supportsAllDrives=true")
        api("PATCH", url, token, {})
        return True
    except Exception as e:
        print(f"  (could not move into folder automatically: {e})")
        return False


def process(token, slug):
    md = DOC_MD[slug]
    paras = parse_md(md)
    reqs, full = build_requests(paras)
    stories = md.count("## Story ")
    print(f"[{slug}] stories={stories} paras={len(paras)} chars={u16(full)}")
    if DRY:
        return None
    if CREATE:
        created = api("POST", "https://docs.googleapis.com/v1/documents", token,
                      {"title": TITLES[slug]})
        doc_id = created["documentId"]
        api("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate",
            token, {"requests": reqs})
        moved = move_to_folder(token, doc_id)
        print(f"  -> created ({'in folder' if moved else 'Drive root, move manually'}): "
              f"https://docs.google.com/document/d/{doc_id}/edit")
        return doc_id
    # UPDATE existing doc in place: clear ALL content, then insert the new body.
    doc_id = UPDATE_IDS[slug]
    doc = api("GET", f"https://docs.googleapis.com/v1/documents/{doc_id}", token)
    end = doc["body"]["content"][-1]["endIndex"]
    if end - 1 > 1:
        api("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", token,
            {"requests": [{"deleteContentRange":
                           {"range": {"startIndex": 1, "endIndex": end - 1}}}]})
    api("POST", f"https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate", token,
        {"requests": reqs})
    print(f"  -> updated: https://docs.google.com/document/d/{doc_id}/edit")
    return doc_id


def main():
    targets = [s for s in TITLES if (ONLY is None or s == ONLY)]
    if not targets:
        print(f"No spec matches --only {ONLY}. Known: {list(TITLES)}")
        return
    token = None if DRY else get_token()
    results = {}
    for slug in targets:
        try:
            results[slug] = process(token, slug)
        except urllib.error.HTTPError as e:
            print(f"[{slug}] HTTP {e.code}: {e.read().decode()[:300]}")
        except Exception as e:
            print(f"[{slug}] ERROR: {e}")
    if not DRY:
        print("\n" + ("Created" if CREATE else "Updated") + " docs:")
        for s, d in results.items():
            if d:
                print(f"  {s}: https://docs.google.com/document/d/{d}/edit")


if __name__ == "__main__":
    mode = "DRY-RUN (no changes)" if DRY else (
        "APPLYING (creating new docs)" if CREATE else "APPLYING (updating existing docs in place)")
    print("MODE:", mode)
    main()
