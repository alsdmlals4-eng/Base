# GitHub 작업 항목 생명주기 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 Issue·승인된 Goal·Branch·Pull Request·GitHub Actions Run·로그·Artifact·Release의 책임, 현재 작업 한도, 종료, 보존, 무손실 정리를 관리하는 공용 정본이다.

Repository 보호·Ruleset·자동 병합 설정은 `docs/GITHUB_PRO_OPERATING_POLICY.md`, 변경 위험별 CI 실행 계층과 중복 Run 취소는 `docs/CI_EXECUTION_COST_POLICY.md`가 계속 책임진다.

## 1. 목표

- 현재 작업과 검토 대상을 열린 PR 소수로 제한한다.
- 같은 목표의 수정·리뷰 대응·테스트 수정은 기존 Branch와 PR을 계속 사용한다.
- 중요한 결정과 최종 검증은 PR에 보존하고 Run·Artifact는 기간 제한이 가능한 실행 증거로 취급한다.
- 병합·종료·삭제 전에 대체 항목, 고유 정보, 재개 조건, 롤백을 남겨 누락을 막는다.
- 기존 누적 항목은 자동 삭제하지 않고 무손실 분류 후 정리한다.

## 2. 객체별 책임과 보존

| 객체 | 책임 | 기본 보존 |
|---|---|---|
| Issue 또는 승인된 Goal | 목표·배경·범위·제외 범위·완료 기준·후속 작업 | 장기 보존 |
| Branch | 승인된 변경의 격리 작업공간 | 병합·종료 후 삭제 가능 |
| Pull Request | 실제 diff·검토·결정·실패 원인·최종 검증·미검증 | 장기 보존 |
| Actions Run | 특정 SHA와 이벤트에서 실행한 자동 검증 증거 | 기간 제한 가능 |
| 로그 | Run의 상세 진단 | 기간 제한 가능 |
| Artifact | 실패 진단·테스트 보고서·임시 빌드·캡처 | 종류별 기간 제한 |
| GitHub Release | 배포 가능한 장기 빌드와 Release note | 장기 보존 |
| `main` Commit | 병합된 논리 변경 | Squash commit으로 보존 |

PR 번호, Run URL, Branch 이름만 별도 문서에 복제해 두 번째 활성 정본으로 만들지 않는다. 현재 상태는 GitHub 객체와 프로젝트 Active Context가 책임지고, 과거 상태는 Git 이력과 종료된 PR이 책임진다.

## 3. 새 PR 생성 전 검색

새 PR을 만들기 전에 다음 순서로 조사한다.

```text
원본 Issue·승인된 Goal
→ 같은 Goal을 참조하는 열린 PR
→ 같은 작업 Branch
→ 대체·후속 PR 링크
→ 현재 열린 PR WIP
→ 새 PR 필요 여부
```

### 3.1 하나의 Goal에는 하나의 활성 PR

같은 Issue 또는 승인된 Goal의 구현·문서·리뷰 수정은 **하나의 Goal에는 하나의 활성 PR**을 기본값으로 사용한다.

다음은 새 PR 생성 사유가 아니다.

- 리뷰 지적 수정
- 테스트 실패 수정
- 같은 범위의 문구·데이터·설정 보완
- 작업 중단 후 동일 목표 재개
- 이전 커밋의 오류 수정
- Draft에서 review 상태로 전환

다음 중 하나가 성립할 때만 독립 PR을 허용한다.

- 별도 승인·검증·롤백이 필요한 독립 변경
- 기존 PR과 함께 병합할 수 없는 긴급 수정
- 책임 원본과 병합 순서가 명확히 분리되는 작업
- Base 수정제안처럼 정책이 제안 PR과 구현 PR 분리를 요구하는 작업
- 기존 PR이 종료됐고 종료 사유·재개 조건·후속 링크가 기록된 작업

새 PR 본문에는 `기존 PR 검색 결과`와 `새 PR 필요 사유`를 남긴다.

## 4. 열린 PR WIP 제한

1인 개발 저장소의 기본 운영 한도는 다음과 같다.

| 상태 | 기본 한도 |
|---|---:|
| `status:active` | 1개 |
| `status:review` | 1개 |
| `status:blocked` 또는 `status:hold` | 1개 |
| 전체 열린 PR | **권장 최대 3개** |

전체 열린 PR이 권장 최대 3개를 넘으면 새 PR을 만들기 전에 기존 항목을 다음 중 하나로 판정한다.

```text
CONTINUE_EXISTING_PR
MERGE_READY
MOVE_TO_REVIEW
RETURN_TO_ISSUE
SUPERSEDED_CLOSE
HOLD_WITH_RESUME_CONDITION
KEEP_UNRESOLVED
```

WIP 초과는 기존 PR을 자동 종료·삭제할 권한이 아니다. 고유 정보, 열린 참조, 미해결 실패, 사용자 결정 대기, Release 증거가 있으면 `KEEP_UNRESOLVED`로 유지한다.

## 5. 상태 Label과 저장 View

공용 기본 Label:

```text
status:active
status:review
status:blocked
status:hold

type:planning
type:docs
type:code
type:ci
type:data

scope:base
scope:project
scope:godot
scope:tooling
```

권장 검색:

```text
is:pr is:open label:"status:active"
is:pr is:open label:"status:review"
is:pr is:open label:"status:blocked"
is:pr is:merged
```

Label이나 GitHub Projects View를 실제 생성하지 못한 환경에서는 PR 본문에 상태를 기록하고 `UNVERIFIED_REPOSITORY_SETTING`으로 남긴다.

## 6. 병합·종료·Branch 처리

### 6.1 병합

- 기본 병합 방식은 **Squash merge**다.
- `main`에는 PR 하나당 논리 변경 하나를 남긴다.
- PR 내부의 세부 커밋과 검토 대화는 PR 기록에서 보존한다.
- 자동 병합 조건은 `docs/GITHUB_PRO_OPERATING_POLICY.md`를 따른다.

### 6.2 병합 후 Branch

병합 후 Branch는 다음 조건을 모두 만족하면 삭제할 수 있다.

- PR이 기본 Branch에 병합됐다.
- 다른 열린 PR의 head 또는 base로 사용되지 않는다.
- Release·hotfix·장기 지원 Branch가 아니다.
- 미병합 고유 커밋이 없다.
- 복구 경로가 PR과 Git 이력에 남아 있다.

Repository의 `Automatically delete head branches` 사용을 권장한다. 실제 설정을 확인하지 못하면 활성화됐다고 주장하지 않고 `UNVERIFIED_REPOSITORY_SETTING`으로 기록한다.

### 6.3 미병합 종료

종료되는 PR에는 다음을 남긴다.

```markdown
## 종료·대체 정보

- 종료 판정: SUPERSEDED_CLOSE | RETURN_TO_ISSUE | HOLD_WITH_RESUME_CONDITION
- 종료 이유:
- 적용된 변경:
- 보존할 조사·실패·결정:
- 대체 Issue·PR:
- 재개 조건:
- Branch 삭제 가능 여부:
```

대체 항목이 없거나 고유 정보가 확인되지 않으면 Branch를 삭제하지 않는다.

## 7. Actions Run·로그·Artifact 보존

### 7.1 기본 운영 목표

| 항목 | 기본 보존 목표 |
|---|---:|
| 성공한 일반 CI 로그·Run | 14일 |
| 실패한 일반 CI 로그·Run | 30일 |
| 실패 진단 Artifact | 14일 |
| 임시 HTML·스크린샷·테스트 보고서 | 14일 |
| 개발용 빌드 | 7일 |
| Release candidate | 30일 |
| 정식 배포 빌드 | Actions Artifact가 아니라 GitHub Release에 보존 |

GitHub가 성공·실패 로그의 차등 보존을 직접 지원하지 않거나 Repository 최소 보존 기간이 더 길면 다음을 사용한다.

- Repository 로그 보존은 실패 분석을 포함할 수 있는 값으로 설정한다.
- 성공한 오래된 Run의 별도 삭제 자동화는 권한·필터·복구 위험을 검증한 경우에만 도입한다.
- Artifact는 `retention-days`로 가능한 한 해당 종류의 목표 기간을 선언한다.
- 실제 설정과 정책 목표의 차이는 Repository Governance Profile 또는 Usage Budget에 기록한다.

### 7.2 Run 삭제 전 PR 증거

Run 또는 Artifact가 만료·삭제돼도 판단을 복원할 수 있도록 PR에 다음을 남긴다.

```markdown
## 최종 검증 요약

- 기준 HEAD SHA:
- 실행한 검사:
- 성공:
- 실패 원인:
- 수정 내용:
- 미검증·차단:
- 장기 보존이 필요한 Artifact:
- 후속 Issue·PR:
```

다음 Run은 정리 후보가 될 수 있다.

- 같은 PR의 새 커밋으로 대체된 취소 Run
- 동일 SHA·동일 목적의 중복 Run
- 후속 성공과 PR 원인 기록이 있는 반복 실패 Run
- 더 이상 사용하지 않는 임시 Workflow Run

다음은 자동 삭제하지 않는다.

- 원인을 찾지 못한 간헐적 실패
- Release·배포·보안 검증 증거
- CI 정책 변경의 기준 Run
- 후속 Issue·PR에서 명시적으로 참조하는 Run

## 8. 오래된 Workflow 처리

사용하지 않는 Workflow는 다음 순서로 처리한다.

```text
INVENTORY
→ DISABLE_OR_BLOCK_TRIGGER
→ RECORD_REPLACEMENT
→ CHECK_REQUIRED_CHECK_REFERENCES
→ OBSERVE
→ DELETE_APPROVED
```

삭제 전 확인:

- Branch protection·Ruleset의 Required Check 이름
- 다른 Workflow의 `workflow_call`·artifact 의존성
- README·정책·Issue·PR 참조
- 고유 secret·permission·runner 계약
- 대체 Workflow와 롤백 경로

확인되지 않은 Workflow는 `KEEP_UNRESOLVED`로 유지한다.

## 9. 기존 누적 항목 무손실 정리

기존 열린 PR과 Run을 기간만으로 일괄 삭제하지 않는다.

### 9.1 PR 정리 순서

1. 열린 PR 목록을 수집한다.
2. Issue·Goal·대체 PR·Branch·HEAD SHA를 연결한다.
3. `active / review / blocked / hold / superseded / unresolved`로 분류한다.
4. 같은 Goal의 PR은 고유 변경과 병합 가능성을 비교한다.
5. 대체된 PR에 종료·대체 정보를 남긴다.
6. 사용자 결정·검증이 필요한 항목은 유지한다.
7. 종료 후 Branch 삭제 조건을 별도로 검사한다.

### 9.2 Run 정리 순서

1. Release·보안·CI 정책 기준 Run을 제외한다.
2. 취소·중복·후속 성공 Run을 찾는다.
3. PR 최종 검증 요약 존재 여부를 확인한다.
4. 참조되지 않는 Artifact와 임시 빌드를 확인한다.
5. 보존 정책과 Repository 설정을 대조한다.
6. 삭제 또는 만료 결과를 보고한다.

## 10. Base와 프로젝트의 책임 분리

### Base 공용

- 객체별 책임과 상태 언어
- 하나의 Goal·하나의 활성 PR 원칙
- WIP 기본값
- 종료·대체·무손실 정리 절차
- Run·Artifact 기본 보존 목표
- PR Template과 정적 검증

### 프로젝트 전용

- 실제 Label·Project View
- Repository 로그 보존 기간
- Artifact별 `retention-days`
- Required Check 이름
- Release·hotfix Branch 목록
- nightly·release Workflow 운영 여부
- 저장소별 WIP 예외와 승인자

프로젝트는 Base 기본값을 완화하거나 강화할 수 있지만 실제 값을 Repository Governance Profile 또는 프로젝트 운영 문서에 선언한다.

## 11. 적용 순서

```text
Base 정책·Template·Test
→ Base PR에서 실제 적용
→ 기존 열린 PR 무손실 인벤토리
→ 활성 프로젝트 한 곳 Pilot
→ 결과·예외 기록
→ 다른 프로젝트 순차 동기화
```

정책 병합만으로 Label, View, 자동 Branch 삭제, 로그 보존 설정이 자동 적용됐다고 간주하지 않는다.

## 12. 완료 조건

- 새 PR 생성 전 기존 Issue·Goal·PR·Branch를 검색한다.
- 같은 Goal의 수정은 기존 PR에서 이어진다.
- 열린 PR WIP와 초과 처리 판정이 기록된다.
- 병합·종료된 PR에 검증·미검증·후속·Branch 처리 정보가 있다.
- Run·Artifact 만료 전 중요한 판단이 PR에 남는다.
- 정식 빌드는 GitHub Release에 보존된다.
- Repository 설정은 실제 확인된 값과 `UNVERIFIED_REPOSITORY_SETTING`을 구분한다.
- 기존 열린 PR과 Run은 승인·증거 없이 자동 삭제되지 않는다.

## 13. 롤백

정책 적용으로 작업이 차단되면 다음 순서로 완화한다.

1. 자동 삭제·자동 종료 작업을 중지한다.
2. 영향을 받은 PR·Branch·Run 목록을 고정한다.
3. 종료된 PR은 필요 시 reopen하고 Branch 복구 가능성을 확인한다.
4. WIP 한도를 권장값으로만 유지하고 강제 자동화를 해제한다.
5. Required Check·Workflow 참조를 원래 값으로 복구한다.
6. 원인, 손실 여부, 재개 조건을 Issue에 기록한다.
