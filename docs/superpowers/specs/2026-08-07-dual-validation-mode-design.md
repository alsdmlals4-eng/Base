# Dual CI Validation Mode Design

**Status:** APPROVED FOR IMPLEMENTATION
**Date:** 2026-08-07
**Original baseline:** `main@4f98f968a377f7b6a11aafa4fc94d11bddbebedc`
**Final verification base:** `main@8a1b868346b5d1cbe50d458e975fca277e42b2a5`

## Goal

Base와 Base를 적용한 공개 프로젝트에서 검증 신뢰도를 낮추지 않으면서 다음 두 실행 모드만 운용한다.

1. `REMOTE_CI` — 기본 모드. GitHub Actions standard hosted runner의 기존 `ci-gate`를 사용한다.
2. `LOCAL_FALLBACK` — GitHub Actions가 현재 PR head의 canonical validation workflow를 아예 시작하지 못했고, 필요한 증거를 로컬에서 동등하게 재현할 수 있는 경우에만 기존 Required Check 문맥 `ci-gate`에 commit status를 발행한다.

라우터/선택기는 세 번째 모드가 아니다. 정상 상태에서는 항상 `REMOTE_CI`를 우선한다.

## Existing Solution First 판정

- `REUSE`: `.github/workflows/validate-game-project-operating-system.yml`의 단일 `ci-gate` Required Check.
- `REUSE`: `tools/run_local_validation.py`의 전체 로컬 검증 계약과 owned temporary-directory 안전장치.
- `REUSE`: `tests/test_local_validation.py`의 기존 회귀 집계 경로. 새 fallback 테스트를 이 집계기에 흡수하면 canonical workflow 수정 없이 `ubuntu-contract`가 실행한다.
- `ABSORB`: `skills/reviewing-and-validating-project-changes`의 `ci-cost-optimization` 모드에 두 실행 모드와 fallback 판정 절차를 흡수한다.
- `REFACTOR`: `docs/CI_EXECUTION_COST_POLICY.md`의 Actions-unavailable 계약을 동등한 로컬 증거를 만들 수 있는 제한적 fallback과 그렇지 못한 blocked 상태로 분리한다.
- `NO NEW BROAD SKILL`: 새 광역 Skill/Mode는 만들지 않는다.
- `BUILD_NEW (bounded tool)`: 로컬 fallback의 preflight, exact-SHA 검증, remote ownership 충돌 탐지, status 발행을 한 번에 수행하는 작은 orchestration tool만 추가한다.

## 왜 새 `base-validation-gate`를 만들지 않는가

초기 설계는 Actions Check와 local commit status를 분리하기 위해 새 `base-validation-gate` Required Check를 제안했다. 적대적 검토 결과, 이 방식은 Base 및 프로젝트의 실제 GitHub Ruleset을 별도로 마이그레이션해야 하고 설정 변경이 코드 PR과 원자적으로 묶이지 않는다.

현재 Base Ruleset은 이미 `ci-gate` 하나를 요구한다. Required Check 이름을 유지하면 외부 설정 마이그레이션 없이 두 모드를 지원할 수 있다.

GitHub는 같은 이름의 Check Run과 commit status가 동시에 존재하면 둘 다 통과해야 한다. 또한 PR workflow run이 시작됐어도 마지막 `ci-gate` Job의 Check Run은 아직 생성되지 않은 구간이 실제로 존재한다. 따라서 `LOCAL_FALLBACK`은 Check Run 부재만 보지 않고 current head의 canonical `REMOTE_CI workflow run` 자체가 없는지도 확인해야 한다.

## Mode contract

### `REMOTE_CI`

- 모든 현재 public 저장소의 기본 모드다.
- 기존 변경 분류, 조건부 publication/Windows smoke, `ci-gate` evaluator를 유지한다.
- 공개 저장소의 standard GitHub-hosted runner는 비용 회피 대상이 아니다. larger/GPU runner 같은 과금 가능 runner는 별도 승인·예산 검토 대상이다.
- current head에 canonical workflow run이 하나라도 존재하면 final `ci-gate` Check Run이 아직 없더라도 `REMOTE_CI`가 검증을 소유한다.
- workflow 또는 테스트 자체가 실패한 경우 `LOCAL_FALLBACK`으로 전환하지 않는다. 실패를 수정하고 같은 모드에서 다시 검증한다.

### `LOCAL_FALLBACK`

다음 조건을 전부 만족해야 한다.

1. 대상은 열린 PR이고 local `HEAD`가 GitHub PR의 `head.sha`와 정확히 일치한다.
2. 대상 base branch가 기대 branch(기본 `main`)와 일치한다.
3. `git fetch origin <base>` 후 최신 `origin/<base>`가 `HEAD`의 ancestor다.
4. 사용자가 전달한 trusted-history SHA가 방금 fetch한 정확한 `origin/<base>` SHA와 같다.
5. 검증 시작 전 worktree가 깨끗하다.
6. 변경 집합이 현재 fallback 계약으로 locally reproducible 하다.
7. current head의 canonical `REMOTE_CI workflow run`이 없다.
8. PR head와 current test merge SHA에 `ci-gate` Check Run이 없다.
9. PR head와 current test merge SHA에 기존 `ci-gate` commit status가 없다.
10. `tools/run_local_validation.py --trusted-history-commit <current-origin-base-sha>`가 성공한다.
11. 검증 종료 후 local HEAD·worktree·origin/base SHA·PR head가 변하지 않았다.
12. locally reproducible 변경 경계가 그대로 유지된다.
13. status 발행 직전에 canonical remote run, Check Run, 기존 commit status 부재를 다시 확인한다.
14. 위 조건이 모두 성공한 경우에만 exact PR head SHA에 commit status `context=ci-gate`, `state=success`를 발행한다.

다음은 fallback 사유로 인정하지 않는다.

- 테스트 실패
- evaluator 실패
- workflow YAML 오류
- required job 실패
- queued/in-progress/cancelled canonical workflow
- 기존 `ci-gate` Check Run 또는 commit status
- 사용자가 단순히 Actions 실행을 원하지 않음
- 비용 0 예산

## Locally reproducible 기본 경계

Base 공용 도구는 보수적으로 시작한다.

기본 허용:

- `.md`, `.txt`
- `docs/`, `skills/`, `templates/`, `schemas/`, `references/` 아래의 검증 가능한 `.json`, `.yaml`, `.yml`

기본 차단:

- `.github/workflows/**`
- `tools/**`, `tests/**`, `scripts/**`, `addons/**`
- Python/GDScript/JS/TS/shell/native binary
- Godot scene/resource/project 설정
- package/requirements/lockfile
- `CODE_OR_ENGINE`
- `CI_TOOLCHAIN_HIGH_RISK`
- 기타 명시적으로 동등 로컬 검증을 증명하지 않은 파일

프로젝트별 Godot/Windows/publication 등가 검증이 실제로 구현·테스트된 뒤에만 해당 프로젝트 계약에서 범위를 확대한다.

## Bounded tool

`tools/run_local_ci_fallback.py`

```text
python tools/run_local_ci_fallback.py \
  --repo alsdmlals4-eng/Base \
  --pr <number> \
  --trusted-history-commit <current-origin-base-sha> \
  [--base main]
```

책임:

- `gh`와 `git`으로 preflight를 수행한다.
- PR metadata, exact head/base SHA, clean worktree, locally reproducible change set을 검증한다.
- current head의 canonical workflow run과 head/test-merge의 `ci-gate` Check Run/status 충돌을 검증한다.
- 기존 `run_local_validation.py`를 실행한다.
- validation 후 race를 막기 위해 모든 SHA/clean/remote-ownership 상태를 다시 확인한다.
- 성공 시 exact head SHA에 `ci-gate=success`를 발행한다.
- 어떤 조건이라도 충족하지 않으면 status를 발행하지 않고 non-zero로 종료한다.

## Security and trust boundary

- 실제 Base Ruleset의 `ci-gate` 요구사항과 strict policy를 유지한다.
- Ruleset bypass actor를 추가하지 않는다.
- branch protection/ruleset을 자동 비활성화하거나 Required Check를 제거하지 않는다.
- 로컬 fallback status는 write 권한을 가진 인증된 GitHub 사용자만 발행할 수 있다.
- `gh auth status`/API 실패는 fail-closed 한다.
- status는 검증한 exact head SHA에만 발행한다.
- dirty worktree, stale base, SHA drift, remote workflow race, Check Run race, existing status, nonlocal evidence는 모두 fail-closed 한다.

## Repository synchronization

이번 변경은 다음 현행 소비자를 동기화한다.

- `docs/CI_EXECUTION_COST_POLICY.md`
- `docs/GITHUB_PRO_OPERATING_POLICY.md`
- `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/reviewing-and-validating-project-changes/LEARNING_LOG.md`
- `tests/test_local_validation.py`의 기존 CI 회귀 집계 경로

`.github/workflows/validate-game-project-operating-system.yml`은 이미 generic `tools/*`·`tests/*`를 코드 변경으로 분류하고 `tests/test_local_validation.py`를 `ubuntu-contract`에서 실행하므로 구조 변경하지 않는다. `templates/project-operations/github/rulesets/solo-main-safety.json`과 실제 Base Ruleset도 `ci-gate`를 그대로 유지한다.

작업 중 PR #200이 `main@8a1b868346b5d1cbe50d458e975fca277e42b2a5`에 병합되어 one-click operator handoff(`Fetch origin → Pull origin → reopen/play`)가 현행 Base 계약이 되었다. 이 변경은 해당 인계 흐름을 중복 구현하지 않고 PR 검증/병합 경로만 보강하며, 최신 main의 operator-handoff 검사와 함께 재검증한다.

## Acceptance criteria

- 실행 모드는 정확히 `REMOTE_CI`와 `LOCAL_FALLBACK` 두 개다.
- 기본 경로는 기존 Actions `ci-gate`이며 public 저장소에서 비용 0을 이유로 fallback하지 않는다.
- canonical remote workflow run, `ci-gate` Check Run 또는 기존 status가 존재하면 fallback success status를 발행하지 못한다.
- dirty/stale/SHA mismatch/base drift/test failure/API failure/nonlocal evidence에서 fail-closed 한다.
- local validation 성공 후 exact SHA에만 `ci-gate=success`를 발행한다.
- `CODE_OR_ENGINE`·`CI_TOOLCHAIN_HIGH_RISK`는 별도 동등 로컬 계약 없이는 fallback 성공 대상이 아니다.
- Ruleset 이름, Required Check 이름, canonical workflow topology, `ci-gate` job은 변경하지 않는다.
- 최신 main에 병합된 PR #200/#210의 operator-handoff 관련 계약과 충돌하지 않는다.
- 새 broad Skill/Mode/Schema는 추가하지 않는다.
- 테스트는 TDD로 먼저 실패를 관찰하고 최소 구현 후 통과시킨다.
- PR에서 실제 GitHub Actions 결과와 Required Check 상태를 확인한다.
