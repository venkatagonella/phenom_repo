# React consumer snippet

Prefer current PDS package **`@phenom/react-ds`** (Storybook: https://pds.phenom.com/react/index.html).

```bash
# VPN on + .npmrc present
npm install @phenom/react-ds @phenom/design-tokens
```

Follow **Guides / Getting Started** in React Storybook for providers and global theme imports.

```tsx
// Example shape — verify exact export names in Storybook / package exports
import { Button } from '@phenom/react-ds';

export function Sample() {
  return <Button /* props per Storybook */>Primary Action</Button>;
}
```

Legacy docs may mention `@phenom/react-ui-components` — do not use that for new PDS-aligned work unless a product already depends on it.
