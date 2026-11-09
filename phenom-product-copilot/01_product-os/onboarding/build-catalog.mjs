// Builds the Product OS catalog (skills, policies, agents) and the "what's new" changelog
// from this repo. The PM OS site reads the JSON it writes, and onboarding/server.py serves it to the
// local dashboard (falling back to parsing skills/ when the file is missing).
// Nobody edits those JSON files by hand: change a skill, re-run this, and the site updates.
//
//   node onboarding/build-catalog.mjs                         # writes onboarding/data/
//   node onboarding/build-catalog.mjs --out <dir>             # write somewhere else (the site build)
//   node onboarding/build-catalog.mjs --extra <workspace-dir> # also list that workspace's .claude/
//                                                             # workflows as "not shared yet"
//   node onboarding/build-catalog.mjs --github                # add feedback issues and pull requests per item (needs gh)
//   node onboarding/build-catalog.mjs --codeowners            # rewrite .github/CODEOWNERS from each item's owner
//   node onboarding/build-catalog.mjs --check                 # exit 1 on a missing owner, bad status or stale CODEOWNERS
//
// Every shared item carries a `metadata:` block in its front matter (see .github/CONTRIBUTING.md):
//   metadata:
//     owner: <github handle>        required
//     status: sandbox | beta | stable | retired
//     try: "<first prompt to try>"
//     example: examples/<slug>/<file>.md
//     audience: <who it is for>      optional, default "All PMs"
import { readFileSync, readdirSync, statSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { join, basename, dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const arg = (name) => {
  const i = process.argv.indexOf(name);
  return i > -1 ? process.argv[i + 1] : undefined;
};
const flag = (name) => process.argv.includes(name);
const shared = resolve(here, ".."); // 01_product-os/
let repoRoot = resolve(shared, "..");
try {
  repoRoot = execFileSync("git", ["-C", shared, "rev-parse", "--show-toplevel"], { encoding: "utf8" }).trim();
} catch {
  /* not a git checkout */
}
// Where 01_product-os/ sits inside the repo ("01_product-os/"), for paths git and GitHub report from the repo root.
const PREFIX = relative(repoRoot, shared) ? `${relative(repoRoot, shared)}/` : "";
const fromRoot = (p) => (PREFIX && p.startsWith(PREFIX) ? p.slice(PREFIX.length) : p);
const workspace = arg("--extra") ? resolve(arg("--extra")) : null;
const out = resolve(arg("--out") ?? join(here, "data"));
const CHECK = flag("--check");
if (!CHECK) mkdirSync(out, { recursive: true });

let tracked = new Set();
try {
  tracked = new Set(execFileSync("git", ["-C", shared, "ls-files"], { encoding: "utf8" }).split("\n"));
  // Files still tracked at their old root-level path count as merged until the move to 01_product-os/ is committed.
  for (const f of execFileSync("git", ["-C", shared, "ls-files", "--full-name", ":(top)"], { encoding: "utf8" }).split("\n")) tracked.add(f);
} catch {
  /* not a git checkout: everything counts as merged */
}

const people = JSON.parse(readFileSync(join(here, "people.json"), "utf8"));
const MAINTAINER = people.maintainer;
const STATUSES = ["sandbox", "beta", "stable", "retired"];

// Workspace items that are personal automations, duplicates of a shared skill, or customer-specific.
const WORKSPACE_DENY = new Set(["eod-digest", "phenom-designer", "sr-triage"]);
// Deprecated pointers that predate the lifecycle stay out of the catalog. New retirements use `status: retired`.
const SHARED_DENY = new Set([]);

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
  "rx-sr-triage-rubric": "RX SR triage rubric",
};

function prettify(slug, kind) {
  if (kind && DISPLAY[`${kind}:${slug}`]) return DISPLAY[`${kind}:${slug}`];
  if (DISPLAY[slug]) return DISPLAY[slug];
  const words = slug.split(/[-_ ]+/).map((w) => ACRONYMS[w.toLowerCase()] ?? w.toLowerCase());
  const first = words[0];
  words[0] = ACRONYMS[first.toLowerCase()] ? first : first.charAt(0).toUpperCase() + first.slice(1);
  return words.join(" ");
}

const unquote = (s) => {
  const t = s.trim();
  if (/^".*"$/.test(t)) return t.slice(1, -1).replace(/\\"/g, '"');
  if (/^'.*'$/.test(t)) return t.slice(1, -1).replace(/''/g, "'");
  return t;
};

/** Minimal front-matter reader: scalars, [inline, lists], "- item" lists, > / | blocks, and one level of nested map. */
function frontMatter(text) {
  const lines = text.replace(/^\s*\n/, "").split(/\r?\n/);
  if (lines[0].trim() !== "---") return {};
  const fm = {};
  let key = null;
  let mode = null; // "block" | "list" | "map" | "list-or-block"
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === "---") break;
    const m = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (m && !line.startsWith(" ")) {
      key = m[1];
      const v = m[2].trim();
      if (v === "") { fm[key] = ""; mode = "list-or-block"; continue; }
      if (/^[>|][-+]?$/.test(v)) { fm[key] = ""; mode = "block"; continue; }
      if (v.startsWith("[") && v.endsWith("]")) {
        fm[key] = v.slice(1, -1).split(",").map((s) => unquote(s)).filter(Boolean);
      } else {
        fm[key] = unquote(v);
      }
      mode = null;
      continue;
    }
    if (!key) continue;
    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && (mode === "list-or-block" || mode === "list")) {
      if (!Array.isArray(fm[key])) fm[key] = [];
      fm[key].push(unquote(item[1]));
      mode = "list";
      continue;
    }
    const sub = line.match(/^\s+([A-Za-z][\w-]*):\s*(.*)$/);
    if (sub && (mode === "list-or-block" || mode === "map")) {
      if (typeof fm[key] !== "object" || Array.isArray(fm[key])) fm[key] = {};
      fm[key][sub[1]] = unquote(sub[2]);
      mode = "map";
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

function git(args) {
  try {
    return execFileSync("git", ["-C", shared, ...args], { encoding: "utf8" }).trim();
  } catch {
    return "";
  }
}

function gitDate(repo, path, mode) {
  try {
    const args = ["-C", repo, "log", "--date=short", "--format=%ad", "--follow"];
    if (mode === "added") args.push("--diff-filter=A");
    else args.push("-1");
    args.push("--", path);
    let outp = execFileSync("git", args, { encoding: "utf8" }).trim().split("\n").filter(Boolean);
    if (!outp.length && repo === shared) {
      // Not committed at its 01_product-os/ path yet: read the history of the old root-level path.
      args[args.length - 1] = `:(top)${path}`;
      outp = execFileSync("git", args, { encoding: "utf8" }).trim().split("\n").filter(Boolean);
    }
    return mode === "added" ? outp.at(-1) ?? null : outp[0] ?? null;
  } catch {
    return null;
  }
}

const authorName = (a) => (a === "officiallybasti" ? "Sebastian Niewoehner" : a);

/** Last commits that touched an item (its file, or its whole folder for folder skills). */
function history(scope) {
  // Also the pre-2026-10-30 location at the repo root, before 01_product-os/ existed.
  const log = git(["log", "--no-merges", "--date=short", "--format=%h|%ad|%an|%s", "-n", "8", "--", scope, `:(top)${scope}`]);
  return log
    .split("\n")
    .filter(Boolean)
    .map((l) => {
      const [hash, date, author, ...s] = l.split("|");
      return { hash, date, author: authorName(author), title: s.join("|") };
    });
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

/** An example output, capped so the catalog stays small. */
function readExample(rel) {
  const p = join(shared, rel);
  if (!existsSync(p)) return null;
  const text = readFileSync(p, "utf8");
  const fm = frontMatter(text);
  const body = text.replace(/^---[\s\S]*?\n---\s*\n/, "");
  const max = 12000;
  return {
    path: rel,
    title: fm.title ?? null,
    prompt: fm.prompt ?? null,
    note: fm.note ?? null,
    content: body.length > max ? body.slice(0, max) + "\n\n…" : body,
    truncated: body.length > max,
  };
}

const items = [];
const problems = [];

function add({ file, kind, source, slugFromFolder = false, command = false }) {
  const text = readFileSync(file, "utf8");
  const fm = frontMatter(text);
  const slug = slugFromFolder ? basename(dirname(file)) : basename(file).replace(/\.(md|mdc|yaml)$/, "");
  if (source === "shared" && SHARED_DENY.has(slug)) return;
  if (source === "workspace" && WORKSPACE_DENY.has(slug)) return;
  const description = clean(fm.description ?? "");
  if (!description) return;
  const rel = relative(source === "shared" ? shared : workspace, file);
  const meta = typeof fm.metadata === "object" && !Array.isArray(fm.metadata) ? fm.metadata : {};
  const id = `${kind}:${slug}`;

  let status = meta.status || null;
  if (!status && /deprecated/i.test(description)) status = "retired";
  if (source === "shared") {
    if (!meta.owner) problems.push({ id, level: "error", text: `${rel}: no metadata.owner` });
    else if (!people.people[meta.owner]) problems.push({ id, level: "warn", text: `${rel}: owner @${meta.owner} is not in onboarding/people.json` });
    if (!status) problems.push({ id, level: "error", text: `${rel}: no metadata.status` });
    else if (!STATUSES.includes(status)) problems.push({ id, level: "error", text: `${rel}: status "${status}" is not one of ${STATUSES.join(", ")}` });
    if (meta.example && !existsSync(join(shared, meta.example))) problems.push({ id, level: "error", text: `${rel}: example ${meta.example} does not exist` });
  }
  const ownerHandle = meta.owner || (source === "workspace" ? MAINTAINER : null);
  const owner = ownerHandle ? { handle: ownerHandle, name: people.people[ownerHandle]?.name ?? ownerHandle, active: people.people[ownerHandle]?.collaborator !== false } : null;

  const triggers = Array.isArray(fm.triggers) ? fm.triggers.slice(0, 12) : [];
  const requires = Array.isArray(fm.requires) ? fm.requires : [];
  const always = fm.always === "true" || fm.alwaysApply === "true";
  const scope = slugFromFolder ? relative(source === "shared" ? shared : workspace, dirname(file)) + "/" : rel;
  items.push({
    id,
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
    scope,
    source,
    owner,
    status: source === "shared" ? status : null,
    audience: meta.audience || "All PMs",
    try: meta.try || null,
    supersededBy: meta["superseded-by"] || null,
    example: source === "shared" && meta.example ? readExample(meta.example) : null,
    history: source === "shared" ? history(scope) : [],
    feedback: [],
    prs: [],
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

// GitHub: the repo behind origin, as owner/name
const remote = git(["remote", "get-url", "origin"]);
const repoSlug = (remote.match(/github\.com[:/]([^/]+\/[^/.]+)/) || [])[1] ?? null;
const repoUrl = repoSlug ? `https://github.com/${repoSlug}` : null;

/** Which catalog item a repo path belongs to: the item itself, or its example folder. */
function itemsForPath(rootPath) {
  const path = fromRoot(rootPath);
  return items.filter((i) => i.source === "shared" && (path === i.path || (i.scope.endsWith("/") && path.startsWith(i.scope)) || path.startsWith(`examples/${i.slug}/`)));
}

let github = null;
if (flag("--github") && repoSlug) {
  const gh = (args) => JSON.parse(execFileSync("gh", args, { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 }));
  try {
    const issues = gh(["issue", "list", "-R", repoSlug, "--state", "all", "--limit", "300", "--json", "number,title,state,author,createdAt,closedAt,labels,comments,url,body"]);
    const prs = gh(["pr", "list", "-R", repoSlug, "--state", "all", "--limit", "200", "--json", "number,title,state,author,createdAt,mergedAt,url,files,reviewDecision,isDraft"]);
    let collaborators = null;
    try {
      collaborators = new Set(gh(["api", `repos/${repoSlug}/collaborators`, "--paginate", "--jq", "[.[].login]"]));
    } catch {
      /* needs push access; skip the check */
    }
    const kindOf = (body = "") => (body.match(/### What kind of feedback\?\s*\n+([^\n]+)/) || [])[1]?.trim() ?? null;
    for (const is of issues) {
      const ids = is.labels.map((l) => l.name).filter((n) => /^(skill|agent|policy):/.test(n));
      const fromBody = (is.body.match(/### Skill or agent\s*\n+`?([a-z]+:[a-z0-9-]+)`?/i) || [])[1];
      for (const id of new Set([...ids, ...(fromBody ? [fromBody] : [])])) {
        const item = items.find((i) => i.id === id);
        if (!item) continue;
        item.feedback.push({
          number: is.number,
          title: is.title.replace(/^\[feedback\]\s*/i, ""),
          state: is.state.toLowerCase(),
          kind: kindOf(is.body),
          author: is.author?.login ?? null,
          created: is.createdAt.slice(0, 10),
          closed: is.closedAt ? is.closedAt.slice(0, 10) : null,
          comments: Array.isArray(is.comments) ? is.comments.length : is.comments ?? 0,
          url: is.url,
        });
      }
    }
    for (const pr of prs) {
      const hit = new Set(pr.files.flatMap((f) => itemsForPath(f.path)));
      for (const item of hit) {
        item.prs.push({
          number: pr.number,
          title: pr.title,
          state: pr.isDraft && pr.state === "OPEN" ? "draft" : pr.state.toLowerCase(),
          author: pr.author?.login ?? null,
          created: pr.createdAt.slice(0, 10),
          merged: pr.mergedAt ? pr.mergedAt.slice(0, 10) : null,
          review: pr.reviewDecision || null,
          url: pr.url,
        });
      }
    }
    if (collaborators) {
      for (const [handle, p] of Object.entries(people.people)) {
        if (!collaborators.has(handle) && items.some((i) => i.owner?.handle === handle && i.source === "shared")) {
          problems.push({ id: null, level: "warn", text: `@${handle} (${p.name}) owns items but is not a collaborator on ${repoSlug}: invite them or reassign` });
          for (const i of items) if (i.owner?.handle === handle) i.owner.active = false;
        }
      }
    }
    github = { repo: repoSlug, fetched: new Date().toISOString().slice(0, 16).replace("T", " "), issues: issues.length, prs: prs.length };
  } catch (e) {
    console.error(`GitHub data skipped: ${e.message.split("\n")[0]}`);
  }
}

// CODEOWNERS: generated from each item's owner, the maintainer co-owns everything as backup reviewer.
const codeowners = [
  "# Generated by onboarding/build-catalog.mjs --codeowners from each item's metadata.owner.",
  "# Do not edit by hand: change the owner in the item's front matter and re-run.",
  "# The maintainer co-owns every path so a review never waits on one person.",
  "",
  `*  @${MAINTAINER}`,
  ...items
    .filter((i) => i.source === "shared" && i.owner)
    .flatMap((i) => {
      const who = [...new Set([i.owner.handle, MAINTAINER])].map((h) => `@${h}`).join(" ");
      return [`/${PREFIX}${i.scope}  ${who}`, ...(existsSync(join(shared, "examples", i.slug)) ? [`/${PREFIX}examples/${i.slug}/  ${who}`] : [])];
    }),
  "",
].join("\n");
const coPath = join(repoRoot, ".github", "CODEOWNERS");
const coCurrent = existsSync(coPath) ? readFileSync(coPath, "utf8") : null;
if (flag("--codeowners")) {
  mkdirSync(dirname(coPath), { recursive: true });
  writeFileSync(coPath, codeowners);
} else if (coCurrent !== codeowners) {
  problems.push({ id: null, level: CHECK ? "error" : "warn", text: ".github/CODEOWNERS is out of date: run node onboarding/build-catalog.mjs --codeowners" });
}

if (CHECK) {
  for (const p of problems) console.log(`${p.level === "error" ? "✗" : "!"} ${p.text}`);
  const errors = problems.filter((p) => p.level === "error").length;
  console.log(errors ? `\n${errors} problem(s). See .github/CONTRIBUTING.md.` : `✓ catalog check passed (${items.length} items, every shared item has an owner and a status)`);
  process.exit(errors ? 1 : 0);
}

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
    const path = fromRoot(m[3] ?? m[2]);
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
  changelog.push({ hash, date, author: authorName(author), title: subj.join("|"), changes: [...changes.values()] });
}

const live = (i) => i.source === "shared" && i.status !== "retired";
const meta = {
  generated: new Date().toISOString().slice(0, 10),
  repo: "phenom-product-copilot",
  repoUrl,
  repoPrefix: PREFIX,
  maintainer: { handle: MAINTAINER, name: people.people[MAINTAINER]?.name ?? MAINTAINER },
  github,
  counts: {
    skills: items.filter((i) => i.kind === "skill" && live(i)).length,
    policies: items.filter((i) => i.kind === "policy" && live(i)).length,
    agents: items.filter((i) => i.kind === "agent" && live(i)).length,
    notShared: items.filter((i) => i.source === "workspace").length,
    notMerged: items.filter((i) => i.source === "shared" && !i.merged).length,
    owners: new Set(items.filter(live).map((i) => i.owner?.handle).filter(Boolean)).size,
    withExample: items.filter((i) => live(i) && i.example).length,
    byStatus: Object.fromEntries(STATUSES.map((s) => [s, items.filter((i) => i.source === "shared" && i.status === s).length])),
  },
  problems,
  lastChange: changelog[0]?.date ?? null,
};

writeFileSync(join(out, "catalog.json"), JSON.stringify({ meta, items }, null, 2));
writeFileSync(join(out, "changelog.json"), JSON.stringify(changelog, null, 2));
console.log(`catalog: ${items.length} items (${JSON.stringify(meta.counts)}), changelog: ${changelog.length} commits${github ? `, GitHub: ${github.issues} issues / ${github.prs} PRs` : ""}`);
for (const p of problems) console.log(`${p.level === "error" ? "✗" : "!"} ${p.text}`);
