#!/usr/bin/env python3
"""Merge NDJSON slice files into CSV + downloadable HTML for RX CRM Core export."""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path("/Users/venkata.gonella/phenom_repo/Disney/exports")
SLICES = ROOT / "slices"
OUT_CSV = ROOT / "rx-crm-core-product-experience-ALL.csv"
OUT_HTML = ROOT / "rx-crm-core-product-experience-ALL.html"
OUT_META = ROOT / "rx-crm-core-product-experience-ALL.meta.json"
EXPECTED_TOTAL = 383220

JQL = '"Product Experience: Product2" = "Recruiter Experience (RX) - CRM - Core"'
JIRA_FILTER = "https://phenompeople.atlassian.net/issues/?jql=" + urllib.parse.quote(
    JQL + " ORDER BY updated DESC"
)


def extract_option(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get("value") or v.get("name") or v.get("displayName") or ""
    if isinstance(v, list):
        return ", ".join(x for x in (extract_option(i) for i in v) if x)
    return str(v)


def extract_date(v):
    if not v:
        return ""
    s = str(v)
    return s[:10] if re.match(r"\d{4}-\d{2}-\d{2}", s) else s


def normalize(raw: dict) -> dict | None:
    if "key" in raw and "fields" not in raw and "jiraId" not in raw:
        # already slim
        key = raw.get("key") or raw.get("jiraId")
        if not key:
            return None
        return {
            "key": key,
            "eta": extract_date(raw.get("eta") or raw.get("ETA")),
            "client": raw.get("client") or raw.get("Client") or "",
            "fixVersions": raw.get("fixVersions")
            if isinstance(raw.get("fixVersions"), str)
            else extract_option(raw.get("fixVersions")),
            "summary": raw.get("summary") or "",
            "status": raw.get("status") or "",
            "issuetype": raw.get("issuetype") or raw.get("issueType") or "",
            "projectKey": raw.get("projectKey") or raw.get("project") or "",
        }

    f = raw.get("fields", raw)
    key = raw.get("key")
    if not key:
        return None
    clients = [
        extract_option(f.get("customfield_11213")),
        extract_option(f.get("customfield_14805")),
        extract_option(f.get("customfield_14396")),
        extract_option(f.get("customfield_14523")),
    ]
    client = next((c for c in clients if c), "")
    eta = extract_date(f.get("customfield_14383")) or extract_date(f.get("customfield_15541"))
    fix = extract_option(f.get("fixVersions"))
    status = f.get("status", {})
    itype = f.get("issuetype", {})
    project = f.get("project", {})
    return {
        "key": key,
        "eta": eta,
        "client": client,
        "fixVersions": fix,
        "summary": f.get("summary") or "",
        "status": status.get("name") if isinstance(status, dict) else (status or ""),
        "issuetype": itype.get("name") if isinstance(itype, dict) else (itype or ""),
        "projectKey": project.get("key") if isinstance(project, dict) else (project or ""),
    }


def load_issues() -> dict[str, dict]:
    issues: dict[str, dict] = {}
    files = sorted(SLICES.rglob("*.ndjson")) + sorted(SLICES.rglob("*.jsonl"))
    # also accept per-slice json arrays
    files += sorted(SLICES.rglob("*.json"))
    for path in files:
        if path.name.endswith(".meta.json") or path.name == "progress.json":
            continue
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            continue
        try:
            if path.suffix == ".json" and text[0] in "[{":
                data = json.loads(text)
                rows = data if isinstance(data, list) else data.get("issues", [])
                for raw in rows:
                    n = normalize(raw)
                    if n:
                        issues[n["key"]] = n
                continue
        except Exception:
            pass
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except Exception:
                continue
            n = normalize(raw)
            if n:
                issues[n["key"]] = n
    return issues


def write_csv(issues: list[dict]) -> None:
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "JIRA ID",
                "ETA",
                "Client",
                "Fix Version",
                "Summary",
                "Status",
                "Issue Type",
                "Project",
                "URL",
            ]
        )
        for i in issues:
            w.writerow(
                [
                    i["key"],
                    i["eta"],
                    i["client"],
                    i["fixVersions"],
                    i["summary"],
                    i["status"],
                    i["issuetype"],
                    i["projectKey"],
                    f"https://phenompeople.atlassian.net/browse/{i['key']}",
                ]
            )


def write_html(issues: list[dict], exported: int) -> None:
    # Embed as JS array of arrays for virtualized rendering (compact).
    rows = [
        [
            i["key"],
            i["eta"],
            i["client"],
            i["fixVersions"],
            i["summary"],
            i["status"],
            i["issuetype"],
            i["projectKey"],
        ]
        for i in issues
    ]
    payload = json.dumps(rows, ensure_ascii=False)
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    pct = (exported / EXPECTED_TOTAL * 100) if EXPECTED_TOTAL else 0
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>RX CRM Core — ALL Product Experience issues</title>
<style>
  :root {{ --bg:#f6f7f9; --card:#fff; --text:#1f2328; --muted:#59636e; --border:#d0d7de; --accent:#0969da; --header:#0a1628; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; background:var(--bg); color:var(--text); }}
  header {{ background:var(--header); color:#fff; padding:24px 28px; }}
  header h1 {{ margin:0 0 8px; font-size:22px; }}
  header p {{ margin:4px 0; color:#c8d1dc; font-size:14px; }}
  header a {{ color:#9ecbff; }}
  main {{ padding:20px 28px 40px; }}
  .cards {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; margin-bottom:16px; }}
  .card {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 16px; }}
  .card .label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
  .card .value {{ font-size:24px; font-weight:650; margin-top:4px; }}
  .toolbar {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; background:var(--card); border:1px solid var(--border); border-radius:10px; padding:12px 14px; margin-bottom:12px; }}
  .toolbar input {{ flex:1; min-width:220px; padding:8px 10px; border:1px solid var(--border); border-radius:8px; }}
  button {{ border:1px solid var(--border); background:#fff; border-radius:8px; padding:8px 12px; cursor:pointer; }}
  button.primary {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
  .note {{ background:#fff8c5; border:1px solid #d4a72c66; border-radius:10px; padding:12px 14px; margin-bottom:12px; font-size:13px; }}
  #viewport {{ background:var(--card); border:1px solid var(--border); border-radius:10px; height:70vh; overflow:auto; }}
  table {{ border-collapse:collapse; width:100%; font-size:12px; }}
  thead th {{ position:sticky; top:0; background:#eef2f6; text-align:left; padding:8px 10px; border-bottom:1px solid var(--border); z-index:1; white-space:nowrap; }}
  tbody td {{ padding:7px 10px; border-bottom:1px solid #eef1f4; vertical-align:top; max-width:420px; word-break:break-word; }}
  tbody tr:hover {{ background:#f3f7fc; }}
  td a {{ color:var(--accent); font-weight:600; text-decoration:none; }}
  @media (max-width:900px) {{ .cards {{ grid-template-columns:repeat(2,1fr); }} }}
</style>
</head>
<body>
<header>
  <h1>Product Experience = Recruiter Experience (RX) - CRM - Core</h1>
  <p>Full entity export · Generated {html.escape(generated)}</p>
  <p><a href="{html.escape(JIRA_FILTER)}" target="_blank" rel="noopener">Open live Jira filter</a></p>
</header>
<main>
  <div class="cards">
    <div class="card"><div class="label">Rows in file</div><div class="value" id="count">{exported:,}</div></div>
    <div class="card"><div class="label">Jira total match</div><div class="value">{EXPECTED_TOTAL:,}</div></div>
    <div class="card"><div class="label">Coverage</div><div class="value">{pct:.1f}%</div></div>
    <div class="card"><div class="label">Columns</div><div class="value" style="font-size:16px;margin-top:10px">ID · ETA · Client · Fix Ver</div></div>
  </div>
  <div class="note">
    Field used: <code>Product Experience: Product2</code> = <code>Recruiter Experience (RX) - CRM - Core</code>.
    Large exports use a virtualized table (renders ~80 rows at a time). Use <strong>Download CSV</strong> for Excel/Sheets.
  </div>
  <div class="toolbar">
    <input id="q" type="search" placeholder="Filter Jira ID, client, fix version, summary, status, project..." />
    <button class="primary" id="dlCsv">Download CSV</button>
    <button id="dlHtml">Download HTML</button>
    <span style="color:var(--muted);font-size:12px">Showing <span id="shown">0</span> matched</span>
  </div>
  <div id="viewport">
    <table>
      <thead>
        <tr>
          <th>JIRA ID</th><th>ETA</th><th>Client</th><th>Fix Version</th>
          <th>Summary</th><th>Status</th><th>Issue Type</th><th>Project</th>
        </tr>
      </thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
</main>
<script id="data" type="application/json">{payload}</script>
<script>
const ALL = JSON.parse(document.getElementById('data').textContent);
const ROW_H = 34;
const BUFFER = 20;
const viewport = document.getElementById('viewport');
const tbody = document.getElementById('tbody');
const shown = document.getElementById('shown');
const q = document.getElementById('q');
let filtered = ALL;
let filterTimer = null;

function esc(s) {{
  return String(s ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
}}

function applyFilter() {{
  const term = q.value.trim().toLowerCase();
  filtered = !term ? ALL : ALL.filter(r => r.join(' ').toLowerCase().includes(term));
  shown.textContent = filtered.length.toLocaleString();
  viewport.scrollTop = 0;
  render();
}}

function render() {{
  const scrollTop = viewport.scrollTop;
  const height = viewport.clientHeight;
  const total = filtered.length;
  const start = Math.max(0, Math.floor(scrollTop / ROW_H) - BUFFER);
  const end = Math.min(total, Math.ceil((scrollTop + height) / ROW_H) + BUFFER);
  const topPad = start * ROW_H;
  const bottomPad = Math.max(0, (total - end) * ROW_H);
  let html = '';
  if (topPad) html += `<tr style="height:${{topPad}}px"><td colspan="8"></td></tr>`;
  for (let i = start; i < end; i++) {{
    const r = filtered[i];
    const key = esc(r[0]);
    html += `<tr>
      <td><a href="https://phenompeople.atlassian.net/browse/${{key}}" target="_blank" rel="noopener">${{key}}</a></td>
      <td>${{esc(r[1])}}</td><td>${{esc(r[2])}}</td><td>${{esc(r[3])}}</td>
      <td>${{esc(r[4])}}</td><td>${{esc(r[5])}}</td><td>${{esc(r[6])}}</td><td>${{esc(r[7])}}</td>
    </tr>`;
  }}
  if (bottomPad) html += `<tr style="height:${{bottomPad}}px"><td colspan="8"></td></tr>`;
  tbody.innerHTML = html;
}}

q.addEventListener('input', () => {{
  clearTimeout(filterTimer);
  filterTimer = setTimeout(applyFilter, 120);
}});
viewport.addEventListener('scroll', () => render(), {{ passive: true }});

document.getElementById('dlCsv').onclick = () => {{
  const headers = ['JIRA ID','ETA','Client','Fix Version','Summary','Status','Issue Type','Project','URL'];
  const lines = [headers.map(h => '"' + h + '"').join(',')];
  for (const r of filtered) {{
    const row = [...r, 'https://phenompeople.atlassian.net/browse/' + r[0]];
    lines.push(row.map(v => '"' + String(v ?? '').replaceAll('"','""') + '"').join(','));
  }}
  const blob = new Blob([lines.join('\\n')], {{ type: 'text/csv;charset=utf-8;' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'rx-crm-core-product-experience-ALL.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}};
document.getElementById('dlHtml').onclick = () => {{
  const blob = new Blob([document.documentElement.outerHTML], {{ type: 'text/html;charset=utf-8;' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'rx-crm-core-product-experience-ALL.html';
  a.click();
  URL.revokeObjectURL(a.href);
}};

shown.textContent = ALL.length.toLocaleString();
render();
</script>
</body>
</html>
"""
    OUT_HTML.write_text(doc, encoding="utf-8")


def main():
    SLICES.mkdir(parents=True, exist_ok=True)
    issues_map = load_issues()
    issues = sorted(issues_map.values(), key=lambda x: x["key"])
    write_csv(issues)
    write_html(issues, len(issues))
    meta = {
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "exportedCount": len(issues),
        "expectedTotal": EXPECTED_TOTAL,
        "coveragePct": round(len(issues) / EXPECTED_TOTAL * 100, 2) if EXPECTED_TOTAL else 0,
        "csv": str(OUT_CSV),
        "html": str(OUT_HTML),
        "sliceFiles": len(list(SLICES.rglob("*"))),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
