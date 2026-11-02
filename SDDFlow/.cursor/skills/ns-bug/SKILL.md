---
name: ns-bug
description: "Use when fixing a bug or regression — finds the spec/REQ that owns the broken behavior, then writes a bugfix doc with root-cause analysis and a mandatory regression test that fails before and passes after the fix."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /ns-bug  (bugfix — root cause first, regression test mandatory)

You are triaging a bug under this repo's SDD process. Follow the SDD constitution (bundled with this plugin as an always-on rule)
(§7 light-flow, §10 regression test). Produce a `bugfix.md`; do **not** write the fix yet.

The user's bug report / reproduction follows this prompt.

---

## Phase 0 — Context discovery (MANDATORY)
1. Read the steering files.
2. Read `northstar/specs/INDEX.md`; find the spec/REQ that owns the broken behavior
   (overlapping `touches`). Read it.
3. Inspect the relevant code paths and the failing scenario.

Post a short Context Summary: which spec/REQ governs this (or "gap — no spec covered it"),
and the code paths involved.

## Clarify — one question at a time (only if needed)
If the reproduction or scope is unclear, ask **one focused question at a time** (multiple-choice
preferred) — e.g. exact steps to reproduce, frequency/severity, which environment. Bugs are
light-flow (§7): ask only what you need to name the root cause and write the regression test —
don't interrogate. If it's already clear, skip this and document the bug.

## Then — document the bug (systematic debugging)
Work the root cause using the `ns-debugging` skill (reproduce → isolate → name
the root cause → verify) — do not propose a fix before the cause is named. Copy
the **bugfix template** (included at the end of this skill) into `northstar/specs/<NNN-slug>/bugfix.md`. Fill:

1. **Actual behavior** — precise, with reproduction. For races, retries, or multi-actor /
   multi-service bugs, include a mermaid `sequenceDiagram` of the failing interaction — it
   explains ordering bugs far better than prose.
2. **Expected behavior** — reference the REQ it should satisfy. If none existed, propose
   one (it will be added to the owning spec's living layer via `amends`).
3. **Root cause** — the real cause, not the symptom. **Do not propose a fix until the
   root cause is named** (constitution §10). If you can't name it yet, say what you'd
   investigate next.
4. **Fix approach** — only after root cause is clear.
5. **Regression test** — name the test file + scenario that FAILS before the fix and
   PASSES after. This is mandatory; a bug without a regression test is not done.
6. **Living-layer update** — if this exposed a missing/wrong requirement, which steering
   file gets corrected.

## Output format
- Context Summary.
- **Write `bugfix.md` to disk** at the path above (create the folder), then run
  regenerate `northstar/specs/INDEX.md` from the specs' front-matter so `northstar/specs/INDEX.md` lists it (a hard check — an unlisted
  spec fails `northstar_check.py` and blocks committing it). Report the file(s) written and a
  short `git diff --stat`-style note — do **not** paste the full body into chat.
- Explicit confirmation of the regression-test scenario.

## Self-check
- Have I named the ROOT cause, or just a symptom?
- Is there a concrete regression test that reproduces the exact failure?
- Did I set `amends`/`supersedes_reqs` if a requirement was wrong or missing?

## Stop
Stop after **writing `bugfix.md`** and reporting (the human reviews the diff). Do **not** write
the fix here. When the human approves, **record it on the doc** (set `bugfix.md`
`approval_state: approved` and `status: approved`, then regenerate `northstar/specs/INDEX.md`) — the
read-only reviewer can't, and `/ns-implement` reads `approval_state` as the gate, so an unrecorded
approval stalls the fix. Never self-approve. Then run `/ns-implement` to apply the fix + the
regression test together.

---

## Templates (self-contained — copy the relevant skeleton into `northstar/specs/<NNN-slug>/`)

### `bugfix.md`

```markdown
---
spec_id: NNN-slug
summary: ""                       # one-line catalog blurb — feeds northstar/specs/INDEX.md (generated)
type: bug
status: draft                     # draft | in_review | approved | implemented
approval_state: pending
owners: [your-handle]
reviewers: []
ticket_ids: []
severity: ""                      # sev1 | sev2 | sev3
risk: medium
touches: []                       # globs of affected code
amends: []                        # spec(s) whose behavior was violated, if any
supersedes_reqs: []               # REQ-IDs that were wrong/missing, if any
northstar_version: 0.1
last_validated_at: ""
---

# Bug: <short description>

> Light flow (constitution §7): a bug usually needs only this file — no separate design.
> A bug means an existing REQ wasn't met, or a REQ was missing. Capture which.

## 1. Context discovered (Phase 0)
- **Spec/REQ that owns this behavior:** <spec_id:REQ-ID, or "no spec covered this — gap">
- **Relevant code paths:** <files inspected>
- **Steering facts that matter:** <e.g. the auth/async pattern involved>

## 2. Actual behavior (what happens now)
<!-- Precise. Include the failing scenario / reproduction steps. For timing/ordering or
     multi-actor bugs (races, retries, multi-service), a mermaid `sequenceDiagram` of the
     failing interaction is usually clearer than prose. -->

## 3. Expected behavior (what should happen)
<!-- Reference the REQ it should satisfy. If no REQ existed, propose one (it goes into the
     owning spec's living layer via `amends`). -->

## 4. Root cause
<!-- The actual cause, not the symptom. Do NOT propose a fix before this is named
     (constitution §10 + systematic debugging). -->

## 5. Fix approach
<!-- The change, in 2–4 bullets. Files touched. -->

## 6. Regression test (mandatory — constitution §10)
<!-- The test that FAILS before the fix and PASSES after. Name the file and the scenario. -->
- *Test:* `tests/.../<name>.test.ts` — <scenario>
- *Fails before fix:* yes
- *Passes after fix:* yes

## 7. Living-layer update
<!-- If this revealed a missing/wrong requirement, which steering file gets
     corrected so the bug class can't silently return. -->

## Changelog
- v0.1.0 — <date> — bug documented — <PR link>
```

