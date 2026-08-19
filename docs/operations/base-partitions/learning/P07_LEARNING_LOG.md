# P07 · Platform, Release & Execution Validation — Learning Log

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

### 2026-08-19 — P07 evidence freshness and validation-consumption audit

```yaml
date: 2026-08-19
work_ref: PR #542 / P07_OPTIMIZATION_AUDIT_2026-08-19
baseline_and_result: >-
  Baseline df8ef644d30fc96456da23a5157e5efb61b620bb retained correct runtime/device/human/submission evidence ceilings,
  but the merged PC/Android delivery guide still described its Base contract as PROPOSED_IN_DRAFT_PR.
  The P07-owned publication marker was corrected to ACTIVE_IN_MAIN, the regression was attached to an existing actively consumed P07 platform test,
  and cross-Part dependency/CI-topology findings were left as CP0 requests rather than written outside P07.
what_worked:
  - resolve latest main and pin the exact baseline before evaluating lifecycle claims
  - trace a rule to its actual consumer/test instead of normalizing status strings by name alone
  - recheck mutable platform policy against first-party sources without promoting project/runtime evidence
  - place the regression in an already consumed P07 test surface after checking Required CI consumption
  - preserve P01 and CP0 write ownership while recording precise cross-Part requests
what_failed_or_was_rejected:
  - leaving a merged current-main contract marked PROPOSED_IN_DRAFT_PR
  - treating existence of a new test file as proof that Required CI executes it
  - creating a new broad compliance/release Skill for a one-line lifecycle defect
  - creating a new global evidence-status schema that would flatten specialized backend/platform/runtime meanings
  - duplicating P01-owned project-operation evidence templates inside P07
  - directly editing the Manifest or .github workflows from a P07 worker
reusable_lesson: >-
  Publication lifecycle and execution evidence are separate axes: a contract may be ACTIVE_IN_MAIN while project pilot,
  physical-device, human-usability, build or store-submission evidence remains NOT_RUN. New regression tests also need consumption proof;
  repository presence alone is not CI execution evidence.
anti_pattern:
  - stale draft/proposed lifecycle markers surviving merge into current canon
  - evidence-state inflation caused by conflating merged documentation with runtime/device/submission proof
  - CI coverage claims based on filenames rather than the workflow command that actually executes them
  - solving a cross-Part dependency by copying the dependency into the consumer Part
  - adding a new Skill or schema before proving a distinct responsibility and consumer
affected_rules_skills_modules:
  - Evidence ceiling
  - LATEST_EXACT_HEAD_ONLY
  - runtime/build proof separate from planning approval
  - platform official-source-first
  - reviewing-and-validating-project-changes
  - Change Validation
  - Evidence Ledger
  - Platform/Store Review
  - Build/Size/Release
evidence:
  - docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md
  - tests/test_platform_review_asset_rights_reference_production.py
  - docs/operations/release-validation/P07_OPTIMIZATION_AUDIT_2026-08-19.md
  - PR #542
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >-
  Integration should consider a shared rule that current canon must not retain stale proposal/draft publication markers,
  and that a claimed regression test must name the workflow/local command that consumes it.
source_followup_questions:
  - Should P07 explicitly declare P01 project-operation evidence templates as a read-only dependency in the Partition Manifest?
  - Should Required CI expose a stable P07 suite entrypoint, or should the Manifest state that its Part validation command is intentionally local-only?
revisit_condition: >-
  Revisit if stale lifecycle markers recur after merge, P01/P07 evidence-template coupling grows,
  or newly added P07 tests repeatedly fail to enter the intended validation surface.
```

## Source Learning

- Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
