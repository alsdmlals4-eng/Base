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
