from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise RuntimeError(f"missing anchor in {path}: {old[:120]!r}")
    if text.count(old) != 1:
        raise RuntimeError(f"anchor not unique in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


POLICY = """# 기획 작업순서·근거·데모 우선 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 기획 작업을 어떤 순서로 묶고, 무엇을 먼저 비교하며, 어떤 근거로 승인하고, 새 정책·Template·Skill을 어디까지 전파 검증할지 정하는 공용 책임 원본이다.

승인 결정의 즉시 정본화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`, 작업 분해의 상세 의존성은 `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`, 외부 근거의 판정은 `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`, 데모 제작 Gate는 `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`가 책임진다.

## 1. 적용 범위

### Google Sheets

- Base 저장소 자체: `BASE_EXCLUDED`. 프로젝트 Google Sheets를 만들거나 동기화하지 않는다.
- 개별 프로젝트에 유효한 Sheet URL·tab·권한이 있음: `PROJECT_SHEET_CONFIGURED`.
- 개별 프로젝트에 Sheet가 없거나 아직 연결하지 않음: `NOT_CONFIGURED`.
- Base 작업을 Sheet 미동기화로 실패 처리하지 않는다.
- 개별 프로젝트에서만 승인 Decision과 작업순서를 프로젝트 Sheet에 동기화한다.

### 내용 보존

- 문서·Skill·정책·Template에 줄 수, 문자 수, 페이지 수, 분량 상한을 완료 조건으로 두지 않는다.
- 간결성보다 내용 보존, 실행 가능성, 책임 경계, 한 단계 발견성, 검증 가능성을 우선한다.
- Reference 분리는 문서를 짧게 만들기 위한 축약이 아니라 책임 분리와 조건부 발견성을 위한 것이다.
- 기존 결정·예외·실패 조건·표·검증 절차가 손실되면 간소화가 아니라 회귀다.

## 2. 모든 L1 이상 작업의 선행 감사

새 질문·기획·계획·구현·검수 전에 다음을 비교한다.

```text
최신 main
→ CURRENT_CONFIRMED_DECISIONS.md
→ 관련 분야 책임 원본
→ 같은 Goal의 열린 PR·최근 병합 PR·대체 PR
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 개별 프로젝트 Google Sheets(PROJECT_SHEET_CONFIGURED일 때)
→ Decision ID·Commit·대체 관계·현재 단계 비교
→ 중복·누락·충돌·구형 참조·미반영 판정
```

필수 판정:

- `DUPLICATE_WORK`: 같은 결과가 이미 정본·구현·PR에 존재한다.
- `DUPLICATE_QUESTION`: 유효한 기존 Decision을 다시 묻는다.
- `MISSING_CANON`: 승인된 내용이 책임 원본에 승격되지 않았다.
- `MISSING_CONSUMER`: 새 정책·Template·Skill을 읽어야 할 소비처가 연결되지 않았다.
- `CANON_CONFLICT`: 둘 이상의 현행 책임 원본이 서로 다른 결정을 주장한다.
- `IMPLEMENTATION_CONFLICT`: 정본과 실제 구현이 다르다.
- `STALE_REFERENCE`: 구형 경로·ID·정책·대체된 결정을 계속 참조한다.
- `MISSING_SYNC`: GitHub 정본·개별 프로젝트 Sheet·추적 surface 중 일부가 누락됐다.
- `NO_CONFLICT`: 현재 범위에서 신규 작업을 진행할 수 있다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·권한·도구·실행 증거가 없어 판정할 수 없다.

차단 Finding이 있으면 새 작업보다 복원·정리·재동기화를 먼저 수행한다.

## 3. 공통 8단계 작업 루프

```text
1. BASELINE_RECOVERY
→ 2. DUPLICATE_OMISSION_CONFLICT_AUDIT
→ 3. EVIDENCE_PACK
→ 4. APPROVAL_BUNDLE
→ 5. CANONICAL_UPDATE
→ 6. PROPAGATION_AUDIT
→ 7. VALIDATION
→ 8. GATE_CLOSE
```

### 3.1 BASELINE_RECOVERY

현재 Decision, 정본, 실제 구현, PR, 프로젝트 Sheet 상태를 복원한다. 이미 확인 가능한 사실은 사용자에게 되묻지 않는다.

### 3.2 DUPLICATE_OMISSION_CONFLICT_AUDIT

작업 시작 전에 필수 판정을 기록한다. 같은 작업·질문을 문구만 바꿔 반복하지 않는다.

### 3.3 EVIDENCE_PACK

중요 기획·방향성·제품 결정은 다음 세 층을 모두 검토한다.

1. `BENCHMARK_EVIDENCE`: 직접 경쟁작, 인접 장르, 실패·혼합 반응 사례.
2. `PLAYER_RESPONSE_EVIDENCE`: 긍정·부정·혼합 리뷰, 커뮤니티, 플레이테스트, 행동 데이터.
3. `PROFESSIONAL_OFFICIAL_EVIDENCE`: 현업 발표·사후 분석·공식 플랫폼·엔진·접근성·운영 권장사항.

단순 오탈자, 기계적 링크 수정, 같은 입력의 검사 재실행 같은 L0 작업은 대규모 근거 조사를 요구하지 않는다. 근거는 정본을 대체하지 않으며 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 변환한다.

### 3.4 APPROVAL_BUNDLE

같은 플레이어 경험·시스템·정본·후속 구현에 영향을 주는 결정을 분야별 묶음으로 승인한다.

```yaml
bundle_id:
discipline:
current_decisions:
duplicate_omission_conflict_result:
evidence_ids:
questions_and_options:
gpt_recommendation:
approved_decisions:
dependencies:
affected_canonical_sources:
affected_consumers:
project_sheet_tabs:
validation_gate:
```

기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리한다. 프로젝트 코어·중요 기획·방향성·정본 충돌만 `USER_DECISION_REQUIRED`로 올린다.

### 3.5 CANONICAL_UPDATE

승인된 Decision을 `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 필요한 Active Context·Issue·Plan에 반영한다. 개별 프로젝트가 `PROJECT_SHEET_CONFIGURED`이면 같은 승인 단위에서 Sheet도 갱신한다.

### 3.6 PROPAGATION_AUDIT

새 정책·Template·Skill·경로·ID를 추가하거나 바꾸면 파일 존재가 아니라 실제 소비를 검사한다.

- 항상 읽는 진입점: `AGENTS.md`, `START_HERE.md`, `README.md`.
- 운영 정본: `OPERATING_MODEL`, Work Mode·Skill routing, Documentation Map.
- 라우팅: Skill Registry, Legacy Alias, shared route.
- 프로젝트 설치: Template README, Project START_HERE, AI_WORKFLOW, 설치·감사·검증 Skill.
- 분야 소비자: 관련 기획서, 분야 Skill, Reference, 데이터 계약.
- 검증: reference freshness, 회귀 테스트, publication·generation, Governance.
- 기록: Learning Log, Changelog, 구현 계획, 병합 후 보고.
- 프로젝트 작업면: 개별 프로젝트 Google Sheets의 해당 tab·row.

소비처가 빠지면 `MISSING_CONSUMER`이며 Gate를 닫지 않는다.

### 3.7 VALIDATION

정본 비교, 정적 검사, 런타임, 접근성, 성능, 플레이테스트, 반응 조사, 적대적 검토 중 현재 범위에 필요한 검증을 실제 실행한다.

### 3.8 GATE_CLOSE

다음을 기록한다.

```text
APPROVED
CANON_UPDATED
CONSUMERS_UPDATED
IMPLEMENTED | IMPLEMENTATION_PENDING
VALIDATED | BLOCKED_UNVERIFIED
SHEET_SYNCED | BASE_EXCLUDED | NOT_CONFIGURED
NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

## 4. 프로젝트 기획 작업순서

분야별 Approval Bundle과 단계별 Gate를 혼합한다.

```text
00 프로젝트 기반·현재 상태
→ 10 제품 방향·시장 약속
→ 20 코어 경험·메인게임·데모 목표
→ 30 데모 범위·품질 기준·제작 기반
→ 40 시스템·성장·경제
→ 50 메인 콘텐츠
→ 51 미니게임(해당 프로젝트만)
→ 52 글쓰기·서사(해당 프로젝트만)
→ 60 UX·UI·접근성
→ 70 아트·오디오·에셋
→ 80 완성 품질 Vertical Slice 데모·플레이테스트
→ 90 본제작·출시·사업
→ 98 Base 반영 후보
→ 99 변경 이력·회고
```

앞 단계가 완전히 끝날 때까지 뒤 분야를 금지하는 폭포수 모델이 아니다. 다만 승인 묶음의 책임 원본과 의존성이 고정되지 않았다면 같은 파일·Schema·자산을 경쟁적으로 수정하지 않는다.

## 5. Demo-First Vertical Slice

기본 제품 경로는 별도 `CORE_POC` Gate를 사용하지 않는다.

```text
CONCEPT_APPROVAL
→ DEMO_FIRST_VERTICAL_SLICE
→ 통합 데모 QA
→ 내부 플레이테스트
→ 외부 플레이테스트·반응 조사
→ DEMO_VALIDATION
→ PRODUCTION_APPROVAL
```

목표는 폐기형 Prototype이 아니라 최종 방향에 가까운 아트·UI·UX·사운드·데이터·저장·복구·성능·접근성을 갖춘 **완성 품질 데모**다.

기술 불확실성이 데모 전체를 차단할 때만 Vertical Slice 작업 내부에 제한된 `TECHNICAL_SPIKE`를 둔다.

- 별도 제품 단계나 사용자 공개 데모로 간주하지 않는다.
- 질문 하나와 성공·실패·중단 기준을 가진다.
- 결과는 데모 구현에 재사용하거나 결정 근거로 기록한다.
- Spike를 이유로 저품질 임시 빌드를 최종 데모처럼 승인하지 않는다.
- 위험한 가설을 숨기지 않되 `CORE_POC` 완료를 별도 Gate로 요구하지 않는다.

과거 `PROTOTYPE_AND_VERTICAL_SLICE`, `CORE_POC`, `SLICE_VALIDATION` 기록은 역사·호환 용어로 보존할 수 있다. 새 작업에서는 각각 `DEMO_FIRST_VERTICAL_SLICE`, 내부 `TECHNICAL_SPIKE`, `DEMO_VALIDATION`으로 해석한다.

## 6. 개별 프로젝트 Google Sheets tab 기준

Base에는 생성하지 않는다. 개별 프로젝트에서만 다음 순서를 사용한다.

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_시스템_성장_경제
50_메인콘텐츠
51_미니게임
52_글쓰기_서사
60_UX_UI_접근성
70_아트_오디오_에셋
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

필요하지 않은 `51_미니게임`, `52_글쓰기_서사`는 생성하지 않는다. 공통 열과 분야별 세부 열은 `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`를 따른다.

## 7. 실패 조건

- 이전 기록을 읽지 않고 같은 질문·작업을 반복한다.
- 새 정책·Template·Skill을 만들고 실제 소비처를 연결하지 않는다.
- 인기작 기능이나 단일 리뷰만으로 방향을 바꾼다.
- 현업·공식 근거를 조사하지 않고 모델 추론만 권장안으로 제시한다.
- 관련 결정을 여러 탭·문서·PR에 흩어 승인한다.
- 문서 길이를 줄이기 위해 결정·예외·검증·실패 조건을 삭제한다.
- 별도 `CORE_POC`를 필수 Gate로 되살린다.
- 임시 Prototype 품질을 완성 데모 품질로 오인한다.
- Base에 프로젝트 Google Sheets 동기화를 요구한다.
"""

SHEET_TEMPLATE = """# 프로젝트 기획 작업순서·Google Sheets tab Template

이 Template은 Base 자체가 아니라 Base를 적용한 **개별 프로젝트**에서 사용한다. 프로젝트 Google Sheets가 없으면 `NOT_CONFIGURED`로 기록하고 Sheet가 있는 것처럼 추정하지 않는다.

## 1. 설치할 tab

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_시스템_성장_경제
50_메인콘텐츠
51_미니게임                 # 필요할 때만
52_글쓰기_서사              # 필요할 때만
60_UX_UI_접근성
70_아트_오디오_에셋
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

## 2. `01_작업순서` 공통 열

| 순서 | Approval Bundle | 분야 | 현재 단계 | 선행 조건 | `BLOCKS` | `INFORMS` | 승인 상태 | 정본 반영 | 소비처 반영 | 구현 | 검증 | 다음 작업 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 3. 분야별 tab 공통 열

| 순서 | Decision ID | Approval Bundle | 현재 확정 내용 | 신규 제안 | 변경 이유 | Evidence ID | GPT 권장안 | 사용자 결정 | 선행·후속 | 책임 정본 경로 | 소비처 | 구현 상태 | 검증 | 누락·충돌 | Sheet 동기화 | 최종 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

`최종 상태`는 `CURRENT / SUPERSEDED / DEFERRED / REJECTED / BLOCKED_UNVERIFIED`를 사용한다.

## 4. `03_근거_라이브러리`

| Evidence ID | 유형 | 출처 | 날짜·버전 | 비교 차원 | 대상 플레이어 | 관찰 사실 | 플레이어 반응 | 현업·공식 권장 | 적용 판정 | 신뢰도 | 후속 검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|

유형:

- `BENCHMARK_EVIDENCE`
- `PLAYER_RESPONSE_EVIDENCE`
- `PROFESSIONAL_OFFICIAL_EVIDENCE`
- `BEHAVIORAL_EVIDENCE`
- `CONTROLLED_EXPERIMENT`

적용 판정은 `ADOPT / ADAPT / AVOID / TEST / IGNORE`를 사용한다.

## 5. `04_누락_충돌_감사`

| Audit ID | 날짜 | 작업·질문 | 비교한 main | 비교한 Decision | 비교한 PR | 비교한 정본 | 비교한 구현 | Sheet 상태 | 판정 | 영향 | 수정 위치 | 재검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

판정:

- `DUPLICATE_WORK`
- `DUPLICATE_QUESTION`
- `MISSING_CANON`
- `MISSING_CONSUMER`
- `CANON_CONFLICT`
- `IMPLEMENTATION_CONFLICT`
- `STALE_REFERENCE`
- `MISSING_SYNC`
- `NO_CONFLICT`
- `BLOCKED_UNVERIFIED`

## 6. Approval Bundle 종료 조건

```text
APPROVED
→ CANON_UPDATED
→ CONSUMERS_UPDATED
→ PROJECT_SHEET_UPDATED
→ IMPLEMENTED | IMPLEMENTATION_PENDING
→ VALIDATED | BLOCKED_UNVERIFIED
→ NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

다음 Bundle은 현재 Bundle의 차단 Finding과 미동기화가 정리된 뒤 진행한다.
"""

NEW_TEST = """from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class DemoFirstPlanningSequenceTests(unittest.TestCase):
    def test_policy_declares_sheet_scope_and_prework_audit(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in (
            "BASE_EXCLUDED",
            "PROJECT_SHEET_CONFIGURED",
            "DUPLICATE_WORK",
            "MISSING_CANON",
            "MISSING_CONSUMER",
            "CANON_CONFLICT",
            "IMPLEMENTATION_CONFLICT",
            "STALE_REFERENCE",
            "PROPAGATION_AUDIT",
        ):
            self.assertIn(term, policy)

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
        combined = skill + reference
        for term in ("줄 수", "문자 수", "분량 상한", "내용 보존", "한 단계 발견성"):
            self.assertIn(term, combined)
        self.assertNotIn("self.assertLessEqual", read("tests/test_skill_system_coverage.py"))

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
"""

write("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md", POLICY)
write("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md", SHEET_TEMPLATE)
write("tests/test_demo_first_planning_sequence.py", NEW_TEST)

replace_once(
    "AGENTS.md",
    "정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다. 외부 벤치마크·리뷰·커뮤니티·모델 해석은 요구사항 권한이나 구현 사실의 정본이 아니다.\n",
    "정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다. 외부 벤치마크·리뷰·커뮤니티·모델 해석은 요구사항 권한이나 구현 사실의 정본이 아니다.\n\n"
    "## 2.1 작업 전 누락·충돌·근거 확인\n\n"
    "- 모든 L1 이상 작업은 최신 main, 현재 Decision, 분야 정본, 같은 Goal의 열린·최근 병합 PR, 실제 구현을 비교해 중복·누락·충돌·구형 참조·미반영을 먼저 판정한다.\n"
    "- 새 정책·Template·Skill·경로·ID는 파일 존재만 확인하지 않고 README·START_HERE·운영 정본·Registry·프로젝트 Template·분야 소비자·Test에 실제 연결됐는지 검사한다.\n"
    "- 중요 기획·방향성 결정은 벤치마킹, 플레이어 반응, 현업 또는 공식 권장 근거를 함께 검토한다.\n"
    "- 문서·Skill의 줄 수·문자 수·분량 상한보다 내용 보존·실행 가능성·한 단계 발견성을 우선한다.\n"
    "- Base 저장소 자체는 프로젝트 Google Sheets 동기화 대상이 아니다. 개별 프로젝트만 Sheet가 구성됐을 때 동기화한다.\n"
    "- 기본 제품 경로는 별도 CORE_POC Gate 없이 완성 품질의 Vertical Slice 데모와 플레이테스트로 진행한다. 상세 계약은 `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`를 따른다.\n"
)

replace_once(
    "docs/DOCUMENTATION_MAP.md",
    "| 승인 결정 즉시 동기화 | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | 질문 전 정본·PR·Sheets 대조, 중복 질문 방지, 승인 즉시 정본·main·Sheets 동기화, 병합 후 적대적 검토 |\n",
    "| 승인 결정 즉시 동기화 | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | 질문 전 정본·PR·Sheets 대조, 중복 질문 방지, 승인 즉시 정본·main·Sheets 동기화, 병합 후 적대적 검토 |\n"
    "| 기획 작업순서·근거·데모 우선 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | 누락·충돌 선감사, 3층 근거 묶음, 분야별 Approval Bundle, 소비처 전파, 개별 프로젝트 Sheet tab, Demo-First Vertical Slice |\n"
)

replace_once(
    "docs/CONFIRMED_DECISION_SYNC_POLICY.md",
    "## 9. Google Sheets 동기화\n\n프로젝트 Sheet에는 `확정 결정` 또는 프로젝트가 선언한 동일 책임 탭을 사용한다.\n",
    "## 9. Google Sheets 동기화\n\nBase 저장소 자체는 프로젝트 Google Sheets 동기화 범위에서 제외하며 `BASE_EXCLUDED`로 기록한다. Base 작업을 Sheet 미동기화 때문에 실패로 판정하지 않는다. 아래 계약은 Base를 적용한 개별 프로젝트가 유효한 Sheet URL·tab·권한을 가진 경우에만 적용한다. Sheet가 없는 개별 프로젝트는 `NOT_CONFIGURED`로 기록한다.\n\n프로젝트 Sheet에는 `확정 결정` 또는 프로젝트가 선언한 동일 책임 탭을 사용한다.\n"
)

replace_once(
    "skills/simplifying-skill-bodies/SKILL.md",
    "description: Use when a SKILL.md or operating router has grown too large and must retain only always-needed routing and execution rules while moving conditional templates, examples, domain detail, and decision tables into linked references with verified progressive disclosure.\n",
    "description: Use when a SKILL.md or operating router has become hard to navigate and must preserve all required behavior while separating always-needed routing from conditional detail through linked references with verified progressive disclosure and no numeric size ceiling.\n"
)
replace_once(
    "skills/simplifying-skill-bodies/SKILL.md",
    "## Workflow\n",
    "## Completeness-first rule\n\n"
    "- 줄 수, 문자 수, 페이지 수, 파일 크기나 임의의 분량 상한을 완료 조건으로 사용하지 않는다.\n"
    "- 본문과 reference의 총 내용에서 승인 결정·예외·검증·실패 조건이 보존돼야 한다.\n"
    "- Reference 이동은 내용 삭제나 테스트 통과용 축약이 아니라 책임 분리와 한 단계 발견성을 위한 것이다.\n"
    "- 짧아졌지만 필요한 판단을 찾기 어렵거나 내용이 빠지면 실패다. 길어도 책임과 경로가 명확하고 실행 가능하면 허용한다.\n\n"
    "## Workflow\n"
)
replace_once(
    "skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md",
    "검증 시 기본 요청은 본문만으로 시작 가능해야 하고, 특수 요청은 한 단계의 명시적 reference 경로로 세부 규칙을 찾을 수 있어야 한다.\n",
    "검증 시 기본 요청은 본문만으로 시작 가능해야 하고, 특수 요청은 한 단계의 명시적 reference 경로로 세부 규칙을 찾을 수 있어야 한다.\n\n"
    "- 줄 수·문자 수·페이지 수·분량 상한은 품질 기준이 아니다.\n"
    "- 이동 전후의 결정·예외·표·실패 조건·검증 절차를 비교해 내용 보존을 증명한다.\n"
    "- 한 단계 발견성을 깨뜨리는 깊은 reference 연쇄와, 크기 감소만을 위한 삭제·축약을 금지한다.\n"
)

replace_once(
    "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
    "요구가 확정되지 않았거나 중요한 사용자 결정이 남아 있으면 실행 순서를 확정하지 않는다.\n\n## 2. 분해 단위\n",
    "요구가 확정되지 않았거나 중요한 사용자 결정이 남아 있으면 실행 순서를 확정하지 않는다.\n\n"
    "## 1.1 분해 전 누락·충돌 감사\n\n"
    "분해 전에 최신 main, 현재 Decision, 관련 분야 정본, 동일 Goal의 열린·최근 병합 PR, 실제 구현과 개별 프로젝트 Sheet를 비교한다. `DUPLICATE_WORK`, `DUPLICATE_QUESTION`, `MISSING_CANON`, `MISSING_CONSUMER`, `CANON_CONFLICT`, `IMPLEMENTATION_CONFLICT`, `STALE_REFERENCE`, `MISSING_SYNC`가 있으면 새 작업 목록보다 복원과 정리를 먼저 배치한다. Base 저장소 자체의 Sheet 상태는 `BASE_EXCLUDED`다.\n\n"
    "## 2. 분해 단위\n"
)
replace_once(
    "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
    "## 8. 출력 형식\n",
    "## 7.1 Approval Bundle\n\n"
    "같은 플레이어 경험·시스템·정본·후속 구현에 영향을 주는 결정을 분야별 `Approval Bundle`로 묶는다. 각 Bundle은 현재 Decision, 누락·충돌 판정, Evidence ID, GPT 권장안, 사용자 승인, 영향받는 정본·소비처·Sheet tab, 검증 Gate를 가진다. 기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분리한다.\n\n"
    "승인 묶음의 기본 분야 순서는 `00 기반 → 10 제품 방향 → 20 코어 경험·데모 목표 → 30 데모 범위·품질·제작 기반 → 40 시스템·성장·경제 → 50 메인 콘텐츠 → 51 미니게임 → 52 글쓰기·서사 → 60 UX·UI·접근성 → 70 아트·오디오·에셋 → 80 데모 Vertical Slice·플레이테스트 → 90 본제작·출시 → 98 Base 후보 → 99 회고`다. 프로젝트에 없는 분야는 건너뛴다.\n\n"
    "## 8. 출력 형식\n"
)

replace_once(
    "skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md",
    "## 3. 비교 대상 선정\n",
    "## 2.1 중요 기획의 필수 Evidence Pack\n\n"
    "중요 기획·방향성·제품 결정은 다음 세 층을 함께 검토한다. 단순 오탈자·기계 수정·동일 입력 검사 재실행은 예외다.\n\n"
    "- `BENCHMARK_EVIDENCE`: 직접 경쟁작, 인접 장르, 실패·혼합 반응 사례에서 비교 원리와 실패 조건을 추출한다.\n"
    "- `PLAYER_RESPONSE_EVIDENCE`: 긍정·부정·혼합 리뷰, 커뮤니티, 플레이테스트와 행동 근거에서 기대·불만·맥락을 구분한다.\n"
    "- `PROFESSIONAL_OFFICIAL_EVIDENCE`: 현업 발표·사후 분석과 공식 플랫폼·엔진·접근성·운영 문서에서 권장 조건과 제약을 확인한다.\n\n"
    "한 층이 다른 층을 대체하지 않는다. 세 층을 모두 찾지 못하면 없는 근거를 만들어내지 않고 `BLOCKED_UNVERIFIED` 또는 제한된 신뢰도로 기록한다.\n\n"
    "## 3. 비교 대상 선정\n"
)

replace_once(
    "docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md",
    "CONCEPT_APPROVAL\n→ PROTOTYPE_AND_VERTICAL_SLICE\n→ PRODUCTION_APPROVAL\n→ RELEASE_CANDIDATE_APPROVAL\n",
    "CONCEPT_APPROVAL\n→ DEMO_FIRST_VERTICAL_SLICE\n→ PRODUCTION_APPROVAL\n→ RELEASE_CANDIDATE_APPROVAL\n\n`PROTOTYPE_AND_VERTICAL_SLICE`는 과거 기록 호환 이름이며 새 작업에서는 `DEMO_FIRST_VERTICAL_SLICE`로 해석한다.\n"
)
replace_once(
    "docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md",
    "- `CORE_POC` 가설\n",
    "- 데모 핵심 위험 등록부와 필요한 내부 `TECHNICAL_SPIKE` 후보\n"
)
replace_once(
    "docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md",
    "## 3. Gate 2 — 프로토타입＋버티컬 슬라이스\n\n### 연속 프로그램\n\n```text\nCORE_POC\n→ 기획 재조정\n→ 버티컬 슬라이스 제작\n→ 통합 데모 QA\n→ SLICE_VALIDATION\n→ 본제작 판단 자료\n```\n\n- `CORE_POC`: 버티컬 슬라이스 전 가장 위험한 핵심 재미·기술·제작 가설의 최소 내부 검증.\n- `SLICE_VALIDATION`: 버티컬 슬라이스 완성 후 외부 플레이·시장 검증.\n\n프로토타입 완료를 Gate 2의 종료로 간주하지 않는다. 실패한 가설을 고품질 자산과 콘텐츠 양으로 덮지 않는다.\n",
    "## 3. Gate 2 — 데모 우선 버티컬 슬라이스\n\n### 연속 프로그램\n\n```text\n데모 계약·품질 기준 확정\n→ 제작 의도 Vertical Slice 구현\n→ 통합 데모 QA\n→ 내부 플레이테스트\n→ 외부 플레이테스트·반응 조사\n→ DEMO_VALIDATION\n→ 본제작 판단 자료\n```\n\n별도 `CORE_POC` 제품 단계는 사용하지 않는다. 첫 통합 플레이 제품은 최종 방향에 가까운 아트·UI·UX·사운드·데이터·저장·복구·성능·접근성을 갖춘 **완성 품질 데모**다.\n\n데모 전체를 차단하는 기술 불확실성이 있을 때만 Vertical Slice 내부에 제한된 `TECHNICAL_SPIKE`를 둔다. Spike는 별도 Gate나 공개 데모가 아니며, 질문 하나와 성공·실패·중단 기준을 갖고 결과를 데모 구현에 재사용하거나 Decision 근거로 기록한다.\n\n`SLICE_VALIDATION`은 과거 호환 이름이며 새 작업에서는 내부·외부 플레이테스트와 반응 조사를 포함하는 `DEMO_VALIDATION`으로 해석한다. 위험한 가설을 완성 자산과 콘텐츠 양으로 덮지 않되, 저품질 폐기형 Prototype을 별도 마일스톤으로 승인하지 않는다.\n"
)
replace_once(
    "docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md",
    "- `APPROVED`: Slice·통합 데모·외부 검증·제작 반복성이 증명됨.\n",
    "- `APPROVED`: 완성 품질 Slice 데모·내외부 플레이테스트·외부 검증·제작 반복성이 증명됨.\n"
)

replace_once(
    "docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md",
    "| `CORE_POC`와 `SLICE_VALIDATION` 분리 | concept Skill + Gate reference | 명시 강화 |\n",
    "| 과거 `CORE_POC`·`SLICE_VALIDATION` | concept Skill + Gate reference | 최신 사용자 결정으로 별도 Core PoC Gate를 제거하고 내부 `TECHNICAL_SPIKE`·`DEMO_VALIDATION` 호환 해석으로 변경 |\n"
)
replace_once(
    "docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md",
    "## 기존 책임 보존\n",
    "## 2026-07-28 최신 사용자 결정\n\n"
    "- 별도 `CORE_POC` 제품 단계는 사용하지 않는다.\n"
    "- 첫 통합 플레이 제품은 완성 품질의 `DEMO_FIRST_VERTICAL_SLICE`다.\n"
    "- 기술 불확실성은 Slice 내부의 제한된 `TECHNICAL_SPIKE`로만 검증한다.\n"
    "- 과거 v6의 `CORE_POC`·`PROTOTYPE_AND_VERTICAL_SLICE`·`SLICE_VALIDATION` 표기는 각각 내부 Spike·`DEMO_FIRST_VERTICAL_SLICE`·`DEMO_VALIDATION`의 역사·호환 용어다.\n\n"
    "## 기존 책임 보존\n"
)

replace_once(
    "templates/planning/VERTICAL_SLICE_PLAN.md",
    "- 제품 단계: `PROTOTYPE_AND_VERTICAL_SLICE`\n",
    "- 제품 단계: `DEMO_FIRST_VERTICAL_SLICE` (`PROTOTYPE_AND_VERTICAL_SLICE`는 과거 호환 이름)\n"
)
replace_once(
    "templates/planning/VERTICAL_SLICE_PLAN.md",
    "## 2. CORE_POC 결과\n\n- 핵심 가설:\n- 가장 위험한 전제:\n- 최소 구현:\n- 빌드·환경:\n- 플레이 과제:\n- 관찰 행동:\n- 성공·실패·중단 기준:\n- 결과:\n- 판정: KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST\n- 버티컬 슬라이스에 반영할 재조정:\n",
    "## 2. 데모 핵심 위험·내부 Spike\n\n별도 `CORE_POC` Gate를 만들지 않는다. 아래는 데모 전체를 차단하는 기술 불확실성이 있을 때만 작성한다.\n\n- 데모 핵심 위험:\n- 영향을 받는 플레이어 약속·범위:\n- 필요한 `TECHNICAL_SPIKE` 질문:\n- 데모에서 재사용할 최소 산출물:\n- 빌드·환경:\n- 성공·실패·중단 기준:\n- 결과·증거:\n- 판정: KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST\n- 데모 계약·품질 기준에 반영할 조정:\n"
)
replace_once(
    "templates/planning/VERTICAL_SLICE_PLAN.md",
    "## 12. SLICE_VALIDATION\n",
    "## 12. DEMO_VALIDATION (`SLICE_VALIDATION` 호환)\n"
)

replace_once(
    "tests/test_vertical_slice_v6_contract.py",
    '            "CORE_POC 결과",\n',
    '            "데모 핵심 위험·내부 Spike",\n'
)
replace_once(
    "tests/test_vertical_slice_v6_contract.py",
    "        for state in (\n",
    "        self.assertIn(\"DEMO_FIRST_VERTICAL_SLICE\", plan)\n"
    "        self.assertIn(\"DEMO_VALIDATION\", plan)\n"
    "        self.assertNotIn(\"## 2. CORE_POC 결과\", plan)\n\n"
    "        for state in (\n"
)

replace_once(
    "tests/test_skill_system_coverage.py",
    "        self.assertLessEqual(\n            len((ROOT / \"skills/governing-legacy-retention-and-archives/SKILL.md\").read_text(encoding=\"utf-8\").splitlines()),\n            150,\n        )\n",
    "        simplifying = package_text(\"simplifying-skill-bodies\")\n"
    "        for term in (\"줄 수\", \"문자 수\", \"분량 상한\", \"내용 보존\", \"한 단계 발견성\"):\n"
    "            self.assertIn(term, simplifying)\n"
)

replace_once(
    "templates/project-operations/README.md",
    "## 발행 정책\n",
    "## 개별 프로젝트 기획 순서·Sheet tab\n\n"
    "Base 저장소 자체에는 Google Sheets를 만들지 않는다. 개별 프로젝트에서 `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`를 사용해 분야별 Approval Bundle과 tab 순서를 설치한다. 기본 제품 경로는 별도 Core PoC 없이 완성 품질의 Vertical Slice 데모·플레이테스트다.\n\n"
    "## 발행 정책\n"
)

replace_once(
    "docs/CHANGELOG.md",
    "## Unreleased - Base audit and operating-contract consistency\n\n",
    "## Unreleased - Base audit and operating-contract consistency\n\n"
    "- Base Sheet 제외, 컴팩트 수치 제한 제거, 작업 전 중복·누락·충돌 감사, 정책·Template·Skill 소비처 전파, 3층 근거 묶음, 분야별 Approval Bundle과 프로젝트 Sheet tab 순서, 별도 Core PoC 없는 완성 품질 Vertical Slice 데모·플레이테스트 기본 경로를 추가했다.\n"
)

replace_once(
    "skills/SKILL_LEARNING_LOG.md",
    "# Base Skill Learning Log\n\n",
    "# Base Skill Learning Log\n\n"
    "## 2026-07-28 내용 보존·근거 묶음·Demo-First 기획 순서 교훈\n\n"
    "- 문서·Skill의 줄 수나 분량을 품질 Gate로 사용하면 실행 계약·예외·검증 조건을 삭제해 테스트만 통과하는 회귀를 만들 수 있다. 수치형 컴팩트 제한 대신 내용 보존·책임 분리·한 단계 발견성을 검증한다.\n"
    "- 작업 시작 전에 이전 Decision·정본·PR·실제 구현을 비교하지 않으면 같은 질문·작업을 반복하고 승인 누락과 소비처 미반영을 뒤늦게 발견한다.\n"
    "- 새 정책·Template·Skill은 생성 여부가 아니라 README·START_HERE·운영 정본·Registry·프로젝트 설치·분야 소비자·Test에서 실제 소비되는지 확인해야 한다.\n"
    "- 중요한 기획은 벤치마킹·플레이어 반응·현업 또는 공식 권장의 세 층 근거를 Approval Bundle에 연결한다.\n"
    "- 사용자의 프로젝트 운영은 별도 Core PoC 마일스톤을 생략하고 제작 의도 자산을 사용하는 완성 품질 Vertical Slice 데모와 플레이테스트로 직접 검증한다. 기술 Spike는 Slice 내부의 제한된 위험 검증으로만 둔다.\n"
    "- Base 자체는 프로젝트 Google Sheets 범위에서 제외하고 개별 프로젝트만 구성된 Sheet에 동기화한다.\n"
    "- 현재 지식 상태: 사용자 승인과 Base 정본·회귀 검증으로 승격할 `PATTERN`.\n\n"
)

registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
by_id = {item["skill_id"]: item for item in registry["skills"]}
updates = {
    "simplifying-skill-bodies": {
        "trigger_tags": ["completeness-first", "no-size-ceiling", "progressive-disclosure"],
        "review_triggers": ["numeric compact limit", "content loss", "deep reference chain"],
    },
    "managing-project-intake-and-work-contract": {
        "trigger_tags": ["approval-bundle", "duplicate-omission-conflict-audit", "planning-sequence"],
        "review_triggers": ["baseline audit missing", "duplicate work", "consumer propagation missing"],
    },
    "analyzing-and-refining-game-concepts": {
        "trigger_tags": ["evidence-pack", "professional-official-evidence"],
        "review_triggers": ["benchmark-only decision", "player response missing", "professional evidence missing"],
    },
    "designing-vertical-slices": {
        "trigger_tags": ["demo-first", "polished-demo", "vertical-slice-playtest", "technical-spike"],
        "review_triggers": ["standalone core poc restored", "prototype quality mistaken for demo", "demo validation missing"],
    },
}
for skill_id, fields in updates.items():
    item = by_id[skill_id]
    for key, values in fields.items():
        for value in values:
            if value not in item[key]:
                item[key].append(value)
    item["last_reviewed_at"] = "2026-07-28"
    item["last_reviewed_commit"] = "fa2252860fc34d7dc2f2fac3c13c565073df4d79"
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

print("demo-first planning sequence patch applied")
