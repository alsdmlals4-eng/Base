# Continuous Work Execution

## 목적

`[연속작업] 진행해`는 사용자가 현재 채팅의 **현재 승인된 작업 계약** 안에서 중간 승인 대기 없이 다음 미완료 작업까지 계속 수행하라고 명시적으로 선택하는 opt-in 트리거다.

이 계약은 새로운 Skill이나 Work Mode가 아니다. `CONTINUOUS_WORK_ACTIVE` / `CONTINUOUS_WORK_INACTIVE`라는 실행 상태를 기존 intake 계약에 얹으며, `PLAN / BUILD / REVIEW` Work Mode를 대체하지 않는다.

## 활성화와 범위

```text
사용자 입력에 [연속작업] 진행해 존재
→ 현재 승인된 작업 계약 확인
→ CONTINUOUS_WORK_ACTIVE

트리거가 없는 일반 요청
→ CONTINUOUS_WORK_INACTIVE
→ 기존 승인·Grill Me 계약 유지
```

- 동일 메시지에 새 작업 범위가 함께 있으면 먼저 intake의 `route → first-prompt → contract → clarify`로 계약을 닫고, 승인된 범위에서만 활성화한다.
- 이미 진행 중인 작업에서 `[연속작업] 진행해`가 입력되면 **현재 승인된 작업 계약**의 남은 범위에 적용한다.
- 이 상태는 채팅 전체에 영구 권한을 부여하지 않는다. 계약 완료, 사용자 중지, 차단 상태 또는 범위 변경에서 종료한다.
- 다음 작업은 승인된 계약의 완료 기준에서 파생된 미완료 작업만 선택한다. 스스로 새 Goal을 만들거나 범위 확대를 하지 않는다.

## 실행 루프

```text
현재 승인된 작업 계약
→ 다음 미완료 작업 선택
→ BUILD에서 작업 수행
→ REVIEW: attack → validate-critique
→ finding 분류
   ├─ 범위 안의 기술적 단일 최소 안전안
   │  → 권장안 자동 승인 간주
   │  → BUILD에서 최소 반영
   │  → REVIEW: regression-recheck → decision-report
   │  → 작업 완료 기록
   │  → 다음 미완료 작업
   ├─ USER_DECISION_REQUIRED
   │  → 연속 실행 중지, 사용자 결정 요청
   └─ BLOCKED_UNVERIFIED
      → 연속 실행 중지, 필요한 증거·권한·입력 보고
→ 완료 기준을 모두 충족할 때까지 반복
→ 최종 실행 보고
```

진행 시간이 긴 경우 짧은 진행 업데이트를 제공할 수 있다. 다만 업데이트를 `진행할까요?`, `승인할까요?` 같은 승인 Gate로 바꾸지 않는다. 차단 조건이 없으면 실행 세션 안에서 다음 작업으로 계속 이동한다.

## 권장안 자동 승인 조건

연속작업에서 권장안을 자동 승인한 것으로 간주하려면 다음을 모두 만족해야 한다.

1. 현재 승인된 작업 계약 범위 안이다.
2. 정본·테스트·명시적 사용자 요구·표준으로 기술적으로 단일 최소 안전안이 결정된다.
3. 적대 검토에서 finding이 유효하다고 확인됐다.
4. 프로젝트 코어, 주요 UX, 콘텐츠 의미, 비용·범위 우선순위를 새로 바꾸지 않는다.
5. 되돌리기 어려운 외부 고위험 행위가 아니다.

`MUST_FIX`와 승인 범위의 기술적 `SHOULD_FIX`는 위 조건을 만족할 때 자동 승인할 수 있다. 단순한 선호나 AI 최초안이라는 이유만으로 자동 승인하지 않는다.

## 자동 승인 금지와 종료 조건

다음 중 하나면 자동 승인하지 않고 연속 루프를 종료하거나 필요한 사용자 결정을 기다린다.

- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- 기존 승인 범위를 넓히는 새 목표 또는 범위 확대
- 서로 유효한 복수 선택지가 프로젝트 코어·주요 UX·콘텐츠 의미·비용 우선순위를 다르게 만드는 결정
- 결제, 계정 삭제, 보안·권한 확대 또는 별도 사용자 자격 확인이 필요한 고위험 외부 행위
- 필요한 정본·도구·권한·입력이 없어 검증할 수 없는 경우
- 사용자가 중지 또는 범위 변경을 지시한 경우
- 현재 승인된 작업 계약의 완료 기준을 모두 충족한 경우

사용자 결정으로 멈췄다가 답변을 받으면 새 결정과 approval reference를 계약에 반영한 뒤, 사용자가 계속 연속작업을 원한다는 현재 지시가 유효한 범위에서 남은 작업을 재개할 수 있다.

## Work Mode 관계

`CONTINUOUS_WORK_ACTIVE`는 Work Mode를 대체하지 않는다. 각 작업은 여전히 한 시점에 `PLAN / BUILD / REVIEW` 중 하나를 주 Work Mode로 사용한다.

일반적인 반복은 다음과 같다.

```text
BUILD
→ REVIEW attack → validate-critique
→ 기술적 권장안 자동 승인 가능 여부 판정
→ BUILD 최소 수정
→ REVIEW regression-recheck
→ 다음 작업
```

기획 충돌이나 새 범위가 생기면 `PLAN`으로 돌아가고, 사용자만 결정 가능한 항목이면 `USER_DECISION_REQUIRED`로 중지한다.

## 비동기·백그라운드 경계

연속작업은 **현재 응답 또는 현재 에이전트 실행 세션 안에서** 다음 작업으로 계속 진행하는 orchestration 계약이다.

다음을 의미하지 않는다.

- 별도 `scheduler` 실행
- `webhook` 이벤트 수신
- 브라우저가 닫힌 뒤의 백그라운드 작업
- 다른 ChatGPT 채팅으로의 자동 메시지 전달
- 미래 시점에 임의로 작업을 재개하는 기능

그런 기능이 필요하면 해당 플랫폼이 제공하는 별도 자동화 기능과 권한 계약을 사용해야 한다.

## 최종 보고

정상 완료 시 중간 승인 질문을 반복 나열하지 않는다. 최종 보고에는 최소 다음을 포함한다.

```yaml
continuous_work_state: COMPLETE | STOPPED_USER_DECISION | BLOCKED_UNVERIFIED | STOPPED_BY_USER
approved_scope:
completed_work: []
adversarial_findings: []
auto_approved_recommendations: []
validation_evidence: []
remaining_risks: []
next_state:
```

`CONTINUOUS_WORK_ACTIVE`였다는 사실과 자동 승인해 반영한 권장안, 적대 검토·회귀 검증 증거를 명확히 남긴다.
