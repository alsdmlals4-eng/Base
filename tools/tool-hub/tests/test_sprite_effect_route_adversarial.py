from __future__ import annotations

import json

import pytest

from test_figma_delivery import png_bytes
from test_figma_exact_tool_route import BASE_ROOT, project_registry, service_for, tool_route_registry
from test_studio_delivery_trust import (
    _authorize_expression_child,
    _registered_hub,
    _studio_headers,
)
from tool_hub.figma_delivery import FigmaDeliveryService


def test_expression_child_cannot_request_effect_route(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = _registered_hub(tmp_path)
    _authorize_expression_child(monkeypatch)

    response = client.post(
        "/internal/studio-delivery/expression-effect-attack",
        content=png_bytes(2, 1),
        headers=_studio_headers("effect_runs"),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "DELIVERY_TOOL_ROUTE_UNAVAILABLE"


def test_recovered_sprite_job_without_stored_route_identity_is_rejected(tmp_path) -> None:
    service, project = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio",
        "omenward",
        "recovery-route-attack",
        png_bytes(2, 1),
        "image/png",
        tool_route_id="sprite_action_runs",
    )
    job_path = project / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "JOB.json"
    document = json.loads(job_path.read_text(encoding="utf-8"))
    for field in (
        "tool_route_id",
        "route_parent_node_id",
        "target_node_id",
        "target_node_name",
        "project_marker_node_id",
        "project_marker_name",
    ):
        document.pop(field, None)
    job_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    restarted = FigmaDeliveryService(
        tmp_path / "runtime",
        service._locator,
        project_registry(),
        tool_routes=tool_route_registry(),
        base_root=BASE_ROOT,
    )
    pairing = restarted.create_pairing("omenward")
    token = restarted.pair_by_code(pairing.pairing_code, "bridge-test").token

    assert restarted.claim_next(token) is None
    assert job_path.is_file()


def test_generic_parent_never_replaces_dedicated_sprite_destination(tmp_path) -> None:
    service, _ = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio",
        "omenward",
        "generic-parent-attack",
        png_bytes(2, 1),
        "image/png",
        tool_route_id="effect_runs",
    )

    assert job.target_node_name == "Effect Runs"
    assert job.target_node_id != job.generation_area_node_id
    assert job.route_parent_node_id == job.generation_area_node_id
