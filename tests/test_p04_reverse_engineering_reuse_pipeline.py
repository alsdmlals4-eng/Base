from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class P04ReverseEngineeringReusePipelineTests(unittest.TestCase):
    def test_benchmark_guide_defines_cross_domain_reuse_pipeline(self) -> None:
        guide = read("docs/BENCHMARKING_REFERENCE_GUIDE.md")

        for term in (
            "BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE",
            "REUSABLE_UNIT_DISCOVERY",
            "PROJECT_FIT_DISCOVERY",
            "GENRE_FOUNDATION_REFERENCE",
            "MECHANIC_PATTERN_LIBRARY",
            "SYSTEM_PATTERN",
            "TOOL_PATTERN",
            "ASSET_MATERIAL_PATTERN",
            "WORKFLOW_PATTERN",
            "SKILL_PATTERN",
            "CLEAN_ROOM_REIMPLEMENTATION",
            "NOVELTY_DELTA",
        ):
            self.assertIn(term, guide)

    def test_shared_reference_requires_project_first_opportunity_scan(self) -> None:
        reference = read(
            "docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md"
        )

        for term in (
            "PROJECT_REUSE_OPPORTUNITY_SCAN",
            "PROJECT_CANON_FIRST",
            "BOTTLENECK_TO_CANDIDATE_SEARCH",
            "EXAMPLE_IS_NOT_SCOPE_LIMIT",
            "EXISTING_SOLUTION_FIRST",
            "REUSE_OWNER_ROUTING",
            "PROJECT_SPECIFIC_SYNTHESIS",
            "VERTICAL_SLICE_EVIDENCE_CEILING",
            "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md",
            "재사용·변형·project adapter",
        ):
            self.assertIn(term, reference)

    def test_reuse_scan_template_covers_non_genre_reusable_units(self) -> None:
        template = read("templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md")

        for term in (
            "Genre foundation",
            "Mechanic / system",
            "Content / data schema",
            "UI / UX",
            "Tool / automation",
            "Asset / image material",
            "Workflow / work structure",
            "Skill / evaluation",
            "Testing / QA",
            "NOVELTY_DELTA",
            "DIRECT_LICENSED_REUSE",
            "PATTERN_EXTRACT",
            "CLEAN_ROOM_REIMPLEMENTATION",
            "PROJECT_ONLY",
            "BASE_PROMOTION_CANDIDATE",
        ):
            self.assertIn(term, template)

    def test_pipeline_does_not_promote_discovery_to_asset_or_skill_authority(self) -> None:
        reference = read(
            "docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md"
        )

        self.assertIn("discovery != PROJECT_ASSET_APPROVED", reference)
        self.assertIn("discovery != NEW_SKILL_APPROVED", reference)
        self.assertIn("discovery != RUNTIME_PROOF", reference)
        self.assertIn("권리", reference)
        self.assertIn("라이선스", reference)

    def test_current_active_projects_have_reusable_module_catalog(self) -> None:
        registry = read(
            "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md"
        )

        for project_key in (
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
        ):
            self.assertIn(project_key, registry)

        for module_id in (
            "RM-SYS-001",
            "RM-SYS-003",
            "RM-SYS-005",
            "RM-SYS-011",
            "RM-SYS-012",
            "RM-SYS-013",
            "RM-SYS-015",
            "RM-SYS-016",
            "RM-SYS-017",
            "RM-SYS-018",
            "RM-SYS-019",
            "RM-SYS-020",
            "RM-NAR-001",
            "RM-NAR-002",
            "RM-TOOL-001",
            "RM-TOOL-003",
            "RM-VIS-001",
            "RM-VIS-003",
            "RM-WORK-001",
            "RM-WORK-002",
        ):
            self.assertIn(module_id, registry)

        for term in (
            "MODULE_CONTRACT_DEFINED",
            "IMPLEMENTATION_NOT_BUILT",
            "RIGHTS_REVIEW_REQUIRED",
            "NOTION_HUMAN_VIEW",
        ):
            self.assertIn(term, registry)

    def test_reusable_module_catalog_keeps_family_contracts_separate(self) -> None:
        gameplay = read(
            "docs/knowledge/game-development/reuse/GAMEPLAY_AND_CONTENT_MODULES.md"
        )
        production = read(
            "docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md"
        )
        visual = read(
            "docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md"
        )

        for term in (
            "GRID_PLACEMENT_RULE_ENGINE",
            "NARRATIVE_NODE_CHOICE_STATE_ENGINE",
            "CARD_ACTION_EFFECT_ENGINE",
            "SURVIVOR_AUTO_COMBAT_PROGRESSION_CORE",
            "FALLING_BLOCK_LINE_CLEAR_CORE",
        ):
            self.assertIn(term, gameplay)

        for term in (
            "DATA_SCHEMA_CROSSREF_VALIDATOR",
            "DETERMINISTIC_SEED_REPLAY_CAPTURE",
            "BALANCE_SCENARIO_BATCH_SIMULATOR",
            "PROJECT_REUSE_OPPORTUNITY_SCAN",
            "SKILL_WORKFLOW_PATTERN_EVAL",
        ):
            self.assertIn(term, production)

        for term in (
            "SEMANTIC_UI_SKIN_KIT",
            "GAMEPLAY_SYMBOL_ATLAS",
            "MODULAR_BACKGROUND_LAYER_KIT",
            "COMBAT_TELEGRAPH_VFX_KIT",
            "PORTRAIT_STATE_VARIANT_KIT",
        ):
            self.assertIn(term, visual)

        self.assertIn("TETRIS_TRADE_DRESS_BOUNDARY", gameplay)
        self.assertIn("DIRECT_LICENSED_REUSE", visual)
        self.assertIn("PROJECT_ASSET_APPROVED", visual)

    def test_p0_reference_implementations_exist(self) -> None:
        for path in (
            "tools/reuse_modules/data_schema_crossref_validator.py",
            "templates/reuse-modules/godot/grid_placement_rule_engine.gd",
            "templates/reuse-modules/godot/candidate_draft_weight_engine.gd",
            "templates/reuse-modules/godot/semantic_ui_skin_kit.gd",
            "templates/reuse-modules/godot/gameplay_symbol_atlas.gd",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_data_schema_crossref_validator_detects_core_failures(self) -> None:
        module_path = ROOT / "tools/reuse_modules/data_schema_crossref_validator.py"
        spec = importlib.util.spec_from_file_location("data_schema_crossref_validator", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "items.json").write_text(
                json.dumps([
                    {"id": "A", "kind": "weapon", "target_id": "MISSING"},
                    {"id": "A", "kind": "invalid", "target_id": "MISSING"},
                    {"id": "B", "kind": "armor"},
                ]),
                encoding="utf-8",
            )
            manifest = {
                "files": [
                    {
                        "path": "items.json",
                        "records": "$",
                        "id_field": "id",
                        "required_fields": ["id", "kind", "target_id"],
                        "enum_fields": {"kind": ["weapon", "armor"]},
                    }
                ],
                "references": [
                    {
                        "source_file": "items.json",
                        "field": "target_id",
                        "target_file": "items.json",
                        "target_id_field": "id",
                        "allow_null": True,
                    }
                ],
            }
            report = module.validate_manifest(root, manifest)
            codes = {item["code"] for item in report["violations"]}
            self.assertTrue({"DUPLICATE_ID", "MISSING_REQUIRED_FIELD", "INVALID_ENUM", "DANGLING_REFERENCE"}.issubset(codes))
            self.assertFalse(report["ok"])

    def test_p0_godot_reference_modules_are_pure_bounded_helpers(self) -> None:
        grid = read("templates/reuse-modules/godot/grid_placement_rule_engine.gd")
        draft = read("templates/reuse-modules/godot/candidate_draft_weight_engine.gd")
        skin = read("templates/reuse-modules/godot/semantic_ui_skin_kit.gd")
        symbols = read("templates/reuse-modules/godot/gameplay_symbol_atlas.gd")

        for source in (grid, draft, skin, symbols):
            self.assertIn("extends RefCounted", source)
            self.assertNotIn("get_tree()", source)
            self.assertNotIn("autoload", source.lower())

        for term in ("OUT_OF_BOUNDS", "OCCUPIED", "preview_payload", "project_predicates"):
            self.assertIn(term, grid)
        for term in ("RandomNumberGenerator", "seed", "reason_trace", "duplicate_policy"):
            self.assertIn(term, draft)
        for term in ("semantic_role", "state", "fallback", "project_skin"):
            self.assertIn(term, skin)
        for term in ("symbol_id", "shape_cue", "text_cue", "color_is_not_sufficient"):
            self.assertIn(term, symbols)

    def test_reuse_adoption_contract_surfaces_exist(self) -> None:
        for path in (
            "tools/reuse_modules/reuse_adoption.py",
            "templates/reuse-modules/PROJECT_REUSE_ADOPTION_MANIFEST.json",
            "docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json",
            "docs/knowledge/game-development/reuse/adoption/README.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_reuse_adoption_tool_applies_selected_module_and_detects_drift(self) -> None:
        module_path = ROOT / "tools/reuse_modules/reuse_adoption.py"
        spec = importlib.util.spec_from_file_location("reuse_adoption", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manifest = {
                "schema_version": 1,
                "base_source_commit": "8553678f70e22f193a2336b591f677dcfa5a8965",
                "modules": {
                    "RM-SYS-001": {
                        "state": "enabled",
                        "source": "templates/reuse-modules/godot/grid_placement_rule_engine.gd",
                        "destination": "vendor/base-reuse/grid_placement_rule_engine.gd",
                    },
                    "RM-SYS-003": {"state": "not_applicable"},
                },
            }
            report = module.apply_adoption(ROOT, project_root, manifest)
            self.assertTrue(report["ok"])
            vendor = project_root / "vendor/base-reuse/grid_placement_rule_engine.gd"
            lock = project_root / ".base-reuse/adoption-lock.json"
            self.assertTrue(vendor.is_file())
            self.assertTrue(lock.is_file())
            self.assertTrue(module.check_adoption(ROOT, project_root, manifest)["ok"])

            vendor.write_text(vendor.read_text(encoding="utf-8") + "\n# project modification\n", encoding="utf-8")
            drift = module.check_adoption(ROOT, project_root, manifest)
            self.assertFalse(drift["ok"])
            self.assertIn("LOCAL_MODIFICATION", {item["code"] for item in drift["violations"]})
            refused = module.apply_adoption(ROOT, project_root, manifest)
            self.assertFalse(refused["ok"])
            self.assertIn("REFUSE_OVERWRITE_LOCAL_MODIFICATION", {item["code"] for item in refused["violations"]})

    def test_reuse_adoption_manifest_rejects_unknown_module_or_state(self) -> None:
        module_path = ROOT / "tools/reuse_modules/reuse_adoption.py"
        spec = importlib.util.spec_from_file_location("reuse_adoption_invalid", module_path)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)

        invalid = {
            "schema_version": 1,
            "base_source_commit": "x",
            "modules": {"RM-UNKNOWN": {"state": "magic"}},
        }
        with self.assertRaises(ValueError):
            module.validate_manifest(invalid)

    def test_active_project_adoption_matrix_covers_all_projects_and_states(self) -> None:
        matrix = json.loads(read("docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json"))
        projects = matrix["projects"]
        expected = {
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
        }
        self.assertEqual(expected, set(projects))
        allowed = {
            "ADOPTED_AND_VERIFIED",
            "READY_TO_ADOPT",
            "DEFERRED_OPEN_PR",
            "DEFERRED_PHASE_GATE",
            "DEFERRED_PRODUCT_GATE",
            "NOT_APPLICABLE",
        }
        self.assertTrue(all(project["status"] in allowed for project in projects.values()))
        self.assertEqual("ADOPTED_AND_VERIFIED", projects["URBAN_LEGEND"]["status"])


if __name__ == "__main__":
    unittest.main()
