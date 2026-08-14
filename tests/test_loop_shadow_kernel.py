from __future__ import annotations

import copy
import hashlib
import importlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class LoopShadowKernelTests(unittest.TestCase):
    maxDiff = None

    def _api(self):
        spec = importlib.util.find_spec("tools.loop_shadow_kernel")
        self.assertIsNotNone(spec, "tools.loop_shadow_kernel production package is missing")
        return importlib.import_module("tools.loop_shadow_kernel")

    def _request(self, *, run_id: str = "RUN_001") -> dict[str, object]:
        return {
            "schema_version": 1,
            "contract_role": "LOOP_SHADOW_REQUEST",
            "project_id": "EXAMPLE_GAME",
            "run_id": run_id,
            "package_id": "PACKAGE_001",
            "source_main_sha": "a" * 40,
            "observed_main_sha": "a" * 40,
            "planning_status": "PLANNING_LOCKED",
            "visual_impact": "NONE",
            "visual_status": "VISUAL_NOT_APPLICABLE",
            "planning_drift": "NO_DRIFT",
            "visual_drift": "NOT_APPLICABLE",
            "approved_requirements": ["REQ_001"],
            "package_requirement_ids": ["REQ_001"],
            "coverage": [
                {
                    "requirement_id": "REQ_001",
                    "tasks": ["TASK_001"],
                    "outputs": ["scripts/example.gd"],
                    "tests": ["tests/test_example.py"],
                    "evidence": ["E2_TEST"],
                }
            ],
            "allowed_paths": ["scripts/example.gd"],
            "changed_paths": ["scripts/example.gd"],
            "required_evidence": ["E2_TEST"],
            "resource_locks": ["EXAMPLE_DOMAIN"],
            "references": [
                {
                    "project_id": "EXAMPLE_GAME",
                    "kind": "CANON",
                    "path": "docs/GDD.md",
                }
            ],
            "budgets": {
                "max_transitions": 16,
                "max_repeated_failures": 2,
            },
            "autonomy": "A2_EXECUTE_ISOLATED",
            "a3_auto_merge_allowlist": [],
            "scheduler_runtime_provider": "NOT_CONFIGURED",
        }

    def _workspace(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "scripts").mkdir()
        (root / "docs").mkdir()
        (root / "scripts/example.gd").write_text("extends Node\n", encoding="utf-8")
        (root / "docs/GDD.md").write_text("# Approved canon\n", encoding="utf-8")
        return temporary, root, root / ".loop-engineering"

    def test_valid_shadow_run_is_deterministic_and_product_read_only(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        product = root / "scripts/example.gd"
        before = hashlib.sha256(product.read_bytes()).hexdigest()

        kernel = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z")
        first = kernel.shadow(self._request())

        self.assertEqual(first.state.value, "SHADOW_COMPLETE")
        self.assertEqual(first.findings, ())
        self.assertEqual(hashlib.sha256(product.read_bytes()).hexdigest(), before)
        receipt = kernel.status("EXAMPLE_GAME", "RUN_001")
        self.assertEqual(receipt["state"], "SHADOW_COMPLETE")
        digest = receipt["receipt_digest"]
        unsigned = dict(receipt)
        unsigned.pop("receipt_digest")
        expected = hashlib.sha256(
            json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(digest, expected)
        self.assertFalse(kernel.leases("EXAMPLE_GAME"))

    def test_stale_sha_blocks_before_lease_or_product_write(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        request = self._request()
        request["observed_main_sha"] = "b" * 40
        product = root / "scripts/example.gd"
        before = product.read_bytes()

        outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(request)

        self.assertEqual(outcome.state.value, "BLOCKED_STALE_SHA")
        self.assertIn("STALE_MAIN_SHA", {finding.code.value for finding in outcome.findings})
        self.assertEqual(product.read_bytes(), before)

    def test_project_identity_and_both_separator_escape_forms_fail_closed(self) -> None:
        api = self._api()
        for unsafe in ("../OTHER/GDD.md", "..\\OTHER\\GDD.md"):
            with self.subTest(unsafe=unsafe):
                temporary, root, state_root = self._workspace()
                self.addCleanup(temporary.cleanup)
                request = self._request()
                request["references"] = [
                    {"project_id": "OTHER_GAME", "kind": "CANON", "path": unsafe}
                ]
                outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(request)
                codes = {finding.code.value for finding in outcome.findings}
                self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
                self.assertTrue({"CROSS_PROJECT_REFERENCE", "UNSAFE_PROJECT_PATH"}.issubset(codes))

    def test_coverage_rejects_missing_mapping_and_unapproved_output(self) -> None:
        api = self._api()
        cases: list[tuple[str, callable, str]] = [
            (
                "missing",
                lambda request: request.__setitem__("coverage", []),
                "UNMAPPED_REQUIREMENT",
            ),
            (
                "extra",
                lambda request: request["coverage"][0]["outputs"].append("scripts/unapproved.gd"),
                "UNAPPROVED_EXTRA_OUTPUT",
            ),
        ]
        for name, mutate, expected_code in cases:
            with self.subTest(name=name):
                temporary, root, state_root = self._workspace()
                self.addCleanup(temporary.cleanup)
                request = self._request()
                mutate(request)
                outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(request)
                self.assertEqual(outcome.state.value, "BLOCKED_COVERAGE")
                self.assertIn(expected_code, {finding.code.value for finding in outcome.findings})

    def test_visual_gap_and_planning_drift_require_user_decision(self) -> None:
        api = self._api()
        cases = []
        visual = self._request()
        visual["visual_impact"] = "NEW_VISUAL_REQUIRED"
        visual["visual_status"] = "VISUAL_LOCKED"
        visual["visual_drift"] = "UNVERIFIED"
        cases.append((visual, "BLOCKED_VISUAL", "USER_DECISION_REQUIRED"))
        planning = self._request(run_id="RUN_002")
        planning["planning_drift"] = "PLANNING_CONFLICT"
        cases.append((planning, "BLOCKED_DRIFT", "PLANNING_CONFLICT"))
        for request, state, code in cases:
            with self.subTest(code=code):
                temporary, root, state_root = self._workspace()
                self.addCleanup(temporary.cleanup)
                outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(request)
                self.assertEqual(outcome.state.value, state)
                self.assertIn(code, {finding.code.value for finding in outcome.findings})

    def test_lease_conflict_blocks_and_preserves_owner(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z")
        kernel.acquire_test_lease("EXAMPLE_GAME", "OTHER_RUN", "EXAMPLE_DOMAIN")

        outcome = kernel.shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_LEASE_CONFLICT")
        leases = kernel.leases("EXAMPLE_GAME")
        self.assertEqual(leases[0]["run_id"], "OTHER_RUN")

    def test_duplicate_successful_input_is_not_reexecuted(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z")
        self.assertEqual(kernel.shadow(self._request()).state.value, "SHADOW_COMPLETE")

        duplicate = self._request(run_id="RUN_002")
        outcome = kernel.shadow(duplicate)

        self.assertEqual(outcome.state.value, "BLOCKED_DUPLICATE_INPUT")
        self.assertIn("DUPLICATE_INPUT", {finding.code.value for finding in outcome.findings})

    def test_repeated_same_failure_stops_as_no_progress(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z")
        request = self._request()
        request["planning_drift"] = "PLANNING_CONFLICT"
        first = kernel.shadow(request)
        second_request = copy.deepcopy(request)
        second_request["run_id"] = "RUN_002"
        second = kernel.shadow(second_request)
        third_request = copy.deepcopy(request)
        third_request["run_id"] = "RUN_003"
        third = kernel.shadow(third_request)

        self.assertEqual(first.state.value, "BLOCKED_DRIFT")
        self.assertEqual(second.state.value, "BLOCKED_DRIFT")
        self.assertEqual(third.state.value, "BLOCKED_NO_PROGRESS")
        self.assertIn("NO_PROGRESS", {finding.code.value for finding in third.findings})

    def test_receipt_cannot_be_overwritten(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z")
        self.assertEqual(kernel.shadow(self._request()).state.value, "SHADOW_COMPLETE")
        before = kernel.status("EXAMPLE_GAME", "RUN_001")

        outcome = kernel.shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_RECEIPT_EXISTS")
        self.assertEqual(kernel.status("EXAMPLE_GAME", "RUN_001"), before)

    def test_budget_and_illegal_state_transition_fail_closed(self) -> None:
        api = self._api()
        temporary, root, state_root = self._workspace()
        self.addCleanup(temporary.cleanup)
        request = self._request()
        request["budgets"]["max_transitions"] = 3
        outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(request)
        self.assertEqual(outcome.state.value, "BLOCKED_BUDGET")
        machine = api.StateMachine()
        with self.assertRaises(api.IllegalTransition):
            machine.advance(api.RunState.SHADOW_COMPLETE)


if __name__ == "__main__":
    unittest.main()
