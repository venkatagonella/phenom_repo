# Voice & structure — Phenom Community articles

House style is derived from the **Screening KB** (kb_id 29). Reference articles:

| Type | Example |
|------|---------|
| Feature / experience description | [Mobile Experience](https://community.phenom.com/kb/articles/9636-mobile-experience), [Desktop Browser Experience](https://community.phenom.com/kb/articles/9823-desktop-browser-experience) |
| Overview | [What is Screening?](https://community.phenom.com/kb/articles/10106-what-is-screening) |
| How-to | [How to Access a Completed Screening…](https://community.phenom.com/kb/articles/9594-how-to-access-a-completed-screening-and-its-evaluations-in-the-crm) |
| FAQ | [Screening FAQ](https://community.phenom.com/kb/articles/10973-screening-faq) |
| Setup | [Setup Guide - Basic Screening](https://community.phenom.com/kb/articles/11823-setup-guide-basic-screening) |

**Type-specific phrasing:** [article-types.md](article-types.md) — read the matching section before drafting.

---

## Article titles vs FAQ questions

**Article titles are topic labels, not customer questions.**

| Type | Title pattern | Examples |
|------|---------------|----------|
| FAQ | `{Product} FAQ` | Screening FAQ |
| Feature / experience | Noun phrase for the surface | Mobile Experience · Desktop Browser Experience |
| How-to | Task or outcome | How to Access a Completed Screening… · One-Click Export and Contact Fields |
| Setup | `{Product} Activation Guide` / `Setup Guide - {Tier}` | LinkedIn CRM Connect Activation Guide |
| Overview | `What is {Product}?` (only common `?` title) | What is Screening? |
| Troubleshooting | `Troubleshooting {Product}` | Troubleshooting LinkedIn CRM Connect |

Customer questions belong as **`###` headings inside** FAQs — not as article titles.

---

## Voice (all types)

Plain, precise, second person. State the rule, then the conditions.

| Do | Don't |
|----|-------|
| "No — recruiters must export candidates manually." | "Candidate flow is seamlessly orchestrated." |
| "This article describes how…" / "This article will show you how…" | "Welcome! In this exciting guide…" |
| "Ask your LinkedIn Admin to confirm the seat type." | "You may want to consider possibly reaching out." |

Rules:

1. **Prose first.** Default to short paragraphs that explain what happens and why. Do **not** turn every article into a bullet stack. Screening feature articles (Mobile / Desktop Experience) are ~0–10% bullet lines; they narrate the journey screen by screen.
2. **Bullets are for inventories, not for the story.** Use lists only for discrete options, field names, tier comparisons, support hours, or a short set of UI items on one screen. If a bullet needs a clause longer than one line, make it a sentence in a paragraph instead.
3. **Answer first** in FAQs and troubleshooting (Yes / No / the constraint, then nuance).
4. **Name who owns the constraint** (Phenom vs LinkedIn Admin vs browser vs customer config).
5. **Second person, present tense.** Prefer "you" / "the recruiter" / "the candidate" over passive voice.
6. **No marketing language** in KB ("seamless", "quick wins", "survival guide").
7. **No roadmap promises.** Unavailable today → say so. Under consideration → **official timeline only via Phenom Product Release Notes**; do not invite ship-date chasing.
8. **One job per article.** Cross-link instead of repeating.
9. **No "In scope / out of scope" table** at the top. Open with one or two sentences that state what the article covers; use Related articles for boundaries.
10. **`NOTE:` for hard limits only.** Date volatile content with `*Current as of: YYYY-MM-DD*`.

---

## Pick a type, then write

Before drafting, choose **one** type and follow [article-types.md](article-types.md):

| Type | When to use | Density |
|------|-------------|---------|
| **Overview** | First orientation ("What is…") | Short prose + a few explained benefit bullets; links out |
| **Feature / experience description** | Walk through a product surface end-to-end | **Mostly paragraphs**; heading per screen/stage; screenshot after each |
| **How-to** | One task with a clear outcome | Prose context + numbered steps where sequence matters |
| **Setup guide** | Activation / configuration spine | Numbered steps or phases; short prose between steps |
| **FAQ** | Many discrete customer questions | Question heading + 2–6 sentence answer; bullets rare |
| **Troubleshooting** | Symptom → recovery | Symptom heading + Cause / Fix in prose |
| **Essentials guide** | Role day-in-the-life | Short stages, links to deep how-tos |
| **Privacy / Security FAQ** | Controller / security reviewer | Same as FAQ; separate article; Legal validation |

If the draft is mostly bullets under every heading, it is almost certainly the wrong shape — rewrite in prose and keep lists for true inventories.

---

## Media callouts

Place callouts **inside the section** they illustrate, with a concrete frame description:

```markdown
> **[SCREENSHOT NEEDED]** — Settings → LinkedIn Integrations, with the **Sign In** button visible.
> *Why:* the reader has to locate a control that text alone can't pinpoint.
```

Feature / experience articles usually need **more screenshots** (one per major screen). Overviews need **fewer** (video + 1–2 orientation shots). FAQs rarely need screenshots unless the answer is UI-specific.

Run `kb_draft.py check <file>` before staging.

---

## Structural conventions

- `##` sections, `###` FAQ questions / sub-sections — don't skip levels
- Screenshot immediately after the paragraph that describes that screen
- Tables for comparisons and field inventories — not as a substitute for explanation
- Put Related articles / Learn More at the end and format every link as a separate bullet for easy scanning

---

## Pre-handoff checklist

- [ ] Correct **article type** chosen; [article-types.md](article-types.md) followed
- [ ] Prose carries the explanation; bullets only where they earn their place
- [ ] One job, one audience
- [ ] FAQ headings are real customer questions; answers lead with the rule
- [ ] Constraints attributed to the owning system
- [ ] Future items point to Release Notes — no ship-date invites
- [ ] Cross-links resolve; volatile claims dated; `TODO (verify)` for unverified claims
- [ ] Related articles / Learn More links are formatted as a bullet list
- [ ] Media callouts placed in-section where visuals are needed
