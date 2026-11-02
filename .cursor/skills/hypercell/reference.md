# Hypercell — reference

Source: [Team #1 — Hypercell Architecture](https://docs.google.com/presentation/d/1AHJQc9poqQYvnKqJokO0HiuniZKRaSj5AUHuhvBpdwY) (title slide: **The Hypercell Matrix**).

## Why hypercells exist

Customer stories in the deck (DHL, Elara, United, CVS, Verisure, Disney, Merck, IRC) show the same pattern: **hiring automation and agents must run differently by role and context**. One global playbook fails when:

- Volume and knockout rules differ (frontline vs professional)
- Geography changes compliance and posting language (California QA vs Mexico volume)
- Workflow strategy differs (Precision & Speed vs Conversion & Scaling)

A **hypercell** is the smallest useful unit where Industry, Function, Role, Workflow, and Geography are fixed so agents, FitScore, messaging, and automations can be tailored.

## Primary dimensions (detail)

### 1. Industry
Business / regulated domain of the employer segment.

Deck examples:
- Manufacturing in Healthcare
- Healthcare Compliance & Digital Health
- Retail (store hiring)
- Consumer / hospitality (Disney cast)
- Logistics / supply chain (DHL)

### 2. Function
Org capability or department the role sits in.

Deck examples:
- Quality Assurance
- Research & Development
- Quality Systems & Regulatory Compliance (AQR)
- Manufacturing Operations / Supply Chain
- Airport Operations / Inflight / Campus

### 3. Role
Concrete job family or title cluster (often plural titles under one cell).

Deck examples:
- Quality Engineer / Specialist; Software Quality Engineer; CAPA Professional; Supplier Quality Manager
- Clinical Research Scientist / CRA
- Store Associate, Cashier, Flight Attendant, Order Filler / Picker

### 4. Workflow
Hiring **behavior pattern**, not ATS stage names alone.

Deck vocabulary:
- High volume, shortage, compliance
- Professional Hiring / Moderate Volume
- Professional / Technical
- Critical Demand Hiring (urgent regulatory / specialized supply)
- Context pairs: High Demand / Low Supply → Precision and Speed; Low Supply / Specialized → Conversion and Scaling

### 5. Geography
Labor market + legal/regulatory surface area.

Deck examples:
- USA / North America / Mexico
- California-specific job posting rules
- US & EU (FDA/EMA), Japan (PMDA), China (NMPA)
- Multi-state home health (Elara: 18 states)

**Geo changes the cell even when Industry×Function×Role are identical** (Quality Engineer California vs Quality Engineer Mexico in the exercise).

## Supporting model

### Pain-point sheet (Step 2)
For each pain point capture:
- Business problem
- What actually breaks
- Downstream business impact
- Evidence sources (audit reports, CAPA logs, Gong, CRM, Looker…)
- Impacted roles (data-backed)
- Applicable geos (data-backed)

### Atomic units (Step 3)
Smallest hiring jobs the cell must execute. Deck QA example:
- Source certified & qualified candidates
- Screen based on requirements before interview
- Follow-up on offered candidates to raise acceptance

### Outcomes (Step 4)
Cell-owned metrics, e.g.:
- Time-to-Offer (fill as fast as possible)
- Offer-Ratio / quality of candidates hired
- Hire rate (Hired/Offered) — deck Q4 example: drop from 90%+ → ~60%

### Constraints (Step 5)
Typed hard gates, e.g.:
- Manufacturing: 21 CFR Part 820; mandatory 10-panel drug screen
- Clinical: ALCOA+ data integrity; CRA travel 50–75%
- Compliance: IEC 62304; 21 CFR Part 11

### Ontology (Step 6)
Attributes that drive FitScore, knockout questions, and JD generation:

1. Certifications  
2. Skills / Competencies  
3. Salary Budget (incl. pay-transparency by state/country)  
4. Education  
5. Location (drives screening question design)  
6. Work Schedule (nights/weekends)  
7. Job Type (PT / FT / contract)  
8. Specialization  

### Crawl | Walk | Run (Step 7)
Same hypercell, deeper automation:

| Stage | Character (QA Specialist example) | Impact called out in deck |
|-------|-----------------------------------|---------------------------|
| **Crawl** | Basic knockout, video/one-way, light scheduling, interview guides | Time-to-screen 13→10d; modest recruiter hour savings |
| **Walk** | Automated pre-qual, Voice Agent, HITL, Interview Intelligence, Hiring Automations | Time-to-screen 13→2d; larger hour savings |
| **Run** | + Intake Agent, Sourcing Agent, Reference Check Agent, Pre-Hire / Certification Check | Also reduces time-to-source 7→3d |

California adjustment example: hard knockouts on FDA/CAPA/batch experience; **do not** auto-reject on job gaps (legal sensitivity); focus on evidence of experience, not tenure.

## Worked decomposition (from deck)

**Cell A — Quality Engineer / Specialist**
- Industry: Manufacturing in Healthcare  
- Function: Quality Assurance  
- Role: Quality Engineer/Specialist  
- Workflow: Professional & Moderate Volume  
- Geography: USA  
- Atomic units: source certified → screen before interview → follow up on offers  

**Cell B — Clinical Research Scientist**
- Industry: Manufacturing in Healthcare  
- Function: R&D  
- Role: Clinical Research Scientist  
- Workflow: Professional & Moderate Volume  
- Geography: USA  

**Cell C — Critical Demand segment (V2)**
- Industry: Healthcare Compliance & Digital Health  
- Function: Quality Systems & Regulatory (AQR)  
- Role: Software Quality Engineer / CAPA / Supplier Quality Manager  
- Workflow: Professional / Technical  
- Geography: North America  
- Count: ~47 roles  

## FitScore alignment

Product language for personalized FitScore hypercell config uses the **same five axes**:  
**Industry × Function × Role × Workflow × Geography** (see PHEM FitScore Hypercell Configurator epics).

## Persona overlay (product usage)

The matrix dimensions describe **what is being hired**. Separately assign **who** operates atomic units:

| Persona | Typical atomic units |
|---------|----------------------|
| Sourcer | Source / shortlist / handoff |
| Recruiter | Screen, schedule trigger, offer follow-up, close |
| Recruitment Lead | Capacity, aging, process alignment across many cells |

Same hypercell → different X+/agent verbs per persona (see related persona intelligence work).

## Anti-patterns

- Treating "Healthcare" or "Retail" alone as a hypercell  
- Ignoring Geography when compliance or posting rules change  
- Building Crawl/Walk/Run as three different industries instead of three maturities of one cell  
- Defining ontology without constraints (knockouts without legal/geo nuance)
