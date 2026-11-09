---
name: token-guard
type: skill
description: "Token budget for every task — suppress verbose output, deep indexing, and heavy tool calls on small/direct work. Always active."
always: true
triggers: [token, concise, efficiency, don't waste tokens, keep it short]
metadata:
  owner: nikhilsharma-phenom
  status: stable
---

# Token Guard

Honor this on **every** task before tools or long replies.

## Core Constraint

- For single-line fixes, typos, or direct local questions, output ONLY the exact code or a 1-sentence answer. No explanations, no markdown padding, no extra file reads.
- Do not trigger full codebase scans or heavy tool calls unless explicitly asked.
- Prefer inline/patch edits over full file generation.

## Before acting

1. Is this a small/direct ask? → Answer or patch with minimal tools (often zero or one file read).
2. Is this ambiguous or multi-step? → Plan briefly; still avoid catalog dumps, full-repo greps, and redundant parallel discovery.
3. Never use "exploration" as an excuse to load full MCP tool catalogs or walk the whole tree for a local question.

## Related

- MCP auth/status checks: `@policies/mcp-connectivity.md` (1–2 calls max, zero catalog dumps)
- Response style: `@policies/llm-token-efficiency.md`
