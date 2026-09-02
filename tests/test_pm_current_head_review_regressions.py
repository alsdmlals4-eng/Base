from __future__ import annotations

import copy
from pathlib import Path
import unittest

from tests.test_project_work_tracking import HEAD, done_receipt, run_cli, tracked_receipt


ROOT = Path(__file__).resolve().parents[1]


class PMCurrentHeadReviewRegressionTests(unittest.TestCase):
    def test_failed_closeout_suppresses_untrusted_board_actions(self) -> None:
        value = done_receipt()
        value["project_work_kanban"]["next_action"] = "Start unrelated next goal"

        result = run_cli(value, "--phase", "closeout", "--render-markdown")

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("PM VIEW: INFORMATION ONLY; EXECUTION BLOCKED", result.stdout)
        self.assertNotIn("Start unrelated next goal", result.stdout)
        self.assertIn("실행 Gate 오류", result.stdout)

    def test_blocked_benchmark_suppresses_task_actions(self) -> None:
        value = tracked_receipt()
        value["benchmark_preflight_receipt"] = {
            "state": "BLOCKED_UNVERIFIED",
            "blocked_sources": ["required original source"],
        }

        result = run_cli(value, "--phase", "start", "--render-markdown")

        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("PM VIEW: INFORMATION ONLY; EXECUTION BLOCKED", result.stdout)
        self.assertNotIn("Run behavior tests", result.stdout)
        self.assertIn("실행 Gate 오류", result.stdout)

    def test_selected_active_item_is_marked_in_pm_view(self) -> None:
        value = tracked_receipt()
        board = value["project_work_kanban"]
        review = copy.deepcopy(board["work_items"][0])
        review.update(
            work_item_id="PM-02",
            title="Independent review",
            status="VERIFY_REVIEW",
            next_action="Review PM-02 evidence",
        )
        board["work_item_refs"].append("PM-02")
        board["work_items"].append(review)
        board["active_work_item_ref"] = "PM-01"

        result = run_cli(value, "--phase", "resume", "--render-markdown")

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PM-01 · IN_PROGRESS · ACTIVE", result.stdout)
        self.assertNotIn("PM-02 · VERIFY_REVIEW · ACTIVE", result.stdout)

    def test_resume_render_ignores_closeout_only_head_input(self) -> None:
        value = done_receipt()
        board = value["project_work_kanban"]
        active = tracked_receipt()["project_work_kanban"]["work_items"][0]
        active.update(work_item_id="PM-02", title="Continue implementation")
        board["work_item_refs"].append("PM-02")
        board["work_items"].append(active)
        board["active_work_item_ref"] = "PM-02"
        board["next_action"] = "Continue PM-02"

        result = run_cli(
            value,
            "--phase",
            "resume",
            "--expected-head-sha",
            "b" * 40,
            "--render-markdown",
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("1 / 2", result.stdout)
        self.assertIn("[x] PM-01 · DONE", result.stdout)
        self.assertNotIn("VERIFY_REVIEW_STALE_HEAD", result.stdout)

    def test_registered_adapter_contract_uses_executable_root_pm_gate(self) -> None:
        text = (ROOT / "docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md").read_text(encoding="utf-8")
        for required in (
            "project_work_kanban",
            "PROJECT_WORK_ITEM_CHECKLIST.md",
            "--phase start",
            "--expected-source-sha",
            "--render-markdown",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_final_closeout_is_after_merge_and_postmerge_readback(self) -> None:
        text = (ROOT / "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md").read_text(
            encoding="utf-8"
        )
        anchors = (
            "PREMERGE_CANDIDATE",
            "FINAL_PR_HEAD_CI_REVIEW_REQUIRED",
            "NORMAL_PROTECTED_MERGE",
            "MERGED_MAIN_POSTMERGE_READBACK",
            "POSTMERGE_CLOSEOUT",
        )
        positions = [text.index(anchor) for anchor in anchors]
        self.assertEqual(sorted(positions), positions)
        closeout_command = text.index("--phase closeout", positions[-1])
        self.assertGreater(closeout_command, positions[-1])
        self.assertIn("merge·postmerge가 필수 작업이면 closeout 전에 DONE으로 표시하지 않는다", text)


if __name__ == "__main__":
    unittest.main()
