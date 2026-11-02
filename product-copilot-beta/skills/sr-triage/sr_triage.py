#!/usr/bin/env python3
"""Deterministic helpers for the sr-triage agent (no LLM calls here).

  context  <sheet.xlsx> <out.json>             allowed values: Jira products (jira-constants.md), scope, L1, L2 per product
  batches  <sheet.xlsx> <outdir> [--all] [--size 40] [--version v1] [--ids ids.json] [--include-reviewed]
                                               ticket batches to classify (default: rows without a current-version recommendation,
                                               never rows a PM marked reviewed)
  validate <context.json> <labels.jsonl>       check agent output against the allowed values; prints a report, exits 1 on hard errors
  lint-details <sheet.xlsx | labels.jsonl>     count Details cells that break knowledge/service-request-analysis/_shared/details-format.md
  validate-child <labels.jsonl>                check child-only output: {id, jira_classification, jira_classification_child, child_confidence, child_reason}
"""
import json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
COPILOT = os.path.abspath(os.path.join(HERE, '..', '..'))
JIRA_CONSTANTS = os.path.join(COPILOT, 'policies', 'jira-constants.md')
SCOPE = os.path.join(COPILOT, 'knowledge', 'service-request-analysis', 'scope.json')
RULEBOOK = os.path.join(COPILOT, 'knowledge', 'service-request-analysis', 'rulebook.md')

TYPES = ['Service Request', 'Bug-Customer']
JIRA_CLASSES = ['Code Issues', 'User Experience Issues', 'Product & Knowledge Issues', 'Configuration Issues',
                'External Dependency Issues', 'Ops Issues']
L1 = ['Access & permissions', 'Data & records', 'Configuration & setup', 'Workflows & automations', 'Communications',
      'Integrations & sync', 'Experience surfaces', 'Insights & reporting', 'Content & localization', 'Reliability & performance']
COHERENT = {'Bug-Customer': {'Code Issues', 'User Experience Issues', 'External Dependency Issues', 'Ops Issues'},
            'Service Request': {'Product & Knowledge Issues', 'Configuration Issues', 'External Dependency Issues'}}
REC = 'Recommendation\n'

# Jira Ticket Classification children (knowledge/service-request-analysis/_shared/ticket-classification.md).
# First the values used on tickets, then Confluence-only values (valid, but not preferred).
CHILDREN = {
    'Product & Knowledge Issues': ['Documentation', 'Non-intuitive Product Behaviour', 'Self-Service Missing', 'Product Requirement',
                                   'Usability, Value KPIs missing', 'Inter Product Dependency'],
    'Configuration Issues': ['Configuration Error', 'Config Move Miss', 'Incorrect Discovery', 'Configuration Missed', 'Wrong Configuration'],
    'Code Issues': ['Functionality', 'Data Quality', 'Data Synchronization', 'Data Pipeline', 'Data Dependency', 'Data Loss', 'Performance',
                    'API', 'Accessibility', 'Customization', 'Accuracy', 'Localisation/I8n', 'Prompt', 'Security'],
    'User Experience Issues': ['Layout', 'Navigation', 'User Flow & Task Completion', 'Accessibility', 'Responsiveness', 'Content & Microcopy',
                               'Localisation / i18n'],
    'External Dependency Issues': ['API Failure', 'API Timeout', 'Invalid API Response', 'Library, Framework Dependency', 'SFTP Issue', 'Webhook Issue'],
    'Ops Issues': ['Infra Scaling - Capacity planning', 'Incorrect Infra Configuration', 'CI/CD Pipeline'],
}
CHILD_FIX = {'Non-intutive Product Behaviour': 'Non-intuitive Product Behaviour', 'Localization / i18n': 'Localisation / i18n', 'Accesibility': 'Accessibility'}
# rule id -> (parent, child) the rule implies (rulebook §5, tier 2). O-AUTO-LATE depends on the parent, handled in rule_child().
RULE_CHILD = {
    'O-CAPABILITY': ('Product & Knowledge Issues', 'Product Requirement'),
    'O-SELF-SERVICE': ('Product & Knowledge Issues', 'Self-Service Missing'),
    'O-HOWTO': ('Product & Knowledge Issues', 'Documentation'),
    'O-PROD-CONFIG': ('Configuration Issues', 'Config Move Miss'),
    'O-FLAG': ('Configuration Issues', 'Configuration Error'),
    'O-SEED': ('Configuration Issues', 'Configuration Error'),
    'O-HOWTO-CHANGE': ('Configuration Issues', 'Configuration Error'),
    'O-BUILDER-FIELD': ('Code Issues', 'Functionality'),
    'O-UI-MISSING': ('Code Issues', 'Functionality'),
    'O-SYNC-FAIL': ('Code Issues', 'Data Synchronization'),
    'O-NULL-FILTER': ('Code Issues', 'Data Quality'),
}


def norm_filed(parent, child):
    """Filed (Jira / ServiceNow) parent and child, spelling-normalised; Security-Related Issues -> Code Issues / Security."""
    parent, child = s(parent), CHILD_FIX.get(s(child), s(child))
    if parent == 'Security-Related Issues': return 'Code Issues', 'Security'
    return parent, child


def rule_child(parent, rules):
    """Tier 2: the child a recorded rule implies for this parent, else ('', '')."""
    for r in rules:
        if r == 'O-AUTO-LATE':
            if parent == 'Ops Issues': return 'Infra Scaling - Capacity planning', r
            if parent == 'Code Issues': return 'Data Synchronization', r
        hit = RULE_CHILD.get(r)
        if hit and hit[0] == parent: return hit[1], r
    return '', ''


def s(v):
    v = '' if v is None else str(v).strip()
    return '' if v == 'None' else v


def rulebook_version():
    m = re.search(r'\*\*Version:\*\*\s*(v\d+)', open(RULEBOOK).read())
    return m.group(1) if m else 'v?'


def jira_products():
    """{experience: [product, ...]} parsed from the Product Experience : Product tables in jira-constants.md."""
    out, cur = {}, None
    for line in open(JIRA_CONSTANTS):
        m = re.match(r'####\s+(.+?)\s+—\s+parent', line)
        if m:
            name = m.group(1).strip()
            cur = None if name.startswith('Z - ') else name
            if cur: out[cur] = []
            continue
        if line.startswith('### '): cur = None
        if cur and line.startswith('|') and not re.match(r'\|\s*(Product|-{2,})', line):
            prod = line.split('|')[1].strip()
            if prod: out[cur].append(prod)
    return out


def sheet_rows(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    rows = list(wb['Tickets'].iter_rows(values_only=True))
    head = [s(x) for x in rows[1]]
    col = {h: i for i, h in enumerate(head) if h}
    return wb, rows, col


def cmd_context(xlsx, out):
    wb, _, _ = sheet_rows(xlsx)
    products = jira_products()
    scope = json.load(open(SCOPE))
    tax_rows = list(wb['Product Taxonomy'].iter_rows(values_only=True))
    hdr = next(i for i, r in enumerate(tax_rows) if r and s(r[0]) == 'Product Experience' and s(r[1]) == 'Product Area')
    alias = {'Roles & Access Management': 'CRM - Role & Access Management', 'CRM - Events': 'CRM - Events and University Recruiting'}
    l2 = collections.defaultdict(list)
    for r in tax_rows[hdr + 1:]:
        if not r or not s(r[3]) or s(r[6]) not in ('active', 'proposed'): continue
        if s(r[2]) not in L1: continue          # skips the retired "Triage quality" placeholder
        prod = alias.get(s(r[1]), s(r[1]))
        l2[prod].append({'l1': s(r[2]), 'l2': s(r[3]), 'description': s(r[4]), 'examples': s(r[5]), 'status': s(r[6])})
    l1defs = {}
    const = list(wb['Constants'].iter_rows(values_only=True))
    start = next(i for i, r in enumerate(const) if r and r[0] and 'Product Categories' in str(r[0]))
    for r in const[start + 1:]:
        if r and len(r) > 1 and s(r[0]) in L1: l1defs[s(r[0])] = s(r[1])
    ctx = {'rulebook_version': rulebook_version(), 'types': TYPES, 'jira_classifications': JIRA_CLASSES, 'l1': L1,
           'l1_definitions': l1defs, 'products': products, 'scope': scope, 'l2_by_product': l2}
    json.dump(ctx, open(out, 'w'), ensure_ascii=False, indent=1)
    print(f"context {out}: {sum(len(v) for v in products.values())} Jira products in {len(products)} experiences, "
          f"{sum(len(v) for v in l2.values())} L2 rows for {len(l2)} products, rulebook {ctx['rulebook_version']}")


def part(t, name, n):
    m = re.search(name + r':\s*(.*?)(?:\n\n(?:Problem|Discussions|Solution):|\Z)', t or '', re.S)
    x = m.group(1).strip() if m else ''
    return x[:n]


def cmd_batches(xlsx, outdir, all_rows=False, size=40, version=None, only_ids=None, include_reviewed=False):
    version = version or rulebook_version()
    _, rows, col = sheet_rows(xlsx)
    g = lambda r, n: s(r[col[n]]) if n in col and col[n] < len(r) else ''
    os.makedirs(outdir, exist_ok=True)
    picked, seen = [], set()
    for r in rows[2:]:
        if not any(r): continue
        j = (re.findall(r'[A-Z][A-Z0-9]*-\d+', g(r, 'JIRA ID')) or [''])[-1]
        tid = g(r, 'Service Now ID') or j
        if not tid or tid in seen: continue
        seen.add(tid)
        if only_ids is not None and tid not in only_ids: continue
        reviewed = g(r, REC + 'Status').lower() == 'reviewed'
        if reviewed and not include_reviewed: continue
        if not all_rows and f'rulebook {version}' in g(r, 'matched_rules'): continue
        det = g(r, 'Details')
        issues = detail_issues(det)
        locked = {'product_experience': g(r, REC + 'Product Experience'), 'product': g(r, REC + 'Product Area'), 'l1': g(r, REC + 'L1 - Category'), 'l2': g(r, REC + 'L1 - Sub-Category'), 'type': g(r, REC + 'Ticket Type')} if reviewed else None
        picked.append({'id': tid, 'summary': g(r, 'Summary'), 'pm_locked': locked, 'details_needs_rewrite': bool(issues), 'details_issues': issues,
                       
                       'details_full': det[:12000],  # full SN + Jira narrative; classify from this, never from a truncated slice
                       'filed': {'sn_component': g(r, 'SN - Component'), 'sn_subcomponent': g(r, 'SN - Sub-Component'),
                                 'sn_request_category': g(r, 'SN - Request Category'), 'jira_product_area': g(r, 'JIRA - Product Area'),
                                 'jira_type': g(r, 'JIRA - Type of Issue/Request'), 'jira_status': g(r, 'JIRA - Status')}})
    n = 0
    for i in range(0, len(picked), size):
        n += 1
        with open(os.path.join(outdir, f'batch-{n:03d}.jsonl'), 'w') as f:
            f.write('\n'.join(json.dumps(x, ensure_ascii=False) for x in picked[i:i + size]) + '\n')
    print(f'{len(picked)} tickets to classify in {n} batches of up to {size} -> {outdir}')


DETAIL_RULES = [
    ('markup tag', re.compile(r'<custom data-type|</custom>|data-id=')),
    ('@mention', re.compile(r'(^|\s)@[A-Z][a-z]+')),
    ('per-comment name/date prefix', re.compile(r'\[\d{4}-\d\d-\d\d\]\s+[A-Z][^:]{2,40}:')),
    ('boilerplate closure', re.compile(r'closing this Service Request \(SR\) in Jira', re.I)),
    ('url', re.compile(r'https?://')),
    ('email address', re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')),
    ('empty template field', re.compile(r'^(Client ask|Note|Ref number|Issue replication|By Support)\s*:\s*(NA|N/A|Yes)?\s*$', re.I | re.M)),
    ('machine paste', re.compile(r'ISODate\(|ObjectId\(|JIRA USER\s*:|JIRA COMMENT\s*:')),
    ('credential or secret', re.compile(r'client_?secret|api[_ -]?key\s*[:=]|password\s*[:=]|bearer\s+[A-Za-z0-9._-]{20,}|\b[0-9a-f]{32}\b', re.I)),
]


def detail_issues(text):
    t = text or ''
    out = [name for name, rx in DETAIL_RULES if rx.search(t)]
    if len(t.split()) > 150: out.append('over 150 words')
    if not all(k in t for k in ('Problem:', 'Discussions:', 'Solution:')): out.append('missing section label')
    return out


def cmd_lint_details(path):
    texts = []
    if path.endswith('.jsonl'):
        texts = [(o['id'], o.get('details', '')) for o in (json.loads(l) for l in open(path) if l.strip())]
    else:
        _, rows, col = sheet_rows(path)
        g = lambda r, n: s(r[col[n]]) if n in col and col[n] < len(r) else ''
        seen = set()
        for r in rows[2:]:
            tid = g(r, 'Service Now ID') or (re.findall(r'[A-Z][A-Z0-9]*-\d+', g(r, 'JIRA ID')) or [''])[-1]
            if tid and tid not in seen: seen.add(tid); texts.append((tid, g(r, 'Details')))
    bad = [(t, detail_issues(x)) for t, x in texts]
    bad = [(t, i) for t, i in bad if i]
    c = collections.Counter(x for _, i in bad for x in i)
    print(f'{len(texts)} rows · {len(bad)} need a rewrite ({100 * len(bad) // max(1, len(texts))}%)')
    for k, v in c.most_common(): print(f'  {v:5d}  {k}')
    return {t for t, _ in bad}


def cmd_validate(ctx_path, labels_path):
    ctx = json.load(open(ctx_path))
    prod_pe = {p: pe for pe, ps in ctx['products'].items() for p in ps}
    hard, soft, n = [], [], 0
    for ln in open(labels_path):
        if not ln.strip(): continue
        n += 1
        o = json.loads(ln); tid = o.get('id', '?')
        def bad(msg): hard.append(f'{tid}: {msg}')
        if not isinstance(o.get('pm_review'), bool): bad(f"pm_review must be a JSON boolean, got {o.get('pm_review')!r}")
        if not isinstance(o.get('rules'), list): bad(f"rules must be a JSON array, got {o.get('rules')!r}")
        if o.get('type') not in TYPES: bad(f"type {o.get('type')!r}")
        if o.get('jira_classification') not in JIRA_CLASSES: bad(f"jira_classification {o.get('jira_classification')!r}")
        if o.get('product') not in prod_pe: bad(f"product {o.get('product')!r} not in jira-constants.md")
        elif prod_pe[o['product']] != o.get('product_experience'): bad(f"product {o['product']!r} belongs to {prod_pe[o['product']]!r}, not {o.get('product_experience')!r}")
        if o.get('l1') not in L1: bad(f"l1 {o.get('l1')!r}")
        l2s = {(x['l1'], x['l2']) for x in ctx['l2_by_product'].get(o.get('product'), [])}
        if l2s and (o.get('l1'), o.get('l2')) not in l2s: bad(f"l2 {o.get('l2')!r} is not an active/proposed {o.get('l1')} L2 of {o.get('product')}")
        if o.get('confidence') not in ('high', 'medium', 'low'): bad(f"confidence {o.get('confidence')!r}")
        if o.get('jira_classification_child') and o.get('jira_classification_child') not in CHILDREN.get(o.get('jira_classification'), []):
            bad(f"jira_classification_child {o.get('jira_classification_child')!r} is not a child of {o.get('jira_classification')!r}")
        if o.get('details'):
            di = detail_issues(o['details'])
            if di: bad(f"details still breaks the format: {', '.join(di)}")
        # Bug-Customer + Configuration is valid for a production config regression (O-PROD-CONFIG, PM decision 2026-10-05)
        regression = o.get('type') == 'Bug-Customer' and o.get('jira_classification') == 'Configuration Issues' and 'O-PROD-CONFIG' in (o.get('rules') or [])
        if o.get('type') in COHERENT and o.get('jira_classification') not in COHERENT[o['type']] and o.get('pm_review') is False and not regression:
            hard.append(f"{tid}: {o.get('type')} + {o.get('jira_classification')} requires pm_review=true")
    print(f'{n} rows · {len(hard)} hard errors · {len(soft)} warnings')
    for x in hard[:50]: print('  ERROR', x)
    for x in soft[:20]: print('  WARN ', x)
    sys.exit(1 if hard else 0)


def cmd_validate_child(labels_path):
    hard, n = [], 0
    for ln in open(labels_path):
        if not ln.strip(): continue
        n += 1; o = json.loads(ln); tid = o.get('id', '?'); p = o.get('jira_classification')
        if p not in CHILDREN: hard.append(f'{tid}: parent {p!r}'); continue
        if o.get('jira_classification_child') not in CHILDREN[p]: hard.append(f"{tid}: child {o.get('jira_classification_child')!r} is not a child of {p}")
        if o.get('child_confidence') not in ('high', 'medium', 'low'): hard.append(f"{tid}: child_confidence {o.get('child_confidence')!r}")
    print(f'{n} rows · {len(hard)} hard errors')
    for x in hard[:50]: print('  ERROR', x)
    sys.exit(1 if hard else 0)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(2)
    if a[0] == 'context': cmd_context(a[1], a[2])
    elif a[0] == 'batches':
        cmd_batches(a[1], a[2], all_rows='--all' in a, size=int(a[a.index('--size') + 1]) if '--size' in a else 40,
                    version=a[a.index('--version') + 1] if '--version' in a else None,
                    only_ids=set(json.load(open(a[a.index('--ids') + 1]))) if '--ids' in a else None,
                    include_reviewed='--include-reviewed' in a)
    elif a[0] == 'validate': cmd_validate(a[1], a[2])
    elif a[0] == 'lint-details': cmd_lint_details(a[1])
    elif a[0] == 'validate-child': cmd_validate_child(a[1])
    else: print(__doc__); sys.exit(2)
