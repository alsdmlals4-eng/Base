from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class RepositoryFirstBootstrapRoutingTests(unittest.TestCase):
    def test_project_operations_readme_installs_repository_first_workspace(self) -> None:
        readme = text("templates/project-operations/README.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "PDF_ONLY_USER_DOWNLOAD",
            "SHARED_ID_AND_SOURCE_SHA_REQUIRED",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "NOTION_UNIQUE_CANON_COUNT = 0",
            "CODEX_NOTION_DEPENDENCY_COUNT = 0",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
        ):
            self.assertIn(token, readme)
        self.assertIn("신규 Notion workspace나 Google Sheet를 설치 완료 조건으로 만들지 않는다", readme)
        self.assertIn("LEGACY_DISCOVERY_ONLY", readme)
        self.assertNotIn(
            "실제 프로젝트에서 생성·채택된 문서와 정확한 Project Notion workspace가 정본 역할을 가진다",
            readme,
        )
        self.assertNotIn(
            "현재 기본 계약은 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`의 `DOMAIN_SPLIT_CANON`",
            readme,
        )
        self.assertNotIn("정확한 Project Notion workspace와 Project relation 확인", readme)

    def test_gpt_custom_instruction_template_uses_repository_authority(self) -> None:
        template = text("templates/custom-instructions.gpt.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "PDF_ONLY_USER_DOWNLOAD",
            "SYS/CNT/UI/UX/AST/AUD/DAT/QA/DEC",
            "GPT_VISUAL_REQUEST",
        ):
            self.assertIn(token, template)
        self.assertIn(
            "AI Markdown은 repository path·branch·exact commit SHA·PR·validation result로 보고한다",
            template,
        )
        self.assertIn("이미지 생성·편집은 내가 명시적으로 요청했을 때만 진행한다", template)
        self.assertIn("새 Notion output이나 GitHub+Notion 이중 동기화를 기본 완료 조건으로 만들지 않는다", template)
        self.assertNotIn("프로젝트 정보는 DOMAIN_SPLIT_CANON을 따른다", template)
        self.assertNotIn("Notion은 사람이 읽고 비교·수정하는", template)
        self.assertNotIn("해당 프로젝트 저장소와 연결된 Notion에서 필요한 최신 정본", template)
        self.assertNotIn("승인된 결정이나 변경은 필요한 GitHub/Notion 정본에 동기화", template)

    def test_codex_custom_instruction_template_uses_exact_repository_inputs(self) -> None:
        template = text("templates/custom-instructions.codex.md")
        for token in (
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "EXACT_REPOSITORY_COMMIT",
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "CURRENT_CODEX_HANDOFF",
            "REPOSITORY_PATH_MANIFEST_SHA256_READBACK",
            "NOTION_ABSENCE_IS_NOT_A_BLOCKER",
            "GPT_VISUAL_REQUEST",
            "READY_FOR_GPT_REVIEW",
        ):
            self.assertIn(token, template)
        self.assertIn("Notion page, attachment 또는 readback이 없다는 이유만으로 구현을 막지 않는다", template)
        self.assertNotIn("시작 시 CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION", template)
        self.assertNotIn("current-use 승인 + Notion upload/attach/readback된 Visual만 사용", template)
        self.assertNotIn("approved Notion Visuals consumed", template)
        self.assertNotIn("DOMAIN_SPLIT_CANON", template)
        self.assertNotIn("NOTION_HUMAN_FACING_CANON", template)

    def test_custom_instruction_guide_routes_to_current_contract(self) -> None:
        guide = text("docs/CUSTOM_INSTRUCTIONS_GUIDE.md")
        for token in (
            "REPOSITORY_PRIMARY_PROJECT_CANON",
            "AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
            "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
            "LEGACY_READ_ONLY_MIGRATION_SOURCE",
            "DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD",
            "EXACTLY_TWO_DELIVERABLES",
            "PDF_ONLY_USER_DOWNLOAD",
            "NOTION_UNIQUE_CANON_COUNT = 0",
            "CODEX_NOTION_DEPENDENCY_COUNT = 0",
            "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
        ):
            self.assertIn(token, guide)
        self.assertIn("새 Notion write나 이중 동기화를 기본 요구하지 않는다", guide)
        self.assertNotIn("`DOMAIN_SPLIT_CANON`처럼 장기적인 정본 분할 원칙", guide)
        self.assertNotIn("NOTION_HUMAN_FACING_CANON\n→ 사람이 읽고 비교·수정하는", guide)


if __name__ == "__main__":
    unittest.main()
