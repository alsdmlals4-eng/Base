from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ResilientExecutionNarrativeReferenceContractTests(unittest.TestCase):
    def test_fresh_powershell_contract_is_discoverable_and_one_block(self) -> None:
        contract_path = ROOT / "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md"
        self.assertTrue(contract_path.is_file())
        contract = contract_path.read_text(encoding="utf-8")
        for term in (
            "FRESH_SHELL_ASSUMPTION",
            "ONE_COPY_PASTE_BLOCK",
            "LOCATION_FIRST",
            "NO_PRIOR_SHELL_STATE_DEPENDENCY",
            "FAIL_FAST",
            "NATIVE_EXIT_CODE_REQUIRED",
            "ERROR_STAGE_MARKER",
            "BEGINNER_SAFE_USER_ACTION",
        ):
            self.assertIn(term, contract)
        owner_path = "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md"
        self.assertIn(owner_path, read("AGENTS.md"))
        self.assertIn(owner_path, read("START_HERE.md"))

    def test_deprecated_tool_hub_is_not_required_by_resilient_execution(self) -> None:
        self.assertFalse((ROOT / "tools/tool-hub").exists())
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        self.assertNotIn("TOOL_HUB: REQUIRED_WHEN_RELEVANT", policy)
        self.assertIn("RECOVER_TRY_ALTERNATIVES_RESUME", policy)

    def test_continuous_work_recalculates_remaining_work_after_postmerge(self) -> None:
        continuous = read(
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
        )
        for term in (
            "REQUIRED_WORK_REMAINING",
            "POSTMERGE_REMAINING_WORK_RECALC",
            "REQUEUE_IN_SCOPE_WHEN_NONZERO",
        ):
            self.assertIn(term, continuous)
        self.assertIn("postmerge", continuous.lower())

    def test_reusable_lessons_route_to_existing_owners_before_new_skill(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        agents = read("AGENTS.md")
        start = read("START_HERE.md")
        for term in (
            "REUSABLE_LESSON_PROMOTION_GATE",
            "REUSE_EXISTING_OWNER",
            "EXTEND_REFERENCE_OR_MODE",
            "EXTRACT_MODULE",
            "BASE_CHANGE_PROPOSAL",
            "NEW_SKILL_LAST",
        ):
            self.assertIn(term, policy)
        self.assertIn("managing-base-change-proposals", agents)
        self.assertIn("evolving-project-discipline-skills", start)

    def test_serial_fiction_owns_paragraph_break_and_breath_craft(self) -> None:
        skill = read("skills/developing-and-revising-serial-fiction/SKILL.md")
        guide = read("docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md")
        combined = skill + "\n" + guide
        for term in (
            "PARAGRAPH_BREAK_AND_BREATH",
            "LINE_BREAK_RHYTHM",
            "PARAGRAPH_LENGTH_PATTERN",
            "DIALOGUE_NARRATION_ALTERNATION",
            "REACTION_ISOLATION",
        ):
            self.assertIn(term, combined)

    def test_private_live_narrative_reference_is_pointer_only(self) -> None:
        pointer_path = ROOT / "docs/knowledge/serial-fiction/BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md"
        self.assertTrue(pointer_path.is_file())
        pointer = pointer_path.read_text(encoding="utf-8")
        for term in (
            "LIVE_CONNECTED_DRIVE_READ",
            "USER_PREFERENCE_EVIDENCE",
            "글따라쓰기",
            "NOT_CANON",
            "NO_STYLE_IMITATION",
        ):
            self.assertIn(term, pointer)
        lowered = pointer.lower()
        for forbidden in (
            "docs.google.com/",
            "drive.google.com/",
            "https://",
            "http://",
            "document_id:",
            "document id:",
        ):
            self.assertNotIn(forbidden, lowered)

    def test_narrative_learning_log_does_not_overclaim_private_source_readback(self) -> None:
        learning = read("skills/developing-and-revising-serial-fiction/LEARNING_LOG.md")
        marker = "## 2026-08-18 — 문단 호흡·private live-reference·CI consumer 전파"
        self.assertIn(marker, learning)
        section = learning.split(marker, 1)[1]
        for term in (
            "source_content_readback: NOT_VERIFIED",
            "focused_contract: GREEN_ON_PR_523_FINAL_HEAD",
            "reference_freshness: GREEN_ON_PR_523_FINAL_HEAD",
            "postmerge_main_readback: VERIFIED",
        ):
            self.assertIn(term, section)

    def test_documentation_map_uses_current_workspace_authority_split(self) -> None:
        docs = read("docs/DOCUMENTATION_MAP.md")
        for term in (
            "PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "V3_COMPATIBILITY_AND_HISTORY_ONLY",
            "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md",
            "NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md",
        ):
            self.assertIn(term, docs)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", docs)
        self.assertNotIn("tools/tool-hub/README.md", docs)


if __name__ == "__main__":
    unittest.main()
