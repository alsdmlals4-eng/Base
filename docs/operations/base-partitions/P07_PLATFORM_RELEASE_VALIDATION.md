# P07 · Platform, Release & Execution Validation — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.


## 역할
실제 diff/정적/runtime evidence 검증, 플랫폼·권리·build/release·backend·DRM의 delivery readiness를 책임진다.

## 핵심 Skill
`reviewing-and-validating-project-changes`.

## 중요 규칙
Evidence ceiling, LATEST_EXACT_HEAD_ONLY, Notion approval != runtime proof, platform official-source-first, 미실행/미구성은 PASS 아님.

## 핵심 Module
Change Validation → Evidence Ledger → Platform/Rights → Build/Release → Backend → Entitlement/DRM.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
실행 증거 없는 완료 주장, 오래된 플랫폼 정책, planning screenshot을 runtime proof로 사용, Android/출시 단계 조기 확대, backend/DRM 과잉 설계.

## 검증/완료
해당 플랫폼/릴리스 focused tests, 최신 공식 출처, exact-head evidence. 최소 5회 전체 review 후 clean까지.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P07_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
