# Continuous Work Execution Trigger Design

## Goal

사용자가 현재 채팅에서 `[연속작업] 진행해`라고 명시하면, 현재 승인된 작업 계약 범위 안에서 중간 승인 대기로 멈추지 않고 `작업 → 적대적 검토 → 권장안 자동 승인 → 반영·검증 → 다음 작업`을 반복한 뒤 완료 또는 차단 시 최종 보고한다.

## Existing-solution disposition

`ABSORB`.

Base에는 이미 다음 책임이 있으므로 새 Skill이나 독립 실행 계층을 만들지 않는다.

- `managing-project-intake-and-work-contract`: 요청, 승인 계약, 순서화
- `running-adversarial-review-and-refinement`: attack, critique validation, regression recheck
- `reviewing-and-validating-project-changes`: 실제 변경 증거
- `maintaining-project-context-and-handoff`: 현재 상태와 다음 작업
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 승인된 범위의 병합 권한 상속

## Activation contract

```text
activation phrase: [연속작업] 진행해
state: CONTINUOUS_WORK_ACTIVE
scope: current approved work contract
```

- 동일 메시지에 작업 요청이 있으면 intake가 계약을 만들고, 명시적 사용자 결정이 남지 않은 범위에서 연속 실행을 시작한다.
- 진행 중인 작업에서 입력하면 현재 승인된 계약의 남은 범위에 적용한다.
- 트리거가 없으면 `CONTINUOUS_WORK_INACTIVE`이며 기존 승인·Grill Me 정책을 그대로 따른다.
- 이 상태는 채팅 전체에 영구 권한을 주지 않는다. 현재 계약이 완료·중지·차단되면 종료된다.

## Execution loop

```text
approved work contract
→ choose next incomplete task inside scope
→ BUILD/perform work
→ REVIEW attack
→ validate-critique
→ classify finding
→ if technical single-safe recommendation: auto-approve recommendation
→ apply minimal approved change
→ regression-recheck / validation
→ mark task complete
→ choose next incomplete task
→ repeat
→ final execution report
```

진행 업데이트는 허용하지만 승인 질문으로 사용하지 않는다.

## Auto-approval boundary

자동 승인 가능한 권장안은 모두 다음 조건을 만족해야 한다.

1. 현재 승인된 계약 범위 안이다.
2. 정본·테스트·사용자 요구·표준으로 단일 최소 안전안이 결정된다.
3. 프로젝트 코어, 주요 UX, 콘텐츠 의미, 비용/범위 우선순위를 새로 바꾸지 않는다.
4. 외부 고위험 행위나 별도 사용자 자격 확인이 필요하지 않다.
5. 적대 검토에서 `MUST_FIX` 또는 승인 범위의 기술적 `SHOULD_FIX`로 검증됐다.

자동 승인하지 않고 멈추는 조건:

- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- 승인 범위를 넓히는 새 목표
- 유효한 복수 선택지가 프로젝트 방향을 다르게 만드는 결정
- 결제, 계정 삭제, 보안·권한 확대 등 별도 확인이 필요한 고위험 외부 행위
- 사용자 중지·범위 변경

## Non-background boundary

`CONTINUOUS_WORK_ACTIVE`는 현재 응답/에이전트 실행 안에서 다음 작업으로 계속 진행하는 orchestration 계약이다. 별도 scheduler, webhook, 백그라운드 프로세스 또는 이후 자동 메시지 전달을 의미하지 않는다.

## Components

### `AGENTS.md`

공용 불변 규칙으로 트리거와 안전 경계를 한 단락으로 요약한다.

### `docs/WORK_MODE_AND_SKILL_ROUTING.md`

상세 상태, 활성화, Work Mode 전환, 자동 승인과 중단 조건의 정본이다.

### `docs/OPERATING_MODEL.md`

전체 생명주기에 연속작업 루프를 one-hop으로 설명한다.

### `skills/managing-project-intake-and-work-contract/SKILL.md`

`route`와 `contract`가 트리거를 감지해 `CONTINUOUS_WORK_ACTIVE`를 계약 실행 상태로 전달하도록 한다.

### `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

실행 프로토콜의 단일 상세 reference다.

### tests

정적 계약 테스트가 트리거, opt-in 경계, 자동 승인 예외, 루프, 비백그라운드 경계와 one-hop 연결을 고정한다.

## Validation

- 새 계약 테스트를 먼저 추가하고 구현 전 실패를 확인한다.
- 구현 뒤 전용 테스트 및 기존 interview/routing/BCP 회귀 테스트를 통과시킨다.
- GitHub Actions의 `ci-gate`까지 통과한다.
- PR diff를 적대 검토하고, 트리거 없는 일반 요청이 자동 승인되는 회귀가 없는지 재확인한다.

## Rollback

문제가 생기면 전용 reference와 연결 문구·테스트를 한 PR 단위로 revert한다. 기존 `PLAN / BUILD / REVIEW`, Grill Me, 병합 권한 상속 규칙은 변경하지 않으므로 rollback 시 기존 운영으로 즉시 복귀한다.
