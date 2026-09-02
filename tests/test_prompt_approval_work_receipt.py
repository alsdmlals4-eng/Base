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


def _receipt() -> dict:
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


class PromptApprovalWorkReceiptTests(unittest.TestCase):
    def test_retained_receipt_binds_the_user_approved_contract(self) -> None:
        value = _receipt()
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

    def test_retained_receipt_tracks_premerge_or_postmerge_truth(self) -> None:
        value = _receipt()
        board = value["project_work_kanban"]
        tasks = {task["work_item_id"]: task for task in board["work_items"]}
        statuses = {identity: task["status"] for identity, task in tasks.items()}

        if board["active_work_item_ref"] is None:
            self.assertEqual(
                {identity: "DONE" for identity in board["work_item_refs"]},
                statuses,
            )
            verified_heads = {task["verified_head_sha"] for task in tasks.values()}
            self.assertEqual(1, len(verified_heads))
            expected_head = next(iter(verified_heads))
            self.assertEqual("STOP_APPROVED_SCOPE_COMPLETE", board["next_action"])
            self.assertEqual(
                [],
                validate_execution_receipt(
                    value,
                    phase="closeout",
                    expected_source_sha=SOURCE,
                    expected_head_sha=expected_head,
                ),
            )
        else:
            self.assertEqual("PAEG-04", board["active_work_item_ref"])
            self.assertEqual(
                {
                    "PAEG-01": "DONE",
                    "PAEG-02": "DONE",
                    "PAEG-03": "DONE",
                    "PAEG-04": "VERIFY_REVIEW",
                },
                statuses,
            )
            self.assertEqual(
                [],
                validate_execution_receipt(
                    value,
                    phase="resume",
                    expected_source_sha=SOURCE,
                ),
            )
            closeout_errors = validate_execution_receipt(
                value,
                phase="closeout",
                expected_source_sha=SOURCE,
                expected_head_sha=tasks["PAEG-03"]["verified_head_sha"],
            )
            self.assertTrue(
                any("closeout requires all required work_items DONE" in error for error in closeout_errors),
                closeout_errors,
            )

    def test_retained_receipt_rejects_contract_drift(self) -> None:
        value = _receipt()
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
