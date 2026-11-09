---
name: service-request-analysis
description: >-
  Analyze ServiceNow → Jira Service Request demand for one product experience
  (layers A–D, SN-first). Use for RX, Screening, Interview Management, Automations,
  or another Product Experience. ALWAYS ask which Product Experience (and for RX, which product area) before any pull.
  Growing context lives under knowledge/service-request-analysis/ — not in this file.
license: Internal use, Phenom Inc.
metadata:
  owner: officiallybasti
  status: beta
  try: "/service-request-analysis RX, CRM - Messaging and Campaigns, since 2026-08-01"
  audience: "PMs who own service request demand"
---

# Service Request analysis by product experience

Thin **workflow**. PE-specific rules and label sheets live under
[`knowledge/service-request-analysis/`](../../knowledge/service-request-analysis/README.md).

## Non-negotiables

1. **SN-first funnel** — Customer → ServiceNow → Jira SUP only when eng/product needed. Jira alone ≠ full demand.
2. **Ask PE (+ area) before any pull** — do not guess.
3. **Snowflake for metrics** — label sheets are label overlays only.
4. **No invented numbers**.
5. **Do not rewrite Jira** unless an owner asks.

## Intake (do this first)

### 1. Product experience

Ask which PE to run (full Snowflake label when known):

| PE folder | Default label to confirm |
|-----------|--------------------------|
| `rx` | `Recruiter Experience (RX)` |
| `screening` | _TODO — confirm in Snowflake_ |
| `interview-management` | _TODO — confirm in Snowflake_ |
| `automations` | _TODO — confirm in Snowflake_ |
| Other | Ask exact `U_PRODUCT_EXPERIENCE` string |

Then load that PE’s folder under `knowledge/service-request-analysis/<pe>/`.

### 2. Product area (required for RX; recommended for others)

For **RX**, ask before pull (full names only):

1. CRM - Profile
2. CRM - Core
3. CRM - Messaging and Campaigns
4. CRM - Automation
5. CRM - Events and University Recruiting
6. Compliance
7. CRM - Role & Access Management
8. All RX areas

For other PEs, ask using that PE’s `areas.md` list (or “all areas” if the list is still TODO).

### 3. Window + request type

- Date window (default: since `2026-05-01`)
- Request-type filter (default: `Service Request`)

## Context map (where to read / write)

| Need | File |
|------|------|
| Classification decision order | [`knowledge/.../rulebook.md`](../../knowledge/service-request-analysis/rulebook.md) |
| Quick cross-PE signal index | [`knowledge/.../_shared/type-rules.md`](../../knowledge/service-request-analysis/_shared/type-rules.md) |
| PE areas + remaps | `knowledge/service-request-analysis/<pe>/areas.md` |
| True-SR packages | `knowledge/service-request-analysis/<pe>/packages.md` |
| Label sheet process + link | `knowledge/service-request-analysis/<pe>/label-sheet.md` |
| SQL / join | [sql-templates.md](sql-templates.md) |
| How new PEs onboard | [adapting-for-other-pes.md](adapting-for-other-pes.md) |

## Snowflake (locked)

| Object | Role |
|--------|------|
| `FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE` | Primary case table |
| `FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_JIRA_TASK` | Bridge |
| Join | `CASE.SYS_ID = JIRA_TASK.U_CASE_NUMBER_VALUE` → `U_JIRA_KEY` |

Do **not** use `SN_CUSTOMERSERVICE_CASE_REPORT` as primary.

### Escalation baseline

Run the population query in [sql-templates.md](sql-templates.md) for the requested window. Do not reuse historical
counts: bridge deletion handling and cases with multiple link rows can change the result.

## Layers A–D (populations — same rubric every time)

| Layer | Population | Outputs |
|-------|------------|---------|
| **A** | All in-scope SN cases (PE + request type + date + area scope) | Suggested true type + area vs filed |
| **B** | A with **no** Jira link | Support-only demand triage |
| **C** | A with Jira link | Escalation rate; label inheritance into Jira |
| **D** | Linked Jira SUP issues | Confirm triage; apply label sheet overlay when present |

### Layer notes (optional learnings)

Keep PE-specific edge notes short here only if they are workflow notes; put rules in knowledge files.

#### Layer A — All in-scope SN
- Definition / filters → sql-templates + PE `areas.md`
- Outputs: type mix, area remap accuracy

#### Layer B — Never escalated
- Definition: no `U_JIRA_KEY` after join
- Outputs: same triage on Support-handled demand

#### Layer C — Escalations
- Definition: join hit (report any-Jira and SUP-only)
- Outputs: escalation rate; bad type/area carried into Jira?

#### Layer D — Jira SUP view
- Definition: SUP issues linked from C
- Label sheet overlay when the PE has one (see PE `label-sheet.md`)
- Outputs: confirmed labels + true-SR packages

## Workflow steps

1. Ask PE (+ area) and confirm window / request type
2. Read `rulebook.md` + PE `areas.md` (+ gold-sheet if any)
3. Pull SN; left-join Jira
4. Produce A–D for the chosen scope
5. Cluster true SRs with PE `packages.md`
6. Deliver: escalation, type mix, area remap, themes, intake-quality summary

## Success criteria

- PE/area asked or confirmed before pull
- All four layers reported
- Join documented
- Snowflake preferred over Sheet/Looker for metrics

## Blockers

- Unclear PE or area → ask
- No Snowflake → stop; ask for access
- CSR display number unknown → use `SYS_ID` + `U_JIRA_KEY`
