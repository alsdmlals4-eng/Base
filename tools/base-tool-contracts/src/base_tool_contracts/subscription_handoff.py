"""Bounded, network-free handoff packets for ChatGPT subscription generation."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
import re
from typing import Literal


class SubscriptionHandoffError(ValueError):
    """Raised when a subscription handoff would be ambiguous or unsafe."""


SubscriptionWorkflow = Literal[
    "character_edit",
    "sprite_pose_sequence",
    "sprite_effect_stages",
]

_PROJECT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{7,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SECRET_PATTERNS = (
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{16,}", re.IGNORECASE),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}", re.IGNORECASE),
    re.compile(r"figd_[A-Za-z0-9_-]{16,}", re.IGNORECASE),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}", re.IGNORECASE),
    re.compile(r"\bOPENAI_API_KEY\b\s*[:=]", re.IGNORECASE),
    re.compile(r"\bapi[_ -]?key\b\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\b(?:access[_ -]?token|token)\b\s*[:=]\s*\S+", re.IGNORECASE),
)
_PRIVATE_ROUTING_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"']+"),
    re.compile(r"(?<![A-Za-z0-9])/(?:home|Users|mnt|tmp|var|etc)/[^\s\"']+"),
    re.compile(r"https?://(?:www\.)?figma\.com/", re.IGNORECASE),
    re.compile(r"\bnode-id=\d+(?:[-:]\d+)?\b", re.IGNORECASE),
)
_WORKFLOW_TOOL = {
    "character_edit": "expression-studio",
    "sprite_pose_sequence": "sprite-animation-studio",
    "sprite_effect_stages": "sprite-animation-studio",
}
_WINDOWS_FILENAME_FORBIDDEN = frozenset('<>:"/\\|?*')


@dataclass(frozen=True)
class SubscriptionHandoffPacket:
    project_id: str
    tool_id: str
    run_id: str
    workflow: SubscriptionWorkflow
    source_filename: str
    source_sha256: str
    instruction: str
    expected_png_count: int
    min_dimension: int
    max_dimension: int
    review_checklist: tuple[str, ...]
    schema_version: int = field(default=1, init=False)
    state: str = field(default="GPT_PRO_HANDOFF_READY", init=False)
    generation_surface: str = field(default="CHATGPT_PRO_SUBSCRIPTION", init=False)
    output_media_type: str = field(default="image/png", init=False)
    provider_call_made: bool = field(default=False, init=False)
    requires_additional_payment: bool = field(default=False, init=False)

    def public_view(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "state": self.state,
            "generation_surface": self.generation_surface,
            "project_id": self.project_id,
            "tool_id": self.tool_id,
            "run_id": self.run_id,
            "workflow": self.workflow,
            "source": {
                "filename": self.source_filename,
                "sha256": self.source_sha256,
            },
            "generation": {
                "instruction": self.instruction,
                "output_media_type": self.output_media_type,
                "expected_png_count": self.expected_png_count,
                "min_dimension": self.min_dimension,
                "max_dimension": self.max_dimension,
            },
            "review_checklist": list(self.review_checklist),
            "provider_call_made": self.provider_call_made,
            "requires_additional_payment": self.requires_additional_payment,
        }


def _safe_filename(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > 160:
        return False
    if any(ord(character) < 32 for character in value):
        return False
    if any(character in _WINDOWS_FILENAME_FORBIDDEN for character in value):
        return False
    return value.lower().endswith(".png")


def _bounded_text(value: object, *, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and len(value) <= maximum
        and "\x00" not in value
    )


def _contains_secret(value: str) -> bool:
    return any(pattern.search(value) for pattern in _SECRET_PATTERNS)


def _contains_private_routing(value: str) -> bool:
    return any(pattern.search(value) for pattern in _PRIVATE_ROUTING_PATTERNS)


def build_subscription_handoff_packet(
    *,
    project_id: str,
    tool_id: str,
    run_id: str,
    workflow: SubscriptionWorkflow,
    source_filename: str,
    source_sha256: str,
    instruction: str,
    expected_png_count: int,
    min_dimension: int,
    max_dimension: int,
    review_checklist: Sequence[str],
) -> SubscriptionHandoffPacket:
    """Build a truthful packet for manual generation in the normal ChatGPT UI.

    This function deliberately performs no provider call, browser automation,
    clipboard access, Figma mutation, or credential handling.
    """

    if not isinstance(project_id, str) or not _PROJECT_ID.fullmatch(project_id):
        raise SubscriptionHandoffError("project identity is invalid")
    if not isinstance(workflow, str) or workflow not in _WORKFLOW_TOOL:
        raise SubscriptionHandoffError("subscription workflow is unsupported")
    expected_tool = _WORKFLOW_TOOL[workflow]
    if not isinstance(tool_id, str) or tool_id != expected_tool:
        raise SubscriptionHandoffError("workflow is not bound to the reviewed tool")
    if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
        raise SubscriptionHandoffError("run identity is invalid")
    if not _safe_filename(source_filename):
        raise SubscriptionHandoffError("source filename must be one local display-only PNG name")
    if not isinstance(source_sha256, str) or not _SHA256.fullmatch(source_sha256):
        raise SubscriptionHandoffError("source sha256 is invalid")
    if not _bounded_text(instruction, maximum=4000):
        raise SubscriptionHandoffError("generation instruction is outside the bounded contract")
    if _contains_secret(instruction) or _contains_private_routing(instruction):
        raise SubscriptionHandoffError(
            "generation instruction contains credential-like or private routing material"
        )
    if type(expected_png_count) is not int or not 1 <= expected_png_count <= 8:
        raise SubscriptionHandoffError("expected PNG count must be between 1 and 8")
    if (
        type(min_dimension) is not int
        or type(max_dimension) is not int
        or not 16 <= min_dimension <= 8192
        or not 16 <= max_dimension <= 8192
        or min_dimension > max_dimension
    ):
        raise SubscriptionHandoffError("dimension range is invalid")
    if isinstance(review_checklist, (str, bytes)) or not isinstance(review_checklist, Sequence):
        raise SubscriptionHandoffError("review checklist must be a bounded sequence of text items")

    checklist = tuple(review_checklist)
    if not 1 <= len(checklist) <= 12:
        raise SubscriptionHandoffError("review checklist must contain 1 to 12 items")
    if any(
        not isinstance(item, str)
        or not _bounded_text(item, maximum=240)
        or _contains_secret(item)
        or _contains_private_routing(item)
        for item in checklist
    ):
        raise SubscriptionHandoffError("review checklist contains invalid or private material")
    if len(checklist) != len(set(checklist)):
        raise SubscriptionHandoffError("review checklist contains duplicate items")

    return SubscriptionHandoffPacket(
        project_id=project_id,
        tool_id=tool_id,
        run_id=run_id,
        workflow=workflow,
        source_filename=source_filename,
        source_sha256=source_sha256,
        instruction=instruction,
        expected_png_count=expected_png_count,
        min_dimension=min_dimension,
        max_dimension=max_dimension,
        review_checklist=checklist,
    )
