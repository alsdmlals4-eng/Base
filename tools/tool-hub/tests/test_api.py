from pathlib import Path

from fastapi.testclient import TestClient

from test_projects import make_project
from tool_hub.app import create_app


BASE_ROOT = Path(__file__).resolve().parents[3]


def client_for(tmp_path: Path, *, bootstrap: bool = True) -> TestClient:
    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
        )
    )
    client.headers["Origin"] = "http://testserver"
    if bootstrap:
        config = client.get("/api/config").json()
        client.headers["X-Hub-CSRF"] = config["csrf_token"]
    return client


def test_catalog_lists_reviewed_tools_and_redacts_registered_root(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces")
    client = client_for(tmp_path)

    created = client.post("/api/projects", json={"project_root": str(project)})
    catalog = client.get("/api/catalog").json()

    assert created.status_code == 201
    assert [item["tool_id"] for item in catalog["tools"]] == [
        "expression-studio",
        "qa-evidence-studio",
        "sprite-animation-studio",
    ]
    assert catalog["projects"][0]["project_id"] == "demo-game"
    assert str(project.resolve()) not in str(catalog)


def test_mutation_requires_exact_origin_session_and_csrf(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    raw = client_for(tmp_path, bootstrap=False)
    missing = raw.post("/api/projects", json={"project_root": str(project)})
    client = client_for(tmp_path)
    foreign = client.post(
        "/api/projects",
        json={"project_root": str(project)},
        headers={"Origin": "https://evil.example"},
    )
    hostile_host = client.post(
        "/api/projects", json={"project_root": str(project)}, headers={"Host": "evil.example"}
    )

    assert missing.status_code == 403
    assert foreign.status_code == 403
    assert hostile_host.status_code == 400


def test_project_registration_error_is_bounded(tmp_path: Path) -> None:
    response = client_for(tmp_path).post(
        "/api/projects", json={"project_root": str(tmp_path / "secret-path")}
    )

    assert response.status_code == 422
    assert str(tmp_path) not in response.json()["detail"]
