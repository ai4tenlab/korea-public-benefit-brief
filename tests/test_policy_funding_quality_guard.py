import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_guard():
    path = ROOT / "scripts" / "validate-policy-funding-post.py"
    spec = importlib.util.spec_from_file_location("policy_funding_guard", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PolicyFundingQualityGuardTests(unittest.TestCase):
    def write_post(self, root: Path, body: str, sources: str) -> Path:
        post = root / "2026-08-11-test-policy-funding.md"
        post.write_text(
            "---\n"
            "layout: post\n"
            "title: 테스트 정책자금 공고\n"
            "description: 검증을 위한 정책자금 공고 요약입니다.\n"
            "date: 2026-08-11 09:00:00 +0900\n"
            "last_modified_at: 2026-08-11 09:00:00 +0900\n"
            "categories: [policy, funding, startup]\n"
            "official_sources:\n"
            f"{sources}"
            "---\n\n"
            f"{body}",
            encoding="utf-8",
        )
        return post

    def test_accepts_policy_funding_post_with_fresh_sources_and_inline_evidence(self):
        guard = load_guard()
        with tempfile.TemporaryDirectory() as directory:
            post = self.write_post(
                Path(directory),
                "## 3줄 요약\n지원 내용은 [기업마당 공식 공고](https://www.bizinfo.go.kr/example)에서 확인한다.\n\n"
                "## 공식 출처와 확인 근거\n- 기업마당 공고\n",
                "  - https://www.bizinfo.go.kr/example\n  - https://www.k-startup.go.kr/example\n",
            )
            checks = guard.build_checks(post)
        results = {name: ok for name, ok, _ in checks}
        self.assertTrue(all(results.values()))

    def test_rejects_post_without_inline_evidence_link(self):
        guard = load_guard()
        with tempfile.TemporaryDirectory() as directory:
            post = self.write_post(
                Path(directory),
                "## 3줄 요약\n지원 내용을 확인하세요.\n\n## 공식 출처와 확인 근거\n- 기업마당 공고\n",
                "  - https://www.bizinfo.go.kr/example\n  - https://www.k-startup.go.kr/example\n",
            )
            checks = guard.build_checks(post)
        results = {name: ok for name, ok, _ in checks}
        self.assertFalse(results["INLINE_OFFICIAL_EVIDENCE"])


if __name__ == "__main__":
    unittest.main()
