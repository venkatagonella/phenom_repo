---
name: Phenom-Slide-Creator
description: "Build Phenom-branded presentation decks from raw content, in EITHER Google Slides or HTML. Use this skill whenever a Phenom employee asks for a deck, slides, presentation, or pitch built in Phenom's theme, or mentions 'Phenom Deck Design', 'Phenom Slide Creator', 'Phenom template', 'Phenom format', 'on-brand slides', or supplies source material (Word doc, existing PPT, PDF, markdown, notes, or pasted text) that needs to be turned into Phenom-styled slides. Trigger even when the request is casual ('make me slides on X', 'turn this doc into a deck', 'I need a presentation for the partner meeting'). The skill ALWAYS asks 'Google Slides or HTML?' and a creativity level (1 On-brand / 2 Balanced / 3 Expressive) first, then builds an on-brand deck from the canonical Phenom template — varied layouts (cover, sections, KPIs, timelines, personas, diagrams, comparisons), Mint/Peach/Honey/Lilac palette, Poppins. Locked brand pods stay fixed at every level; higher levels allow recombined and invented layouts within the design principles."
license: Internal use, Phenom Inc.
---

# Phenom-Slide-Creator

This skill turns source material (a Word doc, an existing deck, a PDF, a markdown file, or pasted text) into a Phenom-branded slide deck, in one of **two output formats the user chooses at the start**:

- **Google Slides** — duplicates the canonical Phenom Google Slides template and fills placeholders. Fully editable, collaborative, on-brand. *Default for most decks.*
- **HTML** — a Phenom-branded, token-driven HTML deck (reveal.js + Poppins + Phosphor icons) that visually mirrors the Google template. Best for fast, self-contained, browser-presentable decks.

Both formats share the same content pipeline and the same design system (Mint/Peach/Honey/Lilac palette, Poppins, 16:9).

## When this skill triggers

- They drop a .docx, .pptx, .pdf, or .md file and say "turn this into a deck"
- They paste raw content (bullets, an outline, notes) and ask for slides
- They mention they need a deck for a Phenom meeting, partner day, customer pitch, internal review, board update, AE training, product launch, etc.

## The pipeline

1. **Intake**: choose output format + **creativity level** + gather source content and clarifications.
2. **Extraction**: turn the source into a clean, structured list of content blocks.
3. **Outline**: group content blocks into a presentation arc (with visual pacing + color rotation).
4. **Layout matching**: for each block, pick the best template slide / HTML component — deviating as much as the chosen creativity level allows, always within the design principles.
5. **Build**: Google Slides route OR HTML route (below).
6. **QA**: render to images and verify nothing overflows, repeats, or stays Lorem-ipsum.

Generate the deck directly — do not ask the user to approve the layout plan before building. Save iteration for after the user has reviewed the rendered deck.

---

## Phase 1 — Intake

Ask the following in one round (use AskUserQuestion). Don't assume format or creativity level.

- **Output format:** **Google Slides** or **HTML**?
- **Creativity level:** **1 · On-brand**, **2 · Balanced**, or **3 · Expressive**? (See "Creativity levels" below. Offer a recommended default based on audience — see the auto-pick rule.)
- **What is this deck for?** Audience and occasion (internal team, customer, partner day, board, executive review, training, launch, etc.).
- **Roughly how long?** Short (5-10 slides), medium (10-20), or full (20+). Skip if already stated.
- **Anything specific to emphasize or omit?**

If the user already supplied format + level + context in their first message, skip the question and proceed.

### Creativity levels

Pick how tightly to follow the template. The **locked pods** (Poppins, the four-family palette + navy, the logo, 16:9, legible contrast, no fabricated screenshots — see "Brand standards") **never change at any level**. Everything else flexes by level:

| Level | What's locked | What flexes | Best for |
|---|---|---|---|
| **1 · On-brand** | Catalog layouts / components used as-is | Content only | Board, executive, customer/partner, regulated, any high-stakes external deck |
| **2 · Balanced** *(default)* | Pods + the component vocabulary | Recombine/resize components, adjust composition & spacing, build **new** layouts from existing tokens, choose icons freely, design simple custom diagrams | Most internal decks, strategy/narrative decks |
| **3 · Expressive** | Pods only | Bold full-bleed type, custom data-viz, editorial layouts, motion (HTML) — any composition that still uses the palette + Poppins | Vision/keynote, marketing moments, launch hero decks |

**Auto-pick (recommend, then confirm):** external / board / regulated → **Level 1**; internal / strategy → **Level 2**; "make it wow" / keynote / launch → **Level 3**. Default to **Level 2** if unsure.

**Format interaction (important):** the Google Slides route is duplicate-and-fill, so it is **effectively Level 1 by construction** — new/recombined layouts aren't practical there. Levels 2–3 are realized in the **HTML route**. If the user picks Level 2–3 *and* Google Slides, tell them that and either (a) drop to Level 1 for Google Slides, or (b) switch to HTML to get the creativity they asked for.

At **Levels 2–3**, every invented or modified layout must still satisfy the **Design principles** (below). At **Level 3**, add a one-line rationale for any custom layout in that slide's speaker notes (so successful inventions can later be folded back into the template).

### Source content

Accept any of these. If the user mentions a file but didn't attach it, ask them to attach it before continuing.

| Source | How to extract |
|--------|----------------|
| .docx (Word) | `pip install python-docx --break-system-packages --quiet`, then read paragraphs, headings, tables. Headings become candidate section titles and slide titles. |
| .pptx / existing deck | Extract the text per slide (e.g. `python -c "from pptx import Presentation; ..."` after `pip install python-pptx --break-system-packages --quiet`, or read an exported PDF). Treat each slide's text as one content block. |
| .pdf | Read the PDF using the `pdf` skill conventions — use `pdftotext` or the skill's extraction scripts. Detect headings by font size if possible. |
| .md / .txt | Read directly. Headings (`#`, `##`) become structure markers. |
| Pasted text in chat | Parse the message body. Look for explicit structure (numbered lists, headings) first; fall back to paragraph breaks. |

---

## Phase 2 — Extraction

Produce an internal list of **content blocks**. A content block is the unit that will become one slide. Each block has:

- `title`: the working slide title (can be revised in Phase 5)
- `kind`: what type of content this is — pick from `cover`, `purpose`, `agenda`, `event_details`, `section_break`, `hero_idea`, `quote`, `executive_summary`, `key_takeaways`, `narrative_text`, `text_with_image`, `bullet_list`, `kpi_metrics`, `table`, `checklist`, `timeline_horizontal`, `timeline_vertical`, `process_steps`, `loop_3`, `loop_4`, `loop_5`, `loop_6`, `interval_loop`, `pyramid`, `inverted_pyramid`, `funnel`, `hierarchy`, `network`, `cards_with_icons`, `persona_1`, `persona_2`, `persona_3`, `persona_4`, `chart_columns_2`, `chart_columns_4`, `closing`, `appendix_break`, `full_bleed_photo`, `dense_text`
- `bullets` or `body`: the actual content
- `notes_seed`: a 1-2 sentence summary that will seed speaker notes

Detect `kind` from cues in the source:

- Numbered steps or "Step 1 / Step 2" patterns → `process_steps`, `timeline_horizontal`, or one of the loops based on count and whether the steps repeat.
- Tables in the source doc → `table` or `kpi_metrics` depending on whether the cells are numbers.
- "Q:" / "A:" or stat callouts (e.g., "73%", "$2.4M") → `kpi_metrics`.
- Quote marks around a sentence with attribution → `quote`.
- Words like "agenda", "schedule", "timing" → `agenda`.
- Words like "appendix" → `appendix_break`.
- "Our purpose", "Our mission", "We believe" → `purpose`.
- Persona-style content with name, role, quote, needs → `persona_1` / `_2` / `_3` / `_4` based on count.
- A list of features or value props (3-6 items each with a short label) → `cards_with_icons`.

### Visual reframe check (run on every block before finalizing `kind`)

Before accepting a text-based `kind`, ask: **"Could this content be presented more visually?"** Upgrade whenever possible:

- **3–6 parallel items** (features, principles, benefits, reasons, capabilities) → prefer `cards_with_icons` or the matching `loop_N` over `bullet_list`. Only use `bullet_list` if the items are genuinely unrelated or too long for a card label.
- **A journey, transformation, or change narrative** → prefer `timeline_horizontal` or `loop_4` over `narrative_text`. The prose can become step labels and short supporting captions.
- **A list of outcomes, priorities, or relative importance** → prefer `pyramid` or `inverted_pyramid` over `bullet_list`.
- **2–5 big numbers embedded in prose** → extract them into a `kpi_metrics` block; the prose becomes the speaker note.
- **A single strong claim with supporting context** → prefer `hero_idea` (ref 11) over `narrative_text`.
- **Only use `bullet_list` or `narrative_text`** if the content is genuinely dense explanatory prose with no discernible structure that a visual layout would serve.

Make sure every deck has, at minimum: one `cover` block, at least one `section_break` if the deck is medium or longer, and one `closing` or `key_takeaways` block at the end. Add them if they're missing from the source.

---

## Phase 3 — Outline

Order the content blocks into a presentation arc:

1. Cover (mandatory)
2. Optional purpose / hero statement (if the deck has one)
3. Optional agenda (for medium / long decks)
4. Section 1 → content blocks → Section 2 → content blocks → … (use section breaks **sparingly** — see rule below)
5. Key takeaways
6. Optional appendix break + appendix slides

For short decks (5-10 slides), skip the agenda and most section breaks.

### Section dividers: use sparingly (important)

Section dividers are **act breaks**, not topic labels. Use one only when there's a **major shift in the kind of content** — e.g. from concept/framework → "in practice", from product → pricing, from problem → solution. A good medium deck typically has **0–3 dividers total**, not one per topic.

- **Do not** put a divider in front of every topic. That fragments the flow and reads as filler.
- Each content slide already carries its own `[Section]` kicker (the small label above the title) — that's what tells the audience which topic they're in. The kicker does the labeling; the divider is reserved for genuine gear-changes.
- If you find yourself adding a divider before most content slides, remove them and keep only the 1–2 that mark real act boundaries.

### Visual pacing (enforce during outline)

After ordering the blocks, scan the sequence for text-heavy clusters:

- **No more than 2 consecutive text-heavy slides** (quote, executive summary, narrative, bullets, dense text). After 2 in a row, the next slide must be a visual break: a diagram (loop / funnel / stack / mind map), KPI/metrics callout, comparison, timeline, or cards.
- **Visual breathing room comes from layout variety, not dividers.** Rotate layouts and color families so consecutive topics feel distinct. Reserve section dividers for the rare act-level switch (see "Section dividers: use sparingly").

### Color family rotation (Mint / Peach / Honey / Lilac)

The Phenom palette has four named families: **Mint** (primary/default), **Peach**, **Honey**, **Lilac** — each a full shade ramp (see `references/google-template-thumbnails/slide-05.png` for the canonical hex values, also encoded in `assets/html-template/phenom-tokens.css`).

**Rotate one family per topic/section** to visually separate content (this — not dividers — is the primary way topics stay distinct):
- Topic 1 → Mint · Topic 2 → Peach · Topic 3 → Honey · Topic 4 → Lilac · then repeat.
- Within a single topic, hold the family consistent (accents, card tints, and the divider if that topic has one).
- Some multi-item layouts intentionally rotate all four families *within* one slide (e.g. cards-with-icons, timeline markers) — that is correct and matches the template.
- Cover and purpose slides use the deep navy background regardless of section.

---

## Design principles (the creative guardrails)

These are the *principles*, not patterns — they are what makes Levels 2–3 safe. Any layout you reuse, modify, or invent must satisfy all of them. They are how the deck stays unmistakably Phenom even when the composition is new.

1. **One idea per slide.** Each slide makes a single point. If it has two, split it.
2. **One focal point.** Establish a clear visual hierarchy — the eye should know where to land first (size, weight, color, or position).
3. **Generous whitespace.** Don't fill the canvas. Breathing room reads as premium; density reads as a document.
4. **Align to a grid.** Edges line up; the header (`[Section]` kicker + title + hairline rule) anchors content slides.
5. **Contrast by construction.** Pastel family tints as fills, the dark end of the family (or `--ink`) for text. Never light text on light fills.
6. **One family per section, rotate between sections.** Never mix families within a section (except the intentional multi-item rotations — cards, timeline markers). Cover/purpose stay navy.
7. **Show, don't list.** Prefer a diagram, metric, comparison, or cards over a bullet list (see the Phase 2 reframe check).
8. **Earn every deviation.** At Levels 2–3, invent only when it serves the content better than the catalog would — not for novelty. Consistency is alignment, not sameness.

---

## Phase 4 — Layout matching

Pick the layout for each content block from the catalog that matches the chosen output format:

- **Google Slides route** → read `references/gslides_template_catalog.md` and use the slide thumbnails in `references/google-template-thumbnails/`. Each block maps to a template slide index (1–37).
- **HTML route** → use the components in `assets/html-template/` (`template.html` shows one live example of each: cover, purpose, divider, metrics, cards, loop, timeline, quote, takeaways).

### How freely to deviate (by creativity level)

- **Level 1** — use catalog layouts / components exactly as-is. No new layouts. (This is the only mode the Google Slides route supports well.)
- **Level 2** — start from the catalog, but recombine and resize components, adjust composition/spacing, and build **new** layouts out of the existing tokens (HTML route) when they fit the content better. Every result must pass the Design principles.
- **Level 3** — treat the catalog as inspiration; compose freely (full-bleed type, custom diagrams/data-viz, editorial layouts, motion) using only the locked pods. Note the rationale in speaker notes.

### Upgraded fallback hierarchy (apply for both routes)

When a block looks like a plain bullet list or narrative, promote it before accepting a text layout:

1. 3–4 short parallel items → **cards with icons** (rotate families across cards).
2. A single bold claim + supporting detail → **purpose / hero**.
3. A sequence of stages → **loop** (cyclical) or **timeline** (chronological).
4. A before/after or current-vs-future contrast → **Comparison Today/Tomorrow** (signature layout; slides 35/36).
5. 2–5 numbers → **metrics**.
6. Only fall back to a text/narrative layout if none of the above fits.

### Variety + signature-layout rules

- Don't use the same layout twice in a row; alternate variants when a layout type repeats.
- **Comparison Today/Tomorrow** is reserved for before/after vision narratives. **Personas** and **Mind Map** only when content is explicitly about people or a concept map.
- **Never include** the template's documentation slides (Color Palette, "Slide Templates", "Infographics", "Assets"). Reuse the *divider layout* only for real sections.

Output of this phase is a plan list — one row per slide, with: position, block, chosen template slide index (Google) or component (HTML), and the section's color family.

---

## Phase 5 — Build

Use the route the user picked in Phase 1.

### Route A — Google Slides (default)

The build is driven by **`mcp/build-gslides.ts`**, which duplicates the canonical template, deletes unused slides, and fills placeholders. It is token-efficient (1–3 batched API calls). All commands run from the `Phenom - Product Copilot/mcp` directory.

**Step A1 — Make the working copy.** The current Google connection has read-only Drive scope, so the script cannot copy the template itself. Ask the user (once) to open the template and **File ▸ Make a copy**, then paste the new deck's URL/ID. (If/when a Drive-write scope is added, omit `deckId` and the script auto-copies — see "Known limitations".)

> Template to copy: `https://docs.google.com/presentation/d/1r1WqCfvohkmfjEdmjzd0pJiFYznxPElyi4IWEZuaWNg/edit`

**Step A2 — Write the build spec** (`/tmp/phenom_spec.json`). One entry per output slide, in order. `template` is the 1-based template slide index from `references/gslides_template_catalog.md`:

```json
{
  "deckName": "Q3 Board Review",
  "deckId": "<the copy's id>",
  "slides": [
    { "template": 1, "replace": { "Phenom Slide Templates": "Q3 Board Review", "Cursor & Claude Skills": "Phenom Product" }, "notes": "Open and frame the three themes." },
    { "template": 6, "replace": { "Slide Templates": "Product Innovation" } },
    { "template": 12, "replace": { "[Section]": "Product Innovation", "[Metrics]": "Impact at a glance" },
      "items": { "100,000": ["4,123","$4M","150%","99.9%","12","3"], "[Metric]": ["Interviews","Saved","Lift","Uptime","Markets","Weeks"] } },
    { "template": 18, "replace": { "[Section]": "Summary" }, "items": { "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor.": ["Point one.","Point two.","Point three.","Point four."] } }
  ]
}
```

- `replace` → unique placeholders (`[Section]`, `[Slide Title]`, `[Metrics]`, `Title`, `Subtitle`, cover strings).
- `items` → repeated placeholders filled in reading order (metrics, cards `[Title]`, `[Stage n]`, timeline `[Event Title]`, `[Skill Name]`, takeaway lines).
- `body` → replaces the longest lorem paragraph (prose slides).
- `notes` → speaker notes (2–4 sentences; the *what* and the *why*).

**Step A3 — Run the build:**

```bash
npx tsx build-gslides.ts /tmp/phenom_spec.json
```

It prints the deck URL. See `references/gslides_template_catalog.md` for the per-slide placeholder/items tokens.

### Route B — HTML

**Step B1 — Copy the template folder** to the output location:

```bash
cp -r "skills/phenom-slide-creator/assets/html-template" "<output>/<deck-name>"
```

The folder contains `template.html` (reveal.js shell + one live example per layout), `phenom-tokens.css` (palette + type, extracted from the Google template), and `phenom-deck.css` (component library). Phosphor icons + Poppins load via CDN.

> **Full-screen requirement (already baked into `phenom-deck.css`):** `html, body { width:100%; height:100%; }` must be present. reveal.js sizes each 1280×720 slide to fill the window by scaling it, but only if the viewport reports a real height. Without the full-height rule the viewport collapses to the slide's natural 720px, so reveal never scales up and the deck renders pinned to the top-left in a small box. Don't remove this rule. (Note: a headless screenshot at exactly `--window-size=1280,720` hides this bug because no scaling is needed — always sanity-check the deck in a normal-sized browser window too.)

**Step B2 — Author the slides.** In the copied `template.html`, replace the example `<section>` slides with one `<section><div class="slide …">…</div></section>` per content block, using the components in `phenom-deck.css`:

- `slide--cover`, `slide--purpose`, `slide--divider` (set `data-family` per section), `metrics-grid` + `metric-tile`, `cards-row` + `icon-card` (set `data-family` per card, Phosphor `<i class="ph ph-…">`), `diagram-split` + `loop`, `timeline`, `quote`, `takeaways`.
- Every content slide uses the `.s-head` header (`.s-kicker` = section, `.s-title` = bracketed-style title, `.s-rule`).
- Set `data-family="mint|peach|honey|lilac"` on each `.slide` to apply the section's color family. Rotate families per section.
- **Do not hardcode colors** — use the CSS variables. To evolve the look, edit `phenom-tokens.css` / `phenom-deck.css`; every deck inherits the change.
- At **Levels 2–3**, add new component classes in `phenom-deck.css` (or per-deck `<style>`) rather than inline one-off styles, and build them from the existing CSS variables so they stay on-brand. Honor the Design principles.

**Step B3 — Portability (ask if the deck must work offline / be emailed).** By default the template pulls reveal.js, Poppins, and Phosphor from CDNs (needs internet at present time). For a fully self-contained, offline/email-safe single file, **vendor the dependencies**: download reveal.js CSS+JS, the Poppins woff2 files (with `@font-face`), and the Phosphor CSS+font into the deck folder (or inline them into `template.html`) and repoint the `<link>`/`<script>` tags locally. Prefer this for any deck that will be presented on an untrusted network or shared as a file.

### Images (both routes)

- **Conceptual / illustrative images** → generate with `GenerateImage` (clean, modern, editorial; no text overlays, logos, or fake screenshots). Google route: the script doesn't embed images, so add generated images manually or note them; HTML route: save into the deck folder and reference with `<img>`.
- **Real product screenshots** → **leave the slot empty** and add a note for the user to paste the actual screenshot. Never fabricate a product UI.
- **Never reuse the template's built-in stock photos.**

---

## Phase 6 — QA

This phase is non-negotiable. The first render almost always has at least one real issue.

### Render to images and inspect

- **Google Slides route:** `npx tsx slides-thumbnails.ts <deckId> /tmp/phenom_qa` (from `mcp/`), then read the PNGs.
- **HTML route:** screenshot with headless Chrome —
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --window-size=1328,5400 --screenshot=/tmp/phenom_qa.png "<output>/<deck-name>/template.html"
  ```
  (For per-slide capture, load `template.html#/N`.)

Inspect (use a subagent for fresh eyes) and flag: leftover `[placeholders]` or lorem, text overflow, overlapping shapes, mismatched item counts, low-contrast text, two consecutive slides with the same layout, any remaining template stock photo, and — for Levels 2–3 — any invented layout that breaks a locked pod or a Design principle (off-palette color, non-Poppins font, mixed families in one section, no clear focal point, cramped whitespace).

After the visual QA pass, fix issues and re-verify once. Don't loop on sub-pixel positioning.

---

## Deliverable

- **Google Slides:** share the deck URL the build script printed.
- **HTML:** share the path to the deck folder's `template.html`.

Plus a short note (≤4 lines), e.g.:

> Built a [N]-slide [Google Slides/HTML] deck for [audience/occasion]. Layouts: cover, 3 section dividers, KPI metrics, 4-step loop, comparison, timeline, key takeaways. Open it to review — happy to iterate on any slide.

Do not write a long per-slide postamble.

---

## Brand standards (the locked pods — never override, at any creativity level)

These are the non-negotiable elements that keep every deck recognizably Phenom even at Level 3. Encoded in `assets/html-template/phenom-tokens.css` and the Google template:

- 16:9 aspect (1280×720 authoring stage)
- **Poppins** (Regular 400, Medium 500, SemiBold 600, Bold 700)
- Type scale: 40px slide title, 52px metric numbers, 18px subhead, 15px body, 13px small, 11px footnote
- Neutrals: `#1a1c2e` primary ink, `#434343` secondary, `#6b6b73` tertiary, `#ffffff` on dark
- Cover/purpose background: deep navy `#131a4a`
- **Palette — four families, each a full ramp** (use the lightest 1–2 shades as fills, darkest for text):
  - Mint `#daf3f2…#203634` (primary) · Peach `#f6e2d5…#46210c` · Honey `#faedd7…#493614` · Lilac `#e9e6f9…#0a0d37`
- Rotate one family per section. Cover keeps navy.
- Never substitute fonts; never invent colors outside these ramps.

---

## Known limitations

- **Drive copy requires a write scope the Google connection currently lacks** (it has `drive.readonly` + `presentations`). Until a `drive.file`/`drive` scope is added to the copilot OAuth, the Google route needs the user to make the copy manually (Step A1). Once added, `build-gslides.ts` auto-copies (omit `deckId`).
- **No programmatic recolor in the Google route.** Color comes from the template slide chosen; per-section family rotation relies on the template's built-in variety + dividers. (HTML route rotates families freely via `data-family`.)
- **Test decks named `ZZ TEST …`** created during setup live in your Drive root and are safe to delete.

---

## Common pitfalls (read once)

- **Skipping the format / creativity-level question.** Always ask Google Slides vs HTML and the creativity level first (Phase 1).
- **Sameness.** Applying Level-1 strictness to every deck makes them all look identical (the #1 complaint about template-locked AI decks). Match the level to the audience; at Levels 2–3, vary composition within the Design principles.
- **Promising Level 2–3 creativity on the Google Slides route.** That route is effectively Level 1; route ambitious decks to HTML.
- **Defaulting to text slides when a visual layout would work.** Apply the visual reframe check (Phase 2) and the upgraded fallback hierarchy (Phase 4).
- **Leaving stock template photos or lorem/`[placeholders]` behind.** Generate contextual images or leave empty with a note; QA every slide.
- **Reusing the same layout twice in a row.** Alternate variants.
- **Setting different values on repeated placeholders via `replace`.** Use `items` (position-ordered) for metrics/cards/timeline/stages — `replace` would set them all identical.
- **Including documentation slides** (Color Palette, "Slide Templates", "Infographics", "Assets"). Exclude them.
- **Mixing color families within a section.** One family per section; rotate between sections.
- **Over-using section dividers** (one per topic). Dividers are act breaks, used sparingly (0–3 per deck); the per-slide `[Section]` kicker labels each topic. See "Section dividers: use sparingly".
- **(HTML) Removing the full-height `html, body` rule** from `phenom-deck.css` — the deck then renders in a small top-left box instead of filling the window. QA in a normal browser window, not just a 1280×720 headless capture.
- **Skipping speaker notes.** Every slide gets 2–4 sentences (the *what* and the *why*).
- **Fabricating product screenshots.** Leave real screenshots empty for the user.

---

## File locations

All paths relative to `Phenom - Product Copilot/`.

**Skill:**
- This skill: `skills/phenom-slide-creator/SKILL.md`

**Google Slides route:**
- Canonical template: deck ID `1r1WqCfvohkmfjEdmjzd0pJiFYznxPElyi4IWEZuaWNg`
- Catalog (template index → layout → placeholders/items): `skills/phenom-slide-creator/references/gslides_template_catalog.md`
- Visual reference thumbnails: `skills/phenom-slide-creator/references/google-template-thumbnails/slide-NN.png`
- Build script: `mcp/build-gslides.ts` — `npx tsx build-gslides.ts <spec.json>` (run from `mcp/`)
- Thumbnail script: `mcp/slides-thumbnails.ts` — `npx tsx slides-thumbnails.ts <deckId> <outDir>`
- Auth: reuses the copilot Google token (`~/.copilot/tokens.json`) via `mcp/src/auth`.

**HTML route:**
- Template folder: `skills/phenom-slide-creator/assets/html-template/` (`template.html`, `phenom-tokens.css`, `phenom-deck.css`)
