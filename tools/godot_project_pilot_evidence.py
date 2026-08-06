import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


class EvidenceVerificationError(ValueError):
    """Raised when runtime evidence cannot be physically trusted."""


@dataclass(frozen=True)
class VerifiedMainInspectEvidence:
    repository: str
    source_commit: str
    base_pilot_commit: str
    main_scene_path: str
    main_scene_sha256: str
    result_sha256: str


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


def _bounded_string(value: object, limit: int) -> str | None:
    if value is None:
        return None
    return str(value)[:limit]


def _bounded_failure_diagnostics(payload: Mapping[str, object]) -> dict[str, object]:
    ledger = payload.get("ledger_states")
    bounded_ledger = (
        [_bounded_string(value, 64) for value in ledger[:4]]
        if isinstance(ledger, list)
        else []
    )
    listener = payload.get("base_network_listener")
    return {
        "status": _bounded_string(payload.get("status"), 64),
        "code": _bounded_string(payload.get("code"), 128),
        "main_scene_inspect": _bounded_string(payload.get("main_scene_inspect"), 64),
        "scratch_scene_rename": _bounded_string(payload.get("scratch_scene_rename"), 64),
        "editor_undo": _bounded_string(payload.get("editor_undo"), 64),
        "scratch_scene_save": _bounded_string(payload.get("scratch_scene_save"), 64),
        "ledger_states": bounded_ledger,
        "base_network_listener": listener if isinstance(listener, bool) else None,
    }


def _load_evidence_payload(workspace: Path, result_path: Path) -> dict[str, object]:
    root = Path(workspace).resolve()
    path = Path(result_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise EvidenceVerificationError("EVIDENCE_PATH_ESCAPE: result") from exc
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceVerificationError(f"RUNTIME_EVIDENCE_INVALID: {exc}") from exc
    if not isinstance(payload, dict):
        raise EvidenceVerificationError("RUNTIME_EVIDENCE_INVALID: root")
    return payload


def verify_main_inspect_evidence(
    workspace: Path,
    main_result_path: Path,
) -> VerifiedMainInspectEvidence:
    root = Path(workspace).resolve()
    result_path = Path(main_result_path).resolve()
    payload = _load_evidence_payload(root, result_path)
    if payload.get("status") != "PASS":
        diagnostics = json.dumps(
            _bounded_failure_diagnostics(payload),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        raise EvidenceVerificationError(f"MAIN_INSPECT_EVIDENCE_FAILED: {diagnostics}")
    if payload.get("main_scene_inspect") != "PASS":
        raise EvidenceVerificationError("MAIN_INSPECT_EVIDENCE_INVALID")
    if payload.get("base_network_listener") is not False:
        raise EvidenceVerificationError("NETWORK_LISTENER_FORBIDDEN")

    declared_path = _require_string(payload, "main_scene_path")
    main_scene = _confined_path(root, declared_path)
    if not main_scene.is_file():
        raise EvidenceVerificationError("EVIDENCE_FILE_MISSING: main scene")
    before_hash = _require_string(payload, "main_scene_sha256_before")
    after_hash = _require_string(payload, "main_scene_sha256_after")
    actual_hash = sha256_file(main_scene)
    if before_hash != after_hash or after_hash != actual_hash:
        raise EvidenceVerificationError("ARTIFACT_BYTE_HASH_MISMATCH: main scene")

    return VerifiedMainInspectEvidence(
        repository=_require_string(payload, "repository"),
        source_commit=_require_string(payload, "source_commit"),
        base_pilot_commit=_require_string(payload, "base_pilot_commit"),
        main_scene_path=declared_path,
        main_scene_sha256=actual_hash,
        result_sha256=sha256_file(result_path),
    )


def verify_runtime_evidence(
    workspace: Path,
    runtime_result_path: Path,
) -> VerifiedRuntimeEvidence:
    result_path = Path(runtime_result_path).resolve()
    root = Path(workspace).resolve()
    payload = _load_evidence_payload(root, result_path)
    if payload.get("status") != "PASS":
        diagnostics = json.dumps(
            _bounded_failure_diagnostics(payload),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        raise EvidenceVerificationError(f"RUNTIME_EVIDENCE_FAILED: {diagnostics}")
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
    }
    path = destination / "project-pilot-evidence.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


__all__ = [
    "EvidenceVerificationError",
    "VerifiedMainInspectEvidence",
    "VerifiedRuntimeEvidence",
    "sha256_file",
    "verify_main_inspect_evidence",
    "verify_runtime_evidence",
    "write_final_evidence",
]
