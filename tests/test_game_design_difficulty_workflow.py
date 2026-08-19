from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DELIVERY_GUIDE = (
    "docs/knowledge/game-development/"
    "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)
DELIVERY_PROFILE = "templates/planning/PC_ANDROID_DELIVERY_PROFILE.md"
TUTORIAL_GUIDE = "docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md"
TUTORIAL_CONTRACT = "templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class GameDesignDifficultyWorkflowTests(unittest.TestCase):
    def test_existing_game_concept_skill_owns_new_modes(self) -> None:
        skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")

        for term in (
            "system-design",
            "difficulty-and-combat-ai",
            "game-system-difficulty-and-combat-ai.md",
            "game-system-difficulty-evidence-sources.md",
            "플레이어 경험 목표",
            "공정성·가독성·대응 가능성",
            "공격 예산",
            "긴장도 페이싱",
            "동적 난이도 조절",
        ):
            self.assertIn(term, skill)

    def test_tutorial_mode_stays_with_the_existing_game_concept_owner(self) -> None:
        skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        guide = read(TUTORIAL_GUIDE)
        contract = read(TUTORIAL_CONTRACT)
        registry = json.loads(read("skills/SKILL_REGISTRY.json"))

        for term in (
            "tutorial-and-onboarding-design",
            TUTORIAL_GUIDE,
            TUTORIAL_CONTRACT,
            "RULE → NEED → DISCOVER → FEEL → PROVE → TRANSFER",
            "안내 없는 독립 수행",
            "접근성 대체 채널",
        ):
            self.assertIn(term, skill + guide + contract)

        skill_ids = {item["skill_id"] for item in registry["skills"]}
        self.assertNotIn("tutorial-and-onboarding-design", skill_ids)

    def test_pc_android_delivery_route_is_conditional(self) -> None:
        skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")

        for term in (
            DELIVERY_GUIDE,
            DELIVERY_PROFILE,
            "Windows+Android 동시 목표",
            "모든 프로젝트에 이 프로필을 강제",
            "같은 날 공개",
        ):
            self.assertIn(term, skill)

    def test_reference_template_and_evidence_define_executable_contract(self) -> None:
        reference_path = (
            ROOT
            / "skills"
            / "analyzing-and-refining-game-concepts"
            / "references"
            / "game-system-difficulty-and-combat-ai.md"
        )
        evidence_path = (
            ROOT
            / "skills"
            / "analyzing-and-refining-game-concepts"
            / "references"
            / "game-system-difficulty-evidence-sources.md"
        )
        template_path = (
            ROOT
            / "templates"
            / "planning"
            / "GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md"
        )
        self.assertTrue(reference_path.is_file())
        self.assertTrue(evidence_path.is_file())
        self.assertTrue(template_path.is_file())

        reference = reference_path.read_text(encoding="utf-8")
        evidence = evidence_path.read_text(encoding="utf-8")
        template = template_path.read_text(encoding="utf-8")

        for term in (
            "Mechanics → Dynamics → Experience → Evidence",
            "개별 적 판단",
            "전투 조율자",
            "난이도·페이싱 디렉터",
            "공격 예산",
            "위협 예산",
            "반응시간",
            "의도적 빗나감",
            "Build Up",
            "Sustain Peak",
            "Peak Fade",
            "Relax",
            "장기 실력",
            "단기 스트레스",
            "히스테리시스",
            "변경 쿨다운",
            "접근성",
            "텔레메트리",
            "플레이테스트",
            "Base 승격 후보",
            "프로젝트 전용 유지",
        ):
            self.assertIn(term, reference)

        for term in (
            "AI-L4D-PACING-001",
            "AI-ATTACK-BUDGET-001",
            "AI-REACTION-001",
            "AI-ACCURACY-001",
            "DDA-REVIEW-001",
            "DDA-SLR-2025-001",
            "ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY",
            "프로젝트 기본값이 아니다",
            "실제 플레이어 검증을 완료했다고 주장하지 않는다",
        ):
            self.assertIn(term, evidence)

        for term in (
            "플레이어 경험 목표",
            "시스템 경계",
            "행동·선택·결과 계약",
            "공정성 안전 규칙",
            "난이도 장벽 프로필",
            "공격·위협 예산",
            "긴장도 상태",
            "적응형 난이도 입력",
            "난이도별 조절 변수",
            "텔레메트리 이벤트",
            "플레이테스트 성공 기준",
            "제외 범위",
            "Base 승격 후보",
            "프로젝트 전용 유지",
        ):
            self.assertIn(term, template)

    def test_registry_routes_without_duplicate_specialist_skill(self) -> None:
        registry = json.loads(read("skills/SKILL_REGISTRY.json"))
        skills = {item["skill_id"]: item for item in registry["skills"]}
        concept = skills["analyzing-and-refining-game-concepts"]

        for trigger in (
            "game-system-design",
            "difficulty-design",
            "combat-ai-design",
            "adaptive-difficulty",
            "dynamic-difficulty-adjustment",
            "attack-budget",
            "threat-budget",
            "tension-pacing",
        ):
            self.assertIn(trigger, concept["trigger_tags"])

        self.assertNotIn("designing-game-difficulty", skills)
        self.assertNotIn("designing-combat-ai", skills)

    def test_human_routes_and_knowledge_guide_are_connected(self) -> None:
        start = read("START_HERE.md")
        doc_map = read("docs/DOCUMENTATION_MAP.md")
        guide = read(
            "docs/knowledge/game-development/"
            "GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md"
        )

        for text in (start, doc_map):
            self.assertIn("system-design", text)
            self.assertIn("difficulty-and-combat-ai", text)
            self.assertIn(
                "GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md",
                text,
            )

        for term in (
            "게임 시스템 설계",
            "난이도 장벽 프로필",
            "공정성 안전 규칙",
            "공격·위협 예산",
            "긴장도 곡선",
            "적응형 난이도",
            "성공을 벌주지 않는다",
        ):
            self.assertIn(term, guide)

    def test_player_value_research_and_vertical_slice_evidence_contract(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md"
        )
        concept = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        research = read("skills/governing-game-user-research-coverage/SKILL.md")
        vertical_slice = read("skills/designing-vertical-slices/SKILL.md")

        self.assertIn("P04_PLAYER_VALUE_TO_EVIDENCE_TRACE", guide)
        for term in (
            "player_promise",
            "meaningful_choice",
            "expected_experience",
            "research_question",
            "observable_signal",
            "evidence_ceiling",
            "slice_acceptance",
        ):
            self.assertIn(term, guide)

        self.assertNotIn("프로젝트 정본·Google Sheets·실제 코드", concept)
        self.assertIn("DECISION_SPECIFIC_RESEARCH", concept)
        self.assertIn("Notion/GitHub", concept)

        for term in (
            "RESEARCH_QUESTION_FIRST",
            "DECISION_RELEVANT_COVERAGE",
            "NOT_APPLICABLE",
            "11/11",
        ):
            self.assertIn(term, research)

        for term in (
            "PLAYER_VALUE_TRACE_REQUIRED",
            "player_promise",
            "meaningful_choice",
            "observable_signal",
            "evidence_ceiling",
            "slice_acceptance",
        ):
            self.assertIn(term, vertical_slice)

    def test_change_and_learning_records_exist(self) -> None:
        changelog = read("docs/CHANGELOG.md")
        learning = read("skills/SKILL_LEARNING_LOG.md")

        for term in (
            "게임 시스템·난이도·전투 AI 설계 구조",
            "새 독립 Skill을 추가하지 않음",
        ):
            self.assertIn(term, changelog)

        for term in (
            "난이도·전투 AI 설계",
            "프로젝트 Pilot 검증 대기",
            "한 번의 성공을 공용 강제 규칙으로 승격하지 않음",
        ):
            self.assertIn(term, learning)


# Required-check bridge: this existing workflow-owned test module deliberately
# imports the focused P04 regressions so game-design/reuse/adoption contract changes
# cannot pass only because a focused test file exists outside the workflow's
# explicit unittest list.
from tests.test_p04_reverse_engineering_reuse_pipeline import (
    P04ReverseEngineeringReusePipelineTests,
)
from tests.test_p04_vertical_slice_player_value_trace import (
    P04VerticalSlicePlayerValueTraceTests,
)


if __name__ == "__main__":
    unittest.main()