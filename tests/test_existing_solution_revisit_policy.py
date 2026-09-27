"""Document-contract regressions; not proof of agent/runtime enforcement."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"
HEADING = "## 6A. 기존 해결책 선보고·보존·재검토"


class ExistingSolutionRevisitPolicyTests(unittest.TestCase):
    def section(self, heading=HEADING, level=2):
        text = POLICY.read_text(encoding="utf-8")
        if level == 3:
            text = self.section()
        self.assertEqual(text.splitlines().count(heading), 1, heading)
        body = text.split(heading + "\n", 1)[1]
        return re.split(r"^#{1," + str(level) + r"} ", body, maxsplit=1, flags=re.M)[0]

    def require(self, heading, terms):
        body = self.section(heading, 3)
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, body)

    def test_existing_owner_and_intake_are_reused(self):
        self.require("### 적용 범위와 책임", (
            "REUSE_FIRST_PREFLIGHT_REQUIRED", "BETTER_ALTERNATIVE_SEARCH",
            "managing-project-intake-and-work-contract",
            "evaluating-godot-assets-and-plugins-before-creation",
            "프로젝트의 채택된 Base 계약", "자동 교체하지 않는다",
        ))

    def test_disclose_material_candidates_before_custom_work(self):
        self.require("### 선보고와 기록", (
            "오픈소스", "공개 알고리즘", "공식 예제", "에셋",
            "자체 제작·추가 개선 전에", "사용자에게 먼저 보고",
            "원출처", "실제 consumer", "직접 사용", "부분 흡수",
            "라이선스", "비용", "롤백",
        ))

    def test_rejections_remain_in_existing_decision_records(self):
        self.require("### 선보고와 기록", (
            "considered_alternatives", "rejected_alternatives", "revisit_conditions",
            "제외 이유", "당시 제약", "승인 근거", "삭제하지 않는다",
            "과거 결정을 덮어쓰지 않고", "별도 후보 Registry",
        ))

    def test_stall_and_repeated_user_question_trigger_revisit(self):
        self.require("### 재검토 트리거와 순서", (
            "같은 실패", "측정 가능한 진전", "시간·토큰·시도 예산",
            "다른 공개 방식", "새로운 증거", "요구사항·플랫폼",
            "다음 동일 방식 수정 전에", "과거 후보와 제외 이유",
            "예산이 없거나 사용량을 측정할 수 없어도",
        ))

    def test_custom_choice_is_not_permanent_search_ban(self):
        self.require("### 승인·채택 경계", (
            "자체 제작 승인은 대안 탐색·보고의 영구 금지가 아니다",
            "명시적 사용 금지", "임의로 해제하지 않는다",
            "자동 설치·구매·교체하지 않는다", "USER_DECISION_REQUIRED",
            "승인된 이미지", "정본 승격", "runtime 검증",
        ))

    def test_research_is_bounded_and_exceptions_keep_reasons(self):
        self.require("### 반복 낭비 제한", (
            "REUSED_EVIDENCE", "NOT_APPLICABLE", "NOT_RUN",
            "scope·consumer·freshness", "반복 추천하지 않는다",
            "검색 범위", "후보를 못 찾은 것", "존재하지 않는다는 증명",
            "BLOCKED_UNVERIFIED",
            "트리거가 발생하면 과거 PASS나 REUSED_EVIDENCE만으로 재검토를 생략하지 않는다",
        ))

    def test_trial_requires_equal_acceptance_and_retained_output(self):
        self.require("### 비교 시험과 증거", (
            "동일한 입력·제약·성공 기준", "측정 지표",
            "기존 결과물", "격리", "사용자가 다시 묻기",
            "런타임", "문서·정적 검사",
        ))

    def test_primary_sources_and_static_evidence_ceiling(self):
        self.require("### 근거와 재사용 교훈", (
            "https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software.html",
            "https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html",
            "사용자 제공 사례", "독립 검증하지 않았다",
            "자동으로 검색·재평가를 실행", "증명하지 않는다",
        ))

    def test_failure_recovery_routes_back_to_candidate_revisit(self):
        body = self.section("## 9. 실패 복구")
        self.assertIn("§6A의 기존 후보 복원·재검토", body)
        self.assertIn("다음 동일 방식 수정 전에", body)

    def test_existing_trade_study_fields_are_preserved(self):
        body = self.section("## 7. 구현 전 Gate")
        for field in ("considered_alternatives: []", "rejected_alternatives: []",
                      "revisit_conditions: []", "acceptance_criteria: []",
                      "verification_plan: []"):
            self.assertIn(field, body)


if __name__ == "__main__":
    unittest.main()
