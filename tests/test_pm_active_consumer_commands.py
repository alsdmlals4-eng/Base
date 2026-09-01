from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools.validate_work_contract_receipt import validate_execution_receipt


ROOT = Path(__file__).resolve().parents[1]
INTAKE = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
DECOMPOSITION = ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md"
EXECUTION_PLAN = ROOT / "templates/planning/EXECUTION_SEQUENCE_PLAN.md"
START_CHECKLIST = ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"
CARD = ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md"
ENTRYPOINTS = (
    ROOT / "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
    ROOT / "templates/project-operations/AI_WORKFLOW.md",
    ROOT / "templates/project-operations/PROJECT_START_HERE.md",
    ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
    ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
)


class PMActiveConsumerCommandTests(unittest.TestCase):
    def read(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"active PM consumer missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_intake_root_example_is_valid_for_actual_start_execution(self) -> None:
        text = self.read(INTAKE)
        match = re.search(
            r"WORK_CONTRACT_RECEIPT_ROOT_JSON_EXAMPLE\s*```json\s*(\{.*?\})\s*```",
            text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "intake must publish one executable root receipt")
        assert match is not None
        receipt = json.loads(match.group(1))
        board = receipt.get("project_work_kanban")
        self.assertIsInstance(board, dict)
        source = board.get("source_main_sha")
        self.assertEqual(
            [],
            validate_execution_receipt(
                receipt,
                phase="start",
                expected_source_sha=source,
            ),
        )

    def test_active_planning_consumers_use_the_execution_gate_not_history_only_validation(self) -> None:
        for path in (INTAKE, DECOMPOSITION, EXECUTION_PLAN, START_CHECKLIST):
            with self.subTest(path=path):
                text = self.read(path)
                for token in (
                    "project_work_kanban",
                    "--phase start",
                    "--expected-source-sha",
                    "--render-markdown",
                ):
                    self.assertIn(token, text)

    def test_every_documented_closeout_supplies_a_trusted_final_head(self) -> None:
        for path in (INTAKE, DECOMPOSITION, EXECUTION_PLAN, START_CHECKLIST, CARD, *ENTRYPOINTS):
            with self.subTest(path=path):
                text = self.read(path)
                if "--phase closeout" in text:
                    self.assertIn("--expected-head-sha", text)


if __name__ == "__main__":
    unittest.main()
