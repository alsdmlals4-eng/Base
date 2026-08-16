from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from .protocol import RunRequest, normalize_contract_path


_AUTHORITY_REFERENCE_KEYS = (
    "planning_lock_path",
    "visual_lock_path",
    "runtime_adapter_path",
    "implementation_package_path",
    "coverage_ledger_path",
    "active_run_path",
    "immutable_run_path",
)


class AuthoritySnapshotError(ValueError):
    pass


@dataclass(frozen=True)
class AuthorityFile:
    path: str
    content: str


@dataclass(frozen=True)
class AuthoritySnapshot:
    project_id: str
    package_id: str
    source_main_sha: str
    capsule_path: str
    runtime_adapter_path: str
    files: tuple[AuthorityFile, ...]
    snapshot_sha256: str

    @property
    def paths(self) -> tuple[str, ...]:
        return tuple(item.path for item in self.files)

    def text(self, relative: str) -> str:
        normalized = normalize_contract_path(relative, "authority_path")
        for item in self.files:
            if item.path == normalized:
                return item.content
        raise AuthoritySnapshotError(f"authority path is not captured: {normalized}")

    def parsed_object(self, relative: str) -> dict[str, object]:
        try:
            value = json.loads(self.text(relative))
        except json.JSONDecodeError as exc:
            raise AuthoritySnapshotError("captured authority JSON is invalid") from exc
        if not isinstance(value, dict):
            raise AuthoritySnapshotError("captured authority JSON must be an object")
        return value


def validate_bundle(capsule_path: Path) -> Iterable[Any]:
    """Load the schema validator only when an authority snapshot is actually captured.

    The generic provider transport imports this module only for the immutable
    snapshot type and must remain usable in its intentionally smaller dependency
    environment. Real capture still executes the canonical M2 bundle validator.
    """
    try:
        from tools.loop_contracts.bundle_validation import validate_bundle as _validate_bundle
    except ImportError as exc:
        raise AuthoritySnapshotError(
            "canonical authority validator dependency is unavailable"
        ) from exc

    return _validate_bundle(capsule_path)


def _closed_path(root: Path, relative: str) -> Path:
    normalized = normalize_contract_path(relative, "authority_path")
    lexical = root.joinpath(*normalized.split("/"))
    current = root
    for part in normalized.split("/"):
        current = current / part
        if current.is_symlink():
            raise AuthoritySnapshotError(f"authority path must not traverse a symlink: {normalized}")
    resolved_root = root.resolve(strict=True)
    resolved = lexical.resolve(strict=False)
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise AuthoritySnapshotError(f"authority path escapes project root: {normalized}")
    if not lexical.is_file():
        raise AuthoritySnapshotError(f"authority file is missing: {normalized}")
    return lexical


def _read_utf8(path: Path, *, relative: str) -> str:
    payload = path.read_bytes()
    if b"\x00" in payload:
        raise AuthoritySnapshotError(f"authority file contains binary NUL data: {relative}")
    try:
        return payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuthoritySnapshotError(f"authority file must be UTF-8 text: {relative}") from exc


def _load_object(text: str, *, relative: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise AuthoritySnapshotError(f"authority file contains invalid JSON: {relative}") from exc
    if not isinstance(value, dict):
        raise AuthoritySnapshotError(f"authority file must contain a JSON object: {relative}")
    return value


def _referenced_project_path(capsule_relative: str, reference: str, *, label: str) -> str:
    capsule_dir = Path(capsule_relative).parent
    return normalize_contract_path((capsule_dir / reference).as_posix(), label)


def _resolve_authority_paths(
    *,
    normalized_capsule: str,
    capsule: dict[str, Any],
) -> tuple[dict[str, str], tuple[str, ...]]:
    resolved_paths: dict[str, str] = {"capsule": normalized_capsule}
    for key in _AUTHORITY_REFERENCE_KEYS:
        value = capsule.get(key)
        if not isinstance(value, str) or not value:
            raise AuthoritySnapshotError(f"authority reference is missing: {key}")
        resolved_paths[key] = _referenced_project_path(
            normalized_capsule,
            value,
            label=key,
        )
    unique_paths = [normalized_capsule]
    unique_paths.extend(
        path for path in resolved_paths.values() if path not in unique_paths
    )
    return resolved_paths, tuple(unique_paths)


def _read_authority_set(root: Path, paths: tuple[str, ...]) -> dict[str, str]:
    return {
        relative: _read_utf8(_closed_path(root, relative), relative=relative)
        for relative in paths
    }


def _assert_request_matches(
    *,
    request: RunRequest,
    capsule: dict[str, Any],
    package: dict[str, Any],
    capsule_relative: str,
    package_relative: str,
) -> None:
    expected = {
        "project_id": capsule.get("project_id"),
        "package_id": package.get("package_id"),
        "expected_main_sha": capsule.get("source_main_sha"),
        "capsule_path": capsule_relative,
        "package_path": package_relative,
        "allowed_paths": tuple(package.get("allowed_paths", ())),
        "forbidden_paths": tuple(package.get("forbidden_paths", ())),
        "resource_locks": tuple(package.get("resource_locks", ())),
        "requirement_ids": tuple(package.get("requirement_ids", ())),
    }
    actual = {
        "project_id": request.project_id,
        "package_id": request.package_id,
        "expected_main_sha": request.expected_main_sha,
        "capsule_path": request.capsule_path,
        "package_path": request.package_path,
        "allowed_paths": request.allowed_paths,
        "forbidden_paths": request.forbidden_paths,
        "resource_locks": request.resource_locks,
        "requirement_ids": request.requirement_ids,
    }
    if actual != expected:
        raise AuthoritySnapshotError("request authority differs from the validated Capsule bundle")


def capture_authority_snapshot(
    *,
    project_root: Path,
    capsule_relative: str,
    request: RunRequest,
) -> AuthoritySnapshot:
    root = Path(project_root).resolve(strict=True)
    normalized_capsule = normalize_contract_path(capsule_relative, "capsule_relative")
    capsule_path = _closed_path(root, normalized_capsule)

    initial_capsule_text = _read_utf8(capsule_path, relative=normalized_capsule)
    initial_capsule = _load_object(initial_capsule_text, relative=normalized_capsule)
    resolved_paths, unique_paths = _resolve_authority_paths(
        normalized_capsule=normalized_capsule,
        capsule=initial_capsule,
    )
    before = _read_authority_set(root, unique_paths)

    findings = list(validate_bundle(capsule_path))
    if findings:
        codes = [getattr(item, "code", "CONTRACT_INVALID") for item in findings]
        raise AuthoritySnapshotError(f"authority bundle is not ready: {codes}")

    after = _read_authority_set(root, unique_paths)
    if after != before:
        raise AuthoritySnapshotError("authority bundle changed during capture")

    capsule_text = before[normalized_capsule]
    capsule = _load_object(capsule_text, relative=normalized_capsule)
    stable_resolved_paths, stable_unique_paths = _resolve_authority_paths(
        normalized_capsule=normalized_capsule,
        capsule=capsule,
    )
    if stable_resolved_paths != resolved_paths or stable_unique_paths != unique_paths:
        raise AuthoritySnapshotError("authority bundle changed during capture")

    package_relative = resolved_paths["implementation_package_path"]
    package_text = before[package_relative]
    package = _load_object(package_text, relative=package_relative)
    _assert_request_matches(
        request=request,
        capsule=capsule,
        package=package,
        capsule_relative=normalized_capsule,
        package_relative=package_relative,
    )

    captured = tuple(
        AuthorityFile(path=relative, content=before[relative])
        for relative in unique_paths
    )
    canonical = json.dumps(
        {
            "project_id": request.project_id,
            "package_id": request.package_id,
            "source_main_sha": request.expected_main_sha,
            "capsule_path": normalized_capsule,
            "runtime_adapter_path": resolved_paths["runtime_adapter_path"],
            "files": [
                {"path": item.path, "content": item.content}
                for item in captured
            ],
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()

    return AuthoritySnapshot(
        project_id=request.project_id,
        package_id=request.package_id,
        source_main_sha=request.expected_main_sha,
        capsule_path=normalized_capsule,
        runtime_adapter_path=resolved_paths["runtime_adapter_path"],
        files=captured,
        snapshot_sha256=digest,
    )
