import json
from pathlib import Path

import pytest
from base_tool_contracts import ProjectFigmaRegistry as SharedProjectFigmaRegistry

from sprite_animation_studio.delivery import DeliveryBlockedError, ProjectFigmaRegistry


def test_sprite_studio_uses_the_shared_figma_registry_owner() -> None:
    assert ProjectFigmaRegistry is SharedProjectFigmaRegistry


def write_registry(tmp_path: Path, *, status: str = "READY_FOR_DELIVERY") -> Path:
    registry = {
        "version": 1,
        "default_delivery_page": "Sprite Animation Studio",
        "default_generation_area": "Generated Assets",
        "entries": [
            {
                "project_id": "demo",
                "display_name": "Demo",
                "figma_file_key": "abc123",
                "figma_url": "https://www.figma.com/design/abc123/demo?node-id=0-1",
                "delivery_status": status,
                "delivery_page_node_id": "10:2",
                "generation_area_node_id": "10:3",
            }
        ],
    }
    path = tmp_path / "figma-targets.json"
    path.write_text(json.dumps(registry), encoding="utf-8")
    return path


def test_registry_resolves_only_a_ready_project_target(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))

    target = registry.resolve_ready_target("demo")

    assert target.figma_file_key == "abc123"
    assert target.delivery_page == "Sprite Animation Studio"
    assert target.generation_area == "Generated Assets"
    assert target.generation_area_node_id == "10:3"


def test_registry_blocks_a_protected_target_without_fallback(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path, status="REGISTERED_NO_MUTATION"))

    with pytest.raises(DeliveryBlockedError, match="REGISTERED_NO_MUTATION"):
        registry.resolve_ready_target("demo")


def test_registry_blocks_unknown_project_id(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))

    with pytest.raises(DeliveryBlockedError, match="not registered"):
        registry.resolve_ready_target("not-demo")


def test_registry_rejects_duplicate_project_id(tmp_path: Path) -> None:
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"].append(dict(payload["entries"][0]))
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate project_id"):
        ProjectFigmaRegistry.load(path)


def test_registry_rejects_a_url_whose_file_key_does_not_match(tmp_path: Path) -> None:
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["figma_url"] = "https://www.figma.com/design/wrong-key/demo?node-id=0-1"
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="does not match"):
        ProjectFigmaRegistry.load(path)


@pytest.mark.parametrize(
    ("page_node_id", "area_node_id"),
    [("invalid", "10:3"), ("10:2", "10:2")],
)
def test_registry_rejects_malformed_or_identical_figma_node_ids(
    tmp_path: Path, page_node_id: str, area_node_id: str
) -> None:
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["delivery_page_node_id"] = page_node_id
    payload["entries"][0]["generation_area_node_id"] = area_node_id
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError, match="node IDs"):
        ProjectFigmaRegistry.load(path)


def test_base_registry_keeps_all_unverified_project_figma_targets_blocked() -> None:
    base_root = Path(__file__).parents[3]
    registry = ProjectFigmaRegistry.load(base_root / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json")

    project_ids = ("coc-fiction", "ten-paces-hidden-moves", "ninja-survival", "switchy-express-cargo-puzzle", "urban-legend", "grimoire-how-to-rewrite-the-world", "blacksmith", "omenward")
    for project_id in project_ids:
        assert registry.routing_state(project_id) == "ROUTING_BLOCKED"
        with pytest.raises(DeliveryBlockedError, match="REGISTERED_NO_MUTATION"):
            registry.resolve_ready_target(project_id)
