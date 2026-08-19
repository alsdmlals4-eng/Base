# P0 Reusable Module Implementation Pilot

- 상태: `BASE_REFERENCE_IMPLEMENTED`
- 승인: 사용자 2026-08-20 — P0 1~4순위 실제 구현 및 프로젝트 Pilot
- 목적: `MODULE_CONTRACT_DEFINED`에서 실제 재사용 가능한 reference implementation + project adapter evidence로 승격한다.
- 상태 우선순위: 이 문서는 아래 P0 ID들의 **최신 구현 상태**를 기록하며, 2026-08-20 이전 `REUSABLE_MODULE_REGISTRY.md`의 `IMPLEMENTATION_NOT_BUILT` 표기는 해당 ID에 한해 이 문서가 갱신한다.

## 구현 대상과 현재 상태

| ID | 구현 | Pilot | 현재 판정 |
|---|---|---|---|
| `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR` | `tools/reuse_modules/data_schema_crossref_validator.py` | Urban Legend PR #208 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED · PROJECT_MERGED` |
| `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE` | `templates/reuse-modules/godot/grid_placement_rule_engine.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE` | `templates/reuse-modules/godot/candidate_draft_weight_engine.gd` | Omenward PR #197 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_CORE · PILOT_MERGE_BLOCKED_CONTROL_PLANE` |
| `RM-VIS-001 SEMANTIC_UI_SKIN_KIT` | `templates/reuse-modules/godot/semantic_ui_skin_kit.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |
| `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS` | `templates/reuse-modules/godot/gameplay_symbol_atlas.gd` | Switchy PR #154 | `BASE_REFERENCE_IMPLEMENTED · PROJECT_ADAPTER_VERIFIED_GUT · PILOT_MERGE_BLOCKED_UNRELATED_BASELINE` |

## 구현 경계

```text
small neutral core
→ thin project adapter
→ project-owned data / rules / visual language
→ deterministic or runtime test
→ adoption decision
```

- Base 공용 코어는 project canon, save state, runtime singleton을 소유하지 않는다.
- Python validator는 stdlib-only, deterministic, read-only다.
- Godot reference modules는 `RefCounted` 기반 순수 helper이며 Autoload/global mutable state를 도입하지 않는다.
- Visual module은 semantic role/symbol contract만 공유하고 실제 product art는 프로젝트 owner가 유지한다.
- Tetris는 진행 중 PR 보호로 `DEFERRED_CONCURRENCY`다.
- Ninja Survival은 프로젝트 phase gate 때문에 `DEFERRED_PHASE_GATE`다.
- Base PR #556의 P09 퇴역 작업 경로는 read-only이며 이 Pilot은 Tool Hub/QA Evidence Studio에 의존하지 않는다.

## TDD evidence

### Base

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

- test-only head `afa3fb2058bcef133b2203245864834cc19eeff1`에서 Godot headless RED를 관찰했다.
- production head `685c4b6b87f6bdb01ac78a6e8311ba2e17da15cf`의 `Validate Omenward Core`는 `SUCCESS`다.
- integer weight, exactly 3 candidates, seeded determinism, no free reroll 경계를 adapter가 보존한다.
- 병합은 보류한다. `Validate Base v9 Adoption Surface`의 adversarial gate가 일반 gameplay/test path를 허용하지 않는 control-plane path policy로 실패하며, Candidate Draft runtime 자체의 실패가 아니다. 이 Pilot에서 foreign workflow policy를 우회·완화하지 않는다.

## 5회 전체 적대적 개선 루프

1. **동시작업/권한 전체 공격** — Tetris open PR을 발견해 `DEFERRED_CONCURRENCY`, Ninja phase gate를 `DEFERRED_PHASE_GATE`, Base #556을 read-only로 격리했다. Pilot 소비자를 Switchy/Omenward/Urban으로 재구성했다.
2. **TDD/증거 전체 공격** — Base 첫 test-only Green이 실제 focused test 미소비임을 발견해 false Green으로 기각하고 영구 Evidence workflow를 실제 RED로 연결했다. 세 프로젝트도 test-first RED를 확인한 뒤 구현했다.
3. **공용화 과잉/의존성 전체 공격** — universal manager/autoload 대신 stdlib-only validator와 `RefCounted` helpers + thin adapter를 유지했다. project save/state/art/rules authority를 Base로 이동하지 않았다.
4. **프로젝트 회귀/실패 원인 전체 공격** — Urban 전체 matrix Green, Omenward Core Green, Switchy GUT Green을 확인했다. Switchy/Omenward의 나머지 실패는 각각 기존 baseline/control-plane 정책으로 분리하고 범위 밖 수정·강제 병합을 거부했다.
5. **신선도/비용/롤백/완료 전체 공격** — 추가 유료 서비스·API·runtime dependency가 없고, Base exact-head required workflows가 모두 Green이며, 각 Pilot이 sidecar/추가 파일 중심이라 revert가 가능함을 재확인했다. 인간 재미·몰입·최종 시각 품질은 `NOT_RUN`으로 유지한다.

```yaml
FULL_LOOP_COUNT: 5
BASE_VALID_MUST_FIX_REMAINING: 0
BASE_EXACT_HEAD_REQUIRED_CI: PASS
URBAN_PILOT: MERGED
SWITCHY_PILOT: VERIFIED_BUT_MERGE_BLOCKED_UNRELATED_BASELINE
OMENWARD_PILOT: VERIFIED_BUT_MERGE_BLOCKED_CONTROL_PLANE
TETRIS_PILOT: DEFERRED_CONCURRENCY
NINJA_PILOT: DEFERRED_PHASE_GATE
LOCAL_CLONE_EXECUTION: NOT_RUN_NETWORK_BLOCKED
HUMAN_PLAYER_EXPERIENCE: NOT_RUN
CLEAN_REVIEW_EXIT_BASE_SCOPE: true
```

## 완료 증거 ceiling

- reference source 존재만으로 프로젝트 재사용 PASS를 주장하지 않는다.
- project adapter 테스트가 실제 해당 프로젝트 CI/Godot에서 실행돼야 `PROJECT_ADAPTER_VERIFIED`다.
- 병합 차단된 Pilot의 sidecar 검증 성공을 전체 프로젝트 merge-ready와 혼동하지 않는다.
- player fun/immersion, 실제 최종 UI 아트 품질은 별도 release-near Vertical Slice/player evidence 없이는 `NOT_RUN`이다.

## Rollback

- Base: eventual squash merge를 revert하면 reference 구현과 상태 문서가 함께 원복된다.
- Urban Legend: merge `5c91f4ff8d88b3e00f66252ba6f566795f2e50a3`를 revert하면 validator/test/manifest 세 파일만 제거된다.
- Switchy/Omenward는 현재 Draft PR이므로 미병합 상태에서 branch를 폐기하면 runtime canon에 영향이 없다.
