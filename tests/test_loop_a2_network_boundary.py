from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.loop_a2_runtime.network_boundary import LinuxUnshareDeniedNetworkBoundary
from tools.loop_a2_runtime.test_executor import NetworkExecutionPlan


class _Completed:
    def __init__(self, *, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class LinuxUnshareDeniedNetworkBoundaryTests(unittest.TestCase):
    def environment(self) -> dict[str, str]:
        return {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONIOENCODING": "utf-8",
            "CI": "1",
        }

    def test_read_only_approved_remains_fail_closed_without_probe(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run"
        ) as run:
            plan = boundary.prepare(
                policy="READ_ONLY_APPROVED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_non_linux_host_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Windows"), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run"
        ) as run:
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_missing_unshare_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.shutil.which", return_value=None
        ), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_relative_path_with_directory_component_is_rejected(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="tools/unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run"
        ) as run:
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_failed_namespace_probe_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"
        ), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run",
            return_value=_Completed(returncode=1, stderr="Operation not permitted"),
        ):
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)

    def test_probe_must_observe_only_loopback(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"
        ), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run",
            return_value=_Completed(returncode=0, stdout='["lo", "eth0"]\n'),
        ):
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNone(plan)

    def test_successful_probe_returns_exact_shell_free_plan_and_preserves_environment(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        environment = self.environment()
        environment["SAFE_SENTINEL"] = "present"
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"
        ), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run",
            return_value=_Completed(returncode=0, stdout='["lo"]\n'),
        ) as run:
            plan = boundary.prepare(
                policy="DENIED",
                argv=("python", "-m", "unittest", "tests.test_example"),
                cwd=Path.cwd(),
                environment=environment,
            )

        self.assertIsInstance(plan, NetworkExecutionPlan)
        assert plan is not None
        self.assertEqual(
            plan.argv,
            (
                "/usr/bin/unshare",
                "--user",
                "--map-root-user",
                "--net",
                "--",
                "python",
                "-m",
                "unittest",
                "tests.test_example",
            ),
        )
        self.assertEqual(dict(plan.environment), environment)
        self.assertEqual(plan.boundary_id, "LINUX_UNSHARE_DENIED_V1")
        probe = run.call_args
        self.assertEqual(probe.kwargs["cwd"], Path.cwd())
        self.assertEqual(probe.kwargs["env"], environment)
        self.assertFalse(probe.kwargs["shell"])
        self.assertLessEqual(probe.kwargs["timeout"], 10)
        self.assertEqual(probe.args[0][0], "/usr/bin/unshare")
        self.assertIn("--net", probe.args[0])
        self.assertEqual(probe.args[0][-3], sys.executable)
        self.assertEqual(probe.args[0][-2], "-c")
        self.assertIn("if_nameindex", probe.args[0][-1])

    def test_successful_probe_is_cached_per_boundary_instance(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch(
            "tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"
        ), patch(
            "tools.loop_a2_runtime.network_boundary.subprocess.run",
            return_value=_Completed(returncode=0, stdout='["lo"]\n'),
        ) as run:
            first = boundary.prepare(
                policy="DENIED",
                argv=("python", "-c", "print(1)"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
            second = boundary.prepare(
                policy="DENIED",
                argv=("python", "-c", "print(2)"),
                cwd=Path.cwd(),
                environment=self.environment(),
            )
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(run.call_count, 1)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-only real namespace probe")
    def test_real_namespace_probe_when_host_supports_it(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary()
        with tempfile.TemporaryDirectory() as temporary:
            plan = boundary.prepare(
                policy="DENIED",
                argv=(sys.executable, "-c", "print('child')"),
                cwd=Path(temporary),
                environment=self.environment(),
            )
        if plan is None:
            self.skipTest("host does not permit unprivileged user+network namespaces")
        self.assertEqual(plan.boundary_id, "LINUX_UNSHARE_DENIED_V1")


if __name__ == "__main__":
    unittest.main()
