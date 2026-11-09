---
title: "Checking for updates without changing anything"
prompt: "/update-product-os what's new? Don't update yet."
note: "Real run on 23 Oct 2026 on a checkout that was already current. Script output first, then the agent's answer."
---

## Script output

```text
## Repo
- branch: main
- commits on origin/main you don't have: 0

## On origin/main, not here
```

## Agent's answer

You're up to date: your checkout of phenom-product-copilot matches `origin/main`, so there is nothing new to pull.

Nothing was changed. When a teammate shares a new skill, run `/update-product-os` again without "don't update" and I'll pull it, relink the slash commands and tell you what's new for you.
