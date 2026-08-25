# P01 · Project Planning, Operations & Notion — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.


## 역할
사용자 요청을 실행 가능한 작업계약으로 만들고 프로젝트 운영·설계문서·handoff·continuity·사람용 Notion/학습 흐름을 책임진다.

## 핵심 Skill
`managing-project-intake-and-work-contract`, `managing-game-project-operating-system`, `managing-design-documents`, `maintaining-project-context-and-handoff`, `maintaining-long-running-task-continuity`, `creating-user-learning-notes`.

## 중요 규칙
- DIRECTION_FIRST
- GPT_FIRST_PLANNING_AND_REVIEW
- NOTION_DEFAULT_PROJECT_WORKSPACE / PROJECT_RELATION_REQUIRED
- SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
- GitHub runtime/structured truth와 Notion human-facing canon 분리
- `SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED`: 게임 프로젝트 작업이 플레이어가 체감하는 연결된 시스템 로직·분기·상태·다중 시스템 흐름을 의미 있게 건드리면, current-state/reuse-first preflight 뒤 구현 준비 판정 전에 `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`의 적용 Gate를 확인한다.
- `REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW`: 현재 승인 Blueprint가 있으면 같은 시스템을 다시 만들지 않고 현재 변경 범위만 REUSE/ADAPT한다.
- `NO_MASS_BLUEPRINT_BACKFILL`: 현재 작업과 무관한 프로젝트·시스템을 Blueprint 부재만으로 미완료 처리하거나 일괄 변환하지 않는다. 단순·이미 명확한 작업은 이유를 남긴 `NOT_APPLICABLE_WITH_REASON`으로 종료할 수 있다.

## 핵심 Module
Intake & Work Contract → current-state / reuse-first → System Blueprint entry check (when applicable) → Project OS → Design Docs → Context/Handoff → Continuity → User Learning/Notion.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
중복 승인 Gate, GPT→Codex 강제 흐름, Notion 프로젝트 혼입, 사람이 읽는 계획과 repository runtime truth 혼동, 오래된 Sheets/HTML 참조, Blueprint의 제3 정본화·불필요한 일괄 backfill·기존 Blueprint 중복 제작.

## 검증/완료
Manifest validation + P01 관련 focused tests + 최소 5회 전체 적대적 개선, 이후 blocker 0까지. 완료보고는 사용자 학습형으로 작성한다.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P01_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.