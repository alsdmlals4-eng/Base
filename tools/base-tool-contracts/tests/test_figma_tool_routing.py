from __future__ import annotations

import json
from pathlib import Path

import pytest

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry
from base_tool_contracts.figma_tool_routing import ProjectFigmaToolRouteRegistry


BASE_ROOT = Path(__file__).resolve().parents[3]
PROJECT_REGISTRY = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
TOOL_REGISTRY = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json"

EXPECTED = {
    "coc-fiction": ("12:3", "15:2", "25:2", "25:5", "23:2"),
    "ten-paces-hidden-moves": ("22:3", "28:2", "40:2", "40:5", "38:2"),
    "ninja-survival": ("12:3", "15:2", "22:2", "22:5", "20:2"),
    "switchy-express-cargo-puzzle": ("11:3", "14:2", "21:2", "21:5", "19:2"),
    "urban-legend": ("11:3", "14:2", "39:2", "39:5", "19:2"),
    "grimoire-how-to-rewrite-the-world": ("8:3", "11:2", "18:2", "18:5", "16:2"),
    "blacksmith": ("13:3", "18:2", "26:2", "26:5", "24:2"),
    "omenward": ("10:3", "13:2", "21:2", "21:5", "19:2"),
}
ROUTE_NAMES = {
    "character_expression_runs": "Expression Runs",
    "sprite_action_runs": "Sprite Action Runs",
    "effect_runs": "Effect Runs",
}


def registries():
    return ProjectFigmaRegistry.load(PROJECT_REGISTRY), ProjectFigmaToolRouteRegistry.load(TOOL_REGISTRY)


def test_all_eight_projects_have_three_exact_visual_routes() -> None:
    projects, routes = registries()
    assert routes.route_pairs() == {
        (project_id, route_id)
        for project_id in EXPECTED
        for route_id in ROUTE_NAMES
    }

    for project_id, (parent, expression, sprite, effect, marker) in EXPECTED.items():
        destinations = {
            "character_expression_runs": expression,
            "sprite_action_runs": sprite,
            "effect_runs": effect,
        }
        for route_id, destination in destinations.items():
            route = routes.resolve_ready_route(project_id, route_id, projects)
            target = projects.resolve_ready_target(project_id)
            assert route.figma_file_key == target.figma_file_key
            assert route.parent_node_id == parent == target.generation_area_node_id
            assert route.parent_node_type == "FRAME"
            assert route.destination_node_id == destination
            assert route.destination_node_type == "FRAME"
            assert route.destination_name == ROUTE_NAMES[route_id]
            assert route.project_marker_node_id == marker
            assert route.project_marker_node_type == "FRAME"
            assert route.project_marker_name == f"Base Tool Hub Route · {project_id}"
        assert len({expression, sprite, effect, parent, marker}) == 5


def test_missing_or_unreviewed_tool_route_fails_closed() -> None:
    projects, routes = registries()
    with pytest.raises(DeliveryBlockedError, match="tool route"):
        routes.resolve_ready_route("urban-legend", "not_a_reviewed_route", projects)
    with pytest.raises(DeliveryBlockedError, match="project"):
        routes.resolve_ready_route("not-a-project", "character_expression_runs", projects)


def test_tool_route_registry_proves_canonical_committed_bytes() -> None:
    _, routes = registries()
    routes.assert_canonical(BASE_ROOT)
    routes.assert_unchanged()


def test_cross_wired_project_parent_or_file_key_is_rejected(tmp_path: Path) -> None:
    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"][0]["parent_node_id"] = "999:1"
    bad_parent = tmp_path / "bad-parent.json"
    bad_parent.write_text(json.dumps(payload), encoding="utf-8")
    routes = ProjectFigmaToolRouteRegistry.load(bad_parent)
    projects = ProjectFigmaRegistry.load(PROJECT_REGISTRY)
    with pytest.raises(DeliveryBlockedError, match="parent"):
        routes.resolve_ready_route("coc-fiction", "character_expression_runs", projects)

    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"][0]["figma_file_key"] = "ABCDEFGHIJKLMNOPQRSTUV"
    bad_file = tmp_path / "bad-file.json"
    bad_file.write_text(json.dumps(payload), encoding="utf-8")
    routes = ProjectFigmaToolRouteRegistry.load(bad_file)
    with pytest.raises(DeliveryBlockedError, match="file"):
        routes.resolve_ready_route("coc-fiction", "character_expression_runs", projects)


def test_duplicate_route_and_invalid_node_shapes_are_rejected(tmp_path: Path) -> None:
    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"].append(dict(payload["entries"][0]))
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        ProjectFigmaToolRouteRegistry.load(duplicate)

    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"][0]["destination_node_id"] = payload["entries"][0]["parent_node_id"]
    same_node = tmp_path / "same-node.json"
    same_node.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="differ"):
        ProjectFigmaToolRouteRegistry.load(same_node)

    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"][0]["project_marker_node_id"] = payload["entries"][0]["destination_node_id"]
    same_marker = tmp_path / "same-marker.json"
    same_marker.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="marker"):
        ProjectFigmaToolRouteRegistry.load(same_marker)


def test_node_types_are_fixed_to_frame_for_the_reviewed_live_structure(tmp_path: Path) -> None:
    payload = json.loads(TOOL_REGISTRY.read_text(encoding="utf-8"))
    payload["entries"][0]["destination_node_type"] = "TEXT"
    bad_type = tmp_path / "bad-type.json"
    bad_type.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        ProjectFigmaToolRouteRegistry.load(bad_type)
