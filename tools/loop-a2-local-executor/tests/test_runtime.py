from __future__ import annotations

from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.job import LocalA2Job
from loop_a2_local_executor.runtime import LocalA2Runtime, LocalRuntimeError, REVIEWED_TEST_IMAGE_REF


class FakeStore:
    def __init__(self, base: Path, project: Path, runtime_root: Path) -> None:
        self.base = base
        self.project = project
        self.runtime_root = runtime_root
        self.calls: list[tuple[str, str, str]] = []

    @contextmanager
    def exact_worktree(self, repository: str, sha: str, role: str):
        self.calls.append((repository, sha, role))
        yield self.base if role == "base" else self.project


class FakeRunner:
    def __init__(self, results: list[subprocess.CompletedProcess[str]]) -> None:
        self.results = list(results)
        self.calls: list[dict[str, object]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append({"argv": tuple(argv), **kwargs})
        return self.results.pop(0)


def job() -> LocalA2Job:
    return LocalA2Job(
        issue_number=12,
        target_repository="alsdmlals4-eng/Blacksmith",
        base_runtime_sha="a" * 40,
        authority_sha="b" * 40,
        capsule="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        run_id="BS_A2_BURNIN_001",
        provider="real",
    )


class RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.base = self.root / "base"
        self.project = self.root / "project"
        self.runtime_root = self.root / "runtime"
        (self.base / "tools").mkdir(parents=True)
        (self.base / "tools/loop_a2.py").write_text("# fixture\n", encoding="utf-8")
        capsule = self.project / "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json"
        capsule.parent.mkdir(parents=True)
        capsule.write_text(json.dumps({"project_id": "BLACKSMITH", "source_main_sha": "c" * 40}), encoding="utf-8")
        self.store = FakeStore(self.base, self.project, self.runtime_root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def success_receipt(self) -> dict[str, object]:
        return {
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

    def runtime(self, runner: FakeRunner) -> LocalA2Runtime:
        return LocalA2Runtime(
            store=self.store,
            runner=runner,
            python_executable="/trusted/python",
            docker_executable="/trusted/docker",
        )

    def test_reviewed_image_reference_is_exact_digest(self) -> None:
        self.assertEqual(
            REVIEWED_TEST_IMAGE_REF,
            "python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65",
        )

    def test_execute_inspects_image_then_runs_exact_host_derived_a2_argv(self) -> None:
        image_id = "sha256:" + "e" * 64
        runner = FakeRunner([
            subprocess.CompletedProcess([], 0, stdout=image_id + "\n", stderr=""),
            subprocess.CompletedProcess([], 0, stdout=json.dumps(self.success_receipt()), stderr=""),
        ])
        result = self.runtime(runner).execute(job())
        self.assertEqual(result["state"], "WAITING_INTEGRATION")
        self.assertEqual(
            runner.calls[0]["argv"],
            ("/trusted/docker", "image", "inspect", "--format", "{{.Id}}", REVIEWED_TEST_IMAGE_REF),
        )
        argv = runner.calls[1]["argv"]
        self.assertEqual(argv[0], "/trusted/python")
        self.assertEqual(argv[1], str(self.base / "tools/loop_a2.py"))
        self.assertEqual(argv[2:4], ("run", "--project-root"))
        self.assertIn(str(self.project), argv)
        self.assertIn("--provider", argv)
        self.assertEqual(argv[argv.index("--provider") + 1], "real")
        self.assertEqual(argv[argv.index("--observed-main-sha") + 1], "c" * 40)
        self.assertEqual(argv[argv.index("--denied-network-docker-image-id") + 1], image_id)
        rendered = " ".join(argv)
        self.assertNotIn("powershell", rendered.casefold())
        self.assertNotIn("cmd.exe", rendered.casefold())

    def test_execute_never_pulls_image(self) -> None:
        runner = FakeRunner([subprocess.CompletedProcess([], 1, stdout="", stderr="not found")])
        with self.assertRaises(LocalRuntimeError) as caught:
            self.runtime(runner).execute(job())
        self.assertEqual(caught.exception.code, "DOCKER_IMAGE_NOT_PRELOADED")
        self.assertTrue(all("pull" not in call["argv"] for call in runner.calls))

    def test_invalid_image_id_fails_before_a2(self) -> None:
        runner = FakeRunner([subprocess.CompletedProcess([], 0, stdout="python:tag\n", stderr="")])
        with self.assertRaises(LocalRuntimeError) as caught:
            self.runtime(runner).execute(job())
        self.assertEqual(caught.exception.code, "DOCKER_IMAGE_ID_INVALID")
        self.assertEqual(len(runner.calls), 1)

    def test_child_environment_excludes_api_and_github_tokens(self) -> None:
        image_id = "sha256:" + "e" * 64
        old = {key: os.environ.get(key) for key in ("OPENAI_API_KEY", "OPENAI_ORG_ID", "OPENAI_PROJECT_ID", "OPENAI_BASE_URL", "GH_TOKEN", "GITHUB_TOKEN")}
        for key in old:
            os.environ[key] = "secret"
        runner = FakeRunner([
            subprocess.CompletedProcess([], 0, stdout=image_id + "\n", stderr=""),
            subprocess.CompletedProcess([], 0, stdout=json.dumps(self.success_receipt()), stderr=""),
        ])
        try:
            self.runtime(runner).execute(job())
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        env = runner.calls[1]["env"]
        for key in old:
            self.assertNotIn(key, env)

    def test_receipt_must_preserve_real_a3_scheduler_and_identity(self) -> None:
        image_id = "sha256:" + "e" * 64
        for key, value in (
            ("state", "BLOCKED_UNVERIFIED"),
            ("provider_mode", "FAKE"),
            ("a3_auto_merge", "ENABLED"),
            ("scheduler", "CONFIGURED"),
            ("run_id", "OTHER_RUN"),
            ("expected_main_sha", "f" * 40),
        ):
            with self.subTest(key=key):
                receipt = self.success_receipt()
                receipt[key] = value
                runner = FakeRunner([
                    subprocess.CompletedProcess([], 0, stdout=image_id + "\n", stderr=""),
                    subprocess.CompletedProcess([], 0, stdout=json.dumps(receipt), stderr=""),
                ])
                with self.assertRaises(LocalRuntimeError) as caught:
                    self.runtime(runner).execute(job())
                self.assertEqual(caught.exception.code, "A2_RECEIPT_INVALID")

    def test_capsule_source_sha_is_required(self) -> None:
        capsule = self.project / job().capsule
        capsule.write_text(json.dumps({"project_id": "BLACKSMITH"}), encoding="utf-8")
        runner = FakeRunner([])
        with self.assertRaises(LocalRuntimeError) as caught:
            self.runtime(runner).execute(job())
        self.assertEqual(caught.exception.code, "CAPSULE_SOURCE_SHA_INVALID")
        self.assertEqual(runner.calls, [])

    def test_symlinked_capsule_is_rejected_even_when_target_stays_inside_authority_root(self) -> None:
        capsule = self.project / job().capsule
        alternate = capsule.parent / "ALTERNATE_CAPSULE.json"
        alternate.write_text(capsule.read_text(encoding="utf-8"), encoding="utf-8")
        capsule.unlink()
        try:
            capsule.symlink_to(alternate.name)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable")
        runner = FakeRunner([])
        with self.assertRaises(LocalRuntimeError) as caught:
            self.runtime(runner).execute(job())
        self.assertEqual(caught.exception.code, "CAPSULE_UNAVAILABLE")
        self.assertEqual(runner.calls, [])


if __name__ == "__main__":
    unittest.main()
