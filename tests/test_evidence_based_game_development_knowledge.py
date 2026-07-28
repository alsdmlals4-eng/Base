from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_ROOT = ROOT / "docs" / "knowledge" / "game-development"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class EvidenceBasedGameDevelopmentKnowledgeTests(unittest.TestCase):
    def test_knowledge_hub_and_method_contract(self) -> None:
        expected_files = (
            "README.md",
            "EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md",
            "GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md",
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md",
            "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "REFERENCE_SOURCE_CATALOG.md",
        )
        for filename in expected_files:
            self.assertTrue((KNOWLEDGE_ROOT / filename).is_file(), filename)

        hub = read("docs/knowledge/game-development/README.md")
        method = read(
            "docs/knowledge/game-development/"
            "EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md"
        )

        for filename in expected_files[1:]:
            self.assertIn(filename, hub)

        for skill_id in (
            "managing-project-intake-and-work-contract",
            "analyzing-and-refining-game-concepts",
            "governing-game-user-research-coverage",
            "designing-art-prompts-and-technique-cards",
            "designing-vertical-slices",
            "reviewing-and-validating-project-changes",
            "running-adversarial-review-and-refinement",
            "evolving-project-discipline-skills",
            "managing-base-change-proposals",
        ):
            self.assertIn(skill_id, hub)

        for coverage in (
            "프로젝트 코어·게임 기획",
            "플레이어 경험·게임 필·보상·난이도",
            "아트 디렉션·캐릭터·환경·UI·애니메이션",
            "내러티브·세계관·콘텐츠 설계",
            "UX·UI·접근성",
            "사운드·음악·오디오 정보 전달",
            "Godot·데이터·저장·성능·플랫폼 기술 기획",
            "QA·자동화·런타임·회귀 검증",
            "프로덕션·범위·Vertical Slice·반복 제작성",
            "벤치마킹·Games User Research·텔레메트리",
            "AI 협업·Prompt·Evals·보안·권리·독립 검수",
            "출시·스토어·마케팅 약속·출시 후 학습",
        ):
            self.assertIn(coverage, method)

        for tier in (
            "T1_PRIMARY_OFFICIAL",
            "T2_PROFESSIONAL_PRACTICE",
            "T3_PLAYER_BEHAVIOR",
            "T4_PLAYER_SELF_REPORT",
            "T5_SYNTHESIS",
            "T6_AI_INFERENCE",
        ):
            self.assertIn(tier, method)

        for status in (
            "VERIFIED_SOURCE",
            "PARTIALLY_VERIFIED",
            "CONTEXT_LIMITED",
            "STALE_RECHECK_REQUIRED",
            "CONFLICTING_EVIDENCE",
            "UNVERIFIED",
        ):
            self.assertIn(status, method)

        for decision in (
            "ADOPT",
            "ADAPT",
            "TEST",
            "AVOID",
            "IGNORE",
            "REFERENCE_ONLY",
        ):
            self.assertIn(decision, method)

        for term in (
            "PLAN",
            "BUILD",
            "REVIEW",
            "Base로 승격",
            "프로젝트에 유지",
            "NOT_STARTED",
            "NOT_APPLICABLE",
        ):
            self.assertIn(term, method)

    def test_game_design_guide_contract(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md"
        )
        for term in (
            "플레이어 약속",
            "대상 플레이어",
            "플레이 상황",
            "감정·판타지",
            "핵심 선택",
            "반복 행동",
            "보상·기억",
            "차별 원리",
            "Mechanics",
            "Dynamics",
            "Experience",
            "게임 필",
            "온보딩",
            "난이도",
            "보상 사다리",
            "실패 후 학습·복구",
            "행동 증거",
            "플레이어 자기보고",
            "플레이테스트",
            "Vertical Slice",
            "ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY",
        ):
            self.assertIn(term, guide)

    def test_art_direction_guide_contract(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        for term in (
            "Visual Pillar",
            "Shape Language",
            "실루엣",
            "Color",
            "Value",
            "Composition",
            "시각적 위계",
            "마스코트·상징",
            "Concept Exploration",
            "Art Bible",
            "Asset Specification",
            "실제 인게임 캡처",
            "Runtime Asset Approval",
            "원출처",
            "라이선스",
            "유사성",
            "생성 이미지는 자동 최종 자산이 아니다",
            "두 번째 같은 유형의 자산",
        ):
            self.assertIn(term, guide)

    def test_ai_assisted_development_guide_contract(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md"
        )
        for term in (
            "ChatGPT",
            "Codex Plan",
            "Codex Build",
            "외부 AI",
            "사용자 승인",
            "Prompt 계약",
            "Context Pack",
            "SPECIFY",
            "MEASURE",
            "IMPROVE",
            "Golden Set",
            "Evals",
            "독립 검수",
            "검수 대기 입력",
            "Prompt Injection",
            "Secret",
            "개인정보",
            "라이선스·출처",
            "모델·도구·버전",
            "토큰·비용·재시도",
            "external-source-review",
        ):
            self.assertIn(term, guide)

    def test_technical_production_guide_contract(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md"
        )
        for term in (
            "Godot",
            "Scene",
            "Resource",
            "Autoload",
            "데이터 책임 경계",
            "저장 Schema",
            "마이그레이션",
            "결정론",
            "PC",
            "모바일",
            "base resolution",
            "aspect ratio",
            "UI scale",
            "터치·키보드·마우스·패드",
            "frame time",
            "CPU·GPU·메모리",
            "로딩·발열",
            "접근성",
            "Vertical Slice",
            "두 번째 콘텐츠",
            "Steam Playtest",
            "User Reviews",
            "Wishlist",
            "Google Play 테스트",
            "공식 출처로 재검증",
        ):
            self.assertIn(term, guide)

    def test_reference_catalog_and_templates_contract(self) -> None:
        catalog = read(
            "docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md"
        )
        evidence = read("templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md")
        case_card = read("templates/research/GAME_DEVELOPMENT_CASE_CARD.md")
        benchmark = read("templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md")

        for domain in (
            "aaai.org",
            "gdcvault.com",
            "learn.microsoft.com",
            "docs.godotengine.org",
            "developer.android.com",
            "partner.steamgames.com",
            "nist.gov",
            "openai.com",
            "docs.github.com",
            "gamesuserresearch.com",
            "academic.oup.com",
        ):
            self.assertIn(domain, catalog)

        for term in (
            "checked_at: 2026-07-29",
            "T1_PRIMARY_OFFICIAL",
            "T2_PROFESSIONAL_PRACTICE",
            "T3_PLAYER_BEHAVIOR",
            "T4_PLAYER_SELF_REPORT",
            "T5_SYNTHESIS",
            "T6_AI_INFERENCE",
            "사용 한계",
            "재검증 조건",
        ):
            self.assertIn(term, catalog)

        for term in (
            "결정 질문",
            "Coverage 선택",
            "Source Plan",
            "Evidence ID",
            "근거 층",
            "근거 상태",
            "상충 근거",
            "개선 판정",
            "정본 반영 위치",
            "검증 계획",
            "미검증·한계",
        ):
            self.assertIn(term, evidence)

        for term in (
            "SUCCESS",
            "FAILURE",
            "MIXED",
            "문제·맥락",
            "접근 방식",
            "관찰된 결과",
            "플레이어 행동",
            "플레이어 자기보고",
            "적용 조건",
            "그대로 복제하지 않을 요소",
            "공용화 후보",
            "프로젝트 전용 유지",
        ):
            self.assertIn(term, case_card)

        for term in (
            "Evidence ID",
            "근거 층",
            "원출처",
            "확인일",
            "실패 사례",
            "REFERENCE_ONLY",
            "Case Card",
        ):
            self.assertIn(term, benchmark)

    def test_documentation_routes_and_no_duplicate_skill(self) -> None:
        readme = read("README.md")
        doc_map = read("docs/DOCUMENTATION_MAP.md")
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        registry = read("skills/SKILL_REGISTRY.json")

        for text in (readme, doc_map, policy):
            self.assertIn("docs/knowledge/game-development/README.md", text)
            self.assertIn("templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md", text)
            self.assertIn("templates/research/GAME_DEVELOPMENT_CASE_CARD.md", text)

        self.assertNotIn('"skill_id":"evidence-based-game-development"', registry)
        self.assertNotIn('"skill_id":"game-development-knowledge-system"', registry)
        self.assertEqual(
            registry.count('"skill_id":"analyzing-and-refining-game-concepts"'),
            1,
        )
        self.assertEqual(
            registry.count(
                '"skill_id":"running-adversarial-review-and-refinement"'
            ),
            1,
        )

    def test_changelog_and_learning_record(self) -> None:
        changelog = read("docs/CHANGELOG.md")
        learning = read("skills/SKILL_LEARNING_LOG.md")

        for term in (
            "근거 기반 게임 개발 지식 허브",
            "게임 기획·아트·개발·AI·벤치마킹",
        ):
            self.assertIn(term, changelog)

        for term in (
            "새 Skill을 추가하지 않음",
            "프로젝트 Pilot 검증 대기",
            "반복 검증 전 공용 강제 규칙으로 승격하지 않음",
        ):
            self.assertIn(term, learning)


if __name__ == "__main__":
    unittest.main()
