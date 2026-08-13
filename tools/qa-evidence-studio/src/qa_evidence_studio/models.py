"""Validated public requests for QA Evidence Studio."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChecklistItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    label: str = Field(min_length=1, max_length=160)
    required: bool = True


class CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=160)
    build_commit: str = Field(pattern=r"^[0-9a-f]{40}$")
    checklist: list[ChecklistItem] = Field(min_length=1, max_length=40)

    @field_validator("checklist")
    @classmethod
    def unique_items(cls, value: list[ChecklistItem]) -> list[ChecklistItem]:
        identifiers = [item.item_id for item in value]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("checklist item_id values must be unique")
        return value


ReviewStatus = Literal["PASS", "FAIL", "BLOCKED", "NOT_RUN"]
