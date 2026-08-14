import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from base_tool_contracts import ProjectIdentityError, validate_project_identity


BASE_ROOT = Path(__file__).resolve().parents[3]


def test_package_import_succeeds_when_posix_fcntl_is_unavailable() -> None:
    source_root = BASE_ROOT / "tools/base-tool-contracts/src"
    code = """
import importlib.abc
import sys

class BlockFcntl(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "fcntl":
            raise ModuleNotFoundError("No module named 'fcntl'")
        return None

sys.modules.pop("fcntl", None)
sys.meta_path.insert(0, BlockFcntl())
import base_tool_contracts
print("BASE_TOOL_CONTRACTS_IMPORT_OK")
"""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(source_root)

    completed = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        check=False,
        text=True,
        env=environment,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "BASE_TOOL_CONTRACTS_IMPORT_OK"


def make_identity_project(root: Path, project_id: str = "demo-game") -> Path:
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True)
    (root / "game").mkdir()
    (root / "project.godot").write_text("[application]\n", encoding="utf-8")
    (root / "skills").mkdir()
    project_registry = b'{"skills":[]}\n'
    (root / "skills" / "SKILL_REGISTRY.json").write_bytes(project_registry)
    legacy = {"protected_paths": ["project.godot", "game/**"]}
    (root / "skills" / "LEGACY_PROJECT_ADAPTER.json").write_text(json.dumps(legacy), encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"], check=True)
    baseline = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(root)], check=True)
    subprocess.run(
        ["git", "-C", str(root), "fetch", "-q", "origin", f"{baseline}:refs/remotes/origin/main"],
        check=True,
    )
    adapter = json.loads(
        (BASE_ROOT / "templates/project-operations/PROJECT_BASE_ADAPTER_V2.json").read_text(encoding="utf-8")
    )
    adapter["project"] = {
        "project_id": project_id,
        "repository": f"owner/{project_id}",
        "engine": "Godot 4.7",
        "root": ".",
    }
    lock = json.loads((BASE_ROOT / "base-v9.3.lock.json").read_text(encoding="utf-8"))
    adapter["base_release"].update(
        repository="alsdmlals4-eng/Base",
        version="9.3.0",
        release_commit=lock["candidate_release_commit"],
        release_evidence_commit=lock["candidate_release_evidence_commit"],
    )
    adapter["base_release"].pop("finalization_commit", None)
    adapter["skill_registry"]["base"] = lock["candidate_registry"]
    adapter["skill_registry"]["project"]["sha256"] = hashlib.sha256(project_registry).hexdigest()
    policy = (json.dumps(legacy["protected_paths"], ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    adapter["protected_baseline"].update(
        commit=baseline,
        authority_kind="REMOTE_TRACKING_REF",
        authority_ref="refs/remotes/origin/main",
        policy_source_type="FIRST_MIGRATION_LEGACY_SOURCE",
        policy_source_path="skills/LEGACY_PROJECT_ADAPTER.json",
        policy_sha256=hashlib.sha256(policy).hexdigest(),
    )
    adapter["protected_paths"] = legacy["protected_paths"]
    (root / "skills" / "PROJECT_BASE_ADAPTER.json").write_text(
        json.dumps(adapter, indent=2) + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "adapter"], check=True)
    return root


def test_shared_identity_returns_the_committed_project_snapshot(tmp_path: Path) -> None:
    project = make_identity_project(tmp_path / "project")

    evidence = validate_project_identity(project, "demo-game", BASE_ROOT)

    assert evidence.project_id == "demo-game"
    assert evidence.repository == "owner/demo-game"
    assert evidence.engine == "Godot 4.7"
    assert evidence.root == project


def test_shared_identity_rejects_a_symlinked_root_component(tmp_path: Path) -> None:
    project = make_identity_project(tmp_path / "project")
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path, target_is_directory=True)

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_PATH_BLOCKED"):
        validate_project_identity(alias / project.name, "demo-game", BASE_ROOT)


def test_shared_identity_rejects_a_nested_directory_as_the_project_root(tmp_path: Path) -> None:
    project = make_identity_project(tmp_path / "project")
    nested = project / "nested"
    nested.mkdir()
    (nested / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (nested / ".asset-vault" / "library").mkdir(parents=True)
    (nested / "skills").mkdir()
    (nested / "skills" / "PROJECT_BASE_ADAPTER.json").write_bytes(
        (project / "skills" / "PROJECT_BASE_ADAPTER.json").read_bytes()
    )

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_PATH_BLOCKED"):
        validate_project_identity(nested, "demo-game", BASE_ROOT)
