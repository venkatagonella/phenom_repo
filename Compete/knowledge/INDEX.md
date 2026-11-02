# Compete knowledge index

Start here when answering competitive-intelligence, vendor-comparison, or job-lifecycle questions in this workspace.

## Packs

| Pack | Path | Use when |
|---|---|---|
| **Roles across competitors (master list)** | `knowledge/ROLES-COMPETE-INDEX.md` | Skills, references, vendor role cheat sheet, Phenom mapping, read order |
| Job lifecycle competitor research | `knowledge/job-lifecycle/` | Job/requisition/posting/publishing/expiry/unposting across Workday, SAP SuccessFactors, Greenhouse, Ashby, Workable, Personio |
| Hiring personas and JTBD | `knowledge/personas-jtbd.md` | Combined hiring-team personas and jobs-to-be-done flows across the same six vendors |
| Core + Hypercell JTBD (Sourcer / Recruiter / Lead) | `knowledge/roles-jtbd-core-hypercell.html` | Most important JTBD per role — Core table + Hypercell table; compete synthesis aligned to Phenom CRM / phenom-knowledge |

## Job lifecycle pack

Read in this order:

1. `knowledge/job-lifecycle/data/competitor-lifecycles.json` — structured benchmark
2. `knowledge/job-lifecycle/docs/lifecycle-comparison.md` — vendor sequences and states
3. `knowledge/job-lifecycle/docs/posting-publishing-expiry-unposting.md` — concept distinctions
4. `knowledge/job-lifecycle/docs/phenom-recommended-domain-model.md` — Phenom three-layer model
5. `knowledge/job-lifecycle/diagrams/job-lifecycles.mmd` — Mermaid sequences
6. `knowledge/job-lifecycle/prompts/competitor-analysis-prompt.md` — output contract

Agent wiring:

- Rule: `.cursor/rules/phenom-job-lifecycle.mdc`
- Skill: `.cursor/skills/competitor-job-lifecycle/SKILL.md`

## Grounding rules

- Cite the pack files; do not invent vendor behavior.
- Label configuration-dependent behavior and confidence.
- Do not treat posting, publishing, expiry, unposting, and job close as synonyms.
- Verify current vendor docs before external-facing claims.

| ATS vendor × recruiter problems (sourced) | `knowledge/ats-vendor-recruiter-problems-matrix.md` | How WD/SF/GH/Ashby/Workable/Personio address recruiter pain themes |
