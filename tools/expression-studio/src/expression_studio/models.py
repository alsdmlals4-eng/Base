"""Strict request contracts for local character-consistency runs."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


Intensity = Literal["A", "B", "C", "D", "E"]
Gaze = Literal["left", "right", "up", "down", "center"]
HeadPose = Literal[
    "turn_left",
    "turn_right",
    "up",
    "down",
    "tilt_left",
    "tilt_right",
    "forward",
    "back",
    "neutral",
]
ExpressionPreset = Literal[
    "idle_neutral",
    "alert",
    "determined",
    "hurt",
    "surprised",
    "joy",
    "anger",
    "fear",
    "blink",
    "wink",
]
EditMode = Literal["expression", "outfit", "scene"]


class ExpressionAnchor(BaseModel):
    """An approved character reference and its review source."""

    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1)
    figma_node_url: HttpUrl
    approval_status: Literal["approved"]


class FaceControl(BaseModel):
    """A product control ID plus deliberately bounded intensity."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(pattern=r"^AU[0-9]+$")
    intensity: Intensity
    side: Literal["left", "right"] | None = None

    @model_validator(mode="after")
    def validate_side(self) -> "FaceControl":
        if self.code == "AU46" and self.side is None:
            raise ValueError("AU46 requires side left or right")
        if self.code != "AU46" and self.side is not None:
            raise ValueError("side is supported only for AU46")
        return self


class ExpressionRequest(BaseModel):
    """One approved-character edit request rooted under one project workspace."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    asset_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    anchor: ExpressionAnchor
    edit_mode: EditMode = "expression"
    edit_prompt: str | None = Field(default=None, max_length=1000)
    controls: list[FaceControl] = Field(default_factory=list, max_length=4)
    gaze: Gaze = "center"
    head_pose: HeadPose = "neutral"
    preset: ExpressionPreset | None = None
    candidate_count: int = Field(ge=1, le=8)

    @model_validator(mode="after")
    def validate_expression_request(self) -> "ExpressionRequest":
        if self.edit_mode == "expression":
            if self.edit_prompt is not None:
                raise ValueError("expression edit does not accept edit_prompt")
            if not self.controls and self.preset is None:
                raise ValueError("an expression request requires at least one control or preset")
            if self.controls and self.preset is not None:
                raise ValueError("choose direct controls or one preset, not both")
            return self

        prompt = self.edit_prompt.strip() if self.edit_prompt is not None else ""
        if not prompt:
            raise ValueError("character edit requires a non-empty edit_prompt")
        if self.controls or self.preset is not None:
            raise ValueError("character edit cannot combine expression controls or presets")
        if self.gaze != "center" or self.head_pose != "neutral":
            raise ValueError("character edit preserves gaze and head pose; use expression mode to change them")
        self.edit_prompt = prompt
        return self
