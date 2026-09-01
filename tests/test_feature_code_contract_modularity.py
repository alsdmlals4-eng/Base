"""Guard the shared feature code-and-contract authoring boundary."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md"
SKILL = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
TEMPLATE = ROOT / "templates/planning/EXECUTION_SEQUENCE_PLAN.md"
HEADING = "## 2.2 기능별 코드·계약 모듈화"


class FeatureCodeContractModularityTests(unittest.TestCase):
    def setUp(self) -> None:
        source = OWNER.read_text(encoding="utf-8")
        self.section = source.partition(HEADING)[2].partition("\n## 3. 분해 원칙")[0]

    def require(self, *clauses: str) -> None:
        for clause in clauses:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.section)

    def test_code_and_contract_share_a_feature_boundary_without_forcing_file_per_function(self) -> None:
        self.require(
            "기능별 코드와 기능 계약은 같은 책임 경계로 설계한다.",
            "기존 모듈·계약·테스트를 먼저 재사용한다.",
            "함수마다 파일·클래스·인터페이스를 만들지 않는다.",
            "작은 기능은 한 파일 또는 기존 문서의 한 절로 유지할 수 있다.",
        )

    def test_contract_has_one_owner_and_an_explicit_public_consumer_boundary(self) -> None:
        self.require(
            "기능 계약의 정본 owner는 하나만 둔다.",
            "같은 수치·규칙·Schema를 코드·문서·JSON에 중복 정본으로 만들지 않는다.",
            "입력·출력 타입, 공개 함수·signal/event, 상태 소유권·전이, 불변조건",
            "다른 기능의 내부 상태를 직접 수정하거나 내부 구현 경로에 결합하지 않는다.",
            "의존 방향과 실제 consumer 경로를 기록한다.",
        )

    def test_contract_change_binds_implementation_consumers_and_evidence_without_overclaiming_runtime(self) -> None:
        self.require(
            "계약·코드·영향 consumer·테스트를 같은 승인 변경 단위로 갱신한다.",
            "정상·경계·실패 fixture",
            "저장 Schema에 영향이 있으면 마이그레이션·복구 fixture를 검증한다.",
            "준비 문서만으로 구현 완료를 주장하지 않는다.",
            "문서 검사 PASS는 실제 모듈 동작·runtime·UX·사용자 승인 PASS가 아니다.",
            "실행하지 않은 검증은 NOT_RUN으로 남긴다.",
        )

    def test_godot_contract_uses_existing_owner_without_globalizing_every_feature(self) -> None:
        self.require(
            "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "Scene·Node·Resource·Script·Autoload",
            "모든 기능을 Autoload 또는 전역 event bus로 만들지 않는다.",
            "기존 프로젝트를 일괄 재구성하지 않는다.",
        )


class FeatureCodeContractRoutingTests(unittest.TestCase):
    def test_meaningful_feature_contract_changes_route_through_existing_intake(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        intake = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "managing-project-intake-and-work-contract"
        )
        for tag in (
            "feature-code-contract-modularity",
            "feature-contract-change",
            "feature-boundary-change",
        ):
            self.assertIn(tag, intake["trigger_tags"])
        self.assertIn("작업 크기·단계 수와 무관하게", " ".join(intake["use_when"]))
        self.assertIn(
            "기능 계약·공개 경계 변경이 없는 승인된 작은 구현",
            " ".join(intake["do_not_use_when"]),
        )

    def test_skill_and_execution_plan_expose_the_existing_boundary(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        plan = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("작은 단일 파일·단일 단계라도 L1 intake 대상", skill)
        self.assertIn(
            "작업 분해가 필요하지 않은 작은 기능을 포함해 `references/work-decomposition-and-sequencing.md`",
            skill,
        )
        for field in (
            "## 기능별 코드·계약 경계",
            "계약 정본 owner",
            "공개 출력·통합 경계",
            "실제 consumer·의존 방향",
            "검증·롤백",
        ):
            self.assertIn(field, plan)


if __name__ == "__main__":
    unittest.main()
