---
name: phenom-design-system
description: >-
  Builds UIs with Phenom Design System (PDS) tokens, Angular px-* components
  (@phenom/angular-ds), and React DS (@phenom/react-ds). Use when creating sample
  websites, prototypes, product screens, Storybook-aligned UI, or when the user
  mentions PDS, Phenom DS, px-button, design tokens, or pds.phenom.com.
---

# Phenom Design System (PDS)

## Source of truth

| Resource | URL / path |
|---|---|
| Angular Storybook | https://pds.phenom.com/angular/index.html |
| React Storybook | https://pds.phenom.com/react/index.html |
| Getting started (Angular) | https://pds.phenom.com/angular/index.html?path=/docs/introduction-getting-started--documentation |
| This reference workspace | `/Users/venkata.gonella/phenom_repo/DesignSystem` |

**Always** resolve component names, props, and variants from Storybook (or the references in this workspace). Do not invent PrimeNG/PrimeReact APIs for product UI — use the PDS wrappers.

## Before building UI

1. Read [getting-started.md](getting-started.md) for install / VPN / `.npmrc`.
2. Read [tokens.md](tokens.md) and use workspace `styles/pds-tokens.css` for visual styling.
3. Pick components from [components.md](components.md) (selectors `px-*`).
4. Follow [usage-recipes.md](usage-recipes.md) for Angular / React / HTML prototype patterns.
5. For cross-workspace wiring, follow [cross-workspace.md](cross-workspace.md).

## Hard rules

1. **Selector prefix is `px`** (Angular): `<px-button>`, `<px-inputtext>`, `<px-modal>`, etc.
2. **Modules** are `Px*Module` (e.g. `PxButtonModule`) imported from `@phenom/angular-ds`.
3. **Do not** use raw PrimeNG/PrimeReact components in new UI when a PDS wrapper exists.
4. **Do not hardcode brand colors** — use CSS variables from `styles/pds-tokens.css` or `@phenom/design-tokens`.
5. **One primary CTA** per viewport (brand indigo / `--bg-brand-primary-default`).
6. **Font**: Poppins for body (`--font-family-body`).
7. **CSS cascade layers** (Angular): `primeng` → `phenomds` → `app`. Put app overrides in the `app` layer only.
8. **VPN + `.npmrc`** required to install private packages from `pie-nexus.phenompro.com`.
9. When a component “seems missing”, check Storybook — names differ (Button → `px-button` / `PxButtonModule`).
10. For **sample/static websites** without npm registry access, import referrable styles from this workspace:

```html
<link rel="stylesheet" href="file:///Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css" />
<link rel="stylesheet" href="file:///Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-utilities.css" />
```

Or copy / symlink those files into the consumer project (preferred for portability).

## Decision tree

```
Need a real Phenom app UI?
  ├─ Angular → @phenom/angular-ds + @phenom/design-tokens (+ PrimeNG peers)
  ├─ React   → @phenom/react-ds + @phenom/design-tokens (+ PrimeReact peers)
  └─ Static sample / marketing mock / no VPN?
        → Use styles/pds-tokens.css + styles/pds-utilities.css
          and HTML templates under templates/html/
```

## Naming cheat sheet

| Concept | Angular | React (current DS) |
|---|---|---|
| Package | `@phenom/angular-ds` | `@phenom/react-ds` |
| Tokens | `@phenom/design-tokens` | `@phenom/design-tokens` |
| Button | `<px-button>` / `PxButtonModule` | Storybook `Button/*` exports |
| Input | `<px-inputtext>` / `PxInputTextModule` | `InputField` (see React Storybook) |
| Legacy React UI (older) | — | `@phenom/react-ui-components` (not the primary PDS) |

## Output expectations

When generating UI for the user:

- Prefer PDS components over custom HTML controls.
- Style with token variables (`var(--bg-brand-primary-default)`, `var(--pds-*)` aliases).
- Link the matching Storybook docs path in a short comment when introducing a component.
- Keep layouts enterprise-dense, not generic SaaS card grids, unless the brief asks otherwise.

## Additional resources

- [getting-started.md](getting-started.md)
- [components.md](components.md)
- [tokens.md](tokens.md)
- [usage-recipes.md](usage-recipes.md)
- [cross-workspace.md](cross-workspace.md)
- [storybook-map.md](storybook-map.md)
- Workspace styles: `/Users/venkata.gonella/phenom_repo/DesignSystem/styles/`
