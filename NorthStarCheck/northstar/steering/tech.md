# Technical steering

## Stack

- **Runtime:** Node.js 18+
- **Language:** TypeScript (ESM)
- **HTTP:** Express 4
- **Tests:** Vitest + Supertest

## Module layout

| Path | Purpose |
|------|---------|
| `src/roles/` | Role registry, feature flags, shared types |
| `src/jobs/` | Job repository, hiring team, job service |
| `src/permissions/` | Authorization for job lifecycle actions |
| `src/api/` | HTTP routes and auth middleware |
| `src/ui/` | Thin HTML/JS demo for permission-driven UI |
| `tests/` | Unit and integration tests mapped to REQ-IDs |

## Auth (reference only)

Requests require headers `x-user-id` and `x-tenant-id`. Production would use platform session/JWT.
