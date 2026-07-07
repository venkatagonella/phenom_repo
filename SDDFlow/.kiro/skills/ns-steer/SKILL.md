---
name: ns-steer
description: "Use when onboarding a brownfield repo or refreshing project context — inspects the actual codebase, detects (does not invent) the stack and conventions, and writes the steering files (product, tech, structure) into northstar/steering/ as the Layer-1 living context."
---

<!-- Generated self-contained SDD bundle — do not edit here; regenerate from the SDD kit. -->

# Prompt: /ns-steer  (brownfield onboarding · keep living context current)

You are setting up or refreshing this repo's **Layer 1 living context** — the steering
files the agent reads before every change. Follow the SDD constitution (bundled as always-on Kiro steering) (§5, §8).

Use this when: onboarding an existing (brownfield) repo to SDD, OR after a change that
altered how the system works and the steering is now stale.

---

## What to do

1. **Inspect the actual codebase** — package manifests, directory structure, config,
   representative modules, tests, existing docs/README. Don't guess; read.
2. **Detect, don't invent**: the stack and versions, the conventions actually in use
   (error handling, async style, API shape, naming), the module boundaries, where things
   live, and any compliance/security patterns evident in code.
3. **Write the three steering files** to `northstar/steering/`, each from its template, filled
   with what you detected (replace the template's example italics with the repo's reality):
   - Copy the **product steering template** (included at the end of this skill) → `northstar/steering/product.md` — what the
     product is, user roles, scope, obligations.
   - Copy the **tech steering template** (included at the end of this skill) → `northstar/steering/tech.md` — stack, conventions,
     testing standards, banned patterns.
   - Copy the **structure steering template** (included at the end of this skill) → `northstar/steering/structure.md` — layout,
     module boundary rules, where new code goes.
   Create the `northstar/steering/` directory if it doesn't exist. If a file already exists,
   **update it in place** (it's living context, §8) rather than starting over — preserve
   anything still accurate.
4. **Flag conflicts**: anywhere the code disagrees with itself (two error formats, mixed
   async styles) — surface it so the human can decide the canonical convention. Keep each
   file lean (~300 words; constitution §13 — `structure.md` may run to ~600 as the codebase
   map) — push depth into specs, not steering.

**Canonical location is fixed (constitution §1).** If the repo already has specs, requirements,
or design docs in another directory (`docs/`, `specs/`, `.kiro/specs/`, a legacy `design/`
folder, etc.), do **not** adopt or write into it. The steering files always go to
`northstar/steering/` and specs always to `northstar/specs/`. Migrate any useful content *from*
the old location into the canonical files, and note the old path so the human can retire it.
SDD never tracks specs or steering outside `northstar/`, however the repo is currently laid out.

## Output format
After writing the files, report (do not paste the full file bodies back):
- A short "What I found" summary (stack, conventions, notable patterns, conflicts).
- The list of files you wrote/updated (`northstar/steering/product.md`, `tech.md`, `structure.md`)
  and a brief `git diff --stat` style note of what changed.
- A list of assumptions you made that the human should verify.

## Self-check
- Did I actually write all three files to `northstar/steering/`? (The deliverable is files on
  disk the human can review as a diff — not drafts in the chat.)
- Is every claim grounded in something I actually read in the repo?
- Did I capture conventions as they ARE, not as they "should" be? (Improvements are
  separate specs, not steering edits.)
- Did I flag every place the codebase is internally inconsistent?

## Stop
Stop after writing the files and reporting. The human reviews the diff and commits. Do
**not** chain into another flow. From then on, every `/ns-*` command loads steering in
Phase 0.

---

## Templates (self-contained — copy the relevant skeleton into `northstar/steering/` — as `product.md`, `tech.md`, `structure.md` respectively)

### `steering-product.md`

```markdown
# Product Steering — What we build & why

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec.
> Replace the example italics with your project's reality. Drafted by `/ns-steer`.

## What this product is
<!-- One paragraph: the product, the core value, the stage (MVP / scaling / mature). -->
_Example: A B2B SaaS that helps HR teams manage employee onboarding. Mid-stage; ~40
customers; reliability and compliance matter more than raw feature velocity._

## Who uses it (roles)
<!-- The user roles the system knows about. These show up in requirements. -->
- _HR Admin — configures workflows, manages employees._
- _Employee — completes onboarding tasks._
- _Manager — approves and tracks their reports._

## Problems it solves / boundaries
<!-- What's in scope and explicitly out of scope for the product. -->
- _In scope: onboarding workflows, document collection, e-signatures._
- _Out of scope: payroll, performance reviews (separate products)._

## Compliance & policy obligations
<!-- Anything that constrains requirements: GDPR, HIPAA, SOC2, data retention, etc. -->
- _GDPR: personal employee data; 90-day retention on exports; access events logged._

## Non-functional defaults that apply to most features
<!-- Defaults the agent should assume unless a spec overrides them. -->
- _All user-facing endpoints require auth; HR-admin actions require MFA._
- _p95 API latency target: < 300ms for read paths._
```

### `steering-tech.md`

```markdown
# Tech Steering — Stack, conventions, standards

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec
> and design. Replace the example italics with your stack. Drafted by `/ns-steer`.

## Stack
<!-- Languages, frameworks, datastores, infra. Pin versions where they matter. -->
- _Backend: Node.js 20+, TypeScript (strict), Express._
- _Frontend: React 18, Vite._
- _Data: PostgreSQL 15, Redis (cache + queues)._
- _Infra: AWS (ECS, RDS), Terraform._

## Conventions
<!-- Naming, error handling, API shape, async patterns — the things every PR must match. -->
- _All async via async/await; no raw promise chains._
- _REST; resource-oriented routes; plural nouns._
- _Standard error envelope: `{ error: { code, message, details } }`._
- _No `any` in TypeScript; prefer explicit types._

## Testing standards
<!-- What "tested" means here. Referenced by constitution §10. -->
- _Unit: Jest. Integration: Jest + test DB. E2E: Playwright._
- _New code: meaningful coverage of acceptance criteria, not a % target._
- _Bugs: a regression test is mandatory (fails before fix, passes after)._

## Constraints / banned patterns
<!-- Things the agent must NOT do. -->
- _No new runtime dependencies without noting it in the spec's design._
- _No direct SQL in controllers; go through the data-access layer in `/db`._
```

### `steering-structure.md`

```markdown
# Structure Steering — How the codebase is organized

> **Layer 1 / living context.** Keep this current; the agent uses it to place new files
> correctly and to find existing code during Phase-0 discovery. Drafted by `/ns-steer`.

## Directory layout
<!-- The top-level map. Where features live, where shared code lives. -->
```
src/
├── api/            # HTTP controllers, one folder per resource
├── services/       # business logic, framework-agnostic
├── db/             # data-access layer, migrations, models
├── lib/            # shared utilities
└── jobs/           # async/queue workers
tests/
├── unit/  integration/  e2e/
```

## Module boundary rules
<!-- What's allowed to import what. The agent must respect these. -->
- _Controllers (`api/`) call services; never touch `db/` directly._
- _Services contain business logic; no HTTP/Express types leak in._
- _Shared helpers go in `lib/`; if used by 3+ modules, it belongs there._

## Where things go
<!-- Conventions for placing new code, so specs/tasks target the right paths. -->
- _A new feature `foo`: `src/api/foo/`, `src/services/foo/`, tests mirror the path._
- _A new background job: `src/jobs/`._
- _A new DB table: migration in `src/db/migrations/`, model in `src/db/models/`._
```

