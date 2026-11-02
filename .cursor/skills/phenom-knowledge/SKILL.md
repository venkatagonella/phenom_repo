---
name: phenom-knowledge
description: >-
  Routes agents into the Phenom Knowledge Framework — code-grounded
  routing.yaml / skill.md / graph.json packs under phenom-knowledge/. Use when
  building Phenom CRM features, finding repos/methods/endpoints, or when the
  user mentions phenom-knowledge, Automations, Messaging, Screening, Analytics,
  or wants a grounded code map before implementing.
---

# Phenom Knowledge Framework — Agent Router

Points any agent at the right **area pack** so it can find repos, controllers,
and methods from real clones instead of guessing.

## Index (start here)

`phenom-knowledge/INDEX.md`

## Area packs

| Area | Path | Status |
|---|---|---|
| Messaging | `phenom-knowledge/messaging/` | Built — prefer skill **phenom-messaging** for deep work |
| Automations | `phenom-knowledge/automations/` | Built |
| Screening | `phenom-knowledge/screening/` | Partial |
| Analytics | `phenom-knowledge/analytics/` | Partial |
| Scheduling | — | Blocked (repos not accessible) |

Each built area has exactly three files:

1. `skill.md` — grounding contract + capability catalog  
2. `routing.yaml` — intent → `repo/path:line`  
3. `graph.json` — nodes/edges across repos  

## Clone root

Engineering clones for line-level grounding live at:

`/Users/venkata.gonella/phenom_repo/MyLocalCRM/repos/<repo>`

(Feasibility index: `Phenom - Engineering/` — see **phenom-engineering-context**.)

## Workflow

1. Open `phenom-knowledge/INDEX.md` → pick the area.  
2. Read that area’s `skill.md`, then `routing.yaml` intents, then `graph.json` if cross-repo.  
3. Open cited files under the clone root; cite `repo/path:line`.  
4. If not in cloned code: say so — do not invent.  
5. For Messaging-heavy work, also load **phenom-messaging**.  
6. For product/team routing (who owns a capability), use  
   `Phenom - Engineering/index/capability-map.md` and  
   `product-copilot-beta/.cursor/policies/platform-routing.md` — do not invent ownership.

## How to invoke

- **“use phenom-knowledge”** / **“load Phenom knowledge for Messaging”**  
- Or name the area: Automations, Messaging, Screening, Analytics.
