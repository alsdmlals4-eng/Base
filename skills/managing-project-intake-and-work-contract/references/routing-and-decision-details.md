# Conditional Routing and Decision Details

새 요청에 실제 설계·정책 선택, 다분야 분해, 모호성, 라우팅 충돌 또는 L2+ 요구의 다중 Task·파일·검증 추적이 필요할 때 읽는다. 단일 분야·해법 확정 작업도 마지막 조건이면 BCP-008 절을 적용한다. 단순 읽기 전용 답변에는 불필요하며, 같은 승인 범위 재개는 기존 추적 Packet과 승인 근거를 재사용한다. 아래 순서와 예시는 intake의 상세 계약이며 별도 승인 owner가 아니다.

## Terminology

- `Work Mode`: AI의 현재 작업 자세·권한·증거 기준. `PLAN / BUILD / REVIEW` 중 한 시점에 하나를 주로 사용한다.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 전문 작업 계약.
- `Skill Mode`: 한 Skill 안에서 선택하는 세부 절차. 이 문서의 `route`, `first-prompt`, `clarify` 등이 해당한다.
- `Prompt`: 사용자의 현재 목표·제약·산출물. Skill 선언문이 아니다.
- `Direction anchor`: 지시문 가장 앞에서 핵심 행동·결과·지배 기준을 고정하는 1~2문장. 배치 순서는 권한을 만들지 않는다.
- `Continuous Work`: 유효한 승인 계약과 `CONTINUATION_INTENT_ALIASES`가 함께 있을 때 `APPROVED_CONTRACT_CONTINUATION`으로 활성화되는 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 상태. Work Mode가 아니라 승인된 계약 안에서 다음 미완료 작업으로 계속 이동하는 orchestration flag다.

상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

승인 결정 복원·중복 질문 방지·Repository/Notion 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

프로젝트 workspace 권위: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` (`DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`, `REPOSITORY_PRIMARY_CANON`, `HUMAN_GDD_PDF_DERIVED_VIEW`, legacy Notion/Google Sheets migration boundary). V3 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`은 `V3_COMPATIBILITY_AND_HISTORY_ONLY`이며 신규 project work route가 아니다.

legacy Google Sheets 해석·이관이 필요한 경우에만 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 compatibility 계약을 참고한다. 이는 신규 입력이나 active workspace 권위를 만들지 않는다. 기존 consumer가 사용하는 legacy literal `project_google_sheet`는 `google_sheet_compatibility_source`의 호환 alias일 뿐이며 신규 Sheet·active sync·정본 권위를 뜻하지 않는다.

연속작업 활성화·자동 승인·blocker recovery·종료 경계: [continuous-work-execution.md](continuous-work-execution.md)

예기치 않은 실행 중단의 Retry/Resume·Watchdog 신호·중복 실행 방지: [task-recovery-protocol.md](task-recovery-protocol.md)

## Work Mode selection

### `PLAN`

- 요구·근거·설계·정본·작업 순서를 확정한다.
- 읽기·조사·제안이 기본이며 승인 전 제품 동작·구조를 변경하지 않는다.

### `BUILD`

- 승인된 계약 범위의 코드·데이터·문서·자산을 구현한다.
- 단계별 검증·롤백을 유지한다.

### `REVIEW`

- 결과를 적대적으로 검토하고 반례·회귀·증거를 찾는다.
- 기본 읽기 전용이다. 수정까지 요청되거나 승인된 finding이 있으면 `BUILD`로 전환해 최소 수정하고 다시 `REVIEW`로 검증한다.

복합 작업은 `PLAN → BUILD → REVIEW`로 전환할 수 있지만 한 시점의 주 Work Mode는 하나다. `CONTINUOUS_WORK_ACTIVE`에서도 이 규칙은 동일하다.

## Automatic selection policy

- 사용자가 Skill·Skill Mode를 언급하지 않아도 현재 요청과 Registry trigger를 비교한다.
- `load_by_default=false`는 자동 선택 금지가 아니라 trigger 불일치 시 읽지 않는다는 뜻이다.
- trigger가 일치하고 `do_not_use_when`에 걸리지 않는 최소 집합만 사용한다.
- 새 기능 또는 기능 계약·공개 경계의 의미 변경은 trigger가 일치한 것으로 보고, 작업 크기·단계 수와 무관하게 intake와 기능 계약 reference를 사용한다.
- 주 책임 분야 Skill은 최대 하나다. Foundation·검증·발행·Handoff는 현재 단계에 필요한 것만 추가한다.
- 사용자에게 “어떤 Skill을 쓸까요?”라고 선택을 전가하지 않는다.
- 사용자가 Skill을 지정해도 trigger·권한·비사용 조건과 충돌하면 그대로 실행하지 않고 이유를 설명한다.
- 새 범위·실패·정본 변경이 생기면 Work Mode와 Skill 라우팅을 다시 계산한다.
- Skill 파일을 읽은 것과 Skill 절차를 실제 실행한 것을 구분한다.
- 실제 capability gap·사용자 지정 인계 등 workflow owner의 조건으로 다른 실행자에게 넘길 때는 `first-prompt → contract → clarify`의 유효한 동일 계약과 승인 참조를 재사용한다. 인계 때문에 같은 질문·계획을 다시 만들지 않는다.
- 신규 실행 기술 제작 압력이 감지되면 설계 Skill보다 기존 대안 평가 Skill을 먼저 호출하고 `existing_solution_disposition`을 계약 입력으로 요구한다.
- 유효한 approval reference 또는 명확한 계속 실행 의도 중 하나라도 없으면 `CONTINUOUS_WORK_INACTIVE`로 유지하고 기존 승인·Grill Me 흐름을 바꾸지 않는다.

## Workflow

### 1. Route automatically once

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

새 기능 또는 기능 계약·공개 경계의 의미 변경은 크기가 작아도 `L1` 이상으로 분류한다. 이미 승인된 기능 경계를 그대로 구현하는 작은 continuation만 기존 approval reference로 intake 재작성을 생략할 수 있다.

최종 결정을 소유하는 `primary_discipline`은 하나만 지정한다. 실제 입력·산출물·검증이 바뀌는 분야만 `affected_disciplines`에 추가한다.

```text
요청 의도·현재 단계·위험
→ PLAN / BUILD / REVIEW
→ Registry trigger·do_not_use_when
→ 최소 Skill 집합
→ 각 Skill의 필요한 Skill Mode
→ CONTINUATION_INTENT_ALIASES와 approval reference 존재 여부
→ CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE 후보
```

발행·검증 Skill은 해당 단계에 도달할 때까지 `deferred_skills`에 둔다. Handoff Skill은 실제 인계가 필요할 때만 선택하며 같은 Work에서 직접 구현하는 경로의 필수 단계가 아니다. 연속작업 후보는 승인 상태가 확인되기 전 실행 권한이 아니다.

### 1.5 Existing Solution First Gate

신규 MCP·addon·CLI·framework·Skill·Mode·execution layer 요청이면 다음을 `PLAN`의 첫 blocker로 둔다.

```text
current environment inventory
→ connected MCP·enabled addon·dependency·existing implementation
→ open/recent PR
→ maintained external solution
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
→ adversarial review
→ user-visible approval state
```

`existing_solution_disposition`이 없으면 `AWAITING_EXISTING_SOLUTION_REVIEW`다. `BUILD_NEW`는 대안으로 해결할 수 없는 차단 결함과 사용자 승인이 모두 있어야 하며, 없으면 custom design·code·PR을 만들지 않는다.

### 1.6 Reuse-First Project Preflight

새로 만들거나 의미 있게 바꾸는 시스템·메커닉·데이터/콘텐츠 구조·UI/UX·시각/Asset·도구/자동화·workflow·Skill/Eval·QA/Test는 tool-only Existing Solution First보다 넓은 `REUSE_FIRST_PREFLIGHT_REQUIRED`를 적용한다.

```text
current project authority + actual implementation/assets/tests
→ Project Asset/Reference/Benchmark already approved or collected
→ PROJECT_WORK_REUSE_HANDOFF + adoption profile/matrix + REUSABLE_MODULE_REGISTRY
→ Base accumulated knowledge/case/reference relevant to this decision
→ targeted cross-project verified evidence only when directly pointed to
→ decision-relevant external benchmark/professional practice/success-failure cases
→ owner-specific reuse/adapt/reference/no-reuse disposition
→ new creation only for the unresolved gap
```

`NOT_RUN`은 신규 제작·`BUILD_NEW`를 차단한다. `REUSED_EVIDENCE`는 동일 승인 범위·같은 consumer·freshness 확인을 만족할 때만 쓴다. `NOT_APPLICABLE`은 새 설계 판단이 없는 기계적 변경에만 이유와 함께 사용한다. 재사용 때문에 프로젝트 고유 규칙·표현·플레이어 경험을 평준화하지 않는다.

### 2. Inspect repository facts

최신 `main`, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본과 실제 repository 파일에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. Notion은 `V4_NOTION_EXCEPTION_ONLY`에 해당할 때만 그 scope를 읽고 exception 또는 migration provenance를 별도로 기록한다. legacy Sheet는 `google_sheet_compatibility_source`에 UNIQUE 미이관 material이 있을 때만 migration evidence로 읽는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

### 3. Build one requirement model

```text
원 요청
→ 문제·목적
→ 사용자·플레이어 경험
→ 범위·비목표
→ 제약·보호 대상
→ 산출물
→ 완료 기준
→ 검증
→ 미검증·보류
```

### 3.1 Build the first prompt

모든 L1 이상 지시문 작성은 [first-prompt-direction-anchoring.md](first-prompt-direction-anchoring.md)를 사용한다.

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
→ conflict scan
```

- 핵심 행동·의도한 결과·지배 기준을 1~2문장으로 압축해 지시문 가장 앞에 둔다.
- Task, Context, Source, Constraints, Output, Validation을 명확히 분리한다.
- 정석안·파격안·통합안은 설계·결정 탐색에 실제 가치가 있을 때만 같은 기준으로 비교한다.
- 앞 문장이 전체 계약을 좁히거나 과장하거나 뒤의 `HARD_CONSTRAINT`와 충돌하면 전체 지시문을 다시 작성한다.
- first-prompt는 초안이며 아직 실행 권한이 없다.

### 3.5 Apply the neutral-recommendation-gate

권장안·판정·설계 선택이 있으면 사용자안과 AI 최초안을 같은 기준으로 비교한다.

```yaml
evaluation_criteria: []
alternatives: []
counterevidence: []
benefits_costs_and_risks: []
reversibility:
unknowns_and_evidence_limits: []
recommended_conclusion:
agreement_or_disagreement_reason:
```

- 사용자안이 검토를 통과하면 근거와 함께 동의한다.
- 다른 안이 더 강하면 차이를 만드는 증거와 함께 권장한다.
- 반대를 위한 반대를 만들지 않는다.
- 증거 부족은 `BLOCKED_UNVERIFIED`로 남긴다.
- L1 이상 기능·설계·아키텍처·정책·방향 결정은 `running-adversarial-review-and-refinement`의 `attack → validate-critique → decision-report`를 PLAN 사전판정 지원 Skill로 실행한다.
- 이 판정의 승인 finding은 `refine-approved-findings`에서 주 책임 분야 Skill BUILD로 한 번만 구현·수정하고, `regression-recheck → decision-report`로 복귀한다.

### 4. Run the Grill Me alignment gate

좋은 프롬프트 변환과 실행 계약 작성 뒤, 실행 전 `Grill Me alignment gate`로 의도·기획 정합성을 확인한다.

- 결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다.
- 기존 Decision이 유효하면 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부·초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.
- 상세 요청은 처음부터 다시 인터뷰하지 않고 direction anchor와 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.
- 계약이 완전하지만 승인되지 않았다면 direction anchor·범위·보호 대상·산출물·검증을 한 번 보여 주고 명시적 승인을 받는다.
- exact contract already approved 상태이면 approval reference를 기록하고 중복 질문 없이 `REUSED_APPROVAL`로 통과한다.
- 중대한 승인 또는 확인이 없으면 `AWAITING_USER_CONFIRMATION`을 유지하고 BUILD·위임·실행으로 이동하지 않는다.

### 5. Closure and confirmation

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

확인 결과는 `CONFIRMED` 또는 `REUSED_APPROVAL`과 approval reference로 기록한다.

### 5.5 Activate bounded continuous work for an approved contract

`[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` 같은 `CONTINUATION_INTENT_ALIASES`가 있고 현재 계약이 `CONFIRMED` 또는 `REUSED_APPROVAL`이면 `APPROVED_CONTRACT_CONTINUATION`으로 [continuous-work-execution.md](continuous-work-execution.md)를 적용해 `CONTINUOUS_WORK_ACTIVE`로 전환한다.

```text
현재 승인된 작업 계약
→ ready task 선택
→ BUILD
→ REVIEW attack → validate-critique
→ 범위 안의 기술적 단일 최소 안전 권장안이면 자동 승인 간주
→ BUILD 최소 반영
→ REVIEW regression-recheck
→ blocker가 있으면 recovery ladder
→ 당장 해결 불가한 국소 task는 defer
→ 독립 ready task 계속
→ 상태 변화 뒤 deferred task 재평가
→ 완료 또는 GLOBAL_TERMINAL_BLOCKER까지 반복
```

`USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위는 자동 승인하지 않는다. 그러나 그 상태가 국소적이거나 복구 가능하면 전체 루프를 즉시 종료하지 않는다. `RECOVERABLE_VERIFICATION_BLOCKER`와 `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`는 재조회·대체 증거·authorized alternate executor를 먼저 시도하고, 당장 풀리지 않으면 해당 task만 defer한다. `GLOBAL_TERMINAL_BLOCKER`는 recovery path를 소진하고 실행 가능한 독립 task가 없을 때만 사용한다. 유효한 계약이나 계속 실행 의도가 없는 요청은 `CONTINUOUS_WORK_INACTIVE`다.

### 6. Produce, sequence and report the approved contract

승인된 범위의 실행 계약·의존성·세부 작업·실제 수행 보고는 [입출력·실행 순서 계약](contract-shapes-and-sequencing.md)을 사용한다. 기존 Plan/receipt의 참조를 재사용하며 새 빈 추적표를 만들지 않는다. 승인 전 사용자에게 구현 개요를 보여주는 것은 이 단계의 BUILD·실행 확정과 다르다.

## Base v9.4 지시 권위·Context 큐레이션

L1 이상 Prompt 계약에서 강한 지시를 추가하기 전에 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 권위를 분류한다. 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 완화하지 않는다.

입력·출력·불변조건·실패조건·검증을 예시보다 먼저 정의하는 Interface-first 계약을 사용한다. 예시는 정상·실패·경계·회귀 Fixture 또는 Golden Set으로 보존한다.

Direction anchor와 first-prompt 순서화는 [first-prompt-direction-anchoring.md](first-prompt-direction-anchoring.md)를 따른다. Context 큐레이션은 현재 `decision_question`을 고정한 뒤 권위·freshness·representation·deduplication·known conflicts·반대 근거·`progressive_load_trigger`·`refresh_trigger`를 기록한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.

## BCP-008 L2+ 명세 추적성

`L2 이상` 작업에서 승인된 요구가 여러 Task·파일·검증으로 분산되면 `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`를 사용한다. 이 Packet은 **별도 책임 원본이 아니다**. intake는 Decision·Requirement·Acceptance ID와 범위를 연결하고, 분야 정본·실제 구현·검증의 내용을 복제하지 않는다.

```text
Decision
→ Requirement
→ Acceptance Criteria
→ Task
→ Implementation Path
→ Verification Evidence
```

- `L0·L1`에는 기본 적용하지 않는다. 다만 실제 영향이 여러 시스템·파일로 확장되면 작업 수준을 다시 판정한다.
- Packet 생성 자체를 완료로 보지 않고 `coverage_status`, `unmapped_items`, `BLOCKED_UNVERIFIED`를 기록한다.
- 문서 정본 연결은 `managing-design-documents`, 실제 diff·테스트 증거 대조는 `reviewing-and-validating-project-changes`가 소유한다.
- 같은 ID를 새 문서마다 재정의하거나 별도 Spec 정본을 만들지 않는다.
