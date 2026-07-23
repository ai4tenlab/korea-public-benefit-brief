import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PublicVerifierRelatedPostsTests(unittest.TestCase):
    def test_requires_related_posts_heading_and_card_link(self):
        verifier = load_module("verify-public-benefit-post.py", "post_verifier")
        html = """
        <html><h1>테스트 정책</h1>
        <meta name='description' content='가' />
        <meta property='og:image' content='/image.png' />
        summary_large_image
        <h2>3줄 요약</h2><h2>한 문장 답변</h2><h2>핵심 정의</h2>
        <h2>FAQ</h2><h2>공식 출처와 확인 근거</h2>
        </html>
        """
        checks = verifier.build_checks("https://example.test/post/", "테스트 정책", 200, html)
        results = {name: ok for name, ok, _ in checks}
        self.assertFalse(results["SECTION_이 글과 함께 읽어보세요"])
        self.assertFalse(results["RELATED_POST_LINK"])


class RelatedPostsRendererTests(unittest.TestCase):
    def test_falls_back_to_recent_post_when_no_tag_or_category_matches(self):
        renderer = load_module("ensure-related-posts.py", "related_renderer")
        current = {
            "url": "/policy/benefit/welfare/2026/07/23/current/",
            "title": "현재 글",
            "tags": ["현재태그"],
            "categories": ["policy", "benefit", "welfare"],
        }
        recent = {
            "url": "/policy/notice/2026/07/22/recent/",
            "title": "최근 글",
            "description": "최근 공개된 정책 글입니다.",
            "tags": ["다른태그"],
            "categories": ["policy", "notice"],
        }
        section = renderer.build_related_section(current, [recent])
        self.assertIn("이 글과 함께 읽어보세요", section)
        self.assertIn('href="/korea-public-benefit-brief/policy/notice/2026/07/22/recent/"', section)
        self.assertIn("최근 글", section)

    def test_filters_out_candidates_not_present_in_pages_worktree(self):
        renderer = load_module("ensure-related-posts.py", "related_renderer")
        public = {"url": "/policy/benefit/2026/07/22/public/", "title": "공개 글"}
        unpublished = {"url": "/policy/benefit/2026/07/23/unpublished/", "title": "미배포 글"}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "policy/benefit/2026/07/22/public/index.html"
            target.parent.mkdir(parents=True)
            target.write_text("<html></html>", encoding="utf-8")
            visible = renderer.public_posts([public, unpublished], root)
        self.assertEqual(visible, [public])


if __name__ == "__main__":
    unittest.main()
