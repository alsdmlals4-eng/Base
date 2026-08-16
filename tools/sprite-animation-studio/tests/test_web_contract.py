from pathlib import Path


WEB = Path(__file__).parents[1] / "web"


def test_workspace_names_the_five_visual_lineage_stages() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")

    for label in ["원본 이미지", "승인 앵커", "동작 후보", "채택 프레임", "최종 시트"]:
        assert label in html


def test_controls_have_labels_for_destructive_actions() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")

    assert 'aria-label="선택 프레임에서 제거"' in html
    assert 'aria-label="프레임 순서 앞으로"' in html


def test_workspace_exposes_all_project_sprite_modes() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")

    for mode in ["expression_variation", "pose_sequence", "effect_stages", "sprite_action"]:
        assert f'value="{mode}"' in html


def test_confirmed_delivery_is_guarded_and_server_owned() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert 'id="confirm-delivery-button"' in html
    assert 'id="refresh-delivery-button"' in html
    assert 'id="confirmed-download"' in html
    assert "확정 및 전달" in html
    assert "Sprite Action Runs" in html
    assert "Effect Runs" in html
    assert "/confirm-delivery" in script
    assert "/delivery-status" in script
    assert "download.href = result.download_url" in script
    assert "/figma-delivery" not in script
    for forbidden in (
        "figma_file_key",
        "target_node_id",
        "generation_area_node_id",
        "project_marker_node_id",
        "X-Base-Tool-Route",
    ):
        assert forbidden not in script


def test_web_bootstraps_read_only_project_identity_and_blocks_simulated_export() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert 'name="project_id" readonly' in html
    assert 'value="demo"' not in html
    assert 'fetch("/api/config")' in script
    assert "delivery_eligible" in script


def test_sprite_web_exposes_ordered_import_queue_and_cost_boundary() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")

    assert 'id="frame-files"' in html
    assert 'name="frames"' in html
    assert "multiple" in html
    assert 'id="import-queue"' in html
    assert 'id="declared-source"' in html
    assert "추가 비용 없는 가져오기" in html + (WEB / "app.js").read_text(encoding="utf-8")
    assert "업로드 순서" in html
    assert 'id="export-button" class="primary" type="button" disabled' in html
    assert "출처 선택은 구독·라이선스 증명이 아닙니다" in html


def test_sprite_web_cost_copy_and_import_requirements_follow_server_run_mode() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert 'id="cost-title"' in html
    assert 'id="cost-detail"' in html
    assert 'id="import-controls"' in html
    assert "유료 API를 호출하지 않습니다" not in html
    assert "function applyRunModeUi()" in script
    assert 'state.config.run_mode === "subscription_handoff_import"' in script
    assert "고정 sprite-gen 실행 모드" in script
    assert ".required = importMode" in script


def test_sprite_web_clears_previous_run_before_client_side_import_validation() -> None:
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert "function resetRunState()" in script
    submit_start = script.index('$("#request-form").addEventListener("submit"')
    reset_call = script.index("resetRunState();", submit_start)
    count_check = script.index("state.uploadQueue.length !== request.action.frame_count", submit_start)

    assert reset_call < count_check
    for marker in ('$("#figma-delivery-status").textContent = ""', "state.active = null", "state.exported = false"):
        assert marker in script
