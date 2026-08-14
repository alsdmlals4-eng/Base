from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import tools.loop_a2 as cli
from tools.loop_a2_runtime.protocol import RunRequest
from tests.test_loop_a2_protocol import valid_request


def _real_request() -> RunRequest:
    value = valid_request()
    value["provider_mode"] = "REAL"
    return RunRequest.from_dict(value)


class SubscriptionCliEntrypointTests(unittest.TestCase):
    def _argv(self, project_root: Path, runtime_root: Path | None) -> list[str]:
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
        return argv

    def test_real_provider_fails_closed_before_factory_when_chatgpt_auth_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            output = io.StringIO()
            with (
                patch.object(cli, "build_request_from_capsule", return_value=_real_request()),
                patch.object(
                    cli,
                    "subscription_codex_cli_gate",
                    return_value={
                        "status": "BLOCKED_UNVERIFIED",
                        "code": "CODEX_CHATGPT_AUTH_REQUIRED",
                        "message": "ChatGPT login required",
                    },
                ),
                patch.object(cli, "build_subscription_provider_components") as factory,
                patch.object(sys, "argv", self._argv(project_root, runtime_root)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 2)
            self.assertEqual(json.loads(output.getvalue())["code"], "CODEX_CHATGPT_AUTH_REQUIRED")
            factory.assert_not_called()

    def test_real_provider_constructs_subscription_components_and_real_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project_root = Path(temp) / "project"
            runtime_root = Path(temp) / "runtime"
            project_root.mkdir()
            components = SimpleNamespace(builder=object(), critic=object())
            outcome = SimpleNamespace(
                state="WAITING_INTEGRATION",
                evidence={"state": "WAITING_INTEGRATION", "provider_mode": "REAL"},
            )
            runtime = MagicMock()
            runtime.run.return_value = outcome
            output = io.StringIO()

            with (
                patch.object(cli, "build_request_from_capsule", return_value=_real_request()) as bridge,
                patch.object(
                    cli,
                    "subscription_codex_cli_gate",
                    return_value={"status": "READY", "code": "CODEX_CHATGPT_AUTH_READY"},
                ),
                patch.object(cli, "build_subscription_provider_components", return_value=components) as factory,
                patch.object(cli, "A2Runtime", return_value=runtime) as runtime_class,
                patch.object(sys, "argv", self._argv(project_root, runtime_root)),
                redirect_stdout(output),
            ):
                result = cli.main()

            self.assertEqual(result, 0)
            bridge.assert_called_once()
            self.assertEqual(bridge.call_args.kwargs["provider_mode"], "REAL")
            factory.assert_called_once_with(repo_root=project_root, runtime_root=runtime_root)
            runtime_class.assert_called_once_with(
                builder=components.builder,
                critic=components.critic,
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


if __name__ == "__main__":
    unittest.main()
