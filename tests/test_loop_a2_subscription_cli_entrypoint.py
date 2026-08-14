from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest
from unittest.mock import ANY, MagicMock, patch

import tools.loop_a2 as cli
from tools.loop_a2_runtime.authority_snapshot import AuthoritySnapshotError
from tools.loop_a2_runtime.codex_cli_transport import CodexCliTransportError
from tools.loop_a2_runtime.network_boundary import DockerNoneDeniedNetworkBoundary
from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.test_executor import ProjectTestExecutor
from tests.test_loop_a2_protocol import valid_request


IMAGE_ID = "sha256:" + "e" * 64


def _real_request() -> RunRequest:
    value = valid_request()
    value["provider_mode"] = "REAL"
    return RunRequest.from_dict(value)


class SubscriptionCliEntrypointTests(unittest.TestCase):
    def _argv(
        self,
        project_root: Path,
        runtime_root: Path | None,
        *,
        image_id: str | None = IMAGE_ID,
    ) -> list[str]:
        argv = [
            "loop_a2.py",
            "run",
            "--project-root",
            str(project_root),
            "--capsule",
            "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
            "--run-id",
            "RUN_REAL_001",
            "--observed-main-sha",
            _real_request().expected_main_sha,
            "--provider",
            "real",
        ]
        if runtime_root is not None:
            argv.extend(["--runtime-root", str(runtime_root)])
        if image_id is not None:
            argv.extend(["--denied-network-docker-image-id", image_id])
        return argv

    def test_factory_owns_chatgpt_auth_failure_after_authority_and_boundary_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            request = _real_request()
            snapshot = object()
            output = io.StringIO()
            with (
                patch.object(cli, "build_request_from_capsule", return_value=request),
                patch.object(cli, "capture_authority_snapshot", return_value=snapshot) as capture,
                patch.object(
                    cli,
                    "build_subscription_provider_components",
                    side_effect=CodexCliTransportError(
                        "CODEX_CHATGPT_AUTH_REQUIRED",
                        "ChatGPT login required",
                    ),
                ) as factory,
                patch.object(sys, "argv", self._argv(project_root, runtime_root)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 2)
            self.assertEqual(json.loads(output.getvalue())["code"], "CODEX_CHATGPT_AUTH_REQUIRED")
            capture.assert_called_once_with(
                project_root=project_root,
                capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                request=request,
            )
            factory.assert_called_once()

    def test_real_provider_constructs_subscription_components_and_real_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            request = _real_request()
            snapshot = object()
            verifier = object()
            components = SimpleNamespace(
                builder=object(),
                critic=object(),
                candidate_verifier=verifier,
            )
            outcome = SimpleNamespace(
                state="WAITING_INTEGRATION",
                evidence={"state": "WAITING_INTEGRATION", "provider_mode": "REAL"},
            )
            runtime = MagicMock()
            runtime.run.return_value = outcome
            output = io.StringIO()

            with (
                patch.object(cli, "build_request_from_capsule", return_value=request) as bridge,
                patch.object(cli, "capture_authority_snapshot", return_value=snapshot) as capture,
                patch.object(cli, "build_subscription_provider_components", return_value=components) as factory,
                patch.object(cli, "A2Runtime", return_value=runtime) as runtime_class,
                patch.object(sys, "argv", self._argv(project_root, runtime_root)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 0)
            bridge.assert_called_once()
            self.assertEqual(bridge.call_args.kwargs["provider_mode"], "REAL")
            capture.assert_called_once_with(
                project_root=project_root,
                capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                request=request,
            )
            factory.assert_called_once_with(
                repo_root=project_root,
                runtime_root=runtime_root,
                authority_snapshot=snapshot,
                run_request=request,
                project_test_executor=ANY,
            )
            executor = factory.call_args.kwargs["project_test_executor"]
            self.assertIsInstance(executor, ProjectTestExecutor)
            self.assertIsInstance(executor.network_boundary, DockerNoneDeniedNetworkBoundary)
            runtime_class.assert_called_once_with(
                builder=components.builder,
                critic=components.critic,
                candidate_verifier=verifier,
                provider_mode="REAL",
            )
            runtime.run.assert_called_once()
            self.assertEqual(json.loads(output.getvalue())["provider_mode"], "REAL")

    def test_real_provider_requires_explicit_runtime_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            project_root.mkdir()
            output = io.StringIO()
            with (
                patch.object(cli, "build_request_from_capsule", return_value=_real_request()),
                patch.object(sys, "argv", self._argv(project_root, None)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 2)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertEqual(payload["code"], "REAL_RUNTIME_ROOT_REQUIRED")

    def test_real_provider_requires_explicit_denied_network_image_before_authority_or_factory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            output = io.StringIO()
            with (
                patch.object(cli, "build_request_from_capsule", return_value=_real_request()),
                patch.object(cli, "capture_authority_snapshot") as capture,
                patch.object(cli, "build_subscription_provider_components") as factory,
                patch.object(
                    sys,
                    "argv",
                    self._argv(project_root, runtime_root, image_id=None),
                ),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 2)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["status"], "BLOCKED_UNVERIFIED")
            self.assertEqual(payload["code"], "REAL_PROJECT_TEST_BOUNDARY_REQUIRED")
            capture.assert_not_called()
            factory.assert_not_called()

    def test_authority_snapshot_failure_blocks_before_factory_auth_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            output = io.StringIO()
            with (
                patch.object(cli, "build_request_from_capsule", return_value=_real_request()),
                patch.object(
                    cli,
                    "capture_authority_snapshot",
                    side_effect=AuthoritySnapshotError("stale authority"),
                ),
                patch.object(cli, "build_subscription_provider_components") as factory,
                patch.object(sys, "argv", self._argv(project_root, runtime_root)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 2)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertEqual(payload["code"], "AUTHORITY_SNAPSHOT_INVALID")
            factory.assert_not_called()


if __name__ == "__main__":
    unittest.main()
