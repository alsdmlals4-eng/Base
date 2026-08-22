from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
EVALUATION_SKILL = ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md"
OPERATING_SKILL = ROOT / "skills/managing-game-project-operating-system/SKILL.md"
PROJECT_SKILL = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
SHARED_ROUTES = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"
START_HERE = ROOT / "START_HERE.md"
DOCUMENTATION_MAP = ROOT / "docs/DOCUMENTATION_MAP.md"
DESIGN = ROOT / "docs/superpowers/specs/2026-08-07-godot-higodot-gut-hera-toolchain-design.md"


class GodotHiGodotGutHeraToolchainTests(unittest.TestCase):
    def test_canonical_policy_separates_author_test_and_live_qa_authorities(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for marker in (
            "SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY",
            "authority_count: 1",
            "DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "persistent_source_mutation: forbidden",
        ):
            self.assertIn(marker, text)

    def test_gut_adoption_is_exact_compatible_and_gdscript_scoped(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for godot_version, gut_version in (
            ("4.7.x", "9.7.1"),
            ("4.6.x", "9.6.1"),
            ("4.5.x", "9.5.0"),
            ("4.3.x–4.4.x", "9.4.0"),
            ("4.2.x", "9.3.0"),
        ):
            self.assertIn(godot_version, text)
            self.assertIn(gut_version, text)
        for marker in (
            "official compatibility matrix",
            "exact version",
            "McpTestSuite",
            "C#/.NET",
            "GDScript",
        ):
            self.assertIn(marker, text)

    def test_hera_acceptance_path_is_read_qa_only_and_source_clean(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for marker in (
            "hera_cli_addon_pair: EXACT_MATCH_REQUIRED",
            "transport: LOCALHOST_ONLY",
            "shared_token: REQUIRED_FOR_BASE_ADOPTION",
            "persistent_editor_write: FORBIDDEN",
            "acceptance_source_delta: NONE",
            "DIAGNOSTIC_ONLY",
            "acceptance_evidence: false",
            "restore_or_restart_required: true",
        ):
            self.assertIn(marker, text)

    def test_high_nutrient_runtime_qa_patterns_are_absorbed_without_second_default_provider(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for marker in (
            "EXTERNAL_RUNTIME_QA_PATTERN_ABSORB_ONLY",
            "HERA_REMAINS_DEFAULT_LIVE_QA_PROVIDER",
            "RUNTIME_QA_SCENARIO_PACKET",
            "WALL_CLOCK_APPROX_REPLAY_IS_NOT_DETERMINISTIC_STATE_REPLAY",
            "STRUCTURED_STATE_BEFORE_SCREENSHOT",
            "VISUAL_DIFF_TWO_AXIS_TOLERANCE",
            "PERFORMANCE_SAMPLE_WINDOW",
            "DIAGNOSTIC_SETUP_IS_NOT_ACCEPTANCE_PATH",
            "mrf/godot-stagehand",
            "satelliteoflove/godot-mcp",
        ):
            self.assertIn(marker, text)

    def test_evaluation_owner_routes_gut_and_hera_without_blanket_installation(self) -> None:
        text = EVALUATION_SKILL.read_text(encoding="utf-8")
        for marker in (
            "godot_test_framework",
            "gut_exact_version",
            "gut_test_consumption_path",
            "hera_cli_addon_pair",
            "hera_live_qa_consumption_path",
            "hera_source_delta_guard",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "McpTestSuite",
            "INSTALLED_UNUSED",
        ):
            self.assertIn(marker, text)

    def test_project_operating_owner_allows_restricted_hera_not_second_writer(self) -> None:
        text = OPERATING_SKILL.read_text(encoding="utf-8")
        for marker in (
            "GUT",
            "Hera",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "INSTALLED_UNUSED",
            "third-party",
            "persistent mutation authority",
        ):
            self.assertIn(marker, text)

    def test_installed_project_skill_stages_author_test_live_qa(self) -> None:
        text = PROJECT_SKILL.read_text(encoding="utf-8")
        for marker in (
            "HiGodot author",
            "GUT deterministic GDScript test",
            "Hera live QA",
            "LIVE_QA_AND_OBSERVABILITY_ONLY",
            "DIAGNOSTIC_ONLY",
            "source-delta",
            "NONE",
        ):
            self.assertIn(marker, text)

    def test_shared_route_adds_toolchain_discovery_without_new_shared_skill(self) -> None:
        payload = json.loads(SHARED_ROUTES.read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in payload["shared_skills"]}
        self.assertEqual(
            set(by_id),
            {
                "governing-legacy-retention-and-archives",
                "evaluating-godot-assets-and-plugins-before-creation",
            },
        )
        item = by_id["evaluating-godot-assets-and-plugins-before-creation"]
        for tag in (
            "gut",
            "gdscript-test-framework",
            "hera-agent",
            "live-runtime-qa",
            "source-delta-guard",
        ):
            self.assertIn(tag, item["trigger_tags"])
        for role in (
            "godot_test_framework",
            "gut_exact_version",
            "gut_test_consumption_path",
            "hera_cli_addon_pair",
            "hera_live_qa_consumption_path",
            "hera_source_delta_guard",
        ):
            self.assertIn(role, item["project_adapter_roles"])

    def test_cold_start_discovers_three_stage_route_from_one_canonical_policy(self) -> None:
        start = START_HERE.read_text(encoding="utf-8")
        documentation_map = DOCUMENTATION_MAP.read_text(encoding="utf-8")
        for marker in (
            "HiGodot",
            "GUT",
            "Hera",
            "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
        ):
            self.assertIn(marker, start)
            self.assertIn(marker, documentation_map)

    def test_approved_design_records_merge_authorization_without_project_installation(self) -> None:
        text = DESIGN.read_text(encoding="utf-8")
        self.assertIn("status: APPROVED_FOR_IMPLEMENTATION", text)
        self.assertIn("implementation: BASE_IMPLEMENTATION_COMPLETE", text)
        self.assertIn("project_installation: NOT_STARTED", text)
        self.assertIn("merge_authorization: GRANTED", text)


if __name__ == "__main__":
    unittest.main()
