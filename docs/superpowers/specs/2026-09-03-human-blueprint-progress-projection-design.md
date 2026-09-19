# 사람용 Blueprint 목표·시스템·케이스 작업현황 통합 설계

- 상태: `USER_APPROVED_DESIGN`
- 승인 근거: `current-user-message:2026-09-03:좋아-아주좋아-교정진행해줘`
- 기준 Base main: `850204b3e5de81a4045111b4a050c46c5a292b59`
- 적용 범위: Base의 사람용 Blueprint PDF 발행 계약과 PM 파생 투영
- 제외 범위: 프로젝트별 게임 규칙·수치·실제 PDF 재발행·Godot 구현

## 1. 문제

현재 Base에는 repository-first 정본, 사람용 Blueprint PDF, AI production spec, `project_work_kanban`이 각각 존재한다. 그러나 사람용 PDF에서 프로젝트 목표, 시스템 기획, 실제 플레이 케이스, 현재 작업과 검증 상태를 한 흐름으로 읽는 공용 계약과 기계 검사가 없다. 이 때문에 기획서는 풍부하지만 작업 현황은 별도 체크리스트를 찾아야 하고, PM 카드는 존재해도 목표·시스템·케이스와의 연결이 사람용 Blueprint에 안정적으로 투영되지 않는다.

## 2. 비교와 결정

### A. 별도 HTML 또는 PM 전용 PDF

- 장점: 필터·표현 자유도가 높다.
- 단점: 새 산출물과 최신성 책임이 생기고, 사용자용 Blueprint와 중복된다.
- 판정: `REJECT`.

### B. GitHub Projects만 사용

- 장점: Issue·PR 상태를 직접 활용한다.
- 단점: 게임 목표·시스템 설계·플레이 케이스·시각 설명을 하나의 사람용 기획 흐름으로 제공하기 어렵다.
- 판정: `ADAPT` — 작업 상태의 원천 중 하나로만 사용한다.

### C. 기존 Blueprint PDF에 통합

- 장점: 사람이 게임과 제작 현황을 같은 문서에서 이해하고, 기존 두 산출물 정책을 유지한다.
- 단점: PDF가 정본처럼 오해되거나 서로 다른 상태 축이 하나의 진행률로 합쳐질 위험이 있다.
- 판정: `ADOPT` — exact source SHA를 가진 읽기 전용 파생 snapshot으로 제한한다.

## 3. 채택 구조

```text
repository canon owners
+ PROJECT_AI_PRODUCTION_SPEC.md의 목표·시스템·케이스 계약
+ project_work_kanban의 현재 작업·차단·다음 행동
+ test/runtime/visual/human evidence
                ↓ source SHA 일치·참조·진행수 검증
HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION
                ↓
기존 HUMAN_MASTER_GDD_PDF 안의 시각 PM 장
```

새 HTML, 별도 PM PDF, 새 상태 저장소를 만들지 않는다. 투영 자료는 현재 정본과 receipt를 읽어 생성하며, PDF에서 직접 체크한 값으로 repository 상태를 변경하지 않는다.

## 4. 상태 축 분리

Blueprint는 다음 세 축을 섞지 않는다.

1. **기획·구현 성숙도**: `DOCUMENTED → CONFIRMED → IMPLEMENTED → AUTOMATED_TEST_PASS → RUNTIME_VERIFIED → UX_VERIFIED → RELEASE_READY`
2. **작업 흐름**: `BACKLOG → READY → IN_PROGRESS → VERIFY_REVIEW → DONE`, 별도 차단 상태 `BLOCKED_UNVERIFIED | USER_DECISION_REQUIRED | DEFERRED`
3. **검증 증거**: `E0_CONTRACT`부터 `E6_HUMAN_PLAYTEST`, 각 결과 `PASS | FAIL | PARTIAL | NOT_RUN | BLOCKED_UNVERIFIED | NOT_APPLICABLE`

자동 테스트 PASS를 runtime·UX·사용자 승인으로 올려 쓰지 않는다.

## 5. PDF 구성

기존 Blueprint PDF 안에 다음 모듈을 둔다.

- `PROJECT_STATUS_DASHBOARD`: 기준 revision, 현재 목표, 목표·시스템·케이스·작업 완료 수, 차단, 사용자 결정, 현재 작업, 다음 행동
- `PROJECT_GOAL_MAP`: 프로젝트 핵심 목표와 하위 목표 관계
- `GOAL_STATUS_CARD`: 목표 가치, 연결 시스템·케이스·작업, 현재·목표 성숙도, blocker와 다음 행동
- `SYSTEM_STATUS_CARD`: 시스템 목적, owner·consumer, 연결 목표·케이스·작업, 기획·데이터·자산·구현·검증 체크
- `CASE_VERIFICATION_MATRIX`: 정상·경계·실패·충돌·중단·복구·저장·UI·접근성·성능 케이스별 기획·구현·증거 상태
- `GOAL_SYSTEM_CASE_WORK_TRACEABILITY`: 목표 ↔ 시스템 ↔ 케이스 ↔ 작업 ↔ evidence 연결

## 6. 진행률 규칙

- 완료 수는 현재 목표에 필요한 항목 중 실제 완료 조건을 충족한 항목만 센다.
- 작업은 `DONE`만 완료다.
- 케이스는 적용 가능하고, 목표 성숙도에 도달했으며, 모든 필수 evidence가 PASS일 때만 완료다.
- `NOT_APPLICABLE`은 이유를 기록하고 분모에서 제외한다.
- 자식 퍼센트를 평균내지 않는다.
- 단일 전체 퍼센트 대신 목표·시스템·케이스·작업 수와 차단 수를 나란히 표시한다.

## 7. 데이터·오류 경계

- projection의 `source_commit`은 PDF metadata와 동일한 40자 SHA여야 한다.
- 모든 `goal_id`, `system_id`, `case_id`, `work_item_id`는 유일하고 참조가 해소되어야 한다.
- PASS에는 evidence locator가 필요하다.
- 차단 작업에는 blocker와 재개 조건이 필요하다.
- source mismatch 또는 오래된 snapshot은 숨기지 않고 `STALE_SNAPSHOT` 또는 validation failure로 표시한다.
- 검증기는 기록 일관성을 확인할 뿐 외부 증거의 진실이나 사용자 승인을 대신 판정하지 않는다.

## 8. 검증

- 계약·템플릿·V4 route token 검사
- valid/invalid projection 단위 테스트
- 중복 ID·미해소 참조·source mismatch·증거 없는 PASS·N/A reason 누락 음성 테스트
- Markdown 렌더에 필수 섹션과 실제 완료 수가 표시되는지 확인
- 전체 Base validation과 PR exact-head CI
- 최소 5회 적대적 검토와 merged-main readback

## 9. 롤백

문제가 생기면 V4의 projection route와 새 contract/template/tool/test 파일을 하나의 squash commit으로 되돌린다. 기존 `HUMAN_MASTER_GDD_PDF`, `PROJECT_AI_PRODUCTION_SPEC.md`, `project_work_kanban`, 프로젝트 정본·runtime에는 데이터 마이그레이션이나 파괴적 변경이 없으므로 기존 흐름으로 즉시 복귀할 수 있다.
