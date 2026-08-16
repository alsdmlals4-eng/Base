from __future__ import annotations

import pytest

from base_tool_contracts.hub_delivery import HubDeliveryError, LocalHubDeliveryClient


def _payload(run_id: str, route_id: str, target: str) -> dict[str, object]:
    return {
        "status": "QUEUED",
        "delivery_id": "1" * 32,
        "tool_id": "sprite-animation-studio" if route_id != "character_expression_runs" else "expression-studio",
        "project_id": "demo",
        "run_id": run_id,
        "content_sha256": "2" * 64,
        "tool_route_id": route_id,
        "target_node_name": target,
        "bridge_state": "BRIDGE_PAIRED",
        "delivery_state": "DELIVERY_PENDING",
        "figma_url": "https://www.figma.com/design/abc123/demo",
    }


def test_sprite_route_is_sent_only_as_bounded_private_header(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LocalHubDeliveryClient("http://127.0.0.1:8764", "t" * 32)
    captured: dict[str, object] = {}

    def fake_request(path: str, **kwargs: object) -> dict[str, object]:
        captured["path"] = path
        captured.update(kwargs)
        return _payload("run-effect", "effect_runs", "Effect Runs")

    monkeypatch.setattr(client, "_json_request", fake_request)

    result = client("run-effect", b"atlas", "image/png", "effect_runs")

    assert result["tool_route_id"] == "effect_runs"
    assert captured["path"] == "/internal/studio-delivery/run-effect"
    assert captured["extra_headers"] == {"X-Base-Tool-Route": "effect_runs"}
    assert captured["content_type"] == "image/png"
    assert captured["data"] == b"atlas"


def test_expression_legacy_three_argument_call_sends_no_route_header(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LocalHubDeliveryClient("http://127.0.0.1:8764", "t" * 32)
    captured: dict[str, object] = {}

    def fake_request(path: str, **kwargs: object) -> dict[str, object]:
        captured["path"] = path
        captured.update(kwargs)
        return _payload("run-expression", "character_expression_runs", "Expression Runs")

    monkeypatch.setattr(client, "_json_request", fake_request)

    result = client("run-expression", b"selected", "image/png")

    assert result["tool_route_id"] == "character_expression_runs"
    assert captured["extra_headers"] == {}


def test_invalid_route_header_identity_is_rejected_before_request(monkeypatch: pytest.MonkeyPatch) -> None:
    client = LocalHubDeliveryClient("http://127.0.0.1:8764", "t" * 32)
    called = False

    def fake_request(path: str, **kwargs: object) -> dict[str, object]:
        nonlocal called
        called = True
        return {}

    monkeypatch.setattr(client, "_json_request", fake_request)

    with pytest.raises(HubDeliveryError, match="route identity"):
        client("run-invalid", b"atlas", "image/png", "Effect Runs")

    assert called is False
