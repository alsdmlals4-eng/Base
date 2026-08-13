# Source Radar — Prompt·Planning·Writing Expansion Plan

**Goal:** 고정 후보 수 제한을 제거하고 프롬프트·게임 기획·글쓰기/작법 Source 감시를 기존 주기 조사 구조에 흡수한다.

**Base:** `f08a78b33aa1d458376da8f783553fe9ce7aa9cd`

## Constraints

- 고정 최소·최대 후보 수는 없다.
- 모든 material candidate를 수량 때문에 누락하지 않는다.
- 후보 보존과 실행 우선순위·용량·의존성은 분리한다.
- 새 ACTIVE Skill, scheduler, Source canon은 만들지 않는다.
- 기존 Watchlist의 원출처 역추적, Evidence, 기존 해결책 우선, 적대적 검토, 승격 Gate를 유지한다.

## Tasks

1. `tests/test_periodic_external_source_discovery_seeds.py`와 `tests/test_weekly_work_improvement_review.py`에 실패 계약을 먼저 추가한다.
2. 테스트 전용 head에서 RED를 확인한다.
3. `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`에 후보 전량 보존 계약과 프롬프트·기획·작법 Source group을 추가한다.
4. `WEEKLY_WORK_IMPROVEMENT_REVIEW.md`에서 고정 개수 제한을 제거하고 후보 보존과 실행 상태를 분리한다.
5. focused test와 Evidence Knowledge CI를 exact head에서 실행한다.
6. 중복 owner, 과잉 일반화, 인기=권위, 연구=인과, 작가 문체 모방, 무제한 noise 축적을 적대적으로 검토한다.
7. 최신 main 동기화와 검증 후 PR merge gate를 적용하고 merge 뒤 main을 readback한다.
