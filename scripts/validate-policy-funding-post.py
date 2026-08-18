#!/usr/bin/env python
"""Quality gate for new policy-funding briefs.

Usage:
  python scripts/validate-policy-funding-post.py _posts/YYYY-MM-DD-slug.md

The gate is intentionally narrow: it applies only to posts categorized as
`funding`. It requires multiple official sources and at least one official
link in the explanatory body, not only in the final source list.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

TRUSTED_OFFICIAL_HOSTS = (
    "bizinfo.go.kr",
    "k-startup.go.kr",
    "semas.or.kr",
    "kosmes.or.kr",
    "kibo.or.kr",
    "kodit.co.kr",
    "smes.go.kr",
    "go.kr",
    "korea.kr",
)


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    parts = text.split("\n---\n", 1)
    return (parts[0][4:], parts[1]) if len(parts) == 2 else ("", text)


def urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s)\]>]+", text)


def is_trusted(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == domain or host.endswith(f".{domain}") for domain in TRUSTED_OFFICIAL_HOSTS)


def build_checks(post_path: Path) -> list[tuple[str, bool, str]]:
    text = post_path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(text)
    categories = re.search(r"^categories:\s*\[(.*?)\]\s*$", front_matter, flags=re.M)
    is_funding = bool(categories and "funding" in {x.strip().lower() for x in categories.group(1).split(",")})
    checks = [("POLICY_FUNDING_CATEGORY", is_funding, categories.group(1) if categories else "missing")]
    if not is_funding:
        return checks

    sources_match = re.search(r"^official_sources:\s*$([\s\S]*?)(?=^[A-Za-z_][\w-]*:|\Z)", front_matter, flags=re.M)
    source_urls = urls(sources_match.group(1) if sources_match else "")
    checks.append(("OFFICIAL_SOURCE_COUNT", len(source_urls) >= 2, str(len(source_urls))))
    checks.append(("TRUSTED_OFFICIAL_SOURCES", bool(source_urls) and all(is_trusted(url) for url in source_urls), ", ".join(source_urls)))

    explanation = body.split("## 공식 출처와 확인 근거", 1)[0]
    inline_urls = urls(explanation)
    has_inline_official = any(is_trusted(url) for url in inline_urls)
    checks.append(("INLINE_OFFICIAL_EVIDENCE", has_inline_official, ", ".join(inline_urls) or "none"))
    return checks


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate-policy-funding-post.py <post-markdown>", file=sys.stderr)
        return 2
    post_path = Path(sys.argv[1])
    if not post_path.is_file():
        print(f"post not found: {post_path}", file=sys.stderr)
        return 2
    failed = False
    for name, ok, detail in build_checks(post_path):
        print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
        failed = failed or not ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
