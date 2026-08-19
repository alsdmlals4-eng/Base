# Production Tool & Workflow Reusable Modules

이 문서는 프로젝트 10개의 반복 제작비를 기준으로 **도구·자동화·검증·작업구조** 재사용 후보를 정리한다.

새 Tool Hub나 새 광역 Skill을 만들기 위한 목록이 아니다. 같은 책임의 기존 Base owner가 있으면 `EXISTING_OWNER_REUSE`가 기본이다.

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

**문제:** RNG·동시해결·stage progression이 있는 게임은 “왜 이 결과가 나왔나”를 재현하기 어렵다.

적용:
- TEN_PACES: 계획 resolution replay.
- OMENWARD: roulette + battle result.
- BLACKSMITH: 강화 outcome/lifecycle scenario.
- NINJA_SURVIVAL: reward/build/encounter sequence.
- TETRIS: piece/chain sequence test.
- SWITCHY: sealed layout retry.

```yaml
run_identity:
  build_or_commit:
  scenario_id:
  seed:
initial_state_hash:
input_events: []
state_checkpoints: []
result_hash:
replay_format_version:
```

검증:
1. 같은 build + scenario + seed + input → 같은 deterministic state hash가 필요한 범위를 선언.
2. presentation timestamp·animation jitter처럼 비결정적이어도 되는 값은 hash에서 제외.
3. replay가 private/hidden information을 부적절하게 노출하지 않는지 확인.

상태: `MODULE_CONTRACT_DEFINED · BASE_PROMOTION_CANDIDATE · IMPLEMENTATION_NOT_BUILT`.

---

## RM-TOOL-003 · BALANCE_SCENARIO_BATCH_SIMULATOR

**판정:** `EXISTING_OWNER_REUSE`.

Base `START_HERE.md`에는 **Balance & Scenario Lab이 다음 독립 후보지만 현재 미구현**이라고 명시돼 있다. 따라서 이 PR은 두 번째 balance tool을 만들지 않는다.

공통 계약만 확정한다.

```yaml
snapshot_input:
scenario_set:
seed_policy:
runs_per_scenario:
metrics:
  distributions: []
  tails: []
  dominant_choices: []
  failure_rates: []
comparison:
  baseline:
  candidate:
output:
  report:
  machine_readable_summary:
  patch_suggestions_non_authoritative:
```

1차 project scenarios:
- OMENWARD: roulette 확률·wave·unit 결과 분포.
- NINJA_SURVIVAL: 보상/백팩 조합/encounter build 성능.
- BLACKSMITH: 강화·경제·의뢰 결과 분포.
- TETRIS: Line/Chain reward bridge와 skill 선택 분포.

증거 ceiling:
- simulation은 플레이어 재미를 증명하지 않는다.
- patch suggestion은 프로젝트 수치 정본을 자동 수정하지 않는다.
- 실제 Tool 구현은 별도 owner/PR에서 진행.

---

## RM-TOOL-004 · QA_EVIDENCE_CAPTURE_ADAPTER

**판정:** `EXISTING_OWNER_REUSE`.

Base에는 이미 `tools/qa-evidence-studio/` 구현이 존재한다. 새 capture app을 만들지 않고 프로젝트 adapter/profile만 추가하는 방향을 우선한다.

```yaml
project_identity:
build_identity:
validation_contract:
  resolution:
  input_path:
  accessibility_checks:
  expected_state_or_screen:
capture_sources:
  screenshot:
  video:
  logs:
  machine_state:
verdict:
  human_or_rule_owner:
  evidence_ceiling:
```

추가 adapter가 필요할 때만 project-local launch/build/capture commands를 정의한다.

`QA_EVIDENCE_CAPTURE_ADAPTER != AI_AUTO_PASS`.

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
→ QA_EVIDENCE_CAPTURE_ADAPTER when runtime/UI evidence is needed
```

추천 대상: URBAN_LEGEND, NINJA_SURVIVAL, OMENWARD, GRIMOIRE, BLACKSMITH.

## B. RNG/해결 결과가 중요한 프로젝트

```text
DETERMINISTIC_SEED_REPLAY_CAPTURE
→ BALANCE_SCENARIO_BATCH_SIMULATOR
→ EXPLAINABLE_RESULT_PACKET
→ runtime/player validation
```

추천 대상: OMENWARD, NINJA_SURVIVAL, BLACKSMITH, TETRIS, TEN_PACES.

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

Godot 4.7 공식 문서는 Resource를 data container로, scripts/scenes를 주요 재사용 객체 메커니즘으로 설명한다. 따라서 공용 Godot Pilot이 필요할 때 다음을 우선 비교한다.

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

- Scenes/Resources의 재사용·인스턴스화를 `ADOPT`.
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
| P0 | `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE` | simulation/replay/debug 기반을 공유할 수 있음 |
| P1 | `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR` | 가치가 크지만 별도 Tool 구현과 프로젝트 snapshot adapter가 필요 |
| P1 | `RM-TOOL-004 QA_EVIDENCE_CAPTURE_ADAPTER` | 기존 Studio가 있어 새 Tool보다 adapter 소비 검증이 우선 |
| ACTIVE | `RM-WORK-001/002` | 이미 Base 방법으로 존재 |

# 완료 상태

이 문서의 신규 tool module은 `MODULE_CONTRACT_DEFINED`다. `RM-TOOL-004`의 Base QA Evidence Studio를 제외하면 공용 executable 구현을 완료했다고 주장하지 않는다. `Balance & Scenario Lab`은 현재 `IMPLEMENTATION_NOT_BUILT` 상태를 유지한다.
