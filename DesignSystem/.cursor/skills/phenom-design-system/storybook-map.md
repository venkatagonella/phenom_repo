# Storybook Map

## Angular — https://pds.phenom.com/angular/index.html

Top-level sections (sidebar order):

1. **Introduction** — Getting Started, Design Tokens, Fonts, Theming, Layering, Changelog, For Contributors
2. **Foundations** — Border Radius, Color Palette, Shadows, Typography, Width Presets, Icons
3. **Form Controls** — InputField, Dropdown, MultiSelect, Checkbox, Radio*, DatePicker, Search, …
4. **Actions** — Button, IconButton, TextButton, SplitButton, SwitchButton, LinkText
5. **Navigation** — Breadcrumb, SidebarNavigation, Tab, ViewSelector
6. **Menus** — Menu, TieredMenu, WizardStepper
7. **Containers** — Card, Accordion, Divider
8. **Overlays** — Modal, ConfirmModal, Sidebar, Popover, Blanket, Tooltip
9. **Data Display** — Table/v1 (+ cell types), Pagination
10. **Feedback** — Snackbar, SystemMessage, Progress*, Skeleton, Status
11. **Identity** — Avatar, AvatarGroup
12. **Indicators & Labels** — Tag, Badge, CategoryChip, NotificationBadge
13. **Phenom Specific** — FitScore, TalentSignal
14. **Layout** — Grid
15. **Miscellaneous / Shared / In Dev / How to Contribute**

Manifest JSON (machine-readable catalog):

```
https://pds.phenom.com/angular/index.json
```

Docs URL pattern:

```
https://pds.phenom.com/angular/index.html?path=/docs/<id>
```

Story URL pattern:

```
https://pds.phenom.com/angular/index.html?path=/story/<id>
```

## React — https://pds.phenom.com/react/index.html

Start at **Guides / Getting Started**. Sections include Button/*, Form/*, Data Display/Table, Navigation/*, Overlay/*, Misc/*, Menu/*.

Manifest:

```
https://pds.phenom.com/react/index.json
```

## When prompting Cursor

Include the exact Storybook docs link for the component you want, e.g.:

```text
Implement the header actions using PDS Button as documented at
https://pds.phenom.com/angular/index.html?path=/docs/actions-button--documentation
Use px-button / PxButtonModule — do not invent a custom button.
```
