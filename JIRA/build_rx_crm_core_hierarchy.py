#!/usr/bin/env python3
"""Build the RX CRM Core Jira hierarchy page from the fetched JSONL snapshots.

Read-only. Does not call Jira. Inputs:
  JIRA/data/rx-crm-core-hierarchy.jsonl
  JIRA/data/rx-crm-core-hierarchy-parents.jsonl
Output:
  JIRA/rx-crm-core-hierarchy.html
"""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "rx-crm-core-hierarchy.html"
BROWSE = "https://phenompeople.atlassian.net/browse/"
RUN_DATE = "26 Oct 2026"

JQL = (
    'project = "PHEM" AND (statusCategory != Done OR (statusCategory = Done '
    "AND statusCategoryChangedDate >= -2w)) AND "
    '"Product Experience: Product2[Dropdown]" = '
    '"Recruiter Experience (RX) - CRM - Core" AND type IN (Epic, Initiative, Story) '
    "ORDER BY status ASC"
)

STATUS_RANK = {
    "To Do": 10,
    "Reopened": 20,
    "Story Grooming": 30,
    "Story Elaboration": 40,
    "Story Ready": 50,
    "Epic Grooming": 60,
    "Epic Ready": 70,
    "UX Queue": 80,
    "UX/UI Validation": 90,
    "Development": 100,
    "In Progress": 110,
    "In QA": 120,
    "PM Acceptance Queue": 130,
    "BLOCKED": 140,
    "ON Hold": 150,
    "Done": 160,
    "Closed": 170,
}
TYPE_RANK = {"Initiative": 0, "Epic": 1, "Story": 2}
CLONE_RELATIONS = {"clones", "is cloned by"}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def key_num(key: str) -> int:
    try:
        return int(str(key).rsplit("-", 1)[-1])
    except (TypeError, ValueError):
        return 0


def is_clone(link: dict) -> bool:
    return link.get("linkType") == "Cloners" or link.get("relation") in CLONE_RELATIONS


def type_class(issue_type: str) -> str:
    name = (issue_type or "").lower()
    if name == "initiative":
        return "t-initiative"
    if name == "epic":
        return "t-epic"
    if name == "story":
        return "t-story"
    return "t-other"


def status_class(status: str, category: str) -> str:
    if status in {"BLOCKED", "Blocked"}:
        return "is-blocked"
    if category == "done":
        return "cat-done"
    if category == "indeterminate":
        return "cat-indeterminate"
    return "cat-new"


def sort_key(node: dict):
    return (
        0 if node.get("inFilter") else 1,
        TYPE_RANK.get(node.get("type"), 9),
        STATUS_RANK.get(node.get("status"), 80),
        key_num(node.get("key") or ""),
        node.get("key") or "",
    )


def descendant_counts(node: dict) -> Counter:
    counts: Counter = Counter()

    def walk(current: dict) -> None:
        for child in current["children"]:
            if child.get("inFilter"):
                counts[child.get("type") or "Other"] += 1
            walk(child)

    walk(node)
    return counts


def has_in_filter(node: dict) -> bool:
    if node.get("inFilter"):
        return True
    return any(has_in_filter(child) for child in node["children"])


def build_nodes(main: list[dict], parents: list[dict]) -> dict[str, dict]:
    nodes: dict[str, dict] = {}

    def ensure(key: str) -> dict:
        if key not in nodes:
            nodes[key] = {
                "key": key,
                "summary": "",
                "type": "Other",
                "status": "",
                "statusCategory": "",
                "assignee": None,
                "fixVersions": [],
                "links": [],
                "inFilter": False,
                "unresolved": False,
                "children": [],
                "parentKey": None,
            }
        return nodes[key]

    def absorb(raw: dict, in_filter: bool) -> None:
        node = ensure(raw["key"])
        node.update(
            {
                "key": raw["key"],
                "summary": raw.get("summary") or "",
                "type": raw.get("type") or "Other",
                "status": raw.get("status") or "",
                "statusCategory": raw.get("statusCategory") or "",
                "assignee": raw.get("assignee"),
                "fixVersions": raw.get("fixVersions") or [],
                "links": raw.get("links") or [],
                "inFilter": in_filter,
                "unresolved": False,
            }
        )

    for raw in main:
        absorb(raw, True)
    for raw in parents:
        if raw["key"] not in nodes or not nodes[raw["key"]]["inFilter"]:
            absorb(raw, False)

    def reaches(start: str, target: str) -> bool:
        seen = set()
        current = start
        while current and current not in seen:
            if current == target:
                return True
            seen.add(current)
            current = nodes[current].get("parentKey")
        return False

    sources = [(raw, True) for raw in main] + [(raw, False) for raw in parents]
    for raw, _in_filter in sources:
        parent = raw.get("parent") or None
        if not parent or not parent.get("key"):
            continue
        parent_key = parent["key"]
        child_key = raw["key"]
        if parent_key == child_key:
            continue
        parent_node = ensure(parent_key)
        if not parent_node.get("summary"):
            parent_node.update(
                {
                    "summary": parent.get("summary") or "",
                    "type": parent.get("type") or "Other",
                    "status": parent.get("status") or "",
                    "statusCategory": parent.get("statusCategory") or "",
                    "inFilter": False,
                    "unresolved": parent_key not in {row["key"] for row in parents}
                    and parent_key not in {row["key"] for row in main},
                }
            )
        if reaches(parent_key, child_key):
            continue
        child = nodes[child_key]
        if child.get("parentKey"):
            continue
        child["parentKey"] = parent_key
        parent_node["children"].append(child)

    for node in nodes.values():
        node["children"].sort(key=sort_key)
    return nodes


def status_html(status: str, category: str) -> str:
    return (
        f'<span class="status {status_class(status, category)}">'
        f"<i></i>{esc(status)}</span>"
    )


def render_link(link: dict, known_keys: set[str], level: int) -> str:
    clone = "1" if is_clone(link) else "0"
    key = link.get("key") or ""
    summary = link.get("summary") or ""
    relation = link.get("relation") or "linked"
    issue_type = link.get("type") or "Item"
    status = link.get("status") or ""
    category = link.get("statusCategory") or ""
    search = " ".join([relation, issue_type, key, summary, status]).lower()
    jump = ""
    if key in known_keys:
        jump = f'<a class="jump" href="#issue-{esc(key)}">In tree</a>'
    return (
        f'<div class="link-row{" is-clone" if clone == "1" else ""}" style="--level:{level}" '
        f'data-clone="{clone}" data-status="{esc(status)}" data-search="{esc(search)}">'
        f'<span class="type {type_class(issue_type)}">{esc(issue_type)}</span>'
        f'<a class="key" href="{BROWSE}{esc(key)}" target="_blank" rel="noopener">{esc(key)}</a>'
        f'<span class="title"><span class="twist"></span>'
        f'<span class="rel">{esc(relation)}</span>'
        f'<span class="summary" title="{esc(summary)}">{esc(summary)}</span></span>'
        f"{status_html(status, category)}"
        f'<span class="who">{jump}</span></div>'
    )


def render_row(node: dict) -> str:
    counts = descendant_counts(node)
    bits = []
    for label, key in (("epics", "Epic"), ("stories", "Story")):
        if counts[key]:
            bits.append(f"{counts[key]} {label}")
    extra = sum(counts[name] for name in counts if name not in {"Epic", "Story"})
    if extra:
        bits.append(f"{extra} other")
    meta = f'<span class="meta">{esc(" · ".join(bits))}</span>' if bits else ""
    if not node.get("inFilter"):
        meta += '<span class="meta">Outside</span>'
    if node.get("unresolved"):
        meta += '<span class="meta">Not loaded</span>'
    links = node.get("links") or []
    clone_n = sum(1 for link in links if is_clone(link))
    other_n = len(links) - clone_n
    if other_n:
        meta += f'<span class="meta linkcount">{other_n} linked</span>'
    if clone_n:
        meta += f'<span class="meta clonecount">{clone_n} clones</span>'
    summary = node.get("summary") or ""
    assignee = node.get("assignee") or ""
    css = "node context" if not node.get("inFilter") else "node"
    return (
        f'<span class="{css}">'
        f'<span class="type {type_class(node.get("type") or "")}">{esc(node.get("type"))}</span>'
        f'<a class="key" href="{BROWSE}{esc(node["key"])}" target="_blank" rel="noopener">{esc(node["key"])}</a>'
        f'<span class="title"><span class="twist"></span>'
        f'<span class="summary" title="{esc(summary)}">{esc(summary)}</span>{meta}</span>'
        f'{status_html(node.get("status") or "", node.get("statusCategory") or "")}'
        f'<span class="who">{esc(assignee)}</span>'
        f"</span>"
    )


def render_node(node: dict, known_keys: set[str], level: int = 0) -> str:
    children = node["children"]
    links = node.get("links") or []
    search_parts = [
        node.get("key") or "",
        node.get("summary") or "",
        node.get("status") or "",
        node.get("type") or "",
        node.get("assignee") or "",
        " ".join(node.get("fixVersions") or []),
    ]
    search_parts.extend(
        " ".join(
            [
                link.get("relation") or "",
                link.get("type") or "",
                link.get("key") or "",
                link.get("summary") or "",
                link.get("status") or "",
            ]
        )
        for link in links
    )
    search = " ".join(search_parts).lower()
    row = render_row(node)
    if children or links:
        inner = ""
        if children:
            inner += '<ul class="tree">' + "".join(render_node(child, known_keys, level + 1) for child in children) + "</ul>"
        if links:
            inner += '<div class="links">' + "".join(render_link(link, known_keys, level + 1) for link in links) + "</div>"
        body = (
            f'<details data-kind="hierarchy" data-type="{esc(node.get("type"))}">'
            f"<summary>{row}</summary>{inner}</details>"
        )
    else:
        body = row
    in_filter = "1" if node.get("inFilter") else "0"
    return (
        f'<li id="issue-{esc(node["key"])}" data-key="{esc(node["key"])}" '
        f'data-status="{esc(node.get("status"))}" data-type="{esc(node.get("type"))}" '
        f'data-infilter="{in_filter}" data-search="{esc(search)}" style="--level:{level}">{body}</li>'
    )


def render_section(section_id: str, title: str, roots: list[dict], known_keys: set[str]) -> str:
    if not roots:
        return ""
    items = "".join(render_node(node, known_keys) for node in roots)
    return (
        f'<section class="block" id="{esc(section_id)}">'
        f"<h2>{esc(title)} <span>{len(roots)}</span></h2>"
        f'<ul class="tree">{items}</ul></section>'
    )


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RX CRM Core Jira hierarchy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../DesignSystem/styles/pds-tokens.css">
<style>
html, body { font-family: var(--font-family-body, Poppins), "Helvetica Neue", Arial, sans-serif; color: var(--color-neutrals-500); background: var(--color-core-white); }
body { margin: 0; font-size: 13px; }
.page { max-width: 1280px; margin: 0 auto; padding: 20px 24px 48px; }
.top { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 4px; }
h1 { font-size: 22px; font-weight: 400; letter-spacing: 0; margin: 0; color: var(--color-neutrals-500); }
.when { font-size: 12px; color: var(--color-neutrals-300); }
.counts { margin: 0 0 12px; font-size: 13px; color: var(--color-neutrals-300); }
.counts b { color: var(--color-neutrals-500); font-weight: 500; }
.bar { position: sticky; top: 0; z-index: 4; background: var(--color-core-white); padding-top: 8px; }
.tools { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.search { flex: 1; min-width: 0; height: 40px; border: 1px solid var(--color-neutrals-75); border-radius: 8px; padding: 0 14px; font: inherit; color: var(--color-neutrals-500); background: var(--color-core-white); }
.search:focus { outline: none; border-color: var(--color-secondary-200); }
select, .tools button { height: 40px; border: 1px solid var(--color-neutrals-75); border-radius: 8px; background: var(--color-core-white); color: var(--color-neutrals-400); font: inherit; font-size: 13px; padding: 0 12px; cursor: pointer; }
.tools button:hover, select:hover { background: var(--color-grays-25); }
.check { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-neutrals-400); white-space: nowrap; }
.shown { font-size: 12px; color: var(--color-neutrals-300); font-variant-numeric: tabular-nums; min-width: 7rem; text-align: right; }
.cols, .node, .link-row { display: grid; grid-template-columns: 92px 108px minmax(0, 1fr) 132px 160px; column-gap: 12px; align-items: center; }
.cols { background: var(--color-core-white); min-height: 36px; padding: 0 8px; border-bottom: 1px solid var(--color-neutrals-75); color: var(--color-neutrals-300); font-size: 12px; font-weight: 500; }
.h-sum { padding-left: 16px; }
h2 { margin: 28px 8px 4px; font-size: 12px; font-weight: 500; letter-spacing: .04em; text-transform: uppercase; color: var(--color-neutrals-300); display: flex; gap: 8px; align-items: center; }
h2 span { font-variant-numeric: tabular-nums; }
ul.tree, ul.tree ul { list-style: none; margin: 0; padding: 0; }
ul.tree li { margin: 0; }
ul.tree details > summary { display: block; cursor: pointer; list-style: none; }
ul.tree details > summary::-webkit-details-marker { display: none; }
.node, .link-row { min-height: 44px; padding: 0 8px; border-bottom: 1px solid var(--color-neutrals-50); }
.node:hover, .link-row:hover { background: var(--color-grays-25); }
.node.context { color: var(--color-neutrals-300); }
.title { display: flex; align-items: center; gap: 8px; min-width: 0; padding-left: calc(var(--level, 0) * 20px); }
.twist { width: 16px; height: 16px; flex: none; position: relative; }
details > summary .twist::before { content: ""; position: absolute; left: 4px; top: 5px; width: 5px; height: 5px; border: solid var(--color-neutrals-300); border-width: 0 1.5px 1.5px 0; transform: rotate(-45deg); }
details[open] > summary .twist::before { transform: rotate(45deg); top: 3px; }
.summary { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.meta, .rel { flex: none; font-size: 12px; color: var(--color-neutrals-300); }
.type { font-size: 12px; font-weight: 500; white-space: nowrap; }
.t-initiative { color: var(--color-secondary-300); }
.t-epic { color: var(--color-primary-400); }
.t-story { color: var(--color-neutrals-300); }
.t-other { color: var(--color-kobe-300); }
.key { font-weight: 500; color: var(--color-secondary-300); text-decoration: none; font-variant-numeric: tabular-nums; white-space: nowrap; }
.key:hover { text-decoration: underline; }
.status { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--color-neutrals-400); white-space: nowrap; }
.status i { width: 8px; height: 8px; border-radius: 50%; background: var(--color-neutrals-200); flex: none; }
.status.cat-indeterminate i { background: var(--color-yellow-300); }
.status.cat-done i { background: var(--color-green-400); }
.status.is-blocked i { background: var(--color-red-400); }
.who { font-size: 13px; color: var(--color-neutrals-400); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.links { display: flex; flex-direction: column; }
.jump { color: var(--color-primary-400); text-decoration: none; font-size: 12px; }
.jump:hover { text-decoration: underline; }
li.is-hidden, .link-row.is-hidden, body.hide-clones .link-row.is-clone, body.hide-links .links, body.hide-links .linkcount, body.hide-clones .clonecount { display: none; }
li.is-context-match > details > summary .node, li.is-context-match > .node { color: var(--color-neutrals-300); }
.sheet { overflow-x: auto; }
</style>
</head>
<body class="hide-clones">
<div class="page">
<header class="top">
<h1>CRM Core</h1>
<span class="when">__RUN_DATE__</span>
</header>
<p class="counts">__STATS__</p>
<div class="bar">
<div class="tools">
<input id="q" class="search" type="search" placeholder="Search" autocomplete="off">
<select id="status" aria-label="Status"><option value="">Status</option>__STATUS_OPTIONS__</select>
<button type="button" id="lvl-init">Initiatives</button>
<button type="button" id="lvl-epic">Epics</button>
<button type="button" id="lvl-story">Stories</button>
<button type="button" id="lvl-all">Expand</button>
<button type="button" id="lvl-none">Collapse</button>
<label class="check"><input id="show-links" type="checkbox" checked> Links</label>
<label class="check"><input id="show-clones" type="checkbox"> Clones</label>
<span class="shown" id="shown"></span>
</div>
</div>
<div class="sheet">
<div class="cols head"><span>Type</span><span>Key</span><span class="h-sum">Summary</span><span>Status</span><span>Assignee</span></div>
__SECTIONS__
</div>
</div>
<script>
const q = document.getElementById('q');
const status = document.getElementById('status');
const showLinks = document.getElementById('show-links');
const showClones = document.getElementById('show-clones');
const shown = document.getElementById('shown');
const inFilterItems = () => document.querySelectorAll('li[data-infilter="1"]');

function setLevel(level) {
  document.querySelectorAll('details[data-kind="hierarchy"]').forEach((d) => {
    const t = d.dataset.type;
    if (level === 'none' || level === 'initiative') d.open = false;
    else if (level === 'all') d.open = true;
    else if (level === 'epic') d.open = t === 'Initiative';
    else if (level === 'story') d.open = t === 'Initiative' || t === 'Epic';
  });
}

function hit(hay, query) {
  if (!query) return true;
  const text = hay || '';
  if (/^[a-z][a-z0-9]*-[0-9]+$/.test(query)) {
    let from = 0;
    while (from < text.length) {
      const i = text.indexOf(query, from);
      if (i < 0) return false;
      const before = i === 0 ? '' : text.charAt(i - 1);
      const after = text.charAt(i + query.length);
      const leftOk = before === '' || !/[a-z0-9]/.test(before);
      const rightOk = after === '' || !/[0-9]/.test(after);
      if (leftOk && rightOk) return true;
      from = i + 1;
    }
    return false;
  }
  return text.includes(query);
}

function applyFilter() {
  const query = q.value.trim().toLowerCase();
  const st = status.value;
  document.body.classList.toggle('hide-links', !showLinks.checked);
  document.body.classList.toggle('hide-clones', !showClones.checked);
  const lis = [...document.querySelectorAll('ul.tree li')];
  const rows = [...document.querySelectorAll('.link-row')];
  lis.forEach((li) => li.classList.remove('is-hidden', 'is-context-match'));
  rows.forEach((row) => row.classList.remove('is-hidden'));
  const active = Boolean(query || st);
  if (active) {
    const ownMatch = new Set();
    lis.forEach((li) => {
      const textOk = hit(li.dataset.search, query);
      const statusOk = !st || li.dataset.status === st;
      if (textOk && statusOk) ownMatch.add(li);
    });
    rows.forEach((row) => {
      const textOk = hit(row.dataset.search, query);
      const statusOk = !st || row.dataset.status === st;
      const parentLi = row.closest('li');
      const parentMatches = parentLi && ownMatch.has(parentLi);
      if (!(textOk && statusOk) && !parentMatches) row.classList.add('is-hidden');
    });
    const visible = new Set(ownMatch);
    const consider = (el) => {
      let parent = el.parentElement;
      while (parent) {
        if (parent.tagName === 'LI') visible.add(parent);
        if (parent.tagName === 'DETAILS') parent.open = true;
        parent = parent.parentElement;
      }
    };
    ownMatch.forEach(consider);
    rows.forEach((row) => {
      if (!row.classList.contains('is-hidden')) consider(row);
    });
    lis.forEach((li) => {
      if (!visible.has(li)) li.classList.add('is-hidden');
      else if (!ownMatch.has(li)) li.classList.add('is-context-match');
    });
  }
  document.querySelectorAll('section.block').forEach((sec) => {
    const roots = [...sec.querySelectorAll(':scope > ul.tree > li')];
    sec.hidden = roots.length > 0 && roots.every((li) => li.classList.contains('is-hidden'));
  });
  const total = inFilterItems().length;
  const visibleCount = [...inFilterItems()].filter((li) => !li.classList.contains('is-hidden')).length;
  shown.textContent = visibleCount + ' / ' + total;
}

q.addEventListener('input', applyFilter);
status.addEventListener('change', applyFilter);
showLinks.addEventListener('change', applyFilter);
showClones.addEventListener('change', applyFilter);
document.getElementById('lvl-init').addEventListener('click', () => setLevel('initiative'));
document.getElementById('lvl-epic').addEventListener('click', () => setLevel('epic'));
document.getElementById('lvl-story').addEventListener('click', () => setLevel('story'));
document.getElementById('lvl-all').addEventListener('click', () => setLevel('all'));
document.getElementById('lvl-none').addEventListener('click', () => setLevel('none'));
document.querySelectorAll('a.jump').forEach((a) => {
  a.addEventListener('click', () => {
    const id = a.getAttribute('href').slice(1);
    let parent = document.getElementById(id);
    while (parent) {
      if (parent.tagName === 'DETAILS') parent.open = true;
      parent = parent.parentElement;
    }
  });
});
applyFilter();
</script>
</body>
</html>
"""


def main() -> None:
    issues = load_jsonl(DATA / "rx-crm-core-hierarchy.jsonl")
    parents = load_jsonl(DATA / "rx-crm-core-hierarchy-parents.jsonl")
    nodes = build_nodes(issues, parents)
    roots = [node for node in nodes.values() if not node.get("parentKey") and has_in_filter(node)]
    roots.sort(key=sort_key)

    def section_roots(predicate) -> list[dict]:
        return [node for node in roots if predicate(node)]

    groups = [
        ("initiatives", "Initiatives", section_roots(lambda n: n["type"] == "Initiative" and n.get("inFilter"))),
        ("initiatives-outside", "Outside filter", section_roots(lambda n: n["type"] == "Initiative" and not n.get("inFilter"))),
        ("epics", "Epics", section_roots(lambda n: n["type"] == "Epic")),
        ("stories", "Stories", section_roots(lambda n: n["type"] == "Story")),
        ("other", "Other", section_roots(lambda n: n["type"] not in {"Initiative", "Epic", "Story"})),
    ]

    known_keys = set(nodes)
    rendered_keys: list[str] = []

    def walk(node: dict) -> None:
        rendered_keys.append(node["key"])
        for child in node["children"]:
            walk(child)

    for _sid, _title, group in groups:
        for node in group:
            walk(node)

    in_filter_keys = [row["key"] for row in issues]
    missing = sorted(set(in_filter_keys) - set(rendered_keys))
    dupes = [key for key, count in Counter(rendered_keys).items() if count > 1 and key in set(in_filter_keys)]
    if missing or dupes:
        raise SystemExit(f"tree check failed missing={missing[:10]} dupes={dupes[:10]}")
    for raw in issues:
        parent_key = (raw.get("parent") or {}).get("key")
        node = nodes[raw["key"]]
        if parent_key and node.get("parentKey") != parent_key:
            raise SystemExit(f"parent mismatch {raw['key']} expected {parent_key} got {node.get('parentKey')}")
        if not parent_key and node.get("parentKey"):
            raise SystemExit(f"unexpected parent on {raw['key']}")

    type_counts = Counter(row["type"] for row in issues)
    other_types = Counter()
    for row in issues:
        for link in row.get("links") or []:
            if (link.get("type") or "") not in {"Initiative", "Epic", "Story"}:
                other_types[link.get("type") or "Item"] += 1
    statuses = sorted({row["status"] for row in issues if row.get("status")}, key=lambda name: (STATUS_RANK.get(name, 80), name))
    stats_html = (
        f"<b>{len(issues):,}</b>"
        f" · {type_counts['Initiative']:,} initiatives"
        f" · {type_counts['Epic']:,} epics"
        f" · {type_counts['Story']:,} stories"
    )
    sections = "".join(
        render_section(sid, title, group, known_keys) for sid, title, group in groups
    )
    status_options = "".join(f'<option value="{esc(name)}">{esc(name)}</option>' for name in statuses)
    html_out = (
        PAGE.replace("__RUN_DATE__", esc(RUN_DATE))
        .replace("__STATS__", stats_html)
        .replace("__STATUS_OPTIONS__", status_options)
        .replace("__SECTIONS__", sections)
    )
    OUT.write_text(html_out)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"roots {len(roots)} rendered {len(rendered_keys)} in-filter {len(in_filter_keys)}")
    print("root sections", {title: len(group) for _sid, title, group in groups})
    print("other link types", other_types.most_common(8))


if __name__ == "__main__":
    main()
