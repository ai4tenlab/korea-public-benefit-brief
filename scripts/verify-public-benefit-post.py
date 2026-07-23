#!/usr/bin/env python
"""Verify a public-benefit GitHub Pages post after publishing.

Usage:
  python scripts/verify-public-benefit-post.py \
    https://ai4tenlab.github.io/korea-public-benefit-brief/benefit/2026/07/11/public-period-products-pilot/ \
    "공공생리대 시범사업, 시작 첫 주에 확인할 대상·장소·주의점"
"""
from __future__ import annotations

import re
import sys
import urllib.request
from html import unescape
from urllib.parse import urljoin


def fetch(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "4TENLAB-post-verifier/1.0"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return int(res.status), res.read()


def attr(html: str, pattern: str) -> str | None:
    m = re.search(pattern, html, flags=re.I | re.S)
    return unescape(m.group(1).strip()) if m else None


def build_checks(url: str, expected_title: str, status: int, html: str) -> list[tuple[str, bool, str]]:
    """Return content-structure checks that can be unit-tested without network access."""
    checks: list[tuple[str, bool, str]] = []
    checks.append(("ARTICLE_200", status == 200, str(status)))
    checks.append(("EXPECTED_TITLE_TEXT", expected_title in html, expected_title))

    h1s = [unescape(re.sub(r"<[^>]+>", "", h).strip()) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, flags=re.I | re.S)]
    checks.append(("SINGLE_VISIBLE_H1", len(h1s) == 1, repr(h1s)))
    checks.append(("H1_MATCHES_TITLE", h1s == [expected_title], repr(h1s)))

    desc = attr(html, r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']')
    checks.append(("META_DESCRIPTION", bool(desc and 40 <= len(desc) <= 220), str(len(desc or ""))))

    og_img = attr(html, r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']')
    checks.append(("OG_IMAGE_PRESENT", bool(og_img), str(og_img)))
    checks.append(("TWITTER_CARD", "summary_large_image" in html, "summary_large_image"))

    # AEO/GEO required sections for policy brief posts.
    for heading in ["3줄 요약", "한 문장 답변", "핵심 정의", "FAQ", "공식 출처와 확인 근거"]:
        checks.append((f"SECTION_{heading}", f">{heading}<" in html or heading in html, heading))

    related = re.search(
        r'<section\b[^>]*\bclass=["\'][^"\']*\brelated-posts\b[^"\']*["\'][^>]*>(.*?)</section>',
        html,
        flags=re.I | re.S,
    )
    related_html = related.group(1) if related else ""
    checks.append(("SECTION_이 글과 함께 읽어보세요", "이 글과 함께 읽어보세요" in related_html, "related-posts"))
    related_links = re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']', related_html, flags=re.I | re.S)
    public_links = [href for href in related_links if href and not href.startswith(("#", "javascript:"))]
    checks.append(("RELATED_POST_LINK", bool(public_links), repr(public_links)))
    return checks


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: verify-public-benefit-post.py <url> <expected-title>", file=sys.stderr)
        return 2

    url, expected_title = sys.argv[1], sys.argv[2]
    status, raw = fetch(url)
    html = raw.decode("utf-8", "replace")
    checks = build_checks(url, expected_title, status, html)

    og_img = attr(html, r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']')
    if og_img:
        img_url = urljoin(url, og_img)
        try:
            img_status, img_raw = fetch(img_url)
            checks.append(("OG_IMAGE_200", img_status == 200, f"{img_status} bytes={len(img_raw)}"))
        except Exception as exc:  # noqa: BLE001 - diagnostic script
            checks.append(("OG_IMAGE_200", False, f"{type(exc).__name__}: {exc}"))

    failed = False
    for name, ok, detail in checks:
        print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")
        failed = failed or not ok

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
