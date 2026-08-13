# Reviewing and Validating Project Changes — Learning Log

## 2026-08-13 — Claim and intent verification must use exact evidence and progressive disclosure

- **Status:** `PATTERN_CANDIDATE`
- **Proposal:** `BCP-2026-027-claim-and-intent-verification-gate`
- **Trigger:** 사용자는 작업 중 할루시네이션을 줄이고, 승인한 의도대로 실제 구현·검증·병합됐는지 확인하는 공용 절차를 요구했다.
- **Observed regression:** PR #313 감사 문서에서 `README.md`가 활성 Skill 수를 하드코딩한다는 검색 결과 기반 가설이 exact-SHA readback 없이 verified finding으로 과승격됐다. PR #316은 baseline·merged main·관련 PR의 exact-SHA readback으로 이를 `INVALIDATED_FINDING`으로 교정했다.
- **Finding 1:** `검색 결과`, snippet, Builder·Agent·모델 설명은 확인 대상의 lead이며 저장소 사실·실행·완료의 단독 Evidence가 아니다.
- **Finding 2:** 기존 `reviewing-and-validating-project-changes`는 이미 `external-ai-result`, `contract-check`, `evidence-report`, 실제 diff 우선, BCP-008 traceability와 fail-closed 상태를 소유한다. 같은 책임의 31번째 Skill 또는 중복 Registry trigger를 추가하면 컨텍스트 비용과 오라우팅이 늘어난다.
- **Finding 3:** 25KB Skill 본문에 전체 절차를 다시 삽입하는 것보다 기존 Skill이 이미 소비하는 `PROJECT_CHANGE_VALIDATION.md`에서 전용 reference로 progressive disclosure하는 편이 책임·발견성·본문 크기를 함께 보존한다.
- **Finding 4:** 새 test 파일을 추가했지만 explicit CI test list가 실행하지 않아 첫 run이 거짓 GREEN이었다. canonical docs·contract suites가 이미 실행하는 aggregator에 전용 test case를 연결한 뒤 exact RED head에서 새 계약 6개만 실패했다.
- **Decision:** 새 ACTIVE Skill과 네 번째 Work Mode를 만들지 않는다. 기존 REVIEW owner와 기존 Registry trigger를 재사용하고, `claim-and-intent-verification.md`, validation template, `SBE-038`, executable regression으로 `MATERIAL_CLAIM_LEDGER`, `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`, `COMPLETION_CLAIM_GATE`를 흡수한다.
- **Fail-closed boundary:** authority·freshness·counterevidence가 없으면 `CLAIM_UNVERIFIED`, Acceptance·diff·필요 Evidence가 연결되지 않으면 `IMPLEMENTATION_UNVERIFIED`, merge SHA·post-merge main readback이 없으면 integration `BLOCKED_UNVERIFIED`를 유지한다. 정적 PASS는 runtime·UX·재미·시장성 PASS가 아니다.
- **TDD evidence:** initial test commit `9a4a6e688e993114466e3f25831555b23fcf5912`; canonical aggregation RED head `8a161eca8d129584aecb3898e8d5622dcfc89efb`; Game Project OS run `31656590653`; docs-validation job `94312314139`; 113 tests 중 기존 계약 통과 후 새 Gate 계약 6개가 예상대로 실패했다.
- **Next trigger:** 실제 프로젝트에서 완료·병합 오판이 반복되거나, 기존 semantic trigger가 사용자 표현을 route하지 못하는 model-run evidence가 두 건 이상 축적되면 Registry trigger 확장을 별도 최소 변경으로 재검토한다.

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
