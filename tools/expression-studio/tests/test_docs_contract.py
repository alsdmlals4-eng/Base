from pathlib import Path


BASE_ROOT = Path(__file__).parents[3]
README = BASE_ROOT / "tools" / "expression-studio" / "README.md"
TEMPLATE = BASE_ROOT / "templates" / "expression-studio" / "project-gpt-figma-delivery.md"


def test_expression_studio_documentation_defines_safe_exact_route_delivery() -> None:
    template = TEMPLATE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert "matching project GPT workspace" in template
    assert "generation_area_node_id" in template
    assert "do not replace" in template
    assert "character_expression_runs" in readme
    assert "Tool Hub" in readme
    assert "브라우저가 다른 project ID나 Figma node를 지정할 수 없습니다" in readme
    assert "SIMULATED / DELIVERY_BLOCKED" in readme
    assert ".asset-vault/library/generated/expression-studio" in readme
