---
name: ns-refactor
description: "Use when restructuring code with NO observable behavior change — produces a refactor doc with a populated invariant matrix and a behavior-preservation test plan. If behavior changes, use ns-specify instead."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /ns-refactor  (no behavior change — invariants over requirements)

You are documenting a refactor under this repo's SDD process. Follow
the SDD constitution (bundled with this plugin as an always-on rule) (§7 light-flow, §10 behavior preservation). Produce a
`refactor.md`; do **not** change code yet.

The user's refactor intent follows this prompt.

---

## Gate check first
If the change would alter ANY observable behavior, it is **not** a refactor. Say so and
recommend `/ns-specify` instead. Proceed only if behavior is preserved exactly.

## Phase 0 — Context discovery (MANDATORY)
1. Read the steering files.
2. Read `northstar/specs/INDEX.md`; find specs/REQs governing the code in scope (overlapping
   `touches`). These behaviors must still hold after the refactor.
3. Inspect the affected code and its existing test coverage.

Post a short Context Summary: what's being refactored, which behaviors are governed by
existing specs, and how well it's currently tested.

## Clarify — one question at a time (only if needed)
If the boundaries are unclear, ask **one focused question at a time** — e.g. exactly which
modules are in scope, or whether a borderline change is allowed to alter behavior (if yes, it's
not a refactor — go to `/ns-specify`). Refactors are light-flow (§7): ask only enough to pin
the scope and the invariant matrix; otherwise skip and document the refactor.

## Then — document the refactor
Copy the **refactor template** (included at the end of this skill) into `northstar/specs/<NNN-slug>/refactor.md`. Fill:

1. **Motivation** — duplication / coupling / readability / perf-neutral cleanup. Why now.
2. **Scope** — exactly what changes structurally and what does NOT change. For
   non-trivial structural moves, a small before/after mermaid `graph` clarifies the change.
3. **Invariant matrix** — the observable behaviors that must be identical before and
   after, each mapped to a test. If coverage is thin, list **characterization tests to
   add first** (before touching the code).
4. **Behavior-preservation evidence** — which existing suites prove equivalence.
5. **Living-layer update** — usually `structure.md` (organization changed), not requirements.

## Output format
- Context Summary.
- **Write `refactor.md` to disk** at the path above (create the folder), with a populated
  invariant matrix, then regenerate `northstar/specs/INDEX.md` so `northstar/specs/INDEX.md` lists it
  (a hard check — an unlisted spec fails `northstar_check.py` and blocks committing it). Report the
  file(s) written and a short `git diff --stat`-style note — do **not** paste the full body into chat.

## Self-check
- Am I certain no observable behavior changes? If unsure, escalate to `/ns-specify`.
- Does every invariant map to a real or to-be-added test?
- Is the safety net (tests) in place BEFORE the refactor runs?

## Stop
Stop after **writing `refactor.md`** and reporting (the human reviews the diff). Do **not** change
code here. When the human approves, **record it on the doc** (set `refactor.md`
`approval_state: approved` and `status: approved`, then regenerate `northstar/specs/INDEX.md`) — the
read-only reviewer can't, and `/ns-implement` reads `approval_state` as the gate, so an unrecorded
approval stalls the work. Never self-approve. Then run `/ns-implement` — which must add any
characterization tests first, then refactor, keeping all invariants green.

---

## Templates (self-contained — copy the relevant skeleton into `northstar/specs/<NNN-slug>/`)

### `refactor.md`

```markdown
---
spec_id: NNN-slug
summary: ""                       # one-line catalog blurb — feeds northstar/specs/INDEX.md (generated)
type: refactor
status: draft                     # draft | in_review | approved | implemented
approval_state: pending
owners: [your-handle]
reviewers: []
risk: low
touches: []                       # globs of affected code
amends: []                        # usually none — refactors don't change behavior
northstar_version: 0.1
last_validated_at: ""
---

# Refactor: <short description>

> **No behavior change.** A refactor that changes observable behavior is not a refactor —
> stop and use `/ns-specify` instead. This doc captures the invariants that MUST hold,
> not new requirements (constitution §10).

## 1. Context discovered (Phase 0)
- **What's being refactored & why:** <duplication / coupling / readability / perf-neutral>
- **Specs/REQs governing the affected code:** <they must still hold after>
- **Relevant code paths:** <files inspected>

## 2. Motivation
<!-- Why now. The cost of leaving it as-is. -->

## 3. Scope
<!-- Exactly what changes structurally. What does NOT change. -->

## 4. Invariant matrix (the safety contract)
<!-- The observable behaviors that must be identical before and after. Each maps to an
     existing test or a characterization test you'll add first. -->
| Invariant | How it's proven | Test |
|---|---|---|
| <e.g. validation rejects empty email with 400 + VALIDATION_ERROR> | existing/added test | `tests/...` |
| <…> | | |

## 5. Behavior-preservation evidence (constitution §10)
- *Existing tests covering this code pass unchanged:* <which suites>
- *Characterization tests added before refactor (if coverage was thin):* <which>

## 6. Living-layer update
<!-- Refactors often update `structure.md` (how code is organized), not requirements. -->

## Changelog
- v0.1.0 — <date> — refactor documented — <PR link>
```

