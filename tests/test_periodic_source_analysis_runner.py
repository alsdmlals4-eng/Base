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
    def test_manual_analysis_module_still_uses_the_fair_batch_selector(self) -> None:
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

    def test_scheduled_workflow_prepares_queue_without_metered_model_or_repository_write_pipeline(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        contract = workflow + "\n" + runner
        for required in (
            'cron: "0 18 * * *"',
            'timezone: "Asia/Seoul"',
            "workflow_dispatch:",
            "bash tools/run_periodic_source_scan_queue.sh",
            "ZERO_INCREMENTAL_COST_QUEUE_PREP",
            "AWAITING_CHATGPT_REVIEW",
            "USER_DIRECTED_CHATGPT_REVIEW",
            "ai_api_call",
            "NONE",
            "issues: write",
        ):
            self.assertIn(required, contract)
        for forbidden in (
            "timeout-minutes",
            "pull_request_target",
            "OPENAI_API_KEY",
            "SOURCE_ANALYSIS_MODEL",
            "python -m tools.periodic_source_analysis",
            "python tools/periodic_source_analysis.py",
            "actions: write",
            "contents: write",
            "pull-requests: write",
            "automation/source-scan-",
            "gh pr create",
            "gh workflow run validate-evidence-knowledge.yml",
            "gh workflow run validate-base-v9-rc.yml",
            "gh workflow run validate-game-project-operating-system.yml",
            "gh run watch",
            "git merge --no-edit origin/main",
            "reviewThreads",
            "gh pr merge",
            "git push origin HEAD:main",
            "git push --force",
            "--admin",
            "--auto",
        ):
            self.assertNotIn(forbidden, contract)

    def test_queue_prep_is_not_scan_success_and_uses_current_open_pr_protection(self) -> None:
        queue_doc = QUEUE_DOC.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        for required in (
            "ZERO_INCREMENTAL_COST_REQUIRED",
            "AWAITING_CHATGPT_REVIEW",
            "Queue preparation",
            "NO_CHANGE",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION",
        ):
            self.assertIn(required, queue_doc)
        self.assertNotIn("BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16", queue_doc)
        for required in (
            "repository_change",
            "NONE",
            "ledger_scan_timestamp_change",
            "candidate_evidence_claim",
            "NOT_RUN",
        ):
            self.assertIn(required, runner)
        for forbidden in (
            "BLOCKED_MODEL_AUTH",
            "BLOCKED_ACTIVE_PR_GUARD",
            "assert_no_foreign_open_prs",
            "foreign_open_prs",
            "detect_foreign_overlap",
        ):
            self.assertNotIn(forbidden, runner)

    def test_actual_source_review_receipt_drives_weekly_scan_state_batch(self) -> None:
        queue_doc = QUEUE_DOC.read_text(encoding="utf-8")
        for required in (
            "ACTUAL_SOURCE_REVIEW_RECEIPT",
            "actual_source_review_receipt:",
            "scanned_source_ids: []",
            "scanned_discovery_seed_ids: []",
            "retained_candidate_source_ids: []",
            "material_candidate_count_by_source: {}",
            "merged_base_contribution_refs: []",
            "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
            "WEEKLY_SCAN_STATE_BATCH",
            "BLOCKED_UNVERIFIED_BACKFILL",
            "last_actual_review_at",
            "ledger_synced_through",
        ):
            self.assertIn(required, queue_doc)

    def test_queue_receipt_markdown_is_not_built_by_unquoted_shell_heredoc(self) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertNotIn('cat >> "$FINAL_PATH" <<EOF', runner)
        self.assertIn('python - "$FINAL_PATH" "$MODE" "$FINAL_STATE"', runner)
        self.assertIn("NO_CHANGE", runner)
        self.assertIn("```yaml", runner)

    def test_temporary_patch_and_export_files_are_removed(self) -> None:
        for path in TEMPORARY_PATCH_FILES:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
