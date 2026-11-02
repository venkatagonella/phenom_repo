# How other workspaces should use this DesignSystem pack

This workspace is a **referrable PDS knowledge + style pack**. It does not replace installing `@phenom/angular-ds` for production, but it lets any Cursor workspace build PDS-aligned sample UIs.

## Option 1 — Personal skill (recommended, all projects)

The skill is installed at:

```
~/.cursor/skills/phenom-design-system/
```

It auto-applies when prompts mention PDS / Phenom DS / px-* / sample websites using Phenom UI.

In any workspace, say:

```text
Build a sample recruiting dashboard using Phenom Design System styles and components.
```

The agent should load the skill and read companion files under `~/.cursor/skills/phenom-design-system/`.

Styles still live in this repo — the personal skill points at:

```
/Users/venkata.gonella/phenom_repo/DesignSystem/styles/
```

## Option 2 — Add this folder to a multi-root workspace

In Cursor / VS Code:

1. **File → Add Folder to Workspace…**
2. Select `/Users/venkata.gonella/phenom_repo/DesignSystem`
3. Save as `*.code-workspace`

Then agents can `@`-mention files:

- `@DesignSystem/styles/pds-tokens.css`
- `@DesignSystem/.cursor/skills/phenom-design-system/SKILL.md`
- `@DesignSystem/templates/html/sample-page.html`

## Option 3 — Symlink styles into the consumer project

```bash
# from the other project root
mkdir -p styles/pds
ln -s /Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css styles/pds/pds-tokens.css
ln -s /Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-utilities.css styles/pds/pds-utilities.css
```

Import in app CSS:

```css
@import "./pds/pds-tokens.css";
@import "./pds/pds-utilities.css";
```

## Option 4 — Copy files (portable / CI-friendly)

```bash
cp /Users/venkata.gonella/phenom_repo/DesignSystem/styles/*.css ./src/styles/pds/
cp -R /Users/venkata.gonella/phenom_repo/DesignSystem/templates/html ./public/pds-samples
```

Re-copy when tokens are refreshed from Storybook.

## Option 5 — Project rule in the consumer repo

Create `.cursor/rules/phenom-ds.mdc` (or `AGENTS.md` section):

```markdown
## Phenom Design System
When building UI, follow the skill at
`/Users/venkata.gonella/phenom_repo/DesignSystem/.cursor/skills/phenom-design-system/SKILL.md`
and use tokens from
`/Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css`.
Storybook: https://pds.phenom.com/angular/index.html
```

## Option 6 — npm packages (production Phenom apps)

Do **not** rely only on this pack:

1. VPN on
2. Valid `.npmrc` → `pie-nexus.phenompro.com`
3. `npm i @phenom/angular-ds @phenom/design-tokens` (or `@phenom/react-ds`)
4. Use real `px-*` / React DS components
5. Keep this pack as the Cursor “memory bank” for naming + Storybook links

## What is referrable vs not

| Referrable from this workspace | Not included (use npm / Storybook) |
|---|---|
| Token CSS variables | Full Angular/React component runtime |
| Utility classes for HTML samples | PrimeNG/PrimeReact peer bundles |
| Component name / selector map | Private Font Awesome Pro assets |
| Usage recipes + prompt snippets | Bitbucket DS source (separate clones) |

## Refreshing tokens from Storybook

When PDS visual language updates, re-extract tokens from:

```
https://pds.phenom.com/angular/*.css
```

and replace `styles/pds-tokens.css`, then bump a note in `CHANGELOG.md` if present.
