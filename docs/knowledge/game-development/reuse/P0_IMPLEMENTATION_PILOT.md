# P0 Reusable Module Implementation Pilot

- 상태: `BASE_REFERENCE_IMPLEMENTED`
- 최신 정리: 2026-08-22 KST
- 목적: `MODULE_CONTRACT_DEFINED` 후보 중 실제 reference implementation과 project evidence가 존재하는 P0/P1 재사용 단위를 **현재 상태만** 요약한다.
- 상세 역사·중간 실패는 Git history와 각 implementation pilot/evidence가 소유한다.

## 현재 구현 상태

| ID | 구현 | Project evidence | 현재 판정 |
|---|---|---|---|
| `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR` | `tools/reuse_modules/data_schema_crossref_validator.py` | Urban Legend PR #208 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED · PROJECT_MERGED` |
| `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE` | `templates/reuse-modules/godot/grid_placement_rule_engine.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE` | `templates/reuse-modules/godot/candidate_draft_weight_engine.gd` | Omenward PR #198 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_CORE · PROJECT_MERGED` |
| `RM-VIS-001 SEMANTIC_UI_SKIN_KIT` | `templates/reuse-modules/godot/semantic_ui_skin_kit.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS` | `templates/reuse-modules/godot/gameplay_symbol_atlas.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR` | `tools/reuse_modules/balance_scenario_batch_simulator.py` | Omenward #202 / Blacksmith #181 / Ninja #24 | `BASE_REFERENCE_IMPLEMENTED · MULTI_PROJECT_READ_ONLY_CONTRACT_EVIDENCE · PROJECT_PRS_MERGED_MAIN_READBACK` |

## 공용 구현 경계

```text
small neutral core
→ thin project adapter / project-owned deterministic record producer
→ project-owned data / rules / visual language
→ deterministic/runtime evidence
→ adoption decision
```

- Base 공용 코어는 project canon, save state, runtime singleton을 소유하지 않는다.
- 실제 product art/rules/numerics는 프로젝트 owner가 유지한다.
- reference implementation 존재는 프로젝트 adoption이나 player-experience PASS가 아니다.
- 같은 기능을 새로 만들기 전에 `REUSABLE_MODULE_REGISTRY.md`와 실제 reference implementation을 먼저 검색한다.

## 기존 P0 project adoption freshness

- Omenward PR #198: `RM-SYS-003` current-main integration, squash merge `67487c932cc883db95da7bc852f4eb33883f0052`.
- stale Omenward PR #197은 superseded/closed-unmerged history이며 current Pilot이 아니다.
- Switchy PR #154는 GUT-verified 범위와 별도 기존 baseline blocker를 분리한다.

## RM-TOOL-003 상세 상태

상세 owner: `docs/knowledge/game-development/reuse/RM_TOOL_003_IMPLEMENTATION_PILOT.md`.

```text
project-owned simulator / deterministic adapter
→ project-supplied run record
→ Base read-only analyzer
→ JSON report
→ GPT/human review
→ 필요 시 Notion human summary
→ project decision owner
```

현재 검증:

- Omenward PR #202: squash merge `b46374e511447cb531709a5d56f3ba9a6e4dcc8d`.
- Blacksmith PR #181: squash merge `307126031956bf5345da20a7b0c4466aa26c9b94`.
- Ninja Survival PR #24: squash merge `46c5e151808f2481cc20be0003dd03866133ae49`.
- Registry reference implementation freshness: Base PR #591 merge `e37c4e72344662b344f62a442dd2f7f39dbad34e`.

```yaml
RM_TOOL_003_BASE_KERNEL: BASE_REFERENCE_IMPLEMENTED_MERGED
RM_TOOL_003_PROJECT_PRS: ALL_THREE_MERGED_MAIN_READBACK
RM_TOOL_003_REGISTRY: REFERENCE_IMPLEMENTATION_EXISTS_ALIGNED_BY_BASE_591
RM_TOOL_003_TOOL_HUB_GUI: RETIRED_NOT_ACTIVE_ROUTE
HUMAN_PLAYER_EXPERIENCE: NOT_RUN
PRODUCT_BALANCE_PASS: NOT_CLAIMED
```

`RM_TOOL_003_TOOL_HUB_GUI: RETIRED_NOT_ACTIVE_ROUTE`는 현재 사용자 결정과 Base 퇴역 정책을 따른다. CLI/JSON으로 목적을 충족하므로 Tool Hub·별도 Balance GUI·외부 HTML·새 local management UI를 자동 재검토 후보로 두지 않는다.

## Evidence ceiling

- `REFERENCE_IMPLEMENTATION_EXISTS != PROJECT_ADOPTED`
- docs-only sidecar 분석 성공은 product balance PASS가 아니다.
- goal-seek output은 non-authoritative candidate ranking이다.
- 사람 플레이를 실행하지 않았으면 재미·난이도·몰입은 `NOT_RUN`이다.
- Switchy처럼 병합 blocker가 남은 Pilot은 검증된 부분과 merge-ready 상태를 분리한다.

## Rollback / freshness

- Base reference의 rollback은 해당 reference merge와 Registry freshness claim을 함께 정합화한다.
- 프로젝트 Pilot은 각 project PR을 독립 revert할 수 있다.
- project-owned simulator와 기존 balance canon은 Base reference rollback과 독립적이다.
- 폐기 Tool Hub/UI 경로의 과거 문서는 active authority가 아니며 필요 시 Git history에서만 조사한다.