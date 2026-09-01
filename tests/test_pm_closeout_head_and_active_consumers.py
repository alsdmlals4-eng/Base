from __future__ import annotations

import inspect
from pathlib import Path
import unittest

from tests.test_project_work_tracking import SOURCE, done_receipt
from tools.validate_work_contract_receipt import validate_execution_receipt


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONSUMERS = (
    "skills/managing-project-intake-and-work-contract/SKILL.md",
    "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
    "templates/planning/EXECUTION_SEQUENCE_PLAN.md",
)


class PMCloseoutHeadAndActiveConsumerTests(unittest.TestCase):
    def test_closeout_api_accepts_trusted_expected_head(self) -> None:
        self.assertIn("expected_head_sha", inspect.signature(validate_execution_receipt).parameters)

    def test_closeout_requires_trusted_expected_head(self) -> None:
        errors = validate_execution_receipt(
            done_receipt(),
            phase="closeout",
            expected_source_sha=SOURCE,
        )
        self.assertIn("expected_head_sha", "\n".join(errors))

    def test_closeout_rejects_receipt_verified_on_another_head(self) -> None:
        errors = validate_execution_receipt(
            done_receipt(),
            phase="closeout",
            expected_source_sha=SOURCE,
            expected_head_sha="b" * 40,
        )
        self.assertIn("verified_head_sha", "\n".join(errors))

    def test_closeout_accepts_matching_trusted_verification_target(self) -> None:
        self.assertEqual(
            [],
            validate_execution_receipt(
                done_receipt(),
                phase="closeout",
                expected_source_sha=SOURCE,
                expected_head_sha="a" * 40,
            ),
        )

    def test_all_active_execution_consumers_use_root_pm_and_trusted_start_command(self) -> None:
        for path in ACTIVE_CONSUMERS:
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("PROJECT_WORK_KANBAN_CHECKLIST", text)
                self.assertIn('"project_work_kanban"', text)
                commands = [
                    line
                    for line in text.splitlines()
                    if "validate_work_contract_receipt.py" in line and "--receipt" in line
                ]
                self.assertTrue(commands, f"{path} must contain an executable receipt command")
                self.assertTrue(
                    any(
                        all(
                            token in line
                            for token in (
                                "--phase start",
                                "--expected-source-sha",
                                "--render-markdown",
                            )
                        )
                        for line in commands
                    ),
                    f"{path} must use the trusted PM start command",
                )

    def test_closeout_docs_require_the_trusted_verification_target(self) -> None:
        for path in (
            "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
            "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
        ):
            text = (ROOT / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn("--expected-head-sha", text)
                self.assertIn("TRUSTED_VERIFICATION_TARGET_HEAD", text)


if __name__ == "__main__":
    unittest.main()
