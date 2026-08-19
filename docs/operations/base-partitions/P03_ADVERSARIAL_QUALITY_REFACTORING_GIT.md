# P03 · Adversarial Quality, Refactoring & Git Integrity — Context Pack

## 역할
적대적 검토·finding 검증·계약보존 리팩터링·Git/workstream 격리·post-change monitor를 책임진다.

## 핵심 Skill
`running-adversarial-review-and-refinement`, `refactoring-with-contract-preservation`, `synchronizing-local-and-github-state`.

## 중요 규칙
`FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`, `CLEAN_REVIEW_EXIT`, POST_CHANGE_MONITOR_LOOP, OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT.

## 핵심 Module
Attack → Validate Critique → Refine Approved Findings → Regression → Git/PR Integrity → Post-change Monitor.

## 경계
실제 runtime/build evidence의 주 owner는 P07. Canon freshness/legacy 전문 처리는 P02. 타 workstream PR은 read-only.

## 우선 공격 대상
5회를 checklist/lens로 축소, 5회에서 강제 종료, 가짜 finding, 동일 finding 중복 수정, unrelated branch/worktree 변경, evidence ceiling 위반.

## 검증/완료
focused adversarial/Git tests와 Part scope 검사. 1~5회 의무 전체 loop 후에도 finding이 있으면 6..N회 계속한다.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P03_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
