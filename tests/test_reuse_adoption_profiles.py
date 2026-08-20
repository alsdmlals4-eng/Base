from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = ROOT / "docs/knowledge/game-development/reuse/adoption/profiles"
PROJECT_KEYS = (
    "COC_FICTION",
    "GRIMOIRE",
    "SWITCHY",
    "TETRIS",
    "URBAN_LEGEND",
    "NINJA_SURVIVAL",
    "MY_LITTLE_BOAT",
    "BLACKSMITH",
    "TEN_PACES",
    "OMENWARD",
)


def load_adoption_module():
    module_path = ROOT / "tools/reuse_modules/reuse_adoption.py"
    spec = importlib.util.spec_from_file_location("reuse_adoption_profiles", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_matrix() -> dict:
    return json.loads(
        (ROOT / "docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json").read_text(
            encoding="utf-8"
        )
    )


class ReuseAdoptionProfileTests(unittest.TestCase):
    def test_all_active_projects_have_machine_valid_profiles_matching_matrix(self) -> None:
        module = load_adoption_module()
        matrix = load_matrix()
        for project_key in PROJECT_KEYS:
            profile_path = PROFILE_ROOT / f"{project_key}.json"
            self.assertTrue(profile_path.is_file(), project_key)
            profile = module.load_manifest(profile_path)
            self.assertEqual(matrix["base_reference_commit"], profile["base_source_commit"])
            self.assertEqual(matrix["projects"][project_key]["modules"], {
                module_id: config["state"]
                for module_id, config in profile["modules"].items()
            })

    def test_enabled_profiles_use_project_specific_destinations(self) -> None:
        expected_destinations = {
            ("SWITCHY", "RM-SYS-001"): "game/reuse/grid_placement_rule_engine.gd",
            ("SWITCHY", "RM-VIS-001"): "game/reuse/semantic_ui_skin_kit.gd",
            ("SWITCHY", "RM-VIS-002"): "game/reuse/gameplay_symbol_atlas.gd",
            ("OMENWARD", "RM-SYS-003"): "vendor/base-reuse/candidate_draft_weight_engine.gd",
            ("MY_LITTLE_BOAT", "RM-VIS-001"): "scripts/base_reuse/semantic_ui_skin_kit.gd",
            ("MY_LITTLE_BOAT", "RM-VIS-002"): "scripts/base_reuse/gameplay_symbol_atlas.gd",
        }
        for (project_key, module_id), destination in expected_destinations.items():
            profile = json.loads((PROFILE_ROOT / f"{project_key}.json").read_text(encoding="utf-8"))
            self.assertEqual("enabled", profile["modules"][module_id]["state"])
            self.assertEqual(destination, profile["modules"][module_id]["destination"])

    def test_adapted_project_implementation_is_not_mislabeled_as_vendored_source(self) -> None:
        profile = json.loads((PROFILE_ROOT / "URBAN_LEGEND.json").read_text(encoding="utf-8"))
        matrix = load_matrix()
        self.assertEqual("ADOPTED_AND_VERIFIED", matrix["projects"]["URBAN_LEGEND"]["status"])
        self.assertEqual("deferred", profile["modules"]["RM-TOOL-001"]["state"])
        self.assertEqual("deferred", matrix["projects"]["URBAN_LEGEND"]["modules"]["RM-TOOL-001"])

    def test_safe_project_rollout_merges_are_recorded_without_overclaiming_runtime(self) -> None:
        matrix = load_matrix()
        expected_merges = {
            "COC_FICTION": "fabc8fc489ff77459b31f0d62906966d94d79d88",
            "GRIMOIRE": "5b51169130c97807234a0c2b457ed90dc3c04f3a",
            "MY_LITTLE_BOAT": "91dc7c0a7df400eda426971b2cabc1a7de688a06",
            "URBAN_LEGEND": "1e75e5dc871ce1ce4d547b0521f6e9b680c46684",
            "NINJA_SURVIVAL": "a84980661767b02391f85d87e8fc4e9fc5dc67e7",
            "BLACKSMITH": "c09d074bd32be889630922896ffdb8ed8c68118d",
            "OMENWARD": "67487c932cc883db95da7bc852f4eb33883f0052",
        }
        for project_key, merge_commit in expected_merges.items():
            installation = matrix["projects"][project_key]["manifest_installation"]
            self.assertEqual("INSTALLED_ON_MAIN", installation["state"])
            self.assertEqual(merge_commit, installation["merge_commit"])

        self.assertEqual(
            "Fiction operating system 32305116843 SUCCESS",
            matrix["projects"]["COC_FICTION"]["manifest_installation"]["verification"],
        )
        self.assertEqual(
            "Validate GRIMOIRE planning and Base v9.4.3 32305233259 SUCCESS",
            matrix["projects"]["GRIMOIRE"]["manifest_installation"]["verification"],
        )
        boat = matrix["projects"]["MY_LITTLE_BOAT"]["manifest_installation"]
        self.assertEqual("STATIC_PROFILE_BLOB_MATCH", boat["verification"])
        self.assertEqual("NOT_RUN_NO_PROJECT_CI", boat["runtime_validation"])
        urban = matrix["projects"]["URBAN_LEGEND"]["manifest_installation"]
        self.assertEqual("Validate Base v9 adoption 32306238522 SUCCESS", urban["verification"])
        self.assertEqual("FULL_PROJECT_REGRESSIONS_SUCCESS_ADAPTED_VALIDATOR_UNCHANGED", urban["runtime_validation"])

        ninja = matrix["projects"]["NINJA_SURVIVAL"]
        self.assertEqual("READY_TO_ADOPT", ninja["status"])
        self.assertEqual("GUT 32317360022 SUCCESS", ninja["manifest_installation"]["verification"])
        self.assertEqual(
            "GODOT_IMPORT_MAIN_SCENE_SMOKE_FULL_GUT_SUCCESS_MANIFEST_ONLY",
            ninja["manifest_installation"]["runtime_validation"],
        )

        blacksmith = matrix["projects"]["BLACKSMITH"]
        self.assertEqual("DEFERRED_PRODUCT_GATE", blacksmith["status"])
        self.assertEqual(
            "Validate Base v9 adoption 32317369978 SUCCESS",
            blacksmith["manifest_installation"]["verification"],
        )
        self.assertEqual(
            "BASE_V9_ADVERSARIAL_AND_PROJECT_REGRESSIONS_SUCCESS_PRODUCT_GATE_UNCHANGED",
            blacksmith["manifest_installation"]["runtime_validation"],
        )

        omenward = matrix["projects"]["OMENWARD"]
        self.assertEqual("ADOPTED_AND_VERIFIED", omenward["status"])
        self.assertEqual("VENDORED_REFERENCE_WITH_PROJECT_ADAPTER", omenward["project_adoption_mode"])
        installation = omenward["manifest_installation"]
        self.assertEqual(
            "Base v9 adoption 32364532263 SUCCESS; Omenward Core Godot 32364532205/96411071736 SUCCESS",
            installation["verification"],
        )
        self.assertEqual(
            "GODOT_4_7_1_IMPORT_ALL_HEADLESS_RUNTIME_SMOKE_SUCCESS_SIDECAR_ONLY",
            installation["runtime_validation"],
        )
        self.assertIn("PRODUCTION_CONSUMER_NOT_CONNECTED", omenward["evidence_ceiling"])
        self.assertEqual(199, omenward["followup_issue"])
        self.assertNotIn("runtime_rollout_policy", omenward)

    def test_ten_paces_rollout_is_deferred_when_current_main_keeps_advancing(self) -> None:
        ten = load_matrix()["projects"]["TEN_PACES"]
        installation = ten["manifest_installation"]
        self.assertEqual("DEFERRED_CONCURRENT_MAIN_CHURN", installation["state"])
        self.assertEqual([167, 169], installation["attempted_prs"])
        self.assertEqual(
            [
                "d1fbe2de9675401e6b5db1b2dd4463b516c261c2",
                "f199eb7963b2012ff8a5ec8540117c1fd49db8cd",
                "c5c54096829c1778996b32873203b85db7d9318a",
            ],
            installation["observed_main_commits"],
        )
        self.assertEqual("NOT_RUN_NO_MANIFEST_INSTALLED", installation["runtime_validation"])
        self.assertIn("concurrent planning", ten["blocker"])

    def test_little_boat_defer_remains_and_omenward_defer_is_superseded(self) -> None:
        matrix = load_matrix()
        decision = json.loads(
            (
                ROOT
                / "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_DEFER_DECISION_2026-08-20.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual("FINAL_WITH_PARTIAL_SUPERSESSION", decision["state"])
        self.assertEqual("MY_LITTLE_BOAT_ONLY", decision["current_effect"])

        boat = matrix["projects"]["MY_LITTLE_BOAT"]
        policy = boat["runtime_rollout_policy"]
        self.assertEqual("DEFER_TO_PROJECT_WORK", policy["state"])
        self.assertEqual("USER_APPROVED", policy["authority"])
        self.assertEqual("2026-08-20", policy["decided_on"])
        self.assertEqual(["RM-VIS-001", "RM-VIS-002"], policy["modules"])
        self.assertFalse(policy["project_files_changed"])
        self.assertEqual("NONE", policy["merge_action"])
        self.assertEqual("DEFER_TO_PROJECT_WORK", decision["projects"]["MY_LITTLE_BOAT"]["state"])
        self.assertEqual("READY_TO_ADOPT", boat["status"])
        self.assertEqual("INSTALLED_ON_MAIN", boat["manifest_installation"]["state"])
        self.assertEqual("NOT_RUN_NO_PROJECT_CI", boat["manifest_installation"]["runtime_validation"])
        self.assertIn("project work", boat["blocker"])

        omenward_decision = decision["projects"]["OMENWARD"]
        self.assertEqual("SUPERSEDED_BY_LATER_USER_APPROVAL", omenward_decision["state"])
        self.assertEqual(198, omenward_decision["superseding_pr"])
        self.assertEqual("67487c932cc883db95da7bc852f4eb33883f0052", omenward_decision["replacement_merge"])
        self.assertEqual("SQUASH_MERGED", omenward_decision["merge_action"])
        self.assertTrue(omenward_decision["project_files_changed"])

    def test_project_work_handoff_routes_every_project_to_reuse_before_new_build(self) -> None:
        handoff_path = (
            ROOT
            / "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json"
        )
        self.assertTrue(handoff_path.is_file())
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
        matrix = load_matrix()
        registry = (
            ROOT
            / "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md"
        ).read_text(encoding="utf-8")
        adoption_readme = (
            ROOT
            / "docs/knowledge/game-development/reuse/adoption/README.md"
        ).read_text(encoding="utf-8")

        self.assertEqual("CURRENT_PROJECT_WORK_HANDOFF", handoff["state"])
        self.assertEqual("ONLY_DURING_APPROVED_PROJECT_WORK", handoff["install_policy"])
        self.assertEqual([], handoff["preinstall_projects"])
        self.assertEqual(set(PROJECT_KEYS), set(handoff["projects"]))
        self.assertEqual(
            "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json",
            matrix["project_work_handoff"],
        )

        for required_step in (
            "READ_CURRENT_PROJECT_AUTHORITY",
            "READ_BASE_REUSE_STATE",
            "EXISTING_MODULE_FIRST",
            "PROJECT_REUSE_OPPORTUNITY_SCAN_IF_NEEDED",
            "ADAPT_OR_EXTRACT_WITH_PROJECT_IDENTITY",
            "IMPLEMENT_ONLY_INSIDE_APPROVED_PROJECT_SCOPE",
        ):
            self.assertIn(required_step, handoff["entry_contract"])

        for required_field in (
            "selected_modules",
            "reuse_mode",
            "project_paths_changed",
            "verification_evidence",
            "evidence_ceiling",
            "rollback",
            "project_only_lessons",
            "base_promotion_candidates",
        ):
            self.assertIn(required_field, handoff["exit_handoff_fields"])

        for project_key in PROJECT_KEYS:
            project = handoff["projects"][project_key]
            self.assertEqual(matrix["projects"][project_key]["repository"], project["repository"])
            self.assertEqual(
                f"docs/knowledge/game-development/reuse/adoption/profiles/{project_key}.json",
                project["profile"],
            )
            self.assertTrue(project["priority_reference_modules"])
            self.assertTrue(project["project_owned_identity"])
            self.assertTrue(project["next_project_work_action"])
            self.assertTrue(project["do_not_flatten_project_identity"])
            for module_id in project["priority_reference_modules"]:
                self.assertIn(module_id, registry)

        for term in (
            "PROJECT_WORK_REUSE_ENTRY_GATE",
            "PROJECT_WORK_REUSE_EXIT_HANDOFF",
            "PROJECT_WORK_REUSE_HANDOFF.json",
            "templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md",
        ):
            self.assertIn(term, adoption_readme)


if __name__ == "__main__":
    unittest.main()