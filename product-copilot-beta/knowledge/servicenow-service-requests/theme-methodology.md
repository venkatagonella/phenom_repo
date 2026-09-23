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
4. **Re-classify** with base + cluster_v1. Rows that still do not match stay **Unclassified**.

### Confidence rules

| Allowed | Not allowed |
|---------|-------------|
| Explicit phrase/regex match on title or body | Force-assign nearest TF-IDF/embedding theme with no threshold |
| Title-only themes when body boilerplate is noisy (e.g. How-to) | Infer `PRODUCT_EXPERIENCE_PRODUCT` for Jira No (column is blank) |
| Leave Unclassified when no rule hits | Invent roadmap commitments from themes |

### How-to theme

`How-to / configuration / enablement question` is **title-only** (`TITLE_ONLY_THEMES`). Body text often contains help-desk phrasing (“how can you help”) that is not a how-to product theme.

## Scripts

```bash
# Cluster base-unclassified + print coverage after cluster_v1 rules
python3 .cursor/skills/servicenow-service-requests/scripts/cluster_unclassified_rx.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --clusters 25 \
  --out product-copilot-beta/knowledge/servicenow-service-requests/snapshot-rx-cluster-v1.json

# Rebuild RX Yes/No HTML report
python3 .cursor/skills/servicenow-service-requests/scripts/build_rx_themes_html.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --out product-copilot-beta/knowledge/servicenow-service-requests/rx-jira-yes-themes.html
```

## Rule source of truth

`.cursor/skills/servicenow-service-requests/scripts/rx_theme_rules.py`

When adding a new cluster round (`cluster_v2`, …): append new rule lists; do not rewrite prior cluster rule sets in place without noting the version in this file.

## Snapshots

| File | Contents |
|------|----------|
| `snapshot-rx-cluster-v1.json` | Cluster sizes, top terms, examples, coverage after cluster_v1 |
| `rx-jira-yes-themes.html` | Interactive Yes vs No theme report + Playbook tab |
| `theme-playbook.md` | Per-theme meaning, phenom-knowledge grounding, reduce-feedback actions |

## Theme playbook (meaning + reduce %)

When asked what a theme **is** or how to **reduce feedback %**, use `theme-playbook.md` (source of truth for prose) and `scripts/rx_theme_playbook.py` (embedded in the HTML Playbook tab).

Ground capabilities in **phenom-knowledge** (`messaging/`, `automations/`, `screening/`). If a pack is missing or a repo is not cloned, say so — do not invent. Reduce-feedback bullets are SR demand signals, not an approved roadmap.
