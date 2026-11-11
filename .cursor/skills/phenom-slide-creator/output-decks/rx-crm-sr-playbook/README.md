# RX CRM Service Request Playbook — deck

`RX-CRM-Service-Request-Playbook.pptx` is a **simplified, clean** 16:9 deck.
Every content slide uses the same two-column table:

| SR theme | Initiative / Epic / Story |
|---|---|
| theme name (normal weight) | open PHEM IDs, or **TBD** |

## Build

```bash
# 1) Refresh theme → Jira rows from board-1091 local JSON (optional if rows JSON is current)
python3 - <<'PY'
# see export block in prior session, or re-run the probe that writes theme-jira-rows.json
PY

# 2) Build the clean PPTX
python3 build_pptx_simple.py
```

Legacy builders (`build_pptx_leadership.py`, `build_pptx.py`) remain for the older
editorial / corporate variants but are **not** the current published file.

## Content source

| File | Role |
|---|---|
| `theme-jira-rows.json` | Per-area theme list + Jira ID cell (or TBD) |
| Board slices under `product-copilot-beta/knowledge/servicenow-service-requests/data/crm-board-1091/` | Open 2026+ Initiative / Epic / Story items |
| `theme_jira_map.py` `JIRA_RULES` | Same title-match rules as the SR themes HTML report |

Done and Blocked items are excluded. Themes with no open mapped item show **TBD**.

## Slide arc

1. Cover  
2. How to read  
3. Coverage at a glance  
4–8. CRM Core (section + tables)  
9–11. CRM Profile  
12–15. CRM Messaging  
16–18. CRM Automations  
19. Close — replace every TBD  

## Also published to

- `product-copilot-beta/knowledge/servicenow-service-requests/RX-CRM-Service-Request-Playbook.pptx`
