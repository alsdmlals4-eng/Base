from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "tools" / "loop-a2-local-executor" / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.runtime import LocalA2Runtime, LocalRuntimeError


class FakeStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.runtime_root = root / "runtime"

    @contextmanager
    def exact_worktree(self, repository: str, sha: str, role: str):
        del repository, sha, role
        yield self.root


class RecordingRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((tuple(str(item) for item in argv), dict(kwargs)))
        return self.responses.pop(0)


class RealAuthorityDependencyTests(unittest.TestCase):
    def test_package_declares_canonical_schema_validator_dependency(self) -> None:
        pyproject = tomllib.loads(
            (ROOT / "tools/loop-a2-local-executor/pyproject.toml").read_text(
                encoding="utf-8"
            )
        )
        dependencies = pyproject["project"]["dependencies"]
        publication_requirements = (
            ROOT / "requirements-publication.txt"
        ).read_text(encoding="utf-8").splitlines()

        self.assertIn("jsonschema==4.26.0", dependencies)
        self.assertIn("jsonschema==4.26.0", publication_requirements)

    def test_shared_preflight_fails_before_docker_when_schema_validator_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image_id = "sha256:" + "e" * 64
            runner = RecordingRunner(
                [
                    subprocess.CompletedProcess(
                        [], 0, stdout=image_id + "\n", stderr=""
                    )
                ]
            )
            runtime = LocalA2Runtime(
                store=FakeStore(root),
                runner=runner,
                python_executable="/trusted/python",
                docker_executable="/trusted/docker",
            )

            with patch.dict(sys.modules, {"jsonschema": None}):
                with self.assertRaises(LocalRuntimeError) as caught:
                    runtime.preflight()

        self.assertEqual(caught.exception.code, "A2_RUNTIME_DEPENDENCY_MISSING")
        self.assertEqual(runner.calls, [])


if __name__ == "__main__":
    unittest.main()
