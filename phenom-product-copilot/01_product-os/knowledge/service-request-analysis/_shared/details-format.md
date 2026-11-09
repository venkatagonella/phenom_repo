# `Details` format (label sheet)

**Goal:** a PM reads one cell and understands what the customer needed, what was found, and how it ended — in under 30 seconds. It summarises the ServiceNow description + work notes **and** the Jira description + comments. It never copies the thread.

Written by the `sr-triage` skill (rewrite step) — see [`skills/sr-triage/SKILL.md`](../../../skills/sr-triage/SKILL.md).

## Structure (required, exactly these three labels)

```
Problem: <what the customer saw or asked for, in plain words; environment only if it matters (PROD/STG). 1–3 sentences, ≤ 60 words.>

Discussions:
- <key finding / root cause, with who found it as a role: Support, Engineering, customer>
- <workaround or options offered; customer pushback if it changed the outcome>
- <2–5 bullets total, each ≤ 25 words, in the order things happened>

Solution: <how it actually ended: fix, workaround, config change, explanation, or "No resolution recorded — closed in ServiceNow". 1–2 sentences. If still open: what is blocked and who owns the next step.>
```

Total target **≤ 150 words**. Longer only when the case genuinely has several distinct causes.

## Always remove

| Remove | Examples |
|---|---|
| Markup and mention tags | `<custom data-type="mention" …>`, `<custom data-type="smartlink" …>`, `<custom data-type="date" …>`, `[text](mailto:…)` |
| People and pings | `@Name`, `fyi @…`, "Hi team", "any update?", "please look at the earliest", "client has escalated" (keep only as "Customer escalated" if it mattered) |
| Empty template fields | `Client ask:` with nothing after it, `Note: NA`, `Issue replication: Yes / By Support Yes`, `Ref number: …`, `Priority: S2` (keep priority only if S1) |
| Boilerplate closures | "We are closing this Service Request (SR) in Jira as the SR has already been closed in ServiceNow…", auto-close notices, duplicates of the same message |
| Links and files | SharePoint / Drive / attachment URLs → "(customer file attached)" at most |
| Personal data | Candidate names, emails, phone numbers → "a candidate", "one email address" |
| Machine pastes | `ISODate(…)`, `ObjectId(…)`, JSON/log dumps, `JIRA USER :`, `JIRA COMMENT :`, stack traces → describe the meaning in one phrase |
| Dates and names per comment | `[2026-05-05] First Last:` prefixes — keep a date only for a milestone that matters (e.g. "fix deployed 12 Jun") |

## Rules

1. **Solution comes from what actually happened**, usually buried in the discussion — never from a boilerplate closing comment. In the example below the real outcome is "remove the flagged email and re-upload; purge that one candidate manually", not "closed in ServiceNow".
2. Write roles, not people: *Support*, *Engineering*, *the customer*, *the vendor*.
3. Plain language over internal jargon; keep product terms customers use (automation, campaign, purge).
4. One idea per bullet. No nested bullets.
5. Same language as the ticket (English unless the ticket is not).
6. ServiceNow-only cases use the SN description + journal; escalated cases merge SN and Jira — never two separate summaries.

## Lint: when a row must be rewritten

`python3 skills/sr-triage/sr_triage.py lint-details <sheet.xlsx>` flags a row when any of these hold: markup tags, `@`-mentions, per-comment `[YYYY-MM-DD] Name:` prefixes, the boilerplate closure sentence, URLs, email addresses, empty template fields, more than 250 words, or a missing Problem / Discussions / Solution label.

## Example

Before (raw, abridged): template fields, 9 comments with @mentions and SharePoint link, two identical auto-close messages as the "Solution".

After:

```
Problem: The customer's monthly GDPR bulk-purge upload (a CSV of email addresses) failed in PROD with "Malicious content found in the file. Process is being aborted." Similar uploads had worked before.

Discussions:
- Support obtained the file; Engineering found the virus scanner matched one email address against a phishing signature and blocked the whole file.
- Customer escalated while the cause was investigated.
- Customer asked how to confirm that candidate was fully purged.

Solution: Remove the flagged email from the file and re-upload; purge that one candidate manually as a single request. No product change.
```
