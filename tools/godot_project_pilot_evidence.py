import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


class EvidenceVerificationError(ValueError):
    """Raised when runtime evidence cannot be physically trusted."""


_MAX_FAILURE_DIAGNOSTIC_BYTES = 1024 * 1024
_MAX_FAILURE_DIAGNOSTIC_DEPTH = 128
_DIAGNOSTIC_ATTEMPT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_SENSITIVE_KEY = re.compile(
    r"token|secret|password|credential|authorization", re.IGNORECASE
)


@dataclass(frozen=True)
class VerifiedRuntimeEvidence:
    repository: str
    source_commit: str
    base_pilot_commit: str
    saved_scene_path: str
    saved_scene_sha256: str
    runtime_result_sha256: str
    ledger_states: tuple[str, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def _confined_path(workspace: Path, declared: str) -> Path:
    root = Path(workspace).resolve()
    if not declared.startswith("res://"):
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE: path must use res://")
    relative = Path(declared.removeprefix("res://"))
    if relative.is_absolute() or ".." in relative.parts:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE")
    candidate = (root / relative).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            target = current.resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE") from exc
    return candidate


def _require_string(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise EvidenceVerificationError(f"RUNTIME_EVIDENCE_INVALID: {key}")
    return value


def _redact_sensitive_values(value: object, *, depth: int = 0) -> object:
    if depth > _MAX_FAILURE_DIAGNOSTIC_DEPTH:
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_INVALID: nested")
    if isinstance(value, dict):
        return {
            key: "[REDACTED]"
            if _SENSITIVE_KEY.search(key)
            else _redact_sensitive_values(item, depth=depth + 1)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_sensitive_values(item, depth=depth + 1) for item in value]
    return value


def preserve_runtime_failure_diagnostics(
    workspace: Path,
    runtime_result_path: Path,
    output_dir: Path,
    *,
    attempt_id: str,
) -> Path:
    """Persist one bounded, redacted failure snapshot without trusting it as PASS."""
    if not _DIAGNOSTIC_ATTEMPT_ID.fullmatch(attempt_id):
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_INVALID: attempt id")

    root = Path(workspace).resolve()
    runtime_path = Path(runtime_result_path).resolve()
    try:
        runtime_path.relative_to(root)
    except ValueError as exc:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE: runtime result") from exc

    try:
        raw = runtime_path.read_bytes()
    except OSError as exc:
        raise EvidenceVerificationError(f"RUNTIME_DIAGNOSTIC_INVALID: {exc}") from exc
    if len(raw) > _MAX_FAILURE_DIAGNOSTIC_BYTES:
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_INVALID: oversized")
    try:
        payload = json.loads(raw)
    except (RecursionError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceVerificationError(f"RUNTIME_DIAGNOSTIC_INVALID: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_INVALID: root")

    try:
        sanitized = _redact_sensitive_values(payload)
        assert isinstance(sanitized, dict)
        sanitized["diagnostic_attempt_id"] = attempt_id
        serialized = (
            json.dumps(
                sanitized,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
    except (RecursionError, TypeError, ValueError) as exc:
        raise EvidenceVerificationError(f"RUNTIME_DIAGNOSTIC_INVALID: nested: {exc}") from exc
    if len(serialized) > _MAX_FAILURE_DIAGNOSTIC_BYTES:
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_INVALID: oversized")

    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    diagnostics_root = destination / "diagnostics"
    attempt_dir = diagnostics_root / attempt_id
    try:
        attempt_dir.resolve(strict=False).relative_to(destination)
    except ValueError as exc:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE: diagnostics output") from exc
    attempt_dir.mkdir(parents=True, exist_ok=True)
    snapshot = attempt_dir / "runtime-result.sanitized.json"
    try:
        with snapshot.open("xb") as handle:
            handle.write(serialized)
    except FileExistsError as exc:
        raise EvidenceVerificationError("RUNTIME_DIAGNOSTIC_EXISTS") from exc
    return snapshot


def verify_runtime_evidence(
    workspace: Path,
    runtime_result_path: Path,
) -> VerifiedRuntimeEvidence:
    result_path = Path(runtime_result_path).resolve()
    root = Path(workspace).resolve()
    try:
        result_path.relative_to(root)
    except ValueError as exc:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE: runtime result") from exc
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceVerificationError(f"RUNTIME_EVIDENCE_INVALID: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceVerificationError("RUNTIME_EVIDENCE_INVALID: root")
    if payload.get("status") != "PASS":
        raise EvidenceVerificationError(
            f"RUNTIME_EVIDENCE_FAILED: {payload.get('status')}"
        )
    for key in (
        "main_scene_inspect",
        "scratch_scene_rename",
        "editor_undo",
        "scratch_scene_save",
    ):
        if payload.get(key) != "PASS":
            raise EvidenceVerificationError(f"RUNTIME_EVIDENCE_INVALID: {key}")
    if payload.get("base_network_listener") is not False:
        raise EvidenceVerificationError("NETWORK_LISTENER_FORBIDDEN")

    ledger = payload.get("ledger_states")
    if ledger != ["COMPLETED", "COMPLETED"]:
        raise EvidenceVerificationError("LEDGER_EVIDENCE_INVALID")
    declared_path = _require_string(payload, "saved_scene_path")
    saved_scene = _confined_path(root, declared_path)
    if not saved_scene.is_file():
        raise EvidenceVerificationError("EVIDENCE_FILE_MISSING: saved scene")
    declared_hash = _require_string(payload, "saved_scene_sha256")
    actual_hash = sha256_file(saved_scene)
    if declared_hash != actual_hash:
        raise EvidenceVerificationError("ARTIFACT_BYTE_HASH_MISMATCH: saved scene")

    return VerifiedRuntimeEvidence(
        repository=_require_string(payload, "repository"),
        source_commit=_require_string(payload, "source_commit"),
        base_pilot_commit=_require_string(payload, "base_pilot_commit"),
        saved_scene_path=declared_path,
        saved_scene_sha256=actual_hash,
        runtime_result_sha256=sha256_file(result_path),
        ledger_states=tuple(str(value) for value in ledger),
    )


def write_final_evidence(
    output_dir: Path,
    *,
    repository: str,
    source_commit: str,
    base_pilot_commit: str,
    project_state: str,
    result: str,
    source_before: Mapping[str, str],
    source_after: Mapping[str, str],
    changed_paths: Sequence[str],
    runtime: VerifiedRuntimeEvidence | None,
    legacy_mutation_authority: str,
    preserved_autoloads: Sequence[str] = (),
    process_records: Sequence[Mapping[str, object]] = (),
    failure_diagnostic_path: str | None = None,
) -> Path:
    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    canonical_before = json.dumps(
        {key: source_before[key] for key in sorted(source_before)},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    canonical_after = json.dumps(
        {key: source_after[key] for key in sorted(source_after)},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    payload: dict[str, object] = {
        "schema_version": "1",
        "repository": repository,
        "source_commit": source_commit,
        "base_pilot_commit": base_pilot_commit,
        "project_state": project_state,
        "result": result,
        "project_load": "PASS" if result == "PASS" else "NOT_APPLICABLE",
        "main_scene_inspect": "PASS" if runtime else "NOT_APPLICABLE",
        "scratch_scene_rename": "PASS" if runtime else "NOT_APPLICABLE",
        "editor_undo": "PASS" if runtime else "NOT_APPLICABLE",
        "scratch_scene_save": "PASS" if runtime else "NOT_APPLICABLE",
        "physical_sha256": "PASS" if runtime else "NOT_APPLICABLE",
        "source_tree_unchanged": "PASS" if not changed_paths else "FAIL",
        "legacy_mutation_authority": legacy_mutation_authority,
        "base_network_listener": False,
        "source_before_sha256": hashlib.sha256(canonical_before).hexdigest(),
        "source_after_sha256": hashlib.sha256(canonical_after).hexdigest(),
        "changed_paths": list(changed_paths),
        "preserved_autoloads": list(preserved_autoloads),
        "process_records": list(process_records),
        "runtime_result_sha256": runtime.runtime_result_sha256 if runtime else None,
        "saved_scene_sha256": runtime.saved_scene_sha256 if runtime else None,
        "saved_scene_path": runtime.saved_scene_path if runtime else None,
        "failure_diagnostic_path": failure_diagnostic_path,
    }
    path = destination / "project-pilot-evidence.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


__all__ = [
    "EvidenceVerificationError",
    "VerifiedRuntimeEvidence",
    "sha256_file",
    "preserve_runtime_failure_diagnostics",
    "verify_runtime_evidence",
    "write_final_evidence",
]
