import json
from pathlib import Path

import jsonschema
import pytest

from sprite_animation_studio.models import SpriteAnimationRequest


def valid_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "project_id": "demo",
        "asset_id": "knight",
        "asset_kind": "character",
        "anchor": {
            "source_path": "art/source/idle.png",
            "figma_node_url": "https://www.figma.com/design/abc123/demo?node-id=1-2",
            "approval_status": "approved",
        },
        "action": {
            "name": "attack",
            "direction": "left",
            "frame_count": 4,
            "fps": 8,
            "loop_mode": "none",
            "prompt": "A heavy left-facing sword strike.",
        },
    }
    payload.update(overrides)
    return payload


def test_request_requires_an_approved_anchor() -> None:
    payload = valid_payload(anchor={"source_path": "art/source/idle.png", "approval_status": "draft"})

    with pytest.raises(ValueError, match="approved"):
        SpriteAnimationRequest.model_validate(payload)


def test_request_rejects_frame_count_above_sixteen() -> None:
    payload = valid_payload(action={"name": "attack", "direction": "left", "frame_count": 17, "fps": 8, "loop_mode": "none", "prompt": "strike"})

    with pytest.raises(ValueError, match="16"):
        SpriteAnimationRequest.model_validate(payload)


@pytest.mark.parametrize(
    ("asset_kind", "mode"),
    [
        ("character", "expression_variation"),
        ("character", "pose_sequence"),
        ("effect", "effect_stages"),
        ("character", "sprite_action"),
        ("effect", "sprite_action"),
    ],
)
def test_request_accepts_supported_sprite_modes(asset_kind: str, mode: str) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload(asset_kind=asset_kind, mode=mode))

    assert request.mode == mode


@pytest.mark.parametrize(
    ("asset_kind", "mode"),
    [("effect", "expression_variation"), ("effect", "pose_sequence"), ("character", "effect_stages")],
)
def test_request_rejects_modes_that_conflict_with_asset_kind(asset_kind: str, mode: str) -> None:
    with pytest.raises(ValueError, match="requires asset_kind"):
        SpriteAnimationRequest.model_validate(valid_payload(asset_kind=asset_kind, mode=mode))


def test_portable_schema_rejects_extra_request_fields() -> None:
    schema_path = Path(__file__).parents[3] / "templates" / "sprite-animation" / "sprite-animation-request.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = valid_payload(unexpected="not allowed")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)


def test_request_rejects_a_browser_controlled_output_root() -> None:
    with pytest.raises(ValueError, match="extra"):
        SpriteAnimationRequest.model_validate(valid_payload(output_root="art/animation-runs/knight"))


def test_portable_schema_accepts_optional_sprite_mode() -> None:
    schema_path = Path(__file__).parents[3] / "templates" / "sprite-animation" / "sprite-animation-request.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    jsonschema.validate(valid_payload(mode="pose_sequence"), schema)


def test_portable_schema_rejects_incompatible_mode_and_asset_kind() -> None:
    schema_path = Path(__file__).parents[3] / "templates" / "sprite-animation" / "sprite-animation-request.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(valid_payload(asset_kind="effect", mode="pose_sequence"), schema)
