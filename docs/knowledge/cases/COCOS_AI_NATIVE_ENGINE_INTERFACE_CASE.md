# COCOS 4 / Cocos CLI AI-native engine interface case

## Purpose

이 사례는 2026-08-24 기준 COCOS 4와 Cocos CLI의 공개 구조에서 **게임 엔진을 교체하지 않고 재사용할 수 있는 machine-facing 개발 계약**만 추출한다. Cocos 구현물·TypeScript/C++ stack·CLI/MCP server를 Base 또는 프로젝트 dependency로 채택하는 문서가 아니다.

```yaml
decision: PATTERN_EXTRACT
ENGINE_DECISION_GODOT_REMAINS: true
COCOS_TECHNIQUES_ONLY: true
NO_ENGINE_MIGRATION: true
runtime_dependency_added: false
new_godot_writer_added: false
```

## Source observations

확인일: 2026-08-24.

1. COCOS 4 공개 README는 과거 Cocos Creator에서 결합되어 있던 엔진과 에디터를 분리하고, AI 통합을 위해 cross-platform framework와 editor core component를 CLI tool로 전환해 engine core capability에 포함하는 방향을 명시한다.
2. Cocos CLI의 공식 command 문서는 project 작업에서 명시적 `--project` 경로를 사용하고 `cocos start-mcp-server --project <project-path>`를 제공한다. 전역 `--no-interactive` 옵션은 CI/자동화 용도로 설명되고 build에는 `--log-dest`가 있다.
3. Cocos CLI 저장소는 unit/E2E test 경로를 함께 제공한다. CONTRIBUTING 문서는 MCP API schema/tool 변경 뒤 `npm run generate:mcp-types`로 E2E용 type-safe definition을 생성하도록 요구하며 E2E/coverage/debug 흐름을 공개한다.
4. COCOS 4의 GitHub Releases에서 2026-08-24 현재 latest 표시는 `4.0.0-alpha.28`이며 2026-08-03 공개다. 따라서 구조적 방향은 참고 가치가 있지만 COCOS 4 자체의 production maturity를 Godot 교체 근거로 사용하지 않는다.

Primary sources:

- https://github.com/cocos/cocos4
- https://github.com/cocos/cocos4/releases
- https://github.com/cocos/cocos-cli
- https://github.com/cocos/cocos-cli/blob/main/docs/en/commands.md
- https://github.com/cocos/cocos-cli/blob/main/docs/en/quick-start.md
- https://github.com/cocos/cocos-cli/blob/main/CONTRIBUTING.md

## Problem extracted from the benchmark

AI/CI가 게임 엔진을 다룰 때 GUI를 자동 클릭하거나 자연어 설명만 믿으면 다음 오류가 생기기 쉽다.

- 잘못된 프로젝트·Scene·Editor instance를 대상으로 작업한다.
- CLI와 MCP가 별도 로직을 가져 같은 operation의 의미가 달라진다.
- schema와 실제 adapter가 어긋나 agent가 존재하지 않는 인자나 동작을 추측한다.
- MCP server 연결이나 tool listing 성공을 실제 게임 변경 성공으로 오판한다.
- 실행 결과가 project/ref/tool version/log/artifact와 결속되지 않아 Implementation Reality Gate를 통과시킬 수 없다.

외부 엔진을 도입하지 않고도 이 문제 해결 구조는 provider-neutral contract로 추출할 수 있다.

## Base fit

Base에는 이미 `TOOL_INTERFACE_SURFACE_SELECTION`이 있어 reusable core 아래 machine-facing CLI/programmatic contract를 두고 human surface를 adapter로 한정한다. COCOS 사례에서 새로 강화할 부분은 **게임 엔진·도구를 agent가 호출할 때의 typed project/operation/evidence boundary**다.

추출 계약은 `docs/CAPABILITY_COMPOSITION_MAP.md`의 `AI_GAME_ENGINE_MACHINE_BOUNDARY`가 소유한다.

```text
exact project identity
→ typed operation
→ shared bounded core
   ├─ CLI
   └─ MCP
→ behavior E2E
→ Implementation Reality Gate
→ structured execution evidence
```

## ADOPT / ADAPT / REJECT

### ADOPT

- `PROJECT_IDENTITY_BEFORE_OPERATION`: machine operation 전에 exact project identity를 결속한다.
- `SHARED_CORE_FOR_CLI_AND_MCP`: CLI/MCP adapter가 하나의 bounded operation core를 공유한다.
- `MCP_E2E_BEHAVIOR_CONTRACT`: transport 연결이 아니라 대표 operation의 project/result/evidence behavior E2E를 검증한다.
- `NONINTERACTIVE_AUTOMATION_PATH`: 승인·보호 Gate를 보존하면서 CI/agent가 사용할 non-interactive path를 제공한다.
- `STRUCTURED_EXECUTION_EVIDENCE`: exact project/ref, adapter/tool version, operation, result, artifacts/log와 미실행 상태를 함께 기록한다.

### ADAPT

- `SCHEMA_GENERATED_TOOL_SURFACE`: Cocos의 TypeScript code generation을 그대로 들여오지 않는다. 현재 Base/Godot/Python 도구에 맞춰 한 closed operation schema/type source에서 CLI/MCP validators·types·fixtures를 생성하거나 기계적으로 동기 검증하는 원리만 적용한다.
- Cocos의 engine/editor 분리 방향은 `core → machine adapter → optional human surface`라는 기존 Base 구조를 강화하는 비교 근거로 사용한다. Godot Editor를 제거하거나 Cocos식 Editor stack을 재구현하지 않는다.

### REJECT NOW

- COCOS 4 또는 Cocos Creator로 기존 프로젝트 엔진 이전.
- Cocos CLI, Node/TypeScript toolchain, COCOS SDK를 Base 필수 dependency로 추가.
- Cocos MCP server를 Godot authoring authority로 사용.
- 새 Tool Hub, Cocos Wizard 복제, 두 번째 GUI 관리 surface 생성.
- HiGodot과 겹치는 두 번째 persistent Godot mutation writer 생성.
- COCOS 4 Alpha 상태의 방향성을 현재 production readiness 증거로 확대 해석.

## Godot authority preservation

`ENGINE_DECISION_GODOT_REMAINS`는 단순 선호가 아니라 이 사례의 명시적 경계다. 현재 Base P06의 Godot toolchain authority는 이 변경으로 바뀌지 않는다.

```text
Godot
├─ persistent authoring: current HiGodot single-authority contract
├─ deterministic GDScript tests: GUT when adopted
├─ live runtime QA/observation: Hera under its restricted role
└─ final repository truth: Git
```

`AI_GAME_ENGINE_MACHINE_BOUNDARY`는 위 owner들이 제공하거나 소비하는 machine-facing contract를 더 명확하게 만들 수 있지만, owner 자체를 대체하거나 추가하지 않는다.

## Evidence ceiling

이번 채택으로 주장할 수 있는 것은 다음까지다.

```yaml
cocos_upstream_pattern_observed: SOURCE_VERIFIED
base_pattern_extracted: CONTRACT_IMPLEMENTED_IN_PR
cocos_runtime_adopted: false
godot_engine_changed: false
new_mcp_runtime_implemented: false
target_project_behavior_e2e_added_by_this_case: false
```

이 사례 문서와 contract regression이 통과해도 개별 Godot 프로젝트의 machine operation이 자동으로 `BEHAVIOR_E2E_VERIFIED`가 되는 것은 아니다. 실제 tool/adapter를 변경하는 후속 작업에서는 대표 project operation을 실행하고 exact target/result/evidence를 다시 검증해야 한다.

## Reuse decision

현재 disposition은 **`PATTERN_EXTRACT + ENGINE_STAY_GODOT`**다.

Cocos가 이후 Beta/Stable로 전환하거나 CLI/MCP contract가 크게 바뀌면 source observation은 다시 확인할 수 있다. 그 변화 자체는 Godot migration trigger가 아니며, 현재 Godot toolchain보다 명확한 장기 가치와 target-project evidence가 있을 때만 별도 엔진 비교를 연다.
