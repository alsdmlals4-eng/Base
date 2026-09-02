from __future__ import annotations

import unittest
from pathlib import Path

from tests.test_project_work_tracking import receipt, tracked_receipt
from tools.validate_work_contract_receipt import validate_execution_receipt, validate_receipt

ROOT = Path(__file__).resolve().parents[1]


class ProjectWorkTrackingIntegrationTests(unittest.TestCase):
    def test_malformed_public_options_fail_closed(self):
        for field in ("phase", "expected_source_sha"):
            for value in ([], {}, 1):
                with self.subTest(field=field, value=value):
                    self.assertTrue(validate_execution_receipt(tracked_receipt(), **{field: value}))

    def test_record_shape_api_is_not_execution_authorization(self):
        self.assertEqual([], validate_receipt(receipt()))
        self.assertTrue(validate_execution_receipt(receipt()))

    def test_project_entrypoints_use_execution_phases_and_visible_output(self):
        for path in (
            "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
            "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
        ):
            text = (ROOT / path).read_text(encoding="utf-8")
            for token in ("PM_EXECUTION_GATE_REQUIRED", "--phase start", "--phase resume", "--phase closeout", "--expected-source-sha", "--render-markdown", "PROJECT_WORK_ITEM_CHECKLIST.md"):
                with self.subTest(path=path, token=token):
                    self.assertIn(token, text)

    def test_card_has_root_projection_and_checkpoint_boundary(self):
        text = (ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md").read_text(encoding="utf-8")
        for token in ('"work_items"', '"acceptance_criteria"', '"required_evidence"', "validate_execution_receipt()", "STOP_APPROVED_SCOPE_COMPLETE", "CHECKPOINT_IS_NOT_COMPLETION", "PM_RECONCILIATION_REQUIRED"):
            self.assertIn(token, text)

    def test_retained_executor_is_not_reactivated_by_documentation(self):
        text = (ROOT / "docs/LOOP_A2_LOCAL_EXECUTOR.md").read_text(encoding="utf-8")
        for token in ("RETAINED_EXECUTOR_NOT_DEFAULT_WORK_ROUTE", "HISTORICAL_RUN_EVIDENCE_NOT_CURRENT_PC_STATUS", "GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED", "CHECKPOINT_IS_NOT_COMPLETION"):
            self.assertIn(token, text)

    def test_repository_ci_discovers_pm_behavior_tests(self):
        text = (ROOT / ".github/workflows/validate-game-project-operating-system.yml").read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertTrue((ROOT / "tests/test_project_work_tracking.py").is_file())


if __name__ == "__main__":
    unittest.main()
