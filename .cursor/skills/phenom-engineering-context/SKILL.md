---
name: phenom-engineering-context
description: >-
  Answers Phenom feasibility and "how does this work in code" questions using
  the read-only engineering index and local clones under Phenom - Engineering/.
  Use when assessing technical feasibility, locating owning repos, tracing
  capabilities across Screening/Messaging/Automations/Recruiter Hub, or when
  the user mentions engineering context, capability-map, or repo catalog.
---

# Phenom Engineering Context

Read-only research layer for feasibility. **Never edit, commit, or push** anything under `Phenom - Engineering/repos/`.

## Start here

1. `Phenom - Engineering/CLAUDE.md` — full workflow  
2. `Phenom - Engineering/index/taxonomy.md` — pillar definitions  
3. `Phenom - Engineering/index/capability-map.md` — capability → pillar/repo  
4. Domain file under `Phenom - Engineering/index/` → then code under `repos/`

## Hard rules

- Cite `repo/path:line` from clones; do not copy full source files into other folders.
- Cap exploration (~5 repos) unless the user expands scope.
- Do not invent ownership — use `capability-map.md` and  
  `product-copilot-beta/.cursor/policies/platform-routing.md`.
- For code-grounded CRM navigation packs, prefer **phenom-knowledge** / **phenom-messaging**.

## Answer shape

- What exists today (repos + entry points)
- Feasibility / risk / unknowns
- Confidence (high if cited from clones; low if index-only)

## Sync / structure

See `Phenom - Engineering/SETUP.md` and `scripts/` if clones or manifests look stale.
