---
name: jira-domain-requirements
description: >-
  Fetch a Jira story or epic from Phenom Atlassian, analyze its scope, and
  produce structured requirements decomposed by platform domain area (CRM,
  Integrations, Analytics, Messaging, Screening, Scheduling, Automations). Use
  when the user provides a Jira URL or key (e.g. PHEM-2190578), asks for
  domain-area requirements, impact analysis by product area, or cross-team
  requirement breakdown from a Jira story.
---

# Jira Domain Requirements

Decompose a Jira story into actionable requirements per Phenom platform domain.
Output is review-ready for pod leads and can feed Northstar specs or child Jira tickets.

## Domain areas

Always evaluate all seven areas. See [domains.md](domains.md) for scope boundaries.

| Area | Typical ownership |
|------|-------------------|
| CRM | Job/candidate entities, recruiter UI, job creation & details |
| Integrations | ATS/HRM job pull, portal publish, external system sync |
| Analytics | Snowflake events, reporting, audit/history, Beacon |
| Messaging | Email/SMS/in-app notifications, templates |
| Screening | Application flows, apply eligibility, candidate-facing gates |
| Scheduling | Cron jobs, timed triggers, calendar-based execution |
| Automations | Workflow engine, tenant scans, rule-based job actions |

## Workflow

```
Task Progress:
- [ ] Step 1: Fetch Jira issue(s)
- [ ] Step 2: Extract requirements from description & acceptance criteria
- [ ] Step 3: Map each requirement to domain area(s)
- [ ] Step 4: Write EARS requirements per area
- [ ] Step 5: Flag gaps, dependencies, and out-of-scope items
- [ ] Step 6: Present summary to user
```

### Step 1: Fetch Jira issue(s)

**Cloud ID:** Use `phenompeople.atlassian.net` as `cloudId`. Fall back to `getAccessibleAtlassianResources` if calls fail.

**Parse input:**
- URL `https://phenompeople.atlassian.net/browse/PHEM-123456` → key `PHEM-123456`
- Bare key `PHEM-123456` → use directly

**Fetch the story:**

```
getJiraIssue(
  cloudId="phenompeople.atlassian.net",
  issueIdOrKey="PHEM-123456",
  fields=["summary", "description", "status", "issuetype", "priority", "parent", "issuelinks", "components", "labels", "comment"],
  expand="renderedFields",
  responseContentFormat="markdown"
)
```

**Also fetch when present:**
- Parent epic (`parent.key`) — broader scope and sibling stories
- Linked issues (`issuelinks`) — dependencies and related work

### Step 2: Extract source requirements

From description and acceptance criteria, capture:

1. **User story** — persona, action, benefit
2. **Functional requirements** — numbered bullets in the ticket
3. **Acceptance criteria** — testable outcomes
4. **Constraints** — timezone, compliance SLAs, customer timelines, feature flags
5. **Explicit non-goals** — what must NOT change

Quote the source Jira key for traceability on every derived requirement.

### Step 3: Map to domain areas

For each source requirement, assign one or more domain areas.

**Rules:**
- One requirement may span multiple areas (e.g. CRM UI + Scheduling cron) — duplicate the parent REQ with area-specific children
- If an area has no impact, include the section with `No requirements — <one-line rationale>`
- Do not invent scope not implied by the ticket; mark assumptions as `ASSUMPTION:`

### Step 4: Write EARS requirements

Use EARS form with stable REQ-IDs:

```
REQ-<AREA>-<NNN>: WHEN/IF/WHILE <trigger> THE SYSTEM SHALL <observable behavior>
```

**Per-area section template:**

```markdown
## <Area>

**Impact:** High | Medium | Low | None
**Source:** PHEM-XXXXXXX (relevant bullets)

### Requirements

| REQ-ID | Requirement | Source |
|--------|-------------|--------|
| REQ-CRM-001 | WHEN ... THE SYSTEM SHALL ... | PHEM-XXXX, bullet 1 |

### Acceptance criteria

- [ ] <testable criterion tied to REQ-ID>

### Dependencies / open questions

- <dependency on another area, epic, or external team>
```

**Cross-cutting items** (localization, analytics) belong in their primary area AND a brief note under Analytics if data is emitted.

For Jira-ready user stories per area, use the Phenom story format from `story-template` skill (User Story / Scenario Given-When-Then / Considerations).

### Step 5: Flag gaps

Always include:

```markdown
## Cross-domain summary

| Area | Impact | REQ count |
|------|--------|-----------|

## Gaps & risks
- <missing AC, ambiguous timezone rule, etc.>

## Suggested child tickets (optional)
- [CRM] <title>
- [Automations] <title>
```

### Step 6: Deliver output

**Default:** Present requirements in chat.

**When user asks to save:** Write to `JIRA/<KEY>-domain-requirements.md` in the workspace (or path they specify).

**Offer next steps** only when relevant: create child Jira tickets (`spec-to-backlog` skill), Northstar spec (`/ns-specify`), or Confluence page.

## Quality bar

- Every REQ-ID is testable — no "fast", "robust", "easy"
- Timezone, tenant, and portal-scope rules stated explicitly
- Compliance SLAs (e.g. unpost within 1 hour) become measurable acceptance criteria
- Distinguish **portal visibility** vs **job entity mutation** when the ticket says so
- Customer go-live dates from the ticket appear in Scheduling/Automations priority notes

## Example invocation

User: "Break down PHEM-2190578 by domain area"

1. Fetch PHEM-2190578 and parent PHEM-2117038
2. Extract Job Expiry field, cron unpost, automations scan requirements
3. CRM → field UI & persistence; Scheduling → cron interval; Automations → tenant scan; Screening → apply blocked post-expiry; Integrations → portal visibility; Analytics → unpost events
4. Messaging → None (no notification mentioned)
5. Output seven sections + cross-domain summary

## Additional resources

- Domain scope definitions: [domains.md](domains.md)
- Jira-ready story format: `story-template` skill in SpecDrivenDev
- Create backlog tickets from requirements: `spec-to-backlog` skill
