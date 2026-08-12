from pathlib import Path


WEB_ROOT = Path(__file__).parents[1] / "web"


def test_web_exposes_separate_face_gaze_and_head_pose_controls() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")

    assert "얼굴 제어" in html
    assert "시선" in html
    assert "머리 방향" in html
    assert "프로젝트 GPT 전송 준비" in html


def test_web_explains_that_figma_placement_happens_in_matching_project_gpt() -> None:
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert "matching project GPT workspace" in script
    assert "/api/runs/" in script


def test_web_renders_resolved_controls_and_anchor_lineage_for_review() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="review-metadata"' in html
    assert "anchor_sha256" in script
    assert "resolved_expression.controls" in script


def test_web_bootstraps_read_only_project_identity_and_blocks_simulated_export() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="project-id" readonly' in html
    assert 'value="demo"' not in html
    assert 'request("/api/config")' in script
    assert "delivery_eligible" in script
