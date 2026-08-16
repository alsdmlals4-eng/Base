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
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.control_plane import sanitize_public_receipt
from loop_a2_local_executor.job import LocalA2Job
from loop_a2_local_executor.runtime import LocalA2Runtime, LocalRuntimeError
from loop_a2_local_executor.service import LocalExecutorService


AUTHOR = "alsdmlals4-eng"
LABEL = "loop-a2-local-job"


class RecordingRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]) -> None:
        self.responses = list(responses)

    def __call__(self, argv, **kwargs):
        del argv, kwargs
        return self.responses.pop(0)


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
        issue_number=448,
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
        "number": 448,
        "author": {"login": AUTHOR},
        "labels": [{"name": LABEL}],
        "body": "```json\n" + json.dumps(body) + "\n```",
    }


def child_terminal(
    *,
    code: str = "SUBSCRIPTION_CODEX_AUTH_REQUIRED",
    role: str = "LOOP_A2_CHILD_TERMINAL",
    status: str = "BLOCKED_UNVERIFIED",
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "contract_role": role,
        "status": status,
        "code": code,
        "message": "private child detail with C:/Users/example/secret",
    }


class ChildTerminalDiagnosticsTests(unittest.TestCase):
    def _runtime_fixture(self, child_stdout: str):
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
            json.dumps(
                {
                    "project_id": "BLACKSMITH",
                    "source_main_sha": "c" * 40,
                    "implementation_package_path": "IMPLEMENTATION_PACKAGE.json",
                }
            ),
            encoding="utf-8",
        )
        (capsule.parent / "IMPLEMENTATION_PACKAGE.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "contract_role": "LOOP_IMPLEMENTATION_PACKAGE",
                    "project_id": "BLACKSMITH",
                    "package_id": "BS_TEST_ONLY",
                    "source_main_sha": "c" * 40,
                }
            ),
            encoding="utf-8",
        )
        image_id = "sha256:" + "e" * 64
        runtime = LocalA2Runtime(
            store=FakeStore(base, project, runtime_root),
            runner=RecordingRunner(
                [
                    subprocess.CompletedProcess([], 0, stdout=image_id + "\n", stderr=""),
                    subprocess.CompletedProcess([], 2, stdout=child_stdout, stderr="private child stderr"),
                ]
            ),
            python_executable="/trusted/python",
            docker_executable="/trusted/docker",
        )
        return temp, runtime

    def test_valid_child_terminal_preserves_only_stable_code(self) -> None:
        temp, runtime = self._runtime_fixture(json.dumps(child_terminal()))
        try:
            with self.assertRaises(LocalRuntimeError) as caught:
                runtime.execute(local_job())
        finally:
            temp.cleanup()

        self.assertEqual(caught.exception.code, "A2_EXECUTION_BLOCKED")
        self.assertEqual(
            caught.exception.public_details,
            {"a2_child_code": "SUBSCRIPTION_CODEX_AUTH_REQUIRED"},
        )
        rendered = json.dumps(caught.exception.public_details, sort_keys=True)
        self.assertNotIn("private child detail", rendered)
        self.assertNotIn("C:/Users", rendered)

    def test_invalid_child_terminal_shapes_remain_generic(self) -> None:
        invalid = (
            child_terminal(role="OTHER_ROLE"),
            child_terminal(status="PASS"),
            child_terminal(code="lowercase-code"),
            child_terminal(code="A" * 129),
        )
        for payload in invalid:
            with self.subTest(payload=payload):
                temp, runtime = self._runtime_fixture(json.dumps(payload))
                try:
                    with self.assertRaises(LocalRuntimeError) as caught:
                        runtime.execute(local_job())
                finally:
                    temp.cleanup()
                self.assertEqual(caught.exception.code, "A2_EXECUTION_BLOCKED")
                self.assertEqual(caught.exception.public_details, {})

    def test_service_allows_child_code_but_drops_raw_material(self) -> None:
        error = LocalRuntimeError(
            "A2_EXECUTION_BLOCKED",
            "private local detail",
            public_details={
                "a2_child_code": "SUBSCRIPTION_CODEX_AUTH_REQUIRED",
                "stdout": "secret",
                "stderr": "secret",
                "message": "private",
            },
        )
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
        self.assertEqual(public["a2_child_code"], "SUBSCRIPTION_CODEX_AUTH_REQUIRED")
        rendered = json.dumps(public, sort_keys=True)
        for forbidden in ("stdout", "stderr", "secret", "message", "private local detail"):
            self.assertNotIn(forbidden, rendered)

    def test_public_receipt_allows_only_child_code_scalar(self) -> None:
        public = sanitize_public_receipt(
            {
                "status": "BLOCKED",
                "code": "A2_EXECUTION_BLOCKED",
                "a2_child_code": "SUBSCRIPTION_CODEX_AUTH_REQUIRED",
                "message": "private",
                "stdout": "secret",
            }
        )

        self.assertEqual(public["a2_child_code"], "SUBSCRIPTION_CODEX_AUTH_REQUIRED")
        rendered = json.dumps(public, sort_keys=True)
        self.assertNotIn("message", rendered)
        self.assertNotIn("stdout", rendered)
        self.assertNotIn("secret", rendered)


if __name__ == "__main__":
    unittest.main()
