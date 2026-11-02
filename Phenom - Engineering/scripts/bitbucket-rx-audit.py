#!/usr/bin/env python3
"""
Audit Bitbucket repos against local clones and RX hub/MFE references.

Usage:
  cd "Phenom - Engineering"
  set -a && source .env && set +a
  python3 scripts/bitbucket-rx-audit.py [--json]

Requires: BITBUCKET_EMAIL, BITBUCKET_API_TOKEN in environment (or .env sourced).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ENGINEERING_ROOT = Path(__file__).resolve().parent.parent
REPOS_YAML = ENGINEERING_ROOT / "scripts" / "repos.yaml"
REPOS_ROOT = ENGINEERING_ROOT / "repos"
CP_UI = REPOS_ROOT / "recruiter-hub" / "cp_ui_app_2.0" / "src"

# Hub API prefixes from cp_ui_app_2.0 (crmHub routes) — production runtime paths
HUB_API_PREFIXES = [
    "candidate-assessment-service", "candidates-api", "crm-automation-service",
    "crm-config-service", "crm-events2", "crm-hiring-status-service",
    "crm-profile-search-service", "crm-search-service", "crm-settings-service",
    "crm-utility-service", "dna-etg", "ecampaign", "email-facade-service",
    "events", "events-config", "events-registration", "facets2", "gdpr",
    "hrm-core-api", "hrm-offer-management-api", "hrm-profile-api",
    "hvh-common-service", "interview-evaluations", "interview-schedule",
    "jobs-api", "lists", "messaging-gateway-service", "microservice-api",
    "notes-api", "notifications", "ops-api-service", "projects-workflows",
    "pup", "scheduling-api-gateway", "sms-service", "spx-utils",
    "tags-service", "tenant-config", "user-preferences", "xplus-gateway",
]

# MFE remoteName values from mfe.config.ts (product UI surfaces in RX shell)
MFE_REMOTES = [
    "applyStudio", "automations", "bgvApp", "crm-ai-cloud-sourcing",
    "crm-boolean-search", "crm-campaigns-ui", "crm-candidates-ui",
    "crm-events-ui", "crm-feature-flags", "crm-filters", "crm-global-search",
    "crm-jobs-ui", "crm-lists-ui", "crm-projects-ui", "crm-templates-ui",
    "crmNotes", "eSign", "fit-score", "hiringManager", "inbox", "nps_ui",
    "offer", "onboarding", "recruiter-dashboard", "requisition",
    "scheduling-pluggable-frontend", "xplus-apps-ui",
]

# Likely Bitbucket slug for hub prefix (when 1:1 mapping isn't obvious)
HUB_TO_LIKELY_SLUG = {
    "lists": "crm-candidate-lists",
    "gdpr": "crm-gdpr",
    "jobs-api": "crm-jobs-service",
    "facets2": "cp-facet-2.0",
    "microservice-api": "candidates-microservice",
    "notes-api": "notes-service",
    "crm-search-service": "crm-domain-search-service",
    "sms-service": "candidates-sms-services",
    "notifications": "candidates-notifications",
    "messaging-gateway-service": "crm-messaging-platform",
}

# Tier A/B/C recommendations — slug verified against Bitbucket where possible
RX_PRIORITY_CLONES = [
    ("crm-candidates-ui", "A", "Candidate profile/list/edit UI — core RX"),
    ("candidates-api", "A", "Core candidate backend API"),
    ("crm-jobs-service", "A", "Jobs backend (hub path: jobs-api)"),
    ("crm-jobs-ui", "A", "Job workspace UI MFE"),
    ("hrm-profile-api", "A", "HRM profile API"),
    ("candidates-microservice", "A", "Hub path: microservice-api — edit/merge/bulk ops"),
    ("crm-hiring-status-service", "B", "Hiring pipeline / status"),
    ("crm-profile-search-service", "B", "Profile search"),
    ("crm-domain-search-service", "B", "CRM domain search (hub: crm-search-service)"),
    ("crm-filters-ui", "B", "Filters/facets UI MFE"),
    ("crm-lists-ui", "B", "Lists UI MFE (backend: crm-candidate-lists)"),
    ("crm-settings-service", "B", "CRM settings hub"),
    ("notes-service", "B", "Notes API (hub: notes-api); UI: crm-notes-ui"),
    ("tags-service", "B", "Candidate tags"),
    ("crm-projects-ui", "B", "Projects UI"),
    ("crm-gdpr", "C", "GDPR / privacy in CRM"),
    ("crm-global-search-ui", "C", "Global search UI MFE"),
    ("crm-data-access-layer", "C", "Shared CRM data access"),
]

# Exclude from clone recommendations (infra/QA/charts)
SKIP_PATTERNS = re.compile(
    r"(helm|chart|qa-|test-|automation$|e2e|playwright|robot|"
    r"config-commons|offline-apis|v2-helm|crm-charts)",
    re.I,
)


def bitbucket_get(url: str) -> dict:
    email = os.environ.get("BITBUCKET_EMAIL")
    token = os.environ.get("BITBUCKET_API_TOKEN")
    if not email or not token:
        sys.exit("Missing BITBUCKET_EMAIL or BITBUCKET_API_TOKEN. Run: set -a && source .env && set +a")
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def fetch_repos(query: str) -> list[dict]:
    repos: list[dict] = []
    q = urllib.parse.quote(query)
    url = (
        "https://api.bitbucket.org/2.0/repositories/phenompeople"
        f"?q={q}&pagelen=100&sort=-updated_on"
        f"&fields=values.name,values.slug,values.updated_on,next"
    )
    while url:
        data = bitbucket_get(url)
        repos.extend(data.get("values", []))
        url = data.get("next")
    return repos


def parse_repos_yaml() -> set[str]:
    names: set[str] = set()
    if not REPOS_YAML.exists():
        return names
    for line in REPOS_YAML.read_text().splitlines():
        m = re.match(r"\s*-\s*name:\s*(.+)", line)
        if m:
            names.add(m.group(1).strip())
    return names


def local_clones() -> set[str]:
    clones: set[str] = set()
    if not REPOS_ROOT.exists():
        return clones
    for git_dir in REPOS_ROOT.rglob(".git"):
        if git_dir.is_dir():
            clones.add(git_dir.parent.name)
    return clones


def main() -> None:
    parser = argparse.ArgumentParser(description="Bitbucket RX/CRM repo audit")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    # Gather Bitbucket catalog
    by_slug: dict[str, dict] = {}
    for query in [
        'name~"crm"', 'name~"rx"', 'name~"candidates-api"', 'name~"jobs-api"',
        'name~"hrm-profile"', 'name~"microservice"', 'name~"notes"', 'name~"tags-service"',
        'name~"cp_ui"', 'name~"candidates-microservice"', 'name~"domain-search"',
    ]:
        for r in fetch_repos(query):
            by_slug[r["slug"]] = r

    yaml_repos = parse_repos_yaml()
    cloned = local_clones()

    priority_results = []
    for slug, tier, reason in RX_PRIORITY_CLONES:
        in_bb = slug in by_slug
        in_yaml = slug in yaml_repos
        on_disk = slug in cloned
        priority_results.append({
            "slug": slug,
            "tier": tier,
            "reason": reason,
            "bitbucket": in_bb,
            "repos_yaml": in_yaml,
            "cloned": on_disk,
            "updated_on": by_slug.get(slug, {}).get("updated_on"),
        })

    # CRM repos on Bitbucket not in workspace (excluding skip patterns)
    crm_all = fetch_repos('name~"crm"')
    missing_crm = []
    for r in crm_all:
        slug = r["slug"]
        if slug in cloned or slug in yaml_repos:
            continue
        if SKIP_PATTERNS.search(slug):
            continue
        missing_crm.append({"slug": slug, "updated_on": r.get("updated_on")})

    report = {
        "summary": {
            "bitbucket_crm_count": len(crm_all),
            "bitbucket_unique_catalog": len(by_slug),
            "repos_yaml_count": len(yaml_repos),
            "local_clone_count": len(cloned),
            "hub_api_prefixes": len(HUB_API_PREFIXES),
            "mfe_remotes": len(MFE_REMOTES),
        },
        "rx_priority_clones": priority_results,
        "missing_crm_on_bitbucket_sample": missing_crm[:40],
        "rx_named_repos_bitbucket": sorted(r["slug"] for r in fetch_repos('name~"rx"')),
        "hub_api_prefixes": HUB_API_PREFIXES,
        "mfe_remotes": MFE_REMOTES,
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return

    print("# RX Platform — Bitbucket Audit\n")
    print(f"Bitbucket CRM repos: {report['summary']['bitbucket_crm_count']}")
    print(f"Local clones: {report['summary']['local_clone_count']}")
    print(f"In repos.yaml: {report['summary']['repos_yaml_count']}\n")

    print("## Priority clone candidates (Tier A/B/C)\n")
    print("| Tier | Slug | Bitbucket | repos.yaml | Cloned | Notes |")
    print("|------|------|-----------|------------|--------|-------|")
    for p in priority_results:
        bb = "yes" if p["bitbucket"] else "**missing**"
        y = "yes" if p["repos_yaml"] else "no"
        c = "yes" if p["cloned"] else "no"
        print(f"| {p['tier']} | `{p['slug']}` | {bb} | {y} | {c} | {p['reason']} |")

    print("\n## RX-named Bitbucket repos (not the main CRM UI stack)\n")
    for s in report["rx_named_repos_bitbucket"]:
        print(f"- `{s}`")

    print("\n## Recent CRM repos on Bitbucket NOT yet cloned (sample, infra excluded)\n")
    for m in missing_crm[:25]:
        print(f"- `{m['slug']}` (updated {m['updated_on'][:10] if m.get('updated_on') else '?'})")

    tier_a_missing = [p for p in priority_results if p["tier"] == "A" and not p["cloned"]]
    print(f"\n## Recommended next action: clone Tier A ({len(tier_a_missing)} repos)\n")
    for p in tier_a_missing:
        print(f"  - {p['slug']}")


if __name__ == "__main__":
    main()
