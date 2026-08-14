from __future__ import annotations

import pytest

from base_tool_contracts import (
    SubscriptionHandoffError,
    SubscriptionHandoffPacket,
    build_subscription_handoff_packet,
    render_chatgpt_pro_prompt,
)


def packet():
    return build_subscription_handoff_packet(
        project_id="urban-legend",
        tool_id="expression-studio",
        run_id="run_20260815_001",
        workflow="character_edit",
        source_filename="agent_anchor.png",
        source_sha256="a" * 64,
        instruction="Keep the approved character identity and change only the winter coat.",
        expected_png_count=4,
        min_dimension=256,
        max_dimension=2048,
        review_checklist=(
            "same character identity",
            "requested outfit change is visible",
        ),
    )


def test_renderer_is_deterministic_copy_ready_and_subscription_only() -> None:
    result = render_chatgpt_pro_prompt(packet())

    assert result == render_chatgpt_pro_prompt(packet())
    for required in (
        "ChatGPT Pro",
        "urban-legend",
        "expression-studio",
        "run_20260815_001",
        "character_edit",
        "agent_anchor.png",
        "a" * 64,
        "Keep the approved character identity and change only the winter coat.",
        "4",
        "256",
        "2048",
        "same character identity",
        "requested outfit change is visible",
        "subscription_handoff_import",
        "CHATGPT_INCLUDED",
        "no API/provider call",
    ):
        assert required in result
    assert len(result.encode("utf-8")) <= 12 * 1024


def test_renderer_does_not_create_private_or_paid_routing_surface() -> None:
    result = render_chatgpt_pro_prompt(packet())
    forbidden = (
        "OPENAI_API_KEY",
        "sk-proj-",
        "figma.com/design/",
        "node-id=",
        "C:\\Users\\",
        "/home/",
        "PowerShell",
        "curl ",
        "selenium",
        "playwright",
    )
    for token in forbidden:
        assert token not in result


def test_renderer_tells_user_to_return_pngs_to_the_same_run() -> None:
    result = render_chatgpt_pro_prompt(packet())
    assert "same Tool Hub run" in result
    assert "PNG" in result
    assert "provider_call_made=false" in result
    assert "requires_additional_payment=false" in result


def test_renderer_revalidates_packet_instead_of_trusting_direct_dataclass_construction() -> None:
    forged = SubscriptionHandoffPacket(
        project_id="urban-legend",
        tool_id="expression-studio",
        run_id="run_20260815_001",
        workflow="character_edit",
        source_filename="agent_anchor.png",
        source_sha256="a" * 64,
        instruction="Deliver to https://www.figma.com/design/ABCDEFGHIJKLMNOPQRSTUV/file?node-id=14-2",
        expected_png_count=4,
        min_dimension=256,
        max_dimension=2048,
        review_checklist=("same character identity",),
    )

    with pytest.raises(SubscriptionHandoffError, match="packet"):
        render_chatgpt_pro_prompt(forged)

    with pytest.raises(SubscriptionHandoffError, match="packet"):
        render_chatgpt_pro_prompt(object())  # type: ignore[arg-type]


def test_renderer_rejects_tampered_fixed_truth_fields() -> None:
    tampered = packet()
    object.__setattr__(tampered, "requires_additional_payment", True)

    with pytest.raises(SubscriptionHandoffError, match="truth fields"):
        render_chatgpt_pro_prompt(tampered)


def test_renderer_stays_bounded_for_maximum_valid_packet() -> None:
    checklist = tuple(
        f"check-{index:02d}-" + ("x" * 220)
        for index in range(12)
    )
    maximum = build_subscription_handoff_packet(
        project_id="urban-legend",
        tool_id="expression-studio",
        run_id="run_20260815_max",
        workflow="character_edit",
        source_filename="agent_anchor.png",
        source_sha256="b" * 64,
        instruction="x" * 4000,
        expected_png_count=8,
        min_dimension=16,
        max_dimension=8192,
        review_checklist=checklist,
    )

    assert len(render_chatgpt_pro_prompt(maximum).encode("utf-8")) <= 12 * 1024
