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


def test_project_gpt_delivery_template_still_blocks_protected_legacy_targets() -> None:
    text = PROJECT_GPT_TEMPLATE.read_text(encoding="utf-8")

    assert "REGISTERED_NO_MUTATION" in text
    assert "새 실행 섹션" in text
    assert "Figma 도구" in text


def test_readme_documents_confirmed_dedicated_delivery_contract() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    for required in (
        "확정 및 전달",
        "Figma Bridge",
        "Sprite Action Runs",
        "Effect Runs",
        "pose_sequence",
        "sprite_action",
        "effect_stages",
        "expression_variation",
        "DELIVERY_TOOL_ROUTE_UNAVAILABLE",
        "exported atlas PNG",
        "USER_PC_TOOL_HUB = NOT_RUN",
        "LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN",
        "GODOT_CONSUMPTION = NOT_RUN",
        "SIMULATED / DELIVERY_BLOCKED",
        ".asset-vault/library/generated/sprite-animation-studio",
        "--port",
    ):
        assert required in text
    assert "ready_for_project_gpt" not in text
    assert "직접 업로드하지 않습니다" not in text


def test_browser_has_no_figma_route_or_node_authority_or_legacy_delivery_call() -> None:
    app_text = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    delivery_text = (ROOT / "web" / "confirmed-delivery.js").read_text(encoding="utf-8")
    text = app_text + "\n" + delivery_text

    assert "confirm-delivery" in delivery_text
    assert "delivery-status" in delivery_text
    assert "confirmed-download" in delivery_text
    assert "/figma-delivery" not in app_text
    assert "project GPT" not in app_text
    for forbidden in (
        "figma_file_key",
        "target_node_id",
        "generation_area_node_id",
        "project_marker_node_id",
        "X-Base-Tool-Route",
    ):
        assert forbidden not in text
