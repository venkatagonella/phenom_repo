# Tech Steering — Stack, conventions, standards

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec
> and design. Drafted by `/ns-steer` from the DesignSystem repo as it exists today.

## Stack

- **Content / samples:** static HTML + CSS (no app framework required for `templates/html/`).
- **Tokens:** CSS custom properties in `styles/pds-tokens.css`; sample utilities in `styles/pds-utilities.css`; page-specific CSS (e.g. `styles/job-fields-settings.css`).
- **Agent guidance:** Cursor skill at `.cursor/skills/phenom-design-system/`; always-on rule `.cursor/rules/phenom-design-system.mdc`.
- **Reference source of truth:** Phenom Storybook — Angular https://pds.phenom.com/angular/index.html ; React https://pds.phenom.com/react/index.html .
- **Catalog:** `references/component-catalog.json`, `references/angular-selectors.txt`.
- **SDD:** specs under `northstar/specs/`; living context under `northstar/steering/`.
- **VCS:** GitHub `venkatagonella/DesignSystem` (public); feature work on `cursor/*` branches.
- **Not present in-repo:** Node/npm app package.json for a runtime SPA; Angular/React apps that import `@phenom/*`.

## Conventions

- UI samples follow the Phenom Design System skill; brand colors come from tokens, not ad-hoc hex (page CSS may still use CRM-matched neutrals when mirroring a specific screen).
- HTML samples are self-contained: link relative CSS, inline small behavior scripts when needed.
- Document Angular/React package usage in `templates/angular/USAGE.md` and `templates/react/USAGE.md` without requiring those packages for HTML demos.
- Specs use EARS (`WHEN/WHILE/IF/WHERE … THE SYSTEM SHALL …`) with stable `REQ-ID`s under `northstar/specs/`.

## Testing standards

- No automated test runner is configured in this repo today.
- For new sample pages: manual check in a local browser (open file or static server) against acceptance criteria in the spec.
- Prefer acceptance criteria that are observable without a private VPN (static markup/behavior), unless a requirement explicitly needs live QA.

## Constraints / banned patterns

- Do not commit secrets (`.npmrc` tokens, Font Awesome keys).
- Do not treat HTML utility classes as a substitute for production `@phenom/angular-ds` / `@phenom/react-ds` in real Phenom apps.
- Do not invent new design-system components outside Storybook naming; map to PDS stories when approximating.
- Do not write SDD specs/steering outside `northstar/`.
