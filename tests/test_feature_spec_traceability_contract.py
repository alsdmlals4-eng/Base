from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_traceability_packet_is_l2_plus_and_noncanonical() -> None:
    template = read("templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md")
    assert "L2 이상" in template
    assert "별도 책임 원본이 아니다" in template
    for token in (
        "decision_id",
        "requirement_id",
        "acceptance_criteria_ids",
        "task_ids",
        "implementation_paths",
        "verification_ids",
        "coverage_status",
        "BLOCKED_UNVERIFIED",
        "CONVERGED",
        "unmapped_items",
    ):
        assert token in template


def test_existing_owners_route_traceability_without_new_skill() -> None:
    intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
    docs = read("skills/managing-design-documents/SKILL.md")
    validation = read("skills/reviewing-and-validating-project-changes/SKILL.md")
    for body in (intake, docs, validation):
        assert "FEATURE_SPEC_TRACEABILITY_PACKET.md" in body
    assert "L0·L1" in intake
    assert "상세 책임 원본" in docs
    assert "coverage_status" in validation
