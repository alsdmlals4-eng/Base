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


def test_project_gpt_handoff_is_guarded_not_an_automatic_upload() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert 'id="figma-delivery-button"' in html
    assert "같은 프로젝트 GPT" in html
    assert "/figma-delivery" in script
    assert "업로드가 완료" not in script


def test_web_bootstraps_read_only_project_identity_and_blocks_simulated_export() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    script = (WEB / "app.js").read_text(encoding="utf-8")

    assert 'name="project_id" readonly' in html
    assert 'value="demo"' not in html
    assert 'fetch("/api/config")' in script
    assert "delivery_eligible" in script
