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
