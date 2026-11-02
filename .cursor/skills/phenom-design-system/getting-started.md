# PDS Getting Started

Canonical Storybook: [Introduction / Getting Started](https://pds.phenom.com/angular/index.html?path=/docs/introduction-getting-started--documentation)

## Packages

| Package | Publishes | Repo |
|---|---|---|
| `@phenom/angular-ds` | Angular components (`px-*`) | `phenom-ds` (Bitbucket) |
| `@phenom/react-ds` | React components | `phenom-react-ds-package` |
| `@phenom/design-tokens` | CSS / SCSS / JS tokens | `pds-design-tokens` |

Published Storybooks:

- Angular: https://pds.phenom.com/angular/index.html
- React: https://pds.phenom.com/react/index.html

## Prerequisites

1. **VPN on** — required for Nexus installs and many builds.
2. **Node 20.x**, npm 10+.
3. **`.npmrc`** in every consumer project (often gitignored in DS repos).

Sample registry config (token from SRE / platform — do not commit secrets):

```ini
registry=https://pie-nexus.phenompro.com/repository/pie-npm-group
loglevel=verbose
timeout=60000
//pie-nexus.phenompro.com/repository/:_auth="YOUR_AUTH_TOKEN"
```

Also configure Font Awesome Pro registries (`@fortawesome`, `@awesome.me`) when icons are needed.

## Angular consumer setup

```bash
# VPN connected
npm install @phenom/angular-ds @phenom/design-tokens
# peers (typical): primeng@^17.18, @fortawesome/*, etc.
npx install-peerdeps @phenom/angular-ds --no-save
```

Import global theme styles from the package (exact path may vary by version — confirm in package `exports` / Storybook Getting Started):

```ts
// styles / angular.json styles array — typical pattern
import '@phenom/design-tokens/css'; // if exported
// plus Angular DS theme / vendor CSS as documented in Storybook
```

Use components via modules:

```ts
import { PxButtonModule, PxInputTextModule } from '@phenom/angular-ds';

@NgModule({
  imports: [PxButtonModule, PxInputTextModule],
})
export class FeatureModule {}
```

```html
<px-button label="Save" styleClass="p-button-primary"></px-button>
```

Selector prefix: **`px`**. Storybook Compodoc / docs pages list inputs and outputs.

### Local Storybook (DS contributors)

```bash
cd phenom-ds
npm ci
npm run sb   # preferred — clears caches
# http://localhost:6006
```

## React consumer setup

```bash
npm install @phenom/react-ds @phenom/design-tokens
```

Wrap the app with the DS / PrimeReact providers as shown in React Storybook **Guides / Getting Started**.

Legacy package `@phenom/react-ui-components` exists in older docs — prefer `@phenom/react-ds` for current PDS work.

## Architecture notes

- Angular + React DS are **facades over PrimeNG / PrimeReact**, styled with Phenom tokens.
- Token pipeline: Figma (Tokens Studio) → `pds-design-tokens` → Style Dictionary → `dist/` → both frameworks.
- CSS layers: `primeng` → `phenomds` → `app`.
- High-impact shared areas: `styles/`, table (`px-table-v1`), snackbar service, shared directives.

## Sample websites without private npm

When VPN/registry is unavailable, build visual samples with this workspace’s referrable CSS:

- `styles/pds-tokens.css`
- `styles/pds-utilities.css`
- `templates/html/`

See `cross-workspace.md`.
