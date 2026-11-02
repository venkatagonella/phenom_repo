---
name: phenom-master-router
description: >-
  Routes work across the Phenom Master Copilot skill packs (design system,
  compete, hypercell, Jira, SpecDrivenDev, engineering context, knowledge,
  slides, product copilot MCPs). Use when unsure which Phenom skill to load, or
  when starting a cross-area product task in phenom-master-copilot.
---

# Phenom Master Copilot — Skill Router

Pick the smallest skill that matches the job. Load supporting skills only as needed.

| If the user wants… | Load |
|--------------------|------|
| PDS / px-* / tokens / prototype UI | **phenom-design-system** |
| Competitor ATS job lifecycle / CI | **competitor-job-lifecycle** (+ Compete/knowledge) |
| Hypercell / Industry×Function×Role×Workflow×Geo | **hypercell** |
| Hiring roles across WD/SF/GH/Ashby/Workable/Personio | **competitor-job-lifecycle** + Compete/knowledge/ROLES-COMPETE-INDEX.md + personas-jtbd.md |
| Jira key → domain requirements | **jira-domain-requirements** |
| Draft/sync Jira epic or story | **jira-workflow** + **jira-api** |
| CRM Core FRD/PRD | **create-prd** / **spec-driven-dev** |
| CRM Core six areas, open Jira backlog, planned timeline, SR demand vs Jira | **crm-core-area** (+ **crm-core-product** for scope/personas) |
| CRM Core areas, open Jira backlog, planned timeline, SR→Jira coverage | **crm-core-area** (+ **crm-core-product** for scope/personas) |
| CRM Core areas, open Jira backlog, planned timeline, SR→Jira coverage | **crm-core-area** (+ **crm-core-product** for scope/personas) |
| Feasibility / how code works | **phenom-engineering-context** |
| Code-grounded CRM maps | **phenom-knowledge** (+ **phenom-messaging**) |
| Phenom-branded deck | **phenom-slide-creator** |
| Customer help-center how-to | **vanilla-kb** |
| Internal strategy/roadmap | **product-context** |
| ServiceNow service requests sheet / SR themes / SR→roadmap signals | **servicenow-service-requests** (sheet-only; no other sources) |
| Usage metrics / SQL | **snowflake-data-context** |
| Google Drive/Docs/Sheets/Cal | **google** |
| Release dates / YY.MM | **release-calendar** |
| PR quality review | **pr-review** |
| Spec-driven *code* change (Northstar) | personal **northstar** / **ns-*** (not duplicated here) |

## Area folders (context)

| Folder | Role |
|--------|------|
| `DesignSystem/` | PDS references + tokens |
| `Compete/` | Competitive knowledge packs |
| `JIRA/` | Domain-requirements outputs |
| `SpecDrivenDev/` | FRD specs + templates |
| `SDDFlow/` | Northstar kit reference |
| `Phenom - Engineering/` | Read-only eng index + clones |
| `phenom-knowledge/` | Area routing packs |
| `product-copilot-beta/` | Policies, MCP, legacy knowledge |
| `PhenomDeckTemplate/` | Slide assets |

## Rules

Project rules under `.cursor/rules/` reinforce Design System, Compete, SpecDrivenDev, and Engineering context. Follow them when those areas apply.
