---
name: skill-feedback
description: "Give feedback on a Product OS skill, agent or policy, or propose a change to it, without leaving the chat. Files a GitHub issue for the item's owner, or makes the edit on a branch and opens a pull request the owner reviews. Use for /skill-feedback, \"feedback on <skill>\", \"this skill got it wrong\", \"the PRD template should…\", \"propose a change to <skill>\", or \"report a problem with an agent\"."
metadata:
  owner: officiallybasti
  status: beta
  try: "/skill-feedback prd The template has no rollout section"
---

# Skill feedback

Every skill, agent and policy has an owner (`metadata.owner` in its front matter). Feedback goes to them as a GitHub issue; a concrete fix goes to them as a pull request. Both show up on the item's page in the PM OS catalog. Rules: `.github/CONTRIBUTING.md`.

## 1. Find the item

Read `01_product-os/onboarding/data/catalog.json` (run `node 01_product-os/onboarding/build-catalog.mjs` if it is missing; item paths in it are relative to `01_product-os/`). Match what the PM named to one item and note its `id` (for example `skill:prd`), `path`, `owner.handle` and `meta.repoUrl`. If two items fit, ask which one. If nothing fits, say so; it may be a personal skill outside the shared repo.

## 2. Issue or pull request

- **Issue** when the PM reports a problem, a gap or an idea, or isn't sure what the fix is.
- **Pull request** when the PM knows the change ("add a rollout section to the template") and it is a small edit to that item or its example.

If it is unclear, ask once: "Should I log this for <owner name>, or make the change and open a pull request for them to review?"

## 3. Draft, clean, confirm

Write the draft and show it to the PM before anything leaves the laptop. Remove customer names, candidate data, ticket contents and anything said in confidence; describe the pattern instead ("an RX customer with 24 locales"). Send only after the PM says yes.

## 4a. File the issue

Use the same headings as the web form, so the catalog reads both the same way:

```bash
gh issue create -R <owner/repo> \
  --title "[feedback] <Item name>: <one line>" \
  --label "<item id>" --label feedback \
  --body-file /tmp/skill-feedback.md
```

Body:

```markdown
### Skill or agent

`<item id>`

### What kind of feedback?

<It worked well | Something broke or was wrong | Missing capability | Unclear instructions>

### What happened

<what the PM asked and what came back, cleaned>

### What you expected

<the better outcome>
```

If `gh` says the label does not exist, run the same command without `--label "<item id>"`; the repo workflow adds the label from the body. If `gh` is not signed in, give the PM the web form link instead: `<repoUrl>/issues/new?template=feedback.yml&title=[feedback]%20<Item name>`.

## 4b. Open the pull request

1. Stop if the checkout has unrelated uncommitted changes; ask the PM what to do with them.
2. `git fetch origin && git switch -c feedback/<slug>-<short-topic> origin/main`
3. Make the smallest edit that does the job, in the item's file under `01_product-os/` or `01_product-os/examples/<slug>/`. Don't change `metadata.owner` or `metadata.status` unless the PM is the owner or the maintainer.
4. `node 01_product-os/onboarding/build-catalog.mjs --check` must pass.
5. Commit, `git push -u origin HEAD`, then `gh pr create --title "<Item name>: <change>" --body-file <file>`, with the body following `.github/pull_request_template.md` and its checklist filled in.
6. Switch the PM back to `main` afterwards. Never push to `main`.

The owner is asked to review automatically.

## 5. Report

One line with the link, who owns it, and when to expect an answer (owners answer within five working days; see `.github/CONTRIBUTING.md`).
