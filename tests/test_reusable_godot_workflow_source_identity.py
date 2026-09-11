from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/reusable-godot-project-pilot.yml"
GUIDE = ROOT / "docs/knowledge/godot/GODOT_MULTI_PROJECT_PILOT_GUIDE.md"


class ReusableGodotWorkflowSourceIdentityTests(unittest.TestCase):
    def test_called_workflow_source_sha_must_match_base_c0_pin(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        guide = GUIDE.read_text(encoding="utf-8")

        for marker in (
            "WORKFLOW_SOURCE_SHA: ${{ job.workflow_sha }}",
            "EXPECTED_BASE_PILOT_COMMIT: ${{ inputs.base_pilot_commit }}",
            'os.environ["WORKFLOW_SOURCE_SHA"] != os.environ["EXPECTED_BASE_PILOT_COMMIT"]',
            "REUSABLE_WORKFLOW_SOURCE_SHA_MISMATCH",
        ):
            self.assertIn(marker, workflow)

        self.assertIn(
            "Every project descriptor and reusable-workflow call pins exactly that SHA",
            guide,
        )


if __name__ == "__main__":
    unittest.main()
