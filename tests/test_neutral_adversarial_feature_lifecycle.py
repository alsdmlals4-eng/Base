from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
EXPECTED_REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class NeutralAdversarialFeatureLifecycleTests(unittest.TestCase):
    def test_always_on_authority_rejects_both_bias_directions(self) -> None:
        agents = read("AGENTS.md")
        for term in (
            "사용자 주장과 AI의 최초 제안",
            "동일한 평가 기준",
            "근거 없는 동의",
            "반대를 위한 반대",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, agents)

    def test_operating_model_connects_feature_delivery_end_to_end(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")
        for term in (
            "중립적 적대 검토 Gate",
            "문제·사용자 가치·완료 기준",
            "대안·반증·위험",
            "분야 Skill BUILD",
            "책임 원본·상태·발행·Handoff",
            "Learning Log",
        ):
            self.assertIn(term, operating)

    def test_routing_keeps_lightweight_and_full_review_boundaries(self) -> None:
        routing = read("docs/WORK_MODE_AND_SKILL_ROUTING.md")
        for term in (
            "경량 중립성 Gate",
            "L0",
            "L1 이상",
            "동의 편향",
            "반대를 위한 반대",
            "running-adversarial-review-and-refinement",
        ):
            self.assertIn(term, routing)

    def test_continuous_work_reuses_adversarial_lifecycle_without_bypassing_user_gates(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        reference = read("skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md")
        task_recovery = read("skills/managing-project-intake-and-work-contract/references/task-recovery-protocol.md")
        routing = read("docs/WORK_MODE_AND_SKILL_ROUTING.md")
        operating = read("docs/OPERATING_MODEL.md")
        agents = read("AGENTS.md")

        for text in (intake, reference, routing, operating, agents):
            self.assertIn("[연속작업] 진행해", text)
            self.assertIn("USER_DECISION_REQUIRED", text)
            self.assertIn("BLOCKED_UNVERIFIED", text)

        for term in (
            "CONTINUOUS_WORK_ACTIVE",
            "CONTINUOUS_WORK_INACTIVE",
            "attack → validate-critique",
            "regression-recheck",
            "현재 승인된 작업 계약",
            "범위 확대",
            "백그라운드",
        ):
            self.assertIn(term, reference)

        for term in (
            "TASK_RECOVERY_PROTOCOL",
            "RETRY",
            "RESUME",
            "연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다",
            "이미 완료된 단계는 다시 실행하지 않는다",
        ):
            self.assertIn(term, task_recovery)

        self.assertIn("task-recovery-protocol.md", intake)
        self.assertIn("Work Mode를 대체하지 않는다", reference)
        self.assertIn("scheduler", reference)
        self.assertIn("webhook", reference)
        self.assertIn("자동 메시지 전달", reference)
        self.assertIn("기존 승인·Grill Me", reference)
        self.assertIn("트리거가 없는", reference)
        self.assertIn("기술적 단일 최소 안전 finding이면 자동 승인", routing)

    def test_registry_balanced_only_exclusion_is_narrow_and_full_loop_resumes(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        adversarial_entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "running-adversarial-review-and-refinement"
        )
        self.assertTrue(
            any("칭찬·균형 평가만 요청" in item for item in adversarial_entry["do_not_use_when"])
        )

        routing = read("docs/WORK_MODE_AND_SKILL_ROUTING.md")
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "결정·권장안이 없는 설명형 칭찬·균형 요약",
            "PLAN 사전판정",
            "`refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정",
            "regression-recheck → decision-report",
        ):
            self.assertIn(term, routing)
        self.assertIn("PLAN 사전판정", intake)
        self.assertIn("결정·권장안이 없는 설명형 칭찬·균형 요약", adversarial)
        self.assertIn("이미 구현된 finding을 다시 수정하지 않는다", adversarial)

    def test_intake_requires_neutral_recommendation_before_contract(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        for term in (
            "neutral-recommendation-gate",
            "evaluation_criteria",
            "alternatives",
            "counterevidence",
            "reversibility",
            "recommended_conclusion",
        ):
            self.assertIn(term, intake)
        self.assertLess(
            intake.index("neutral-recommendation-gate"),
            intake.index("### 5. Closure and confirmation"),
        )

    def test_adversarial_review_is_symmetric_without_manufactured_opposition(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "사용자안",
            "AI 최초안",
            "같은 평가 기준",
            "반대를 위한 반대",
            "동의할 수 있다",
        ):
            self.assertIn(term, adversarial)

    def test_adversarial_review_repeats_minimum_five_then_until_verified_clean_exit(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "FULL_SCOPE_REVIEW",
            "FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "CLEAN_REVIEW_EXIT",
            "loop_index",
            "최소 5회의 완전한 전체 개선 루프",
            "5회 이후에도",
            "새로운 유효 오류·충돌·누락·blocking finding이 0",
            "이미 구현된 finding을 다시 수정하지 않는다",
        ):
            self.assertIn(term, adversarial)

        self.assertNotIn("FIVE_DISTINCT_ADVERSARIAL_ROUNDS", adversarial)
        self.assertNotIn("ROUND_1_INTENT_ASSUMPTIONS_SCOPE", adversarial)

    def test_p03_current_main_evidence_bounded_takeover(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        finding = read("skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md")
        audit = read("skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md")
        postmerge = read("templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md")
        sync = read("skills/synchronizing-local-and-github-state/SKILL.md")
        safe_sync = read("skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md")

        for token in ("FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE", "FULL_LOOP_IS_NOT_A_REVIEW_LENS", "Loop 1=scope"):
            self.assertIn(token, adversarial)
        for text in (finding, audit, postmerge):
            self.assertIn("CONFIGURED_PROJECT_WORKSPACE", text)
        for text in (sync, safe_sync):
            for token in ("execution_surface", "GITHUB_CONNECTOR_ONLY", "NOT_APPLICABLE_CONNECTOR_ONLY", "OPEN_PR_READ_ONLY_BY_DEFAULT"):
                self.assertIn(token, text)

    def test_socratic_review_lens_is_selective_evidence_first_and_meta_validated(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        socratic = read(
            "skills/running-adversarial-review-and-refinement/references/"
            "socratic-questioning-lenses.md"
        )

        for term in (
            "Socratic Review Lens",
            "references/socratic-questioning-lenses.md",
            "저장소·정본·실제 구현·도구",
            "사용자에게 묻지 않는다",
            "관련된 Lens만",
            "가짜 Finding",
        ):
            self.assertIn(term, adversarial)

        for term in (
            "Clarification",
            "Assumptions",
            "Reasons / Evidence",
            "Viewpoints",
            "Implications / Consequences",
            "Meta-question",
            "관련된 Lens만",
            "가짜 Finding",
            "사용자 질문은 마지막 수단",
            "BLOCKED_UNVERIFIED",
            "USER_DECISION_REQUIRED",
            "답이 달라지면 실제 결정도 달라지는가",
        ):
            self.assertIn(term, socratic)

        self.assertNotIn("skill_id: socratic-questioning", socratic)

    def test_post_change_monitor_loop_rechecks_prs_omissions_conflicts_and_complements(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        operating = read("docs/OPERATING_MODEL.md")

        for text in (adversarial, operating):
            for term in (
                "POST_CHANGE_MONITOR_LOOP",
                "same-goal-open-and-recent-pr-recheck",
                "untouched-consumer-and-derivative-recheck",
                "OMISSION",
                "CONFLICT",
                "COMPLEMENT_GAP",
                "DUPLICATE_WORK",
                "NO_MATERIAL_FOLLOWUP",
                "exact-head-validation",
                "post-merge-main-readback",
            ):
                self.assertIn(term, text)

        for term in (
            "변경을 완료로 보고하기 전",
            "병합 뒤",
            "새 변경을 만들지 않는다",
            "백그라운드 실행을 의미하지 않는다",
        ):
            self.assertIn(term, adversarial)

    def test_behavior_fixture_covers_sycophancy_boundary(self) -> None:
        data = json.loads((ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(item for item in data["cases"] if item["case_id"] == "SBE-011")
        self.assertEqual("boundary", case["case_type"])
        self.assertEqual("PLAN", case["expected_work_mode"])
        self.assertEqual("managing-project-intake-and-work-contract", case["expected_primary_skill"])
        self.assertEqual(
            ["running-adversarial-review-and-refinement"],
            case["expected_supporting_skills"],
        )
        self.assertEqual(
            {"평가 기준", "대안", "반증", "위험", "미검증"},
            set(case["required_evidence"]),
        )
        self.assertEqual("REQUIRED", case["expected_user_decision_state"])

    def test_behavior_fixtures_cover_opposition_pressure_and_evidence_gap(self) -> None:
        data = json.loads((ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = {item["case_id"]: item for item in data["cases"]}
        opposition = cases["SBE-012"]
        evidence_gap = cases["SBE-013"]

        for case in (opposition, evidence_gap):
            self.assertEqual("boundary", case["case_type"])
            self.assertEqual("PLAN", case["expected_work_mode"])
            self.assertEqual("managing-project-intake-and-work-contract", case["expected_primary_skill"])
            self.assertEqual(
                ["running-adversarial-review-and-refinement"],
                case["expected_supporting_skills"],
            )
            self.assertEqual(
                ["route", "attack", "validate-critique", "decision-report"],
                case["expected_skill_modes"],
            )

        self.assertIn("무조건 틀렸", opposition["prompt"])
        self.assertEqual(
            {"동일 평가 기준", "장점", "반증", "위험", "권장 결론"},
            set(opposition["required_evidence"]),
        )
        self.assertEqual("REQUIRED", opposition["expected_user_decision_state"])

        self.assertIn("증거가 없", evidence_gap["prompt"])
        self.assertEqual(
            {"증거 한계", "BLOCKED_UNVERIFIED", "확인 조건", "미검증"},
            set(evidence_gap["required_evidence"]),
        )
        self.assertEqual("DEFERRED", evidence_gap["expected_user_decision_state"])

    def test_behavior_fixture_excludes_decisionless_balanced_summary(self) -> None:
        data = json.loads((ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = {item["case_id"]: item for item in data["cases"]}
        summary = cases["SBE-014"]

        self.assertEqual("boundary", summary["case_type"])
        self.assertEqual("PLAN", summary["expected_work_mode"])
        self.assertEqual("creating-user-learning-notes", summary["expected_primary_skill"])
        self.assertEqual([], summary["expected_supporting_skills"])
        self.assertEqual(["capture", "explain"], summary["expected_skill_modes"])
        self.assertIn("running-adversarial-review-and-refinement", summary["forbidden_skills"])
        self.assertIn("managing-project-intake-and-work-contract", summary["forbidden_skills"])
        self.assertIn("권장하거나 결정하지 말고", summary["prompt"])
        self.assertEqual(
            {"장점", "한계", "미결정"},
            set(summary["required_evidence"]),
        )
        self.assertEqual("NOT_REQUIRED", summary["expected_user_decision_state"])

    def test_poc_survivors_promote_to_l2_detail_without_a_new_active_skill(self) -> None:
        concepts = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        documents = read("skills/managing-design-documents/SKILL.md")
        template = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
        traceability = read("templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md")
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        skill_ids = {entry["skill_id"] for entry in registry["skills"]}

        for term in (
            "KEEP / CHANGE / RETEST",
            "pre-PoC",
            "REMOVE / DEFER",
            "승격",
            "GAME_FEATURE_DESIGN_SPEC.md",
        ):
            self.assertIn(term, concepts)
        for term in (
            "L0 Project Direction",
            "L1 Feature Brief",
            "L2 GAME_FEATURE_DESIGN_SPEC",
            "L3 FEATURE_SPEC_TRACEABILITY_PACKET",
            "Task progress",
            "executed verification",
            "reference/compose",
        ):
            self.assertIn(term, documents)
        for term in (
            "Player Problem",
            "Player Verbs",
            "Entry / Exit / Cancel / Re-entry",
            "State & Rules",
            "Acceptance Criteria",
            "Cut-down / Rollback",
            "USER_DECISION_REQUIRED",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, template)
        self.assertIn("design_spec_id", traceability)
        self.assertIn("canonical_design_spec_path", traceability)
        self.assertNotIn("game-feature-design", skill_ids)

    def test_reference_freshness_recognizes_the_focused_contract_test(self) -> None:
        config = json.loads((ROOT / ".github" / "reference-freshness.json").read_text(encoding="utf-8"))
        rule = next(
            item
            for item in config["coupled_change_rules"]
            if item["name"] == "local-skill-contract-learning-test-sync"
        )
        self.assertIn(
            "tests/test_neutral_adversarial_feature_lifecycle.py",
            rule["require_any_changed"],
        )

    def test_released_registry_identity_remains_pinned_while_current_registry_can_evolve(self) -> None:
        lock = json.loads((ROOT / "base-v9.4.lock.json").read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EXPECTED_REGISTRY_SHA256, lock["candidate_registry"]["sha256"])
        current = json.loads(REGISTRY.read_text(encoding="utf-8"))
        current_ids = {entry["skill_id"] for entry in current["skills"]}
        self.assertIn("running-adversarial-review-and-refinement", current_ids)


if __name__ == "__main__":
    unittest.main()
