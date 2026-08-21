# P03 · Adversarial Quality, Refactoring & Git Integrity — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER` · `OPEN_PR_READ_ONLY_BY_DEFAULT`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 merged-main 오류·충돌·누락을 발견하면 `CROSS_PART_CHANGE`로 owner를 기록해 수정할 수 있다. 모든 open/draft/ready PR·branch는 read-only이며 mutation은 사용자가 PR 번호와 허용 동작을 명시한 경우에만 가능하다.


## 역할
적대적 검토·finding 검증·계약보존 리팩터링·Git/workstream 격리·post-change monitor를 책임진다.

## 핵심 Skill
`running-adversarial-review-and-refinement`, `refactoring-with-contract-preservation`, `synchronizing-local-and-github-state`.

## 중요 규칙
`FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`, `CLEAN_REVIEW_EXIT`, POST_CHANGE_MONITOR_LOOP, OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT.

## 핵심 Module
Attack → Validate Critique → Refine Approved Findings → Regression → Git/PR Integrity → Post-change Monitor.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
5회를 checklist/lens로 축소, 5회에서 강제 종료, 가짜 finding, 동일 finding 중복 수정, unrelated branch/worktree 변경, evidence ceiling 위반.

## 검증/완료
focused adversarial/Git tests와 Part scope 검사. 1~5회 의무 전체 loop 후에도 finding이 있으면 6..N회 계속한다.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P03_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
