from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase

from .protocol import ProtocolError, normalize_contract_path


@dataclass(frozen=True)
class ScopeFinding:
    code: str
    path: str
    message: str


def _matches(pattern: str, path: str) -> bool:
    normalized_pattern = normalize_contract_path(pattern, "pattern")
    normalized_path = normalize_contract_path(path, "changed_path")
    if normalized_pattern.endswith("/**"):
        prefix = normalized_pattern[:-3].rstrip("/")
        return normalized_path == prefix or normalized_path.startswith(prefix + "/")
    if normalized_pattern.endswith("/"):
        prefix = normalized_pattern.rstrip("/")
        return normalized_path == prefix or normalized_path.startswith(prefix + "/")
    return fnmatchcase(normalized_path, normalized_pattern)


def validate_changed_paths(
    changed_paths: tuple[str, ...],
    allowed_patterns: tuple[str, ...],
    forbidden_patterns: tuple[str, ...],
) -> tuple[ScopeFinding, ...]:
    findings: list[ScopeFinding] = []
    for raw_path in changed_paths:
        try:
            path = normalize_contract_path(raw_path, "changed_path")
        except ProtocolError as exc:
            findings.append(ScopeFinding("UNSAFE_CHANGED_PATH", str(raw_path), str(exc)))
            continue
        if any(_matches(pattern, path) for pattern in forbidden_patterns):
            findings.append(ScopeFinding("FORBIDDEN_PATH_WRITE", path, "path matches an explicit forbidden pattern"))
            continue
        if not any(_matches(pattern, path) for pattern in allowed_patterns):
            findings.append(ScopeFinding("OUT_OF_SCOPE_WRITE", path, "path is not covered by an allowed pattern"))
    return tuple(findings)
