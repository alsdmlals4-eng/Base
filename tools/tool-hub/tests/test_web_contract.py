from pathlib import Path

from fastapi.testclient import TestClient

from test_api import client_for
from test_projects import make_project


def test_hub_browser_is_project_first_and_has_no_raw_command_surface(tmp_path: Path) -> None:
    response = client_for(tmp_path).get("/")

    assert response.status_code == 200
    html = response.text
    assert 'id="project-registration"' in html
    assert 'id="tool-catalog"' in html
    assert "프로젝트를 먼저 연결" in html
    assert "QA Evidence Studio" in html
    assert "command" not in html.lower()
    assert "shell" not in html.lower()


def test_hub_api_launches_only_typed_qa_adapter(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    client = client_for(tmp_path)
    client.post("/api/projects", json={"project_root": str(project)})
    try:
        qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "demo-game"}
        )
        unsupported = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "demo-game"}
        )

        assert qa.status_code == 200
        assert qa.json()["url"].startswith("http://127.0.0.1:")
        assert unsupported.status_code == 409
        assert "not enabled in this vertical slice" in unsupported.json()["detail"]
    finally:
        client.close()
