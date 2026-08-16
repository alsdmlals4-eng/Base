from __future__ import annotations

import json
from pathlib import Path

import pytest

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry, ProjectFigmaToolRouteRegistry


BASE_ROOT = Path(__file__).resolve().parents[3]
PROJECT_REGISTRY = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
TOOL_REGISTRY = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json"


def _payload() -> dict[str, object]:
    return json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))


def _entry(payload: dict[str, object], project_id: str, route_id: str) -> dict[str, object]:
    entries = payload["entries"]
    assert isinstance(entries, list)
    return next(
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("project_id") == project_id
        and entry.get("tool_route_id") == route_id
    )


def _write(tmp_path: Path, payload: dict[str, object], name: str) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def test_sprite_route_destination_rename_is_rejected(tmp_path: Path) -> None:
    payload = _payload()
    _entry(payload, "urban-legend", "sprite_action_runs")["destination_name"] = "Effect Runs"

    with pytest.raises(ValueError, match="destination name"):
        ProjectFigmaToolRouteRegistry.load(_write(tmp_path, payload, "renamed.json"))


def test_project_marker_name_drift_is_rejected(tmp_path: Path) -> None:
    payload = _payload()
    _entry(payload, "urban-legend", "effect_runs")["project_marker_name"] = "Base Tool Hub Route · omenward"

    with pytest.raises(ValueError, match="marker"):
        ProjectFigmaToolRouteRegistry.load(_write(tmp_path, payload, "marker-drift.json"))


def test_route_reparent_is_rejected_against_project_authority(tmp_path: Path) -> None:
    payload = _payload()
    _entry(payload, "urban-legend", "effect_runs")["parent_node_id"] = "999:1"
    routes = ProjectFigmaToolRouteRegistry.load(_write(tmp_path, payload, "reparented.json"))
    projects = ProjectFigmaRegistry.load(PROJECT_REGISTRY)

    with pytest.raises(DeliveryBlockedError, match="parent"):
        routes.resolve_ready_route("urban-legend", "effect_runs", projects)
