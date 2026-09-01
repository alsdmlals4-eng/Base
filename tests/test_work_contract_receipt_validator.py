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


if __name__ == "__main__":
    unittest.main()
