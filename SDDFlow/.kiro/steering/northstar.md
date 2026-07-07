---
inclusion: always
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Spec-Driven Development (SDD) — Kiro overview

This repo uses SDD. The full method is bundled in this `.kiro/` folder — skills, subagents, and the constitution (loaded as always-on steering). Nothing else is needed.

## How to work
- Enter through **`/northstar`** — it classifies the change, matches ceremony to risk, and hands off to the right flow.
- Always do **Phase-0 context discovery** first: read `northstar/steering/*`, scan `northstar/specs/INDEX.md`, read overlapping specs (match `touches:`), inspect the code.
- **Two layers:** living context (`northstar/steering/*`) is updated in place; increment specs (`northstar/specs/NNN-slug/`) are immutable and link later changes via `amends:` / `supersedes_reqs:`.

## Bundled skills
- **`/ns-bug`** — Use when fixing a bug or regression — finds the spec/REQ that owns the broken behavior, then writes a bugfix doc with root-cause analysis and a mandatory regression test that fails before and passes after the fix.
- **`/ns-finish`** — Use when an implemented change is ready to ship — verifies tests, the per-task/final reviews, and the SDD checks are green, sets the spec to implemented with a Changelog entry, refreshes the living layer and INDEX, then opens a PR (Bitbucket/GitHub-aware) linking the spec.
- **`/ns-implement`** — Use when an approved spec is ready to build — executes tasks.md in dependency order with per-task spec-compliance and code-quality reviews, writing tests for each REQ-ID. Requires approval_state: approved (stops if pending).
- **`/northstar`** — Use when you want to make ANY code change and aren't already in a specific SDD flow — describe the change and this routes it: classifies feature / bug / refactor / brownfield onboarding / implement, matches the ceremony tier to the risk, and hands off to the right ns-* flow.
- **`/ns-refactor`** — Use when restructuring code with NO observable behavior change — produces a refactor doc with a populated invariant matrix and a behavior-preservation test plan. If behavior changes, use ns-specify instead.
- **`/ns-specify`** — Use when starting a feature, greenfield build, performance change, or migration that needs a spec — runs Phase-0 context discovery, then writes an EARS spec to northstar/specs/, and for higher-risk (Full-tier) work also writes design.md and tasks.md through their approval gates. Not for bug fixes (use ns-bug) or behavior-preserving refactors (use ns-refactor).
- **`/ns-steer`** — Use when onboarding a brownfield repo or refreshing project context — inspects the actual codebase, detects (does not invent) the stack and conventions, and writes the steering files (product, tech, structure) into northstar/steering/ as the Layer-1 living context.

Technique practices (pulled in by the flows): `ns-tdd`, `ns-debugging`, `ns-receiving-review`, `ns-brainstorming`.

## Bundled subagents
- **`ns-code-quality-reviewer`** — Use after spec-compliance passes to review code quality — conventions, banned patterns, meaningful tests, clarity, robustness, and security. Read-only; blocks only on Important issues.
- **`ns-implementer`** — Use when executing a single task from an approved spec's tasks.md — implements exactly one task with strict TDD (failing test first), matches project conventions, runs tests, commits, and reports one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED. Does not review its own work or start other tasks.
- **`ns-spec-compliance-reviewer`** — Use after a task is implemented, before the code-quality review, to verify the code matches its spec/REQ-IDs exactly (nothing missing, nothing extra) by reading the actual diff and tests. Read-only; do not trust the report.
- **`ns-spec-reviewer`** — Use when a drafted spec needs review before the requirements approval gate — verify EARS form, unique REQ-IDs, testable acceptance criteria, scope, and amends/supersedes linkage. Read-only; do not rubber-stamp.
- **`ns-tasks-reviewer`** — Use when a tasks.md needs review before implementation — verify every spec REQ-ID is covered by a dependency-aware, buildable, traceable task plan. Read-only; do not rubber-stamp.

## Enforcement & metrics
Spec validity and the org-wide "% of PRs with specs" metric are enforced **centrally by ops** (e.g. a Bitbucket webhook), not per-repo. This bundle ships only the agent behavior.
