# Refreshing the local CSV

1. Open https://docs.google.com/spreadsheets/d/1cmz5PB6LO65AJWC1PU_vdFJbc_2pZ6ykPuVUkrCbAF8/edit
2. Select the data tab whose first header cell is `CASE_NUMBER`
3. **File → Download → Comma Separated Values (.csv)**
4. Move/rename the file to:

```text
product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv
```

5. Confirm headers match `schema.md`
6. Run:

```bash
python3 .cursor/skills/servicenow-service-requests/scripts/summarize_srs.py \
  --csv product-copilot-beta/knowledge/servicenow-service-requests/data/all-service-requests.csv
```

Do not commit the CSV if it contains customer PII beyond what your repo policy allows; keep it local if needed.
