# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. 용어

### Work Mode

요청을 처리하는 동안 AI의 **주된 작업 자세·권한·증거 기준**을 정한다. 대화 전체에 영구 고정되는 성격이 아니라 현재 작업 단계의 운영 상태다.

| Work Mode | 핵심 목적 | 기본 행동 |
|---|---|---|
| `PLAN` | 의도·요구·근거·설계·순서 확정 | GPT가 조사·정본 복원·대안 비교·Acceptance·구현 준비를 닫음 |
| `BUILD` | 승인된 계약의 실제 구현 | Codex가 current GitHub+Notion을 재수화하고 code/data/Scene/Resource/test/runtime을 변경 |
| `REVIEW` | 결과를 적대적으로 검토·검증·판정 | GPT가 기획 일치·증거·회귀·누락을 공격하고 다음 경로를 판정 |

복합 작업은 `PLAN → BUILD → REVIEW`처럼 순차 전환할 수 있다. 한 시점에는 주 Work Mode 하나만 둔다.

### Skill

특정 책임을 반복 수행하는 전문 작업 계약이다. trigger, 입력, 절차, 산출물, 실패 조건과 검증을 가진다.

예: `managing-game-project-operating-system`, `reviewing-and-validating-project-changes`.

### Skill Mode

한 Skill 내부에서 현재 필요한 세부 절차·권한을 선택한다. 문서에서 별도 수식어 없이 Skill 안에 적힌 `mode`는 Skill Mode를 뜻한다.

### Grill Me

Grill Me는 독립 Skill ID가 아니라 `managing-project-intake-and-work-contract`의 `clarify` Skill Mode에서 실행하는 핵심 의사결정 인터뷰 프로토콜이다.

- 저장소·Notion에서 답할 수 있는 사실을 다시 묻지 않는다.
- 프로젝트 방향을 바꾸는 사용자 결정만 한 번에 하나씩 묻는다.
- 선택지·장단점·GPT 권장안·확정 영향을 제공한다.
- 답변을 결정 원장과 책임 원본에 반영한다.
- 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 권장안으로 확정하고 질문을 계속 늘리지 않는다.

Reference: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`

### Prompt

현재 사용자가 원하는 구체적인 목표·제약·산출물이다. Prompt가 Work Mode·Skill·Skill Mode를 직접 선언할 필요는 없다.

### Continuous Work

`[연속작업] 진행해`는 현재 승인된 작업 계약의 남은 범위를 중간 승인 대기로 끊지 않고 연속 수행하라는 **명시적 opt-in 실행 flag**다.

- 상태: `CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE`
- Work Mode를 대체하지 않는다.
- 새 Skill이나 장기 권한이 아니다.
- 트리거가 없는 요청은 `CONTINUOUS_WORK_INACTIVE`다.
- blocker/종료 판정은 `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`의 recovery ladder와 Global Progress Queue를 따른다.

## 2. GPT ↔ Codex 역할 분리 라우팅

공용 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

```text
GPT PLAN
→ GitHub + Notion current canon 복원
→ 조사·벤치마킹·대안 비교
→ 기획·Flow·UI/UX·데이터·시각 요구 설계
→ 적대적 검토·IRG
→ 필요한 이미지가 있으면 GPT visual pipeline
→ Notion 승인 Visual upload/attach/readback
→ IMPLEMENTATION_READY

구현/코딩 없음
→ GPT REVIEW / canon readback / 종료

구현/코딩 있음
→ CODEX_IMPLEMENTATION_HANDOFF
→ Codex CODEX_REHYDRATE_GITHUB_AND_NOTION
→ 필요 시 CODEX_PREFLIGHT_OPTIONAL
→ Codex BUILD
→ actual test/runtime/play evidence
→ GPT REVIEW
→ 승인/수정/기획반환/Visual반환
```

핵심 불변식:

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_PREFLIGHT_OPTIONAL
```

과거 `GPT 평상시 Godot 구현 보조·POC → 기획·구현·POC 누적 → USER_REQUESTED_CODEX_HANDOFF`는 **SUPERSEDED_FLOW_COMPATIBILITY_LITERAL**이다. current workflow로 재활성화하지 않는다.

`ON_DEMAND_CODEX_HANDOFF`와 `USER_REQUESTED_CODEX_HANDOFF`는 사용자가 명시적으로 Codex 인계를 요청하는 경우의 호환 trigger로 남을 수 있지만, **정상 구현 전환의 필수 조건은 아니다.** `IMPLEMENTATION_READY + 실제 BUILD task 존재`가 기본 인계 조건이다.

## 3. 자동 실행 순서

```text
사용자 Prompt
→ 의도·현재 단계·위험 파악
→ Project/Base/Notion/GitHub 권위 복원
→ 주 Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 필요한 최소 Skill 자동 선택
→ 각 Skill의 Skill Mode 자동 선택
→ [연속작업] 존재 여부와 승인 범위 확인
→ PLAN이면 GPT 수행
→ BUILD가 필요하면 Codex handoff
→ REVIEW는 GPT가 결과·증거 검수
→ CONTINUOUS_WORK_ACTIVE이면 recover/defer/continue
→ readback / 병합 Gate / 다음 Slice
→ 사용 이유·결과·증거 보고
```

사용자가 Skill 이름이나 mode를 지정하면 강한 힌트로 사용하지만 실제 trigger·비사용 조건·권한과 충돌하면 current canon을 우선한다.

## 4. 자동 선택 규칙

- `load_by_default=false`는 자동 선택 금지가 아니라 trigger가 없을 때 불필요하게 읽지 않는다는 뜻이다.
- 사용자가 어떤 Skill을 쓸지 선택하지 않아도 Registry가 자동 라우팅한다.
- 주 책임 분야 Skill은 최대 하나다.
- Foundation·검증·발행·Handoff Skill은 현재 단계에 필요한 것만 추가한다.
- 같은 책임을 여러 Skill로 중복 실행하지 않는다.
- 새 사실·실패·범위 변경·정본 변경이 생기면 다시 라우팅한다.
- Skill 파일을 읽은 것과 실제 절차를 실행한 것을 구분한다.
- 새 독립 Skill보다 기존 통합 Skill의 Skill Mode·reference로 책임을 보존할 수 있는지 먼저 확인한다.
- `[연속작업] 진행해`는 사용자 승인 자체를 새로 만드는 문구가 아니다. 현재 계약의 `CONFIRMED` 또는 `REUSED_APPROVAL` 범위 안에서만 `CONTINUOUS_WORK_ACTIVE`를 부여한다.

## 5. 경량 중립성 Gate와 전체 적대 검토 경계

권장안·판정·설계 선택은 `평가 기준 → 대안 → 반증 → 이익·비용·위험 → 되돌리기 난이도 → 미검증 → 권장 결론` 순서의 경량 중립성 Gate를 사용한다. 이는 **동의 편향**을 막지만 **반대를 위한 반대**를 요구하지 않는다.

- `L0`: 오탈자·명백한 기계 수정·동일 입력 검사 재실행은 전체 적대 검토 Skill을 호출하지 않는다.
- Registry의 `칭찬·균형 평가만 요청` 비사용 조건은 **결정·권장안이 없는 설명형 칭찬·균형 요약**에만 적용한다. 중요한 결정·권장안을 포함한 비교는 이 예외로 적대적 검토를 우회하지 않는다.
- `L1 이상` PLAN 사전판정은 `running-adversarial-review-and-refinement: attack → validate-critique → decision-report`를 적용한다.
- 승인된 finding이 **기획·정본 교정**이면 GPT PLAN/REVIEW owner에서 최소 수정한다.
- 승인된 finding이 **제품 code/data/Scene/Resource/test/runtime 수정**이면 `refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정한다. current role에서 실제 product mutation executor는 Codex이며, GPT가 같은 finding을 다시 직접 구현하지 않는다.
- 수정 뒤 REVIEW의 `regression-recheck → decision-report`로 이동한다. 이미 구현된 finding을 다시 수정하지 않는다.
- 적대적 검토 Skill은 분야 작성/구현 owner를 빼앗지 않는다.
- 최소 full loop count와 clean exit는 latest Base adversarial owner를 따른다.
- 증거가 부족하면 `BLOCKED_UNVERIFIED`와 필요한 확인 조건을 반환한다.

### REVIEW 기본 루트

`REVIEW`는 요청된 파일이나 diff만 수동 확인하는 모드가 아니다. Registry·Documentation Map·정본·참조 관계를 사용해 **변경 파일, 같은 책임의 원본, 활성 소비자, 인접 시스템, 변경됐어야 하지만 untouched인 파일, 테스트·템플릿·파생본**까지 영향 범위를 만든다.

```text
review-scope-map
→ attack
→ validate-critique
→ finding 분류
   ├─ DOC_OR_CANON_CORRECTION → GPT bounded correction
   ├─ IMPLEMENTATION_CORRECTION → CODEX_IMPLEMENTATION_HANDOFF
   ├─ USER_DECISION_REQUIRED
   ├─ BLOCKED_UNVERIFIED
   └─ NO_CHANGE
→ 수정 후 regression-recheck
→ whole-state re-attack
→ evidence-report
```

- 저장소나 도구로 답할 수 있는 사실, 명백한 오류, 참조 누락, 테스트 실패, 표준 위반은 사용자 질문으로 전가하지 않는다.
- 사용자에게 묻는 항목은 둘 이상의 유효한 선택지가 프로젝트 코어, 플레이어 경험, 주요 UX, 콘텐츠 의미, 범위 또는 비용 우선순위를 다르게 만드는 충돌로 제한한다.
- 전체 저장소를 무조건 정독하지 않고 영향 지도를 근거로 범위를 넓힌다.

담당 절차:

- 공격·finding 분류: `running-adversarial-review-and-refinement`
- 실제 diff·정적·런타임·접근성·성능·회귀 증거: `reviewing-and-validating-project-changes`
- 사용자 결정 인터뷰: `managing-project-intake-and-work-contract: clarify`

## 6. 권한 전환

### PLAN — GPT

- 읽기·조사·벤치마킹·기획·계약 작성
- Notion 사람용 기획/Flow/Visual/표 교정
- 이미지 brief·생성·편집·검수와 승인 Visual delivery
- L2+ 마스터 구현계획·패키지/Acceptance/rollback 계약
- 구현 준비 판정과 Codex handoff
- 제품 code/Scene/Resource/runtime 구현은 수행하지 않음

### BUILD — Codex

- 실제 GitHub + relevant Notion 재수화
- 승인 범위 code/data/Scene/Resource/config/test/build/runtime 구현
- 안전한 기술 세부 결정·리팩터링
- 실제 test/runtime evidence
- 프로젝트가 채택한 persistent authoring authority 준수
- 이미지 생성·생성형 편집 금지
- current-use 승인 + Notion attach/readback된 Visual만 소비
- 이미지 부족 시 `GPT_VISUAL_REQUEST`
- 프로젝트 코어·주요 UX·경제·서사·범위 변경 시 `CHANGE_PROPOSAL`

### REVIEW — GPT

- 승인 기획과 실제 diff/Commit/test/runtime 대조
- Notion/GitHub sync와 evidence ceiling 검사
- Codex image-generation 금지 준수 검사
- 승인 Visual provenance/사용처 검사
- 적대적 finding과 회귀 검사
- `PACKAGE_APPROVED | PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES | USER_REVIEW_REQUIRED | CHANGE_PROPOSAL | WAITING_GPT_VISUAL | REVISE | BLOCKED | UNVERIFIED` 판정

## 7. Codex 구현 인계

`CODEX_IMPLEMENTATION_HANDOFF` 최소 입력:

```yaml
handoff_mode: CODEX_IMPLEMENTATION_HANDOFF
trigger: IMPLEMENTATION_READY | USER_REQUESTED_CODEX_HANDOFF | CONTINUOUS_WORK_EXECUTOR_HANDOFF
intent_and_player_outcome:
implementation_ready: true
actual_state_verification_required: true
notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []
github_sources:
  repository:
  agents:
  active_context:
  structured_canon: []
  implementation_paths: []
protected_behavior_and_contracts: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
forbidden_or_high_risk_changes: []
visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST
```

Codex는 handoff를 정본으로 맹신하지 않고 current GitHub+Notion을 다시 읽는다.

### `CODEX_PREFLIGHT_OPTIONAL`

고위험·불확실·다중 의존성에서만 읽기 전용 기술 Plan을 추가한다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

Plan 생략은 rehydration 생략이 아니다.

## 8. Visual 반환 경로

Codex가 별도 image asset 필요성을 발견하면 직접 만들지 않는다.

```yaml
GPT_VISUAL_REQUEST:
  implementation_task:
  why_required:
  player_or_ui_role:
  asset_type:
  target_screen_or_scene:
  required_dimensions_or_ratio:
  transparency_or_format:
  visual_constraints:
  existing_approved_references: []
  notion_destination:
  acceptance_criteria: []
```

```text
WAITING_GPT_VISUAL
→ GPT brief / 사용자 승인 / 생성·편집 / 검수
→ exact Notion Visual/Asset upload + Approved + readback
→ Codex fresh-read
→ BUILD resume
```

독립 구현이 가능하면 Visual 대기 때문에 전체 프로젝트 작업을 멈추지 않는다.

## 9. `[연속작업] 진행해` 권한 전환 루프

`CONTINUOUS_WORK_ACTIVE`에서는 현재 승인된 작업 계약의 실행 순서를 Global Progress Queue로 관리한다.

```text
현재 승인된 작업 계약
→ ready PLAN task → GPT
→ ready BUILD task → CONTINUOUS_WORK_EXECUTOR_HANDOFF → Codex
→ Codex result → GPT REVIEW attack / validate-critique
→ blocker면 RECOVERABLE_VERIFICATION / RECOVERABLE_EXECUTION_ROUTE / LOCAL_TASK / USER_DECISION / HIGH_RISK 분류
→ recoverable이면 재조회·대체 evidence·authorized executor 시도
→ 당장 못 풀리면 해당 task만 deferred
→ 독립 ready task 계속
→ 상태 변화 뒤 deferred 재평가
→ 모든 완료 기준 충족 또는 GLOBAL_TERMINAL_BLOCKER까지 반복
```

- `BLOCKED_UNVERIFIED`는 task/evidence 상태일 수 있으며 그 자체로 전역 종료가 아니다.
- `tool-output truncation`, queued/in-progress CI, 첫 exact-head 조회 실패는 `EVIDENCE_TRANSPORT_INCOMPLETE`로 재조회한다.
- 구현 단계에서 현재 surface에 Codex/executor 실행 경로가 실제 없으면 **실행했다고 주장하지 않는다.** executor-ready handoff/checkpoint를 준비하고 해당 task를 `DEFERRED_EXTERNAL_EXECUTOR`로 둔다.
- `[연속작업] 진행해`는 동일 승인 범위의 `CONTINUOUS_WORK_EXECUTOR_HANDOFF`를 허용하므로 `Codex로 넘길까요?` 같은 재승인을 만들지 않는다.
- **기술적 단일 최소 안전 finding이면 자동 승인**할 수 있다. 여기서 자동 승인은 새 기획 결정을 만드는 것이 아니라, 이미 승인된 범위의 기술 finding을 Codex BUILD queue에 넣는 뜻이다. Codex가 최소 수정한 뒤 GPT가 `regression-recheck`와 whole-state REVIEW를 수행한다.
- 같은 승인 목표의 구현·검증 방법, 테스트 규모 확대, 재조회·재실행, 동작 보존 최소 수정은 새 제품 결과·예산·권한을 만들지 않는 한 `USER_DECISION_REQUIRED`가 아니다.
- 진짜 사용자 결정, 범위 확대, 고위험 외부 행위는 자동 승인하지 않지만 독립 ready task가 있으면 계속한다.
- `GLOBAL_TERMINAL_BLOCKER`는 recovery path를 소진하고, 독립 ready task가 없고, 기존 approval/authorized executor로도 진행할 수 없을 때만 사용한다.

짧은 진행 업데이트는 허용하지만 승인 질문으로 사용하지 않는다. `CONTINUOUS_WORK_ACTIVE`는 현재 응답/실행 orchestration이며 scheduler·webhook·백그라운드 자동 수행을 뜻하지 않는다.

## 10. 구현 패키지와 승인 게이트

L2 이상·다중 의존성 작업은 전체 설계를 마스터 구현계획 하나로 유지하고 구현을 검증 가능한 결과 단위의 패키지로 순차 진행한다. 작은 국소 작업에는 패키지 체계를 형식적으로 강제하지 않는다.

```text
상위 구현 추적 단위
├─ 패키지 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 작업만 병렬화한다.

패키지 종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

담당 Skill: `maintaining-project-context-and-handoff`의 `implementation-package-handoff`.

## 11. 병합

기본 병합 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다. **별도 사용자 병합 승인**은 이미 승인된 동일 범위의 정상 병합에 기본 필수가 아니다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 사용자의 명시적 승인이 완료된 동일 범위는 **추가 확인·재승인·병합 승인 요청 없이** 현재 repository의 실제 merge gate를 통과하면 병합할 수 있다.

`CONTINUOUS_WORK_ACTIVE`는 이 병합 Gate를 삭제하지 않는다. 각 PR은 current exact HEAD·required checks·독립 검토·thread·차단 상태 조건을 그대로 충족해야 한다.

병합 전 확인:

- current reviewed HEAD == current PR HEAD
- current repository required checks PASS
- unresolved review thread 0
- current ruleset / branch protection
- 허용 merge method
- `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `WAITING_GPT_VISUAL`, P0/P1 blocker 없음

특정 check 이름을 공용 문서에서 영구 고정하지 않는다. 다른 독립 open/draft/ready PR은 read-only로 보호한다.

## 12. 필수 실행 보고

L1 이상 작업은 최종 보고에 실제 사용한 항목을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | UNVERIFIED
```

Codex 구현을 사용했다면:

```yaml
codex_result:
  changed_files_and_reasons: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  change_proposals: []
```

`CONTINUOUS_WORK_ACTIVE`였다면 완료한 작업, deferred 작업, recovery, 적대적 finding, 회귀 검증, 최종 종료 상태를 함께 보고한다.

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음`을 기록한다. 모든 Skill을 나열하지 않는다.

## 13. 예시

### 기능 구현

```text
Prompt: 전투 결과 저장 기능을 구현해줘.
GPT PLAN: 저장 책임·Schema·호환성·Acceptance 설계 + 적대적 검토
→ IMPLEMENTATION_READY
→ CODEX_IMPLEMENTATION_HANDOFF
Codex: GitHub + Notion 재수화
→ 필요 시 CODEX_PREFLIGHT_OPTIONAL
→ BUILD 구현·테스트·Commit/PR
GPT REVIEW: 저장·불러오기·경계·회귀·기획 일치 검수
→ merge gate
```

### 연속작업

```text
Prompt: [연속작업] 진행해
→ 현재 승인 계약과 남은 완료 기준 복원
→ ready PLAN은 GPT
→ ready BUILD는 CONTINUOUS_WORK_EXECUTOR_HANDOFF로 Codex
→ CI 결과가 잘리면 EVIDENCE_TRANSPORT_INCOMPLETE 재조회
→ Codex 실행경로가 없으면 해당 BUILD task만 DEFERRED_EXTERNAL_EXECUTOR
→ 다른 ready task 계속
→ 승인 범위 PR은 merge gate 통과 시 별도 병합 승인 없이 병합
→ 모든 recovery가 소진되고 ready task가 없을 때만 GLOBAL_TERMINAL_BLOCKER
```

### 이미지가 필요한 UI 구현

```text
GPT PLAN: 화면 구조·상태·Visual requirement 승인
Codex BUILD: 승인된 Notion Visual로 UI 구현
→ 필요한 portrait 없음
→ GPT_VISUAL_REQUEST
GPT: brief → 사용자 승인 → image 제작/검수 → Notion upload/readback
Codex: 새 Visual fresh-read → UI 구현 재개
GPT REVIEW
```

### GDD 검수

```text
GPT REVIEW: 영향 범위 → 적대적 공격 → 기술 검수안 / 사용자 결정 분리
문서·Notion만 바뀌면 Codex 없이 종료
실제 구현 변경이 필요하면 CODEX_IMPLEMENTATION_HANDOFF
```

### Grill Me

```text
Prompt: Grill Me로 프로젝트 방향을 확실히 정해줘.
GPT PLAN: 저장소·Notion·결정 상태 조사
→ clarify + Grill Me
→ 결정 질문 하나와 권장안
→ 답변을 결정 원장·책임 원본에 반영
→ 차단 질문이 없으면 종료
```

## CLAIM_AND_INTENT_VERIFICATION_GATE

완료·검증·병합 주장 또는 승인 의도와 실제 구현의 일치 판정은 `REVIEW`에서 `reviewing-and-validating-project-changes: claim-and-intent-verification`으로 라우팅한다.

```text
material claim 원자화
→ authority·freshness·counterevidence
→ 승인 Intent·Acceptance와 actual diff 연결
→ exact HEAD 실행 Evidence
→ Completion Claim Gate
→ merge 뒤 post-merge main readback
```

검색 결과·생산자 설명·모델 자신감·테스트 정의·다른 SHA의 PASS는 직접 Evidence가 아니다. 필수 Evidence가 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`를 유지한다.

Reference: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
