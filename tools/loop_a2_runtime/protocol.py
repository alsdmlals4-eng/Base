from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Any, Mapping

_ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_DRIVE_RE = re.compile(r"^[A-Za-z]:[/\\]")


class ProtocolError(ValueError):
    """Raised when a worker or review message expands authority or is malformed."""


def _exact_keys(value: Mapping[str, Any], expected: set[str], role: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ProtocolError(
            f"{role} keys mismatch: unknown={sorted(actual - expected)}, "
            f"missing={sorted(expected - actual)}"
        )


def _string(value: Any, field: str, *, nonempty: bool = True, max_length: int = 4096) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise ProtocolError(f"{field} must be a non-empty string")
    if len(value) > max_length:
        raise ProtocolError(f"{field} exceeds {max_length} characters")
    return value


def _identifier(value: Any, field: str) -> str:
    result = _string(value, field, max_length=64)
    if not _ID_RE.fullmatch(result):
        raise ProtocolError(f"{field} is not a bounded uppercase identifier")
    return result


def _sha(value: Any, field: str) -> str:
    result = _string(value, field, max_length=40)
    if not _SHA_RE.fullmatch(result):
        raise ProtocolError(f"{field} must be a lowercase 40-hex SHA")
    return result


def normalize_contract_path(value: Any, field: str) -> str:
    raw = _string(value, field, max_length=1024)
    if "\x00" in raw:
        raise ProtocolError(f"{field} contains NUL")
    normalized = unicodedata.normalize("NFC", raw).replace("\\", "/")
    if normalized.startswith("/") or _DRIVE_RE.match(raw):
        raise ProtocolError(f"{field} must be project-relative")
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ProtocolError(f"{field} contains an unsafe path segment")
    return "/".join(parts)


def normalize_contract_pattern(value: Any, field: str) -> str:
    raw = _string(value, field, max_length=1024)
    if "\x00" in raw:
        raise ProtocolError(f"{field} contains NUL")
    normalized = unicodedata.normalize("NFC", raw).replace("\\", "/")
    if normalized.startswith("/") or _DRIVE_RE.match(raw):
        raise ProtocolError(f"{field} must be project-relative")
    trailing_directory = normalized.endswith("/")
    core = normalized[:-1] if trailing_directory else normalized
    if not core:
        raise ProtocolError(f"{field} contains an unsafe path segment")
    parts = core.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ProtocolError(f"{field} contains an unsafe path segment")
    return normalized


def _path_tuple(value: Any, field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ProtocolError(
            f"{field} must be a {'possibly empty' if allow_empty else 'non-empty'} list"
        )
    if len(value) > 256:
        raise ProtocolError(f"{field} exceeds 256 entries")
    result = tuple(normalize_contract_path(item, f"{field}[]") for item in value)
    if len(set(result)) != len(result):
        raise ProtocolError(f"{field} contains duplicates")
    return result


def _pattern_tuple(value: Any, field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ProtocolError(
            f"{field} must be a {'possibly empty' if allow_empty else 'non-empty'} list"
        )
    if len(value) > 256:
        raise ProtocolError(f"{field} exceeds 256 entries")
    result = tuple(normalize_contract_pattern(item, f"{field}[]") for item in value)
    if len(set(result)) != len(result):
        raise ProtocolError(f"{field} contains duplicates")
    return result


def _id_tuple(value: Any, field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ProtocolError(
            f"{field} must be a {'possibly empty' if allow_empty else 'non-empty'} list"
        )
    if len(value) > 256:
        raise ProtocolError(f"{field} exceeds 256 entries")
    result = tuple(_identifier(item, f"{field}[]") for item in value)
    if len(set(result)) != len(result):
        raise ProtocolError(f"{field} contains duplicates")
    return result


@dataclass(frozen=True)
class Budgets:
    max_turns: int
    max_repair_cycles: int
    timeout_seconds: int

    @classmethod
    def from_dict(cls, value: Any) -> "Budgets":
        if not isinstance(value, dict):
            raise ProtocolError("budgets must be an object")
        _exact_keys(
            value,
            {"max_turns", "max_repair_cycles", "timeout_seconds"},
            "budgets",
        )
        if not isinstance(value["max_turns"], int) or not 1 <= value["max_turns"] <= 50:
            raise ProtocolError("max_turns must be 1..50")
        if (
            not isinstance(value["max_repair_cycles"], int)
            or not 0 <= value["max_repair_cycles"] <= 5
        ):
            raise ProtocolError("max_repair_cycles must be 0..5")
        if (
            not isinstance(value["timeout_seconds"], int)
            or not 1 <= value["timeout_seconds"] <= 3600
        ):
            raise ProtocolError("timeout_seconds must be 1..3600")
        return cls(
            value["max_turns"],
            value["max_repair_cycles"],
            value["timeout_seconds"],
        )


@dataclass(frozen=True)
class RunRequest:
    schema_version: int
    contract_role: str
    project_id: str
    run_id: str
    package_id: str
    expected_main_sha: str
    capsule_path: str
    package_path: str
    allowed_paths: tuple[str, ...]
    forbidden_paths: tuple[str, ...]
    resource_locks: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    budgets: Budgets
    provider_mode: str

    _KEYS = {
        "schema_version",
        "contract_role",
        "project_id",
        "run_id",
        "package_id",
        "expected_main_sha",
        "capsule_path",
        "package_path",
        "allowed_paths",
        "forbidden_paths",
        "resource_locks",
        "requirement_ids",
        "budgets",
        "provider_mode",
    }

    @classmethod
    def from_dict(cls, value: Any) -> "RunRequest":
        if not isinstance(value, dict):
            raise ProtocolError("run request must be an object")
        _exact_keys(value, cls._KEYS, "run request")
        if (
            value["schema_version"] != 1
            or value["contract_role"] != "LOOP_A2_RUN_REQUEST"
        ):
            raise ProtocolError("unsupported run request contract")
        provider_mode = _string(
            value["provider_mode"],
            "provider_mode",
            max_length=8,
        )
        if provider_mode not in {"FAKE", "REAL"}:
            raise ProtocolError("provider_mode must be FAKE or REAL")
        return cls(
            1,
            "LOOP_A2_RUN_REQUEST",
            _identifier(value["project_id"], "project_id"),
            _identifier(value["run_id"], "run_id"),
            _identifier(value["package_id"], "package_id"),
            _sha(value["expected_main_sha"], "expected_main_sha"),
            normalize_contract_path(value["capsule_path"], "capsule_path"),
            normalize_contract_path(value["package_path"], "package_path"),
            _pattern_tuple(value["allowed_paths"], "allowed_paths"),
            _pattern_tuple(
                value["forbidden_paths"],
                "forbidden_paths",
                allow_empty=True,
            ),
            _id_tuple(value["resource_locks"], "resource_locks"),
            _id_tuple(value["requirement_ids"], "requirement_ids"),
            Budgets.from_dict(value["budgets"]),
            provider_mode,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "contract_role": self.contract_role,
            "project_id": self.project_id,
            "run_id": self.run_id,
            "package_id": self.package_id,
            "expected_main_sha": self.expected_main_sha,
            "capsule_path": self.capsule_path,
            "package_path": self.package_path,
            "allowed_paths": list(self.allowed_paths),
            "forbidden_paths": list(self.forbidden_paths),
            "resource_locks": list(self.resource_locks),
            "requirement_ids": list(self.requirement_ids),
            "budgets": {
                "max_turns": self.budgets.max_turns,
                "max_repair_cycles": self.budgets.max_repair_cycles,
                "timeout_seconds": self.budgets.timeout_seconds,
            },
            "provider_mode": self.provider_mode,
        }


@dataclass(frozen=True)
class WorkerError:
    code: str
    message: str

    @classmethod
    def from_dict(cls, value: Any) -> "WorkerError":
        if not isinstance(value, dict):
            raise ProtocolError("worker error must be an object")
        _exact_keys(value, {"code", "message"}, "worker error")
        return cls(
            _identifier(value["code"], "error.code"),
            _string(
                value["message"],
                "error.message",
                max_length=2048,
            ),
        )


@dataclass(frozen=True)
class WorkerResult:
    schema_version: int
    contract_role: str
    project_id: str
    run_id: str
    package_id: str
    expected_main_sha: str
    role: str
    status: str
    changed_paths: tuple[str, ...]
    summary: str
    usage: Mapping[str, int]
    errors: tuple[WorkerError, ...]

    _KEYS = {
        "schema_version",
        "contract_role",
        "project_id",
        "run_id",
        "package_id",
        "expected_main_sha",
        "role",
        "status",
        "changed_paths",
        "summary",
        "usage",
        "errors",
    }

    @classmethod
    def from_dict(cls, value: Any) -> "WorkerResult":
        if not isinstance(value, dict):
            raise ProtocolError("worker result must be an object")
        _exact_keys(value, cls._KEYS, "worker result")
        if (
            value["schema_version"] != 1
            or value["contract_role"] != "LOOP_A2_WORKER_RESULT"
        ):
            raise ProtocolError("unsupported worker result contract")
        if value["role"] != "BUILDER":
            raise ProtocolError("worker role must be BUILDER")
        status = value["status"]
        if status not in {"COMPLETED", "FAILED", "BLOCKED"}:
            raise ProtocolError("unsupported worker status")
        usage = value["usage"]
        if not isinstance(usage, dict):
            raise ProtocolError("usage must be an object")
        _exact_keys(usage, {"turns"}, "usage")
        if (
            not isinstance(usage["turns"], int)
            or not 0 <= usage["turns"] <= 50
        ):
            raise ProtocolError("usage.turns must be 0..50")
        raw_errors = value["errors"]
        if not isinstance(raw_errors, list) or len(raw_errors) > 64:
            raise ProtocolError(
                "errors must be a list with at most 64 entries"
            )
        errors = tuple(WorkerError.from_dict(item) for item in raw_errors)
        if status == "COMPLETED" and errors:
            raise ProtocolError(
                "COMPLETED worker result cannot contain errors"
            )
        if status in {"FAILED", "BLOCKED"} and not errors:
            raise ProtocolError(
                f"{status} worker result must contain at least one error"
            )
        return cls(
            1,
            "LOOP_A2_WORKER_RESULT",
            _identifier(value["project_id"], "project_id"),
            _identifier(value["run_id"], "run_id"),
            _identifier(value["package_id"], "package_id"),
            _sha(value["expected_main_sha"], "expected_main_sha"),
            "BUILDER",
            status,
            _path_tuple(
                value["changed_paths"],
                "changed_paths",
                allow_empty=True,
            ),
            _string(value["summary"], "summary", max_length=2048),
            {"turns": usage["turns"]},
            errors,
        )


@dataclass(frozen=True)
class ReviewFinding:
    code: str
    severity: str
    message: str
    paths: tuple[str, ...]
    requirement_ids: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Any) -> "ReviewFinding":
        if not isinstance(value, dict):
            raise ProtocolError("review finding must be an object")
        _exact_keys(
            value,
            {"code", "severity", "message", "paths", "requirement_ids"},
            "review finding",
        )
        severity = _string(
            value["severity"],
            "finding.severity",
            max_length=2,
        )
        if severity not in {"P0", "P1", "P2"}:
            raise ProtocolError("finding severity must be P0, P1, or P2")
        return cls(
            _identifier(value["code"], "finding.code"),
            severity,
            _string(
                value["message"],
                "finding.message",
                max_length=2048,
            ),
            _path_tuple(
                value["paths"],
                "finding.paths",
                allow_empty=True,
            ),
            _id_tuple(
                value["requirement_ids"],
                "finding.requirement_ids",
                allow_empty=True,
            ),
        )


@dataclass(frozen=True)
class ReviewResult:
    schema_version: int
    contract_role: str
    project_id: str
    run_id: str
    package_id: str
    expected_main_sha: str
    role: str
    verdict: str
    findings: tuple[ReviewFinding, ...]
    checked_requirement_ids: tuple[str, ...]

    _KEYS = {
        "schema_version",
        "contract_role",
        "project_id",
        "run_id",
        "package_id",
        "expected_main_sha",
        "role",
        "verdict",
        "findings",
        "checked_requirement_ids",
    }

    @classmethod
    def from_dict(cls, value: Any) -> "ReviewResult":
        if not isinstance(value, dict):
            raise ProtocolError("review result must be an object")
        _exact_keys(value, cls._KEYS, "review result")
        if (
            value["schema_version"] != 1
            or value["contract_role"] != "LOOP_A2_REVIEW_RESULT"
        ):
            raise ProtocolError("unsupported review result contract")
        if value["role"] != "CRITIC":
            raise ProtocolError("review role must be CRITIC")
        verdict = _string(value["verdict"], "verdict", max_length=32)
        if verdict not in {
            "PASS",
            "MUST_FIX",
            "USER_DECISION_REQUIRED",
            "BLOCKED_UNVERIFIED",
        }:
            raise ProtocolError("unsupported review verdict")
        raw_findings = value["findings"]
        if not isinstance(raw_findings, list) or len(raw_findings) > 128:
            raise ProtocolError(
                "findings must be a list with at most 128 entries"
            )
        findings = tuple(
            ReviewFinding.from_dict(item) for item in raw_findings
        )
        if verdict == "PASS" and findings:
            raise ProtocolError("PASS review result cannot contain findings")
        if verdict != "PASS" and not findings:
            raise ProtocolError(
                f"{verdict} review result must contain at least one finding"
            )
        return cls(
            1,
            "LOOP_A2_REVIEW_RESULT",
            _identifier(value["project_id"], "project_id"),
            _identifier(value["run_id"], "run_id"),
            _identifier(value["package_id"], "package_id"),
            _sha(value["expected_main_sha"], "expected_main_sha"),
            "CRITIC",
            verdict,
            findings,
            _id_tuple(
                value["checked_requirement_ids"],
                "checked_requirement_ids",
                allow_empty=True,
            ),
        )
