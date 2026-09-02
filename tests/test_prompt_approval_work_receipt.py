from __future__ import annotations

import json
import unittest
from pathlib import Path

from tools.prompt_approval_gate import compute_prompt_contract_sha256
from tools.validate_work_contract_receipt import validate_execution_receipt


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = (
    ROOT
    / "docs"
    / "reviews"
    / "2026-09-03-prompt-approval-execution-gate-work-receipt.json"
)
SOURCE = "850204b3e5de81a4045111b4a050c46c5a292b59"


class PromptApprovalWorkReceiptTests(unittest.TestCase):
    def test_retained_receipt_binds_the_user_approved_contract(self) -> None:
        value = json.loads(RECEIPT.read_text(encoding="utf-8"))
        gate = value["prompt_approval_gate"]
        approval = gate["approval"]

        self.assertEqual("L2", value["work_level"])
        self.assertEqual("CONFIRMED", approval["state"])
        self.assertEqual("CURRENT_USER_MESSAGE", approval["approval_reference_authority"])
        self.assertEqual(
            "current-user-message:2026-09-03:권장-통합안승인",
            approval["approval_reference"],
        )
        self.assertEqual(
            compute_prompt_contract_sha256(gate),
            approval["approved_contract_sha256"],
        )
        self.assertFalse(approval["scope_changed_since_approval"])

    def test_retained_receipt_authorizes_only_its_current_active_work_item(self) -> None:
        value = json.loads(RECEIPT.read_text(encoding="utf-8"))
        errors = validate_execution_receipt(
            value,
            phase="start",
            expected_source_sha=SOURCE,
        )
        self.assertEqual([], errors)

    def test_retained_receipt_rejects_contract_drift(self) -> None:
        value = json.loads(RECEIPT.read_text(encoding="utf-8"))
        value["prompt_approval_gate"]["contract"]["task_and_success"] += " drift"
        errors = validate_execution_receipt(
            value,
            phase="start",
            expected_source_sha=SOURCE,
        )
        self.assertTrue(
            any("approved_contract_sha256 does not match" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
