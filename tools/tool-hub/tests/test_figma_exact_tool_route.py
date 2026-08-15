from __future__ import annotations

from pathlib import Path

import pytest

from base_tool_contracts import (
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectFigmaToolRouteRegistry,
)
from test_figma_delivery import paired_token, png_bytes
from test_projects import make_project
from tool_hub.figma_delivery import BridgeReceipt, DeliveryError, FigmaDeliveryService
from tool_hub.projects import ProjectLocator


BASE_ROOT = Path(__file__).resolve().parents[3]
PROJECT_REGISTRY_PATH = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
TOOL_ROUTE_REGISTRY_PATH = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json"


def project_registry() -> ProjectFigmaRegistry:
    return ProjectFigmaRegistry.load(PROJECT_REGISTRY_PATH)


def tool_route_registry() -> ProjectFigmaToolRouteRegistry:
    return ProjectFigmaToolRouteRegistry.load(TOOL_ROUTE_REGISTRY_PATH)


def service_for(tmp_path: Path, project_id: str = "coc-fiction") -> tuple[FigmaDeliveryService, Path]:
    project = make_project(tmp_path / "project", project_id)
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, project_id)
    service = FigmaDeliveryService(
        tmp_path / "runtime",
        locator,
        project_registry(),
        tool_routes=tool_route_registry(),
        base_root=BASE_ROOT,
    )
    return service, project


def test_expression_delivery_binds_exact_character_expression_destination(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path)
    job = service.enqueue("expression-studio", "coc-fiction", "run-character", png_bytes(), "image/png")
    route = tool_route_registry().resolve_ready_route(
        "coc-fiction",
        "character_expression_runs",
        project_registry(),
    )

    assert job.tool_route_id == "character_expression_runs"
    assert job.route_parent_node_id == route.parent_node_id
    assert job.target_node_id == route.destination_node_id
    assert job.target_node_name == route.destination_name
    assert job.project_marker_node_id == route.project_marker_node_id
    assert job.project_marker_name == route.project_marker_name
    assert job.target_node_id != job.generation_area_node_id


def test_receipt_must_confirm_exact_tool_destination_not_generic_generation_area(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path)
    token = paired_token(service, "coc-fiction")
    job = service.enqueue("expression-studio", "coc-fiction", "run-receipt", png_bytes(), "image/png")
    claimed = service.claim_next(token)
    assert claimed is not None

    with pytest.raises(DeliveryError, match="FIGMA_TARGET_MISMATCH"):
        service.finalize(
            token,
            job.delivery_id,
            BridgeReceipt(
                "999:1",
                claimed.node_name,
                claimed.generation_area_node_id,
                claimed.content_sha256,
                "bridge-test",
                "image-hash",
            ),
        )

    receipt = service.finalize(
        token,
        job.delivery_id,
        BridgeReceipt(
            "999:1",
            claimed.node_name,
            claimed.target_node_id,
            claimed.content_sha256,
            "bridge-test",
            "image-hash",
        ),
    )
    assert receipt.target_node_id == claimed.target_node_id
    assert receipt.target_node_id != claimed.generation_area_node_id


def test_sprite_delivery_fails_closed_until_a_dedicated_tool_route_exists(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path, "omenward")

    with pytest.raises(DeliveryError, match="DELIVERY_TOOL_ROUTE_UNAVAILABLE"):
        service.enqueue(
            "sprite-animation-studio",
            "omenward",
            "run-sprite-action",
            png_bytes(),
            "image/png",
        )


def test_claim_revalidates_exact_tool_route_before_exposing_job(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = service_for(tmp_path)
    token = paired_token(service, "coc-fiction")
    service.enqueue("expression-studio", "coc-fiction", "run-route-drift", png_bytes(), "image/png")

    def route_changed() -> None:
        raise DeliveryBlockedError("Figma tool-route registry changed after loading")

    monkeypatch.setattr(service._tool_routes, "assert_unchanged", route_changed)

    with pytest.raises(DeliveryError, match="DELIVERY_TOOL_ROUTE_UNAVAILABLE"):
        service.claim_next(token)


def test_bridge_plugin_and_api_use_exact_target_and_route_identity() -> None:
    plugin = (BASE_ROOT / "tools" / "figma-bridge" / "code.js").read_text(encoding="utf-8")
    app = (BASE_ROOT / "tools" / "tool-hub" / "src" / "tool_hub" / "app.py").read_text(encoding="utf-8")

    assert "job.target_node_id" in plugin
    assert "job.route_parent_node_id" in plugin
    assert "job.project_marker_node_id" in plugin
    assert "job.target_node_name" in plugin
    assert "job.project_marker_name" in plugin
    assert "getNodeByIdAsync(job.generation_area_node_id)" not in plugin

    for field in (
        '"tool_route_id": job.tool_route_id',
        '"route_parent_node_id": job.route_parent_node_id',
        '"target_node_id": job.target_node_id',
        '"target_node_name": job.target_node_name',
        '"project_marker_node_id": job.project_marker_node_id',
        '"project_marker_name": job.project_marker_name',
    ):
        assert field in app
