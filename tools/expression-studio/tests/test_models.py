import pytest

from expression_studio.models import ExpressionRequest


def valid_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "project_id": "demo",
        "asset_id": "hero",
        "anchor": {
            "source_path": "art/source/hero.png",
            "figma_node_url": "https://www.figma.com/design/abc123/demo?node-id=1-2",
            "approval_status": "approved",
        },
        "controls": [{"code": "AU46", "intensity": "C", "side": "left"}],
        "gaze": "center",
        "head_pose": "neutral",
        "candidate_count": 2,
    }
    payload.update(overrides)
    return payload


def test_wink_request_accepts_an_approved_character_anchor() -> None:
    request = ExpressionRequest.model_validate(valid_payload())

    assert request.controls[0].code == "AU46"
    assert request.anchor.approval_status == "approved"


def test_wink_request_requires_and_preserves_an_eye_side() -> None:
    request = ExpressionRequest.model_validate(
        valid_payload(controls=[{"code": "AU46", "intensity": "C", "side": "left"}])
    )

    assert request.controls[0].side == "left"


def test_request_rejects_more_than_four_face_controls() -> None:
    payload = valid_payload(controls=[{"code": "AU1", "intensity": "A"}] * 5)

    with pytest.raises(ValueError, match="at most 4"):
        ExpressionRequest.model_validate(payload)


def test_request_rejects_a_browser_controlled_output_root() -> None:
    with pytest.raises(ValueError, match="extra"):
        ExpressionRequest.model_validate(valid_payload(output_root="art/expression-runs/hero"))


def test_request_requires_a_control_or_preset() -> None:
    with pytest.raises(ValueError, match="control or preset"):
        ExpressionRequest.model_validate(valid_payload(controls=[]))


def test_request_rejects_unknown_request_fields() -> None:
    with pytest.raises(ValueError, match="extra"):
        ExpressionRequest.model_validate(valid_payload(unexpected="blocked"))
