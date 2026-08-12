from pathlib import Path
import subprocess
import json

import pytest

from sprite_animation_studio.paths import PathViolation, create_run_paths, resolve_project_path


def test_resolve_project_path_rejects_parent_escape(tmp_path: Path) -> None:
    with pytest.raises(PathViolation, match="escapes project root"):
        resolve_project_path(tmp_path, "../Base/secret.txt")


def test_create_run_paths_stays_under_project_root(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".asset-vault" / "library").mkdir(parents=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    paths = create_run_paths(tmp_path, "knight", "attack_heavy", "run-001")

    assert paths.run_dir == tmp_path / ".asset-vault" / "library" / "generated" / "sprite-animation-studio" / "knight" / "attack_heavy" / "run-001"
    assert paths.run_dir.is_relative_to(tmp_path)


def test_create_run_paths_rejects_a_missing_asset_vault(tmp_path: Path) -> None:
    with pytest.raises(PathViolation, match="asset vault"):
        create_run_paths(tmp_path, "knight", "attack_heavy", "run-001")


def test_create_run_paths_rejects_dynamic_symlinks_and_effective_ignore_negation(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    library = tmp_path / ".asset-vault" / "library"
    tool_root = library / "generated" / "sprite-animation-studio"
    tool_root.mkdir(parents=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    outside = tmp_path.parent / f"{tmp_path.name}-outside-sprite"
    outside.mkdir()
    (tool_root / "knight").symlink_to(outside, target_is_directory=True)

    with pytest.raises(PathViolation, match="symlink|vault"):
        create_run_paths(tmp_path, "knight", "attack_heavy", "run-001")
    assert list(outside.iterdir()) == []

    (tool_root / "knight").unlink()
    (tmp_path / ".gitignore").write_text(".asset-vault/\n!.asset-vault/\n", encoding="utf-8")
    with pytest.raises(PathViolation, match="gitignored"):
        create_run_paths(tmp_path, "knight", "attack_heavy", "run-002")


def test_create_run_paths_rejects_tracked_global_only_and_protected_vault(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    library = tmp_path / ".asset-vault" / "library"
    library.mkdir(parents=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    tracked = library / "tracked.txt"
    tracked.write_text("tracked", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-f", ".asset-vault/library/tracked.txt"], check=True)
    with pytest.raises(PathViolation, match="tracked"):
        create_run_paths(tmp_path, "knight", "attack", "run-001")

    subprocess.run(["git", "-C", str(tmp_path), "rm", "--cached", "-q", ".asset-vault/library/tracked.txt"], check=True)
    (tmp_path / ".gitignore").write_text("", encoding="utf-8")
    (tmp_path / ".git" / "info" / "exclude").write_text(".asset-vault/\n", encoding="utf-8")
    with pytest.raises(PathViolation, match="project .gitignore"):
        create_run_paths(tmp_path, "knight", "attack", "run-002")

    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    adapter = tmp_path / "skills" / "PROJECT_BASE_ADAPTER.json"
    adapter.parent.mkdir()
    adapter.write_text(json.dumps({"protected_paths": [".asset-vault/**"]}), encoding="utf-8")
    with pytest.raises(PathViolation, match="protected"):
        create_run_paths(tmp_path, "knight", "attack", "run-003")
