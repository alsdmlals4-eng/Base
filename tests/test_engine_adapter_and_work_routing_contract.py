from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EngineAdapterAndWorkRoutingContractTests(unittest.TestCase):
    def test_engine_policy_keeps_neutral_core_with_godot_default_adapter(self) -> None:
        policy = (ROOT / "docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md").read_text(encoding="utf-8")
        for term in (
            "ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE",
            "GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER",
            "STABLE_ENGINE_BASELINE",
            "NO_AUTOMATIC_LATEST_FOLLOW",
            "CANARY_BEFORE_ENGINE_BASELINE_PROMOTION",
            "ENGINE_MIGRATION_REQUIRES_SEPARATE_REALITY_GATE",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
        ):
            self.assertIn(term, policy)

    def test_p06_routes_provider_neutral_core_through_current_godot_adapter(self) -> None:
        text = (ROOT / "docs/operations/base-partitions/P06_GODOT_RUNTIME_TOOLCHAIN.md").read_text(encoding="utf-8")
        for term in (
            "ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE",
            "GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER",
            "STABLE_ENGINE_BASELINE",
            "ENGINE_BASELINE_AND_ADAPTER_POLICY.md",
        ):
            self.assertIn(term, text)

    def test_p08_routes_chat_work_and_codex_by_task_shape(self) -> None:
        text = (ROOT / "docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md").read_text(encoding="utf-8")
        for term in (
            "CHAT_QUICK_DISCUSSION_DEFAULT",
            "WORK_LONG_MULTISTEP_NONCODING_DEFAULT",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON",
        ):
            self.assertIn(term, text)

    def test_work_does_not_replace_notion_or_repository_authority(self) -> None:
        policy = (ROOT / "docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("Work는 실행 작업면이며 새 정본 저장소가 아니다", policy)
        self.assertIn("Notion", policy)
        self.assertIn("GitHub", policy)


if __name__ == "__main__":
    unittest.main()
