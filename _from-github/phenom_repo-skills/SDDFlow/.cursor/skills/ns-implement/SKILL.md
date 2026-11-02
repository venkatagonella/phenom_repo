---
name: ns-implement
description: "Use when an approved spec is ready to build — executes tasks.md in dependency order with per-task spec-compliance and code-quality reviews, writing tests for each REQ-ID. Requires approval_state: approved (stops if pending)."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /ns-implement  (execute an approved spec)

You are implementing an **approved** spec under this repo's SDD process. Follow
the SDD constitution (bundled with this plugin as an always-on rule) (§2 approval, §9 tasks, §10 tests, §8 living-layer update).

The user will name the spec (e.g. "implement 001-notification-preferences"). If unclear,
ask which spec.

---

## Pre-flight
1. Open the spec folder (`northstar/specs/<NNN-slug>/`). Read `spec.md`/`bugfix.md`/`refactor.md`
   and `design.md`/`tasks.md` if present.
2. **Verify the gate**: the spec's `approval_state` must be `approved`. If it's still `pending`,
   **stop and ask the human to approve** (constitution §6) — never self-approve a spec. If the
   human approves now, **record it first** before implementing: set the doc's
   `approval_state: approved` and `status: approved`, then regenerate `northstar/specs/INDEX.md`, so
   the gate is captured in the spec and not just in chat. Do not implement while it reads `pending`.
   For a **Full-tier** feature spec (`risk: high` / large `blast_radius` / migration), also
   verify `design.md` **and** `tasks.md` exist and are approved (`design.md`
   `approval_state: approved`; `tasks.md` `status: approved`) — these are the §6 Design and
   Tasks gates. If they're missing, stop and send the human back to `/ns-specify` to produce
   them rather than improvising a plan here. (Light-flow bugs/refactors have no `tasks.md` —
   that's expected; see Execute.)
3. Re-read the steering files so the implementation matches conventions.
4. **Isolate the work (git) — ASK FIRST, never create or switch branches silently.** Branch
   creation is a **mandatory, explicit gate**: do NOT run `git branch`, `git checkout -b`,
   `git switch -c`, or `git worktree add` until you have asked the human and they have answered.
   Silently auto-creating a branch can strand uncommitted or untracked changes — so STOP and ask
   before touching git state. Walk through these in order:

   a. **Ask whether to create a new branch at all.** First show the current state — the current
      branch (`git branch --show-current`) and whether the working tree is clean
      (`git status --short`). Then offer:
      - **Create a new branch** (recommended when on `main`/`master` or a shared branch), or
      - **Stay on the current branch.**
      Never implement on `main`/`master` without explicit consent either way.
   b. **If they choose to create one, ask the branch NAME.** Propose a spec-derived default
      (e.g. `northstar/<NNN-slug>`) but let the human override it.
   c. **Then ask which branch to create it FROM.** Offer concrete options, don't assume:
      - **From the current branch** (name it explicitly), or
      - **From another existing branch** — list the local branches (`git branch`), and remotes
        (`git branch -r`) if useful, so they can pick the base.
   d. **Protect in-flight work.** If the working tree has uncommitted or untracked changes, flag
      them before switching and confirm how to handle them (bring along, stash, or commit first)
      so nothing is lost or carried onto the wrong branch.

   Only after these answers, create the branch from the chosen base — or, for parallel/long-running
   work, a git worktree (`git worktree add ../<slug> -b <name> <base>`) so it stays isolated from
   your main checkout. Confirm you're on the intended branch before writing any code.
5. **Pick an execution mode** and state it:
   - **Autonomous** (default for low/medium-risk specs) — run task → review → next without
     pausing; surface only blockers, disagreements, and the final summary.
   - **Checkpointed** (default for `risk: high` / large `blast_radius`, or on request) — pause
     for the human after each task's reviews pass before starting the next.
   When unsure, ask once which mode they want, then proceed.
6. **Pick a commit mode** (this controls git writes — ask once if the human hasn't said):
   - **Commit per task** *(default)* — the implementer commits each task on completion, so every
     per-task review runs against an isolated, already-committed diff. Recommended for most work.
   - **Stage only (no commit)** — the implementer stages the task's files but does NOT commit,
     leaving the changes staged for the human to review and commit/squash themselves. Use this
     when you want to own the commit history (e.g. one squashed commit) or keep the tree
     uncommitted. In this mode nothing is ever committed automatically.
   Pass the chosen commit mode to **every** implementer dispatch.

## Model tiering (pick the model per task, not one for the whole run)
Match the model to the task's difficulty to balance quality and cost — choose per dispatch:
- **Mechanical** (boilerplate, rename, wiring, trivial CRUD) → a cheaper/faster model.
- **Standard** (typical feature task, integration, normal logic) → the default model.
- **Hard** (tricky algorithm, concurrency, security-sensitive, ambiguous design, debugging) →
  the most capable model.
The **reviewers always run capable** — review judgment is where quality is won. If your IDE
can't set a per-dispatch model, ignore this and use the session model.

## Tasks-review loop (automatic — only when a `tasks.md` exists)
Before executing, verify the plan covers the spec. This is folded in — the human does not
invoke it. (Light-flow bugs/refactors have no `tasks.md`; skip this step for them.)

1. **Dispatch the review** via the **`ns-tasks-reviewer`** subagent:
   - **Subagent-capable env** (Cursor and Kiro both): invoke `ns-tasks-reviewer` with the
     `tasks.md` and `spec.md` paths.
   - **Otherwise**: perform the review inline using the `ns-tasks-reviewer` subagent with the
     same rigor. Don't rubber-stamp.
2. **Act on the verdict:** `Approved` → proceed to Execute. `Issues Found` → fix `tasks.md`,
   re-review, repeat until approved.
3. **Loop safety:** advisory only; after **5 iterations**, or disagreement on the same issue
   across **3 rounds**, or 2 malformed reviewer outputs — surface to the human.

## Execute — one task at a time, via the implementer
Work the tasks **in dependency order**. If there's no `tasks.md` (light-flow bug/refactor),
derive the minimal ordered steps from the doc and treat each as a task.

**Dispatch model (subagent-capable env, e.g. Cursor — the default):** for each task, dispatch
the **`ns-implementer`** subagent with the
task text, its `REQ-IDs`, the spec/`design.md` paths, the conventions, and the execution + commit
modes.
It implements that single task with strict TDD and reports a status. Pick its model by tier
(above). **In an env without subagents (e.g. Kiro), the main agent plays the implementer role
itself** — same protocol, same TDD discipline, inline.

- **Parallelism:** tasks marked `[P]` in `tasks.md` are independent and MAY be dispatched in
  parallel (separate implementer subagents). Never parallelize tasks with a dependency edge;
  when in doubt, serialize. Reviews still run per task.
- **TDD is mandatory** — the implementer (or you, inline) applies the `ns-tdd` skill:
  failing test first → minimal code → green → refactor. A REQ-ID without a passing test is not done.
- **Bugs**: regression test FIRST, watch it fail, then fix, then watch it pass.
- **Refactors**: invariant tests must exist and pass BEFORE refactoring; keep them green; change
  no observable behavior.
- Follow `tech.md` conventions and `structure.md` placement exactly.

**Handle the implementer's reported status** (constitution-aligned 4-status protocol):
`DONE` → proceed to review. `DONE_WITH_CONCERNS` → read the concerns; resolve correctness/scope
ones before review. `NEEDS_CONTEXT` → provide what's missing and re-dispatch. `BLOCKED` → give
more context, use a stronger model, split the task, or escalate to the human. Never force the
same model to silently retry the same failing approach.

## Per-task review loop (Level-2 — after each task, before moving on)
Once a task is implemented, its tests pass, and its changes are committed (or staged, in
**stage-only** commit mode), run the **two-stage review** before starting the next task. The
order is fixed: **spec-compliance first, then code-quality.** (In stage-only mode the review runs
on the diff of the files the task touched, since there's no per-task commit to diff against.)

1. **Spec-compliance review** — invoke the **`ns-spec-compliance-reviewer`** subagent (or, if
   subagents are unavailable, review inline using the `ns-spec-compliance-reviewer` subagent).
   Give it the task text + its `REQ-IDs`, the spec path, and the diff. `Issues Found` → fix →
   re-review. Proceed only on `Spec compliant`.
2. **Code-quality review** — invoke the **`ns-code-quality-reviewer`** subagent (or inline via
   the `ns-code-quality-reviewer` subagent). An **Important** issue → fix → re-review. Minor
   items are advisory and don't block.
3. When both are ✅, mark the task done and move on. Never start the quality review before
   spec-compliance is ✅; never advance a task with an open Important issue.

When acting on any review's feedback (here and in the tasks/spec/final reviews), apply
the `ns-receiving-review` skill: verify each point on merit, fix root causes not symptoms,
and push back with evidence rather than agreeing reflexively.

**Loop safety:** reviewers are advisory; after 5 review iterations on a task, persistent
disagreement on one issue across 3 rounds, or 2 malformed reviewer outputs — surface to the human.

## Living-layer update (constitution §8 — don't skip)
If this change altered current behavior, update the relevant `northstar/steering/*`
in the SAME change so the living layer never drifts.

## Output / behavior
- Work task by task. After each, state which REQ-ID it satisfied and that its test passes.
- Keep the diff aligned to the spec. If you discover the spec is wrong or incomplete,
  STOP and flag it — amend the spec via the proper flow rather than silently diverging.

## Final review (after all tasks)
Before calling it done, run one whole-implementation pass over the full diff: a final
**`ns-code-quality-reviewer`** subagent over the entire diff (or inline via
the `ns-code-quality-reviewer` subagent), plus a last spec-compliance check that **every
`REQ-ID` in the spec is satisfied and tested**. Fix any Important issue and re-review. This
catches cross-task / integration problems the per-task reviews can't see.

## Self-check before you call it done
- Did every task pass both reviews (spec-compliance ✅ then code-quality ✅), and did the final
  whole-diff review pass?
- Does every REQ-ID have a passing test?
- For bugs: does the regression test fail without the fix?
- For refactors: do all invariants still hold and behavior is unchanged?
- Did I update the living layer if behavior changed?
- Set the spec's `status: implemented` and add a `Changelog` entry.

## Stop
Stop when all tasks are complete, both per-task reviews and the final review have passed, and
tests are green. Summarize what shipped, mapped to REQ-IDs, and note the living-layer updates
made.
