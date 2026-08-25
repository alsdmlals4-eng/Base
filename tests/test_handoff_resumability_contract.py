from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = (ROOT / "docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md").read_text(encoding="utf-8")
TEMPLATE = (ROOT / "templates/project-operations/HANDOFF.md").read_text(encoding="utf-8")


def test_receiver_ack_is_distinct_from_packet_readiness():
    required = ["PACKET_READY", "PENDING_RECEIVER_ACK", "TRANSFER_ACCEPTED", "receiver_ack"]
    for token in required:
        assert token in METHOD or token in TEMPLATE, token


def test_resume_checkpoint_prevents_duplicate_side_effects():
    required = ["last_safe_checkpoint", "next_safe_action", "side_effects_already_applied", "idempotency"]
    for token in required:
        assert token in METHOD or token in TEMPLATE, token


def test_pending_user_decisions_are_explicit_resume_gates():
    required = ["pending_user_decisions", "approval_required_before_resume"]
    for token in required:
        assert token in METHOD or token in TEMPLATE, token


def test_resume_rehydrates_instruction_and_canon_surfaces():
    required = ["instruction_surface_readback", "AGENTS.md", "CONTEXT_DRIFT_RECHECK_REQUIRED"]
    for token in required:
        assert token in METHOD or token in TEMPLATE, token


def test_handoff_context_is_curated_not_transcript_dumped():
    required = ["context_sanitation", "raw tool log", "3~7"]
    for token in required:
        assert token in METHOD or token in TEMPLATE, token
