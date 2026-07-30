from __future__ import annotations

import re
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


def commit_all(root: Path, message: str) -> str:
    git(root, "add", ".")
    git(root, "-c", "user.name=Review Tests", "-c", "user.email=review@example.invalid", "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


class BaseV91ReviewRemediationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("check_base_v9_integrity", ROOT / "tools/check_base_v9_integrity.py")
        assert spec and spec.loader
        cls.integrity = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.integrity)

    def test_ci_uses_exact_action_allowlist_and_installs_pinned_validation_requirements(self) -> None:
        allowed = {
            "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
            "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
            "actions/setup-node": "49933ea5288caeca8642d1e84afbd3f7d6820020",
            "actions/upload-artifact": "ea165f8d65b6e75b540449e92b4886f43607fa02",
            "actions/dependency-review-action": "da24556b548a50705dd671f47852072ea4c105d9",
        }
        seen: set[str] = set()
        for workflow in (ROOT / ".github/workflows").glob("*.yml"):
            text = workflow.read_text(encoding="utf-8")
            for action, ref in re.findall(r"uses:\s+(actions/[^@\s]+)@([0-9a-f]+)", text):
                self.assertIn(action, allowed, f"Unreviewed official Action in {workflow.name}: {action}")
                self.assertEqual(ref, allowed[action], f"Wrong immutable ref for {action} in {workflow.name}")
                seen.add(action)
        self.assertEqual(seen, set(allowed))

        requirements = ROOT / ".github/validation-requirements.txt"
        self.assertTrue(requirements.is_file())
        requirement_text = requirements.read_text(encoding="utf-8")
        self.assertRegex(requirement_text, r"(?m)^jsonschema==[0-9]+\.[0-9]+\.[0-9]+$")
        workflow = (ROOT / ".github/workflows/validate-base-v9-rc.yml").read_text(encoding="utf-8")
        install = "python -m pip install --requirement .github/validation-requirements.txt"
        self.assertIn(install, workflow)
        self.assertLess(workflow.index(install), workflow.index("python tools/build_base_v9_artifacts.py --check"))

    def test_dependency_review_covers_common_manifest_and_lock_formats(self) -> None:
        workflow = (ROOT / ".github/workflows/dependency-review.yml").read_text(encoding="utf-8")
        for pattern in (
            "**/package-lock.json",
            "**/yarn.lock",
            "**/bun.lockb",
            "**/Pipfile.lock",
            "**/uv.lock",
            "**/Cargo.lock",
            "**/go.sum",
            "**/Gemfile.lock",
            "**/composer.lock",
        ):
            self.assertIn(pattern, workflow)

    def test_v90_frozen_artifacts_match_declared_historical_blobs_byte_for_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            git(repository, "init", "-q")
            frozen = (
                "base.lock.json",
                ".codex-plugin/plugin.json",
                "skills/BASE_V9_SKILL_SNAPSHOT.json",
            )
            for index, relative in enumerate(frozen):
                path = repository / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(f"frozen-{index}\n".encode("utf-8"))
            evidence = commit_all(repository, "v9.0 evidence")
            lock = {
                "compatibility_base": {
                    "release_evidence_commit": evidence,
                    "frozen_artifacts": list(frozen),
                }
            }
            self.assertEqual(self.integrity.frozen_artifact_errors(repository, lock), [])

            for relative in frozen:
                with self.subTest(relative=relative):
                    path = repository / relative
                    original = path.read_bytes()
                    path.write_bytes(original + b"x")
                    errors = self.integrity.frozen_artifact_errors(repository, lock)
                    self.assertTrue(any(relative in error for error in errors), errors)
                    path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
