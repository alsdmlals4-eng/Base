import json
from pathlib import Path
import subprocess

import pytest

from tool_hub.projects import ProjectBindingError, ProjectLocator


BASE_ROOT = Path(__file__).resolve().parents[3]


def make_project(
    root: Path,
    project_id: str = "demo-game",
    *,
    schema_version: int = 2,
    partial_adapter: bool = False,
) -> Path:
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True)
    adapter = json.loads(
        (BASE_ROOT / "templates" / "project-operations" / "PROJECT_BASE_ADAPTER_V2.json").read_text(encoding="utf-8")
    )
    adapter["schema_version"] = schema_version
    adapter["project"] = {
        "project_id": project_id,
        "repository": f"owner/{project_id}",
        "engine": "Godot 4.7",
        "root": ".",
    }
    if partial_adapter:
        adapter = {
            "schema_version": schema_version,
            "artifact_role": "PROJECT_BASE_ADAPTER",
            "project": adapter["project"],
        }
    (root / "skills").mkdir()
    (root / "skills" / "PROJECT_BASE_ADAPTER.json").write_text(
        json.dumps(adapter), encoding="utf-8"
    )
    return root


def test_locator_registers_exact_v2_project_and_redacts_root(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces")
    locator = ProjectLocator(tmp_path / "machine-projects.json")

    binding = locator.register(project)
    public = locator.public_projects()

    assert binding.project_id == "demo-game"
    assert binding.root == project.resolve()
    assert public == [{"project_id": "demo-game", "display_name": "demo-game", "state": "READY"}]
    assert str(project.resolve()) not in json.dumps(public)


def test_locator_reloads_and_revalidates_fingerprint(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    config = tmp_path / "machine-projects.json"
    ProjectLocator(config).register(project)

    assert ProjectLocator(config).resolve("demo-game").root == project.resolve()


def test_locator_rejects_v1_and_invalid_project_identity(tmp_path: Path) -> None:
    with pytest.raises(ProjectBindingError, match="v2"):
        ProjectLocator(tmp_path / "one.json").register(
            make_project(tmp_path / "v1", schema_version=1)
        )
    with pytest.raises(ProjectBindingError, match="project_id"):
        ProjectLocator(tmp_path / "two.json").register(
            make_project(tmp_path / "invalid", project_id="Invalid ID")
        )


def test_locator_rejects_partial_document_that_only_claims_v2(tmp_path: Path) -> None:
    with pytest.raises(ProjectBindingError, match="schema"):
        ProjectLocator(tmp_path / "projects.json").register(
            make_project(tmp_path / "partial", partial_adapter=True)
        )


def test_locator_rejects_non_git_or_unignored_vault(tmp_path: Path) -> None:
    non_git = tmp_path / "non-git"
    non_git.mkdir()
    with pytest.raises(ProjectBindingError, match="Git worktree"):
        ProjectLocator(tmp_path / "one.json").register(non_git)

    project = make_project(tmp_path / "tracked")
    (project / ".gitignore").write_text("", encoding="utf-8")
    with pytest.raises(ProjectBindingError, match="gitignored"):
        ProjectLocator(tmp_path / "two.json").register(project)
