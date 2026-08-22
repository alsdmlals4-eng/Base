# RM-TOOL-003 · Sweep, Strategy & Model-Fidelity Extension

```yaml
owner: RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR
status: CONTRACT_EXTENSION
public_module_id: NO_NEW_PUBLIC_MODULE_ID
```

이 문서는 `PRODUCTION_TOOL_WORKFLOW_MODULES.md`의 `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`를 대체하지 않는다. 기존 distribution / paired-seed / outlier / dominant-choice / goal-seek 계약에 **전략 baseline, parameter sweep, simulation-model fidelity**를 추가하는 bounded extension이다.

## 외부 benchmark provenance

Primary source inspected:

- `https://github.com/applesnort/godot-autosim`
- repository README / addon README
- `docs/prds/parameter-sweep.md`
- `addons/godot_autosim/core/balance_assertions.gd`
- root `LICENSE`

Observed:

- Godot 4.6+용 automated game simulation / balance testing framework로 공개되어 있다.
- random, greedy, custom strategy를 교체 가능한 bot policy로 사용한다.
- report에서 win rate, mean, median, stddev 등을 비교하고 GUT용 statistical assertion을 제공한다.
- `assert_no_dominant_strategy`는 여러 strategy report의 승률 상한을 검사한다.
- parameter sweep은 한 parameter의 여러 값을 순회하고 각 step에서 full simulation batch를 실행한다.
- sweep PRD는 step 간 같은 seed를 사용해 변경 parameter 외 RNG 차이를 줄이는 것을 명시한다.
- threshold 탐색은 관측된 step 사이를 linear interpolation한다.
- 실제 게임 로직이 rendering과 분리돼 있으면 실제 rule code를 직접 adapter로 호출할 수 있고, physics/timer/navigation 등 때문에 어려우면 balance-relevant mechanics를 수학 model로 다시 표현하는 경로를 설명한다.
- root license는 **MIT license**다.

Disposition:

```text
PATTERN_EXTRACT
PROJECT_ADOPTION_REQUIRES_EXISTING_SOLUTION_FIRST
```

`godot-autosim`을 Base 또는 모든 프로젝트의 기본 dependency로 자동 설치하지 않는다. 실제 프로젝트 adoption은 Godot version, existing runner/test, dependency inventory, maintenance, exact pin, project rule reuse 가능성, rollback을 별도 비교한다.

---

## 1. STRATEGY_BASELINE_MATRIX

하나의 simulation policy 결과를 “밸런스”라고 부르지 않는다. 선택 정책 자체가 결과를 바꾸므로 최소한 다음 역할을 구분한다.

```yaml
STRATEGY_BASELINE_MATRIX:
  RANDOM_BASELINE:
    purpose: 탐색 없는 기준선과 accidental strength 탐지
  HEURISTIC_BASELINE:
    purpose: 한 metric 또는 명시 규칙을 탐욕적으로 최적화하는 단순 정책
  PROJECT_STRATEGY:
    purpose: 프로젝트가 실제로 기대하는 build/decision policy 또는 대표 bot
  ADVERSARIAL_OR_STRESS_STRATEGY:
    purpose: 알려진 exploit·dominant choice·극단 조합 압박
```

모든 프로젝트가 네 종류를 전부 구현해야 한다는 뜻은 아니다. 현재 질문을 구분할 수 있는 최소 전략 집합만 사용한다.

### 해석 경계

`SIMULATION_STRATEGY_IS_NOT_PLAYER_BEHAVIOR_PROOF`.

- random bot이 높은 승률을 보인다고 실제 플레이어에게 게임이 자동으로 “너무 쉽다”고 단정하지 않는다.
- greedy policy가 dominant하다고 실제 사람이 그 전략을 발견·실행·선호한다는 뜻은 아니다.
- 반대로 단순 bot이 exploit을 재현하면 **기계적으로 강한 선택지 후보**를 발견한 evidence가 될 수 있다.
- player skill, information access, execution burden, UX discoverability, fun은 별도 playtest/human evidence가 필요하다.

전략 비교 시 가능한 경우 동일 scenario/seed 집합을 사용해 strategy delta와 RNG delta를 분리한다.

---

## 2. PARAMETER_SWEEP_SINGLE_AXIS_FIRST

수치 튜닝은 여러 parameter를 동시에 흔들기 전에 **한 축을 고정된 비교 조건에서 순회**하는 것을 기본값으로 한다.

```yaml
parameter_sweep:
  mode: PARAMETER_SWEEP_SINGLE_AXIS_FIRST
  parameter:
  values: []
  locked_parameters: []
  scenario_set: []
  seed_set: []
  strategies: []
  metrics: []
  reports_by_value: []
  threshold_targets: []
```

`PAIR_SWEEP_STEPS_BY_SEED_SET`.

각 parameter value에서 가능한 경우 동일한 seed set과 scenario set을 재사용한다. 한 step마다 무작위 seed가 달라지면 parameter 효과와 표본 변동을 혼동하기 쉽다.

다축 sweep이 실제로 필요하면 조합 폭증과 interaction effect를 별도 실험 설계 문제로 취급한다. 단순 nested loop를 기본 공용 계약으로 만들지 않는다.

### threshold

`THRESHOLD_ESTIMATE_NOT_RECOMMENDED_VALUE`.

관측된 두 parameter step 사이에서 target metric crossing을 interpolation해도 그 값은 **탐색용 추정치**다. “이 값이 최적 밸런스” 또는 프로젝트 정본 변경 권한을 주지 않는다.

`SWEEP_THRESHOLD_REQUIRES_UNCERTAINTY_CHECK`.

stochastic 결과에서 threshold 근처의 의사결정이 중요하면:

1. threshold 주변 값을 더 촘촘히 재측정한다.
2. 충분한 seed/run 수를 사용한다.
3. confidence interval 또는 반복 batch 변동을 본다.
4. 인접 값의 ordering이 안정적인지 확인한다.
5. 실제 프로젝트 runner와 model fidelity를 확인한다.

단일 linear interpolation 결과만으로 수치를 확정하지 않는다.

---

## 3. Simulation adapter fidelity

simulation이 실제 production rule을 얼마나 재사용하는지 명시한다.

```yaml
simulation_adapter:
  mode: AUTHORITATIVE_RULE_ADAPTER | ABSTRACT_MATH_MODEL
  reused_production_rules: []
  reimplemented_rules: []
  omitted_systems: []
  approximation_assumptions: []
  parity_scenarios: []
  parity_result:
```

### AUTHORITATIVE_RULE_ADAPTER

`AUTHORITATIVE_RULE_ADAPTER`는 가능한 범위에서 프로젝트의 실제 balance-relevant rule/state transition 함수를 직접 호출한다.

적합한 경우:

- rendering과 domain logic이 분리돼 있음.
- pure/deterministic rule을 headless에서 호출 가능.
- 실제 content/data schema를 안전하게 read-only snapshot으로 공급 가능.

이 경로도 physics, presentation, asynchronous side effect, save/platform behavior를 자동으로 검증하지 않는다.

### ABSTRACT_MATH_MODEL

`ABSTRACT_MATH_MODEL`은 실제 runtime 전체를 실행하지 않고 balance-relevant mechanics를 별도 순수 모델로 근사한다.

적합한 경우:

- physics/navigation/timer/animation tree 때문에 대량 simulation에서 실제 runtime을 반복하기 어려움.
- 초기 설계 탐색에서 수치 관계만 빠르게 비교하려 함.
- production code에 직접 coupling하는 비용이 현재 가치보다 큼.

장점은 속도와 탐색 비용이다. 단점은 **모델과 실제 게임 규칙의 drift**다.

`MODEL_PARITY_CHECK_REQUIRED_FOR_PRODUCTION_CLAIM`.

math model 결과를 production 판단에 사용하려면 대표 scenario에서 최소한 다음을 대조한다.

```text
same initial state / content
→ same deterministic inputs where possible
→ production rule/runtime observed result
↔ model predicted result
→ material delta 설명
```

완전한 일치를 항상 요구하지는 않지만, 어떤 차이를 의도적으로 무시했는지와 그 차이가 현재 metric에 왜 안전한지 설명할 수 있어야 한다.

`MODEL_SIMULATION_PASS_IS_NOT_PRODUCTION_RUNTIME_PASS`.

math model이 balance threshold를 통과해도 actual runtime integration, effect ordering, save/load, physics, UI, performance, player behavior는 별도 Evidence다.

---

## 4. 전략 × parameter 비교

parameter sweep과 strategy comparison을 함께 사용할 때는 최소한 다음을 분리한다.

```yaml
comparison_grid:
  parameter_axis:
  strategy_axis:
  paired_scenarios: true
  paired_seed_set: true
  metrics:
    - distributions
    - failure_rates
    - dominant_choice_rate
    - strategy_delta
    - parameter_delta
```

목표는 “어떤 수치가 평균 승률 50%인가” 하나가 아니라:

- 어느 strategy에서만 급격히 깨지는가?
- random baseline과 project strategy 사이 격차가 지나치게 큰가?
- 특정 parameter에서 dominant strategy가 새로 생기는가?
- tail/failure rate가 평균과 다르게 악화되는가?
- threshold가 seed set에 따라 크게 움직이는가?

를 함께 보는 것이다.

---

## 5. CI / regression 후보

실제 프로젝트가 반복 simulation을 채택한 뒤에는 사람의 눈으로 매번 표를 확인하는 대신 안정된 invariant만 CI assertion 후보로 올린다.

예:

```yaml
balance_regression_candidate:
  scenario_set:
  exact_rule_or_model_identity:
  strategy:
  seed_set:
  run_count:
  assertions:
    win_rate_range:
    median_range:
    stddev_max:
    failure_rate_max:
    dominant_strategy_max:
```

주의:

- design target이 자주 변하는 초기 기획 단계에서는 CI threshold가 오히려 iteration을 방해할 수 있다.
- statistical assertion은 run count와 variance를 고려해야 한다.
- CI PASS는 재미·공정성·시장성 PASS가 아니다.
- 실제 design decision이 바뀌면 threshold 변경은 “테스트 고치기”가 아니라 의도 변경 evidence와 함께 검토한다.

---

## 6. Existing Solution First

프로젝트별 선택 순서:

```text
현재 production rule/test/runner 확인
→ 이미 headless batch 가능한지 확인
→ 작은 project-local script로 질문을 답할 수 있는지 확인
→ RM-TOOL-002/003 packet으로 report/seed/evidence 정렬
→ 외부 maintained tool 도입 가치 비교
→ 반복 소비가 입증될 때만 shared implementation/UI 확대
```

`godot-autosim` 직접 adoption은 MIT라는 이유만으로 자동 승인하지 않는다. exact Godot compatibility, project adapter cost, 실제 production rule 재사용 정도, dependency update/rollback과 GUT/기존 runner 중복을 비교한다.

---

## 7. 적용 우선순위

현재 Base 기준 추천 순서:

1. **OMENWARD**: roulette/wave/unit read-only snapshot에서 strategy + parameter sweep Pilot.
2. **BLACKSMITH**: 강화 확률·내구도·경제 변수에서 tail risk와 tipping point 탐색.
3. **NINJA_SURVIVAL**: reward/backpack/build 전략별 dominant choice 탐색.
4. **TETRIS**: Line/Chain reward bridge와 skill 선택 정책 비교.

이 순서는 implementation authority가 아니다. 각 프로젝트의 최신 canon, blocker, open PR 상태를 먼저 읽는다.

## Evidence ceiling

```text
FAST_SIMULATION != HIGH_FIDELITY_SIMULATION
HIGH_RUN_COUNT != CORRECT_MODEL
RANDOM_BASELINE != PLAYER_SKILL_MODEL
INTERPOLATED_THRESHOLD != OPTIMAL_VALUE
MODEL_PARITY_SAMPLE != FULL_RUNTIME_EQUIVALENCE
```

실제 프로젝트 Pilot이 없으면 이 문서는 `CONTRACT_EXTENSION`이며 executable Base implementation 완료를 주장하지 않는다.
