# PDS Component Catalog (Angular)

Storybook sidebar is authoritative. Selector prefix: **`px`**. Modules: **`Px*Module`** from `@phenom/angular-ds`.

Full machine-readable list: `../../../references/component-catalog.json`  
Selectors: `../../../references/angular-selectors.txt`

## Quick map (Storybook title → selector)

### Actions
| Storybook | Selector | Module |
|---|---|---|
| Actions/Button | `px-button` | `PxButtonModule` |
| Actions/IconButton | `px-iconbutton` | `PxIconButtonModule` |
| Actions/TextButton | `px-textbutton` | `PxTextButtonModule` |
| Actions/SplitButton | `px-splitbutton` | `PxSplitButtonModule` |
| Actions/SwitchButton | `px-switchbutton` | `PxSwitchButtonModule` |
| Actions/LinkText | `px-link-text` | `PxLinkTextModule` |

### Form controls
| Storybook | Selector | Module |
|---|---|---|
| InputField | `px-inputtext` | `PxInputTextModule` |
| InputNumber | `px-inputnumber` | `PxInputNumberModule` |
| TextArea | `px-textarea` | — (check package export) |
| Dropdown | `px-dropdown` | `PxDropdownModule` |
| MultiSelect | `px-multiselect` | `PxMultiselectModule` |
| AutoComplete | `px-autocomplete` | `PxAutocompleteModule` |
| Checkbox | `px-checkbox` | `PxCheckBoxModule` |
| RadioButton | `px-radiobutton` | `PxRadioButtonModule` |
| RadioGroup | `px-radio-group` | `PxRadioGroupModule` |
| RadioPanels | `px-radio-panels` | `PxRadioPanelsModule` |
| Switch | `px-switch` | `PxSwitchModule` |
| DatePicker | `px-calendar` | `PxCalendarModule` |
| ColorPicker | `px-color-picker` | `PxColorPickerModule` |
| Search | `px-search-input` | `PxSearchInputModule` |
| SearchWithCategory | `px-search-with-category` | `PxSearchWithCategoryModule` |
| Label | `px-label` | `PxLabelModule` |
| Helper | `px-helper` | `PxHelperModule` |
| Rating | `px-rating` | `PxRatingModule` |
| Slider | `px-slider` | `PxSliderModule` |
| File Upload | `px-fileupload` | `PxFileUploadModule` |
| RichTextEditor | `px-texteditor` | — |

### Containers / layout
| Storybook | Selector |
|---|---|
| Card | `px-card` |
| Accordion | `px-accordion` / `px-accordion-tab` |
| Divider | `px-divider` |
| Grid | `px-grid` |

### Navigation / menus
| Storybook | Selector |
|---|---|
| Breadcrumb | `px-breadcrumb` |
| SidebarNavigation | `px-sidebar-navigation` |
| Tab | `px-tabmenu` |
| ViewSelector | `px-view` / `px-viewgroup` |
| Menu / TieredMenu | `px-menu` / `px-tieredmenu` |
| WizardStepper | `px-wizard-stepper` |

### Overlays / feedback
| Storybook | Selector |
|---|---|
| Modal | `px-modal` |
| ConfirmModal | `px-confirm-dialog` |
| Sidebar | `px-sidebar` |
| Popover | `px-popover` |
| Blanket | `px-blanket` |
| Snackbar | `px-snackbar` |
| SystemMessage | `px-system-messages` |
| ProgressBar / Spinner / Skeleton | `px-progress-bar` / `px-spinner` / `px-skeleton` |
| Status | `px-status` |

### Data display
| Storybook | Selector |
|---|---|
| Table/v1 | `px-table-v1` (+ many `px-table-v1-cell-*`) |
| Pagination | `px-paginator` |

### Identity / indicators / Phenom-specific
| Storybook | Selector |
|---|---|
| Avatar / AvatarGroup | `px-avatar` / `px-avatar-group` |
| Tag / NumberBadge / NotificationBadge | `px-tag` / `px-badge` / `px-notification-badge` |
| CategoryChip | `px-categorychip` |
| FitScore | `px-fitscore` |
| TalentSignal | `px-talent-signal` |

## Storybook deep link pattern

```
https://pds.phenom.com/angular/index.html?path=/docs/<story-id>
```

Examples:

- Button docs: `...?path=/docs/actions-button--documentation`
- InputField docs: `...?path=/docs/form-controls-inputfield--documentation`
- Design tokens: `...?path=/docs/introduction-design-tokens--documentation`

## Usage discipline

1. Prefer DS public API props — do not pierce into PrimeNG DOM.
2. Visual overrides → DS theme extensions / token variables, not ad-hoc hex colors.
3. Treat `px-table-v1`, form controls, sidebar, modal, snackbar as high-blast-radius.
4. `IN_DEV/*` Storybook entries may be unstable — avoid in production samples unless requested.
