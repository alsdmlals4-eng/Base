from __future__ import annotations

import inspect
import json
import os
from pathlib import Path
import subprocess
import unittest


class _ExecRunner:
    def __init__(self, *, payload: dict[str, object] | None = None, returncode: int = 0, write_output: bool = True) -> None:
        self.payload = payload or {
            "status": "COMPLETED",
            "summary": "bounded",
            "writes": [],
            "blocked_reason": "",
        }
        self.returncode = returncode
        self.write_output = write_output
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        argv = tuple(str(item) for item in argv)
        self.calls.append((argv, dict(kwargs)))
        schema_path = Path(argv[argv.index("--output-schema") + 1])
        output_path = Path(argv[argv.index("--output-last-message") + 1])
        if not schema_path.is_file():
            raise AssertionError("schema file must exist before codex exec")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if schema.get("type") != "object":
            raise AssertionError("structured output schema must be an object")
        if self.write_output:
            output_path.write_text(json.dumps(self.payload), encoding="utf-8")
        return subprocess.CompletedProcess(argv, self.returncode, stdout="", stderr="")


class _RawOutputRunner(_ExecRunner):
    def __init__(self, raw_output: str) -> None:
        super().__init__()
        self.raw_output = raw_output

    def __call__(self, argv, **kwargs):
        argv = tuple(str(item) for item in argv)
        self.calls.append((argv, dict(kwargs)))
        schema_path = Path(argv[argv.index("--output-schema") + 1])
        output_path = Path(argv[argv.index("--output-last-message") + 1])
        if not schema_path.is_file():
            raise AssertionError("schema file must exist before codex exec")
        output_path.write_text(self.raw_output, encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")


class CodexCliTransportTests(unittest.TestCase):
    def test_process_is_ephemeral_read_only_config_isolated_shell_and_web_disabled_and_shell_free(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess

        runner = _ExecRunner()
        previous = {key: os.environ.get(key) for key in ("OPENAI_API_KEY", "GITHUB_TOKEN", "CODEX_HOME")}
        os.environ["OPENAI_API_KEY"] = "sk-must-not-enter-child"
        os.environ["GITHUB_TOKEN"] = "gh-must-not-enter-child"
        os.environ["CODEX_HOME"] = "/tmp/test-codex-home"
        try:
            result = CodexCliProcess(run_command=runner).invoke(
                instructions="Return bounded JSON only.",
                input_text='{"approved":true}',
                schema={"type": "object", "properties": {}, "additionalProperties": True},
                timeout_seconds=30,
                model=None,
            )
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

        self.assertEqual(json.loads(result)["status"], "COMPLETED")
        argv, kwargs = runner.calls[0]
        self.assertEqual(argv[0], "codex")
        exec_index = argv.index("exec")
        self.assertGreater(exec_index, 0)
        self.assertIn("--strict-config", argv[:exec_index])
        config_pairs = [
            argv[index + 1]
            for index, item in enumerate(argv[:exec_index])
            if item == "-c"
        ]
        self.assertIn("features.shell_tool=false", config_pairs)
        self.assertIn("features.web_search_request=false", config_pairs)
        self.assertIn("features.web_search_cached=false", config_pairs)
        self.assertIn("features.standalone_web_search=false", config_pairs)
        for required in ("--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check"):
            self.assertIn(required, argv[exec_index + 1 :])
        sandbox_index = argv.index("--sandbox")
        self.assertEqual(argv[sandbox_index + 1], "read-only")
        self.assertEqual(argv[-1], "-")
        self.assertFalse(kwargs.get("shell", False))
        self.assertNotIn("OPENAI_API_KEY", kwargs["env"])
        self.assertNotIn("GITHUB_TOKEN", kwargs["env"])
        self.assertEqual(kwargs["env"].get("CODEX_HOME"), "/tmp/test-codex-home")
        self.assertNotIn("sk-must-not-enter-child", str(kwargs))
        self.assertNotIn("gh-must-not-enter-child", str(kwargs))
        self.assertIn("Return bounded JSON only.", kwargs["input"])
        self.assertIn('{"approved":true}', kwargs["input"])

    def test_explicit_model_is_forwarded_without_changing_auth_mode(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess

        runner = _ExecRunner()
        CodexCliProcess(run_command=runner).invoke(
            instructions="i",
            input_text="{}",
            schema={"type": "object"},
            timeout_seconds=30,
            model="gpt-5-codex",
        )
        argv = runner.calls[0][0]
        model_index = argv.index("--model")
        self.assertEqual(argv[model_index + 1], "gpt-5-codex")
        self.assertNotIn("--api-key", argv)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)

    def test_nonzero_missing_output_timeout_and_oversize_fail_closed(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess, CodexCliTransportError

        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_EXEC_NONZERO"):
            CodexCliProcess(run_command=_ExecRunner(returncode=7)).invoke(
                instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=30
            )
        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_OUTPUT_MISSING"):
            CodexCliProcess(run_command=_ExecRunner(write_output=False)).invoke(
                instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=30
            )

        def timeout_runner(argv, **kwargs):
            raise subprocess.TimeoutExpired(argv, kwargs.get("timeout", 1))

        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_EXEC_TIMEOUT"):
            CodexCliProcess(run_command=timeout_runner).invoke(
                instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=1
            )

        huge = {"value": "x" * 4096}
        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_OUTPUT_LIMIT"):
            CodexCliProcess(run_command=_ExecRunner(payload=huge), max_output_bytes=128).invoke(
                instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=30
            )

    def test_malformed_json_and_secret_echo_fail_closed(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess, CodexCliTransportError

        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_OUTPUT_INVALID"):
            CodexCliProcess(run_command=_RawOutputRunner("not-json")).invoke(
                instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=30
            )

        previous = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "sk-output-sentinel"
        try:
            with self.assertRaisesRegex(CodexCliTransportError, "CODEX_OUTPUT_SECRET_ECHO"):
                CodexCliProcess(run_command=_RawOutputRunner(json.dumps({"value": "sk-output-sentinel"}))).invoke(
                    instructions="i", input_text="{}", schema={"type": "object"}, timeout_seconds=30
                )
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous

    def test_responses_client_adapts_existing_structured_contract_without_sdk_or_paid_key(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess, CodexCliResponsesClient

        runner = _ExecRunner(payload={"verdict": "PASS", "findings": [], "checked_requirement_ids": ["REQ_1"]})
        client = CodexCliResponsesClient(process=CodexCliProcess(run_command=runner))
        response = client.responses.create(
            model="CODEX_PLAN_DEFAULT",
            instructions="critic",
            input='{"requirement_ids":["REQ_1"]}',
            text={"format": {"type": "json_schema", "name": "review", "strict": True, "schema": {"type": "object"}}},
            store=False,
            max_output_tokens=512,
            timeout=30,
        )

        self.assertEqual(json.loads(response.output_text)["verdict"], "PASS")
        self.assertIsNone(response.usage)
        self.assertNotIn("--model", runner.calls[0][0])

    def test_responses_client_rejects_non_structured_or_persistent_requests(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess, CodexCliResponsesClient, CodexCliTransportError

        client = CodexCliResponsesClient(process=CodexCliProcess(run_command=_ExecRunner()))
        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_REQUEST_POLICY_INVALID"):
            client.responses.create(
                model="CODEX_PLAN_DEFAULT",
                instructions="x",
                input="{}",
                text={},
                store=False,
                max_output_tokens=10,
                timeout=30,
            )
        with self.assertRaisesRegex(CodexCliTransportError, "CODEX_REQUEST_POLICY_INVALID"):
            client.responses.create(
                model="CODEX_PLAN_DEFAULT",
                instructions="x",
                input="{}",
                text={"format": {"schema": {"type": "object"}}},
                store=True,
                max_output_tokens=10,
                timeout=30,
            )

    def test_subscription_factory_requires_immutable_authority_snapshot(self) -> None:
        from tools.loop_a2_runtime.codex_cli_transport import build_subscription_provider_components

        parameter = inspect.signature(build_subscription_provider_components).parameters.get(
            "authority_snapshot"
        )
        self.assertIsNotNone(parameter)
        self.assertIs(parameter.default, inspect.Parameter.empty)


if __name__ == "__main__":
    unittest.main()
