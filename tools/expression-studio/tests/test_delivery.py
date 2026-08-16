import json
from pathlib import Path

import pytest
from base_tool_contracts import ProjectFigmaRegistry as SharedProjectFigmaRegistry

from expression_studio.delivery import DeliveryBlockedError, ProjectFigmaRegistry


def test_expression_studio_uses_the_shared_figma_registry_owner() -> None:
    assert ProjectFigmaRegistry is SharedProjectFigmaRegistry


def write_registry(tmp_path: Path, *, status: str = "READY_FOR_DELIVERY") -> Path:
    payload = {
        "version": 1,
        "default_delivery_page": "Sprite Animation Studio",
        "default_generation_area": "Generated Assets",
        "entries": [
            {
                "project_id": "demo",
                "display_name": "Demo",
                "repository_url": "https://github.com/example/demo.git",
                "figma_file_key": "abc123",
                "figma_url": "https://www.figma.com/design/abc123/demo?node-id=0-1",
                "delivery_status": status,
                "delivery_page_node_id": "10:2",
                "generation_area_node_id": "10:3",
            }
        ],
    }
    target = tmp_path / "figma-targets.json"
    target.write_text(json.dumps(payload), encoding="utf-8")
    return target


def test_registry_resolves_only_a_ready_project_target(tmp_path: Path) -> None:
    target = ProjectFigmaRegistry.load(write_registry(tmp_path)).resolve_ready_target("demo")

    assert target.figma_file_key == "abc123"
    assert target.generation_area_node_id == "10:3"


def test_registry_blocks_a_protected_target_without_fallback(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path, status="REGISTERED_NO_MUTATION"))

    with pytest.raises(DeliveryBlockedError, match="REGISTERED_NO_MUTATION"):
        registry.resolve_ready_target("demo")


def test_registry_rejects_a_url_whose_file_key_does_not_match(tmp_path: Path) -> None:
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["figma_url"] = "https://www.figma.com/design/wrong-key/demo?node-id=0-1"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="does not match"):
        ProjectFigmaRegistry.load(path)


def test_registry_rejects_malformed_or_identical_figma_target_node_ids(tmp_path: Path) -> None:
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["generation_area_node_id"] = "not-a-figma-node"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="node ID"):
        ProjectFigmaRegistry.load(path)

    payload["entries"][0]["generation_area_node_id"] = payload["entries"][0]["delivery_page_node_id"]
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="must differ"):
        ProjectFigmaRegistry.load(path)


def test_base_registry_keeps_all_reviewed_project_figma_targets_ready() -> None:
    base_root = Path(__file__).parents[3]
    registry = ProjectFigmaRegistry.load(base_root / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json")

    for project_id in (
        "coc-fiction",
        "ten-paces-hidden-moves",
        "ninja-survival",
        "switchy-express-cargo-puzzle",
        "urban-legend",
        "grimoire-how-to-rewrite-the-world",
        "blacksmith",
        "omenward",
    ):
        assert registry.routing_state(project_id) == "ROUTING_CONFIGURED"
        target = registry.resolve_ready_target(project_id)
        assert target.project_id == project_id
        assert target.generation_area_node_id
