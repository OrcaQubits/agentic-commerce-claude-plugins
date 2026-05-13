#!/usr/bin/env python3
"""Publish all converted plugins (and optionally individual skills) to ClawHub.

ClawHub publishing is done via the `clawhub` CLI. Two granularities are
supported:

  - **Bundle plugins** — each plugin in ``dist/openclaw/<plugin>`` is published
    as a single ``bundle-plugin`` package. Users install one slug to get the
    whole plugin (all its skills + AGENTS.md context).

  - **Skills** — each ``SKILL.md`` is published as an independent slug-addressable
    skill via ``clawhub sync``. Users install one slug to get one skill.

This script wraps both flows and supports ``--dry-run``.

Prerequisites:
  - ``clawhub`` CLI installed: ``npm i -g clawhub``
  - Authenticated: ``clawhub login`` (browser) or ``clawhub login --token clh_…``
  - Conversion already run: ``python scripts/convert.py --platform openclaw``

Usage:
    python scripts/publish-clawhub.py                           # publish everything (plugins + skills)
    python scripts/publish-clawhub.py --mode plugins            # bundles only
    python scripts/publish-clawhub.py --mode skills             # individual skills only
    python scripts/publish-clawhub.py --plugin spree-commerce   # one plugin
    python scripts/publish-clawhub.py --dry-run                 # preview without uploading
    python scripts/publish-clawhub.py --owner orcaqubits        # scope owner
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_OPENCLAW = REPO_ROOT / "dist" / "openclaw"
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def load_plugins() -> list[str]:
    """Return the list of plugin names from marketplace.json."""
    with open(MARKETPLACE, encoding="utf-8") as f:
        data = json.load(f)
    return [p["name"] for p in data.get("plugins", [])]


def check_clawhub_cli() -> None:
    if shutil.which("clawhub") is None and shutil.which("clawhub.cmd") is None:
        print(
            "ERROR: 'clawhub' CLI not found in PATH. Install with: npm i -g clawhub",
            file=sys.stderr,
        )
        sys.exit(1)


def check_clawhub_auth() -> None:
    """Run ``clawhub whoami`` to verify the user is logged in."""
    result = subprocess.run(
        ["clawhub", "whoami"], capture_output=True, text=True, check=False,
        shell=sys.platform == "win32",
    )
    if result.returncode != 0:
        print(
            "ERROR: Not authenticated with ClawHub. Run 'clawhub login' first.",
            file=sys.stderr,
        )
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    print(f"Authenticated as: {result.stdout.strip()}")


def publish_plugin(plugin_name: str, *, owner: str | None, dry_run: bool) -> bool:
    """Publish one plugin as a bundle-plugin. Returns True on success."""
    plugin_dir = DIST_OPENCLAW / plugin_name
    if not plugin_dir.is_dir():
        print(f"  [skip] {plugin_name}: {plugin_dir} not found")
        return False

    pkg_json = plugin_dir / "package.json"
    if not pkg_json.is_file():
        print(f"  [skip] {plugin_name}: no package.json (re-run convert.py first)")
        return False

    cmd = [
        "clawhub",
        "package",
        "publish",
        str(plugin_dir),
        "--family",
        "bundle-plugin",
    ]
    if owner:
        cmd += ["--owner", owner]
    if dry_run:
        cmd.append("--dry-run")

    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, check=False, shell=sys.platform == "win32")
    return result.returncode == 0


def publish_skills_for_plugin(plugin_name: str, *, dry_run: bool) -> bool:
    """Run ``clawhub sync`` against one plugin's ``skills/`` directory.

    ``clawhub sync`` expects ``--workdir`` to be a directory containing a
    ``skills/`` subdirectory; it does not recurse multi-plugin trees. So we
    invoke it once per plugin.
    """
    plugin_dir = DIST_OPENCLAW / plugin_name
    if not (plugin_dir / "skills").is_dir():
        return True  # nothing to do — not a failure

    cmd = [
        "clawhub",
        "--workdir", str(plugin_dir),
        "--dir", "skills",
        "sync",
    ]
    if dry_run:
        cmd.append("--dry-run")
    else:
        cmd.append("--all")

    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, check=False, shell=sys.platform == "win32")
    return result.returncode == 0


def publish_skills(*, dry_run: bool, only_plugin: str | None = None) -> bool:
    """Sync skills across every plugin (or just one)."""
    plugins = [only_plugin] if only_plugin else load_plugins()
    all_ok = True
    for name in plugins:
        print(f"\n[skills: {name}]")
        ok = publish_skills_for_plugin(name, dry_run=dry_run)
        all_ok = all_ok and ok
    return all_ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=["plugins", "skills", "all"],
        default="all",
        help="What to publish (default: all)",
    )
    parser.add_argument(
        "--plugin",
        help="Publish only one plugin by name (implies --mode plugins for the package step)",
    )
    parser.add_argument("--owner", help="ClawHub owner/scope (e.g. orcaqubits)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    parser.add_argument(
        "--skip-auth-check",
        action="store_true",
        help="Skip 'clawhub whoami' check (useful for offline dry-runs)",
    )
    args = parser.parse_args()

    check_clawhub_cli()
    if not args.skip_auth_check and not args.dry_run:
        check_clawhub_auth()

    if not DIST_OPENCLAW.is_dir():
        print(
            f"ERROR: {DIST_OPENCLAW} not found. Run "
            "'python scripts/convert.py --platform openclaw' first.",
            file=sys.stderr,
        )
        return 1

    successes: list[str] = []
    failures: list[str] = []

    # 1. Bundle plugins
    if args.mode in ("plugins", "all"):
        if args.plugin:
            plugins = [args.plugin]
        else:
            plugins = load_plugins()

        print(f"\n=== Publishing {len(plugins)} plugin(s) as bundle-plugin ===")
        for name in plugins:
            print(f"\n[{name}]")
            ok = publish_plugin(name, owner=args.owner, dry_run=args.dry_run)
            (successes if ok else failures).append(f"plugin:{name}")

    # 2. Individual skills via sync — one invocation per plugin's skills/ dir
    if args.mode in ("skills", "all"):
        print("\n=== Publishing individual skills via 'clawhub sync' (per plugin) ===")
        ok = publish_skills(dry_run=args.dry_run, only_plugin=args.plugin)
        (successes if ok else failures).append("skills-sync")

    print("\n=== Summary ===")
    print(f"  succeeded: {len(successes)}")
    for s in successes:
        print(f"    + {s}")
    if failures:
        print(f"  failed:    {len(failures)}")
        for f in failures:
            print(f"    - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
