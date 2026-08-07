# GitHub Pro 저장소 운영 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 branch protection, branch/tag ruleset, auto-merge, Actions 사용량과 저장소 확산 순서를 관리하는 공용 정본이다.

## 1. 적용 원칙

- 현재 Base와 활성 게임 저장소는 public 저장소로 운영하며, standard GitHub-hosted Actions는 `REMOTE_CI` 기본 경로로 사용한다.
- 비용 0은 공개 저장소의 standard GitHub-hosted runner를 우회하는 이유가 아니다.
- 미래에 private 저장소를 만들거나 larger/GPU runner를 사용할 경우 현재 GitHub billing 조건을 별도로 검토한다.
- 비공개 Push ruleset은 GitHub Team 이상 기능이므로 Pro 공용 Template에 포함하지 않는다.
- 저장소 설정은 Base에서 정책과 importable Template을 제공하고 각 프로젝트에서 실제 visibility, Required Check 이름과 기본 Branch를 확인한 뒤 적용한다.
- 모든 프로젝트를 동시에 잠그지 않는다. Base에서 검증한 뒤 활성 프로젝트에 하나씩 순차 확산한다.

Official references:

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/committing-changes-to-your-project/about-status-checks

## 1.1 Repository health baseline

Base의 공개 저장소 표면은 다음 네 파일이 책임진다.

| 표면 | 정본 | 계약 |
|---|---|---|
| 재사용 권한 | `LICENSE` | Base 자체의 MIT 조건; 제3자 고지는 별도 유지 |
| 취약점 신고 | `SECURITY.md` | `main` 지원, 민감 정보 공개 금지, private reporting 우선 |
| 변경 소유 | `.github/CODEOWNERS` | 실제 write owner와 `.github/` 자체 소유 |
| 의존성 갱신 | `.github/dependabot.yml` | 지원되는 실제 manifest 기반 주간 제안; 자동 병합 권한 없음 |

파일 존재와 Repository setting은 다른 증거다. 실제 설정이나 첫 GitHub 실행을 확인하기 전에는 `UNVERIFIED_REPOSITORY_SETTING` 또는 `NOT_RUN`으로 기록한다.

Base의 현재 의존성 생태계와 package-manager 지원 범위는 실제 manifest와 GitHub 지원 문서를 기준으로 확인한다. Dependabot PR도 일반 Required Check와 병합 금지 조건을 우회하지 않는다.

## 2. Repository Governance Profile

각 저장소는 `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`를 사용해 다음을 선언한다. Base 자체의 현행 값은 `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`가 책임진다.

```yaml
repository:
owner:
visibility: public | private
plan_capability: FREE_PUBLIC | PRO_PRIVATE
primary_branch:
required_check: ci-gate
merge_method: squash
auto_merge: enabled | disabled | unverified
ruleset: active | disabled | unverified
rollout_stage: BASE | PILOT | ACTIVE | DEFERRED
```

확인하지 못한 설정은 `unverified`로 둔다.

Repository Governance Profile은 rename·transfer·visibility·기본 Branch·Required Check 같은 현재 상태를 갱신하는 가변 정본이다. 반대로 `base*.lock.json`은 발행 당시의 동결된 역사적 identity이므로 현재 설정을 유도하는 입력으로 사용하지 않는다.

Base의 Required Check `ci-gate` 소유자는 `.github/workflows/validate-game-project-operating-system.yml` 하나다. 다른 Workflow는 고유한 Job 이름을 사용하며, Repository Ruleset에서 선택된 `ci-gate`가 이 소유자의 check run인지 실제 PR로 확인한다.

## 3. Solo Main Safety Ruleset

기본 Template:

`templates/project-operations/github/rulesets/solo-main-safety.json`

대상은 `~DEFAULT_BRANCH`이며 다음을 요구한다.

- PR을 통해서만 기본 Branch 변경
- 승인 리뷰 수 `0`
- review thread 해결
- squash merge만 허용
- `ci-gate` 성공
- 최신 기본 Branch 기준 검사
- linear history
- force push 차단
- 기본 Branch 삭제 차단

### 승인 리뷰 수가 0인 이유

1인 개발자는 자신의 PR을 승인할 수 없으므로 승인 1개를 강제하면 정상적인 자동 병합이 차단될 수 있다. 코드 품질 게이트는 Required Check, unresolved conversation, GPT 검수와 상태 계약으로 유지한다.

## 4. 자동 병합 정책

기본 모드:

```text
AUTO_MERGE_AFTER_REQUIRED_CHECKS
```

자동 병합은 다음을 모두 만족할 때 허용한다.

- PR이 Draft가 아님
- 검수 기준 HEAD SHA와 현재 HEAD SHA가 일치
- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- 저장소가 선언한 Required Check 성공
- unresolved review thread 없음
- `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `REVISE`, `BLOCKED`, `UNVERIFIED` 없음
- 저장소의 허용된 병합 방식 확인
- active Ruleset 또는 동등한 branch protection 존재

상태:

- `AUTO_MERGE_ELIGIBLE`: 조건 충족, auto-merge를 활성화할 수 있음
- `AUTO_MERGE_ENABLED`: GitHub에 auto-merge 예약됨
- `AUTO_MERGE_BLOCKED`: 기획 결정·검증·Repository 설정으로 차단됨
- `UNVERIFIED_REPOSITORY_SETTING`: Repository 설정을 실제 확인하지 못함

`AGENT_MERGE_REQUIRED`에 따라 조건을 충족한 PR은 담당 에이전트가 정책에 따라 병합할 수 있다. 다만 현재 작업처럼 사용자가 Draft 유지 또는 별도 병합 승인을 요구한 경우 그 작업 계약을 우선한다. `USER_REVIEW_REQUIRED`와 `CHANGE_PROPOSAL`은 구현 전 사용자 결정을 요구한다.

## 5. Auto-merge Repository 설정

Repository에서 다음 설정이 필요하다.

```text
Settings
→ General
→ Pull Requests
→ Allow auto-merge
```

Auto-merge는 PR이 즉시 병합 가능한 상태에서는 UI에 표시되지 않을 수 있다. Required Check 또는 다른 병합 요구조건을 기다리는 PR에서 활성화한다.

## 6. Actions 사용량과 두 검증 모드

### `REMOTE_CI`

- Base와 현재 활성 프로젝트처럼 public 저장소인 경우 standard GitHub-hosted runner를 기본 경로로 사용한다.
- 공개 저장소의 비용 최적화는 paid minutes 회피보다 피드백 속도, runner 낭비, 외부 의존성 실패, 중복 matrix 감소를 목적으로 유지한다.
- larger/GPU runner 및 미래 private repository는 현재 GitHub billing 조건을 확인한 뒤 별도 예산을 적용한다.
- 현재 head에 canonical `REMOTE_CI workflow run`이 하나라도 존재하면 final `ci-gate` Check Run이 아직 생성되지 않았더라도 `REMOTE_CI`가 해당 SHA를 소유한다.
- `ci-gate` Check Run 또는 기존 `ci-gate` commit status가 있으면 local fallback으로 덮지 않는다.

### `LOCAL_FALLBACK`

`LOCAL_FALLBACK`은 Actions 인프라·권한·서비스 문제로 canonical `REMOTE_CI workflow run` 자체가 현재 head에 없고, head/test-merge의 `ci-gate` Check Run과 기존 status도 없을 때만 검토한다.

`tools/run_local_ci_fallback.py`는 다음을 모두 확인해야 한다.

- exact PR/local head
- clean worktree
- freshly fetched current `origin/<base>` ancestry와 exact trusted-history SHA
- locally reproducible 변경 경계
- 검증 전후 canonical remote run / `ci-gate` Check Run / 기존 status 부재
- 기존 `tools/run_local_validation.py` 성공
- 검증 후 SHA·base·worktree 불변
- exact head에만 `ci-gate=success` status 발행

현재 Base 공용 계약에서는 문서와 제한적 정본/템플릿만 locally reproducible 기본 범위로 취급한다. `CODE_OR_ENGINE`, `CI_TOOLCHAIN_HIGH_RISK`, workflow·tool·test·Godot·package/lockfile 변경은 별도 동등 로컬 검증 계약이 없으면 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`다.

`ci-gate` Check Run이 실패·취소·대기·실행 중이거나 canonical remote run이 존재하는 상태는 fallback 사유가 아니다. 원격 CI 실패를 수정하거나 실행을 재개한다.

세부 계약은 `docs/CI_EXECUTION_COST_POLICY.md`가 책임진다.

## 7. Packages와 Codespaces

### Packages

공용 CI container는 반복 설치 시간이 측정상 병목일 때만 도입한다.

후보:

- publication dependencies
- Godot headless validation
- Python contract validation

도입 전 image 크기, 저장소 사용량, 전송량, update 책임을 기록한다.

### Codespaces

선택 적용 대상:

- Base Skill·문서·Schema·Python 도구 작업
- CI 실패 재현
- HTML 기획 도구

Godot GUI 플레이테스트·아트·오디오 주 작업 환경으로 강제하지 않는다.

## 8. 단계적 적용

### Stage 1 — Base

- 정책·Template·회귀 테스트 병합
- `ci-gate` Required Check 기준 고정
- `REMOTE_CI` 정상 경로 검증
- 제한적 `LOCAL_FALLBACK`의 fail-closed 계약 검증
- `Allow auto-merge` 설정 확인
- 정책 PR에서 실제 Required Check 검증

### Stage 2 — Public project pilot

- `omenward` 같은 활성 public 프로젝트의 Repository Profile 작성 또는 현행 확인
- Ruleset 가져오기
- 실제 Required Check 확인
- standard GitHub-hosted `REMOTE_CI` 확인
- 필요한 경우에만 프로젝트별 locally reproducible fallback 범위 검증
- 차단·롤백 기록

### Stage 3 — 순차 확산

Pilot 성공 후 다음 활성 프로젝트에 하나씩 적용한다.

- Blacksmith
- urban-legend
- Ten-Paces-Hidden-Moves
- 그 외 활성 Godot 프로젝트

각 저장소의 현재 visibility와 Required Check를 실제 확인한 뒤 적용하며, Base의 과거 상태를 그대로 복사하지 않는다.

## 9. 자동 병합 금지

- 필수 검사 실패·취소·미실행
- Draft PR
- 검수 후 HEAD 변경
- unresolved conversation
- 사용자 체감 판단 필요
- 프로젝트 코어·MVP·플레이 규칙 변경
- 저장 호환성 파괴
- Repository setting 미확인
- Required Check 이름 미확인
- canonical `REMOTE_CI workflow run`이 존재하는데 local fallback을 시도함
- `LOCAL_FALLBACK` preflight, locally reproducible 경계 또는 exact-SHA 재검증 실패

## 10. 롤백

Ruleset 오작동 시:

1. Ruleset을 `disabled`로 변경한다.
2. auto-merge를 비활성화한다.
3. PR을 Draft로 전환한다.
4. Required Check 이름과 Workflow Job 이름을 대조한다.
5. 직접 Push로 우회하지 않고 설정을 수정한다.
6. 원인과 재개 조건을 Issue에 기록한다.

Fallback 도구 오작동 시에는 Ruleset을 변경하지 않는다. `tools/run_local_ci_fallback.py` 사용을 중단하고 `REMOTE_CI` 또는 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED` 상태로 복귀한다.

## 11. 완료 조건

- Repository Profile이 현재 설정을 반영한다.
- `solo-main-safety` Ruleset이 active다.
- `ci-gate`가 Required Check다.
- public standard GitHub-hosted `REMOTE_CI`가 기본이다.
- `LOCAL_FALLBACK`은 canonical remote run·기존 gate evidence가 없고 locally reproducible exact-SHA 안전조건을 모두 만족할 때만 사용할 수 있다.
- `Allow auto-merge` 상태가 확인됐다.
- 자동 병합 허용·차단 상태가 PR에 기록된다.
- 실제 Required Check PR 증거가 있다.
