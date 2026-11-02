Source: Bitbucket Cloud API, workspace `phenompeople`, fetched 2026-07-10. Cross-reference against `index/taxonomy.md` for how these map to this workspace's jobs-to-be-done pillars — Bitbucket's own project grouping may differ from our JTBD taxonomy and that's expected; use this file as raw input for refining placement decisions, not as a replacement for taxonomy.md.

## Status: API authentication working

Credential in `Phenom - Engineering/.env` (git-ignored): `BITBUCKET_EMAIL` + `BITBUCKET_API_TOKEN` (Atlassian API token with Bitbucket scope).

| Auth method | Result |
|---|---|
| `curl -u "$BITBUCKET_EMAIL:$BITBUCKET_API_TOKEN"` | ✅ Works for REST API v2.0 |
| `Authorization: Bearer <token>` | ❌ 401 — not supported |
| `x-token-auth` Basic | ❌ 401 |
| HTTPS `git clone` with email+token | ❌ 401 — use **SSH** for git (`sync-repos.sh` unchanged) |

**67 Bitbucket projects** in workspace `phenompeople`. Sample keys: `AUT` (Automation_engine), `CAN` (CANDIDATES), `MCS` (MCS), `SCHEDULING`, `II` (interview-intelligence).

## Onboarded repos — confirmed Bitbucket project

| Repo slug | JTBD area | Bitbucket project | Default branch note |
|---|---|---|---|
| automation-ui-2 | Platform → Automations → Workflow | AUT / Automation_engine | `main` |
| automation-service-2 | Platform → Automations → Workflow | AUT / Automation_engine | `main` |
| automation-engine-mfes | Platform → Automations → Workflow | AUT / Automation_engine | **`develop`** — `main` is README-only |
| action-centre | Platform → Automations → Workflow | AUT / Automation_engine | **`action-center-dev-2`** — `main` is README-only |
| ae_statesmith | Platform → Automations → Workflow | AUT / Automation_engine | **`auto-transitions`** — `main` is README-only |
| campaign-execution-service | Candidate Engagement | MCS | `main` |
| video-hub | Screening | MCS | `main` |
| cp_ui_app_2.0 | Recruiter Hub | CAN / CANDIDATES | `main` |
| crm-config-service | Recruiter Hub | CAN / CANDIDATES | `main` |
| crm-messaging-platform | Platform → Messaging | CAN / CANDIDATES | `main` |
| scheduling-main-app | Interview Management → Scheduling | SCHEDULING | `main` |
| phenom-internal-calendar | Interview Management → Scheduling | SCHEDULING | `main` |
| scheduling-orchestration | Interview Management → Scheduling | SCHEDULING | `main` |
| scheduling-rule-parser | Interview Management → Scheduling | SCHEDULING | `main` |
| interview-management-service | Interview Management → II | II | `main` |
| interview-management-ui | Interview Management → II | II | `main` |
| evaluation-service | Interview Management → II | II | `main` |
| meeting-bot-orchestrator | Interview Management → II | II | `main` |
| ii-phone-recordings-service | Interview Management → II | II | `main` |

## Other cloned repos (project TBD via API — run refresh)

| Repo slug | Likely area | Notes |
|---|---|---|
| assessment-management-service | Screening | Cloned locally |
| video-assessment-ats | Screening | Cloned locally |
| assessment-streaming-service | Screening | Cloned locally |
| odva-transcription-app | Screening | Cloned locally |
| video-assessment-gdpr | Screening | Cloned locally |
| crm-recruiter-dashboard | Recruiter Hub | Cloned locally |
| crm-candidate-lists | Recruiter Hub | Cloned locally |
| candidates-email-campaign | Candidate Engagement | Cloned locally |
| storm-campaign | Candidate Engagement | Cloned locally |
| storm-campaign-conf | Candidate Engagement | Cloned locally |
| storm-sms-campaign-conf | Candidate Engagement | Cloned (empty stub) |
| storm-hob-campaign | Candidate Engagement | Cloned (empty stub) |
| storm-hob-campaign-conf | Candidate Engagement | Cloned locally |
| crm-campaigns-v2 | Candidate Engagement | Cloned locally |
| crm-storm-transactions | Candidate Engagement | Cloned locally |
| crm-storm-transactions-conf | Candidate Engagement | Cloned locally |
| crm-storm-job-pull | Recruiter Hub → jobs | Cloned locally (`release_25_02`) |
| crm-storm-job-pull-conf | Recruiter Hub → jobs | Cloned locally |
| storm-candidates | Recruiter Hub → storm | Cloned locally |
| storm-candidates-conf | Recruiter Hub → storm | Cloned locally |
| storm-candsignals-conf | Recruiter Hub → storm | Cloned locally (runtime JAR gap) |
| storm-candauto-conf | Recruiter Hub → storm | Cloned locally (runtime JAR gap) |
| storm-candidatescore-conf | Recruiter Hub → storm | Cloned locally (runtime JAR gap) |
| storm-integrations | Recruiter Hub → storm | Cloned (empty stub) |
| hrm-jobs-api | Recruiter Hub → hrm | Cloned locally |
| hrm-jobs-service | Recruiter Hub → hrm | Cloned locally |
| hrm-profile-api | Recruiter Hub → hrm | Cloned locally (moved from candidates/) |
| hrm-profile-service | Recruiter Hub → hrm | Cloned locally |
| hrm-accounts-api | Recruiter Hub → hrm | Cloned locally |
| hrm-gigs-api | Recruiter Hub → hrm | Cloned locally |
| crm-automation-service | Platform → Automations → CRM Automations | Cloned locally |
| crm-workflows | Platform → Automations → CRM Automations | Cloned locally |
| crm-automations-ui | Platform → Automations → CRM Automations | Cloned locally |
| automation-search-service | Platform → Automations → CRM Automations | Cloned locally |
| crm-automation | Platform → Automations → CRM Automations (QA/E2E) | Cloned locally |
| candidates_email_microservice | Messaging | In repos.yaml |
| candidates-sms-services | Messaging | In repos.yaml |
| candidates-notifications | Messaging | In repos.yaml |

## Refresh this file

```bash
cd "Phenom - Engineering"
set -a && source .env && set +a

# Full RX/CRM clone gap analysis (recommended)
python3 scripts/bitbucket-rx-audit.py

# List Bitbucket projects
curl -s -u "$BITBUCKET_EMAIL:$BITBUCKET_API_TOKEN" \
  "https://api.bitbucket.org/2.0/workspaces/phenompeople/projects?pagelen=100"
```

See also `index/rx-platform-coverage.md` for RX platform scope and priority clone list.
