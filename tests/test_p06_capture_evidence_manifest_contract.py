from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md"
REGISTRY = ROOT / "[수정제안서]/PROPOSAL_REGISTRY.json"
PROPOSAL = ROOT / "[수정제안서]/BCP-2026-047-runtime-visual-capture-manifest-pattern/PROPOSAL.md"


class RuntimeVisualCaptureManifestContractTests(unittest.TestCase):
    def test_existing_capture_owner_exposes_an_optional_bounded_runtime_visual_manifest(self) -> None:
        text = MODULES.read_text(encoding="utf-8")
        for token in (
            "OPTIONAL_RUNTIME_VISUAL_CAPTURE_MANIFEST",
            "SMALLEST_REPRESENTATIVE_CAPTURE_SET",
            "NO_COMMON_CAPTURE_SCHEMA_OR_BINARY_POLICY",
            "source_commit_or_build:",
            "run_or_entry_identity:",
            "visible_scene_or_state:",
            "artifact_path:",
            "sha256:",
            "dimensions:",
            "actual_consumers:",
            "diagnostics_or_source_delta:",
            "evidence_ceiling:",
            "RUNTIME_VISUAL_CAPTURE_IS_NOT_HUMAN_OR_DEVICE_PASS",
        ):
            self.assertIn(token, text)

    def test_bcp047_closeout_links_the_merged_minimal_existing_owner_implementation(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        entry = next(item for item in registry["proposals"] if item["proposal_id"] == "BCP-2026-047-runtime-visual-capture-manifest-pattern")
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertIn("2026-09-01", entry["approval_ref"])
        self.assertEqual("https://github.com/alsdmlals4-eng/Base/pull/819", entry["implementation_pr"])

        proposal = PROPOSAL.read_text(encoding="utf-8")
        self.assertIn("- 상태: `IMPLEMENTED`", proposal)
        self.assertIn("구현 closeout", proposal)
        self.assertIn("PR #819", proposal)
        self.assertIn("19fb7b437b764ac2d0cf438e4361c0d02e71a40a", proposal)
        self.assertIn("새 Skill·문서·registry가 필요 없는 이유", proposal)


if __name__ == "__main__":
    unittest.main()
