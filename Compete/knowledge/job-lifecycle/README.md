# Phenom Job Lifecycle Competitor Research

Cursor-ready research bundle for analyzing job creation, requisition, posting, publishing, expiry, unposting, filling, closing, and reopening workflows across Phenom's core competitor set.

## Included competitors

* Workday
* SAP SuccessFactors
* Greenhouse
* Ashby
* Workable
* Personio

## Contents

* `.cursor/rules/phenom-job-lifecycle.mdc` — Cursor project rule (wired at workspace root).
* `.cursor/skills/competitor-job-lifecycle/SKILL.md` — Compete agent skill.
* `docs/lifecycle-comparison.md` — detailed comparison of entity lifecycle and states.
* `docs/posting-publishing-expiry-unposting.md` — definitions and platform differences.
* `docs/phenom-recommended-domain-model.md` — suggested Phenom model and invariants.
* `diagrams/job-lifecycles.mmd` — Mermaid sequence diagrams for all six competitors.
* `data/competitor-lifecycles.json` — structured comparison data for agent use.
* `prompts/competitor-analysis-prompt.md` — reusable analysis prompt.

## How to use in Cursor

Installed in the Compete workspace:

1. Rule: `.cursor/rules/phenom-job-lifecycle.mdc`
2. Skill: `.cursor/skills/competitor-job-lifecycle/SKILL.md`
3. Structured data: `knowledge/job-lifecycle/data/competitor-lifecycles.json`
4. Ask the Compete agent to compare a vendor workflow against the Phenom recommended model.

## Scope and confidence

This bundle captures the research and working conclusions produced in the preceding conversation. It is a product-management benchmark, not a claim that every configuration is universal across customer tenants or product editions. Vendor workflows are highly configurable, so the agent must label configuration-dependent behavior and verify current vendor documentation before making external-facing claims.

## Core terminology

* **Job/requisition** — the internal hiring demand record.
* **Opening** — a headcount slot attached to a job or requisition.
* **Posting** — a candidate-facing or channel-specific listing associated with a job.
* **Publishing** — the action that makes a posting or job visible to candidates.
* **Expiry** — an automatic or date-driven end condition for a posting.
* **Unposting/unpublishing** — an explicit action that removes a posting from candidate-facing availability.
* **Archiving/closing** — a stronger terminal or administrative action on the job/requisition itself.

The most important modeling rule is: a posting can be expired or unpublished while its underlying job/requisition remains open.
