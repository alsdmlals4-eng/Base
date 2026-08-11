# BCP-2026-021-ci-source-fidelity-for-vendored-dependencies — Vendored dependency CI source-fidelity gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/ninja-survival-godot`
- 기준 커밋: `b6c4b8a082a120f65e833b133684b899f00e05ba`
- 관련 프로젝트 PR: `https://github.com/alsdmlals4-eng/ninja-survival-godot/pull/18`
- 선행 관찰 PR: `https://github.com/alsdmlals4-eng/ninja-survival-godot/pull/17`
- 제출일: `2026-08-12`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- Learning ID: `LRN-NS-2026-08-12-001`
- Project Application: `APPLIED` — `.github/workflows/gut.yml` source-shape-aware dependency preparation + duplicate-UID import gate
- Project Verification: PR #18 exact validation revision completed all workflow steps and 250/250 GUT tests; the absent/not-vendored bootstrap route is directly verified. The vendored route remains an explicit validation requirement for T00 PR #17 before that provider package can merge.

## 관찰과 증거

`ninja-survival-godot`의 기존 CI는 GUT이 저장소에 없다는 전제에서 매 실행마다 GUT 9.7.1을 내려받아 다음처럼 복사했다.

```text
cp -R Gut-9.7.1/addons/gut addons/gut
```

T00 provider-adoption PR #17은 `addons/gut/**`를 저장소가 소유하는 vendored dependency로 추가했다. 같은 workflow를 Linux에서 실행하자 다운로드한 `gut` 디렉터리가 기존 `addons/gut` 아래로 다시 들어가 `addons/gut/gut/**`가 생성되었다. Godot import는 `res://addons/gut/gut/...`와 `res://addons/gut/...` 사이의 다수 `UID duplicate detected` 경고를 보고했지만 smoke/GUT 단계는 계속 통과했고 workflow conclusion은 success였다.

즉 CI의 준비 단계가 검증 대상 checkout의 source shape를 바꿔 버려, **green check가 실제 의도한 repository state를 검증했다는 보장이 사라졌다.** 이 사례에서 문제는 GUT 자체의 실패가 아니라, 이미 source-owned인 dependency 경로에 CI가 별도 bootstrap copy를 overlay한 것이다.

프로젝트 PR #18은 다음 project-side closure를 병합했다.

1. `addons/gut/plugin.cfg`가 있으면 vendored GUT 9.7.1을 검증·재사용한다.
2. vendored route에서 `addons/gut/gut` 중첩 트리를 거부한다.
3. GUT이 없을 때만 pinned GUT 9.7.1을 CI용으로 bootstrap한다.
4. partial pre-existing `addons/gut` 경로에는 bootstrap copy를 overlay하지 않는다.
5. Godot import output을 보존하고 `UID duplicate detected`가 있으면 실패한다.

PR #18의 exact validation revision에서 Godot 4.7.1 설치, GUT 준비, project import, main-scene smoke, full GUT regression이 모두 성공했고 250/250 테스트가 통과했다. 이 exact run은 기존 main처럼 GUT이 아직 vendored되지 않은 route의 호환성을 직접 증명한다. T00의 vendored route는 PR #17이 최신 main을 기준으로 다시 검증될 때 별도로 닫아야 하며, 이 제안은 그 미검증을 숨기지 않는다.

### Root Cause

CI dependency preparation이 `dependency absent`와 `dependency already owned by checkout`을 구분하지 않았고, 설치 destination이 이미 존재할 때 copy semantics가 source tree를 중첩시키는 상황을 fail-closed하지 않았다. 또한 engine import가 source identity duplication을 진단했지만 그 진단이 required validation failure로 승격되지 않았다.

### Existing Base Coverage

현재 Base의 `managing-game-project-operating-system`은 GUT을 project-specific third-party deterministic test authority로 취급하고 exact version, consumption path, compatibility, validation, rollback을 요구한다. provider adoption/verify 책임도 기존 owner에 있다. 따라서 새 broad Skill은 필요하지 않다.

현재 Base의 일반 PR/validation·adversarial 계약은 exact validation identity와 stale/false evidence를 공격하지만, **source-owned dependency가 생긴 뒤에도 CI bootstrap이 같은 destination을 덮어 validated tree를 변형하는 구체적 failure mode**는 공용 proposal로 명시되어 있지 않았다.

### Existing Solution Verdict

`ABSORB`

향후 구현 승인이 별도로 주어진다면 새 Skill을 만들기보다 기존 project-operating/validation owner의 provider/dependency verification mode와 관련 workflow/template/test reference에 최소 흡수하는 것이 적절하다.

## 일반화 후보

### Proposed General Principle

CI에서 dependency/tool 준비 단계는 checkout의 source ownership을 먼저 식별해야 한다.

```text
checkout
→ dependency destination ownership check
→ source-owned/vendored이면 exact identity를 verify하고 reuse
→ absent이고 CI bootstrap이 계약상 허용될 때만 isolated/pinned bootstrap
→ partial/ambiguous pre-existence면 fail closed
→ preparation 뒤 source-shape invariant 검사
→ parser/import/compiler diagnostics 중 duplicate identity 신호를 validation failure로 승격
→ product/regression tests
```

핵심 원리는 다음과 같다.

- **Repository-owned dependency wins over bootstrap:** checkout이 dependency 경로를 이미 소유하면 CI는 같은 경로에 별도 다운로드 copy를 overlay하지 않는다.
- **Bootstrap is conditional, not unconditional:** dependency가 없고 CI bootstrap이 정식 계약일 때만 exact pin으로 준비한다.
- **Ambiguous pre-existence fails closed:** expected manifest가 없지만 destination이 존재하는 partial/mixed state를 자동 덮어쓰지 않는다.
- **Source-shape invariant is a validation input:** 준비 단계가 intended source topology를 바꾸지 않았는지 검사한다.
- **Identity-collision diagnostics are not cosmetic:** parser/import/compiler가 duplicate resource/module/package identity를 보고하면 그 중복이 source fidelity를 깨는 경우 required check를 실패시킨다.
- **Green is meaningful only for the intended tree:** 테스트 자체가 통과해도 준비 단계가 검증 대상을 다른 트리로 바꿨다면 merge evidence로 승격하지 않는다.

### Benchmark

공식 GitHub Actions dependency caching 문서는 hosted runner에서 dependency를 다시 다운로드할 수 있고 cache가 dependency 재사용을 위한 별도 메커니즘임을 설명한다. 이는 source checkout과 dependency cache/bootstrap 역할을 분리하는 근거다.

- `https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows`
- `https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching`

Google Engineering Practices의 Small CL 원칙은 self-contained 변경과 관련 테스트를 함께 두고, build를 깨뜨리는 중간 상태를 피하도록 권장한다.

- `https://google.github.io/eng-practices/review/developer/small-cls.html`

여기서 “vendored dependency가 있으면 같은 경로에 bootstrap copy를 overlay하지 않는다”는 문장은 위 문서의 직접 인용이 아니라, `ninja-survival-godot`의 재현 가능한 failure evidence와 source/CI 역할 분리 원칙을 결합한 일반화다.

## 프로젝트 전용으로 남길 내용

다음은 Base 공용 규칙으로 승격하지 않고 `ninja-survival-godot`에 남긴다.

- Godot Engine `4.7.1` exact target
- GUT `9.7.1` exact target
- `addons/gut/plugin.cfg`, `addons/gut/gut_cmdln.gd`, `addons/gut/gut` 구체 경로
- `UID duplicate detected`라는 Godot-specific diagnostic literal과 해당 workflow grep implementation
- T00 PR #17, HiGodot 3.1.4, Hera Agent Godot 1.0.0 provider package 관계
- T00 merge 뒤 T01 baseline을 refresh/recreate해야 하는 MVP-4 Phase-C sequencing
- Ninja 프로젝트의 현재 CI workflow 구조 및 package branch policy

## 적용 조건과 비사용 조건

### Use When

- CI가 dependency/tool을 다운로드해 checkout 내부 경로에 설치한다.
- 같은 dependency가 향후 vendored/submodule/generated-source 형태로 repository-owned가 될 수 있다.
- dependency bootstrap destination이 이미 존재할 때 copy/extract semantics가 중첩·혼합 state를 만들 수 있다.
- parser/import/compiler가 duplicate module/resource/package identity를 진단할 수 있다.
- green test 결과가 “원래 checkout을 검증했다”는 전제에 의존한다.

### Do Not Use When

- dependency가 checkout 밖의 isolated tool cache/environment에만 설치되고 source topology와 충돌하지 않는다.
- package manager의 lockfile-driven install이 project contract이며 install directory가 명시적으로 generated/ephemeral이고 repository-owned source와 혼동되지 않는다.
- duplicate diagnostic가 의도된 namespacing/fixture duplication이고 source-fidelity 문제와 무관하다는 별도 검증이 있다.
- 프로젝트가 dependency를 vendoring하지 않고 CI-only bootstrap만 정식 권위로 유지한다. 이 경우에도 pin/identity 검증은 필요하지만 vendored-reuse branch 자체는 필요 없다.

## 반례와 위험

### Counterexamples

1. Node/Python 패키지를 clean virtual environment/cache에 lockfile로 설치하는 workflow: checkout source와 동일 경로를 overlay하지 않으므로 이 제안의 source-tree guard를 그대로 복제할 필요가 없다.
2. 테스트 fixture가 의도적으로 같은 logical ID의 malformed/duplicate 파일을 포함하는 negative test: duplicate diagnostic 자체가 test input이므로 global grep failure가 오히려 테스트를 막을 수 있다.
3. generated vendor tree가 build마다 재생성되는 것이 프로젝트 정식 계약인 경우: repository-owned manifest와 generated destination의 owner가 분리되어 있다면 `reuse vendored`보다 clean regeneration verification이 맞다.

### Risks

- generic warning text를 무조건 fail 처리하면 정상적인 intentional duplicate fixture까지 차단할 수 있다.
- manifest 존재만 보고 vendored dependency를 신뢰하면 stale/wrong version을 놓칠 수 있으므로 exact identity 검증이 함께 필요하다.
- CI bootstrap과 source-owned dependency를 둘 다 지원하면 workflow branch가 늘어나므로 representative route 검증이 필요하다.
- source-fidelity guard를 광범위한 “warning = error” 정책으로 확대하면 noise와 유지비가 증가한다.

## 영향 범위와 검증

### Affected Consumers — future implementation candidates only

이번 proposal-only 단계에서는 아래 활성 Base 파일을 변경하지 않는다. 향후 별도 구현 승인 시 Existing Solution First를 다시 수행한다.

- `skills/managing-game-project-operating-system/SKILL.md`의 provider/dependency verify mode
- 프로젝트 CI/bootstrap reference 또는 template가 실제 owner로 존재한다면 해당 기존 owner
- project operating-system verification regression/test
- adversarial review의 false-green/source-shape lens가 기존 owner에 흡수 가능한지 검토

새 broad Skill 생성은 현재 verdict에서 `REJECTED`; 기존 owner 흡수가 우선이다.

### Validation Plan

1. project fixture A: dependency absent → pinned bootstrap → expected test suite PASS.
2. project fixture B: exact vendored dependency present → no overlay/copy → expected test suite PASS.
3. project fixture C: destination directory present but expected manifest absent → fail closed before overwrite.
4. project fixture D: nested duplicate/source-identity collision을 의도적으로 만들면 import/parser guard가 RED.
5. exact validation revision에서 preparation 로그와 source-shape invariant를 확인한다.
6. Base 구현 시 selection/non-selection behavior를 검증해 isolated package-manager installs에 과잉 적용되지 않음을 확인한다.

### Regression Plan

- 기존 CI-only dependency bootstrap 프로젝트는 dependency absent route를 유지해야 한다.
- 이미 vendored dependency를 사용하는 프로젝트는 network bootstrap 없이 동일 suite를 실행할 수 있어야 한다.
- provider exact-pin/compatibility/rollback 요구를 약화하지 않는다.
- warning-as-error 일반화가 아니라 identity/source-fidelity 관련 신호로 범위를 제한한다.

### Rollback

향후 Base 구현이 과잉 차단을 만든다면 새 Skill을 제거하는 방식이 아니라 기존 owner에 추가된 source-ownership guard/mode/reference만 이전 계약으로 되돌리고, 프로젝트 고유 CI guard는 각 프로젝트의 검증된 local rule로 유지한다.

### Adversarial Findings

- `MUST_FIX`: 없음 — project-side source-fidelity guard와 handoff가 PR #18에서 merge/readback됨.
- `SHOULD_FIX`: vendored route 자체는 T00 PR #17의 최신-main revalidation에서 아직 직접 PASS를 받아야 한다. 이 때문에 본 제안의 지식 상태를 `검증 완료 표준`으로 과장하지 않고 `패턴`으로 유지한다.
- `REJECTED_CRITIQUE`: “green CI면 source fidelity 검사 불필요” — PR #17 로그가 반례다. 준비 단계가 source tree를 변경한 뒤에도 suite가 green일 수 있었다.
- `DEFER`: Hera/export runtime hygiene는 별도 Goal이며 이 BCP에 섞지 않는다.
- `USER_DECISION_REQUIRED`: Base 활성 구현 승인. 이번 proposal-only 실행은 구현 권한을 부여하지 않는다.

## 필요한 도구·파일·권한

- 필요 항목: source-control checkout ownership 판단, dependency manifest/version identity, CI log, engine/parser/import diagnostic, existing project-operating/validation owner
- 필요한 이유: dependency preparation 전후의 source topology와 exact identity를 비교하기 위해 필요하다.
- 설치·적용 방법: Base 활성 구현은 이번 단계에서 수행하지 않는다. 별도 승인 단계에서 Existing Solution First 후 기존 owner에 최소 흡수한다.
- 설치 후 확인 명령: 프로젝트별 canonical CI/test command 및 source-shape invariant check. Godot/GUT literal command는 공용 Base 계약으로 고정하지 않는다.
- 최소 권한: proposal-only 단계는 `[수정제안서]/**` write만 사용한다. 향후 구현은 별도 승인 필요.

## 승인과 구현

- 사용자 승인 근거: `미승인` — 본 proposal의 저장·병합 권한과 Base 활성 구현 승인은 분리한다.
- 구현 PR: `없음`
- 구현 상태: `NOT_STARTED_IN_THIS_STAGE`
- 구현 경계: `SEPARATE_FOLLOWUP_STAGE`
- 롤백: proposal-only PR은 해당 BCP + Registry entry만 revert할 수 있다. Base 활성 구현 파일은 이번 단계에서 변경하지 않는다.
