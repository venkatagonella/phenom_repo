# Article types — phrasing guidelines

Use these after you pick a type in [voice-and-structure.md](voice-and-structure.md). Patterns are taken from Screening Community articles.

---

## 1. Overview — "What is X?"

**Job:** Orient someone who has never used the product. Do not document every feature.

**Reference:** [What is Screening?](https://community.phenom.com/kb/articles/10106-what-is-screening)

**How it reads:**

- Open with video (optional) then **1–2 paragraphs** on the problem and value.
- Benefits may be a short list, but each bullet is a **named benefit + one explanatory clause** — not a bare feature label.
- Describe the process in **prose** (who does what), then link to deep guides. Use numbered steps only for a short "getting started" path.
- End with Learn More links as a bullet list — the overview is a hub, not an encyclopedia.

**Avoid:** Turning the whole overview into four bullet lists (benefits, LinkedIn side, CRM side, getting started). That reads like a slide deck, not a Help Center article.

**Skeleton:**

```markdown
[optional video]

## Benefits of X
[1–2 paragraphs]
**Key benefits include:**
- **Name:** One-sentence explanation…
- **Name:** One-sentence explanation…

## The X process / experience
[prose: who participates and what happens]
#### Recruiter / LinkedIn side
[short paragraph + link to how-tos]
#### CRM side
[short paragraph + link to how-tos]

## Getting Started
[2–4 sentences or a short numbered path with links]

## Learn More
- [Related article]
- [Related article]
```

---

## 2. Feature / experience description

**Job:** Walk the reader through a product surface as the user experiences it (candidate journey, recruiter screen flow, widget behaviour).

**References:** [Mobile Experience](https://community.phenom.com/kb/articles/9636-mobile-experience), [Desktop Browser Experience](https://community.phenom.com/kb/articles/9823-desktop-browser-experience)

**How it reads (this is the prose-heavy type):**

- Open with **one paragraph** situating where the reader is in the journey and what this article covers ("This article will show you how… works within the mobile app").
- Each `##` heading is a **stage or screen** in order (Invitation email → Welcome page → Landing page → …).
- Under each heading: **paragraphs that narrate what the user sees and does**, then a screenshot. Explain edge cases in prose or a NOTE.
- Bullets appear only when listing several items on one screen (e.g. home screen contents). Prefer embedding those items in a sentence when there are only two or three.
- UI labels in **bold** or quotes when the user must click them.

**Avoid:**

- "What you get" / "What to check" tables as the main content
- Bullet lists under every heading
- Abstract capability inventories with no journey

**Skeleton:**

```markdown
After the user has [context], they can [choice]. This article will show you how [surface] works.

## Stage or screen name

[2–4 sentences: what appears, what the user does, what happens next.]

> **[SCREENSHOT NEEDED]** — …

[Optional NOTE for limits or exceptions.]

## Next stage or screen name
…
```

**LinkedIn examples of this type:** Profile Widget walkthrough; one-click export *screen* experience; CRM tab / In-CRM indicator as lived UI — not a field inventory.

For every article type, format Related articles / Learn More links at the end as one link per bullet. This is an intentional exception to the prose-first rule because link lists are reference inventories and easier to scan vertically.

---

## 3. How-to (task)

**Job:** Get the reader from prerequisites to a completed task.

**Reference:** [How to Access a Completed Screening…](https://community.phenom.com/kb/articles/9594-how-to-access-a-completed-screening-and-its-evaluations-in-the-crm)

**How it reads:**

- Open with prose (and optional video): what becomes possible and where in the product.
- Sections describe **where to go and what you will see**, in full sentences.
- Use **numbered steps** when order is strict. Use short bullets only for prerequisites or grouped options under a prose intro.
- Call out behaviour that surprises people in a NOTE after the relevant paragraph (not a separate mega-table unless comparing many fields).

**Avoid:** Opening with three stacked bullet lists before any explanation.

**Skeleton:**

```markdown
This article describes how to [task].

[Optional video]

## [First place in the product]

To [goal], go to [path]. You will see [what appears]. From here you can [actions].

> **[SCREENSHOT NEEDED]** — …

## [Next outcome]
[prose…]
```

**When a field inventory is required** (e.g. what syncs): introduce it in prose ("The integration can share the following candidate fields:"), then a compact list or table, then a **paragraph** clarifying the common misunderstanding (e.g. email not auto-filled on export). Never leave the inventory unexplained.

---

## 4. Setup / Activation guide

**Job:** Get the tenant connected or configured in the right order.

**References:** Screening Setup Guides; LinkedIn Activation Guide (12190)

**How it reads:**

- Short opener + critical NOTE (Admin required, one contract, production only, etc.).
- **`## Step N: Action`** with 2–4 instructional sentences and a screenshot per step.
- Do not bury license theory here — link to a Licenses / seats article.

---

## 5. FAQ

**Job:** Answer many discrete questions quickly without becoming a how-to.

**Reference:** [Screening FAQ](https://community.phenom.com/kb/articles/10973-screening-faq)

**How it reads:**

- Group under topic `##` headings.
- Each question is an `###` written as the customer asks it.
- Answer in **2–6 sentences of prose**. Lead with Yes / No / the rule.
- Bullets only when listing tiers, hours, or mutually exclusive options.
- End with "Find out more about [X] here" linking to the canonical article — do not paste the how-to into the FAQ.

**Avoid:** Tables of "in scope" at the top; multi-section essays under one question.

---

## 6. Troubleshooting

**Job:** Diagnose a symptom and recover.

**How it reads:**

- `###` = symptom in the user's words.
- **Cause** and **Fix** as short prose paragraphs (one or two sentences each), not only bold labels with fragments.
- Link to the deep article for permanent guidance.
- Keep "If that doesn't work" as a final sentence pointing to Care / Support with what to attach.

**Avoid:** Turning troubleshooting into a giant comparison table with no narrative.

---

## 7. Essentials guide (per role)

**Job:** A short day-in-the-life for one persona.

**How it reads:** Video, short prose per stage, numbered path, links to full how-tos. Title includes the audience ("Essentials Guide for Recruiters — …").

---

## 8. Privacy / Security FAQ

Same mechanics as FAQ; audience is a security reviewer. Separate article. Requires Legal/Privacy validation before publish.

---

## Quick self-check before handoff

| If you wrote… | Ask… |
|---------------|------|
| Bullets under almost every heading | Can this be 2–3 sentences that tell the story? |
| A table of capabilities | Did I introduce it and explain the gotcha in prose? |
| An overview that lists every feature | Did I link out instead of documenting in place? |
| An FAQ answer longer than ~6 sentences | Should this be a how-to with a link from the FAQ? |
| A feature article with no screenshots planned | Do I need a callout per major screen (Screening pattern)? |
