from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = (
    "docs/knowledge/game-development/"
    "PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md"
)
README_PATH = "docs/knowledge/game-development/README.md"
REGISTRY_PATH = "skills/SKILL_REGISTRY.json"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectCreationDeliveryOrchestrationTests(unittest.TestCase):
    maxDiff = None

    def test_orchestration_guide_exists_and_is_routed(self) -> None:
        self.assertTrue((ROOT / GUIDE_PATH).is_file(), GUIDE_PATH)
        readme = read(README_PATH)
        self.assertIn("PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md", readme)
        self.assertIn("프로젝트 생성·전달 orchestration", readme)

    def test_phase_order_separates_planning_review_visuals_and_build(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "PLANNING_COMPLETE",
            "FINAL_REVIEW_COMPLETE",
            "SERIAL_VISUAL_PRODUCTION",
            "VISUAL_PRODUCTION_COMPLETE",
            "CODEX_BUILD_ALLOWED",
            "DRAFT_VISUAL",
        ):
            self.assertIn(term, guide)

        self.assertLess(guide.index("PLANNING_COMPLETE"), guide.index("FINAL_REVIEW_COMPLETE"))
        self.assertLess(guide.index("FINAL_REVIEW_COMPLETE"), guide.index("SERIAL_VISUAL_PRODUCTION"))
        self.assertLess(guide.index("SERIAL_VISUAL_PRODUCTION"), guide.index("CODEX_BUILD_ALLOWED"))

    def test_user_gated_visual_queue_locks_inventory_style_and_result_approval(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "VISUAL_ASSET_INVENTORY",
            "ART_STYLE_LOCK",
            "NEXT_ASSET_BRIEF",
            "GENERATION_APPROVAL",
            "GENERATE_ONE_ASSET",
            "VISUAL_QA",
            "RESULT_APPROVAL_BEFORE_NEXT_ASSET",
            "user-gated",
        ):
            self.assertIn(term, guide)

    def test_localization_is_ready_early_but_exact_locale_set_is_project_owned(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "PROJECT_DECLARED_LOCALE_SET",
            "LOCALIZATION_READY",
            "locale key",
            "font fallback",
            "baked-in",
            "zh-Hans",
            "zh-Hant",
            "PROJECT_ADAPTER_VALUE",
        ):
            self.assertIn(term, guide)
        self.assertIn("Base 전체의 고정 4개 언어 의무가 아니다", guide)

    def test_responsive_ui_preserves_semantics_not_pixel_coordinates(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "PC_STANDARD",
            "PC_WIDE",
            "MOBILE_LANDSCAPE",
            "SAME_INFORMATION_HIERARCHY_NOT_PIXEL_IDENTICAL",
            "SAME_PRIMARY_ACTION_SEMANTICS",
            "anchors",
            "containers",
            "safe area",
        ):
            self.assertIn(term, guide)

    def test_existing_dedicated_local_environment_and_hera_boundaries_are_reused(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
            "ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP",
            "fresh project-scoped PowerShell",
            "self-contained Godot",
            "project-scoped HiGodot",
            "project-scoped CODEX_HOME",
            "Hera",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "one copy/paste",
        ):
            self.assertIn(term, guide)
        self.assertIn("별도 PowerShell 설치본", guide)
        self.assertIn("금지 도구가 아니다", guide)

    def test_incident_recovery_searches_existing_cases_before_generalizing(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "BASE_CASE_RECOVERY_LOOP",
            "docs/knowledge/cases/**",
            "skills/SKILL_LEARNING_LOG.md",
            "[수정제안서]/**",
            "BOUNDED_WORKAROUND_OR_RECOVERY",
            "NEW_VERIFIED_CASE_IF_NEEDED",
            "BCP_ONLY_IF_GENERALIZABLE",
            "재현",
            "회귀",
            "비사용 조건",
        ):
            self.assertIn(term, guide)

    def test_narrative_event_ideation_starts_from_message_and_characters_without_forced_moral(self) -> None:
        guide = read(GUIDE_PATH)
        for term in (
            "MESSAGE_AND_CHARACTER_BEFORE_EVENT",
            "MESSAGE_OR_QUESTION",
            "CHARACTER_VALUES_WANTS_RELATIONSHIPS",
            "EVENT_PRESSURE",
            "CHOICE_OR_ACTION",
            "CONSEQUENCE",
            "AFTERMATH",
            "강제 교훈",
        ):
            self.assertIn(term, guide)

    def test_orchestration_does_not_create_a_new_broad_skill(self) -> None:
        registry = read(REGISTRY_PATH)
        for forbidden in (
            '"skill_id":"project-creation-delivery-orchestration"',
            '"skill_id":"serial-visual-production"',
            '"skill_id":"multi-language-responsive-game-ui"',
        ):
            self.assertNotIn(forbidden, registry)


if __name__ == "__main__":
    unittest.main()
