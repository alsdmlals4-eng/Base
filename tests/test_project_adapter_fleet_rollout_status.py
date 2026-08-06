from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = ROOT / "docs/operations/decisions/DEC-BASE-20260805-001.md"
AUDIT_PATH = ROOT / "docs/operations/PROJECT_ADAPTER_FLEET_AUDIT_2026-08-05.md"

COMPLETED = {
    "Ten-Paces-Hidden-Moves": (
        "PR #95",
        "7083829d8eb627e46227c0ac98845adfc2c61bb4",
    ),
    "urban-legend": (
        "PR #153",
        "1cda33f9eb238c9a32d0a8f4a3edfa5e203b0634",
    ),
    "Blacksmith": (
        "PR #112",
        "4dc4f3f8a6fc4d379c5eddce8b59fc8733e6a4ed",
    ),
    "Switchy-Express-Cargo-Puzzle": (
        "PR #87",
        "dc2a6696beced12c8e352fa154648cdb4e80796b",
    ),
}


class ProjectAdapterFleetRolloutStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.decision = DECISION_PATH.read_text(encoding="utf-8")
        self.audit = AUDIT_PATH.read_text(encoding="utf-8")

    def test_decision_records_partial_completion_without_reauthorizing_completed_projects(self) -> None:
        self.assertIn("project_rollout: PARTIAL_COMPLETE", self.decision)
        self.assertNotIn("project_mutation: AUTHORIZED_NOT_STARTED", self.decision)
        self.assertIn("completed_projects: 4", self.decision)
        self.assertIn("blocked_projects: 1", self.decision)
        self.assertIn("separately_managed_projects: 1", self.decision)
        for repository, (pr, merge_sha) in COMPLETED.items():
            self.assertIn(repository, self.decision)
            self.assertIn(pr, self.decision)
            self.assertIn(merge_sha, self.decision)

    def test_omenward_is_fail_closed_and_grimoire_is_separately_managed(self) -> None:
        for text in (self.decision, self.audit):
            self.assertIn("OMENWARD", text)
            self.assertIn("BLOCKED_ENVIRONMENT_RUNNER_AND_AUTHORIZATION", text)
            self.assertIn("PR #148", text)
            self.assertIn("GRIMOIRE", text)
            self.assertIn("SEPARATELY_MANAGED", text)

    def test_audit_matrix_reflects_current_project_disposition(self) -> None:
        self.assertIn(
            "result: FOUR_PROJECTS_MERGED_ONE_BLOCKED_ONE_SEPARATELY_MANAGED",
            self.audit,
        )
        self.assertNotIn("project_mutations: NOT_STARTED", self.audit)
        for repository, (pr, merge_sha) in COMPLETED.items():
            self.assertIn(repository, self.audit)
            self.assertIn(pr, self.audit)
            self.assertIn(merge_sha, self.audit)
        self.assertIn("SUPERSEDED_DUPLICATE_PR_113", self.audit)
        self.assertIn("SUPERSEDED_DUPLICATE_PR_90", self.audit)

    def test_evidence_ceiling_remains_truthful(self) -> None:
        for text in (self.decision, self.audit):
            self.assertIn("runtime_validation: NOT_RUN", text)
            self.assertIn("physical_device_validation: NOT_RUN", text)
            self.assertIn("human_validation: HUMAN_NOT_RUN", text)
            self.assertIn("google_sheets_sync: NOT_APPLICABLE_BASE_CONTRACT", text)


if __name__ == "__main__":
    unittest.main()
