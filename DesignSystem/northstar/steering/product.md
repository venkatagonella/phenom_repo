# Product Steering — What we build & why

> **Layer 1 / living context.** Keep this current; the agent reads it before every spec.
> Drafted by `/ns-steer` from the DesignSystem repo as it exists today.

## What this product is

A **referrable Phenom Design System (PDS) pack** for Cursor: skills, Storybook-aligned component maps, CSS tokens, and static HTML sample pages. Agents and humans use it to build sample CRM-like UIs that look like Phenom products without treating this repo as the production `@phenom/angular-ds` / `@phenom/react-ds` source.

Stage: early pack — tokens, skills, and a small set of HTML samples (including Job Fields settings).

## Who uses it (roles)

- **Cursor agent** — reads skill/rules/tokens to generate sample UI in this or another workspace.
- **Phenom engineer / designer** — opens HTML samples locally and copies patterns into consumer apps.
- **Consumer app maintainer** — attaches this pack (skill, multi-root, or symlink) but ships real UI via official PDS npm packages.

## Problems it solves / boundaries

- **In scope:** portable CSS tokens/utilities; Cursor skill + rules; HTML/Angular/React usage notes; static sample pages that mirror CRM settings/jobs UX for demos.
- **Out of scope:** production CRM backend/API; publishing `@phenom/*` packages; replacing live Storybook; authenticated QA environments as a runtime dependency.

## Compliance & policy obligations

- Do not commit `.npmrc` auth tokens or Font Awesome secrets.
- Sample pages may mimic CRM screens for local demo only; they must not claim to be the live CRM app.

## Non-functional defaults that apply to most features

- Prefer PDS CSS variables from `styles/pds-tokens.css` / utilities; do not invent brand colors.
- Angular naming in docs/samples follows `px-*` selectors; HTML samples may approximate with CSS classes.
- Sample pages must load as static files (or a trivial local static server) with no private package install required for HTML demos.
- Accessibility: interactive samples need keyboard-reachable controls and visible focus for nav/actions.
