from __future__ import annotations

import re
import importlib.util
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
V90_OUTPUTS = {
    ".codex-plugin/plugin.json",
    "base.lock.json",
    "skills/BASE_V9_SKILL_SNAPSHOT.json",
    "docs/generated/BASE_ACTIVE_SKILLS.md",
    "docs/operations/BASE_V9_DECISION_REGISTRY.json",
    "docs/operations/GITHUB_OBJECT_LEDGER.json",
    "docs/operations/ADVERSARIAL_REVIEW_MANIFEST.json",
    "docs/operations/SHEET_CONTROL_CONTRACT.json",
}


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


def frozen_entry(root: Path, evidence: str, relative: str) -> dict[str, str]:
    raw = subprocess.run(
        ["git", "-C", str(root), "show", f"{evidence}:{relative}"],
        capture_output=True,
        check=True,
    ).stdout
    return {
        "path": relative,
        "git_blob_oid": git(root, "rev-parse", f"{evidence}:{relative}"),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def release_history(root: Path) -> tuple[dict, str, str]:
    git(root, "init", "-q")
    git(root, "config", "core.autocrlf", "false")
    registry = root / "skills/SKILL_REGISTRY.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text('{"skills":[]}\n', encoding="utf-8")
    for index, relative in enumerate(sorted(V90_OUTPUTS - {"base.lock.json"})):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"artifact-{index}\n", encoding="utf-8")
    pending = {
        "release_line": "v9.0.0",
        "release_state": "BASE_RELEASE_PENDING_CI",
        "final_release_state": "BASE_RELEASE_PENDING_CI",
        "source_of_truth": "skills/SKILL_REGISTRY.json",
        "registry_sha256": hashlib.sha256(registry.read_bytes()).hexdigest(),
    }
    write_json(root / "base.lock.json", pending)
    release_commit = commit_all(root, "v9.0 release payload")
    released = dict(pending)
    released.update(
        {
            "release_state": "BASE_RELEASED",
            "final_release_state": "BASE_RELEASED",
            "release_commit": release_commit,
        }
    )
    write_json(root / "base.lock.json", released)
    evidence_commit = commit_all(root, "v9.0 release evidence")
    (root / "README.md").write_text("later trusted history\n", encoding="utf-8")
    trusted_tip = commit_all(root, "later trusted history")
    lock = {
        "compatibility_base": {
            "release_line": "v9.0.0",
            "release_state": "BASE_RELEASED",
            "release_commit": release_commit,
            "release_evidence_commit": evidence_commit,
            "frozen_artifacts": [
                frozen_entry(root, evidence_commit, relative) for relative in sorted(V90_OUTPUTS)
            ],
            "historical_registry": {
                "commit": evidence_commit,
                "path": "skills/SKILL_REGISTRY.json",
                "sha256": hashlib.sha256(registry.read_bytes()).hexdigest(),
                "hash_definition": "RAW_FILE_BYTES_SHA256",
            },
        },
        "candidate_registry": {
            "path": "skills/SKILL_REGISTRY.json",
            "sha256": hashlib.sha256(registry.read_bytes()).hexdigest(),
            "hash_definition": "RAW_FILE_BYTES_SHA256",
        },
    }
    return lock, evidence_commit, trusted_tip


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
        self.assertRegex(requirement_text, r"(?m)^Pillow==[0-9]+\.[0-9]+\.[0-9]+$")
        self.assertRegex(requirement_text, r"(?m)^markdown-it-py==[0-9]+\.[0-9]+\.[0-9]+$")
        self.assertRegex(requirement_text, r"(?m)^pypdf==[0-9]+\.[0-9]+\.[0-9]+$")
        workflow = (ROOT / ".github/workflows/validate-base-v9-rc.yml").read_text(encoding="utf-8")
        install = "python -m pip install --requirement .github/validation-requirements.txt"
        self.assertIn(install, workflow)
        self.assertLess(workflow.index(install), workflow.index("python tools/build_base_v9_artifacts.py --check"))
        self.assertIn("fetch-depth: 0", workflow)
        self.assertIn(
            "TRUSTED_HISTORY_COMMIT: ${{ github.event.pull_request.base.sha || github.sha }}",
            workflow,
        )
        self.assertIn('--trusted-history-commit "$TRUSTED_HISTORY_COMMIT"', workflow)

    def test_dependency_review_covers_common_manifest_and_lock_formats(self) -> None:
        workflow = (ROOT / ".github/workflows/dependency-review.yml").read_text(encoding="utf-8")
        self.assertIn("vars.DEPENDENCY_REVIEW_ENABLED == 'true'", workflow)
        self.assertNotIn("github.event.repository.private == false", workflow)
        self.assertIn("DEFERRED_UNTIL_REPOSITORY_SECURITY_ENABLED", workflow)
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
            ".github/workflows/**",
            '"action.yml"',
            '"action.yaml"',
            "**/action.yml",
            "**/action.yaml",
        ):
            self.assertIn(pattern, workflow)

    def test_v91_release_evidence_record_binds_the_merged_candidate_payload(self) -> None:
        evidence_path = ROOT / "docs/operations/BASE_V9_1_RELEASE_EVIDENCE.json"
        schema_path = ROOT / "schemas/base-v9-1-release-evidence-v1.schema.json"
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(evidence), key=lambda error: list(error.path))
        self.assertEqual(errors, [])
        self.assertEqual(evidence["release_payload_commit"], "3c158f52cfdad889970aef4d6ce6650a6fea0645")
        self.assertEqual(evidence["candidate_registry"]["path"], "skills/SKILL_REGISTRY.json")
        self.assertEqual(
            evidence["candidate_registry"]["sha256"],
            "e06003cb986e979aa46c06839de178c3fb9ff10bdf440e750712d90d6c5ae7bb",
        )

    def test_v90_frozen_artifacts_pin_all_historical_blobs_without_freezing_current_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            git(repository, "init", "-q")
            frozen = tuple(sorted(V90_OUTPUTS))
            for index, relative in enumerate(frozen):
                path = repository / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(f"frozen-{index}\n".encode("utf-8"))
            evidence = commit_all(repository, "v9.0 evidence")
            lock = {
                "compatibility_base": {
                    "release_evidence_commit": evidence,
                    "frozen_artifacts": [frozen_entry(repository, evidence, relative) for relative in frozen],
                }
            }
            self.assertEqual(self.integrity.frozen_artifact_errors(repository, lock), [])

            for relative in frozen:
                (repository / relative).write_bytes(f"current evolution: {relative}\r\n".encode("utf-8"))
            self.assertEqual(self.integrity.frozen_artifact_errors(repository, lock), [])

            incomplete = json.loads(json.dumps(lock))
            incomplete["compatibility_base"]["frozen_artifacts"].pop()
            self.assertTrue(any("complete" in error.lower() for error in self.integrity.frozen_artifact_errors(repository, incomplete)))

            duplicate = json.loads(json.dumps(lock))
            duplicate["compatibility_base"]["frozen_artifacts"][-1] = duplicate["compatibility_base"]["frozen_artifacts"][0]
            self.assertTrue(any("complete" in error.lower() for error in self.integrity.frozen_artifact_errors(repository, duplicate)))

            additional = json.loads(json.dumps(lock))
            additional["compatibility_base"]["frozen_artifacts"].append(
                {"path": "extra.json", "git_blob_oid": "0" * 40, "sha256": "0" * 64}
            )
            self.assertTrue(any("complete" in error.lower() for error in self.integrity.frozen_artifact_errors(repository, additional)))

            bad_oid = json.loads(json.dumps(lock))
            bad_oid["compatibility_base"]["frozen_artifacts"][0]["git_blob_oid"] = "0" * 40
            self.assertTrue(any("blob id" in error.lower() for error in self.integrity.frozen_artifact_errors(repository, bad_oid)))

            bad_hash = json.loads(json.dumps(lock))
            bad_hash["compatibility_base"]["frozen_artifacts"][0]["sha256"] = "0" * 64
            self.assertTrue(any("sha-256" in error.lower() for error in self.integrity.frozen_artifact_errors(repository, bad_hash)))

            unavailable_repository = repository / "unavailable"
            unavailable_repository.mkdir()
            git(unavailable_repository, "init", "-q")
            (unavailable_repository / "README.md").write_text("no frozen blobs\n", encoding="utf-8")
            unavailable_evidence = commit_all(unavailable_repository, "evidence without frozen outputs")
            unavailable = json.loads(json.dumps(lock))
            unavailable["compatibility_base"]["release_evidence_commit"] = unavailable_evidence
            self.assertTrue(
                any(
                    "historical blob is unavailable" in error.lower()
                    for error in self.integrity.frozen_artifact_errors(unavailable_repository, unavailable)
                )
            )

    def test_v90_historical_blob_check_is_crlf_and_current_evolution_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            source = workspace / "source"
            clone = workspace / "clone"
            source.mkdir()
            git(source, "init", "-q")
            for index, relative in enumerate(sorted(V90_OUTPUTS)):
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(f"line-{index}\nsecond-line\n".encode("utf-8"))
            evidence = commit_all(source, "v9.0 evidence")
            subprocess.run(
                ["git", "clone", "-q", "-c", "core.autocrlf=true", str(source), str(clone)],
                check=True,
                capture_output=True,
            )
            lock = {
                "compatibility_base": {
                    "release_evidence_commit": evidence,
                    "frozen_artifacts": [
                        frozen_entry(source, evidence, relative) for relative in sorted(V90_OUTPUTS)
                    ],
                }
            }
            self.assertEqual(self.integrity.frozen_artifact_errors(clone, lock), [])
            mutated = clone / "docs/generated/BASE_ACTIVE_SKILLS.md"
            mutated.write_bytes(mutated.read_bytes() + b"semantic-mutation")
            self.assertEqual(self.integrity.frozen_artifact_errors(clone, lock), [])

    def test_v91_lock_separates_historical_and_current_registry_authority(self) -> None:
        lock = json.loads((ROOT / "base-v9.1.lock.json").read_text(encoding="utf-8"))
        base_lock = json.loads((ROOT / "base.lock.json").read_text(encoding="utf-8"))
        historical = lock["compatibility_base"]["historical_registry"]
        current = lock["candidate_registry"]
        self.assertEqual(historical["commit"], lock["compatibility_base"]["release_evidence_commit"])
        self.assertEqual(historical["path"], base_lock["source_of_truth"])
        self.assertEqual(historical["sha256"], base_lock["registry_sha256"])
        current_path = ROOT / current["path"]
        self.assertEqual(current["sha256"], hashlib.sha256(current_path.read_bytes()).hexdigest())
        self.assertEqual(self.integrity.registry_authority_errors(ROOT, lock), [])

    def test_release_evidence_is_exact_transition_inside_trusted_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            lock, evidence_commit, trusted_tip = release_history(repository)
            release_errors = getattr(self.integrity, "release_evidence_errors", lambda *_: [])
            self.assertEqual(
                release_errors(repository, lock, trusted_tip),
                [],
            )

            rebound = json.loads(json.dumps(lock))
            rebound["compatibility_base"]["release_evidence_commit"] = trusted_tip
            rebound["compatibility_base"]["historical_registry"]["commit"] = trusted_tip
            rebound["compatibility_base"]["frozen_artifacts"] = [
                frozen_entry(repository, trusted_tip, relative) for relative in sorted(V90_OUTPUTS)
            ]
            self.assertEqual(self.integrity.frozen_artifact_errors(repository, rebound), [])
            self.assertTrue(
                any(
                    "transition boundary" in error.lower()
                    for error in release_errors(repository, rebound, trusted_tip)
                )
            )

            self.assertTrue(
                any(
                    "trusted history" in error.lower()
                    for error in release_errors(repository, lock, "f" * 40)
                )
            )
            tree = git(repository, "rev-parse", f"{evidence_commit}^{{tree}}")
            unrelated = subprocess.run(
                [
                    "git", "-C", str(repository),
                    "-c", "user.name=Review Tests",
                    "-c", "user.email=review@example.invalid",
                    "commit-tree", tree, "-m", "unrelated trusted tip",
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            self.assertTrue(
                any(
                    "not an ancestor" in error.lower()
                    for error in release_errors(repository, lock, unrelated)
                )
            )

    def test_historical_registry_uses_evidence_base_lock_not_current_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            lock, _, _ = release_history(repository)
            write_json(
                repository / "base.lock.json",
                {
                    "release_line": "v10.0.0",
                    "release_state": "FUTURE_EVOLUTION",
                    "source_of_truth": "future/REGISTRY.json",
                    "registry_sha256": "0" * 64,
                },
            )
            self.assertEqual(self.integrity.registry_authority_errors(repository, lock), [])


if __name__ == "__main__":
    unittest.main()
