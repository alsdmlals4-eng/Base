from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
