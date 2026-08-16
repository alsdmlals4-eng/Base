from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

import sprite_animation_studio.app as sprite_app
from sprite_animation_studio.app import create_app
from sprite_animation_studio.engine import FakeSpriteEngine
from sprite_animation_studio.service import RunBlockedError, SpriteAnimationService


class RecordingSender:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, str, str | None]] = []
        self.last: dict[str, object] | None = None
        self.verified = False

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
            "figma_url": "https://www.figma.com/design/abc123/demo",
        }
        return dict(self.last)

    def status(self, delivery_id: str) -> dict[str, object]:
        assert self.last is not None
        assert delivery_id == self.last["delivery_id"]
        current = dict(self.last)
        if self.verified:
            current["status"] = "DELIVERED_VERIFIED"
            current["bridge_state"] = "BRIDGE_PAIRED"
            current["delivery_state"] = "FIGMA_DELIVERED_VERIFIED"
        return current


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        ("pose_sequence", "sprite_action_runs"),
        ("sprite_action", "sprite_action_runs"),
        ("effect_stages", "effect_runs"),
    ],
)
def test_delivery_route_is_derived_only_from_server_owned_run_mode(
    tmp_path: Path, mode: str, expected: str
) -> None:
    service = SpriteAnimationService(tmp_path, FakeSpriteEngine(), project_id="demo")
    service._runs["run-one"] = SimpleNamespace(request=SimpleNamespace(mode=mode))  # type: ignore[assignment]

    assert service.delivery_route_id("run-one") == expected


def test_expression_variation_is_not_authorized_for_sprite_delivery(tmp_path: Path) -> None:
    service = SpriteAnimationService(tmp_path, FakeSpriteEngine(), project_id="demo")
    service._runs["run-one"] = SimpleNamespace(  # type: ignore[assignment]
        request=SimpleNamespace(mode="expression_variation")
    )

    with pytest.raises(RunBlockedError, match="DELIVERY_TOOL_ROUTE_UNAVAILABLE"):
        service.delivery_route_id("run-one")


def test_app_exposes_bodyless_confirm_status_and_download_endpoints(tmp_path: Path) -> None:
    sender = RecordingSender()
    app = create_app(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        bind_origin="http://testserver",
        test_mode=True,
        hub_delivery_sender=sender,
    )

    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/api/runs/{run_id}/confirm-delivery" in paths
    assert "/api/runs/{run_id}/delivery-status" in paths
    assert "/api/runs/{run_id}/confirmed-download" in paths


def _confirmed_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    sender: RecordingSender,
    *,
    atlas_bytes: bytes = b"reviewed-atlas-png-bytes",
    mode: str = "sprite_action",
) -> tuple[TestClient, SimpleNamespace]:
    atlas = tmp_path / ".asset-vault" / "runs" / "run-one" / "exports" / "atlas.png"
    atlas.parent.mkdir(parents=True, exist_ok=True)
    atlas.write_bytes(atlas_bytes)
    sha = hashlib.sha256(atlas_bytes).hexdigest()
    route = "effect_runs" if mode == "effect_stages" else "sprite_action_runs"
    record = SimpleNamespace(
        status="exported",
        export=SimpleNamespace(atlas=atlas),
        export_output_sha256={"atlas": sha},
        request=SimpleNamespace(project_id="demo", mode=mode),
        provider_call_made=False,
    )

    monkeypatch.setattr(SpriteAnimationService, "get_run", lambda _self, _run_id: record)
    monkeypatch.setattr(SpriteAnimationService, "prepare_figma_delivery", lambda _self, _run_id: SimpleNamespace())
    monkeypatch.setattr(SpriteAnimationService, "delivery_route_id", lambda _self, _run_id: route)

    def read_staged(_root: Path, path: Path, *, expected_sha256: str | None = None) -> bytes:
        data = path.read_bytes()
        if expected_sha256 is not None and hashlib.sha256(data).hexdigest() != expected_sha256:
            raise ValueError("staged file SHA-256 mismatch")
        return data

    monkeypatch.setattr(sprite_app, "_read_staged_file", read_staged)
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
    return client, record


def test_confirm_delivery_sends_exact_exported_atlas_and_same_sha(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sender = RecordingSender()
    atlas_bytes = b"exact-atlas-payload"
    client, record = _confirmed_client(tmp_path, monkeypatch, sender, atlas_bytes=atlas_bytes)

    response = client.post("/api/runs/run-one/confirm-delivery")

    assert response.status_code == 200, response.text
    body = response.json()
    expected_sha = hashlib.sha256(atlas_bytes).hexdigest()
    assert sender.calls == [("run-one", atlas_bytes, "image/png", "sprite_action_runs")]
    assert body["content_sha256"] == expected_sha == record.export_output_sha256["atlas"]
    assert body["tool_route_id"] == "sprite_action_runs"
    assert body["target_node_name"] == "Sprite Action Runs"
    assert body["download_url"] == "/api/runs/run-one/confirmed-download"
    assert body["delivery_status_url"] == "/api/runs/run-one/delivery-status"


def test_effect_confirm_delivery_uses_effect_route(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sender = RecordingSender()
    client, _ = _confirmed_client(tmp_path, monkeypatch, sender, mode="effect_stages")

    response = client.post("/api/runs/run-one/confirm-delivery")

    assert response.status_code == 200, response.text
    assert sender.calls[0][3] == "effect_runs"
    assert response.json()["target_node_name"] == "Effect Runs"


def test_delivery_status_and_download_remain_bound_to_confirmed_atlas(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sender = RecordingSender()
    atlas_bytes = b"atlas-for-status-and-download"
    client, _ = _confirmed_client(tmp_path, monkeypatch, sender, atlas_bytes=atlas_bytes)
    confirmed = client.post("/api/runs/run-one/confirm-delivery")
    assert confirmed.status_code == 200, confirmed.text

    sender.verified = True
    status = client.get("/api/runs/run-one/delivery-status")
    download = client.get("/api/runs/run-one/confirmed-download")

    assert status.status_code == 200, status.text
    assert status.json()["status"] == "CONFIRMED_AND_VERIFIED"
    assert status.json()["figma_delivery"] == "VERIFIED"
    assert download.status_code == 200
    assert download.content == atlas_bytes
    assert download.headers["X-Content-SHA256"] == hashlib.sha256(atlas_bytes).hexdigest()


def test_atlas_tamper_is_blocked_before_sender_invocation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sender = RecordingSender()
    client, record = _confirmed_client(tmp_path, monkeypatch, sender, atlas_bytes=b"original-atlas")
    record.export.atlas.write_bytes(b"tampered-atlas")

    response = client.post("/api/runs/run-one/confirm-delivery")

    assert response.status_code == 409
    assert sender.calls == []
