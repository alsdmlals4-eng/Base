from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/loopctl.py"


class LoopShadowKernelCliTests(unittest.TestCase):
    def _request(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "contract_role": "LOOP_SHADOW_REQUEST",
            "project_id": "EXAMPLE_GAME",
            "run_id": "RUN_CLI_001",
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

    def _run(self, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        self.assertTrue(CLI.is_file(), "tools/loopctl.py is missing")
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validate_shadow_status_and_leases_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "docs").mkdir()
            product = root / "scripts/example.gd"
            product.write_text("extends Node\n", encoding="utf-8")
            (root / "docs/GDD.md").write_text("# Approved canon\n", encoding="utf-8")
            request_path = root / "request.json"
            request_path.write_text(json.dumps(self._request()), encoding="utf-8")
            state_root = root / ".loop-engineering"
            before = hashlib.sha256(product.read_bytes()).hexdigest()

            validated = self._run(
                "validate", str(request_path), "--project-root", str(root), "--state-root", str(state_root), cwd=ROOT
            )
            self.assertEqual(validated.returncode, 0, validated.stderr)
            self.assertEqual(json.loads(validated.stdout)["status"], "PASS")
            self.assertFalse(state_root.exists(), "validate must not write state")

            shadowed = self._run(
                "shadow", str(request_path), "--project-root", str(root), "--state-root", str(state_root),
                "--now", "2026-08-14T00:00:00Z", cwd=ROOT
            )
            self.assertEqual(shadowed.returncode, 0, shadowed.stderr)
            self.assertEqual(json.loads(shadowed.stdout)["state"], "SHADOW_COMPLETE")
            self.assertEqual(hashlib.sha256(product.read_bytes()).hexdigest(), before)

            status = self._run(
                "status", "--project-id", "EXAMPLE_GAME", "--run-id", "RUN_CLI_001",
                "--project-root", str(root), "--state-root", str(state_root), cwd=ROOT
            )
            self.assertEqual(status.returncode, 0, status.stderr)
            self.assertEqual(json.loads(status.stdout)["state"], "SHADOW_COMPLETE")

            leases = self._run(
                "leases", "--project-id", "EXAMPLE_GAME", "--project-root", str(root),
                "--state-root", str(state_root), cwd=ROOT
            )
            self.assertEqual(leases.returncode, 0, leases.stderr)
            self.assertEqual(json.loads(leases.stdout), [])

    def test_cli_returns_stable_blocked_exit_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "docs").mkdir()
            (root / "scripts/example.gd").write_text("extends Node\n", encoding="utf-8")
            (root / "docs/GDD.md").write_text("# Approved canon\n", encoding="utf-8")
            request = self._request()
            request["observed_main_sha"] = "b" * 40
            request_path = root / "request.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")

            result = self._run(
                "shadow", str(request_path), "--project-root", str(root),
                "--state-root", str(root / ".loop-engineering"),
                "--now", "2026-08-14T00:00:00Z", cwd=ROOT
            )
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(payload["state"], "BLOCKED_STALE_SHA")
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
