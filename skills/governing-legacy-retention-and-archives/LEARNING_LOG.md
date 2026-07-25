# Legacy Retention and Archive Governance Learning Log

## 2026-07-25 — 원문 보존과 현재 권한 격리

- 반복 문제: 구형 자료를 삭제하지 않으려다 활성 경로에 계속 두거나, 경로만 남기고 본문을 비워 근거와 복구 가능성을 잃었다.
- 공용 계약: lifecycle과 retention classification을 분리하고, archive record는 `active_authority: false`, `implementation_authority: NONE`을 강제한다.
- 자료 유형별 경계: 문서, inactive Skill, evidence, generated derivative, source/runtime asset, secret와 Git branch는 같은 보존 절차를 사용하지 않는다.
- RED 증거: Base Actions run `30160236473`에서 Skill·Registry·coverage coupled change 누락을 `ubuntu-contract` 실패로 확인했다.
- concurrent integration: Base PR #39가 동일 Skill ID와 shared-route adapter 구조를 먼저 병합해, 중복 Skill을 만들지 않고 승인 계약만 보강했다.
- fresh-context pressure scenarios: `NOT_RUN` — 독립 subagent runner 미연결.
- 지식 상태: 공용 판단 계약은 `PATTERN`; 네 프로젝트 adapter 적용과 실제 legacy migration 효과는 검증 전 `OBSERVATION`.
