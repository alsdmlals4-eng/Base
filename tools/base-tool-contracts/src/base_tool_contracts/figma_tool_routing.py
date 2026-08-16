"""Canonical tool-specific descendant routes inside reviewed project Figma targets."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .figma_routing import DeliveryBlockedError, ProjectFigmaRegistry
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


_CANONICAL_REGISTRY = Path("docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json")
_CANONICAL_ROUTE_DESTINATION_NAMES = {
    "character_expression_runs": "Expression Runs",
    "sprite_action_runs": "Sprite Action Runs",
    "effect_runs": "Effect Runs",
}
RouteStatus = Literal["REGISTERED_NO_MUTATION", "READY_FOR_DELIVERY", "ARCHIVED"]
NodeType = Literal["FRAME"]


def _descriptor_reads_supported() -> bool:
    return bool(getattr(os, "O_NOFOLLOW", 0)) and os.name != "nt"


def _read_registry_file(path: Path) -> bytes:
    reader = read_regular_nofollow if _descriptor_reads_supported() else read_regular_portable_nofollow
    raw, _ = reader(path)
    return raw


class _RouteEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    tool_route_id: str = Field(pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    figma_file_key: str = Field(pattern=r"^[A-Za-z0-9]+$")
    parent_node_id: str = Field(pattern=r"^\d+:\d+$")
    parent_node_type: NodeType
    destination_node_id: str = Field(pattern=r"^\d+:\d+$")
    destination_node_type: NodeType
    destination_name: str = Field(min_length=1, max_length=120)
    project_marker_node_id: str = Field(pattern=r"^\d+:\d+$")
    project_marker_node_type: NodeType
    project_marker_name: str = Field(min_length=1, max_length=180)
    delivery_status: RouteStatus


class _RouteDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal[1]
    purpose: str | None = None
    entries: list[_RouteEntry] = Field(min_length=1)


@dataclass(frozen=True)
class ProjectFigmaToolRoute:
    project_id: str
    tool_route_id: str
    figma_file_key: str
    parent_node_id: str
    parent_node_type: str
    destination_node_id: str
    destination_node_type: str
    destination_name: str
    project_marker_node_id: str
    project_marker_node_type: str
    project_marker_name: str


class ProjectFigmaToolRouteRegistry:
    """Reviewed descendant-node routing; never a mutation client or credential store."""

    def __init__(self, document: _RouteDocument, *, config_sha256: str, source_path: Path) -> None:
        keys = [(entry.project_id, entry.tool_route_id) for entry in document.entries]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate project/tool route in Figma tool-route registry")
        for entry in document.entries:
            if entry.parent_node_id == entry.destination_node_id:
                raise ValueError("Figma tool-route parent and destination node IDs must differ")
            if entry.project_marker_node_id in {
                entry.parent_node_id,
                entry.destination_node_id,
            }:
                raise ValueError("Figma tool-route project marker node must differ from route nodes")
            expected_marker = f"Base Tool Hub Route · {entry.project_id}"
            if entry.project_marker_name != expected_marker:
                raise ValueError("Figma tool-route project marker must match project_id")
            expected_destination = _CANONICAL_ROUTE_DESTINATION_NAMES.get(entry.tool_route_id)
            if expected_destination is None:
                raise ValueError("Figma tool-route ID is not a reviewed canonical route")
            if entry.destination_name != expected_destination:
                raise ValueError("Figma tool-route destination name must match route ID")
        self._document = document
        self._entries = {
            (entry.project_id, entry.tool_route_id): entry for entry in document.entries
        }
        self.config_sha256 = config_sha256
        self.source_path = source_path

    @classmethod
    def load(cls, path: Path) -> "ProjectFigmaToolRouteRegistry":
        try:
            raw = _read_registry_file(path)
            payload = json.loads(raw.decode("utf-8"))
        except (OSError, TrustedFileError) as error:
            raise ValueError("Figma tool-route registry is unavailable or crosses a link") from error
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Figma tool-route registry is invalid JSON") from error
        return cls(
            _RouteDocument.model_validate(payload),
            config_sha256=hashlib.sha256(raw).hexdigest(),
            source_path=Path(os.path.abspath(path)),
        )

    def route_pairs(self) -> set[tuple[str, str]]:
        return {
            (entry.project_id, entry.tool_route_id)
            for entry in self._document.entries
            if entry.delivery_status != "ARCHIVED"
        }

    def assert_canonical(self, base_root: Path) -> None:
        root = Path(os.path.abspath(base_root))
        expected = root / _CANONICAL_REGISTRY
        if self.source_path != expected:
            raise DeliveryBlockedError("Figma tool-route registry is not the canonical Base registry")
        try:
            if _descriptor_reads_supported():
                root_fd = open_directory_nofollow(root)
                try:
                    current, _ = read_regular_at(root_fd, _CANONICAL_REGISTRY)
                    committed = run_trusted_git(
                        root_fd,
                        "show",
                        f"HEAD:{_CANONICAL_REGISTRY.as_posix()}",
                    )
                finally:
                    os.close(root_fd)
            else:
                current, _ = read_regular_portable_nofollow(expected)
                committed = run_portable_git(
                    root,
                    "show",
                    f"HEAD:{_CANONICAL_REGISTRY.as_posix()}",
                )
        except TrustedFileError as error:
            raise DeliveryBlockedError("canonical Figma tool-route proof is unavailable") from error
        if (
            committed.returncode != 0
            or normalized_line_endings(current) != normalized_line_endings(committed.stdout)
        ):
            raise DeliveryBlockedError("canonical Figma tool-route registry must match committed Base bytes")
        if hashlib.sha256(current).hexdigest() != self.config_sha256:
            raise DeliveryBlockedError("canonical Figma tool-route registry changed after loading")

    def assert_unchanged(self) -> None:
        try:
            raw = _read_registry_file(self.source_path)
        except (OSError, TrustedFileError) as error:
            raise DeliveryBlockedError("Figma tool-route registry is unavailable during revalidation") from error
        if hashlib.sha256(raw).hexdigest() != self.config_sha256:
            raise DeliveryBlockedError("Figma tool-route registry changed after loading")

    def resolve_ready_route(
        self,
        project_id: str,
        tool_route_id: str,
        project_registry: ProjectFigmaRegistry,
    ) -> ProjectFigmaToolRoute:
        try:
            target = project_registry.resolve_ready_target(project_id)
        except DeliveryBlockedError as error:
            raise DeliveryBlockedError("project is not ready for Figma tool routing") from error

        entry = self._entries.get((project_id, tool_route_id))
        if entry is None:
            raise DeliveryBlockedError("tool route is not registered for the project")
        if entry.delivery_status != "READY_FOR_DELIVERY":
            raise DeliveryBlockedError(
                f"tool route is blocked by delivery_status {entry.delivery_status}"
            )
        if entry.figma_file_key != target.figma_file_key:
            raise DeliveryBlockedError("tool route Figma file does not match the bound project")
        if entry.parent_node_id != target.generation_area_node_id:
            raise DeliveryBlockedError("tool route parent does not match the bound project generation area")
        expected_destination = _CANONICAL_ROUTE_DESTINATION_NAMES.get(entry.tool_route_id)
        if expected_destination is None or entry.destination_name != expected_destination:
            raise DeliveryBlockedError("tool route destination name does not match reviewed route identity")
        if not re.fullmatch(r"\d+:\d+", entry.destination_node_id):
            raise DeliveryBlockedError("tool route destination node ID is invalid")

        return ProjectFigmaToolRoute(
            project_id=entry.project_id,
            tool_route_id=entry.tool_route_id,
            figma_file_key=entry.figma_file_key,
            parent_node_id=entry.parent_node_id,
            parent_node_type=entry.parent_node_type,
            destination_node_id=entry.destination_node_id,
            destination_node_type=entry.destination_node_type,
            destination_name=entry.destination_name,
            project_marker_node_id=entry.project_marker_node_id,
            project_marker_node_type=entry.project_marker_node_type,
            project_marker_name=entry.project_marker_name,
        )
