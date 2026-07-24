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

## 2. Repository Governance Profile

각 저장소는 `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`를 사용해 다음을 선언한다.

```yaml
repository:
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
- Repository의 `Allow auto-merge` 활성화
- active Ruleset 또는 동등한 branch protection 존재

상태:

- `AUTO_MERGE_ELIGIBLE`: 조건 충족, auto-merge를 활성화할 수 있음
- `AUTO_MERGE_ENABLED`: GitHub에 auto-merge 예약됨
- `AUTO_MERGE_BLOCKED`: 기획 결정·검증·Repository 설정으로 차단됨
- `UNVERIFIED_REPOSITORY_SETTING`: Repository 설정을 실제 확인하지 못함

사용자 최종 병합 클릭은 기본 필수가 아니다. 다만 `USER_REVIEW_REQUIRED`와 `CHANGE_PROPOSAL`은 자동 병합 전에 사용자 결정을 요구한다.

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
