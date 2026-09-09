from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping


EVIDENCE_CEILING = (
    "CLI_EXPORT_AND_READBACK_ONLY_NOT_GODOT_RUNTIME_NOT_HUMAN_APPROVAL"
)
ASSET_ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_-]{0,63}$")
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
SUPPORTED_SHEET_TYPES = frozenset({"horizontal", "vertical", "rows", "columns", "packed"})
CONFIG_KEYS = frozenset(
    {
        "schema_version",
        "source_roots",
        "candidate_output_root",
        "allowed_source_extensions",
        "sheet_type",
        "border_padding",
        "shape_padding",
        "inner_padding",
        "timeout_seconds",
        "use_noinapp",
    }
)


class BridgeError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {"status": "BLOCKED", "code": self.code}
        if self.detail:
            result["detail"] = self.detail
        return result


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _is_link_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    isjunction = getattr(os.path, "isjunction", None)
    return bool(isjunction(path)) if isjunction is not None else False


def _reject_link_traversal(root: Path, relative: Path, code: str) -> None:
    current = root
    for part in relative.parts:
        current = current / part
        if _is_link_or_junction(current):
            raise BridgeError(code, _relative_posix(current, root))


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError as error:
        raise BridgeError("PATH_OUTSIDE_PROJECT", str(path)) from error


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path, code: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BridgeError(code, f"{path.name}: {error}") from error


def _require_int(data: Mapping[str, object], key: str, minimum: int, maximum: int) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= maximum:
        raise BridgeError(
            "INVALID_CONFIG",
            f"{key} must be an integer between {minimum} and {maximum}",
        )
    return value


@dataclass(frozen=True)
class BridgeConfig:
    project_root: Path
    config_path: Path
    source_roots: tuple[Path, ...]
    candidate_output_root: Path
    allowed_source_extensions: tuple[str, ...]
    sheet_type: str
    border_padding: int
    shape_padding: int
    inner_padding: int
    timeout_seconds: int
    use_noinapp: bool

    @classmethod
    def load(
        cls,
        project_root: Path | str,
        config_path: Path | str | None = None,
    ) -> "BridgeConfig":
        root = Path(project_root).expanduser().resolve()
        if not root.is_dir():
            raise BridgeError("INVALID_CONFIG", f"project root is not a directory: {root}")

        raw_config_path = Path(config_path) if config_path is not None else Path(".aseprite-bridge.json")
        if raw_config_path.is_absolute():
            resolved_config_path = raw_config_path.expanduser().resolve()
        else:
            resolved_config_path = (root / raw_config_path).resolve()
        if not _is_within(resolved_config_path, root):
            raise BridgeError("PATH_OUTSIDE_PROJECT", str(resolved_config_path))
        if not resolved_config_path.is_file():
            raise BridgeError("CONFIG_NOT_FOUND", _relative_posix(resolved_config_path, root))

        data = _read_json(resolved_config_path, "INVALID_CONFIG")
        if not isinstance(data, dict):
            raise BridgeError("INVALID_CONFIG", "configuration root must be a JSON object")
        unknown = sorted(set(data) - CONFIG_KEYS)
        if unknown:
            raise BridgeError("INVALID_CONFIG", f"unknown keys: {', '.join(unknown)}")
        if data.get("schema_version") != 1:
            raise BridgeError("INVALID_CONFIG", "schema_version must be 1")

        raw_source_roots = data.get("source_roots")
        if not isinstance(raw_source_roots, list) or not raw_source_roots:
            raise BridgeError("INVALID_CONFIG", "source_roots must be a non-empty array")
        source_roots: list[Path] = []
        for value in raw_source_roots:
            if not isinstance(value, str) or not value.strip():
                raise BridgeError("INVALID_CONFIG", "source_roots entries must be non-empty strings")
            raw_path = Path(value)
            if raw_path.is_absolute():
                raise BridgeError("INVALID_CONFIG", "source_roots must be project-relative")
            unresolved = root / raw_path
            _reject_link_traversal(root, raw_path, "INVALID_CONFIG")
            resolved = unresolved.resolve()
            if not _is_within(resolved, root):
                raise BridgeError("PATH_OUTSIDE_PROJECT", value)
            if not resolved.is_dir():
                raise BridgeError("INVALID_CONFIG", f"source_root is not a directory: {value}")
            source_roots.append(resolved)

        raw_candidate_root = data.get("candidate_output_root")
        if not isinstance(raw_candidate_root, str) or not raw_candidate_root.strip():
            raise BridgeError("INVALID_CONFIG", "candidate_output_root must be a non-empty string")
        candidate_path = Path(raw_candidate_root)
        if candidate_path.is_absolute():
            raise BridgeError("INVALID_CONFIG", "candidate_output_root must be project-relative")
        try:
            _reject_link_traversal(root, candidate_path, "INVALID_CONFIG")
        except BridgeError as error:
            raise BridgeError(
                "INVALID_CONFIG",
                f"candidate_output_root traverses a symlink/junction: {error.detail}",
            ) from error
        candidate_root = (root / candidate_path).resolve()
        if not _is_within(candidate_root, root):
            raise BridgeError("PATH_OUTSIDE_PROJECT", raw_candidate_root)
        if candidate_root == root:
            raise BridgeError("INVALID_CONFIG", "candidate_output_root cannot equal project_root")
        if not any(
            candidate_root != source_root and _is_within(candidate_root, source_root)
            for source_root in source_roots
        ):
            raise BridgeError(
                "INVALID_CONFIG",
                "candidate_output_root must be inside one source_root and cannot equal it",
            )

        raw_extensions = data.get("allowed_source_extensions")
        if not isinstance(raw_extensions, list) or not raw_extensions:
            raise BridgeError(
                "INVALID_CONFIG",
                "allowed_source_extensions must be a non-empty array",
            )
        extensions: list[str] = []
        for value in raw_extensions:
            if not isinstance(value, str) or not value.startswith(".") or len(value) < 2:
                raise BridgeError(
                    "INVALID_CONFIG",
                    "allowed_source_extensions entries must start with '.'",
                )
            normalized = value.lower()
            if normalized not in extensions:
                extensions.append(normalized)

        sheet_type = data.get("sheet_type")
        if not isinstance(sheet_type, str) or sheet_type not in SUPPORTED_SHEET_TYPES:
            raise BridgeError(
                "INVALID_CONFIG",
                "sheet_type must be horizontal, vertical, rows, columns, or packed",
            )
        border_padding = _require_int(data, "border_padding", 0, 1024)
        shape_padding = _require_int(data, "shape_padding", 0, 1024)
        inner_padding = _require_int(data, "inner_padding", 0, 1024)
        timeout_seconds = _require_int(data, "timeout_seconds", 1, 600)
        use_noinapp = data.get("use_noinapp")
        if not isinstance(use_noinapp, bool):
            raise BridgeError("INVALID_CONFIG", "use_noinapp must be a boolean")

        return cls(
            project_root=root,
            config_path=resolved_config_path,
            source_roots=tuple(source_roots),
            candidate_output_root=candidate_root,
            allowed_source_extensions=tuple(extensions),
            sheet_type=sheet_type,
            border_padding=border_padding,
            shape_padding=shape_padding,
            inner_padding=inner_padding,
            timeout_seconds=timeout_seconds,
            use_noinapp=use_noinapp,
        )
