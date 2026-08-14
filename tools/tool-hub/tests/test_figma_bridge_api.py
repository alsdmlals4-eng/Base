from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from test_api import BASE_ROOT
from test_figma_delivery import png_bytes
from test_projects import make_project
from tool_hub.app import create_app


def _client_for_bridge_test(tmp_path: Path) -> TestClient:
    app = create_app(
        BASE_ROOT,
        tmp_path / "machine-projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        launch_supported=False,
    )
    client = TestClient(app)
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]
    return client


def _register(client: TestClient, project: Path, project_id: str) -> None:
    response = client.post(
        "/api/projects",
        json={"project_id": project_id, "project_root": str(project)},
    )
    assert response.status_code == 201


def registered_app_client(tmp_path: Path) -> TestClient:
    project = make_project(tmp_path / "Project", "coc-fiction")
    client = _client_for_bridge_test(tmp_path)
    _register(client, project, "coc-fiction")
    return client


def _pair(client: TestClient, project_id: str = "coc-fiction") -> tuple[str, TestClient]:
    pairing = client.post(f"/api/figma/pairing/{project_id}", json={})
    assert pairing.status_code == 200
    bridge = TestClient(client.app)
    paired = bridge.post(
        "/bridge/pair",
        json={"pairing_code": pairing.json()["pairing_code"], "bridge_version": "bridge-test"},
    )
    assert paired.status_code == 200
    return paired.json()["token"], bridge


def test_browser_pairing_derives_destination_from_registered_project(tmp_path: Path) -> None:
    client = registered_app_client(tmp_path)

    response = client.post("/api/figma/pairing/coc-fiction", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "coc-fiction"
    assert body["status"] == "PAIRING_REQUIRED"
    assert len(body["pairing_code"]) == 6
    assert body["figma_url"].startswith("https://www.figma.com/design/")
    assert "figma_file_key" not in body
    assert "generation_area_node_id" not in body

    injected = client.post(
        "/api/figma/pairing/coc-fiction",
        json={"figma_file_key": "attacker", "node_id": "999:999"},
    )
    assert injected.status_code == 422


def test_bridge_pair_uses_only_one_time_code_and_does_not_require_browser_session(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project", "coc-fiction")
    app = create_app(
        BASE_ROOT,
        tmp_path / "machine-projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        launch_supported=False,
    )
    browser = TestClient(app)
    browser.headers["Origin"] = "http://testserver"
    config = browser.get("/api/config").json()
    browser.headers["X-Hub-CSRF"] = config["csrf_token"]
    _register(browser, project, "coc-fiction")
    pairing = browser.post("/api/figma/pairing/coc-fiction", json={}).json()

    bridge = TestClient(app)
    paired = bridge.post(
        "/bridge/pair",
        json={"pairing_code": pairing["pairing_code"], "bridge_version": "bridge-test"},
    )

    assert paired.status_code == 200
    assert paired.json()["project_id"] == "coc-fiction"
    assert paired.json()["token"]
    assert "figma_file_key" not in paired.text
    assert "figma_url" not in paired.text
    assert pairing["pairing_code"] not in paired.text

    replay = bridge.post(
        "/bridge/pair",
        json={"pairing_code": pairing["pairing_code"], "bridge_version": "bridge-test"},
    )
    assert replay.status_code == 409

    injected = bridge.post(
        "/bridge/pair",
        json={
            "pairing_code": "000000",
            "bridge_version": "bridge-test",
            "project_id": "omenward",
            "figma_file_key": "attacker",
        },
    )
    assert injected.status_code == 422


def test_bridge_job_endpoint_requires_bearer_not_browser_csrf(tmp_path: Path) -> None:
    client = registered_app_client(tmp_path)

    response = client.get("/bridge/jobs/next")

    assert response.status_code == 401
    assert response.json()["detail"] == "BRIDGE_AUTH_REQUIRED"


def test_bridge_claim_content_release_round_trip_uses_exact_bytes(tmp_path: Path) -> None:
    client = registered_app_client(tmp_path)
    payload = png_bytes(2, 1)
    job = client.app.state.figma_delivery.enqueue(
        "expression-studio", "coc-fiction", "run-api", payload, "image/png"
    )
    token, bridge = _pair(client)
    auth = {"Authorization": f"Bearer {token}"}

    claimed = bridge.get("/bridge/jobs/next", headers=auth)
    assert claimed.status_code == 200
    body = claimed.json()
    assert body["status"] == "DELIVERY_PENDING"
    assert body["delivery_id"] == job.delivery_id
    assert body["content_sha256"] == job.content_sha256
    assert body["node_name"] == job.node_name
    assert "figma_file_key" not in body
    assert "figma_url" not in body
    assert "project_root" not in body

    content = bridge.get(f"/bridge/jobs/{job.delivery_id}/content", headers=auth)
    assert content.status_code == 200
    assert content.content == payload
    assert content.headers["content-type"].startswith("image/png")
    assert content.headers["x-content-sha256"] == job.content_sha256

    released = bridge.post(f"/bridge/jobs/{job.delivery_id}/release", json={}, headers=auth)
    assert released.status_code == 200
    assert released.json() == {"delivery_id": job.delivery_id, "status": "QUEUED"}
    assert bridge.get("/bridge/jobs/next", headers=auth).json()["delivery_id"] == job.delivery_id


def test_bridge_content_is_denied_across_projects(tmp_path: Path) -> None:
    coc = make_project(tmp_path / "Coc", "coc-fiction")
    omen = make_project(tmp_path / "Omen", "omenward")
    client = _client_for_bridge_test(tmp_path)
    _register(client, coc, "coc-fiction")
    _register(client, omen, "omenward")
    omen_job = client.app.state.figma_delivery.enqueue(
        "sprite-animation-studio", "omenward", "run-omen", png_bytes(2, 1), "image/png"
    )
    coc_token, coc_bridge = _pair(client, "coc-fiction")

    response = coc_bridge.get(
        f"/bridge/jobs/{omen_job.delivery_id}/content",
        headers={"Authorization": f"Bearer {coc_token}"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "DELIVERY_SCOPE_MISMATCH"


def test_bridge_receipt_finalizes_exact_claim_without_leaking_authority(tmp_path: Path) -> None:
    client = registered_app_client(tmp_path)
    job = client.app.state.figma_delivery.enqueue(
        "expression-studio", "coc-fiction", "run-receipt", png_bytes(), "image/png"
    )
    token, bridge = _pair(client)
    auth = {"Authorization": f"Bearer {token}"}
    claimed = bridge.get("/bridge/jobs/next", headers=auth).json()
    receipt_payload = {
        "created_node_id": "999:1000",
        "created_node_name": claimed["node_name"],
        "target_node_id": claimed["generation_area_node_id"],
        "content_sha256": claimed["content_sha256"],
        "bridge_version": "bridge-test",
        "image_hash": "figma-image-hash",
    }

    response = bridge.post(
        f"/bridge/jobs/{job.delivery_id}/receipt",
        json=receipt_payload,
        headers=auth,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["delivery_id"] == job.delivery_id
    assert body["status"] == "FIGMA_DELIVERED_VERIFIED"
    serialized = response.text
    assert token not in serialized
    assert "figma_file_key" not in serialized
    assert "project_root" not in serialized

    duplicate = bridge.post(
        f"/bridge/jobs/{job.delivery_id}/receipt",
        json=receipt_payload,
        headers=auth,
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"] == "DELIVERY_ALREADY_VERIFIED"

    injected = bridge.post(
        f"/bridge/jobs/{job.delivery_id}/receipt",
        json=receipt_payload | {"figma_file_key": "attacker"},
        headers=auth,
    )
    assert injected.status_code == 422


def test_browser_figma_status_is_redacted_and_project_scoped(tmp_path: Path) -> None:
    client = registered_app_client(tmp_path)
    client.app.state.figma_delivery.enqueue(
        "expression-studio", "coc-fiction", "run-status", png_bytes(), "image/png"
    )

    response = client.get("/api/figma/status/coc-fiction")

    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "coc-fiction"
    assert body["delivery_state"] == "DELIVERY_PENDING"
    assert body["pending_count"] == 1
    serialized = response.text
    for forbidden in ("pairing_code", "token", "figma_file_key", "generation_area_node_id", "project_root"):
        assert forbidden not in serialized
