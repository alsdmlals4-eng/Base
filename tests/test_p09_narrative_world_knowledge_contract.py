from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md"
FALLBACK = ROOT / "docs/knowledge/methods/NOTION_KNOWLEDGE_QUERY_FALLBACK.md"
README = ROOT / "docs/knowledge/README.md"
HUMAN_HOME = ROOT / "docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md"
HOME_COMPAT = ROOT / "docs/coordination/2026-08-24_PR621_HUMAN_HOME_CONFLICT_CORRECTION.md"


class NarrativeWorldKnowledgeContractTests(unittest.TestCase):
    def test_narrative_world_knowledge_model_contract(self) -> None:
        text = METHOD.read_text(encoding="utf-8")
        for token in (
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
        ):
            self.assertIn(token, text)

    def test_notion_knowledge_query_fallback_contract(self) -> None:
        text = FALLBACK.read_text(encoding="utf-8")
        for token in (
            "NOTION_QUERY_FALLBACK",
            "VIEW_MODE_FIRST",
            "DATA_SOURCE_SCOPED_SEARCH",
            "PAGE_FETCH_READBACK",
            "SOURCE_EXACT_CHECK",
            "TARGETED_UPDATE_ONLY",
            "SEARCH_NOT_EXHAUSTIVE",
            "NO_AUTO_PROMOTION_FROM_SEARCH",
        ):
            self.assertIn(token, text)

    def test_knowledge_model_is_routed_from_knowledge_readme(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("NARRATIVE_WORLD_KNOWLEDGE_MODEL.md", text)
        self.assertIn("서사·세계관 정본 조사·구조화", text)

    def test_summary_first_narrative_ux_respects_human_home_owner(self) -> None:
        home = HUMAN_HOME.read_text(encoding="utf-8")
        compat = HOME_COMPAT.read_text(encoding="utf-8")

        for token in (
            "AI_INTERPRETATION_FOR_USER_CORRECTION",
            "HUMAN_EDIT_GUIDE_REQUIRED",
            "AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED",
            "HUMAN_HOME_PROGRESSIVE_DISCLOSURE",
        ):
            self.assertIn(token, home)
            self.assertIn(token, compat)

        self.assertIn(
            "SUMMARY_FIRST_IS_PROGRESSIVE_DISCLOSURE_NOT_SECTION_REMOVAL", compat
        )
        self.assertIn("docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md", compat)
        self.assertIn("skills/building-project-visual-dashboards/SKILL.md", compat)

    def test_human_home_compatibility_respects_host_image_precedence(self) -> None:
        compat = HOME_COMPAT.read_text(encoding="utf-8")
        for token in (
            "HOST_PLATFORM_PRECEDENCE",
            "HOST_POLICY_OVERRIDE",
            "RUNTIME_ENFORCEMENT_NOT_GUARANTEED",
        ):
            self.assertIn(token, compat)


if __name__ == "__main__":
    unittest.main()
