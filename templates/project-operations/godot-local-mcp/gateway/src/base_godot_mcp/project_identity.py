from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path


class ProjectIdentityError(ValueError):
    """Project identity validation error with a stable code."""


@dataclass(frozen=True, slots=True)
class ProjectIdentity:
    normalized_root: str
    normalized_root_sha256: str
    project_file_sha256: str
    fingerprint: str

    @classmethod
    def from_root(cls, root: str | Path) -> "ProjectIdentity":
        resolved = Path(root).expanduser().resolve(strict=True)
        project_file = resolved / "project.godot"
        if not project_file.is_file():
            raise ProjectIdentityError("PROJECT_GODOT_NOT_FOUND")
        normalized_root = os.path.normcase(str(resolved))
        root_sha = hashlib.sha256(normalized_root.encode("utf-8")).hexdigest()
        project_sha = hashlib.sha256(project_file.read_bytes()).hexdigest()
        fingerprint = hashlib.sha256(
            f"{normalized_root}\0{project_sha}".encode("utf-8")
        ).hexdigest()
        return cls(
            normalized_root=normalized_root,
            normalized_root_sha256=root_sha,
            project_file_sha256=project_sha,
            fingerprint=fingerprint,
        )

    def public_summary(self) -> dict[str, str]:
        return {
            "project_fingerprint": self.fingerprint,
            "normalized_project_path_sha256": self.normalized_root_sha256,
            "project_godot_sha256": self.project_file_sha256,
        }
