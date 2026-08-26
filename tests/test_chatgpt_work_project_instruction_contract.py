from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"
APPENDIX = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md"


class ChatGPTWorkProjectInstructionContractTests(unittest.TestCase):
    def _text(self) -> str:
        self.assertTrue(TARGET.exists(), "Work-native project instruction must exist")
        return TARGET.read_text(encoding="utf-8")

    def _appendix(self) -> str:
        self.assertTrue(APPENDIX.exists(), "Work-native compatibility appendix must exist")
        return APPENDIX.read_text(encoding="utf-8")

    def test_minimal_entry_and_memory_authority(self) -> None:
        text = self._text()
        for term in (
            "PROJECT_PLUS_INSTRUCTION_PLUS_OPTIONAL_GOAL_IS_SUFFICIENT_INPUT",
            "WORK_SELF_STARTING_FRESH_READ_BOOTSTRAP",
            "DEFAULT_MEMORY_DISCOVERY_ONLY_NOT_CANON",
            "MEMORY_CONFLICT_CURRENT_PROJECT_CANON_WINS",
            "PAST_CONVERSATION_NOT_REQUIRED",
        ):
            self.assertIn(term, text)

    def test_work_codex_and_engine_boundaries(self) -> None:
        text = self._text()
        for term in (
            "CHAT_QUICK_DISCUSSION_DEFAULT",
            "WORK_LONG_MULTISTEP_NONCODING_DEFAULT",
            "WORK_EXECUTION_SURFACE_NOT_CANON",
            "CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE",
            "ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON",
            "GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER",
            "STABLE_ENGINE_BASELINE",
            "NO_AUTOMATIC_LATEST_FOLLOW",
            "CANARY_BEFORE_ENGINE_BASELINE_PROMOTION",
        ):
            self.assertIn(term, text)

    def test_r54_planning_reuse_and_skill_coverage_survive(self) -> None:
        text = self._text()
        for term in (
            "REVISION_NON_REGRESSION_GATE",
            "BASE_OWNER_PROGRESSIVE_LOAD",
            "CURRENT_SKILL_REGISTRY_COVERAGE_GATE",
            "FRESH_READ_PROJECT_BOOTSTRAP",
            "ENTRY_STATE_RECONCILIATION_BLOCKING_GATE",
            "WHOLE_PROJECT_AUDIT_FIRST",
            "CORE_REQUIREMENT_TRACEABILITY",
            "REUSE_FIRST_PREFLIGHT_REQUIRED",
            "MARKET_SUCCESS_FAILURE_COMPARISON",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "EXISTING_SOLUTION_FIRST",
            "PARTIAL_ABSORPTION",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
        ):
            self.assertIn(term, text)

    def test_r54_visual_and_player_evidence_survive(self) -> None:
        text = self._text()
        for term in (
            "PRODUCTION_INFORMATION",
            "TEXT_TABLE_FLOW_DB_FIRST",
            "ACTUAL_CONSUMER_REQUIRED",
            "VISUAL_REQUIREMENT_DELETE_TEST_GATE",
            "VISUAL_ASSET_COVERAGE",
            "ART_STYLE_LOCK",
            "TEXT_BRIEF_STOP_REQUIRED",
            "NOTION_IMAGE_UPLOAD_ROUTING",
            "IMPLEMENTATION_REALITY_GATE",
            "HUMAN_USABILITY_EVIDENCE",
            "PLAYER_EXPERIENCE_EVIDENCE",
            "DECISION_SCREEN_COMPREHENSION_GATE",
            "MULTI_PLATFORM_SHARED_CORE_GATE",
            "ko / en / ja / zh-*",
            "pc_standard / pc_wide_or_ultrawide / mobile_landscape",
        ):
            self.assertIn(term, text)

    def test_r54_slice_runtime_recovery_and_delivery_survive(self) -> None:
        text = self._text()
        for term in (
            "IMPLEMENTATION_READY",
            "SLICE_DELIVERY_LOOP",
            "PLAYABLE_SLICE_BOUNDARY",
            "AUDIO_VISUAL_POC_EVIDENCE",
            "CANONICAL_REFLECTION_AFTER_PLAY",
            "RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE",
            "CASE_LOOKUP_BEFORE_RETRY",
            "MULTI_ROUTE_RECOVERY_LADDER",
            "INCIDENT_SOLUTION_LESSON_LOOP",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE",
            "CURRENT_REQUIRED_CHECK_DISCOVERY",
            "DOMAIN_SPLIT_CANON",
            "ASSET_PROVENANCE",
            "ZERO_INCREMENTAL_COST_REQUIRED",
        ):
            self.assertIn(term, text)

    def test_adversarial_and_completion_contracts_survive(self) -> None:
        text = self._text()
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "FULL_LOOP_IS_NOT_A_REVIEW_LENS",
            "REQUIRED_WORK_REMAINING: 0",
            "COMPLETION_CANDIDATE",
            "IMPLEMENTATION_CORRECTION_RESCAN",
            "POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED",
            "NOT_RUN",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, text)

    def test_skill_routing_is_dynamic_not_hardcoded(self) -> None:
        text = self._text()
        self.assertIn("SKILL_REGISTRY.json", text)
        self.assertIn("trigger", text)
        self.assertIn("not_applicable", text)
        self.assertIn("Skill을 전부 항상 실행하지 않는다", text)
        self.assertIn("고정 Skill 목록", text)

    def test_compatibility_appendix_restores_delegated_r54_boundaries(self) -> None:
        text = self._appendix()
        for term in (
            "PROJECT_WORK_ONLY_WHEN_CURRENT_USER_REQUEST_AUTHORIZES_EXECUTION",
            "REQUIRED_SOURCE_UNREADABLE",
            "brainstorming/design exploration",
            "writing-plans",
            "systematic debugging",
            "verification-before-completion",
            "Toolchain Freshness",
            "STABLE_ENGINE_BASELINE",
            "Fresh Shell",
            "HiGodot/GUT/Hera",
            "COMPATIBILITY_ONLY migration source",
            "local Codex launcher",
            "WORK_PROMPT_EFFICIENCY_WITHOUT_CAPABILITY_LOSS",
        ):
            self.assertIn(term, text)

    def test_p08_discovers_the_complete_work_bundle(self) -> None:
        p08 = (ROOT / "docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md").read_text(encoding="utf-8")
        self.assertIn("CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md", p08)
        self.assertIn("CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md", p08)


if __name__ == "__main__":
    unittest.main()
