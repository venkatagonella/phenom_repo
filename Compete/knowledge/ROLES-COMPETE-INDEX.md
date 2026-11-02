# Roles across competing companies — reading list

Vendors covered in this workspace / chat: **Workday**, **SAP SuccessFactors**, **Greenhouse**, **Ashby**, **Workable**, **Personio** (plus Phenom CRM for mapping).

Use this file as the single entry point for **hiring-team roles / personas**, not only job-lifecycle states.

## Skills to load

| Skill | Path | Use for |
|-------|------|---------|
| **phenom-master-router** | `.cursor/skills/phenom-master-router/SKILL.md` | Pick the right pack |
| **competitor-job-lifecycle** | `.cursor/skills/competitor-job-lifecycle/SKILL.md` | Job/req/posting lifecycle by vendor |
| **hypercell** | `.cursor/skills/hypercell/SKILL.md` | Industry×Function×Role×Workflow×Geo personalization (role *family* being hired + persona overlay) |
| Compete local copy | `Compete/.cursor/skills/competitor-job-lifecycle/SKILL.md` | Same skill when working inside Compete/ |

## Rules

| Rule | Path |
|------|------|
| Compete knowledge (always on in Compete) | `Compete/.cursor/rules/compete-knowledge.mdc` |
| Job lifecycle concepts | `.cursor/rules/phenom-job-lifecycle.mdc` / `Compete/.cursor/rules/phenom-job-lifecycle.mdc` |

## Knowledge packs (authoritative data)

| Pack | Path | Role-relevant content |
|------|------|------------------------|
| **Index** | `Compete/knowledge/INDEX.md` | Start here |
| **Personas + JTBD** | `Compete/knowledge/personas-jtbd.md` | Canonical personas + vendor name map + JTBD flows |
| **Core + Hypercell JTBD** | `Compete/knowledge/roles-jtbd-core-hypercell.html` | Sourcer / Recruiter / Lead — Core vs Hypercell JTBD |
| Job lifecycle JSON | `Compete/knowledge/job-lifecycle/data/competitor-lifecycles.json` | Per-vendor entity + sequence (who acts is in personas pack) |
| Lifecycle comparison | `Compete/knowledge/job-lifecycle/docs/lifecycle-comparison.md` | Vendor sequences & states |
| Posting concepts | `Compete/knowledge/job-lifecycle/docs/posting-publishing-expiry-unposting.md` | Do not conflate publish/unpost/close |
| Phenom domain model | `Compete/knowledge/job-lifecycle/docs/phenom-recommended-domain-model.md` | Job → Posting → Channel |
| Mermaid diagrams | `Compete/knowledge/job-lifecycle/diagrams/job-lifecycles.mmd` | Sequences |
| Analysis prompt | `Compete/knowledge/job-lifecycle/prompts/competitor-analysis-prompt.md` | Output contract |
| Hypercell reference | `.cursor/skills/hypercell/reference.md` | Dimension detail + Crawl/Walk/Run |

## Session canvases (chat synthesis — Phenom + compete)

Located under Cursor project canvases for Compete (not in git packs):

| Canvas | Content |
|--------|---------|
| `recruiter-sourcer-lead-jtbd.canvas.tsx` | Recruiter / Sourcer / Lead JTBD + vendor labels |
| `hiring-personas-jtbd.canvas.tsx` | Broader hiring personas |
| `recruiter-jtbd-workflow.canvas.tsx` | Recruiter Own→Close stages |
| `persona-crm-page-access.canvas.tsx` | Phenom CRM must-see / must-not by persona |
| `persona-effectiveness-krs.canvas.tsx` | Combined KRs for R / S / Lead |
| `persona-intelligence-capabilities.canvas.tsx` | Intelligence capabilities by persona |

Path pattern: `~/.cursor/projects/Users-venkata-gonella-phenom-repo-Compete/canvases/`

## Vendor role name cheat sheet

From `personas-jtbd.md` (config-dependent; verify tenant docs before external claims):

| Canonical persona | Workday | SuccessFactors | Greenhouse | Ashby | Workable | Personio |
|-------------------|---------|----------------|------------|-------|----------|----------|
| Recruiter | Recruiter / Primary Recruiter | `R` (+ `W` second) | Recruiter | Recruiter | Recruiter | Recruiting-app editor / lead |
| Sourcer | Recruiting Sourcer | `S` | Sourcer | Sourcer | Usually folded into Recruiter | Not first-class |
| Coordinator | Recruiting Coordinator | `T` | Coordinator | Recruiting Coordinator | Often Recruiter | Often recruiter / team member |
| Hiring Manager | Hiring Manager | `G` | Hiring Manager | Hiring Manager | Hiring Manager | Hiring-team role |
| Recruiting Admin / Lead-like | Recruiting Administrator | Recruiting Admin | Site Admin | Organization Admin | Admin / Super Admin | Administrator / lead recruiter |
| Interviewer | (panel) | (interviewers) | Basic / Interviewer | Limited Access / Interviewer | Candidate Reviewer / Hiring Contributor | Interviewer on team |
| Approver | BP approvers | Route map / `O` / `Q` | Job approval (if on) | Job approval (if on) | Hiring Plan | Platform approvals |
| Agency | Portal / integration | Portal / integration | Portal / integration | Agency / External | External Recruiter | External + restricted role |

**Coverage note:** Sourcer + Coordinator are first-class on WD, SF, GH, Ashby. Workable and Personio usually fold that work into Recruiter / custom roles.

**Product takeaway:** Model **persona (relationship/tasks)** separately from **permission (what they can do)** — strongest on Greenhouse, Ashby, Workable, Personio; Workday/SF use security groups vs operators.

## Phenom mapping (from chat)

| Compete persona | Phenom surface |
|-----------------|----------------|
| Recruiter | CRM Recruiter → Primary Recruiter on job (granular hiring-team) |
| Sourcer | CRM Sourcer (+ job-level Sourcer when enabled) |
| Recruitment Lead | Analytics **Recruiter Manager** (+ CRM Recruiter if they assign) — not a CRM hiring-team label today |

## Recommended read order (roles)

1. This file  
2. `personas-jtbd.md`  
3. `roles-jtbd-core-hypercell.html`  
4. Skill **competitor-job-lifecycle** + `competitor-lifecycles.json` (lifecycle context)  
5. Skill **hypercell** (when scoping intelligence to a hiring cell + persona overlay)  
6. Session canvases for Phenom CRM ACL / KRs / intelligence if building product
