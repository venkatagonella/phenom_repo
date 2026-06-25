# NorthStarCheck

Reference implementation for **Secondary Recruiter** job-level role permissions (PHEM-2109151).

## What it demonstrates

- Role registry with Primary Recruiter and Secondary Recruiter
- `hiring_team_expanded_roles` feature flag (per-tenant)
- Secondary Recruiter can **create** jobs (template / blank / clone)
- Only **Primary Recruiter** can **delete** or **close** jobs when the flag is ON
- Server-side enforcement with UI permission endpoint

## Quick start

```bash
npm install
npm test
npm run dev
```

## UI

Phenom Design System (PDS) styled CRM shell modeled after Pipeline **Create New Job**:

- **Demo hub:** `http://localhost:3000/`
- **Create flow:** `/ui/create-job?userId=secondary-demo&tenantId=demo-tenant`
- **Job details:** `/ui/create-job?jobId=...&userId=...&tenantId=demo-tenant`

Design tokens: `src/ui/pds.css` (Poppins, slate palette, purple accent per [PDS](https://pds.phenom.com/angular/index.html?path=/docs/introduction-getting-started--documentation)).

## Spec

See `northstar/specs/001-secondary-recruiter-role-enforcement/`.
