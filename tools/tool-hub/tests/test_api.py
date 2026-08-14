from pathlib import Path
import subprocess

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


def test_platform_without_descriptor_runtime_starts_in_catalog_only_mode(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            launch_supported=False,
        )
    )

    response = client.get("/api/catalog")

    assert response.status_code == 200
    assert {
        item["tool_id"]: item["launch_state"] for item in response.json()["tools"]
    } == {
        "expression-studio": "BLOCKED_PLATFORM",
        "qa-evidence-studio": "BLOCKED_PLATFORM",
        "sprite-animation-studio": "BLOCKED_PLATFORM",
    }


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


def make_visual_project(root: Path, project_id: str) -> Path:
    project = make_project(root, project_id)
    anchors = project / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    anchors.parent.mkdir(exist_ok=True)
    anchors.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    subprocess.run(["git", "-C", str(project), "add", "docs/APPROVED_VISUAL_ANCHORS.json"], check=True)
    subprocess.run(["git", "-C", str(project), "commit", "-qm", "visual anchors"], check=True)
    return project


def test_visual_studios_launch_only_for_a_registered_verified_project(tmp_path: Path) -> None:
    project = make_visual_project(tmp_path / "Project With Spaces", "coc-fiction")
    client = client_for(tmp_path)
    with client:
        missing = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "coc-fiction"}
        )
        assert missing.status_code == 409

        assert client.post("/api/projects", json={"project_root": str(project)}).status_code == 201
        expression = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "coc-fiction"}
        )
        sprite = client.post(
            "/api/launch", json={"tool_id": "sprite-animation-studio", "project_id": "coc-fiction"}
        )

        assert expression.status_code == 200
        assert sprite.status_code == 200
        assert expression.json()["status"] == "RUNNING"
        assert sprite.json()["status"] == "RUNNING"
        assert expression.json()["url"] != sprite.json()["url"]
        assert str(project.resolve()) not in expression.text + sprite.text


def test_blocked_visual_start_cannot_affect_qa_or_another_project(tmp_path: Path) -> None:
    qa_project = make_project(tmp_path / "qa-project", "demo-game")
    visual_project = make_visual_project(tmp_path / "visual-project", "ten-paces-hidden-moves")
    client = client_for(tmp_path)
    with client:
        assert client.post("/api/projects", json={"project_root": str(qa_project)}).status_code == 201
        assert client.post("/api/projects", json={"project_root": str(visual_project)}).status_code == 201
        qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "demo-game"}
        )
        blocked = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "demo-game"}
        )
        other = client.post(
            "/api/launch",
            json={"tool_id": "sprite-animation-studio", "project_id": "ten-paces-hidden-moves"},
        )
        repeated_qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "demo-game"}
        )

        assert qa.status_code == 200
        assert blocked.status_code == 409
        assert other.status_code == 200
        assert repeated_qa.status_code == 200
        assert repeated_qa.json()["url"] == qa.json()["url"]
        assert other.json()["url"] != qa.json()["url"]
