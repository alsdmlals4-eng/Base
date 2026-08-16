from __future__ import annotations

import json
from pathlib import Path


BASE_ROOT = Path(__file__).resolve().parents[3]


def read(relative: str) -> str:
    return (BASE_ROOT / relative).read_text(encoding="utf-8")


def test_character_ui_preserves_subscription_import_surface() -> None:
    index = read("tools/expression-studio/web/index.html")
    app = read("tools/expression-studio/web/app.js")

    assert "<title>Character Studio</title>" in index
    assert "<h1>Character Studio</h1>" in index
    assert 'id="edit-mode"' in index
    assert 'value="expression"' in index
    assert 'value="outfit"' in index
    assert 'value="scene"' in index
    assert 'id="edit-prompt"' in index
    assert 'maxlength="1000"' in index

    assert "edit_mode: editMode" in app
    assert "edit_prompt: editPrompt" in app
    assert 'studioConfig.run_mode === "subscription_handoff_import"' in app
    assert 'body.append("declared_source", document.querySelector("#declared-source").value)' in app
    assert 'request("/api/import-runs"' in app
    assert "OPENAI_API_KEY" not in index
    assert "OPENAI_API_KEY" not in app


def test_character_registry_and_launch_tuple_expand_together_without_losing_subscription_pin() -> None:
    registry = json.loads(read("tools/TOOL_REGISTRY.json"))
    validator = read("tools/validate_tool_registry.py")
    adapters = read("tools/tool-hub/src/tool_hub/adapters.py")

    expression = next(item for item in registry["tools"] if item["tool_id"] == "expression-studio")
    expected = [
        "expression_variation",
        "identity_preserving_edit",
        "outfit_variation",
        "scene_relocation",
        "image_import",
        "figma_delivery_packet",
    ]
    assert expression["display_name"] == "Character Studio"
    assert expression["capabilities"] == expected

    for capability in expected:
        assert f'"{capability}"' in validator
        assert f'"{capability}"' in adapters

    assert '"--run-mode"' in adapters
    assert '"subscription_handoff_import"' in adapters
    assert '"--approved-anchor-registry"' in adapters
    assert '"--figma-target-registry"' in adapters
