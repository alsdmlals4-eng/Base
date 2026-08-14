from __future__ import annotations

import pytest

from expression_studio.catalog import resolve_expression
from expression_studio.engine import generation_instruction
from expression_studio.models import ExpressionRequest
from tests.test_models import valid_payload


def _character_edit_payload(edit_mode: str, prompt: str) -> dict[str, object]:
    return valid_payload(
        edit_mode=edit_mode,
        edit_prompt=prompt,
        controls=[],
        preset=None,
        gaze="center",
        head_pose="neutral",
    )


def test_outfit_edit_preserves_identity_and_changes_only_wardrobe() -> None:
    request = ExpressionRequest.model_validate(
        _character_edit_payload("outfit", "navy field coat with brass fasteners")
    )

    instruction = generation_instruction(request, resolve_expression(request))

    assert request.edit_mode == "outfit"
    assert "Preserve the exact same character identity" in instruction
    assert "face geometry" in instruction
    assert "hairstyle" in instruction
    assert "body proportions" in instruction
    assert "pose" in instruction
    assert "background" in instruction
    assert "Change only clothing, costume, and wearable accessories" in instruction
    assert "navy field coat with brass fasteners" in instruction


def test_scene_edit_preserves_character_design_and_changes_only_location() -> None:
    request = ExpressionRequest.model_validate(
        _character_edit_payload("scene", "rainy neon alley at night")
    )

    instruction = generation_instruction(request, resolve_expression(request))

    assert request.edit_mode == "scene"
    assert "Preserve the exact same character identity and design" in instruction
    assert "face geometry" in instruction
    assert "hairstyle" in instruction
    assert "costume" in instruction
    assert "body proportions" in instruction
    assert "pose" in instruction
    assert "Change only the environment, location, and background" in instruction
    assert "rainy neon alley at night" in instruction


def test_character_edit_requires_a_bounded_edit_prompt() -> None:
    with pytest.raises(ValueError, match="edit_prompt"):
        ExpressionRequest.model_validate(_character_edit_payload("outfit", ""))

    with pytest.raises(ValueError, match="edit_prompt"):
        ExpressionRequest.model_validate(_character_edit_payload("scene", "x" * 1001))


def test_character_edit_rejects_expression_controls_and_pose_changes() -> None:
    with pytest.raises(ValueError, match="character edit"):
        ExpressionRequest.model_validate(
            valid_payload(
                edit_mode="outfit",
                edit_prompt="red ceremonial coat",
                controls=[{"code": "AU46", "intensity": "C", "side": "left"}],
            )
        )

    with pytest.raises(ValueError, match="character edit"):
        ExpressionRequest.model_validate(
            _character_edit_payload("scene", "mountain shrine") | {"head_pose": "turn_left"}
        )


def test_expression_mode_remains_backward_compatible() -> None:
    request = ExpressionRequest.model_validate(valid_payload())

    assert request.edit_mode == "expression"
    assert request.edit_prompt is None
    instruction = generation_instruction(request, resolve_expression(request))
    assert "wink the left eye" in instruction
