# P09 · Content, Narrative & Publication — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.


## 역할
연재소설, 게임 서사/캐릭터/voice, 게임개발 YouTube 등 외부 콘텐츠 제작·발행 규칙을 책임진다.

## 핵심 Skill
`producing-game-development-youtube-videos`, `developing-and-revising-serial-fiction`.

## 중요 규칙
project canon first, voice/style consistency, rights/provenance, project-specific vs Base reusable lesson separation.

## 핵심 Module
Serial Fiction → Narrative/Character/Voice → Game-dev YouTube → Publication Evidence → Reusable Writing Lessons.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
정사/voice drift, 프로젝트 고유 서사를 Base 공용 규칙으로 승격, 외부 표현 복제, 발행 성공을 게임 runtime 완료로 혼동.

## 검증/완료
writing/fiction/youtube/narrative focused tests + scope 검사. 최소 5회 전체 적대적 개선 후 clean까지.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P09_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: FICTION_AND_INTERACTIVE_NARRATIVE, YOUTUBE_AND_VIDEO_EDITING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
