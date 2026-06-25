# Product steering

## Recruiter-family roles (reference implementation)

When `hiring_team_expanded_roles` is enabled for a tenant:

| Role | Category | Delete/Close | Create jobs |
|------|----------|--------------|-------------|
| Primary Recruiter | Leading | Allowed on assigned jobs | Allowed |
| Secondary Recruiter | Supporting | Denied | Allowed |

Legacy `Recruiter` hiring-team memberships resolve to Primary Recruiter without changing the display label.

When the flag is OFF, all users with legacy `Recruiter` membership retain full delete/close/create behavior.
