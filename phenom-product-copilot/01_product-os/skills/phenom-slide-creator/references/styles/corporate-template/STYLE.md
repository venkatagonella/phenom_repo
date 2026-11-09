# Style: `corporate-template`

The canonical Phenom Google Slides template ("Product - Slide Bank for Cursor") and its HTML twin. Poppins, white content slides, deep navy `#131a4a` covers with the lilac/peach swoosh, four tint families (Mint, Peach, Honey, Lilac), grey stat tiles, navy table headers.

**Use for:** customer and partner decks, board updates, anything that must look like official Phenom collateral, decks a colleague will keep editing in Google Slides.

Everything about this style already lives in the skill:

- Tokens and type: `assets/html-template/phenom-tokens.css`
- Layout catalogue with placeholders: `references/gslides_template_catalog.md`
- Thumbnails: `references/google-template-thumbnails/slide-01..37.png`
- Rules: SKILL.md → "Brand standards", "Color family rotation", "Design principles"

Example decks built in this style: see `references/decks.md` (RAG – Broadstreet Builders, Team 5: Operationalizing RAG). Those decks mix the template's own slides with AI-authored Poppins slides using coloured top-border cards, so they are a good reference for what "Level 2" looks like in this style.

## Build routes

- **Google Slides template fill** (`mcp/build-gslides.ts`) — Level 1 only.
- **HTML** (`assets/html-template/`) — Levels 1–3.
- **Claude Slides artifact** — use `assets/artifact-slides/leadership-editorial/build_deck.py` with `"style": "corporate-template"`: it swaps in Poppins, white paper, navy `#131a4a` and the Mint/Peach/Honey/Lilac tints. Layout vocabulary is the same.
