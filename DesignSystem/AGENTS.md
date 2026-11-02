# Agents — Phenom Design System workspace

This repository is a **referrable PDS pack** for Cursor: skills, Storybook-aligned component maps, and CSS tokens used to build sample websites in other workspaces.

## Required reading

1. `.cursor/skills/phenom-design-system/SKILL.md`
2. `styles/pds-tokens.css` + `styles/pds-utilities.css`
3. Official Storybook: https://pds.phenom.com/angular/index.html?path=/docs/introduction-getting-started--documentation

## Goals

- Keep styling **portable** via CSS variables in `styles/`.
- Keep component naming aligned with Angular `px-*` / React Storybook.
- Document how other workspaces attach this pack (see skill `cross-workspace.md` and root `README.md`).

## Do not

- Commit `.npmrc` auth tokens or Font Awesome secrets.
- Treat HTML utility classes as a replacement for production `@phenom/angular-ds` / `@phenom/react-ds` in real Phenom apps.
