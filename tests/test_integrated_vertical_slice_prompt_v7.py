from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "templates" / "prompts" / "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md"


def read(path: str | Path) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class IntegratedVerticalSlicePromptV7Tests(unittest.TestCase):
    def test_single_attachment_prompt_exists_and_replaces_split_v6_usage(self) -> None:
        self.assertTrue(PROMPT_PATH.is_file(), str(PROMPT_PATH))
        prompt = read(PROMPT_PATH)

        for term in (
            'contract_name: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT',
            'contract_version: "7.0"',
            "execution_model: INTERVIEW_DRIVEN_INTEGRATED_EXECUTION",
            "이 파일 하나만 첨부",
            "별도 축약 실행문을 요구하지 않는다",
            "STALE_PROMPT_CONTRACT",
        ):
            self.assertIn(term, prompt)

    def test_prompt_uses_current_preflight_planning_and_demo_first_contracts(self) -> None:
        prompt = read(PROMPT_PATH)

        for term in (
            "BASE_EXCLUDED",
            "DUPLICATE_OMISSION_CONFLICT_AUDIT",
            "EVIDENCE_PACK",
            "APPROVAL_BUNDLE",
            "PROPAGATION_AUDIT",
            "BENCHMARK_EVIDENCE",
            "PLAYER_RESPONSE_EVIDENCE",
            "PROFESSIONAL_OFFICIAL_EVIDENCE",
            "DEMO_FIRST_VERTICAL_SLICE",
            "DEMO_VALIDATION",
            "TECHNICAL_SPIKE",
            "00 프로젝트 기반·현재 상태",
            "80 완성 품질 Vertical Slice 데모·플레이테스트",
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
            "작업 시작 인터뷰",
            "이미 유효한 Decision을 다시 묻지 않는다",
            "RECOMMENDED_DEFAULT",
            "USER_DECISION_REQUIRED",
            "GPT→Codex",
            "repository-wide-audit",
            "CURRENT_AUTHORITY",
            "ACTIVE_CONSUMER",
            "ALLOWED_LEGACY",
            "Requirement Coverage",
            "Skill Coverage",
            "Artifact Coverage",
        ):
            self.assertIn(term, prompt)

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
                "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md",
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

        coverage = read("docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md")
        self.assertIn("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md", coverage)
        self.assertIn("MIGRATION_TRACEABILITY", coverage)
        self.assertIn("active_authority: false", coverage)


if __name__ == "__main__":
    unittest.main()
