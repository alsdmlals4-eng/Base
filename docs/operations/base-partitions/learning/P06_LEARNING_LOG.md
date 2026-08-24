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

### 2026-08-24 · BCP-2026-029 / PR #646 — Cocos machine-interface pattern extraction

```yaml
date: 2026-08-24
work_ref: "BCP-2026-029 / Base PR #646"
baseline_and_result: >-
  Approved main kept Godot and the HiGodot/GUT/Hera authority split but did not yet have
  a reusable game-engine machine-boundary contract tying exact project identity, typed
  operations, shared CLI/MCP core semantics, behavior E2E, and structured evidence
  together. The implementation branch added that provider-neutral contract and a dated
  COCOS 4/Cocos CLI case without adopting Cocos runtime, Node/TypeScript, another MCP
  writer, or another management surface.
what_worked:
  - "Formal BCP lifecycle separated proposal, approval, and implementation after the first draft exposed the governance omission."
  - "TDD RED on the approved latest main proved the new contract was absent before documentation implementation."
  - "GREEN run 32696469871 passed Base integrity/release checks and 385 focused tests with one pre-existing environment skip, including HiGodot single-authority and the three new machine-boundary regressions."
  - "Provider-specific syntax was kept in the dated case while reusable identity/core/schema/E2E/evidence invariants were routed through existing Base owners."
what_failed_or_was_rejected:
  - "The pre-BCP draft PR #642 was closed unmerged after adversarial review found that active Base paths had been changed before formal proposal lifecycle completion."
  - "COCOS 4 engine migration was rejected because the observed 4.x line was still Alpha and no target-project evidence justified replacing Godot."
  - "Cocos CLI/MCP, Node/TypeScript dependencies, a new Tool Hub, and a second Godot persistent writer were rejected as unnecessary authority/dependency expansion."
  - "MCP connectivity/tool discovery was rejected as a substitute for representative project/result/evidence behavior E2E."
reusable_lesson: >-
  When another engine or tool demonstrates a useful AI-native interface, separate the
  provider from the invariant: preserve the current engine and writer authority unless
  migration evidence exists, and extract exact identity, typed operation, shared adapter
  core, behavior E2E, and structured evidence as reusable machine-boundary contracts.
anti_pattern:
  - "Treat a fashionable engine's CLI/MCP surface as a reason to migrate the production engine."
  - "Add a second writer because its transport is convenient."
  - "Report MCP handshake or tool listing as proof that a game-engine action succeeded."
  - "Force schema code generation on tiny tools when mechanical drift validation is sufficient."
affected_rules_skills_modules:
  - "Existing Solution First"
  - "HiGodot single persistent authoring authority"
  - "Implementation Reality Gate"
  - "BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE"
  - "AI_GAME_ENGINE_MACHINE_BOUNDARY"
  - "TOOL_INTERFACE_SURFACE_SELECTION"
evidence:
  - "BCP submission PR #643 merged at 5672fb1bba267b9346c1938be8c5ac7a838256c4"
  - "BCP approval PR #644 merged at 6d884218c4294608c8fe2ca9176420caad4eaae6"
  - "Formal implementation RED run 32696165900: expected machine-boundary contract failures"
  - "Formal implementation GREEN run 32696469871: integrity/release PASS; 385 tests OK (skipped=1)"
  - "docs/knowledge/cases/COCOS_AI_NATIVE_ENGINE_INTERFACE_CASE.md"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >-
  Realized by BCP-2026-029 through the existing benchmarking and capability-composition
  owners. Do not create a new Skill, engine adapter, or provider dependency solely for
  this lesson.
source_followup_questions:
  - "Has COCOS 4 moved from Alpha to a stable contract that materially changes the benchmark?"
  - "Do current Godot machine-facing owners expose schema/type drift or behavior-E2E gaps in a real project?"
  - "Can a smaller CLI/programmatic path solve a future machine-operation need without adding MCP?"
revisit_condition: >-
  Revisit when a current Godot tool/adapter is materially revised, when a representative
  project exposes project-identity/schema/E2E failure, or when COCOS 4/CLI reaches a
  materially different stable interface. None of these conditions alone authorize an
  engine migration.
```

## Source Learning

- Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.