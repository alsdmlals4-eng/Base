from pathlib import Path

from test_api import client_for
from test_projects import make_project


WEB_ROOT = Path(__file__).resolve().parents[1] / "web"


def web_source(name: str) -> str:
    return (WEB_ROOT / name).read_text(encoding="utf-8")


def test_hub_warns_that_reviewed_runtime_must_not_be_edited_during_launch() -> None:
    html = web_source("index.html")

    assert "동일 OS 사용자 계정과 기기 관리자는 신뢰 대상" in html
    assert "도구 실행 중 Base·Studio 파일을 편집하지 마세요" in html
    assert "HARDENED_RUNTIME_DEFERRED" in html


def test_hub_browser_is_project_first_and_has_no_raw_command_surface(tmp_path: Path) -> None:
    response = client_for(tmp_path).get("/")

    assert response.status_code == 200
    html = response.text
    assert 'id="project-registration"' in html
    assert 'id="known-project"' in html
    assert 'id="registered-project-list"' in html
    assert 'id="tool-catalog"' in html
    assert "프로젝트를 먼저 연결" in html
    assert "QA Evidence Studio" in html
    assert "Expression Studio" in html
    assert "Sprite Animation Studio" in html
    assert "ROUTING_REGISTERED" in html
    assert "ANCHOR_EVIDENCE_MISSING" in html
    assert "BLOCKED_UNVERIFIED" in html
    assert "INCLUDED_OR_LOCAL_HANDOFF" in html
    assert "Figma 업로드 증거가 아닙니다" in html
    assert "AI 생성 증거가 아닙니다" in html
    assert "command" not in html.lower()
    assert "shell" not in html.lower()
    assert "<iframe" not in html.lower()
    assert "marketplace" not in html.lower()
    assert "balance" not in html.lower()
    assert "C:\\" not in html
    assert "/home/" not in html


def test_catalog_marks_all_three_reviewed_child_adapters_runnable(tmp_path: Path) -> None:
    catalog = client_for(tmp_path).get("/api/catalog").json()

    assert {
        item["tool_id"]: item["launch_state"] for item in catalog["tools"]
    } == {
        "expression-studio": "RUNNABLE",
        "qa-evidence-studio": "RUNNABLE",
        "sprite-animation-studio": "RUNNABLE",
    }
    assert "project_root" not in str(catalog)
    assert "launch_nonce" not in str(catalog)


def test_browser_uses_text_only_labels_and_project_tool_scoped_child_state() -> None:
    script = web_source("app.js")

    assert "innerHTML" not in script
    assert "button.textContent = `${project.display_name} · ${project.state}`" in script
    assert "const childStates = new Map()" in script
    assert "const launchProjectId = state.projectId" in script
    assert "setChildState(launchProjectId, tool.tool_id" in script
    assert "project_id: launchProjectId" in script
    assert "child.project_id !== launchProjectId || child.tool_id !== tool.tool_id" in script
    assert "status.textContent = childState.status" in script


def test_browser_submits_the_selected_known_project_and_keeps_registered_projects_separate() -> None:
    script = web_source("app.js")

    assert 'const knownProjects = document.querySelector("#known-project")' in script
    assert "project.project_id" in script
    assert 'project_id: document.querySelector("#known-project").value' in script
    assert 'document.querySelector("#registered-project-list")' in script
    assert "project_root" not in script.split("function renderRegisteredProjects", 1)[-1].split("function ", 1)[0]


def test_browser_opens_only_the_authenticated_loopback_url_returned_by_launch() -> None:
    script = web_source("app.js")

    assert 'const child = await api("/api/launch"' in script
    assert "const childUrl = new URL(child.url)" in script
    assert 'childUrl.protocol !== "http:"' in script
    assert 'childUrl.hostname !== "127.0.0.1"' in script
    assert "!childUrl.port" in script
    assert 'window.open(childUrl.href, "_blank", "noopener")' in script
    assert 'window.open(`http://' not in script


def test_missing_project_anchor_evidence_has_a_truthful_public_reason(tmp_path: Path) -> None:
    project = make_project(tmp_path / "visual-project", "coc-fiction")
    client = client_for(tmp_path)
    with client:
        assert client.post(
            "/api/projects",
            json={"project_id": "coc-fiction", "project_root": str(project)},
        ).status_code == 201

        response = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "coc-fiction"}
        )

        assert response.status_code == 409
        assert response.json()["detail"] == "PROJECT_ANCHOR_EVIDENCE_UNAVAILABLE"


def test_hub_api_preserves_qa_launch_client(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "omenward")
    client = client_for(tmp_path)
    with client:
        client.post(
            "/api/projects", json={"project_id": "omenward", "project_root": str(project)}
        )
        qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "omenward"}
        )
        assert qa.status_code == 200
        assert qa.json()["url"].startswith("http://127.0.0.1:")
        assert qa.json()["status"] == "RUNNING"
