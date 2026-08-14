from __future__ import annotations

import ast
import importlib
import importlib.util
import json
import tempfile
import unittest
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "tools/loop_shadow_kernel"


class LoopShadowKernelAdversarialTests(unittest.TestCase):
    def _api(self):
        spec = importlib.util.find_spec("tools.loop_shadow_kernel")
        self.assertIsNotNone(spec, "tools.loop_shadow_kernel production package is missing")
        return importlib.import_module("tools.loop_shadow_kernel")

    def _request(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "contract_role": "LOOP_SHADOW_REQUEST",
            "project_id": "EXAMPLE_GAME",
            "run_id": "RUN_ADV_001",
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
            "coverage": [{
                "requirement_id": "REQ_001",
                "tasks": ["TASK_001"],
                "outputs": ["scripts/example.gd"],
                "tests": ["tests/test_example.py"],
                "evidence": ["E2_TEST"],
            }],
            "allowed_paths": ["scripts/example.gd"],
            "changed_paths": ["scripts/example.gd"],
            "required_evidence": ["E2_TEST"],
            "resource_locks": ["EXAMPLE_DOMAIN"],
            "references": [{"project_id": "EXAMPLE_GAME", "kind": "CANON", "path": "docs/GDD.md"}],
            "budgets": {"max_transitions": 16, "max_repeated_failures": 2},
            "autonomy": "A2_EXECUTE_ISOLATED",
            "a3_auto_merge_allowlist": [],
            "scheduler_runtime_provider": "NOT_CONFIGURED",
        }

    def _root(self):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "scripts").mkdir()
        (root / "docs").mkdir()
        (root / "scripts/example.gd").write_text("extends Node\n", encoding="utf-8")
        (root / "docs/GDD.md").write_text("# Approved canon\n", encoding="utf-8")
        return temporary, root

    def test_unknown_fields_and_duplicate_normalized_paths_are_rejected(self) -> None:
        api = self._api()
        cases = []
        unknown = self._request()
        unknown["model"] = "gpt"
        cases.append((unknown, "UNKNOWN_FIELD"))
        duplicate = self._request()
        duplicate["allowed_paths"] = ["scripts/café.gd", "scripts/cafe\u0301.gd"]
        duplicate["changed_paths"] = ["scripts/café.gd"]
        duplicate["coverage"][0]["outputs"] = ["scripts/café.gd"]
        cases.append((duplicate, "DUPLICATE_NORMALIZED_PATH"))
        for request, expected in cases:
            with self.subTest(expected=expected):
                temporary, root = self._root()
                self.addCleanup(temporary.cleanup)
                outcome = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z").shadow(request)
                self.assertEqual(outcome.state.value, "BLOCKED_INVALID_CONTRACT")
                self.assertIn(expected, {finding.code.value for finding in outcome.findings})

    def test_symlink_reference_escape_is_rejected_when_supported(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        outside = root.parent / f"{root.name}-outside"
        outside.mkdir(exist_ok=True)
        self.addCleanup(lambda: outside.rmdir() if outside.exists() else None)
        link = root / "docs/link"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable")
        request = self._request()
        request["references"] = [{"project_id": "EXAMPLE_GAME", "kind": "CANON", "path": "docs/link/file.md"}]
        outcome = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z").shadow(request)
        self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
        self.assertIn("UNSAFE_SYMLINK", {finding.code.value for finding in outcome.findings})

    def test_kernel_has_no_model_network_subprocess_or_product_writer_import(self) -> None:
        self._api()
        forbidden_roots = {"openai", "requests", "httpx", "socket", "subprocess", "urllib"}
        forbidden_calls = {"eval", "exec", "compile"}
        violations: list[str] = []
        for path in sorted(PACKAGE_ROOT.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in forbidden_roots:
                            violations.append(f"{path.name}:import:{alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.split(".")[0] in forbidden_roots:
                        violations.append(f"{path.name}:from:{node.module}")
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in forbidden_calls:
                        violations.append(f"{path.name}:call:{node.func.id}")
        self.assertEqual(violations, [])

    def test_state_root_must_be_project_bound_and_reserved(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        outside = root.parent / f"{root.name}-state"
        outcome = api.ShadowKernel(root, outside, now="2026-08-14T00:00:00Z").shadow(self._request())
        self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
        self.assertIn("UNSAFE_STATE_ROOT", {finding.code.value for finding in outcome.findings})
        self.assertFalse(outside.exists())

    def test_status_and_leases_reject_path_like_identifiers(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z")
        for method, arguments in (
            (kernel.status, ("../../OTHER", "RUN_ADV_001")),
            (kernel.status, ("EXAMPLE_GAME", "../../RUN")),
            (kernel.leases, ("../../OTHER",)),
        ):
            with self.subTest(method=method.__name__, arguments=arguments):
                with self.assertRaises(ValueError):
                    method(*arguments)

    def test_corrupt_prior_receipt_fails_closed(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z")
        self.assertEqual(kernel.shadow(self._request()).state.value, "SHADOW_COMPLETE")
        receipt_path = root / ".loop-engineering/projects/EXAMPLE_GAME/runs/RUN_ADV_001/receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["state"] = "TAMPERED"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        request = self._request()
        request["run_id"] = "RUN_ADV_002"

        outcome = kernel.shadow(request)

        self.assertEqual(outcome.state.value, "BLOCKED_INVALID_CONTRACT")
        self.assertIn("RECEIPT_CORRUPT", {finding.code.value for finding in outcome.findings})

    def test_internal_state_symlink_is_rejected(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        outside = root.parent / f"{root.name}-state-outside"
        outside.mkdir(exist_ok=True)
        self.addCleanup(lambda: outside.rmdir() if outside.exists() and not any(outside.iterdir()) else None)
        state_root = root / ".loop-engineering"
        state_root.mkdir()
        try:
            (state_root / "projects").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable")

        outcome = api.ShadowKernel(root, state_root, now="2026-08-14T00:00:00Z").shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
        self.assertIn("UNSAFE_STATE_ROOT", {finding.code.value for finding in outcome.findings})
        self.assertFalse(any(outside.iterdir()))

    def test_busy_lease_guard_fails_closed(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        lock = root / ".loop-engineering/projects/EXAMPLE_GAME/leases.lock"
        lock.parent.mkdir(parents=True)
        lock.write_text("OTHER_RUN\n", encoding="utf-8")

        outcome = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z").shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_LEASE_CONFLICT")
        self.assertIn("LEASE_CONFLICT", {finding.code.value for finding in outcome.findings})

    def test_a3_scheduler_and_autonomy_are_fail_closed_constants(self) -> None:
        api = self._api()
        cases = []
        a3 = self._request()
        a3["a3_auto_merge_allowlist"] = ["docs/**"]
        cases.append(a3)
        scheduler = self._request()
        scheduler["scheduler_runtime_provider"] = "CRON"
        cases.append(scheduler)
        autonomy = self._request()
        autonomy["autonomy"] = "A3_AUTO_MERGE"
        cases.append(autonomy)
        for request in cases:
            with self.subTest(request=request):
                temporary, root = self._root()
                self.addCleanup(temporary.cleanup)
                outcome = api.ShadowKernel(root, root / ".loop-engineering", now="2026-08-14T00:00:00Z").shadow(request)
                self.assertEqual(outcome.state.value, "BLOCKED_INVALID_CONTRACT")
                self.assertIn("UNSAFE_AUTONOMY", {finding.code.value for finding in outcome.findings})


if __name__ == "__main__":
    unittest.main()
