from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess

import pytest

from base_tool_contracts import (
    StagingViolation,
    confined_staging_read_bytes,
    create_verified_run_directories,
    safe_staging_write_bytes,
    stable_staging_tree,
    staging_identity,
)


def make_vault(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True)


def test_staging_lifecycle_writes_and_reads_inside_verified_vault(tmp_path: Path) -> None:
    make_vault(tmp_path)
    run_dir, leaves = create_verified_run_directories(
        tmp_path,
        dynamic_components=("generated", "sprite", "hero", "run_20260815"),
        leaf_directories=("frames", "exports"),
    )
    payload = b"portable-staging-evidence"
    digest = hashlib.sha256(payload).hexdigest()

    with stable_staging_tree(tmp_path, run_dir, staging_identity(run_dir)) as stable:
        frames = stable.open_directory("frames", expected_identity=staging_identity(leaves[0]))
        written = safe_staging_write_bytes(frames, "frame-000.png", payload)

    assert written == leaves[0] / "frame-000.png" or written.name == "frame-000.png"
    assert confined_staging_read_bytes(tmp_path, leaves[0] / "frame-000.png", expected_sha256=digest) == payload


@pytest.mark.skipif(os.name != "nt", reason="Windows reparse-point portable boundary")
def test_windows_portable_staging_rejects_linked_generated_directory(tmp_path: Path) -> None:
    make_vault(tmp_path)
    library = tmp_path / ".asset-vault" / "library"
    outside = tmp_path.parent / f"{tmp_path.name}-outside"
    outside.mkdir()
    linked = library / "generated"
    try:
        linked.symlink_to(outside, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"Windows runner cannot create a directory symlink: {error}")

    with pytest.raises(StagingViolation, match="gitignored|link|reparse"):
        create_verified_run_directories(
            tmp_path,
            dynamic_components=("generated", "sprite", "hero", "run_20260815"),
            leaf_directories=("frames",),
        )

    assert not (outside / "sprite").exists()
