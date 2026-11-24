# Template fields and preflight checklist

Use with the preflight in `SKILL.md`. **R** = required, **O** = optional (may stay as-is or empty). ObjectIds are from the deck snapshot (revision `nmHlnU9QV_CVbw`); re-read the deck before using them, since duplicates get new IDs.

## A. Cover (slide 1)

| Field | Req | objectId | Limit |
|---|---|---|---|
| Title | R | `g3fa1d24ceb7_1_477` | ≤ 2 lines, ≈ 25 chars |
| Subtitle | O | `g3fa1d24ceb7_1_478` | 1 line; box is empty in the deck |
| Background image | R | `g3fa1d24ceb7_1_490` | Reuse; flag if new art is needed |
| Logo | R | group `g3fa1d24ceb7_1_487` | Do not edit |

## B. Table of contents (slide 2)

| Field | Req | objectId |
|---|---|---|
| Title | R | `h6bb78224b3568e60_14_240` |
| Section 1 / 2 / 3 block | R | `…_14_250` / `…_14_252` / `…_14_254` |
| Numerals 01 / 02 / 03 | R | `…_14_251` / `…_14_253` / `…_14_255` |

Each block: name, blank line, 2–3 items, one or two words each.

## C. Section divider (slides 3, 8, 17)

| Field | Req | Example objectId (slide 3) |
|---|---|---|
| Numeral | R | `h6628fe36ad6de217_22_0` |
| Section name | R | `h6628fe36ad6de217_22_1` |
| Background + illustration | R | `g3f9d847fdca_0_30`, `g3f9d847fdca_0_29` |

Numeral keeps a trailing space in the deck (`01 `). Section name ≤ 2 words.

## D. Narrative (slide 4)

| Field | Req | objectId |
|---|---|---|
| Kicker | R | `g3fa03ba6233_3_60` |
| Title | R | `g3fa03ba6233_3_30` |
| Lead | R | `g3fa03ba6233_3_31` |
| Body | R | `g3fa03ba6233_3_34` |
| Panel art | O | group `h74c50b089664850b_1_558` |

## E. Intro + table (slide 5)

| Field | Req | objectId |
|---|---|---|
| Kicker | R | `h74c50b089664850b_1_521` |
| Title | R | `h74c50b089664850b_1_520` |
| Left lead | R | `h74c50b089664850b_1_531` |
| Intro block | R | `h74c50b089664850b_1_525` |
| Table (3 columns, header + 4 rows) | R | `h74c50b089664850b_1_524` |
| Panel art | O | `h4f78e14c6b9337ab_31_25` |

Table has a fixed 5 × 3 shape. More rows overflow the slide: flag instead of adding rows.

## F. Two-block text (slides 6 and 7)

| Field | Req | objectId (slide 6) |
|---|---|---|
| Kicker | R | `h6bb78224b3568e60_14_229` |
| Title | R | `h6bb78224b3568e60_14_228` |
| Main text | R | `h6bb78224b3568e60_14_231` |
| Panel images | O | `h74c50b089664850b_1_564` |

## G. Three-row principles (slide 18)

| Field | Req | objectId |
|---|---|---|
| Kicker | R | `g3fa1d24ceb7_1_240` |
| Title | R | `g3fa1d24ceb7_1_241` |
| Lead | R | `g3fa1d24ceb7_1_242` |
| Section label | R | `g3fa1d24ceb7_1_239` |
| Row 01 / 02 / 03 | R (all three) | `…_244` / `…_245` / `…_247` |
| Tile images | R | `…_246`, `…_251`, `…_259` |

## H. 2 × 2 guideline grid (slide 19)

| Field | Req | objectId |
|---|---|---|
| Kicker | R | `g3fa1d24ceb7_1_348` |
| Title | R | `g3fa1d24ceb7_1_349` |
| Lead | R | `g3fa1d24ceb7_1_350` |
| Section label | R | `g3fa1d24ceb7_1_386` |
| Cells 1–4 | R (all four) | `…_351`, `…_352`, `…_353`, `…_354` |
| Tile images | R | `…_380`, `…_381`, `…_382`, `…_383` |

## K. Closing (slide 20)

| Field | Req | objectId |
|---|---|---|
| Title | R | `g3fa1d24ceb7_1_124` |
| Lead | R | `g3fa1d24ceb7_1_400` |
| Intro | R | `g3fa1d24ceb7_1_405` |
| Contact cards | R | `g3fa1d24ceb7_1_408`, `g3fa1d24ceb7_1_411` |
| Disclaimer | O | `g3fa1d24ceb7_1_428` |

## Common "not in template" cases to flag

- Subtitle or date on a content slide (no box exists)
- A fourth item in a 3-row or 2 × 2 layout
- Extra table rows or columns
- Footer, slide number or page logo
- Chart, KPI or big-number slide (the master has a `Big number` layout, but no brand slide uses it)
- New section divider art
- Speaker notes (deck notes exist; not part of the template spec)
