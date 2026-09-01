from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/validate_work_contract_receipt.py"


def receipt():
    return {
        "work_level": "L1",
        "benchmark_preflight_receipt": {"state": "PASS", "entries": [{
            "source_and_evidence": "Base source 1bc9c0c and current validator",
            "observed_pattern": "PM template is not consumed by the CLI",
            "project_fit_and_difference": "reuse the receipt gate, add behavior validation",
            "disposition": "ADAPT"}]},
        "context_configuration_hygiene": {"scope": "PM receipt gate", "inventory": [{
            "path": "tools/validate_work_contract_receipt.py", "classification": "ACTIVE_OWNER",
            "owner_or_provenance": "Base", "references_and_consumers": "project starter CLI"}]},
    }


def run_cli(value, *args):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "receipt.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return subprocess.run([sys.executable, str(CLI), "--receipt", str(path), *args],
                              text=True, capture_output=True, check=False)


class ProjectWorkTrackingCLITests(unittest.TestCase):
    def test_default_start_gate_rejects_missing_pm_tracking(self):
        result = run_cli(receipt())
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("project_work_kanban", result.stdout)

    def test_recorded_benchmark_blocker_does_not_authorize_execution(self):
        value = receipt()
        value["benchmark_preflight_receipt"] = {
            "state": "BLOCKED_UNVERIFIED", "blocked_sources": ["required original source"]}
        result = run_cli(value)
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn("BLOCKED_UNVERIFIED", result.stdout)


def tracked_receipt():
    value = receipt()
    value["project_work_kanban"] = {
        "goal_or_slice_issue_ref": "https://github.com/alsdmlals4-eng/Base/issues/825",
        "source_main_sha": "1bc9c0cbc679f1d88cf1652d48df9273ba234401",
        "work_item_refs": ["PM-01"], "active_work_item_ref": "PM-01",
        "next_action": "Implement the approved receipt gate",
        "work_items": [{
            "work_item_id": "PM-01", "title": "PM receipt gate", "status": "IN_PROGRESS",
            "canon_owner": "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md",
            "actual_consumers": ["project startup"], "depends_on": [],
            "acceptance_criteria": ["AC-01"], "required_evidence": ["E2_TEST"],
            "checklist": [{"id": "AC-01", "text": "missing PM is rejected", "status": "IN_PROGRESS"}],
            "verification": [{"level": "E2_TEST", "status": "NOT_RUN", "evidence": []}],
            "next_action": "Run behavior tests",
        }],
    }
    return value


def done_receipt():
    value = tracked_receipt()
    board = value["project_work_kanban"]
    board["active_work_item_ref"] = None
    board["next_action"] = "STOP_APPROVED_SCOPE_COMPLETE"
    task = board["work_items"][0]
    task.update(status="DONE", verified_head_sha="a" * 40, repository_readback="PASS", readback_evidence=["recorded exact-head readback"],
                rollback="Revert isolated change", must_fix_remaining=0, blocked_unverified_remaining=0,
                user_decision_required_remaining=0, next_action="STOP_APPROVED_SCOPE_COMPLETE")
    task["checklist"][0].update(status="PASS", evidence=["recorded test run on exact head"])
    task["verification"][0].update(status="PASS", evidence=["recorded test run on exact head"])
    return value


class ProjectWorkTrackingBehaviorTests(unittest.TestCase):
    def assert_rejected(self, value, reason, *args):
        result = run_cli(value, *args)
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertIn(reason, result.stdout, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_valid_start_renders_real_work_not_empty_template(self):
        result = run_cli(tracked_receipt(), "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("0 / 1", result.stdout)
        self.assertIn("PM-01", result.stdout)
        self.assertIn("IN_PROGRESS", result.stdout)
        self.assertNotIn("[x]", result.stdout)

    def test_closeout_requires_all_work_done(self):
        self.assert_rejected(tracked_receipt(), "closeout", "--phase", "closeout")

    def test_verified_completion_is_counted(self):
        result = run_cli(done_receipt(), "--phase", "closeout", "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("1 / 1", result.stdout)
        self.assertIn("[x]", result.stdout)

    def test_wrong_progress_is_rejected(self):
        value = tracked_receipt()
        value["project_work_kanban"]["progress_summary"] = {"completed_items": 1, "applicable_items": 1}
        self.assert_rejected(value, "progress_summary")

    def test_missing_evidence_does_not_count_as_pass(self):
        value = done_receipt()
        value["project_work_kanban"]["work_items"][0]["checklist"][0]["evidence"] = []
        self.assert_rejected(value, "evidence", "--phase", "closeout")

    def test_runtime_not_run_cannot_be_relabelled_done(self):
        value = done_receipt()
        task = value["project_work_kanban"]["work_items"][0]
        task["required_evidence"].append("E3_RUNTIME")
        task["verification"].append({"level": "E3_RUNTIME", "status": "NOT_RUN", "evidence": []})
        self.assert_rejected(value, "E3_RUNTIME", "--phase", "closeout")

    def test_checkpoint_does_not_authorize_completion(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"][0].update(status="DONE", checkpoint_commit_sha="a" * 40)
        value["project_work_kanban"]["active_work_item_ref"] = None
        self.assert_rejected(value, "DONE", "--phase", "closeout")

    def test_required_acceptance_cannot_be_omitted(self):
        value = done_receipt()
        value["project_work_kanban"]["work_items"][0]["acceptance_criteria"].append("AC-02")
        self.assert_rejected(value, "AC-02", "--phase", "closeout")

    def test_empty_work_items_are_not_a_work_plan(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"] = []
        value["project_work_kanban"]["work_item_refs"] = []
        self.assert_rejected(value, "work_items")

    def test_duplicate_ids_are_rejected(self):
        import copy
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"].append(copy.deepcopy(value["project_work_kanban"]["work_items"][0]))
        self.assert_rejected(value, "duplicate")

    def test_missing_required_work_ref_is_rejected(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_item_refs"].append("PM-02")
        self.assert_rejected(value, "work_item_refs")

    def test_blocked_task_requires_reason_and_resume_condition(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"][0]["status"] = "BLOCKED_UNVERIFIED"
        self.assert_rejected(value, "resume_condition")

    def test_unfinished_dependency_does_not_unlock_ready_task(self):
        import copy
        value = tracked_receipt()
        board = value["project_work_kanban"]
        task = copy.deepcopy(board["work_items"][0])
        task.update(work_item_id="PM-02", status="READY", depends_on=["PM-01"])
        board["work_item_refs"].append("PM-02")
        board["work_items"].append(task)
        self.assert_rejected(value, "dependency")

    def test_expected_source_mismatch_is_rejected(self):
        self.assert_rejected(tracked_receipt(), "source_main_sha", "--expected-source-sha", "b" * 40)

    def test_unhashable_input_reports_errors_instead_of_crashing(self):
        value = tracked_receipt()
        value["work_level"] = []
        self.assert_rejected(value, "work_level")

    def test_l0_mechanical_work_retains_reasoned_exemption(self):
        value = receipt()
        value["work_level"] = "L0"
        value["benchmark_preflight_receipt"] = {"state": "NOT_APPLICABLE", "reason_not_applicable": "whitespace only"}
        result = run_cli(value)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


class ProjectWorkTrackingAdversarialTests(unittest.TestCase):
    def test_done_requires_exact_verified_head_not_checkpoint_only(self):
        value = done_receipt()
        value["project_work_kanban"]["work_items"][0].pop("verified_head_sha", None)
        result = run_cli(value, "--phase", "closeout")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("verified_head_sha", result.stdout)

    def test_closeout_stops_instead_of_inventing_another_goal(self):
        value = done_receipt()
        value["project_work_kanban"]["next_action"] = "Invent another unrelated game"
        result = run_cli(value, "--phase", "closeout")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("STOP_APPROVED_SCOPE_COMPLETE", result.stdout)

    def test_all_nested_malformed_fields_fail_without_traceback(self):
        import copy
        from tools.validate_work_contract_receipt import validate_execution_receipt
        paths = [
            ("work_level",), ("benchmark_preflight_receipt", "state"),
            ("benchmark_preflight_receipt", "entries", 0, "disposition"),
            ("context_configuration_hygiene", "inventory", 0, "classification"),
            ("project_work_kanban", "work_item_refs"),
            ("project_work_kanban", "active_work_item_ref"),
            ("project_work_kanban", "work_items", 0, "status"),
            ("project_work_kanban", "work_items", 0, "depends_on"),
            ("project_work_kanban", "work_items", 0, "acceptance_criteria"),
            ("project_work_kanban", "work_items", 0, "required_evidence"),
            ("project_work_kanban", "work_items", 0, "checklist", 0, "status"),
            ("project_work_kanban", "work_items", 0, "verification", 0, "status"),
        ]
        for path in paths:
            for malformed in (None, [], {}, ["x", {}], True, 7):
                with self.subTest(path=path, malformed=malformed):
                    if path[-1] == "depends_on" and malformed == []:
                        continue  # An empty dependency list is a valid independent task.
                    value = copy.deepcopy(tracked_receipt())
                    cursor = value
                    for key in path[:-1]: cursor = cursor[key]
                    cursor[path[-1]] = malformed
                    self.assertTrue(validate_execution_receipt(value))

    def test_independent_blocker_does_not_stop_active_task(self):
        import copy
        value = tracked_receipt(); board = value["project_work_kanban"]
        task = copy.deepcopy(board["work_items"][0])
        task.update(work_item_id="PM-02", status="BLOCKED_UNVERIFIED", blocker="required runtime unavailable", resume_condition="engine becomes available")
        board["work_items"].append(task); board["work_item_refs"].append("PM-02")
        result = run_cli(value, "--phase", "resume", "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("0 / 2", result.stdout)
        self.assertIn("required runtime unavailable", result.stdout)

    def test_cycle_and_wip_violation_are_both_rejected(self):
        import copy
        from tools.validate_work_contract_receipt import validate_execution_receipt
        value = tracked_receipt(); board = value["project_work_kanban"]
        task = copy.deepcopy(board["work_items"][0]); task.update(work_item_id="PM-02", depends_on=["PM-01"])
        board["work_items"][0]["depends_on"] = ["PM-02"]
        board["work_items"].append(task); board["work_item_refs"].append("PM-02")
        errors = "\n".join(validate_execution_receipt(value))
        self.assertIn("cycle", errors); self.assertIn("WIP", errors)

    def test_required_acceptance_cannot_be_waived(self):
        from tools.validate_work_contract_receipt import validate_execution_receipt
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"][0]["checklist"][0].update(status="NOT_APPLICABLE", reason="skip")
        self.assertIn("cannot be NOT_APPLICABLE", "\n".join(validate_execution_receipt(value)))

    def test_optional_not_applicable_is_excluded_from_child_count(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"][0]["checklist"].append({"id":"OPT-01", "text":"mobile build", "status":"NOT_APPLICABLE", "reason":"desktop-only tooling"})
        result = run_cli(value, "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertIn("(0 / 1)", result.stdout)

    def test_boolean_counters_are_not_zero(self):
        value = done_receipt()
        value["project_work_kanban"]["work_items"][0]["must_fix_remaining"] = False
        result = run_cli(value, "--phase", "closeout")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must_fix_remaining", result.stdout)

    def test_renderer_does_not_emit_active_links_or_html(self):
        value = tracked_receipt()
        value["project_work_kanban"]["work_items"][0]["title"] = "[click](https://example.invalid) <img src=x>"
        result = run_cli(value, "--render-markdown")
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertNotIn("[click](", result.stdout)
        self.assertNotIn("<img", result.stdout)

    def test_invalid_utf8_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"; path.write_bytes(b"\xff")
            result = subprocess.run([sys.executable, str(CLI), "--receipt", str(path)], text=True, capture_output=True)
            self.assertEqual(2, result.returncode)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
