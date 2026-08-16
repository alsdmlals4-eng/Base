from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.job import LocalA2Job
from loop_a2_local_executor.runtime import (
    LocalA2Runtime,
    LocalRuntimeError,
    REVIEWED_TEST_IMAGE_REF,
)


class ProofStore:
    def __init__(self, base: Path, project: Path, runtime_root: Path) -> None:
        self.base = base
        self.project = project
        self.runtime_root = runtime_root

    @contextmanager
    def exact_worktree(self, repository: str, sha: str, role: str):
        yield self.base if role == "base" else self.project


class ProofRunner:
    def __init__(
        self,
        *,
        image_id: str,
        receipt: dict[str, object],
        image_id_present: bool = True,
    ) -> None:
        self.image_id = image_id
        self.receipt = receipt
        self.image_id_present = image_id_present
        self.digest_inspects = 0
        self.calls: list[tuple[str, ...]] = []

    def __call__(self, argv, **kwargs):
        command = tuple(argv)
        self.calls.append(command)

        if command[0] == "/trusted/docker" and command[1:3] == ("image", "inspect"):
            reference = command[-1]
            if reference == REVIEWED_TEST_IMAGE_REF:
                self.digest_inspects += 1
                if self.digest_inspects == 1:
                    return subprocess.CompletedProcess(list(argv), 0, stdout=self.image_id + "\n", stderr="")
                return subprocess.CompletedProcess(list(argv), 1, stdout="", stderr="digest alias unavailable")
            if reference == self.image_id:
                if self.image_id_present:
                    return subprocess.CompletedProcess(list(argv), 0, stdout=self.image_id + "\n", stderr="")
                return subprocess.CompletedProcess(list(argv), 1, stdout="", stderr="image id unavailable")

        if command[:3] == ("/trusted/docker", "version", "--format"):
            return subprocess.CompletedProcess(list(argv), 0, stdout="linux/amd64\n", stderr="")

        if command[0] == "/trusted/python":
            return subprocess.CompletedProcess(list(argv), 0, stdout=json.dumps(self.receipt), stderr="")

        raise AssertionError(f"unexpected command: {command!r}")


def _fixture(root: Path) -> tuple[ProofStore, LocalA2Job, dict[str, object]]:
    base = root / "base"
    project = root / "project"
    runtime_root = root / "runtime"
    (base / "tools").mkdir(parents=True)
    (base / "tools/loop_a2.py").write_text("# fixture\n", encoding="utf-8")
    capsule = project / "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json"
    capsule.parent.mkdir(parents=True)
    capsule.write_text(
        json.dumps({"project_id": "BLACKSMITH", "source_main_sha": "c" * 40}),
        encoding="utf-8",
    )
    job = LocalA2Job(
        issue_number=437,
        target_repository="alsdmlals4-eng/Blacksmith",
        base_runtime_sha="a" * 40,
        authority_sha="b" * 40,
        capsule="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        run_id="BS_A2_BURNIN_001",
        provider="real",
    )
    receipt = {
        "schema_version": 1,
        "contract_role": "LOOP_A2_RUN_RECEIPT",
        "project_id": "BLACKSMITH",
        "run_id": "BS_A2_BURNIN_001",
        "package_id": "BS_TEST_ONLY",
        "expected_main_sha": "c" * 40,
        "state": "WAITING_INTEGRATION",
        "provider_mode": "REAL",
        "a3_auto_merge": "DISABLED",
        "scheduler": "NOT_CONFIGURED",
        "receipt_digest": "d" * 64,
    }
    return ProofStore(base, project, runtime_root), job, receipt


class RuntimeImageProofContinuityTests(unittest.TestCase):
    def test_execute_reuses_preflight_verified_image_id_when_digest_alias_later_disappears(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            store, job, receipt = _fixture(Path(temp))
            image_id = "sha256:" + "e" * 64
            runner = ProofRunner(image_id=image_id, receipt=receipt)
            runtime = LocalA2Runtime(
                store=store,
                runner=runner,
                python_executable="/trusted/python",
                docker_executable="/trusted/docker",
            )

            self.assertEqual(runtime.preflight()["status"], "READY")
            result = runtime.execute(job)

            self.assertEqual(result["state"], "WAITING_INTEGRATION")
            self.assertEqual(runner.digest_inspects, 1)
            self.assertEqual(
                runner.calls[1],
                ("/trusted/docker", "image", "inspect", "--format", "{{.Id}}", image_id),
            )
            a2_argv = runner.calls[2]
            self.assertEqual(a2_argv[0], "/trusted/python")
            self.assertEqual(a2_argv[a2_argv.index("--denied-network-docker-image-id") + 1], image_id)
            rendered = "\n".join(" ".join(call) for call in runner.calls)
            self.assertNotIn(" pull ", f" {rendered} ")
            self.assertNotIn(" image ls ", f" {rendered} ")

    def test_cached_preflight_proof_fails_closed_when_exact_image_id_is_gone(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            store, job, receipt = _fixture(Path(temp))
            image_id = "sha256:" + "e" * 64
            runner = ProofRunner(image_id=image_id, receipt=receipt, image_id_present=False)
            runtime = LocalA2Runtime(
                store=store,
                runner=runner,
                python_executable="/trusted/python",
                docker_executable="/trusted/docker",
            )

            self.assertEqual(runtime.preflight()["status"], "READY")
            with self.assertRaises(LocalRuntimeError) as caught:
                runtime.execute(job)

            self.assertEqual(caught.exception.code, "DOCKER_IMAGE_NOT_PRELOADED")
            self.assertEqual(runner.digest_inspects, 1)
            self.assertEqual(
                runner.calls[1],
                ("/trusted/docker", "image", "inspect", "--format", "{{.Id}}", image_id),
            )
            self.assertEqual(len(runner.calls), 2)


if __name__ == "__main__":
    unittest.main()
