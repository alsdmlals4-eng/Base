"""Validate the reviewed Base interactive-tool manifest without executing it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

from jsonschema import Draft202012Validator


class RegistryError(ValueError):
    """Raised when registry data expands the reviewed execution boundary."""


_FIELDS = {
    "tool_id",
    "display_name",
    "audience",
    "owner_path",
    "launch_adapter",
    "health_path",
    "project_scoped",
    "capabilities",
    "production_engine_required_for_delivery",
}
_ADAPTERS = {"expression_studio", "qa_evidence_studio", "sprite_animation_studio"}
_REVIEWED_TUPLES = {
    "expression-studio": (
        "tools/expression-studio",
        "expression_studio",
        ("expression_variation", "image_import", "figma_delivery_packet"),
    ),
    "qa-evidence-studio": (
        "tools/qa-evidence-studio",
        "qa_evidence_studio",
        ("developer_pc_review", "image_evidence", "qa_evidence_packet"),
    ),
    "sprite-animation-studio": (
        "tools/sprite-animation-studio",
        "sprite_animation_studio",
        ("sprite_action", "expression_variation", "pose_sequence", "effect_stages"),
    ),
}
_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_CAPABILITY = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RegistryError("registry must be readable UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise RegistryError("registry root must be an object")
    return payload


def load_registry(base_root: Path, registry_path: Path) -> tuple[dict[str, object], ...]:
    root = base_root.resolve()
    payload = _load_json(registry_path)
    if set(payload) - {"$schema", "schema_version", "tools"}:
        raise RegistryError("registry root contains an unknown field")
    if payload.get("schema_version") != 1 or not isinstance(payload.get("tools"), list):
        raise RegistryError("registry schema_version 1 and tools array are required")
    seen: set[str] = set()
    reviewed: list[dict[str, object]] = []
    for raw in payload["tools"]:
        if not isinstance(raw, dict):
            raise RegistryError("tool entry must be an object")
        unknown = set(raw) - _FIELDS
        if unknown:
            raise RegistryError(f"tool entry contains an unknown field: {sorted(unknown)[0]}")
        missing = _FIELDS - set(raw)
        if missing:
            raise RegistryError(f"tool entry is missing required field: {sorted(missing)[0]}")
        tool_id = raw["tool_id"]
        if not isinstance(tool_id, str) or not _ID.fullmatch(tool_id):
            raise RegistryError("tool_id is invalid")
        if tool_id in seen:
            raise RegistryError(f"duplicate tool_id: {tool_id}")
        seen.add(tool_id)
        owner_value = raw["owner_path"]
        if not isinstance(owner_value, str) or Path(owner_value).is_absolute():
            raise RegistryError("owner_path must be relative")
        owner_relative = Path(owner_value)
        if ".." in owner_relative.parts:
            raise RegistryError("owner_path traversal is forbidden")
        if len(owner_relative.parts) != 2 or owner_relative.parts[0] != "tools":
            raise RegistryError("owner_path must be one direct tools directory")
        owner = (root / owner_relative).resolve()
        if root not in owner.parents or not owner.is_dir():
            raise RegistryError("owner directory does not exist inside Base")
        adapter = raw["launch_adapter"]
        if adapter not in _ADAPTERS:
            raise RegistryError("launch adapter is not reviewed")
        if raw["audience"] != "HUMAN_INTERACTIVE" or raw["health_path"] != "/api/status" or raw["project_scoped"] is not True:
            raise RegistryError("interactive tool boundary fields are invalid")
        capabilities = raw["capabilities"]
        if not isinstance(capabilities, list) or not capabilities or any(
            not isinstance(item, str) or not _CAPABILITY.fullmatch(item) for item in capabilities
        ):
            raise RegistryError("capabilities must be non-empty reviewed identifiers")
        if len(set(capabilities)) != len(capabilities):
            raise RegistryError("capabilities must be unique")
        reviewed_tuple = _REVIEWED_TUPLES.get(tool_id)
        if reviewed_tuple is None or (
            owner_value,
            adapter,
            tuple(capabilities),
        ) != reviewed_tuple:
            raise RegistryError("tool must use its fixed reviewed tuple")
        if not isinstance(raw["display_name"], str) or not raw["display_name"]:
            raise RegistryError("display_name is required")
        if not isinstance(raw["production_engine_required_for_delivery"], bool):
            raise RegistryError("production engine flag must be boolean")
        reviewed.append(dict(raw))
    try:
        schema = _load_json(root / "schemas" / "base-tool-registry-v1.schema.json")
        schema_errors = list(Draft202012Validator(schema).iter_errors(payload))
    except (OSError, ValueError) as error:
        raise RegistryError("tool registry schema owner is unreadable") from error
    if schema_errors:
        raise RegistryError("tool registry does not conform to its schema owner")
    return tuple(sorted(reviewed, key=lambda item: str(item["tool_id"])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--registry", type=Path)
    args = parser.parse_args()
    registry = args.registry or args.base_root / "tools" / "TOOL_REGISTRY.json"
    try:
        tools = load_registry(args.base_root, registry)
    except RegistryError as error:
        print(f"Tool registry invalid: {error}")
        return 1
    print(f"Tool registry valid: {len(tools)} reviewed interactive tools")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
