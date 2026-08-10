from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md"
TEMPLATE = ROOT / "templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md"
SKILL = ROOT / "skills/analyzing-and-refining-game-concepts/SKILL.md"
START = ROOT / "START_HERE.md"
INDEX = ROOT / "docs/knowledge/game-development/README.md"
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"


class TutorialAndOnboardingDesignContractTests(unittest.TestCase):
    def test_learning_ladder_and_failure_boundaries_exist(self) -> None:
        self.assertTrue(GUIDE.is_file(), "tutorial guide must exist")
        guide = GUIDE.read_text(encoding="utf-8")
        for token in ("RULE", "NEED", "DISCOVER", "FEEL", "PROVE", "TRANSFER"):
            self.assertIn(token, guide)
        for phrase in (
            "강제 패배",
            "정적 조작표",
            "가짜 성장",
            "안내 없는 독립 수행",
            "다른 상황에서 재사용",
        ):
            self.assertIn(phrase, guide)

    def test_project_first_evidence_and_accessibility_contract(self) -> None:
        self.assertTrue(GUIDE.is_file(), "tutorial guide must exist")
        self.assertTrue(TEMPLATE.is_file(), "tutorial contract template must exist")
        combined = GUIDE.read_text(encoding="utf-8") + TEMPLATE.read_text(encoding="utf-8")
        for phrase in (
            "프로젝트 정본",
            "실제 코드",
            "Google Sheets",
            "벤치마크",
            "플레이테스트",
            "텔레메트리",
            "Skip",
            "복습",
            "접근성 대체 채널",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(phrase, combined)

    def test_existing_skill_owns_tutorial_design_without_new_broad_skill(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("tutorial-and-onboarding-design", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md", skill)

        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        skill_ids = {item["skill_id"] for item in registry["skills"]}
        self.assertNotIn("tutorial-and-onboarding-design", skill_ids)

    def test_human_discoverability_routes_to_existing_owner(self) -> None:
        start = START.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("튜토리얼·온보딩·첫 세션 학습", start)
        self.assertIn("analyzing-and-refining-game-concepts", start)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", index)


if __name__ == "__main__":
    unittest.main()
