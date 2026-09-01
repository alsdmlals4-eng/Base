from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.loop_a2_runtime.network_boundary import (
    DockerNoneDeniedNetworkBoundary,
    LinuxUnshareDeniedNetworkBoundary,
)
from tools.loop_a2_runtime.test_executor import NetworkExecutionPlan


IMAGE_ID = "sha256:" + ("a" * 64)


class _Completed:
    def __init__(self, *, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class BoundaryTestCase(unittest.TestCase):
    def environment(self) -> dict[str, str]:
        return {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONIOENCODING": "utf-8",
            "CI": "1",
        }


class LinuxUnshareDeniedNetworkBoundaryTests(BoundaryTestCase):
    def test_read_only_approved_remains_fail_closed_without_probe(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            plan = boundary.prepare(policy="READ_ONLY_APPROVED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_non_linux_host_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Windows"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_missing_unshare_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.shutil.which", return_value=None), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_relative_path_with_directory_component_is_rejected(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="tools/unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)
        run.assert_not_called()

    def test_failed_namespace_probe_remains_fail_closed(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=1, stderr="Operation not permitted")):
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)

    def test_probe_must_observe_only_loopback(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/unshare"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout='["lo", "eth0"]\n')):
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNone(plan)

    def test_successful_probe_returns_exact_shell_free_plan_and_preserves_environment(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary(unshare_executable="unshare")
        environment = self.environment()
        environment["SAFE_SENTINEL"] = "present"
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary._resolve_executable", return_value="/usr/bin/unshare"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout='["lo"]\n')) as run:
            plan = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest", "tests.test_example"), cwd=Path.cwd(), environment=environment)
        self.assertIsInstance(plan, NetworkExecutionPlan)
        assert plan is not None
        self.assertEqual(plan.argv, ("/usr/bin/unshare", "--user", "--map-root-user", "--net", "--", "python", "-m", "unittest", "tests.test_example"))
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
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary._resolve_executable", return_value="/usr/bin/unshare"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout='["lo"]\n')) as run:
            first = boundary.prepare(policy="DENIED", argv=("python", "-c", "print(1)"), cwd=Path.cwd(), environment=self.environment())
            second = boundary.prepare(policy="DENIED", argv=("python", "-c", "print(2)"), cwd=Path.cwd(), environment=self.environment())
        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        self.assertEqual(run.call_count, 1)

    @unittest.skipUnless(sys.platform.startswith("linux"), "Linux-only real namespace probe")
    def test_real_namespace_probe_when_host_supports_it(self) -> None:
        boundary = LinuxUnshareDeniedNetworkBoundary()
        with tempfile.TemporaryDirectory() as temporary:
            plan = boundary.prepare(policy="DENIED", argv=(sys.executable, "-c", "print('child')"), cwd=Path(temporary), environment=self.environment())
        if plan is None:
            self.skipTest("host does not permit unprivileged user+network namespaces")
        self.assertEqual(plan.boundary_id, "LINUX_UNSHARE_DENIED_V1")


class DockerNoneDeniedNetworkBoundaryTests(BoundaryTestCase):
    def test_requires_immutable_local_image_id(self) -> None:
        with self.assertRaises(ValueError):
            DockerNoneDeniedNetworkBoundary(image_id="python:3.12-slim")
        with self.assertRaises(ValueError):
            DockerNoneDeniedNetworkBoundary(image_id="sha256:abc")

    def test_unsupported_host_and_read_only_approved_remain_fail_closed(self) -> None:
        boundary = DockerNoneDeniedNetworkBoundary(image_id=IMAGE_ID)
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Darwin"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            self.assertIsNone(boundary.prepare(policy="DENIED", argv=("python", "-V"), cwd=Path.cwd(), environment=self.environment()))
        run.assert_not_called()
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            self.assertIsNone(boundary.prepare(policy="READ_ONLY_APPROVED", argv=("python", "-V"), cwd=Path.cwd(), environment=self.environment()))
        run.assert_not_called()

    def test_windows_host_constructs_same_docker_none_boundary_plan(self) -> None:
        boundary = DockerNoneDeniedNetworkBoundary(
            image_id=IMAGE_ID,
            docker_executable=sys.executable,
        )
        environment = self.environment()
        with tempfile.TemporaryDirectory() as temporary:
            cwd = Path(temporary).resolve()
            with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Windows"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout=IMAGE_ID + "\n")) as run:
                plan = boundary.prepare(
                    policy="DENIED",
                    argv=("python", "-c", "print('windows-host')"),
                    cwd=cwd,
                    environment=environment,
                )
        self.assertIsInstance(plan, NetworkExecutionPlan)
        assert plan is not None
        self.assertEqual(plan.boundary_id, "DOCKER_NONE_DENIED_V1")
        args = list(plan.argv)
        self.assertEqual(args[0], str(Path(sys.executable).resolve(strict=True)))
        self.assertIn("--pull", args)
        self.assertEqual(args[args.index("--pull") + 1], "never")
        self.assertIn("--network", args)
        self.assertEqual(args[args.index("--network") + 1], "none")
        self.assertIn("--read-only", args)
        self.assertIn("--cap-drop", args)
        self.assertEqual(args[args.index("--cap-drop") + 1], "ALL")
        self.assertIn("no-new-privileges", args)
        mount = args[args.index("--mount") + 1]
        self.assertIn(f"src={cwd}", mount)
        self.assertIn("dst=/workspace", mount)
        self.assertIn("readonly", mount)
        inspect = run.call_args.args[0]
        self.assertEqual(inspect[:3], [str(Path(sys.executable).resolve(strict=True)), "image", "inspect"])
        self.assertEqual(inspect[-1], IMAGE_ID)

    def test_missing_docker_or_missing_exact_image_fail_closed(self) -> None:
        boundary = DockerNoneDeniedNetworkBoundary(image_id=IMAGE_ID)
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.shutil.which", return_value=None), patch("tools.loop_a2_runtime.network_boundary.subprocess.run") as run:
            self.assertIsNone(boundary.prepare(policy="DENIED", argv=("python", "-V"), cwd=Path.cwd(), environment=self.environment()))
        run.assert_not_called()
        boundary = DockerNoneDeniedNetworkBoundary(image_id=IMAGE_ID)
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.shutil.which", return_value="/usr/bin/docker"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=1, stderr="No such image")):
            self.assertIsNone(boundary.prepare(policy="DENIED", argv=("python", "-V"), cwd=Path.cwd(), environment=self.environment()))

    def test_exact_image_inspection_is_cached_and_plan_uses_none_network(self) -> None:
        boundary = DockerNoneDeniedNetworkBoundary(
            image_id=IMAGE_ID,
            docker_executable=sys.executable,
        )
        environment = self.environment()
        environment["SAFE_SENTINEL"] = "present"
        with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout=IMAGE_ID + "\n")) as run:
            first = boundary.prepare(policy="DENIED", argv=("python", "-m", "unittest"), cwd=Path.cwd(), environment=environment)
            second = boundary.prepare(policy="DENIED", argv=("python", "-V"), cwd=Path.cwd(), environment=environment)
        self.assertEqual(run.call_count, 1)
        self.assertIsInstance(first, NetworkExecutionPlan)
        self.assertIsNotNone(second)
        assert first is not None
        self.assertEqual(first.boundary_id, "DOCKER_NONE_DENIED_V1")
        self.assertEqual(dict(first.environment), environment)
        argv = list(first.argv)
        self.assertEqual(argv[0], str(Path(sys.executable).resolve(strict=True)))
        self.assertIn("--network", argv)
        self.assertEqual(argv[argv.index("--network") + 1], "none")
        self.assertIn("--read-only", argv)
        self.assertIn("--cap-drop", argv)
        self.assertEqual(argv[argv.index("--cap-drop") + 1], "ALL")
        self.assertIn("no-new-privileges", argv)
        self.assertIn(IMAGE_ID, argv)
        self.assertEqual(argv[-3:], ["python", "-m", "unittest"])
        self.assertNotIn("SAFE_SENTINEL", argv)
        self.assertIn("CI", argv)
        self.assertIn("PYTHONIOENCODING", argv)
        self.assertNotIn(environment["PATH"], argv)
        self.assertNotIn("PATH", argv[argv.index("--workdir") + 2 : argv.index(IMAGE_ID)])

    def test_docker_plan_mounts_only_cwd_read_only_and_never_pulls(self) -> None:
        boundary = DockerNoneDeniedNetworkBoundary(
            image_id=IMAGE_ID,
            docker_executable=sys.executable,
        )
        with tempfile.TemporaryDirectory() as temporary:
            cwd = Path(temporary).resolve()
            with patch("tools.loop_a2_runtime.network_boundary.platform.system", return_value="Linux"), patch("tools.loop_a2_runtime.network_boundary.subprocess.run", return_value=_Completed(returncode=0, stdout=IMAGE_ID + "\n")) as run:
                plan = boundary.prepare(policy="DENIED", argv=("python", "-c", "print(1)"), cwd=cwd, environment=self.environment())
        assert plan is not None
        args = list(plan.argv)
        self.assertNotIn("pull", args)
        self.assertIn("--pull", args)
        self.assertEqual(args[args.index("--pull") + 1], "never")
        self.assertIn("--mount", args)
        mount = args[args.index("--mount") + 1]
        self.assertIn(f"src={cwd}", mount)
        self.assertIn("dst=/workspace", mount)
        self.assertIn("readonly", mount)
        self.assertIn("--workdir", args)
        self.assertEqual(args[args.index("--workdir") + 1], "/workspace")
        inspect_call = run.call_args.args[0]
        self.assertEqual(
            inspect_call[:3],
            [str(Path(sys.executable).resolve(strict=True)), "image", "inspect"],
        )
        self.assertEqual(inspect_call[-1], IMAGE_ID)


if __name__ == "__main__":
    unittest.main()
