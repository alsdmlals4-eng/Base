from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "tools" / "loop-a2-local-executor" / "src"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.control_plane import GhControlPlane, sanitize_public_receipt
from loop_a2_local_executor.job import LocalA2Job
from loop_a2_local_executor.runtime import LocalA2Runtime, LocalRuntimeError
from loop_a2_local_executor.service import LocalExecutorService
from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess
from tools.loop_a2_runtime.provider_gate import subscription_codex_cli_gate


AUTHOR = "alsdmlals4-eng"
LABEL = "loop-a2-local-job"


class RecordingRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((tuple(str(item) for item in argv), dict(kwargs)))
        return self.responses.pop(0)


class CodexExecRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        argv = tuple(str(item) for item in argv)
        self.calls.append((argv, dict(kwargs)))
        output_path = Path(argv[argv.index("--output-last-message") + 1])
        output_path.write_text(json.dumps({"status": "COMPLETED"}), encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")


class FakeStore:
    def __init__(self, base: Path, project: Path, runtime_root: Path) -> None:
        self.base = base
        self.project = project
        self.runtime_root = runtime_root

    @contextmanager
    def exact_worktree(self, repository: str, sha: str, role: str):
        del repository, sha
        yield self.base if role == "base" else self.project


class FakePlane:
    def __init__(self, issues: list[dict[str, object]]) -> None:
        self.issues = issues
        self.published: list[tuple[int, dict[str, object], bool]] = []

    def list_open_jobs(self):
        return tuple(self.issues)

    def publish_terminal(self, number, receipt, *, close):
        self.published.append((number, dict(receipt), close))


class FailingRuntime:
    def __init__(self, error: LocalRuntimeError) -> None:
        self.error = error

    def execute(self, job: LocalA2Job):
        del job
        raise self.error


def local_job() -> LocalA2Job:
    return LocalA2Job(
        issue_number=443,
        target_repository="alsdmlals4-eng/Blacksmith",
        base_runtime_sha="a" * 40,
        authority_sha="b" * 40,
        capsule="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        run_id="BS_A2_BURNIN_001",
        provider="real",
    )


def valid_issue() -> dict[str, object]:
    body = {
        "schema_version": 1,
        "contract_role": "LOOP_A2_LOCAL_JOB",
        "target_repository": "alsdmlals4-eng/Blacksmith",
        "base_runtime_sha": "a" * 40,
        "authority_sha": "b" * 40,
        "capsule": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        "run_id": "BS_A2_BURNIN_001",
        "provider": "real",
    }
    return {
        "number": 443,
        "author": {"login": AUTHOR},
        "labels": [{"name": LABEL}],
        "body": "```json\n" + json.dumps(body) + "\n```",
    }


class WindowsUtf8BlockedReceiptDiagnosticsTests(unittest.TestCase):
    def test_control_plane_subprocess_capture_is_explicit_utf8_replace(self) -> None:
        runner = RecordingRunner([
            subprocess.CompletedProcess([], 0, stdout="[]", stderr=""),
        ])
        plane = GhControlPlane(
            control_repository="alsdmlals4-eng/Base",
            required_label=LABEL,
            gh_executable="/trusted/gh",
            runner=runner,
        )

        plane.list_open_jobs()

        kwargs = runner.calls[0][1]
        self.assertIs(kwargs["text"], True)
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertIs(kwargs["shell"], False)

    def test_subscription_login_subprocess_capture_is_explicit_utf8_replace(self) -> None:
        runner = RecordingRunner([
            subprocess.CompletedProcess([], 0, stdout="Logged in using ChatGPT\n", stderr=""),
        ])

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "READY")
        kwargs = runner.calls[0][1]
        self.assertIs(kwargs["text"], True)
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertIs(kwargs["shell"], False)

    def test_codex_exec_subprocess_capture_is_explicit_utf8_replace(self) -> None:
        runner = CodexExecRunner()

        CodexCliProcess(run_command=runner).invoke(
            instructions="Return bounded JSON only.",
            input_text="{}",
            schema={"type": "object"},
            timeout_seconds=30,
        )

        kwargs = runner.calls[0][1]
        self.assertIs(kwargs["text"], True)
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertIs(kwargs["shell"], False)

    def _runtime_fixture(self, child_stdout: str, *, child_returncode: int = 1):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        base = root / "base"
        project = root / "project"
        runtime_root = root / "runtime"
        (base / "tools").mkdir(parents=True)
        (base / "tools" / "loop_a2.py").write_text("# fixture\n", encoding="utf-8")
        capsule = project / local_job().capsule
        capsule.parent.mkdir(parents=True)
        capsule.write_text(
            json.dumps({"project_id": "BLACKSMITH", "source_main_sha": "c" * 40}),
            encoding="utf-8",
        )
        image_id = "sha256:" + "e" * 64
        runner = RecordingRunner([
            subprocess.CompletedProcess([], 0, stdout=image_id + "\n", stderr=""),
            subprocess.CompletedProcess([], child_returncode, stdout=child_stdout, stderr="private child stderr"),
        ])
        runtime = LocalA2Runtime(
            store=FakeStore(base, project, runtime_root),
            runner=runner,
            python_executable="/trusted/python",
            docker_executable="/trusted/docker",
        )
        return temp, runtime

    def test_nonzero_same_run_a2_receipt_preserves_only_safe_diagnostics(self) -> None:
        blocked = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_RECEIPT",
            "project_id": "BLACKSMITH",
            "run_id": "BS_A2_BURNIN_001",
            "package_id": "BS_TEST_ONLY",
            "expected_main_sha": "c" * 40,
            "state": "PROVIDER_FAILURE",
            "finding_codes": ["BUILDER_PROVIDER_EXCEPTION", "SECOND_PRIVATE_FINDING"],
            "changed_paths": ["private/local/path.txt"],
            "provider_mode": "REAL",
            "integration_eligible": False,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
            "provider_error_type": "CodexCliTransportError",
            "receipt_digest": "d" * 64,
            "message": "private provider detail",
        }
        temp, runtime = self._runtime_fixture(json.dumps(blocked))
        try:
            with self.assertRaises(LocalRuntimeError) as caught:
                runtime.execute(local_job())
        finally:
            temp.cleanup()

        self.assertEqual(caught.exception.code, "A2_EXECUTION_BLOCKED")
        self.assertEqual(
            getattr(caught.exception, "public_details", {}),
            {
                "a2_state": "PROVIDER_FAILURE",
                "a2_finding_code": "BUILDER_PROVIDER_EXCEPTION",
                "a2_provider_error_type": "CodexCliTransportError",
                "a2_receipt_digest": "d" * 64,
            },
        )
        rendered = json.dumps(getattr(caught.exception, "public_details", {}), sort_keys=True)
        self.assertNotIn("private/local", rendered)
        self.assertNotIn("private provider detail", rendered)
        self.assertNotIn("SECOND_PRIVATE_FINDING", rendered)

    def test_nonzero_invalid_or_mismatched_output_remains_generic(self) -> None:
        mismatched = {
            "contract_role": "LOOP_A2_RUN_RECEIPT",
            "project_id": "BLACKSMITH",
            "run_id": "OTHER_RUN",
            "package_id": "BS_TEST_ONLY",
            "expected_main_sha": "c" * 40,
            "state": "PROVIDER_FAILURE",
            "finding_codes": ["BUILDER_PROVIDER_EXCEPTION"],
            "provider_mode": "REAL",
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
            "receipt_digest": "d" * 64,
        }
        for stdout in ("not-json", json.dumps(mismatched)):
            with self.subTest(stdout=stdout[:16]):
                temp, runtime = self._runtime_fixture(stdout)
                try:
                    with self.assertRaises(LocalRuntimeError) as caught:
                        runtime.execute(local_job())
                finally:
                    temp.cleanup()
                self.assertEqual(caught.exception.code, "A2_EXECUTION_BLOCKED")
                self.assertEqual(getattr(caught.exception, "public_details", {}), {})

    def test_service_publishes_only_allowlisted_runtime_diagnostics(self) -> None:
        error = LocalRuntimeError("A2_EXECUTION_BLOCKED", "private local detail")
        error.public_details = {
            "a2_state": "PROVIDER_FAILURE",
            "a2_finding_code": "BUILDER_PROVIDER_EXCEPTION",
            "a2_provider_error_type": "CodexCliTransportError",
            "a2_receipt_digest": "d" * 64,
            "stdout": "secret",
            "stderr": "secret",
            "reasoning": "hidden",
        }
        plane = FakePlane([valid_issue()])
        service = LocalExecutorService(
            control_plane=plane,
            runtime=FailingRuntime(error),
            trusted_author=AUTHOR,
            required_label=LABEL,
        )

        result = service.once()

        self.assertEqual(result["code"], "A2_EXECUTION_BLOCKED")
        public = plane.published[0][1]
        self.assertEqual(public["a2_state"], "PROVIDER_FAILURE")
        self.assertEqual(public["a2_finding_code"], "BUILDER_PROVIDER_EXCEPTION")
        self.assertEqual(public["a2_provider_error_type"], "CodexCliTransportError")
        self.assertEqual(public["a2_receipt_digest"], "d" * 64)
        rendered = json.dumps(public, sort_keys=True)
        for forbidden in ("stdout", "stderr", "secret", "reasoning", "hidden", "private local detail"):
            self.assertNotIn(forbidden, rendered)

    def test_public_receipt_allows_safe_diagnostics_but_drops_raw_material(self) -> None:
        public = sanitize_public_receipt(
            {
                "status": "BLOCKED",
                "code": "A2_EXECUTION_BLOCKED",
                "a2_state": "PROVIDER_FAILURE",
                "a2_finding_code": "BUILDER_PROVIDER_EXCEPTION",
                "a2_provider_error_type": "CodexCliTransportError",
                "a2_receipt_digest": "d" * 64,
                "stdout": "secret",
                "stderr": "secret",
            }
        )

        self.assertEqual(public["a2_finding_code"], "BUILDER_PROVIDER_EXCEPTION")
        self.assertEqual(public["a2_provider_error_type"], "CodexCliTransportError")
        rendered = json.dumps(public, sort_keys=True)
        self.assertNotIn("stdout", rendered)
        self.assertNotIn("stderr", rendered)
        self.assertNotIn("secret", rendered)


if __name__ == "__main__":
    unittest.main()
