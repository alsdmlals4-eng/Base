from pathlib import Path

from fastapi.testclient import TestClient

from qa_evidence_studio.app import create_app
from test_api import make_project


def test_browser_surface_explains_real_review_gate_and_deferred_scope(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    response = TestClient(
        create_app(project, "demo-game", bind_origin="http://testserver", test_mode=True)
    ).get("/")

    assert response.status_code == 200
    html = response.text
    assert 'id="session-form"' in html
    assert 'id="readiness-gate"' in html
    assert 'id="review-workspace"' in html
    assert 'id="android-status"' in html
    assert "이미지와 UX 배치를 완료한 뒤" in html
    assert "개발자 본인" in html
    assert "출시 준비 직전까지 연결 보류" in html


def test_browser_script_does_not_render_user_checklist_with_inner_html() -> None:
    script = (Path(__file__).resolve().parents[1] / "web" / "app.js").read_text(encoding="utf-8")

    assert ".innerHTML" not in script
