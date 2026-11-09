---
name: sr-triage
description: >-
  The single recommender for the "RX - Service Request Analysis" sheet. Classifies each support ticket once:
  ticket type, product experience and product (Jira constants), Jira ticket classification, level 1 / level 2,
  reasoning, confidence and PM-review flag. Use for nightly batches of new tickets, backfills after a rulebook
  version bump, and re-checking a single ticket. Replaces Service Sarah and ad-hoc Claude rubrics.
metadata:
  owner: officiallybasti
  status: beta
  try: "/sr-triage Classify the tickets added to the RX sheet since yesterday"
  audience: "RX PMs"
---

# SR triage

One rulebook, one agent, one recommendation per ticket. The rules live in
[`knowledge/service-request-analysis/rulebook.md`](../../knowledge/service-request-analysis/rulebook.md) — read it
fully before classifying. Product names come only from `policies/jira-constants.md`; which products the SR
Prevention tool shows lives in `knowledge/service-request-analysis/scope.json`.

## Inputs

| Input | How to get it |
|---|---|
| Sheet export (.xlsx) | Google Drive `download_file_content` on sheet `1dTFPQUDCWflvrJ8xjfGm_21Ea_mGlFeZkIyjMCT8Sto`, export as xlsx |
| Context (allowed values) | `python3 skills/sr-triage/sr_triage.py context <sheet.xlsx> <work>/context.json` |
| Batches | `python3 skills/sr-triage/sr_triage.py batches <sheet.xlsx> <work>/batches [--all]` — default picks rows without a current-version recommendation and never rows with Status = reviewed |

## Classify (per batch, ~40 tickets)

For each ticket in a batch, follow rulebook §2 in order and produce one JSON line:

```json
{"id":"CS0353239","type":"Bug-Customer","product_experience":"Recruiter Experience (RX)","product":"CRM - Automation",
 "jira_classification":"Code Issues","l1":"Workflows & automations","l2":"Trigger & execution failures",
 "reasoning":"Bug-Customer — audit shows a project-stage update that never happened; supported behaviour failed (O-AUTOMATION). CRM - Automation (filed).",
 "confidence":"high","pm_review":false,"rules":["O-AUTOMATION"]}
```

- Also return `jira_classification_child`: the child under your parent, from [`knowledge/service-request-analysis/_shared/ticket-classification.md`](../../knowledge/service-request-analysis/_shared/ticket-classification.md), chosen in the order of rulebook §5 (Jira-filed child if the parent matches, else Support-filed, else rule-implied, else your judgement). A child doubt alone does not set `pm_review`.
- Values must be copied exactly from `context.json` (types, Jira classifications, products per experience, L1, L2 per product).
- Read problem, discussions and solution — never the title alone. Filed fields are weak signals.
- `rules` lists the rulebook ids you relied on (override `O-…` and routing `R-ROUTE-…` ids); empty when none applied.
- Write `<work>/labels/batch-NNN.jsonl` with one line per input ticket, same order, every id exactly once.

## Rewrite Details (same pass)

When a batch row has `details_needs_rewrite: true`, also return a `details` field: rewrite `details_full` (ServiceNow
description + work notes and Jira description + comments) into the format in
[`knowledge/service-request-analysis/_shared/details-format.md`](../../knowledge/service-request-analysis/_shared/details-format.md):
`Problem:` / `Discussions:` (2–5 bullets) / `Solution:`, ≤ 150 words, roles instead of names, no markup, links, emails or
boilerplate closures, and the Solution taken from what actually happened. Classify from the full raw text, not from your summary.
Rows without the flag get no `details` field (the existing cell is kept).

## Validate

`python3 skills/sr-triage/sr_triage.py validate <work>/context.json <work>/labels/batch-NNN.jsonl`

Fix every hard error by re-reading that ticket (one retry). If it still fails, set `pm_review: true`, keep the closest
valid values and say what is missing in the reasoning. Warnings (incoherent type + classification) must carry `pm_review: true`.

## Write to the sheet

Only the "Recommendation …" columns, `matched_rules`, and `Details` when a rewritten `details` is present, located by header name. The writer saves the previous Details text to a local backup file before overwriting it. Stamp Status = `proposed`,
Analysed By = `SR Triage Agent`, Analysed On = today, matched_rules = `rulebook <version>; <rules>`. Never overwrite a row
with Status = `reviewed`; never touch SN or JIRA columns.

This repository does not bundle a sheet writer. Stop after validated JSONL unless the runtime provides a reviewed writer
that locates columns by header, backs up existing Details, supports a dry run, and enforces the guards above. Never improvise
direct cell writes from row numbers.

## Guardrails

- Do not run the old keyword rules or produce a second opinion; this skill is the only writer of recommendations.
- A rulebook change bumps the version in `rulebook.md`; the next run re-classifies all non-reviewed rows.
- Lint the sheet's Details with `sr_triage.py lint-details <sheet.xlsx>`; every run should lower that count.
- Report per run: tickets classified, PM-review rate, hard errors left, and type / product agreement with any reviewed rows in the batch.
