from pathlib import Path


ROOT = Path(__file__).parents[1]
ADOPTION_GUIDE = Path(__file__).parents[3] / "docs" / "knowledge" / "game-development" / "SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md"
PROJECT_GPT_TEMPLATE = Path(__file__).parents[3] / "templates" / "sprite-animation" / "project-gpt-figma-delivery.md"


def test_readme_states_that_credentials_and_generated_art_are_not_committed() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "API 키" in text
    assert "커밋하지 않습니다" in text


def test_adoption_guide_requires_figma_lineage_project_runtime_and_bridge_boundaries() -> None:
    text = ADOPTION_GUIDE.read_text(encoding="utf-8")

    assert "Figma 노드 URL" in text
    assert "Godot 런타임 검증" in text
    assert "Base Tool Hub → Figma Bridge" not in text
    assert "Tool Hub → Figma Bridge 전달" in text
    assert "sprite_action_runs" in text
    assert "effect_runs" in text
    assert "LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN" in text
    assert "Project GPT packet 수동 배치" in text


def test_legacy_named_delivery_template_routes_through_tool_hub_bridge() -> None:
    text = PROJECT_GPT_TEMPLATE.read_text(encoding="utf-8")

    for token in (
        "Base Tool Hub + Figma Bridge",
        "sprite_action_runs",
        "effect_runs",
        "Sprite Action Runs",
        "Effect Runs",
        "DELIVERY_RUN_ROUTE_MISMATCH",
        "DELIVERY_RUN_CONTENT_MISMATCH",
        "DELIVERED_VERIFIED",
    ):
        assert token in text

    for stale in (
        "Use this action only after a visual result has been generated or curated in the **same project GPT workspace**",
        "The Base browser can prepare a `ready_for_project_gpt` packet",
    ):
        assert stale not in text


def test_readme_documents_dedicated_server_owned_sprite_routes_and_evidence_ceiling() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")

    for token in (
        "pose_sequence",
        "sprite_action",
        "Sprite Action Runs",
        "effect_stages",
        "Effect Runs",
        "expression_variation",
        "DELIVERY_TOOL_ROUTE_UNAVAILABLE",
        "exported atlas PNG",
        "USER_PC_TOOL_HUB = NOT_RUN",
        "REAL_CHATGPT_PRO_POSE_SEQUENCE = NOT_RUN",
        "REAL_CHATGPT_PRO_EFFECT_STAGES = NOT_RUN",
        "LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN",
        "GODOT_CONSUMPTION = NOT_RUN",
    ):
        assert token in text

    assert "SIMULATED / DELIVERY_BLOCKED" in text
    assert ".asset-vault/library/generated/sprite-animation-studio" in text
    assert "--port" in text


def test_browser_exposes_confirmed_delivery_without_route_or_node_authority() -> None:
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "web" / "app.js").read_text(encoding="utf-8")

    for token in (
        "confirm-delivery",
        "delivery-status",
        "confirmed-download",
        "확정 및 전달",
        "Sprite Action Runs",
        "Effect Runs",
    ):
        assert token in html + javascript

    for forbidden in (
        "figma_file_key",
        "target_node_id",
        "generation_area_node_id",
        "project_marker_node_id",
        "X-Base-Tool-Route",
    ):
        assert forbidden not in javascript

    assert "request.mode" not in javascript[javascript.find("confirm-delivery") :]
