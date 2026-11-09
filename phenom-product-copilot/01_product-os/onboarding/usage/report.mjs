#!/usr/bin/env node
// Summarises this laptop's PM OS usage log (~/.copilot/usage/events.jsonl, written by log-usage.mjs).
//   node onboarding/usage/report.mjs              # readable summary, last 30 days
//   node onboarding/usage/report.mjs --days 7
//   node onboarding/usage/report.mjs --json       # used by onboarding/server.py → /api/usage
//   node onboarding/usage/report.mjs --export     # writes a shareable summary (counts only, no session ids)
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const DIR = join(homedir(), ".copilot", "usage");
const LOG = join(DIR, "events.jsonl");
const arg = (n) => {
  const i = process.argv.indexOf(n);
  return i > -1 ? process.argv[i + 1] : undefined;
};
const days = Number(arg("--days") || 30);
const since = new Date(Date.now() - days * 864e5);

function load() {
  if (!existsSync(LOG)) return [];
  return readFileSync(LOG, "utf8")
    .split("\n")
    .filter(Boolean)
    .map((l) => {
      try {
        return JSON.parse(l);
      } catch {
        return null;
      }
    })
    .filter((e) => e && e.ts && new Date(e.ts) >= since);
}

function rank(events, kind) {
  const m = new Map();
  for (const e of events.filter((x) => x.kind === kind && x.name)) {
    const r = m.get(e.name) || { name: e.name, count: 0, last: e.ts, harness: {} };
    r.count += 1;
    if (e.ts > r.last) r.last = e.ts;
    r.harness[e.harness] = (r.harness[e.harness] || 0) + 1;
    m.set(e.name, r);
  }
  return [...m.values()].sort((a, b) => b.count - a.count);
}

export function summarise(events) {
  const day = (e) => e.ts.slice(0, 10);
  const sessions = {};
  const seen = new Set();
  for (const e of events) {
    const key = `${e.harness}:${e.session || day(e)}`;
    if (!seen.has(key)) {
      seen.add(key);
      sessions[e.harness] = (sessions[e.harness] || 0) + 1;
    }
  }
  const daily = [];
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(Date.now() - i * 864e5).toISOString().slice(0, 10);
    const list = events.filter((e) => day(e) === d);
    daily.push({ date: d, events: list.length, workflows: list.filter((e) => ["skill", "agent", "command"].includes(e.kind)).length });
  }
  return {
    available: existsSync(LOG),
    days,
    users: [...new Set(events.map((e) => e.user).filter(Boolean))],
    activeDays: new Set(events.map(day)).size,
    sessions,
    prompts: events.filter((e) => e.kind === "prompt" || e.kind === "command").length,
    skills: rank(events, "skill"),
    agents: rank(events, "agent"),
    commands: rank(events, "command"),
    daily,
    first: events[0]?.ts ?? null,
    last: events.at(-1)?.ts ?? null,
  };
}

const s = summarise(load());
if (process.argv.includes("--json")) {
  process.stdout.write(JSON.stringify(s));
} else if (process.argv.includes("--export")) {
  const out = join(DIR, `summary-${(s.users[0] || "me").replace(/[^a-z0-9.@-]/gi, "_")}-${new Date().toISOString().slice(0, 10)}.json`);
  const { daily, ...rest } = s;
  writeFileSync(out, JSON.stringify({ ...rest, exportedAt: new Date().toISOString() }, null, 2));
  console.log(`Wrote ${out}`);
} else {
  const line = (r) => `  ${String(r.count).padStart(4)}  ${r.name}`;
  console.log(`PM OS usage, last ${days} days${s.users.length ? ` (${s.users.join(", ")})` : ""}`);
  console.log(`Active days: ${s.activeDays}   Sessions: ${Object.entries(s.sessions).map(([h, n]) => `${h} ${n}`).join(", ") || "none"}   Prompts: ${s.prompts}`);
  for (const [t, list] of [["Skills", s.skills], ["Agents", s.agents], ["Slash commands", s.commands]]) {
    console.log(`\n${t}`);
    console.log(list.length ? list.slice(0, 10).map(line).join("\n") : "  none yet");
  }
  if (!s.available) console.log("\nNo log yet. It starts when you open this repo in Claude Code or Cursor.");
}
