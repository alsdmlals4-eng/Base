from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = ROOT / "docs" / "knowledge" / "vertical-slice"


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

    def test_gameplay_validation_is_release_near_vertical_slice_first(self) -> None:
        long_horizon = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        stage = read("docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md")
        slice_skill = read("skills/designing-vertical-slices/SKILL.md")
        concept_skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")

        for token in (
            "RELEASE_NEAR_VERTICAL_SLICE_FIRST",
            "GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE",
            "SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE",
            "TECHNICAL_SPIKE_INTERNAL_ONLY",
        ):
            self.assertIn(token, long_horizon)
            self.assertIn(token, stage)

        for text in (slice_skill, plan):
            self.assertIn("SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED", text)
            for term in ("UI", "이미지", "사운드", "VFX", "시스템"):
                self.assertIn(term, text)

        for text in (concept_skill, plan):
            self.assertIn("PLAYER_APPEAL_QUALITY_GATE", text)
            for term in ("독창성", "DDD", "일관성", "복잡성", "난이도"):
                self.assertIn(term, text)

        for text in (long_horizon, concept_skill, plan):
            self.assertIn("EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT", text)

        for text in (long_horizon, visual, stage, slice_skill, plan):
            self.assertIn("실제 게임 사용 후보", text)
            self.assertIn("player-facing placeholder", text)

        self.assertNotIn("VISUAL_NOT_MATERIAL_TO_THIS_POC", visual)
        self.assertIn("SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE", visual)
        self.assertIn("shipping-intent", visual.lower())
        self.assertIn("별도 `CORE_POC` 제품 단계는 사용하지 않는다", stage)

    def test_concept_lifecycle_treats_poc_as_technical_spike_not_player_validation(self) -> None:
        concept = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        reference = read("skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md")
        self.assertNotIn("POC_BUILD_AND_TEST", concept)
        self.assertNotIn("REPEAT_POC", concept)
        self.assertIn("TECHNICAL_SPIKE_INTERNAL_ONLY", concept)
        self.assertIn("`poc-contract`은 과거 호환 mode", concept)
        self.assertIn("RELEASE_NEAR_VERTICAL_SLICE_FIRST", concept)
        self.assertIn("designing-vertical-slices", concept)
        self.assertNotIn("player_task_and_observed_behavior", reference)
        self.assertNotIn("REPEAT_POC", reference)
        self.assertIn("TECHNICAL_SPIKE_INTERNAL_ONLY", reference)
        self.assertIn("RELEASE_NEAR_VERTICAL_SLICE_FIRST", reference)
        self.assertIn("designing-vertical-slices", reference)

    def test_part_contexts_consume_release_near_rule_and_current_coordinator_semantics(self) -> None:
        p04 = read("docs/operations/base-partitions/P04_GAME_DESIGN_CORE_VERTICAL_SLICE.md")
        p05 = read("docs/operations/base-partitions/P05_ART_UX_UI_VISUAL_ASSETS.md")

        for text in (p04, p05):
            self.assertIn("RELEASE_NEAR_VERTICAL_SLICE_FIRST", text)
            self.assertIn("SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE", text)
            self.assertIn("실제 게임 사용 후보", text)
            self.assertIn("player-facing placeholder", text)
            self.assertIn("OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM", text)
            self.assertNotIn("다른 독립 open/draft/ready PR·branch·worktree는", text)

    def test_knowledge_references_preserve_detail_under_demo_first_authority(self) -> None:
        stage_path = "docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md"
        orchestration_path = "docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md"
        assets_path = "docs/knowledge/vertical-slice/ASSET_MASCOT_AND_TUNING.md"
        stage = read(stage_path)
        orchestration = read(orchestration_path)
        assets = read(assets_path)

        for path in (
            KNOWLEDGE_DIR / "INTEGRATED_DEMO_STAGE_GATES.md",
            KNOWLEDGE_DIR / "SKILL_ORCHESTRATION_AND_EVIDENCE.md",
            KNOWLEDGE_DIR / "ASSET_MASCOT_AND_TUNING.md",
        ):
            self.assertTrue(path.is_file(), str(path))

        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")
        for path in (stage_path, orchestration_path, assets_path):
            self.assertIn(path, plan)

        for gate in (
            "CONCEPT_APPROVAL",
            "DEMO_FIRST_VERTICAL_SLICE",
            "PRODUCTION_APPROVAL",
            "RELEASE_CANDIDATE_APPROVAL",
        ):
            self.assertIn(gate, stage)

        self.assertIn("PROTOTYPE_AND_VERTICAL_SLICE", stage)
        self.assertIn("과거 기록 호환 이름", stage)
        self.assertIn("별도 `CORE_POC` 제품 단계는 사용하지 않는다", stage)
        self.assertIn("TECHNICAL_SPIKE", stage)
        self.assertIn("DEMO_VALIDATION", stage)

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
            "DEMO_FIRST_FULL_PROFILE",
            "VERTICAL_SLICE_FULL_PROFILE",
            "TECHNICAL_SPIKE",
            "DEMO_VALIDATION",
            "GRILL_0_INITIAL_INTENT",
            "P0",
            "Superpowers",
            "DeepSeek",
            "Requirement Coverage",
            "Skill Coverage",
            "Artifact Coverage",
        ):
            self.assertIn(term, orchestration)

        self.assertNotIn("→ CORE_POC", orchestration)
        self.assertNotIn("`CORE_POC`·버티컬 슬라이스 계약", orchestration)
        self.assertNotIn("→ 외부 Slice Validation", orchestration)

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
            "데모 핵심 위험·내부 Spike",
            "WHY→플레이→판매 추적표",
            "PC 통합 데모 패키지",
            "모바일 통합 데모 패키지",
            "Balance Tuning Backlog",
            "Skill 실행 증거",
            "Requirement Coverage",
        ):
            self.assertIn(term, plan)

        self.assertIn("DEMO_FIRST_VERTICAL_SLICE", plan)
        self.assertIn("DEMO_VALIDATION", plan)
        self.assertNotIn("## 2. CORE_POC 결과", plan)

        for state in (
            "EXECUTED_AND_EVIDENCED",
            "EXECUTED_UNVERIFIED",
            "ROUTED_NOT_NEEDED",
            "NOT_AVAILABLE",
            "BLOCKED",
            "FALLBACK_USED",
        ):
            self.assertIn(state, evidence)

    def test_no_duplicate_vertical_slice_or_repository_audit_skill_is_introduced(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        self.assertIn('"skill_id":"designing-vertical-slices"', registry)
        self.assertEqual(registry.count('"skill_id":"designing-vertical-slices"'), 1)
        self.assertEqual(
            registry.count('"skill_id":"running-adversarial-review-and-refinement"'),
            1,
        )
        self.assertIn('"repository-wide-audit"', registry)
        self.assertNotIn('"skill_id":"vertical-slice-master-reference"', registry)
        self.assertNotIn('"skill_id":"repository-wide-adversarial-audit"', registry)
        self.assertNotIn('"integrated-demo-package"', registry)
        self.assertNotIn('"skill-coverage-audit"', registry)

    def test_requirement_coverage_is_non_authoritative_migration_traceability(self) -> None:
        coverage = read("docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md")
        for term in (
            "document_role: MIGRATION_TRACEABILITY",
            "active_authority: false",
            "implementation_authority: NONE",
            "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md",
            "상세 정본 복원·작업 시작 인터뷰·실행 지시를 단일 첨부 파일로 통합",
            "기존 `designing-vertical-slices` Skill의 책임·mode·Registry 계약은 보존",
            "Requirement·Skill·Artifact 완전성",
            "ALLOWED_LEGACY",
            "STALE_PROMPT_CONTRACT",
        ):
            self.assertIn(term, coverage)

    def test_no_orphaned_v6_references_remain_inside_skill_package(self) -> None:
        for path in (
            ROOT / "skills/designing-vertical-slices/references/integrated-demo-stage-gates.md",
            ROOT / "skills/designing-vertical-slices/references/skill-orchestration-and-evidence.md",
            ROOT / "skills/designing-vertical-slices/references/asset-mascot-and-tuning.md",
        ):
            self.assertFalse(path.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
