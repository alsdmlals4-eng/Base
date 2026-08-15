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
from tests.test_delivery import write_registry
from tests.test_import_api import import_parts, png


class RecordingSender:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, str]] = []

    def __call__(self, run_id: str, image_bytes: bytes, media_type: str) -> dict[str, object]:
        self.calls.append((run_id, image_bytes, media_type))
        return {
            "delivery_id": "delivery-one",
            "status": "QUEUED",
            "tool_id": "expression-studio",
            "project_id": "demo",
            "run_id": run_id,
            "content_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "tool_route_id": "character_expression_runs",
            "target_node_name": "Expression Runs",
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


def test_confirm_and_deliver_exports_exact_selected_bytes_and_queues_them(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    other = png((30, 30, 220, 255))
    data, files = import_parts(selected, other)
    imported = client.post("/api/import-runs", data=data, files=files)
    assert imported.status_code == 201, imported.text
    run_id = imported.json()["run_id"]

    response = client.post(
        f"/api/runs/{run_id}/confirm-delivery",
        json={"selected_candidate": 0},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "CONFIRMED_AND_QUEUED"
    assert body["project_save"] == "SAVED"
    assert body["figma_delivery"] == "QUEUED"
    assert body["delivery_id"] == "delivery-one"
    assert body["tool_route_id"] == "character_expression_runs"
    assert body["target_node_name"] == "Expression Runs"
    assert body["content_sha256"] == hashlib.sha256(selected).hexdigest()
    assert sender.calls == [(run_id, selected, "image/png")]

    exported = list((tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio").rglob("selected.png"))
    assert len(exported) == 1
    assert exported[0].read_bytes() == selected


def test_confirm_and_deliver_can_retry_same_export_but_browser_cannot_choose_route(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    selected = png((220, 30, 30, 255))
    data, files = import_parts(selected, png((30, 30, 220, 255)))
    run_id = client.post("/api/import-runs", data=data, files=files).json()["run_id"]

    first = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    retry = client.post(f"/api/runs/{run_id}/confirm-delivery", json={"selected_candidate": 0})
    injected = client.post(
        f"/api/runs/{run_id}/confirm-delivery",
        json={"selected_candidate": 0, "target_node_id": "999:999", "figma_file_key": "attacker"},
    )

    assert first.status_code == 200
    assert retry.status_code == 200
    assert len(sender.calls) == 2
    assert sender.calls[0][1] == sender.calls[1][1] == selected
    assert injected.status_code == 422


def test_delivery_credential_is_not_added_to_browser_config_or_status(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)

    combined = json.dumps(client.get("/api/config").json()) + json.dumps(client.get("/api/status").json())

    assert "BASE_TOOL_HUB_DELIVERY_TOKEN" not in combined
    assert "delivery_token" not in combined
