from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class P06RuntimeUISemanticEvidenceContractTests(unittest.TestCase):
    def test_p06_prefers_semantic_targeting_and_rejects_ambiguous_matches(self):
        context = (
            ROOT
            / "docs"
            / "operations"
            / "base-partitions"
            / "P06_GODOT_RUNTIME_TOOLCHAIN.md"
        ).read_text(encoding="utf-8")

        self.assertIn("SEMANTIC_UI_TARGET_BEFORE_COORDINATE", context)
        self.assertIn("EXACTLY_ONE_OR_FAIL", context)
        self.assertIn("COORDINATE_FALLBACK", context)
        self.assertIn("expected_count: 1", context)

    def test_dispatch_ack_is_not_runtime_acceptance_completion(self):
        context = (
            ROOT
            / "docs"
            / "operations"
            / "base-partitions"
            / "P06_GODOT_RUNTIME_TOOLCHAIN.md"
        ).read_text(encoding="utf-8")

        self.assertIn("ACTION_DISPATCH_IS_NOT_COMPLETION", context)
        self.assertIn("dispatch_ack_is_completion: false", context)
        self.assertIn("host_observation_required: true", context)
        self.assertIn("expected_state_or_event:", context)
        self.assertIn("INCONCLUSIVE_NOT_PASS", context)

    def test_p06_reuses_existing_runtime_evidence_owners(self):
        p06 = (
            ROOT
            / "docs"
            / "operations"
            / "base-partitions"
            / "P06_GODOT_RUNTIME_TOOLCHAIN.md"
        ).read_text(encoding="utf-8")
        higodot = (
            ROOT
            / "docs"
            / "knowledge"
            / "godot"
            / "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
        ).read_text(encoding="utf-8")

        self.assertIn("HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md", p06)
        self.assertIn("STRUCTURED_STATE_BEFORE_SCREENSHOT", p06)
        self.assertIn("WALL_CLOCK_APPROX_REPLAY_IS_NOT_DETERMINISTIC_STATE_REPLAY", p06)
        self.assertIn("STRUCTURED_STATE_BEFORE_SCREENSHOT", higodot)
        self.assertIn("WALL_CLOCK_APPROX_REPLAY_IS_NOT_DETERMINISTIC_STATE_REPLAY", higodot)


if __name__ == "__main__":
    unittest.main()
