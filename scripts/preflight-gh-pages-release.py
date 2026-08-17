#!/usr/bin/env python
"""Block unsafe legacy GitHub Pages releases before the single gh-pages push.

Usage:
  python scripts/preflight-gh-pages-release.py ../korea-public-benefit-brief-pages

The target must be the already-rendered static worktree. This script does not
write, stage, commit, or push files. It reports release-blocking problems so a
publisher can fix the complete artifact before making one atomic gh-pages push.
"""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_ROOT_FILES = (".nojekyll", "index.html", "feed.xml", "sitemap.xml")
BLOCKED_FILE_NAMES = {".DS_Store"}
BLOCKED_SUFFIXES = {".pyc", ".pyo"}
BLOCKED_DIR_NAMES = {"__pycache__"}


def blocked_paths(pages_root: Path) -> list[Path]:
    """Return generated/runtime artifacts that must never reach gh-pages."""
    found: list[Path] = []
    for path in pages_root.rglob("*"):
        if path.name in BLOCKED_DIR_NAMES or path.name in BLOCKED_FILE_NAMES or path.suffix in BLOCKED_SUFFIXES:
            found.append(path)
    return sorted(found)


def build_checks(pages_root: Path) -> list[tuple[str, bool, str]]:
    """Build pure filesystem checks so tests can cover the release gate."""
    checks: list[tuple[str, bool, str]] = []
    checks.append(("PAGES_ROOT_EXISTS", pages_root.is_dir(), str(pages_root)))
    if not pages_root.is_dir():
        return checks

    for name in REQUIRED_ROOT_FILES:
        path = pages_root / name
        checks.append((f"REQUIRED_{name}", path.is_file(), str(path.relative_to(pages_root))))

    bad = blocked_paths(pages_root)
    detail = ", ".join(str(path.relative_to(pages_root)) for path in bad) or "none"
    checks.append(("NO_RUNTIME_ARTIFACTS", not bad, detail))
    return checks


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: preflight-gh-pages-release.py <rendered-pages-root>", file=sys.stderr)
        return 2

    pages_root = Path(sys.argv[1]).resolve()
    failed = False
    for name, ok, detail in build_checks(pages_root):
        print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
        failed = failed or not ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
