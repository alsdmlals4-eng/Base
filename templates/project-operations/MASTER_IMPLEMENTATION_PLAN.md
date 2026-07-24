# 마스터 구현계획

## 1. 문서 상태

```yaml
project:
status: DRAFT | CONFIRMED | READY_FOR_IMPLEMENTATION_HANDOFF | REVISE | BLOCKED | UNVERIFIED
planning_branch:
baseline_branch:
baseline_commit:
integrated_design:
parent_implementation_issue:
updated_at:
```

## 2. 최종 구현 목표

## 3. 플레이어 가치

## 4. 승인된 프로젝트 코어

## 5. 불변 조건

- 프로젝트 코어:
- Core Loop:
- 플레이어 규칙:
- 데이터·저장 호환성:
- UI·UX 핵심 흐름:
- 수정 금지 자산·결정:

## 6. 구현 포함 범위

## 7. 구현 제외 범위

## 8. 공통 수정 금지 범위

## 9. 데이터·저장·ID·Schema 보호 조건

## 10. 구현 패키지 지도

| 패키지 ID | 결과 | 선행 패키지 | 플레이 가능·검증 가능 산출물 | 주요 위험 | 승인 게이트 | Branch | PR | 상태 |
|---|---|---|---|---|---|---|---|---|

## 11. 의존성

| 선행 | 관계 | 후행 | 근거 | 실패 시 조치 |
|---|---|---|---|---|

관계는 `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES / OPTIONAL_FOLLOWUP`을 사용한다.

## 12. 공통 테스트 전략

### 정적 검사

### Godot headless·import

### 런타임·플레이 검증

### 저장·불러오기·마이그레이션

### 정상·실패·경계·회귀

### 접근성·성능

## 13. 승인 게이트

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

## 14. `CHANGE_PROPOSAL` 기준

- 프로젝트 코어·Core Loop 변경
- 플레이어 규칙·보상·실패 결과 변경
- 신규 시스템·MVP 범위 변경
- 주요 UI·UX·콘텐츠 의미 변경
- 승인 기능 제거
- 저장 호환성을 깨는 Schema 변경

## 15. Branch·PR·병합 계약

- 상위 구현 Issue:
- 패키지 Branch 형식:
- 패키지 PR 형식:
- 기본 병렬성: `SEQUENTIAL`
- 기본 병합 정책: `AUTO_MERGE_AFTER_REQUIRED_CHECKS`
- Required Check: `ci-gate`
- 자동 병합 차단 상태: `USER_REVIEW_REQUIRED / CHANGE_PROPOSAL / REVISE / BLOCKED / UNVERIFIED`
- 수동 사용자 병합 승인: `OPTIONAL_EXCEPTION`
- Codex `main` 직접 Push: `FORBIDDEN`
- Codex force push·amend·PR 생성·병합: `FORBIDDEN`

## 16. Repository 병합 설정

```yaml
repository_auto_merge: enabled | disabled | UNVERIFIED
ruleset: active | disabled | UNVERIFIED
required_check: ci-gate
required_review_thread_resolution: true
required_approving_review_count: 0
allowed_merge_method: squash
```

## 17. 롤백 계획

## 18. Vertical Slice 완료 기준

## 19. 다음 프로덕션 단계 진입 조건

## 20. 남은 위험과 `UNVERIFIED`

## 21. 사용자 결정 기록

사용자 체감·프로젝트 코어·MVP·호환성처럼 실제 결정이 필요한 항목만 기록한다.

| 결정 | 사용자 답변 | 기준 대화·Issue | 반영 Commit |
|---|---|---|---|
