from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "templates" / "planning" / "PC_ANDROID_DELIVERY_PROFILE.md"
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GooglePlayGamesServicesLifecycleTests(unittest.TestCase):
    def test_existing_platform_service_owner_is_reused(self) -> None:
        guide = read(GUIDE)
        profile = read(PROFILE)
        self.assertIn("platform_service_adapter", guide)
        self.assertIn("google_play:", profile)
        self.assertIn("google_play_games_services:", profile)

    def test_pgs_lifecycle_is_conditional_and_fail_closed(self) -> None:
        profile = read(PROFILE)
        for term in (
            "usage_scope: NOT_USED | PLANNED | IN_USE | UNKNOWN",
            "integration_surface: NONE | JAVA_KOTLIN | NATIVE | ENGINE_PLUGIN | UNKNOWN",
            "pgs_generation: NONE | V2 | V1_LEGACY | UNKNOWN",
            "migration_status: NOT_APPLICABLE | CURRENT_V2 | MIGRATION_REQUIRED | BLOCKED_UNVERIFIED",
            "physical_device_auth_and_feature_status:",
            "play_games_services_v2_auth_and_features_when_used",
            "google_play_games_services_lifecycle:",
        ):
            self.assertIn(term, profile)

        self.assertIn("`usage_scope: NOT_USED`이면 관련 상태는 `NOT_APPLICABLE`", profile)
        self.assertNotIn("pgs_generation: V2\n", profile)
        self.assertNotIn("migration_status: CURRENT_V2\n", profile)

    def test_pgs_identity_and_dependency_upgrade_failures_are_separate(self) -> None:
        profile = read(PROFILE)
        for term in (
            "identity_model_status:",
            "PLATFORM_AND_INGAME_SEPARATED",
            "V1_PLAYER_ID_PRIMARY_LEGACY",
            "dependency_upgrade_compile_status:",
            "platform identity",
            "primary in-game account identity",
            "compile failure",
            "release-like Android build",
        ):
            self.assertIn(term, profile)

    def test_current_official_sources_and_third_party_version_check_are_preserved(self) -> None:
        profile = read(PROFILE)
        for source in (
            "https://developer.android.com/games/pgs/deprecation",
            "https://developer.android.com/games/pgs/migration_overview",
            "https://developer.android.com/games/pgs/downloads",
        ):
            self.assertIn(source, profile)

        for term in (
            "일부가 v2일 수 있으므로",
            "exact plugin release/source",
            "Asset Library에 존재한다는 사실만으로 `CURRENT_V2`",
            "license·maintenance·permissions·tests·rollback",
        ):
            self.assertIn(term, profile)

    def test_shutdown_date_and_plugin_version_are_not_frozen_as_defaults(self) -> None:
        profile = read(PROFILE)
        self.assertIn("May/June 2027 차이", profile)
        self.assertIn("단일 종료일을 영구 상수로 복제하지 않는다", profile)
        self.assertNotIn("shutdown_at: 2027-", profile)
        self.assertNotIn("sdk_or_plugin_version: 21.0.0", profile)


if __name__ == "__main__":
    unittest.main()
