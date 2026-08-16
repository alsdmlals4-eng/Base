from pathlib import Path


BASE_ROOT = Path(__file__).parents[3]
README = BASE_ROOT / "tools" / "expression-studio" / "README.md"
TEMPLATE = BASE_ROOT / "templates" / "expression-studio" / "project-gpt-figma-delivery.md"


def test_expression_studio_documentation_defines_canonical_tool_hub_bridge_handoff() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    for token in (
        "Base Tool Hub + Figma Bridge",
        "character_expression_runs",
        "Expression Runs",
        "DELIVERED_VERIFIED",
        "generation_area_node_id",
    ):
        assert token in template

    for stale in (
        "Use this procedure only after the **matching project GPT workspace**",
        "has received an Expression Studio `ready_for_project_gpt` packet",
    ):
        assert stale not in template

    assert "확정 및 전달" in readme
    assert "character_expression_runs" in readme
    assert "Sprite Action Runs" in readme
    assert "Effect Runs" in readme
    assert "DELIVERY_TOOL_ROUTE_UNAVAILABLE" in readme
    assert "SIMULATED / DELIVERY_BLOCKED" in readme
    assert ".asset-vault/library/generated/expression-studio" in readme
