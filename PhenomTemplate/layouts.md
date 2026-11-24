# Layout archetypes

Units are points on a 720 × 405 canvas, as `x,y wxh`. Source: `read_slide_layout` on the live deck. "Duplicate" = `duplicate_object` on the slide objectId, then edit text by objectId.

## Shared content-slide chrome

Used by archetypes B, D, E, F, G, H and the palette/logo slides.

| Element | Box | Style |
|---|---|---|
| Slide background | full | Bone `#F3F0E9` |
| Left panel | `0,-1 241x406` | Rectangle, theme fill (renders black) |
| Kicker | `39,14 108x24` | DM Sans 8 pt bold, ALL CAPS, white (e.g. `MESSAGING`, `VISUAL IDENTITY`, `ART DIRECTION`) |
| Title | `39,55 228x49` | Fraunces 27–28 pt, white. Slides with a two-line kicker box use y = 67 |
| Lead / intro | `39,119 ~175xN` | DM Sans 9 pt white; first line bold, then regular |
| Panel art | bottom-left, bleeds off the edge | Retro-surreal PNG, 0 pt margin on purpose |
| Right area | starts x ≈ 264 | Black text on Bone |

## A. Cover (slide 1, `g3fa1d24ceb7_1_472`)

| Element | Box | Style |
|---|---|---|
| Background image | `0,0 720x405` | Full bleed (`Phenom_1920x1080_bg_4.jpg`) |
| Logo group | `52,16` | White vector wordmark + P |
| Title | `56,112 324x102` | Fraunces 40 pt, white, 2 lines max |
| Empty text box | `56,202 224x24` | Present but empty; optional subtitle slot |

## B. Table of contents (slide 2, `h6bb78224b3568e60_14_238`)

Shared chrome plus three numbered blocks at y = 58, 160, 277.

| Element | Box | Style |
|---|---|---|
| Numeral `01`/`02`/`03` | `319,y 52x42` | 25 pt bold, Mirage Dust `#AD7B8B` |
| Section block | `365,y 153xN` | DM Sans 13 pt bold: section name, blank line, then 2–3 items |

Fixed at three sections. Adding a fourth needs a new row: flag it.

## C. Section divider (slides 3, 8, 17)

IDs: `g3f9d847fdca_0_15`, `g3f9d847fdca_0_31`, `g3f9d847fdca_0_43`. No panel, no kicker.

| Element | Box | Style |
|---|---|---|
| Background | `0,0 720x405` | Full-bleed night/dusk scene |
| Illustration | `388,114 276x256` | Right-hand PNG with cutout |
| Numeral | `60,94 318x124` | Fraunces 90 pt (SemiBold), white, e.g. `01 ` |
| Section name | `60,204 219x41` | Fraunces 22 pt, white |

New sections need a new background and illustration. Duplicate the nearest divider and flag the art.

## D. Narrative / long copy (slide 4, `g3fa03ba6233_3_28`)

Shared chrome plus:

| Element | Box | Style |
|---|---|---|
| Lead | `39,119 174x85` | 9 pt, bold first line |
| Body | `264,22 418x361` | 9 pt DM Sans, black, headline paragraph first |

Longest text slide in the deck (about 330 words). Do not exceed it.

## E. Intro + table (slide 5, `h74c50b089664850b_1_518`)

Shared chrome plus:

| Element | Box | Style |
|---|---|---|
| Intro heading + paragraph + `Voice Pillars` label | `264,23 433x110` | 9 pt, black, first and last lines bold |
| Table | `265,142 430x227`, 5 rows × 3 cols | Header row: black fill, white text; body rows: no fill, black text, thin dividers |
| Left lead | `39,119 188x25` | 9 pt bold, white |
| Panel art | `3,164 286x241` | Bleeds off bottom |

Columns: Pillar, What It Means, Sounds Like. Quotes in the last column are italic.

## F. Two-block text (slides 6 and 7)

IDs: `h6bb78224b3568e60_14_226`, `g3f8ef254153_37_9`. Same chrome, each with one large text box on the right (heading block, then a second heading block such as "How the Voice Comes to Life" or "What Stays Constant") and one or two panel images. Read live before duplicating.

## G. Three-row principles (slide 18, `g3fa1d24ceb7_1_237`)

| Element | Box | Style |
|---|---|---|
| Section label | `280,29 200x30` | 13 pt bold, black |
| Rows 01–03 | `280,73 / 170 / 282, 277xN` | 13 pt: `01<tab>Name`, blank line, one sentence. Numbers in Mirage Dust |
| Image tiles | `568,73 / 176 / 279, 100x87` | Black rounded rectangles with a cut-out PNG on top, one per row |
| Panel | title y = 67, lead `39,119 176x157` | |

Exactly three rows. Row text boxes overflow in the source deck: keep each description to one sentence.

## H. 2 × 2 guideline grid (slide 19, `g3fa1d24ceb7_1_345`)

| Element | Box | Style |
|---|---|---|
| Section label | `280,29 200x30` | 13 pt bold |
| Cells | text at `280,83` `496,83` `280,245` `495,243`, each ≈ `111x100` | 12 pt: bold heading, blank line, 1–2 sentences |
| Tiles | `386,84` `599,84` `386,243` `599,243`, each `89x111` | Black rounded rectangles + PNG overlay |

Exactly four cells. The source text overflows its boxes: shorten body text to about 15 words.

## I. Palette / spec specimens (slides 9–13)

Typography (9, 10), color ramps (11, 12), CTA examples (13). Dense spec slides: shared chrome, section label `Brand …` at the top of the right area, then specimens. Edit hex values and labels only; do not restructure swatch rows. See [tokens.md](tokens.md) for the values.

## J. Logo and icons (slides 14–16)

Reference-only. Copy logo and icon assets by duplicating; do not re-draw. Minimum size: > 70 px height for the full logo, **P** mark below that.

## K. Closing / contacts (slide 20, `g3fa03ba6233_3_94`)

| Element | Box | Style |
|---|---|---|
| Title | `39,67 228x49` | `Questions?` Fraunces 28 pt |
| Lead | `39,119 184x80` | 9 pt, 2 short lines |
| Intro | `281,28 408x88` | 13 pt, bold heading + paragraph |
| Contact cards | `281,126 163x109` and `470,126 180x109` | 12 pt: role, one sentence, name, email |
| Disclaimer | `281,240 378x34` | 7.5 pt, `#434343` |

Contacts in the current deck: Creative, Jonathan Ryle; Messaging, Monica Montesa. Keep them unless the user changes them.
