from __future__ import annotations

from pathlib import Path

from base_tool_contracts import ProjectFigmaRegistry


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"

EXPECTED_LIVE_TARGETS = {
    "coc-fiction": ("12:2", "12:3"),
    "ten-paces-hidden-moves": ("22:2", "22:3"),
    "ninja-survival": ("12:2", "12:3"),
    "switchy-express-cargo-puzzle": ("11:2", "11:3"),
    "urban-legend": ("11:2", "11:3"),
    "grimoire-how-to-rewrite-the-world": ("8:2", "8:3"),
    "blacksmith": ("13:2", "13:3"),
    "omenward": ("10:2", "10:3"),
}


def test_live_verified_projects_route_to_their_exact_figma_delivery_areas() -> None:
    registry = ProjectFigmaRegistry.load(REGISTRY)
    registry.assert_canonical(ROOT)

    for project_id, (page_node_id, area_node_id) in EXPECTED_LIVE_TARGETS.items():
        assert registry.routing_state(project_id) == "ROUTING_CONFIGURED"
        target = registry.resolve_ready_target(project_id)
        assert target.delivery_page == "Sprite Animation Studio"
        assert target.generation_area == "Generated Assets"
        assert target.delivery_page_node_id == page_node_id
        assert target.generation_area_node_id == area_node_id
