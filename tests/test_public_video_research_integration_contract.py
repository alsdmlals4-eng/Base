from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class PublicVideoResearchIntegrationContractTests(unittest.TestCase):
    def test_reference_implementation_and_registry_are_connected(self) -> None:
        self.assertTrue((ROOT / "tools/public_video_research_ingest.py").is_file())
        registry = read("docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md")
        production = read("docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md")

        for term in (
            "RM-TOOL-005",
            "PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER",
            "REFERENCE_IMPLEMENTATION_EXISTS",
            "tools/public_video_research_ingest.py",
            "LOCAL_RESEARCH_ONLY",
            "ASR_FALLBACK_REQUIRED",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, registry + "\n" + production)

    def test_visual_provider_adapter_is_provider_neutral_and_project_owned(self) -> None:
        registry = read("docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md")
        visual = read("docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md")

        for term in (
            "RM-VIS-006",
            "VISUAL_CREATIVE_PROVIDER_ADAPTER",
            "AI_SERVICE | LOCAL_MODEL | MANUAL | OUTSOURCE",
            "PROJECT_ASSET_APPROVED",
            "HUMAN_EDIT_DELTA",
        ):
            self.assertIn(term, registry + "\n" + visual)

        self.assertIn("project_visual_canon_ref", visual)
        self.assertIn("provider는", visual)
        self.assertIn("새 지출", visual)

    def test_human_edit_delta_stays_under_existing_workflow_eval_owner(self) -> None:
        production = read("docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md")
        self.assertIn("RM-WORK-002 · SKILL_WORKFLOW_PATTERN_EVAL", production)
        self.assertIn("HUMAN_EDIT_DELTA", production)
        for term in (
            "baseline_total_minutes",
            "candidate_generation_or_creation_minutes",
            "attempt_count",
            "human_edit_minutes",
            "integration_minutes",
            "qa_minutes",
            "net_minutes_saved",
        ):
            self.assertIn(term, production)
        self.assertNotIn("RM-WORK-003 · HUMAN_EDIT_DELTA", production)

    def test_reuse_scan_requires_public_video_provenance_without_committing_full_transcript(self) -> None:
        template = read("templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md")
        for term in (
            "Public video evidence provenance",
            "transcript_source_kind",
            "retrieval_tool_and_version",
            "timestamp_evidence",
            "content_claim_ceiling",
            "BLOCKED_UNVERIFIED",
            "전체 제3자 transcript 전문",
            "HUMAN_EDIT_DELTA",
        ):
            self.assertIn(term, template)

    def test_design_explicitly_rejects_new_broad_hub_and_paid_default_fallback(self) -> None:
        design = read("docs/superpowers/specs/2026-08-22-public-video-research-and-creative-provider-adapters-design.md")
        for term in (
            "new_broad_skill: NONE",
            "new_hub_or_gui: NONE",
            "incremental_paid_cost: 0",
            "유료 transcript API",
            "No video/audio download",
        ):
            self.assertIn(term, design)


if __name__ == "__main__":
    unittest.main()
