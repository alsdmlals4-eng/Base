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


if __name__ == "__main__":
    unittest.main()
