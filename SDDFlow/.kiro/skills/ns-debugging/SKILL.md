---
name: ns-debugging
description: "Use when diagnosing a bug, failure, or unexpected behavior before proposing any fix — a 4-phase root-cause method (reproduce → isolate → name the root cause → verify) that bans guess-and-check patching and requires naming the real cause before writing a fix."
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Practice: Systematic debugging (root cause before fix)

The constitution (§10) forbids proposing a fix before the **root cause** is named. Guessing and
patching symptoms hides bugs and breeds regressions. Work the phases in order.

## Phase 1 — Reproduce reliably
- Get a deterministic reproduction: exact steps, inputs, environment, and the precise failure
  (error text, wrong output, timing). If it's intermittent, find what makes it more frequent.
- Write the reproduction down. For races / retries / multi-actor or multi-service failures, draw
  the failing interaction as a mermaid `sequenceDiagram` — ordering bugs are far clearer visually.
- This reproduction becomes the **regression test** later (it must fail now, pass after the fix).

## Phase 2 — Isolate
- Narrow the surface: bisect (commits, inputs, components) until you have the smallest thing that
  still fails. Remove variables one at a time.
- Read the actual code path and the real data/logs — don't theorize from memory. Confirm each
  assumption ("is this value what I think?") with evidence, not belief.

## Phase 3 — Name the root cause
- State the **real** cause in one sentence: the specific condition/logic/contract that produces
  the failure — not the symptom. "It returns null" is a symptom; "we never initialize X when the
  cache misses on first request" is a root cause.
- If you can't name it yet, say so and state exactly what you'd investigate next. Do **not**
  start writing a fix.

## Phase 4 — Fix and verify
- Fix the root cause, not the symptom. Prefer the fix that also prevents the **class** of bug
  (defense in depth: validate at the boundary, fail loudly, add the invariant) without
  over-engineering.
- Verify: the regression test now passes, the original reproduction is gone, and you haven't
  broken neighboring behavior (run the surrounding suite).
- Wait on conditions, not on time — if the bug involved async/timing, assert on the actual
  state/event rather than adding sleeps.

## Anti-patterns
- Changing things until the symptom disappears without understanding why.
- "Fixing" by widening a try/except, bumping a timeout, or special-casing the one failing input.
- Declaring it fixed without a test that fails without the fix.
