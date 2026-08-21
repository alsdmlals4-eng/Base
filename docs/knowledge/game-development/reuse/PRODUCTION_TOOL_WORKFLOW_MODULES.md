# Production Tool & Workflow Reusable Modules

이 문서는 프로젝트 10개의 반복 제작비를 기준으로 **도구·자동화·검증·작업구조** 재사용 후보를 정리한다.

새 Tool Hub·QA capture app·광역 Skill을 만들기 위한 목록이 아니다. 같은 책임의 기존 Base owner와 repository/runtime evidence가 있으면 `EXISTING_OWNER_REUSE`가 기본이다.

---

## RM-TOOL-001 · DATA_SCHEMA_CROSSREF_VALIDATOR

**문제:** JSON/Resource/Markdown 기반 콘텐츠가 늘수록 ID 오타, dangling reference, 잘못된 enum, 중복 key, 상태 전이 누락이 반복된다.

적용 후보:
- URBAN_LEGEND: 사건·동료·장비·연구·활동.
- NINJA_SURVIVAL: 아이템·조합·보상·적/스테이지.
- OMENWARD: TokenSource·roulette·unit·stage.
- GRIMOIRE: 글자·회로·주문·effect.
- TETRIS: Skill·Energy/Tier bridge.
- SWITCHY: semantic asset/data manifests.
- BLACKSMITH: item/order/history definitions.

```yaml
module: DATA_SCHEMA_CROSSREF_VALIDATOR
inputs:
  roots: []
  schema_rules: []
  id_namespaces: []
checks:
  - parseability
  - schema/type
  - unique IDs
  - reference existence
  - enum/domain constraints
  - forbidden cycles where configured
  - unreachable/orphan records where configured
outputs:
  - deterministic finding list
  - file/path/record locator
  - severity
  - remediation hint
exit_contract:
  invalid_contract: nonzero
  warnings_only: configurable
```

### 구현 원칙

- validator는 데이터를 수정하지 않는다.
- 프로젝트별 schema는 adapter/config로 둔다.
- 문자열 전체를 하드코딩한 하나의 Base 검사기로 만들지 않는다.
- project runtime owner가 존재하면 그 serialization/parser를 가능하면 재사용한다.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT`.

---

## RM-TOOL-002 · DETERMINISTIC_SEED_REPLAY_CAPTURE

**문제:** RNG·동시해결·stage progression이 있는 게임은 “왜 이 결과가 나왔나”를 재현하기 어렵다. Preview가 실제 runtime RNG나 mutable state를 건드리면 같은 입력도 다른 결과를 만들 수 있으므로 **관찰/예측과 실제 인과 상태 변경의 경계**까지 replay 계약에 포함한다.

적용:
- TEN_PACES: 계획 resolution replay.
- OMENWARD: roulette + battle result.
- BLACKSMITH: 강화 outcome/lifecycle scenario.
- NINJA_SURVIVAL: reward/build/encounter sequence.
- TETRIS: piece/chain sequence test.
- SWITCHY: sealed layout retry.
- GRIMOIRE: 주문 preview와 실제 effect commit 분리.

```yaml
run_identity:
  build_or_commit:
  scenario_id:
  seed:
initial_state_hash:
input_events: []
causal_boundary:
  preview_reads_state: true
  preview_mutates_runtime_state: false
  preview_consumes_runtime_rng: false
  runtime_rng_consumption_points: []
resolution_windows:
  - window_id:
    opens_on:
    pending_effects: []
    closes_on:
    authoritative_result_checks: []
    priority_rules: []
state_checkpoints: []
result_hash:
replay_format_version:
```

필수 invariant:

```text
PREVIEW_DOES_NOT_MUTATE_CAUSAL_STATE
PREVIEW_DOES_NOT_CONSUME_RUNTIME_RNG
RNG_CONSUMPTION_HAS_EXPLICIT_CAUSAL_BOUNDARY
```

검증:
1. 같은 build + scenario + seed + input → 같은 deterministic state hash가 필요한 범위를 선언.
2. presentation timestamp·animation jitter처럼 비결정적이어도 되는 값은 hash에서 제외.
3. replay가 private/hidden information을 부적절하게 노출하지 않는지 확인.
4. preview가 randomness를 보여줘야 하면 runtime RNG stream을 소비하지 말고 copied/sandbox RNG 또는 분석용 분포를 사용한다.
5. win/loss·resource depletion·next-state UI처럼 권위 있는 결과는 선언된 resolution window가 닫힌 뒤 한 번 확정한다. 중간 step은 debug trace로 남길 수 있지만 authoritative result가 아니다.
6. replay가 RNG를 사용했다면 어떤 causal boundary에서 어떤 stream/seed가 소비됐는지 재현 가능한 형태로 남긴다.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT`.

---

## RM-TOOL-003 · BALANCE_SCENARIO_BATCH_SIMULATOR

**판정:** `MODULE_CONTRACT_DEFINED`.

Balance/scenario simulation은 공통 가치가 있지만 현재 공용 executable이 존재한다고 가정하지 않는다. 별도 대형 Tool을 만들기 전에 프로젝트별 **read-only snapshot + deterministic runner + repository-native report** 조합을 우선하고, 실제 반복 사용 가치가 검증된 뒤에만 기존 Tool Hub의 얇은 UI/launcher로 승격한다.

```yaml
snapshot_input:
scenario_set:
seed_policy:
runs_per_scenario:
metrics:
  distributions:
    - mean
    - median
    - percentile_05
    - percentile_25
    - percentile_75
    - percentile_95
  confidence_intervals: []
  tails: []
  dominant_choices: []
  failure_rates: []
  paired_seed_delta: []
comparison:
  baseline:
  candidates: []
  pair_by_seed: true
explainability:
  reason_trace: []
  trigger_counts: []
  outlier_runs: []
goal_seek:
  targets: []
  adjustable_parameters: []
  locked_parameters: []
  constraints: []
  output_candidates_only: true
output:
  report:
  machine_readable_summary:
  patch_suggestions_non_authoritative:
```

### 분석 원칙

- 평균 하나로 판정하지 않고 **분포·꼬리 위험·실패율·지배 선택지**를 함께 본다.
- baseline과 candidate는 가능한 경우 같은 scenario/seed 집합으로 짝지어 비교해 RNG 차이를 설계 차이로 오인하지 않는다.
- outlier는 제거하기 전에 원인을 trace한다. 데이터 오류인지 실제 long-tail 위험인지 구분한다.
- goal seeking은 목표 metric에 가까운 **후보 수치 범위**를 제안할 수 있지만 프로젝트 정본을 자동 수정하지 않는다.
- parameter lock은 “이번 실험에서 바꾸지 않을 값”을 보호하는 실험 계약이지 게임 데이터의 새 권위가 아니다.
- simulation 결과는 `RM-SYS-004 EXPLAINABLE_RESULT_PACKET` 또는 동등한 project-owned 결과 형식으로 사람이 원인을 역추적할 수 있어야 한다.

### 1차 project scenarios

- **OMENWARD 우선 Pilot:** roulette 확률·wave·unit 결과 분포. production consumer를 건드리지 않는 read-only snapshot sidecar부터 검증한다.
- NINJA_SURVIVAL: 보상/백팩 조합/encounter build 성능.
- BLACKSMITH: 강화·경제·의뢰 결과 분포.
- TETRIS: Line/Chain reward bridge와 skill 선택 분포.

### Existing Solution First / 구현 경로 비교

| 경로 | 판정 | 이유 |
|---|---|---|
| 프로젝트별 임시 script만 계속 작성 | `ADAPT_AS_PHASE_0` | 초기 비용은 낮지만 비교 UI·공통 report·재현 계약이 반복될 수 있음 |
| 외부 balance GUI를 Base 표준으로 직접 탑재 | `REJECT_AS_DEFAULT` | 엔진/보안/프로젝트 격리/라이선스 owner가 이중화되고 Tool Hub와 책임이 겹침 |
| 독립 거대 Balance 앱을 새로 구축 | `DEFER` | 실제 소비가 증명되기 전에 UI·편집기·export 기능을 과잉 구축할 위험 |
| 기존 RM-TOOL-002/003 계약 + project adapter + 필요 시 Tool Hub thin surface | `ADOPT` | deterministic evidence를 먼저 만들고 검증된 반복 작업만 공용 UI로 올릴 수 있음 |

공개 외부 도구의 좋은 기능은 `BENCHMARK_SOURCE_NOTES.md`에 근거를 남긴 뒤 `ADAPT`한다. 특정 외부 앱의 UI·코드 구조를 그대로 Base의 런타임 권위로 복제하지 않는다.

증거 ceiling:
- simulation은 플레이어 재미를 증명하지 않는다.
- patch suggestion과 goal-seek output은 프로젝트 수치 정본을 자동 수정하지 않는다.
- 실제 executable 구현은 별도 evidence/approval 없이 완료로 주장하지 않는다.
- read-only snapshot Pilot이 실제 프로젝트 runner와 동일 규칙을 사용했는지 확인 전에는 production balance PASS가 아니다.

---

## Cross-cutting contract · ATOMIC_RESOLUTION_BOUNDARY

이 항목은 새 `RM-SYS-*` module ID를 추가하지 않는다. **`RM-SYS-002 PHASED_SESSION_STATE_MACHINE`, `RM-SYS-004 EXPLAINABLE_RESULT_PACKET`, `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`가 공유하는 작은 경계 계약**이다.

문제는 하나의 player action이 여러 effect·death·resource change·UI update를 연쇄 발생시킬 때 중간 상태가 최종 결과처럼 노출되는 것이다. 프로젝트마다 전투 manager를 통합하는 대신 각 project resolver가 다음 경계를 선언한다.

```yaml
resolution_window:
  window_id:
  opens_on:
  allowed_mutations: []
  deferred_authoritative_checks: []
  priority_rules: []
  closes_when:
  publish_after_close:
  replay_checkpoint:
preview_policy:
  reads_authoritative_state: true
  mutates_authoritative_state: false
  consumes_runtime_rng: false
```

예:
- 마지막 자원 소진과 마지막 적 처치가 같은 연쇄에서 발생하면 프로젝트가 명시한 priority rule로 **전체 연쇄 후** 승패를 정한다.
- 다음 행동/탄환/카드/주문 preview는 현재 상태를 읽을 수 있지만 실제 RNG나 authoritative container를 선소비하지 않는다.
- UI는 animation 중 transient state를 보여줄 수 있어도 authoritative result packet은 resolution close 뒤 확정한다.

적용 후보: OMENWARD auto battle trigger chain, TETRIS line/chain→skill effect, GRIMOIRE multi-effect spell, TEN_PACES simultaneous resolution, BLACKSMITH enhancement consequence, NINJA_SURVIVAL proc/kill/reward sequence.

이 계약은 각 프로젝트의 effect ordering이나 승패 우선순위를 통일하지 않는다. **경계를 명시하고 테스트 가능하게 만드는 것**만 공용화한다.

---

## RM-TOOL-004 · REPOSITORY_NATIVE_EVIDENCE_CAPTURE

**판정:** `EXISTING_OWNER_REUSE · NO_DEDICATED_CAPTURE_APP`.

프로젝트 검증 증거는 별도 QA 관리 앱을 기본 경로로 두지 않고 **이미 존재하는 repository/runtime/test/CI 증거**를 exact project/build identity에 묶는다.

```yaml
project_identity:
build_identity:
validation_contract:
  resolution_or_viewport:
  input_path:
  accessibility_checks:
  expected_state_or_screen:
capture_sources:
  screenshots: []
  video: []
  logs: []
  test_results: []
  machine_state: []
storage:
  repository_or_ci_artifact:
  notion_human_link_when_useful:
verdict:
  human_or_rule_owner:
  evidence_ceiling:
```

원칙:

1. GUT/Godot/Hera/CLI/CI처럼 현재 프로젝트가 이미 채택한 evidence source를 우선한다.
2. screenshot/video가 필요한 경우 현재 실행환경에서 직접 캡처하고 commit/build/viewport/input context를 함께 기록한다.
3. Notion은 사람이 보는 링크·preview·설명면이 될 수 있지만 repository/runtime truth를 대체하지 않는다.
4. 사람이 실제로 관찰하지 않은 usability/fun evidence는 `NOT_RUN`이다.
5. capture app·project adapter·별도 local management UI를 신규 기본 의존성으로 만들지 않는다.

`REPOSITORY_NATIVE_EVIDENCE_CAPTURE != AI_AUTO_PASS`.

---

## RM-WORK-001 · PROJECT_REUSE_OPPORTUNITY_SCAN

**상태:** `BASE_ACTIVE_METHOD`.

현재 Base의 merged reverse-engineering pipeline과 `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`가 owner다.

```text
PROJECT_CANON_FIRST
→ REPEATED_COST_AND_BOTTLENECK_MAP
→ candidate search
→ multi-source reverse engineering
→ reusable contract
→ Existing Solution First
→ fit / cost / risk
→ NOVELTY_DELTA
→ project pilot
→ PROJECT_ONLY | BASE_PROMOTION_CANDIDATE
```

새 `reuse-discovery` 광역 Skill을 만들지 않는다. 프로젝트 기획/벤치마킹 작업의 조건부 절차로 사용한다.

---

## RM-WORK-002 · SKILL_WORKFLOW_PATTERN_EVAL

**상태:** `BASE_ACTIVE_METHOD`.

Owner: `docs/AI_SKILL_ADOPTION_GUIDE.md`의 `REVERSE_ENGINEERED_SKILL_WORKFLOW_CANDIDATE`, `PATTERN_NOT_PACKAGE_COPY`, `EVAL_BEFORE_PROMOTION`.

```yaml
candidate:
trigger:
inputs:
source_of_truth:
steps:
output:
failure_recovery:
placement_options:
  - existing instruction
  - template/reference
  - existing Skill mode
  - deterministic tool
  - EXTERNAL_PROCESS_OVERLAY
  - new Skill/Agent last
baseline_eval:
candidate_eval:
negative_route_eval:
maintenance_cost:
```

### PROJECT_SUBSYSTEM_CHANGE_MAP

외부 프로젝트의 세분화된 agent/skill 구조에서 유용한 것은 **Skill 개수**가 아니라 “이 subsystem을 바꿀 때 어떤 owner·상태·UI·테스트까지 추적해야 하는가”를 명시하는 부분이다. 프로젝트마다 새 Skill을 대량 생성하기 전에 다음 change map을 기존 planning/implementation 계약에 붙인다.

```yaml
project_subsystem_change_map:
  subsystem:
  canonical_owner:
  authored_data_owner:
  mutable_runtime_owner:
  resolver_or_service_owner:
  presenter_or_ui_owner:
  touch_points: []
  cross_domain_dependencies: []
  invariants: []
  required_tests: []
  forbidden_shortcuts: []
  rollback:
  skill_promotion_gate:
    repeated_frequency:
    routing_value:
    baseline_eval:
    candidate_eval:
```

원칙:
- authored immutable data와 run/session 중 변하는 mutable state의 owner를 가능한 경우 분리한다.
- presenter/UI는 의도를 전달하고 결과를 표시할 수 있지만 gameplay state의 우회 owner가 되지 않는다.
- named subsystem 변경은 data → runtime state → resolver → persistence → UI → tests 경로를 따라 영향 범위를 확인한다.
- change map이 기존 AGENTS/Skill/owner 문서와 중복되면 새 파일을 만들지 않고 기존 owner에 흡수한다.
- 반복 빈도와 routing/eval 개선이 실제로 확인될 때만 dedicated Skill로 승격한다.

### 승격 금지 조건

- 유명 팀이 쓴다는 이유만 있음.
- 이름만 다르고 기존 Skill과 책임이 같음.
- trigger가 너무 넓어 unrelated 작업까지 라우팅함.
- 실제 전후 Eval이 없음.
- Tool/권한/정본 경계가 명확하지 않음.

---

# 1차 공용 Tool/Workflow 조합

## A. 데이터 중심 프로젝트

```text
PROJECT_REUSE_OPPORTUNITY_SCAN
→ DATA_SCHEMA_CROSSREF_VALIDATOR
→ project-specific unit tests
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE when runtime/UI evidence is needed
```

추천 대상: URBAN_LEGEND, NINJA_SURVIVAL, OMENWARD, GRIMOIRE, BLACKSMITH.

## B. RNG/해결 결과가 중요한 프로젝트

```text
DETERMINISTIC_SEED_REPLAY_CAPTURE
→ ATOMIC_RESOLUTION_BOUNDARY
→ BALANCE_SCENARIO_BATCH_SIMULATOR when justified
→ EXPLAINABLE_RESULT_PACKET
→ repository-native runtime evidence
→ human/player validation when the claim requires it
```

추천 대상: OMENWARD, NINJA_SURVIVAL, BLACKSMITH, TETRIS, TEN_PACES, GRIMOIRE.

## C. 콘텐츠/서사 프로젝트

```text
CANON_SOURCE_PROVENANCE_REGISTRY
→ DATA_SCHEMA_CROSSREF_VALIDATOR
→ CONTINUITY_REVISION_REGRESSION
→ EXTERNAL_ARTIFACT_RECONCILIATION_WORKFLOW
```

추천 대상: COC_FICTION, URBAN_LEGEND, GRIMOIRE.

---

# Godot 재사용 구현 원칙

Godot 프로젝트의 공용 Pilot이 필요할 때 다음을 우선 비교한다.

```text
Resource data contract
+ small rule service/script
+ project adapter
+ project-owned scene/presenter
```

하지만 다음 경우 project-local 구현을 유지한다.

- adapter가 공용 코드보다 커짐.
- 프로젝트마다 상태/시간/rollback 의미가 다름.
- shared dependency가 upgrade/CI 위험을 키움.
- 공용화로 코드량은 줄어도 이해/디버그 시간이 늘어남.

---

# Benchmark / Existing Solution notes

## Godot

- Scenes/Resources의 재사용·인스턴스화를 `ADOPT` 후보로 검토한다.
- 하나의 거대 autoload/global manager는 이 조사에서 도출된 결론이 아니다.

## GitHub reusable workflow pattern

반복 CI 절차를 복사하지 않고 중앙 호출 계약으로 재사용하는 원리를 workflow module 설계에 `ADAPT`한다. Base 자체 Required Check 구조는 별도 CI owner가 소유한다.

## External addons/tools

Godot addon, GitHub repo, marketplace tool은 발견 즉시 설치하지 않는다.

```text
Existing Solution First
→ license
→ version/Godot compatibility
→ security/supply chain
→ maintenance
→ exact project consumer
→ bounded pilot
→ rollback
```

---

# 구현 우선순위

| Priority | Module | 이유 |
|---|---|---|
| P0 | `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR` | 여러 프로젝트의 반복 오류를 낮은 UI/runtime 위험으로 줄일 수 있음 |
| P0 | `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE` | simulation/replay/debug 기반과 preview/RNG 인과 경계를 공유할 수 있음 |
| P1 | `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR` | 가치가 크지만 project snapshot/runner evidence가 먼저 필요; OMENWARD read-only Pilot이 1차 소비자 |
| ACTIVE | `ATOMIC_RESOLUTION_BOUNDARY` | 새 runtime module이 아니라 기존 FSM/result/replay owner가 공유하는 경계 계약 |
| ACTIVE | `RM-TOOL-004 REPOSITORY_NATIVE_EVIDENCE_CAPTURE` | 별도 앱 없이 기존 test/runtime/CI 증거를 재사용 |
| ACTIVE | `RM-WORK-001/002` | 이미 Base 방법으로 존재; subsystem change map은 Skill 증식 전 단계 |

# 완료 상태

이 문서의 신규 tool contract는 실제 executable 구현과 분리한다. `RM-TOOL-004`는 별도 프로그램이 아니라 현재 repository/runtime evidence를 조합하는 **활성 방법 계약**이다. `RM-TOOL-001/002/003`은 실제 공용 executable 증거가 생기기 전까지 `IMPLEMENTATION_NOT_BUILT` 또는 project-local pilot 상태를 유지한다. `ATOMIC_RESOLUTION_BOUNDARY`와 `PROJECT_SUBSYSTEM_CHANGE_MAP`은 기존 owner를 보강하는 계약이며 별도 공용 runtime/Skill 구현이 아니다.
