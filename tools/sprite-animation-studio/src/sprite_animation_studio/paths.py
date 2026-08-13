"""Project-confined paths for sprite animation runs."""

from dataclasses import dataclass
from pathlib import Path

from base_tool_contracts import StagingViolation, assert_verified_staging_path, create_verified_run_directories, stable_staging_tree, staging_identity


class PathViolation(ValueError):
    """Raised when a caller attempts to leave the configured project root."""


@dataclass(frozen=True)
class RunPaths:
    run_dir: Path
    frames_dir: Path
    exports_dir: Path
    identity: tuple[int, int]
    frames_identity: tuple[int, int]
    exports_identity: tuple[int, int]


def resolve_project_path(project_root: Path, candidate: str) -> Path:
    root = project_root.resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise PathViolation(f"path escapes project root: {candidate}")
    return target


def create_run_paths(project_root: Path, asset_id: str, action_name: str, run_id: str) -> RunPaths:
    try:
        run_dir, leaves = create_verified_run_directories(
            project_root,
            dynamic_components=("generated", "sprite-animation-studio", asset_id, action_name, run_id),
            leaf_directories=("frames", "exports"),
        )
    except StagingViolation as error:
        raise PathViolation(str(error)) from error
    return RunPaths(
        run_dir=run_dir,
        frames_dir=leaves[0],
        exports_dir=leaves[1],
        identity=staging_identity(run_dir),
        frames_identity=staging_identity(leaves[0]),
        exports_identity=staging_identity(leaves[1]),
    )


def stable_run_tree(project_root: Path, paths: RunPaths):
    return stable_staging_tree(project_root, paths.run_dir, paths.identity)


def revalidate_run_paths(project_root: Path, paths: RunPaths) -> None:
    for path in (paths.run_dir, paths.frames_dir, paths.exports_dir):
        try:
            assert_verified_staging_path(project_root, path)
        except StagingViolation as error:
            raise PathViolation(str(error)) from error
