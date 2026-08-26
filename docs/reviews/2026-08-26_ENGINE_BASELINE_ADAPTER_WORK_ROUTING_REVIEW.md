# Engine Baseline / Adapter / Work Routing — Adversarial Review

## Scope

2026-08-26 사용자 승인에 따라 다음 변경을 current Base에 적용하기 전 전체 방향을 다섯 번 다시 공격했다.

- existing portfolio keeps current Godot projects;
- stable engine baseline and canary-only promotion;
- engine-neutral product-implementation core above current Godot adapter;
- Chat / Work / Codex task-shape routing;
- Notion human-facing canon and repository runtime truth preserved.

Runtime/game migration은 이번 검토 범위가 아니다.

## Evidence before review

- TDD RED: first PR state intentionally lacked the new policy/P06/P08 terms.
- First GREEN attempt exposed one real compatibility regression in existing `tests/test_p08_ai_operations_contract.py`: the P08 rewrite had removed the exact legacy Godot surface tokens `GDScript/product code` and `Scene/Resource/Autoload/runtime wiring`.
- Root cause: the generic Codex owner wording replaced rather than specialized the existing Godot vocabulary.
- Correction: generic `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER` now sits above, while the existing Godot strings remain explicit compatibility surfaces.
- Base Partition and Evidence Knowledge checks passed during the correction cycle; Base v9 returned GREEN after the compatibility vocabulary was restored.
- Notion P06/P08 destination readback confirmed the new top-level routing and active P08 flow.
- Pre-existing PR #660 paths remain untouched.

## Full Loop 1 — Authority / Canon attack

**Attack:** `ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE` or Work could become a third project authority and compete with Notion/GitHub/project canon.

**Finding:** Must-fix unless the neutral layer is limited to execution invariants and Work is explicitly non-canonical.

**Correction/defense:** `ENGINE_BASELINE_AND_ADAPTER_POLICY.md` assigns human-facing planning/visual canon to Notion and structured/code/test/runtime truth to repository. Work is `WORK_EXECUTION_SURFACE_NOT_CANON`. Engine selection comes from `ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON`.

**Result:** CLEAN.

## Full Loop 2 — Existing Godot compatibility attack

**Attack:** Genericizing P08 could silently break existing Godot handoff/test consumers even though no migration was approved.

**Finding:** REAL REGRESSION. Existing focused CI failed because exact compatibility strings disappeared.

**Correction:** Restored `GDScript/product code` and `Scene/Resource/Autoload/runtime wiring`; retained `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER` as the current Godot specialization instead of deleting/renaming it. HiGodot/GUT/Hera remain current adapter responsibilities.

**Result:** CLEAN after correction; this loop produced the concrete defect caught by CI.

## Full Loop 3 — Engine update policy attack

**Attack:** `NO_AUTOMATIC_LATEST_FOLLOW` could turn into indefinite version neglect and create security/store/platform debt.

**Finding:** A freeze-without-revisit policy would be unsafe.

**Correction/defense:** Update triggers explicitly include blocker/critical defect, security, required platform/store change, plugin/SDK compatibility, measured productivity benefit, and support-end risk. Promotion still requires isolated canary, compatibility/regression/runtime/export evidence, rollback, and planned maintenance window.

**Result:** CLEAN.

## Full Loop 4 — Work overreach attack

**Attack:** Because Work can perform long multi-step tasks across connected apps/files, it could absorb Codex product implementation or replace persistent project truth.

**Finding:** Must preserve owner boundaries independent of UI surface.

**Correction/defense:** `CHAT_QUICK_DISCUSSION_DEFAULT` handles short conversational work; `WORK_LONG_MULTISTEP_NONCODING_DEFAULT` handles GPT-owned planning/research/review/Base/Notion/document work; `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER` begins at actual software/game product implementation. Work output must be written/read back through existing Notion/GitHub owners.

**Result:** CLEAN.

## Full Loop 5 — Migration overreach / MCP bias attack

**Attack:** Unity's stronger official MCP/CLI or future engine AI features could be mistaken for sufficient evidence to migrate the current portfolio.

**Finding:** MCP transport/tool availability is not total-development-cost evidence.

**Correction/defense:** `ENGINE_MIGRATION_REQUIRES_SEPARATE_REALITY_GATE` compares actual Scene/script/test/build/tooling dependencies, 2D/3D production speed, agent behavior E2E, platform/build ecosystem, licensing, migration loss, and long-run productivity. `MCP_IS_ADAPTER_CAPABILITY_NOT_ENGINE_SELECTION_AUTHORITY` prevents MCP alone from deciding engine adoption. Unity remains a future new/low-implementation canary candidate only.

**Result:** CLEAN.

## Cross-project impact review

Existing project engine/runtime canon remains unchanged, so mass-editing project repositories would create churn without player or implementation value. Each existing project continues using its current Godot baseline and project-specific Godot authority. The new policy changes **how future engine upgrades/migrations are decided**, not current runtime behavior.

## Open-workstream review

PR #723 changes only:

- new engine baseline policy;
- P06/P08 Base partition docs;
- design/plan/review evidence;
- focused contract tests.

It does not modify PR #660-owned `docs/CAPABILITY_COMPOSITION_MAP.md` or `docs/DOCUMENTATION_MAP.md`, and does not mutate other pre-existing open PRs.

## Evidence ceiling

This review can support:

- Base policy/workflow correction;
- stable baseline/canary decision contract;
- Chat/Work/Codex routing contract;
- current Godot adapter compatibility preservation;
- Notion P06/P08 semantic alignment.

It cannot support:

- Unity migration readiness;
- Unity-vs-Godot implementation benchmark PASS;
- any project engine upgrade;
- Godot/Unity runtime performance claim;
- physical device or human gameplay PASS.

## Final disposition

`ADOPT_AND_CORRECT`.

The long-term efficient state is **engine-neutral decision/implementation invariants + current Godot adapter + stable pinned production baselines + canary-only engine changes + Chat/Work/Codex routing by task shape**. Re-open the engine decision only when the policy's explicit migration/revisit conditions produce new evidence.
