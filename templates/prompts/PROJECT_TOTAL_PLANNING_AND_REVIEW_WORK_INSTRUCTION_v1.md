---
contract_name: PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION
contract_version: "1.0"
status: ACTIVE_PROJECT_PLANNING_AND_REVIEW_PROMPT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
usage: "Base와 대상 프로젝트의 최신 작업 구조를 먼저 복원한 뒤 [총기획] 또는 [검수]를 실행하는 단일 첨부 작업지시문"
supported_modes:
  - TOTAL_PLANNING
  - REVIEW
specialized_prompt:
  vertical_slice_implementation: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
default_review_authority: READ_ONLY
authority_boundary: "최신 사용자 지시, 대상 프로젝트 정본·실제 구현, 프로젝트가 채택한 Base 계약보다 높은 권한을 갖지 않는다."
core_policies:
  - CORE_CONTENT_TRACEABILITY
  - PROJECT_ENVIRONMENT_FIRST
  - REPOSITORY_FIRST
  - TOTAL_PLANNING_COVERAGE
  - CANONICAL_SINGLE_SOURCE
  - BENCHMARK_AND_PLAYER_EVIDENCE
  - NEUTRAL_RECOMMENDATION_GATE
  - ADVERSARIAL_REVIEW_LIFECYCLE
  - PLAN_BUILD_REVIEW_SEPARATION
  - SOURCE_CONSUMER_PROPAGATION
  - EVIDENCE_BEFORE_COMPLETION
---

# 프로젝트 `[총기획]`·`[검수]` 통합 작업지시문 v1

## 0. 사용 방법

이 파일을 첨부하고 아래 입력 블록을 제공한다.

```yaml
mode: TOTAL_PLANNING | REVIEW | AUTO
base_repository: https://github.com/alsdmlals4-eng/Base
project_repository:
project_google_sheet:
current_goal:
requested_deliverables:
protected_decisions: []
protected_files_or_assets: []
explicit_exclusions: []
review_fix_authority: READ_ONLY | APPROVED_FINDINGS_ONLY
```

### `[핵심 내용]` — 목적 보존 구역

```text
[핵심 내용]
이번 프로젝트의 핵심 목적, 현재 확정된 방향, 반드시 포함할 기능·경험·콘텐츠,
금지·제외 사항, 원하는 결과물과 완료 기준을 원문 그대로 붙여 넣는다.
```

`[핵심 내용]`은 요약·정리·리팩터링 과정에서 삭제하거나 약화할 수 없는 보호 입력이다.

작업 시작과 종료에 다음 표를 대조한다.

| 원문 요구 | 기획·검수 요구로 해석 | 책임 정본·실제 대상 | 검증 방법 | 상태 |
|---|---|---|---|---|
|  |  |  |  | `PENDING` |

허용 상태:

- `CONFIRMED`
- `IMPLEMENTED`
- `VALIDATED`
- `DEFERRED_WITH_REASON`
- `OUT_OF_SCOPE_CONFIRMED`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`

핵심 요구가 책임 정본·실제 구현·검증 중 어느 것에도 연결되지 않으면 완료로 판정하지 않는다.

---

## 1. 이 작업지시문의 책임

이 문서는 다음 두 작업만 수행한다.

### `[총기획]`

프로젝트의 기존 정본·결정·실제 구현을 먼저 복원하고, 프로젝트 전체 기획을 누락 없이 정리·보완·통합해 실행 가능한 GDD와 후속 제작 계약을 만든다.

### `[검수]`

총기획서, 분야별 정본, 실제 코드·데이터·Scene·Resource·자산·테스트를 적대적으로 대조해 왜곡·누락·충돌·중복·구형 참조·실현 불가능성·회귀 위험을 판정한다.

기본 검수 권한은 `READ_ONLY`다. 사용자가 수정까지 요청했거나 승인한 finding이 있을 때만 최소 수정하고 다시 검수한다.

이 문서는 다음을 자동으로 수행하지 않는다.

- 사용자가 요청하지 않은 게임 구현
- 프로젝트 코어·주요 UX·서사·아트 방향의 무단 변경
- 승인 자산 삭제·교체
- 파일·폴더 대량 이동·삭제
- Google Sheets를 GitHub 정본보다 높은 권한으로 취급
- 테스트·런타임·플레이테스트를 실행하지 않고 통과로 보고
- 모든 Skill과 모든 파일의 무차별 로드

---

## 2. 권한 순서

```text
최신 사용자 지시와 승인
→ 프로젝트 AGENTS.md·보안·엔진·데이터 규칙
→ 현재 확정 Decision·Active Context·승인된 작업 계약
→ 등록된 기획 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트가 채택한 Base 계약과 pin
→ Base 최신 main의 현행 운영 정본·Skill Registry
→ 이 작업지시문
→ 외부 벤치마크·리뷰·과거 대화·초안·AI 추론
```

- 하위 자료가 상위 자료를 자동으로 덮어쓰지 않는다.
- 외부 사례는 개선 가설이며 프로젝트 요구나 실제 구현의 정본이 아니다.
- 이 Prompt가 최신 Base와 충돌하면 최신 Base를 적용하고 `STALE_PROMPT_CONTRACT`를 기록한다.
- 정상 동작 중인 사용자 변경과 승인된 결정·자산을 임의로 되돌리지 않는다.

---

## 3. 작업 환경 우선 복원

기획이나 검수 전에 Base와 프로젝트의 현행 작업 구조를 먼저 확인한다.

### 3.1 Base 읽기 순서

```text
최신 main과 정확한 SHA
→ 같은 Goal의 열린·최근 병합 PR
→ START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md
→ skills/SKILL_REGISTRY.json
→ 현재 요청에 필요한 최소 Skill·Reference·Template·Test
```

`Base를 전부 살펴본다`는 모든 파일을 무작정 읽는다는 뜻이 아니다. Registry와 Documentation Map으로 현재 작업의 책임 원본과 활성 소비자를 선별하고, 새 연결·충돌·누락이 발견될 때만 범위를 확장한다.

### 3.2 프로젝트 읽기 순서

```text
최신 main·정확한 SHA·현재 브랜치
→ 열린·최근 병합 PR·Issue·Plan
→ 프로젝트 AGENTS.md·START_HERE
→ ACTIVE_CONTEXT·CURRENT_CONFIRMED_DECISIONS
→ DOCUMENTATION_MAP·DESIGN_DOCUMENT_REGISTRY
→ 현재 GDD·분야별 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트 Google Sheets(구성됐을 때)
→ 생성본·PDF·DOCX·Dashboard·Manifest
```

Base의 프로젝트 Template을 실제 프로젝트의 활성 상태로 오인하지 않는다.

### 3.3 환경 확인표

```yaml
base_main_sha:
project_main_sha:
current_branch_and_head:
working_tree_state:
repository_read_access:
repository_write_access:
related_open_and_recent_prs:
project_engine_and_version:
actual_project_path:
required_tools_and_versions:
available_runtime_or_build_environment:
project_google_sheet_state:
validation_commands:
required_checks:
protected_paths:
rollback_path:
unverified_inputs:
```

확인하지 못한 항목은 추정하지 않고 `NOT_AVAILABLE`, `NOT_RUN`, `BLOCKED_UNVERIFIED` 중 하나로 기록한다.

---

## 4. 모드 선택

### `TOTAL_PLANNING`

다음 요청에 사용한다.

- 프로젝트 전체 기획을 처음 작성한다.
- 기존 기획을 최신 Base 구조에 맞게 통합·보완한다.
- 흩어진 결정과 문서를 하나의 책임 구조로 정리한다.
- 프로젝트 코어부터 제작·검증·출시까지 전체 기획 누락을 확인한다.
- 구현 전에 Codex나 개발팀이 실행할 수 있는 총기획·제작 계약을 만든다.

주 Work Mode:

```text
PLAN
→ 필요한 정본 문서 작성·갱신에 한해 BUILD
→ REVIEW
```

제품 코드·Scene·데이터 구현은 별도 요청이 없으면 범위 밖이다.

### `REVIEW`

다음 요청에 사용한다.

- 총기획서나 GDD가 충분한지 검수한다.
- 기획과 실제 구현이 일치하는지 확인한다.
- 최신 파일과 구형 파일의 참조 충돌을 찾는다.
- 누락·중복·왜곡·실현 불가능한 항목을 찾는다.
- PR·외부 AI 결과·기획 수정 결과를 독립 검수한다.

주 Work Mode:

```text
REVIEW
→ 승인된 finding 수정이 있을 때만 BUILD
→ REVIEW 재검증
```

### `AUTO`

사용자 요청에서 주 목적을 판정한다.

- 새 기획·통합·구조화가 핵심이면 `TOTAL_PLANNING`
- 기존 결과의 판정·오류 탐색이 핵심이면 `REVIEW`
- 둘 다 요청하면 `TOTAL_PLANNING → REVIEW` 순서로 진행한다.

한 시점에는 주 모드 하나만 둔다.

---

## 5. Base Skill·Superpowers 라우팅

새 L1 이상 요청은 `managing-project-intake-and-work-contract`로 한 번만 접수한다.

### 공통 Foundation

- `managing-project-intake-and-work-contract`
- `running-adversarial-review-and-refinement`
- `reviewing-and-validating-project-changes`
- 필요 시 `auditing-canonical-reference-freshness`
- 종료 시 `maintaining-project-context-and-handoff`

### `[총기획]` 주 책임 후보

현재 trigger와 프로젝트 상태에 따라 필요한 최소 항목만 선택한다.

- 기존 프로젝트 코어 판정: `identifying-project-core`
- 기획 단계 프로젝트 코어 확정: `establishing-project-core`
- 핵심 컨셉·뾰족한 재미·벤치마크·PoC·플레이테스트: `analyzing-and-refining-game-concepts`
- 기획 책임 원본 작성·구조·발행: `managing-design-documents`
- 대표 경험·데모·제작 파이프라인: `designing-vertical-slices`
- UX/UI·시각 구현 결과: `auditing-and-refining-ui-art`
- 프로젝트 고유 반복 절차 학습: `evolving-project-discipline-skills`

주 책임 분야 Skill은 한 단계에서 최대 하나만 둔다.

### `[검수]` 주 책임

- 실패 가정 공격과 finding 판정:
  `running-adversarial-review-and-refinement`
- 계약·diff·정적·런타임·접근성·성능·회귀 증거:
  `reviewing-and-validating-project-changes`
- 경로·ID·Schema·정본·파생본 전파:
  `auditing-canonical-reference-freshness`
- UI·아트의 전문 시각 검수:
  `auditing-and-refining-ui-art`

### Superpowers

실행 환경에 실제 Skill이 제공될 때만 사용한다.

```text
using-superpowers
→ 총기획·창의적 설계 전 brainstorming
→ 다단계 작업 전 writing-plans
→ 구현 수정이 포함될 때 test-driven-development
→ 실패 원인이 불명확할 때 systematic-debugging
→ 완료 주장 전 verification-before-completion
→ 주요 결과·PR 완료 전 requesting-code-review
```

외부 Skill을 Base Registry에 중복 생성하지 않는다. 사용할 수 없으면 Base의 동등 책임으로 수행하고 `NOT_AVAILABLE`을 기록한다.

---

## 6. 공통 선행 감사

`[총기획]`과 `[검수]` 모두 새 작업 전에 다음을 비교한다.

```text
최신 main
→ 현재 확정 Decision
→ 관련 분야 책임 원본
→ 같은 Goal의 열린·최근 병합 PR
→ 실제 구현
→ 프로젝트 Sheet(구성됐을 때)
→ 생성본·발행본
→ 중복·누락·충돌·구형 참조·미반영 판정
```

필수 판정:

- `DUPLICATE_WORK`
- `DUPLICATE_QUESTION`
- `MISSING_CANON`
- `MISSING_CONSUMER`
- `MISSING_SYNC`
- `CANON_CONFLICT`
- `IMPLEMENTATION_CONFLICT`
- `STALE_REFERENCE`
- `ORPHANED_REFERENCE`
- `DUPLICATE_ACTIVE_SOURCE`
- `DERIVATIVE_STALE`
- `ALLOWED_LEGACY`
- `NO_CONFLICT`
- `BLOCKED_UNVERIFIED`

차단 finding이 있으면 새 기획 작성보다 복원·충돌 해소·재동기화를 먼저 수행한다.

### 질문 규칙

저장소에서 확인할 수 있는 사실은 사용자에게 묻지 않는다.

사용자에게 묻는 것은 다음처럼 결과 방향을 바꾸는 결정뿐이다.

- 프로젝트 코어와 비타협 조건
- 플레이어에게 약속할 대표 경험
- 주요 시스템·UX·서사·아트 방향
- 범위·비용·일정의 중대한 교환
- 둘 이상의 유효한 정본이 충돌하는 결정
- 승인된 기능·자산·정체성의 제거·대체

질문은 가장 차단적인 결정부터 한 번에 하나씩 제시한다.

각 질문에는 다음을 포함한다.

- 충돌 또는 결정 이유
- 유효한 선택지
- 선택지별 장단점
- GPT 권장안
- 확정 시 영향 범위

사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 권장안으로 확정하고 질문을 반복하지 않는다.

---

# PART A. `[총기획]`

## 7. `[총기획]` 목표

`[총기획]`은 문서 분량을 늘리는 작업이 아니다.

다음을 증명하는 작업이다.

1. 프로젝트가 누구에게 어떤 경험을 약속하는가.
2. 그 경험을 반복하게 만드는 뾰족한 재미와 핵심 루프가 무엇인가.
3. 모든 시스템·콘텐츠·세계·표현이 같은 방향을 지지하는가.
4. 제작 가능한 범위와 순서로 나뉘어 있는가.
5. 실제 구현·검증·출시 단계에서 사용할 책임 원본과 수용 기준이 있는가.
6. 기존 결정·구현·자산이 누락되거나 왜곡되지 않았는가.

---

## 8. `[총기획]` 실행 루프

```text
1. BASELINE_RECOVERY
→ 2. CORE_AND_PROMISE
→ 3. EVIDENCE_AND_BENCHMARK
→ 4. TOTAL_PLANNING_MODULES
→ 5. CROSS_SYSTEM_COHERENCE
→ 6. APPROVAL_BUNDLES
→ 7. CANONICAL_UPDATE
→ 8. IMPLEMENTATION_HANDOFF
→ 9. ADVERSARIAL_REVIEW
→ 10. GATE_CLOSE
```

---

## 9. 프로젝트 코어와 플레이어 약속

먼저 다음을 한 문장 또는 검증 가능한 계약으로 확정한다.

```yaml
project_one_line_pitch:
target_player_and_play_context:
genre_platform_engine:
player_promise:
project_core:
non_negotiable_strengths:
pointed_fun:
core_loop:
session_loop:
meta_progression:
key_player_choices:
success_failure_and_recovery:
target_emotion_and_game_feel:
differentiation_hypothesis:
scope_boundary:
```

프로젝트 코어가 이미 존재하면 새로 발명하지 말고 실제 기획·구현·사용자 결정을 근거로 복원한다.

코어가 불명확하면 `identifying-project-core` 또는 `establishing-project-core`로 라우팅한다.

### 중립성 Gate

사용자안과 AI 최초안은 같은 기준으로 비교한다.

```yaml
evaluation_criteria:
alternatives:
supporting_evidence:
counterevidence:
player_value:
production_cost:
operational_burden:
compatibility_and_regression_risk:
reversibility:
unknowns:
recommended_conclusion:
```

검토 결과 사용자안이 가장 강하면 근거와 함께 채택한다. 다른 안이 더 강하면 차이를 만드는 근거를 제시한다. 반대를 위한 반대는 금지한다.

---

## 10. 벤치마킹·플레이어 근거

조사 전에 현재 결정을 바꿀 질문을 고정한다.

예:

- 이 핵심 루프는 플레이어가 반복할 이유를 제공하는가.
- 비슷한 게임의 이탈 지점은 무엇이었는가.
- 해당 UX가 목표 플랫폼과 입력 방식에 적합한가.
- 이 콘텐츠 구조는 팀 규모와 제작 속도에서 유지 가능한가.

### 출처 우선순위

1. 공식 게임·엔진·플랫폼 문서와 실제 제품
2. 개발자 발표·사후 분석·기술 블로그
3. 실제 플레이 관찰·텔레메트리·퍼널
4. 플레이어 리뷰·인터뷰·커뮤니티
5. 전문 서적·종합 자료
6. AI 추론

### 조사 규칙

- 성공 사례뿐 아니라 실패·혼합 반응도 확인한다.
- 제품 사실과 플레이어 의견을 구분한다.
- 행동 데이터와 자기보고를 구분한다.
- 패치·플랫폼·플레이타임·언어·표본 차이를 기록한다.
- 인기 기능을 그대로 복사하지 않는다.
- `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 판정한다.
- 외부 근거가 프로젝트 코어보다 높은 권한을 갖지 않는다.

### 실무 적용표

| Evidence ID | 결정 질문 | 관찰 사실 | 성공·실패 조건 | 프로젝트 차이 | 적용 판정 | 후속 검증 |
|---|---|---|---|---|---|---|

---

## 11. 총기획 6개 영역

관련 없는 항목은 억지로 채우지 않고 `NOT_APPLICABLE`과 이유를 기록한다.

### `00 프로젝트 기반·현재 상태`

필수 확인:

- 프로젝트 저장소·엔진·플랫폼·현재 Stage
- 프로젝트 한 문장 설명
- 현재 확정 Decision
- 활성 GDD와 책임 원본
- 실제 구현 상태
- 열린 Issue·PR·Plan
- 보호 결정·자산·경로
- 현재 위험·차단 finding
- 프로젝트 Sheet와 발행 상태
- 다음 Approval Bundle

### `10 제품·경험`

필수 기획:

- 타깃 플레이어와 플레이 상황
- 플레이어 약속·제품 방향
- 핵심 컨셉·뾰족한 재미
- Core Loop·Session Loop·Meta Loop
- 조작과 핵심 선택
- 승리·실패·복구
- 온보딩·학습 곡선
- 난이도·도전·보상
- 게임 필·피드백·가독성
- 접근성 기본 방향
- 시장·스토어 약속과 실제 경험의 일치

### `20 시스템·콘텐츠`

필수 기획:

- 전체 시스템 관계도
- 메인 게임 규칙과 상태
- 핵심 입력·출력·보상
- 자원·경제·성장·강화
- 콘텐츠 구조와 반복 규칙
- 레벨·스테이지·미션 구조
- 적·AI·난이도 구조
- 아이템·장비·스킬·캐릭터
- 실패·복구·저장·호환성
- 핵심 수치·공식·단위·초기 시험값
- 시스템 간 양성·음성 피드백
- 데모·Vertical Slice·본제작 범위

### `30 세계·서사`

해당 프로젝트에 필요한 범위만 기획한다.

- 세계관 규칙과 금기
- 배경·장소·시간·세력
- 주요인물·조연·관계
- 플레이어 역할과 동기
- 메인 서사·사건·콘텐츠 흐름
- 정보 공개 순서
- 시스템과 서사의 연결
- 반복 콘텐츠의 서사적 정당화
- 톤·문체·용어·명명 규칙
- 모순·연속성·스포일러 관리

### `40 표현·UX`

필수 기획:

- 전체 사용자 흐름과 화면 구조
- 핵심 HUD·메뉴·상태 전달
- 입력 장치·포커스·취소·확인
- 실패·오류·파괴 행동 UX
- 아트 디렉션·형태·색·재질·카메라
- 캐릭터·환경·이펙트·애니메이션 역할
- 사운드·음악·효과음·정보 전달
- 접근성 대체 채널
- 승인 이미지·레퍼런스·출처·라이선스
- 이미지 생성·수정·검수 상태
- 실제 엔진 화면과 기획 이미지의 구분

### `50 제작·기술·검증`

필수 기획:

- 기술 구조와 책임 경계
- 데이터·ID·Schema·저장·마이그레이션
- 엔진·플러그인·외부 서비스·라이선스
- 제작 파이프라인과 반복 제작성
- 마일스톤·Approval Bundle·의존성
- Vertical Slice·데모 목표 품질
- 테스트·QA·회귀·플레이테스트
- 접근성 검증 범위
- 성능 예산과 목표 플랫폼
- 텔레메트리·분석·피드백 계획
- 배포·스토어·출시·운영
- 수익·사업 모델(해당할 때)
- 위험·대체안·중단 조건·롤백
- Codex·개발팀 구현 인계

### `99 변경 이력·학습`

- Decision 추가·대체·기각·보류
- 변경 이유와 Evidence
- 실제 반영 Commit
- 실패·회귀·복구 기록
- 프로젝트 Skill 학습 후보
- Base 환류 후보
- 다음 재검토 조건

---

## 12. 각 기획 항목의 최소 계약

모든 중요 기획 항목은 다음 필드를 가진다.

```yaml
module_id:
question_or_player_problem:
current_confirmed_decision:
player_value:
relationship_to_project_core:
evidence_ids:
alternatives_considered:
gpt_recommendation:
user_decision_status:
rules_and_state:
inputs:
outputs_and_feedback:
dependencies:
affected_systems_and_content:
edge_cases_and_failure_recovery:
initial_values_and_tuning_range:
implementation_scope:
out_of_scope:
canonical_source:
affected_consumers:
acceptance_criteria:
validation:
implementation_status:
validation_status:
unknowns_and_revisit_trigger:
```

정본에 없는 임의 숫자는 확정값으로 쓰지 않는다. 초기값은 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 표시한다.

---

## 13. 분야 간 정합성 검수

총기획의 각 영역을 따로 완성한 뒤 다음 연결을 검사한다.

- 플레이어 약속 ↔ 핵심 루프
- 핵심 루프 ↔ 보상·성장·경제
- 시스템 ↔ 콘텐츠 제작량
- 세계·서사 ↔ 플레이 규칙
- UX·UI ↔ 시스템 상태와 입력
- 아트·사운드 ↔ 정보 전달과 게임 필
- 접근성 ↔ 핵심 정보·입력·시간 제한
- 저장·데이터 ↔ 성장·콘텐츠·업데이트
- Vertical Slice ↔ 대표 경험과 제작 파이프라인
- 출시 약속 ↔ 실제 범위·품질·운영 능력

충돌은 숨기지 않고 다음 중 하나로 판정한다.

- `MUST_RESOLVE`
- `USER_DECISION_REQUIRED`
- `TEST_IN_VERTICAL_SLICE`
- `DEFERRED_WITH_BOUNDARY`
- `NO_CONFLICT`

---

## 14. Approval Bundle

같은 플레이어 경험이나 후속 구현에 영향을 주는 결정을 묶어서 승인한다.

```yaml
bundle_id:
discipline:
goal:
current_decisions:
new_or_changed_decisions:
evidence_ids:
alternatives:
gpt_recommendation:
user_decisions_required:
dependencies:
affected_canonical_sources:
affected_consumers:
implementation_handoff:
validation_gate:
rollback:
```

사용자 승인 전 프로젝트 코어·주요 UX·서사·아트 방향을 확정 상태로 기록하지 않는다.

---

## 15. 책임 원본 갱신

승인된 내용만 다음에 반영한다.

- `CURRENT_CONFIRMED_DECISIONS.md`
- `ACTIVE_CONTEXT.md`
- `DESIGN_DOCUMENT_REGISTRY.json`
- 분야별 GDD 책임 원본
- 필요한 Issue·Plan·Roadmap
- 프로젝트 Sheet(구성됐을 때)
- 생성본·발행본·Manifest(정책이 요구할 때)

한 질문에 둘 이상의 활성 정본을 만들지 않는다.

`v2`, `final`, `latest`, 날짜별 활성 복제본을 새 정본으로 만들지 않는다.

변경 후 다음 소비자를 확인한다.

- START_HERE·Documentation Map
- Registry·Router·Template
- 실제 구현 계약·데이터 Schema
- 테스트·Fixture·Workflow
- PDF·DOCX·Sheet·Dashboard·Manifest
- 구형 경로·ID·용어 참조

누락 소비자가 있으면 `MISSING_CONSUMER`로 Gate를 닫지 않는다.

---

## 16. 구현 인계 패키지

`[총기획]`의 기본 종료점은 구현 자체가 아니라 실행 가능한 인계다.

```yaml
implementation_goal:
approved_decisions_and_canonical_sources:
player_visible_outcome:
in_scope:
out_of_scope:
protected_decisions_files_assets:
files_and_systems_expected_to_change:
data_and_state_ownership:
dependencies_and_execution_order:
acceptance_criteria:
normal_failure_edge_and_regression_cases:
runtime_and_platform_validation:
accessibility_scope:
performance_budget:
documentation_and_consumer_updates:
rollback:
open_user_decisions:
blocked_unverified:
```

복잡한 작업은 `Issue → Plan → 구현 패키지 → 검증 Gate`로 나눈다.

---

# PART B. `[검수]`

## 17. `[검수]` 목표

검수는 문장을 예쁘게 고치는 작업이 아니다.

다음을 판정하는 작업이다.

1. `[핵심 내용]`과 사용자 결정이 정확히 보존됐는가.
2. 총기획의 필수 영역과 연결이 빠지지 않았는가.
3. 서로 다른 정본이 충돌하지 않는가.
4. 기획과 실제 구현이 일치하는가.
5. 구형 파일·경로·ID·용어가 활성 상태로 남지 않았는가.
6. 제작·기술·콘텐츠 규모가 현실적으로 실행 가능한가.
7. 플레이어 경험·UX·접근성·성능·운영 위험이 통제됐는가.
8. 실제 증거 없이 완료 상태가 상승하지 않았는가.

---

## 18. 검수 권한

기본값:

```yaml
review_fix_authority: READ_ONLY
```

`READ_ONLY`에서는 finding과 수정안을 보고하지만 파일을 수정하지 않는다.

다음 조건에서만 수정한다.

```yaml
review_fix_authority: APPROVED_FINDINGS_ONLY
```

- 사용자가 검수와 수정을 함께 명시했다.
- 사용자 승인 범위가 이미 존재한다.
- 기술적으로 단일 답이 있는 명백한 누락·오류다.
- 프로젝트 코어·주요 UX·서사·아트 방향을 바꾸지 않는다.

수정 후 반드시 REVIEW로 돌아와 회귀를 재검사한다.

---

## 19. 검수 기준선

```yaml
review_target:
baseline_branch_and_commit:
approved_work_contract:
core_content_traceability:
current_confirmed_decisions:
canonical_sources:
actual_implementation:
changed_files_or_diff:
related_open_and_recent_prs:
project_sheet_state:
generated_and_published_derivatives:
validation_environment:
protected_strengths_and_assets:
```

검색 결과나 일부 파일만 보고 저장소 전체를 검수했다고 주장하지 않는다.

---

## 20. 검수 생명주기

```text
REVIEW_SCOPE_MAP
→ BASELINE_RECOVERY
→ CONTRACT_AND_CORE_CHECK
→ COVERAGE_AND_CANON_CHECK
→ IMPLEMENTATION_ALIGNMENT
→ ADVERSARIAL_ATTACK
→ VALIDATE_CRITIQUE
→ FINDING_DECISION
→ 승인된 경우 MINIMAL_FIX
→ REGRESSION_RECHECK
→ EVIDENCE_REPORT
```

적대적 검토의 기본 경로:

```text
attack
→ validate-critique
→ decision-report
```

수정 권한이 있을 때:

```text
attack
→ validate-critique
→ approved finding
→ 분야 주 책임 Skill BUILD
→ regression-recheck
→ decision-report
```

적대적 검토 Skill이 분야 작성 책임을 빼앗거나 같은 finding을 반복 수정하지 않는다.

---

## 21. 검수 관점

각 관점을 `APPLIED / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 기록한다.

### A. 목적·코어 보존

- `[핵심 내용]`이 약화·왜곡·삭제됐는가.
- 프로젝트 코어와 플레이어 약속이 일치하는가.
- 뾰족한 재미가 기능 목록에 묻혔는가.
- 승인된 강점과 자산이 보존됐는가.
- AI나 벤치마크가 프로젝트 방향을 임의로 바꿨는가.

### B. 총기획 범위·누락

- `00 / 10 / 20 / 30 / 40 / 50 / 99` 영역 중 필요한 것이 빠졌는가.
- 각 기획 항목에 규칙·입력·출력·실패·복구·검증이 있는가.
- 핵심 시스템과 콘텐츠가 연결됐는가.
- 데모·Vertical Slice·본제작 경계가 명확한가.
- 출시·운영 약속이 실제 범위에 맞는가.

### C. 정본·결정 정합성

- 한 질문에 둘 이상의 활성 정본이 있는가.
- 최신 Decision이 누락됐는가.
- `SUPERSEDED / REJECTED / DEFERRED` 결정이 부활했는가.
- 프로젝트 Sheet와 GitHub 정본이 다른가.
- PDF·DOCX·Dashboard·Manifest가 원본보다 오래됐는가.

### D. 시스템·수치·상호작용

- Core Loop와 보상·성장·경제가 같은 행동을 강화하는가.
- 자원 생성·소비·인플레이션·막힘이 통제되는가.
- 시스템 간 무한 루프·악용·소프트락이 있는가.
- 초기 시험값과 확정값이 구분됐는가.
- 실패·복구·저장 호환성이 정의됐는가.

### E. 세계·서사·콘텐츠 연속성

- 세계관 규칙과 플레이 규칙이 충돌하는가.
- 인물·세력·사건의 동기와 순서가 일관되는가.
- 정보 공개 시점과 플레이어 지식이 맞는가.
- 반복 콘텐츠가 설정과 플레이 목적을 훼손하는가.
- 용어와 명명 규칙이 통일됐는가.

### F. UX·UI·아트·사운드

- 핵심 정보가 적시에 명확하게 전달되는가.
- 입력·포커스·취소·확인·오류 복구가 정의됐는가.
- 색·텍스트·아이콘·오디오 등 대체 채널이 있는가.
- 기획 이미지와 실제 구현 화면을 혼동하는가.
- 승인 이미지·레퍼런스·라이선스가 보존됐는가.
- 아트·사운드가 게임 필과 정보 전달을 지원하는가.

### G. 제작·기술·운영 가능성

- 팀·도구·일정·예산에 비해 범위가 과도한가.
- 데이터·Schema·저장·마이그레이션 책임이 있는가.
- 외부 플러그인·서비스·라이선스 위험이 있는가.
- 반복 제작 파이프라인이 증명됐는가.
- 목표 플랫폼 성능과 빌드 경로가 정의됐는가.
- 운영·업데이트·지원 비용이 누락됐는가.

### H. 벤치마크·근거 품질

- 성공 사례만 선택했는가.
- 다른 장르·팀 규모·플랫폼을 과잉 일반화했는가.
- 플레이어 행동과 자기보고를 혼동했는가.
- 오래된 패치·버전·표본을 현재 사실처럼 사용했는가.
- AI 추론을 공식 사실처럼 사용했는가.
- 근거가 실제 기획 결정과 검증으로 연결됐는가.

### I. 실제 구현 정렬

- 기획된 기능이 실제 코드·데이터·Scene·자산에 존재하는가.
- 실제 구현이 기획과 다른 규칙을 사용하는가.
- 구현되지 않은 기능이 완료로 표시됐는가.
- 변경된 정본의 소비자·테스트가 untouched인가.
- 정상·실패·경계·회귀 테스트가 있는가.
- 런타임·렌더·플레이테스트를 실제로 실행했는가.

### J. 구형 참조·전파

- 구형 파일명·경로·Skill ID·Schema·제품 단계가 활성 참조로 남았는가.
- 새 정본을 읽어야 할 START_HERE·Registry·Template·Test가 누락됐는가.
- Legacy가 역사·호환·Fixture 목적으로만 남아 있는가.
- 고아 파일·중복 현행본·stale 파생본이 있는가.

---

## 22. Finding 판정

- `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함
- `SHOULD_FIX`: 현재 범위에서 가치가 크고 회귀 위험이 통제되는 결함
- `USER_DECISION_REQUIRED`: 둘 이상의 유효한 선택지가 프로젝트 방향을 다르게 만듦
- `DEFER`: 유효하지만 현재 범위·근거·비용상 보류
- `REJECTED_CRITIQUE`: 취향·중복·잘못된 전제·범위 밖 비판
- `BLOCKED_UNVERIFIED`: 필요한 정본·도구·권한·실행 증거가 없음
- `ALLOWED_LEGACY`: 역사·호환·Fixture 목적으로 현행 권한 없이 보존

### Finding Ledger

| ID | 심각도 | 관점 | 위치 | 증거 | 영향 | 판정 | 수정 방향 | 검증 |
|---|---|---|---|---|---|---|---|---|

비판은 사실성·발생 가능성·영향·범위·수정 비용을 다시 검증한다.

유효한 비판이 없으면 근거 있는 `NO_CHANGE` 또는 `REJECTED_CRITIQUE`를 기록한다.

---

## 23. 승인된 최소 수정

승인된 `MUST_FIX`와 `SHOULD_FIX`만 수정한다.

- 기존 장점과 정상 경로를 보존한다.
- 기능 추가와 정리·리팩터링을 분리한다.
- 사용자 결정이 필요한 항목을 몰래 확정하지 않는다.
- 같은 정보의 새 활성 복제본을 만들지 않는다.
- 경로·ID·Schema 변경 시 모든 소비자를 추적한다.
- 수정 전후 diff와 롤백을 유지한다.

---

## 24. 회귀 재검사

수정 후 다음을 다시 공격한다.

- `[핵심 내용]` 보존
- 프로젝트 코어와 대표 경험
- 기존 정상 경로
- 시스템·콘텐츠 상호작용
- 저장·데이터·호환성
- UX·접근성·성능
- 구형 참조와 소비자 전파
- 새 중복 정본·새 고아 파일
- 실제 테스트·런타임 증거
- 롤백 가능성

수정으로 새 결함이 생기면 Gate를 닫지 않는다.

---

## 25. 검증 계층

현재 범위에 적용되는 것만 실행한다.

```text
contract-check
→ multi-lens-review
→ reference-freshness
→ static-validation
→ runtime-validation
→ accessibility-review
→ performance-profile
→ regression
→ evidence-report
```

실행 상태:

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`
- `BLOCKED_UNVERIFIED`

한 계층의 통과를 다른 계층의 통과로 확장하지 않는다.

예:

- 문서 정적 검사가 통과해도 런타임이 검증된 것은 아니다.
- 이미지가 있어도 실제 UI 구현·접근성이 검증된 것은 아니다.
- 테스트가 통과해도 플레이어 재미가 증명된 것은 아니다.
- Evidence Pack이 있어도 실제 시장성·성능·출시 준비가 증명된 것은 아니다.

---

## 26. 산출물

### `[총기획]` 필수 산출물

1. `Baseline Recovery Record`
2. `[핵심 내용] Requirement Traceability`
3. 프로젝트 코어·플레이어 약속·비타협 조건
4. `00 / 10 / 20 / 30 / 40 / 50 / 99` 총기획 Coverage
5. 분야별 Approval Bundle과 Decision 상태
6. 벤치마크·플레이어·현업 Evidence
7. 시스템·콘텐츠·세계·표현·제작 간 정합성 판정
8. 갱신된 책임 원본과 소비자 전파 상태
9. 구현 인계 패키지
10. 미결정·보류·미검증·위험·다음 Gate
11. 총기획 완료 후 적대적 검수 보고

### `[검수]` 필수 산출물

1. 검수 기준 Branch·Commit·정본·실제 구현
2. 검수 범위 지도와 미검증 범위
3. `[핵심 내용]` 보존 판정
4. 총기획 Coverage Matrix
5. 정본·Decision·구현·Sheet·파생본 비교
6. Finding Ledger
7. `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER`
8. `REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY`
9. 승인된 경우 실제 반영한 최소 수정
10. 정적·런타임·접근성·성능·회귀 결과
11. 최종 판정·남은 위험·다음 조건

---

## 27. 완료 Gate

### `[총기획]` 완료 조건

- `[핵심 내용]`의 모든 요구가 추적됨
- 프로젝트 코어·플레이어 약속·뾰족한 재미가 명확함
- 필요한 총기획 영역이 `CONFIRMED / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 판정됨
- 시스템·콘텐츠·세계·표현·제작 간 충돌이 처리됨
- 승인 Decision이 책임 원본에 반영됨
- 영향 소비자와 구형 참조가 감사됨
- 구현 인계에 범위·완료 기준·검증·롤백이 있음
- 실행하지 않은 검증이 명시됨
- 적대적 검수 후 차단 finding이 없음

최종 상태:

- `TOTAL_PLANNING_APPROVED`
- `TOTAL_PLANNING_APPROVED_WITH_DEFERRED_ITEMS`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- `REVISE`

### `[검수]` 완료 조건

- 정확한 기준 Branch·Commit·정본·diff가 있음
- 전체라고 주장한 범위의 실제 인벤토리 증거가 있음
- 공격 finding이 재검증됨
- 사용자 결정과 기술 오류가 분리됨
- 승인되지 않은 수정이 없음
- 수정 후 회귀 재검사가 있음
- 실행하지 않은 테스트·런타임·사람 검수가 명시됨
- 남은 위험과 재개 조건이 있음

최종 상태:

- `NO_CONFLICT`
- `CONFLICT_FIXED`
- `MUST_FIX_REMAINS`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- `REVIEW_ONLY_COMPLETE`

---

## 28. GitHub 작업 경계

파일 변경이 필요한 경우:

```text
최신 main 확인
→ 별도 branch 또는 worktree
→ 변경 전 기준 SHA 기록
→ 최소 변경
→ 관련 테스트·검증
→ 적대적 재검토
→ Draft PR
→ exact HEAD 재검증
```

- `main` 직접 push, force push, 기존 사용자 변경 덮어쓰기를 하지 않는다.
- PR 설명에는 목표·범위·보호 대상·변경 파일·검증·미검증·롤백을 기록한다.
- Required Check와 unresolved thread를 확인한다.
- 과거 HEAD의 테스트 통과를 현재 HEAD의 통과로 사용하지 않는다.
- 사용자가 병합까지 명시하지 않았다면 Draft PR 전달에서 멈춘다.

---

## 29. 최종 보고 형식

```md
# 작업 결과

## 실행 모드
- `[총기획]` 또는 `[검수]`
- Work Mode 전환
- 사용한 Skill·Skill Mode와 선택 이유

## 기준선
- Base main SHA
- Project main SHA
- 작업 Branch·HEAD
- 열린·최근 PR
- 책임 원본·실제 구현·Sheet 상태

## `[핵심 내용]` 추적 결과

## `[총기획]` Coverage 또는 `[검수]` Scope

## 벤치마크·근거와 적용 판정

## 적대적 검토 Finding

## 변경한 정본·문서·구현·소비자

## 검증 결과
- PASS
- FAIL
- NOT_RUN
- NOT_APPLICABLE
- BLOCKED_UNVERIFIED

## 보호한 기존 결정·자산·정상 경로

## 미결정·보류·남은 위험·롤백

## 최종 판정과 다음 Gate
```

---

## 30. 실패 조건

다음 중 하나라도 해당하면 완료가 아니다.

- 프로젝트 환경과 정본을 읽기 전에 새 기획을 발명함
- 저장소에서 확인할 수 있는 사실을 사용자에게 반복 질문함
- `[핵심 내용]`을 축약하며 목적을 약화함
- 기능 목록은 많지만 프로젝트 코어·플레이어 약속이 없음
- 총기획 영역 간 연결을 확인하지 않음
- 성공 사례만 벤치마킹함
- AI 추론을 공식 사실로 사용함
- 초기 시험값을 확정 수치로 기록함
- 검수에서 비판을 만들기 위해 장점을 억지로 부정함
- 비판의 사실성과 영향을 재검증하지 않음
- 사용자 승인 없이 주요 기획을 수정함
- 변경 파일만 보고 untouched 소비자·테스트·파생본을 확인하지 않음
- 구형 파일명만으로 삭제함
- Sheet·PDF·Dashboard를 GitHub 정본이나 실제 구현으로 오인함
- 실행하지 않은 테스트·런타임·플레이테스트를 통과로 보고함
- 현재 HEAD가 아닌 과거 증거로 완료를 주장함
- 남은 위험·미검증·롤백 없이 완료를 선언함
