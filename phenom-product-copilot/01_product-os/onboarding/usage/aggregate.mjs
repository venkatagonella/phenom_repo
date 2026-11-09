#!/usr/bin/env node
// Team view of PM OS usage: folds many PMs' usage logs into one summary for the PM OS "Team usage" page.
// Input: one events.jsonl per PM (written by log-usage.mjs). Output: counts per team, week and item.
// No email, session id or prompt reaches the output.
//
//   node onboarding/usage/aggregate.mjs --in <dir-of-jsonl> --teams <teams.json> --out <team-usage.json>
//
// teams.json maps a PM's work email to a team name: { "pm@phenom.com": "Recruiter Experience (RX)" }.
// Unmapped PMs count under "Unassigned".
import { readFileSync, readdirSync, writeFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const WORKFLOW = new Set(["skill", "agent", "command"]);
const DAY = 864e5;

/** Monday (UTC) of the week an ISO timestamp falls in, as YYYY-MM-DD. */
export function weekOf(ts) {
  const d = new Date(ts);
  const back = (d.getUTCDay() + 6) % 7;
  return new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - back)).toISOString().slice(0, 10);
}

/**
 * events: [{ts, kind, name, user, harness}], teams: {email: team}, ownerEmails: {email: handle}
 * Returns the summary the Team usage page reads.
 */
export function aggregate(events, { teams = {}, ownerEmails = {}, now = new Date(), weeks = 12 } = {}) {
  const thisWeek = weekOf(now.toISOString());
  const weekList = [];
  for (let i = weeks - 1; i >= 0; i--) weekList.push(weekOf(new Date(Date.parse(thisWeek) - i * 7 * DAY).toISOString()));
  const from = Date.parse(weekList[0]);
  const d30 = now.getTime() - 30 * DAY;
  const d60 = now.getTime() - 60 * DAY;
  const teamOf = (u) => teams[u] ?? "Unassigned";

  const all = new Set();
  const teamPms = new Map(); // team -> Set(user)
  const active30 = new Set();
  const weekly = new Map(weekList.map((w) => [w, { week: w, pms: new Set(), runs: 0 }]));
  const items = new Map();

  for (const e of events) {
    if (!e.user || !e.ts) continue;
    const t = Date.parse(e.ts);
    all.add(e.user);
    const team = teamOf(e.user);
    if (!teamPms.has(team)) teamPms.set(team, new Set());
    teamPms.get(team).add(e.user);
    if (!WORKFLOW.has(e.kind) || !e.name) continue;
    if (t >= d30) active30.add(e.user);
    const w = weekly.get(weekOf(e.ts));
    if (w && t >= from) {
      w.pms.add(e.user);
      w.runs += 1;
    }
    const key = `${e.kind}:${e.name}`;
    let it = items.get(key);
    if (!it) {
      it = { kind: e.kind, name: e.name, runs30: 0, pms30: new Set(), pms60: new Set(), teams30: new Map(), weekly: new Map(weekList.map((x) => [x, 0])), last: e.ts };
      items.set(key, it);
    }
    if (e.ts > it.last) it.last = e.ts;
    if (t >= d60) it.pms60.add(e.user);
    if (t >= d30) {
      it.runs30 += 1;
      it.pms30.add(e.user);
      if (!it.teams30.has(team)) it.teams30.set(team, new Set());
      it.teams30.get(team).add(e.user);
    }
    const wk = weekOf(e.ts);
    if (it.weekly.has(wk)) it.weekly.set(wk, it.weekly.get(wk) + 1);
  }

  const owners = new Set(Object.keys(ownerEmails));
  return {
    generated: now.toISOString().slice(0, 10),
    weeks: weekList,
    totals: { roster: Math.max(Object.keys(teams).length, all.size), pms: all.size, active30: active30.size, active7: weekly.get(thisWeek)?.pms.size ?? 0, runs30: [...items.values()].reduce((n, i) => n + i.runs30, 0) },
    weekly: [...weekly.values()].map((w) => ({ week: w.week, activePms: w.pms.size, runs: w.runs })),
    teams: [...new Set([...Object.values(teams), ...teamPms.keys()])]
      .map((name) => {
        const seen = teamPms.get(name) ?? new Set();
        const roster = Object.values(teams).filter((t) => t === name).length;
        return { name, roster: Math.max(roster, seen.size), setUp: seen.size, active30: [...seen].filter((u) => active30.has(u)).length };
      })
      .sort((a, b) => b.roster - a.roster),
    items: [...items.values()]
      .map((i) => ({
        kind: i.kind,
        name: i.name,
        runs30: i.runs30,
        pms30: i.pms30.size,
        pms60: i.pms60.size,
        ownerUsed30: [...i.pms30].some((u) => owners.has(u)),
        teams30: Object.fromEntries([...i.teams30.entries()].map(([t, s]) => [t, s.size])),
        weekly: [...i.weekly.values()],
        last: i.last.slice(0, 10),
      }))
      .sort((a, b) => b.runs30 - a.runs30),
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const arg = (n) => {
    const i = process.argv.indexOf(n);
    return i > -1 ? process.argv[i + 1] : undefined;
  };
  const dir = arg("--in");
  if (!dir) {
    console.error("usage: aggregate.mjs --in <dir-of-jsonl> [--teams teams.json] [--out team-usage.json]");
    process.exit(2);
  }
  const events = readdirSync(dir)
    .filter((f) => f.endsWith(".jsonl"))
    .flatMap((f) =>
      readFileSync(join(dir, f), "utf8")
        .split("\n")
        .filter(Boolean)
        .map((l) => {
          try {
            return JSON.parse(l);
          } catch {
            return null;
          }
        })
        .filter(Boolean),
    );
  const teams = arg("--teams") && existsSync(arg("--teams")) ? JSON.parse(readFileSync(arg("--teams"), "utf8")) : {};
  const people = JSON.parse(readFileSync(new URL("../people.json", import.meta.url), "utf8")).people;
  const ownerEmails = Object.fromEntries(Object.entries(people).filter(([, p]) => p.email).map(([h, p]) => [p.email, h]));
  const result = { sample: false, ...aggregate(events, { teams, ownerEmails }) };
  const out = arg("--out") ?? "team-usage.json";
  writeFileSync(out, JSON.stringify(result, null, 2));
  console.log(`${out}: ${result.totals.pms} PMs, ${result.totals.active30} active in 30 days, ${result.items.length} items`);
}
