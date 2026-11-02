---
name: ns-receiving-review
description: "Use when responding to code-review or spec-review feedback (from a human or a reviewer subagent) — evaluate each point on technical merit, verify before applying, fix root causes not symptoms, and push back with evidence on anything wrong instead of agreeing reflexively."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Practice: Receiving review feedback (with technical rigor)

The SDD flows run review loops — `ns-spec-reviewer`, `ns-tasks-reviewer`,
`ns-spec-compliance-reviewer`, `ns-code-quality-reviewer`, plus human reviewers. Reviews are
**advisory**: they flag, you decide. Quality comes from engaging with each point honestly, not
from reflexive agreement or defensiveness.

## For each piece of feedback
1. **Understand it.** Restate the concern in your own words. If it's ambiguous, ask — don't guess
   at what the reviewer meant and "fix" the wrong thing.
2. **Evaluate on merit.** Is it correct? Verify against the spec/REQ-IDs, the code, and the
   constitution — not against who said it. Check the claim before acting on it (reproduce the
   bug, read the cited line, run the test).
3. **Act:**
   - **Valid** → fix the **root cause**, not just the flagged line. If the same mistake exists
     elsewhere, fix it there too. Re-run the relevant test/review.
   - **Wrong or based on a misunderstanding** → push back with evidence (a test, a spec line, a
     measurement). Don't silently comply with something that makes the work worse.
   - **Partially right** → take the correct part, explain what you're not changing and why.
4. **Don't over-correct.** A minor/advisory note doesn't require a redesign. Match the response
   to the severity (Important blocks; Minor is advisory).

## Stance
- No performative agreement ("Great catch!" then a non-fix). No defensiveness either.
- Reviewer ≠ authority over truth; evidence is. A good disagreement, backed by a test or a spec
  reference, is a valid outcome — surface it to the human if it persists.
- After addressing feedback, **re-run the same review** and proceed only on Approved /
  Spec compliant (or an Important-free code-quality pass).

## Loop safety
If you and a reviewer disagree on the same issue across ~3 rounds, or you've iterated ~5 times,
stop looping and surface it to the human with both positions and your reasoning.
