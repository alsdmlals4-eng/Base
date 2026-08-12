"""Strict request contracts for local sprite-animation runs."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


SpriteAnimationMode = Literal[
    "expression_variation",
    "pose_sequence",
    "effect_stages",
    "sprite_action",
]


class Anchor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1)
    figma_node_url: HttpUrl
    approval_status: Literal["approved"]


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    direction: Literal["left", "right", "up", "down", "none"]
    frame_count: int = Field(ge=1, le=16)
    fps: int = Field(ge=1, le=60)
    loop_mode: Literal["none", "linear", "pingpong"]
    prompt: str = Field(min_length=1, max_length=2000)


class SpriteAnimationRequest(BaseModel):
    """A project-root-relative animation request with an approved visual anchor."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    asset_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    asset_kind: Literal["character", "effect"]
    mode: SpriteAnimationMode = "sprite_action"
    anchor: Anchor
    action: Action

    @model_validator(mode="after")
    def mode_must_match_asset_kind(self) -> "SpriteAnimationRequest":
        required_asset_kind = {
            "expression_variation": "character",
            "pose_sequence": "character",
            "effect_stages": "effect",
        }.get(self.mode)
        if required_asset_kind and self.asset_kind != required_asset_kind:
            raise ValueError(f"mode {self.mode} requires asset_kind {required_asset_kind}")
        return self
