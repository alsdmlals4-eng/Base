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
            "figma_node_url": "https://www.figma.com/design/demo?node-id=1-2",
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
        "output_root": "art/animation-runs/knight",
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


def test_portable_schema_rejects_extra_request_fields() -> None:
    schema_path = Path(__file__).parents[3] / "templates" / "sprite-animation" / "sprite-animation-request.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = valid_payload(unexpected="not allowed")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(payload, schema)
