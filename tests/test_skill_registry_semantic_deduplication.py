from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"


class SkillRegistrySemanticDeduplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.skills = {entry["skill_id"]: entry for entry in payload["skills"]}

    def test_game_concept_route_keeps_only_the_strictly_more_complete_use_when(self) -> None:
        self.assertEqual(
            [
                "핵심 컨셉·뾰족한 재미·제약·DDD, 게임 시스템 경계, 난이도·전투 AI, 비교 게임·플레이어 반응·행동 근거·플레이테스트를 개선안과 PoC·재조정 방향으로 변환한다."
            ],
            self.skills["analyzing-and-refining-game-concepts"]["use_when"],
        )

    def test_distinct_multi_route_entries_are_not_over_pruned(self) -> None:
        review_routes = self.skills["reviewing-and-validating-project-changes"]["use_when"]
        ui_routes = self.skills["auditing-and-refining-ui-art"]["use_when"]

        self.assertEqual(2, len(review_routes))
        self.assertTrue(any("코드·데이터·문서·자산·CI 변경" in route for route in review_routes))
        self.assertTrue(any("완료 주장과 승인 의도" in route for route in review_routes))

        self.assertEqual(2, len(ui_routes))
        self.assertTrue(any("게임 UX/UI 경험" in route for route in ui_routes))
        self.assertTrue(any("A~E 영역" in route for route in ui_routes))


if __name__ == "__main__":
    unittest.main()
