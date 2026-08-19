# P06 · Godot, Runtime & Technical Toolchain — Learning Log

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

### 2026-08-19 · PR #536 — historical Godot adapter authority clarity

```yaml
date: 2026-08-19
work_ref: "Base PR #536 / P06 optimization"
baseline_and_result: >-
  Baseline df8ef644d30fc96456da23a5157e5efb61b620bb had a current HiGodot
  single-writer policy but retained Base live-editor documents still used active/current
  authority language. The P06 branch kept unique security/runtime evidence while making
  every retained legacy document explicitly historical and routing current writer/tool
  roles to HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md.
what_worked:
  - "TDD first: exact-head RED proved the four legacy documents lacked the required historical/current-authority boundary before production-document edits."
  - "Minimal authority-label normalization preserved stale-state, approval, rollback, identity, physical-evidence, and Pilot learning instead of deleting it."
  - "Current Godot/GUT/HiGodot/Hera primary/upstream checks supported keeping the existing author→test→live-QA responsibility split."
what_failed_or_was_rejected:
  - "Keeping the baseline unchanged was rejected because direct document entry could still present v2 as active authority."
  - "Deleting all legacy adapter artifacts was rejected because unique audit/regression consumers remain."
  - "Adding a new legacy-history Skill or provider-neutral Godot orchestration layer was rejected as routing/context overhead without a measured blocker."
  - "QA Evidence Studio cleanup was not absorbed because open PR #530 owns active changes there and is read-only to P06."
reusable_lesson: >-
  Retained legacy evidence must declare its non-authoritative status inside each directly
  discoverable document, name the current canonical authority, and have a regression
  guard against stale active-authority wording. An archive index alone is insufficient
  because search/direct links can bypass it.
anti_pattern:
  - "Preserve an obsolete implementation for audit but leave active/current wording inside the retained file."
  - "Treat archive retention as permission to keep a second writer route discoverable."
  - "Delete unique historical evidence before proving consumer/reference zero and an approved destination for reusable lessons."
affected_rules_skills_modules:
  - "HiGodot single persistent authoring authority"
  - "Existing Solution First"
  - "actual runtime evidence before PASS"
  - "evaluating-godot-assets-and-plugins-before-creation"
  - "Godot Authoring Authority"
  - "Editor / Runtime Adapter Evidence"
evidence:
  - "RED commit 6481375f2d75223e25d84533955f3fdac24df44e: 5 expected failures in Validate Base v9 Operating Contracts"
  - "GREEN run 32223186130: Base v9 contract job and adversarial gate PASS after authority normalization"
  - "docs/operations/godot-runtime/P06_OPTIMIZATION_2026-08-19.md"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >-
  Integration may generalize the direct-document legacy-status regression pattern for
  other Parts that retain obsolete implementation evidence. Do not promote P06-specific
  provider names or Godot rules into a generic policy.
source_followup_questions:
  - "Has the stable Godot/GUT compatibility baseline changed at the next engine or test-framework upgrade?"
  - "Has HiGodot's upstream architecture/security changed enough to require a new authoring-authority review?"
  - "Does Hera still need the same Base-local QA-only restriction at its next exact-pair upgrade?"
revisit_condition: >-
  Revisit on Godot major/minor upgrade, HiGodot authority change, GUT compatibility change,
  Hera role/security change, PR #530 QA-tooling resolution, or proven consumer-zero for
  the historical Base adapter surface.
```

## Source Learning

- Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
