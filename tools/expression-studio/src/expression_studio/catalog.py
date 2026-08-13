"""Curated product controls, presets, and pre-generation conflict checks."""

from dataclasses import dataclass

from .models import ExpressionPreset, ExpressionRequest, FaceControl, Gaze, HeadPose


class ExpressionControlError(ValueError):
    """Raised when a requested product control has no supported meaning."""


class ExpressionConflictError(ValueError):
    """Raised when two controls cannot be truthfully expressed at once."""


CONTROL_PHRASES: dict[str, str] = {
    "AU1": "raise the inner brows",
    "AU2": "raise the outer brows",
    "AU4": "lower and draw the brows together",
    "AU5": "raise the upper eyelids",
    "AU6": "raise the cheeks",
    "AU7": "tighten the eyelids",
    "AU9": "wrinkle the nose",
    "AU10": "raise the upper lip",
    "AU12": "pull the lip corners upward",
    "AU14": "form dimples",
    "AU15": "pull the lip corners downward",
    "AU16": "lower the lower lip",
    "AU17": "raise the chin",
    "AU18": "pucker the lips",
    "AU20": "stretch the lips sideways",
    "AU23": "tighten the lips",
    "AU24": "press the lips together",
    "AU25": "part the lips slightly",
    "AU26": "drop the jaw",
    "AU27": "stretch the mouth wide open",
    "AU28": "draw the lips inward",
    "AU41": "let the upper eyelids droop",
    "AU42": "narrow the eyes",
    "AU43": "close both eyes",
    "AU44": "squint the eyes",
    "AU45": "blink both eyes",
}

GAZE_PHRASES: dict[Gaze, str] = {
    "left": "look to the left",
    "right": "look to the right",
    "up": "look upward",
    "down": "look downward",
    "center": "keep the gaze centered",
}

HEAD_POSE_PHRASES: dict[HeadPose, str] = {
    "turn_left": "turn the head to the left",
    "turn_right": "turn the head to the right",
    "up": "raise the head",
    "down": "lower the head",
    "tilt_left": "tilt the head to the left",
    "tilt_right": "tilt the head to the right",
    "forward": "move the head forward",
    "back": "move the head back",
    "neutral": "keep the head pose neutral",
}

CONFLICT_PAIRS = {
    frozenset({"AU43", "AU5"}),
    frozenset({"AU43", "AU42"}),
    frozenset({"AU43", "AU45"}),
    frozenset({"AU43", "AU46"}),
    frozenset({"AU24", "AU25"}),
    frozenset({"AU26", "AU27"}),
    frozenset({"AU18", "AU20"}),
}

PRESET_CONTROLS: dict[ExpressionPreset, tuple[FaceControl, ...]] = {
    "idle_neutral": (),
    "alert": (FaceControl(code="AU5", intensity="B"),),
    "determined": (FaceControl(code="AU4", intensity="B"), FaceControl(code="AU7", intensity="B")),
    "hurt": (FaceControl(code="AU4", intensity="C"), FaceControl(code="AU15", intensity="C")),
    "surprised": (FaceControl(code="AU1", intensity="C"), FaceControl(code="AU5", intensity="C"), FaceControl(code="AU26", intensity="B")),
    "joy": (FaceControl(code="AU6", intensity="C"), FaceControl(code="AU12", intensity="C")),
    "anger": (FaceControl(code="AU4", intensity="D"), FaceControl(code="AU7", intensity="C"), FaceControl(code="AU23", intensity="B")),
    "fear": (FaceControl(code="AU1", intensity="C"), FaceControl(code="AU5", intensity="C"), FaceControl(code="AU20", intensity="B")),
    "blink": (FaceControl(code="AU45", intensity="B"),),
    "wink": (FaceControl(code="AU46", intensity="C", side="left"),),
}


@dataclass(frozen=True)
class ResolvedExpression:
    controls: tuple[FaceControl, ...]
    gaze: Gaze
    head_pose: HeadPose
    preset: ExpressionPreset | None
    movement_phrases: tuple[str, ...]
    gaze_phrase: str
    head_pose_phrase: str


def _phrase(control: FaceControl) -> str:
    if control.code == "AU46":
        return f"wink the {control.side} eye"
    return CONTROL_PHRASES[control.code]


def _validate_controls(controls: tuple[FaceControl, ...]) -> None:
    unknown = sorted({control.code for control in controls if control.code != "AU46" and control.code not in CONTROL_PHRASES})
    if unknown:
        raise ExpressionControlError(f"unsupported expression control: {', '.join(unknown)}")
    keys = [(control.code, control.side) for control in controls]
    if len(keys) != len(set(keys)):
        raise ExpressionControlError("the same expression control cannot be selected twice")
    if sum(control.code == "AU46" for control in controls) > 1:
        raise ExpressionConflictError("two AU46 winks would close both eyes; use AU43 for both eyes closed")
    codes = {control.code for control in controls}
    for pair in CONFLICT_PAIRS:
        if pair.issubset(codes):
            first, second = sorted(pair)
            raise ExpressionConflictError(f"expression controls conflict: {first} cannot be combined with {second}")


def resolve_expression(request: ExpressionRequest) -> ResolvedExpression:
    """Resolve an approved request to reviewable movements without invoking an engine."""
    controls = PRESET_CONTROLS[request.preset] if request.preset is not None else tuple(request.controls)
    _validate_controls(controls)
    return ResolvedExpression(
        controls=controls,
        gaze=request.gaze,
        head_pose=request.head_pose,
        preset=request.preset,
        movement_phrases=tuple(_phrase(control) for control in controls),
        gaze_phrase=GAZE_PHRASES[request.gaze],
        head_pose_phrase=HEAD_POSE_PHRASES[request.head_pose],
    )
