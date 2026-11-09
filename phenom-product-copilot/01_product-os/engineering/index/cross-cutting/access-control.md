---
name: access-control
type: index
description: "Cross-cutting index — where roles, permissions, scopes/departmentalization, and tenant isolation live per product. Built for the Unified Access Control platform workstream."
last_reviewed: 2026-07-27
---

# Access Control — Cross-Cutting Baseline

Access control does not belong to one pillar, so it does not route through `taxonomy.md`. Start here for any question shaped like:

- "Where are roles/permissions stored for product X?"
- "Does product X use departmentalization / scope filtering?"
- "Who is allowed to see this record, and what enforces that?"
- "What would break if we moved product X onto a shared access model?"

## The pattern across Phenom (as far as we've audited)

Products generally do **not** own a permission store. The recurring shape is:

1. **Identity + permission grants live in a central service** — `usermanagement` (`validateTokenAndPermissions`). Products send a bearer token and get back user id, permissions, roles, and scope attributes.
2. **Products store per-object membership, not roles** — e.g. who is on the interview panel, who a record was forwarded to. This is the part a unified model most often fails to capture.
3. **Org scoping (departmentalization) is a shared library**, `com.phenompeople.crm:departmentalization-commons` + `crm-commons`, which injects a Mongo filter clause. Adoption is inconsistent — some services pull the library, others have it stubbed off, others never adopted it.
4. **Tenant isolation is a document field**, `refNum`, on essentially every collection. Not separate databases per tenant.

The consolidation risk is therefore usually **not** "many permission stores to merge" — across the two products audited so far there is exactly *one* permission collection in total. The real problems are:

- **Scope is expressed at least three different ways** — departmentalization Mongo filters, tenant entitlement lists, and `My`/`All` permission naming — plus per-object membership.
- **Enforcement lives at different layers** — server-side per object in one product, edge-only with the decision handed to the client in another.

See the [cross-product comparison](#cross-product-comparison) for the side-by-side.

## Audit status by pillar

| Pillar / domain | Status | Detail |
|---|---|---|
| Product Experiences → Interview Management (II) | ✅ **Audited 2026-07-27** | [See below](#interview-intelligence-ii) |
| Product Experiences → Interview Management (Scheduling) | ⬜ Not yet audited | Different Bitbucket project + team than II; audit separately |
| Product Experiences → Screening | ✅ **Audited 2026-07-27** | [See below](#screening-video-assessment--odva) |
| Product Experiences → Candidate Engagement | ⬜ Not yet audited | |
| Recruiter Hub | ◐ **Partially known** | `crm-commons` is the *source* of the departmentalization/scope ACL library — see `index/repos/recruiter-hub/crm-commons.md`. Consumer-side audit not done. |
| Recruiter Hub → HRM | ⬜ Not yet audited | `hrm-accounts-api` handles HM identity / auto-provision — likely relevant |
| Platform → Automations | ⬜ Not yet audited | |
| Platform → Messaging | ⬜ Not yet audited | |
| Platform → Privacy & Compliance | ⬜ Not yet audited | Consent ≠ access control; keep the two separate in any baseline |

⬜ means **nobody has looked yet** — it does not mean "no access control". Do not report an un-audited pillar as having none.

---

## Interview Intelligence (II)

**Audited:** 2026-07-27 · **Repos:** `interview-management-service`, `evaluation-service`, `meeting-bot-orchestrator`, `ii-phone-recordings-service` · **Branch:** all `main` (`interview-management-service` @ `00072b1`, 2026-06-10)

### Headline

II stores **almost no access-control data in Mongo**. There is exactly one permission collection, `permissionsForRole`, and it holds only a static access-tier → capability-flag mapping. The authority for identity and permissions is the central **User Management** service. Everything else that looks like access control is per-object membership on the interview documents.

### Databases

Two Mongo databases, shared by all four services:

| DB | Config key | Used by |
|---|---|---|
| `interviewmanagement` | `db.name` (IMS), `dbii.name` (evaluation-service), `MONGO_DB` (bot orchestrator), `spring.data.mongodb.database` (phone) | all four |
| `InterviewEvaluations` | `evaluations.db.name` (IMS), `db.name` (evaluation-service) | IMS, evaluation-service |

`evaluation-service` also configures `crm.candidates.db.name=_candidates`, but no main-code usage was found — **open question**, may be dead config.

### The one permission collection

| Collection | DB | Shape | Read by |
|---|---|---|---|
| `permissionsForRole` | `interviewmanagement` | `{ accessType, permissions: { …flags } }` | `CacheLoaderService` — 600s in-process cache, max 20 entries |

Constant: `II_PERMISSIONS_FOR_ROLE = "permissionsForRole"` at `ApplicationConstants.java:898`.

**The role → access-tier decision is hardcoded in Java, not in Mongo** (`TokenUtils.getPermissionsForRole()`, lines 230–252, carrying its own `//TODO read from config`):

| Hiring-team role | Originating app | Invited? | Access tier |
|---|---|---|---|
| Recruiter | CRM (`Candidate App`) | — | `ADMIN` |
| Hiring Manager | HRM (`Hiring Manager`) | yes | `EDIT` |
| Interviewer | HRM (`Hiring Manager`) | yes | `VIEW` |

Changing these mappings is a code deploy, not a data change. `II_DEMO_ROLE` also exists as an access type (`ApplicationConstants.java:1208`).

### Where authorization actually happens

| Layer | Mechanism | Location |
|---|---|---|
| Token + permission grants | `validateTokenAndPermissions` → **User Management** (`auth.url=https://usermanagement-<env>.phenompro.com/`) | `TokenValidationService` (IMS); `filters/Authorization.java` (evaluation-service) |
| Permission naming | Grants arrive prefixed `II_`, stripped to bare keys before use | `TokenUtils.getPermissionsFromTokenResponse` |
| API gate | Coarse — request rejected only when the user has **zero** permissions (`permissions.size() < 1` → `INVALID_USER`) | `TokenUtils.verifyIncomingRequest` |
| Play action wiring | `@With(Authorization)` / `@With(Authentication)` per controller | `app/…/auth/` |
| Tenant | `refNum` document field + `x-ph-refNum` / `ph-org-code` headers | all services |

`Authentication` is the weaker variant — it validates the token but skips the permission-count check.

### Per-object membership (the part a unified role model will miss)

Whether a user may open a specific recording is decided by membership on the `meetings` document, plus a live CRM lookup — **not** by a stored role:

| Field | Meaning |
|---|---|
| `meetings.forwardedList[]` | Explicit per-recording shares; `emailId` + `access` (`ADMIN`/`EDIT`/`VIEW`) |
| `meetings.panel.required[]`, `meetings.panel.optional[]` | Interview participants; `email`, `participantType`, `evaluator` |
| `meetings.createdBy` | Organiser |
| `job.hiringTeamList[]` | Role on the job — **fetched live from CRM, not stored in II Mongo** |
| `iiPermissions`, `usersWithRecordingAccess` | **Computed response fields**, not storage — do not treat as a grant store |

In `evaluation-service` the equivalent membership fields are `requestedTo` / `requestedToId`, `requestedBy`, `submittedById`, `taggedRecruiters` on `pendingEvaluations` / `evaluationSubmission`.

### Departmentalization / scope — inconsistent, and this is the real finding

| Service | Shared libs | Scope enforcement |
|---|---|---|
| `evaluation-service` | `departmentalization-commons:12.2` + `crm-commons:12.2` | **Active.** `ScopeFilterService.addQueryForScope()` → `DepartmentalizationUtils.getMongoScopeFilter(ScopeFilterRequest(refNum, EntityType.RECRUITER_ACTIVITY))`, merged into the Mongo find query. Persisted as `scope` on submissions. |
| `interview-management-service` | `crm-config-commons:3.1.1` only — **no** `crm-commons`, **no** departmentalization lib | **Off, and hardcoded.** `IIFeatureFlagUtil.isDepartmentalizationEnabledFromCrm()` is `return false;` with the flag check commented out (lines 40–43). |

Consequence worth escalating: scope filtering for **meetings and recordings cannot be enabled by flipping a tenant flag** today — it needs code. `SCOPE_ATTR = "scopeAttr"` exists as a constant (`ApplicationConstants.java:962`) and `scopeAttr` is copied onto `pendingEvaluations` from the CRM jobs API, but it does not gate meeting reads.

### Collections that look like access control but are not

Flag these explicitly in any baseline sheet so they don't get merged into a global user/permission model:

| Collection | DB | What it actually is |
|---|---|---|
| `recruiterDetails` | `interviewmanagement` | **Twilio phone verification** for `ii-phone-recordings-service` — recruiter phone binding + OTP state. Not authorization. |
| `subAccountDetails` | `interviewmanagement` | Twilio sub-account config per tenant |
| `customer_configs`, `configurations` | `InterviewEvaluations` / `interviewmanagement` | Tenant feature config |
| `meetingParticipantDetails` | `interviewmanagement` | Recall.ai participant capture |
| `candidateConsent`, `candidateConsentAuditLog`, `meetingTokenDetails` | `interviewmanagement` | **Candidate consent + deeplink tokens.** Privacy concern, not RBAC — keep separate. |

### Open questions for the II team

- **Auth coverage.** 11 controllers in `interview-management-service` apply `@With(Authorization)` or `@With(Authentication)`. Eight apply no Play auth action: `BulkImportController`, `Gpt3Controller`, `HealthCheckController`, `MetricsController`, `OAuthConfigController`, `OnboardingController`, `ProxyController`, `S3ServiceController`. Health and metrics are expected; the rest need confirmation of whether they validate inline or rely on gateway protection. **Not yet verified either way — ask before reporting as a gap.**
- `meeting-bot-orchestrator` read endpoints were found to take `x-ph-refnum` / path params with no NestJS guard in-repo. Confirm whether an API gateway enforces auth in front of it.
- `evaluation-service` parses `II_*` permissions into `TokenDetails` but no in-repo call to `getPermissions()` was found — confirm where those grants are actually enforced (gateway? UI? User Management response?).
- Is the `permissionsForRole` collection seeded per tenant or globally? Seed data is not in the repo.
- Is `crm.candidates.db.name=_candidates` in `evaluation-service` live or dead config?

### Confidence

Directly line-verified: the two DB names, `permissionsForRole` + `CacheLoaderService`, the hardcoded role→tier mapping, the hardcoded-`false` departmentalization flag, `evaluation-service`'s shared-lib dependencies and `ScopeFilterService`, `auth.url`, and the `@With` controller counts. Reported by code scan but not line-verified: the exact membership-field query construction in `VideoTranscriptService`, and the bot-orchestrator/phone-service auth surfaces. Treat the second group as needing confirmation before it goes into a platform commitment.

---

## Screening (Video Assessment / ODVA)

**Audited:** 2026-07-27 · **Repos + branches** (all six have an empty `main` — these are the real branches):

| Repo | Branch | Commit |
|---|---|---|
| `video-hub` | `feat_common_may_2026` | `8e3a66e` (2026-07-09) |
| `assessment-management-service` | `release_2.2` | `f0e38c5` (2026-04-22) |
| `assessment-streaming-service` | `release_1.0` | `cac3c93` (2026-04-22) |
| `video-assessment-ats` | `fun_stg_deployment` | `be21a70` (2026-05-20) |
| `video-assessment-gdpr` | `func_24_02_phApplicationId` | `c4c7eb0` (2026-07-07) |
| `odva-transcription-app` | `func_1.1_PHEM-2098529_assembly_ai_integration` | `26df0d9` (2026-07-16) |

### Headline

**Screening calls User Management through the exact same mechanism as II, but enforces more at the edge and stores even less.** All authorization happens in **`video-hub`**, which acts as a gateway; the other five services have no authorization of their own. Screening stores **zero** access-control data in Mongo — not even II's single `permissionsForRole` collection.

### Same as II — the call to User Management is structurally identical

| Aspect | Both products |
|---|---|
| Method | `TokenValidationService.validateTokenAndPermissions(...)` |
| Endpoint resolution | Redis DDO key `validateAuthLoginToken` → `WSUtils.makeWSCall` → `redisManager.getDDO()` → environment endpoint + api path |
| Constant | `REDIS_DDO_VALIDATE_AUTH_LOGIN_TOKEN` — `video-hub/…/utils/RedisKeys.java:13`, IMS `…/utils/ApplicationConstants.java:1846` |
| Headers | `Authorization: <token>` + `PhenomSource: VX` |
| Payload | `{ applicationName: <originatorApp> }`, defaulting to `"Candidate App"` |
| Verb | POST |
| Permission convention | Product-prefixed keys stripped to bare names |

So a shared access model does **not** need to change the transport or the contract for either product. That's the good news for the workstream.

### Different from II — four divergences that matter

**1. Screening enforces tenant entitlements; II does not.** `TokenValidationService.hasEntitlementAccess()` (`video-hub`) requires `user_id` **and** a non-empty `entitlements[]` array containing either `ALL` (constant `ALL_TENANTS`) or the request's `refNum`. It additionally filters the request payload's `childRefnums[]` down to only entitled tenants, i.e. parent/child tenant hierarchy narrowing. II has no equivalent — it only checks `user_id` is present, then that the user has at least one permission. **This is the strongest per-user access check found in either product so far** and is a candidate pattern for the unified model.

**2. Screening's permission model is typed and ownership-scoped.** `models/ODVAEntityPermissions.java` is a concrete class:

```
viewMyQuestionnaires      viewAllQuestionnaires
modifyMyQuestionnaires    modifyAllQuestionnaires
duplicateMyQuestionniares duplicateAllQuestionniares   (sic — typo is in the code)
```

The **My/All distinction is baked into the permission names** rather than handled by a separate scope mechanism. Contrast II, which returns untyped boolean flags from the `permissionsForRole` Mongo document. Worth raising: this is a third way of expressing scope, alongside departmentalization and per-object membership.

**3. `video-hub` already fronts both products.** `TokenUtils.getODVAPermissionsFromTokenResponse(tokenResult, product)` branches on a `product` argument: `"vx"` strips the `ODVA_` prefix (plus passes through `Settings_ODVA`, `settings_odvaDefaultSettings`, and any `sms*` / `email*` keys), while `"iim"` strips `II_` — the same prefix `interview-management-service` uses. This gateway is therefore already a shared entry point across Screening and Interview Intelligence, not a Screening-only component.

**4. Enforcement is gateway-only, and permissions are handed to the client.** `video-hub`'s three controllers use **no** `@With(...)` action composition — authorization lives inside `services/ApiService.java`, which validates the token then proxies to a resolved target service URL. `ApiService` also writes the permission set into the outbound API response (`apiResult.set(PERMISSIONS, tokenData.getPermissions())` at roughly ten call sites), pushing the actual allow/deny decision to the calling UI. II instead computes per-object `iiPermissions` server-side and wires auth per controller.

`video-hub` also registers a global `OriginValidationFilter` alongside `CORSFilter` in `app/Filters.java`; `interview-management-service`'s equivalent registers CORS only. So Screening layers Origin validation → tenant entitlement → token validity at the edge, where II layers token validity → permission count → per-object membership deeper in the stack. Confirmed for the five downstream services: **zero** inbound-auth wiring (no `@With`, no servlet filter, no interceptor, no `Filters.java`) — the only `Authorization` header found in `assessment-management-service` is an *outbound* Basic-auth call to a third-party provider (`TGAssessmentService.java:129`), not an inbound check.

### Databases

| DB | Config key | Services |
|---|---|---|
| `mongo_ngcc_dev` (dev; confirm prod name) | `mongo.db` | `video-hub`, `assessment-management-service`, `assessment-streaming-service`, `video-assessment-ats`, `video-assessment-gdpr` — **one shared DB for all five Play services** |
| three URIs: default / offline / vxim | `spring.data.{default,offline,vxim}.mongodb.uri` | `odva-transcription-app` (Spring Boot) |

Note this is a completely different Mongo estate from II's `interviewmanagement` / `InterviewEvaluations`.

**No access-control collections exist in any of them.** Collections observed are all business data — `transcriptionRawEvents`, `videoTranscriptionsCollection`, `videoTranscriptionsResultCollection` (`odva-transcription-app`), `videoAssessmentTranscriptSummaryResult` (`video-assessment-gdpr`). The Play services build collection names dynamically rather than via constants, so this is **not a complete collection inventory** — if the platform sheet needs every collection, that needs a dedicated pass.

### Departmentalization / scope

**None, anywhere.** No screening repo declares `crm-commons` or `departmentalization-commons` in `build.sbt` / `build.gradle` / `pom.xml`. There is no `getMongoScopeFilter` usage and no `scopeAttr` handling. Scope, to the extent it exists, is expressed as tenant entitlements plus the `My`/`All` permission naming above.

### Open questions for the Screening team

- The five downstream services have **no authorization of their own**. Confirm they are only ever reachable through `video-hub` (or an infra-level gateway) and not directly addressable — this is the single biggest assumption in this audit.
- `video-hub` hands permissions to the caller in the API response. Confirm whether any server-side enforcement exists beyond token validity + tenant entitlement, or whether the UI is genuinely trusted for allow/deny.
- Is `ODVAEntityPermissions` the complete Screening permission surface, or just the questionnaire subset? The prefix filter also admits `Settings_ODVA`, `sms*`, and `email*` keys that the typed model doesn't cover.
- Confirm the production Mongo DB name — `mongo_ngcc_dev` is the dev value.
- ⚠️ **Hygiene, not access control:** the `conf/*.conf` files in these repos contain plaintext Mongo credentials for shared non-prod environments. Worth raising separately with the team; deliberately not reproduced in this index.

### Confidence

Line-verified: the `validateAuthLoginToken` constants in both products, the full `hasEntitlementAccess` logic, `ODVAEntityPermissions` fields, the `vx`/`iim` prefix branching, the absence of `@With` in `video-hub` controllers, the shared `mongo.db` value across five services, and the absence of departmentalization in all six build files. Inferred: that the five downstream services are gateway-only (based on absence of auth code, not on positive proof of network restriction) — treat as the item to confirm first.

---

## Cross-product comparison

For the platform team, the differences matter more than the similarities:

| Dimension | Interview Intelligence | Screening |
|---|---|---|
| Calls User Management | ✅ `validateAuthLoginToken` | ✅ identical mechanism |
| Permission key prefix | `II_` | `ODVA_` (+ `Settings_ODVA`, `sms*`, `email*`) |
| Access data in Mongo | 1 collection (`permissionsForRole`) | **none** |
| Per-user gate | has ≥1 permission | **tenant entitlement match** (`ALL` or `refNum`) |
| Permission shape | untyped boolean flags | typed class, `My`/`All` scoped |
| Where enforced | per-controller `@With` + per-object computation | gateway only, decision handed to client |
| Per-object membership | ✅ heavy (`forwardedList`, `panel`) | none found |
| Departmentalization | active in `evaluation-service`, hardcoded off in IMS | **none anywhere** |
| Mongo estate | `interviewmanagement`, `InterviewEvaluations` | `mongo_ngcc*` (+ odva URIs) |

Three consolidation implications:
1. **The transport is already uniform** — both products use the same DDO, headers, and payload. A shared model can keep that contract.
2. **There are at least three competing ways to express scope**: departmentalization (`evaluation-service`), tenant entitlements (`video-hub`), and `My`/`All` permission naming (`ODVAEntityPermissions`) — plus per-object membership in II. Picking one is the actual design problem.
3. **Enforcement location differs fundamentally** — II enforces server-side per object; Screening validates at the edge and trusts the client. A single model has to decide which, and Screening's downstream services would need enforcement added if the answer is server-side.

---

## How to audit the next pillar

Repeatable and quick — roughly 15 minutes per domain. Run from a repo root under `repos/`.

```bash
# 1. Mongo databases in play
rg -n 'db\.name|database=|MONGO_DB|mongodb\.uri' --glob '!*test*' \
  src/main/resources conf config 2>/dev/null

# 2. Collection name constants (find the constants file first, then list it)
rg -n 'COLLECTION|@Document|getCollection\(' --glob '!*test*' -l
rg -n 'COLLECTION\s*=\s*"' <constants-file>

# 3. Is there a permission/role store at all?
rg -in 'permission|role.*mapping|accessType|acl' --glob '!*test*' -l

# 4. Central auth delegation (expect a hit — this is the norm)
rg -n 'validateTokenAndPermissions|auth\.url|usermanagement' --glob '!*test*'

# 5. Departmentalization adoption — check the BUILD FILE, not just code
rg -n 'departmentaliz|crm-commons' build.gradle build.sbt pom.xml package.json 2>/dev/null
rg -n 'getMongoScopeFilter|ScopeFilterRequest|scopeAttr' --glob '!*test*'

# 6. Auth coverage gaps (Java/Play example — adapt per stack)
for f in <controllers-dir>/*.java; do rg -q '@With' "$f" || echo "no-auth-action: $(basename $f)"; done
```

Two traps this audit hit, worth avoiding:

- **Exclude test files.** II's test tree references methods and collection names that read like production config and will skew the picture. Every `rg` above uses `--glob '!*test*'` for that reason.
- **Check the build file for departmentalization, not just code.** A service can have `scopeAttr` constants and scope-shaped fields while having no scope enforcement at all — `interview-management-service` is exactly that case.

When done, add a section above following the II template — headline, databases, permission stores, enforcement layers, membership fields, departmentalization status, look-alike collections, open questions, confidence — and flip the pillar's row in the audit-status table.
