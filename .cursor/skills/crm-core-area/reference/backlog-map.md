# CRM Core Jira backlog map (generated)

Generated from `snapshot-crm-core-jira-areas.json`, run date 2026-10-23. Do not edit by hand; rerun `build_crm_core_backlog_map.py`.

JQL: `project = PHEM AND "Product Experience: Product2[Dropdown]" = "Recruiter Experience (RX) - CRM - Core" AND type IN (Epic, Initiative, Story) AND created >= 2026-01-01 AND status NOT IN (Done, Blocked, "In QA", "PM Acceptance Queue")`

Legend: **I** Initiative, **E** Epic, **S** Story. After the status comes the item's Fix Version target (`~N mo` = months from the run date), `slipped` (release date passed, item still open) or `Backlog` (no release). `branch:` rolls up every counted item below a parent, across all areas.

## Hiring status / pipeline / stages / lead status

4 items (I 0 · E 1 · S 3). Planned 1 · slipped 0 · unplanned 3. Latest planned release: OffCycle-2026 (~2.3 mo). Pace estimate: 0.2–0.3 team-months for 3 open stories.

- **E** PHEM-2270995 Enhancement for Agency module · To Do — branch: latest OffCycle-2026 (~2.3 mo); 3 planned / 0 slipped / 0 unplanned _(counted under Not in the six areas)_
  - **S** PHEM-2271103 Lead & Applicant Counts by Agency · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2136326 RX - Core - Translation Experience for Hiring Status · To Do · Backlog
- **E** PHEM-1237317 Customer Development · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1467013 Enforce Separate Spotlights for Leads and Applicants When Hiring Pipeline Is Enabled · To Do · Backlog
- **E** PHEM-1126283 RX Exports and Imports · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1700218 Enable "Latest Job Stage" as an Exportable Field · Story Elaboration · Backlog

## Jobs / requisitions / applications / posting

55 items (I 2 · E 16 · S 37). Planned 23 · slipped 8 · unplanned 24. Latest planned release: OffCycle-2026 (~2.3 mo). Pace estimate: 3–4 team-months for 37 open stories.

- **I** PHEM-2412940 Siemens Healthineers Requirements on product improvements for CRM Core · To Do — branch: latest 26.11 (~1.2 mo); 3 planned / 1 slipped / 0 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-2491710 Translations for 2 system job fields not available on career site · In Progress · 26.11 (~1.2 mo)
  - **E** PHEM-2435084 Translations for 4 additional job fields not available · To Do · 26.11 (~1.2 mo)
  - **E** PHEM-2199077 HIRE - Allow creation of private links for confidential jobs · In Progress · 26.09 slipped
- **I** PHEM-2341558 Screening FY26 | Omnichannel Screening · In Progress — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **E** PHEM-2270129 PQS | CRM | Clear Questionnaire Selection on Job Create/Edit | [Disney, Sep 15] · Done — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
    - **S** PHEM-2270130 CRM – FE – Allow clearing questionnaire selection in Create/Edit Job form · To Do · Backlog
- **I** PHEM-2252378 RX - Disney Enhancements - Phase 2 by Sept. 20 · To Do — branch: latest OffCycle-2026 (~2.3 mo); 7 planned / 0 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-2260385 CRM – Bulk Edit Job Requisitions · To Do · 26.11 (~1.2 mo) — branch: latest OffCycle-2026 (~2.3 mo); 7 planned / 0 slipped / 0 unplanned
    - **S** PHEM-2383238 S6. RX – Show and standardize Job system fields in settings (for bulk edit) · Development · OffCycle-2026 (~2.3 mo)
    - **S** PHEM-2383155 S5. RX – FE/BE – Bulk edit results panel (history APIs + UI) · To Do · 26.11 (~1.2 mo)
    - **S** PHEM-2314688 S4. RX + Notifications – Review results via Jobs panel deep link · To Do · OffCycle-2026 (~2.3 mo)
    - **S** PHEM-2314682 S3. RX – BE – Async batch processing and activities audit · Development · OffCycle-2026 (~2.3 mo)
    - **S** PHEM-2314673 S1. RX – FE – Bulk edit flow on Jobs · Development · OffCycle-2026 (~2.3 mo)
  - **E** PHEM-2252497 CRM - Application Search Index & Application-Centric List (Evaluation + App Fields) · To Do · Backlog
- **I** PHEM-1987584 RedDot Integration · To Do · 26.06 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
  - **E** PHEM-1987585 RedDot CRM MVP · To Do · Backlog
- **I** PHEM-1987368 RX Views / Spotlights · To Do — branch: no planned release; 0 planned / 1 slipped / 1 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-1987497 Job-Attribute Spotlights MVP · To Do · Backlog
- **I** PHEM-1970578 RX Core Job Activity View · To Do · 26.05 slipped
- **I** PHEM-591477 CRM Personalisation · To Do — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 0 unplanned _(context: outside filter)_
  - **E** PHEM-710076 RX Views / Spotlights · To Do — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 0 unplanned _(context: outside filter)_
    - **S** PHEM-1549914 Display Contextual Job Variation Status in Grid when Filtering by Posting Status · To Do · OffCycle-2026 (~2.3 mo)
- **I** PHEM-521288 Multi Language Support - Allianz · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **E** PHEM-398531 Additional Fields - Support multi-language for additional fields in CRM · Epic Grooming — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
    - **S** PHEM-2486436 Core – BE – Flow additional job field translations to career site · Story Ready · Backlog
- **E** PHEM-2495077 Job Creation Enhancement Using Req Templates · In Progress — branch: no planned release; 0 planned / 1 slipped / 0 unplanned _(context: outside filter)_
  - **S** PHEM-2490597 Populate all selected languages in publish section by default · To Do · 26.10 slipped
- **E** PHEM-2396086 CRM – Insert assets from Asset Manager into job descriptions and email templates · To Do · OffCycle-2026 (~2.3 mo) — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 1 unplanned
  - **S** PHEM-2522906 Core – FE – Align Asset Manager MFE with CMS design · To Do · Backlog
- **E** PHEM-2391005 CRM – Custom job statuses (Phenom Hire + ATS) · To Do · Backlog
- **E** PHEM-2281914 RX Job Activity - Phase 2 · To Do · 26.09 slipped
- **E** PHEM-2278020 IX and CRM: Job workflow optimisation · To Do — branch: latest OffCycle-2026 (~2.3 mo); 4 planned / 0 slipped / 0 unplanned _(counted under Forwarding / LinkedIn / ATS↔CRM sync)_
  - **S** PHEM-2280602 Disclaimer text handling with req templates apis · Development · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2267008 CRM to Workday Job Lifecycle Sync (Create / Publish / Unpublish) · In Progress — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 1 slipped / 0 unplanned _(counted under Forwarding / LinkedIn / ATS↔CRM sync)_
  - **S** PHEM-2268634 E1. RX – QA – E2E Create → Publish → Unpublish (incl. failure/retrigger) · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2202537 Visibility and search on primary job title for Disney · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2186925 Hire - Schedule posting of a job · To Do · 26.10 slipped — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 1 slipped / 0 unplanned
  - **S** PHEM-2201265 CRM Core: Publishing Job in CRM based on configured date and time · UX/UI Validation · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2184565 Notify recruiters and hiring managers when assigned to a job · To Do · Backlog
- **E** PHEM-2180576 Document viewer for Job attachments · In Progress · 26.10 slipped — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 1 slipped / 0 unplanned
  - **S** PHEM-2358556 CRM – FE – Fix CSV, XLS, and XLSX rendering in Job document viewer · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2117038 RX - Unpost Job based on Job expiry, Job Status, etc · In Progress — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-2190578 CRM Core: Expiring job based on configured date and time in Job entity · UX/UI Validation · Backlog
- **E** PHEM-2104070 4. Data Migration with Role Assignment Logic · To Do — branch: no planned release; 0 planned / 1 slipped / 2 unplanned _(counted under Access / CRM not opening / permissions)_
  - **S** PHEM-2104071 4.1: Migrate Existing Job Hiring Team Data · To Do · Backlog
- **E** PHEM-1974314 Addition of Scheduling Flow to Blank/Edit Job Screens · To Do · Backlog
- **E** PHEM-1939858 [CRM] Streamline Move Application — application ID, confidentiality & post-move clarity · Epic Grooming — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 0 unplanned _(context: outside filter)_
  - **S** PHEM-2137298 CRM Core — Validate impact for Move Application feature · Story Grooming · OffCycle-2026 (~2.3 mo)
- **E** PHEM-1902635 CRM – Job page — Overview tab · To Do · Backlog
- **E** PHEM-1354652 Availability Management · To Do — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1699793 creation of columns for job availability · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-1353262 RX Core Support Ticket Reduction · To Do — branch: latest 26.11 (~1.2 mo); 1 planned / 0 slipped / 11 unplanned _(context: outside filter)_
  - **S** PHEM-1701444 Copy Hiring Team when the Default job got changed · Story Ready · Backlog
  - **S** PHEM-1504031 Job field mapper config remover from UI · To Do · Backlog
- **E** PHEM-791913 RX Jobs · To Do — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 7 unplanned _(context: outside filter)_
  - **S** PHEM-1873657 Converting of jobdetails to jobpostings array · Development · Backlog
  - **S** PHEM-1873652 send only modified fields to backend in job edit flo · To Do · Backlog
  - **S** PHEM-1873651 Flink integration to listen to Business events and push to Doris in link services · To Do · Backlog
  - **S** PHEM-1873650 send emails to recruiters & CP events integration · To Do · Backlog
  - **S** PHEM-1873649 Editing of a job phenomhire flow · Development · Backlog
  - **S** PHEM-1873648 Creating of private job in phenomhire flow · Development · Backlog
  - **S** PHEM-1873647 Create draft job/confidential jobs in phenomhire flow · Development · Backlog
  - **S** PHEM-1529975 API - Update Additional Job Fields · Development · OffCycle-2026 (~2.3 mo)
  - **S** PHEM-1529974 API - Unpublish Job · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-521185 Enhance Agency module in CRM · In Progress — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2182747 Cross-Filtering Agencies by Country and Job Category · Development · Backlog
- **E** PHEM-55375 Field management in RX · Done — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-1700207 Enabling field management in the existing Job field for disney · Development · OffCycle-2026 (~2.3 mo)
- **S** PHEM-2396523 Implementing audit logs for candidate and application fields · To Do · 26.11 (~1.2 mo)
- **S** PHEM-2259436 UUID should be generated and passed in the create/edit job payload · To Do · OffCycle-2026 (~2.3 mo)
- **S** PHEM-2122618 Intake Agent: Surface Existing CRM Job Description at Start of Intake Conversation · To Do · 26.07 slipped
- **S** PHEM-1982214 My Jobs & Interview Visibility · To Do · Backlog
- **S** PHEM-1979661 Internal posted description and Title not visible in CRM, only external title and content is shown · To Do · Backlog
- **S** PHEM-1699770 Integration of jobs fields mfe in crm settings · To Do · OffCycle-2026 (~2.3 mo)

## Forwarding / LinkedIn / ATS↔CRM sync

21 items (I 2 · E 9 · S 10). Planned 7 · slipped 7 · unplanned 7. Latest planned release: OffCycle-2026 (~2.3 mo). Pace estimate: 0.8–1.1 team-months for 10 open stories.

- **I** PHEM-2341256 LinkedIn CRM Connectivity & Enhancements · To Do · 26.11 (~1.2 mo) — branch: latest 26.11 (~1.2 mo); 2 planned / 0 slipped / 0 unplanned
  - **E** PHEM-2341415 CRM and LinkedIn Broken Pipeline · To Do · 26.11 (~1.2 mo)
- **I** PHEM-1957943 RX Projects · To Do — branch: no planned release; 0 planned / 3 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-1957974 HRM <> CRM Projects 26.05 · To Do · 26.07 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
- **I** PHEM-1957322 RX Core - LinkedIn CRM Connect · To Do · 26.05 slipped — branch: no planned release; 0 planned / 3 slipped / 0 unplanned
  - **E** PHEM-2014661 LinkedIn CRM Hardening 26.06 · To Do · 26.05 slipped
  - **E** PHEM-1957323 LinkedIn CRM Hardening 26.05 · To Do · 26.05 slipped
- **I** PHEM-937647 HRM <> CRM workflows · In Progress — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **E** PHEM-1346553 HRM EPIC: Project workflow - PHASE I · Done — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
    - **S** PHEM-2014648 HRM Projects Activities Sync · Story Grooming · Backlog
- **I** PHEM-657552 HCM Updates to Created Jobs · To Do — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 0 unplanned _(context: outside filter)_
  - **E** PHEM-1547838 HCM Updates to Created Jobs · To Do — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 0 unplanned _(context: outside filter)_
    - **S** PHEM-1695834 [CRM] API for Updating Job Attribute Updates from ERM · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2278041 CRM ↔ Workday Job Sync — Failure Handling, Retry & Manual Retrigger · To Do · Backlog — branch: latest 26.11 (~1.2 mo); 1 planned / 0 slipped / 1 unplanned
  - **S** PHEM-2268624 A2. RX – FE – Job sync status display + filter + manual retrigger CTA · To Do · 26.11 (~1.2 mo)
- **E** PHEM-2278020 IX and CRM: Job workflow optimisation · To Do · OffCycle-2026 (~2.3 mo) — branch: latest OffCycle-2026 (~2.3 mo); 4 planned / 0 slipped / 0 unplanned
  - **S** PHEM-2280606 Hosting of offline service · To Do · OffCycle-2026 (~2.3 mo)
  - **S** PHEM-2280605 Api for creating ats jobs in job service · ON Hold · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2267008 CRM to Workday Job Lifecycle Sync (Create / Publish / Unpublish) · In Progress · 26.10 slipped — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 1 slipped / 0 unplanned
- **E** PHEM-2260823 CRM - LinkedIn CRM Connect - InMail Stub Profile · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-2288791 CRM – FE/BE – InMail Stub Profile hydration · To Do · Backlog
- **E** PHEM-2104059 3. ATS Integration — Role-Aware Job Pull · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 3 unplanned
  - **S** PHEM-2104068 3.2: ATS Adapter Updates (SuccessFactors, Workday, Others) · To Do · Backlog
  - **S** PHEM-2104061 3.1: Generic ATS-to-CRM Role Mapping Engine & Admin UI · To Do · Backlog
- **E** PHEM-2007989 Indeed Integration — Migrate Phenom Hire to Job Sync API and Enable Native Apply Experience · To Do · Backlog
- **E** PHEM-1916976 RX Localization · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **S** PHEM-1917001 Sync supported locales between HRM and CRM to ensure cross-product parity · To Do · Backlog
- **S** PHEM-2363294 Improvement to New Hire ADP Integration · To Do · 26.06 slipped

## Access / CRM not opening / permissions

46 items (I 0 · E 8 · S 38). Planned 8 · slipped 5 · unplanned 33. Latest planned release: OffCycle-2026 (~2.3 mo). Pace estimate: 3.1–4.1 team-months for 38 open stories.

- **I** PHEM-2252378 RX - Disney Enhancements - Phase 2 by Sept. 20 · To Do — branch: latest OffCycle-2026 (~2.3 mo); 7 planned / 0 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-2260385 CRM – Bulk Edit Job Requisitions · To Do — branch: latest OffCycle-2026 (~2.3 mo); 7 planned / 0 slipped / 0 unplanned _(counted under Jobs / requisitions / applications / posting)_
    - **S** PHEM-2314676 S2. RX – Permissions and field eligibility for bulk edit · To Do · 26.11 (~1.2 mo)
- **I** PHEM-2018552 Schema-Driven UI (SDUI) for CRM · To Do — branch: no planned release; 0 planned / 0 slipped / 29 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-2024863 Page schema API (storage & delivery) · In Progress — branch: no planned release; 0 planned / 0 slipped / 9 unplanned _(counted under Not in the six areas)_
    - **S** PHEM-2024950 Tenant isolation and RBAC · To Do · Backlog
- **I** PHEM-1987498 Notes · To Do — branch: no planned release; 0 planned / 1 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-1987505 Note Associations · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(counted under Not in the six areas)_
    - **S** PHEM-1987583 Departmentalization for Notes Association · To Do · Backlog
- **I** PHEM-1957943 RX Projects · To Do — branch: no planned release; 0 planned / 3 slipped / 2 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-1957974 HRM <> CRM Projects 26.05 · To Do — branch: no planned release; 0 planned / 1 slipped / 1 unplanned _(counted under Forwarding / LinkedIn / ATS↔CRM sync)_
    - **S** PHEM-1957991 Maintain Team Member ID & Visualize User Access · ON Hold · Backlog
- **E** PHEM-2492867 Worker council users cannot access leads · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 3 unplanned
  - **S** PHEM-2492869 Core – BE – Block worker council lead access for departmentalized jobs · To Do · Backlog
  - **S** PHEM-2492868 Core – FE – Hide the lead tab in a job from the worker council role · Story Grooming · Backlog
- **E** PHEM-2267012 RX – RBAC to Restrict Recruiter Download / Export in CRM · To Do · 26.10 slipped — branch: latest 26.11 (~1.2 mo); 5 planned / 1 slipped / 0 unplanned
  - **S** PHEM-2288888 F1. RX – QA – E2E Restrict download/export (CRM + II + HRM) · To Do · 26.11 (~1.2 mo)
  - **S** PHEM-2288887 E2. Events – FE/BE – Restrict event candidate/report export · To Do · 26.11 (~1.2 mo)
  - **S** PHEM-2288886 E1. Onboarding – FE/BE – Restrict onboarding report export · To Do · 26.11 (~1.2 mo)
  - **S** PHEM-2288881 A2. Platform – BE – Implement authorization evaluate + tenant Restrict/Deny (fail-closed, exemptions) · Development · 26.11 (~1.2 mo)
  - **S** PHEM-2270497 B1. RX – FE/BE – Restrict all CRM download & export keys (P0) · To Do · 26.11 (~1.2 mo)
- **E** PHEM-2178519 Deparmentalization support for Employee/Candidate connections · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 2 unplanned
  - **S** PHEM-2178515 Support departmentalization framework for Employee/Candidate connections feature · To Do · Backlog
- **E** PHEM-2163324 ENBW - Restrict Independent Lead Visibility · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2163333 Platform Architecture - "NA" (Not Applicable) Scope Handling · To Do · Backlog
  - **S** PHEM-2163326 Interim Workaround - Default Project & CRM Automation (Immediate Unblock) · To Do · Backlog
- **E** PHEM-2104082 7. Role-Based UI Visibility & Filtering · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 5 unplanned
  - **S** PHEM-2106057 7.5: Role-aware analytics ETL and role-filtered dashboards · To Do · Backlog
  - **S** PHEM-2106044 7.4: Refactor HRM scheduling widget to use roleCategory for action gating · To Do · Backlog
  - **S** PHEM-2106019 7.3: Add expanded hiring team roles to VX screening evaluation configuration · To Do · Backlog
  - **S** PHEM-2106005 7.2: Role-aware HRM task assignment for expanded hiring team roles · To Do · Backlog
  - **S** PHEM-2104083 7.1: "My Jobs" — Role-Aware Filtering & Default Views · To Do · Backlog
- **E** PHEM-2104079 6. Role-Aware Auto-Provisioning · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 2 unplanned
  - **S** PHEM-2104081 6.2: [Deferred Post-MVP] Default Notification Profiles per Provisioning Source · To Do · Backlog
  - **S** PHEM-2104080 6.1: Role-Differentiated Auto-Provisioning · To Do · Backlog
- **E** PHEM-2104076 5. Tenant-Level Notification Configuration · To Do — branch: no planned release; 0 planned / 1 slipped / 3 unplanned _(counted under How-to / configuration / enablement question)_
  - **S** PHEM-2106102 5.3: Add role-specific email template tokens for expanded hiring team roles · To Do · Backlog
  - **S** PHEM-2104078 5.2: Notification Dispatch Engine — Role-Aware Routing · To Do · Backlog
  - **S** PHEM-2104077 5.1: [Deferred Post-MVP] Admin UI Role-to-Notification Trigger Mapping · To Do · Backlog
- **E** PHEM-2104070 4. Data Migration with Role Assignment Logic · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 2 unplanned
  - **S** PHEM-2106084 4.2: Validate CBAC access integrity during and after role migration · To Do · Backlog
- **E** PHEM-2104062 2. Role Display & Assignment UI · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
  - **S** PHEM-2104063 2.1: Hiring Team Widget — Role Display & Assignment · To Do · Backlog
- **E** PHEM-2104059 3. ATS Integration — Role-Aware Job Pull · To Do — branch: no planned release; 0 planned / 1 slipped / 3 unplanned _(counted under Forwarding / LinkedIn / ATS↔CRM sync)_
  - **S** PHEM-2104069 3.3: CRM-Native Job Creation — Role Assignment in Hiring Team Setup · To Do · Backlog
- **E** PHEM-2079228 Employee Detail Page Visibility - With Consent No in CRM · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-1353262 RX Core Support Ticket Reduction · To Do — branch: latest 26.11 (~1.2 mo); 1 planned / 0 slipped / 11 unplanned _(context: outside filter)_
  - **S** PHEM-2215042 Handle role assignment propagation · To Do · Backlog
  - **S** PHEM-1504053 Enhancement in Departmentalization Migration Script · To Do · Backlog
- **E** PHEM-1027271 RX Core General · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1546009 Extend forced logout from 8 to 12 hrs · To Do · Backlog
- **E** PHEM-55375 Field management in RX · Done — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-1697298 feature flag based & permissions fields handling in field management · To Do · Backlog
- **S** PHEM-2165622 RBC Ask: disable tag creation and tag management access to ALL users except the list provided below · To Do · OffCycle-2026 (~2.3 mo)
- **S** PHEM-2020503 Research and Discovery Job-Level Hiring Team Roles · To Do · Backlog
- **S** PHEM-2005892 AI Agent Settings to CRM & Implement Admin Access with Media Preview · To Do · Backlog
- **S** PHEM-1982218 Sourcer Role Ingestion & Visibility · To Do · Backlog
- **S** PHEM-1982216 Privacy Segmentation · To Do · Backlog
- **S** PHEM-1982212 Role Ingestion & CRM Display · Story Ready · Backlog
- **S** PHEM-1577362 New Associate Interviewer Role · UX Queue · Backlog

## Events / university recruiting

0 items (I 0 · E 0 · S 0). Planned 0 · slipped 0 · unplanned 0. Latest planned release: none.

No items.

## How-to / configuration / enablement question

17 items (I 1 · E 4 · S 12). Planned 6 · slipped 5 · unplanned 6. Latest planned release: OffCycle-2026 (~2.3 mo). Pace estimate: 1–1.3 team-months for 12 open stories.

- **I** PHEM-1970553 RX Core Self-Servicing Errors · To Do · 26.05 slipped — branch: no planned release; 0 planned / 2 slipped / 0 unplanned
  - **E** PHEM-1970555 Specific Error Improvements 26.05 · To Do · 26.05 slipped
- **I** PHEM-1970182 RX Special Customers · To Do — branch: no planned release; 0 planned / 1 slipped / 1 unplanned _(counted under Not in the six areas)_
  - **E** PHEM-1970183 Tenant Centralization - PwC and All 26.06 · To Do · Backlog
- **E** PHEM-2262596 Feature flag Revamp · To Do · OffCycle-2026 (~2.3 mo) — branch: latest OffCycle-2026 (~2.3 mo); 3 planned / 0 slipped / 0 unplanned
  - **S** PHEM-2396537 Settings nav revamp — group settings + search · To Do · OffCycle-2026 (~2.3 mo)
  - **S** PHEM-2262679 Jobs Feature Flag revamp · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2104076 5. Tenant-Level Notification Configuration · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 3 unplanned
- **E** PHEM-1856531 Enhance Survey forms product in CRM and flowstudio · To Do — branch: no planned release; 0 planned / 0 slipped / 3 unplanned _(counted under Not in the six areas)_
  - **S** PHEM-1856957 Add Surveys into CRM and make form creation self configuration · To Do · Backlog
- **E** PHEM-1587500 Product bugs reduction · To Do — branch: no planned release; 0 planned / 2 slipped / 0 unplanned _(counted under Not in the six areas)_
  - **S** PHEM-1694112 in provisioning flow in tenant name has to be considered instead of customer name · To Do · 25.03 slipped
- **E** PHEM-1354652 Availability Management · To Do — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1697756 Field Management HRIT integration for selecting weekday/weekend days · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-1353262 RX Core Support Ticket Reduction · To Do — branch: latest 26.11 (~1.2 mo); 1 planned / 0 slipped / 11 unplanned _(context: outside filter)_
  - **S** PHEM-2215062 Update error messages for documents handling on projects · Development · 26.11 (~1.2 mo)
  - **S** PHEM-1950567 Refactor CRM Tenant Provisioning Flow · Development · Backlog
- **E** PHEM-570627 Build Candidate NPS to capture the overall hiring experience · In Progress — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-1507369 NPS Reminder Configuration & Smart Suppression · To Do · Backlog
- **E** PHEM-521185 Enhance Agency module in CRM · In Progress — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2056461 Bulk Upload configurations for Agency Recruiter · Story Elaboration · Backlog
- **E** PHEM-55375 Field management in RX · Done — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-1873654 Filterable fields APIs from field management · Development · OffCycle-2026 (~2.3 mo)
  - **S** PHEM-1697297 Location field from backend in UI in field management · To Do · Backlog
- **S** PHEM-1403720 Fit Score - Please turn feature flag on in staging environment for Saks · To Do · 21.11 slipped

## Not in the six areas

135 items (I 12 · E 24 · S 99). Planned 12 · slipped 14 · unplanned 109. Latest planned release: 27.01 (~3.3 mo). Pace estimate: 8–10.6 team-months for 99 open stories.

- **I** PHEM-2506130 Audit Log Console · To Do · 27.01 (~3.3 mo)
- **I** PHEM-2412940 Siemens Healthineers Requirements on product improvements for CRM Core · To Do · 26.11 (~1.2 mo) — branch: latest 26.11 (~1.2 mo); 3 planned / 1 slipped / 0 unplanned
- **I** PHEM-2306172 Executive Recruiting · To Do · Backlog
- **I** PHEM-2252378 RX - Disney Enhancements - Phase 2 by Sept. 20 · To Do · Backlog — branch: latest OffCycle-2026 (~2.3 mo); 7 planned / 0 slipped / 2 unplanned
- **I** PHEM-2018552 Schema-Driven UI (SDUI) for CRM · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 29 unplanned
  - **E** PHEM-2026330 CRM Candidates SDUI (list and detail) · In Progress · Backlog — branch: no planned release; 0 planned / 0 slipped / 6 unplanned
    - **S** PHEM-2026338 BFF integration and UX states · To Do · Backlog
    - **S** PHEM-2026337 Domain nodes and lazy resolvers · To Do · Backlog
    - **S** PHEM-2026336 Detail schema candidate.detail.default · To Do · Backlog
    - **S** PHEM-2026335 List schema candidate.list.default · To Do · Backlog
    - **S** PHEM-2026331 Domain model and EntityPack · To Do · Backlog
  - **E** PHEM-2024961 CRM consumption (runtime integration) · In Progress · Backlog — branch: no planned release; 0 planned / 0 slipped / 8 unplanned
    - **S** PHEM-2026340 SDUI platform npm package (Jobs + Candidates) · To Do · Backlog
    - **S** PHEM-2024967 Performance guardrail · To Do · Backlog
    - **S** PHEM-2024966 Contract and golden tests · To Do · Backlog
    - **S** PHEM-2024965 Observability · To Do · Backlog
    - **S** PHEM-2024964 Graceful degradation · To Do · Backlog
    - **S** PHEM-2024963 Feature flag: remote-first · To Do · Backlog
    - **S** PHEM-2024962 Configure remote base URL · To Do · Backlog
  - **E** PHEM-2024953 Schema editor (authoring UI) · In Progress · Backlog — branch: no planned release; 0 planned / 0 slipped / 5 unplanned
    - **S** PHEM-2024960 Diff vs last published (optional) · To Do · Backlog
    - **S** PHEM-2024958 Save draft · To Do · Backlog
    - **S** PHEM-2024957 Structured helpers (optional MVP slice) · To Do · Backlog
    - **S** PHEM-2024956 JSON editor with validation · To Do · Backlog
  - **E** PHEM-2024863 Page schema API (storage & delivery) · In Progress · Backlog — branch: no planned release; 0 planned / 0 slipped / 9 unplanned
    - **S** PHEM-2026559 Schema classification · To Do · Backlog
    - **S** PHEM-2024952 Operational readiness · To Do · Backlog
    - **S** PHEM-2024951 Audit trail · To Do · Backlog
    - **S** PHEM-2024949 Server-side validation pipeline · To Do · Backlog
    - **S** PHEM-2024948 Publish draft · To Do · Backlog
    - **S** PHEM-2024947 Create and update draft · To Do · Backlog
    - **S** PHEM-2024946 Published schema GET contract · To Do · Backlog
- **I** PHEM-1992228 Consent · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **E** PHEM-1992235 Reconsent · To Do · Backlog
- **I** PHEM-1991264 CRM Core Product Bugs · To Do · 26.06 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
  - **E** PHEM-1991295 Offer Letter Fields · To Do · Backlog
- **I** PHEM-1987498 Notes · To Do · 26.06 slipped — branch: no planned release; 0 planned / 1 slipped / 2 unplanned
  - **E** PHEM-1987505 Note Associations · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 2 unplanned
- **I** PHEM-1987368 RX Views / Spotlights · To Do · 26.06 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
- **I** PHEM-1970552 RX Core Ad Hoc Support Tickets and Defects · To Do · 26.05 slipped
- **I** PHEM-1970182 RX Special Customers · To Do · 26.06 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
- **I** PHEM-1957943 RX Projects · To Do · 26.05 slipped — branch: no planned release; 0 planned / 3 slipped / 2 unplanned
  - **E** PHEM-1957993 Project Enhancements for High-Volume Sourcing · To Do · 26.05 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
    - **S** PHEM-1957994 Inline Dropdown Editing for Ratings and Tags · To Do · Backlog
- **I** PHEM-1698278 RX - Performance Optimizations · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 23 unplanned
  - **E** PHEM-1699697 Migrate Moment.js to Luxon · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 6 unplanned
    - **S** PHEM-1699703 Remove Moment.js Dependencies · To Do · Backlog
    - **S** PHEM-1699702 Migrate Components (Phase 2) · To Do · Backlog
    - **S** PHEM-1699700 Migrate Components (Phase 1) · To Do · Backlog
    - **S** PHEM-1699699 Migrate Date Utility Services · To Do · Backlog
    - **S** PHEM-1699698 Create DateUtilsLuxonService · To Do · Backlog
  - **E** PHEM-1699646 Change Detection & Template Performance · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 8 unplanned
    - **S** PHEM-1699696 Replace Pipes with Getters & Migrate *ngIf to @if · To Do · Backlog
    - **S** PHEM-1699695 Add trackBy to All *ngFor Loops · To Do · Backlog
    - **S** PHEM-1699694 Remove Function Calls from Templates · To Do · Backlog
    - **S** PHEM-1699651 Implement OnPush in Complex Components · To Do · Backlog
    - **S** PHEM-1699649 Implement OnPush in Components with Subscriptions · To Do · Backlog
    - **S** PHEM-1699648 Implement OnPush in Simple Components · To Do · Backlog
    - **S** PHEM-1699647 Audit Current Change Detection Strategy · To Do · Backlog
  - **E** PHEM-1699637 Remove jQuery Dependency · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 4 unplanned
    - **S** PHEM-1699644 Replace jQuery in Components (Phase 2) · To Do · Backlog
    - **S** PHEM-1699641 Replace jQuery in Components (Phase 1) · To Do · Backlog
    - **S** PHEM-1699638 Create DOM Utility Service · To Do · Backlog
  - **E** PHEM-1698277 Bundle Size Optimization - Lazy Load Heavy Dependencies · In Progress · Backlog — branch: no planned release; 0 planned / 0 slipped / 4 unplanned
    - **S** PHEM-1973954 Delete unused code · Development · Backlog
    - **S** PHEM-1870274 Optimize application constant files for treeshaking · Development · Backlog
    - **S** PHEM-1698284 Verify Lazy Loading Functionality · Story Ready · Backlog
- **I** PHEM-1388851 Disney - Email Template enhancement · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **E** PHEM-1388855 Conditional Widgets in Templates & Unified Messaging API · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
    - **S** PHEM-1382258 Core - Update payload to support unified Messaging API · To Do · Backlog
    - **S** PHEM-1382251 Core - Define entities & placeholders for Messaging templates · To Do · Backlog
- **E** PHEM-2496708 Epic: Agency Candidate Ownership Enhancement · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 4 unplanned
  - **S** PHEM-2496711 Story 1 - Ownership model – per-agency ownership window · To Do · Backlog
  - **S** PHEM-2496710 Story 2 - "Agency Ownership Validity" column with filters · To Do · Backlog
  - **S** PHEM-2496709 Story 3 - Agency Archives – read-only view of past submissions · To Do · Backlog
- **E** PHEM-2412480 CRM - Agency Recruiter Email Communication · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1983286 Communication Medium Between Recruiter and Agency in CRM · To Do · Backlog
- **E** PHEM-2394800 Handle Employee Identity Events Across Downstream Services · To Do — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2398582 Scheduling — Remap Employee Interview Schedule and History · To Do · Backlog
  - **S** PHEM-2394844 CRM — Remap Candidate Profiles and Referral References · To Do · Backlog
- **E** PHEM-2391093 [Disney] Split Weekly Availability into per-field groups (enable + knockout per question) · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2350122 Creation and Management of MBR and WBR Metrics - RX core and profile · To Do · 26.10 slipped — branch: no planned release; 0 planned / 1 slipped / 1 unplanned
  - **S** PHEM-2350340 Proposal of new metrics for MBR / WBR for RX core and profile · To Do · Backlog
- **E** PHEM-2270995 Enhancement for Agency module · To Do · OffCycle-2026 (~2.3 mo) — branch: latest OffCycle-2026 (~2.3 mo); 3 planned / 0 slipped / 0 unplanned
  - **S** PHEM-2271120 Client-Level Field Visibility - Manage Columns · To Do · OffCycle-2026 (~2.3 mo)
- **E** PHEM-2247948 User Interface Improvements in CRM - New PDS system · To Do · 26.09 slipped — branch: latest 26.11 (~1.2 mo); 3 planned / 1 slipped / 0 unplanned
  - **S** PHEM-2278439 [PDS Refresh CRM Core] Left Hand Navigation Bar in CRM with flexibility for users to move icons per their need · To Do · 26.11 (~1.2 mo)
  - **S** PHEM-2262912 [PDS Refresh CRM Core] All Actions from List page / Details page · To Do · 26.11 (~1.2 mo)
  - **S** PHEM-2262903 [PDS Refresh CRM Core] Add Note from List page and Details page · To Do · 26.11 (~1.2 mo)
- **E** PHEM-2188780 Filter notes by Job ID in the notes section · To Do · Backlog
- **E** PHEM-2178655 Handle localization across Phenom products using lokalise · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 2 unplanned
  - **S** PHEM-2179428 Migrate localization to lokalise · Story Ready · Backlog
- **E** PHEM-2172552 CRM Core adhoc issues · To Do · 26.07 slipped
- **E** PHEM-1951222 Interview Agent · Epic Ready — branch: no planned release; 0 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2006000 AI Interview Details - Column Management & Filtering · To Do · Backlog
  - **S** PHEM-2005934 AI Interview Agent Analytics/Reports · To Do · Backlog
- **E** PHEM-1916976 RX Localization · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 2 unplanned
- **E** PHEM-1856881 [RX Profile] Allianz – Candidate purge without application purge (anonymize, CRM removal & retain applications) · In Progress — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-2121528 Core – BE – Remove anonymized candidate from projects, Spotlights, Recent Search history - at least vet may not require work [P1] · To Do · Backlog
- **E** PHEM-1856531 Enhance Survey forms product in CRM and flowstudio · To Do · Backlog — branch: no planned release; 0 planned / 0 slipped / 3 unplanned
  - **S** PHEM-1856979 Show analytics at the form level · To Do · Backlog
- **E** PHEM-1587500 Product bugs reduction · To Do · 26.02 slipped — branch: no planned release; 0 planned / 2 slipped / 0 unplanned
- **E** PHEM-1566327 Signals enhancements · To Do · 26.03 slipped
- **E** PHEM-1483121 Candidate / Job Executive presentation materials · To Do — branch: no planned release; 0 planned / 0 slipped / 13 unplanned _(context: outside filter)_
  - **S** PHEM-1513195 Capture Executive Feedback on Reports · To Do · Backlog
  - **S** PHEM-1513194 Share Report via Secure Web Link · To Do · Backlog
  - **S** PHEM-1513192 Generate Metrics as Snapshot with Timestamp · To Do · Backlog
  - **S** PHEM-1513191 Display Recruiting Funnel Metrics · To Do · Backlog
  - **S** PHEM-1513189 Control Resume Inclusion in Reports · To Do · Backlog
  - **S** PHEM-1513187 Include Structured Candidate Detail Modules · To Do · Backlog
  - **S** PHEM-1513186 Control Candidate Ordering and Grouping · To Do · Backlog
  - **S** PHEM-1513184 Preview Executive Report Before Sending · To Do · Backlog
  - **S** PHEM-1513183 Generate Executive Summary Report · To Do · Backlog
  - **S** PHEM-1513181 Select Report Language and Localize Content · To Do · Backlog
  - **S** PHEM-1513178 Apply Business Unit Branding to Reports · To Do · Backlog
  - **S** PHEM-1513177 Configure Widgets and Custom Blocks · To Do · Backlog
  - **S** PHEM-1513110 Edit Existing Report Templates · To Do · Backlog
- **E** PHEM-1354652 Availability Management · To Do — branch: latest OffCycle-2026 (~2.3 mo); 2 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1479460 Candidate Availability MVP · To Do · Backlog
- **E** PHEM-1353262 RX Core Support Ticket Reduction · To Do — branch: latest 26.11 (~1.2 mo); 1 planned / 0 slipped / 11 unplanned _(context: outside filter)_
  - **S** PHEM-2267654 RX – FE – Clarify create-new-tag affordance in Tags UI · To Do · Backlog
  - **S** PHEM-2174697 Offboarding API improvements · To Do · Backlog
  - **S** PHEM-2087330 Migration of Counts topology to Flink Service · To Do · Backlog
  - **S** PHEM-1694111 Get Feature Notes query to get case insensetive on entity · To Do · Backlog
  - **S** PHEM-1566523 Notes issues as support ticket reduction · To Do · Backlog
  - **S** PHEM-1504025 Reordering of options issue for tranlations · To Do · Backlog
- **E** PHEM-832215 RX Projects · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1693767 Increase Column Limit in Projects Module · To Do · Backlog
- **E** PHEM-570627 Build Candidate NPS to capture the overall hiring experience · In Progress — branch: latest OffCycle-2026 (~2.3 mo); 1 planned / 0 slipped / 2 unplanned _(context: outside filter)_
  - **S** PHEM-2380351 Emoji Style Rating - Survey · To Do · OffCycle-2026 (~2.3 mo)
  - **S** PHEM-1506795 Embed Form Studio into CRM UI · To Do · Backlog
- **E** PHEM-395677 RX - Localization Framework · To Do — branch: no planned release; 0 planned / 0 slipped / 1 unplanned _(context: outside filter)_
  - **S** PHEM-1698115 Update incorrect translation for "Screening" · To Do · Backlog
- **S** PHEM-2318056 Allow decimals in salary grid for India and Srilanka Region · To Do · 26.06 slipped
- **S** PHEM-2314766 Default Workflow for projects is not getting generated for the new tenants · To Do · 26.06 slipped
- **S** PHEM-2288883 B2. RX – FE – Reuse HRM document viewer in CRM (view without download) · To Do · 26.11 (~1.2 mo)
- **S** PHEM-2285654 Field audit logs · To Do · OffCycle-2026 (~2.3 mo)
- **S** PHEM-2235741 Notes Schema Creation And validation · To Do · Backlog
- **S** PHEM-2219956 CRM - Add Eval Avg Rating field to candidate list · To Do · Backlog
- **S** PHEM-2219955 CRM - Filtering updates for scorecard results in candidate list · ON Hold · Backlog
- **S** PHEM-2014705 Not consuming years of experience as expected · To Do · Backlog
- **S** PHEM-2009286 Automation of dependency delta fields congestion into CRM · To Do · Backlog
- **S** PHEM-1984552 Add validation for Brand and Identifier fields and improve email template selection logic based on Brand + Identifier combination. · To Do · Backlog
- **S** PHEM-1982219 Sourcer Analytics Tracking · To Do · Backlog
- **S** PHEM-1982217 Interviewer Notification Controls · To Do · Backlog
- **S** PHEM-1982213 Customizable Notification Preferences · Story Grooming · Backlog
- **S** PHEM-1929736 Mongo DB sharding implementaiton · To Do · OffCycle-2026 (~2.3 mo)
- **S** PHEM-1692609 Grouped Fields Not Updating Automatically · Story Ready · Backlog
