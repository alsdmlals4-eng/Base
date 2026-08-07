# One-Click Play Handoff Policy

## 목적

대표 Vertical Slice·Demo·사용자 검수 빌드는 저장소를 정상 동기화한 뒤 엔진의 기본 **Project Play**만 실행하면 실제 플레이 흐름을 확인할 수 있어야 한다. 사용자가 별도 Scene 선택, Project Settings 변경, 입력 모드 전환, 플러그인·feature flag 설정, 파일 교체를 해야 하는 상태는 최종 인계가 아니다.

## 적용 범위

- 게임 프로젝트의 대표 Vertical Slice와 Demo
- 사용자·기획자·리뷰어에게 전달하는 로컬 실행 빌드
- 기본 프로젝트 진입점과 대표 플레이 흐름
- GitHub 원격 변경을 사용자 로컬 작업공간으로 전달하는 절차

개발자용 validation harness, 테스트 Scene, 플랫폼별 export·feature override는 별도로 유지할 수 있다. 다만 일반 사용자의 기본 실행 경로를 대체하거나 숨기면 안 된다.

## 정본 책임

- 대표 플레이 범위·성공·실패·복귀: `designing-vertical-slices`
- 실제 기본 실행·UI·입력·회귀 검증: `reviewing-and-validating-project-changes`
- commit·push와 로컬 동기화 안전성: `synchronizing-local-and-github-state`
- repository·branch·commit SHA·실행 인계: `maintaining-project-context-and-handoff`
- 프로젝트 적용 서식: Base의 Vertical Slice·검증·Handoff Template

이 문서는 공통 계약만 정의한다. 프로젝트 고유 Scene 경로, 실행 파일, 조작법, 플랫폼 Gate는 프로젝트 저장소가 기록한다.

## 전달 흐름

실행 요약: `Fetch origin → Pull origin → 로컬 HEAD 확인 → Project Play`

```text
승인된 구현·자동 검증
→ 작업 Branch에 commit·push
→ 사용자에게 repository·branch·commit SHA 전달
→ GitHub Desktop에서 해당 repository·branch 선택
→ Fetch origin
→ Pull origin
→ 로컬 HEAD가 전달 commit SHA와 일치하는지 확인
→ 엔진 프로젝트 다시 열기
→ Project Play
→ 기대 첫 화면
→ 실제 대표 플레이의 성공·실패·복귀
```

### Fetch와 Pull

- `Fetch origin`은 원격 변경 존재 여부와 원격 참조를 갱신한다.
- `Pull origin` 또는 동등한 안전한 fast-forward가 실제 로컬 파일을 갱신한다.
- Fetch만 수행한 상태를 적용 완료로 보고하지 않는다.
- DIRTY·DIVERGED 상태에서는 사용자 변경을 덮어쓰는 hard reset·force push를 기본 해결책으로 사용하지 않는다.

## 기본 실행 계약

최종 인계 대상은 다음을 모두 만족해야 한다.

1. 프로젝트 파일을 열고 **Project Play**를 누르면 대표 Demo의 기대 첫 화면이 뜬다.
2. 별도 Scene 선택이나 Scene 전용 실행을 요구하지 않는다.
3. 편집기에서 main Scene, 입력 모드, 플러그인, feature flag를 수동 설정하게 하지 않는다.
4. 타이틀·브리핑·튜토리얼 등 시작 흐름에서 실제 gameplay surface로 이동할 수 있다.
5. 핵심 HUD·도구·입력 표면이 표시되고 사용 가능하다.
6. 대표 Golden Path와 실패 Path가 모두 결과까지 도달한다.
7. 같은 실행 안에서 재시도·수정·타이틀 또는 허용된 복귀 흐름을 사용할 수 있다.
8. 플랫폼·validation 전용 진입점이 기본 사용자 경로를 훼손하지 않는다.

## 구현자의 실제 진입점 통합 경계

사용자가 **Project Play로 직접 실검증**하는 것이 승인된 목표라면, 구현자는 기능 파일만 만든 뒤 “기존 진입점은 범위 밖”이라는 이유로 멈추지 않는다. 실제 Project Play에서 대표 흐름에 도달하기 위한 **필요한 최소 통합 변경**은 같은 승인 범위의 integration edge로 취급한다.

- Task의 주 구현 폴더가 `scenes/vertical_slice/`, `scripts/vertical_slice/ui/`처럼 제한되어 있어도, 그 제한은 주 구현 파일의 소유 범위를 뜻한다. 사용자 실검증에 꼭 필요한 entrypoint·router·project setting 연결까지 자동 금지한다는 뜻으로 해석하지 않는다.
- Godot에서는 필요할 경우 `project.godot`의 `application/run/main_scene`, `MainMenu` → App Router → 대상 기능 연결, 그리고 실제 진입에 필수적인 최소 Autoload·InputMap·Resource 연결을 함께 변경할 수 있다.
- 이런 Project Settings·Main Scene·Autoload·InputMap 변경은 기존 Godot 구조 변경 안전 Gate, Git 복구 지점, diff 검토, import/parse, 관련 테스트와 rollback 요구를 그대로 따른다.
- 실검증과 관계없는 Project Settings 정리, 다른 Scene의 임의 교체, 대규모 migration 또는 unrelated refactor는 이 integration edge에 포함하지 않는다.

### A/B 기본 판정

동일 기능에 다음 선택지가 모두 기술적으로 가능하면 사용자 실검증 목표에서는 B를 기본으로 한다.

- **A — 격리 검증:** 새 Scene·MainMenu·Router를 만들지만 기존 프로젝트 기본 진입점은 유지한다.
- **B — 실제 진입점 통합:** 새 Scene·MainMenu·Router를 만들고 기본 Project Play의 실제 진입점까지 연결한다.

A는 다음 경우에만 기본 선택할 수 있다.

- 사용자가 기존 Main Scene을 유지하라고 명시했다.
- 작업이 의도적으로 독립 `Prototype/Test Scene` 또는 validation fixture다.
- 진입점 변경 자체가 승인되지 않은 새로운 제품·기획 결정을 필요로 한다.
- 안전한 rollback이 없거나 변경이 현재 승인 범위를 넘어 고위험 구조 변경으로 확대된다.

사용자 실검증이 승인 목표인데 단순히 변경 파일 수를 줄이거나 Task 폴더 경계를 좁게 해석하기 위해 A에서 종료하지 않는다. 반대로 B도 무제한 범위 확대 허가는 아니다.

## 자동 검증 계약

적용 가능한 엔진 테스트는 최소한 다음을 증명한다.

- 기본 entrypoint가 존재하고 로드된다.
- 기본 Project Play root가 대표 Demo root를 생성한다.
- 기대 첫 화면 상태가 맞다.
- 실제 gameplay surface로 전환된다.
- 핵심 HUD·도구·입력 영역이 visible·enabled 상태다.
- 대표 성공·실패·재시도·수정·복귀 경로가 회귀 테스트로 연결된다.
- 기존 validation harness와 플랫폼 override가 유지된다.

패키징·export·해시·headless PASS는 실제 화면·음향·물리 입력·완주 PASS를 대신하지 않는다.

Godot에서 사용자 실검증이 계약된 경우 Scene 전용 실행만으로 완료하지 않고 기본 **Project Play (`F5 / Run Project`)**에서 의도한 Main Scene과 대표 사용자 흐름을 확인한다.

## 수동 검수 상태

```text
NOT_RUN
→ 자동·패키징 증거는 있으나 사용자가 실제 기본 실행을 하지 않음

PASS
→ 전달 commit을 받은 실제 환경에서 Project Play로 시작해 대표 흐름을 완주함

FAIL · RETEST_REQUIRED
→ 화면·HUD·입력·흐름·오디오·복귀 중 하나라도 기대와 다름

BLOCKED
→ 엔진·권한·환경·동기화 문제로 실행 자체가 불가능함
```

사용자가 실행했으나 화면이 비거나 조작할 수 없으면 `FAIL · RETEST_REQUIRED`다. 이전 자동 PASS나 export PASS를 근거로 Ready·완료·Production PASS를 유지하지 않는다.

## Handoff 필수 필드

```yaml
repository:
branch:
commit_sha:
working_tree_expectation: CLEAN | USER_CHANGES_PRESERVED
update_steps:
  - Fetch origin
  - Pull origin
  - local HEAD verification
project_file:
default_play_action: Project Play
expected_first_screen:
representative_play_flow:
controls:
automated_tests:
manual_tests:
known_failures_and_not_run:
rollback:
```

## 완료 실패 조건

다음 중 하나라도 해당하면 인계 완료가 아니다.

- 사용자가 별도 Scene을 찾아 실행해야 함
- main Scene 또는 Project Settings를 수동으로 지정해야 함
- 사용자 실검증이 승인됐는데 실제 Project Play 진입점 연결 없이 격리 Scene만 구현함
- Fetch만 안내하고 Pull·로컬 HEAD 확인을 생략함
- 기본 실행 후 gameplay HUD·도구·입력이 나타나지 않음
- 시작 화면만 있고 실제 플레이 성공·실패·복귀가 연결되지 않음
- 패키징 성공을 실제 실행 성공으로 보고함
- 사용자의 실패 증거가 있는데 상태를 PASS로 유지함
- 전달 Branch·commit SHA가 불명확함

## 롤백

기본 실행 전환이 기존 validation harness, 플랫폼 export 또는 저장 호환성을 훼손하면 제품 bootstrap 변경을 되돌리고 해당 전용 entrypoint를 복구한다. 사용자 로컬 변경은 보존하며 force push·hard reset으로 문제를 숨기지 않는다.
