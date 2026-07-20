#!/usr/bin/env python3
"""Ad-hoc/site CI helper for mobile CSS and thumbnail hygiene.

Checks:
- homepage renders post thumbnails through .post-thumb-link
- CSS contains mobile-first thumbnail/card constraints
- no exact duplicate image binaries exist under assets/images/thumbnails
- every post image path exists
"""
from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def report(name: str, ok: bool, detail: str = "") -> bool:
    print(f"{'PASS' if ok else 'FAIL'} {name}{' :: ' + detail if detail else ''}")
    return ok


def main() -> int:
    failures: list[str] = []

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8")

    checks = [
        ("index_uses_thumbnail_link", "post-thumb-link" in index),
        ("index_lazy_loads_thumbnails", 'loading="lazy"' in index),
        ("css_mobile_media_query", "@media(max-width:760px)" in css),
        ("css_mobile_card_two_column", ".post-item{grid-template-columns:104px 1fr" in css),
        ("css_mobile_thumb_height_limited", ".post-thumb-link img{height:84px" in css),
        ("css_article_thumbnail_max_height", "max-height:220px" in css and ".post-thumbnail img" in css),
        ("css_no_horizontal_overflow", "overflow-x:hidden" in css),
    ]
    for name, ok in checks:
        if not report(name, ok):
            failures.append(name)

    # Post image references exist.
    for post in sorted((ROOT / "_posts").glob("*.md")):
        text = post.read_text(encoding="utf-8")
        match = re.search(r"^image:\s*[\"']?([^\"'\n]+)[\"']?\s*$", text, re.M)
        if not match:
            continue
        rel = match.group(1).strip().lstrip("/")
        ok = (ROOT / rel).exists()
        if not report(f"post_image_exists:{post.name}", ok, rel):
            failures.append(f"missing image {rel}")

    # Exact duplicate image detection.
    hashes: dict[str, list[Path]] = defaultdict(list)
    for img in sorted((ROOT / "assets/images/thumbnails").glob("*")):
        if img.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        hashes[hashlib.sha256(img.read_bytes()).hexdigest()].append(img)
    dupes = {h: files for h, files in hashes.items() if len(files) > 1}
    if not report("no_exact_duplicate_thumbnail_files", not dupes, "; ".join(",".join(str(f.relative_to(ROOT)) for f in files) for files in dupes.values())):
        failures.append("duplicate thumbnail files")

    if failures:
        print("VERIFY_MOBILE_THUMBNAILS_FAIL")
        return 1
    print("VERIFY_MOBILE_THUMBNAILS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
