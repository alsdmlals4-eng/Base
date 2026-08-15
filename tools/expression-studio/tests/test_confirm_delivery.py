from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from base_tool_contracts import ApprovedAnchorRegistry
from fastapi.testclient import TestClient
from PIL import Image

from expression_studio.app import create_app
from expression_studio.delivery import ProjectFigmaRegistry
from expression_studio.engine import FakeExpressionEngine
from expression_studio.hub_delivery import HubDeliveryError
from tests.test_delivery import write_registry
from tests.test_import_api import import_parts, png


class RecordingSender:
    def __init__(self, *, fail_count: int = 0) -> None:
        self.calls: list[tuple[str, bytes, str]] = []
        self.status_calls: list[str] = []
        self.fail_count = fail_count
        self.verified = False

    def __call__(self, run_id: str, image_bytes: bytes, media_type: str) -> dict[str, object]:
        self.calls.append((run_id, image_bytes, media_type))
        if self.fail_count:
            self.fail_count -= 1
            raise HubDeliveryError("temporary Tool Hub delivery failure")
        return {
            "delivery_id": "delivery-one",
            "status": "QUEUED",
            "tool_id": "expression-studio",
            "project_id": "demo",
            "run_id": run_id,
            "content_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "tool_route_id": "character_expression_runs",
            "target_node_name": "Expression Runs",
            "bridge_state": "PAIRING_REQUIRED",
            "delivery_state": "DELIVERY_PENDING",
            "figma_url": "https://www.figma.com/design/abc123/demo?node-id=10-3",
            "pairing_code": "123456",
            "pairing_expires_at": 9999999999.0,
        }

    def status(self, delivery_id: str) -> dict[str, object]:
        self.status_calls.append(delivery_id)
        if self.verified:
            return {
                "delivery_id": delivery_id,
                "status": "DELIVERED_VERIFIED",
                "tool_id": "expression-studio",
                "project_id": "demo",
                "run_id": "ignored-by-status-fixture",
                "content_sha256": "f" * 64,
                "tool_route_id": "character_expression_runs",
                "target_node_name": "Expression Runs",
                "bridge_state": "BRIDGE_PAIRED",
                "delivery_state": "FIGMA_DELIVERED_VERIFIED",
                "figma_url": "https://www.figma.com/design/abc123/demo?node-id=10-3",
            }
        return {
            "delivery_id": delivery_id,
            "status": "QUEUED",
            "tool_id": "expression-studio",
            "project_id": "demo",
            "run_id": "ignored-by-status-fixture",
            "content_sha256": "f" * 64,
            "tool_route_id": "character_expression_runs",
            "target_node_name": "Expression Runs",
            "bridge_state": "PAIRING_REQUIRED",
            "delivery_state": "DELIVERY_PENDING",
            "figma_url": "https://www.figma.com/design/abc123/demo?node-id=10-3",
            "pairing_code": "123456",
            "pairing_expires_at": 9999999999.0,
        }


def confirmed_client(project_root: Path, sender: RecordingSender) -> TestClient:
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    (project_root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
    (project_root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    approved = project_root / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    approved.parent.mkdir(parents=True, exist_ok=True)
    approved.write_text(
        json.dumps(
            {
                "version": 1,
                "entries": [
                    {
                        "project_id": "demo",
                        "source_path": "art/source/hero.png",
                        "figma_node_url": "https://www.figma.com/design/abc123/demo?node-id=1-2",
                        "source_sha256": hashlib.sha256(anchor.read_bytes()).hexdigest(),
                        "approval_state": "APPROVED",
                        "evidence": {
                            "kind": "EXPORTED_SNAPSHOT",
                            "ref": "test-approved-anchor",
                            "checked_at": "2026-08-15T00:00:00Z",
                        },
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", str(project_root)], check=True)
    subprocess.run(["git", "-C", str(project_root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(project_root), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(project_root), "add", ".gitignore", "art", "docs"], check=True)
    subprocess.run(["git", "-C", str(project_root), "commit", "-qm", "approved anchor"], check=True)
    figma_registry = ProjectFigmaRegistry.load(write_registry(project_root))
    anchor_registry = ApprovedAnchorRegistry.load(approved)
    app = create_app(
        project_root,
        FakeExpressionEngine(project_root),
        registry=figma_registry,
        project_id="demo",
        bind_origin="http://testserver",
        test_mode=True,
        anchor_registry=anchor_registry,
        run_mode="subscription_handoff_import",
        hub_delivery_sender=sender,
    )
    client = TestClient(app)
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Studio-CSRF"] = config["csrf_token"]
    return client


def imported_run(client: TestClient, selected: bytes, other: bytes) -> str:
    data, files = import_parts(selected, other)
    imported = client.post("/api/import-runs", data=data, files=files)
    assert imported.status_code == 201, imported.text
    return imported.json()["run_id"]


def test_confirm_and_deliver_exports_exact_selected_bytes_and_reports_bridge_required(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    other = png((30, 30, 220, 255))
    run_id = imported_run(client, selected, other)

    response = client.post(
        f"/api/runs/{run_id}/confirm-delivery",
        json={"selected_candidate": 0},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "CONFIRMED_BRIDGE_REQUIRED"
    assert body["project_save"] == "SAVED"
    assert body["figma_delivery"] == "BRIDGE_REQUIRED"
    assert body["bridge_state"] == "PAIRING_REQUIRED"
    assert body["delivery_state"] == "DELIVERY_PENDING"
    assert body["pairing_code"] == "123456"
    assert body["figma_url"].startswith("https://www.figma.com/design/")
    assert body["delivery_status_url"] == f"/api/runs/{run_id}/delivery-status"
    assert body["download_state"] == "DOWNLOAD_READY"
    assert body["download_url"] == f"/api/runs/{run_id}/confirmed-download"
    assert body["delivery_id"] == "delivery-one"
    assert body["tool_route_id"] == "character_expression_runs"
    assert body["target_node_name"] == "Expression Runs"
    assert body["content_sha256"] == hashlib.sha256(selected).hexdigest()
    assert body["provider_call_made"] is False
    assert sender.calls == [(run_id, selected, "image/png")]

    exported = list((tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio").rglob("selected.png"))
    assert len(exported) == 1
    assert exported[0].read_bytes() == selected


def test_delivery_status_refresh_promotes_cached_confirmation_to_verified(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    run_id = imported_run(client, selected, png((30, 30, 220, 255)))
    confirmed = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0}).json()

    sender.verified = True
    refreshed = client.get(confirmed["delivery_status_url"])
    retry = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})

    assert refreshed.status_code == 200, refreshed.text
    body = refreshed.json()
    assert body["status"] == "CONFIRMED_AND_VERIFIED"
    assert body["figma_delivery"] == "VERIFIED"
    assert body["bridge_state"] == "BRIDGE_PAIRED"
    assert body["delivery_state"] == "FIGMA_DELIVERED_VERIFIED"
    assert "pairing_code" not in body
    assert body["download_state"] == "DOWNLOAD_READY"
    assert retry.json() == body
    assert sender.status_calls == ["delivery-one"]
    assert len(sender.calls) == 1


def test_confirm_and_deliver_is_idempotent_after_success_and_browser_cannot_choose_route(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    other = png((30, 30, 220, 255))
    run_id = imported_run(client, selected, other)

    first = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    retry = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    changed = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 1})
    injected = client.post(
        f"/api/runs/{run_id}/confirm-delivery",
        json={"selected_candidate": 0, "target_node_id": "999:999", "figma_file_key": "attacker"},
    )

    assert first.status_code == 200
    assert retry.status_code == 200
    assert retry.json() == first.json()
    assert len(sender.calls) == 1
    assert sender.calls[0][1] == selected
    assert changed.status_code == 409
    assert injected.status_code == 422


def test_failed_hub_delivery_keeps_same_export_retryable(tmp_path: Path) -> None:
    sender = RecordingSender(fail_count=1)
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    run_id = imported_run(client, selected, png((30, 30, 220, 255)))

    failed = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    retry = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})

    assert failed.status_code == 409
    assert retry.status_code == 200, retry.text
    assert len(sender.calls) == 2
    assert sender.calls[0][1] == sender.calls[1][1] == selected


def test_confirmed_download_requires_confirmation_and_serves_exact_export(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    run_id = imported_run(client, selected, png((30, 30, 220, 255)))

    blocked = client.get(f"/api/runs/{run_id}/confirmed-download")
    confirmed = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    download = client.get(confirmed.json()["download_url"])

    assert blocked.status_code == 409
    assert confirmed.status_code == 200
    assert download.status_code == 200
    assert download.content == selected
    assert download.headers["content-type"].startswith("image/png")
    assert download.headers["content-disposition"].startswith("attachment;")
    assert ".png" in download.headers["content-disposition"]

    exported = next((tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio").rglob("selected.png"))
    exported.write_bytes(png((20, 200, 20, 255)))
    tampered = client.get(confirmed.json()["download_url"])
    assert tampered.status_code == 409


def test_legacy_figma_packet_is_blocked_after_direct_queue_confirmation(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    run_id = imported_run(client, png((220, 30, 30, 255)), png((30, 30, 220, 255)))

    confirmed = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    legacy = client.post(f"/api/runs/{run_id}/figma-delivery")

    assert confirmed.status_code == 200
    assert legacy.status_code == 409
    assert "already queued" in legacy.json()["detail"]


def test_delivery_credential_is_not_added_to_browser_config_or_status(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)

    combined = json.dumps(client.get("/api/config").json()) + json.dumps(client.get("/api/status").json())

    assert "BASE_TOOL_HUB_DELIVERY_TOKEN" not in combined
    assert "delivery_token" not in combined
