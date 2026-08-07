# HiGodot + GUT + Hera Godot Toolchain Design

## Status

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approved_direction: HIGODOT_AUTHORING_GUT_TEST_HERA_LIVE_QA
approved_by_user: true
approved_at: 2026-08-07
base_main: 4f98f968a377f7b6a11aafa4fc94d11bddbebedc
branch: agent/godot-higodot-gut-hera-toolchain-implementation
implementation: BASE_IMPLEMENTATION_COMPLETE
project_installation: NOT_STARTED
merge_authorization: GRANTED
merge_authorized_at: 2026-08-07
```

## 1. Goal

Godot 프로젝트에서 AI와 자동화가 실제 제작·검증·실행 QA까지 이어지도록 다음 세 도구를 역할이 겹치지 않는 하나의 작업 루프로 사용한다.

```text
HiGodot
= persistent Godot authoring / editor mutation authority

GUT
= deterministic GDScript test authority when adopted

Hera Agent Godot CLI
= live runtime QA / input / screenshot / diagnostics / observation authority
```

핵심 목적은 세 도구를 단순 설치하는 것이 아니라 다음 증거 사슬을 만드는 것이다.

```text
요구와 승인 범위
→ HiGodot으로 구현
→ Godot import / parse
→ GUT focused tests
→ GUT regression
→ Hera live run / input / inspect / assert / diagnostics / screenshot
→ Hera 단계의 source-mutation 없음 확인
→ Git diff
→ adversarial review
```

이 설계는 2026-08-06에 병합된 HiGodot 단일 저작 권위와 선택적 Godot addon 활용 정책을 폐기하지 않는다. 테스트와 live QA를 별도 책임으로 분리하여 단일 저작 권위를 유지한 채 검증 폭을 확장한다.

## 2. Current Base authority and conflict

현재 Base 정본 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`는 HiGodot을 유일한 Godot 저작·편집 mutation authority로 둔다. 동일 책임의 두 번째 MCP, EditorPlugin, Bridge 또는 CLI mutation authority는 금지한다.

현재 정본은 Hera Agent Godot을 `BENCHMARK_REFERENCE_ONLY`로 두고 활성화를 금지한다. 반면 최신 addon 활용 정책은 테스트, 대화, 플랫폼 서비스, 개발 편의처럼 저작 권위가 다른 addon은 평가·소비 경로·rollback을 갖춘 경우 선택적으로 공존할 수 있도록 허용한다.

Hera v1은 editor mutation 기능도 제공하므로 아무 제한 없이 HiGodot과 동시에 활성화하면 기존 단일 저작 권위를 깨뜨린다. 따라서 Hera 전체 기능을 두 번째 저작 권위로 채택하지 않고, live QA와 observation 기능만 운영 권한으로 채택한다.

## 3. External benchmark facts as of 2026-08-07

### 3.1 HiGodot / Godot AI

Official source:

- https://github.com/hi-godot/godot-ai

확인된 현재 공개 계약:

- Godot 4.5+를 요구하고 4.7+를 권장한다.
- 약 43개 MCP tool에서 120개 이상의 operation을 제공한다.
- Scene, Node, Script, UI, Material, Animation 등 실제 editor authoring 범위를 제공한다.
- Codex는 `godot-ai attach` stdio bridge 구성을 지원한다.
- 자체 `McpTestSuite` GDScript 테스트 프레임워크와 `test_run`도 포함한다.

Base disposition:

```yaml
provider: hi-godot/godot-ai
disposition: REUSE
role: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
```

### 3.2 GUT

Official sources:

- https://github.com/bitwes/Gut
- https://gut.readthedocs.io/en/latest/Command-Line.html

확인된 현재 공개 계약:

- GUT 9.x는 Godot 4.x용이다.
- CLI 실행을 지원한다.
- 테스트 성공은 exit code `0`, 실패는 `1`을 반환한다.
- JUnit XML 결과를 내보낼 수 있다.
- Godot 버전별 호환 버전은 공식 README에서 분리한다.

2026-08-07 기준 호환 핀 후보:

| Godot | GUT |
|---|---|
| 4.7.x | 9.7.1 |
| 4.6.x | 9.6.1 |
| 4.5.x | 9.5.0 |
| 4.3.x–4.4.x | 9.4.0 |
| 4.2.x | 9.3.0 |

새 Godot 또는 GUT 릴리스가 나오면 이 표를 영구 상수로 신뢰하지 않고 공식 README를 다시 확인한다.

Base disposition:

```yaml
provider: bitwes/Gut
disposition: REUSE
role: DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED
```

### 3.3 Hera Agent Godot

Official sources:

- https://store.godotengine.org/asset/notnull92/hera-agent-godot/
- https://github.com/NotNull92/hera-agent-godot

확인된 현재 공개 계약:

- 현재 Asset Store 버전은 v1.0.0이다.
- v1 major line은 CLI invocation, output stream, exit-code meaning, response field, JSON type에 stable contract와 SemVer/deprecation 정책을 둔다고 명시한다.
- Godot 4.2–4.7 stable에서 검증됐다고 명시하고 4.7을 권장한다.
- localhost HTTP EditorPlugin + compact JSON CLI 구조다.
- editor read/write, runtime inspect/input/assert, diagnostics, screenshot capture/diff, QA 기능을 제공한다.
- CLI와 addon을 함께 업데이트하고 Godot을 완전히 재시작하는 upgrade 절차를 안내한다.
- shared token을 사용할 수 있다.

이전 조사에서 Hera v1.0.0을 Asset Store의 `unstable` 표시로 분류한 판단은 현재 공식 페이지와 일치하지 않는다. 이 설계는 그 판단을 폐기한다.

Hera의 low-token 수치 비교는 공급자가 공개한 자체 측정·추정이다. Base가 독립 측정한 결과로 취급하지 않으며 실제 프로젝트에서 local token/call/output 측정을 하기 전에는 성능 우위를 확정 사실로 기록하지 않는다.

Base disposition:

```yaml
provider: NotNull92/hera-agent-godot
disposition: REUSE
role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
persistent_editor_mutation_authority: false
```

## 4. Authority model

```yaml
persistent_godot_authoring:
  provider: HiGodot
  authority_count: 1

gdscript_project_tests:
  provider: GUT
  authority_count: 1
  condition: GUT_ADOPTED

live_runtime_qa_and_observation:
  provider: Hera CLI
  authority_count: 1
  persistent_source_mutation: forbidden

final_repository_change_truth:
  provider: Git
```

### 4.1 HiGodot owns persistent authoring

HiGodot이 담당한다.

- Scene과 Node의 생성·삭제·구조 변경
- script 생성·수정·attach
- Resource·Theme·Material 등의 persistent 변경
- project settings, input map, autoload
- 파일 생성·수정·이동·삭제
- persistent editor mutation 이후 저장·재관찰

기존 Base L0–L3 operation gate와 rollback·diff·import·test 요구는 유지한다.

### 4.2 GUT owns deterministic GDScript project tests

GUT이 채택된 프로젝트에서는 반복 가능한 GDScript 기반 프로젝트 테스트 suite의 기본 정본을 GUT으로 둔다.

대상 예:

- 게임 규칙
- 상태 전이
- 저장·불러오기
- 경제·전투·퍼즐
- 데이터 변환
- regression 가능한 UI/domain logic

HiGodot의 `McpTestSuite`는 GUT과 같은 요구를 중복 구현하는 두 번째 canonical suite가 되지 않는다. 기존 프로젝트에 이미 `McpTestSuite` 테스트가 있다면 자동 삭제·변환하지 않고 프로젝트별 migration input으로 분류한다.

```yaml
when_gut_is_adopted:
  new_canonical_gdscript_project_tests: GUT
  duplicate_same_case_in_mcp_test_suite: forbidden
  existing_mcp_test_suite_tests: PRESERVE_UNTIL_PROJECT_DECISION
```

C#/.NET 테스트, 네이티브 SDK 테스트, 플랫폼 sandbox 테스트, 빌드·패키징 테스트처럼 GUT의 책임 밖인 검증 체계는 이 규칙으로 대체하지 않는다.

GUT이 필요 없는 기획 전용 또는 실행 코드가 없는 프로젝트에는 설치하지 않는다.

### 4.3 Hera owns live QA, not persistent authoring

Hera는 실제 Editor와 running game을 관찰하고 입력·QA 증거를 만드는 데 사용한다.

기본 허용 책임:

- Editor/instance readiness 확인
- read-only scene/node/resource/theme inspection
- game run / stop
- runtime tree와 runtime UI inspection
- 실제 input injection과 input-log 확인
- semantic click과 state assertion
- output / diagnostics
- screenshot capture
- local screenshot diff
- `game qa diagnose`
- smoke
- 위 허용 명령만 포함하는 bounded batch

기본 금지 책임:

- scene/node persistent add/remove/set
- script create/edit
- project file/folder mutation
- resource persistent write
- `theme set`
- main scene 변경
- persistent filesystem mutation
- editor state를 변경할 수 있는 `eval`
- HiGodot과 동일 결과를 만드는 editor authoring operation

Hera의 `game set` 또는 runtime `call`처럼 실행 중 상태를 강제로 바꾸는 기능은 소스 persistent mutation은 아니지만 실제 플레이 경로를 우회할 수 있다. 따라서 일반 acceptance evidence에는 사용하지 않는다.

필요한 경우 다음 제한적 상태로만 허용한다.

```yaml
hera_runtime_mutation_exception:
  mode: DIAGNOSTIC_ONLY
  acceptance_evidence: false
  reason_required: true
  restore_or_restart_required: true
```

Screenshot diff의 threshold는 anti-aliasing 흔들림을 줄이는 기계적 허용치일 뿐 디자인 품질 승인 기준이 아니다. 시각적 스타일·구도·가독성처럼 사람 판단이 필요한 항목은 별도 human review 상태를 유지한다.

## 5. Selective adoption, not blanket installation

Base에 세 도구의 역할 계약을 추가한다고 해서 모든 Godot 저장소에 세 addon을 자동 복사하지 않는다.

프로젝트별 판정:

```text
AI authoring 필요
→ HiGodot 평가·exact pin·canary

테스트 가능한 GDScript 제품 코드 존재
→ GUT 평가·Godot 호환 pin·실제 test consumption path

실행 가능한 game과 live QA 필요
→ Hera 평가·CLI/addon pair pin·live QA consumption path
```

프로젝트가 현재 단계를 충족하지 않으면 `DEFERRED`다. 설치돼 있지만 실제 소비 경로가 없으면 기존 정책대로 `INSTALLED_UNUSED`로 판정한다.

세 도구를 모두 쓰는 활성 Godot 제품 프로젝트의 목표 상태 예시는 다음과 같다.

```yaml
HiGodot:
  state: ADOPTED_ACTIVE
  consumption: editor_authoring

GUT:
  state: ADOPTED_ACTIVE
  consumption: focused_and_regression_tests

Hera:
  state: ADOPTED_ACTIVE
  consumption: live_runtime_qa
```

## 6. Version and upgrade contract

모든 프로젝트 adoption은 floating latest를 금지한다.

### HiGodot

기존 `HIGODOT_ADOPTION_RECORD.json`의 exact release 또는 exact commit, Godot version, canary, regression, rollback 정책을 그대로 사용한다.

### GUT

```yaml
gut_exact_version: required
godot_compatibility_match: required
floating_latest: forbidden
upgrade_review: required
focused_test_after_upgrade: required
regression_after_upgrade: required
rollback_or_removal: required
```

Godot engine upgrade와 GUT upgrade를 독립적으로 보지 않는다. engine version이 바뀌면 공식 GUT compatibility matrix를 다시 확인한다.

### Hera

```yaml
hera_cli_exact_version: required
hera_addon_exact_version: required
cli_addon_version_pair_match: required
floating_latest: forbidden
full_editor_restart_after_upgrade: required
status_smoke_after_upgrade: required
live_qa_canary: required
rollback_or_removal: required
```

v1 stable contract는 무검토 자동 업데이트의 근거가 아니다. minor release에서도 additive field와 experimental surface가 변할 수 있으므로 exact pin과 canary를 유지한다.

## 7. Local security and transport boundary

HiGodot은 기존 Base의 loopback-only 정책을 유지한다.

Hera도 Base 채택에서는 로컬 개발 PC의 loopback 범위로 제한한다.

```yaml
hera_transport:
  localhost_only: true
  lan: forbidden
  public_exposure: forbidden
  port_forwarding: forbidden
  remote_tunnel: forbidden
  shared_token: required_for_base_adoption
```

shared token 원문은 저장소, evidence, prompt, log에 기록하지 않는다. 프로젝트에는 token 존재 여부와 검증 상태만 남긴다.

GUT은 테스트 runner이며 별도 network authority를 갖지 않는다.

## 8. Standard execution flow

### 8.1 Bootstrap

```text
project identity
→ exact Godot version
→ Base/project adapter integrity
→ HiGodot exact pin and readiness
→ GUT adoption and exact compatible version
→ Hera CLI/addon exact pair and localhost/shared-token readiness
→ Git status / rollback checkpoint
```

필요한 도구가 채택되지 않은 단계라면 억지로 설치하지 않고 `DEFERRED` 또는 `NOT_CONFIGURED`를 기록한다.

### 8.2 Author

```text
requirements and scope
→ HiGodot L0 observation
→ HiGodot L1/L2/L3 classification
→ HiGodot persistent mutation
→ re-observe target
→ Git diff
→ Godot import / parse
```

### 8.3 Deterministic test

```text
smallest affected GUT test selection
→ focused GUT run
→ failure returns to HiGodot authoring
→ package gate에서 affected regression 또는 full regression
→ optional/required project JUnit evidence
```

GUT CLI의 실패 exit code를 무시하고 다음 단계로 진행하지 않는다.

### 8.4 Live QA

Hera 단계 시작 직전에 현재 tracked working-tree state를 snapshot한다.

```text
pre-Hera git status / tracked-diff fingerprint
→ hera status / instances
→ game run
→ real input or semantic click
→ runtime inspect / assert
→ output / diagnostics
→ screenshot capture / diff when relevant
→ game qa diagnose when relevant
→ stop or controlled reset
→ post-Hera git status / tracked-diff fingerprint
```

Hera QA 단계는 시작 전에 존재하던 HiGodot 변경을 없애라고 요구하지 않는다. 대신 **Hera 단계 자체가 새로운 tracked source mutation을 추가하지 않았음**을 증명한다.

```yaml
hera_phase_tracked_source_delta: NONE
```

Hera 단계 전후 fingerprint가 다르고 그 차이가 live QA의 허용된 runtime artifact가 아니라 tracked project source라면 acceptance를 중단한다.

### 8.5 Final review

```text
Git diff
→ GUT result
→ Hera live evidence
→ requirement coverage
→ adversarial attack
→ validate critique
→ regression recheck
→ decision report
```

## 9. Failure routing

### HiGodot authoring failure

- mutation retry 전에 현재 Editor/Scene 상태를 다시 읽는다.
- Hera의 editor write로 우회하지 않는다.
- 필요한 경우 Hera read-only diagnostics로 runtime 또는 Editor observation을 보조할 수 있다.

### GUT failure

- 실패 테스트와 요구를 비교한다.
- 구현 결함이면 HiGodot authoring으로 돌아간다.
- 테스트 자체가 구형 요구를 주장하면 기획·정본 비교 후 test change를 별도 판정한다.
- 테스트를 통과시키기 위해 assertion을 임의 완화하지 않는다.

### Hera live QA failure

- input-log, assertion, diagnostics, screenshot 등 재현 증거를 보존한다.
- persistent 수정은 HiGodot에서 수행한다.
- 수정 뒤 최소 affected GUT와 Hera scenario를 다시 실행한다.

### Tool unavailable or incompatible

- 다른 도구에 같은 권한을 넘겨 임시 통과시키지 않는다.
- `NOT_CONFIGURED`, `NOT_RUN`, `BLOCKED_UNVERIFIED`, `DEFERRED` 중 실제 상태를 기록한다.

## 10. Evidence contract

최소 실행 보고:

```yaml
project_identity:
godot_version:

higodot:
  exact_pin:
  operation_level:
  changed_targets:
  import_parse:

gut:
  adoption_state:
  exact_version:
  selected_tests:
  exit_code:
  result:
  junit_evidence:

hera:
  adoption_state:
  cli_exact_version:
  addon_exact_version:
  transport: LOOPBACK_ONLY
  shared_token_present: true/false/unverified
  scenarios:
  runtime_assertions:
  diagnostics:
  screenshots:
  pre_post_tracked_delta: NONE/CHANGED/UNVERIFIED

git_diff:
adversarial_review:
runtime:
human:
unverified:
production_readiness: false
```

파일 존재, tool listing, connection 성공만으로 GUT regression, Hera live QA 또는 production readiness를 PASS로 올리지 않는다.

## 11. Base integration design

새 광역 Skill을 만들지 않는다. 기존 owner를 확장한다.

### Canonical policy

`docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

- HiGodot의 단일 **persistent authoring** 권위 유지
- Hera `BENCHMARK_REFERENCE_ONLY` 고정 금지를 제거
- Hera를 restricted live-QA/observation provider로 정의
- GUT canonical deterministic GDScript testing boundary 연결
- Hera editor mutation 금지와 pre/post source-delta guard 추가

### Godot evaluation owner

`skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`

- HiGodot/GUT/Hera 역할 분리 평가
- Godot↔GUT compatibility pin
- Hera CLI/addon pair와 support evidence
- consumption path와 `INSTALLED_UNUSED` 판정
- 같은 authoring authority 중복 검사

### Project operating-system owner

`skills/managing-game-project-operating-system/SKILL.md`

- third-party inventory에서 GUT/Hera exact version·role·consumption·validation·rollback 확인
- 기존 HiGodot adoption record는 HiGodot provider record로 유지
- 프로젝트별 선택적 채택과 upgrade verification 추가

### Installed Godot operations Skill

`templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`

현재의 HiGodot authoring workflow를 다음 orchestration으로 확장한다.

```text
HiGodot author
→ GUT deterministic validation when adopted
→ Hera live QA when adopted and runnable
→ Git/adversarial validation
```

이 Skill이 GUT 테스트 본문이나 Hera 정책 정본을 복제하지 않고 공용 policy와 project inventory를 참조한다.

### Discovery

`START_HERE.md`의 Godot 자동화 route에서 세 역할을 한 단계 안에 발견할 수 있게 한다. 필요한 경우 기존 Documentation Map과 shared-route reference를 갱신하되 새 broad route/Skill은 만들지 않는다.

### Tests

기존 aggregate contract suite에 focused regression을 연결한다. 새 GitHub Actions workflow를 만드는 것이 기본안이 아니다.

필수 불변 조건:

1. HiGodot만 persistent Godot authoring authority다.
2. Hera persistent editor/source mutation은 활성 QA 경로에서 금지된다.
3. GUT adoption은 exact Godot-compatible pin과 실제 test consumption을 요구한다.
4. GUT 채택 프로젝트에서 동일 GDScript test case를 McpTestSuite와 두 canonical suite로 유지하지 않는다.
5. C#/.NET·native·platform test authority는 GUT으로 강제 대체하지 않는다.
6. Hera CLI/addon pair exact pin과 localhost boundary가 있다.
7. Hera acceptance QA는 pre/post tracked source delta가 없어야 한다.
8. `game set/call` 진단 예외는 acceptance evidence가 아니다.
9. 세 도구를 모든 프로젝트에 일괄 설치하지 않는다.
10. installed-unused state는 제거 또는 defer된다.
11. 신규 ACTIVE Skill 수는 증가하지 않는다.

## 12. Adversarial pre-review

### MUST_FIX resolved by this design

| Finding | Resolution |
|---|---|
| HiGodot와 Hera가 동시에 editor write를 하면 authoring authority가 2개가 됨 | Hera persistent write 금지, HiGodot 단일 authoring 유지 |
| GUT과 HiGodot McpTestSuite가 같은 테스트의 두 정본이 될 수 있음 | GUT adopted 시 새 canonical GDScript project tests는 GUT, 기존 McpTestSuite는 migration input |
| GUT을 모든 test authority로 해석하면 C#/.NET·플랫폼 검증을 침범함 | GUT 권위를 GDScript 반복 테스트로 한정 |
| Hera runtime mutation으로 실제 플레이 경로를 우회할 수 있음 | `DIAGNOSTIC_ONLY`, acceptance evidence 금지 |
| Hera QA가 실수로 source를 변경할 수 있음 | pre/post tracked-diff fingerprint, Hera-phase delta `NONE` 요구 |
| Godot/GUT 버전 불일치 | official compatibility matrix 기반 exact pin |
| Hera CLI와 addon 버전 drift | exact pair match + full Editor restart + smoke |
| localhost addon이 다른 local process에 노출될 수 있음 | Base adoption에서 shared token 요구, secret 비기록 |
| provider marketing token 수치를 사실로 확정할 위험 | 독립 실측 전 vendor claim으로만 취급 |
| 비표준 disposition 이름이 Base 상태 모델을 흐릴 수 있음 | `disposition: REUSE` + 별도 `role_restriction`으로 정규화 |

### REJECTED_CRITIQUE

- `Hera가 write 기능을 갖고 있으므로 도구 전체를 금지해야 한다`: 역할 제한과 source-delta 검증으로 live QA 가치를 보존할 수 있으므로 과잉 제한이다.
- `세 도구를 쓰려면 새 Godot orchestration Skill이 필요하다`: 기존 evaluation, operating-system, installed operation owner로 책임을 보존할 수 있어 새 broad Skill은 중복이다.
- `HiGodot McpTestSuite가 있으므로 GUT은 필요 없다`: GUT은 독립 test framework, CLI exit contract, JUnit, mature test utilities를 제공하며 사용자 요구와 반복 가능한 GDScript project test authority에 부합한다. 단 프로젝트별 실제 필요가 없으면 설치하지 않는다.

## 13. Non-goals

이번 설계 및 다음 Base 구현은 다음을 포함하지 않는다.

- 모든 Godot 프로젝트에 GUT/Hera 일괄 설치
- 실제 사용자 프로젝트의 addon 복사·활성화
- 개인 MCP 설정 또는 credential 수정
- Hera source fork
- Hera persistent editor authoring 허용
- HiGodot 제거 또는 authoring authority 축소
- 기존 프로젝트 테스트의 자동 GUT migration
- C#/.NET·native·platform test framework 대체
- 새로운 Base MCP, Bridge, CLI wrapper 또는 broad Skill 제작
- CI 비용을 늘리는 새 workflow를 근거 없이 추가
- 실제 Windows/Android/device/human production readiness 주장

## 14. Definition of done for implementation

다음 구현 단계의 완료 기준은 다음과 같다.

- 공용 Godot 정본이 HiGodot/GUT/Hera 역할 경계를 한 번만 정의한다.
- 기존 owner Skill과 project template이 해당 정본을 소비한다.
- START_HERE에서 Godot 요청이 세 역할을 발견할 수 있다.
- HiGodot single-authority regression이 계속 통과한다.
- GUT exact compatible pin과 consumption-path 계약이 테스트된다.
- Hera exact pair, localhost/shared-token, persistent-write prohibition, source-delta guard가 테스트된다.
- 동일 GDScript 테스트 이중 정본 방지 규칙이 있다.
- C#/.NET·native·platform 검증 책임을 침범하지 않는다.
- 신규 ACTIVE Skill이 없다.
- project-specific forced installation이 없다.
- implementation exact head에서 focused contract tests와 기존 관련 aggregate suite가 통과한다.
- adversarial review의 unresolved P0/P1이 0이다.
- 실제 project/runtime 실행을 하지 않았다면 `NOT_RUN`으로 남긴다.

## 15. Written-spec self-review

자체검토에서 다음 두 모호성을 발견했고 같은 문서에서 수정했다.

1. Hera disposition에 Base enum 밖의 이름을 쓰던 표현을 `REUSE + role_restriction`으로 정규화했다.
2. GUT 권위를 모든 project test가 아닌 GDScript 기반 반복 테스트로 한정해 C#/.NET·native·platform test 책임을 보존했다.

최종 체크:

```yaml
placeholder_TODO: 0
placeholder_TBD: 0
internal_authority_conflict: 0
base_disposition_enum_valid: true
non_gdscript_test_scope_preserved: true
new_broad_skill: false
blanket_project_installation: false
higodot_authoring_authority_count: 1
gut_gdscript_test_authority_when_adopted: 1
hera_persistent_authoring_authority: 0
hera_live_qa_role: defined
external_vendor_claims_separated_from_base_evidence: true
implementation: BASE_IMPLEMENTATION_COMPLETE
```