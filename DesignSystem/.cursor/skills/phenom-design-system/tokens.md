# PDS Design Tokens

## Production source

- Package: `@phenom/design-tokens` (from `pds-design-tokens` repo)
- Built outputs: `dist/css`, `dist/scss`, `dist/js` (Style Dictionary)
- Figma: Tokens Studio sync into `tokens/**/*.json`

## Referrable styles in this workspace

For sample websites and Cursor-driven prototypes **without** installing private packages:

| File | Purpose |
|---|---|
| `styles/pds-tokens.css` | Semantic CSS variables extracted from published Angular Storybook |
| `styles/pds-utilities.css` | Small utility classes (buttons, surfaces, type) built on those tokens |

Absolute path (this machine):

```
/Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css
/Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-utilities.css
```

## Core aliases (prototypes)

Use these first — they map to Storybook semantic tokens:

```css
var(--pds-brand)          /* indigo CTA (Storybook secondary brand) */
var(--pds-brand-hover)
var(--pds-brand-teal)     /* Storybook primary/teal accent */
var(--pds-text)
var(--pds-text-muted)
var(--pds-surface)
var(--pds-surface-muted)
var(--pds-border)
var(--pds-success)
var(--pds-warning)
var(--pds-error)
var(--pds-radius-md)
var(--pds-shadow-sm)
var(--font-family-body)   /* Poppins */
```

In Storybook token CSS, `--color-primary-*` is teal and indigo CTAs map to `--color-secondary-*` / `--bg-brand-secondary-*`.

## Semantic token families (from Storybook CSS)

- `--bg-*` — surfaces, brand fills, overlays, disabled
- `--text-*` — default / subtle / inverse / brand text
- `--border-*` — default, strong, focus, error
- `--icon-*` — icon colors
- `--color-*` — palette primitives
- `--spacing-*` — spacing scale
- `--font-*` — size / weight / line-height
- `--borderRadius-*` / radius tokens
- `--shadows-*`
- `--feedback-*` — success / warning / error / info
- `--opacity-*`

## Typography

- Body font: **Poppins**
- Load for HTML samples:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

## Rules

1. Never introduce a new hex for brand/UI chrome if a token exists.
2. Prefer semantic tokens (`--bg-brand-primary-default`) over raw palette (`--color-*`) in components.
3. Keep numeric tables / metrics in `tabular-nums` when showing dense data.
4. Max **one** primary brand button per viewport.
