---
name: ns-tdd
description: "Use when writing any implementation or bugfix code — enforces the strict RED→GREEN→REFACTOR cycle: write a failing test first, watch it fail for the right reason, write minimal code to pass, watch it pass, then refactor with tests green. A REQ-ID without a test is not done."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Practice: Test-Driven Development (RED → GREEN → REFACTOR)

In this kit, tests are not an afterthought — every `REQ-ID` is satisfied **and tested**
(constitution §10). Write the test first, always, in a tight loop.

## The cycle (one behavior at a time)
1. **RED** — Write the smallest test that captures the next bit of required behavior. Run it.
   Confirm it fails, and that it fails **for the reason you expect** (not a typo/import error).
   A test that passes immediately, or fails for the wrong reason, is not a real RED.
2. **GREEN** — Write the **minimal** code to make that test pass. No extra abstraction, no
   speculative options, nothing the test doesn't demand. Run it. Confirm green.
3. **REFACTOR** — With the test green, clean up names, duplication, and structure. Re-run tests
   after each change. Never refactor on red.

Repeat per behavior until the task's REQ-IDs are covered.

## Rules
- **Never write implementation before its failing test.** If you already wrote code, write the
  test, then prove it would have failed (e.g. comment out the code and watch red).
- **Bugs:** the regression test must fail **before** the fix and pass **after**. That proving
  step is the whole point — it shows the test actually catches the bug.
- **Refactors:** they change structure, not behavior. The existing tests/invariants are your
  safety net — they must be green before you start and stay green throughout.
- **Map tests to REQ-IDs.** Reference the REQ-ID in or near the test so traceability is obvious
  (the soft `northstar_check` test-reference check and reviewers look for this).
- **Don't over-test.** One clear test per behavior beats ten redundant ones. Test behavior and
  contracts, not private implementation details.

## Anti-patterns
- Writing all the code, then backfilling tests that only assert what you happened to build.
- Tests that never fail (assert true, or assert on mocks you fully control).
- Skipping the "watch it fail" step — you then don't know the test exercises the new behavior.
