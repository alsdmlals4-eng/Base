# Codex 패키지 Plan 재검수 보고서

## 1. 작업 모드

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
report_status: PLAN_REVIEW_COMPLETE | PLAN_REVIEW_WITH_TECHNICAL_IMPROVEMENTS | CHANGE_PROPOSAL | USER_DECISION_REQUIRED | BLOCKED | UNVERIFIED
```

## 2. 패키지 식별

```yaml
project:
package_id:
package_title:
allowed_branch:
baseline_branch:
baseline_commit:
master_implementation_plan:
package_contract:
```

## 3. 읽은 규칙과 책임 원본

| 경로 | 역할 | 확인 상태 | 핵심 계약 |
|---|---|---|---|

## 4. 최신 저장소 조사

- 실제 Godot 버전:
- 프로젝트 루트:
- Autoload:
- 주요 Scene:
- 관련 GDScript·Resource·런타임 데이터:
- 테스트·검증 명령:
- 사용자 기존 변경:
- 접근하지 못한 항목:

## 5. 예상 파일과 실제 파일 대조

| 계획상 파일 | 실제 경로·대체 파일 | 상태 | 조치 |
|---|---|---|---|

## 6. 현재 구현 상태

| 요소 | `IMPLEMENTED / PARTIALLY_IMPLEMENTED / PLANNED / PROPOSED / DEFERRED / REMOVED / UNVERIFIED` | 근거 |
|---|---|---|

## 7. 기술 개선 제안

기술 개선은 플레이어 결과와 승인된 데이터 계약을 유지해야 한다.

| 제안 | 이유 | 플레이어 결과 변화 | 데이터·저장 영향 | 테스트 | 자동 반영 가능 여부 |
|---|---|---|---|---|---|

## 8. `CHANGE_PROPOSAL`

| 변경 대상 | 기존 승인 계약 | 제안 | 필요한 이유 | 플레이어·범위·호환성 영향 | 구현 중단 범위 | 결정권자 |
|---|---|---|---|---|---|---|

변경 제안이 없으면 `NONE`으로 기록한다.

## 9. 사용자 결정 필요

| 질문 | 선택지 | 기술 영향 | 사용자 체감 영향 | 권장안 |
|---|---|---|---|---|

결정이 필요 없으면 `NONE`으로 기록한다.

## 10. 작업 단위

### 작업 PKG-X-01 — 작업명

- 해결할 finding:
- 플레이어 가치:
- 현재 상태:
- 목표 상태:
- 확인한 파일:
- 예상 수정 파일:
- 예상 생성 파일:
- 데이터·저장 영향:
- 연결 영향:
- 수정 금지:
- Red:
- Green:
- Refactor:
- 회귀 테스트:
- 완료 기준:
- 독립 Commit:
- 롤백:
- 기획 단계 반환 조건:

## 11. 의존성과 실행 순서

| 선행 | 관계 | 후행 | 근거 |
|---|---|---|---|

## 12. 검증 명령

| 목적 | 명령 | 기대 결과 | 실행 가능 여부 | 미실행 이유 |
|---|---|---|---|---|

## 13. 위험·중단 조건

## 14. Codex Plan 최종 판정

```yaml
report_status:
technical_improvements: []
change_proposals: []
user_decisions: []
blockers: []
tests_not_run: []
remaining_unverified: []
recommended_next_action:
```
