"""Project-confined paths for sprite animation runs."""

from dataclasses import dataclass
from pathlib import Path


class PathViolation(ValueError):
    """Raised when a caller attempts to leave the configured project root."""


@dataclass(frozen=True)
class RunPaths:
    run_dir: Path
    frames_dir: Path
    exports_dir: Path


def resolve_project_path(project_root: Path, candidate: str) -> Path:
    """Resolve a relative user path without allowing it to escape ``project_root``."""
    root = project_root.resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise PathViolation(f"path escapes project root: {candidate}")
    return target


def create_run_paths(
    project_root: Path,
    asset_id: str,
    action_name: str,
    run_id: str,
    output_root: str | None = None,
) -> RunPaths:
    """Create the isolated workspace for one asset/action run beneath the project."""
    if not all(value and value.replace("-", "").replace("_", "").isalnum() for value in (asset_id, action_name, run_id)):
        raise PathViolation("run identifiers must contain only letters, numbers, hyphens, or underscores")

    relative_root = output_root or f"art/animation-runs/{asset_id}"
    run_dir = resolve_project_path(project_root, f"{relative_root.rstrip('/')}/{run_id}")
    frames_dir = run_dir / "frames"
    exports_dir = run_dir / "exports"
    frames_dir.mkdir(parents=True, exist_ok=True)
    exports_dir.mkdir(parents=True, exist_ok=True)
    return RunPaths(run_dir=run_dir, frames_dir=frames_dir, exports_dir=exports_dir)
