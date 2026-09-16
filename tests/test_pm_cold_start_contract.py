from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.validate_work_contract_receipt import (
    compute_prompt_contract_sha256,
    validate_execution_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates/project-operations"
PROMPT_GATE = TEMPLATES / "PROMPT_APPROVAL_GATE_RECEIPT.json"
PROMPT_REFERENCE = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "prompt-approval-execution-gate.md"
)
SOURCE = "1bc9c0cbc679f1d88cf1652d48df9273ba234401"


class PMColdStartContractTests(unittest.TestCase):
    def test_canonical_startup_and_prompt_fragment_are_executable_after_confirmation(self):
        text = (TEMPLATES / "WORK_PROJECT_START_CANON_CHECKLIST.md").read_text(encoding="utf-8")
        section = text.split("### 12.1 Receipt extension", 1)[1].split("### 12.2", 1)[0]
        match = re.search(r"```json\s*\n(.*?)\n```", section, re.S)
        self.assertIsNotNone(match)
        value = json.loads(match.group(1))
        for field in (
            "work_level",
            "benchmark_preflight_receipt",
            "context_configuration_hygiene",
            "project_work_kanban",
        ):
            self.assertIn(field, value)

        value["prompt_approval_gate"] = json.loads(PROMPT_GATE.read_text(encoding="utf-8"))
        self.assertTrue(
            validate_execution_receipt(
                value,
                phase="prepare",
                expected_source_sha=SOURCE,
            )
        )

        def fill(item):
            if isinstance(item, dict):
                return {key: fill(child) for key, child in item.items()}
            if isinstance(item, list):
                return [fill(child) for child in item]
            if isinstance(item, str) and item.startswith("<") and item.endswith(">"):
                return "explicit test fixture, not production evidence"
            return item

        value = fill(value)
        value["project_work_kanban"]["source_main_sha"] = SOURCE
        self.assertEqual(
            [],
            validate_execution_receipt(
                value,
                phase="prepare",
                expected_source_sha=SOURCE,
            ),
        )
        start_errors = validate_execution_receipt(
            value,
            phase="start",
            expected_source_sha=SOURCE,
        )
        self.assertTrue(
            any("requires CONFIRMED or REUSED_APPROVAL" in error for error in start_errors),
            start_errors,
        )

        approval = value["prompt_approval_gate"]["approval"]
        approval.update(
            state="CONFIRMED",
            approval_reference="repository-approved-test-fixture:cold-start",
            approval_reference_authority="REPOSITORY_APPROVED_DECISION",
        )
        approval["approved_contract_sha256"] = compute_prompt_contract_sha256(
            value["prompt_approval_gate"]
        )
        self.assertEqual(
            [],
            validate_execution_receipt(
                value,
                phase="start",
                expected_source_sha=SOURCE,
            ),
        )

    def test_prompt_gate_fragment_and_reference_are_current(self):
        gate = json.loads(PROMPT_GATE.read_text(encoding="utf-8"))
        self.assertEqual(1, gate["schema_version"])
        self.assertEqual("REQUIRED", gate["applicability"])
        self.assertEqual("AWAITING_USER_CONFIRMATION", gate["approval"]["state"])
        self.assertIsNone(gate["approval"]["approved_contract_sha256"])

        reference = PROMPT_REFERENCE.read_text(encoding="utf-8")
        for required in (
            "PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED",
            "--phase prepare",
            "EXECUTION AUTHORIZED: NO",
            "CONFIRMED | REUSED_APPROVAL",
            "UNTRUSTED_CONTEXT",
            "compute_prompt_contract_sha256()",
        ):
            with self.subTest(required=required):
                self.assertIn(required, reference)

    def test_cold_start_commands_supply_trusted_source_and_display(self):
        for name in (
            "PROJECT_START_HERE.md",
            "AI_WORKFLOW.md",
            "WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
        ):
            text = (TEMPLATES / name).read_text(encoding="utf-8")
            commands = [
                line
                for line in text.splitlines()
                if "python " in line and "validate_work_contract_receipt.py --receipt" in line
            ]
            self.assertTrue(commands, name)
            for line in commands:
                with self.subTest(file=name):
                    self.assertIn("--expected-source-sha", line)
                    self.assertIn("--render-markdown", line)
                    self.assertIn("--phase start", line)

    def test_transition_order_selects_active_before_execution_gate(self):
        text = (TEMPLATES / "PROJECT_WORK_ITEM_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertNotIn("다음 작업 선택 전 --phase resume", text)
        self.assertIn("다음 승인 작업을 먼저 선택해 IN_PROGRESS", text)
        self.assertIn("INFORMATION ONLY; EXECUTION BLOCKED", text)


if __name__ == "__main__":
    unittest.main()
