from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_ID = "BCP-2026-006-game-youtube-devlog-marketing-workflow"
PROPOSAL_PATH = ROOT / "[수정제안서]" / PROPOSAL_ID / "PROPOSAL.md"
DESIGN_PATH = ROOT / "[수정제안서]" / PROPOSAL_ID / "DESIGN.md"
REGISTRY_PATH = ROOT / "[수정제안서]" / "PROPOSAL_REGISTRY.json"
APPROVAL_REF = "https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204"
IMPLEMENTATION_PR = "https://github.com/alsdmlals4-eng/Base/pull/174"
IMPLEMENTATION_MERGE_SHA = "5c8f2f8845a9f0e4dbaf644529c5e3cdbf5ebbd8"


class BCP006ImplementedStateTests(unittest.TestCase):
    def read_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"Missing lifecycle artifact: {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_proposal_records_implemented_state_and_evidence_limits(self) -> None:
        text = self.read_text(PROPOSAL_PATH)
        for token in (
            "- 상태: `IMPLEMENTED`",
            APPROVAL_REF,
            IMPLEMENTATION_PR,
            IMPLEMENTATION_MERGE_SHA,
            "active_skill_implementation: IMPLEMENTED",
            "real_project_video_pilot: NOT_RUN",
            "human_audience_validation: HUMAN_NOT_RUN",
            "conversion_validation: CONVERSION_UNVERIFIED",
            "production_marketing_effectiveness: NOT_PROVEN",
        ):
            self.assertIn(token, text)

    def test_design_links_the_same_implementation_without_overclaiming(self) -> None:
        text = self.read_text(DESIGN_PATH)
        for token in (
            "- 상태: `IMPLEMENTED`",
            IMPLEMENTATION_PR,
            IMPLEMENTATION_MERGE_SHA,
            "real_project_video_pilot: NOT_RUN",
            "human_audience_validation: HUMAN_NOT_RUN",
            "conversion_validation: CONVERSION_UNVERIFIED",
            "production_marketing_effectiveness: NOT_PROVEN",
        ):
            self.assertIn(token, text)

    def test_proposal_registry_matches_proposal_and_design(self) -> None:
        registry = json.loads(self.read_text(REGISTRY_PATH))
        entries = {
            entry["proposal_id"]: entry
            for entry in registry["proposals"]
        }
        self.assertIn(PROPOSAL_ID, entries)
        entry = entries[PROPOSAL_ID]
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertEqual(APPROVAL_REF, entry["approval_ref"])
        self.assertEqual(IMPLEMENTATION_PR, entry["implementation_pr"])


if __name__ == "__main__":
    unittest.main()
