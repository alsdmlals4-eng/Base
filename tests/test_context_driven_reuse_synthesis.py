from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md"
SYNTHESIS = ROOT / "docs/knowledge/research/CONTEXT_DRIVEN_REUSE_SYNTHESIS.md"
SCAN = ROOT / "templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md"
REGISTRY = ROOT / "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md"
ARTIFACT = ROOT / "docs/knowledge/game-development/reuse/HUMAN_FACING_ARTIFACT_SYNTHESIS.md"
P0 = ROOT / "docs/knowledge/game-development/reuse/P0_IMPLEMENTATION_PILOT.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def table_row(text: str, module_id: str) -> str:
    for line in text.splitlines():
        if line.startswith("|") and f"`{module_id}`" in line:
            return line
    raise AssertionError(f"missing Registry row for {module_id}")


class ContextDrivenReuseSynthesisTests(unittest.TestCase):
    def test_pipeline_supports_evidence_and_context_origins_without_collapsing_validation(self) -> None:
        text = read(PIPELINE)
        for marker in (
            "CANDIDATE_ORIGIN_GATE",
            "EVIDENCE_DERIVED",
            "CONTEXT_SYNTHESIZED",
            "HYBRID",
            "SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS",
            "CONTEXT_SYNTHESIS_IS_NOT_VALIDATION",
            "EVIDENCE_REQUIRED_FOR_PROMOTION",
            "CONTEXT_DRIVEN_REUSE_SYNTHESIS.md",
        ):
            self.assertIn(marker, text)

    def test_context_synthesis_contract_is_falsifiable_and_yagni_bounded(self) -> None:
        text = read(SYNTHESIS)
        for marker in (
            "PLANNED_MULTI_CONSUMER",
            "PREDICTED_REPEAT_COST",
            "ONE_INPUT_MULTI_OUTPUT",
            "RESPONSIBILITY_TANGLE",
            "COMPOSITION_OPPORTUNITY",
            "CROSS_PROJECT_PLAN_PATTERN",
            "USER_REUSE_INTENT",
            "context_basis:",
            "planned_consumers:",
            "falsification_test:",
            "smallest_pilot:",
            "rollback_or_discard_condition:",
            "VAGUE_FUTURE_USE_IS_NOT_A_TRIGGER",
        ):
            self.assertIn(marker, text)

    def test_project_reuse_scan_records_origin_maturity_validation_and_context_basis(self) -> None:
        text = read(SCAN)
        for marker in (
            "candidate_origin:",
            "EVIDENCE_DERIVED | CONTEXT_SYNTHESIZED | HYBRID",
            "maturity:",
            "validation_state:",
            "context_basis:",
            "planned_consumers:",
            "falsification_test:",
            "smallest_pilot:",
            "SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS",
            "EVIDENCE_REQUIRED_FOR_PROMOTION",
        ):
            self.assertIn(marker, text)

    def test_registry_defines_three_axis_state_and_human_artifact_candidate(self) -> None:
        text = read(REGISTRY)
        for marker in (
            "candidate_origin",
            "EVIDENCE_DERIVED",
            "CONTEXT_SYNTHESIZED",
            "HYBRID",
            "maturity",
            "validation_state",
            "RM-WORK-003",
            "HUMAN_FACING_ARTIFACT_SYNTHESIS",
        ):
            self.assertIn(marker, text)

        row = table_row(text, "RM-WORK-003")
        self.assertIn("HYBRID", row)
        self.assertIn("MODULE_CONTRACT_DEFINED", row)
        self.assertIn("VALIDATION_NOT_RUN", row)
        self.assertNotIn("BASE_ACTIVE_METHOD", row)

    def test_presentation_pattern_is_provider_neutral_and_preserves_canon_boundaries(self) -> None:
        text = read(ARTIFACT)
        for marker in (
            "INPUT_MODE_GENERATE",
            "INPUT_MODE_STRUCTURE_EXISTING",
            "INPUT_MODE_IMPORT",
            "OUTLINE_BEFORE_LAYOUT",
            "CLAIM_AND_EVIDENCE_CHECK",
            "BRAND_VISUAL_CONSTRAINTS_BEFORE_GENERATION",
            "EDITABLE_BLOCK_ARTIFACT",
            "LAYOUT_VARIANTS_WITH_CONTENT_PRESERVATION",
            "CLAIM_GAP_REVIEW_AFTER_GENERATION",
            "HUMAN_VISUAL_REVIEW",
            "IMPORTED_CONTENT_IS_NOT_IMPORTED_VISUAL_CANON",
            "EXPORT_IS_DERIVATIVE_NOT_CANON",
            "PROVIDER_USE_IS_OPTIONAL_NOT_BASE_DEPENDENCY",
        ):
            self.assertIn(marker, text)

        for provider in ("Gamma", "Canva", "Beautiful.ai", "Pitch", "SlidesAI"):
            self.assertIn(provider, text)

        self.assertNotRegex(text, re.compile(r"DEFAULT_PROVIDER\s*:\s*(Gamma|Canva|Beautiful\.ai|Pitch|SlidesAI)"))

    def test_completed_main_p0_reference_implementations_are_not_reported_as_unbuilt(self) -> None:
        registry = read(REGISTRY)
        pilot = read(P0)
        module_ids = (
            "RM-TOOL-001",
            "RM-SYS-001",
            "RM-SYS-003",
            "RM-VIS-001",
            "RM-VIS-002",
            "RM-TOOL-003",
        )
        for module_id in module_ids:
            with self.subTest(module_id=module_id):
                self.assertIn(module_id, pilot)
                row = table_row(registry, module_id)
                self.assertIn("REFERENCE_IMPLEMENTATION_EXISTS", row)
                self.assertNotIn("IMPLEMENTATION_NOT_BUILT", row)


if __name__ == "__main__":
    unittest.main()
