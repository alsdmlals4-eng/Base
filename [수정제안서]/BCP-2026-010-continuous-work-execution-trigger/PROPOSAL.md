# BCP-2026-010 — `[연속작업] 진행해` 연속작업 실행 루프

## 출처와 상태

- 제안 ID: `BCP-2026-010-continuous-work-execution-trigger`
- 출처 프로젝트: `alsdmlals4-eng/Base`
- Base 기준 커밋: `a912cc001ff4d4e3415fb4b4931723c49eb08d9a`
- 제출일: `2026-08-08`
- 상태: `SUBMITTED`
- 기존 해법 판정: `ABSORB`
- 구현 PR: 구현 승인 뒤 별도 기록

## 관찰과 증거

Base에는 이미 다음 책임이 있다.

- `PLAN / BUILD / REVIEW` Work Mode 전환
- L1 이상 적대 검토 생명주기
- 승인된 finding의 최소 수정과 회귀 재검증
- 사용자가 명시적으로 승인한 항목의 병합 권한 상속
- `모두 권장안대로` 입력 시 남은 동등 유형 Grill Me 결정을 권장안으로 확정하는 규칙

그러나 사용자가 한 채팅에서 장시간 작업을 맡길 때, 각 단계가 끝날 때마다 `진행할까요?`, `승인할까요?`, `다음 단계로 넘어갈까요?` 같은 승인 대기로 멈추지 않고 다음 작업까지 계속 수행하라는 명시적 공용 트리거가 없다.

동일 Goal의 열린·최근 PR을 조사했으며, 과거 PR #7의 `continuous learning`은 Skill 학습·라우팅 지속성을 다루고 이번 승인 연속 실행 권한과는 책임이 다르다. 새 독립 Skill이나 외부 자동화 도구를 만들 필요는 없으므로 Existing Solution First 판정은 `ABSORB`다.

## 일반화 후보

사용자가 해당 채팅에서 정확한 활성화 의도로 `[연속작업] 진행해`라고 지시하면, 그 요청의 승인된 범위 안에서 다음 루프를 반복한다.

```text
작업 수행
→ 적대적 검토
→ 검증된 finding 분류
→ 범위 안에서 단일 최선 권장안 결정
→ 권장안 자동 승인 간주
→ 즉시 반영·검증
→ 다음 미완료 작업 선택
→ 반복
→ 전체 범위 완료 후 최종 보고
```

새 Skill은 만들지 않는다. 기존 `managing-project-intake-and-work-contract`, `running-adversarial-review-and-refinement`, `reviewing-and-validating-project-changes`, `maintaining-project-context-and-handoff`의 입력·산출물·권한을 유지하고, intake/Work Mode 라우팅 계약에 `CONTINUOUS_WORK` 실행 상태를 흡수한다.

활성화 문구는 다음으로 고정한다.

```text
[연속작업] 진행해
```

동일 메시지에 작업 범위가 함께 있으면 그 범위에 즉시 적용하고, 기존 진행 중인 작업에서 입력되면 현재 승인된 작업 계약의 남은 범위에 적용한다. 트리거가 없는 일반 요청에는 연속작업 자동 승인 규칙을 적용하지 않는다.

## 적용 조건과 비사용 조건

자동 승인 가능한 권장안은 다음 조건을 모두 만족해야 한다.

- 이미 승인된 작업 계약 범위 안이다.
- 정본·테스트·명시적 요구·표준으로 기술적으로 단일 최소 안전안이 결정된다.
- 프로젝트 코어·주요 UX·콘텐츠 의미·비용/범위 우선순위를 새로 바꾸지 않는다.
- 되돌리기 어려운 외부 고위험 행위가 아니다.

자동 승인하지 않는 조건:

- `USER_DECISION_REQUIRED`
- 기존 승인 범위를 넓히는 새 목표
- 서로 유효한 복수 선택지가 프로젝트 방향을 다르게 만드는 결정
- 결제, 계정 삭제, 보안/권한 확대, 사용자 자격·외부 시스템에 중대한 영향을 주는 행위
- 필요한 정본·권한·도구가 없어 `BLOCKED_UNVERIFIED`인 항목
- 사용자가 중지·범위 변경을 지시한 경우

작업이 길면 짧은 진행 업데이트는 허용하지만, 업데이트 자체를 승인 Gate로 사용하지 않는다. 차단 사유가 없으면 같은 실행 세션 안에서 다음 미완료 작업을 계속 진행한다.

다음 중 하나일 때 루프를 종료한다.

- 승인된 작업 계약의 완료 기준을 모두 충족
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- 안전/권한상 사용자 확인이 필요한 외부 행위 도달
- 사용자가 중지·범위 변경을 지시

## 반례와 위험

### MUST_FIX — 일반 요청까지 자동 승인되는 위험

트리거 없는 요청에 적용하면 기존 Grill Me와 승인 Gate를 무력화한다. 따라서 `[연속작업] 진행해`를 명시적 opt-in으로 제한한다.

### MUST_FIX — 자동 승인으로 기획 결정을 은폐하는 위험

연속 실행은 승인된 범위의 기술적 권장안만 자동 확정한다. 방향성이 달라지는 유효한 복수 선택지는 `USER_DECISION_REQUIRED`를 유지한다.

### MUST_FIX — 무한 루프·과잉 작업 위험

`다음 작업`은 승인된 작업 계약과 완료 기준에서 파생된 미완료 작업만 선택한다. 새 목표를 스스로 생성해 범위를 확장하지 않는다.

### SHOULD_FIX — 장시간 작업에서 진행 상황이 보이지 않는 문제

짧은 진행 업데이트를 허용하되 승인 요청 문구를 섞지 않는다.

### REJECTED_CRITIQUE — 모든 승인 Gate를 제거해야 더 자동화된다

사용자만 결정할 수 있는 방향 변경과 고위험 외부 행위까지 자동화하면 권한 경계가 깨진다. 연속성은 유지하되 기존 안전·기획 Gate는 보존한다.

## 영향 범위와 검증

예상 구현 범위:

1. `AGENTS.md` — 공용 불변 트리거·권한 경계 요약
2. `docs/OPERATING_MODEL.md` — 연속작업 실행 생명주기
3. `docs/WORK_MODE_AND_SKILL_ROUTING.md` — 활성화·자동 승인·중단 조건 상세 계약
4. `skills/managing-project-intake-and-work-contract/SKILL.md` — route/contract에서 트리거 감지와 연속 실행 상태 전달
5. `skills/managing-project-intake-and-work-contract/references/` — 세부 실행 프로토콜
6. `tests/` — 트리거, 비트리거, 사용자 결정 예외, 종료 조건 회귀 계약
7. `docs/CHANGELOG.md`, Learning Log 등 실제 활성 소비자

보호 범위:

- 기존 `PLAN / BUILD / REVIEW` 권한 분리
- Grill Me의 사용자 전용 방향 결정
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`
- 기존 병합/CI/리뷰 Gate
- 프로젝트별 고유 결정과 정본

구현 검증:

- 트리거 문구가 활성 계약에 존재한다.
- 트리거가 없는 일반 요청은 기존 승인 Gate를 유지한다.
- `USER_DECISION_REQUIRED`와 `BLOCKED_UNVERIFIED`는 자동 승인되지 않는다.
- 자동 승인 대상은 승인 범위 안의 기술적 권장안으로 제한된다.
- 적대 검토 후 검증된 finding만 수정한다.
- 다음 작업 선택이 기존 계약 범위를 넘어가지 않는다.
- 완료/차단/사용자 중지 조건에서 루프가 종료된다.
- 기존 Skill routing, Grill Me, 병합 권한 상속 계약이 회귀하지 않는다.

## 승인과 구현

2026-08-08 사용자는 다음 흐름을 Base에 넣는 의사를 명시했다.

> 작업 완료 → 적대적 검토 → 권장안 결정 → 자동 승인 처리 → 다음 작업 → … → 최종 보고

이후 활성화 방식도 다음과 같이 명시했다.

> 내가 해당 채팅에서 `[연속작업] 진행해` 라고 하면 연속작업 실행루프가 진행되게 하는걸로 만들어줘

이 사용자 지시는 후속 승인 단계의 근거로 보존한다. BCP 생명주기 규칙에 따라 신규 제안 PR 자체는 `SUBMITTED`로 시작하며, 제안 병합 뒤 별도 승인 PR에서 `APPROVED_FOR_IMPLEMENTATION`과 `approval_ref`를 기록한다.
