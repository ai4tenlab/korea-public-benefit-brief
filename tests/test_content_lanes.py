from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ContentLaneTemplateTests(unittest.TestCase):
    def test_home_has_two_filtered_three_post_lanes(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("생활정책·혜택", home)
        self.assertIn("정책자금", home)
        self.assertIn("unless post.categories contains 'funding'", home)
        self.assertIn("if post.categories contains 'funding'", home)
        self.assertIn("living_count < 3", home)
        self.assertIn("funding_count < 3", home)

    def test_navigation_links_to_living_policy_archive(self):
        layout = (ROOT / "_layouts" / "default.html").read_text(encoding="utf-8")
        self.assertIn("/living-policy/", layout)
        self.assertIn("생활정책·혜택", layout)
        self.assertNotIn(">포스팅<", layout)

    def test_each_archive_has_honest_empty_state_and_filter(self):
        living = (ROOT / "living-policy.md").read_text(encoding="utf-8")
        funding = (ROOT / "policy-funding.md").read_text(encoding="utf-8")
        self.assertIn("unless post.categories contains 'funding'", living)
        self.assertIn("if post.categories contains 'funding'", funding)
        self.assertIn("공식 공고를 검증", funding)


if __name__ == "__main__":
    unittest.main()
