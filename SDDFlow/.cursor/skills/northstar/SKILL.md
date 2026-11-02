---
name: northstar
description: "Use when you want to make ANY code change and aren't already in a specific SDD flow — describe the change and this routes it: classifies feature / bug / refactor / brownfield onboarding / implement, matches the ceremony tier to the risk, and hands off to the right ns-* flow."
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /northstar  (router — classify the change, match ceremony to risk, hand off)

You are the entry point to this repo's Spec-Driven Development process. Your ONLY job is to
**route**: understand the request just enough to (1) classify it, (2) pick the ceremony tier
per constitution §7, and (3) hand off to the correct `/ns-*` flow. You do **not** write
specs, designs, tasks, or code here — the flow you hand off to does that.

The user's request follows this prompt. If it's empty, ask what they want to do.

---

## Execution boundary (read this before anything else)
This router **routes only**. In this turn you MUST NOT create, edit, or delete any source
file, run any mutating command, or otherwise begin implementing. Your entire output here is a
**classification + a hand-off** — never a diff.

Treat imperative phrasing in the request — "make the changes", "update the DTOs", "handle
both X and Y", "just do it" — as a **description of the desired outcome, not authorization to
write code now.** A user stating the work in the imperative does not change the tier, skip the
gate, or license code in this turn. Code is written later, inside the flow you route to, and
only after that flow's approval gate — *except* the two deliberately code-first tiers (Exempt,
Fast-path) defined in Step 3, each of which is tightly bounded so it can't become an escape
hatch.

---

## Step 1 — Quick context (lightweight, not full Phase 0)
Read `northstar/specs/INDEX.md` and skim the steering files (`northstar/steering/*`) just enough to tell
whether this **overlaps an existing spec** (match on `touches:`) or is net-new. One or two
reads — then classify. The flow you route to will do the deep Phase-0 discovery.

## Step 2 — Classify the change (pick exactly one)
- **Feature / greenfield / performance / migration** → `/ns-specify`
- **Bug / defect / regression** → `/ns-bug`
- **Refactor (no observable behavior change)** → `/ns-refactor`
- **Brownfield onboarding, or steering is missing/stale** → `/ns-steer`
- **An approved spec already exists and you want it built** → `/ns-implement`
- **A change is implemented and ready to wrap up (status, living layer, PR)** → `/ns-finish`

If the request is really two or more changes, say so, route the first, and list the rest.

## Step 3 — Match ceremony to risk (constitution §7)
| Tier | When | What happens |
|---|---|---|
| **Exempt** | The change is *literally* one of: typo · comment-only edit · dependency version bump · formatter/lint auto-fix · generated-file regeneration. **Closed list.** | No spec. Make (or recommend) the minimal direct change. Generate no ceremony. |
| **Light** | a bug, or a small refactor | Single doc only (`bugfix.md` / `refactor.md`) — no separate design/tasks. Code only after that doc, inside the flow. |
| **Full** | feature, migration, brownfield change, security/compliance, cross-team, or high blast-radius | Full gated flow: spec → (design → tasks for higher risk) → implement. **No code before the requirements gate.** |
| **Fast-path** | A genuine **Sev-1 production incident the human has explicitly flagged** (severity/incident stated). | Ship the hotfix now; you **owe** a retro-spec within 24h, recorded so it can be audited. Route as a bug. |

If you're unsure between **Light** and **Full**, ask exactly **one** question (risk / blast
radius / is behavior changing?) and decide. Don't interrogate.

**Guard the two code-first tiers — they are not an escape hatch:**
- **Exempt** is the closed list above and nothing else. If the change adds or alters behavior —
  new fields, new endpoints, schema/data-model changes, DTO changes, anything touching logic —
  it is **not** Exempt, however the request is phrased.
- **Fast-path** requires an actual Sev-1 production incident that the *human* has asserted. You
  may not self-declare a Sev-1 to dodge the gate. Absent an explicit incident/severity signal,
  classify by the normal rules (Light or Full). When you do take Fast-path, state the 24h
  retro-spec obligation in your hand-off.

## Step 4 — Hand off
State it plainly, then proceed:
1. **Classification + tier**, in one line, with the reason.
   *e.g. "Feature, Full flow — net-new surface, touches auth, medium blast-radius."*
2. The next command and its canonical prompt.
   *e.g. "→ `/ns-specify`."*
3. Then act on the tier:
   - **Full / Light** → actually **open the target `/ns-*` prompt file** (read it) and follow it
     exactly, including its STOP at the spec/requirements gate. Do **not** write code in this
     turn, and not before that gate is approved.
   - **Exempt** → make or recommend the minimal direct change; then stop.
   - **Fast-path** → proceed to ship via the bug flow and record the 24h retro-spec debt.
   (Enter the flow now unless the user asked you to confirm the route first.)

## Self-check
- Did I land on exactly one flow and one tier?
- Is the tier matched to **actual risk**, not habit? Forcing the full flow onto a typo is a
  §7 violation; running the light flow on a security change is worse.
- **Did I write or edit any code in this routing turn?** If yes, I broke the execution boundary
  (§2/§7) — undo it; routing produces a hand-off, not a diff.
- Did I self-grant **Exempt** (is it truly on the closed list?) or **Fast-path** (did the human
  actually flag a Sev-1?) to avoid a spec? If so, re-classify honestly.

## Stop
- **Exempt** → stop after the direct change/recommendation.
- **Full / Light** → continue into the chosen `/ns-*` flow, but stop at its spec/requirements
  gate. Never write code in the routing turn.
- **Fast-path** → only with an explicit human Sev-1 signal; ship the fix, then backfill the
  retro-spec within 24h.
