from __future__ import annotations

import inspect

import pytest

from base_tool_contracts.subscription_handoff import (
    SubscriptionHandoffError,
    SubscriptionHandoffPacket,
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
        "generation_surface": "CHATGPT_PRO_SUBSCRIPTION",
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
            "output_media_type": "image/png",
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


def test_truth_fields_are_not_constructor_or_builder_inputs() -> None:
    result = packet()
    assert result.generation_surface == "CHATGPT_PRO_SUBSCRIPTION"
    assert result.output_media_type == "image/png"

    parameters = inspect.signature(SubscriptionHandoffPacket).parameters
    for fixed_field in (
        "schema_version",
        "state",
        "generation_surface",
        "output_media_type",
        "provider_call_made",
        "requires_additional_payment",
    ):
        assert fixed_field not in parameters

    with pytest.raises(TypeError):
        packet(generation_surface="OPENAI_API")
    with pytest.raises(TypeError):
        packet(output_media_type="image/jpeg")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("project_id", "../other-project"),
        ("project_id", 123),
        ("tool_id", "qa-evidence-studio"),
        ("run_id", "bad run id"),
        ("run_id", 123),
        ("source_filename", "C:\\Users\\user\\secret.png"),
        ("source_filename", "../secret.png"),
        ("source_filename", "secret:stream.png"),
        ("source_sha256", "not-a-sha"),
        ("source_sha256", 123),
        ("instruction", ""),
        ("instruction", 123),
        ("instruction", "x" * 4001),
        ("instruction", "use sk-proj-abcdefghijklmnopqrstuvwxyz0123456789"),
        ("instruction", "token=abcdefghijklmnopqrstuvwxyz0123456789"),
        ("instruction", "Use C:\\Users\\user\\Private\\anchor.png as reference."),
        ("instruction", "Use /home/user/private/anchor.png as reference."),
        ("instruction", "Deliver to https://www.figma.com/design/ABCDEFGHIJKLMNOPQRSTUV/file?node-id=14-2"),
        ("expected_png_count", 0),
        ("expected_png_count", 9),
        ("expected_png_count", 1.5),
        ("min_dimension", 15),
        ("min_dimension", 256.5),
        ("max_dimension", 8193),
        ("max_dimension", 2048.5),
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

    for bad_checklist in (
        (),
        "same character identity",
        (123,),
        ("same character identity", "same character identity"),
        ("x" * 241,),
        ("compare against C:\\Users\\user\\Private\\anchor.png",),
        ("compare against /home/user/private/anchor.png",),
        ("verify https://figma.com/design/ABCDEFGHIJKLMNOPQRSTUV/file?node-id=14-2",),
    ):
        with pytest.raises(SubscriptionHandoffError, match="review"):
            packet(review_checklist=bad_checklist)
