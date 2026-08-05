from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_ID = "BCP-2026-005-godot-live-editor-contract-v2"
PROPOSAL_PATH = ROOT / "[수정제안서]" / PROPOSAL_ID / "PROPOSAL.md"
REGISTRY_PATH = ROOT / "[수정제안서]" / "PROPOSAL_REGISTRY.json"
APPROVAL_REF = "https://github.com/alsdmlals4-eng/Base/pull/154#issuecomment-5187157323"
IMPLEMENTATION_PR = "https://github.com/alsdmlals4-eng/Base/pull/161"
IMPLEMENTATION_MERGE_SHA = "339a48be688e312b7894e1f2372aecfe0ee3f6f4"
C0_PILOT_PR = "https://github.com/alsdmlals4-eng/Base/pull/183"
C0_PILOT_MERGE_SHA = "0084d5a6dd546aa001ced46b8cc8e3db8f38035d"


class BCP005ImplementedStateTests(unittest.TestCase):
    def read_text(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"Missing lifecycle artifact: {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_proposal_records_implemented_state_and_evidence_chain(self) -> None:
        text = self.read_text(PROPOSAL_PATH)
        for token in (
            "- 상태: `IMPLEMENTED`",
            "- 현재 BCP 단계: `IMPLEMENTED`",
            APPROVAL_REF,
            IMPLEMENTATION_PR,
            IMPLEMENTATION_MERGE_SHA,
            "https://github.com/alsdmlals4-eng/Base/pull/162",
            "5e23aaad85842505e009fa7f1872e70576ef59f0",
            "https://github.com/alsdmlals4-eng/Base/pull/165",
            "48273f79ab261a1f064adfc7431c99a74a22c33a",
            "https://github.com/alsdmlals4-eng/Base/pull/166",
            "bd72e61722ebb4e29dd66b0885fba9428b1c14fb",
            C0_PILOT_PR,
            C0_PILOT_MERGE_SHA,
        ):
            self.assertIn(token, text)

    def test_proposal_preserves_truthful_readiness_limits(self) -> None:
        text = self.read_text(PROPOSAL_PATH)
        for token in (
            "static_v2_contract: IMPLEMENTED",
            "base_c0_multi_project_pilot: IMPLEMENTED",
            "isolated_godot_editor_runtime: PASS",
            "real_project_pilots: NOT_RUN",
            "production_transport: NOT_IMPLEMENTED",
            "mcp_profile: NOT_IMPLEMENTED",
            "runtime_debugger: NOT_IMPLEMENTED",
            "windows_production_operation: NOT_RUN",
            "physical_input: NOT_RUN",
            "human_editor_usability: HUMAN_NOT_RUN",
            "production_adapter_ready: NOT_READY",
        ):
            self.assertIn(token, text)

    def test_proposal_registry_matches_primary_implementation(self) -> None:
        registry = json.loads(self.read_text(REGISTRY_PATH))
        entries = {entry["proposal_id"]: entry for entry in registry["proposals"]}
        self.assertIn(PROPOSAL_ID, entries)
        entry = entries[PROPOSAL_ID]
        self.assertEqual("IMPLEMENTED", entry["status"])
        self.assertEqual(APPROVAL_REF, entry["approval_ref"])
        self.assertEqual(IMPLEMENTATION_PR, entry["implementation_pr"])


if __name__ == "__main__":
    unittest.main()
