#!/usr/bin/env node
// PM OS usage logger. Called by Claude Code hooks (.claude/settings.json) and Cursor hooks (.cursor/hooks.json).
// Writes ONE metadata line per event to ~/.copilot/usage/events.jsonl on this laptop:
//   when, which tool (Claude Code or Cursor), who (git or Cursor email), and the NAME of the skill,
//   agent or slash command. Never prompt text, arguments, file contents, transcripts or tool output.
// Never prints to stdout (Claude Code would add it to the conversation) and never fails the hook.
// Opt out: set PMOS_USAGE=off, or create ~/.copilot/usage/OPT_OUT.
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { basename, join } from "node:path";
import { execFileSync } from "node:child_process";

const DIR = join(homedir(), ".copilot", "usage");
const LOG = join(DIR, "events.jsonl");

function readStdin() {
  try {
    return JSON.parse(readFileSync(0, "utf8") || "{}");
  } catch {
    return {};
  }
}

/** Work email for Claude Code events: PMOS_USER_EMAIL, else the signed-in Claude account, else git. Cached for a week. */
function workEmail(cwd) {
  if (process.env.PMOS_USER_EMAIL) return process.env.PMOS_USER_EMAIL;
  const cache = join(DIR, "identity.json");
  try {
    const c = JSON.parse(readFileSync(cache, "utf8"));
    if (c.email && Date.now() - c.at < 7 * 864e5) return c.email;
  } catch {}
  let email = null;
  try {
    // Only the email field is read from Claude Code's account file.
    email = JSON.parse(readFileSync(join(homedir(), ".claude.json"), "utf8"))?.oauthAccount?.emailAddress || null;
  } catch {}
  if (!email) {
    try {
      email = execFileSync("git", ["config", "user.email"], { cwd: cwd || process.cwd(), timeout: 1000, encoding: "utf8" }).trim() || null;
    } catch {}
  }
  try {
    mkdirSync(DIR, { recursive: true });
    writeFileSync(cache, JSON.stringify({ email, at: Date.now() }));
  } catch {}
  return email;
}

/** Leading "/name" of a prompt, without anything after it. */
function slashCommand(prompt) {
  const m = typeof prompt === "string" ? prompt.trim().match(/^\/([A-Za-z0-9:._-]+)/) : null;
  return m ? m[1] : null;
}

/** Skill name when an agent opens a SKILL.md (how Cursor loads skills). */
function skillFromPath(p) {
  const m = typeof p === "string" ? p.match(/skills\/([^/]+)\/SKILL\.md$/) : null;
  return m ? m[1] : null;
}

function classify(harness, d) {
  const ev = d.hook_event_name || "";
  const tool = d.tool_name || "";
  const input = d.tool_input || {};
  if (/^session_?start$/i.test(ev)) return { kind: "session", name: d.source || d.composer_mode || null };
  if (ev === "UserPromptSubmit" || ev === "beforeSubmitPrompt") {
    const cmd = slashCommand(d.prompt);
    return cmd ? { kind: "command", name: cmd } : { kind: "prompt", name: null };
  }
  if (ev === "subagentStart") return { kind: "agent", name: d.subagent_type || null };
  if (/^(Pre|Post)ToolUse$/i.test(ev) || /^(pre|post)ToolUse$/.test(ev)) {
    if (tool === "Skill") return { kind: "skill", name: input.skill || input.name || input.command || null };
    if (tool === "Agent" || tool === "Task") return { kind: "agent", name: input.subagent_type || "general-purpose" };
    const fromPath = skillFromPath(input.file_path || input.path || input.target_file);
    if (fromPath) return { kind: "skill", name: fromPath };
  }
  return null;
}

try {
  if (process.env.PMOS_USAGE === "off" || existsSync(join(DIR, "OPT_OUT"))) process.exit(0);
  const hint = process.argv[2] || "unknown";
  const d = readStdin();
  // Cursor can also run Claude Code project hooks; let Cursor's own hooks.json log those sessions.
  if (hint === "claude-code" && d.cursor_version) process.exit(0);
  const harness = d.cursor_version ? "cursor" : hint;
  const c = classify(harness, d);
  if (!c) process.exit(0);
  mkdirSync(DIR, { recursive: true });
  const root = (Array.isArray(d.workspace_roots) && d.workspace_roots[0]) || d.cwd || process.cwd();
  const line = {
    ts: new Date().toISOString(),
    harness,
    kind: c.kind,
    name: c.name,
    user: d.user_email || workEmail(d.cwd),
    session: d.session_id || d.conversation_id || null,
    workspace: basename(root),
    v: 1,
  };
  appendFileSync(LOG, JSON.stringify(line) + "\n");
} catch {
  /* logging must never break the user's session */
}
process.exit(0);
