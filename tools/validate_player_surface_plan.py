#!/usr/bin/env python3
"""Stable facade for the declared player-surface plan validator.

The preserved core performs the original route, state, asset and CLI checks.
This facade adds cross-record invariants that require the complete packet at
once. Success remains structural evidence only, never runtime or approval proof.
"""
from __future__ import annotations

import importlib.util
import re
from ipaddress import IPv4Address, ip_address
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

_CORE_PATH = Path(__file__).with_name("validate_player_surface_plan_core.py")
_SPEC = importlib.util.spec_from_file_location("_player_surface_plan_core", _CORE_PATH)
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - checkout corruption
    raise ImportError(f"cannot load player-surface validator core: {_CORE_PATH}")
_core = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_core)

CEILING = _core.CEILING
MAX_PACKET_BYTES = _core.MAX_PACKET_BYTES
MAX_RECORDS = _core.MAX_RECORDS


def _repository_key(value: Any) -> str | None:
    """Return one canonical owner/repo identity; reject path-navigation tokens."""
    if not isinstance(value, str) or not value or value != value.strip():
        return None
    normalized = value.casefold()
    if normalized.startswith("/") or normalized.endswith("/"):
        return None
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    parts = normalized.split("/")
    if len(parts) != 2 or any(part in {"", ".", ".."} for part in parts):
        return None
    return normalized if all(re.fullmatch(r"[a-z0-9_.-]+", part) for part in parts) else None


def _normalized_url_parts(path: str) -> list[str] | None:
    """Decode bounded URL escaping and resolve RFC-style dot segments."""
    decoded = path
    for _ in range(4):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    if any(ord(char) < 32 or ord(char) == 127 for char in decoded) or "\\" in decoded:
        return None
    parts: list[str] = []
    for part in decoded.split("/"):
        if part in {"", "."}:
            continue
        if part == "..":
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)
    return parts


def _legacy_ipv4(host: str) -> IPv4Address | None:
    """Parse inet_aton-style decimal/octal/hex IPv4 forms without DNS."""
    pieces = host.split(".")
    if not 1 <= len(pieces) <= 4 or any(
        not re.fullmatch(r"(?:0[xX][0-9a-fA-F]+|[0-9]+)", piece) for piece in pieces
    ):
        return None
    values: list[int] = []
    try:
        for piece in pieces:
            if piece.lower().startswith("0x"):
                values.append(int(piece, 16))
            elif len(piece) > 1 and piece.startswith("0"):
                values.append(int(piece, 8))
            else:
                values.append(int(piece, 10))
    except ValueError:
        return None

    limits = {
        1: (0xFFFFFFFF,),
        2: (0xFF, 0xFFFFFF),
        3: (0xFF, 0xFF, 0xFFFF),
        4: (0xFF, 0xFF, 0xFF, 0xFF),
    }[len(values)]
    if any(value > limit for value, limit in zip(values, limits)):
        return None
    if len(values) == 1:
        packed = values[0]
    elif len(values) == 2:
        packed = (values[0] << 24) | values[1]
    elif len(values) == 3:
        packed = (values[0] << 24) | (values[1] << 16) | values[2]
    else:
        packed = (
            (values[0] << 24)
            | (values[1] << 16)
            | (values[2] << 8)
            | values[3]
        )
    return IPv4Address(packed)


def _source_repository(host: str, parts: list[str]) -> str | None:
    if host in {"github.com", "www.github.com", "raw.githubusercontent.com", "codeload.github.com"}:
        return _repository_key("/".join(parts[:2])) if len(parts) >= 2 else None
    if host == "api.github.com":
        if len(parts) < 3 or parts[0] != "repos":
            return None
        return _repository_key("/".join(parts[1:3]))
    return None


def _external_source(row: dict[str, Any], project: Any) -> bool:
    """Validate public locator/repository identity, not authenticity or chronology."""
    source = row.get("source")
    project_key = _repository_key(project)
    if project_key is None or not isinstance(source, str) or not source.strip():
        return False
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in source):
        return False
    try:
        url = urlsplit(source)
        host = (url.hostname or "").casefold().rstrip(".")
        if url.scheme not in {"http", "https"} or not host:
            return False
        if url.username is not None or url.password is not None:
            return False
        url.port  # Reject malformed ports without connecting.
    except ValueError:
        return False

    try:
        address = ip_address(host)
    except ValueError:
        address = _legacy_ipv4(host)
        if address is None and all(
            re.fullmatch(r"(?:0[xX][0-9a-fA-F]+|[0-9]+)", piece)
            for piece in host.split(".")
        ):
            return False
    if address is not None:
        if not address.is_global:
            return False
    elif "." not in host or host.endswith((".local", ".localhost")) or host == "localhost":
        return False

    parts = _normalized_url_parts(url.path)
    if parts is None:
        return False
    repository = _source_repository(host, parts)
    declared = row.get("source_repository")
    if declared is not None:
        declared_key = _repository_key(declared)
        if declared_key is None or (repository is not None and repository != declared_key):
            return False
        repository = declared_key
    elif row.get("evidence_kind") == "SOURCE_CODE" and repository is None:
        # Non-GitHub repository-hosted code needs an explicit canonical identity.
        return False
    return repository is None or repository != project_key


# The preserved core resolves these helpers from its module globals at call time.
# Replacing them keeps identity and origin checks fail-closed without duplicating
# the route/state/asset validator.
_core._repository_key = _repository_key
_core._external_source = _external_source
_core_validate_packet = _core.validate_packet


def _records(packet: dict[str, Any], name: str) -> list[dict[str, Any]]:
    value = packet.get(name)
    if not isinstance(value, list) or len(value) > MAX_RECORDS:
        return []
    return [item for item in value if isinstance(item, dict)]


def _raster_target_ownership_errors(packet: dict[str, Any]) -> list[str]:
    """Require every composed raster part to be owned on that target surface."""
    modules = {
        row.get("id")
        for row in _records(packet, "modules")
        if isinstance(row.get("id"), str) and row.get("id")
    }
    owned_targets: dict[str, set[str]] = {module_id: set() for module_id in modules}
    for family in _records(packet, "visual_families"):
        if family.get("production") == "NATIVE_UI":
            continue
        targets = family.get("surfaces")
        module_ids = family.get("module_ids")
        if not isinstance(targets, list) or not isinstance(module_ids, list):
            continue
        valid_targets = {target for target in targets if isinstance(target, str) and target}
        for module_id in module_ids:
            if isinstance(module_id, str) and module_id in modules:
                owned_targets[module_id].update(valid_targets)

    unowned: set[tuple[str, str]] = set()
    for composition in _records(packet, "compositions"):
        surface = composition.get("surface")
        parts = composition.get("parts")
        if not isinstance(surface, str) or not surface or not isinstance(parts, list):
            continue
        for part in parts:
            if not isinstance(part, dict):
                continue
            module_id = part.get("module_id")
            if (isinstance(module_id, str) and module_id in modules
                    and surface not in owned_targets.get(module_id, set())):
                unowned.add((surface, module_id))
    return [
        f"RASTER_MODULE_TARGET_UNOWNED: {surface}/{module_id}"
        for surface, module_id in sorted(unowned)
    ]


def validate_packet(packet: Any, gate: str = "plan") -> list[str]:
    """Run core validation plus final repository and raster-consumer invariants."""
    errors = list(_core_validate_packet(packet, gate))
    if not isinstance(packet, dict):
        return errors
    if _repository_key(packet.get("repository")) is None and not any(
        error.startswith("SOURCE_IDENTITY:") for error in errors
    ):
        errors.append(
            "SOURCE_IDENTITY: version, derived role, exact revision, canonical "
            "owner/repo, owner and approval locator required"
        )
    errors.extend(_raster_target_ownership_errors(packet))
    return errors


# The core CLI owns bounded JSON parsing and structured argument errors. Point
# its runtime call at the facade so direct imports and CLI execution are equal.
_core.validate_packet = validate_packet


def main() -> int:
    return _core.main()


if __name__ == "__main__":
    raise SystemExit(main())
