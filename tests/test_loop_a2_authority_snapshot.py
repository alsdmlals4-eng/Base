from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import tools.loop_a2_runtime.authority_snapshot as authority_snapshot
from tools.loop_a2_runtime.authority_snapshot import (
    AuthoritySnapshotError,
    capture_authority_snapshot,
)
from tools.loop_a2_runtime.contract_bridge import build_request_from_capsule
from tools.loop_a2_runtime.protocol import Budgets


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates" / "project-operations" / "loop"
CAPSULE = "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json"


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=check,
    )


def _rewrite_source_fields(value: object, source_sha: str) -> object:
    if isinstance(value, dict):
        result: dict[str, object] = {}
        for key, item in value.items():
            if key in {"source_main_sha", "source_commit"}:
                result[key] = source_sha
            else:
                result[key] = _rewrite_source_fields(item, source_sha)
        return result
    if isinstance(value, list):
        return [_rewrite_source_fields(item, source_sha) for item in value]
    return value


class AuthoritySnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        _git(self.repo, "init", "-b", "main")
        _git(self.repo, "config", "user.name", "Loop Test")
        _git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts/example.gd").write_text("extends Node\n", encoding="utf-8")
        _git(self.repo, "add", ".")
        _git(self.repo, "commit", "-m", "implementation baseline")
        self.baseline = _git(self.repo, "rev-parse", "HEAD").stdout.strip()

        loop = self.repo / "docs/operations/loop"
        shutil.copytree(TEMPLATE_ROOT, loop)
        for path in sorted(loop.rglob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            value = _rewrite_source_fields(value, self.baseline)
            path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

        self.request = build_request_from_capsule(
            project_root=self.repo,
            capsule_relative=CAPSULE,
            run_id="RUN_AUTHORITY_001",
            provider_mode="REAL",
            budgets=Budgets(12, 2, 600),
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_snapshot_captures_post_baseline_authority_without_redefining_baseline(self) -> None:
        absent = _git(
            self.repo,
            "cat-file",
            "-e",
            f"{self.baseline}:{CAPSULE}",
            check=False,
        )
        self.assertNotEqual(absent.returncode, 0, "fixture must keep Capsule out of baseline")
        self.assertEqual(self.request.expected_main_sha, self.baseline)

        snapshot = capture_authority_snapshot(
            project_root=self.repo,
            capsule_relative=CAPSULE,
            request=self.request,
        )

        self.assertEqual(snapshot.project_id, self.request.project_id)
        self.assertEqual(snapshot.package_id, self.request.package_id)
        self.assertEqual(snapshot.source_main_sha, self.baseline)
        self.assertIn(self.request.capsule_path, snapshot.paths)
        self.assertIn(self.request.package_path, snapshot.paths)
        self.assertRegex(snapshot.snapshot_sha256, r"^[0-9a-f]{64}$")
        self.assertEqual(
            snapshot.parsed_object(self.request.package_path)["package_id"],
            self.request.package_id,
        )

    def test_snapshot_rejects_request_authority_mismatch(self) -> None:
        value = self.request.to_dict()
        value["package_id"] = "OTHER_PACKAGE"
        from tools.loop_a2_runtime.protocol import RunRequest

        mismatched = RunRequest.from_dict(value)
        with self.assertRaisesRegex(AuthoritySnapshotError, "request"):
            capture_authority_snapshot(
                project_root=self.repo,
                capsule_relative=CAPSULE,
                request=mismatched,
            )

    def test_snapshot_rejects_symlinked_authority_file(self) -> None:
        package = self.repo / self.request.package_path
        real = package.with_name("IMPLEMENTATION_PACKAGE_REAL.json")
        package.rename(real)
        try:
            package.symlink_to(real.name)
        except (OSError, NotImplementedError):
            real.rename(package)
            self.skipTest("symlink unavailable")

        with self.assertRaisesRegex(AuthoritySnapshotError, "symlink"):
            capture_authority_snapshot(
                project_root=self.repo,
                capsule_relative=CAPSULE,
                request=self.request,
            )

    def test_snapshot_rejects_schema_valid_authority_mutation_during_capture(self) -> None:
        planning = self.repo / "docs/operations/loop/PLANNING_LOCK.json"
        original_validate = authority_snapshot.validate_bundle

        def validate_then_mutate(capsule_path: Path):
            findings = original_validate(capsule_path)
            value = json.loads(planning.read_text(encoding="utf-8"))
            value["protected_meanings"].append(
                "Concurrent editor mutation must not enter this snapshot."
            )
            planning.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
            return findings

        with patch.object(
            authority_snapshot,
            "validate_bundle",
            side_effect=validate_then_mutate,
        ):
            with self.assertRaisesRegex(
                AuthoritySnapshotError,
                "changed during capture",
            ):
                capture_authority_snapshot(
                    project_root=self.repo,
                    capsule_relative=CAPSULE,
                    request=self.request,
                )


if __name__ == "__main__":
    unittest.main()
