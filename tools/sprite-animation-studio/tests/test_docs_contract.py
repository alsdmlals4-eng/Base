from pathlib import Path


ROOT = Path(__file__).parents[1]
ADOPTION_GUIDE = Path(__file__).parents[3] / "docs" / "knowledge" / "game-development" / "SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md"
PROJECT_GPT_TEMPLATE = Path(__file__).parents[3] / "templates" / "sprite-animation" / "project-gpt-figma-delivery.md"


def test_readme_states_that_credentials_and_generated_art_are_not_committed() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "API 키" in text
    assert "커밋하지 않습니다" in text


def test_adoption_guide_requires_figma_lineage_and_project_runtime_check() -> None:
    text = ADOPTION_GUIDE.read_text(encoding="utf-8")

    assert "Figma 노드 URL" in text
    assert "Godot 런타임 검증" in text


def test_project_gpt_delivery_template_blocks_protected_targets_and_uses_new_run_sections() -> None:
    text = PROJECT_GPT_TEMPLATE.read_text(encoding="utf-8")

    assert "REGISTERED_NO_MUTATION" in text
    assert "새 실행 섹션" in text
    assert "Figma 도구" in text


def test_readme_distinguishes_local_packet_preparation_from_project_gpt_placement() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "ready_for_project_gpt" in text
    assert "직접 업로드하지 않습니다" in text
    assert "SIMULATED / DELIVERY_BLOCKED" in text
    assert ".asset-vault/library/generated/sprite-animation-studio" in text
    assert "--port" in text
