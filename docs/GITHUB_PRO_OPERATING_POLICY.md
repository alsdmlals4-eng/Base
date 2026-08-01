# GitHub Pro 저장소 운영 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 GitHub Pro의 branch protection, branch/tag ruleset, auto-merge, Actions 사용량과 저장소 확산 순서를 관리하는 공용 정본이다.

## 1. 적용 원칙

- 공개 저장소의 표준 GitHub-hosted Actions는 공개 저장소 계약에 따라 사용하고, Pro의 포함 사용량은 주로 비공개 저장소에 배분한다.
- 비공개 저장소에서는 GitHub Pro가 제공하는 protected branch와 branch/tag ruleset을 사용한다.
- 비공개 Push ruleset은 GitHub Team 이상 기능이므로 Pro 공용 Template에 포함하지 않는다.
- 저장소 설정은 Base에서 정책과 importable Template을 제공하고 각 프로젝트에서 실제 Required Check 이름과 기본 Branch를 확인한 뒤 적용한다.
- 모든 프로젝트를 동시에 잠그지 않는다. Base → 비공개 `omenward` → 다른 활성 프로젝트 순으로 확산한다.

Official references:

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository

## 1.1 Repository health baseline

Base의 공개 저장소 표면은 다음 네 파일이 책임진다.

| 표면 | 정본 | 계약 |
|---|---|---|
| 재사용 권한 | `LICENSE` | Base 자체의 MIT 조건; 제3자 고지는 별도 유지 |
| 취약점 신고 | `SECURITY.md` | `main` 지원, 민감 정보 공개 금지, private reporting 우선 |
| 변경 소유 | `.github/CODEOWNERS` | 실제 write owner와 `.github/` 자체 소유 |
| 의존성 갱신 | `.github/dependabot.yml` | 지원되는 실제 manifest 기반 주간 제안; 자동 병합 권한 없음 |

파일 존재와 Repository setting은 다른 증거다. `SECURITY.md`는 private vulnerability reporting을 활성화하지 않고, `CODEOWNERS`는 승인 필수 Ruleset을 활성화하지 않으며, `dependabot.yml`은 Dependabot alerts나 dependency graph 설정을 활성화하지 않는다. 실제 설정이나 첫 GitHub 실행을 확인하기 전에는 각각 `UNVERIFIED_REPOSITORY_SETTING` 또는 `NOT_RUN`으로 기록한다.

Base의 현재 의존성 생태계는 루트 `package.json`·`pnpm-lock.yaml`의 `npm`(pnpm), `requirements-publication.txt`의 `pip`, `.github/workflows/`의 `github-actions` 세 가지다. 그러나 저장소는 `pnpm@11.9.0`을 선언하고 현재 GitHub 공식 지원표는 pnpm v7-v10만 명시하므로, `npm` entry는 `DEPENDABOT_DEFERRED_PNPM_11`로 보류한다. package manager를 이 작업에서 임의 하향하지 않으며 공식 지원과 실제 update run을 확인한 뒤 별도 활성화한다. 활성화된 `pip`·`github-actions`의 minor/patch는 생태계별로 묶을 수 있지만 major 변경은 별도 PR·exact-head CI·리뷰를 거친다. Dependabot PR도 일반 Required Check와 병합 금지 조건을 우회하지 않는다.

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

Repository Governance Profile은 rename·transfer·visibility·기본 Branch·Required Check 같은 현재 상태를 갱신하는 가변 정본이다. 반대로 `base*.lock.json`은 발행 당시의 동결된 역사적 identity이므로 현재 CODEOWNERS나 보안 경로를 유도하는 입력으로 사용하지 않는다. 현재 profile의 identity가 바뀌면 `.github/CODEOWNERS`, 보안 경로, Workflow와 회귀 검사를 같은 변경에서 대조한다.

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

`AGENT_MERGE_REQUIRED`에 따라 조건을 충족한 PR은 담당 에이전트가 즉시 병합한다. `Allow auto-merge`가 활성화되면 예약하고, 그렇지 않으면 저장소가 허용한 직접 병합을 실행한다. 별도 사용자 병합 승인은 필요하지 않다. 다만 `USER_REVIEW_REQUIRED`와 `CHANGE_PROPOSAL`은 병합 승인이 아니라 구현 전 사용자 결정을 요구한다.

## 5. Auto-merge Repository 설정

Repository에서 다음 설정이 필요하다.

```text
Settings
→ General
→ Pull Requests
→ Allow auto-merge
```

Auto-merge는 PR이 즉시 병합 가능한 상태에서는 UI에 표시되지 않을 수 있다. Required Check 또는 다른 병합 요구조건을 기다리는 PR에서 활성화한다.

## 6. Actions 사용량

- Base처럼 공개 저장소인 경우 비용 최적화는 Pro 포함 분을 아끼기 위한 목적보다 피드백 속도·runner 낭비·외부 의존성 실패 감소를 목적으로 유지한다.
- `omenward` 같은 비공개 저장소는 Pro 포함 Actions 사용량에 직접 영향을 주므로 변경 위험별 CI 계층을 필수 적용한다.
- Budget은 `templates/project-operations/github/GITHUB_USAGE_BUDGET.md`에 기록한다.
- 사용량 한도·추가 과금·runner 장애로 필수 검증을 실행하지 못하면 `UNVERIFIED`이며 자동 병합하지 않는다.

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
- `Allow auto-merge` 설정 확인
- 정책 PR에서 실제 auto-merge 검증

### Stage 2 — `omenward` Pilot

- Repository Profile 작성
- Ruleset 가져오기
- 실제 Required Check 확인
- Auto-merge 활성화
- 한 개 PR에서 자동 병합 검증
- 차단·롤백 기록

### Stage 3 — 순차 확산

Pilot 성공 후 다음 활성 프로젝트에 하나씩 적용한다.

- Blacksmith
- urban-legend
- Ten-Paces-Hidden-Moves
- 그 외 활성 Godot 프로젝트

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

## 10. 롤백

Ruleset 오작동 시:

1. Ruleset을 `disabled`로 변경한다.
2. auto-merge를 비활성화한다.
3. PR을 Draft로 전환한다.
4. Required Check 이름과 Workflow Job 이름을 대조한다.
5. 직접 Push로 우회하지 않고 설정을 수정한다.
6. 원인과 재개 조건을 Issue에 기록한다.

## 11. 완료 조건

- Repository Profile이 현재 설정을 반영한다.
- `solo-main-safety` Ruleset이 active다.
- `ci-gate`가 Required Check다.
- `Allow auto-merge`가 활성화됐다.
- 자동 병합 허용·차단 상태가 PR에 기록된다.
- 실제 자동 병합 PR 증거가 있다.
