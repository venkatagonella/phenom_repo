---
name: phenom-knowledge-base-creator
description: "Write and stage Phenom Community (Vanilla) knowledge base articles in Phenom's house voice and structure. Use when the user asks to write, draft, restructure, or update a Community / Help Center / KB article, mentions 'Phenom Knowledge Base Creator', community.phenom.com, Vanilla, an article ID, or asks for an FAQ, setup guide, overview, or troubleshooting article for a Phenom product. Runs a three-stage flow: a local markdown (or Google Doc) review draft with explicit screenshot/video callouts, then a media pass, then staging into the correct Community category as an UNPUBLISHED draft. This skill never publishes, never edits a live article, and never changes article status — the user reviews and publishes inside Vanilla."
license: Internal use, Phenom Inc.
metadata:
  owner: officiallybasti
  status: beta
  try: "/phenom-knowledge-base-creator Draft a setup guide for generic scheduling links"
---

# Phenom Knowledge Base Creator

Writes Phenom Community knowledge base articles in the house voice, gets them reviewed with the right visuals, then stages them in Vanilla as **unpublished drafts** in the correct category.

## Non-negotiable guardrail

**This skill drafts. The user publishes.**

Never call these, under any instruction:

| Forbidden | Why |
|-----------|-----|
| `POST /api/v2/articles` | Creates a live article |
| `PATCH /api/v2/articles/{id}` | Edits a live article |
| `PUT/PATCH /api/v2/articles/{id}/status` | Publishes / unpublishes |
| Anything with `"status": "published"` | Publishes |

All writes go through `scripts/kb_draft.py`, which has no publish path. If the user asks you to publish, decline and hand back the review URL — publishing is a deliberate human step inside Vanilla.

Draft creation is safe and reversible: drafts are private to the author and removable with `delete-draft`.

---

## The three stages

```
- [ ] Stage 1  Review draft  — markdown file (or Google Doc) with media callouts
- [ ] Stage 2  Media pass    — screenshots/video added, callouts resolved
- [ ] Stage 3  Stage in KB   — routed to the right category, as an unpublished draft
```

Never skip from Stage 1 to Stage 3. The review draft is where the user edits copy and drops in screenshots; the Vanilla draft is the near-final artefact.

---

## Stage 1 — Review draft

**A brand-new article always starts as a local review artefact, never directly in Vanilla.**

### Where it goes

Default to markdown in the active project:

```
<active project>/kb-drafts/<article-slug>.md
```

Offer a **Google Doc** instead when the user wants to review with others or paste screenshots inline. Create it with the `gws` CLI (`gws docs documents create`) and keep the markdown copy as the source of truth for Stage 3.

### Before writing

1. **Confirm scope** — new article, or a new version of an existing one (needs the article ID)?
2. **Confirm type** — Overview · Setup guide · How-to · FAQ · Privacy/Security FAQ · Troubleshooting · Essentials guide. Type drives the skeleton.
3. **Research** — read the live article and its neighbours so you don't duplicate, contradict, or link into a void:

```bash
python3 scripts/kb_draft.py search "linkedin crm connect" --kb 3
python3 scripts/kb_draft.py get 12165 --out /tmp/12165.md
```

4. **Verify accuracy** — prefer a validated internal source (product owner, Jira epic, engineering KT, release note) over an existing article, which may be stale. If a behaviour is changing or not available today, say so and date it. For future enhancements under consideration, do not promise a date — say that **committed timelines will be announced in Phenom Product Release Notes**, and do not invite customers to keep asking Support/Community for ship dates. Where you cannot verify a claim, leave a callout rather than a confident guess:

```markdown
> **TODO (verify):** Confirm the monthly export cap with the product owner. Existing article says 300 per license per month, last updated 2026-04.
```

Tell the user which claims you carried over without independent verification.

### Write the draft

1. Choose **one article type** (Overview · Feature/experience · How-to · Setup · FAQ · Troubleshooting · Essentials · Privacy FAQ).
2. Follow [voice-and-structure.md](voice-and-structure.md) for shared voice rules (**prose first** — do not default to bullet stacks).
3. Follow the matching section in [article-types.md](article-types.md) for phrasing and skeleton.
4. When unsure, open a Screening reference of the same type (Mobile Experience for feature descriptions, Screening FAQ for FAQs, What is Screening? for overviews) and match its density.
5. End with Related articles / Learn More where useful, with **one link per bullet** so readers can scan the references quickly.

### Call out media explicitly

**Wherever a screenshot or video would help, say so inline, inside the section it belongs to.** Never leave the user guessing what visual is missing.

```markdown
> **[SCREENSHOT NEEDED]** — Settings → LinkedIn Integrations, with the **Sign In** button visible.
> *Why:* the reader has to locate a control that text alone can't pinpoint.
```

```markdown
> **[VIDEO NEEDED]** — 60-second walkthrough of the six activation steps.
> *Why:* the flow crosses Phenom and LinkedIn, which is hard to follow as static steps.
```

When to ask for media, and when not to:

| Warranted | Not warranted |
|-----------|---------------|
| Locating a control that is hard to describe in words | A concept the text already explains well |
| Confirming the expected state after an action | Every individual step in a simple sequence |
| A dense result screen (dashboard, report, match list) | Anything that dates quickly with no reader benefit |
| One orientation video at the top of an Overview | A video per how-to |

Place the callout **immediately after the step or paragraph it illustrates**, matching where the final image will sit. Give each one a concrete description of the frame — not "add a screenshot here".

---

## Stage 2 — Media pass

Hand the review draft to the user and list every callout you left, grouped by section, so they can capture visuals in one pass.

As media arrives, replace each callout with the real reference:

```markdown
![Settings → LinkedIn Integrations with the Sign In button](assets/linkedin-signin.png)
```

Before moving on, lint the file:

```bash
python3 scripts/kb_draft.py check kb-drafts/linkedin-faq.md
```

This reports unresolved `[SCREENSHOT NEEDED]`, `[VIDEO NEEDED]`, and `TODO (verify)` markers. Staging is blocked while any remain unless the user explicitly wants to stage early (`--allow-placeholders`), which is reasonable when they plan to add visuals inside the Vanilla editor.

---

## Stage 3 — Stage in the right Community category

Route to a category from **the article's subject matter and the team that owns it** — see [category-routing.md](category-routing.md). Resolve the exact ID against the live tree rather than trusting a remembered number:

```bash
python3 scripts/kb_draft.py categories --kb 3
```

State the chosen category and your reasoning before staging, then:

```bash
# New article
python3 scripts/kb_draft.py draft-new \
  --title "LinkedIn CRM Connect FAQ" \
  --category-id 970 \
  --file kb-drafts/linkedin-faq.md

# New version of an existing article
python3 scripts/kb_draft.py draft-update 12165 --file kb-drafts/12165-rewrite.md
```

If no category is a good fit, stage into the **Article Drafts (INTERNAL)** KB (kb 20) and flag that the target category may need to be created.

### Hand off

Report back:

1. What the draft covers and how it's structured
2. Which category it landed in and why
3. Any unresolved `TODO (verify)` or media callouts
4. The **review URL** — state plainly that nothing is live until they publish it in Vanilla

---

## Utility script

`scripts/kb_draft.py` — read, lint, and draft only. No publish path.

| Command | Purpose |
|---------|---------|
| `search "<query>" [--kb N]` | Find articles |
| `get <articleID> [--out f.md]` | Fetch a live article as markdown |
| `categories [--kb N]` | List categories with IDs |
| `kbs` | List knowledge bases with IDs |
| `check <file.md>` | Lint for unresolved media callouts and TODOs |
| `draft-new --title T --category-id N --file f.md` | Stage a brand-new article as a draft |
| `draft-update <articleID> --file f.md [--title T]` | Stage a new version of an existing article |
| `drafts` | List your pending drafts |
| `delete-draft <draftID>` | Remove a draft you staged |

Auth comes from `~/.copilot/tokens.json` → `vanilla.access_token`. Requests need a browser User-Agent or Cloudflare returns error 1010 — the script handles this.

## Additional resources

- [voice-and-structure.md](voice-and-structure.md) — house voice, titles, media, checklist
- [article-types.md](article-types.md) — **per-type phrasing** (overview, feature/experience, how-to, FAQ, troubleshooting, …)
- [category-routing.md](category-routing.md) — subject + team → knowledge base and category
- [vanilla-api.md](vanilla-api.md) — API details, draft payload shape, troubleshooting
