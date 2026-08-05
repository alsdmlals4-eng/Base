from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)
PROFILE = ROOT / "templates" / "planning" / "PC_ANDROID_DELIVERY_PROFILE.md"
GUIDE_PATH = (
    "docs/knowledge/game-development/"
    "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)
PROFILE_PATH = "templates/planning/PC_ANDROID_DELIVERY_PROFILE.md"


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class PcAndroidCrossPlatformDeliveryTests(unittest.TestCase):
    maxDiff = None

    def test_required_artifacts_exist(self) -> None:
        missing = [
            str(path.relative_to(ROOT))
            for path in (GUIDE, PROFILE)
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_profile_is_conditional_not_universal(self) -> None:
        guide = read(GUIDE)
        for term in (
            "PC_ANDROID_DUAL_TARGET_CANDIDATE",
            "DUAL_TARGET_APPROVED",
            "DUAL_TARGET_CONDITIONAL",
            "SINGLE_TARGET_FIRST",
            "BLOCKED_UNVERIFIED",
            "턴제",
            "시간 압박",
            "정밀·고속 입력",
            "QA·지원 역량",
            "모든 프로젝트에 강제하지 않는다",
        ):
            self.assertIn(term, guide)

    def test_one_core_and_platform_adapter_boundary(self) -> None:
        guide = read(GUIDE)
        for term in (
            "shared_gameplay_rules",
            "shared_content_data",
            "shared_save_schema",
            "shared_deterministic_state",
            "input_adapter",
            "layout_profile",
            "lifecycle_adapter",
            "quality_profile",
            "platform_service_adapter",
            "코드 공유율",
            "PC UI를 축소",
        ):
            self.assertIn(term, guide)

    def test_ui_input_and_lifecycle_defaults(self) -> None:
        guide = read(GUIDE)
        profile = read(PROFILE)
        for term in (
            "1280 × 720",
            "canvas_items",
            "expand",
            "48 dp",
            "8 dp",
            "hover-only",
            "semantic action",
            "background",
            "foreground",
            "Android back",
            "실제 Android 기기",
        ):
            self.assertIn(term, guide)

        for term in (
            "base_resolution:",
            "orientation:",
            "stretch_mode: canvas_items",
            "stretch_aspect: expand",
            "touch_target_min_dp: 48",
            "touch_spacing_recommended_dp: 8",
            "physical_android_evidence:",
            "save_and_lifecycle:",
        ):
            self.assertIn(term, profile)

    def test_release_waves_and_volatile_store_facts(self) -> None:
        guide = read(GUIDE)
        profile = read(PROFILE)
        for term in (
            "STOVE",
            "Google Play",
            "Steam",
            "release_wave_1",
            "release_wave_2",
            "same_day_launch_required: false",
            "12명",
            "14일",
            "100달러",
            "25달러",
            "VERIFY_CURRENT_OFFICIAL_SOURCE",
            "STOVE 비용",
            "정책 확인일: 2026-08-05",
        ):
            self.assertIn(term, guide)

        for term in (
            "google_play_account_type:",
            "closed_test_requirement:",
            "tester_capacity:",
            "release_wave_1:",
            "release_wave_2:",
            "same_day_launch_required: false",
            "official_policy_checked_at:",
        ):
            self.assertIn(term, profile)

    def test_benchmark_and_evidence_limits_are_explicit(self) -> None:
        guide = read(GUIDE)
        for term in (
            "Into the Breach",
            "Slay the Spire",
            "Dicey Dungeons",
            "Balatro",
            "모바일 인터페이스를 다시 설계",
            "동시 출시의 보편적 성공 공식",
            "실제 프로젝트 Pilot",
            "HUMAN_NOT_RUN",
            "DEVICE_NOT_RUN",
        ):
            self.assertIn(term, guide)

    def test_template_contains_project_decision_and_rollback(self) -> None:
        profile = read(PROFILE)
        for term in (
            "delivery_profile_id:",
            "candidate_status:",
            "target_platforms:",
            "shared_core_contract:",
            "platform_adapters:",
            "performance_budget:",
            "test_matrix:",
            "decision:",
            "rollback:",
            "unresolved_evidence:",
        ):
            self.assertIn(term, profile)

    def test_existing_routes_discover_the_contract(self) -> None:
        for path in (
            "README.md",
            "START_HERE.md",
            "docs/knowledge/game-development/README.md",
            "skills/analyzing-and-refining-game-concepts/SKILL.md",
        ):
            text = read(path)
            self.assertIn(GUIDE_PATH, text, path)
            self.assertIn(PROFILE_PATH, text, path)

    def test_no_new_broad_skill(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        for forbidden in (
            '"skill_id":"pc-android-cross-platform-delivery"',
            '"skill_id":"cross-platform-game-development"',
            '"skill_id":"multi-platform-release-management"',
        ):
            self.assertNotIn(forbidden, registry)

    def test_change_is_recorded(self) -> None:
        changelog = read("docs/CHANGELOG.md")
        self.assertIn("PC_ANDROID_DUAL_TARGET_CANDIDATE", changelog)
        self.assertIn(GUIDE_PATH, changelog)


if __name__ == "__main__":
    unittest.main()
