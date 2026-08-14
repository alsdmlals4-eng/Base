"""Single validated owner for project-bound Figma routing data."""

from __future__ import annotations

import json
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib.parse import parse_qs, urlsplit

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .trusted_files import (
    TrustedFileError,
    normalized_line_endings,
    open_directory_nofollow,
    read_regular_at,
    read_regular_nofollow,
    read_regular_portable_nofollow,
    run_portable_git,
    run_trusted_git,
)


_CANONICAL_REGISTRY = Path("docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json")


def _descriptor_reads_supported() -> bool:
    return bool(getattr(os, "O_NOFOLLOW", 0)) and os.name != "nt"


def _read_registry_file(path: Path) -> bytes:
    reader = read_regular_nofollow if _descriptor_reads_supported() else read_regular_portable_nofollow
    raw, _ = reader(path)
    return raw


class DeliveryBlockedError(RuntimeError):
    """Raised when a project Figma destination must not be used."""


DeliveryStatus = Literal["REGISTERED_NO_MUTATION", "READY_FOR_DELIVERY", "ARCHIVED"]


class _RegistryEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    display_name: str = Field(min_length=1)
    repository_url: HttpUrl
    figma_file_key: str = Field(pattern=r"^[A-Za-z0-9]+$")
    figma_url: HttpUrl
    delivery_status: DeliveryStatus
    delivery_page_node_id: str | None = None
    generation_area_node_id: str | None = None


class _RegistryDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal[1]
    purpose: str | None = None
    default_delivery_page: str = Field(min_length=1)
    default_generation_area: str = Field(min_length=1)
    entries: list[_RegistryEntry] = Field(min_length=1)


@dataclass(frozen=True)
class ProjectFigmaTarget:
    project_id: str
    display_name: str
    figma_file_key: str
    figma_url: str
    delivery_page: str
    generation_area: str
    delivery_page_node_id: str
    generation_area_node_id: str


@dataclass(frozen=True)
class ProjectRepositoryPointer:
    project_id: str
    display_name: str
    repository_url: str
    repository_name: str
    routing_state: str


class ProjectFigmaRegistry:
    """A routing registry, never a credential store or mutation client."""

    def __init__(self, document: _RegistryDocument, *, config_sha256: str, source_path: Path) -> None:
        project_ids = [entry.project_id for entry in document.entries]
        if len(project_ids) != len(set(project_ids)):
            raise ValueError("duplicate project_id in Figma target registry")
        for entry in document.entries:
            repository = urlsplit(str(entry.repository_url))
            if (
                repository.scheme != "https"
                or repository.hostname != "github.com"
                or repository.username
                or repository.password
                or repository.port
                or repository.query
                or repository.fragment
                or not re.fullmatch(r"/[^/]+/[^/]+\.git", repository.path)
            ):
                raise ValueError(
                    f"GitHub repository URL for project_id {entry.project_id!r} is invalid"
                )
            if entry.figma_url.scheme != "https" or entry.figma_url.host != "www.figma.com":
                raise ValueError(f"Figma URL for project_id {entry.project_id!r} must use https://www.figma.com")
            parts = entry.figma_url.path.split("/")
            if len(parts) < 3 or parts[1] != "design" or parts[2] != entry.figma_file_key:
                raise ValueError(
                    f"Figma URL file key does not match figma_file_key for project_id {entry.project_id!r}"
                )
            node_ids = (entry.delivery_page_node_id, entry.generation_area_node_id)
            if any(node_ids) and not all(node_ids):
                raise ValueError(f"Figma page and generation area node IDs must be supplied together for {entry.project_id!r}")
            if all(node_ids):
                if any(not re.fullmatch(r"\d+:\d+", node_id or "") for node_id in node_ids):
                    raise ValueError(f"Figma node IDs for project_id {entry.project_id!r} must use canonical form")
                if entry.delivery_page_node_id == entry.generation_area_node_id:
                    raise ValueError(f"Figma delivery page and generation area node IDs must differ for project_id {entry.project_id!r}")
        self._document = document
        self._entries = {entry.project_id: entry for entry in document.entries}
        repository_urls = [str(entry.repository_url).casefold() for entry in document.entries]
        if len(repository_urls) != len(set(repository_urls)):
            raise ValueError("duplicate repository_url in Figma target registry")
        self.config_sha256 = config_sha256
        self.source_path = source_path

    @classmethod
    def load(cls, path: Path) -> "ProjectFigmaRegistry":
        try:
            raw = _read_registry_file(path)
            payload = json.loads(raw.decode("utf-8"))
        except (OSError, TrustedFileError) as error:
            raise ValueError("Figma target registry is unavailable or crosses a symlink") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Figma target registry is invalid JSON") from error
        return cls(
            _RegistryDocument.model_validate(payload),
            config_sha256=hashlib.sha256(raw).hexdigest(),
            source_path=Path(os.path.abspath(path)),
        )

    def assert_canonical(self, base_root: Path) -> None:
        """Prove this is Base's exact committed Figma routing authority."""
        root = Path(os.path.abspath(base_root))
        expected = root / _CANONICAL_REGISTRY
        if self.source_path != expected:
            raise DeliveryBlockedError("Figma target registry is not the canonical Base registry")
        try:
            if _descriptor_reads_supported():
                root_fd = open_directory_nofollow(root)
                try:
                    current, _ = read_regular_at(root_fd, _CANONICAL_REGISTRY)
                    committed = run_trusted_git(root_fd, "show", f"HEAD:{_CANONICAL_REGISTRY.as_posix()}")
                finally:
                    os.close(root_fd)
            else:
                current, _ = read_regular_portable_nofollow(expected)
                committed = run_portable_git(root, "show", f"HEAD:{_CANONICAL_REGISTRY.as_posix()}")
        except TrustedFileError as error:
            raise DeliveryBlockedError("canonical Figma registry proof is unavailable") from error
        if committed.returncode != 0 or normalized_line_endings(current) != normalized_line_endings(committed.stdout):
            raise DeliveryBlockedError("canonical Figma registry must match its committed Base blob")
        if hashlib.sha256(current).hexdigest() != self.config_sha256:
            raise DeliveryBlockedError("canonical Figma registry changed after loading")

    def assert_unchanged(self) -> None:
        try:
            raw = _read_registry_file(self.source_path)
            current = hashlib.sha256(raw).hexdigest()
        except (OSError, TrustedFileError) as error:
            raise DeliveryBlockedError("Figma target registry is unavailable during delivery revalidation") from error
        if current != self.config_sha256:
            raise DeliveryBlockedError("Figma target registry changed after Studio startup")

    def routing_state(self, project_id: str) -> str:
        entry = self._entries.get(project_id)
        if entry is None:
            return "ROUTING_UNAVAILABLE"
        if entry.delivery_status == "ARCHIVED":
            return "ROUTING_ARCHIVED"
        if entry.delivery_status != "READY_FOR_DELIVERY":
            return "ROUTING_BLOCKED"
        if not entry.delivery_page_node_id or not entry.generation_area_node_id:
            return "ROUTING_BLOCKED"
        return "ROUTING_CONFIGURED"

    def registration_state(self, project_id: str) -> str:
        """Report routing registration without implying delivery readiness."""
        entry = self._entries.get(project_id)
        if entry is None:
            return "ROUTING_UNAVAILABLE"
        if entry.delivery_status == "ARCHIVED":
            return "ROUTING_ARCHIVED"
        if entry.delivery_status == "REGISTERED_NO_MUTATION":
            return "ROUTING_REGISTERED"
        if entry.delivery_page_node_id and entry.generation_area_node_id:
            return "ROUTING_CONFIGURED"
        return "ROUTING_BLOCKED"

    def public_projects(self) -> list[dict[str, str]]:
        """Return the human-facing project catalog without Figma target details."""
        return [
            {
                "project_id": entry.project_id,
                "display_name": entry.display_name,
                "repository_name": Path(urlsplit(str(entry.repository_url)).path).stem,
                "routing_state": self.registration_state(entry.project_id),
            }
            for entry in self._document.entries
            if entry.delivery_status != "ARCHIVED"
        ]

    def repository_pointer(self, project_id: str) -> ProjectRepositoryPointer:
        entry = self._entries.get(project_id)
        if entry is None or entry.delivery_status == "ARCHIVED":
            raise DeliveryBlockedError("project repository pointer is unavailable")
        repository_url = str(entry.repository_url)
        return ProjectRepositoryPointer(
            project_id=entry.project_id,
            display_name=entry.display_name,
            repository_url=repository_url,
            repository_name=Path(urlsplit(repository_url).path).stem,
            routing_state=self.registration_state(project_id),
        )

    def resolve_ready_target(self, project_id: str) -> ProjectFigmaTarget:
        entry = self._entries.get(project_id)
        if entry is None:
            raise DeliveryBlockedError(f"project_id {project_id!r} is not registered for Figma delivery")
        if entry.delivery_status != "READY_FOR_DELIVERY":
            raise DeliveryBlockedError(
                f"project_id {project_id!r} is blocked by delivery_status {entry.delivery_status}"
            )
        if not entry.delivery_page_node_id or not entry.generation_area_node_id:
            raise DeliveryBlockedError(f"project_id {project_id!r} has no configured Figma generation-area node")
        return ProjectFigmaTarget(
            project_id=entry.project_id,
            display_name=entry.display_name,
            figma_file_key=entry.figma_file_key,
            figma_url=str(entry.figma_url),
            delivery_page=self._document.default_delivery_page,
            generation_area=self._document.default_generation_area,
            delivery_page_node_id=entry.delivery_page_node_id,
            generation_area_node_id=entry.generation_area_node_id,
        )

    def validate_anchor_url(self, project_id: str, anchor_url: str) -> str:
        entry = self._entries.get(project_id)
        if entry is None:
            raise DeliveryBlockedError(f"project_id {project_id!r} is not registered for Figma routing")
        parsed = urlsplit(anchor_url)
        parts = parsed.path.split("/")
        if parsed.scheme != "https" or parsed.hostname != "www.figma.com":
            raise DeliveryBlockedError("anchor Figma URL must use https://www.figma.com")
        if len(parts) < 3 or parts[1] != "design" or parts[2] != entry.figma_file_key:
            raise DeliveryBlockedError("anchor Figma file must match the bound project")
        node_id = parse_qs(parsed.query).get("node-id", [""])[0].replace("-", ":")
        if not re.fullmatch(r"\d+:\d+", node_id):
            raise DeliveryBlockedError("anchor Figma node-id must use canonical numeric form")
        return node_id
