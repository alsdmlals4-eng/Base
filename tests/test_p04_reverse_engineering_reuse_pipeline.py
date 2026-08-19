from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class P04ReverseEngineeringReusePipelineTests(unittest.TestCase):
    def test_global_pipeline_covers_cross_domain_reuse(self) -> None:
        doc = read("docs/BENCHMARK_REVERSE_ENGINEERING_AND_REUSE_PIPELINE.md")
        for term in (
            "PROJECT_REUSE_OPPORTUNITY_SCAN",
            "REUSABLE_UNIT_DISCOVERY",
            "GENRE_FOUNDATION_REFERENCE",
            "SYSTEM_PATTERN",
            "TOOL_PATTERN",
            "ASSET_MATERIAL_PATTERN",
            "WORKFLOW_PATTERN",
            "SKILL_PATTERN",
            "TEST_QA_PATTERN",
            "CLEAN_ROOM_REIMPLEMENTATION",
            "NOVELTY_DELTA",
            "REUSE_OWNER_ROUTING",
        ):
            self.assertIn(term, doc)

    def test_skill_reference_is_project_first_not_example_limited(self) -> None:
        ref = read(
            "skills/analyzing-and-refining-game-concepts/references/"
            "reverse-engineering-reuse-pipeline.md"
        )
        for term in (
            "PROJECT_CANON_FIRST",
            "BOTTLENECK_TO_CANDIDATE_SEARCH",
            "EXAMPLE_IS_NOT_SCOPE_LIMIT",
            "EXISTING_SOLUTION_FIRST",
            "PROJECT_SPECIFIC_SYNTHESIS",
            "VERTICAL_SLICE_EVIDENCE_CEILING",
        ):
            self.assertIn(term, ref)

    def test_scan_template_includes_non_genre_candidates_and_authority_boundaries(self) -> None:
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
            "DIRECT_LICENSED_REUSE",
            "PATTERN_EXTRACT",
            "CLEAN_ROOM_REIMPLEMENTATION",
            "PROJECT_ONLY",
            "BASE_PROMOTION_CANDIDATE",
        ):
            self.assertIn(term, template)

        self.assertIn("discovery != PROJECT_ASSET_APPROVED", template)
        self.assertIn("discovery != NEW_SKILL_APPROVED", template)
        self.assertIn("discovery != RUNTIME_PROOF", template)


if __name__ == "__main__":
    unittest.main()
