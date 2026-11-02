# Hiring personas and jobs to be done

Combined from Workday, SAP SuccessFactors, Greenhouse, Ashby, Workable, and Personio product docs, help centers, and knowledge bases. Vendor workflows are configurable; names below are the common pattern, not a claim that every tenant is identical.

**Sources:** Workday Recruiting security and subprocess docs; SAP SuccessFactors recruiting operators; Greenhouse hiring team and task docs; Ashby user permissions and hiring team; Workable recruiting access levels; Personio recruiting roles and external recruiter docs.

## Canonical personas

Across all six platforms, hiring work clusters into these people. Vendors use different labels for the same job.

| Canonical persona | Core job | Typical vendor names |
|---|---|---|
| Hiring Manager | Get a qualified person onto my team | Workday Hiring Manager; SF `G`; Greenhouse / Ashby / Workable Hiring Manager; Personio hiring-team role (often named Hiring Manager) |
| Recruiter | Fill the job on time with a fair process | Workday Recruiter / Primary Recruiter; SF `R` (and `W` second recruiter); Greenhouse Recruiter; Ashby Recruiter; Workable Recruiter; Personio recruiting-app editor / lead recruiter |
| Recruiting Coordinator | Keep interviews and candidate logistics moving | Workday Recruiting Coordinator; SF `T`; Greenhouse Coordinator; Ashby Recruiting Coordinator |
| Sourcer | Build a pipeline before and after a job is posted | Workday Recruiting Sourcer; SF `S`; Greenhouse Sourcer; Ashby Sourcer |
| Interviewer / Reviewer | Give a useful yes/no on a candidate | Greenhouse Basic user; Ashby Limited Access; Workable Candidate Reviewer / Hiring Contributor; Personio interviewer on a hiring team |
| Approver | Control headcount, budget, and offer risk | Workday business-process approvers; SF route map / Originator `O` / VP HR `Q`; Workable Hiring Plan; Greenhouse / Ashby job approval if configured |
| HR Partner | Keep hiring aligned with policy and the employee record | Workday HR Partner; SF VP HR `Q`; Personio HR manager with recruiting access |
| Recruiting Admin | Make the system match how the company hires | Workday Recruiting Administrator; SF Recruiting Admin; Greenhouse Site Admin; Ashby Organization Admin; Workable Admin; Personio Administrator |
| Agency Recruiter | Submit only my agency’s candidates | Workable External Recruiter; Ashby Agency / External Recruiter; Personio external employee + recruiting role |
| Candidate | Find a relevant job and complete the process | Career site / Candidate Home on all six |

Coordinator and sourcer are first-class on Workday, SuccessFactors, Greenhouse, and Ashby. Workable and Personio usually fold that work into Recruiter, Hiring Contributor, or a custom recruiting role.

## Combined hiring flow

One end-to-end flow. Each step shows who typically owns it.

```text
Need a hire
  → Hiring Manager / Recruiter: create job or requisition
  → Approver / HR Partner: approve headcount and budget
  → Recruiter: open job, create posting, publish to channels
  → Sourcer: find prospects; Agency: submit agency candidates
  → Candidate: apply
  → Recruiter: screen and advance or reject
  → Hiring Manager: review shortlist
  → Coordinator: schedule interviews
  → Interviewer: meet candidate and submit scorecard
  → Recruiter + Hiring Manager: decide
  → Recruiter: draft offer; Approver / HR / Compensation: approve
  → Candidate: accept or decline
  → Recruiter / Admin: mark hired, fill opening, unpost or close job
```

A posting can expire or be unpublished while the job stays open. Closing the job is a stronger action than removing one listing.

## Jobs to be done by persona

Each persona has one job statement, then the simple flow they run.

### 1. Hiring Manager

**Job:** When I have work my team cannot cover, I want to define the role and choose the person, so I can fill the seat without becoming the recruiter.

1. Request or create the job / requisition (sometimes originator).
2. Confirm title, openings, location, and must-have skills.
3. Wait for approval, or approve if I am also an approver.
4. Review the recruiter’s shortlist (Greenhouse Hiring Manager Review stage).
5. Interview and score the finalists.
6. Decide hire or reject.
7. Confirm offer details I am allowed to see (salary is often Recruiter / Hiring Manager only).
8. Confirm the opening is filled.

Workday often treats the hiring manager as owner of the requisition. Greenhouse treats them as the subject-matter expert for the interview, not the process owner. Workable hiring managers can see offers but cannot publish jobs directly.

### 2. Recruiter

**Job:** When a job is approved, I want to run intake through hire, so a qualified candidate is hired on time without breaking process.

1. Take ownership of the approved job (Primary Recruiter / responsible recruiter).
2. Complete job setup: hiring team, interview plan, scorecards.
3. Create posting and publish internal / external / channels.
4. Source, review applications, advance or reject.
5. Hand scheduling to the coordinator when one exists.
6. Drive hiring-manager review and interviewer feedback.
7. Draft the offer and route approval.
8. Unpost, fill openings, close or reopen the job.

Greenhouse assigns application review, advance/reject, scorecard reminders, and take-home tests to the recruiter. Ashby separates hiring-team *relationship* from *permission* to act. SuccessFactors can have a second recruiter (`W`).

### 3. Recruiting Coordinator

**Job:** When candidates are ready to meet the team, I want to schedule and communicate cleanly, so interviews happen and candidates are not left waiting.

1. Inherit the application (job-level default, changeable per candidate).
2. Schedule interviews and send kits / calendar holds.
3. Be the frontline contact for logistics.
4. Track no-shows and reschedules.
5. Hand the candidate back to the recruiter after the stage.

Workday: interview scheduling and offer paperwork. Greenhouse: scheduling tasks only, and those default tasks cannot be edited. Ashby: Recruiting Coordinator on job, opening, or application. Workable/Personio: usually a recruiter or hiring-team member with interview permissions.

### 4. Sourcer

**Job:** When we will need talent (sometimes before a requisition exists), I want to find and engage people, so recruiters have a pipeline ready.

1. Search and outreach (often Chrome extension / sequences).
2. Add prospects, not only applicants.
3. Tag source and keep the person warm.
4. Hand off to the recruiter when a job is open.
5. Stop when the job is filled or paused.

First-class on Workday, SuccessFactors, Greenhouse, and Ashby. Greenhouse gives sourcers no default system tasks. Ashby Hiring Manager (or higher) is required for the Chrome extension. Phenom CRM is adding Sourcer as a distinct hiring-team role for the same reason.

### 5. Interviewer / Reviewer

**Job:** When I am asked to assess someone, I want just enough context to give a clear recommendation, so the hiring team can decide without me living in the ATS.

1. Receive interview or review assignment.
2. Read the briefing / resume (often cannot see the full pipeline).
3. Meet the candidate or review the application.
4. Submit a scorecard or evaluation.
5. Leave. Do not move stages, send offers, or see salary.

Ashby Limited Access: interview briefing and feedback only. Workable Candidate Reviewer: evaluate and comment only. Workable Hiring Contributor: can email candidates but not see offers. Greenhouse Basic users interview without being on the hiring team.

### 6. Approver

**Job:** When the company is about to spend headcount or compensation, I want a clear yes/no, so we do not hire off-budget or off-policy.

1. Receive a requisition or offer task.
2. Check openings, cost center, and level.
3. Approve, send back, or deny.
4. For offers, review pay, bonus, and equity if in scope.
5. Recruiter continues only after approval.

Workday routes these as business-process steps (manager, HR Partner, Compensation Partner). SuccessFactors uses a route map on the requisition. Workable Hiring Plan has requisition owner vs requisition hiring manager. Greenhouse and Ashby may require job approval before Open.

### 7. HR Partner

**Job:** When hiring touches the employee record, I want policy and data to stay correct, so the hire can become a worker without cleanup later.

1. Advise on requisition fields and org assignment.
2. Approve or validate offers against pay equity / policy.
3. Confirm ready-for-hire / pre-hire conversion.
4. Hand off to onboarding.

Strongest on Workday and SuccessFactors. Personio HR managers often sit in recruiting because HR and ATS are one product. Lighter as a named hiring-team role on Greenhouse, Ashby, and Workable.

### 8. Recruiting Admin

**Job:** When the company changes how it hires, I want roles, templates, and permissions to match, so every other persona sees only what they need.

1. Configure job / requisition templates and approval chains.
2. Define hiring-team roles and access (Job Admin levels, access roles, permission sets).
3. Set career site, posting channels, and offer templates.
4. Manage confidential jobs and private fields.
5. Report across jobs, not one pipeline.

Workday: unconstrained Recruiting Administrator plus role-based constrained groups. Greenhouse: Site Admin vs Job Admin vs Basic. Ashby: Organization Admin vs Elevated vs Limited; hiring team does not by itself grant permission. Workable: Admin / Super Admin plus optional permission sets. Personio: platform roles plus recruiting roles on a job or application.

### 9. Agency Recruiter

**Job:** When I am contracted to fill a job, I want to submit my candidates only, so I can be measured without seeing the client’s full pipeline.

1. Get invited to a specific job.
2. Upload candidates into Applied / Sourced (or equivalent).
3. See and manage only those candidates.
4. Comment or email if allowed.
5. Cannot see career-site applicants, other agencies, evaluations, or employee data.

Workable and Ashby are explicit. Personio: tracking channel without login, or external employee profile with a restricted recruiting role. Workday / SuccessFactors / Greenhouse typically use agency portals or integrations.

### 10. Candidate

**Job:** When I want a new role, I want to find a relevant job and complete each step without repeating myself, so I can get an offer or a clear no.

1. Discover the job (career site, board, referral, direct link).
2. Apply (internal or external).
3. Complete tasks: assessments, scheduling, documents.
4. Interview.
5. Accept or decline offer.
6. If the posting is unlisted, apply via direct link; if unpublished or expired, cannot apply.

Workday Candidate Home; all six have career sites. Ashby Listed vs Unlisted vs Unpublished matters for whether a hidden link still works.

## Product takeaway

Model **personas separately from permissions**. Greenhouse, Ashby, Workable, and Personio all say: hiring-team role = relationship and tasks/notifications; permission level = what the person can actually do. Workday and SuccessFactors encode the same split as security groups vs operators on a requisition.
