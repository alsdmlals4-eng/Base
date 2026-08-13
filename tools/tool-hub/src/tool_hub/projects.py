"""Machine-local project locator with exact v2 adapter identity."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any

from jsonschema import Draft202012Validator


class ProjectBindingError(ValueError):
    pass


_PROJECT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _fingerprint(root: Path, adapter_bytes: bytes) -> str:
    stat = root.stat()
    material = f"{root}:{stat.st_dev}:{stat.st_ino}:".encode() + hashlib.sha256(adapter_bytes).digest()
    return hashlib.sha256(material).hexdigest()


@dataclass(frozen=True)
class ProjectBinding:
    project_id: str
    root: Path
    repository: str
    engine: str
    fingerprint: str

    def public_view(self) -> dict[str, str]:
        return {"project_id": self.project_id, "display_name": self.project_id, "state": "READY"}


class ProjectLocator:
    def __init__(self, config_path: Path, *, adapter_schema: Path | None = None) -> None:
        self.config_path = config_path
        self.adapter_schema = adapter_schema or Path(__file__).resolve().parents[4] / "schemas" / "project-base-adapter-v2.schema.json"

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

    def _inspect(self, root_value: Path) -> ProjectBinding:
        root = root_value.resolve()
        top = _git(root, "rev-parse", "--show-toplevel")
        if top.returncode != 0 or not top.stdout.strip() or Path(top.stdout.strip()).resolve() != root:
            raise ProjectBindingError("selected root must be the exact Git worktree root")
        adapter_path = root / "skills" / "PROJECT_BASE_ADAPTER.json"
        try:
            adapter_bytes = adapter_path.read_bytes()
            adapter = json.loads(adapter_bytes)
        except (OSError, json.JSONDecodeError) as error:
            raise ProjectBindingError("PROJECT_BASE_ADAPTER v2 is required") from error
        if not isinstance(adapter, dict) or adapter.get("schema_version") != 2 or adapter.get("artifact_role") != "PROJECT_BASE_ADAPTER":
            raise ProjectBindingError("PROJECT_BASE_ADAPTER v2 is required")
        try:
            schema = json.loads(self.adapter_schema.read_text(encoding="utf-8"))
            validation_errors = sorted(Draft202012Validator(schema).iter_errors(adapter), key=lambda item: list(item.absolute_path))
        except (OSError, json.JSONDecodeError) as error:
            raise ProjectBindingError("PROJECT_BASE_ADAPTER v2 schema owner is unreadable") from error
        if validation_errors:
            if any(list(error.absolute_path) == ["project", "project_id"] for error in validation_errors):
                raise ProjectBindingError("adapter project_id must be canonical kebab-case")
            raise ProjectBindingError("PROJECT_BASE_ADAPTER v2 schema validation failed")
        project = adapter.get("project")
        if not isinstance(project, dict):
            raise ProjectBindingError("adapter project identity is missing")
        project_id = project.get("project_id")
        if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
            raise ProjectBindingError("adapter project_id must be canonical kebab-case")
        if project.get("root") != ".":
            raise ProjectBindingError("adapter project root must be exact repository root")
        repository = project.get("repository")
        engine = project.get("engine")
        if not isinstance(repository, str) or not repository or not isinstance(engine, str) or not engine:
            raise ProjectBindingError("adapter repository and engine are required")
        vault = root / ".asset-vault" / "library"
        if not vault.is_dir() or vault.is_symlink():
            raise ProjectBindingError("project Asset Vault library must exist")
        ignored = _git(root, "check-ignore", "-q", "--no-index", "--", ".asset-vault/library/.hub-probe")
        if ignored.returncode != 0:
            raise ProjectBindingError("project Asset Vault must be gitignored by the project")
        return ProjectBinding(project_id, root, repository, engine, _fingerprint(root, adapter_bytes))

    def register(self, project_root: Path) -> ProjectBinding:
        binding = self._inspect(project_root)
        config = self._read_config()
        projects: dict[str, Any] = config["projects"]
        projects[binding.project_id] = {
            "project_root": str(binding.root),
            "fingerprint": binding.fingerprint,
        }
        self._write_config(config)
        return binding

    def resolve(self, project_id: str) -> ProjectBinding:
        config = self._read_config()
        record = config["projects"].get(project_id)
        if not isinstance(record, dict) or not isinstance(record.get("project_root"), str):
            raise ProjectBindingError("registered project was not found")
        binding = self._inspect(Path(record["project_root"]))
        if binding.project_id != project_id or binding.fingerprint != record.get("fingerprint"):
            raise ProjectBindingError("registered project identity drifted")
        return binding

    def public_projects(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for project_id in sorted(self._read_config()["projects"]):
            try:
                result.append(self.resolve(project_id).public_view())
            except ProjectBindingError:
                result.append({"project_id": project_id, "display_name": project_id, "state": "IDENTITY_DRIFT"})
        return result
