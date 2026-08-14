from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

from tools.loop_a2_runtime.test_executor import ProjectTestExecutor


def _require_boundary():
    spec = importlib.util.find_spec("tools.loop_a2_runtime.python_denied_network")
    if spec is None:
        raise AssertionError("Python DENIED network boundary is not implemented")
    from tools.loop_a2_runtime.python_denied_network import PythonUnittestDenyNetworkBoundary

    return PythonUnittestDenyNetworkBoundary


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=True
    )
    return completed.stdout.strip()


class PythonDeniedNetworkBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        _git(self.repo, "init", "-b", "main")
        _git(self.repo, "config", "user.name", "Loop Test")
        _git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "tests").mkdir()
        (self.repo / "tests/__init__.py").write_text("", encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "baseline")
        self.sha = _git(self.repo, "rev-parse", "HEAD")
        self.adapter = self.repo / "RUNTIME_ADAPTER.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _write_probe(self, body: str) -> None:
        path = self.repo / "tests/test_boundary_probe.py"
        path.write_text(textwrap.dedent(body), encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "probe")
        self.sha = _git(self.repo, "rev-parse", "HEAD")

    def _write_adapter(
        self,
        argv: list[str],
        *,
        network: str = "DENIED",
    ) -> None:
        value = {
            "schema_version": 1,
            "contract_role": "LOOP_RUNTIME_ADAPTER",
            "project_id": "TEST_GAME",
            "status": "PROJECT_ADAPTER_VALIDATED",
            "engine": {"name": "Fixture", "version": "1"},
            "languages": ["Python"],
            "source_roots": ["tests/"],
            "test_commands": [
                {
                    "command_id": "BOUNDARY_PROBE",
                    "argv": argv,
                    "working_directory": ".",
                    "timeout_seconds": 20,
                    "network": network,
                }
            ],
            "runtime_commands": [],
            "build_commands": [],
            "protected_paths": ["tests/"],
            "semantic_resource_domains": ["TEST_DOMAIN"],
            "rollback_strategy": "Discard verification worktree.",
        }
        self.adapter.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def _run(self, argv: list[str], *, network: str = "DENIED"):
        Boundary = _require_boundary()
        self._write_adapter(argv, network=network)
        executor = ProjectTestExecutor(network_boundary=Boundary())
        return executor.run_all(
            adapter_path=self.adapter,
            worktree_path=self.repo,
            expected_project_id="TEST_GAME",
            expected_main_sha=self.sha,
        )

    def test_module_and_boundary_identity_exist(self) -> None:
        Boundary = _require_boundary()
        boundary = Boundary()
        self.assertEqual(boundary.boundary_id, "PYTHON_AUDIT_DENY_NETWORK_V1")

    def test_normal_python_unittest_passes(self) -> None:
        self._write_probe(
            """
            import unittest

            class Probe(unittest.TestCase):
                def test_ok(self):
                    self.assertEqual(2 + 2, 4)
            """
        )
        result = self._run(["python", "-m", "unittest", "tests.test_boundary_probe", "-v"])
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.commands[0].network_boundary_id, "PYTHON_AUDIT_DENY_NETWORK_V1")

    def test_socket_creation_is_denied_inside_test_runtime(self) -> None:
        self._write_probe(
            """
            import socket
            import unittest

            class Probe(unittest.TestCase):
                def test_socket_denied(self):
                    with self.assertRaises(PermissionError):
                        socket.socket()
            """
        )
        result = self._run(["python", "-m", "unittest", "tests.test_boundary_probe", "-v"])
        self.assertEqual(result.status, "PASS")

    def test_subprocess_and_os_system_are_denied(self) -> None:
        self._write_probe(
            """
            import os
            import subprocess
            import sys
            import unittest

            class Probe(unittest.TestCase):
                def test_subprocess_denied(self):
                    with self.assertRaises(PermissionError):
                        subprocess.run([sys.executable, '-c', 'pass'], check=False)

                def test_os_system_denied(self):
                    with self.assertRaises(PermissionError):
                        os.system('echo forbidden')
            """
        )
        result = self._run(["python", "-m", "unittest", "tests.test_boundary_probe", "-v"])
        self.assertEqual(result.status, "PASS")

    def test_ctypes_dynamic_loading_escape_is_denied(self) -> None:
        self._write_probe(
            """
            import ctypes
            import unittest

            class Probe(unittest.TestCase):
                def test_ctypes_denied(self):
                    with self.assertRaises(PermissionError):
                        ctypes.CDLL(None)
            """
        )
        result = self._run(["python", "-m", "unittest", "tests.test_boundary_probe", "-v"])
        self.assertEqual(result.status, "PASS")

    def test_openai_key_is_not_inherited(self) -> None:
        self._write_probe(
            """
            import os
            import unittest

            class Probe(unittest.TestCase):
                def test_secret_absent(self):
                    self.assertIsNone(os.environ.get('OPENAI_API_KEY'))
            """
        )
        previous = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "sk-test-must-not-cross-boundary"
        try:
            result = self._run(["python", "-m", "unittest", "tests.test_boundary_probe", "-v"])
            self.assertEqual(result.status, "PASS")
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous

    def test_unsupported_python_c_is_still_fail_closed(self) -> None:
        result = self._run(["python", "-c", "print('must not run')"])
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "NETWORK_POLICY_UNENFORCED")

    def test_non_unittest_module_is_still_fail_closed(self) -> None:
        result = self._run(["python", "-m", "http.server"])
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "NETWORK_POLICY_UNENFORCED")

    def test_read_only_approved_is_not_promoted_to_denied_boundary(self) -> None:
        result = self._run(
            ["python", "-m", "unittest", "tests.test_boundary_probe"],
            network="READ_ONLY_APPROVED",
        )
        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.commands[0].error_code, "NETWORK_POLICY_UNENFORCED")


if __name__ == "__main__":
    unittest.main()
