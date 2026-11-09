---
name: candidate-engagement
type: index
description: "Domain index for Candidate Engagement repos — email/SMS campaigns, nurture, audience targeting, campaign analytics"
pillar: Product Experiences
last_reviewed: 2026-07-20
---

# Candidate Engagement

## Scope

Candidate outreach and nurture before or alongside the hiring funnel:
- Email and SMS **campaigns** — definition, scheduling, sending, templates
- **Audience segmentation** and candidate-list targeting for campaigns
- Campaign **execution** (including video-enriched outreach)
- Real-time campaign **event tracking** and analytics (opens, clicks, transactions)
- Storm **deploy configs** (`*-conf`) for campaign topologies and related lanes

Not in scope:
- Screening questions, knockout logic, assessment integrations (→ Screening)
- Message delivery transport layer (→ Platform → Messaging) — this pillar owns campaign *domain* logic; Messaging owns send pipes
- Recruiter-facing campaign builder UI hosted in CRM shell (→ Recruiter Hub)
- IX job ingest / hub-profile Storm processing (→ Recruiter Hub `crm-storm-job-pull`, `storm-candidates`)

## Repo manifests

**Use [`index/repos/candidate-engagement/capability-index.md`](../repos/candidate-engagement/capability-index.md) before grepping `repos/product-experiences/candidate-engagement/`.** Curated manifests cover campaign APIs, Storm runtimes, and `*-conf` deploy repos. Two parallel campaign stacks exist (v1 `candidates-email-campaign`, v2 `crm-campaigns-v2`) — confirm with the owning team which is authoritative for new work.

## Key repos

See `index/repo-catalog.md` for full stack/status/"also used by" detail.

### Campaign management & execution

| Repo | Purpose | Start here |
|------|---------|------------|
| `candidates-email-campaign` | **v1** campaign management API — defines/sends email + SMS campaigns, templates, analytics, CMS campaign config | `app/controllers/CampaignController.java` |
| `crm-campaigns-v2` | **v2** campaign engine — facet-based audience segmentation, fair scheduling, CDC, REST job orchestration, Spark/Kafka streaming. ⚠️ Internal package/artifact names say `messagingv2` despite the repo being named "campaigns-v2" — this is a legacy naming carry-over, not a sign it belongs in Platform → Messaging (see manifest for detail) | `restapi/`, `facet-sql-builder/` |
| `campaign-execution-service` | Executes candidate outreach campaigns; injects video context (Kaltura) into campaign content | `app/com/phenompeople/mcs/campaignexecution/controllers/CampaignExecutionController.java` |

### Campaign analytics & event processing (Storm)

| Repo | Purpose | Start here |
|------|---------|------------|
| `storm-campaign` | Real-time campaign event tracking (opens/clicks) + autoresponder/drip campaign scheduling via Apache Storm topology | `src/jvm/com/phenompeople/tracker/topology/EmailCampaignsTopology.java` |
| `storm-campaign-conf` | Env config for campaign Storm topologies | `EmailCampaign/camp-storm-config.properties` |
| `storm-hob-campaign-conf` | HOB EmailCampaign deploy lane config (HOB acronym undocumented) | `HobEmailCampaign/camp-storm-config.properties` |
| `storm-hob-campaign` / `storm-sms-campaign-conf` | **Empty stubs** — do not scan; use `storm-campaign` + confs above | — |
| `crm-storm-transactions` | Real-time campaign transaction/stats processing via Storm — email campaign analytics bolts, transactional sends, recruiter digest, plus one GDPR-specific bolt | `src/jvm/com/phenompeople/StormTransactions/topology/CRMTransactionsTopology.java`, `bolt/EmailCampaignAnalyticsStatsBolt/` |
| `crm-storm-transactions-conf` | Env config for CRMTransactions topology | `CRMTransactions/storm-transactions-config.properties` |

## Common feasibility patterns

- **New campaign type or channel** → start with `candidates-email-campaign` or `crm-campaigns-v2` depending on v1 vs v2 stack; check Recruiter Hub for where recruiters configure it.
- **Audience / segment for a campaign** → `crm-campaigns-v2` (`facet-sql-builder/`) + Recruiter Hub `crm-candidate-lists` for list/filter infra.
- **Campaign send / delivery** → Platform → Messaging (`candidates_email_microservice`, `crm-messaging-platform` campaign modules).
- **Campaign triggered by automation** → Platform → Automations owns trigger/recipe; this pillar owns campaign definition and execution APIs.
- **Campaign analytics (opens/clicks)** → `storm-campaign`, `crm-storm-transactions` (+ matching `*-conf` for env/topic wiring).

## Platform dependencies

- **Messaging** — email/SMS delivery, templates at transport layer
- **Automations** — campaign triggers, scheduled nurture recipes
- **Recruiter Hub** — campaign builder UI, candidate lists for audiences (`crm-candidate-lists`); CRM Storm candidate/job ingest lives under Recruiter Hub `storm/` / `jobs/`
- **Privacy & Compliance** — GDPR bolt in `crm-storm-transactions`; consent for outreach

## Eng contacts

_Fill in once known — team name, PM, Slack channel._
