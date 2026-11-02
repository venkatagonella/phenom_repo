# Google Slides Template Catalog — "Product - Slide Bank for Cursor"

Canonical Google Slides template the skill builds from.

- **Template ID:** `1r1WqCfvohkmfjEdmjzd0pJiFYznxPElyi4IWEZuaWNg`
- **Slides:** 37 (1-based index = the `template` field in a build spec)
- **Visual reference:** `references/google-template-thumbnails/slide-NN.png` (one PNG per slide; regenerate with `slides-thumbnails.ts`)

When building a Google deck, pick the template slide whose layout fits each content block, then fill its placeholders via `build-gslides.ts`. Use the **thumbnails** as the source of truth for what each slide looks like.

## How placeholders are filled

| Field | Mechanism | Use for |
|-------|-----------|---------|
| `replace` | `replaceAllText` scoped to the slide | Unique placeholders: `[Section]`, `[Slide Title]`, `[Metrics]`, `Title`, `Subtitle`, cover strings |
| `items` | position-ordered (top→bottom, left→right) per-shape replace | Repeated placeholders: `[Metric]`, `100,000`, `[Title]`, `[Event Title]`, `[Stage 1..n]`, `[Skill Name]` |
| `body` | replaces the longest lorem-ipsum text box | Prose / narrative paragraphs |
| `notes` | inserted into the slide's notes page | Speaker notes |

## Catalog

> **Exclude from output** (documentation/catalog slides): 4, 5 (Color Palette), 6, 21, 37 (category dividers "Slide Templates" / "Infographics" / "Assets"). Reuse the **divider layout** (slide 6) only by repurposing it for a *real* section divider.

| # | Layout | Use for | Key placeholders |
|---|--------|---------|------------------|
| 1 | Cover (navy + gradient thread) | Deck title slide | `Phenom Slide Templates` (title), `Cursor & Claude Skills` (subtitle) |
| 2 | Purpose / hero (navy) | One-line mission statement | hero line + small label |
| 3 | Title / Subtitle | Generic section title | `Title`, `Subtitle` |
| 6 | **Section divider** (gradient blob + rotated rail) | Real section breaks | section title text, `Phenom Partner Day 2024` footer |
| 7 / 8 | Agenda | Time/topic agenda | `[Agenda]`, `[Section]` |
| 9 | Quote + body | Pull quote / testimonial | quote text, `[Section]` |
| 10 | Section title (`[Slide Title]`) | Plain titled content frame | `[Slide Title]`, `[Section]` |
| 11 | Diagram + insights | Chart/mockup with insight bullets | `[Slide Title]`, `[Insight]` (items) |
| 12 | Metrics 6-up | 4–6 KPIs | `[Metric]` ×6, `100,000` ×6, `[Metrics]` (items + replace) |
| 13 | Metrics 3-up + accomplishments | 3 KPIs + prose | `[Metric]` ×3, `100,000` ×3, body |
| 14 | Metrics + table | KPIs blended with a table | `[Metrics with Table]`, numbers |
| 15 | Table | Table-only | `[Table]`, `[Section]` |
| 16 | Checklist (3-col) | Grouped checklists | `[Checklist]`, `[subtask 1..5]` (items) |
| 17 | Checklist + lead | Checklist with intro paragraph | `[Checklist Title]`, body |
| 18 | **Key Takeaways** (staircase) | Closing summary | `[Section]`, takeaway lines (items) |
| 19 | Timeline progression | Labeled stages over time | `[Timeline Progression]`, `[Title]`, `Month, Year` (items) |
| 20 | Product screenshot | Large image + paragraph | image (LEAVE EMPTY for manual paste), body |
| 22 | Cards with Icons | 3–4 parallel items | `[Title]` ×4 (items), `[Cards with Icons]`, body |
| 23 | Cards with Humans | 3–4 people/role cards | `[Title]` ×4 (items), images (manual) |
| 24 | Personas (detailed) | Single rich persona | name, role, `[Skill Name]` (items), bio body |
| 25 | Mind Map | 4-topic radial map | `[Mind Map Title]`, `[Topic One..Four]` (items) |
| 26 | 3-Step Loop | 3-stage cycle | `[Stage 1..3]` (items), `[Diagram Title]`, body |
| 27 | 4-Step Loop | 4-stage cycle | `[Stage 1..4]` (items) |
| 28 | 5-Step Loop | 5-stage cycle | `[Stage 1..5]` (items) |
| 29 | 4-Layer Funnel | Decreasing funnel | numbers (items), body |
| 30 | 4-Layered Blocks | Stacked layers | `[Layer Title]` ×4 (items) |
| 31 | 5-Layer Stack | 5-layer architecture | layer labels (items) |
| 32 | 3-Layer Stack | 3-layer architecture | layer labels + descriptions (items) |
| 33 | Timeline Horizontal | Milestones with years | `[Event Title]` (items), years (items) |
| 34 | Timeline Vertical | Vertical milestones | `[Event Title]` (items), years (items) |
| 35 | **Comparison — Today** (grayscale) | Before state (signature) | role labels, pain points (items) |
| 36 | **Comparison — Tomorrow** (color) | After state (signature) | role labels, improvements (items) |

## Per-section color family (Mint / Peach / Honey / Lilac)

The template's slides already carry their designed tints (cards rotate families; loops use Honey/Peach/Lilac; timeline markers rotate). In the Google route, color comes from the chosen template slide — there is no recolor step. To rotate families per section, rely on the template's built-in variety and section dividers. (Full programmatic recolor is a future enhancement; see SKILL.md "Known limitations".)
