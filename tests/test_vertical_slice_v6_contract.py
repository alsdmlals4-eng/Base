from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "designing-vertical-slices"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class VerticalSliceV6ContractTests(unittest.TestCase):
    def test_existing_vertical_slice_skill_authority_is_preserved(self) -> None:
        skill = read("skills/designing-vertical-slices/SKILL.md")
        for mode in (
            "slice-contract",
            "quality-bar",
            "pipeline-proof",
            "playtest-evidence",
            "decision-gate",
        ):
            self.assertIn(f"`{mode}`", skill)

        for decision in ("EXPAND", "REWORK", "REPEAT_SLICE", "HOLD", "STOP"):
            self.assertIn(decision, skill)

        self.assertIn("templates/planning/VERTICAL_SLICE_PLAN.md", skill)
        self.assertNotIn("integrated-demo-package", skill)
        self.assertNotIn("skill-coverage-audit", skill)

    def test_conditional_references_exist_and_preserve_v6_responsibilities(self) -> None:
        stage = read("skills/designing-vertical-slices/references/integrated-demo-stage-gates.md")
        orchestration = read("skills/designing-vertical-slices/references/skill-orchestration-and-evidence.md")
        assets = read("skills/designing-vertical-slices/references/asset-mascot-and-tuning.md")

        for path in (
            SKILL_DIR / "references/integrated-demo-stage-gates.md",
            SKILL_DIR / "references/skill-orchestration-and-evidence.md",
            SKILL_DIR / "references/asset-mascot-and-tuning.md",
        ):
            self.assertTrue(path.is_file(), str(path))

        for gate in (
            "CONCEPT_APPROVAL",
            "PROTOTYPE_AND_VERTICAL_SLICE",
            "PRODUCTION_APPROVAL",
            "RELEASE_CANDIDATE_APPROVAL",
        ):
            self.assertIn(gate, stage)

        for term in (
            "Steam 메인, STOVE, itch.io",
            "Steam 출시 예정 페이지",
            "STOVE 피드백",
            "Steam Playtest",
            "텀블벅 준비도",
            "Google Play만 고려",
        ):
            self.assertIn(term, stage)

        for term in (
            "PLANNING_ONLY_PROFILE",
            "VERTICAL_SLICE_FULL_PROFILE",
            "GRILL_0_INITIAL_INTENT",
            "P0",
            "Superpowers",
            "DeepSeek",
            "Requirement Coverage",
            "Skill Coverage",
            "Artifact Coverage",
        ):
            self.assertIn(term, orchestration)

        for term in (
            "에셋스토어",
            "적합한 자산이 없거나",
            "세계관 마스코트",
            "INITIAL_TEST_VALUE",
            "PLAYTEST_TUNING_REQUIRED",
            "Asset License Ledger",
        ):
            self.assertIn(term, assets)

    def test_templates_capture_demo_package_and_skill_evidence(self) -> None:
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")
        evidence = read("templates/project-operations/SKILL_EXECUTION_EVIDENCE.md")

        for term in (
            "CORE_POC 결과",
            "WHY→플레이→판매 추적표",
            "PC 통합 데모 패키지",
            "모바일 통합 데모 패키지",
            "Balance Tuning Backlog",
            "Skill 실행 증거",
            "Requirement Coverage",
        ):
            self.assertIn(term, plan)

        for state in (
            "EXECUTED_AND_EVIDENCED",
            "EXECUTED_UNVERIFIED",
            "ROUTED_NOT_NEEDED",
            "NOT_AVAILABLE",
            "BLOCKED",
            "FALLBACK_USED",
        ):
            self.assertIn(state, evidence)

    def test_no_new_duplicate_skill_or_registry_trigger_is_introduced(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        self.assertIn('"skill_id":"designing-vertical-slices"', registry)
        self.assertEqual(registry.count('"skill_id":"designing-vertical-slices"'), 1)
        self.assertNotIn('"skill_id":"vertical-slice-master-reference"', registry)
        self.assertNotIn('"integrated-demo-package"', registry)
        self.assertNotIn('"skill-coverage-audit"', registry)

    def test_requirement_coverage_document_maps_v6_without_duplicate_canonical_source(self) -> None:
        coverage = read("docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md")
        for term in (
            "대형 중복 정본",
            "기존 `designing-vertical-slices` Skill의 책임·mode·Registry 계약은 보존",
            "Requirement·Skill·Artifact 완전성",
            "v6 전체를 하나의 활성 Base 문서로 복제하지 않는다",
            "기존 Skill 본문을 바꾸지 않아 Registry·Learning Log companion 계약",
        ):
            self.assertIn(term, coverage)


if __name__ == "__main__":
    unittest.main()
