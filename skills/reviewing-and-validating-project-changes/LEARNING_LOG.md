# Reviewing and Validating Project Changes — Learning Log

## 2026-08-07 — Remote ownership must be detected before local fallback

- **Status:** `PATTERN_CANDIDATE`
- **Trigger:** 공개 저장소에서 비용을 이유로 CI를 우회하지 않으면서, GitHub Actions 인프라가 실제로 불가할 때만 로컬 검증으로 Required Check를 대체하는 두 모드 구조를 설계·구현했다.
- **Finding 1:** 공개 저장소의 standard GitHub-hosted runner는 정상 `REMOTE_CI` 경로이므로 paid-minute 예산 0은 fallback 조건이 아니다.
- **Finding 2:** PR workflow run이 이미 생성되어 `pending` 상태여도 마지막 `ci-gate` Job의 Check Run은 아직 존재하지 않을 수 있다. 따라서 “`ci-gate` Check Run이 없다”만으로 Actions 장애를 판정하면 정상 원격 실행과 local status가 경쟁할 수 있다.
- **Finding 3:** `run_local_validation.py`가 강한 정적·회귀 검증을 제공해도 Windows/Godot/publication 같은 모든 CI 증거를 항상 재현하는 것은 아니다. 따라서 로컬에서 동등하게 재현 가능한 변경만 fallback 성공 대상으로 허용해야 한다.
- **Decision:** `REMOTE_CI`와 `LOCAL_FALLBACK` 두 실행 모드만 유지한다. local fallback은 canonical REMOTE_CI workflow run 자체와 `ci-gate` Check Run·기존 `ci-gate` commit status가 모두 없고, exact head·clean worktree·현재 `origin/<base>`·locally reproducible change boundary가 검증 전후 유지될 때만 기존 local validator를 실행해 exact head에 success status를 발행한다.
- **Fail-closed boundary:** 테스트·workflow 실패, queued/in-progress remote run, code/engine/CI change처럼 비로컬 증거가 필요한 변경, stale base, SHA drift, dirty tree, GitHub API 실패, 기존 gate status/check는 fallback으로 덮지 않는다. 동등한 증거를 만들 수 없으면 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`다.
- **Evidence:** Draft PR #208의 TDD RED에서 production fallback tool 부재를 먼저 실패로 확인했다. 후속 실제 Actions 관찰에서는 canonical workflow run이 `pending`이며 job이 아직 0개인 구간이 존재해 Check Run-only 판정의 race를 재현했다. Reference-freshness 검사는 Skill 변경에 learning log와 기존 통합 회귀 동기화를 요구해 누락된 소비자를 추가로 찾았다.
- **Next trigger:** 두 개 이상의 프로젝트에서 실제 GitHub Actions 인프라 장애가 발생해 LOCAL_FALLBACK을 사용했을 때, 프로젝트별 Godot/Windows 등가 로컬 검증 계약을 추가할 때, GitHub가 required checks/status semantics 또는 public runner billing을 변경할 때 재검토한다.
