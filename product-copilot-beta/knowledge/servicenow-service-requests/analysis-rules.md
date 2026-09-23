# Analysis rules (anti-hallucination)

## Allowed evidence

- Rows and columns in the canonical sheet / local CSV export of that sheet
- Column semantics documented in `schema.md` and the sheet’s own SQL tab (`query-definition.md`)
- Theme labels produced by the **documented** high-confidence phrase classifier
  (`.cursor/skills/servicenow-service-requests/scripts/rx_theme_rules.py`) when the user asks for themes

## Forbidden

- Filling blank `PRODUCT_EXPERIENCE` or `PRODUCT_EXPERIENCE_PRODUCT` from description text unless the user explicitly asks for a **proposed** labeling pass — and then label it as proposed, not as sheet truth
- Using other Drive docs, filtered subset sheets, strategy docs, KB, Snowflake, or Jira as supporting evidence
- Claiming roadmap commitments, ETAs, or “we should build X” as facts from SRs alone
- Quoting partial Drive MCP snippets as if they were the full population
- Inventing theme taxonomies before inspecting the actual short/long text for the filtered set
- **Force-assigning** themes to unclassified SRs via nearest-neighbor / low-threshold similarity
- Presenting cluster membership alone as a final theme without a derived high-confidence phrase rule

## Theme classification rules (RX)

Follow `theme-methodology.md`:

1. Prefer **phrase / regex** rules (base, then cluster-derived `cluster_v1`, …).
2. To grow coverage: **cluster unclassified → inspect → add high-confidence rules** (never silent force-label).
3. Keep `Unclassified / other` when no rule matches.
4. Always state method, population filters, classified %, and example `CASE_NUMBER`s.
5. For `JIRA_CREATED=No`, do not expect `PRODUCT_EXPERIENCE_PRODUCT` (blank by sheet SQL design).

## Required answer shape

1. **Population:** row count, `CREATED_ON_UTC` min/max, filters applied  
2. **Structured key areas:** table of `PRODUCT_EXPERIENCE` (± `PRODUCT_EXPERIENCE_PRODUCT`) with counts and %  
3. **Caveats:** blank rates; spam/duplicate only if those `SUB_STATUS` (or equivalent) values appear  
4. **Themes (if asked):** method stated (base / cluster_vN); classified %; top themes with counts; 3–5 `CASE_NUMBER` examples each; residual unclassified count  
5. **Roadmap framing:** “signals from service requests,” not “roadmap decisions”

## When data is missing

If `data/all-service-requests.csv` is absent:

> Full row-level analysis is blocked: Google Drive MCP cannot export this spreadsheet (file too large). Export Sheet1 as CSV to `product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv` and rerun.

Do not answer key-area or roadmap questions with incomplete samples.
