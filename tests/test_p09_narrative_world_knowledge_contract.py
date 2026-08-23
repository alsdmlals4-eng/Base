from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md"
README = ROOT / "docs/knowledge/README.md"
HUMAN_HOME = ROOT / "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md"
HOME_COMPAT = ROOT / "docs/coordination/2026-08-24_PR621_HUMAN_HOME_CONFLICT_CORRECTION.md"


def test_narrative_world_knowledge_model_contract():
    text = METHOD.read_text(encoding="utf-8")
    for token in [
        "AUTHORITY_MAP",
        "ENTITY_EXTRACTION",
        "EVENT_EXTRACTION",
        "RELATION_RULE_EXTRACTION",
        "EVIDENCE_LINK",
        "CONTRADICTION_AUDIT",
        "HUMAN_PRIMER",
        "USER_APPROVAL",
        "VISUAL_GATE",
        "NARRATIVE KNOWLEDGE · Master",
        "NARRATIVE EVENT · Ledger",
        "CANON EVIDENCE · Ledger",
        "BLOCKED_BY_TEXT",
        "READY_FOR_VISUAL",
        "CORE_CONFIRMED",
        "CURRENT_CANDIDATE",
        "CONFLICT",
        "Center Peek",
    ]:
        assert token in text


def test_knowledge_model_is_routed_from_knowledge_readme():
    text = README.read_text(encoding="utf-8")
    assert "NARRATIVE_WORLD_KNOWLEDGE_MODEL.md" in text
    assert "서사·세계관 정본 조사·구조화" in text


def test_summary_first_narrative_ux_respects_human_home_owner():
    home = HUMAN_HOME.read_text(encoding="utf-8")
    compat = HOME_COMPAT.read_text(encoding="utf-8")

    for token in (
        "AI_INTERPRETATION_FOR_USER_CORRECTION",
        "HUMAN_EDIT_GUIDE_REQUIRED",
        "AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED",
        "HUMAN_HOME_PROGRESSIVE_DISCLOSURE",
    ):
        assert token in home
        assert token in compat

    assert "SUMMARY_FIRST_IS_PROGRESSIVE_DISCLOSURE_NOT_SECTION_REMOVAL" in compat
    assert "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md" in compat
    assert "skills/building-project-visual-dashboards/SKILL.md" in compat
