# Structure Steering — How the codebase is organized

> **Layer 1 / living context.** Keep this current; the agent uses it to place new files
> correctly and to find existing code during Phase-0 discovery. Drafted by `/ns-steer`.

## Directory layout

```
.cursor/
├── rules/phenom-design-system.mdc    # always-on PDS rule
└── skills/phenom-design-system/      # skill + progressive refs
styles/
├── pds-tokens.css                    # portable design tokens
├── pds-utilities.css                 # HTML sample utilities
├── job-fields-settings.css           # page-specific CRM Job Fields styles
└── jobs-dashboard.css                # Jobs sample + expandable SidebarNavigation
templates/
├── html/                             # static sample pages
│   ├── sample-page.html
│   ├── jobs-dashboard.html           # CRM Jobs sample + expandable LHN
│   └── job-fields-settings.html      # settings shell + fixed left nav
├── angular/USAGE.md
└── react/USAGE.md
references/                           # catalog + consumer rule snippet
northstar/
├── steering/                         # living context (this folder)
└── specs/                            # increment specs (INDEX + NNN-slug/)
README.md
AGENTS.md
```

## Module boundary rules

- **Tokens/utilities** (`styles/pds-*.css`) stay portable; page-specific CSS stays in its own file beside the page concern.
- **Skills/rules** teach agents; they do not replace Storybook as the component source of truth.
- **HTML templates** may approximate `px-*` components with markup + CSS; production consumers use official packages.
- **Northstar** owns requirements and living context only under `northstar/`; do not add parallel `docs/specs` trees for SDD.

## Where things go

- **New static CRM-like sample page:** `templates/html/<page>.html` + `styles/<page>.css` (or shared styles if truly reusable).
- **New PDS guidance for agents:** extend `.cursor/skills/phenom-design-system/` (and keep personal skill mirror in sync if still used).
- **New catalog entries:** `references/component-catalog.json` / selector lists.
- **New feature/bug/refactor work:** `northstar/specs/<NNN-slug>/` with INDEX update; no code until the flow’s approval gate allows it.
- **Left-hand navigation patterns:**
  - **Fixed settings nav:** `templates/html/job-fields-settings.html` (`.setting-menu`) — unchanged.
  - **Expandable PDS SidebarNavigation (sample):** `templates/html/jobs-dashboard.html` + `styles/jobs-dashboard.css` — collapse/expand control; icons+labels expanded, icons-only collapsed (Storybook `navigation-sidebarnavigation--expanded`).
