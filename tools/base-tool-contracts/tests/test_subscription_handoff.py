from __future__ import annotations

import pytest

from base_tool_contracts.subscription_handoff import (
    SubscriptionHandoffError,
    build_subscription_handoff_packet,
)


def packet(**overrides):
    values = {
        "project_id": "urban-legend",
        "tool_id": "expression-studio",
        "run_id": "run_20260815_001",
        "workflow": "character_edit",
        "source_filename": "agent_anchor.png",
        "source_sha256": "a" * 64,
        "instruction": "Keep the approved character identity and change only the winter coat.",
        "expected_png_count": 4,
        "min_dimension": 256,
        "max_dimension": 2048,
        "review_checklist": (
            "same character identity",
            "requested outfit change is visible",
            "no unrequested background change",
        ),
    }
    values.update(overrides)
    return build_subscription_handoff_packet(**values)


def test_valid_packet_is_deterministic_and_never_claims_provider_execution() -> None:
    first = packet()
    second = packet()

    assert first == second
    assert first.public_view() == {
        "schema_version": 1,
        "state": "GPT_PRO_HANDOFF_READY",
        "project_id": "urban-legend",
        "tool_id": "expression-studio",
        "run_id": "run_20260815_001",
        "workflow": "character_edit",
        "source": {
            "filename": "agent_anchor.png",
            "sha256": "a" * 64,
        },
        "generation": {
            "instruction": "Keep the approved character identity and change only the winter coat.",
            "expected_png_count": 4,
            "min_dimension": 256,
            "max_dimension": 2048,
        },
        "review_checklist": [
            "same character identity",
            "requested outfit change is visible",
            "no unrequested background change",
        ],
        "provider_call_made": False,
        "requires_additional_payment": False,
    }


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("project_id", "../other-project"),
        ("tool_id", "qa-evidence-studio"),
        ("run_id", "bad run id"),
        ("source_filename", "C:\\Users\\user\\secret.png"),
        ("source_filename", "../secret.png"),
        ("source_sha256", "not-a-sha"),
        ("instruction", ""),
        ("instruction", "x" * 4001),
        ("instruction", "use sk-proj-abcdefghijklmnopqrstuvwxyz0123456789"),
        ("expected_png_count", 0),
        ("expected_png_count", 9),
        ("min_dimension", 15),
        ("max_dimension", 8193),
    ],
)
def test_invalid_or_private_inputs_fail_closed(field: str, value: object) -> None:
    with pytest.raises(SubscriptionHandoffError):
        packet(**{field: value})


def test_workflow_is_bound_to_the_reviewed_tool() -> None:
    with pytest.raises(SubscriptionHandoffError, match="workflow"):
        packet(tool_id="sprite-animation-studio", workflow="character_edit")

    pose = packet(
        tool_id="sprite-animation-studio",
        workflow="sprite_pose_sequence",
        source_filename="sprite_anchor.png",
    )
    assert pose.tool_id == "sprite-animation-studio"

    effect = packet(
        tool_id="sprite-animation-studio",
        workflow="sprite_effect_stages",
        source_filename="effect_anchor.png",
    )
    assert effect.workflow == "sprite_effect_stages"


def test_dimension_range_and_review_checklist_are_bounded() -> None:
    with pytest.raises(SubscriptionHandoffError, match="dimension"):
        packet(min_dimension=2048, max_dimension=256)

    with pytest.raises(SubscriptionHandoffError, match="review"):
        packet(review_checklist=())

    with pytest.raises(SubscriptionHandoffError, match="review"):
        packet(review_checklist=("same character identity", "same character identity"))

    with pytest.raises(SubscriptionHandoffError, match="review"):
        packet(review_checklist=("x" * 241,))
