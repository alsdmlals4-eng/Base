from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md"
DOC_MAP = ROOT / "docs/DOCUMENTATION_MAP.md"
BASE_PR_TEMPLATE = ROOT / ".github/pull_request_template.md"
PROJECT_PR_TEMPLATE = ROOT / "templates/pull_request_template.md"
CI_TEST = ROOT / "tests/test_ci_workflow_cost_policy.py"


class GithubWorkItemLifecyclePolicyTests(unittest.TestCase):
    def test_policy_defines_responsibilities_and_limits(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for term in (
            "Issue 또는 승인된 Goal",
            "하나의 Goal에는 하나의 활성 PR",
            "전체 열린 PR",
            "권장 최대 3개",
            "Squash merge",
            "병합 후 Branch",
            "Actions Run",
            "Artifact",
            "GitHub Release",
            "UNVERIFIED_REPOSITORY_SETTING",
            "KEEP_UNRESOLVED",
        ):
            self.assertIn(term, text)

    def test_policy_defines_default_retention_targets(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for term in (
            "성공한 일반 CI 로그·Run | 14일",
            "실패한 일반 CI 로그·Run | 30일",
            "실패 진단 Artifact | 14일",
            "개발용 빌드 | 7일",
            "Release candidate | 30일",
        ):
            self.assertIn(term, text)

    def test_templates_route_reuse_and_retention(self) -> None:
        base = BASE_PR_TEMPLATE.read_text(encoding="utf-8")
        project = PROJECT_PR_TEMPLATE.read_text(encoding="utf-8")

        for text in (base, project):
            self.assertIn("기존 PR 검색", text)
            self.assertIn("새 PR 필요 사유", text)
            self.assertIn("Run·Artifact", text)
            self.assertIn("Branch 처리", text)
            self.assertIn("미검증", text)

        self.assertNotIn("docs/BASE_RULES_VERSION.md", base)
        self.assertNotIn("docs/AI_SHARED_WORK_RULES.md", base)
        self.assertIn("docs/BASE_RULES_VERSION.md", project)
        self.assertNotIn("docs/AI_SHARED_WORK_RULES.md", project)

    def test_documentation_map_and_existing_ci_suite_load_policy(self) -> None:
        doc_map = DOC_MAP.read_text(encoding="utf-8")
        ci_test = CI_TEST.read_text(encoding="utf-8")
        self.assertIn("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md", doc_map)
        self.assertIn(
            "from tests.test_github_work_item_lifecycle_policy import ",
            ci_test,
        )
        self.assertIn("GithubWorkItemLifecyclePolicyTests", ci_test)


if __name__ == "__main__":
    unittest.main()
