from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "templates" / "prompts" / "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md"
V8_PROMPT_PATH = ROOT / "templates" / "prompts" / "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md"
LEGACY_PROMPT_PATH = ROOT / "templates" / "prompts" / "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md"


def read(path: str | Path) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class IntegratedVerticalSlicePromptV7Tests(unittest.TestCase):
    def test_single_attachment_prompt_exists_and_replaces_split_v6_usage(self) -> None:
        self.assertTrue(PROMPT_PATH.is_file(), str(PROMPT_PATH))
        self.assertTrue(V8_PROMPT_PATH.is_file(), str(V8_PROMPT_PATH))
        self.assertTrue(LEGACY_PROMPT_PATH.is_file(), str(LEGACY_PROMPT_PATH))
        prompt = read(PROMPT_PATH)
        v8 = read(V8_PROMPT_PATH)
        legacy = read(LEGACY_PROMPT_PATH)

        for term in (
            'contract_name: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT',
            'contract_version: "9.1"',
            'release_line: "Base v9.3"',
            "usage: \"이 파일 하나만 첨부하면 저장소 우선 인터뷰부터 기획·Codex 인계·구현·검수·병합 후 Notion/repository readback까지 현재 작업에 필요한 절차를 실행한다.\"",
            "execution_model: SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION",
            "APPLICATION_BINDING",
            "REPOSITORY_FIRST_INTERVIEW",
            "INTEGRATED_DELIVERY_PROFILE",
            "RECONCILIATION_PLANNING_PROFILE",
            "STALE_PROMPT_CONTRACT",
        ):
            self.assertIn(term, prompt)

        for term in (
            "active_authority: false",
            "status: SUPERSEDED_COMPATIBILITY",
            "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
        ):
            self.assertIn(term, legacy)

        for term in ("active_authority: false", "status: SUPERSEDED_COMPATIBILITY", "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md"):
            self.assertIn(term, v8)

    def test_prompt_uses_current_preflight_planning_and_demo_first_contracts(self) -> None:
        prompt = read(PROMPT_PATH)

        for term in (
            "DUPLICATE_OMISSION_CONFLICT_AUDIT",
            "EVIDENCE_PACK",
            "APPROVAL_BUNDLE",
            "PROPAGATION_AUDIT",
            "DEMO_FIRST_VERTICAL_SLICE",
            "DEMO_VALIDATION",
            "TECHNICAL_SPIKE",
            "LEGACY_SHEET_COMPATIBILITY_MIGRATION",
            "INTERMEDIATE_VISUAL_CHECKPOINT",
            "DRAFT_VISUAL",
            "Screen Interpretation Review",
            "MISSING_CANON",
            "VISUAL_CANONICAL_CONFLICT",
            "TECHNICAL_REVIEW_PROPOSAL",
        ):
            self.assertIn(term, prompt)

        self.assertNotIn(
            "stage_model:\n  - CONCEPT_APPROVAL\n  - PROTOTYPE_AND_VERTICAL_SLICE",
            prompt,
        )
        self.assertNotIn("→ CORE_POC\n→ 기획 재조정", prompt)
        self.assertNotIn("CORE_POC부터 버티컬 슬라이스", prompt)
        self.assertNotIn("→ 외부 Slice Validation", prompt)

    def test_prompt_contains_interview_handoff_repository_audit_and_completion_evidence(self) -> None:
        prompt = read(PROMPT_PATH)

        for term in (
            "이미 확정된 질문은 다시 묻지 않는다",
            "origin/main",
            "PROJECT_BASE_ADAPTER.json",
            "PROJECT_SKILL_SNAPSHOT.json",
            "보호 경로",
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "COMPATIBILITY_ONLY",
            "Source / Consumer / Propagation Map",
            "Approval Bundle",
            "PLAN_AND_CODEX_HANDOFF",
            "CANONICAL_UPDATE_AND_IMPLEMENTATION",
            "MERGE_AND_SYNC",
            "merged main",
        ):
            self.assertIn(term, prompt)

    def test_reconciliation_is_conditional_and_single_attachment_can_finish_an_authorized_delivery(self) -> None:
        prompt = read(PROMPT_PATH)

        self.assertIn("모든 첨부의 기본값이 아니라", prompt)
        self.assertIn("`INTEGRATED_DELIVERY_PROFILE`은 `PLAN_OR_DECISION` 또는 `IMPLEMENTATION_REQUESTED`에 쓰는 기본 실행 경로", prompt)
        self.assertIn("새 첨부나 별도 축약 Prompt를 요구하지 않는다", prompt)
        for term in (
            "GitHub Issue",
            "/goal Implement GitHub Issue #[NUMBER] exactly as specified.",
            "Codex 구현 인계",
            "독립 리뷰·적대적 검토",
            "병합된 main을 기준으로만",
            "legacy Sheet 단독 변경은 언제나 `PROPOSED_SHEET_CHANGE`",
        ):
            self.assertIn(term, prompt)

        self.assertNotIn("Google Sheet 쓰기", prompt)
        self.assertNotIn("병합 후 Google Sheet 동기화", prompt)

    def test_existing_adversarial_skill_owns_repository_wide_audit_without_duplicate_skill(self) -> None:
        skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        protocol_path = (
            ROOT
            / "skills"
            / "running-adversarial-review-and-refinement"
            / "references"
            / "repository-wide-audit-protocol.md"
        )
        registry = read("skills/SKILL_REGISTRY.json")

        self.assertIn("`repository-wide-audit`", skill)
        self.assertIn(
            "references/repository-wide-audit-protocol.md",
            skill,
        )
        self.assertTrue(protocol_path.is_file(), str(protocol_path))
        self.assertIn("CURRENT_AUTHORITY", read(protocol_path))
        self.assertIn("UNTOUCHED_CONSUMER", read(protocol_path))
        self.assertIn("repository-wide-audit", registry)
        self.assertNotIn('"skill_id":"repository-wide-adversarial-audit"', registry)

    def test_prompt_and_mode_are_connected_to_active_consumers(self) -> None:
        for path in (
            "START_HERE.md",
            "docs/DOCUMENTATION_MAP.md",
            "templates/project-operations/README.md",
        ):
            self.assertIn(
                "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
                read(path),
                path,
            )

        orchestration = read(
            "docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md"
        )
        self.assertIn("DEMO_FIRST_VERTICAL_SLICE", orchestration)
        self.assertIn("DEMO_VALIDATION", orchestration)
        self.assertIn("TECHNICAL_SPIKE", orchestration)
        self.assertNotIn("→ CORE_POC", orchestration)
        self.assertNotIn("`CORE_POC`·버티컬 슬라이스 계약", orchestration)

        coverage = read("docs/knowledge/VERTICAL_SLICE_V8_TO_V9_MIGRATION.md")
        self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md", coverage)
        self.assertIn("MIGRATION_TRACEABILITY", coverage)
        self.assertIn("active_authority: false", coverage)
        self.assertIn("835EAEEC6205DD3D0BB5D9CE49A8B4940ED07A108E15F6C1B04299446FD5868F", coverage)
        self.assertIn("39AF1CAFE1C8D132667F68AC731AB970615E7B55A09AEA93CFB56141803D0506", coverage)


if __name__ == "__main__":
    unittest.main()
