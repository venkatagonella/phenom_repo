---
name: ns-brainstorming
description: "Use before drafting a spec or design when intent or approach is unclear — a Socratic loop that asks one question at a time (multiple-choice preferred), explores 2–3 alternatives with a recommendation, and presents the design in small validated sections instead of one big dump."
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Practice: Brainstorming before the spec (low-friction clarification)

Wasted specs come from drafting before the intent is clear. Brainstorming is the cheap,
conversational step that prevents it — scaled to the risk of the change (constitution §7). For a
small, well-scoped change this may be a single question or none; for a high-risk / high-blast
change, earn a few more.

## How to run it
1. **One question at a time.** Ask the single most decision-relevant question, then **wait** for
   the answer before the next. Never dump a questionnaire — that's friction, and it buries the
   one question that actually matters.
2. **Prefer multiple-choice.** Offer concrete options ("A: per-user opt-in / B: org default /
   C: both") rather than open "what do you want?". It's faster for the human and surfaces the
   real trade-off.
3. **Explore alternatives.** When a genuine design choice exists, present **2–3 approaches** with
   their trade-offs and a **clear recommendation** — don't make the human invent options. Make a
   reasonable default decision for low-stakes choices and just note it.
4. **Scale to risk.** Stop asking the moment you can write testable requirements. Extra questions
   past that point are friction. Conversely, don't skip clarification on a compliance / data /
   migration change just to move fast.
5. **Validate in small sections.** When you start shaping the design, present it in pieces
   (problem framing → approach → key contracts) and confirm each before expanding, instead of
   one large block the human has to review all at once.

## When to skip
If the request is unambiguous and low-risk, skip straight to drafting and note any assumptions
you made. Brainstorming is a tool for resolving real ambiguity, not a mandatory ceremony.

## Hand-off
Brainstorming ends when you can state the change as testable EARS requirements. Carry the
decisions (and the alternatives you rejected, briefly) into the spec so the rationale isn't lost.
