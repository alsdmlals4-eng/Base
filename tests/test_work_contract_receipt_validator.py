from __future__ import annotations

import unittest

from tools.validate_work_contract_receipt import validate_receipt


def valid_receipt() -> dict:
    return {
        "work_level": "L1",
        "benchmark_preflight_receipt": {
            "state": "PASS",
            "entries": [
                {
                    "source_and_evidence": "exact repository commit and relevant consumer",
                    "observed_pattern": "existing owner separates data from presentation",
                    "project_fit_and_difference": "reuse the boundary, not project-specific content",
                    "disposition": "ADAPT",
                }
            ],
        },
        "context_configuration_hygiene": {
            "scope": "files and contracts touched by this L1 change",
            "inventory": [
                {
                    "path": "docs/example.md",
                    "classification": "ACTIVE_OWNER",
                    "owner_or_provenance": "current repository owner",
                    "references_and_consumers": "checked direct consumer",
                }
            ],
        },
    }


class WorkContractReceiptValidatorTests(unittest.TestCase):
    def test_l1_pass_receipt_requires_observable_benchmark_entry_and_scoped_hygiene(self) -> None:
        self.assertEqual([], validate_receipt(valid_receipt()))

    def test_pass_without_evidence_entry_is_rejected(self) -> None:
        receipt = valid_receipt()
        receipt["benchmark_preflight_receipt"]["entries"] = []
        self.assertIn(
            "benchmark_preflight_receipt.entries is required for PASS",
            validate_receipt(receipt),
        )

    def test_l1_cannot_claim_not_applicable_for_benchmark_preflight(self) -> None:
        receipt = valid_receipt()
        receipt["benchmark_preflight_receipt"] = {
            "state": "NOT_APPLICABLE",
            "reason_not_applicable": "formatting only",
        }
        self.assertIn(
            "NOT_APPLICABLE is restricted to L0",
            validate_receipt(receipt),
        )

    def test_blocked_preflight_requires_the_unreadable_source_or_blocker(self) -> None:
        receipt = valid_receipt()
        receipt["benchmark_preflight_receipt"] = {
            "state": "BLOCKED_UNVERIFIED",
            "blocked_sources": [],
        }
        self.assertIn(
            "blocked_sources is required for BLOCKED_UNVERIFIED",
            validate_receipt(receipt),
        )

    def test_removal_requires_reference_zero_and_recoverable_readback_evidence(self) -> None:
        receipt = valid_receipt()
        receipt["context_configuration_hygiene"]["inventory"] = [
            {
                "path": "docs/obsolete-candidate.md",
                "classification": "OBSOLETE_CANDIDATE",
                "owner_or_provenance": "confirmed duplicate",
                "references_and_consumers": "pending",
                "removal_proposed": True,
            }
        ]
        errors = validate_receipt(receipt)
        self.assertIn("references_and_consumers_zero_before_removal is required", errors)
        self.assertIn("git_recoverable_removal_and_readback is required", errors)

    def test_operator_case_reconstruction_requires_every_evidence_boundary(self) -> None:
        reconstruction = {
            "input_anchor_and_source": "operator supplied a greybox prototype request",
            "staged_execution_and_handoffs": "prototype, human test, then themed iteration",
            "human_decision_and_approval_boundary": "human selects the next prototype",
            "observable_outcome_and_evidence_ceiling": "reported outcome; no independent reproduction",
            "nontransferable_or_unobserved": "internal tooling was not available",
            "project_trial_and_acceptance_gate": "run one small project trial before adoption",
        }
        for missing_field in reconstruction:
            with self.subTest(missing_field=missing_field):
                receipt = valid_receipt()
                receipt["benchmark_preflight_receipt"]["entries"][0]["operator_case_reconstruction"] = {
                    field: value for field, value in reconstruction.items() if field != missing_field
                }
                self.assertIn(
                    f"benchmark_preflight_receipt.entries[0].operator_case_reconstruction.{missing_field} is required",
                    validate_receipt(receipt),
                )

    def test_operator_case_reconstruction_must_be_an_object(self) -> None:
        for invalid_value in (None, "reported in a public card"):
            with self.subTest(invalid_value=invalid_value):
                receipt = valid_receipt()
                receipt["benchmark_preflight_receipt"]["entries"][0]["operator_case_reconstruction"] = invalid_value
                self.assertIn(
                    "benchmark_preflight_receipt.entries[0].operator_case_reconstruction must be an object",
                    validate_receipt(receipt),
                )

    def test_complete_operator_case_reconstruction_is_accepted(self) -> None:
        receipt = valid_receipt()
        receipt["benchmark_preflight_receipt"]["entries"][0]["operator_case_reconstruction"] = {
            "input_anchor_and_source": "operator supplied a greybox prototype request",
            "staged_execution_and_handoffs": "prototype, human test, then themed iteration",
            "human_decision_and_approval_boundary": "human selects the next prototype",
            "observable_outcome_and_evidence_ceiling": "reported outcome; no independent reproduction",
            "nontransferable_or_unobserved": "internal tooling was not available",
            "project_trial_and_acceptance_gate": "run one small project trial before adoption",
        }
        self.assertEqual([], validate_receipt(receipt))


if __name__ == "__main__":
    unittest.main()
