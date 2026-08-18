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

        agents = read("AGENTS.md")
        start = read("START_HERE.md")
        owner_path = "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md"
        self.assertIn(owner_path, agents)
        self.assertIn(owner_path, start)

    def test_tool_hub_first_transition_consumes_fresh_shell_contract(self) -> None:
        readme = read("tools/tool-hub/README.md")
        for term in (
            "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md",
            "FRESH_SHELL_ASSUMPTION",
            "$Stage = '0/4 LOCATION'",
            "Set-Location",
        ):
            self.assertIn(term, readme)
        location_index = readme.index("Set-Location")
        venv_index = readme.index("py -3.12 -m venv .venv")
        self.assertLess(location_index, venv_index)

        workflow = read(".github/workflows/validate-base-long-horizon-work-contract.yml")
        self.assertIn('"tools/tool-hub/README.md"', workflow)

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
        self.assertIn("0", continuous)

    def test_reusable_lessons_route_to_existing_owners_before_new_skill(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "REUSABLE_LESSON_PROMOTION_GATE",
            "REUSE_EXISTING_OWNER",
            "EXTEND_REFERENCE_OR_MODE",
            "EXTRACT_MODULE",
            "BASE_CHANGE_PROPOSAL",
            "NEW_SKILL_LAST",
            "managing-base-change-proposals",
            "evolving-project-discipline-skills",
        ):
            self.assertIn(term, policy)

    def test_serial_fiction_owns_paragraph_break_and_breath_craft(self) -> None:
        skill = read("skills/developing-and-revising-serial-fiction/SKILL.md")
        guide = read(
            "docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md"
        )
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
        pointer_path = (
            ROOT
            / "docs"
            / "knowledge"
            / "serial-fiction"
            / "BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md"
        )
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

        serial_readme = read("docs/knowledge/serial-fiction/README.md")
        self.assertIn("BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md", serial_readme)

    def test_documentation_map_uses_current_workspace_authority_split(self) -> None:
        docs = read("docs/DOCUMENTATION_MAP.md")
        for term in (
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
            "REPO_NATIVE_STRUCTURED_DATA",
            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
            "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",
            "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md",
        ):
            self.assertIn(term, docs)
        self.assertNotIn(
            "일반 프로젝트의 기획·상태 확인은 GitHub 정본과 구성된 프로젝트 GDD Google Sheets를 우선한다.",
            docs,
        )


if __name__ == "__main__":
    unittest.main()