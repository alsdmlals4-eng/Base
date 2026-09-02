from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
SKILL = ROOT / "skills" / "managing-project-intake-and-work-contract" / "SKILL.md"
OPENAI = ROOT / "skills" / "managing-project-intake-and-work-contract" / "agents" / "openai.yaml"
REFERENCE = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "prompt-approval-execution-gate.md"
)
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
TEMPLATE = ROOT / "templates" / "project-operations" / "PROMPT_APPROVAL_GATE_RECEIPT.json"
VALIDATOR = ROOT / "tools" / "validate_work_contract_receipt.py"


class PromptApprovalRoutingContractTests(unittest.TestCase):
    def test_existing_intake_owner_remains_single_owner(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertIn("모든 L1 이상 지시문 작성", agents + "\n" + skill)
        self.assertIn("Grill Me alignment gate", agents + "\n" + skill)
        self.assertNotIn('"skill_id": "prompt-approval', registry)
        self.assertNotIn('"skill_id":"prompt-approval', registry.replace(" ", ""))

    def test_openai_entrypoint_calls_the_machine_confirmation_boundary(self) -> None:
        text = OPENAI.read_text(encoding="utf-8")
        for required in (
            "source-aware prompt contract",
            "preparation mode",
            "CONFIRMED or REUSED_APPROVAL",
            "before mutation, Codex handoff, or external-agent delegation",
            "read-only discovery",
            "L0 mechanical work",
            "exact approved continuation",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_reference_template_and_validator_share_the_same_contract(self) -> None:
        reference = REFERENCE.read_text(encoding="utf-8")
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        validator = VALIDATOR.read_text(encoding="utf-8")
        for required in (
            "PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED",
            "CURRENT_USER_MESSAGE",
            "REPOSITORY_APPROVED_DECISION",
            "UNTRUSTED_CONTEXT",
            "--phase prepare",
            "scope_changed_since_approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, reference)
                self.assertIn(required, json.dumps(template, ensure_ascii=False) + validator)
        self.assertEqual("AWAITING_USER_CONFIRMATION", template["approval"]["state"])
        self.assertIsNone(template["approval"]["approved_contract_sha256"])


if __name__ == "__main__":
    unittest.main()
