from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BCAVisualSheetWorkflowTests(unittest.TestCase):
    def test_v9_is_active_and_v6_to_v8_are_compatibility_only(self) -> None:
        v9 = (ROOT / "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md").read_text(encoding="utf-8")
        v8 = (ROOT / "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md").read_text(encoding="utf-8")
        v7 = (ROOT / "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md").read_text(encoding="utf-8")
        self.assertIn('contract_version: "9.1"', v9)
        self.assertIn("SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION", v9)
        self.assertIn("REPOSITORY_FIRST_INTERVIEW", v9)
        self.assertIn("INTEGRATED_DELIVERY_PROFILE", v9)
        self.assertIn("CONDITIONAL_RECONCILIATION", v9)
        self.assertIn("PROJECT_SHEET_SEMANTIC_TABS", v9)
        self.assertIn("INTERMEDIATE_VISUAL_CHECKPOINT", v9)
        self.assertIn("PROJECT_BASE_ADAPTER.json", v9)
        self.assertIn("AGENT_MERGE_REQUIRED", v9)
        self.assertIn("PROJECT_BASE_SKILL_ADAPTER.json", v9)
        self.assertIn("SUPERSEDED_COMPATIBILITY", v8)
        self.assertIn("SUPERSEDED_COMPATIBILITY", v7)
        self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md", v7)

    def test_sheet_contract_has_semantic_and_visual_tabs(self) -> None:
        sheet = (ROOT / "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md").read_text(encoding="utf-8")
        for tab in (
            "11_세계관", "12_핵심루프", "13_주요인물", "14_조연_세력_관계",
            "40_핵심시스템_메인콘텐츠", "71_이미지기획_생성목록", "72_이미지검수_승인로그",
        ):
            self.assertIn(tab, sheet)
        for term in ("World ID", "Loop ID", "Character ID", "System ID", "APPROVED_CANDIDATE"):
            self.assertIn(term, sheet)

    def test_art_skill_contains_generation_and_review_modes(self) -> None:
        skill = (ROOT / "skills/designing-art-prompts-and-technique-cards/SKILL.md").read_text(encoding="utf-8")
        for mode in ("planning-visualization", "intermediate-visual-checkpoint", "final-visual-candidate", "visual-qa-and-approval"):
            self.assertIn(f"`{mode}`", skill)
        for status in ("GENERATED_EXPLORATION", "REVISION_REQUIRED", "PROJECT_ASSET_APPROVED", "APPLIED_AND_RUNTIME_VERIFIED"):
            self.assertIn(status, skill)
        self.assertIn("생성 결과는 자동 최종 자산이 아니다", skill)

    def test_registry_routes_existing_visual_work_without_a_duplicate_skill(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        entry = next(item for item in registry["skills"] if item["skill_id"] == "designing-art-prompts-and-technique-cards")
        for tag in ("planning-visualization", "intermediate-visual-checkpoint", "final-visual-candidate", "visual-qa-and-approval", "image-mockup", "image-approval"):
            self.assertIn(tag, entry["trigger_tags"])

    def test_active_entrypoints_reference_v9_not_v7(self) -> None:
        for path in ("START_HERE.md", "docs/DOCUMENTATION_MAP.md", "templates/project-operations/README.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md", text, path)
            self.assertNotIn("상세 기획·Demo-First Vertical Slice·GPT→Codex·전체 검수 지시를 파일 하나로 첨부해야 할 때는 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`", text, path)

    def test_policy_forbids_duplicate_sheet_creation_and_false_approval(self) -> None:
        policy = (ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md").read_text(encoding="utf-8")
        for term in ("NOT_CONFIGURED", "새 Sheet를 추정 생성", "자동 최종 자산", "repository-wide-audit", "71_이미지기획_생성목록", "72_이미지검수_승인로그"):
            self.assertIn(term, policy)

    def test_visual_workspace_policy_supports_gdd_and_external_contexts(self) -> None:
        policy = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        for context in ("GDD", "EXTERNAL_COLLABORATION", "BOTH"):
            self.assertIn(context, policy)


if __name__ == "__main__":
    unittest.main()
