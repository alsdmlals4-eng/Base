from pathlib import Path


WEB_ROOT = Path(__file__).parents[1] / "web"


def test_web_exposes_separate_face_gaze_and_head_pose_controls() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")

    assert "얼굴 제어" in html
    assert "시선" in html
    assert "머리 방향" in html
    assert "확정 및 전달" in html


def test_web_confirms_selected_candidate_directly_to_tool_hub_delivery() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="confirm-delivery-button" type="button" disabled' in html
    assert 'id="export-button"' not in html
    assert 'id="delivery-button"' not in html
    assert "/confirm-delivery" in script
    assert "/figma-delivery" not in script
    assert "matching project GPT workspace" not in script
    assert "project_save" in script
    assert "figma_delivery" in script
    assert "target_node_name" in script


def test_web_renders_resolved_controls_and_anchor_lineage_for_review() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="review-metadata"' in html
    assert "anchor_sha256" in script
    assert "resolved_expression.controls" in script


def test_web_bootstraps_read_only_project_identity_and_blocks_simulated_delivery() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="project-id" readonly' in html
    assert 'value="demo"' not in html
    assert 'request("/api/config")' in script
    assert "delivery_eligible" in script


def test_expression_web_exposes_import_first_controls_without_auto_confirmation() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="candidate-files"' in html
    assert 'name="candidates"' in html
    assert "multiple" in html
    assert 'id="declared-source"' in html
    for source in ("CHATGPT_INCLUDED", "FIGMA_INCLUDED", "LOCAL_GENERATOR", "OTHER_USER_SUPPLIED"):
        assert f'value="{source}"' in html
    assert "추가 비용 없는 가져오기" in html + script
    assert 'id="confirm-delivery-button" type="button" disabled' in html
    assert "출처 선택은 구독·라이선스 증명이 아닙니다" in html
    assert "selectedCandidate = null" in script


def test_expression_web_cost_copy_and_import_requirements_follow_server_run_mode() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert 'id="cost-title"' in html
    assert 'id="cost-detail"' in html
    assert 'id="import-controls"' in html
    assert "유료 API를 호출하지 않습니다" not in html
    assert "function applyRunModeUi()" in script
    assert 'studioConfig.run_mode === "subscription_handoff_import"' in script
    assert "OpenAI API 별도 과금 모드" in script
    assert ".required = importMode" in script


def test_expression_web_clears_previous_run_before_every_new_submission() -> None:
    script = (WEB_ROOT / "app.js").read_text(encoding="utf-8")

    assert "function resetRunState()" in script
    submit_start = script.index('document.querySelector("#expression-form").addEventListener("submit"')
    reset_call = script.index("resetRunState();", submit_start)
    request_start = script.index("const payload = requestPayload();", submit_start)

    assert reset_call < request_start
    for marker in (
        "currentRunId = null",
        "currentRunDeliveryEligible = false",
        'document.querySelector("#delivery-result").textContent = ""',
    ):
        assert marker in script
