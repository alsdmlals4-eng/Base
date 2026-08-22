# P0 Reusable Module Implementation Pilot

- 상태: `BASE_REFERENCE_IMPLEMENTED`
- 승인: 사용자 2026-08-20 — P0 1~4순위 실제 구현 및 프로젝트 Pilot; 2026-08-22 — `RM-TOOL-003` 남은 구현·다중 프로젝트 검증 진행
- 목적: `MODULE_CONTRACT_DEFINED`에서 실제 재사용 가능한 reference implementation + project adapter/evidence로 승격한다.
- 상태 우선순위: 이 문서는 아래 P0 ID들의 **최신 구현 상태**를 기록하며, 이전 `REUSABLE_MODULE_REGISTRY.md` 또는 분야 문서의 `IMPLEMENTATION_NOT_BUILT` 표기는 해당 ID에 한해 이 문서와 각 전용 implementation pilot이 갱신한다.
- `RM-TOOL-003` 상세 상태 owner: `docs/knowledge/game-development/reuse/RM_TOOL_003_IMPLEMENTATION_PILOT.md`.

## 구현 대상과 현재 상태

| ID | 구현 | Pilot | 현재 판정 |
|---|---|---|---|
| `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR` | `tools/reuse_modules/data_schema_crossref_validator.py` | Urban Legend PR #208 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED · PROJECT_MERGED` |
| `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE` | `templates/reuse-modules/godot/grid_placement_rule_engine.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE` | `templates/reuse-modules/godot/candidate_draft_weight_engine.gd` | Omenward PR #198 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_CORE · PROJECT_MERGED` |
| `RM-VIS-001 SEMANTIC_UI_SKIN_KIT` | `templates/reuse-modules/godot/semantic_ui_skin_kit.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS` | `templates/reuse-modules/godot/gameplay_symbol_atlas.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR` | `tools/reuse_modules/balance_scenario_batch_simulator.py` | Omenward #202 / Blacksmith #181 / Ninja #24 | `BASE_REFERENCE_IMPLEMENTED · MULTI_PROJECT_READ_ONLY_CONTRACT_EVIDENCE · PROJECT_PRS_PENDING_MERGE` |

## 구현 경계

```text
small neutral core
→ thin project adapter / project-owned deterministic record producer
→ project-owned data / rules / visual language
→ deterministic or runtime evidence
→ adoption decision
```

- Base 공용 코어는 project canon, save state, runtime singleton을 소유하지 않는다.
- Python validator와 balance analyzer는 stdlib-only, deterministic/read-only 경계를 유지한다.
- `RM-TOOL-003`은 게임별 simulator가 아니라 project-supplied run record의 공통 후처리 kernel이다.
- Godot reference modules는 `RefCounted` 기반 순수 helper이며 Autoload/global mutable state를 도입하지 않는다.
- Visual module은 semantic role/symbol contract만 공유하고 실제 product art는 프로젝트 owner가 유지한다.
- Tetris는 진행 중 PR 보호로 `DEFERRED_CONCURRENCY`다.
- Ninja Survival의 product Phase gate는 유지된다. 2026-08-22 RM-TOOL-003 Pilot은 legacy actuator docs-only evidence이며 T01~T14 실행 순서를 바꾸지 않는다.
- Base PR #556의 P09 퇴역 작업 경로는 read-only이며 이 Pilot은 별도 Tool Hub/QA Evidence Studio에 의존하지 않는다.

## TDD evidence

### Base · 기존 P0

1. test-only head는 Game Project OS가 새 focused test를 실행하지 않아 `FALSE_GREEN`으로 기각했다.
2. 영구 P04 Evidence workflow에 실제 소비 경로를 연결한 뒤 run `32288042416`에서 **135 tests / 의도한 3개 실패**를 관찰했다. 실패 원인은 구현 파일 부재였다.
3. reference 구현 후 exact head `94d546ddddc475a14d30a61062b480fa6da48dbc`에서:
   - Evidence-Based Game Development Knowledge `32288276303`: `SUCCESS`
   - Base v9 Operating Contracts `32288276325`: `SUCCESS`
   - Game Project Operating System `32288276336`: `SUCCESS`

### Urban Legend · RM-TOOL-001

- test-only head에서 core baseline RED를 관찰했다.
- production head `005d7fdbf0e69aa151cb0f328b7a1156ca1624b9`:
  - Validate Project Base Adapter: `SUCCESS`
  - Validate core and documentation baseline: `SUCCESS`
  - Validate full matrix: `SUCCESS`
  - Validate ANNUAL-MVP-001: `SUCCESS`
- protected `data/episodes/*`, save/campaign/economy/ending rules, 기존 ID, `scripts/core/game_state.gd`, `project.godot`은 수정하지 않았다.
- PR #208 squash merge: `5c91f4ff8d88b3e00f66252ba6f566795f2e50a3`.

### Switchy · RM-SYS-001 / RM-VIS-001 / RM-VIS-002

- test-only head `492c0258a42c5982176f95c516bccc404f1b0e1e`에서 GUT/Project Contract RED를 관찰했다.
- production head `bdcd0d67ce0e509ce75d62f960650ee17fe9cae2`에서 **GUT 9.7.1 Tests SUCCESS** 및 Thin Adapter Migration SUCCESS로 새 grid/UI/symbol tests가 실제 Godot에서 통과했다.
- 병합은 보류한다. 전체 Project Contract에는 이번 변경과 무관한 기존 `godot-ai` 3.1.3 기대 vs 3.1.4 실제 버전 불일치가 있고, 별도 Godot regression에는 기존 game-over responsive/overlay lifecycle 실패가 남아 있다.
- LIFO/cargo/route/time/scoring/save/map/controls와 기존 product PNG/manifest는 변경하지 않았다.

### Omenward · RM-SYS-003

- stale PR #197을 재사용/수정하지 않고 current-main fresh integration PR #198을 사용했다.
- PR #198 exact head `0196ff79a3dd7c5cf25685d48a8bb337d2fbebec`:
  - `Validate Base v9 adoption` run `32364532263`: `SUCCESS`
  - `Validate Omenward Core` run `32364532205`: `SUCCESS`
- integer weight, exactly 3 candidates, seeded determinism, no free reroll 경계를 adapter가 보존한다.
- product authority file 변경 없이 squash merge `67487c932cc883db95da7bc852f4eb33883f0052`로 main에 반영됐다.
- stale PR #197은 superseded/closed-unmerged history로만 취급한다.

### RM-TOOL-003 · Base kernel

- test-first contract에서 구현 파일 부재 RED를 확인한 뒤 stdlib-only analyzer를 작성했다.
- 이후 전체 구현 범위를 5회 공격해 다음 실제 결함을 수정했다.
  1. `NaN/Infinity` 통계 오염 → finite-only.
  2. 동일 failure tag 중복 시 rate > 1 → run별 dedupe + denominator 명시.
  3. median-only goal seek가 volatile 후보를 과대평가 → inside-target share 추가.
  4. `int()` seed coercion이 identity를 붕괴 → strict JSON integer/schema.
  5. report metadata alias가 input을 간접 수정 가능 → deep-copy 반환.
- 회귀 owner:
  - `tests/test_balance_scenario_batch_simulator.py`
  - `tests/test_balance_scenario_batch_schema.py`
  - `tests/test_balance_scenario_batch_read_only.py`

### Omenward · RM-TOOL-003 PR #202

- changed paths: `docs/analysis/balance/`의 Markdown + JSON 두 파일만 추가.
- open canon reconciliation PR #201과 changed-path 교집합 0.
- 10,000 deterministic seed planning-envelope Pilot에서 normalization 이후 raw envelope 밖으로 이동하는 표본을 W1 `1.24%`, W2 `1.93%`, Final `3.44%` 관찰했다.
- `Validate Base v9 adoption` run `32539884644`: `SUCCESS`.
- `Validate Project Core Documentation` run `32539884555`와 `Validate Omenward GDD Sheet Adoption` run `32539884696`은 current main의 기존 canon/legacy-validator drift로 실패했다. 로그는 `PROJECT_CORE`, `CURRENT_IMPLEMENTATION_STATUS`, historical C1/Vertical Slice marker 불일치를 지목하며 이번 두 sidecar 파일과 무관하다. 이 범위는 open PR #201이 소유하므로 #202에서 우회·수정하지 않는다.
- runtime/human/final numerics는 계속 `NOT_RUN/NOT_APPROVED`.

### Blacksmith · RM-TOOL-003 PR #181

- 기존 `tools/simulate_enhancement_balance.py`가 `EnhancementSession` 규칙을 반영하는 project simulator owner임을 확인했다.
- Base가 enhancement rule을 재구현하지 않고 optional deterministic record → shared post-processor 경계만 정의했다.
- 2개 docs/evidence 파일만 추가했고 protected product path 변경은 0.
- exact head `cb5dc9509769f3ae4ea8436718bfe0b2c917b115`에서 다음이 모두 `SUCCESS`:
  - Validate Project Base Adapter `32539891538`
  - Validate Base v9 adoption `32539891528`
  - Validate Thin Adapter Migration `32539891561`
  - Validate Blacksmith BCA Adoption `32539891585`
  - PR validation `32539891645`

### Ninja Survival · RM-TOOL-003 PR #24

- current legacy `WaveSpawner` default `batch_size=2`, `max_active_enemies=8`를 initial active `0..8` 전부 열거했다.
- enabled/disabled variant 모두 cap violation 0; disabled spawn count는 항상 0.
- `data/stages/`가 `.gitkeep`뿐임을 확인해 DEC-026 신규 balance는 생성/추정하지 않았다.
- 2개 docs/evidence 파일만 추가했고 runtime/data/test 변경은 0.
- exact head `6b4cb0bfc48d9029f209ea9e9d4f0d0692220722`의 GUT run `32539901612`: `SUCCESS`.

## 기존 P0 5회 전체 적대적 개선 루프

1. **동시작업/권한 전체 공격** — Tetris open PR을 발견해 `DEFERRED_CONCURRENCY`, Ninja phase gate를 `DEFERRED_PHASE_GATE`, Base #556을 read-only로 격리했다. Pilot 소비자를 Switchy/Omenward/Urban으로 재구성했다.
2. **TDD/증거 전체 공격** — Base 첫 test-only Green이 실제 focused test 미소비임을 발견해 false Green으로 기각하고 영구 Evidence workflow를 실제 RED로 연결했다. 세 프로젝트도 test-first RED를 확인한 뒤 구현했다.
3. **공용화 과잉/의존성 전체 공격** — universal manager/autoload 대신 stdlib-only validator와 `RefCounted` helpers + thin adapter를 유지했다. project save/state/art/rules authority를 Base로 이동하지 않았다.
4. **프로젝트 회귀/실패 원인 전체 공격** — Urban 전체 matrix Green, Omenward Core Green, Switchy GUT Green을 확인했다. Switchy/Omenward의 당시 나머지 실패는 기존 baseline/control-plane 정책으로 분리하고 범위 밖 수정·강제 병합을 거부했다.
5. **신선도/비용/롤백/완료 전체 공격** — 추가 유료 서비스·API·runtime dependency가 없고, Base exact-head required workflows가 모두 Green이며, 각 Pilot이 sidecar/추가 파일 중심이라 revert가 가능함을 재확인했다. 인간 재미·몰입·최종 시각 품질은 `NOT_RUN`으로 유지한다.

## RM-TOOL-003 구현 5회 전체 적대적 개선 루프

1. **수치 유효성** — finite-only metric/target.
2. **비율 의미** — failure run dedupe와 choice-event denominator 고정.
3. **후보 추천 왜곡** — median + actual target-share로 goal-seek 보강.
4. **재현 identity/schema** — seed 및 container fail-closed.
5. **read-only/authority** — input alias 차단, project rule owner 분리, GUI 자동 승격 거부.

```yaml
FULL_LOOP_COUNT_EXISTING_P0: 5
FULL_LOOP_COUNT_RM_TOOL_003: 5
BASE_VALID_MUST_FIX_REMAINING_BEFORE_CI: 0
RM_TOOL_003_BASE_KERNEL: BASE_REFERENCE_IMPLEMENTED
RM_TOOL_003_OMENWARD: SIDECAREVIDENCE_BASE_V9_PASS_EXISTING_DOC_DRIFT_SEPARATED
RM_TOOL_003_BLACKSMITH: FIVE_WORKFLOWS_SUCCESS
RM_TOOL_003_NINJA: GUT_SUCCESS
RM_TOOL_003_PROJECT_PRS: OPEN_UNMERGED_READ_ONLY
RM_TOOL_003_TOOL_HUB_GUI: DEFER
LOCAL_CLONE_EXECUTION: NOT_RUN_NETWORK_BLOCKED
HUMAN_PLAYER_EXPERIENCE: NOT_RUN
PRODUCT_BALANCE_PASS: NOT_CLAIMED
```

## 완료 증거 ceiling

- reference source 존재만으로 프로젝트 재사용 PASS를 주장하지 않는다.
- project adapter/test가 실제 해당 프로젝트 CI/Godot에서 실행돼야 runtime 관련 `PROJECT_ADAPTER_VERIFIED`를 주장한다.
- docs-only Pilot의 sidecar 분석 성공을 전체 프로젝트 merge-ready/product balance와 혼동하지 않는다.
- Omenward #202의 두 baseline validator failure는 별도 #201 영역이며 이번 Pilot에서 수정하지 않는다.
- player fun/immersion, 실제 최종 UI 아트 품질, final product balance는 별도 release-near Vertical Slice/player evidence 없이는 `NOT_RUN/NOT_APPROVED`다.
- `RM-TOOL-003`의 goal-seek output은 non-authoritative candidate ranking이며 project data를 자동 변경하지 않는다.

## Rollback

- Base: eventual squash merge를 revert하면 reference analyzer/test/template와 `RM_TOOL_003_IMPLEMENTATION_PILOT.md` 상태 문서를 함께 원복한다.
- Urban Legend: merge `5c91f4ff8d88b3e00f66252ba6f566795f2e50a3`를 revert하면 validator/test/manifest 세 파일만 제거된다.
- Omenward RM-SYS-003: merge `67487c932cc883db95da7bc852f4eb33883f0052`를 revert하면 isolated vendor/reference adapter scope만 제거된다.
- Switchy의 기존 Pilot은 현재 미병합 보호 상태를 유지한다.
- Omenward #202 / Blacksmith #181 / Ninja #24는 docs-only open PR이므로 미병합 상태에서 폐기하면 product/runtime canon에 영향이 없다.
