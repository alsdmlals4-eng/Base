# RUNNABLE_BY_USER — Godot 실제 프로젝트 진입점 검증

## 목적

Godot Scene·Script·UI를 개별적으로 만드는 것과 사용자가 실제 프로젝트를 실행해 확인할 수 있는 상태는 다르다. 이 reference는 **사용자 실검증이 승인된 목표에 포함된 경우** 구현을 격리 Scene에서 끝내지 않고 실제 프로젝트 진입점까지 필요한 최소 범위로 연결하는 계약이다.

Godot의 `Run Current Scene`은 현재 Scene만 실행한다. `F5 / Run Project`는 프로젝트 Main Scene에서 시작한다. 사용자에게 실제 앱 흐름을 확인시키는 것이 목표라면 `Run Current Scene` 성공만으로 `RUNNABLE_BY_USER`를 충족했다고 판단하지 않는다.

## 활성 조건

다음 중 하나가 승인된 작업 계약에 있으면 이 Gate를 적용한다.

- 사용자가 Godot에서 직접 실행해 결과를 확인해야 한다.
- Vertical Slice·데모·대표 플레이 흐름을 실제 앱 시작부터 검증해야 한다.
- 새 `MainMenu`, App Router, 시작 화면, 부트스트랩 Scene 또는 그와 동등한 진입 흐름을 구현한다.
- 기능 자체보다 **실제 사용자가 도달하는 통합 경로**가 수용 기준이다.

반대로 독립 기술 실험, fixture, 명시적 Prototype/Test Scene만 검증하는 작업에는 자동 적용하지 않는다.

## A/B 결정 규칙

### A — 격리 Scene 유지

새 Scene·Router를 만들되 기존 프로젝트 진입점을 바꾸지 않는다.

A는 다음 경우에만 기본 선택할 수 있다.

- 사용자가 기존 Main Scene을 유지하라고 명시했다.
- 작업이 의도적으로 독립 `Prototype/Test Scene`이다.
- 실제 진입점 변경이 승인된 제품 흐름과 별개의 새로운 기획 결정을 요구한다.
- 안전한 rollback을 확보할 수 없거나 필요한 변경이 승인 범위를 넘어 L3 수준으로 확대된다.

A를 선택했다면 `Run Current Scene` 증거와 실제 프로젝트 진입점이 미연결 상태임을 명시한다. 사용자 실검증이 승인 목표인데 단순히 파일 수를 줄이기 위해 A를 선택해서는 안 된다.

### B — 실제 프로젝트 진입점 통합

사용자가 실제 프로젝트를 실행해 확인하는 것이 승인된 목표라면 **B를 기본 선택**한다.

필요한 최소 통합 변경에는 다음이 포함될 수 있다.

- `project.godot`의 `application/run/main_scene`
- `MainMenu` → `App Router` → 대상 기능으로 이어지는 Scene 연결
- 실제 진입에 필수적인 Autoload, InputMap, Resource 또는 Project Settings 연결
- 대상 기능으로 진입·복귀·종료하기 위해 필요한 최소 연결 코드

Task가 `scenes/vertical_slice/` 또는 `scripts/vertical_slice/ui/`처럼 주 구현 폴더를 지정하더라도, 사용자 실검증에 필수적인 `project.godot` 등의 통합 파일까지 금지한다는 뜻으로 자동 해석하지 않는다. 대신 **필요한 최소 통합 변경**만 허용된 integration edge로 취급한다.

B는 범위 무제한 확대 허가가 아니다. 실검증과 관계없는 정리, 리팩터링, 다른 Scene 교체, **무관한 Project Settings** 변경은 금지한다.

## 변경 위험도와 rollback

`project.godot`, Main Scene, Autoload, InputMap 또는 구조적 Scene 연결 변경은 기존 `L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE` 또는 실제 영향에 따라 L3 Gate를 그대로 적용한다.

변경 전:

1. 현재 `application/run/main_scene`과 대상 Scene·Router 상태를 기록한다.
2. Git status와 예상 changed files를 기록한다.
3. branch, checkpoint commit 또는 exact backup으로 `rollback` 경로를 확보한다.
4. 기존 사용자 변경과 보호 경로를 확인한다.

변경 후:

1. 실제 diff가 승인된 integration edge를 넘지 않는지 확인한다.
2. Godot import/parse 오류를 확인한다.
3. 관련 자동 테스트와 회귀 테스트를 실행한다.
4. 기존 정상 시작·복귀·종료 경로가 깨지지 않았는지 확인한다.
5. 예상 밖 Project Settings 변경이 있으면 원인을 판정하고 승인 범위 밖이면 되돌린다.

## 실행 검증 순서

```text
현재 Main Scene·rollback 기록
→ 필요한 최소 Scene/Router 구현
→ 필요한 최소 project.godot·통합 연결
→ import/parse
→ 관련 test
→ Run Current Scene smoke (필요 시)
→ F5 / Run Project
→ Main Scene 확인
→ MainMenu/App Router/대상 기능 실제 흐름 확인
→ 복귀·종료·오류·회귀 확인
→ diff 재검토
```

### F5 수용 기준

사용자 실검증 목표에서는 다음을 확인한다.

1. `F5 / Run Project`가 의도한 Main Scene에서 시작한다.
2. 시작 화면에서 대상 기능까지 사용자가 실제 UI/입력 흐름으로 도달할 수 있다.
3. `MainMenu`와 `App Router`가 있다면 실제 runtime에서 연결된다.
4. 기능 진입 후 최소 정상 경로를 완료할 수 있다.
5. 필요한 경우 이전 화면으로 복귀하거나 정상 종료할 수 있다.
6. parse/import/runtime 오류가 새로 발생하지 않는다.
7. 기존 필수 진입 경로를 교체했다면 해당 회귀 검증을 수행한다.

## 완료 상태 구분

- `USER_RUNNABLE_READY`: 구현과 실제 프로젝트 진입점 연결, 자동 검증 및 수행 가능한 runtime 검증까지 완료되어 사용자가 바로 확인할 수 있는 상태다.
- `HUMAN_VERIFIED`: 사용자가 직접 실행하거나 승인된 사람 검증자가 실제 화면·조작을 확인한 증거가 있다.
- `NOT_RUN`: 해당 runtime·device·human 검증을 실행하지 않았다.
- `BLOCKED_UNVERIFIED`: Editor/session, provider, rollback, 권한 또는 필요한 환경이 없어 검증할 수 없다.

`USER_RUNNABLE_READY`를 `HUMAN_VERIFIED`로 표현하지 않는다. 사용자가 아직 실행하지 않았다면 “사용자가 즉시 실검증 가능한 상태”까지만 보고한다.

## 보고 필드

```yaml
user_runnable_gate: APPLIED / NOT_APPLICABLE / BLOCKED_UNVERIFIED
entrypoint_decision: A_ISOLATED_SCENE / B_REAL_PROJECT_ENTRYPOINT
main_scene_before:
main_scene_after:
integration_edges_changed:
operation_level: L1 / L2 / L3
git_checkpoint:
rollback:
import_and_parse:
tests:
run_current_scene:
run_project_f5:
actual_user_flow:
regression:
user_runnable_status: USER_RUNNABLE_READY / NOT_RUN / BLOCKED_UNVERIFIED
human_status: HUMAN_VERIFIED / NOT_RUN
unverified:
```

## 실패 조건

- 사용자 실검증이 승인 목표인데 격리 Scene 생성만 하고 완료 처리
- `Run Current Scene` 성공을 `F5 / Run Project` 증거로 대체
- 실제 프로젝트 진입에 필요하다는 이유로 무관한 Project Settings까지 정리
- rollback 없이 `project.godot`·Autoload·InputMap·Main Scene 변경
- Task의 주 폴더 범위를 integration edge 전면 금지로 오해해 실제 앱 경로를 의도적으로 미연결
- 반대로 실검증을 이유로 승인되지 않은 제품 흐름·대규모 migration까지 확대
- `USER_RUNNABLE_READY`를 실제 사용자 확인인 `HUMAN_VERIFIED`로 허위 승격
