# Contributing to the Product OS

Every skill, agent and policy in this repo has one owner and one status. The PM OS catalog reads both from the item's front matter, so the catalog, the review requests and the dashboards never drift from the files.

## Every item carries a metadata block

```yaml
---
name: prd
description: "What it does, written for a PM who has never seen it"
metadata:
  owner: officiallybasti          # GitHub handle, required
  status: beta                    # sandbox | beta | stable | retired, required
  try: "Write a PRD for bulk SMS opt-out in CRM Messaging"   # the first prompt to try
  example: examples/prd/bulk-sms-opt-out.md                  # a real output, optional
  audience: "RX PMs"              # optional, default "All PMs"
  superseded-by: skill:sr-triage  # retired items only
---
```

- The owner's handle must be in `01_product-os/onboarding/people.json` and be a collaborator on the repo.
- `node 01_product-os/onboarding/build-catalog.mjs --check` fails a pull request when an owner or status is missing. It also fails when `.github/CODEOWNERS` is stale: regenerate it with `--codeowners`, never edit it by hand.
- Examples live in `01_product-os/examples/<slug>/`. Use a real output with the customer, candidate and personal details taken out. Front matter: `title`, `prompt` (what was asked) and `note` (anything a reader should know).

## What an owner does

- Answers feedback issues within five working days: fix, decline with a reason, or ask a question.
- Reviews pull requests on the item. The catalog check workflow requests the review automatically; the maintainer co-owns every path as a backup.
- Keeps `try` and the example current when the behaviour changes.
- Hands over before leaving a team: a pull request that changes `metadata.owner`. Until then the maintainer is the owner.

## Lifecycle

| Status | What it means for a PM | To get here |
|--------|------------------------|-------------|
| **sandbox** | Try it; it may change or disappear | Owner, status and description set; no customer data or credentials |
| **beta** | Works for more than its author; the owner answers feedback | At least 2 PMs besides the owner used it in the last 30 days, and `try` works |
| **stable** | Recommended for every PM; breaking changes are announced in What's new | At least 3 PMs besides the owner used it in the last 30 days, it has an example output, and no "something broke" feedback is open for more than five working days |
| **retired** | No longer recommended; its slash command is unlinked | No runs in 60 days, or replaced (`superseded-by`). Deleted one release later |

Promotion and retirement are pull requests that change `metadata.status`. The owner proposes a promotion; the maintainer approves it. The Team usage page in the PM OS lists the items that meet the next bar, and the ones that look ready to retire.

## Give feedback or propose a change

| You want to | Do this |
|-------------|---------|
| Tell the owner something worked, broke or is missing | From Claude Code: `/skill-feedback <skill> <what happened>`. In the browser: the item's page in the catalog, then **Leave feedback** |
| Fix it yourself | `/skill-feedback` and say you want to make the change: it edits on a branch and opens the pull request. Or use **Propose a change** on the item's page to edit in GitHub |
| Add a new skill | Create `01_product-os/skills/<name>/SKILL.md` with the metadata block, `status: sandbox`, and open a pull request |

Feedback issues carry a label with the item's id (`skill:prd`), added by the label workflow. The catalog shows open feedback and pull requests on each item's page.

## Usage data

Hooks in `.claude/settings.json` and `.cursor/hooks.json` log the name of each skill, agent and slash command a PM runs to `~/.copilot/usage/events.jsonl` on their own laptop. Never prompt text, files or output. Opt out with `PMOS_USAGE=off` or a file at `~/.copilot/usage/OPT_OUT`. The team view counts PMs per team, not individuals.
