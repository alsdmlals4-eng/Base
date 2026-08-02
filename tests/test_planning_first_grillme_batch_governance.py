from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class PlanningFirstGrillMeBatchGovernanceTests(unittest.TestCase):
    def test_planning_first_authority_precedes_build(self) -> None:
        for relative in (
            "AGENTS.md",
            "docs/OPERATING_MODEL.md",
            "docs/WORK_MODE_AND_SKILL_ROUTING.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
        ):
            with self.subTest(relative=relative):
                text = read(relative)
                self.assertIn("기획 우선 원칙", text)
                self.assertIn("승인된 실행 계약", text)
                self.assertIn("L0", text)
                self.assertLess(text.index("기획 우선 원칙"), text.index("BUILD"))

    def test_detailed_numeric_defaults_and_planning_conflicts_are_separated(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        grill = read(
            "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
        )
        sync = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for text in (intake, grill, sync):
            self.assertIn("DETAILED_NUMERIC_DEFAULT", text)
            self.assertIn("RECOMMENDED_DEFAULT", text)
            self.assertIn("PLANNING_CONFLICT", text)
            self.assertIn("USER_DECISION_REQUIRED", text)
            self.assertIn("GRILL_ME_REQUIRED", text)
        self.assertIn("난이도 곡선", grill)
        self.assertIn("경제", grill)
        self.assertIn("성장 속도", grill)
        self.assertIn("세션 길이", grill)
        self.assertIn("보상 의미", grill)

    def test_grill_me_batch_is_max_ten_with_early_checkpoint(self) -> None:
        grill = read(
            "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
        )
        sync = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        lifecycle = read("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md")
        for text in (grill, sync, lifecycle):
            self.assertIn("MAX_APPROVED_DECISIONS_PER_BATCH: 10", text)
            self.assertIn("GM-BATCH-YYYY-MM-DD-NN", text)
            self.assertIn("조기 체크포인트", text)
            self.assertIn("TEN_APPROVALS", text)
            self.assertIn("HIGH_IMPACT", text)
            self.assertIn("CANON_CONFLICT", text)
            self.assertIn("SESSION_END", text)
            self.assertIn("USER_REQUEST", text)
        self.assertIn("11번째 질문", grill)
        self.assertIn("병합·재동기화 전", grill)
        self.assertIn("10건 미만", grill)

    def test_immediate_recording_and_merged_main_sync_are_distinct(self) -> None:
        grill = read(
            "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
        )
        sync = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        for text in (grill, sync):
            self.assertIn("활성 배치 Branch", text)
            self.assertIn("Decision별 논리 Commit", text)
            self.assertIn("APPROVED_PENDING_MERGE", text)
            self.assertIn("BATCH_PR_OPEN", text)
            self.assertIn("SYNCED_TO_MAIN", text)
            self.assertIn("merged main SHA", text)
            self.assertIn("Sheet", text)
        self.assertIn("main 동기화 완료를 주장하지 않는다", sync)

    def test_batch_merge_requires_exact_head_checks_and_adversarial_review(self) -> None:
        routing = read("docs/WORK_MODE_AND_SKILL_ROUTING.md")
        sync = read("docs/CONFIRMED_DECISION_SYNC_POLICY.md")
        lifecycle = read("docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md")
        for text in (routing, sync, lifecycle):
            self.assertIn("exact-head", text)
            self.assertIn(
                "attack → validate-critique → regression-recheck → decision-report",
                text,
            )
            self.assertIn("unresolved thread 0", text)
            self.assertIn("P0/P1 0", text)
        self.assertIn("하나의 활성 Grill Me 배치 PR", lifecycle)

    def test_decision_record_template_exposes_batch_state(self) -> None:
        template = read("templates/project-operations/GRILL_ME_DECISION_RECORD.md")
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
        ):
            self.assertIn(term, template)

    def test_released_registry_and_v941_lock_remain_unchanged(self) -> None:
        registry = ROOT / "skills/SKILL_REGISTRY.json"
        self.assertEqual(EXPECTED_REGISTRY_SHA256, hashlib.sha256(registry.read_bytes()).hexdigest())
        lock = json.loads((ROOT / "base-v9.4.1.lock.json").read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EXPECTED_REGISTRY_SHA256, lock["candidate_registry"]["sha256"])


if __name__ == "__main__":
    unittest.main()
