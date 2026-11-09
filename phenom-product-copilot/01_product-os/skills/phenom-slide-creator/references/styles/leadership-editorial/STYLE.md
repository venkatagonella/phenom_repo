# Style: `leadership-editorial`

The look of the 2026 leadership decks ("Applied AI 2.0: operating our moats", "Theme 2: Operationalizing RAG"). Editorial, warm, serif headlines with one italic phrase, off-white paper, navy and honey as the only strong colours, surreal retro-futurist photography on dark covers. Reads as a magazine feature, not a template.

**Use for:** leadership meetings, strategy narratives, workshop decks, concept introductions, anything where the argument matters more than the brand chrome.
**Do not use for:** customer-facing commercial decks, board packs that must match the corporate template (use `corporate-template`).

Thumbnails: `thumbnails/applied-ai-2-0-sheet0..4.png` (60 slides), `thumbnails/theme-2-rag-sheet0..2.png` (37 slides). A black variant, Hari's "Leading at the Speed of AI": `thumbnails-hari-speed-of-ai/` (white content slides, black cloud-bank dividers, coral `#E88050` for the second sentence of a title; good for giant single-number slides, the five-link chain with top rules, readiness bars). Open them before designing; they are the source of truth.

Imagery (clean, text-free slide images): `../../../assets/imagery/` — `rocket-cover-full.jpg` for covers, `clouds-black-full.jpg`, `whale-full.jpg`, `astronauts-full.jpg` for dividers and closings.

## Tokens

| Token | Value | Used for |
|---|---|---|
| paper | `#F2F0EA` | slide background (light slides) |
| card | `#FFFFFF` / `#FAF8F3` | white cards and table bodies |
| ink | `#141416` | headlines, body on light |
| body | `#414241` | secondary body text |
| muted | `#6B6B6B` / `#8A8A8A` | captions, sources, table headers |
| navy | `#22224B` | dark cards, callout bars, table header rows, the "60%" tile |
| navy-kicker | `#373775` | eyebrow kicker text, link text, pill buttons |
| black | `#141416` | full-bleed statement slides, left rail (Theme 2 variant) |
| honey | `#EDE0C3` fill · `#CEA667` strong | the first/accent card, the 20% evals card, step 02 |
| rose | `#EEDDD9` | second tint, handoff and finding boxes |
| lilac | `#DDDDEA` / `#EBEBF1` fill · `#77779F` strong | third tint, worksheet rows, tables |
| sage | `#DDE3D5` fill · `#8A9A7B` strong | "runs on AI" column, step 01 |
| mauve | `#A67D8B` | big serif numerals "01 02 03" on cards |
| status | green `#2F7A4F` · amber `#A86A12` · red `#B23A32` | RAG text only, never fills |
| dark-card text | `#FFFFFF` title · `#DDDDEA` body | on navy cards |

Rotate tints across a row of cards in this order: honey → rose → lilac → white (then sage if a fifth is needed). A navy card is the emphasis card (the "AI does the work" column, the "Test" row, the last of a set).

## Type

- Headlines: **Fraunces** 600 (Google Fonts `Fraunces:wght@600` + `ital`). Titles are sentences with a full stop, and one phrase set in *italic* for emphasis: "We verticalized well. *Operations is the gap.*"
- Body: **DM Sans** 400/500/700.
- Scale on the 1920×1080 canvas: title 60px (52px on split slides), subtitle 30px, card title 28–30px, body 24–26px, kicker 24px uppercase letter-spacing 1px, big numerals 44–56px serif mauve, statement numerals 300–400px serif.
- Never below 24px.

## Chrome (every slide)

- Kicker top-left: `SECTION  |  SUB-SECTION` in navy-kicker, uppercase. Pattern `PART 1 | THE SHIFT`, `EVALS | 1 OF 3`, `HOW LEADERS DO IT | SELLS AI | LEGAL`.
- Title under it, then a 30px subtitle in body colour, then a hairline rule or just 40px of air.
- Small Phenom "p" mark bottom-left (`logo-dark.png` on paper, `logo-light.png` on dark).
- Optional **left rail** (Theme 2 variant): 72px black strip with the deck name rotated vertically and the white "p" at the bottom. Choose rail on/off per deck, never per slide.
- Bottom **callout bar** on most content slides: full-width, 20px/32px padding, either navy with white text (`The point`, `Steal this`, `For Phenom`) or a tint with ink text (`Feedback`, `Source`, `Exercise preview`). Starts with a bold 2-word label then one sentence. This is the signature element; use it to land the slide's one takeaway.
- Source line, 24px muted, under the callout when a slide cites data.

## Layout catalogue (what the decks actually use)

| Layout | What it is | Seen on |
|---|---|---|
| `cover` | Navy/dark photo (surreal retro space, sailors, whale, UFO) left-aligned title block, logo top-centre | AI 2.0 s01, s21, s34 |
| `divider` | Dark photo or flat black, kicker + two-line serif title + one-line sub, bottom-left | AI 2.0 s10, s13, s35, s41; Theme 2 "01 Share" style uses a huge numeral |
| `statement` | Full black, 3 giant serif numerals `20 | 60 | 20` with thin dividers and a proportional bar; builds up over 3–4 slides | AI 2.0 s06–s09 |
| `cards` | 3 or 4 white/tinted cards, serif numeral or icon chip top, bold title, body; one card may be navy | s03, s04, s16, s17 |
| `tiles` | 3 big-number tiles in a row (`20% / 60% / 20%`), navy-tint-navy | s11 |
| `steps` | 3–6 numbered circles on a line, label + caption under each; circles rotate sage/honey/lilac/rose | s05, s19, s48, s49, s53 |
| `triptych` | Company case: logo-stat card (white) + three columns 20% / 60% / 20% (tint / navy / honey), "Steal this" callout, source | s24–s31 |
| `table` | Navy header row, white body, optional first column bold, group spine on the left | s26, s32, s50, s52 |
| `compare` | Two columns: light card vs navy card (Protect vs Grow, Sells AI vs Runs on AI) | s23, s37, s38 |
| `rows` | Worksheet rows: icon chip + bold label + description, rows tinted, last row navy | s43, s47, s55 |
| `stats` | 4 stat tiles (number + label + sub) above 3 explainer cards | s56 (churn), Theme 2 s06 |
| `links` | White card with a list of underlined links + a right-hand diagram/screenshot | s42, s46 |
| `brief` | Two-column annotated example: left tinted box with numbered lines, right the six labelled parts | s18 |
| `check` | Checklist card with PASS / FAIL pills on the right | s19 |
| `loop` | Boxes with arrows forming a cycle (Brief → Reason → Act → Evaluate → Learn) | s22 |
| `split` | Left: kicker, question-title, three labelled paragraphs. Right: white panel with a product mock | Operationalising RAG view slides |
| `takeaway` | Black slide, three white/honey cards with icon, one closing line | s57 |

## Rules that make it look right

1. One idea per slide and one callout bar that says it.
2. Titles are sentences. Put the surprising half in italic.
3. Tints are backgrounds only; text is always ink or white. Status colours only on status words.
4. Photos only on dark slides (cover, divider), never on content slides. Use the surreal retro-futurist set; never stock office photos.
5. Numbers get the serif; everything else DM Sans.
6. Three or four of anything, never five, unless it is a numbered step line.
7. Dark slides are rare: cover, dividers, statement, takeaway. Everything else is paper.
8. Sources in 24px muted at the very bottom, always when a number is on the slide.

## Build routes that support this style

- **Claude Slides artifact** (default): `assets/artifact-slides/leadership-editorial/build_deck.py` turns a JSON spec into the deck files. Fonts load from Google Fonts. Export to Google Slides from the artifact's Share menu.
- **HTML**: same tokens; add the layouts to a per-deck stylesheet.
- **Google Slides template route**: not supported (the corporate template has different fonts and chrome).
