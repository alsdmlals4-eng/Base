"""Strict request contracts for local sprite-animation runs."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


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

    project_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    asset_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    asset_kind: Literal["character", "effect"]
    anchor: Anchor
    action: Action
    output_root: str = Field(min_length=1)

    @field_validator("output_root")
    @classmethod
    def output_root_must_be_relative(cls, value: str) -> str:
        if value.startswith("/") or ".." in value.replace("\\", "/").split("/"):
            raise ValueError("output_root must be relative to project_root")
        return value
