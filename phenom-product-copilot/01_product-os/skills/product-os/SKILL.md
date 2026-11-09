---
name: 01_product-os
description: "Open Product OS: start Product OS Local on this laptop (setup checks, your usage, commands to copy) and give the link to Product OS Hosted (setup journey, skill catalog, what's new, team usage). Also checks that every shared tool (Jira, Figma, Slack, Glean, design system, Snowflake, Google) is signed in. Use for /01_product-os, \"open product os\", \"show my setup\", \"check connections\", \"are my tools connected\", \"where is the catalog\", or when a PM asks how to get started."
metadata:
  owner: officiallybasti
  status: beta
  try: "/01_product-os"
---

# Open Product OS

Product OS has two pages. Open the right one and say in one line which is which.

| | Product OS Local | Product OS Hosted |
|---|---|---|
| Where | `http://127.0.0.1:8787`, served from this repo | The shared page (productos.phenom.pro once live) |
| Shows | Setup checks for this laptop, your own usage, commands to copy | Setup journey, skill catalog, what's new, team usage, how it works |
| Seen by | Only this PM | Every PM, the same page |

## Run

From the repo root:

```bash
./01_product-os/onboarding/open.sh
```

It starts Product OS Local if it isn't running and opens it in the browser. Product OS Local has an "Open Product OS Hosted" button in its top bar.

## Then say

- The Local address, and that it must keep running for the Hosted page to tick off setup steps.
- The Hosted link from the button (or `PRODUCT_OS_HOSTED_URL` if set).
- If the script fails: Node or Python missing, or port 8787 taken. Show the last lines of the log it names.

Never start other servers, and never change files from this skill.

Then offer the connection check below.

## Check connections

For `/01_product-os check connections` (or "are my tools connected?"). Product OS Local can see that a tool is set up, not that the PM signed in, so ask each tool who the PM is. One identity call per tool, no catalog dumps (`policies/mcp-connectivity.md`):

| Tool | Call | Where it comes from |
|---|---|---|
| Jira + Confluence | `atlassianUserInfo` | Claude Code: Atlassian plugin. Cursor: `.cursor/mcp.json` |
| Figma | `whoami` | Claude Code: Figma plugin. Cursor: `.cursor/mcp.json` |
| Slack | read the PM's own profile (`slack_read_user_profile` or equivalent) | Claude Code: Slack plugin. Cursor: `.cursor/mcp.json` |
| Glean | `search` for the PM's name, 1 result | `glean_default` in both files |
| Design system | `list_components` on the React and the Angular server | React: `setup-design-system.sh`. Angular: `phenom-ds-storybook` in both files |
| Snowflake | `execute_snowflake_query` with `SELECT CURRENT_USER()` | copilot server |
| Help center | `search_kb` with any short query | copilot server |
| Google | Claude Code: `list_recent_files` (Drive connector). Cursor: `list_calendars` | Claude Code: claude.ai connectors. Cursor: copilot server |

Report one table: tool, connected / sign in needed / not set up, and the fix:

- **Sign in needed:** Claude Code → `/mcp`, pick the tool, Authenticate. Cursor → Settings → MCP, Connect.
- **Not set up:** Claude Code asks to approve the repo's tools and install its plugins the first time the folder opens. If that was declined, approve them in `/mcp` and install with `/plugin install <name>@claude-plugins-official`. Google in Claude Code: claude.ai → Settings → Connectors. React design system: `bash 01_product-os/onboarding/setup-design-system.sh`. Snowflake or help center: `cd 01_product-os/mcp && npm run setup`.
- **Listed twice** (same tool from a plugin and a manual entry, e.g. two Slack servers): tell the PM which one to remove. The repo's copy stays.

Optional tools (Miro, Granola) are not checked unless the PM asks.
