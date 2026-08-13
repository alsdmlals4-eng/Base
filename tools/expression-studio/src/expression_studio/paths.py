"""Project-root-safe paths for expression studio outputs."""

from dataclasses import dataclass
from pathlib import Path

from base_tool_contracts import StagingViolation, assert_verified_staging_path, create_verified_run_directories, stable_staging_tree, staging_identity


@dataclass(frozen=True)
class RunPaths:
    run_dir: Path
    candidates_dir: Path
    exports_dir: Path
    identity: tuple[int, int]
    candidates_identity: tuple[int, int]
    exports_identity: tuple[int, int]


def resolve_project_path(project_root: Path, relative_path: str) -> Path:
    root = project_root.resolve()
    candidate = (root / relative_path).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("path must stay inside project_root")
    return candidate


def create_run_paths(project_root: Path, asset_id: str, run_id: str) -> RunPaths:
    try:
        run_dir, leaves = create_verified_run_directories(
            project_root,
            dynamic_components=("generated", "expression-studio", asset_id, run_id),
            leaf_directories=("candidates", "exports"),
        )
    except StagingViolation as error:
        raise ValueError(str(error)) from error
    return RunPaths(
        run_dir=run_dir,
        candidates_dir=leaves[0],
        exports_dir=leaves[1],
        identity=staging_identity(run_dir),
        candidates_identity=staging_identity(leaves[0]),
        exports_identity=staging_identity(leaves[1]),
    )


def stable_run_tree(project_root: Path, paths: RunPaths):
    return stable_staging_tree(project_root, paths.run_dir, paths.identity)


def revalidate_run_paths(project_root: Path, paths: RunPaths) -> None:
    for path in (paths.run_dir, paths.candidates_dir, paths.exports_dir):
        try:
            assert_verified_staging_path(project_root, path)
        except StagingViolation as error:
            raise ValueError(str(error)) from error
