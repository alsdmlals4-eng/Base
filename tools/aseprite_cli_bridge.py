#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


class BridgeError(RuntimeError):
    """Expected operator-facing failure for the Aseprite bridge."""


_ASSET_ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9_-]{0,63}$")
_ALLOWED_EXTENSIONS = frozenset({".aseprite", ".ase"})
_ALLOWED_SHEET_TYPES = frozenset(
    {"rows", "columns", "horizontal", "vertical", "packed"}
)
_ALLOWED_ADOPTION_STATES = frozenset(
    {
        "CANDIDATE",
        "TRIAL_APPROVED",
        "ADOPTED_ACTIVE",
        "ADOPTED_DISABLED",
        "DEFERRED",
        "REJECTED",
        "INSTALLED_UNUSED",
        "REMOVAL_PENDING",
        "REMOVED",
    }
)
_ALLOWED_PROFILE_KEYS = frozenset(
    {
        "schema_version",
        "adoption_state",
        "source_roots",
        "candidate_output_root",
        "allowed_source_extensions",
        "allow_overwrite",
        "timeout_seconds",
        "sheet_type",
    }
)
_DEFAULT_PROFILE: dict[str, Any] = {
    "schema_version": 1,
    "adoption_state": "CANDIDATE",
    "source_roots": [".asset-vault/library", "assets/source/aseprite"],
    "candidate_output_root": ".asset-vault/library/aseprite-generated",
    "allowed_source_extensions": [".aseprite", ".ase"],
    "allow_overwrite": False,
    "timeout_seconds": 60,
    "sheet_type": "rows",
}


@dataclass(frozen=True)
class ExecutableInfo:
    path: Path
    discovery_source: str


@dataclass(frozen=True)
class BridgeConfig:
    project_root: Path
    source_roots: tuple[Path, ...]
    candidate_output_root: Path
    allowed_source_extensions: tuple[str, ...]
    allow_overwrite: bool
    timeout_seconds: int
    sheet_type: str
    adoption_state: str


def _is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(callable(is_junction) and is_junction())


def _reject_symlink_chain(base: Path, candidate: Path, label: str) -> None:
    try:
        relative = candidate.relative_to(base)
    except ValueError as error:
        raise BridgeError(f"{label} escapes its declared root") from error
    current = base
    if _is_link_like(current):
        raise BridgeError(f"{label} must not traverse a symlink or junction")
    for part in relative.parts:
        current = current / part
        if _is_link_like(current):
            raise BridgeError(f"{label} must not traverse a symlink or junction")


def _require_relative_project_path(project_root: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise BridgeError(f"{label} must be a non-empty repository-relative path")
    raw = Path(value)
    if raw.is_absolute():
        raise BridgeError(f"{label} must be repository-relative")
    if ".." in raw.parts:
        raise BridgeError(f"{label} must not contain '..'")
    lexical = Path(os.path.abspath(project_root / raw))
    _reject_symlink_chain(project_root, lexical, label)
    resolved = lexical.resolve(strict=False)
    try:
        relative = resolved.relative_to(project_root)
    except ValueError as error:
        raise BridgeError(f"{label} escapes the project root") from error
    if relative == Path("."):
        raise BridgeError(f"{label} must not be the project root")
    return lexical


def _load_profile_data(config_path: Path | None) -> dict[str, Any]:
    if config_path is None:
        return dict(_DEFAULT_PROFILE)
    path = Path(config_path).expanduser().resolve()
    if not path.is_file():
        raise BridgeError(f"Profile does not exist: {path}")
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BridgeError(f"Profile is not valid UTF-8 JSON: {path}") from error
    if not isinstance(loaded, dict):
        raise BridgeError("Profile root must be a JSON object")
    unknown = sorted(set(loaded) - _ALLOWED_PROFILE_KEYS)
    if unknown:
        raise BridgeError("Unknown profile keys: " + ", ".join(unknown))
    merged = dict(_DEFAULT_PROFILE)
    merged.update(loaded)
    return merged


def load_config(project_root: Path | str, config_path: Path | str | None) -> BridgeConfig:
    root = Path(project_root).expanduser().resolve()
    if not root.is_dir():
        raise BridgeError(f"Project root does not exist: {root}")
    data = _load_profile_data(None if config_path is None else Path(config_path))

    if data.get("schema_version") != 1:
        raise BridgeError("Only profile schema_version 1 is supported")

    source_values = data.get("source_roots")
    if not isinstance(source_values, list) or not source_values:
        raise BridgeError("source_roots must be a non-empty JSON array")
    source_roots = tuple(
        _require_relative_project_path(root, value, "source_roots entry")
        for value in source_values
    )

    candidate_root = _require_relative_project_path(
        root, data.get("candidate_output_root"), "candidate_output_root"
    )

    extensions = data.get("allowed_source_extensions")
    if not isinstance(extensions, list) or not extensions:
        raise BridgeError("allowed_source_extensions must be a non-empty JSON array")
    normalized_extensions: list[str] = []
    for value in extensions:
        if not isinstance(value, str):
            raise BridgeError("allowed_source_extensions entries must be strings")
        normalized = value.lower()
        if normalized not in _ALLOWED_EXTENSIONS:
            raise BridgeError(f"Unsupported source extension in profile: {value}")
        normalized_extensions.append(normalized)

    allow_overwrite = data.get("allow_overwrite")
    if not isinstance(allow_overwrite, bool):
        raise BridgeError("allow_overwrite must be true or false")

    timeout_seconds = data.get("timeout_seconds")
    if (
        not isinstance(timeout_seconds, int)
        or isinstance(timeout_seconds, bool)
        or not 1 <= timeout_seconds <= 600
    ):
        raise BridgeError("timeout_seconds must be an integer from 1 through 600")

    sheet_type = data.get("sheet_type")
    if sheet_type not in _ALLOWED_SHEET_TYPES:
        raise BridgeError(
            "sheet_type must be one of: " + ", ".join(sorted(_ALLOWED_SHEET_TYPES))
        )

    adoption_state = data.get("adoption_state")
    if adoption_state not in _ALLOWED_ADOPTION_STATES:
        raise BridgeError(
            "adoption_state must be one of: "
            + ", ".join(sorted(_ALLOWED_ADOPTION_STATES))
        )

    return BridgeConfig(
        project_root=root,
        source_roots=source_roots,
        candidate_output_root=candidate_root,
        allowed_source_extensions=tuple(normalized_extensions),
        allow_overwrite=allow_overwrite,
        timeout_seconds=timeout_seconds,
        sheet_type=sheet_type,
        adoption_state=adoption_state,
    )


def validate_asset_id(asset_id: str) -> str:
    if not isinstance(asset_id, str) or not _ASSET_ID_PATTERN.fullmatch(asset_id):
        raise BridgeError(
            "asset_id must match [A-Z0-9][A-Z0-9_-]{0,63}"
        )
    return asset_id


def resolve_source(config: BridgeConfig, source: Path | str) -> Path:
    path = Path(source).expanduser()
    if not path.is_absolute():
        path = config.project_root / path
    lexical = Path(os.path.abspath(path))
    if _is_within(lexical, config.project_root):
        _reject_symlink_chain(config.project_root, lexical, "Aseprite source")
    resolved = lexical.resolve()
    if not resolved.is_file():
        raise BridgeError(f"Aseprite source does not exist: {resolved}")
    if resolved.suffix.lower() not in config.allowed_source_extensions:
        raise BridgeError(
            "Aseprite source extension is not allowed: " + resolved.suffix.lower()
        )
    if not any(_is_within(resolved, root.resolve()) for root in config.source_roots):
        raise BridgeError("Aseprite source is outside every declared source root")
    return resolved


def resolve_candidate_dir(config: BridgeConfig, asset_id: str) -> Path:
    identifier = validate_asset_id(asset_id)
    _reject_symlink_chain(
        config.project_root,
        config.candidate_output_root,
        "candidate_output_root",
    )
    candidate = config.candidate_output_root / identifier
    _reject_symlink_chain(config.candidate_output_root, candidate, "Candidate output")
    resolved = candidate.resolve(strict=False)
    if not _is_within(resolved, config.candidate_output_root.resolve(strict=False)):
        raise BridgeError("Candidate output escapes candidate_output_root")
    return candidate


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _clean_executable_value(value: str) -> str:
    return value.strip().strip('"').strip("'").strip()


def _executable_info(value: str | Path, source: str) -> ExecutableInfo | None:
    cleaned = _clean_executable_value(str(value))
    if not cleaned:
        return None
    path = Path(cleaned).expanduser().resolve()
    if not path.is_file():
        return None
    return ExecutableInfo(path=path, discovery_source=source)


def _common_aseprite_locations(environment: Mapping[str, str]) -> tuple[Path, ...]:
    values: list[Path] = []
    for key in ("ProgramFiles", "PROGRAMFILES", "ProgramFiles(x86)", "PROGRAMFILES(X86)"):
        base = environment.get(key)
        if not base:
            continue
        base_path = Path(_clean_executable_value(base)).expanduser()
        values.extend(
            (
                base_path / "Aseprite" / "Aseprite.exe",
                base_path / "Steam" / "steamapps" / "common" / "Aseprite" / "Aseprite.exe",
            )
        )
    local_app_data = environment.get("LOCALAPPDATA")
    if local_app_data:
        values.append(
            Path(_clean_executable_value(local_app_data)).expanduser()
            / "Programs"
            / "Aseprite"
            / "Aseprite.exe"
        )
    home = Path(environment.get("HOME") or Path.home()).expanduser()
    values.extend(
        (
            Path("/Applications/Aseprite.app/Contents/MacOS/aseprite"),
            home / "Applications" / "Aseprite.app" / "Contents" / "MacOS" / "aseprite",
            Path("/usr/local/bin/aseprite"),
            Path("/usr/bin/aseprite"),
            home / ".local" / "bin" / "aseprite",
            home / ".steam" / "steam" / "steamapps" / "common" / "Aseprite" / "aseprite",
            home / ".local" / "share" / "Steam" / "steamapps" / "common" / "Aseprite" / "aseprite",
        )
    )
    return tuple(values)


def discover_aseprite(
    explicit: Path | str | None,
    environment: Mapping[str, str] | None = None,
) -> ExecutableInfo:
    env = dict(os.environ if environment is None else environment)
    if explicit is not None:
        result = _executable_info(explicit, "explicit")
        if result is None:
            raise BridgeError(f"Explicit Aseprite executable does not exist: {explicit}")
        return result

    environment_value = env.get("ASEPRITE_PATH")
    if environment_value:
        result = _executable_info(environment_value, "environment")
        if result is None:
            raise BridgeError("ASEPRITE_PATH does not point to an existing file")
        return result

    for name in ("aseprite", "Aseprite", "aseprite.exe", "Aseprite.exe"):
        discovered = shutil.which(name, path=env.get("PATH"))
        if discovered:
            result = _executable_info(discovered, "path")
            if result is not None:
                return result

    for candidate in _common_aseprite_locations(env):
        result = _executable_info(candidate, "common_location")
        if result is not None:
            return result

    raise BridgeError(
        "Aseprite executable was not found. Set ASEPRITE_PATH or pass --aseprite."
    )


def _run_aseprite(
    arguments: Sequence[str], timeout_seconds: int
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            list(arguments),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as error:
        raise BridgeError(
            f"Aseprite command exceeded the {timeout_seconds}s timeout"
        ) from error
    except OSError as error:
        raise BridgeError(f"Aseprite command could not start: {error}") from error
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "no diagnostic output").strip()
        if len(detail) > 2000:
            detail = detail[-2000:]
        raise BridgeError(
            f"Aseprite command failed with exit code {result.returncode}: {detail}"
        )
    return result


def read_aseprite_version(executable: ExecutableInfo, timeout_seconds: int) -> str:
    result = _run_aseprite([str(executable.path), "--version"], timeout_seconds)
    version = (result.stdout or result.stderr).strip().splitlines()
    if not version:
        raise BridgeError("Aseprite --version returned no version text")
    return version[0].strip()


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _project_relative(config: BridgeConfig, path: Path) -> str:
    try:
        return path.resolve().relative_to(config.project_root).as_posix()
    except ValueError as error:
        raise BridgeError("Path is outside the project root") from error


def inspect_source(
    config: BridgeConfig,
    executable: ExecutableInfo,
    source: Path | str,
) -> dict[str, object]:
    resolved_source = resolve_source(config, source)
    version = read_aseprite_version(executable, config.timeout_seconds)
    command = [
        str(executable.path),
        "-b",
        "--list-layer-hierarchy",
        "--list-tags",
        "--list-slices",
        "--data=",
        str(resolved_source),
    ]
    result = _run_aseprite(command, config.timeout_seconds)
    try:
        metadata = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise BridgeError("Aseprite inspection did not return valid JSON") from error
    if not isinstance(metadata, dict):
        raise BridgeError("Aseprite inspection JSON root must be an object")
    return {
        "status": "PASS",
        "operation": "inspect",
        "source": _project_relative(config, resolved_source),
        "source_sha256": sha256_file(resolved_source),
        "aseprite_version": version,
        "metadata": metadata,
    }


def _candidate_paths(config: BridgeConfig, asset_id: str) -> tuple[Path, Path, Path, Path]:
    candidate_dir = resolve_candidate_dir(config, asset_id)
    identifier = validate_asset_id(asset_id)
    return (
        candidate_dir,
        candidate_dir / f"{identifier}.png",
        candidate_dir / f"{identifier}.json",
        candidate_dir / f"{identifier}.receipt.json",
    )


def _require_candidate_file(config: BridgeConfig, path: Path, label: str) -> Path:
    if _is_link_like(path):
        raise BridgeError(f"{label} must not be a symlink or junction")
    resolved = path.resolve()
    if not _is_within(resolved, config.candidate_output_root):
        raise BridgeError(f"{label} escapes candidate_output_root")
    if not resolved.is_file():
        raise BridgeError(f"{label} does not exist: {_project_relative(config, resolved)}")
    return resolved


def _validate_png(path: Path) -> None:
    try:
        with path.open("rb") as stream:
            signature = stream.read(8)
    except OSError as error:
        raise BridgeError(f"Could not read exported PNG: {error}") from error
    if signature != b"\x89PNG\r\n\x1a\n":
        raise BridgeError("Exported PNG does not have a valid PNG signature")
    if path.stat().st_size <= 8:
        raise BridgeError("Exported PNG is empty")


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BridgeError(f"{label} is not valid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise BridgeError(f"{label} root must be a JSON object")
    return value


def _validate_metadata(path: Path) -> dict[str, Any]:
    metadata = _read_json_object(path, "Aseprite metadata")
    if "frames" not in metadata or not isinstance(metadata["frames"], (list, dict)):
        raise BridgeError("Aseprite metadata must contain frames as an array or object")
    if "meta" not in metadata or not isinstance(metadata["meta"], dict):
        raise BridgeError("Aseprite metadata must contain meta as an object")
    return metadata


def _write_json(path: Path, value: Mapping[str, object]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _copy_exclusive(source: Path, destination: Path) -> None:
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with source.open("rb") as input_stream, os.fdopen(descriptor, "wb") as output_stream:
            descriptor = -1
            shutil.copyfileobj(input_stream, output_stream)
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _publish_bundle(
    staged_paths: tuple[Path, Path, Path],
    final_paths: tuple[Path, Path, Path],
    overwrite: bool,
) -> None:
    if not overwrite:
        created: list[Path] = []
        try:
            for staged, final in zip(staged_paths, final_paths, strict=True):
                _copy_exclusive(staged, final)
                created.append(final)
        except Exception:
            for final in reversed(created):
                try:
                    final.unlink()
                except FileNotFoundError:
                    pass
            raise
        return

    backup_root = staged_paths[0].parent / ".previous"
    backup_root.mkdir()
    backups: dict[Path, Path] = {}
    published: list[Path] = []
    try:
        for final in final_paths:
            if final.exists() or _is_link_like(final):
                backup = backup_root / final.name
                os.replace(final, backup)
                backups[final] = backup
        for staged, final in zip(staged_paths, final_paths, strict=True):
            os.replace(staged, final)
            published.append(final)
    except Exception:
        for final in reversed(published):
            try:
                final.unlink()
            except FileNotFoundError:
                pass
        for final, backup in backups.items():
            if backup.exists():
                os.replace(backup, final)
        raise


def _utc_now_text() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def export_candidate(
    config: BridgeConfig,
    executable: ExecutableInfo,
    source: Path | str,
    asset_id: str,
    *,
    overwrite: bool = False,
) -> dict[str, object]:
    identifier = validate_asset_id(asset_id)
    resolved_source = resolve_source(config, source)
    candidate_dir, png_path, metadata_path, receipt_path = _candidate_paths(
        config, identifier
    )
    final_paths = (png_path, metadata_path, receipt_path)

    if overwrite and not config.allow_overwrite:
        raise BridgeError(
            "The profile forbids overwrite; set allow_overwrite=true and pass "
            "--overwrite explicitly"
        )
    linked_outputs = [path for path in final_paths if _is_link_like(path)]
    if linked_outputs:
        relative = ", ".join(
            path.relative_to(config.project_root).as_posix()
            for path in linked_outputs
        )
        raise BridgeError(
            f"Candidate output must not be a symlink or junction: {relative}"
        )
    existing = [path for path in final_paths if path.exists()]
    if existing and not overwrite:
        relative = ", ".join(_project_relative(config, path.resolve()) for path in existing)
        raise BridgeError(f"Candidate output already exists: {relative}")

    candidate_dir.mkdir(parents=True, exist_ok=True)
    _reject_symlink_chain(
        config.candidate_output_root,
        candidate_dir,
        "Candidate output",
    )
    version = read_aseprite_version(executable, config.timeout_seconds)

    with tempfile.TemporaryDirectory(
        prefix=".aseprite-export-", dir=candidate_dir
    ) as temporary_directory:
        staging = Path(temporary_directory)
        staged_png = staging / png_path.name
        staged_metadata = staging / metadata_path.name
        staged_receipt = staging / receipt_path.name
        command = [
            str(executable.path),
            "-b",
            "--list-layer-hierarchy",
            "--list-tags",
            "--list-slices",
            str(resolved_source),
            "--sheet",
            str(staged_png),
            "--data",
            str(staged_metadata),
            "--format",
            "json-array",
            "--sheet-type",
            config.sheet_type,
        ]
        _run_aseprite(command, config.timeout_seconds)
        if not staged_png.is_file() or not staged_metadata.is_file():
            raise BridgeError("Aseprite did not create both PNG and JSON outputs")
        _validate_png(staged_png)
        _validate_metadata(staged_metadata)

        receipt: dict[str, object] = {
            "schema_version": 1,
            "status": "PASS",
            "operation": "export",
            "asset_id": identifier,
            "source": _project_relative(config, resolved_source),
            "source_sha256": sha256_file(resolved_source),
            "aseprite_version": version,
            "generated_at_utc": _utc_now_text(),
            "command_contract": {
                "batch": True,
                "metadata": ["layer_hierarchy", "tags", "slices"],
                "format": "json-array",
                "sheet_type": config.sheet_type,
                "arbitrary_lua": False,
                "arbitrary_cli_arguments": False,
            },
            "outputs": {
                "spritesheet_png": {
                    "path": _project_relative(config, png_path),
                    "sha256": sha256_file(staged_png),
                    "size_bytes": staged_png.stat().st_size,
                },
                "metadata_json": {
                    "path": _project_relative(config, metadata_path),
                    "sha256": sha256_file(staged_metadata),
                    "size_bytes": staged_metadata.stat().st_size,
                },
            },
            "evidence_ceiling": [
                "BASE_BRIDGE_EXPORT_ONLY",
                "NOT_PROJECT_ADOPTION",
                "NOT_GODOT_RUNTIME_VERIFIED",
                "NOT_USER_ASSET_APPROVAL",
            ],
        }
        _write_json(staged_receipt, receipt)
        try:
            _publish_bundle(
                (staged_png, staged_metadata, staged_receipt),
                final_paths,
                overwrite,
            )
        except FileExistsError as error:
            raise BridgeError(
                "Candidate output appeared during export; no files were replaced"
            ) from error
        except OSError as error:
            raise BridgeError(f"Could not publish candidate outputs: {error}") from error

    validate_candidate(config, identifier)
    return {
        "status": "PASS",
        "operation": "export",
        "asset_id": identifier,
        "receipt": _project_relative(config, receipt_path),
    }


def validate_candidate(config: BridgeConfig, asset_id: str) -> dict[str, object]:
    identifier = validate_asset_id(asset_id)
    _, png_path, metadata_path, receipt_path = _candidate_paths(config, identifier)
    png = _require_candidate_file(config, png_path, "Spritesheet PNG")
    metadata_file = _require_candidate_file(config, metadata_path, "Metadata JSON")
    receipt_file = _require_candidate_file(config, receipt_path, "Receipt JSON")
    _validate_png(png)
    _validate_metadata(metadata_file)
    receipt = _read_json_object(receipt_file, "Aseprite receipt")

    if receipt.get("schema_version") != 1:
        raise BridgeError("Aseprite receipt schema_version must be 1")
    if receipt.get("status") != "PASS" or receipt.get("operation") != "export":
        raise BridgeError("Aseprite receipt status and operation must describe a passing export")
    if receipt.get("asset_id") != identifier:
        raise BridgeError("Aseprite receipt asset_id does not match the requested asset")
    aseprite_version = receipt.get("aseprite_version")
    if not isinstance(aseprite_version, str) or not aseprite_version.strip():
        raise BridgeError("Aseprite receipt must contain a non-empty version")
    generated_at = receipt.get("generated_at_utc")
    if not isinstance(generated_at, str) or not generated_at.endswith("Z"):
        raise BridgeError("Aseprite receipt generated_at_utc must be a UTC timestamp")
    expected_command_contract = {
        "batch": True,
        "metadata": ["layer_hierarchy", "tags", "slices"],
        "format": "json-array",
        "sheet_type": config.sheet_type,
        "arbitrary_lua": False,
        "arbitrary_cli_arguments": False,
    }
    if receipt.get("command_contract") != expected_command_contract:
        raise BridgeError("Aseprite receipt command contract was changed or weakened")
    expected_evidence_ceiling = [
        "BASE_BRIDGE_EXPORT_ONLY",
        "NOT_PROJECT_ADOPTION",
        "NOT_GODOT_RUNTIME_VERIFIED",
        "NOT_USER_ASSET_APPROVAL",
    ]
    if receipt.get("evidence_ceiling") != expected_evidence_ceiling:
        raise BridgeError("Aseprite receipt evidence ceiling was changed or weakened")
    source_value = receipt.get("source")
    if not isinstance(source_value, str):
        raise BridgeError("Aseprite receipt source must be a repository-relative path")
    source = resolve_source(config, source_value)
    if receipt.get("source_sha256") != sha256_file(source):
        raise BridgeError("Aseprite source hash does not match the receipt")

    outputs = receipt.get("outputs")
    if not isinstance(outputs, dict):
        raise BridgeError("Aseprite receipt outputs must be an object")
    expected = {
        "spritesheet_png": png,
        "metadata_json": metadata_file,
    }
    for key, output_path in expected.items():
        record = outputs.get(key)
        if not isinstance(record, dict):
            raise BridgeError(f"Aseprite receipt is missing output record: {key}")
        if record.get("path") != _project_relative(config, output_path):
            raise BridgeError(f"Aseprite receipt path does not match output: {key}")
        if record.get("sha256") != sha256_file(output_path):
            raise BridgeError(f"Aseprite output hash does not match the receipt: {key}")
        if record.get("size_bytes") != output_path.stat().st_size:
            raise BridgeError(f"Aseprite output size does not match the receipt: {key}")

    return {
        "status": "PASS",
        "operation": "validate",
        "asset_id": identifier,
        "receipt": _project_relative(config, receipt_file),
    }


def _add_common_arguments(parser: argparse.ArgumentParser, *, include_executable: bool) -> None:
    parser.add_argument(
        "--project-root",
        default=".",
        help="Target project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--config",
        help="Optional JSON profile. Safe defaults are used when omitted.",
    )
    if include_executable:
        parser.add_argument(
            "--aseprite",
            help="Optional path to Aseprite. Overrides ASEPRITE_PATH and auto-discovery.",
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect and export Aseprite sources through a restricted, local-only CLI boundary."
        )
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    doctor_parser = subparsers.add_parser(
        "doctor", help="Find Aseprite and report the exact local version."
    )
    _add_common_arguments(doctor_parser, include_executable=True)

    inspect_parser = subparsers.add_parser(
        "inspect", help="Read layers, tags, slices, and source hash without writing files."
    )
    _add_common_arguments(inspect_parser, include_executable=True)
    inspect_parser.add_argument("--source", required=True)

    export_parser = subparsers.add_parser(
        "export", help="Export PNG/JSON into the declared local candidate root."
    )
    _add_common_arguments(export_parser, include_executable=True)
    export_parser.add_argument("--source", required=True)
    export_parser.add_argument("--asset-id", required=True)
    export_parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace an existing local candidate only when the profile also sets "
            "allow_overwrite=true."
        ),
    )

    validate_parser = subparsers.add_parser(
        "validate", help="Verify candidate files and receipt hashes."
    )
    _add_common_arguments(validate_parser, include_executable=False)
    validate_parser.add_argument("--asset-id", required=True)
    return parser


def _relative_root(config: BridgeConfig, path: Path) -> str:
    return path.resolve().relative_to(config.project_root).as_posix()


def _doctor_payload(
    config: BridgeConfig,
    executable: ExecutableInfo,
    version: str,
) -> dict[str, object]:
    return {
        "status": "PASS",
        "operation": "doctor",
        "aseprite_version": version,
        "executable_path": str(executable.path),
        "discovery_source": executable.discovery_source,
        "profile_adoption_state": config.adoption_state,
        "source_roots": [_relative_root(config, root) for root in config.source_roots],
        "candidate_output_root": _relative_root(
            config, config.candidate_output_root
        ),
        "allow_overwrite": config.allow_overwrite,
        "timeout_seconds": config.timeout_seconds,
    }


def _print_json(value: Mapping[str, object]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(None if argv is None else list(argv))
        config = load_config(args.project_root, args.config)
        if args.operation == "doctor":
            executable = discover_aseprite(args.aseprite)
            result = _doctor_payload(
                config,
                executable,
                read_aseprite_version(executable, config.timeout_seconds),
            )
        elif args.operation == "inspect":
            executable = discover_aseprite(args.aseprite)
            result = inspect_source(config, executable, args.source)
        elif args.operation == "export":
            executable = discover_aseprite(args.aseprite)
            result = export_candidate(
                config,
                executable,
                args.source,
                args.asset_id,
                overwrite=args.overwrite,
            )
        elif args.operation == "validate":
            result = validate_candidate(config, args.asset_id)
        else:  # pragma: no cover - argparse enforces the subcommand set.
            raise BridgeError(f"Unsupported operation: {args.operation}")
        _print_json(result)
        return 0
    except BridgeError as error:
        print(f"ASEPRITE_BRIDGE_ERROR: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("ASEPRITE_BRIDGE_ERROR: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
