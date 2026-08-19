# P03 · Adversarial Quality, Refactoring & Git Integrity — Learning Log

> 이 로그는 해당 Part 작업에서 실제로 확인된 교훈만 축적한다. 추정·외부 snippet·미검증 Source는 학습 사실로 승격하지 않는다.

## 작업별 Learning Checkpoint

각 완료 작업마다 아래 형식으로 하나의 checkpoint를 추가한다. 새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`로 명시하고 억지 교훈을 만들지 않는다.

```yaml
date:
work_ref:
baseline_and_result:
what_worked: []
what_failed_or_was_rejected: []
reusable_lesson:
anti_pattern: []
affected_rules_skills_modules: []
evidence: []
reuse_scope: PART_ONLY | BASE_PROMOTION_CANDIDATE | PROJECT_ONLY | NO_NEW_REUSABLE_LESSON
promotion_candidate:
source_followup_questions: []
revisit_condition:
```

## Source Learning

- Source domains: CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.

### 2026-08-20 — Current-main P03 takeover after single-coordinator correction

```yaml
work_ref: "P03 coordinator takeover / PR #549; supersedes unfinished #537"
baseline_and_result: "current Base main c8de06cdd63ddcb9121d8321bf135eaea9e14f06 -> current-main selective P03 integration"
what_worked:
  - "Revalidated #537 as coordinator backlog instead of treating open PR state as another active worker."
  - "Reused only evidence-bounded P03 semantics on the latest main rather than merging the stale branch wholesale."
  - "Made FULL_LOOP_IS_NOT_A_REVIEW_LENS explicit in the P03 Skill so review lenses cannot be counted as separate full loops."
what_failed_or_was_rejected:
  - "The original #537 loop count is not reused because several entries described separate review lenses rather than repeated whole-lifecycle attacks."
  - "Blind old-branch merge was rejected because it could overwrite newer coordinator/open-PR policy."
reusable_lesson: "Open PR state and active ownership must be separated; takeover should selectively rehydrate unique semantic deltas onto current main and rerun current review evidence."
anti_pattern: "Counting scope/UX/CI as separate adversarial loops or treating stale branch bytes as current authority."
affected_rules_skills_modules:
  - "running-adversarial-review-and-refinement"
  - "synchronizing-local-and-github-state"
  - "Finding Validation / Git Sync & Isolation"
evidence:
  - "focused RED run 32272479838"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "current-owner-evidence takeover + selective current-main semantic rehydration"
source_followup_questions: []
revisit_condition: "Revisit if actual simultaneous workers become common or execution-surface evidence becomes machine-schema owned."
```
