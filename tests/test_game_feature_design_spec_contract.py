from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_game_feature_design_spec_template_declares_l2_behavior_contract() -> None:
    template = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
    for token in (
        "L2",
        "Player Problem",
        "Experience Intent",
        "Player Verbs",
        "Entry / Exit / Cancel / Re-entry",
        "State & Rules",
        "Success / Failure / Partial Success / Recovery",
        "Data & Balance",
        "Benchmark Decision",
        "Risk & Prototype",
        "Acceptance Criteria",
        "Telemetry / Playtest",
        "Cut-down / Rollback",
        "Open Decisions",
        "USER_DECISION_REQUIRED",
        "BLOCKED_UNVERIFIED",
    ):
        assert token in template


def test_feature_spec_is_progressive_and_does_not_take_traceability_ownership() -> None:
    template = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
    assert "PoC" in template
    assert "L0" in template and "L1" in template
    assert "Task progress" in template
    assert "executed verification" in template
    assert "소유하지" in template


def test_existing_owner_skills_route_feature_detail_without_new_skill() -> None:
    docs = read("skills/managing-design-documents/SKILL.md")
    concepts = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
    registry = read("skills/SKILL_REGISTRY.json")
    assert "GAME_FEATURE_DESIGN_SPEC.md" in docs
    assert "GAME_FEATURE_DESIGN_SPEC.md" in concepts
    assert "PoC" in concepts and "승격" in concepts
    assert "game-feature-design" not in registry


def test_document_hierarchy_and_traceability_link_upstream_spec() -> None:
    system = read("templates/planning/DESIGN_DOCUMENT_SYSTEM.md")
    packet = read("templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md")
    assert "L0" in system and "L1" in system and "L2" in system and "L3" in system
    assert "GAME_FEATURE_DESIGN_SPEC" in system
    assert "design_spec_id" in packet
    assert "canonical_design_spec_path" in packet
    assert "별도 책임 원본이 아니다" in packet
