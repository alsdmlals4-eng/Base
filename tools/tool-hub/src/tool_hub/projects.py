"""Machine-local project locator with exact v2 adapter identity."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from base_tool_contracts import (
    AnchorEvidenceError,
    ApprovedAnchorRegistry,
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectIdentityError,
    validate_project_identity,
)

class ProjectBindingError(ValueError):
    pass


@dataclass(frozen=True)
class ProjectBinding:
    project_id: str
    root: Path
    repository: str
    engine: str
    fingerprint: str
    adapter_sha256: str = ""
    protected_paths: tuple[str, ...] = ()
    validator_sha256: str = ""

    def public_view(self) -> dict[str, str]:
        return {"project_id": self.project_id, "display_name": self.project_id, "state": "READY"}


class ProjectLocator:
    def __init__(self, config_path: Path, *, adapter_schema: Path | None = None) -> None:
        self.config_path = config_path
        self.base_root = Path(__file__).resolve().parents[4]
        self.adapter_schema = adapter_schema or self.base_root / "schemas" / "project-base-adapter-v2.schema.json"

    def _read_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {"schema_version": 1, "projects": {}}
        try:
            value = json.loads(self.config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ProjectBindingError("machine project locator is unreadable") from error
        if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("projects"), dict):
            raise ProjectBindingError("machine project locator schema is invalid")
        return value

    def _write_config(self, value: dict[str, Any]) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temp_name = tempfile.mkstemp(prefix=".projects-", suffix=".json", dir=self.config_path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.config_path)
        finally:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass

    def _inspect(self, root_value: Path, expected_project_id: str | None = None) -> ProjectBinding:
        try:
            evidence = validate_project_identity(root_value, expected_project_id, self.base_root)
        except ProjectIdentityError as error:
            raise ProjectBindingError(str(error)) from error
        return ProjectBinding(
            evidence.project_id,
            evidence.root,
            evidence.repository,
            evidence.engine,
            evidence.root_fingerprint,
            evidence.adapter_sha256,
            evidence.protected_paths,
            evidence.validator_sha256,
        )

    def register(
        self,
        project_root: Path,
        expected_project_id: str,
    ) -> ProjectBinding:
        binding = self._inspect(project_root, expected_project_id)
        config = self._read_config()
        projects: dict[str, Any] = config["projects"]
        projects[binding.project_id] = {
            "project_root": str(binding.root),
            "fingerprint": binding.fingerprint,
        }
        self._write_config(config)
        return binding

    def inspect(self, project_root: Path, expected_project_id: str) -> ProjectBinding:
        """Validate a candidate without recording it in the machine locator."""
        return self._inspect(project_root, expected_project_id)

    def resolve(self, project_id: str) -> ProjectBinding:
        config = self._read_config()
        record = config["projects"].get(project_id)
        if not isinstance(record, dict) or not isinstance(record.get("project_root"), str):
            raise ProjectBindingError("registered project was not found")
        binding = self._inspect(Path(record["project_root"]), project_id)
        if binding.project_id != project_id or binding.fingerprint != record.get("fingerprint"):
            raise ProjectBindingError("registered project identity drifted")
        return binding

    def preflight_visual(
        self,
        project_id: str,
        figma_registry: ProjectFigmaRegistry,
        anchor_registry: ApprovedAnchorRegistry,
    ) -> ProjectBinding:
        """Resolve a project only when Base's canonical visual route is registered."""
        try:
            figma_registry.assert_canonical(self.base_root)
        except DeliveryBlockedError as error:
            raise ProjectBindingError("PROJECT_FIGMA_ROUTING_UNAVAILABLE") from error
        state = figma_registry.registration_state(project_id)
        if state not in {"ROUTING_REGISTERED", "ROUTING_CONFIGURED"}:
            raise ProjectBindingError("PROJECT_FIGMA_ROUTING_UNAVAILABLE")
        binding = self.resolve(project_id)
        try:
            anchor_registry.assert_project_owned(binding.root)
        except AnchorEvidenceError as error:
            raise ProjectBindingError("PROJECT_ANCHOR_EVIDENCE_UNAVAILABLE") from error
        return binding

    def public_projects(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for project_id in sorted(self._read_config()["projects"]):
            try:
                result.append(self.resolve(project_id).public_view())
            except ProjectBindingError:
                result.append({"project_id": project_id, "display_name": project_id, "state": "IDENTITY_DRIFT"})
        return result
