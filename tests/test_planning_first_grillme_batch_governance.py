from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
POLICY = "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"
TEMPLATE = "templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class PlanningFirstGrillMeBatchGovernanceTests(unittest.TestCase):
    def test_agents_routes_to_the_single_detailed_policy(self) -> None:
        agents = read("AGENTS.md")
        self.assertIn("기획 우선 원칙", agents)
        self.assertIn(POLICY, agents)
        self.assertIn("승인된 실행 계약", agents)
        self.assertIn("L0", agents)
        self.assertLess(agents.index("기획 우선 원칙"), agents.index("BUILD"))
        self.assertTrue((ROOT / POLICY).is_file())
        self.assertTrue((ROOT / TEMPLATE).is_file())

    def test_detailed_numeric_defaults_and_planning_conflicts_are_separated(self) -> None:
        policy = read(POLICY)
        for term in (
            "DETAILED_NUMERIC_DEFAULT",
            "RECOMMENDED_DEFAULT",
            "PLANNING_CONFLICT",
            "USER_DECISION_REQUIRED",
            "GRILL_ME_REQUIRED",
            "난이도 곡선",
            "경제",
            "성장 속도",
            "세션 길이",
            "보상 의미",
        ):
            self.assertIn(term, policy)

    def test_grill_me_batch_is_max_ten_with_early_checkpoint(self) -> None:
        policy = read(POLICY)
        for term in (
            "MAX_APPROVED_DECISIONS_PER_BATCH: 10",
            "GM-BATCH-YYYY-MM-DD-NN",
            "조기 체크포인트",
            "TEN_APPROVALS",
            "HIGH_IMPACT",
            "CANON_CONFLICT",
            "IMPLEMENTATION_BLOCKED",
            "SESSION_END",
            "USER_REQUEST",
            "DIFF_SIZE",
            "11번째 질문",
            "병합·재동기화 전",
            "10건 미만",
        ):
            self.assertIn(term, policy)
        self.assertIn("최대 승인 Decision 수", policy)
        self.assertIn("최소량", policy)

    def test_immediate_recording_and_merged_main_sync_are_distinct(self) -> None:
        policy = read(POLICY)
        for term in (
            "활성 배치 Branch",
            "Decision별 논리 Commit",
            "APPROVED_PENDING_MERGE",
            "BATCH_PR_OPEN",
            "SYNCED_TO_MAIN",
            "merged main SHA",
            "Sheet",
            "main 동기화 완료를 주장하지 않는다",
        ):
            self.assertIn(term, policy)

    def test_batch_merge_requires_exact_head_checks_and_adversarial_review(self) -> None:
        policy = read(POLICY)
        for term in (
            "exact-head",
            "attack → validate-critique → regression-recheck → decision-report",
            "unresolved thread 0",
            "P0/P1 0",
            "하나의 활성 Grill Me 배치 PR",
        ):
            self.assertIn(term, policy)

    def test_checkpoint_template_exposes_batch_state_and_evidence_limits(self) -> None:
        template = read(TEMPLATE)
        for term in (
            "grill_me_batch_id",
            "max_approved_decisions_per_batch: 10",
            "approved_decision_count",
            "checkpoint_reason",
            "batch_pr",
            "batch_exact_head",
            "required_checks",
            "adversarial_review",
            "merge_commit",
            "APPROVED_PENDING_MERGE",
            "SYNCED_TO_MAIN",
            "real_project_batch_execution",
            "external_model_behavior",
            "human_process_usability",
        ):
            self.assertIn(term, template)

    def test_policy_names_official_review_benchmarks_and_keeps_them_non_authoritative(self) -> None:
        policy = read(POLICY)
        self.assertIn("google.github.io/eng-practices/review/developer/small-cls.html", policy)
        self.assertIn("google.github.io/eng-practices/review/reviewer/standard.html", policy)
        self.assertIn("docs.github.com", policy)
        self.assertIn("외부 벤치마크는 요구사항 정본이 아니다", policy)

    def test_released_registry_and_v941_lock_remain_unchanged(self) -> None:
        registry = ROOT / "skills/SKILL_REGISTRY.json"
        self.assertEqual(EXPECTED_REGISTRY_SHA256, hashlib.sha256(registry.read_bytes()).hexdigest())
        lock = json.loads((ROOT / "base-v9.4.1.lock.json").read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EXPECTED_REGISTRY_SHA256, lock["candidate_registry"]["sha256"])


if __name__ == "__main__":
    unittest.main()
