import pytest

from expression_studio.catalog import ExpressionConflictError, ExpressionControlError, resolve_expression
from expression_studio.models import ExpressionRequest
from tests.test_models import valid_payload


def request_with(*codes: str) -> ExpressionRequest:
    controls = [
        {"code": code, "intensity": "C", **({"side": "left"} if code == "AU46" else {})}
        for code in codes
    ]
    return ExpressionRequest.model_validate(valid_payload(controls=controls))


def test_au46_resolves_to_a_side_specific_wink_phrase() -> None:
    resolved = resolve_expression(request_with("AU46"))

    assert resolved.movement_phrases == ("wink the left eye",)


def test_closed_eyes_and_upper_lid_raise_are_rejected_before_generation() -> None:
    with pytest.raises(ExpressionConflictError, match=r"AU43.*AU5"):
        resolve_expression(request_with("AU43", "AU5"))


def test_unknown_control_id_is_rejected_before_generation() -> None:
    with pytest.raises(ExpressionControlError, match="AU999"):
        resolve_expression(request_with("AU999"))


def test_wink_preset_resolves_to_visible_control_and_phrase() -> None:
    request = ExpressionRequest.model_validate(valid_payload(controls=[], preset="wink"))

    resolved = resolve_expression(request)

    assert resolved.preset == "wink"
    assert resolved.controls[0].code == "AU46"
    assert resolved.movement_phrases == ("wink the left eye",)


def test_gaze_and_head_pose_are_resolved_separately_from_face_controls() -> None:
    request = ExpressionRequest.model_validate(valid_payload(gaze="right", head_pose="turn_left"))

    resolved = resolve_expression(request)

    assert resolved.gaze_phrase == "look to the right"
    assert resolved.head_pose_phrase == "turn the head to the left"


def test_two_opposite_side_winks_are_rejected_as_a_bilateral_eye_closure_request() -> None:
    request = ExpressionRequest.model_validate(
        valid_payload(
            controls=[
                {"code": "AU46", "intensity": "C", "side": "left"},
                {"code": "AU46", "intensity": "C", "side": "right"},
            ]
        )
    )

    with pytest.raises(ExpressionConflictError, match="both eyes"):
        resolve_expression(request)
