#!/usr/bin/env python3
"""Stable facade for the declared player-surface plan validator.

The preserved core performs the original route, state, asset and CLI checks.
This facade adds cross-record invariants that require the complete packet at
once. Success remains structural evidence only, never runtime or approval proof.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Any

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
    """Return a canonical owner/repo identity; reject path-only dot segments."""
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip("/").casefold().removesuffix(".git")
    parts = value.split("/")
    if len(parts) != 2 or any(part in {".", ".."} for part in parts):
        return None
    return value if all(re.fullmatch(r"[a-z0-9_.-]+", part) for part in parts) else None


# The preserved core resolves this helper from its module globals at call time.
# Replacing it keeps self-reference and SOURCE_IDENTITY checks fail-closed.
_core._repository_key = _repository_key
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
