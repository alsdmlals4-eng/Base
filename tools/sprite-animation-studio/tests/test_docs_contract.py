from pathlib import Path


ROOT = Path(__file__).parents[1]
ADOPTION_GUIDE = Path(__file__).parents[3] / "docs" / "knowledge" / "game-development" / "SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md"


def test_readme_states_that_credentials_and_generated_art_are_not_committed() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "API 키" in text
    assert "커밋하지 않습니다" in text


def test_adoption_guide_requires_figma_lineage_and_project_runtime_check() -> None:
    text = ADOPTION_GUIDE.read_text(encoding="utf-8")

    assert "Figma 노드 URL" in text
    assert "Godot 런타임 검증" in text
