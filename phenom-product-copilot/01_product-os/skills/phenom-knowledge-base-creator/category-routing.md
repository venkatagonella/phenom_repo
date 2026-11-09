# Category routing — where a Community article belongs

Route on two signals: **what the article is about** and **which team owns the capability**. Product area decides the knowledge base; the team confirms it when an article could plausibly sit in two places.

Category IDs shift as the tree is reorganised. Always confirm before staging:

```bash
python3 scripts/kb_draft.py categories --kb <id>
```

---

## Step 1 — Knowledge base, by product area and owning team

| Article is about | Knowledge base | kb_id | Typical owning team |
|------------------|----------------|-------|---------------------|
| Recruiter workflows, pipelines, projects, candidate records, sourcing, campaigns | **CRM** | 3 | Recruiter Experience (RX) |
| Screening questionnaires, video/voice screening, evaluations | **Screening** | 29 | Screening |
| Interview scheduling, recording, playback, evaluation, debriefs | **Interview Experience** | 36 | Interview Intelligence / Scheduling |
| Dashboards, reports, metric definitions, exports | **Analytics** | 2 | Talent Analytics |
| Career site, job pages, SEO, CMS / Design Studio | **Career Site and Design Studio** | 8 | CIM / CX |
| Hiring manager portal, HM tasks, HM feedback | **Hiring Manager** | 11 | Hiring Manager |
| Internal mobility, referrals, gigs, mentoring, career pathing | **Employee Experience** | 22 | Employee Experience |
| Chatbot configuration, intents, Talent Companion | **Phenom Bot** | 12 | Phenom Bot |
| Agentic AI capabilities, Voice Agent | **AI Agents** | 52 | AI |
| Release notes and changelog | **Product Release Notes** | 31 | Product Marketing / owning PM |
| Not ready for a live KB, or the target category doesn't exist yet | **Article Drafts (INTERNAL)** | 20 | Author |

Cross-team articles: file under the KB matching **the surface the reader is looking at**, not the team that built the backend. A LinkedIn integration article that a recruiter reads inside the CRM belongs in CRM, even though Integration Experience owns the connector. Cross-link to the other team's article instead of duplicating it.

For the fuller capability-to-team map, see `policies/platform-routing.md`.

---

## Step 2 — Category within the knowledge base

### CRM (kb 3) — most common for RX work

| Subject | Category | ID |
|---------|----------|-----|
| Candidate records, profiles, adding candidates | Candidate Management | 88 |
| LinkedIn CRM Connect | Candidate Management > LinkedIn CRM Connect | 970 |
| Employee profiles and referrals in CRM | Candidate Management > Employee Profiles & Referrals | 248 |
| Projects and project setup | Projects | 94 |
| Job requisitions in CRM | Job Management | 93 |
| Pipeline stages and hiring workflow | Hiring Pipeline | 625 |
| Automations, triggers, workflows | Automations | 101 |
| Tenant settings, admin configuration | Settings & Configurations | 102 |
| User roles and permissions | Access & User Roles | 189 |
| Email campaigns and 1:1 email | Email - 1:1 & Campaigns | 183 |
| SMS campaigns and 1:1 SMS | SMS - 1:1 & Campaigns | 184 |
| WhatsApp | WhatsApp | 185 |
| Search and filters | Search | 336 |
| Spotlights and candidate lists | Spotlights & Lists | 89 |
| Tags | Tags | 238 |
| Events and university recruiting | Events & University Recruiting | 90 |
| Talent community | Talent Community | 98 |
| AI features inside CRM | Artificial Intelligence (AI) | 178 |
| Orientation for new CRM users | Basics & Getting Started | 249 |
| Notes on candidate profiles | Notes | 97 |

### Screening (kb 29) — the house-style reference

| Subject | Category | ID |
|---------|----------|-----|
| What it is, benefits, getting started | Product Overview | 779 |
| Recruiter / candidate / HM workflows | Product Functionality | 82 |
| Setup, roles, integrations | Setup & Configuration | 81 |
| FAQs, privacy, support, analytics | Support, Security and Others | 83 |
| Voice Agent | Voice Agent (Beta) | 860 |

### Interview Experience (kb 36)

| Subject | Category | ID |
|---------|----------|-----|
| Scheduling meetings | Schedule Meetings | 987 |
| Running meetings | Conduct Meetings | 856 |
| Reviewing recordings and evaluations | Review Meetings | 483 |
| Interview setup | Interview Setup and Configuration | 554 |
| Scheduling setup | Scheduling Setup and Configuration | 732 |
| Templates and libraries | Templates and Libraries | 565 |

### Other knowledge bases

| KB | Categories |
|----|-----------|
| **Analytics** (2) | Getting Started 103 · Reports 493 · Custom Dashboard 107 · Recruiter Experience 138 · Candidate Experience 110 · Manager Experience 196 · Employee Experience 128 · Talent Marketing 122 |
| **Career Site** (8) | Career Site 323 · Design Studio (CMS) 507 · SEO 330 |
| **Hiring Manager** (11) | Overview 31 · Candidate Management 33 · Hiring Manager FAQs 212 · Settings, Configurations & Permissions 161 · Task Management 846 · For Recruiters 366 |
| **Employee Experience** (22) | Internal Mobility 164 · Referrals 165 · Gigs 167 · Mentoring 166 · Career Pathing 168 · Learning 171 · EX FAQs 306 · Configuration 173 |
| **Phenom Bot** (12) | Chatbot Basics 332 · Bot Settings 176 · Chatbot FAQs 333 · Talent Companion 670 |
| **Article Drafts (INTERNAL)** (20) | CRM 233 · Screening 418 · Scheduling 419 · Interview Intelligence 470 · GDPR 232 · Security, Privacy & Compliance 601 · Career Site and CMS 428 |

---

## Step 3 — Sanity checks before staging

- **Does a sibling already cover this?** Search the category first; a new version of an existing article often beats a new one.
- **Would a reader look here?** Categories are navigation, not org chart.
- **Does the article type match its neighbours?** An FAQ dropped among setup guides usually signals the wrong category.
- **No good fit?** Stage into Article Drafts (INTERNAL) (kb 20) and flag that a new category may be needed — don't force it somewhere plausible-but-wrong.
