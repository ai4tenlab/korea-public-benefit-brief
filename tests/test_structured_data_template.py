import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StructuredDataTemplateTests(unittest.TestCase):
    def test_post_layout_declares_article_and_breadcrumb_schema(self):
        post_layout = (ROOT / "_layouts" / "post.html").read_text(encoding="utf-8")
        self.assertIn('"@type":"BlogPosting"', post_layout)
        self.assertIn('"@type":"BreadcrumbList"', post_layout)
        self.assertIn('datePublished', post_layout)
        self.assertIn('dateModified', post_layout)
        self.assertIn('mainEntityOfPage', post_layout)

    def test_default_layout_exposes_article_social_metadata(self):
        default_layout = (ROOT / "_layouts" / "default.html").read_text(encoding="utf-8")
        self.assertIn('article:published_time', default_layout)
        self.assertIn('article:modified_time', default_layout)


if __name__ == "__main__":
    unittest.main()
