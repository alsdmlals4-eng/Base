from __future__ import annotations

import inspect
import unittest
from datetime import date, timedelta
from pathlib import Path

from tools.periodic_source_analysis import run_analysis
from tools.periodic_source_scan_queue import select_due_source_batch


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
BASE_V9_WORKFLOW = ROOT / ".github" / "workflows" / "validate-base-v9-rc.yml"
RUNNER = ROOT / "tools" / "run_periodic_source_scan_queue.sh"
QUEUE_DOC = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_SCAN_QUEUE.md"
TEMPORARY_PATCH_FILES = (
    ROOT / ".github" / "workflows" / "tmp-export-source-rotation.yml",
    ROOT / ".github" / "workflows" / "tmp-source-workflow-permission-scope.yml",
    ROOT / ".github" / "workflows" / "tmp-apply-source-validator-patch.yml",
    ROOT / "tools" / "apply_source_rotation_import.py",
    ROOT / "tools" / "apply_source_workflow_permission_scope.py",
    ROOT / "tools" / "apply_source_validator_patch.py",
)


def source(source_id: str) -> dict[str, object]:
    return {
        "source_id": source_id,
        "name": source_id,
        "domains": ["GAME_DEVELOPMENT"],
        "roles": ["AUTHORITY_TARGET"],
        "recommended_cadence": "daily-or-weekly",
        "scan_surfaces": ["recent articles"],
        "last_successful_scan_at": None,
        "last_material_candidate_at": None,
        "last_base_contribution_at": None,
        "last_base_contribution_ref": None,
        "material_candidate_count_since_tracking_start": 0,
        "base_contribution_count_since_tracking_start": 0,
        "status": "ACTIVE",
    }


def payload(ids: list[str]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "test fixture",
        "sources": [source(source_id) for source_id in ids],
    }


class PeriodicSourceAnalysisRunnerTests(unittest.TestCase):
    def test_runner_entry_point_uses_the_fair_batch_selector(self) -> None:
        self.assertTrue(callable(run_analysis))
        self.assertIn("select_due_source_batch", inspect.getsource(run_analysis))

    def test_equal_priority_sources_rotate_in_non_overlapping_daily_batches(self) -> None:
        ledger = payload([f"source-{index}" for index in range(6)])
        start = date(2026, 8, 14)
        first_cycle = [
            {
                str(row["source_id"])
                for row in select_due_source_batch(
                    ledger,
                    start + timedelta(days=offset),
                    batch_size=2,
                )
            }
            for offset in range(3)
        ]
        self.assertTrue(first_cycle[0].isdisjoint(first_cycle[1]))
        self.assertTrue(first_cycle[0].isdisjoint(first_cycle[2]))
        self.assertTrue(first_cycle[1].isdisjoint(first_cycle[2]))
        self.assertEqual(
            {f"source-{index}" for index in range(6)},
            set().union(*first_cycle),
        )

    def test_workflow_delegates_to_all_exact_head_validators_without_recursion(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        base_v9_workflow = BASE_V9_WORKFLOW.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        contract = workflow + "\n" + runner
        for required in (
            'cron: "0 18 * * *"',
            'timezone: "Asia/Seoul"',
            "workflow_dispatch:",
            "bash tools/run_periodic_source_scan_queue.sh",
            "python -m tools.periodic_source_analysis",
            "automation/source-scan-",
            "gh pr create",
            "gh workflow run validate-evidence-knowledge.yml",
            "gh workflow run validate-base-v9-rc.yml",
            "gh workflow run validate-game-project-operating-system.yml",
            "validation_level=full",
            "gh run watch",
            "git merge --no-edit origin/main",
            "reviewThreads",
            "gh pr merge",
            "--squash",
            "--match-head-commit",
            "No material candidate survived the Evidence gate.",
        ):
            self.assertIn(required, contract)
        self.assertIn("workflow_dispatch:", base_v9_workflow)
        for forbidden in (
            "timeout-minutes",
            "pull_request_target",
            "python tools/periodic_source_analysis.py",
            "git push origin HEAD:main",
            "git push --force",
            "--admin",
            "--auto",
        ):
            self.assertNotIn(forbidden, contract)
        trigger_block = workflow.split("\npermissions:", 1)[0]
        self.assertNotIn("PERIODIC_SOURCE_CANDIDATE_LEDGER.json", trigger_block)
        self.assertNotIn("PERIODIC_SOURCE_OPERATIONS_LEDGER.json", trigger_block)

    def test_scheduled_write_automation_defers_while_foreign_pr_is_open(self) -> None:
        queue_doc = QUEUE_DOC.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertIn("SCHEDULED_AUTOMATION_ACTIVE_PR_GUARD", queue_doc)
        for required in (
            "BLOCKED_ACTIVE_PR_GUARD",
            "BLOCKED_ACTIVE_PR_GUARD_QUERY",
            "BLOCKED_MERGE_NOT_IMMEDIATE",
            "foreign_open_prs",
            "assert_no_foreign_open_prs",
            'assert_no_foreign_open_prs ""',
            'assert_no_foreign_open_prs "$pr_number"',
        ):
            self.assertIn(required, runner)
        self.assertLess(
            runner.index('assert_no_foreign_open_prs ""'),
            runner.index("python -m tools.periodic_source_analysis"),
        )
        self.assertLess(
            runner.rindex('assert_no_foreign_open_prs "$pr_number"'),
            runner.rindex("gh pr merge"),
        )

    def test_temporary_patch_and_export_files_are_removed(self) -> None:
        for path in TEMPORARY_PATCH_FILES:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
