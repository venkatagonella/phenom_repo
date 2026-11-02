---
name: platform-routing
type: policy
description: "Cross-team platform routing table — which platform teams to engage when an Epic touches shared capabilities"
requires: []
always: false
triggers: [epic, cross-team, dependency, platform, automation, scheduling, notifications, candidate, career site, cim, data platform, feature flag, config, routing]
---

Before finalising any Epic, scan your requirements for the capability areas below. If there is a match, engage the listed platform team **before** finalising requirements — not after. This ensures features build on shared capabilities instead of duplicating them.

## How to use

1. **Scan your Epic's requirements** for keywords in the "Capability Area" column
2. **If there's a match**: read their documentation, contact the PM, and add the team to the Epic's Cross-Team Dependencies table
3. **If you're unsure**: reach out to the platform PM directly — they can quickly confirm whether your feature overlaps

---

## Routing Table

| Capability Area | What They Own | Platform Team | PM Contact | Slack Channel | Documentation |
|-----------------|---------------|---------------|------------|---------------|---------------|
| **Unified Candidate Experience** | All candidate-facing UI: apply flow, candidate portal, status pages, candidate communications UI. Any feature visible to the candidate must follow CX guidelines for styling, accessibility, and component usage. | CX Team | _[CX PM]_ | _[#cx-team]_ | _[CX guidelines]_ |
| **CIM / Career Site** | Job pages, career site widgets, SEO, job search, apply button, CIM configuration. Any feature that appears on or modifies the job page or career site. | CIM Team | _[CIM PM]_ | _[#cim-team]_ | _[CIM guidelines]_ |
| **Automation Engine** | All workflow automation: auto-advance, auto-reject, triggers, scheduled tasks, reminders, conditional logic, workflow steps. If your feature needs any automated action, build it as an Automation Engine workflow — not custom logic. | Automation Engine | _[AE PM]_ | _[#automation-engine]_ | _[AE scope doc]_ |
| **Scheduling Platform** | Calendar integration, availability checks, time zone handling, scheduling invitations, conflict resolution, rescheduling. Any feature involving booking or managing time. | Scheduling Team | _[SCH PM]_ | _[#scheduling-team]_ | _[SCH guidelines]_ |
| **Interview Intelligence** | Interview recording, playback, transcription, evaluation forms, debrief summaries, conversation intelligence metrics. Any feature involving interview content or interviewer feedback. | Interview Intelligence | _[II PM]_ | _[#interview-intelligence]_ | _[II guidelines]_ |
| **Notifications / Messaging Platform** | Email, SMS, and in-app notifications to candidates and users. Templates, delivery, personalisation, localisation. If your feature sends any communication, it should route through the notifications platform. | Notifications / Messaging Team | _[Notifications PM]_ | _[#notifications]_ | _[Notifications guidelines]_ |
| **Talent Analytics** | Dashboards, reporting, analytics, report builder, data exports, Snowflake data models. If your feature produces data that needs to be reported on, pulled in the report builder, or exported. *(Always referred to as "Talent Analytics".)* | Talent Analytics Team | _[Talent Analytics PM]_ | _[#talent-analytics]_ | _[Analytics guidelines]_ |
| **Integration Experience** | ATS job pull, integration sync, connectors (SuccessFactors, Workday, etc.), ATS-field-to-CRM mapping. If your feature consumes or maps data from an external ATS. *(Always referred to as "Integration Experience" — not "ATS / Integrations" or "Connectors".)* | Integration Experience Team | _[Integration Experience PM]_ | _[#integration-experience]_ | _[Integration guidelines]_ |
| **Platform Config** | Tenant-level settings, feature flags, configuration toggles, global defaults. If your feature needs a per-tenant toggle or configuration option. | Platform Team | _[Platform PM]_ | _[#platform-config]_ | _[Config guidelines]_ |

---

## Why this matters

- **Consistency** — Platform teams maintain shared services and design patterns. Building on them avoids fragmentation.
- **Scalability** — Platform capabilities are designed to be configurable and reusable. Custom one-off logic creates technical debt.
- **Speed** — Engaging early avoids late-stage rework when platform teams discover your feature duplicates or conflicts with their service.
- **Onboarding** — New PMs may not know who owns what. This table gives you the name, channel, and docs so you can reach the right person immediately.

---

> **Maintenance**: Update the table above when platform teams, contacts, or documentation links change. This file is the single source of truth for "which team owns this capability."
>
> Last reviewed: _2026-05-11_
