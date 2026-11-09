---
name: servicenow-service-requests
description: >-
  Analyzes Phenom ServiceNow service requests from the canonical Google Sheet
  only — key areas (PRODUCT_EXPERIENCE / PRODUCT_EXPERIENCE_PRODUCT), high-confidence
  RX themes (base + cluster_v1 phrase rules), and roadmap signals grounded in sheet
  rows. Use when the user asks about service requests, SR themes, Jira Yes vs No,
  or SR→roadmap questions. Never invent themes or use sources outside this sheet.
metadata:
  owner: gvsrk
  status: sandbox
---

# ServiceNow Service Requests (sheet-only)

## Source of truth (only)

| Field | Value |
|-------|--------|
| Title | All Servicenow service requests from 2026-01-01 |
| Spreadsheet ID | `1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8` |
| URL | https://docs.google.com/spreadsheets/d/1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8/edit |
| Local CSV (preferred for analysis) | `01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv` |

**Hard rules**

1. Use **only** this spreadsheet (or a CSV exported from it into the local path above).
2. Do **not** use product-context, vanilla-kb, Snowflake, Jira, Confluence, Glean, other Drive files, prior analyses, or meeting notes as evidence.
3. Do **not** invent theme labels, priorities, or roadmap commitments that are not supported by counted sheet rows.
4. If the local CSV is missing or incomplete, say so and stop — do not fill gaps with assumptions.
5. Every quantitative claim must include filters used (date range, PRODUCT_EXPERIENCE, etc.) and row counts.
6. For themes: use high-confidence phrase rules; **never force-label** unclassified via low-threshold similarity. Follow `theme-methodology.md`.

## When to use

- Key areas / volume by product experience or product
- Themes in free-text short description + description (especially RX Yes vs No)
- Roadmap-oriented questions answered **only** as “what SRs show,” not “what Phenom will build”
- Client / status / Jira-link breakdowns from sheet columns

## Load order

1. Read `01_product-os/knowledge/servicenow-service-requests/schema.md`
2. Read `01_product-os/knowledge/servicenow-service-requests/analysis-rules.md`
3. For RX / theme questions, also read `01_product-os/knowledge/servicenow-service-requests/theme-methodology.md`
4. For “what does this theme mean / how do we reduce feedback %,” also read `theme-playbook.md` and load **phenom-knowledge** (Messaging / Automations / Screening) — do not invent capabilities outside those packs
5. Confirm local CSV exists (see Data acquisition below). If missing, ask the user to export before answering.
6. Run scripts under `01_product-os/skills/servicenow-service-requests/scripts/`
7. Optional caches: `snapshot-key-areas.md`, `snapshot-rx-cluster-v1.json`, `rx-jira-yes-themes.html`

## Data acquisition

Google Drive MCP **cannot export** this ~6.6MB workbook (`File too large for export`). Do not pretend partial MCP snippets are the full population.

**User export (required for full analysis)**

1. Open the sheet URL above.
2. File → Download → Comma Separated Values (.csv)  
   (If the workbook has multiple tabs, download the data tab that has `CASE_NUMBER` as header — typically Sheet1.)
3. Save as:  
   `01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv`
4. Re-run the skill.

## Analysis playbooks

### A — Key areas (structured)

1. `PRODUCT_EXPERIENCE` — experience area on the case  
2. `PRODUCT_EXPERIENCE_PRODUCT` — finer product label when present (often from linked Jira; blank for most Jira No)

Report counts, share, blank rate. Do not rename labels.

### B — Themes (high-confidence path)

1. Filter population (e.g. RX + `JIRA_CREATED`).
2. Classify with `rx_theme_rules.classify_theme_with_source` (base + cluster_v1).
3. Report classified %, source mix, theme counts, example `CASE_NUMBER`s, residual unclassified.
4. To raise coverage: cluster unclassified → inspect → add `CLUSTER_VN` phrase rules → document in `theme-methodology.md`. Do **not** silent force-label.

### C — Theme meaning & reduce feedback %

1. Classify themes (playbook B).
2. For each theme (or priority set), open `theme-playbook.md` / `rx_theme_playbook.py`.
3. Ground “what it is” + reduce actions in **phenom-knowledge** packs cited there; if pack says gap/not cloned, say so.
4. Frame reduce actions as **demand signals**, not committed roadmap. Include theme n and %.

### D — Roadmap questions

Frame as **demand / friction signals from SRs**, not committed roadmap. Include n and `CREATED_ON_UTC` span. Use playbook C for theme-level articulation.

## Scripts

```bash
python3 01_product-os/skills/servicenow-service-requests/scripts/summarize_srs.py \
  --csv 01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --product-experience "Recruiter Experience (RX)"
```

```bash
python3 01_product-os/skills/servicenow-service-requests/scripts/cluster_unclassified_rx.py \
  --csv 01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --out 01_product-os/knowledge/servicenow-service-requests/snapshot-rx-cluster-v1.json
```

```bash
python3 01_product-os/skills/servicenow-service-requests/scripts/build_rx_themes_html.py \
  --csv 01_product-os/knowledge/servicenow-service-requests/data/all-service-requests.csv \
  --ticket-class-snapshot 01_product-os/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json \
  --out 01_product-os/knowledge/servicenow-service-requests/rx-jira-yes-themes.html
```

```bash
python3 01_product-os/skills/servicenow-service-requests/scripts/analyze_rx_ticket_classification.py \
  --csv "/path/to/servicenow service requests with all fields.csv" \
  --out 01_product-os/knowledge/servicenow-service-requests/snapshot-rx-ticket-classification.json
```

## Related context files

| File | Purpose |
|------|---------|
| `…/schema.md` | Column dictionary |
| `…/query-definition.md` | SQL tab semantics (do not re-run Snowflake under this skill) |
| `…/analysis-rules.md` | Anti-hallucination + theme confidence rules |
| `…/theme-methodology.md` | Cluster → high-confidence rules process |
| `…/theme-playbook.md` | Per-theme meaning + phenom-knowledge grounding + reduce-feedback actions |
| `…/snapshot-rx-ticket-classification.json` | Filtered all-fields → theme × ticket classification |
| `…/SOURCE.md` | Provenance |
| `scripts/rx_theme_rules.py` | Phrase rules (base + cluster_v1) |
| `scripts/rx_theme_playbook.py` | Structured playbook reduce bullets |
| `scripts/analyze_rx_ticket_classification.py` | Build ticket-class snapshot for Playbook tab |
