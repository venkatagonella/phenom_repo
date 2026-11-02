# PDS Usage Recipes

## A) HTML / static sample site (no private npm)

Best for demos in other Cursor workspaces when VPN/registry is unavailable.

1. Copy or symlink `styles/pds-tokens.css` + `styles/pds-utilities.css`.
2. Start from `templates/html/sample-page.html`.
3. Compose with utility classes (`.pds-btn-primary`, `.pds-card`, `.pds-field`, …).
4. Keep visual language: Poppins, indigo primary, dense enterprise layout.

```html
<link rel="stylesheet" href="../styles/pds-tokens.css" />
<link rel="stylesheet" href="../styles/pds-utilities.css" />
<button class="pds-btn pds-btn-primary">Primary Action</button>
```

## B) Angular app with real DS packages

```ts
import { PxButtonModule, PxCardModule, PxInputTextModule } from '@phenom/angular-ds';

@Component({
  standalone: true, // or NgModule imports
  imports: [PxButtonModule, PxCardModule, PxInputTextModule],
  template: `
    <px-card>
      <px-inputtext placeholder="Search"></px-inputtext>
      <px-button label="Search"></px-button>
    </px-card>
  `,
})
export class SamplePage {}
```

Verify props against Storybook docs for that component. Global theme CSS must be loaded once at app shell.

## C) React app with `@phenom/react-ds`

1. Follow React Storybook **Guides / Getting Started**.
2. Import components from `@phenom/react-ds` (names follow React Storybook titles under `Button/`, `Form/`, etc.).
3. Include theme / token CSS from the package + `@phenom/design-tokens`.
4. Wrap with required providers (`PrimeReactProvider` pattern in Storybook preview).

## D) Prompt pattern for other workspaces

Paste this at the start of a chat in a consumer workspace:

```text
Use the Phenom Design System skill and references from
/Users/venkata.gonella/phenom_repo/DesignSystem

Rules:
- Read DesignSystem/.cursor/skills/phenom-design-system/SKILL.md
- Style with DesignSystem/styles/pds-tokens.css (+ pds-utilities.css for HTML)
- Prefer px-* Angular components / @phenom/react-ds when packages are installed
- Match Storybook: https://pds.phenom.com/angular/index.html
```

## E) Figma → code

1. Align Figma layer/component names with Storybook (`px-button`, not “Primary Button”).
2. Paste Figma frame links into Cursor when MCP is connected.
3. If a control looks missing, search Storybook for alternate names before inventing UI.
