from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_design_md_template_is_visual_only_and_version_pinned() -> None:
    template = read("templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md")
    for token in (
        "format_version",
        "source_commit_or_release",
        "last_verified_at",
        "colors:",
        "typography:",
        "spacing:",
        "components:",
        "godot_theme_mapping",
        "web_token_mapping",
        "reference_provenance",
        "accessibility_constraints",
        "validation_status",
    ):
        assert token in template
    assert "게임 규칙" in template
    assert "소유하지 않는다" in template
    assert "alpha" in template


def test_game_ux_ui_remains_behavior_owner() -> None:
    ux = read("templates/planning/GAME_UX_UI_SYSTEM.md")
    adapter = read(
        "skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md"
    )
    assert "DESIGN.md" in ux
    assert "시각 토큰" in ux
    assert "플레이어 경험" in ux
    assert "GAME_UX_UI_SYSTEM" in adapter
    assert "Theme" in adapter
    assert "CSS" in adapter
