#!/usr/bin/env python
"""Render or repair the required related-reading block in legacy Pages HTML.

Use this when GitHub Pages serves pre-rendered ``gh-pages`` content rather
than running Jekyll from ``main``. It deliberately mirrors the post-layout
fallback: matching tags/categories first, then recent public posts.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

PROJECT_BASE = "/korea-public-benefit-brief"


def parse_list(value: str) -> list[str]:
    value = value.strip().strip("[]")
    return [item.strip().strip('"\'') for item in value.split(",") if item.strip()]


def parse_post(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, flags=re.S)
    if not match:
        raise ValueError(f"missing front matter: {path}")
    meta: dict[str, object] = {"tags": [], "categories": []}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in {"tags", "categories"}:
            meta[key] = parse_list(value)
        else:
            meta[key] = value.strip('"\'')
    name_match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md$", path.name)
    if not name_match:
        raise ValueError(f"unexpected post filename: {path.name}")
    year, month, day, slug = name_match.groups()
    categories = meta["categories"]
    category_path = "/".join(str(item) for item in categories)
    meta["url"] = f"/{category_path}/{year}/{month}/{day}/{slug}/"
    meta["date_key"] = f"{year}{month}{day}"
    meta["body"] = match.group(2)
    return meta


def card(post: dict[str, object], label: str) -> str:
    title = html.escape(str(post.get("title", "제목 없는 글")))
    description = html.escape(str(post.get("description", "")))
    href = html.escape(PROJECT_BASE + str(post["url"]), quote=True)
    image = str(post.get("image", ""))
    image_alt = html.escape(str(post.get("image_alt") or post.get("title", "")), quote=True)
    image_html = ""
    if image:
        image_src = image if image.startswith(PROJECT_BASE + "/") else PROJECT_BASE + image
        image_html = f'<a class="related-thumb" href="{href}"><img src="{html.escape(image_src, quote=True)}" alt="{image_alt}" loading="lazy"></a>'
    return (
        '<article class="related-card">'
        f"{image_html}"
        '<div class="related-copy">'
        f"<p>{html.escape(label)} · 함께 읽기</p>"
        f'<h3><a href="{href}">{title}</a></h3>'
        f"<span>{description}</span>"
        "</div></article>"
    )


def public_posts(candidates: list[dict[str, object]], pages_root: Path) -> list[dict[str, object]]:
    """Keep only candidates whose rendered page already exists in gh-pages."""
    return [
        post
        for post in candidates
        if (pages_root / str(post["url"]).strip("/") / "index.html").is_file()
    ]


def build_related_section(current: dict[str, object], candidates: list[dict[str, object]], limit: int = 3) -> str:
    """Return required related-reading markup, including deterministic fallback."""
    current_tags = set(current.get("tags", []))
    current_categories = set(current.get("categories", []))
    eligible = [post for post in candidates if post.get("url") != current.get("url")]
    eligible.sort(key=lambda post: str(post.get("date_key", "")), reverse=True)
    matched: list[tuple[dict[str, object], str]] = []
    for post in eligible:
        shared_tags = current_tags.intersection(post.get("tags", []))
        shared_categories = current_categories.intersection(post.get("categories", []))
        if shared_tags or shared_categories:
            label = sorted(shared_tags)[0] if shared_tags else sorted(shared_categories)[0]
            matched.append((post, label))
        if len(matched) == limit:
            break
    selected = matched or [(post, "최근 글") for post in eligible[:limit]]
    if not selected:
        raise ValueError("cannot render related reading: no other public posts available")
    cards = "\n".join(card(post, label) for post, label in selected)
    return (
        '<section class="related-posts" aria-labelledby="related-posts-title">\n'
        '  <div class="related-heading"><p class="eyebrow">KEEP READING</p><h2 id="related-posts-title">이 글과 함께 읽어보세요</h2></div>\n'
        f'  <div class="related-grid">{cards}</div>\n'
        "</section>"
    )


def inject_related_section(rendered_html: str, section: str) -> str:
    pattern = r'<section\b[^>]*\bclass=["\'][^"\']*\brelated-posts\b[^"\']*["\'][^>]*>.*?</section>'
    if re.search(pattern, rendered_html, flags=re.I | re.S):
        return re.sub(pattern, section, rendered_html, count=1, flags=re.I | re.S)
    article_end = re.search(r"</article>", rendered_html, flags=re.I)
    if not article_end:
        raise ValueError("cannot inject related reading: rendered page has no </article>")
    return rendered_html[: article_end.end()] + "\n" + section + rendered_html[article_end.end() :]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("post", type=Path, help="source Markdown post")
    parser.add_argument("rendered_index", type=Path, help="legacy gh-pages index.html")
    parser.add_argument("--posts-dir", type=Path, default=None, help="source _posts directory")
    parser.add_argument("--pages-root", type=Path, required=True, help="root of the checked-out gh-pages worktree")
    args = parser.parse_args()
    posts_dir = args.posts_dir or args.post.parent
    current = parse_post(args.post)
    candidates = public_posts([parse_post(path) for path in posts_dir.glob("*.md")], args.pages_root)
    section = build_related_section(current, candidates)
    rendered = args.rendered_index.read_text(encoding="utf-8")
    updated = inject_related_section(rendered, section)
    args.rendered_index.write_text(updated, encoding="utf-8")
    print(f"RELATED_POSTS_RENDERED: {args.rendered_index}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
