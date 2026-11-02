# Angular consumer snippet

```bash
# VPN on + .npmrc present
npm install @phenom/angular-ds @phenom/design-tokens
npx install-peerdeps @phenom/angular-ds --no-save
```

```ts
import { Component } from '@angular/core';
import { PxButtonModule, PxInputTextModule, PxCardModule } from '@phenom/angular-ds';

@Component({
  selector: 'app-pds-sample',
  standalone: true,
  imports: [PxButtonModule, PxInputTextModule, PxCardModule],
  template: `
    <px-card>
      <px-inputtext placeholder="Search"></px-inputtext>
      <px-button label="Search"></px-button>
    </px-card>
  `,
})
export class PdsSampleComponent {}
```

Confirm inputs/outputs in Storybook:

https://pds.phenom.com/angular/index.html?path=/docs/actions-button--documentation

For Cursor styling hints while packages are unavailable, still import referrable tokens from this workspace’s `styles/pds-tokens.css` into global styles.
