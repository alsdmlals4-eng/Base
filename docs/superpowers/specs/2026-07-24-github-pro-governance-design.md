# GitHub Pro 저장소 거버넌스 설계

## 목표

GitHub Pro에서 사용할 수 있는 비공개 저장소 보호·Ruleset·자동 병합 기능을 Base 공용 계약으로 만들고, `omenward`에서 먼저 시범 적용한 뒤 다른 활성 프로젝트로 순차 확산한다.

## 확정 결정

- 적용 방식: Base 공용 정책·Template → `omenward` 시범 → 다른 프로젝트 순차 확산
- 기본 병합 정책: `AUTO_MERGE_AFTER_REQUIRED_CHECKS`
- 사용자 최종 병합 승인은 기본 필수 조건에서 제거한다.
- `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `REVISE`, `BLOCKED`, `UNVERIFIED` 상태에서는 자동 병합하지 않는다.
- 1인 개발 저장소에서는 필수 승인 리뷰 수를 `0`으로 둔다.
- Required Check는 조건부 세부 Job이 아니라 안정된 `ci-gate`를 사용한다.
- main 직접 Push, force push, branch 삭제는 Ruleset으로 차단한다.
- 자동 병합은 Repository의 `Allow auto-merge`가 활성화되고 PR이 필수 검사 대기 상태일 때 사용한다.

## 근거

- GitHub Pro는 공개·비공개 저장소의 protected branch와 branch/tag ruleset을 지원한다.
- Auto-merge는 GitHub Pro의 공개·비공개 저장소에서 사용할 수 있고 모든 필수 검토·상태 검사가 충족되면 병합한다.
- 비공개 저장소의 Push ruleset은 GitHub Team 이상이므로 이번 범위에서 제외한다.
- Ruleset은 JSON으로 가져와 여러 저장소에 재사용할 수 있다.

Official references:

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository

## 공용 구조

```text
Base
├─ GitHub Pro 운영 정책
├─ Solo main safety Ruleset JSON
├─ 저장소 설정·예산 점검 Template
├─ 자동 병합 승인 게이트
└─ 정적 회귀 테스트

omenward
└─ Base Template 시범 적용 Issue
```

## 자동 병합 게이트

```text
PR 생성
→ required check 실행
→ GPT가 diff·계약·미검증 상태 확인
→ AUTO_MERGE_ELIGIBLE 판정
→ auto-merge 활성화
→ ci-gate·대화 해결·Ruleset 조건 충족
→ GitHub 자동 병합
```

자동 병합 허용 조건:

- PR이 Draft가 아님
- 현재 HEAD SHA가 검수 기준과 일치
- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `ci-gate` 등 저장소가 선언한 Required Check 성공
- 해결되지 않은 review thread 없음
- `USER_REVIEW_REQUIRED` 또는 `CHANGE_PROPOSAL` 없음
- Repository에서 auto-merge 사용 가능

## Ruleset

`solo-main-safety`는 기본 Branch를 대상으로 다음을 요구한다.

- PR을 통한 변경
- 필수 승인 리뷰 `0`
- review conversation 해결
- squash merge 허용
- `ci-gate` 통과
- 최신 base와 검증
- linear history
- force push 차단
- branch 삭제 차단

## 적용 단계

1. Base 정책·Template·테스트를 별도 PR로 병합한다.
2. Base Repository의 `Allow auto-merge`를 활성화한다.
3. `omenward`에 시범 적용 Issue를 만들고 Ruleset을 가져온다.
4. `omenward`의 실제 Required Check 이름을 확인해 `ci-gate` 계약을 적용한다.
5. 한 개 구현 PR에서 자동 병합을 검증한다.
6. 성공 후 Blacksmith, urban-legend, Ten-Paces-Hidden-Moves 등 활성 프로젝트로 순차 확산한다.

## 제외

- required approval 1개 이상
- CODEOWNERS 승인 강제
- 비공개 저장소 Push ruleset
- merge queue
- 모든 저장소 동시 적용
- 필수 검사 실패·미검증 상태의 자동 병합

## 완료 조건

- Base에 정책·Ruleset·점검 Template·회귀 테스트가 존재한다.
- 기존 GPT–Codex 정책의 사용자 최종 병합 필수 문구가 자동 병합 게이트로 교체된다.
- `omenward` 시범 적용 Issue가 생성된다.
- Base 새 PR에서 실제 Actions가 통과한다.
- Repository 설정 권한으로 가능한 경우 PR auto-merge가 활성화된다.
- 설정 API·도구 한계로 직접 적용하지 못한 항목은 정확한 UI 경로와 `UNVERIFIED_REPOSITORY_SETTING` 상태로 기록한다.
