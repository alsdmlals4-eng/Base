from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class V47WorkflowAlignmentTests(unittest.TestCase):
    def test_entrypoints_retire_tool_hub_and_qa_studio_from_active_project_flow(self) -> None:
        start = read("START_HERE.md")
        readme = read("README.md")
        docs_map = read("docs/DOCUMENTATION_MAP.md")
        retirement = read("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md")
        powershell = read("docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md")

        for term in (
            "TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW",
            "QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW",
            "NO_DEFAULT_READ_OF_RETIRED_SURFACE",
        ):
            self.assertIn(term, retirement)

        self.assertNotIn("로컬 Tool Hub와 프로젝트 자동 탐색", start)
        self.assertNotIn("이미지·UX 배치 후 개발자 PC 증거 검토: `tools/qa-evidence-studio/README.md`", start)
        self.assertIn("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md", start)
        self.assertIn("TOOL_HUB_RETIRED_FROM_DEFAULT_ROUTE", powershell)
        self.assertNotIn("Tool Hub 실제 runtime**을 우선", powershell)

        self.assertNotIn("[PC 우선 QA Evidence Studio](tools/qa-evidence-studio/README.md)", readme)
        self.assertNotIn("QA Evidence Studio는 Figma/Notion과 독립적인 실제 PC 런타임 증거 도구이므로 유지합니다.", readme)
        self.assertIn("REPOSITORY_NATIVE_EVIDENCE_CAPTURE", readme)

        self.assertNotIn("| QA runtime evidence | `tools/qa-evidence-studio/README.md`", docs_map)
        self.assertIn("REPOSITORY_NATIVE_EVIDENCE_CAPTURE", docs_map)

    def test_operating_model_uses_repository_first_not_google_sheet_gdd_authority(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")
        self.assertIn("DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE", operating)
        self.assertIn("REPOSITORY_PRIMARY_CANON", operating)
        self.assertIn("HUMAN_GDD_PDF_DERIVED_VIEW", operating)
        self.assertIn("REPOSITORY_RUNTIME_TRUTH", operating)
        self.assertIn("COMPATIBILITY_ONLY", operating)
        self.assertIn("docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md", operating)
        self.assertNotIn("GDD Google Sheets는 `USER_FACING_GDD_WORKSPACE`", operating)

    def test_reuse_catalog_uses_repository_native_evidence_capture(self) -> None:
        modules = read("docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md")
        registry = read("docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md")
        for text in (modules, registry):
            self.assertIn("RM-TOOL-004", text)
            self.assertIn("REPOSITORY_NATIVE_EVIDENCE_CAPTURE", text)
            self.assertNotIn("`tools/qa-evidence-studio`", text)
        self.assertIn("repository_or_ci_artifact", modules)
        self.assertIn("notion_human_link_when_useful", modules)

    def test_creative_frontier_and_visualization_need_map_are_explicit(self) -> None:
        long_horizon = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        reuse = read("docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md")
        planning = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")

        for text in (long_horizon, reuse):
            self.assertIn("CREATIVE_BENCHMARK_FRONTIER", text)
            self.assertIn("ORIGINALITY_FUN_CREATIVITY_REVIEW", text)
        for term in (
            "DIRECT_GENRE_BEST_IN_CLASS",
            "ADJACENT_GENRE_BEST_IN_CLASS",
            "DISTINCTIVE_OR_INNOVATIVE_WORK",
            "FAILURE_OR_MIXED_CASE",
        ):
            self.assertIn(term, reuse)

        self.assertIn("PROJECT_VISUALIZATION_NEED_MAP", planning)
        self.assertIn("exact Project Notion", planning)
        self.assertIn("fun_hypothesis", reuse)
        self.assertIn("PLAYER_EVIDENCE_REQUIRED_FOR_FUN_PASS", reuse)

    def test_existing_long_horizon_safety_and_completion_contracts_remain(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_REQUIRED",
            "EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "BALANCE_BUDGET",
            "WORLD_STORYLINE_FIT_REQUIRED",
            "REUSABLE_SYSTEM_EXTRACTION",
            "RELEASE_NEAR_VERTICAL_SLICE_FIRST",
            "LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT",
            "REQUIRED_WORK_REMAINING: 0",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION",
        ):
            self.assertIn(term, policy)
        self.assertNotIn("TOOL_HUB: REQUIRED_WHEN_RELEVANT", policy)

    def test_pixel_art_reference_uses_current_project_visual_authority(self) -> None:
        pixel = read("docs/knowledge/game-development/PIXEL_ART_STYLE_SYSTEM.md")
        for stale in (
            "Figma 승인",
            "Figma Visual Bible",
            "Figma 승인 Reference",
        ):
            self.assertNotIn(stale, pixel)
        for current in (
            "Notion",
            "Project Visual Reference",
            "PROJECT_ART_CANON_REMAINS_PROJECT_OWNED",
        ):
            self.assertIn(current, pixel)

    def test_flexible_structure_has_no_fixed_skill_count_gate(self) -> None:
        manifest = read("docs/operations/BASE_PARTITION_MANIFEST.json")
        skill_readme = read("skills/README.md")
        self.assertNotIn("게임 설계 Skill이 8개 이상으로 증가", manifest)
        self.assertIn("Skill 수 자체는 목표가 아니다", skill_readme)

    def test_user_action_and_completion_remain_learning_oriented(self) -> None:
        powershell = read("docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md")
        partitions = read("docs/operations/BASE_PARTITION_OPERATING_MODEL.md")
        agents = read("AGENTS.md")
        self.assertIn("BEGINNER_SAFE_USER_ACTION", powershell)
        for term in (
            "이 Part가 왜 존재하는가",
            "가장 중요한 규칙",
            "BEFORE → AFTER",
            "기대효과",
        ):
            self.assertIn(term, partitions)
        self.assertIn("사용자 학습형 완료보고", agents)

    def test_prebuild_report_and_live_github_notion_sync_are_explicit(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        documents = read("skills/managing-design-documents/SKILL.md")
        planning = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        combined = "\n".join((intake, documents, planning))

        for term in (
            "FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN",
            "PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT",
            "USER_APPROVAL_BEFORE_BUILD",
            "APPROVED_DECISION_GITHUB_NOTION_SYNC_DURING_WORK",
            "POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK",
        ):
            self.assertIn(term, combined)

        self.assertIn("Base", intake)
        self.assertIn("Project Notion Home", intake)
        self.assertIn("open/recent PR", intake)
        self.assertIn("변경 전", intake)
        self.assertIn("변경 후", intake)
        self.assertIn("기대효과", intake)
        self.assertIn("GitHub", documents)
        self.assertIn("Notion", documents)
        self.assertIn("readback", documents)


if __name__ == "__main__":
    unittest.main()
