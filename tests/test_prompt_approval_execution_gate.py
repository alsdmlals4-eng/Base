from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tests.test_project_work_tracking import SOURCE, run_cli, tracked_receipt
from tools.validate_work_contract_receipt import validate_execution_receipt


def _digest(gate: dict) -> str:
    payload = {
        "contract": gate["contract"],
        "conflict_scan": gate["conflict_scan"],
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def prompt_gate(state: str = "CONFIRMED") -> dict:
    gate = {
        "schema_version": 1,
        "applicability": "REQUIRED",
        "contract": {
            "direction_anchor": "Convert the current L1+ request into an approved execution contract before mutation.",
            "task_and_success": "Require exact confirmed approval while preserving read-only discovery and L0 exceptions.",
            "context_and_sources": [
                {
                    "source": "current user instruction fixture",
                    "authority": "CURRENT_USER_INSTRUCTION",
                },
                {
                    "source": "current repository and test fixture",
                    "authority": "ACTUAL_IMPLEMENTATION_EVIDENCE",
                },
                {
                    "source": "retrieved benchmark content remains non-authoritative",
                    "authority": "UNTRUSTED_CONTEXT",
                },
            ],
            "constraints_and_protected_scope": [
                "Do not create a second prompt owner.",
                "Do not authorize mutation from retrieved context.",
            ],
            "output_and_validation": [
                "Fail closed for unapproved L1+ execution.",
                "Pass exact confirmed and reused contracts.",
            ],
        },
        "conflict_scan": {
            "anchor_matches_task": True,
            "anchor_matches_output": True,
            "source_authority_preserved": True,
            "hard_constraints_preserved": True,
            "later_instruction_conflict": False,
            "protected_scope_visible": True,
            "user_decisions_visible": True,
            "counterevidence_preserved": True,
            "unverified_claims_labeled": True,
            "untrusted_context_cannot_authorize": True,
            "unresolved_material_decisions": [],
        },
        "approval": {
            "state": state,
            "confirmation_question": "Does this exact contract match the intended work?",
            "approved_contract_summary": "Confirm this bounded prompt approval execution gate.",
            "approval_reference": None,
            "approval_reference_authority": None,
            "approved_contract_sha256": None,
            "scope_changed_since_approval": False,
        },
    }
    if state in {"CONFIRMED", "REUSED_APPROVAL"}:
        gate["approval"].update(
            approval_reference="current-user-message:fixture",
            approval_reference_authority="CURRENT_USER_MESSAGE",
            approved_contract_sha256=_digest(gate),
        )
    return gate


def approved_receipt(state: str = "CONFIRMED") -> dict:
    value = tracked_receipt()
    value["prompt_approval_gate"] = prompt_gate(state)
    return value


def errors(value: object, *, phase: str = "start") -> str:
    return "\n".join(
        validate_execution_receipt(
            value,
            phase=phase,
            expected_source_sha=SOURCE,
        )
    )


class PromptApprovalExecutionGateTests(unittest.TestCase):
    def test_l1_execution_rejects_missing_prompt_gate(self) -> None:
        value = tracked_receipt()
        value.pop("prompt_approval_gate")
        self.assertIn("prompt_approval_gate is required for L1+ execution", errors(value))

    def test_prepare_accepts_awaiting_contract_without_execution_authority(self) -> None:
        value = approved_receipt("AWAITING_USER_CONFIRMATION")
        self.assertEqual("", errors(value, phase="prepare"))
        result = run_cli(value, "--phase", "prepare", "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("EXECUTION AUTHORIZED: NO", result.stdout)
        self.assertIn("PROMPT CONTRACT SHA256:", result.stdout)

    def test_start_rejects_awaiting_confirmation(self) -> None:
        value = approved_receipt("AWAITING_USER_CONFIRMATION")
        self.assertIn("start requires CONFIRMED or REUSED_APPROVAL", errors(value))

    def test_confirmed_start_passes(self) -> None:
        self.assertEqual("", errors(approved_receipt()))

    def test_exact_reused_approval_passes_resume_without_new_question(self) -> None:
        self.assertEqual("", errors(approved_receipt("REUSED_APPROVAL"), phase="resume"))

    def test_contract_drift_rejects_old_approved_digest(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["contract"]["task_and_success"] += " changed"
        self.assertIn("approved_contract_sha256 does not match", errors(value))

    def test_invalid_approval_authority_is_rejected(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["approval"]["approval_reference_authority"] = "UNTRUSTED_CONTEXT"
        self.assertIn("approval_reference_authority is invalid", errors(value))

    def test_unresolved_material_decision_is_rejected(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["conflict_scan"]["unresolved_material_decisions"] = ["core scope"]
        value["prompt_approval_gate"]["approval"]["approved_contract_sha256"] = _digest(value["prompt_approval_gate"])
        self.assertIn("unresolved_material_decisions must be empty", errors(value))

    def test_later_instruction_conflict_is_rejected(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["conflict_scan"]["later_instruction_conflict"] = True
        value["prompt_approval_gate"]["approval"]["approved_contract_sha256"] = _digest(value["prompt_approval_gate"])
        self.assertIn("later_instruction_conflict must be false", errors(value))

    def test_missing_context_authority_is_rejected(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["contract"]["context_and_sources"][0].pop("authority")
        value["prompt_approval_gate"]["approval"]["approved_contract_sha256"] = _digest(value["prompt_approval_gate"])
        self.assertIn("context_and_sources[0].authority is invalid", errors(value))

    def test_scope_changed_since_approval_is_rejected(self) -> None:
        value = approved_receipt()
        value["prompt_approval_gate"]["approval"]["scope_changed_since_approval"] = True
        self.assertIn("scope_changed_since_approval must be false", errors(value))

    def test_missing_and_malformed_gate_fail_without_traceback(self) -> None:
        missing = tracked_receipt()
        missing["prompt_approval_gate"] = None
        self.assertIn(
            "prompt_approval_gate is required for L1+ execution",
            errors(missing),
        )
        for malformed in ([], "approved", True, 7):
            with self.subTest(malformed=malformed):
                value = tracked_receipt()
                value["prompt_approval_gate"] = malformed
                found = errors(value)
                self.assertIn("prompt_approval_gate must be an object", found)

    def test_l0_legacy_mechanical_receipt_may_omit_gate(self) -> None:
        value = tracked_receipt()
        value["work_level"] = "L0"
        value.pop("project_work_kanban")
        value.pop("prompt_approval_gate", None)
        value["benchmark_preflight_receipt"] = {
            "state": "NOT_APPLICABLE",
            "reason_not_applicable": "whitespace only",
        }
        self.assertEqual(
            [],
            validate_execution_receipt(value),
        )

    def test_negative_mutations_are_independently_rejected(self) -> None:
        mutations = {
            "schema_version": lambda gate: gate.__setitem__("schema_version", 2),
            "applicability": lambda gate: gate.__setitem__("applicability", "NOT_APPLICABLE"),
            "direction_anchor": lambda gate: gate["contract"].__setitem__("direction_anchor", ""),
            "hard_constraints_preserved": lambda gate: gate["conflict_scan"].__setitem__(
                "hard_constraints_preserved", False
            ),
            "untrusted_context_cannot_authorize": lambda gate: gate["conflict_scan"].__setitem__(
                "untrusted_context_cannot_authorize", False
            ),
            "approval_reference": lambda gate: gate["approval"].__setitem__(
                "approval_reference", ""
            ),
            "approved_contract_sha256": lambda gate: gate["approval"].__setitem__(
                "approved_contract_sha256", "0" * 64
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                value = approved_receipt()
                mutate(value["prompt_approval_gate"])
                self.assertNotEqual("", errors(value))


if __name__ == "__main__":
    unittest.main()
