from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class PostmergeGithubNotionLongTermContractTests(unittest.TestCase):
    def test_long_term_best_method_is_a_canonical_goal_not_a_speed_shortcut(self) -> None:
        sources = (
            text("AGENTS.md"),
            text("docs/OPERATING_MODEL.md"),
            text("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"),
        )
        for source in sources:
            with self.subTest(source=source[:40]):
                self.assertIn("BEST_LONG_TERM_EFFICIENT_METHOD", source)
                self.assertIn("QUALITY_OVER_RESPONSE_SPEED", source)
                self.assertIn("BENCHMARK_PRACTICE_COMPARISON", source)

    def test_operating_model_uses_domain_split_canon_not_active_sheets(self) -> None:
        operating_model = text("docs/OPERATING_MODEL.md")
        for token in (
            "DOMAIN_SPLIT_CANON",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "COMPATIBILITY_ONLY",
        ):
            self.assertIn(token, operating_model)
        self.assertNotIn(
            "게임 프로젝트에 구성된 GDD Google Sheets는 `USER_FACING_GDD_WORKSPACE`로 사용",
            operating_model,
        )
        self.assertNotIn(
            "사용자 GDD 작업면 → 프로젝트 Google Sheets(`USER_FACING_GDD_WORKSPACE`)",
            operating_model,
        )

    def test_project_merge_closes_github_notion_review_correction_and_progress(self) -> None:
        sources = (
            text("AGENTS.md"),
            text("docs/OPERATING_MODEL.md"),
            text("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"),
            text("skills/managing-game-project-operating-system/SKILL.md"),
        )
        for source in sources:
            with self.subTest(source=source[:40]):
                self.assertIn("POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP", source)
                self.assertIn("POSTMERGE_CORRECTION_REQUIRED", source)
                self.assertIn("PROGRESS_READBACK_REQUIRED", source)

    def test_retired_visual_tools_are_not_cold_start_routes(self) -> None:
        start = text("START_HERE.md")
        for retired_route in (
            "tools/tool-hub/README.md",
            "tools/expression-studio/README.md",
            "tools/sprite-animation-studio/README.md",
        ):
            self.assertNotIn(retired_route, start)
        self.assertIn("RETIRED_HISTORY_ONLY", start)
        self.assertIn("tools/qa-evidence-studio/README.md", start)

    def test_legacy_sheet_template_cannot_install_a_new_sheet(self) -> None:
        template = text("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        self.assertIn("COMPATIBILITY_ONLY", template)
        self.assertIn("DO_NOT_INSTALL_NEW", template)
        self.assertNotIn("새 Sheet에 설치하는 권장 핵심 tab", template)

    def test_core_ci_runs_whole_unittest_discovery(self) -> None:
        workflow = text(".github/workflows/validate-game-project-operating-system.yml")
        self.assertIn("core-regression", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("CORE_REGRESSION_RESULT", workflow)
        core = workflow.split("\n  core-regression:\n", 1)[1].split(
            "\n  ubuntu-contract:\n", 1
        )[0]
        job_header = core.split("\n    steps:\n", 1)[0]
        self.assertNotIn("needs: classify-changes", job_header)
        self.assertNotIn("if:", job_header)

    def test_local_validation_has_dependency_preflight_and_documented_setup(self) -> None:
        runner = text("tools/run_local_validation.py")
        readme = text("README.md")
        self.assertIn("LOCAL_VALIDATION_REQUIRED_MODULES", runner)
        self.assertIn("LOCAL_VALIDATION_DEPENDENCY_MISSING", runner)
        self.assertIn(
            "python -m pip install --requirement .github/validation-requirements.txt",
            readme,
        )

    def test_continuation_intent_reuses_an_approved_contract_without_magic_words(self) -> None:
        skill = text("skills/managing-project-intake-and-work-contract/SKILL.md")
        reference = text(
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
        )
        for source in (skill, reference):
            self.assertIn("CONTINUATION_INTENT_ALIASES", source)
            self.assertIn("진행해", source)
            self.assertIn("계속해", source)
            self.assertIn("남은 작업 진행", source)
            self.assertIn("APPROVED_CONTRACT_CONTINUATION", source)

    def test_project_install_templates_inherit_long_term_postmerge_goal(self) -> None:
        start = text("templates/project-operations/PROJECT_START_HERE.md")
        active = text("templates/project-operations/ACTIVE_CONTEXT.md")
        for token in (
            "BEST_LONG_TERM_EFFICIENT_METHOD",
            "QUALITY_OVER_RESPONSE_SPEED",
            "BENCHMARK_PRACTICE_COMPARISON",
            "POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP",
            "PROGRESS_READBACK_REQUIRED",
        ):
            self.assertIn(token, start)
        self.assertIn("postmerge_progress_readback", active)

    def test_retired_visual_tools_cannot_reactivate_through_ci_or_adapter_docs(self) -> None:
        canonical_ci = text(".github/workflows/validate-game-project-operating-system.yml")
        long_horizon_ci = text(".github/workflows/validate-base-long-horizon-work-contract.yml")
        adapter = text("docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md")
        for path in (
            "tools/tool-hub",
            "tools/expression-studio",
            "tools/sprite-animation-studio",
        ):
            self.assertNotIn(path, canonical_ci)
            self.assertNotIn(path, long_horizon_ci)
        self.assertIn("RETIRED_HISTORY_ONLY", adapter)
        self.assertNotIn("For Tool Hub identity", adapter)


if __name__ == "__main__":
    unittest.main()
