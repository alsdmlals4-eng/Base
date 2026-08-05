import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from jsonschema import Draft202012Validator


BehaviorKind = Literal[
    "PYTHON_UNITTEST_MODULE",
    "PYTHON_PYTEST_PATH",
    "GODOT_SCRIPT",
]

_ZERO_SHA = "0" * 40
_TARGET_PATTERNS = {
    "PYTHON_UNITTEST_MODULE": re.compile(r"^tests(?:\.[A-Za-z_][A-Za-z0-9_]*)+$"),
    "PYTHON_PYTEST_PATH": re.compile(
        r"^tests/[A-Za-z0-9_./-]+\.py(?:::[A-Za-z_][A-Za-z0-9_]*)?$"
    ),
    "GODOT_SCRIPT": re.compile(r"^res://tests/[A-Za-z0-9_./-]+\.gd$"),
}


@dataclass(frozen=True)
class BehaviorCheck:
    kind: BehaviorKind
    target: str
    timeout_seconds: int


@dataclass(frozen=True)
class ProjectPilotDescriptor:
    repository: str
    project_id: str
    base_pilot_commit: str
    project_state: str
    godot_version: str
    godot_archive_sha256: str
    project_file: str | None
    main_scene_source: str
    legacy_editor_plugins: tuple[str, ...]
    legacy_autoloads: tuple[str, ...]
    scratch_scene_path: str
    behavior_checks: tuple[BehaviorCheck, ...]
    expected_platform: str

    @property
    def is_runtime_project(self) -> bool:
        return self.project_state == "EXISTING_GODOT_PROJECT"


def _default_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "schemas/godot-project-pilot-v1.schema.json"


def _format_error(error: object) -> str:
    path = ".".join(str(item) for item in getattr(error, "absolute_path", ()))
    message = str(getattr(error, "message", error))
    return f"{path or '<root>'}: {message}"


def load_descriptor(
    path: Path,
    schema_path: Path | None = None,
) -> ProjectPilotDescriptor:
    descriptor_path = Path(path).resolve()
    try:
        payload = json.loads(descriptor_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"DESCRIPTOR_JSON_INVALID: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("DESCRIPTOR_SCHEMA_INVALID: <root>: expected object")

    resolved_schema = Path(schema_path or _default_schema_path()).resolve()
    try:
        schema = json.loads(resolved_schema.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"DESCRIPTOR_SCHEMA_UNAVAILABLE: {exc}") from exc

    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda item: tuple(str(value) for value in item.absolute_path),
    )
    if errors:
        joined = "; ".join(_format_error(error) for error in errors)
        raise ValueError(f"DESCRIPTOR_SCHEMA_INVALID: {joined}")

    if payload["base_pilot_commit"] == _ZERO_SHA:
        raise ValueError("DESCRIPTOR_NOT_CONFIGURED: base_pilot_commit is the safe template value")

    checks: list[BehaviorCheck] = []
    for raw in payload["behavior_checks"]:
        kind = str(raw["kind"])
        target = str(raw["target"])
        pattern = _TARGET_PATTERNS[kind]
        if not pattern.fullmatch(target):
            raise ValueError(
                f"DESCRIPTOR_SCHEMA_INVALID: behavior_checks.target invalid for {kind}"
            )
        checks.append(
            BehaviorCheck(
                kind=kind,
                target=target,
                timeout_seconds=int(raw["timeout_seconds"]),
            )
        )

    identity = payload["project_identity"]
    godot = payload["godot"]
    return ProjectPilotDescriptor(
        repository=str(identity["repository"]),
        project_id=str(identity["project_id"]),
        base_pilot_commit=str(payload["base_pilot_commit"]),
        project_state=str(payload["project_state"]),
        godot_version=str(godot["version"]),
        godot_archive_sha256=str(godot["archive_sha256"]),
        project_file=payload["project_file"],
        main_scene_source=str(payload["main_scene_source"]),
        legacy_editor_plugins=tuple(str(value) for value in payload["legacy_editor_plugins"]),
        legacy_autoloads=tuple(str(value) for value in payload["legacy_autoloads"]),
        scratch_scene_path=str(payload["scratch_scene_path"]),
        behavior_checks=tuple(checks),
        expected_platform=str(payload["expected_platform"]),
    )


__all__ = ["BehaviorCheck", "ProjectPilotDescriptor", "load_descriptor"]
