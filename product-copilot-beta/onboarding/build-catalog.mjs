// Builds the Product OS catalog (skills, policies, agents) and the "what's new" changelog
// from this repo. The PM OS site reads the JSON it writes, and onboarding/server.py serves it to the
// local dashboard (falling back to parsing skills/ when the file is missing).
// Nobody edits those JSON files by hand: change a skill, re-run this, and the site updates.
//
//   node onboarding/build-catalog.mjs                         # writes onboarding/data/
//   node onboarding/build-catalog.mjs --out <dir>             # write somewhere else (the site build)
//   node onboarding/build-catalog.mjs --extra <workspace-dir> # also list that workspace's .claude/
//                                                             # workflows as "not shared yet"
import { readFileSync, readdirSync, statSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { join, basename, dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const arg = (name) => {
  const i = process.argv.indexOf(name);
  return i > -1 ? process.argv[i + 1] : undefined;
};
const shared = resolve(here, "..");
const workspace = arg("--extra") ? resolve(arg("--extra")) : null;
const out = resolve(arg("--out") ?? join(here, "data"));
mkdirSync(out, { recursive: true });

let tracked = new Set();
try {
  tracked = new Set(execFileSync("git", ["-C", shared, "ls-files"], { encoding: "utf8" }).split("\n"));
} catch {
  /* not a git checkout: everything counts as merged */
}

// Workspace items that are personal automations, duplicates of a shared skill, or customer-specific.
const WORKSPACE_DENY = new Set(["eod-digest", "phenom-designer", "sr-triage"]);
// Deprecated pointers stay out of the catalog.
const SHARED_DENY = new Set(["rx-sr-triage-rubric", "granola-sync"]);

const ACRONYMS = { prd: "PRD", jira: "Jira", sr: "SR", kb: "KB", ptg: "PTG", rx: "RX", wbr: "WBR", mcp: "MCP", api: "API", ai: "AI", fire: "FIRE", ds: "DS", llm: "LLM", ui: "UI" };
// Display names keyed by "kind:slug" first, then by slug.
const DISPLAY = {
  "command:ptg-diagnose": "Path-to-Green diagnosis",
  "skill:ptg-hypercell": "Path-to-Green hypercell deep dive",
  "agent:ptg-hypercell": "PTG: Hypercell analyst",
  "path-to-green": "Path-to-Green rules",
  "ptg-promise": "PTG: Promise analyst",
  "ptg-delivery": "PTG: Delivery analyst",
  "ptg-need-now": "PTG: Need Now analyst",
  "ptg-hypercell-scout": "PTG: Hypercell scout",
  "ptg-org-chart": "PTG: Org chart analyst",
  "comptetitor-research": "Competitor research",
  "jira": "Jira constants",
  "jira-constants": "Jira constants",
  "phenom-ds-figma": "Phenom DS for Figma",
  "update-product-os": "Update Product OS",
};

function prettify(slug, kind) {
  if (kind && DISPLAY[`${kind}:${slug}`]) return DISPLAY[`${kind}:${slug}`];
  if (DISPLAY[slug]) return DISPLAY[slug];
  const words = slug.split(/[-_ ]+/).map((w) => ACRONYMS[w.toLowerCase()] ?? w.toLowerCase());
  const first = words[0];
  words[0] = ACRONYMS[first.toLowerCase()] ? first : first.charAt(0).toUpperCase() + first.slice(1);
  return words.join(" ");
}

/** Minimal front-matter reader: scalars, [inline, lists], "- item" lists, and > / | blocks. */
function frontMatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0].trim() !== "---") return {};
  const fm = {};
  let key = null;
  let mode = null; // "block" | "list"
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === "---") break;
    const m = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (m && !line.startsWith(" ")) {
      key = m[1];
      const v = m[2].trim();
      if (v === "" ) { fm[key] = ""; mode = "list-or-block"; continue; }
      if (/^[>|][-+]?$/.test(v)) { fm[key] = ""; mode = "block"; continue; }
      if (v.startsWith("[") && v.endsWith("]")) {
        fm[key] = v.slice(1, -1).split(",").map((s) => s.trim().replace(/^["']|["']$/g, "")).filter(Boolean);
      } else {
        fm[key] = v.replace(/^["']|["']$/g, "");
      }
      mode = null;
      continue;
    }
    if (!key) continue;
    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && (mode === "list-or-block" || mode === "list")) {
      if (!Array.isArray(fm[key])) fm[key] = [];
      fm[key].push(item[1].trim().replace(/^["']|["']$/g, ""));
      mode = "list";
      continue;
    }
    if ((mode === "block" || mode === "list-or-block") && line.trim()) {
      fm[key] = (fm[key] ? fm[key] + " " : "") + line.trim();
      mode = "block";
    }
  }
  return fm;
}

function clean(desc = "") {
  return desc
    .replace(/\s+/g, " ")
    .replace(/Usage:\s*\/\S+(\s+\S+)*$/i, "") // drop usage examples (they name customer accounts)
    .replace(/\bmars\b/gi, "<account>")
    .trim();
}

function firstSentence(desc) {
  const s = desc.match(/^(.+?[.!?])(\s|$)/);
  const one = s ? s[1] : desc;
  return one.length > 170 ? one.slice(0, 167).replace(/\s+\S*$/, "") + "…" : one;
}

function gitDate(repo, path, mode) {
  try {
    const args = ["-C", repo, "log", "--date=short", "--format=%ad", "--follow"];
    if (mode === "added") args.push("--diff-filter=A");
    else args.push("-1");
    args.push("--", path);
    const outp = execFileSync("git", args, { encoding: "utf8" }).trim().split("\n").filter(Boolean);
    return mode === "added" ? outp.at(-1) ?? null : outp[0] ?? null;
  } catch {
    return null;
  }
}

function mtime(p) {
  return statSync(p).mtime.toISOString().slice(0, 10);
}

function listFiles(dir, ext) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter((f) => f.endsWith(ext)).map((f) => join(dir, f));
}

function listSkillFolders(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .map((d) => join(dir, d, "SKILL.md"))
    .filter((p) => existsSync(p));
}

const items = [];

function add({ file, kind, source, slugFromFolder = false, command = false }) {
  const text = readFileSync(file, "utf8");
  const fm = frontMatter(text);
  const slug = slugFromFolder ? basename(dirname(file)) : basename(file).replace(/\.(md|mdc|yaml)$/, "");
  if (source === "shared" && SHARED_DENY.has(slug)) return;
  if (source === "workspace" && WORKSPACE_DENY.has(slug)) return;
  const description = clean(fm.description ?? "");
  if (!description) return;
  const rel = relative(source === "shared" ? shared : workspace, file);
  const triggers = Array.isArray(fm.triggers) ? fm.triggers.slice(0, 12) : [];
  const requires = Array.isArray(fm.requires) ? fm.requires : [];
  const always = fm.always === "true" || fm.alwaysApply === "true";
  const isDeprecated = /deprecated/i.test(description);
  if (isDeprecated) return;
  items.push({
    id: `${kind}:${slug}`,
    slug,
    name: prettify(fm.name && /^[a-z0-9-]+$/.test(fm.name) ? fm.name : slug, kind),
    merged: source === "shared" ? tracked.size === 0 || tracked.has(rel) : false,
    kind,
    command: command ? `/${slug}` : null,
    summary: firstSentence(description),
    description,
    triggers,
    requires,
    always,
    path: rel,
    source,
    updated: source === "shared" ? gitDate(shared, rel) ?? mtime(file) : mtime(file),
    added: source === "shared" ? gitDate(shared, rel, "added") : null,
  });
}

// Shared repo: the Product OS
for (const f of [...listFiles(join(shared, "skills"), ".md"), ...listFiles(join(shared, "skills"), ".mdc")]) add({ file: f, kind: "skill", source: "shared" });
for (const f of listSkillFolders(join(shared, "skills"))) add({ file: f, kind: "skill", source: "shared", slugFromFolder: true, command: true });
for (const f of listFiles(join(shared, "policies"), ".md")) add({ file: f, kind: "policy", source: "shared" });
for (const f of listFiles(join(shared, "agents"), ".yaml")) add({ file: f, kind: "agent", source: "shared" });

// Optional: a maintainer's workspace workflows that are shareable but not promoted yet
if (workspace) {
  const ws = join(workspace, ".claude");
  for (const f of listSkillFolders(join(ws, "skills"))) add({ file: f, kind: "skill", source: "workspace", slugFromFolder: true, command: true });
  for (const f of listFiles(join(ws, "commands"), ".md")) add({ file: f, kind: "command", source: "workspace", command: true });
  for (const f of listFiles(join(ws, "agents"), ".md")) add({ file: f, kind: "agent", source: "workspace" });
  for (const f of listFiles(join(ws, "agents", "path-to-green-analysis"), ".md")) add({ file: f, kind: "agent", source: "workspace" });
}

items.sort((a, b) => (a.source === b.source ? a.name.localeCompare(b.name) : a.source === "shared" ? -1 : 1));

// Changelog: non-merge commits on the shared repo, newest first
const SECTION = [
  [/^skills\/([^/]+)\/SKILL\.md$/, "skill"],
  [/^skills\/([^/]+)\.mdc?$/, "skill"],
  [/^policies\/([^/]+)\.md$/, "policy"],
  [/^agents\/([^/]+)\.yaml$/, "agent"],
  [/^knowledge\/([^/]+)\//, "knowledge"],
  [/^engineering\/index\//, "engineering"],
  [/^onboarding\//, "onboarding"],
];
const log = execFileSync("git", ["-C", shared, "log", "--no-merges", "--date=short", "--format=@@%h|%ad|%an|%s", "--name-status", "-n", "60"], { encoding: "utf8" });
const changelog = [];
for (const chunk of log.split("@@").filter(Boolean)) {
  const [head, ...rest] = chunk.trim().split("\n");
  const [hash, date, author, ...subj] = head.split("|");
  const changes = new Map();
  for (const line of rest) {
    const m = line.match(/^([AMDR])\d*\t(.+?)(?:\t(.+))?$/);
    if (!m) continue;
    const status = m[1];
    const path = m[3] ?? m[2];
    for (const [re, area] of SECTION) {
      const hit = path.match(re);
      if (!hit) continue;
      const slug = area === "engineering" ? "engineering index" : area === "onboarding" ? "onboarding" : hit[1];
      const key = `${area}:${slug}`;
      const prev = changes.get(key);
      const isNew = status === "A" && (area !== "knowledge" && area !== "engineering");
      changes.set(key, { area, slug, name: prettify(slug, area), change: prev?.change === "added" || isNew ? "added" : "updated" });
      break;
    }
  }
  changelog.push({ hash, date, author: author === "officiallybasti" ? "Sebastian Niewoehner" : author, title: subj.join("|"), changes: [...changes.values()] });
}

const meta = {
  generated: new Date().toISOString().slice(0, 10),
  repo: "phenom-product-copilot",
  counts: {
    skills: items.filter((i) => i.kind === "skill" && i.source === "shared").length,
    policies: items.filter((i) => i.kind === "policy").length,
    agents: items.filter((i) => i.kind === "agent" && i.source === "shared").length,
    notShared: items.filter((i) => i.source === "workspace").length,
    notMerged: items.filter((i) => i.source === "shared" && !i.merged).length,
  },
  lastChange: changelog[0]?.date ?? null,
};

writeFileSync(join(out, "catalog.json"), JSON.stringify({ meta, items }, null, 2));
writeFileSync(join(out, "changelog.json"), JSON.stringify(changelog, null, 2));
console.log(`catalog: ${items.length} items (${JSON.stringify(meta.counts)}), changelog: ${changelog.length} commits`);
