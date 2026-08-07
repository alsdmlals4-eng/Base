# Dual CI Validation Mode Design

**Status:** APPROVED FOR IMPLEMENTATION  
**Date:** 2026-08-07  
**Baseline:** `main@4f98f968a377f7b6a11aafa4fc94d11bddbebedc`

## Goal

Base와 Base를 적용한 공개 프로젝트에서 검증 신뢰도를 낮추지 않으면서 다음 두 실행 모드만 운용한다.

1. `REMOTE_CI` — 기본 모드. GitHub Actions 표준 hosted runner의 기존 `ci-gate`를 사용한다.
2. `LOCAL_FALLBACK` — GitHub Actions가 인프라·권한·서비스 수준에서 아예 Required Check를 만들지 못한 경우에만 로컬에서 동등한 검증을 실행하고 기존 Required Check 문맥 `ci-gate`에 commit status를 발행한다.

라우터/선택기는 세 번째 모드가 아니다. 정상 상태에서는 항상 `REMOTE_CI`를 우선하고, 엄격한 fallback 전제조건이 모두 충족될 때만 `LOCAL_FALLBACK`으로 전환한다.

## Existing Solution First 판정

- `REUSE`: `.github/workflows/validate-game-project-operating-system.yml`의 단일 `ci-gate` Required Check.
- `REUSE`: `tools/run_local_validation.py`의 전체 로컬 검증 계약과 owned temporary-directory 안전장치.
- `ABSORB`: `skills/reviewing-and-validating-project-changes`의 `ci-cost-optimization` 모드에 두 실행 모드와 fallback 판정 절차를 흡수한다.
- `REFACTOR`: `docs/CI_EXECUTION_COST_POLICY.md`의 “Actions 사용 불가 = 항상 UNVERIFIED” 계약을, 동등한 로컬 증거를 만들 수 있는 제한적 fallback과 그렇지 못한 blocked 상태로 분리한다.
- `NO NEW BROAD SKILL`: 새 광역 Skill/Mode는 만들지 않는다.
- `BUILD_NEW (bounded tool)`: 로컬 fallback의 preflight, exact-SHA 검증, `ci-gate` 충돌 탐지, status 발행을 한 번에 수행하는 작은 orchestration tool만 추가한다.

## 왜 새 `base-validation-gate`를 만들지 않는가

초기 설계는 Actions Check와 local commit status를 분리하기 위해 새 `base-validation-gate` Required Check를 제안했다. 적대적 검토 결과, 이 방식은 Base 및 모든 프로젝트의 실제 GitHub Ruleset을 별도로 마이그레이션해야 하고 설정 변경이 코드 PR과 원자적으로 묶이지 않는다.

현재 Base Ruleset은 이미 `ci-gate` 하나를 요구한다. 따라서 Required Check 이름을 유지하면 외부 설정 마이그레이션 없이 두 모드를 지원할 수 있다.

GitHub는 같은 이름의 Check Run과 commit status가 동시에 존재하면 둘 다 통과해야 한다. 그러므로 `LOCAL_FALLBACK`은 현재 PR head SHA와 현재 test merge SHA 어디에도 `ci-gate` Check Run이 존재하지 않을 때만 허용한다. Check가 생성되었거나 실패·취소·대기 상태라면 fallback으로 덮어쓰지 않고 `REMOTE_CI` 실패/보류로 남긴다.

## Mode contract

### `REMOTE_CI`

- 모든 공개 저장소의 기본 모드다.
- 기존 변경 분류, 조건부 publication/Windows smoke, `ci-gate` evaluator를 유지한다.
- 공개 저장소의 표준 GitHub-hosted runner는 비용 회피 대상이 아니다. larger/GPU runner 같은 유료 runner는 별도 승인 없이는 사용하지 않는다.
- workflow 또는 테스트 자체가 실패한 경우 `LOCAL_FALLBACK`으로 전환하지 않는다. 실패를 수정하고 같은 모드에서 다시 검증한다.

### `LOCAL_FALLBACK`

다음 조건을 전부 만족해야 한다.

1. 대상은 열린 PR이고 local `HEAD`가 GitHub PR의 `head.sha`와 정확히 일치한다.
2. 대상 base branch가 기대한 branch(기본 `main`)와 일치한다.
3. `git fetch origin <base>` 후 최신 `origin/<base>`가 `HEAD`의 ancestor여야 한다. 즉 strict required checks의 up-to-date 조건을 우회하지 않는다.
4. 검증 시작 전 worktree가 깨끗해야 한다.
5. PR head SHA의 Check Runs에 `name == "ci-gate"`가 없어야 한다.
6. PR API가 제공하는 현재 `merge_commit_sha`가 있으면 그 SHA에도 `ci-gate` Check Run이 없어야 한다.
7. `tools/run_local_validation.py --trusted-history-commit <trusted-sha>`가 성공해야 한다.
8. 검증 종료 후 `HEAD`가 바뀌지 않았고 worktree가 다시 깨끗해야 한다.
9. status 발행 직전에 head/test-merge SHA의 `ci-gate` Check Run 부재를 다시 확인한다. 검증 도중 Actions가 살아나 Check를 만들었다면 로컬 status를 발행하지 않는다.
10. 위 조건이 모두 성공한 경우에만 PR head SHA에 commit status `context=ci-gate`, `state=success`를 발행한다.

다음은 fallback 사유로 인정하지 않는다.

- 테스트 실패
- evaluator 실패
- workflow YAML 오류
- required job 실패
- 사용자가 단순히 Actions 실행을 원하지 않음
- 비용 0 예산(공개 표준 runner는 비용 회피 대상이 아님)

## New bounded tool

`tools/run_local_ci_fallback.py`

CLI:

```text
python tools/run_local_ci_fallback.py \
  --repo alsdmlals4-eng/Base \
  --pr <number> \
  --trusted-history-commit <sha> \
  [--base main]
```

책임:

- `gh`와 `git`으로 preflight를 수행한다.
- PR metadata와 exact SHA를 검증한다.
- current head/test-merge의 `ci-gate` Check Run 존재 여부를 확인한다.
- 기존 `run_local_validation.py`를 실행한다.
- validation 후 race를 막기 위해 SHA/clean/check-run 상태를 다시 확인한다.
- 성공 시 GitHub commit status API에 `ci-gate=success`를 발행한다.
- 어떤 조건이라도 충족하지 않으면 status를 발행하지 않고 non-zero로 종료한다.

도구는 GitHub Actions 실패를 성공으로 바꾸는 우회기가 아니라, Actions가 Required Check를 **생성하지 못한** 상황에서 동일한 검증 증거를 공급하는 제한된 대체 실행기다.

## Security and trust boundary

- 실제 Base Ruleset의 `ci-gate` 요구사항과 strict policy를 유지한다.
- Ruleset bypass actor를 추가하지 않는다.
- branch protection/ruleset을 자동 비활성화하거나 Required Check를 제거하지 않는다.
- 로컬 fallback status는 write 권한을 가진 인증된 GitHub 사용자만 발행할 수 있다.
- 로컬 도구는 `gh auth status`/API 실패 시 fail-closed 한다.
- status는 검증한 exact head SHA에만 발행한다.
- dirty worktree, stale base, SHA drift, check-run race는 모두 fail-closed 한다.

## Repository synchronization

이번 변경은 다음 현행 소비자를 동기화한다.

- `docs/CI_EXECUTION_COST_POLICY.md`
- `docs/GITHUB_PRO_OPERATING_POLICY.md`
- `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `.github/workflows/validate-game-project-operating-system.yml`의 새 tool/test 자기검증 목록

`templates/project-operations/github/rulesets/solo-main-safety.json`과 실제 Base Ruleset은 `ci-gate`를 그대로 유지하므로 변경하지 않는다.

열린 PR #200의 one-click handoff(`Fetch origin → Pull origin → reopen/play`)는 중복 구현하지 않는다. 이 변경은 PR 검증/병합 경로만 보강하며, #200의 사용자 인계 흐름과 충돌하지 않아야 한다.

## Acceptance criteria

- 저장소에 실행 모드는 정확히 `REMOTE_CI`와 `LOCAL_FALLBACK` 두 개만 정의된다.
- 기본 경로는 기존 Actions `ci-gate`이며 공개 저장소에서 비용 0을 이유로 fallback하지 않는다.
- 현재 SHA에 `ci-gate` Check Run이 존재하면 local fallback은 성공 status를 발행하지 못한다.
- dirty/stale/SHA-mismatch/test-failure/API-failure에서 fail-closed 한다.
- local validation 성공 후 exact SHA에만 `ci-gate=success`를 발행한다.
- Ruleset 이름과 Required Check 이름은 변경하지 않는다.
- 새 broad Skill/Mode/Schema는 추가하지 않는다.
- 테스트는 TDD로 먼저 실패를 관찰하고 최소 구현 후 통과시킨다.
- PR에서 실제 GitHub Actions 결과와 Required Check 상태를 확인한다.
