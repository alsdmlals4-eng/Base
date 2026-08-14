from __future__ import annotations

import inspect
import unittest
from datetime import date, timedelta
from pathlib import Path

from tools.periodic_source_analysis import run_analysis
from tools.periodic_source_scan_queue import select_due_source_batch


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
RUNNER = ROOT / "tools" / "run_periodic_source_scan_queue.sh"
TEMPORARY_PATCH_FILES = (
    ROOT / ".github" / "workflows" / "tmp-export-source-rotation.yml",
    ROOT / ".github" / "workflows" / "tmp-source-workflow-permission-scope.yml",
    ROOT / "tools" / "apply_source_rotation_import.py",
    ROOT / "tools" / "apply_source_workflow_permission_scope.py",
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

    def test_equal_priority_sources_rotate_across_daily_batches(self) -> None:
        ledger = payload([f"source-{index}" for index in range(6)])
        start = date(2026, 8, 14)
        batches = [
            [
                row["source_id"]
                for row in select_due_source_batch(
                    ledger,
                    start + timedelta(days=offset),
                    batch_size=2,
                )
            ]
            for offset in range(6)
        ]
        self.assertNotEqual(batches[0], batches[1])
        self.assertEqual(
            {f"source-{index}" for index in range(6)},
            {source_id for batch in batches for source_id in batch},
        )

    def test_workflow_delegates_to_a_bounded_verified_runner_without_recursion(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        contract = workflow + "\n" + runner
        for required in (
            'cron: "0 18 * * *"',
            'timezone: "Asia/Seoul"',
            "workflow_dispatch:",
            "bash tools/run_periodic_source_scan_queue.sh",
            "automation/source-scan-",
            "gh pr create",
            "gh workflow run validate-evidence-knowledge.yml",
            "gh workflow run validate-game-project-operating-system.yml",
            "validation_level=full",
            "gh run watch",
            "git merge --no-edit origin/main",
            "reviewThreads",
            "gh pr merge",
            "--auto",
            "--squash",
            "--match-head-commit",
            "No material candidate survived the Evidence gate.",
        ):
            self.assertIn(required, contract)
        for forbidden in (
            "timeout-minutes",
            "pull_request_target",
            "git push origin HEAD:main",
            "git push --force",
            "--admin",
        ):
            self.assertNotIn(forbidden, contract)
        trigger_block = workflow.split("\npermissions:", 1)[0]
        self.assertNotIn("PERIODIC_SOURCE_CANDIDATE_LEDGER.json", trigger_block)
        self.assertNotIn("PERIODIC_SOURCE_OPERATIONS_LEDGER.json", trigger_block)

    def test_temporary_patch_and_export_files_are_removed(self) -> None:
        for path in TEMPORARY_PATCH_FILES:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
