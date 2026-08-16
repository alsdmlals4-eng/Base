from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from sprite_animation_studio.app import create_app
from sprite_animation_studio.engine import FakeSpriteEngine
from sprite_animation_studio.service import RunBlockedError, SpriteAnimationService


class RecordingSender:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, str, str | None]] = []
        self.last: dict[str, object] | None = None

    def __call__(
        self,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        tool_route_id: str | None = None,
    ) -> dict[str, object]:
        self.calls.append((run_id, image_bytes, media_type, tool_route_id))
        target = {
            "sprite_action_runs": "Sprite Action Runs",
            "effect_runs": "Effect Runs",
        }[str(tool_route_id)]
        self.last = {
            "status": "QUEUED",
            "delivery_id": "1" * 32,
            "tool_id": "sprite-animation-studio",
            "project_id": "demo",
            "run_id": run_id,
            "content_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "tool_route_id": tool_route_id,
            "target_node_name": target,
            "bridge_state": "BRIDGE_PAIRED",
            "delivery_state": "DELIVERY_PENDING",
            "figma_url": "https://www.figma.com/design/abc123/example",
        }
        return dict(self.last)

    def status(self, delivery_id: str) -> dict[str, object]:
        assert self.last is not None
        assert delivery_id == self.last["delivery_id"]
        verified = dict(self.last)
        verified["status"] = "DELIVERED_VERIFIED"
        verified["bridge_state"] = "BRIDGE_PAIRED"
        verified["delivery_state"] = "FIGMA_DELIVERED_VERIFIED"
        return verified


def _service_with_mode(tmp_path: Path, mode: str) -> SpriteAnimationService:
    service = SpriteAnimationService(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        run_mode="subscription_handoff_import",
    )
    service._runs["run-route"] = SimpleNamespace(request=SimpleNamespace(mode=mode))  # type: ignore[assignment]
    return service


@pytest.mark.parametrize("mode", ["pose_sequence", "sprite_action"])
def test_sprite_action_modes_derive_sprite_action_route(tmp_path: Path, mode: str) -> None:
    service = _service_with_mode(tmp_path, mode)

    assert service.delivery_route_id("run-route") == "sprite_action_runs"


def test_effect_stages_derives_effect_route(tmp_path: Path) -> None:
    service = _service_with_mode(tmp_path, "effect_stages")

    assert service.delivery_route_id("run-route") == "effect_runs"


def test_expression_variation_has_no_dedicated_sprite_delivery_route(tmp_path: Path) -> None:
    service = _service_with_mode(tmp_path, "expression_variation")

    with pytest.raises(RunBlockedError, match="DELIVERY_TOOL_ROUTE_UNAVAILABLE"):
        service.delivery_route_id("run-route")


def _client_for_confirmed_atlas(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    mode: str,
    sender: RecordingSender,
) -> tuple[TestClient, str, Path, bytes]:
    run_id = f"run-{mode.replace('_', '-')}"
    atlas_bytes = b"\x89PNG\r\n\x1a\nreviewed-atlas-bytes"
    atlas_path = tmp_path / ".asset-vault" / "staging" / "sprite-test" / "exports" / "atlas.png"
    atlas_path.parent.mkdir(parents=True, exist_ok=True)
    atlas_path.write_bytes(atlas_bytes)
    expected_sha = hashlib.sha256(atlas_bytes).hexdigest()
    record = SimpleNamespace(
        run_id=run_id,
        status="exported",
        export=SimpleNamespace(atlas=atlas_path),
        export_output_sha256={"atlas": expected_sha},
        request=SimpleNamespace(mode=mode, project_id="demo"),
        provider_call_made=False,
    )

    monkeypatch.setattr(SpriteAnimationService, "get_run", lambda self, value: record if value == run_id else None)
    monkeypatch.setattr(SpriteAnimationService, "prepare_figma_delivery", lambda self, value: SimpleNamespace())

    app = create_app(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        bind_origin="http://testserver",
        test_mode=True,
        hub_delivery_sender=sender,
    )
    client = TestClient(app)
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Studio-CSRF"] = config["csrf_token"]
    return client, run_id, atlas_path, atlas_bytes


@pytest.mark.parametrize(
    ("mode", "expected_route", "expected_target"),
    [
        ("pose_sequence", "sprite_action_runs", "Sprite Action Runs"),
        ("sprite_action", "sprite_action_runs", "Sprite Action Runs"),
        ("effect_stages", "effect_runs", "Effect Runs"),
    ],
)
def test_confirm_delivery_sends_exact_exported_atlas_and_route(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    expected_route: str,
    expected_target: str,
) -> None:
    sender = RecordingSender()
    client, run_id, _atlas_path, atlas_bytes = _client_for_confirmed_atlas(
        tmp_path,
        monkeypatch,
        mode=mode,
        sender=sender,
    )

    response = client.post(f"/api/runs/{run_id}/confirm-delivery")

    assert response.status_code == 200, response.text
    assert sender.calls == [(run_id, atlas_bytes, "image/png", expected_route)]
    body = response.json()
    assert body["content_sha256"] == hashlib.sha256(atlas_bytes).hexdigest()
    assert body["tool_route_id"] == expected_route
    assert body["target_node_name"] == expected_target
    assert body["download_url"] == f"/api/runs/{run_id}/confirmed-download"
    assert body["delivery_status_url"] == f"/api/runs/{run_id}/delivery-status"


def test_confirm_delivery_blocks_expression_variation_without_sender_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sender = RecordingSender()
    client, run_id, _atlas_path, _atlas_bytes = _client_for_confirmed_atlas(
        tmp_path,
        monkeypatch,
        mode="expression_variation",
        sender=sender,
    )

    response = client.post(f"/api/runs/{run_id}/confirm-delivery")

    assert response.status_code == 409
    assert response.json()["detail"] == "DELIVERY_TOOL_ROUTE_UNAVAILABLE"
    assert sender.calls == []


def test_confirm_delivery_detects_atlas_tamper_before_sender_invocation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sender = RecordingSender()
    client, run_id, atlas_path, _atlas_bytes = _client_for_confirmed_atlas(
        tmp_path,
        monkeypatch,
        mode="effect_stages",
        sender=sender,
    )
    atlas_path.write_bytes(b"changed-after-export")

    response = client.post(f"/api/runs/{run_id}/confirm-delivery")

    assert response.status_code == 409
    assert sender.calls == []
