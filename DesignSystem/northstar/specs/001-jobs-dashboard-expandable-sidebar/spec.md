---
spec_id: 001-jobs-dashboard-expandable-sidebar
summary: Local Jobs dashboard sample with PDS expandable SidebarNavigation; Job Fields fixed settings nav unchanged
type: feature
status: implemented
approval_state: approved
owners: [venkatagonella]
reviewers: [venkatagonella]
ticket_ids: []
risk: low
blast_radius: Demo-only HTML sample and nav pattern docs; does not change production CRM or Job Fields settings page
touches:
  - templates/html/jobs-dashboard.html
  - styles/jobs-dashboard.css
  - README.md
  - northstar/steering/structure.md
amends: []
supersedes_reqs: []
compliance_tags: []
northstar_version: 0.1
originating_ide: cursor
last_validated_at: "2026-08-12"
---

# Jobs dashboard sample with expandable sidebar

## 1. Summary

Deliver a local static sample page that looks like Phenom CRM Jobs (`/dashboard/jobs`), styled with this pack’s Phenom Design System tokens and skill guidance. The page uses an expandable/collapsible left navigation modeled on PDS Storybook `SidebarNavigation` (expanded), instead of the fixed settings left nav used on the Job Fields sample. The Job Fields settings page remains unchanged.

## 2. Context discovered (Phase 0)

- **Steering reviewed:** product (static PDS sample pack), tech (HTML/CSS + Storybook source of truth), structure (new samples under `templates/html/` + page CSS; current LHN is fixed `.setting-menu` on Job Fields).
- **Existing specs that overlap (`touches`):** none — first increment spec.
- **Requirements this change amends/supersedes:** none — net new.
- **Relevant code paths:** `templates/html/job-fields-settings.html` (fixed settings nav), `styles/job-fields-settings.css`, `styles/pds-tokens.css`, `styles/pds-utilities.css` (fixed `.pds-sidebar`), `.cursor/skills/phenom-design-system/components.md` (`px-sidebar-navigation`).
- **Current behavior:** Job Fields sample shows a always-expanded text list of settings links with no collapse control. No Jobs dashboard sample exists. PDS documents `SidebarNavigation` / `px-sidebar-navigation` with an Expanded story.
- **Scope choice (human):** **A** — expandable sidebar on the new Jobs page only; do not retrofit Job Fields.

## 3. Requirements (EARS)

### 3.1 Jobs sample page

- **REQ-001** — WHEN a user opens the Jobs sample over localhost (or as a static file served from this repo) THE SYSTEM SHALL display a Jobs dashboard page at `templates/html/jobs-dashboard.html`.
  - *Acceptance:* Opening the page URL shows a document title or visible page heading that includes “Jobs”.

- **REQ-002** — WHEN the Jobs sample is displayed THE SYSTEM SHALL present a CRM-like jobs list area that includes at least: a page title, a toolbar with search, and a table (or list) of three or more sample job rows with columns for job title, job id, and status.
  - *Acceptance:* Manual check shows title + search control + ≥3 rows with those three columns populated with static sample data (no live API).

- **REQ-003** — WHEN the Jobs sample is styled THE SYSTEM SHALL load `styles/pds-tokens.css` and page styles that use PDS CSS variables for brand/surface/text colors (no new invented brand palette).
  - *Acceptance:* Page `<link>` includes `pds-tokens.css`; computed brand/nav accent colors resolve through CSS variables defined in that file (or aliases that reference them).

### 3.2 Change from fixed left nav → expandable SidebarNavigation

These requirements describe what must change relative to the **current** Job Fields fixed left nav pattern (`.setting-menu` always showing full labels).

- **REQ-004** — WHEN the Jobs sample left navigation is rendered in the default state THE SYSTEM SHALL show the PDS SidebarNavigation **expanded** pattern: icon + text label for each primary nav item (reference: Storybook `navigation-sidebarnavigation--expanded`).
  - *Acceptance:* In the default view, each primary nav item shows both a visible icon and a visible text label; “Jobs” (or equivalent) is marked current via `aria-current="page"` or an equivalent active style.

- **REQ-005** — WHEN the Jobs sample page chrome is displayed THE SYSTEM SHALL provide one user-activatable control that collapses and expands the left navigation (a single toggle is allowed).
  - *Acceptance:* A focusable control is present in the sidebar chrome; its accessible name indicates collapse when expanded and expand when collapsed (or an equivalent state-aware name).

- **REQ-006** — WHEN the user activates the sidebar collapse control while expanded THE SYSTEM SHALL switch the left navigation to a collapsed state that hides nav item text labels and keeps icons visible.
  - *Acceptance:* After one activation of the collapse control, nav labels are not visible and icons remain visible; main content remains usable beside the narrower sidebar.

- **REQ-007** — WHEN the user activates the sidebar expand control while collapsed THE SYSTEM SHALL restore the expanded state with icons and text labels visible again.
  - *Acceptance:* After expand, labels are visible again without reloading the page.

- **REQ-008** — WHILE the sidebar is collapsed OR expanded THE SYSTEM SHALL keep the selected Jobs destination indicated as the current page.
  - *Acceptance:* Current-item indication remains present in both states (style and/or `aria-current`).

- **REQ-009** — WHERE the Jobs sample defines primary destinations THE SYSTEM SHALL include at least these left-nav items: Dashboard, Jobs (current), Candidates, Settings.
  - *Acceptance:* All four labels appear in the expanded state; Jobs is the current item.

- **REQ-010** — IF a consumer compares Job Fields vs Jobs samples THEN THE SYSTEM SHALL leave `templates/html/job-fields-settings.html` using its existing fixed settings left nav (no expandable SidebarNavigation retrofit in this increment).
  - *Acceptance:* Diff for this feature does not change the Job Fields `.setting-menu` markup/behavior to the expandable pattern.

- **REQ-011** — WHERE sidebar styles for the Jobs sample are added THE SYSTEM SHALL keep them in `styles/jobs-dashboard.css` (or other Jobs-only assets) so that `templates/html/sample-page.html` and shared `styles/pds-utilities.css` behavior remain unchanged.
  - *Acceptance:* This feature’s diff does not modify `templates/html/sample-page.html` or `styles/pds-utilities.css`.

### 3.3 Local host / delivery

- **REQ-012** — WHEN a developer follows the local-host instructions in `README.md` THE SYSTEM SHALL serve the Jobs sample at `templates/html/jobs-dashboard.html` without private npm packages.
  - *Acceptance:* `README.md` documents one local server command and the URL/path to open; the page loads with only the repo’s static assets.

## 4. Non-functional requirements

- **NFR-001 (perf):** WHEN the Jobs sample is loaded from a local static server THE SYSTEM SHALL become interactive (sidebar toggle responds) within 3 seconds on a typical developer laptop with warm cache.
  - *Acceptance:* Manual stopwatch check from navigation start to first successful collapse toggle under 3 seconds.
- **NFR-002 (security):** WHERE the sample runs locally THE SYSTEM SHALL not require or embed secrets, auth tokens, or live CRM credentials.
  - *Acceptance:* No `.npmrc` tokens, API keys, or session cookies are added by this feature’s files.
- **NFR-003 (a11y):** WHEN the sidebar collapse/expand control is present THE SYSTEM SHALL be reachable by keyboard (Tab), SHALL expose an accessible name (e.g. “Collapse navigation” / “Expand navigation”), and SHALL show a visible focus indicator when focused.
  - *Acceptance:* Keyboard-only user can focus and activate the control; accessible name is exposed via visible text or `aria-label`; focused control shows a non-default visible outline or equivalent focus style.

## 5. Out of scope

- Retrofitting Job Fields (or other existing samples) to expandable SidebarNavigation.
- Live CRM data, authentication, or calling `candidates-intqa.phenompro.com`.
- Installing `@phenom/angular-ds` / `@phenom/react-ds` for this HTML sample.
- Pixel-perfect parity with every Jobs QA widget (filters, bulk actions, infinite scroll) beyond the minimum in REQ-002.
- Production CRM code changes.
- Changes to shared `styles/pds-utilities.css` or `templates/html/sample-page.html` in this increment.

## 6. Open questions

- None for requirements approval (scope choice A confirmed).

## Changelog

- v0.1.0 — 2026-08-12 — initial draft — pending PR
- v0.1.1 — 2026-08-12 — address spec review: require toggle control; Jobs-only CSS; README local host; visible focus
- v0.1.2 — 2026-08-12 — requirements gate approved by venkatagonella
