# Gameplay & Content Reusable Modules

이 문서는 `REUSABLE_MODULE_REGISTRY.md`의 gameplay/content/narrative 후보를 **프로젝트 고유 표현과 분리된 계약**으로 정리한다.

기본 구현 원칙:

```text
neutral contract
→ project adapter
→ project-specific data/content/visual language
→ PoC
→ release-near Vertical Slice when player experience is claimed
```

공용 module은 프로젝트 코어를 소유하지 않는다. 하나의 거대 `UniversalGameManager`로 합치지 않고, 입력/출력이 좁은 작은 계약을 우선한다.

---

## RM-SYS-001 · GRID_PLACEMENT_RULE_ENGINE

**목적:** 격자 위에서 조각을 배치·회전·이동할 때 매 프로젝트마다 좌표/충돌/preview/합법성 검사를 다시 만들지 않는다.

1차 프로젝트: `TETRIS`, `NINJA_SURVIVAL`, `SWITCHY`.

```yaml
module: GRID_PLACEMENT_RULE_ENGINE
inputs:
  - board_bounds
  - occupied_cells
  - piece_footprint
  - anchor
  - rotation
  - placement_context
rules:
  - transform footprint into board coordinates
  - reject out-of-bounds cells
  - reject or classify overlap by project policy
  - run project-specific placement predicates
outputs:
  - valid | invalid
  - occupied_target_cells
  - reason_codes
  - preview_payload
non_responsibilities:
  - scoring
  - combat effects
  - project art
  - inventory ownership
```

### Adapter 예

- TETRIS: 낙하 조각/board/line-clear 규칙을 별도 adapter에서 소비.
- NINJA_SURVIVAL: 가방 footprint, 90도 회전, adjacency, 특수 overlap 규칙을 adapter에서 소비.
- SWITCHY: track tile footprint, 금지 구역, 교체·회전, 연결성 규칙을 adapter에서 소비.

`MODULE_CONTRACT_DEFINED`; shared runtime은 `IMPLEMENTATION_NOT_BUILT`.

---

## RM-SYS-002 · PHASED_SESSION_STATE_MACHINE

**목적:** BUILD/RUN, 조사/결과, 전투/REST처럼 명시적 phase가 있는 프로젝트의 전환 규칙·pause/timer 정책을 공통 형식으로 만든다.

```yaml
phase_id:
allowed_actions: []
entry_guard:
entry_effects: []
exit_guard:
exit_effects: []
timers:
  session_clock:
  combat_clock:
  phase_local_clock:
pause_policy:
commit_boundary:
recovery_target:
```

적용 seed:
- SWITCHY `BUILD → RUN → RESULT`
- NINJA_SURVIVAL `COMBAT → REST/WORKBENCH → COMMIT → COMBAT`
- GRIMOIRE `DRAW → CIRCUIT → TARGET/USE → RESULT`
- TETRIS active-board pause vs enemy Combat Clock
- URBAN_LEGEND day/week progression
- OMENWARD preparation/deployment/auto battle/result
- MY_LITTLE_BOAT voyage/session phases

공통 FSM은 **시간의 의미를 통일하지 않는다**. 각 clock의 진행/정지 정책을 data로 명시하는 것이 목적이다.

---

## RM-SYS-003 · CANDIDATE_DRAFT_WEIGHT_ENGINE

**목적:** “N개 후보 중 선택”, 확률 pool, rarity, 조건부 후보, pity/readiness, reroll/lock을 하나의 후보 생성 계약으로 추상화한다.

```yaml
request:
  pool_id:
  candidate_count:
  current_state:
  seed:
filters:
  eligibility:
  duplicate_policy:
weights:
  base_weight:
  state_modifiers:
  pity_or_readiness:
post_generation:
  reroll_budget:
  lockable_slots:
outputs:
  candidates:
  generation_reason_trace:
```

1차 소비:
- NINJA_SURVIVAL: boss reward / 성장 선택.
- OMENWARD: TokenSource/roulette probability 설계와 후보 pool.
- URBAN_LEGEND: 사건·동료 지원·연구 선택의 조건/확률.

이 module은 결과 선택 UI를 소유하지 않는다. UI는 후보 list를 받아 표시한다.

---

## RM-SYS-004 · EXPLAINABLE_RESULT_PACKET

**목적:** 결과가 단순 숫자 요약이 아니라 “왜 이렇게 됐는지 → 무엇이 바뀌었는지 → 다음 설계에 무엇을 참고할지”를 구조화한다.

```yaml
result_id:
observed_facts: []
state_deltas: []
causes:
  - cause_id:
    evidence:
    contribution:
consequences:
  immediate: []
  delayed: []
next_design_hints: []
claim_ceiling:
```

적용:
- TEN_PACES replay 원인 설명.
- OMENWARD 전투 결과와 다음 룰렛/배치 설계.
- URBAN_LEGEND 주간 인과 summary.
- BLACKSMITH 아이템/의뢰 결과와 후속 귀결.
- NINJA_SURVIVAL REST summary/추천.
- SWITCHY route failure/완료 이유.

`next_design_hints`는 자동 정답 추천이 아니라 관찰 근거를 압축한다.

---

## RM-SYS-005 · EVENT_CONDITION_CHOICE_OUTCOME_ENGINE

**목적:** 텍스트 사건, dialogue, 현장 선택, 병편지, 자유 일정 등을 한 프로젝트 전용 if/else 덩어리로 만들지 않는다.

### `NARRATIVE_NODE_CHOICE_STATE_ENGINE`과의 관계

`RM-SYS-005`는 게임 시스템 관점의 event contract이고 `RM-NAR-001`은 서사 flow/상태 관점의 상위 narrative contract다. 하나의 구현으로 합쳐야 한다는 뜻은 아니다.

```yaml
event_id:
entry_conditions: []
priority:
once_or_repeat_policy:
presentation_payload:
choices:
  - choice_id:
    visible_when:
    enabled_when:
    costs: []
    immediate_effects: []
    scheduled_effects: []
    next_node_or_exit:
fallback:
telemetry_or_evidence_tags: []
```

Benchmark adaptation:
- Seoul 2033 계열에서 보이는 **선택 + 능력/아이템/상태 + 이후 상황 영향** 원리를 `ADAPT`.
- ink의 branching/gather/state runtime separation을 `ADAPT`.
- Yarn Spinner의 runner/presenter/variable-storage separation을 `ADAPT`.

고유 문장·사건·캐릭터는 복제하지 않는다.

---

## RM-SYS-006 · DELAYED_CONSEQUENCE_REENTRY_ENGINE

**목적:** 지금 한 선택의 결과가 며칠/주/챕터 뒤 다시 나타날 때 scheduling과 provenance를 분리한다.

```yaml
consequence_id:
source_action_id:
created_at_game_state:
trigger:
  time_or_turn:
  state_conditions: []
  event_conditions: []
payload:
resolution_policy:
expire_policy:
provenance:
```

적용:
- BLACKSMITH: 납품 아이템 → 나중의 경기/평판/재방문.
- URBAN_LEGEND: 활동·선택 → 이후 위험/사건/지원.
- COC_FICTION: setup/payoff를 runtime queue로 강제하지는 않지만 분석/추적 pattern으로 사용 가능.

---

## RM-SYS-007 · STAGE_WAVE_ENCOUNTER_DIRECTOR

**목적:** 시간/단계에 따른 적 압력과 encounter budget을 data-driven하게 표현한다.

```yaml
stage_id:
duration_or_end_condition:
pressure_curve:
spawn_or_encounter_budget:
segments:
  - start:
    end:
    enemy_pool:
    budget:
    modifiers:
elite_policy:
boss_policy:
recovery_windows: []
```

적용: NINJA_SURVIVAL, OMENWARD, GRIMOIRE의 boss/encounter phase.

이 module은 개별 enemy AI를 소유하지 않는다.

---

## RM-SYS-008 · RESEARCH_RESOURCE_QUEUE

**목적:** 비용을 지불해 일정 기간 후 지식/기능/자원을 획득하는 research/preparation workflow를 재사용한다.

```yaml
research_id:
requirements: []
costs: []
duration:
capacity_cost:
interrupt_policy:
completion_rewards: []
reservation_policy:
```

URBAN_LEGEND의 연구 노드/예약/queue가 주요 seed다. GRIMOIRE에서는 수업·학습·준비 구조에 필요한 경우 adapter로 검토한다.

---

## RM-SYS-009 · COMPANION_SUPPORT_TRIGGER_ENGINE

**목적:** 동료/소환수/정령이 조건에 따라 지원하되 플레이어 선택을 대행하지 않도록 지원 trigger를 data로 분리한다.

```yaml
support_id:
owner_entity:
eligibility:
trigger_window:
chance_or_readiness:
guarantee_after:
cost:
effect:
feedback:
```

적용:
- URBAN_LEGEND: 동료 선택, 준비도/readiness, 조건부 지원.
- GRIMOIRE: 동반 정령/수호 소환수.
- MY_LITTLE_BOAT: 동료 반응은 combat support가 아니므로 effect adapter를 감정/대사 반응으로 바꾼다.

---

## RM-SYS-010 · COLLECTION_HISTORY_REGISTRY

**목적:** 획득한 대상이 단순 inventory item이 아니라 **획득·변형·사용·추억·결과의 history**를 가지게 한다.

```yaml
record_id:
entity_type:
origin:
current_state:
history_events:
  - event_id:
    time:
    kind:
    payload:
links:
  owner:
  world_event:
  album_or_archive:
```

적용:
- BLACKSMITH 장비 생애/납품 기록.
- MY_LITTLE_BOAT 사진/수집/앨범.
- GRIMOIRE 해결 기록/마도서.

---

## RM-SYS-011 · CARD_ACTION_EFFECT_ENGINE

**목적:** 카드 자체를 모든 게임에 강제하는 것이 아니라, **행동/기술/주문을 data-defined effect unit으로 표현**해 UI·인벤토리·전투와 분리한다.

Slay the Spire의 “카드가 build 구성 단위이고 다양한 카드/유물 조합을 반복 조정한다”는 구조를 `ADAPT`하되 카드 UI/명칭/수치/고유 효과는 복제하지 않는다.

```yaml
action_id:
tags: []
requirements: []
costs: []
target_rule:
effects:
  - effect_type:
    magnitude_or_payload:
    timing:
    conditions: []
upgrade_or_variant_links: []
presentation_key:
```

1차 project adapters:
- GRIMOIRE: 주문/글자/회로 결과를 effect payload로 연결.
- TETRIS: 공격/방어/치유 Skill 역할.
- NINJA_SURVIVAL: ninjutsu/능력.

Deck/hand/draw/discard는 필요한 프로젝트에서만 별도 adapter다.

---

# Project-seed genre/system foundations

다음 module은 현재 하나의 프로젝트 정체성이 강하다. 공용 계약은 만들되 다른 프로젝트에서 실제 가치가 확인되기 전에는 범용 framework로 구현하지 않는다.

## RM-SYS-012 · SURVIVOR_AUTO_COMBAT_PROGRESSION_CORE

Seed: `NINJA_SURVIVAL`.

Vampire Survivors 계열에서 관찰되는 원리를 다음처럼 추상화한다.

```text
continuous enemy pressure
→ mostly automatic repeated combat action
→ XP/progression pickup
→ periodic bounded growth choice
→ build snowball
→ run end
→ bounded meta progression
```

```yaml
run_clock:
auto_action_sources: []
pressure_director:
progression_meter:
level_choice_request:
build_state:
run_meta_boundary:
```

Ninja의 REST/workbench/백팩은 이 core 외부의 고유 차별 layer로 유지한다.

---

## RM-SYS-013 · FALLING_BLOCK_LINE_CLEAR_CORE

Seed: `TETRIS`.

`TETRIS_TRADE_DRESS_BOUNDARY`가 항상 적용된다.

```yaml
board:
falling_piece_footprint:
spawn_policy:
movement_and_rotation_policy:
lock_condition:
completion_detector:
clear_resolution:
score_or_resource_adapter:
```

Base가 추출하는 것은 **격자 공간에 조각을 배치하고 완료 조건을 판정해 board를 갱신하는 추상 계약**이다.

금지:
- Tetris/Tetrimino 명칭을 generic module 명칭으로 사용.
- 공식 조각 표현·색·UI·음악·로고·trade dress를 복제.
- 이 문서를 권리 적합성 PASS로 해석.

상태: `RIGHTS_REVIEW_REQUIRED`.

---

## RM-SYS-014 · CHAIN_MATCH_COMBO_CORE

Seed: `TETRIS` 프로젝트의 Chain board.

```yaml
board_or_field:
connectivity_rule:
match_predicate:
minimum_chain:
resolution_order:
gravity_or_refill_policy:
combo_accumulator:
resource_adapter:
```

Line board와 동일 board implementation을 억지로 공유하지 않고 공통 인터페이스만 맞춘다.

---

## RM-SYS-015 · HIDDEN_PLAN_RESOLUTION_ENGINE

Seed: `TEN_PACES`.

```yaml
public_state:
player_private_plan:
opponent_private_plan:
resolution_steps:
  - ordering_rule:
    simultaneous_conflict_rule:
    movement_rule:
    action_rule:
public_observation_filter:
replay_trace:
```

핵심 boundary:
- resolver는 양쪽 plan을 받아 해결할 수 있음.
- AI planner는 플레이어 private plan을 읽지 못함.
- replay는 해결 후 공개 가능한 원인 trace만 사용.

`PROJECT_IMPLEMENTATION_EXISTS`; shared implementation은 별도 Pilot 전 공용화하지 않는다.

---

## RM-SYS-016 · ROUTE_STACK_LOGISTICS_ENGINE

Seed: `SWITCHY`.

```yaml
route_graph:
cargo_encounter_order:
stack_policy: LIFO | project_adapter
switch_states:
occupancy_locks:
pickup_rule:
unload_rule:
reachability_preflight:
route_end_failure:
```

Switchy의 실제 LIFO/연속 TOP 하역은 project policy이고, 공용 core는 route traversal + ordered cargo state + preflight 인터페이스를 추출한다.

---

## RM-SYS-017 · SPELL_COMPOSE_VALIDATE_COMMIT_ENGINE

Seed: `GRIMOIRE`.

```text
compose primitive
→ arrange relation/circuit
→ prepare immutable action
→ select target/context
→ validate resource + state
→ explicit commit
→ atomic resolve
→ result record
```

```yaml
primitive_inputs: []
composition_graph:
prepared_action:
target_context:
validation_rules: []
commit_token:
atomic_effect_packet:
result_record:
```

프로젝트의 글자 의미·세계관·마법 표현은 공용 module이 소유하지 않는다.

---

## RM-SYS-018 · ROULETTE_TOKEN_SOURCE_ENGINE

Seed: `OMENWARD`.

```yaml
token_sources:
  - source_id:
    token_pool:
    weights:
    activation_condition:
roulette_slots:
roll_seed:
probability_modifiers: []
outputs:
  rolled_tokens:
  probability_trace:
```

핵심은 확률을 숨기는 RNG가 아니라 **플레이어가 확률 생산 구조를 설계하고 결과를 해석할 수 있는 것**이다.

---

## RM-SYS-019 · PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE

Seed: `BLACKSMITH`.

```yaml
item_state:
next_upgrade:
  success_probability:
  success_delta:
  failure_outcomes:
  compensation:
stop_value:
milestone_modifiers: []
result_history:
```

핵심 선택:

```text
지금 확정해 가치를 보존
vs
추가 기대값을 위해 현재 가치를 위험에 노출
```

UI·수치·아이템 표현은 project-specific이다.

---

## RM-SYS-020 · CALM_DISCOVERY_SESSION_CORE

Seed: `MY_LITTLE_BOAT`.

전투/실패 압박이 없는 짧은 session에서도 상태와 선택이 의미 있게 남도록 하는 core다.

```yaml
session_intent_or_mood:
session_duration:
ambient_encounter_pool:
view_or_speed_choices:
collectible_moments:
companion_reactions:
archive_updates:
comfort_options:
```

`failure_state`를 의무화하지 않는다. 성취는 발견·기록·관계·회고로 표현할 수 있다.

---

# Narrative modules

## RM-NAR-001 · NARRATIVE_NODE_CHOICE_STATE_ENGINE

1차 프로젝트: `COC_FICTION`, `URBAN_LEGEND`, `GRIMOIRE`, 선택적으로 `MY_LITTLE_BOAT`.

```yaml
node_id:
content_ref:
entry_conditions: []
state_reads: []
choices:
  - id:
    condition:
    text_or_presentation_ref:
    state_writes: []
    divert:
continuation:
state_snapshot:
```

ink/Yarn Spinner에서 확인되는 **flow/runtime와 presentation의 분리**를 `ADAPT`한다. 특정 외부 언어를 Base 표준으로 강제하지 않는다.

---

## RM-NAR-002 · CANON_SOURCE_PROVENANCE_REGISTRY

**목적:** 설정/사건/원문/Decision/현재 원고가 충돌할 때 어떤 출처가 무엇을 증명하는지 추적한다.

```yaml
claim_or_fact_id:
current_value:
authority_level:
source_refs: []
valid_from:
supersedes: []
conflicts: []
verification_state:
```

COC-Fiction의 Canon Registry·source manifest가 강한 seed다. 게임 프로젝트에서는 lore/quest/event canon에 필요한 만큼만 축소한다.

---

## RM-NAR-003 · CONTINUITY_REVISION_REGRESSION

```yaml
revision_scope:
before_state:
after_state:
checks:
  canon:
  causality:
  pov:
  timeline:
  location_and_movement:
  entity_state:
  forbidden_setting:
  index_and_outline:
findings: []
```

자동 check는 문학 품질 PASS가 아니라 **모순/누락 후보 탐지**다.

---

## RM-NAR-004 · EXTERNAL_ARTIFACT_RECONCILIATION_WORKFLOW

Seed: `COC_FICTION`의 외부 최신 원고와 repository legacy tail reconciliation.

```text
external candidate
+ current repository artifact
+ current canon
→ delta extraction
→ KEEP | APPLY | REWORK | REJECT
→ approved delta only
→ dependent index/outline/registry propagation
→ readback
```

다른 프로젝트에서 Notion/외부 문서/이전 branch의 기획을 현재 정본에 흡수할 때도 적용 가능한 workflow seed다.

---

# 공통 구현 경계

## Godot 권장 adapter shape

공용 runtime Pilot을 만들 경우 Godot의 Scenes/Resources 재사용 모델에 맞춰 **data Resource + pure rule service + project presenter/adapter**를 우선 비교한다.

```text
Reusable Resource/Data
→ Stateless/Pure-ish Rule Service
→ Project Adapter
→ Project Scene/UI
```

이 구조가 모든 module에 강제되는 것은 아니다. 저장/성능/복잡도 측정에서 더 단순한 project-local 코드가 우세하면 공용 runtime 구현을 기각한다.

## 완료 증거 ceiling

- 이 문서: `MODULE_CONTRACT_DEFINED`.
- 공용 코드: 별도 `IMPLEMENTATION_NOT_BUILT` unless explicitly evidenced.
- 프로젝트 적용: project branch/runtime에서 실제 사용 확인 필요.
- 재미·몰입: release-near Vertical Slice + 플레이 evidence 필요.
- 권리: 별도 rights/license review 필요.
