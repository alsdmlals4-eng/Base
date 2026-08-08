# Managing Project Intake and Work Contracts — Learning Log

## 2026-08-08 — Explicit bounded continuous-work execution

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 현재 채팅에서 `[연속작업] 진행해`라고 명시하면 `작업 → 적대적 검토 → 권장안 결정 → 자동 승인 처리 → 다음 작업 → … → 최종 보고`를 중간 승인 대기 없이 수행하라는 요청.
- **Finding:** Base에는 이미 승인된 계약, `PLAN / BUILD / REVIEW`, 적대 검토, 기술 finding 반영, 회귀 재검증, 승인 범위의 병합 권한 상속이 있었지만 이를 하나의 명시적 opt-in 연속 실행 상태로 묶는 계약은 없었다. 또한 새 standalone 테스트 파일만 추가하면 일부 명시적 CI 목록에서 소비되지 않아 거짓 GREEN이 될 수 있음을 RED 단계에서 다시 확인했다.
- **Decision:** 새 Skill이나 Work Mode를 만들지 않고 Existing Solution First를 `ABSORB`로 판정했다. intake에 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 flag와 `references/continuous-work-execution.md`를 추가하고, `[연속작업] 진행해`가 있을 때만 현재 승인된 작업 계약의 남은 범위에서 다음 미완료 작업을 자동 선택한다. 기술적 단일 최소 안전 권장안은 적대 검토 뒤 자동 승인으로 간주할 수 있지만 `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위, 사용자 중지는 자동 승인하지 않는다.
- **Evidence:** PR #228의 TDD RED에서 GitHub Actions `Validate Game Project Operating System` run `31256943151`, job `93101653170`가 새 reference 부재를 정확히 실패시켰고 나머지 기존 계약 테스트는 통과했다. 구현 뒤에는 기존 CI의 reference-freshness가 변경된 intake Skill에 대해 인정된 회귀 테스트와 Learning Log 동반 변경을 요구해 추가 소비자 누락도 탐지했다.
- **Boundary:** 연속작업은 현재 응답·에이전트 실행 세션 안의 orchestration이다. scheduler, webhook, 브라우저가 닫힌 뒤의 백그라운드 처리, 다른 ChatGPT 채팅 자동 메시지 전송을 의미하지 않는다. 트리거가 없는 일반 요청의 승인·Grill Me 흐름은 바꾸지 않는다.
- **다음 검토 트리거:** 실제 프로젝트에서 연속작업이 승인 범위를 넘어 새 Goal을 생성하거나, 사용자 전용 결정을 자동 확정하거나, 고위험 외부 행위를 우회하거나, 지나친 중간 보고/무한 반복으로 작업 연속성을 해칠 때 이 계약을 재검토한다.
