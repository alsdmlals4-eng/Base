from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AiBootstrapDriftContractTests(unittest.TestCase):
    def read(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_gpt_template_keeps_dynamic_authority_and_no_deprecated_workspace(self) -> None:
        text = self.read("templates/custom-instructions.gpt.md")

        for required in (
            "bootstrap layer",
            "DOMAIN_SPLIT_CANON",
            "AGENTS.md",
            "START_HERE.md",
            "Active Context",
            "현재 채택된 Base 계약",
            "MIGRATION_ONLY_UNTIL_REMOVAL",
        ):
            self.assertIn(required, text)

        for forbidden in (
            "HTML 대시보드 설계",
            "Google Sheets를 기본",
            "너는 구현 담당자다",
        ):
            self.assertNotIn(forbidden, text)

    def test_codex_template_uses_dynamic_authority_bootstrap(self) -> None:
        text = self.read("templates/custom-instructions.codex.md")

        for required in (
            "stable bootstrap",
            "DOMAIN_SPLIT_CANON",
            "AGENTS.md",
            "START_HERE.md",
            "Active Context",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
            "현재 세션",
            "actual evidence",
        ):
            self.assertIn(required, text)

        for forbidden in (
            "너는 구현 담당자다",
            "docs/AI_WORKFLOW_RULES.md",
            "docs/MVP_WORKFLOW_CHECKLIST.md",
            "docs/BENCHMARKING_REFERENCE_GUIDE.md",
        ):
            self.assertNotIn(forbidden, text)

    def test_copilot_template_is_repository_map_not_fixed_file_checklist(self) -> None:
        text = self.read("templates/copilot-instructions.md")

        for required in (
            "repository bootstrap",
            "DOMAIN_SPLIT_CANON",
            "AGENTS.md",
            "Active Context",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
            "path-specific",
        ):
            self.assertIn(required, text)

        for forbidden in (
            "docs/AI_SHARED_WORK_RULES.md",
            "USER_FACING_GDD_WORKSPACE",
        ):
            self.assertNotIn(forbidden, text)

    def test_project_agents_scaffold_routes_current_domain_canons(self) -> None:
        text = self.read("templates/AGENTS.project.md")

        for required in (
            "DOMAIN_SPLIT_CANON",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "REPOSITORY_RUNTIME_TRUTH",
            "MIGRATION_ONLY_UNTIL_REMOVAL",
            "current Base",
            "current open PR",
        ):
            self.assertIn(required, text)

        for forbidden in (
            "docs/AI_WORKFLOW_RULES.md",
            "docs/MVP_WORKFLOW_CHECKLIST.md",
            "USER_FACING_GDD_WORKSPACE",
        ):
            self.assertNotIn(forbidden, text)

    def test_sheet_control_contract_is_migration_only(self) -> None:
        data = json.loads(self.read("docs/operations/SHEET_CONTROL_CONTRACT.json"))

        self.assertGreaterEqual(data["schema_version"], 2)
        self.assertEqual(data["project_sheet_role"], "MIGRATION_ONLY_UNTIL_REMOVAL")
        self.assertEqual(data["active_human_facing_canon"], "NOTION_DEFAULT_PROJECT_WORKSPACE")
        self.assertEqual(data["active_structured_canon"], "REPOSITORY_STRUCTURED_CANON")
        self.assertEqual(data["runtime_truth"], "REPOSITORY_RUNTIME_TRUTH")
        self.assertFalse(data["external_sheet_writes_authorized"])
        self.assertNotEqual(data["project_sheet_role"], "USER_FACING_GDD_WORKSPACE")

    def test_custom_instruction_guide_marks_executor_audit_current(self) -> None:
        text = self.read("docs/CUSTOM_INSTRUCTIONS_GUIDE.md")

        for required in (
            "Codex/Copilot bootstrap",
            "repository-wide",
            "path-specific",
            "dynamic authority",
        ):
            self.assertIn(required, text)

        self.assertNotIn(
            "Codex 템플릿 자체의 상세 read-order와 stale-path 감사는 GPT 맞춤설정 변경과 독립된 변경 범위로 수행한다.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
