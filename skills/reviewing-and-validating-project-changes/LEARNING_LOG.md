# Reviewing and Validating Project Changes — Learning Log

## 2026-08-14 — Completion claims need executable binding, not contract presence alone

- **Status:** `PATTERN_CANDIDATE`
- **Trigger:** BCP-2026-027의 material claim·Intent·Evidence ceiling 계약은 존재했지만, 작업자의 완료 문장을 actual diff와 현재 Git 상태에서 실행한 검증 결과에 기계적으로 묶는 소비자가 부족했다.
- **Finding 1:** Skill 본문, Schema, Template, 테스트 파일이 존재한다는 사실은 해당 기능이 실제 검수 경로에서 실행됐다는 증거가 아니다. 구현 실재성은 exact base/HEAD, clean worktree, actual changed paths, Acceptance별 implementation path와 fresh command result를 함께 요구해야 한다.
- **Finding 2:** 종료 코드 0만으로 성공을 판정하면 no-op 또는 잘못된 명령도 통과할 수 있다. 검수 명령은 사전 승인된 argv, timeout, exit code와 기대 output marker를 함께 검사해야 한다.
- **Finding 3:** producer가 record에 기입한 PASS·SHA·Evidence level은 verifier 입력일 뿐 독립 Evidence가 아니다. 신뢰 base는 reviewer/CI가 전달하고, 기본 Evidence ceiling은 `TEST`로 제한하며 `RUNTIME`·`RENDER`는 check ID별 명시 승인을 요구해야 한다. `HUMAN` Evidence는 자동 생성하지 않는다.
- **Finding 4:** pre-merge 검증이 구현·검증·Intent를 통과해도 integration은 merged state, merge SHA, 새 main readback과 post-merge checks 전까지 `BLOCKED_UNVERIFIED`다.
- **Decision:** 기존 `reviewing-and-validating-project-changes`의 `claim-and-intent-verification` Mode에 `tools/check_review_evidence.py`, 입력·결과 Schema, task record Template, 반례 회귀를 흡수한다. 새 ACTIVE Skill이나 중복 BCP owner를 만들지 않는다.
- **Fail-closed boundary:** no execution, stale/no-op base, dirty worktree, 범위 밖·보호 경로 변경, unchanged implementation path, unapproved program, timeout·실패·marker 누락, Evidence inflation은 `FAIL`, `NOT_RUN`, `CLAIM_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`를 유지한다.
- **Evidence:** PR #330의 최초 Game Project OS 실패는 packaged script가 owner Skill에 연결되지 않은 사실을 검출했다. 이후 canonical top-level tool, Skill 연결, implementation evidence index와 adversarial tests를 추가했고 Base v9 및 Skill Behavior Evidence가 exact head에서 통과했다. 최종 Game Project OS와 post-merge main readback은 별도 완료 조건으로 유지한다.
- **Next trigger:** 실제 프로젝트의 Godot runtime/render check를 record에 연결할 때, 비-Python 실행 프로그램 allowlist를 늘릴 때, required CI 또는 provenance 서명을 도입할 때 재검토한다.

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
