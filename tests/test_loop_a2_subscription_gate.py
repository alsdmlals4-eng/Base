from __future__ import annotations

import os
import subprocess
import unittest

from tools.loop_a2_runtime.provider_gate import real_provider_gate, subscription_codex_cli_gate


class _Runner:
    def __init__(
        self,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int = 0,
        error: Exception | None = None,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.error = error
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((tuple(argv), dict(kwargs)))
        if self.error is not None:
            raise self.error
        return subprocess.CompletedProcess(
            argv,
            self.returncode,
            stdout=self.stdout,
            stderr=self.stderr,
        )


class SubscriptionProviderGateTests(unittest.TestCase):
    def test_paid_openai_api_is_forbidden_by_policy_even_when_old_env_is_present(self) -> None:
        old_approval = os.environ.get("LOOP_A2_REAL_PROVIDER_APPROVED")
        old_key = os.environ.get("OPENAI_API_KEY")
        os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = "1"
        os.environ["OPENAI_API_KEY"] = "sk-should-not-authorize"
        try:
            result = real_provider_gate()
        finally:
            if old_approval is None:
                os.environ.pop("LOOP_A2_REAL_PROVIDER_APPROVED", None)
            else:
                os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = old_approval
            if old_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = old_key

        self.assertEqual(result["status"], "NOT_PLANNED")
        self.assertEqual(result["code"], "PAID_OPENAI_API_FORBIDDEN")
        self.assertNotIn("sk-should-not-authorize", str(result))

    def test_chatgpt_authenticated_codex_cli_is_ready(self) -> None:
        runner = _Runner(stdout="Logged in using ChatGPT\n")

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_READY")
        self.assertEqual(runner.calls[0][0], ("codex", "login", "status"))
        self.assertFalse(runner.calls[0][1].get("shell", False))

    def test_official_stderr_chatgpt_status_is_ready(self) -> None:
        runner = _Runner(stderr="Logged in using ChatGPT\n")

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_READY")

    def test_dual_stream_chatgpt_status_fails_closed(self) -> None:
        runner = _Runner(
            stdout="Logged in using ChatGPT\n",
            stderr="Logged in using ChatGPT\n",
        )

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "BLOCKED_UNVERIFIED")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_REQUIRED")

    def test_extra_stderr_diagnostics_fail_closed(self) -> None:
        runner = _Runner(stderr="warning\nLogged in using ChatGPT\n")

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "BLOCKED_UNVERIFIED")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_REQUIRED")

    def test_api_key_authenticated_codex_cli_is_rejected(self) -> None:
        runner = _Runner(stderr="Logged in using an API key - sk-redacted\n")

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "BLOCKED_UNVERIFIED")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_REQUIRED")
        self.assertNotIn("sk-redacted", str(result))

    def test_missing_codex_cli_fails_closed(self) -> None:
        runner = _Runner(error=FileNotFoundError("codex"))

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "BLOCKED_UNVERIFIED")
        self.assertEqual(result["code"], "CODEX_CLI_UNAVAILABLE")

    def test_login_status_failure_fails_closed_without_leaking_stderr(self) -> None:
        runner = _Runner(stderr="OPENAI_API_KEY=secret", returncode=1)

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "BLOCKED_UNVERIFIED")
        self.assertEqual(result["code"], "CODEX_LOGIN_STATUS_FAILED")
        self.assertNotIn("OPENAI_API_KEY", str(result))
        self.assertNotIn("secret", str(result))


if __name__ == "__main__":
    unittest.main()
