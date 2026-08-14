from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / "docs" / "CONTROLLED_VOCABULARY.md"
START_HERE = ROOT / "START_HERE.md"
DOCUMENTATION_MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class ControlledVocabularyContractTests(unittest.TestCase):
    def test_vocabulary_is_discoverable_without_creating_a_new_skill(self) -> None:
        self.assertTrue(VOCABULARY.is_file())
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        documentation_map = DOCUMENTATION_MAP.read_text(encoding="utf-8")
        registry = REGISTRY.read_text(encoding="utf-8")

        self.assertIn("docs/CONTROLLED_VOCABULARY.md", start_here)
        self.assertIn("docs/CONTROLLED_VOCABULARY.md", documentation_map)
        self.assertIn("공용 용어", documentation_map)
        self.assertIn("BASE_SHARED", vocabulary)
        self.assertIn("Bounded Context", vocabulary)
        self.assertIn("Ubiquitous Language", vocabulary)
        self.assertNotIn('"id": "terminology"', registry)
        self.assertNotIn('"id": "implementation-reality-gate"', registry)

    def test_product_experiment_terms_answer_different_questions(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Prototype",
            "Spike",
            "Proof of Concept",
            "Walking Skeleton",
            "Graybox / Blockout",
            "First Playable",
            "Vertical Slice",
            "Minimum Viable Product, MVP",
            "Demo",
            "Release Candidate",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("실제 목표 사용자와 핵심 가치 가설을 학습", vocabulary)
        self.assertIn("대표 경험·목표 품질·통합·실제 플레이·반복 제작성", vocabulary)
        self.assertIn("강제 선형 단계가 아니라 서로 다른 검증 질문", vocabulary)

    def test_irg_is_fail_closed_and_explicitly_base_local(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Implementation Reality Gate",
            "BASE_LOCAL_ALIAS",
            "MATERIAL_CLAIM_LEDGER",
            "INTENT_IMPLEMENTATION_FIDELITY_MATRIX",
            "COMPLETION_CLAIM_GATE",
            "Evidence Provenance",
            "Evidence Ceiling",
            "exact-HEAD fresh execution",
            "CLAIM_UNVERIFIED",
            "IMPLEMENTATION_UNVERIFIED",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("업계 표준 용어가 아니다", vocabulary)
        self.assertIn("테스트 파일 존재를 테스트 실행", vocabulary)
        self.assertIn("정적 PASS를 runtime", vocabulary)

    def test_project_management_terms_preserve_scrum_and_generic_boundaries(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Milestone",
            "Sprint",
            "Product Backlog",
            "Backlog",
            "Epic",
            "User Story",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Sprint ≠ Milestone", vocabulary)
        self.assertIn("Epic과 User Story는 Scrum Guide의 필수 Artifact가 아니다", vocabulary)
        self.assertIn("User Story ≠ 전체 명세", vocabulary)

    def test_release_terms_do_not_collapse_alpha_beta_early_access_rc_and_gold(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Alpha",
            "Beta",
            "Early Access",
            "Release Candidate",
            "Gold / Gold Master",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Alpha·Beta는 조직별 Entry/Exit Criteria", vocabulary)
        self.assertIn("Early Access ≠ Beta", vocabulary)
        self.assertIn("Early Access ≠ Pre-Purchase", vocabulary)
        self.assertIn("Gold / Gold Master ≠ Release Candidate", vocabulary)

    def test_testing_terms_separate_level_purpose_acceptance_and_base_recheck(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Component / Unit Test",
            "Integration Test",
            "End-to-End / E2E Test",
            "Smoke Test",
            "Sanity Test",
            "User Acceptance Testing / UAT",
            "Regression Testing",
            "Regression Recheck",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Smoke/Sanity의 경계는 조직별 편차가 크다", vocabulary)
        self.assertIn("UAT ≠ 일반 QA", vocabulary)
        self.assertIn("Regression Testing ≠ Regression Recheck", vocabulary)

    def test_code_maintenance_terms_distinguish_signal_debt_refactor_and_rewrite(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Code Smell",
            "Technical Debt",
            "Refactor",
            "Rewrite",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Refactor = 외부 관찰 가능한 동작·계약을 보존", vocabulary)
        self.assertIn("Rewrite ≠ 큰 Refactor", vocabulary)
        self.assertIn("Code Smell ≠ 버그·Technical Debt 확정 증거", vocabulary)

    def test_git_and_version_terms_preserve_operation_and_versioning_boundaries(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Branch",
            "Rebase",
            "Cherry-pick",
            "Hotfix",
            "Semantic Versioning / SemVer",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Rebase ≠ Merge", vocabulary)
        self.assertIn("Cherry-pick ≠ Branch Merge", vocabulary)
        self.assertIn("Hotfix ≠ Git 명령", vocabulary)
        self.assertIn("SemVer는 public API를 선언", vocabulary)

    def test_wave2_keeps_one_canonical_row_and_does_not_force_unit_component_equivalence(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")

        self.assertEqual(vocabulary.count("| **Release Candidate** |"), 1)
        self.assertEqual(vocabulary.count("| **Regression Recheck** |"), 1)
        self.assertIn("Component / Unit Test는 검색 묶음 이름", vocabulary)
        self.assertIn("Unit Test를 모든 조직에서 Component Test와 완전히 동일한 범위로 강제하지 않는다", vocabulary)
        self.assertIn("STANDARDIZED_CONTEXT (ISTQB)", vocabulary)

    def test_work_tracking_terms_separate_issue_bug_defect_and_incident(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in ("Issue", "Bug", "Defect", "Incident"):
            self.assertIn(term, vocabulary)

        self.assertIn("Issue ≠ Bug", vocabulary)
        self.assertIn("Incident ≠ 개별 Bug/Defect", vocabulary)
        self.assertIn(
            "Bug와 Defect를 모든 조직에서 완전히 동일하거나 완전히 다른 용어로 강제하지 않는다",
            vocabulary,
        )

    def test_requirement_terms_separate_requirement_specification_and_constraint(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in ("Requirement", "Specification", "Constraint"):
            self.assertIn(term, vocabulary)

        self.assertIn("Requirement ≠ Specification", vocabulary)
        self.assertIn("Constraint를 Requirement의 보편적 하위형으로 강제하지 않는다", vocabulary)
        self.assertIn("Acceptance Criteria ≠ Requirement 전체", vocabulary)

    def test_structure_terms_distinguish_dependency_coupling_and_cohesion(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in ("Dependency", "Coupling", "Cohesion"):
            self.assertIn(term, vocabulary)

        self.assertIn("Dependency 존재 ≠ Tight Coupling 확정", vocabulary)
        self.assertIn("Coupling = 모듈 간 상호의존 정도", vocabulary)
        self.assertIn("Cohesion = 한 모듈 내부 책임들의 논리적 관련성", vocabulary)

    def test_interface_terms_distinguish_api_abi_protocol_and_schema(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in ("API", "ABI", "Protocol", "Schema"):
            self.assertIn(term, vocabulary)

        self.assertIn("API compatibility ≠ ABI compatibility", vocabulary)
        self.assertIn("Protocol ≠ Endpoint 목록", vocabulary)
        self.assertIn("Schema ≠ Protocol", vocabulary)
        self.assertIn("OpenAPI ≠ 모든 종류의 API", vocabulary)
        self.assertIn("JSON Schema ≠ 모든 종류의 Schema", vocabulary)

    def test_delivery_terms_distinguish_build_package_artifact_deployment_and_release(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in ("Build", "Package", "Artifact", "Deployment", "Release"):
            self.assertIn(term, vocabulary)

        self.assertIn("Build process ≠ Build output", vocabulary)
        self.assertIn("Artifact ≠ Package", vocabulary)
        self.assertIn("Deployment ≠ Release", vocabulary)
        self.assertIn("Release Candidate ≠ Release", vocabulary)

    def test_observability_terms_distinguish_telemetry_metrics_logs_traces_and_profiles(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        for term in (
            "Telemetry",
            "Metrics",
            "Logging / Logs",
            "Tracing / Traces",
            "Profiling / Profiles",
        ):
            self.assertIn(term, vocabulary)

        self.assertIn("Metrics ≠ Logs", vocabulary)
        self.assertIn("Logs ≠ Traces", vocabulary)
        self.assertIn("Tracing ≠ Profiling", vocabulary)
        self.assertIn("관측 signal 존재 ≠ 원인 규명 완료", vocabulary)

    def test_wave3_preserves_canonical_rows_and_context_limits(self) -> None:
        vocabulary = VOCABULARY.read_text(encoding="utf-8")

        self.assertEqual(vocabulary.count("| **Release Candidate** |"), 1)
        self.assertEqual(vocabulary.count("| **Regression Recheck** |"), 1)
        self.assertEqual(vocabulary.count("| **Release** |"), 1)
        self.assertIn("ARTIFACT Kind ≠ Build Artifact", vocabulary)
        self.assertIn("OpenTelemetry Profiles의 Alpha 상태 ≠ Profiling 일반의 Alpha 상태", vocabulary)


if __name__ == "__main__":
    unittest.main()
