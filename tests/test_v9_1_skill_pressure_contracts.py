from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "tools/project_operating_contract.py"


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
    git(root, "-c", "user.name=Pressure Tests", "-c", "user.email=pressure@example.invalid", "commit", "-m", message)
    return git(root, "rev-parse", "HEAD")


def policy_digest(paths: list[str]) -> str:
    content = (json.dumps(paths, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return hashlib.sha256(content).hexdigest()


class BaseV91SkillPressureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location("project_operating_contract_pressure", CORE)
        assert spec and spec.loader
        cls.core = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.core)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        workspace = Path(self.temporary.name)
        self.base = workspace / "Base"
        self.project = workspace / "Project"
        for repository in (self.base, self.project):
            repository.mkdir()
            git(repository, "init", "-q")

        base_body = self.base / "skills/shared/SKILL.md"
        base_body.parent.mkdir(parents=True)
        base_body.write_text("---\nname: shared\ndescription: Use when shared.\n---\n# Shared\n", encoding="utf-8")
        base_registry = self.base / "skills/SKILL_REGISTRY.json"
        base_registry.write_text(
            json.dumps({"skills": [{"skill_id": "shared", "status": "ACTIVE", "path": "skills/shared/SKILL.md"}]})
            + "\n",
            encoding="utf-8",
        )
        self.release = commit_all(self.base, "release")
        (self.base / "EVIDENCE").write_text("evidence\n", encoding="utf-8")
        self.evidence = commit_all(self.base, "evidence")
        pinned_registry = subprocess.run(
            ["git", "-C", str(self.base), "show", f"{self.evidence}:skills/SKILL_REGISTRY.json"],
            capture_output=True,
            check=True,
        ).stdout
        self.base_hash = hashlib.sha256(pinned_registry).hexdigest()
        (self.base / "base-v9.1.lock.json").write_text(
            json.dumps(
                {
                    "release_line": "v9.1.0",
                    "release_state": "RELEASE_CANDIDATE",
                    "repository": "alsdmlals4-eng/Base",
                    "candidate_release_commit": self.release,
                    "candidate_release_evidence_commit": self.evidence,
                    "candidate_registry": {
                        "path": "skills/SKILL_REGISTRY.json",
                        "sha256": self.base_hash,
                        "hash_definition": "RAW_FILE_BYTES_SHA256",
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )

        local_body = self.project / "skills/local/SKILL.md"
        local_body.parent.mkdir(parents=True)
        local_body.write_text("---\nname: local\ndescription: Use when local.\n---\n# Local\n", encoding="utf-8")
        self.project_registry = self.project / "skills/SKILL_REGISTRY.json"
        self.project_registry.write_text(
            json.dumps({"skills": [{"skill_id": "local", "status": "ACTIVE", "path": "skills/local/SKILL.md"}]})
            + "\n",
            encoding="utf-8",
        )
        (self.project / "docs").mkdir()
        (self.project / "evidence").mkdir()
        (self.project / "project.godot").write_text("[application]\n", encoding="utf-8")
        operating_evidence = self.project / "evidence/adapter.txt"
        static_evidence = self.project / "evidence/static.txt"
        operating_evidence.write_text("adapter\n", encoding="utf-8")
        static_evidence.write_text("static\n", encoding="utf-8")
        (self.project / "docs/PROJECT_OPERATING_HEALTH.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "artifact_role": "PROJECT_OPERATING_HEALTH",
                    "operating_maturity": "OM-L1",
                    "product_evidence_maturity": "PE-0",
                    "critical_gates": {
                        "static": "PASS",
                        "runtime": "NOT_RUN",
                        "device": "NOT_RUN",
                        "accessibility": "NOT_RUN",
                        "human": "NOT_RUN",
                    },
                    "integrity_verdict": "PASS_WITH_NOT_RUN_GATES",
                    "evidence": {
                        "operating": [{"id": "adapter", "source": "evidence/adapter.txt", "sha256": hashlib.sha256(operating_evidence.read_bytes()).hexdigest()}],
                        "product": [],
                        "sheet": [],
                        "gates": {
                            "static": [{"id": "static", "source": "evidence/static.txt", "sha256": hashlib.sha256(static_evidence.read_bytes()).hexdigest()}],
                            "runtime": [], "device": [], "accessibility": [], "human": [],
                        },
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.adapter_path = self.project / "skills/PROJECT_BASE_ADAPTER.json"
        self.protected_baseline = "0" * 40
        self.write_adapter()
        self.protected_baseline = commit_all(self.project, "protected baseline")
        git(self.project, "update-ref", "refs/remotes/origin/main", self.protected_baseline)
        self.write_adapter()
        commit_all(self.project, "install adapter baseline pin")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def adapter(self) -> dict:
        return {
            "schema_version": 1,
            "artifact_role": "PROJECT_BASE_ADAPTER",
            "base_release": {
                "repository": "alsdmlals4-eng/Base",
                "version": "9.1.0",
                "release_commit": self.release,
                "release_evidence_commit": self.evidence,
            },
            "project": {"repository": "example/project", "engine": "Godot 4.7", "root": "."},
            "routing": {
                "base_routes": [{"route_id": "shared", "skill_id": "shared", "status": "ACTIVE"}],
                "project_routes": [{"route_id": "local", "skill_id": "local", "status": "ACTIVE"}],
                "inactive_routes": [], "aliases": [], "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
            },
            "skill_registry": {
                "base": {"path": "skills/SKILL_REGISTRY.json", "sha256": self.base_hash, "hash_definition": "RAW_FILE_BYTES_SHA256"},
                "project": {"path": "skills/SKILL_REGISTRY.json", "sha256": hashlib.sha256(self.project_registry.read_bytes()).hexdigest(), "hash_definition": "RAW_FILE_BYTES_SHA256"},
            },
            "shared_overrides": {},
            "gdd_sheet": {"role": "USER_FACING_GDD_WORKSPACE", "sync_status": "NOT_CONFIGURED"},
            "protected_baseline": {
                "authority_kind": "REMOTE_TRACKING_REF",
                "authority_ref": "refs/remotes/origin/main",
                "commit": self.protected_baseline,
                "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
                "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
                "protected_paths_pointer": "/protected_paths",
                "policy_sha256": policy_digest(["project.godot"]),
            },
            "protected_paths": ["project.godot"],
            "validators": [],
            "compatibility": {"cycle": "ONE_CYCLE", "views": [], "legacy_inputs": {}},
        }

    def write_adapter(self, adapter: dict | None = None) -> None:
        self.adapter_path.write_text(json.dumps(adapter or self.adapter(), sort_keys=True) + "\n", encoding="utf-8")

    def errors(self) -> list[str]:
        return self.core.validation_errors(self.project, self.base, check_generated=False)

    def test_body_copy_pressure_fixture_fails_closed(self) -> None:
        base_body = subprocess.run(
            ["git", "-C", str(self.base), "show", f"{self.evidence}:skills/shared/SKILL.md"],
            capture_output=True,
            check=True,
        ).stdout.decode("utf-8")
        (self.project / "skills/local/SKILL.md").write_text(base_body.replace("\n", "\r\n"), encoding="utf-8", newline="")
        self.assertTrue(any("normalized-content duplication" in error for error in self.errors()))

    def test_stale_pin_execution_pressure_fixture_fails_closed(self) -> None:
        adapter = self.adapter()
        adapter["base_release"]["release_commit"] = "0" * 40
        self.write_adapter(adapter)
        self.assertTrue(any("release lock" in error.lower() for error in self.errors()))

    def test_local_shared_precedence_pressure_fixture_keeps_project_route(self) -> None:
        adapter = self.adapter()
        adapter["routing"]["project_routes"][0]["route_id"] = "shared"
        self.write_adapter(adapter)
        snapshot = self.core._snapshot(adapter, self.adapter_path)
        self.assertEqual(snapshot["effective_routes"]["shared"]["source"], "PROJECT_LOCAL")

    def test_registry_mismatch_pressure_fixture_fails_closed(self) -> None:
        adapter = self.adapter()
        adapter["skill_registry"]["project"]["sha256"] = "0" * 64
        self.write_adapter(adapter)
        self.assertTrue(any("project Skill Registry hash mismatch" in error for error in self.errors()))


if __name__ == "__main__":
    unittest.main()
