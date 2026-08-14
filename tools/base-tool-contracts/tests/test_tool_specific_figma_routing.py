from __future__ import annotations

import json
from pathlib import Path

import pytest

from base_tool_contracts import ProjectFigmaRegistry


ROOT = Path(__file__).parents[3]
CANONICAL = ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"

EXPECTED_EXPRESSION_NODES = {
    "coc-fiction": "15:2",
    "ten-paces-hidden-moves": "28:2",
    "ninja-survival": "15:2",
    "switchy-express-cargo-puzzle": "14:2",
    "urban-legend": "14:2",
    "grimoire-how-to-rewrite-the-world": "11:2",
    "blacksmith": "18:2",
    "omenward": "13:2",
}


def test_canonical_registry_routes_expression_to_live_inspected_nodes() -> None:
    registry = ProjectFigmaRegistry.load(CANONICAL)

    for project_id, expected_node in EXPECTED_EXPRESSION_NODES.items():
        target = registry.resolve_ready_target(project_id)
        assert target.node_for_tool("expression-studio") == expected_node
        assert target.tool_destinations["expression-studio"] == expected_node


def test_unmapped_sprite_route_falls_back_to_generation_area() -> None:
    registry = ProjectFigmaRegistry.load(CANONICAL)
    target = registry.resolve_ready_target("urban-legend")

    assert target.node_for_tool("sprite-animation-studio") == target.generation_area_node_id


def test_tool_destination_rejects_malformed_tool_or_node(tmp_path: Path) -> None:
    payload = json.loads(CANONICAL.read_text(encoding="utf-8"))
    payload["entries"] = [dict(payload["entries"][0])]
    payload["entries"][0]["project_id"] = "demo"
    payload["entries"][0]["repository_url"] = "https://github.com/example/demo.git"
    payload["entries"][0]["tool_destinations"] = {"Expression Studio": "999:999"}
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError):
        ProjectFigmaRegistry.load(path)

    payload["entries"][0]["tool_destinations"] = {"expression-studio": "not-a-node"}
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError):
        ProjectFigmaRegistry.load(path)
