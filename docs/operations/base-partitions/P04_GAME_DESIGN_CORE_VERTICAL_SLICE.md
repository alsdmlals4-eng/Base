# P04 · Game Design, Core, Player Research & Vertical Slice — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER` · `OPEN_PR_READ_ONLY_BY_DEFAULT`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 merged-main 오류·충돌·누락을 발견하면 `CROSS_PART_CHANGE`로 owner를 기록해 수정할 수 있다. 모든 open/draft/ready PR·branch는 read-only이며 mutation은 사용자가 PR 번호와 허용 동작을 명시한 경우에만 가능하다.

## 역할
게임의 플레이어 가치, 컨셉, 프로젝트 코어, 기능/밸런스, 사용자 연구와 Vertical Slice 설계를 책임진다.

## 핵심 Skill
`analyzing-and-refining-game-concepts`, `identifying-project-core`, `establishing-project-core`, `designing-vertical-slices`, `governing-game-user-research-coverage`.

## 중요 규칙
player value first, 현행 조사→최소 3개 실질 대안→benchmark→trade study, BETTER_ALTERNATIVE_SEARCH, LONG_TERM_PLAN_FIT_REQUIRED, WORLD_STORYLINE_FIT_REQUIRED, `RELEASE_NEAR_VERTICAL_SLICE_FIRST`, `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`.

플레이어 경험 검증은 짧더라도 **실제 게임 사용 후보**인 UI/UX·이미지/아트·애니메이션/연출·음악/효과음·VFX/피드백·핵심 시스템/데이터/콘텐츠를 연결한 완성형 Vertical Slice에서 수행한다. 플레이어가 보는·듣는·조작하는 경로에는 임시 `player-facing placeholder`나 dummy presentation을 남기지 않는다. 시스템-only PoC는 `TECHNICAL_SPIKE_INTERNAL_ONLY`로 좁은 기술 질문에 사용할 수 있지만 재미·몰입·가독성·첫인상·판매력·감정·기억·전체 UX의 PASS 근거가 아니다.

## 핵심 Module
Concept → Core Identification → Core Establishment → Feature/Balance → Player Research → Technical Spike(필요 시) → Complete Release-near Vertical Slice → Human Play Evidence.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 **실제 활성** workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
기능 수 늘리기, 플레이어 감정/선택/보상 누락, 허수 대안, 벤치마크 복사, 테스트 불가능한 acceptance, 시스템-only PoC를 player-experience evidence로 승격, player-facing placeholder가 남은 Slice를 최종 플레이테스트 대상으로 사용, 프로젝트 고유 내용을 Base 공용화.

## 검증/완료
관련 planning/vertical slice 회귀와 Part scope 검사. 최소 5회 **전체 lifecycle** 적대적 개선 후 clean까지. 관점 5개를 5회로 세지 않는다.

## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P04_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: GAME_DEVELOPMENT.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
