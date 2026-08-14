from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from base_tool_contracts import ProjectFigmaRegistry
from test_projects import make_project
from tool_hub.app import create_app
from tool_hub.figma_bridge import DeliveryReceipt, FigmaBridgeStore


BASE_ROOT = Path(__file__).resolve().parents[3]
PNG_BYTES = b"\x89PNG\r\n\x1a\nbridge-api-fixture"


def browser_client(tmp_path: Path, store: FigmaBridgeStore) -> TestClient:
    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            figma_bridge_store=store,
        )
    )
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]
    return client


def register_project(client: TestClient, tmp_path: Path, project_id: str = "urban-legend") -> None:
    project = make_project(tmp_path / project_id, project_id)
    response = client.post(
        "/api/projects",
        json={"project_id": project_id, "project_root": str(project)},
    )
    assert response.status_code == 201


def canonical_target(project_id: str = "urban-legend"):
    registry = ProjectFigmaRegistry.load(
        BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
    )
    return registry.resolve_ready_target(project_id)


def plugin_headers(token: str, file_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Figma-File-Key": file_key,
    }


def test_browser_creates_pairing_only_for_registered_project(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "bridge-private")
    client = browser_client(tmp_path, store)

    blocked = client.post("/api/figma-bridge/pairings", json={"project_id": "urban-legend"})
    register_project(client, tmp_path)
    created = client.post("/api/figma-bridge/pairings", json={"project_id": "urban-legend"})

    assert blocked.status_code == 409
    assert created.status_code == 201
    payload = created.json()
    assert payload["project_id"] == "urban-legend"
    assert payload["pairing_code"]
    assert "figma_url" in payload
    assert "generation_area_node_id" not in payload
    assert "figma_file_key" not in payload
    assert str(tmp_path) not in created.text


def test_plugin_exchange_uses_pairing_code_without_browser_csrf(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "bridge-private")
    browser = browser_client(tmp_path, store)
    register_project(browser, tmp_path)
    pairing = browser.post(
        "/api/figma-bridge/pairings", json={"project_id": "urban-legend"}
    ).json()
    file_key = canonical_target().figma_file_key

    plugin = TestClient(browser.app)
    response = plugin.post(
        "/api/figma-bridge/plugin/pairings/exchange",
        json={"pairing_code": pairing["pairing_code"], "current_file_key": file_key},
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == "urban-legend"
    assert response.json()["capability_token"]


def test_plugin_claim_artifact_and_receipt_require_route_bound_capability(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "bridge-private")
    browser = browser_client(tmp_path, store)
    register_project(browser, tmp_path)
    target = canonical_target()
    export = tmp_path / "urban-legend" / "AssetVault" / "candidate.png"
    export.parent.mkdir(parents=True, exist_ok=True)
    export.write_bytes(PNG_BYTES)
    job = store.enqueue(
        tool_id="expression-studio",
        project_id="urban-legend",
        run_id="run-001",
        export_path=export,
        target=target,
        media_type="image/png",
    )
    pairing = browser.post(
        "/api/figma-bridge/pairings", json={"project_id": "urban-legend"}
    ).json()
    plugin = TestClient(browser.app)
    exchange = plugin.post(
        "/api/figma-bridge/plugin/pairings/exchange",
        json={"pairing_code": pairing["pairing_code"], "current_file_key": target.figma_file_key},
    )
    token = exchange.json()["capability_token"]
    headers = plugin_headers(token, target.figma_file_key)

    unauthorized = plugin.get("/api/figma-bridge/plugin/jobs/next")
    claimed = plugin.get("/api/figma-bridge/plugin/jobs/next", headers=headers)
    artifact = plugin.get(
        f"/api/figma-bridge/plugin/jobs/{job.delivery_id}/artifact", headers=headers
    )
    receipt = DeliveryReceipt(
        delivery_id=job.delivery_id,
        project_id=job.project_id,
        figma_file_key=job.figma_file_key,
        generation_area_node_id=job.generation_area_node_id,
        created_node_id="99:1",
        artifact_sha256=job.artifact_sha256,
        artifact_byte_length=job.artifact_byte_length,
        width=32,
        height=32,
    )
    accepted = plugin.post(
        f"/api/figma-bridge/plugin/jobs/{job.delivery_id}/receipt",
        headers=headers,
        json=receipt.public_view(),
    )

    assert unauthorized.status_code == 401
    assert claimed.status_code == 200
    assert claimed.json()["delivery_id"] == job.delivery_id
    assert claimed.json()["generation_area_node_id"] == target.generation_area_node_id
    assert artifact.status_code == 200
    assert artifact.content == PNG_BYTES
    assert artifact.headers["content-type"].startswith("image/png")
    assert artifact.headers["etag"].strip('"') == job.artifact_sha256
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "FIGMA_DELIVERED_VERIFIED"


def test_wrong_file_key_cannot_claim_other_route(tmp_path: Path) -> None:
    store = FigmaBridgeStore(tmp_path / "bridge-private")
    browser = browser_client(tmp_path, store)
    register_project(browser, tmp_path)
    target = canonical_target()
    pairing = browser.post(
        "/api/figma-bridge/pairings", json={"project_id": "urban-legend"}
    ).json()
    plugin = TestClient(browser.app)
    exchange = plugin.post(
        "/api/figma-bridge/plugin/pairings/exchange",
        json={"pairing_code": pairing["pairing_code"], "current_file_key": target.figma_file_key},
    )
    token = exchange.json()["capability_token"]

    response = plugin.get(
        "/api/figma-bridge/plugin/jobs/next",
        headers=plugin_headers(token, "IhxUJaS6ik6MpBzdxt6o8D"),
    )

    assert response.status_code == 409
