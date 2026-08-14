from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from test_api import BASE_ROOT
from test_projects import make_project
from tool_hub.app import create_app


def test_client(tmp_path: Path) -> TestClient:
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


def registered_app_client(tmp_path: Path) -> TestClient:
    project = make_project(tmp_path / "Project", "coc-fiction")
    client = test_client(tmp_path)
    response = client.post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(project)},
    )
    assert response.status_code == 201
    return client


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
    assert browser.post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(project)},
    ).status_code == 201
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
