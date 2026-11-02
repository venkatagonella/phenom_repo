---
name: ns-finish
description: "Use when an implemented change is ready to ship — verifies tests, the per-task/final reviews, and the SDD checks are green, sets the spec to implemented with a Changelog entry, refreshes the living layer and INDEX, then opens a PR (Bitbucket/GitHub-aware) linking the spec."
disable-model-invocation: true
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /ns-finish  (verify → update living layer & index → PR)

You are finishing an implemented change under this repo's SDD process. Follow
the SDD constitution (bundled with this plugin as an always-on rule) (§1 specs in git, §8 living layer, §10 tests). Do **not** write new
feature code here — if something is incomplete, go back to `/ns-implement`.

The user names the spec or branch. If unclear, infer from the current branch and recent specs.

---

## 1. Verify it's actually done
- All tests pass.
- Every `REQ-ID` in the spec has a passing test (bugs: the regression test fails before / passes
  after the fix; refactors: invariants green, behavior unchanged).
- The per-task reviews and the final whole-diff review passed (Level-2). If they didn't, stop
  and return to `/ns-implement`.
- Make sure the SDD checks are green — they run automatically in CI on the PR (Bitbucket/GitHub-aware). Fix anything they flag before landing.
- **Git state:** if the working tree has uncommitted or staged changes (e.g. implementation ran
  in **stage-only** commit mode), surface them and let the human commit or squash them first —
  never push or open a PR with unaccounted-for uncommitted work.

## 2. Update the record (Layer 1 + spec status)
- If behavior or structure changed, update the living layer in the SAME change:
  `northstar/steering/*`. The living layer must never drift (§8).
- Set the spec's front-matter `status: implemented`, set `last_validated_at` to today, and add
  a `## Changelog` entry (version — date — what shipped — REQ-IDs — PR link).
- Refresh the catalog so `northstar/specs/INDEX.md` reflects the new status/summary — regenerate it from the specs' front-matter.

## 3. Choose how to land it (ask the human — don't assume)
Present the disposition options and let the human pick (default: **Open a PR**):

1. **Open a PR** *(default)* — push the branch and open a PR whose description **links the spec**
   (`northstar/specs/<NNN-slug>/`) and lists the `REQ-IDs` delivered. Detect the host from the git remote:
   on **Bitbucket** the `bitbucket-pipelines.yml` checks run automatically; on **GitHub** the
   `.github/workflows/northstar.yml` checks run. Use the org's PR template if present; otherwise a short
   **Summary** + **Test plan**. Don't merge until the SDD checks and human review are green.
2. **Merge directly** — only with explicit consent and when policy allows (e.g. trunk-based, no
   required PR). Re-run the SDD checks first; never force-push to `main`/`master`.
3. **Keep the branch** — leave the work on its branch/worktree for later; do nothing destructive.
4. **Discard** — only on explicit confirmation. Make sure the spec/docs you want to keep are
   committed, then the branch can be abandoned.

## 4. Worktree cleanup (if you used one)
If implementation ran in a git worktree (`git worktree add ../<slug> …`), clean it up **after**
the work is safely landed or intentionally kept:
- Confirm the branch is pushed/merged (or the human chose to keep/discard it).
- From the main checkout: `git worktree remove ../<slug>` (use `--force` only if you're sure
  there's nothing uncommitted you need). Then `git worktree prune`.
- Never remove a worktree with uncommitted changes you haven't accounted for.

## Self-check
- Tests green, every `REQ-ID` tested, per-task + final reviews passed?
- Living layer updated (or genuinely n/a)? Spec marked `implemented` with a Changelog entry?
- `northstar/specs/INDEX.md` regenerated and in sync? Disposition chosen by the human; PR (if opened) links
  the spec and lists REQ-IDs? Worktree cleaned up (or intentionally kept)?

## Stop
Stop after the chosen disposition is done (PR open and CI running / merged / branch kept /
discarded) and any worktree is cleaned up. Report what landed where, the `REQ-IDs` shipped, and
the living-layer updates made. Next step is human review and merge (if a PR was opened).
