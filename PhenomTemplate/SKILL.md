---
name: phenom-brand-template-2026
description: >-
  Builds and edits Google Slides in the 2026 Phenom Brand Book template: the
  black left panel + Bone content layout, Fraunces / DM Sans / VT323 type,
  Cosmic Indigo / Mirage Dust palette, section dividers, tables and guideline
  grids. Runs a missing-field preflight before touching any slide and keeps
  titles short and bullets scannable. Use when creating or modifying slides or
  decks "in the Phenom brand template", "Brand Book 2026 format", or when the
  user mentions the 2026 Phenom Brand Book gslides, Brand Guidelines deck, or
  asks to match its layouts. For brand rules without slides use
  phenom-brand-2026; for product UI use phenom-design-system.
---

# Phenom Brand Template 2026 (Google Slides)

## Source of truth

| Item | Value |
|---|---|
| Deck | `Copy of 2026 Phenom Brand Book` (Google Slides) |
| Presentation ID | `1oaSCPDh-u88LMYTH4FxUFRDNh0h1SyiwxtCUR1eW9BI` |
| Local pointer | `~/Library/CloudStorage/GoogleDrive-venkata.gonella@phenom.com/My Drive/Copy of 2026 Phenom Brand Book.gslides` (JSON stub; never edit it) |
| Canvas | 720 × 405 pt (16:9), 20 slides |
| Snapshot | revision `nmHlnU9QV_CVbw`, read 2026-11-24 |

Always re-read the deck (`read_presentation`) before editing. Do not trust this snapshot over the live file.

## Critical: this template has no placeholders

All 20 slides use one layout, **White Blank** (`g3f9d847fdca_0_8`). Titles, kickers and body copy are plain text boxes; the black panel is a rectangle. `add_slide` with a layout therefore yields an empty slide. The other 28 layouts in the master (White Content, Black Grid, Title Slide, …) are unused by any brand slide.

So "match layouts and placeholders" means: **duplicate an existing slide and replace text by objectId**. Never rebuild a slide from scratch or use an unused master layout unless the user asks.

## Workflow

Copy and track:

```
- [ ] 1. Read deck (read_presentation) and pick the archetype from layouts.md
- [ ] 2. Run the missing-field preflight (below) and report it
- [ ] 3. Wait for answers if any required field is missing
- [ ] 4. Duplicate the source slide (duplicate_object), then set_shape_text per field
- [ ] 5. Verify: read_slide_layout (lints) + get_slide_thumbnail
- [ ] 6. Summarize what changed and any flags
```

### Preflight: flag missing template fields (before modifying anything)

1. Match the request to one archetype in [layouts.md](layouts.md).
2. List that archetype's fields from [template-fields.md](template-fields.md).
3. Compare with what the user supplied. Output this table first:

```markdown
| Field | Status | Note |
|---|---|---|
| Kicker | Missing | e.g. MESSAGING |
| Title | Provided | "Tone of Voice" (13 chars) |
| Lead line | Provided | |
| Body | Provided | Too long: trim to ≤ 60 words |
| Image | Not in template | Slide has no image slot; add? |
```

4. Status values: **Provided**, **Missing** (template has it, user did not give it), **Not in template** (user content has no matching field), **Needs edit** (breaks a rule in content-rules.md).
5. If any required field is **Missing** or **Not in template**, stop and ask (use AskQuestion). Do not invent copy, delete boxes, or add new text boxes silently. Proceed only if the user says to use defaults or to leave fields empty.
6. Optional fields may stay empty; say so in the table.

## Hard rules

1. Fonts: **Fraunces** for titles and numerals, **DM Sans** for everything else, **VT323** for button labels only.
2. Palette from [tokens.md](tokens.md) only. No new colors, no Poppins, no PDS corporate colors.
3. Sentence case. ALL CAPS only for the 8 pt kicker and other short labels.
4. Content slides: black left panel (x 0 to 241 pt) + Bone `#F3F0E9` right area. Keep the 39 pt left margin.
5. Long copy on solid backgrounds. Gradients and art only for covers, dividers and tiles.
6. Reuse existing images by duplicating slides. Image bytes are not readable via the API; if new art is needed, flag it instead of substituting stock imagery.
7. Logo: full lockup for height > 70 px, **P** mark below that. Do not redraw it.
8. Respect the content limits in [content-rules.md](content-rules.md): short titles, scannable bullets.

## After editing: verification

- `read_slide_layout`: fix `text_overflow`, `off_slide` on new elements, and `low_contrast`. Known lints already present in the source deck (full-height panel at y = -1, overlapping panel/title boxes) are inherited and can be ignored.
- `get_slide_thumbnail`: confirm nothing is clipped and the panel/content split is intact.

## References

- [layouts.md](layouts.md): slide archetypes, coordinates, which slide to duplicate
- [template-fields.md](template-fields.md): required / optional fields per archetype, objectIds
- [tokens.md](tokens.md): colors, type scale, button and logo rules
- [content-rules.md](content-rules.md): titles, bullets, voice, imagery
- Related skills: `phenom-brand-2026` (brand rules from the PPTX), `phenom-design-system` (product UI)

## Open questions in the source deck

- Panel fill is a theme color that renders black; hex not exposed via API. Tokens list Eclipse Noir `#141416`. Confirm before hard-coding.
- Slide numbers, footers and a closing logo slide do not exist in the template.
- Slides 6 and 7 geometry was not sampled; read it live before duplicating.
