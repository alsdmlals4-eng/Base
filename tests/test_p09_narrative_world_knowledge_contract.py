from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md"
README = ROOT / "docs/knowledge/README.md"


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
