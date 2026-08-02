---
contract_name: PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION
contract_version: "2.0"
status: ACTIVE_PROJECT_PLANNING_AND_REVIEW_PROMPT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
usage: "Base와 대상 프로젝트의 현행 작업환경을 복원한 뒤 [총기획] 또는 [검수]를 실행하는 단일 첨부 작업지시문"
modes:
  - TOTAL_PLANNING
  - REVIEW
default_review_authority: READ_ONLY
specialized_prompt:
  vertical_slice_implementation: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
core_gates:
  - PROJECT_ENVIRONMENT_FIRST
  - CORE_CONTENT_TRACEABILITY
  - GRILL_ME_DECISION_GATE
  - NEUTRAL_RECOMMENDATION_GATE
  - ADVERSARIAL_REVIEW_LIFECYCLE
  - PR_CHECK_EXACT_HEAD
  - EVIDENCE_BEFORE_COMPLETION
---

# 프로젝트 `[총기획]`·`[검수]` 통합 작업지시문 v2

## 0. 입력

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

### `[핵심 내용]`

```text
[핵심 내용]
프로젝트의 목적, 현재 확정 방향, 반드시 포함할 경험·기능·콘텐츠,
금지·제외 사항, 원하는 결과물과 완료 조건을 원문 그대로 붙여 넣는다.
```

`[핵심 내용]`은 요약·정리 중 삭제하거나 약화할 수 없는 보호 입력이다.

| 원문 요구 | 책임 원본·실제 대상 | 총기획·검수 항목 | 검증 | 상태 |
|---|---|---|---|---|
|  |  |  |  | `PENDING` |

허용 상태:

`CONFIRMED / IMPLEMENTED / VALIDATED / DEFERRED_WITH_REASON / OUT_OF_SCOPE_CONFIRMED / USER_DECISION_REQUIRED / BLOCKED_UNVERIFIED`

모든 핵심 요구가 위 상태 중 하나로 닫히지 않으면 완료가 아니다.

---

## 1. 책임과 권한

### `[총기획]`

프로젝트의 기존 결정·정본·실제 구현을 복원하고, 전체 기획을 누락 없이 통합해 실행 가능한 GDD와 구현 인계 계약을 만든다.

### `[검수]`

총기획·분야별 정본·실제 구현을 대조해 왜곡·누락·충돌·중복·구형 참조·실현 불가능성·회귀 위험을 판정한다.

기본 검수 권한은 `READ_ONLY`다. 사용자가 수정까지 요청했거나 finding을 승인한 경우에만 최소 수정하고 다시 검수한다.

### 권한 순서

```text
최신 사용자 지시·승인
→ 프로젝트 AGENTS.md·보안·엔진·데이터 규칙
→ 현재 Decision·Active Context·승인 작업 계약
→ 등록된 기획 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트가 채택한 Base 계약
→ Base 최신 main의 현행 운영 정본·Skill Registry
→ 이 Prompt
→ 외부 사례·과거 대화·초안·AI 추론
```

외부 근거는 개선 가설이지 프로젝트 요구나 구현 사실의 정본이 아니다.

---

## 2. 작업환경 우선 복원

기획·검수 전에 반드시 현재 환경과 권한 구조를 확인한다.

### Base

```text
최신 main SHA·열린/최근 PR
→ START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md
→ skills/SKILL_REGISTRY.json
→ 필요한 최소 Skill·Reference·Template·Test
```

### 프로젝트

```text
최신 main SHA·현재 Branch·열린/최근 PR·Issue
→ 프로젝트 AGENTS.md·START_HERE
→ ACTIVE_CONTEXT·CURRENT_CONFIRMED_DECISIONS
→ DOCUMENTATION_MAP·DESIGN_DOCUMENT_REGISTRY
→ 현재 GDD·분야별 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 구성된 Google Sheet
→ PDF·DOCX·Dashboard·Manifest
```

`전부 살펴본다`는 모든 파일·Skill을 무차별 로드한다는 뜻이 아니다. 책임 지도와 Registry로 현재 작업의 정본·소비자·영향 범위를 만들고, 새 연결이 발견될 때만 확장한다.

### Baseline Recovery Record

```yaml
base_main_sha:
project_main_sha:
current_branch_and_head:
related_open_and_recent_prs:
canonical_sources:
current_decisions:
actual_implementation_state:
sheet_state:
protected_scope:
tools_versions_permissions:
validation_commands:
required_checks:
rollback:
unverified:
```

확인하지 못한 항목은 `NOT_AVAILABLE / NOT_RUN / BLOCKED_UNVERIFIED`로 기록한다.

---

## 3. Work Mode·Skill·Superpowers

### Work Mode

- `TOTAL_PLANNING`: `PLAN → 기획 정본 BUILD → REVIEW`
- `REVIEW`: `REVIEW → 승인 finding만 BUILD → REVIEW`
- `AUTO`: 새 기획·통합이면 `TOTAL_PLANNING`, 결과 판정이면 `REVIEW`, 둘 다면 순차 실행

제품 코드·Scene·데이터 구현은 별도 요청이 없으면 총기획 범위 밖이다.

### 최소 Base Skill

공통:

- `managing-project-intake-and-work-contract`
- `running-adversarial-review-and-refinement`
- `reviewing-and-validating-project-changes`
- 필요 시 `auditing-canonical-reference-freshness`
- 종료 시 `maintaining-project-context-and-handoff`

총기획 분야 후보:

- `identifying-project-core`
- `establishing-project-core`
- `analyzing-and-refining-game-concepts`
- `managing-design-documents`
- `designing-vertical-slices`
- `auditing-and-refining-ui-art`

현재 단계의 주 책임 분야 Skill은 최대 하나다.

### Superpowers

실제 제공되는 경우 다음 순서로 사용한다.

```text
using-superpowers
→ creative/design 전 brainstorming
→ 다단계 작업 전 writing-plans
→ 구현 수정 시 test-driven-development
→ 실패 원인 조사 시 systematic-debugging
→ 완료 주장 전 verification-before-completion
→ 주요 결과·PR 완료 전 requesting-code-review
```

외부 Skill을 Base Registry에 중복 생성하지 않는다.

---

## 4. 공통 선행 감사

모든 L1 이상 총기획·검수 전에 다음을 비교한다.

```text
최신 main
→ 현재 Decision
→ 분야 책임 원본
→ 동일 Goal의 열린·최근 병합 PR
→ 실제 구현
→ 구성된 Sheet
→ 생성·발행본
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

차단 finding이 있으면 새 기획보다 복원·충돌 해소·재동기화를 먼저 수행한다.

---

## 5. Grill Me 핵심 결정 Gate

`Grill Me`는 독립 Skill이 아니라 `managing-project-intake-and-work-contract: clarify`의 핵심 결정 인터뷰다.

사용 조건:

- 프로젝트 코어·플레이어 판타지·Core Loop
- 뾰족한 재미 우선순위
- 충돌하는 시스템·UX·콘텐츠 원칙
- MVP·데모·본제작 범위
- 실패·복구·보상 의미
- 차별화·가장 위험한 가설
- GPT·Codex·개발팀 책임 경계
- 기존 승인 정본의 대체

### 질문 전 검사

```text
main HEAD
→ 동일 Goal Issue·PR·Branch
→ 최근 병합·후속·대체 PR
→ AGENTS·START_HERE·ACTIVE_CONTEXT
→ CURRENT_CONFIRMED_DECISIONS
→ 관련 책임 원본
→ 실제 구현
→ Sheet Decision
→ 현재 대화
→ 질문 필요성
```

다음은 묻지 않는다.

- 저장소나 정본에서 확인 가능한 사실
- 이미 승인된 동일 결정
- 대체·기각·보류된 안
- 구현 세부와 초기 시험값
- 동일 Goal PR에서 처리 중인 결정
- 이전 승인 건이 아직 동기화되지 않은 상태

문구가 달라도 결정 대상과 영향이 같으면 `DUPLICATE_QUESTION`이다.

### 질문 방식

- 한 번에 하나의 차단 결정만 묻는다.
- 선택지·장단점·프로젝트 영향·GPT 권장안을 제공한다.
- 사용자안과 AI안을 동일 기준으로 검토한다.
- 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 반복 질문하지 않는다.

```md
## Grill Me — <Decision ID>

### 기존 정본 비교
- 기존 Decision:
- 책임 원본:
- main HEAD:
- 관련 PR:
- Sheet 상태:

### 질문
<하나의 핵심 결정>

### 선택지
#### A
- 장점:
- 단점:
- 영향:

#### B
- 장점:
- 단점:
- 영향:

### GPT 권장안
<근거·반증·제작 가능성을 비교한 결론>

### 확정 영향
<갱신할 정본·시스템·범위·후속 작업>

### 답변
A / B / 직접 수정안 / 권장안대로
```

### 답변 후 동기화

```text
Decision 상태 판정
→ 기존 Issue·PR conversation에 기록
→ CURRENT_CONFIRMED_DECISIONS 갱신
→ 분야 정본·Approval Bundle 갱신
→ 필요 시 ACTIVE_CONTEXT·Plan 갱신
→ Commit·main/PR 상태 확인
→ 구성된 Sheet 동기화
→ 정본·Commit·Sheet 재조회
→ SYNCED 판정
→ 다음 질문 재평가
```

사용자 승인 전 GPT 제안은 확정 Decision이 아니다.

---

# PART A. `[총기획]`

## 6. 총기획 목표

총기획은 문서 분량을 늘리는 작업이 아니라 다음을 증명하는 작업이다.

1. 누구에게 어떤 경험을 약속하는가.
2. 반복 원동력과 뾰족한 재미가 무엇인가.
3. 시스템·콘텐츠·세계·표현이 같은 방향을 지지하는가.
4. 제작 가능한 범위와 순서인가.
5. 구현·검증에 필요한 정본과 수용 기준이 있는가.
6. 기존 결정·구현·자산이 보존됐는가.

## 7. 총기획 실행 루프

```text
BASELINE_RECOVERY
→ CORE_AND_PROMISE
→ GRILL_ME_DECISIONS
→ BENCHMARK_AND_EVIDENCE
→ TOTAL_PLANNING_COVERAGE
→ CROSS_SYSTEM_COHERENCE
→ APPROVAL_BUNDLES
→ CANONICAL_UPDATE
→ IMPLEMENTATION_HANDOFF
→ ADVERSARIAL_REVIEW
→ GATE_CLOSE
```

## 8. 프로젝트 코어

```yaml
one_line_pitch:
target_player_and_context:
genre_platform_engine:
player_promise:
project_core:
non_negotiable_strengths:
pointed_fun:
core_loop:
session_loop:
meta_loop:
key_choices:
success_failure_recovery:
target_emotion_and_game_feel:
differentiation:
scope_boundary:
```

이미 존재하는 코어는 새로 발명하지 않고 정본·구현·사용자 결정에서 복원한다.

### 중립성 Gate

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

사용자안이 가장 강하면 근거와 함께 동의하고, 다른 안이 강하면 차이를 만드는 근거를 제시한다. 반대를 위한 반대는 금지한다.

## 9. 벤치마킹과 근거

조사 전에 현재 결정을 바꿀 질문을 고정한다.

출처 우선순위:

1. 공식 제품·엔진·플랫폼 문서
2. 개발자 발표·사후 분석·기술 자료
3. 실제 플레이·텔레메트리·퍼널
4. 플레이어 리뷰·인터뷰·커뮤니티
5. 전문 종합 자료
6. AI 추론

규칙:

- 성공·실패·혼합 사례를 함께 본다.
- 제품 사실·행동·자기보고·해석을 분리한다.
- 패치·플랫폼·표본·플레이타임 차이를 기록한다.
- 인기 기능을 복사하지 않는다.
- `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 판정한다.
- 외부 근거가 프로젝트 코어보다 높은 권한을 갖지 않는다.

| Evidence ID | 결정 질문 | 사실·반응 | 적용 조건·한계 | 판정 | 후속 검증 |
|---|---|---|---|---|---|

## 10. 총기획 Coverage

필요한 항목을 `CONFIRMED / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 판정한다.

### `00 프로젝트 기반`

- 저장소·엔진·플랫폼·Stage
- 현재 Decision·GDD·정본
- 실제 구현 상태
- 열린 PR·Issue·Plan
- 보호 결정·자산·경로
- Sheet·발행 상태
- 위험·차단 finding·다음 Gate

### `10 제품·경험`

- 타깃 플레이어·플레이 상황
- 플레이어 약속·제품 방향
- 핵심 컨셉·뾰족한 재미
- Core·Session·Meta Loop
- 조작·선택·승패·복구
- 온보딩·난이도·보상
- 게임 필·피드백·가독성
- 접근성 기본 방향
- 스토어 약속과 실제 경험

### `20 시스템·콘텐츠`

- 전체 시스템 관계
- 메인 규칙·상태·입력·출력
- 성장·경제·강화·자원
- 콘텐츠·레벨·미션 구조
- 적·AI·난이도
- 아이템·장비·스킬·캐릭터
- 실패·복구·저장·호환성
- 수치·공식·단위·시험값
- 데모·Vertical Slice·본제작 범위

### `30 세계·서사`

해당 프로젝트에 필요한 범위만 적용한다.

- 세계 규칙·금기·장소·세력
- 주요인물·조연·관계
- 플레이어 역할·동기
- 사건·정보 공개·콘텐츠 흐름
- 시스템과 서사의 연결
- 톤·문체·용어·명명
- 모순·연속성·스포일러

### `40 표현·UX`

- 사용자 흐름·화면 구조
- HUD·메뉴·상태 전달
- 입력·포커스·취소·오류 복구
- 아트·카메라·이펙트·애니메이션
- 사운드·음악·정보 전달
- 접근성 대체 채널
- 승인 이미지·레퍼런스·라이선스
- 기획 이미지와 실제 엔진 화면 구분

### `50 제작·기술·검증`

- 기술 구조·책임 경계
- 데이터·ID·Schema·저장·마이그레이션
- 엔진·플러그인·서비스·라이선스
- 제작 파이프라인·반복 제작성
- 마일스톤·의존성·Approval Bundle
- Vertical Slice 목표 품질
- 테스트·QA·회귀·플레이테스트
- 접근성·성능 예산
- 텔레메트리·피드백
- 배포·출시·운영·사업
- 위험·대안·중단 조건·롤백
- Codex·개발팀 인계

### `99 변경·학습`

- Decision 추가·대체·기각·보류
- Evidence와 변경 이유
- 반영 Commit
- 실패·회귀·복구
- 프로젝트 Skill·Base 환류 후보
- 재검토 조건

## 11. 기획 항목 최소 계약

```yaml
module_id:
problem_or_player_question:
current_decision:
player_value_and_core_relation:
evidence_ids:
alternatives_and_recommendation:
user_decision_status:
rules_inputs_outputs_feedback:
dependencies_and_affected_systems:
failure_recovery_edge_cases:
initial_values_and_tuning_range:
implementation_scope_and_exclusions:
canonical_source_and_consumers:
acceptance_criteria:
validation:
implementation_status:
validation_status:
unknowns_and_revisit_trigger:
```

정본에 없는 수치는 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 표시한다.

## 12. 분야 간 정합성

반드시 대조한다.

- 플레이어 약속 ↔ 핵심 루프
- 핵심 루프 ↔ 보상·성장·경제
- 시스템 ↔ 콘텐츠 제작량
- 세계·서사 ↔ 플레이 규칙
- UX ↔ 상태·입력
- 아트·사운드 ↔ 정보 전달·게임 필
- 접근성 ↔ 정보·입력·시간
- 저장·데이터 ↔ 성장·업데이트
- Vertical Slice ↔ 대표 경험·제작 파이프라인
- 출시 약속 ↔ 범위·품질·운영 능력

판정:

`MUST_RESOLVE / USER_DECISION_REQUIRED / TEST_IN_VERTICAL_SLICE / DEFERRED_WITH_BOUNDARY / NO_CONFLICT`

## 13. Approval Bundle·정본화

```yaml
bundle_id:
discipline_and_goal:
current_and_changed_decisions:
evidence_ids:
alternatives_and_recommendation:
user_decisions_required:
dependencies:
affected_canonical_sources:
affected_consumers:
implementation_handoff:
validation_gate:
rollback:
```

승인된 내용만 `CURRENT_CONFIRMED_DECISIONS`, `ACTIVE_CONTEXT`, 분야 GDD, Registry, Issue·Plan, 구성된 Sheet와 필요한 발행본에 반영한다.

한 질문에 활성 정본은 하나만 둔다. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.

정본 변경 후 START_HERE·Map·Registry·Template·Schema·Test·Workflow·PDF·Sheet·Manifest와 구형 참조를 확인한다. 누락 소비자가 있으면 `MISSING_CONSUMER`다.

## 14. 구현 인계

총기획의 기본 종료점은 구현 자체가 아니라 실행 가능한 인계다.

```yaml
implementation_goal:
approved_decisions_and_sources:
player_visible_outcome:
in_scope:
out_of_scope:
protected_scope:
expected_files_and_systems:
data_and_state_ownership:
dependencies_and_order:
acceptance_criteria:
normal_failure_edge_regression:
runtime_platform_accessibility_performance:
documentation_and_consumers:
rollback:
open_decisions:
blocked_unverified:
```

복잡한 작업은 `Issue → Plan → 구현 패키지 → 검증 Gate`로 나눈다.

---

# PART B. `[검수]`

## 15. 검수 목표·권한

검수는 문장 윤문이 아니라 다음을 판정한다.

- `[핵심 내용]`과 Decision 보존
- 총기획 Coverage와 분야 연결
- 정본 간 충돌
- 기획과 실제 구현 일치
- 구형 경로·ID·용어
- 제작·기술·콘텐츠 실현 가능성
- UX·접근성·성능·운영 위험
- 근거 없는 완료 상태

기본:

```yaml
review_fix_authority: READ_ONLY
```

수정은 사용자가 함께 요청했거나 승인한 finding만 허용한다. 수정 뒤 반드시 REVIEW로 돌아온다.

## 16. 적대적 검토 생명주기

```text
REVIEW_SCOPE_MAP
→ BASELINE_RECOVERY
→ CONTRACT_AND_CORE_CHECK
→ COVERAGE_AND_CANON_CHECK
→ IMPLEMENTATION_ALIGNMENT
→ attack
→ validate-critique
→ finding decision
→ 승인 finding만 분야 Skill BUILD
→ regression-recheck
→ decision-report
```

공격과 비판 검증을 분리한다. 사용자안과 AI 최초안을 동일 기준으로 공격한다. 유효한 장점을 억지로 부정하지 않는다.

### 검수 관점

1. 목적·코어 보존
2. 총기획 범위·누락
3. 정본·Decision·Sheet·파생본
4. 시스템·수치·경제·악용·복구
5. 세계·서사·콘텐츠 연속성
6. UX·UI·아트·사운드·접근성
7. 제작·기술·성능·운영 가능성
8. 벤치마크·근거 품질
9. 기획과 실제 구현·테스트 정렬
10. 구형 참조·untouched 소비자·고아 파일

각 관점을 `APPLIED / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 기록한다.

## 17. Finding Ledger

판정:

- `MUST_FIX`
- `SHOULD_FIX`
- `USER_DECISION_REQUIRED`
- `DEFER`
- `REJECTED_CRITIQUE`
- `BLOCKED_UNVERIFIED`
- `ALLOWED_LEGACY`

| ID | 심각도 | 관점 | 위치 | 증거 | 영향 | 판정 | 수정 방향 | 검증 |
|---|---|---|---|---|---|---|---|---|

비판의 사실성·발생 가능성·영향·범위·수정 비용을 재검증한다.

승인된 `MUST_FIX`와 `SHOULD_FIX`만 최소 수정한다. 사용자 결정 항목은 몰래 확정하지 않는다.

## 18. 검증 계층

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

상태:

`PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED_UNVERIFIED`

한 계층의 통과를 다른 계층의 통과로 확장하지 않는다.

- 문서 검사 ≠ 런타임 검증
- 이미지 존재 ≠ UI 구현·접근성 검증
- 테스트 통과 ≠ 재미 검증
- Evidence 작성 ≠ 시장성·출시 준비 검증

---

## 19. PR_CHECK exact-HEAD Gate

`PR_CHECK`는 PR 존재 확인이 아니라 승인 계약과 정확한 HEAD가 통합 가능한지 판정하는 독립 Gate다.

### PR 전

```text
최신 main·동일 Goal PR 재조회
→ 별도 Branch/worktree
→ 기준 main SHA·HEAD 기록
→ 승인 범위·예상 파일 확정
→ 최소 변경
→ 관련 검증
→ attack → validate-critique
→ Draft PR
```

### PR 검사 순서

```text
PR metadata·base·head
→ exact HEAD SHA
→ 전체 changed-file inventory·diff
→ 승인 계약·정본·실제 변경 대조
→ 범위 밖·보호 경로·커밋 구성
→ Required Check·Actions
→ review·unresolved thread
→ 최신 main·behind·mergeability
→ Ruleset·branch protection·merge 방식
→ PR 적대적 재검토
→ 최종 판정
```

필수 확인:

- 검수한 HEAD와 현재 HEAD가 같은가.
- 모든 changed file의 필요성이 설명되는가.
- 변경됐어야 하지만 untouched인 소비자·테스트·파생본은 없는가.
- CI가 exact HEAD에서 실행됐는가.
- 실패·취소·skip·미실행을 성공으로 오인하지 않았는가.
- unresolved review thread가 0인가.
- 사용자 결정·차단 finding이 남지 않았는가.
- 최신 main 기준 검증인가.
- Required Check 이름과 실제 check run이 일치하는가.
- 롤백이 유효한가.

### HEAD 변경

```text
new HEAD
→ diff 재조회
→ 계약·정본·소비자 재대조
→ 필요한 테스트·Actions 재실행
→ thread 재확인
→ regression-recheck
→ 새 exact-HEAD 판정
```

과거 HEAD의 테스트·리뷰·승인을 현재 HEAD 증거로 사용하지 않는다.

### PR 상태

- `PR_DRAFT_IN_PROGRESS`
- `PR_REVISE`
- `PR_USER_DECISION_REQUIRED`
- `PR_BLOCKED_UNVERIFIED`
- `PR_CHECKS_FAILED`
- `PR_REVIEW_THREADS_OPEN`
- `PR_APPROVED_EXACT_HEAD`
- `AUTO_MERGE_ELIGIBLE`
- `MERGE_NOT_REQUESTED`

병합 가능 조건:

- Draft가 아님
- exact HEAD 일치
- 승인 범위와 diff 일치
- Required Check 성공
- unresolved thread 0
- 차단 finding·사용자 결정 없음
- 최신 main 기준 검증
- Ruleset·merge 방식 확인
- `regression-recheck → decision-report` 완료

사용자가 작업지시문과 Draft PR만 요청했으면 `MERGE_NOT_REQUESTED`로 멈춘다.

---

## 20. 필수 산출물

### `[총기획]`

1. Baseline Recovery Record
2. `[핵심 내용]` 추적표
3. 프로젝트 코어·플레이어 약속
4. `00 / 10 / 20 / 30 / 40 / 50 / 99` Coverage
5. Grill Me Decision·Approval Bundle
6. 벤치마크·플레이어·현업 Evidence
7. 분야 간 정합성 판정
8. 갱신 정본·소비자 전파
9. 구현 인계
10. 미결정·미검증·위험
11. 적대적 검수 보고
12. 변경이 있으면 PR_CHECK

### `[검수]`

1. 기준 Branch·Commit·정본·실제 구현
2. 검수 범위와 미검증 범위
3. `[핵심 내용]` 보존 판정
4. Coverage Matrix
5. 정본·Decision·구현·Sheet·파생본 비교
6. Finding Ledger
7. 승인된 최소 수정
8. 정적·런타임·접근성·성능·회귀 결과
9. PR_CHECK
10. 최종 판정·위험·다음 조건

---

## 21. 완료 Gate

### 총기획

- 모든 핵심 요구 추적
- 코어·플레이어 약속·뾰족한 재미 확정 또는 미결정 표시
- 필요한 Coverage 판정
- 분야 충돌 처리
- Grill Me 승인 Decision 동기화
- 정본·소비자·구형 참조 감사
- 구현 인계에 범위·검증·롤백 존재
- 적대적 검토 후 차단 finding 없음
- 변경 PR의 exact-HEAD Check 완료

판정:

`TOTAL_PLANNING_APPROVED / TOTAL_PLANNING_APPROVED_WITH_DEFERRED_ITEMS / USER_DECISION_REQUIRED / BLOCKED_UNVERIFIED / REVISE`

### 검수

- 정확한 Branch·Commit·diff
- 전체라고 주장한 범위의 실제 인벤토리
- 공격 finding 재검증
- 사용자 결정과 기술 오류 분리
- 승인되지 않은 수정 없음
- 수정 후 회귀 재검사
- 실행하지 않은 검증 명시
- PR exact-HEAD 상태 명시
- 위험·재개 조건 존재

판정:

`NO_CONFLICT / CONFLICT_FIXED / MUST_FIX_REMAINS / USER_DECISION_REQUIRED / BLOCKED_UNVERIFIED / REVIEW_ONLY_COMPLETE`

---

## 22. 최종 보고

```md
# 작업 결과

## 실행 모드·사용 Skill
## Base·프로젝트 기준선
## `[핵심 내용]` 추적
## Grill Me Decision과 동기화
## 총기획 Coverage 또는 검수 Scope
## 벤치마크·근거
## 적대적 검토 Finding
## 변경한 정본·문서·구현·소비자
## 검증: PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED_UNVERIFIED
## PR_CHECK exact HEAD·Checks·Threads·Merge 판정
## 보호한 결정·자산·정상 경로
## 미결정·보류·위험·롤백
## 최종 판정·다음 Gate
```

---

## 23. 실패 조건

- 환경·정본 확인 전 새 기획 발명
- 저장소 사실을 사용자에게 반복 질문
- `[핵심 내용]` 약화
- 프로젝트 코어 없이 기능 목록만 확장
- 총기획 분야 연결 미검사
- 성공 사례만 벤치마킹
- AI 추론을 공식 사실로 사용
- 시험값을 확정값으로 기록
- Grill Me 중복 질문·다중 질문·승인 미동기화
- 반대를 위한 적대 검토
- 비판의 사실성·영향 미검증
- 사용자 승인 없는 주요 기획 수정
- changed file만 보고 untouched 소비자 누락
- 구형 파일명만으로 삭제
- Sheet·PDF·Dashboard를 정본·구현으로 오인
- 실행하지 않은 검증을 PASS로 보고
- 과거 HEAD 증거로 현재 PR 승인
- unresolved thread·Required Check 실패를 무시
- 위험·미검증·롤백 없이 완료 선언
