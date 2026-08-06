---
name: godot-live-editor-operations
description: Use in an installed Godot project when HiGodot capabilities must be bootstrapped, observed, mutated, validated, resumed, recovered, or upgraded.
---

# Godot Live Editor Operations

## 책임과 단일 실행 권위

이 파일은 프로젝트에 설치되는 얇은 작업 Skill이다. 공용 정책은 다음 Base 정본에서 읽고 프로젝트에 복제하지 않는다.

- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

```yaml
provider: hi-godot/godot-ai
execution_authority: SOLE_GODOT_EXECUTION_AUTHORITY
authority_count: 1
network_mode: LOOPBACK_ONLY
```

HiGodot Godot AI addon과 MCP 서버만 현재 Godot 편집 실행 권위다. Base custom MCP, Base network Bridge, 과거 live-editor Adapter와 Hera는 현재 실행 fallback이 아니다. 과거 Base 계약·Schema·Pilot·테스트는 보안·evidence·rollback의 감사 자료로만 읽는다.

프로젝트는 `HIGODOT_ADOPTION_RECORD.json`에서 정확한 provider pin, Godot 버전, host client, enabled domain, 검증 증거와 rollback pin만 소유한다. `exact_release_or_commit: NOT_CONFIGURED`, `network_mode != LOOPBACK_ONLY`, DeepSeek 등록, 또는 두 번째 mutation authority가 발견되면 engine action 전에 중단한다.

## Modes

`bootstrap` → `observe` → `mutate` → `validate` → `resume` → `recover`

## Bootstrap Gate

```text
validate Base adapter pin and generated snapshot
→ read HIGODOT_ADOPTION_RECORD.json
→ verify exact HiGodot release or commit
→ verify project.godot and active Editor/session
→ verify client profile
→ verify LOOPBACK_ONLY
→ reject duplicate Godot mutation authority
→ identify one primary domain
→ load minimum exact operation schema
```

다음이면 실행 전에 중단한다.

- HiGodot exact pin 없음 또는 실제 설치와 불일치
- 프로젝트·Editor/session을 특정할 수 없음
- `DeepSeek` 또는 미승인 host에서 요청
- LAN, public URL, port forwarding, remote tunnel
- HiGodot과 겹치는 두 번째 addon·MCP·Bridge 활성화
- 필요한 domain·operation을 확인하지 않고 추측 호출
- 변경 전 Git 복구 지점이 필요한데 없음

## 도구와 Context 선택

HiGodot의 전체 도구 catalog와 모든 Schema를 기본 Context에 넣지 않는다.

```text
작업 의도에서 domain 식별
→ readiness 확인
→ one primary domain
→ progressive schema discovery
→ minimum exact operation
→ bounded result
→ 상태 재관찰과 검증
```

- 지원되는 경우 rollup domain과 deferred schema loading을 사용한다.
- 한 단계에는 one primary domain만 둔다.
- 실패 후 무관한 도구를 순차 추측하지 않는다.
- mutation 재시도 전 target 상태를 다시 읽는다.
- HiGodot이 반환한 session·operation·Node reference를 사용한다.
- 큰 Scene tree·log·catalog는 필요한 부분만 요약한다.

## Operation Levels

### L0_OBSERVE

Editor/session, Scene hierarchy, Node·Resource·setting·log·diagnostics·test 상태를 읽는다.

- active project와 Editor/session을 확인한다.
- 필요한 범위만 읽는다.
- mutation 준비 관찰이면 대상 경로·현재 값·dirty/import 상태를 기록한다.

### L1_REVERSIBLE_WRITE

Node 생성·rename, property 변경, script attach, 일반 Scene·Resource 저장처럼 국소적이고 Git 또는 Editor undo로 복구 가능한 변경이다.

- target과 expected result를 기록한다.
- 실행 뒤 같은 대상을 재관찰한다.
- changed files와 diff를 검토한다.
- 관련 Godot parse/import/test를 실행한다.

### L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE

다음 HiGodot 기능은 금지하지 않고 사용한다.

- Node deletion
- file write, creation, modification, move, or deletion
- Scene 구조 변경
- project settings와 input map 변경
- autoload 추가·변경·제거
- script·Resource 교체와 구조적 filesystem 변경

필수 절차:

1. 사용자가 명시한 이름·대상·범위 안인지 확인한다.
2. 변경 전 Git status, 대상 Scene·Node·파일·setting을 기록한다.
3. branch, checkpoint commit 또는 exact backup으로 rollback을 확보한다.
4. 한 bounded operation group만 실행한다.
5. 전체 diff와 예상 밖 변경을 검토한다.
6. Godot import/parse와 영향 테스트를 실행한다.
7. runtime·device·human 미실행은 `NOT_RUN`으로 남긴다.

사용자가 요청한 Node deletion이나 file write는 같은 명명 범위에서 중복 질문하지 않는다. 새 삭제 대상, unrelated cleanup, project-wide 범위 확대는 사용자 승인을 다시 받는다.

### L3_HIGH_IMPACT_CHANGE

대규모 migration, 핵심 Scene·subsystem 삭제, 전역 project settings·autoload·input map 재구성, 저장소 전체 serialized asset rewrite다.

- written plan
- 적대적 사전 검토
- 명시적 사용자 승인
- isolated branch
- checkpoint commit
- full project regression
- rollback 검증

없이는 실행하지 않는다.

## Client Boundary

```yaml
Codex CLI:
  HiGodot MCP: enabled

GPT Godot Authoring profile:
  HiGodot MCP: enabled

DeepSeek Analysis profile:
  HiGodot MCP: absent
  credential: absent
  Godot access: forbidden
```

프로젝트 공용 `.vscode/mcp.json` 또는 `.codex/config.toml`을 만들지 않는다. 개인 host profile을 프로젝트 정본으로 복사하거나 credential을 evidence에 기록하지 않는다.

## Provider Adoption and Upgrade

`managing-game-project-operating-system`이 설치·exact pin·canary·rollback을 소유한다.

```text
release and security diff
→ isolated fixture
→ addon import/startup
→ read canary
→ destructive canary and exact restore
→ representative project canary
→ project regression
→ staged adoption
```

floating latest와 자동 무검토 업데이트는 금지한다. connection 성공이나 tools/list만으로 runtime·regression·production readiness를 PASS로 올리지 않는다.

## Existing Owner Routing

- 대안 조사·채택 판정: `evaluating-godot-assets-and-plugins-before-creation`
- 설치·provider pin·upgrade·rollback: `managing-game-project-operating-system`
- runtime 재현·원인 격리: `diagnosing-game-engine-runtime-failures`
- static·runtime·regression 검증: `reviewing-and-validating-project-changes`
- UI·screenshot·engine/physical input 구분: `auditing-and-refining-ui-art`
- pending task·checkpoint·resume: `maintaining-long-running-task-continuity`
- 외부 계약·Schema·catalog freshness: `auditing-canonical-reference-freshness`
- 반복 증거 기반 Skill 승격 판정: `evolving-project-discipline-skills`

현재 주 책임 owner가 작업 범위와 승인 경계를 정하고, 이 Skill은 HiGodot 실행·검증 증거를 묶는다.

## Mode Rules

### `bootstrap`

provider pin, addon 활성 상태, MCP host, project·Editor/session, client profile, network mode와 domain readiness를 검증한다.

### `observe`

필요한 domain의 최소 operation으로 현재 상태를 읽고 bounded output을 만든다.

### `mutate`

L1/L2/L3를 분류하고 해당 Gate를 충족한 operation만 실행한다. stale target 또는 scope mismatch는 중단한다.

### `validate`

HiGodot 응답만 신뢰하지 않고 Git diff, Godot 재관찰, import/parse, 관련 test, 가능한 runtime 결과를 교차 검증한다.

### `resume`

HiGodot이 반환한 기존 session·operation·job identity를 조회하고 initiating mutation을 중복 실행하지 않는다.

### `recover`

현재 Git·Scene·filesystem·Editor 상태를 다시 읽고 rollback 또는 forward recovery를 선택한다. addon 시작 실패 시 Godot recovery mode와 HiGodot 비활성화 절차를 사용하되 두 번째 addon으로 우회하지 않는다.

## Output

```yaml
mode:
provider: hi-godot/godot-ai
provider_pin:
project_identity:
editor_session:
client_profile:
operation_level:
primary_domain:
operation:
requested_scope:
changed_targets:
git_checkpoint:
rollback:
import_and_parse:
tests:
runtime:
human:
unverified:
production_readiness: false
```

## Failure Conditions

- HiGodot 외 두 번째 Godot 실행 권위
- DeepSeek MCP 등록 또는 credential
- non-loopback transport
- exact pin·rollback 없음
- 전체 tool/schema 선로딩
- wrong-tool wandering 또는 상태 재관찰 없는 retry
- 사용자 범위를 넘는 Node deletion·file write·project settings·autoload 변경
- L2에서 diff·rollback·import/test 누락
- L3에서 계획·명시 승인·full regression 누락
- connection·정적 파일 존재를 runtime·human·production PASS로 보고
