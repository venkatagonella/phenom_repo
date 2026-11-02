---
name: hypercell
description: >-
  Applies Phenom's Hypercell framework — Industry × Function × Role × Workflow ×
  Geography personalization with constraints, ontology, outcomes, and Crawl/Walk/Run
  maturity. Use when the user mentions hypercell, hypercell matrix, decomposing a
  hiring segment, FitScore hypercell config, persona×role playbooks, or wants
  intelligence/automation scoped to a precise hiring cell rather than a whole
  industry.
---

# Hypercell

Phenom's unit of **platform-level personalization**: adjust experiences, agents,
FitScore, messaging, and workflows from a **composable set of contextual dimensions**
— not from industry alone.

Canonical source deck: [Team #1 — Hypercell Architecture](https://docs.google.com/presentation/d/1AHJQc9poqQYvnKqJokO0HiuniZKRaSj5AUHuhvBpdwY) ("The Hypercell Matrix").

## When to use

- Define or review a hypercell for a customer / role family
- Scope intelligence, automations, or agents to a precise hiring segment
- FitScore or matching config per cell (Industry × Function × Role × Workflow × Geo)
- Move a problem statement from "industry-wide" → vertical → **hypercell-level precision**

## Core dimension model (the matrix)

A hypercell is the intersection of these **five primary dimensions**:

| # | Dimension | What it answers | Examples from the deck |
|---|-----------|-----------------|------------------------|
| 1 | **Industry** | What business / regulated domain? | Manufacturing in Healthcare; Healthcare Compliance & Digital Health; Retail |
| 2 | **Function** | Which org capability / department? | Quality Assurance; R&D; Quality Systems & Regulatory (AQR); Airport Ops |
| 3 | **Role** | Which job family / title cluster? | Quality Engineer/Specialist; Clinical Research Scientist; Store Associate; Flight Attendant; Order Filler |
| 4 | **Workflow** | How does hiring behave here? | High volume / shortage / compliance; Professional & Moderate Volume; Critical Demand; Professional / Technical |
| 5 | **Geography** | Where do rules and labor markets apply? | USA; Mexico; North America; California-specific posting; Tier-2 city |

**Naming pattern:**  
`{Industry} · {Function} · {Role} · {Workflow} · {Geography}`  
Example: `Manufacturing in Healthcare · Quality Assurance · Quality Engineer · Professional Moderate Volume · USA`

### Supporting layers (not the five axes, but required to operationalize)

| Layer | Purpose |
|-------|---------|
| **Pain points** | Business problem + evidence (Gong, Customer 360, CRM/Analytics/Looker), roles & geos **backed by numbers** |
| **Atomic units** | Discrete hiring jobs the cell must execute (e.g. source certified talent, screen before interview, follow up on offers) |
| **Outcomes / metrics** | What success means for *this* cell (e.g. Time-to-Offer, Offer-Ratio, Hire rate Hired/Offered) |
| **Constraints** | Hard gates (regulatory, safety, travel %, cybersecurity standards, pay transparency by state) |
| **Ontology** | Structured attributes used by FitScore / screening / JD (certs, skills, education, location, schedule, job type, specialization, salary budget) |
| **Persona overlay** | Who acts in the product (Recruiter, Sourcer, Recruitment Lead, HM) — same cell, different UI/agent verbs |
| **Maturity** | **Crawl \| Walk \| Run** automation depth for the same cell |

Do **not** call a vague industry problem a hypercell. Hypercell-level precision names **role + moment + geo/workflow** (and preferably persona).

## Agent workflow

When asked to build or analyze a hypercell, run these steps (from the deck exercise):

### Step 1 — Ground in customer evidence
Pull pain points from Customer 360, Gong, Phusion X+, Workforce Intelligence, CRM/Analytics/Looker. Prefer quantified volume (apps, hires, locations).

### Step 2 — Identify pain points → roles → geos
For each pain point: business problem, what breaks, downstream impact, evidence sources, **impacted roles**, **applicable geos** — both backed by data.

### Step 3 — Decompose the hypercell
Fill the five dimensions + list **atomic units** (and why each matters for this cell).  
Optional: group into a **Critical Demand Hiring Segment** when regulatory/urgency dominates.

### Step 4 — Define outcomes
Pick cell-specific metrics (examples from deck: Time-to-Offer; Offer-Ratio; hire-rate drop after offer).

### Step 5 — Define constraints
Map constraint type → rule (e.g. 21 CFR Part 820; 10-panel drug screen; ALCOA+; IEC 62304 / Part 11; CA pay transparency).

### Step 6 — Define ontology
Certifications, Skills/Competencies, Salary Budget, Education, Location, Work Schedule, Job Type, Specialization — enough for FitScore weights, knockout questions, and JD.

### Step 7 — Crawl | Walk | Run
Design three maturity workflows for the **same** hypercell (same dimensions), increasing agent/automation depth. Measure impact (time-to-screen, recruiter hours saved, time-to-interview, time-to-source).

Copy this checklist:

```
Hypercell Progress:
- [ ] Evidence & pain points quantified
- [ ] Five dimensions named
- [ ] Atomic units listed
- [ ] Outcomes / KRs set
- [ ] Constraints mapped
- [ ] Ontology fields defined
- [ ] Crawl / Walk / Run sketched
- [ ] Persona overlay noted (who uses which atomic units)
```

## Output template

```markdown
# Hypercell: <Name>

## Dimensions
| Dimension | Value |
|-----------|-------|
| Industry | |
| Function | |
| Role | |
| Workflow | |
| Geography | |

## Pain points (evidence-backed)
1. …

## Atomic units
- …

## Outcomes / metrics
- …

## Constraints
| Type | Constraint |
|------|------------|
| | |

## Ontology
| Attribute | Requirement |
|-----------|-------------|
| Certifications | |
| Skills | |
| Education | |
| Location | |
| Work schedule | |
| Job type | |
| Specialization | |
| Salary / pay transparency | |

## Crawl | Walk | Run
| Stage | Flow summary | Primary agents/automations | Target impact |
|-------|--------------|----------------------------|---------------|
| Crawl | | | |
| Walk | | | |
| Run | | | |

## Persona overlay
| Persona | Atomic units they own | Must not do |
|---------|----------------------|-------------|
| Sourcer | | |
| Recruiter | | |
| Recruitment Lead | | |
```

## Precision ladder (use when sharpening a problem)

| Level | Example quality |
|-------|-----------------|
| Industry-wide | "Candidate engagement is low" |
| Vertical | "Retail hourly candidates don't respond to outreach" |
| **Hypercell** | "Retail hourly · Store Associate · High volume · Tier-2 city · 48h post-apply · SMS-preferring re-applicant — generic email from shared inbox" |

## Guardrails

- Always fill all **five** primary dimensions before recommending product/agent design.
- Geography changes constraints and ontology (e.g. California QA posting rules ≠ Mexico volume hiring).
- Workflow is about **hiring behavior** (volume, shortage, compliance, professional), not just ATS stage names.
- Crawl/Walk/Run must keep the **same** hypercell identity; only automation depth changes.
- Cite the source deck when stating the matrix definition.

## Related detail

- Full exercise examples, ontology list, and Crawl/Walk/Run illustrations: [reference.md](reference.md)
- FitScore product mapping (same 5 axes): Phenom epic language *Industry × Function × Role × Workflow × Geography*
- Compete persona JTBD packs: `Compete/knowledge/` + **competitor-job-lifecycle** when comparing ATS roles
