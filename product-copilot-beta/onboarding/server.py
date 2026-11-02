#!/usr/bin/env python3
"""Local, read-only onboarding dashboard for Phenom Product Copilot."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import threading
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ONBOARDING_DIR = Path(__file__).resolve().parent
REPO_ROOT = ONBOARDING_DIR.parent
HOME = Path.home()


def run(*args: str, timeout: int = 3) -> tuple[int, str]:
    try:
        result = subprocess.run(
            args,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return result.returncode, (result.stdout or result.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)


def check(
    key: str,
    label: str,
    detail: str,
    state: str,
    *,
    command: str | None = None,
    optional: bool = False,
) -> dict:
    return {
        "key": key,
        "label": label,
        "detail": detail,
        "state": state,
        "command": command,
        "optional": optional,
    }


def token_status() -> tuple[set[str], bool]:
    token_file = HOME / ".copilot" / "tokens.json"
    if not token_file.exists():
        return set(), False
    try:
        data = json.loads(token_file.read_text())
    except (OSError, json.JSONDecodeError):
        return set(), True

    providers: set[str] = set()
    for key, value in data.items():
        if key in {"google", "snowflake", "vanilla"} and isinstance(value, dict):
            if value.get("access_token") or value.get("metadata"):
                providers.add(key)
    return providers, True


def skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(errors="replace")
    metadata: dict[str, str] = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip("\"'")

    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    metadata.setdefault("name", title_match.group(1).strip() if title_match else path.stem)
    if "description" not in metadata:
        body = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
        paragraphs = [
            line.strip()
            for line in body.splitlines()
            if line.strip() and not line.startswith(("#", "|", "-", "`"))
        ]
        metadata["description"] = paragraphs[0] if paragraphs else "Shared Copilot workflow."
    return metadata


def category_for(path: Path, name: str) -> str:
    haystack = f"{path} {name}".lower()
    categories = [
        ("Engineering", ("engineering", "feasibility")),
        ("Design", ("design", "slide")),
        ("Jira", ("jira", "prd", "release", "fire")),
        ("Knowledge", ("knowledge", "google", "snowflake", "vanilla")),
        ("Feedback", ("feedback", "support", "community")),
    ]
    for category, keywords in categories:
        if any(keyword in haystack for keyword in keywords):
            return category
    return "Product"


CATEGORY_BY_KIND = {"policy": "Standards", "agent": "Agents", "command": "Workflows", "skill": "Workflows"}


def catalog() -> list[dict]:
    """Prefer the generated catalog (onboarding/build-catalog.mjs); fall back to parsing skills/ directly."""
    generated = ONBOARDING_DIR / "data" / "catalog.json"
    if generated.exists():
        try:
            data = json.loads(generated.read_text(encoding="utf-8"))
            items = []
            for item in data.get("items", []):
                if item.get("source") != "shared":
                    continue
                category = CATEGORY_BY_KIND.get(item.get("kind"), "Workflows")
                if item.get("requires"):
                    category = {"jira": "Jira", "google": "Google", "snowflake": "Data", "vanilla": "Knowledge base"}.get(
                        item["requires"][0], category
                    )
                items.append(
                    {
                        "name": item["name"],
                        "description": item.get("summary") or item.get("description", ""),
                        "category": category,
                        "path": item["path"],
                        "prompt": item["command"] + " " if item.get("command") else f"Use the {item['name']} skill to help me with ",
                        "command": item.get("command"),
                        "kind": item.get("kind"),
                        "updated": item.get("updated"),
                    }
                )
            if items:
                return items
        except (OSError, ValueError, KeyError):
            pass
    candidates = list((REPO_ROOT / "skills").glob("*.md"))
    candidates.extend((REPO_ROOT / "skills").glob("*/SKILL.md"))
    items: list[dict] = []
    for path in sorted(candidates):
        metadata = skill_frontmatter(path)
        name = metadata["name"]
        rel = path.relative_to(REPO_ROOT)
        items.append(
            {
                "name": name,
                "description": metadata["description"],
                "category": category_for(rel, name),
                "path": str(rel),
                "prompt": f"Use the {name} skill to help me with ",
            }
        )
    return items


def linked_skill_count() -> int:
    """Symlinks in ~/.claude/skills that point into this repo (what onboarding/link-skills.sh creates)."""
    target = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "skills"
    if not target.is_dir():
        return 0
    count = 0
    for link in target.iterdir():
        try:
            if link.is_symlink() and str(link.resolve()).startswith(str((REPO_ROOT / "skills").resolve())):
                count += 1
        except OSError:
            continue
    return count


def engineering_clone_count() -> int:
    """Count configured clone targets without walking 5+ GB of source files."""
    registry = REPO_ROOT / "engineering" / "scripts" / "repos.yaml"
    clone_root = REPO_ROOT / "engineering" / "repos"
    if not registry.exists() or not clone_root.exists():
        return 0

    count = 0
    for line in registry.read_text(errors="replace").splitlines():
        match = re.match(r"^\s+path:\s*(.+?)\s*$", line)
        if not match:
            continue
        relative_path = match.group(1).strip("\"'")
        if (clone_root / relative_path / ".git").is_dir():
            count += 1
    return count


def setup_status() -> dict:
    checks: list[dict] = []

    git_code, branch = run("git", "branch", "--show-current")
    checks.append(
        check(
            "repo",
            "Copilot repository",
            f"Connected on {branch}" if git_code == 0 and branch else "Not opened as a Git repository",
            "ready" if git_code == 0 and branch else "missing",
            command="git status",
        )
    )

    profile = REPO_ROOT / "me.md"
    profile_ready = profile.exists() and profile.stat().st_size > 30
    checks.append(
        check(
            "profile",
            "Personal profile",
            "me.md is present and stays local" if profile_ready else "Add your role, products, and preferences",
            "ready" if profile_ready else "missing",
            command='open "me.md"',
        )
    )

    node_code, node_version = run("node", "--version")
    major_match = re.search(r"(\d+)", node_version)
    node_ready = node_code == 0 and major_match and int(major_match.group(1)) >= 20
    checks.append(
        check(
            "node",
            "Node.js",
            f"{node_version} installed" if node_ready else "Node.js 20 or newer is required",
            "ready" if node_ready else "missing",
            command="brew install node",
        )
    )

    deps_ready = (REPO_ROOT / "mcp" / "node_modules").is_dir()
    checks.append(
        check(
            "mcp-deps",
            "Copilot tools",
            "Local MCP dependencies installed" if deps_ready else "Install local Copilot dependencies",
            "ready" if deps_ready else "missing",
            command="cd mcp && npm install",
        )
    )

    config_ready = (REPO_ROOT / ".cursor" / "mcp.json").exists() or (REPO_ROOT / ".mcp.json").exists()
    checks.append(
        check(
            "mcp-config",
            "Tool connection",
            "Copilot MCP is configured for this workspace" if config_ready else "Add .cursor/mcp.json (Cursor) or .mcp.json (Claude Code)",
            "ready" if config_ready else "missing",
            command='open ".cursor/mcp.json"',
        )
    )

    providers, token_file_exists = token_status()
    provider_labels = {"google": "Google Workspace", "snowflake": "Snowflake", "vanilla": "Vanilla KB"}
    for provider, label in provider_labels.items():
        ready = provider in providers
        detail = "Authenticated" if ready else (
            "Credentials file needs repair" if token_file_exists else "Authentication required"
        )
        is_optional = provider != "google"
        checks.append(
            check(
                provider,
                label,
                detail if ready or not is_optional else f"Optional: {detail.lower()}",
                "ready" if ready else ("optional" if is_optional else "missing"),
                command="cd mcp && npm run setup",
                optional=is_optional,
            )
        )

    clone_count = engineering_clone_count()
    checks.append(
        check(
            "engineering",
            "Engineering context",
            f"{clone_count} local repositories available" if clone_count else "Optional: clone only your product area",
            "ready" if clone_count else "optional",
            command="./engineering/scripts/sync-repos.sh --list",
            optional=True,
        )
    )

    linked = linked_skill_count()
    checks.append(
        check(
            "skills-linked",
            "Slash commands",
            f"{linked} skills linked into Claude Code and Cursor" if linked else "Link the skill folders so /commands appear",
            "ready" if linked else "missing",
            command="bash onboarding/link-skills.sh",
        )
    )

    catalog_file = ONBOARDING_DIR / "data" / "catalog.json"
    head_code, head_time = run("git", "log", "-1", "--format=%ct")
    catalog_fresh = catalog_file.exists() and (
        head_code != 0 or not head_time.strip().isdigit() or catalog_file.stat().st_mtime >= int(head_time.strip())
    )
    checks.append(
        check(
            "catalog",
            "Skill catalog",
            "Catalog is current" if catalog_fresh else ("Catalog is older than the last update" if catalog_file.exists() else "Catalog not built yet"),
            "ready" if catalog_fresh else "attention",
            command="/update-product-os",
            optional=True,
        )
    )

    git_status_code, git_status = run("git", "status", "--porcelain", "--untracked-files=no")
    changed = len(git_status.splitlines()) if git_status_code == 0 else 0
    checks.append(
        check(
            "updates",
            "Shared updates",
            f"{changed} edited file{'s' if changed != 1 else ''}; the update stops until you keep or stash them" if changed else "Ready to update",
            "attention" if changed else "ready",
            command="/update-product-os",
            optional=True,
        )
    )

    required = [item for item in checks if not item["optional"]]
    ready_count = sum(item["state"] == "ready" for item in required)
    return {
        "checks": checks,
        "summary": {
            "ready": ready_count,
            "total": len(required),
            "percent": round(ready_count / len(required) * 100) if required else 0,
        },
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "repository": REPO_ROOT.name,
    }


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ONBOARDING_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        return

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/status":
            self.send_json({**setup_status(), "skills": catalog()})
            return
        if route in {"/", "/dashboard"}:
            self.path = "/index.html"
        super().do_GET()

    def send_json(self, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        # The PM OS site (opened from disk or from productos.phenom.pro) reads this from the browser.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Open the local Copilot onboarding dashboard.")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), DashboardHandler)
    url = f"http://127.0.0.1:{args.port}"
    print(f"Phenom Copilot onboarding: {url}")
    print("Setup data stays on this computer. Press Ctrl+C to stop.")
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
