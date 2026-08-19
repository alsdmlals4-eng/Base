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

    def test_skill_reference_requires_project_first_opportunity_scan(self) -> None:
        reference = read(
            "skills/analyzing-and-refining-game-concepts/references/"
            "reverse-engineering-reuse-pipeline.md"
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
            "skills/analyzing-and-refining-game-concepts/references/"
            "reverse-engineering-reuse-pipeline.md"
        )

        self.assertIn("discovery != PROJECT_ASSET_APPROVED", reference)
        self.assertIn("discovery != NEW_SKILL_APPROVED", reference)
        self.assertIn("discovery != RUNTIME_PROOF", reference)
        self.assertIn("권리", reference)
        self.assertIn("라이선스", reference)


if __name__ == "__main__":
    unittest.main()
