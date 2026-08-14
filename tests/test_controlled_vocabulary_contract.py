from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / "docs" / "CONTROLLED_VOCABULARY.md"
START_HERE = ROOT / "START_HERE.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class ControlledVocabularyContractTests(unittest.TestCase):
    def test_vocabulary_is_discoverable_without_creating_a_new_skill(self) -> None:
        self.assertTrue(VOCABULARY.is_file())
        vocabulary = VOCABULARY.read_text(encoding="utf-8")
        start_here = START_HERE.read_text(encoding="utf-8")
        registry = REGISTRY.read_text(encoding="utf-8")

        self.assertIn("docs/CONTROLLED_VOCABULARY.md", start_here)
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


if __name__ == "__main__":
    unittest.main()
