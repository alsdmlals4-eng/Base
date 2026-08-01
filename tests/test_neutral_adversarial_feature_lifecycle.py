from __future__ import annotations

import hashlib
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

    def test_released_registry_identity_remains_unchanged(self) -> None:
        self.assertEqual(EXPECTED_REGISTRY_SHA256, hashlib.sha256(REGISTRY.read_bytes()).hexdigest())
        lock = json.loads((ROOT / "base-v9.4.lock.json").read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EXPECTED_REGISTRY_SHA256, lock["candidate_registry"]["sha256"])


if __name__ == "__main__":
    unittest.main()
