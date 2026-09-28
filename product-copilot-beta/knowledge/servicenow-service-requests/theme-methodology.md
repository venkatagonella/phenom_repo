# RX theme methodology (high-confidence)

## Goal

Classify Recruiter Experience (RX) service-request themes from sheet text with **high confidence**. Leave residual SRs as `Unclassified / other` rather than force a weak label.

## Population

- `PRODUCT_EXPERIENCE` = `Recruiter Experience (RX)`
- Usually split by `JIRA_CREATED` ∈ {`Yes`, `No`}
- Text fields: `SHORT_DESCRIPTION` (title), `DESCRIPTION` (body)
- **No comments column** in the sheet export

## Method (recommendation #1 — cluster then rule)

1. **Base phrase rules** — exclusive first-match regex on title, then title+body (`BASE_THEME_RULES` in `rx_theme_rules.py`).
2. **Cluster residual unclassified** — TF-IDF (1–2 grams) + MiniBatchKMeans on rows still unclassified under base rules only.
3. **Derive high-confidence rules from clusters** — inspect top terms + example case titles; add phrase patterns only when cluster language clearly maps to an existing theme (or one new tightly scoped theme). Stored as `CLUSTER_V1_THEME_RULES`.
4. **Re-classify** with base + cluster_v1 + **cluster_v2** (DESCRIPTION-grounded
   phrases from residual playbook tickets). Rows that still do not match stay
   **Unclassified** in the Yes/No tabs; the Playbook ticket-class view **excludes**
   Unclassified (every playbook row must land in a named theme).

### Confidence rules

| Allowed | Not allowed |
|---------|-------------|
| Explicit phrase/regex match on title or body | Force-assign nearest TF-IDF/embedding theme with no threshold |
| Title-only themes when body boilerplate is noisy (e.g. How-to) | Infer `PRODUCT_EXPERIENCE_PRODUCT` for Jira No (column is blank) |
| cluster_v2 phrases taken from real DESCRIPTION text of residual SRs | Invent roadmap commitments from themes |
| Leave Unclassified when no rule hits (Yes/No tabs) | Show Unclassified in the Playbook ticket-class view |

### How-to theme

`How-to / configuration / enablement question` is **title-only** (`TITLE_ONLY_THEMES`). Body text often contains help-desk phrasing (“how can you help”) that is not a how-to product theme.

## Scripts

```bash
# Cluster base-unclassified + print coverage after cluster rules
python3 .cursor/skills/servicenow-service-requests/scripts/cluster_unclassified_rx.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --clusters 25 \
  --out product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-cluster-v1.json

# Rebuild RX Yes/No HTML report + Playbook (ticket classification)
python3 .cursor/skills/servicenow-service-requests/scripts/analyze_rx_ticket_classification.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --out product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json

python3 .cursor/skills/servicenow-service-requests/scripts/build_rx_themes_html.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --ticket-class-snapshot product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json \
  --out product-copilot-beta/knowledge/servicenow-service-requests/rx-jira-yes-themes.html
```

## Rule source of truth

`.cursor/skills/servicenow-service-requests/scripts/rx_theme_rules.py`

When adding a new cluster round (`cluster_v2`, …): append new rule lists; do not rewrite prior cluster rule sets in place without noting the version in this file.

**cluster_v2 (2026-09-28):** DESCRIPTION review of residual filtered RX + CRM PEP
tickets previously labeled Unclassified. Phrase rules only; Playbook no longer
renders an Unclassified theme.

## Snapshots

| File | Contents |
|------|----------|
| `snapshot-rx-cluster-v1.json` | Cluster sizes, top terms, examples, coverage after cluster_v1 |
| `snapshot-rx-ticket-classification.json` | Filtered all-fields CSV → theme × `U_TICKET_CLASSIFICATION` counts |
| `rx-jira-yes-themes.html` | Playbook (ticket-class accordions) + Yes vs No tabs |
| `theme-playbook.md` | Per-theme meaning, phenom-knowledge grounding, reduce-feedback actions |

## Ticket-classification Playbook (option A)

Population for the Playbook ticket-class view (all-fields CSV):

1. `U_ISSUE_TYPE` contains `Service Request`
2. `U_TICKET_CLASSIFICATION` in the 7 allowed values
3. `U_PRODUCT_EXPERIENCE` contains `Recruiter Experience (RX)`
4. `PRODUCT_EXPERIENCE_PRODUCT` exclusive allowlist: CRM - Core, CRM - Profile, CRM - Automation, CRM - Messaging and Campaigns

Build:

```bash
python3 .cursor/skills/servicenow-service-requests/scripts/analyze_rx_ticket_classification.py \
  --csv "/path/to/servicenow service requests with all fields.csv" \
  --out product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json

python3 .cursor/skills/servicenow-service-requests/scripts/build_rx_themes_html.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --ticket-class-snapshot product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json \
  --out product-copilot-beta/knowledge/servicenow-service-requests/rx-jira-yes-themes.html
```

Four accordions (Product & Knowledge, Configuration, User Experience, Code): themes with ≥1 row in that class; reduce bullets from `rx_theme_playbook.py` only. Themes may appear in multiple sections.

## Theme playbook (meaning + reduce %)

When asked what a theme **is** or how to **reduce feedback %**, use `theme-playbook.md` (source of truth for prose) and `scripts/rx_theme_playbook.py` (embedded in the HTML Playbook tab).

Ground capabilities in **phenom-knowledge** (`messaging/`, `automations/`, `screening/`). If a pack is missing or a repo is not cloned, say so — do not invent. Reduce-feedback bullets are SR demand signals, not an approved roadmap.
