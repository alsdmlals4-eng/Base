from __future__ import annotations

import importlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


class LoopShadowKernelHardeningTests(unittest.TestCase):
    def _api(self):
        spec = importlib.util.find_spec("tools.loop_shadow_kernel")
        self.assertIsNotNone(spec, "tools.loop_shadow_kernel production package is missing")
        return importlib.import_module("tools.loop_shadow_kernel")

    def _request(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "contract_role": "LOOP_SHADOW_REQUEST",
            "project_id": "EXAMPLE_GAME",
            "run_id": "RUN_HARD_001",
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
            "references": [{
                "project_id": "EXAMPLE_GAME",
                "kind": "CANON",
                "path": "docs/GDD.md",
            }],
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

    def test_missing_authority_reference_blocks(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        request = self._request()
        request["references"][0]["path"] = "docs/MISSING.md"

        outcome = api.ShadowKernel(
            root,
            root / ".loop-engineering",
            now="2026-08-14T00:00:00Z",
        ).shadow(request)

        self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
        self.assertIn("REFERENCE_MISSING", {finding.code.value for finding in outcome.findings})

    def test_nested_state_root_fails_closed_without_uncaught_io(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)

        outcome = api.ShadowKernel(
            root,
            root / ".loop-engineering/runtime",
            now="2026-08-14T00:00:00Z",
        ).shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_PROJECT_ISOLATION")
        self.assertIn("UNSAFE_STATE_ROOT", {finding.code.value for finding in outcome.findings})
        self.assertFalse((root / ".loop-engineering/runtime").exists())

    def test_corrupt_same_run_receipt_is_reported_before_exists(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        kernel = api.ShadowKernel(
            root,
            root / ".loop-engineering",
            now="2026-08-14T00:00:00Z",
        )
        self.assertEqual(kernel.shadow(self._request()).state.value, "SHADOW_COMPLETE")
        receipt_path = (
            root
            / ".loop-engineering/projects/EXAMPLE_GAME/runs/RUN_HARD_001/receipt.json"
        )
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["state"] = "TAMPERED"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        outcome = kernel.shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_INVALID_CONTRACT")
        self.assertIn("RECEIPT_CORRUPT", {finding.code.value for finding in outcome.findings})

    def test_duplicate_normalized_lease_entries_fail_closed(self) -> None:
        api = self._api()
        temporary, root = self._root()
        self.addCleanup(temporary.cleanup)
        ledger = root / ".loop-engineering/projects/EXAMPLE_GAME/leases.json"
        ledger.parent.mkdir(parents=True)
        ledger.write_text(
            json.dumps([
                {"resource": "EXAMPLE_DOMAIN", "run_id": "RUN_HARD_001"},
                {"resource": "example_domain", "run_id": "RUN_HARD_001"},
            ]),
            encoding="utf-8",
        )

        outcome = api.ShadowKernel(
            root,
            root / ".loop-engineering",
            now="2026-08-14T00:00:00Z",
        ).shadow(self._request())

        self.assertEqual(outcome.state.value, "BLOCKED_LEASE_CONFLICT")
        self.assertIn("LEASE_LEDGER_CORRUPT", {finding.code.value for finding in outcome.findings})


if __name__ == "__main__":
    unittest.main()
