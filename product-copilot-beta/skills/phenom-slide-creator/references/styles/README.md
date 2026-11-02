# Style library

One folder per style. Each has a `STYLE.md` (tokens, type, chrome, layout catalogue, rules) and `thumbnails/` (contact sheets of the reference decks). Pick the style at intake; the layout vocabulary is shared, the tokens are not.

| Style | Feel | Fonts | Pick when |
|---|---|---|---|
| [`leadership-editorial`](leadership-editorial/STYLE.md) | Editorial, warm paper, serif titles with an italic phrase, navy callout bars, surreal photos on dark slides | Fraunces + DM Sans | Leadership meetings, strategy, workshops, concept intros (default for internal narrative decks) |
| [`corporate-template`](corporate-template/STYLE.md) | Official Phenom collateral: white, Poppins, navy cover with swoosh, Mint/Peach/Honey/Lilac | Poppins | Customer, partner, board, anything others will edit in Google Slides |

Reference decks per style and how to add a new style: `../decks.md`. Text-free photo crops from the leadership decks (clouds, boat, whale, rocket, UFO…): `../../assets/imagery/`.

## Adding a style from a deck you like

1. Get the deck as a PDF (Google Slides: File → Download → PDF, or the Drive connector's `download_file_content` with `exportMimeType: application/pdf`).
2. Render thumbnails and a contact sheet: `swift scripts/render-pdf.swift deck.pdf out/` then `python3 scripts/contact_sheet.py out/ sheet`.
3. Read the sheets. Sample colours with Pillow (`Image.getpixel`), list fonts with `grep -a BaseFont deck.pdf`.
4. Write `references/styles/<id>/STYLE.md` using the leadership-editorial file as the template: tokens, type, chrome, layout catalogue (with slide numbers), rules.
5. Copy the sheets into `references/styles/<id>/thumbnails/`, add the deck to `references/decks.md`, and add a token set to `build_deck.py` (`STYLES` dict) if the artifact route should support it.
