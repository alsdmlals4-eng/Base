from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class P08AiOperationsContractTests(unittest.TestCase):
    def test_external_executor_rehydrates_current_canon_and_gpt_reviews(self) -> None:
        skill = (ROOT / "skills/orchestrating-deepseek-worktrees/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "EXECUTOR_REHYDRATION_GATE",
            "GPT_PRIMARY_REVIEWER",
            "GPT_NONCODING_PROJECT_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "REVIEW_PENDING",
            "exact branch/commit",
            "AGENTS.md",
        ):
            self.assertIn(term, skill)

    def test_p08_routes_base_and_notion_to_gpt_and_godot_product_to_codex(self) -> None:
        text = (ROOT / "docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md").read_text(encoding="utf-8")
        for term in (
            "GPT_BASE_NOTION_GOVERNANCE_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "GDScript/product code",
            "Scene/Resource/Autoload/runtime wiring",
            "Base Python test·CI contract·Registry/generated checker",
        ):
            self.assertIn(term, text)
        self.assertNotIn("OPTIONAL_CODEX_EXECUTOR", text)

    def test_p08_routes_chat_work_and_engine_adapter_without_replacing_godot_compatibility(self) -> None:
        text = (ROOT / "docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md").read_text(encoding="utf-8")
        for term in (
            "CHAT_QUICK_DISCUSSION_DEFAULT",
            "WORK_LONG_MULTISTEP_NONCODING_DEFAULT",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON",
        ):
            self.assertIn(term, text)

    def test_engine_baseline_policy_keeps_neutral_core_and_current_godot_adapter(self) -> None:
        policy = (ROOT / "docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE",
            "GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER",
            "STABLE_ENGINE_BASELINE",
            "NO_AUTOMATIC_LATEST_FOLLOW",
            "CANARY_BEFORE_ENGINE_BASELINE_PROMOTION",
            "ENGINE_MIGRATION_REQUIRES_SEPARATE_REALITY_GATE",
            "WORK_EXECUTION_SURFACE_NOT_CANON",
        ):
            self.assertIn(term, policy)
        p06 = (ROOT / "docs/operations/base-partitions/P06_GODOT_RUNTIME_TOOLCHAIN.md").read_text(encoding="utf-8")
        self.assertIn("ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE", p06)
        self.assertIn("GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER", p06)

    def test_external_ai_optionality_is_separate_from_godot_implementation_owner(self) -> None:
        text = (ROOT / "skills/orchestrating-deepseek-worktrees/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("외부 AI 사용은 optional", text)
        self.assertIn("실제 게임 프로젝트의 Godot 제품 구현", text)
        learning = (ROOT / "skills/orchestrating-deepseek-worktrees/LEARNING_LOG.md").read_text(encoding="utf-8")
        self.assertIn("code format is not Codex ownership", learning)

    def test_p08_learning_history_remains_discoverable_but_current_correction_wins(self) -> None:
        learning = (ROOT / "skills/orchestrating-deepseek-worktrees/LEARNING_LOG.md").read_text(encoding="utf-8")
        self.assertIn("CURRENT_CORRECTION", learning)
        self.assertIn("SUPERSEDED INTERIM", learning)
        self.assertIn("REVALIDATED_FOCUSED_AND_BASE_V9_ON_727ecb15", learning)
        self.assertIn("tests/test_p08_ai_operations_contract.py", learning)
        self.assertIn("docs/operations/base-partitions/learning/P08_LEARNING_LOG.md", learning)

    def test_codex_image_generation_is_not_p08_executor_capability(self) -> None:
        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "CODEX_IMAGE_GENERATION_FORBIDDEN",
            "CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY",
            "GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING",
        ):
            self.assertIn(term, policy)


    def test_intake_ai_solution_layer_selection_routes_before_build(self) -> None:
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        capability = (ROOT / "docs/CAPABILITY_COMPOSITION_MAP.md").read_text(encoding="utf-8")
        for term in (
            "PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER",
            "AI_SOLUTION_LAYER_SELECTION_BEFORE_BUILD",
            "NO_AUTO_FEATURE_FROM_VOCABULARY",
            "smallest sufficient layer",
        ):
            self.assertIn(term, intake)
        for term in (
            "AI_SOLUTION_LAYER_SELECTION",
            "DETERMINISTIC_WORKFLOW_BEFORE_OPEN_ENDED_AGENT",
            "HARNESS_COMPONENTS_REQUIRE_LOAD_BEARING_EVIDENCE",
            "AGI_ASI_AWARENESS_ONLY",
        ):
            self.assertIn(term, capability)


if __name__ == "__main__":
    unittest.main()
