from __future__ import annotations

import pytest

from base_tool_contracts.subscription_handoff import SubscriptionHandoffPacket


def test_packet_is_project_run_scoped_and_subscription_only() -> None:
    packet = SubscriptionHandoffPacket.create(
        project_id="urban-legend",
        tool_id="expression-studio",
        run_id="run-001",
        reference="approved character anchor",
        instruction="Change only the winter coat while preserving identity and art style.",
        output_count=4,
        review_checklist=("identity preserved", "only outfit changed"),
    )

    public = packet.public_view()
    assert public["project_id"] == "urban-legend"
    assert public["tool_id"] == "expression-studio"
    assert public["run_id"] == "run-001"
    assert public["generation_surface"] == "CHATGPT_PRO"
    assert public["run_mode"] == "subscription_handoff_import"
    assert public["output_media_type"] == "image/png"
    assert public["output_count"] == 4
    assert "api" not in " ".join(public.keys()).lower()
    assert "key" not in " ".join(public.keys()).lower()


@pytest.mark.parametrize(
    "overrides",
    [
        {"project_id": "../escape"},
        {"tool_id": "Expression Studio"},
        {"run_id": ""},
        {"instruction": ""},
        {"output_count": 0},
        {"output_count": 9},
        {"instruction": "Use OPENAI_API_KEY to call the provider"},
        {"instruction": "Use sk-proj-secret"},
        {"reference": r"C:\\private\\hero.png"},
        {"reference": "/home/user/private/hero.png"},
    ],
)
def test_packet_rejects_invalid_or_secret_bearing_inputs(overrides: dict[str, object]) -> None:
    values: dict[str, object] = {
        "project_id": "urban-legend",
        "tool_id": "expression-studio",
        "run_id": "run-001",
        "reference": "approved character anchor",
        "instruction": "Change only the winter coat.",
        "output_count": 4,
        "review_checklist": ("identity preserved",),
    }
    values.update(overrides)

    with pytest.raises(ValueError):
        SubscriptionHandoffPacket.create(**values)


def test_packet_has_no_destination_override_surface() -> None:
    with pytest.raises(TypeError):
        SubscriptionHandoffPacket.create(
            project_id="urban-legend",
            tool_id="expression-studio",
            run_id="run-001",
            reference="approved character anchor",
            instruction="Change only the coat.",
            output_count=1,
            review_checklist=("identity preserved",),
            figma_node_id="999:999",  # type: ignore[call-arg]
        )
