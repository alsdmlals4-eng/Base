from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "research" / "WEEKLY_WORK_IMPROVEMENT_REVIEW.md"
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"


class WeeklyWorkImprovementReviewTests(unittest.TestCase):
    def test_template_preserves_requested_cross_domain_review_shape(self) -> None:
        self.assertTrue(TEMPLATE.is_file())
        content = TEMPLATE.read_text(encoding="utf-8")

        for required in (
            "A. 메인게임",
            "B. 미니게임",
            "C. 글쓰기",
            "D. 종합 반영안",
            "이번 주 핵심 변화와 근거",
            "현재 작업 방식의 개선점",
            "직접 경쟁작",
            "인접 장르",
            "장르 밖 참고작",
            "실패·혼합 반응",
            "핵심 플레이어 또는 독자 경험",
            "첫 10분 또는 첫 장면",
            "핵심 루프 또는 장면 진행 구조",
            "반복 피로도와 감정 곡선",
            "선택과 결과",
            "온보딩·UI/UX 또는 문장 가독성",
            "비주얼 아이덴티티·마스코트·상징·문체",
            "콘텐츠 제작 비용과 1인 제작 현실성",
            "판매 포인트 또는 독자 유입 포인트",
            "성공 요인과 실패·이탈 요인",
            "그대로 참고할 요소",
            "현재 프로젝트에 맞게 변형할 요소",
            "도입하지 말아야 할 요소",
            "작은 실험으로 검증할 요소와 성공 기준",
        ):
            self.assertIn(required, content)

    def test_template_requires_delta_evidence_routing_and_actionable_outputs(self) -> None:
        content = TEMPLATE.read_text(encoding="utf-8")

        for required in (
            "PREVIOUS_REPORT_DELTA",
            "NEW_EVIDENCE_OR_NEW_COMPARISON_DIMENSION",
            "ORIGINAL_SOURCE_BACKTRACE",
            "freshness",
            "scope",
            "sample_or_method",
            "commercial_or_vendor_interest",
            "SOURCE_FACT",
            "PLAYER_OR_READER_EVIDENCE",
            "PROFESSIONAL_OFFICIAL_GUIDANCE",
            "MODEL_INFERENCE",
            "PROJECT_RECOMMENDATION",
            "BASE_PROMOTION_CANDIDATE",
            "PROJECT_ONLY",
            "target_project_or_consumer",
            "GitHub Issue",
            "Codex Goal",
            "테스트 체크리스트",
            "research_question",
            "method",
            "evidence_type",
            "success_criteria",
            "HUMAN_USABILITY_EVIDENCE",
            "PLAYER_EXPERIENCE_EVIDENCE",
            "N/A — reason",
            "NO_CHANGE",
        ):
            self.assertIn(required, content)

        self.assertIn("지난 보고서와 동일한 작품", content)
        self.assertIn("새로운 근거나 비교 가치", content)
        self.assertIn("적대적 검토", content)
        self.assertIn("같은 Goal의 열린·최근 병합 PR", content)
        self.assertIn("억지 변경", content)

    def test_template_is_existing_owner_orchestration_not_a_new_active_skill(self) -> None:
        content = TEMPLATE.read_text(encoding="utf-8")
        for required in (
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
            "analyzing-and-refining-game-concepts",
            "developing-and-revising-serial-fiction",
            "evolving-project-discipline-skills",
            "running-adversarial-review-and-refinement",
            "managing-base-change-proposals",
        ):
            self.assertIn(required, content)

        registry = REGISTRY.read_text(encoding="utf-8")
        self.assertNotIn("weekly-work-improvement", registry)
        self.assertNotIn("conducting-weekly-improvement", registry)

    def test_watchlist_links_to_template_one_hop(self) -> None:
        template_path = "templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md"
        self.assertIn(template_path, WATCHLIST.read_text(encoding="utf-8"))

    def test_evidence_workflow_executes_weekly_review_contract(self) -> None:
        content = WORKFLOW.read_text(encoding="utf-8")
        self.assertGreaterEqual(content.count("tests/test_weekly_work_improvement_review.py"), 4)
        self.assertIn("contents: read", content)
        self.assertNotIn("contents: write", content)


if __name__ == "__main__":
    unittest.main()
