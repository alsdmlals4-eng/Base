"""Guard the intake authoring contract, not real project modularity/runtime."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md"
HEADING = "## 2.2 기능별 코드·계약 모듈화"


class FeatureCodeContractModularityTests(unittest.TestCase):
    def setUp(self):
        source = OWNER.read_text(encoding="utf-8")
        self.section = source.partition(HEADING)[2].partition("\n## 3. 분해 원칙")[0]

    def require(self, *clauses):
        for clause in clauses:
            with self.subTest(clause=clause):
                self.assertIn(clause, self.section)

    def test_new_code_and_contracts_share_feature_boundaries(self):
        self.require(
            "기능별 코드와 기능 계약은 같은 책임 경계로 설계한다.",
            "Base의 Python·자동화 코드와 프로젝트 제품 코드 모두에 적용한다.",
            "기존 모듈·계약·테스트를 먼저 재사용한다.",
        )

    def test_existing_work_fields_are_reused_without_parallel_registry(self):
        self.require(
            "별도 Registry·추적표·문서 세트를 의무 생성하지 않는다.",
            "`step_id / outcome`", "`files_or_systems / owner_or_skill`",
            "`inputs / output / integration_interface`", "`dependencies / parallel_with`",
            "`acceptance_criteria / validation`", "`rollback`",
        )

    def test_granularity_is_not_one_file_per_function(self):
        self.require(
            "함수마다 파일·클래스·인터페이스를 만들지 않는다.",
            "작은 기능은 한 파일 또는 기존 문서의 한 절로 유지할 수 있다.",
            "물리적으로 같은 폴더에 둘 의무는 없다.",
        )

    def test_single_owner_and_no_duplicated_rules(self):
        self.require(
            "기능 계약의 정본 owner는 하나만 둔다.",
            "공용 불변조건은 기존 owner를 참조하고 기능별 차이만 해당 계약이 소유한다.",
            "같은 수치·규칙·Schema를 코드·문서·JSON에 중복 정본으로 만들지 않는다.",
        )

    def test_public_boundary_covers_state_errors_and_lifecycle(self):
        self.require(
            "입력·출력 타입, 공개 함수·signal/event, 상태 소유권·전이, 불변조건",
            "오류·취소·재시도·중복 실행의 의미",
            "다른 기능의 내부 상태를 직접 수정하거나 내부 구현 경로에 결합하지 않는다.",
        )

    def test_dependencies_and_real_consumers_are_identified(self):
        self.require(
            "의존 방향과 실제 consumer 경로를 기록한다.",
            "순환 의존·숨은 전역 상태·소유권 충돌을 검토한다.",
            "계획 경로는 실제 존재하는 consumer로 표시하지 않는다.",
        )

    def test_godot_uses_existing_engine_owner_and_boundary_rules(self):
        self.require(
            "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "Scene·Node·Resource·Script·Autoload", "프로젝트가 채택한 엔진 버전",
            "모든 기능을 Autoload 또는 전역 event bus로 만들지 않는다.",
            "정적 정의·런타임 상태·저장 상태·표현 상태",
        )

    def test_contract_changes_follow_consumers_and_preparation_boundary(self):
        self.require(
            "계약·코드·영향 consumer·테스트를 같은 승인 변경 단위로 갱신한다.",
            "호환성 파괴 여부와 영향 consumer를 먼저 확인한다.",
            "저장 Schema에 영향이 있으면 마이그레이션·복구 fixture를 검증한다.",
            "Work 준비와 Codex 구현이 분리된 경우",
            "exact repository revision", "준비 문서만으로 구현 완료를 주장하지 않는다.",
        )

    def test_unit_integration_runtime_and_human_evidence_are_separate(self):
        self.require(
            "정상·경계·실패 fixture", "공개 계약 일치 검사", "consumer 통합 검사",
            "문서 검사 PASS는 실제 모듈 동작·runtime·UX·사용자 승인 PASS가 아니다.",
            "실행하지 않은 검증은 NOT_RUN으로 남긴다.",
            "실제 인게임 캡처", "exact revision",
        )

    def test_existing_projects_and_scope_are_protected(self):
        self.require(
            "프로젝트의 최신 AGENTS.md·채택 계약·기존 구조를 우선한다.",
            "Base 최신 버전으로 프로젝트 lock을 자동 교체하지 않는다.",
            "기존 프로젝트를 일괄 재구성하지 않는다.",
            "새 프레임워크·패키지·유료 도구를 기본 요구하지 않는다.",
        )

    def test_example_is_not_new_product_canon_or_shared_runtime_claim(self):
        self.require(
            "아래는 구조 설명 예시이며 프로젝트의 새 규칙·경로·구현 사실이 아니다.",
            "피해 계산", "DamageResult", "전투 실행", "HUD",
            "프로젝트 고유 규칙·수치·경로는 프로젝트에 남긴다.",
            "기능 계약 작성은 Base 공용 구현·프로젝트 채택 완료를 뜻하지 않는다.",
        )


if __name__ == "__main__":
    unittest.main()
