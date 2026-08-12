"""Project-owned approved-anchor evidence consumed by local generation tools."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Literal


class AnchorEvidenceError(ValueError):
    pass


class _Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["EXPORTED_SNAPSHOT", "FIGMA_CONNECTOR"]
    ref: str = Field(min_length=1)
    checked_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class _Entry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    source_path: str = Field(min_length=1)
    figma_node_url: HttpUrl
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    approval_state: Literal["APPROVED"]
    evidence: _Evidence


class _Document(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: Literal[1]
    entries: list[_Entry]


class ApprovedAnchorRegistry:
    def __init__(self, document: _Document, *, config_sha256: str, source_path: Path) -> None:
        keys = [(entry.project_id, entry.source_path) for entry in document.entries]
        if len(keys) != len(set(keys)):
            raise AnchorEvidenceError("duplicate approved-anchor project/source key")
        self._entries = {(entry.project_id, entry.source_path): entry for entry in document.entries}
        self.config_sha256 = config_sha256
        self.source_path = source_path

    @classmethod
    def load(cls, path: Path) -> "ApprovedAnchorRegistry":
        try:
            raw = path.read_bytes()
            payload = json.loads(raw.decode("utf-8"))
            document = _Document.model_validate(payload)
        except Exception as error:
            raise AnchorEvidenceError(f"approved-anchor registry is invalid: {path}") from error
        resolved = path.resolve()
        if path.is_symlink():
            raise AnchorEvidenceError("approved-anchor registry must not be a symlink")
        return cls(document, config_sha256=hashlib.sha256(raw).hexdigest(), source_path=resolved)

    def assert_project_owned(self, project_root: Path) -> None:
        root = project_root.resolve()
        if self.source_path != root and root not in self.source_path.parents:
            raise AnchorEvidenceError("approved-anchor registry must be stored inside the project workspace")
        relative = self.source_path.relative_to(root).as_posix()
        tracked = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
            capture_output=True,
            text=True,
            check=False,
        )
        if tracked.returncode != 0:
            raise AnchorEvidenceError("approved-anchor registry must be a tracked project-owned artifact")
        committed = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{relative}"],
            capture_output=True,
            check=False,
        )
        if committed.returncode != 0 or committed.stdout != self.source_path.read_bytes():
            raise AnchorEvidenceError("approved-anchor registry must exactly match its committed project blob")

    def assert_unchanged(self) -> None:
        try:
            current = hashlib.sha256(self.source_path.read_bytes()).hexdigest()
        except OSError as error:
            raise AnchorEvidenceError("approved-anchor registry is unavailable during revalidation") from error
        if current != self.config_sha256:
            raise AnchorEvidenceError("approved-anchor registry changed after Studio startup")

    def evidence(self, *, project_id: str, source_path: str, figma_node_url: str, source_bytes: bytes) -> dict[str, str]:
        """Return exact project-owned evidence after source, URL, and SHA verification."""
        state = self.verify(
            project_id=project_id,
            source_path=source_path,
            figma_node_url=figma_node_url,
            source_bytes=source_bytes,
        )
        entry = self._entries[(project_id, source_path)]
        return {
            "verification_state": state,
            "registry_sha256": self.config_sha256,
            "evidence_kind": entry.evidence.kind,
            "evidence_ref": entry.evidence.ref,
            "checked_at": entry.evidence.checked_at,
        }

    def verify(self, *, project_id: str, source_path: str, figma_node_url: str, source_bytes: bytes) -> str:
        entry = self._entries.get((project_id, source_path))
        if entry is None:
            raise AnchorEvidenceError("approved-anchor evidence is missing for the project source")
        if str(entry.figma_node_url) != figma_node_url:
            raise AnchorEvidenceError("approved-anchor Figma node URL does not match pinned evidence")
        if entry.source_sha256 != hashlib.sha256(source_bytes).hexdigest():
            raise AnchorEvidenceError("approved-anchor source SHA-256 does not match pinned evidence")
        return "ANCHOR_EVIDENCE_VERIFIED"
