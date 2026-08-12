from pathlib import Path

import pytest

from sprite_animation_studio.paths import PathViolation, create_run_paths, resolve_project_path


def test_resolve_project_path_rejects_parent_escape(tmp_path: Path) -> None:
    with pytest.raises(PathViolation, match="escapes project root"):
        resolve_project_path(tmp_path, "../Base/secret.txt")


def test_create_run_paths_stays_under_project_root(tmp_path: Path) -> None:
    paths = create_run_paths(tmp_path, "knight", "attack_heavy", "run-001")

    assert paths.run_dir == tmp_path / "art" / "animation-runs" / "knight" / "run-001"
    assert paths.run_dir.is_relative_to(tmp_path)


def test_create_run_paths_honors_the_requested_project_relative_output_root(tmp_path: Path) -> None:
    paths = create_run_paths(tmp_path, "knight", "attack_heavy", "run-001", output_root="art/derived/knight")

    assert paths.run_dir == tmp_path / "art" / "derived" / "knight" / "run-001"
