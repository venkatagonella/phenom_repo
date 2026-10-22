# RX CRM Service Request Playbook — deck

`RX-CRM-Service-Request-Playbook.pptx` (21 slides, 16:9) is built in the
**`leadership-editorial`** style — Fraunces titles with an italic phrase, DM Sans body,
warm paper `#F2F0EA`, navy callout bars, surreal photography on the cover and dividers.
Creativity level 1: catalog layouts only.

Two builds target the same filename, so run the one whose look you want:

```bash
python3 build_pptx_leadership.py   # leadership-editorial (current file)
    10|python3 build_pptx.py              # corporate-template (Poppins, Mint/Peach/Honey/Lilac)
```

## QA

```bash
python3 render_qa_leadership.py    # 1:1 PNGs + contact sheet in qa-render-leadership/
python3 qa_fit_leadership.py       # fonts, 24px floor, tokens, contrast, notes, repeats
```

    20|`render_qa_leadership.py` fetches the Fraunces / DM Sans variable TTFs into `qa-fonts/`
on first run, so overflow is measured with real metrics. Render 1:1 — at any other scale
the font size rounds and the wrap points shift, which invents overflow that is not there.
`gen_font_metrics.py` regenerates `font-metrics.json`, the per-character advance widths
the build script wraps with; that is what makes the layout exact and deterministic
without the fonts installed.

**Fonts are not installed on this machine.** PowerPoint will substitute until Fraunces
and DM Sans are added from Google Fonts (or from `qa-fonts/`). The file names them
correctly, so it renders as designed once they are present.
    30|
## Where the content comes from

Neither build script authors content. Every number and sentence is read at build time from:

| Source | Supplies |
|---|---|
| `product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-crm-areas-jira-yn.json` | funnel counts, area and theme counts, Jira Yes/No splits, percentages |
| `.cursor/skills/servicenow-service-requests/scripts/rx_theme_playbook.py` | area blurbs, per-theme `means` / `problem` / `reduce` text, `PRIORITY_ORDER` |

These are the same two inputs behind `rx-jira-yes-themes.html`, so the deck and the HTML
    40|report cannot disagree.

## One correction vs the HTML header

The snapshot's `funnel.jira_Yes` (555) and `funnel.jira_No` (842) count every RX Service
Request *before* theme classification, and sum to 1,397 — not 1,164. The deck therefore
derives the split inside the classified population by summing the per-area figures:
**522 Jira Yes / 642 Jira No**, asserted equal to `n_filtered` at build time. Slide 5
shows both and labels the funnel pair as pre-classification.

Slide 20 is worded "the six priority themes, by Service Request volume" — not "the six
    50|largest". Screening / interview / scheduling / offer / notifications (99) and Email
template content / hyperlinks / branding (98) are bigger but sit outside `PRIORITY_ORDER`.

## Slide arc → catalog layout

| # | Layout | Slide |
|---|---|---|
| 1 | `cover` | What recruiters keep asking Phenom to fix in CRM (`rocket-cover-full.jpg`) |
| 2 | `cards` | Method: scope, theme assignment, wording |
| 3 | `numbers` | Funnel, 29,310 → 1,164 |
    60|| 4 | `stats` | At a glance: four area tiles + three explainer cards |
| 5 | `compare` | The Jira split inside the 1,164: 522 Yes vs 642 No |
| 6 | `divider` | 01 · What the Service Requests actually say (`clouds-black-full.jpg`) |
| 7–10 | `cards` · `rows` · `cards` · `chain` | CRM Core, six themes |
| 11–12 | `compare` · `rows` | CRM Profile, two themes |
| 13–16 | `cards` · `rows` · `cards` · `chain` | CRM Messaging, six themes |
| 17–18 | `compare` · `rows` | CRM Automations, two themes |
| 19 | `divider` | 02 · Where to start (`sunset-band-full.jpg`, text in the baked-in band) |
| 20 | `table` | The six priority themes |
| 21 | `takeaway` | More than half never becomes a Jira ticket |
    70|
Every slide carries 2–4 sentences of speaker notes. Each area's "what the tickets say"
slide shows every theme with its SR count and Jira Yes/No split; the matching "what to do
in Phenom" slide shows that theme's `reduce` bullets verbatim.

## Also published to

- `product-copilot-beta/knowledge/servicenow-service-requests/RX-CRM-Service-Request-Playbook.pptx`
- Google Drive, My Drive root, file id `1ehuyEOJBeapr89kX8rYSwyxCsD-J5w2L`
  (`~/.local/bin/rclone copy <pptx> gdrive: -P` — stays a real `.pptx`, never converted)
