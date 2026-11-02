# Phenom Design System — Cursor reference pack

Referrable styles, skills, and component maps for building sample websites with the [Phenom Design System (PDS)](https://pds.phenom.com/angular/index.html?path=/docs/introduction-getting-started--documentation).

This repo is **not** the npm source of `@phenom/angular-ds`. It is the Cursor-facing pack you attach from other workspaces so agents reuse the same tokens, naming, and Storybook links.

## What’s inside

| Path | Purpose |
|---|---|
| `.cursor/skills/phenom-design-system/` | Agent skill + progressive references |
| `.cursor/rules/phenom-design-system.mdc` | Always-on rule when this workspace is open |
| `styles/pds-tokens.css` | **Referrable** CSS custom properties (from published Storybook) |
| `styles/pds-utilities.css` | HTML utility classes for static samples |
| `templates/html/` | Sample pages (Jobs dashboard, Job Fields, sample) |
| `templates/angular/`, `templates/react/` | Package install / usage notes |
| `references/` | Catalog JSON + selector list |
| `AGENTS.md` | Agent entrypoint for this workspace |

## Official PDS links

- Angular Storybook: https://pds.phenom.com/angular/index.html
- React Storybook: https://pds.phenom.com/react/index.html
- Packages (private Nexus, VPN + `.npmrc`): `@phenom/angular-ds`, `@phenom/react-ds`, `@phenom/design-tokens`

## How to refer this workspace from another workspace

### 1) Personal skill (best for all projects)

Already mirrored to:

```text
~/.cursor/skills/phenom-design-system/
```

In any project chat:

```text
Build a sample site using Phenom Design System.
Use tokens from /Users/venkata.gonella/phenom_repo/DesignSystem/styles/
```

### 2) Multi-root workspace

**File → Add Folder to Workspace…** → select this `DesignSystem` folder. Then `@`-mention:

```text
@DesignSystem/styles/pds-tokens.css
@DesignSystem/.cursor/skills/phenom-design-system/SKILL.md
```

### 3) Symlink or copy styles into the consumer app

```bash
mkdir -p styles/pds
ln -s /Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css styles/pds/pds-tokens.css
ln -s /Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-utilities.css styles/pds/pds-utilities.css
```

```css
@import "./pds/pds-tokens.css";
@import "./pds/pds-utilities.css";
```

### 4) Drop a consumer rule

In the other repo, add `.cursor/rules/use-phenom-ds.mdc`:

```markdown
---
description: Phenom Design System references
alwaysApply: true
---

UI work must follow:
/Users/venkata.gonella/phenom_repo/DesignSystem/.cursor/skills/phenom-design-system/SKILL.md

Import styles from:
/Users/venkata.gonella/phenom_repo/DesignSystem/styles/pds-tokens.css
```

### 5) Production Phenom apps

Use private packages (VPN + `.npmrc`), not only this CSS pack:

```bash
npm install @phenom/angular-ds @phenom/design-tokens
# or
npm install @phenom/react-ds @phenom/design-tokens
```

Keep using this pack as the naming / Storybook “memory bank” for Cursor.

Full options: `.cursor/skills/phenom-design-system/cross-workspace.md`

## Quick preview

Open in a browser:

```text
templates/html/sample-page.html
templates/html/jobs-dashboard.html
templates/html/job-fields-settings.html
```

## Local host (Jobs dashboard)

From the repo root, start a static server (no private npm packages required):

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/templates/html/jobs-dashboard.html
```

The Jobs sample uses an expandable left nav modeled on PDS Storybook
[SidebarNavigation — Expanded](https://pds.phenom.com/angular/index.html?path=/story/navigation-sidebarnavigation--expanded).
Use the « / » control to collapse (icons only) and expand (icons + labels).

## Refreshing tokens

Tokens in `styles/pds-tokens.css` were extracted from published Angular Storybook CSS on pds.phenom.com. Re-extract when the design system visual baseline changes.
