# RX CRM Service Request Playbook — deck

`RX-CRM-Service-Request-Playbook.pptx` (16 slides, 16:9, Poppins, Mint/Peach/Honey/Lilac).

## Regenerate

```bash
python3 build_pptx.py      # writes the .pptx
python3 render_qa.py       # renders qa-render/slide-NN.png and flags text overflow
```

## Where the content comes from

The build script authors no content. Every number and sentence is read at build time from:

| Source | Supplies |
|---|---|
| `product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-crm-areas-jira-yn.json` | funnel counts, area and theme counts, Jira Yes/No splits, percentages |
| `.cursor/skills/servicenow-service-requests/scripts/rx_theme_playbook.py` | area blurbs, per-theme `means` / `problem` / `reduce` text, `PRIORITY_ORDER` |

These are the same two inputs behind `rx-jira-yes-themes.html`, so the deck and the HTML
report cannot disagree.

## One correction vs the HTML header

The snapshot's `funnel.jira_Yes` (555) and `funnel.jira_No` (842) count every RX Service
Request *before* theme classification, and sum to 1,397 — not 1,164. The deck therefore
derives the split inside the classified population by summing the per-area figures:
**522 Jira Yes / 642 Jira No**, asserted equal to `n_filtered` at build time.

## Structure

1. Cover · 2. How to read · 3. Funnel · 4. At a glance
5–14. Per CRM area (Core, Profile, Messaging, Automations): "What the N Service Requests
actually say" then "What to do in Phenom"
15. Six priority themes · 16. Close

Themes with 3+ per area render as cards/columns; areas with 2 themes render as full-width
bands and additionally show the theme's `means` ("what this theme covers").
