from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class DemoFirstPlanningSequenceTests(unittest.TestCase):
    def test_approved_blueprint_delivery_is_complete_and_evidence_bound(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        section = policy.split("### `APPROVED_BLUEPRINT_END_TO_END_DELIVERY`", 1)[1].split("### `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`", 1)[0]
        for term in ("ALL_APPROVED_REQUIREMENTS_COVERED", "HANDOFF_IS_NOT_DELIVERY",
                     "USER_TESTABLE_DELIVERY", "USER_TESTABLE_NOT_HUMAN_PASS",
                     "모든 필수 항목", "이미지 파일 생성", "실제 씬·노드·리소스·상태",
                     "Godot 실행", "병합 후 readback", "2회", "정확한 blocker",
                     "새 후보 이미지의 최종 승인은 아니다"):
            with self.subTest(term=term):
                self.assertIn(term, section)

    def test_delivery_cleanup_preserves_runtime_and_recoverability(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in ("RECOVERABLE_DESKTOP_CLEANUP", "governing-legacy-retention-and-archives/SKILL.md",
                     "실제 바탕화면 경로", "SHA-256", "복원 방법", "소유권 불명",
                     "실행에 필요한 파일", "영구 삭제는 별도 권한 없이 하지 않는다",
                     "대상이 없으면 폴더를 만들지 않고 0건으로 보고한다"):
            with self.subTest(term=term):
                self.assertIn(term, policy)

    def test_delivery_routes_do_not_reduce_whole_blueprint_to_one_slice(self) -> None:
        for path in ("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md",
                     "docs/GPT_CODEX_WORKFLOW_POLICY.md",
                     "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"):
            with self.subTest(path=path):
                policy = read(path)
                self.assertIn("APPROVED_BLUEPRINT_END_TO_END_DELIVERY", policy)
                self.assertIn("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md", policy)
        self.assertNotIn("승인 단위는 게임 전체 일괄 확정이 아니라", read("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"))

    def test_basic_design_precedes_approval_and_detail_follows_it(self) -> None:
        policy = read("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md")
        section = policy.split("### 1.1 기본 설계와 상세 설계의 승인 경계", 1)[1].split("## 2.", 1)[0]
        order = ("기획 + 기본 설계", "→ 검토·보완", "→ 사용자 승인 또는 유효한 기존 승인 재사용",
                 "→ 상세 설계", "→ 구현", "→ 실제 실행 검증·교정", "→ 결과 설명과 블루프린트 갱신")
        positions = [section.index(term) for term in order]
        self.assertEqual(positions, sorted(positions))

    def test_design_boundary_preserves_scope_authority_and_evidence(self) -> None:
        policy = read("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md")
        for term in ("와이어프레임·플로우맵", "구현 가능성·위험", "완료 기준·검증·롤백",
                     "별도로 승인된 제한 범위", "영향받는 결정만 재승인", "저장 호환성",
                     "PLAY_MEANINGFUL_WORK_SLICE", "모든 최종 자산을 먼저 제작하지 않는다",
                     "실제 Godot 제품의 상세 구현 설계와 구현은 Codex", "명시적인 사용자 선언",
                     "무엇이 바뀌었는가 / 어떤 연결로 작동하는가 / 사용자가 어떻게 확인하는가",
                     "사용자 기획 승인은 Human/Player 검증 PASS가 아니다"):
            with self.subTest(term=term):
                self.assertIn(term, policy)

    def test_design_boundary_routes_existing_consumers_to_single_owner(self) -> None:
        for path in ("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md",
                     "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md"):
            with self.subTest(path=path):
                text = read(path)
                self.assertIn("BASIC_DESIGN_BEFORE_APPROVAL_DETAILED_DESIGN_AFTER_APPROVAL", text)
                self.assertIn("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md", text)

    def test_policy_declares_current_workspace_scope_and_prework_audit(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in (
            "REPOSITORY_PRIMARY_CANON",
            "HUMAN_GDD_PDF_DERIVED_VIEW",
            "V4_NOTION_EXCEPTION_ONLY",
            "REPOSITORY_RUNTIME_TRUTH",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "DUPLICATE_WORK",
            "MISSING_CANON",
            "MISSING_CONSUMER",
            "CANON_CONFLICT",
            "IMPLEMENTATION_CONFLICT",
            "STALE_REFERENCE",
            "PROPAGATION_AUDIT",
        ):
            self.assertIn(term, policy)
        for stale in (
            "USER_FACING_GDD_WORKSPACE",
            "PROJECT_SHEET_CONFIGURED",
        ):
            self.assertNotIn(stale, policy)

    def test_material_planning_uses_three_layer_evidence_and_approval_bundles(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        evidence = read("skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md")
        sequence = read("skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md")
        for term in ("BENCHMARK_EVIDENCE", "PLAYER_RESPONSE_EVIDENCE", "PROFESSIONAL_OFFICIAL_EVIDENCE"):
            self.assertIn(term, policy)
            self.assertIn(term, evidence)
        self.assertIn("Approval Bundle", policy)
        self.assertIn("Approval Bundle", sequence)

    def test_compact_size_ceiling_is_removed_without_losing_discoverability(self) -> None:
        skill = read("skills/simplifying-skill-bodies/SKILL.md")
        reference = read("skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md")
        coverage_checker = read("tools/check_skill_system_coverage.py")
        combined = skill + reference
        for term in ("줄 수", "문자 수", "분량 상한", "내용 보존", "한 단계 발견성"):
            self.assertIn(term, combined)
        self.assertNotIn("self.assertLessEqual", read("tests/test_skill_system_coverage.py"))
        self.assertNotIn("exceeds 150 lines", coverage_checker)
        self.assertNotIn("len(text.splitlines()) > 150", coverage_checker)
        self.assertIn("completeness-first contract", coverage_checker)
        self.assertIn("Missing completeness contract token", coverage_checker)

    def test_demo_first_vertical_slice_has_no_standalone_core_poc_section(self) -> None:
        stage = read("docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md")
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in ("DEMO_FIRST_VERTICAL_SLICE", "DEMO_VALIDATION", "완성 품질 데모", "TECHNICAL_SPIKE"):
            self.assertIn(term, policy + stage + plan)
        self.assertNotIn("## 2. CORE_POC 결과", plan)
        self.assertIn("별도 `CORE_POC`", stage)

    def test_project_sheet_tabs_follow_approved_planning_order(self) -> None:
        template = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        ordered = (
            "00_프로젝트_허브",
            "01_작업순서",
            "03_근거_라이브러리",
            "04_누락_충돌_감사",
            "20_코어경험_데모목표",
            "80_데모_버티컬슬라이스_플레이테스트",
            "99_변경이력",
        )
        positions = [template.index(term) for term in ordered]
        self.assertEqual(positions, sorted(positions))


if __name__ == "__main__":
    unittest.main()
