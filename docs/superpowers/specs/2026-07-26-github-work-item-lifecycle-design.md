# GitHub Work Item Lifecycle Design

## 1. 목적

Base와 Base를 적용한 1인 게임 프로젝트에서 Issue·Goal·Branch·Pull Request·GitHub Actions Run·Artifact·Release가 누적되어 현재 작업을 방해하지 않도록 생명주기와 보존 책임을 분리한다.

이 설계의 핵심은 기록 삭제가 아니라 다음을 보장하는 것이다.

- 현재 작업은 소수의 열린 PR과 저장된 View에서 즉시 찾는다.
- 같은 Goal의 수정은 기존 Branch·PR을 계속 사용한다.
- Actions Run과 Artifact는 임시 증거로 취급하고 중요한 판단은 PR에 요약한다.
- 병합·종료된 PR과 Git 이력은 장기 기록으로 보존한다.
- 삭제·종료 전 후속 링크와 재개 조건을 남겨 누락을 막는다.

## 2. 검토한 접근

### 접근 A — 기록 보존형 생명주기 정책

Issue/Goal을 작업 정본, PR을 변경·판단·검증 정본, Run을 임시 실행 증거, Release를 장기 배포 산출물로 분리한다. 열린 PR WIP 제한, 같은 Goal의 PR 재사용, Squash merge, 병합 후 Branch 삭제, Run·Artifact 보존 기간을 함께 규정한다.

장점:

- 결정과 실패 근거를 잃지 않는다.
- 현재 작업 화면만 간결해진다.
- Base와 여러 프로젝트에 동일하게 확산할 수 있다.

단점:

- 초기에는 Label·Template·Repository 설정을 정렬해야 한다.

### 접근 B — 오래된 PR·Run 일괄 정리

오래된 PR과 Run을 기간 기준으로 대량 종료·삭제한다.

장점:

- 즉시 화면이 줄어든다.

단점:

- 후속 링크·실패 원인·검증 근거가 없는 항목을 잘못 제거할 위험이 크다.
- 누적 원인을 해결하지 못해 다시 쌓인다.

### 접근 C — 모든 장기 기록을 별도 문서로 이전

PR과 Run의 내용을 별도 Archive 문서나 데이터베이스에 복제한 뒤 GitHub 항목을 적극 정리한다.

장점:

- GitHub 화면은 가장 단순해진다.

단점:

- 두 번째 책임 원본과 동기화 비용이 생긴다.
- Git 자체의 검색·연결·검토 기록을 약화시킨다.

## 3. 선택

접근 A를 채택한다. Base의 기존 `docs/GITHUB_PRO_OPERATING_POLICY.md`와 `docs/CI_EXECUTION_COST_POLICY.md`는 각각 Repository 보호·병합 설정과 CI 실행 계층을 책임진다. 새 문서는 그 사이에서 Issue·Goal·Branch·PR·Run·Artifact·Release의 생명주기와 보존 책임을 단일 정본으로 관리한다.

## 4. 책임 경계

| 객체 | 책임 | 장기 보존 |
|---|---|---|
| Issue 또는 승인된 Goal | 목표·범위·완료 기준·후속 작업 | 보존 |
| Branch | 현재 구현 격리 | 병합·종료 후 삭제 가능 |
| Pull Request | 실제 변경·검토·결정·최종 검증 요약 | 보존 |
| Actions Run | 특정 SHA의 자동 실행 증거 | 기간 제한 가능 |
| Artifact | 실패 진단·임시 결과물 | 종류별 기간 제한 |
| Release | 배포 가능한 장기 산출물 | 보존 |
| `main` Commit | 병합된 논리 변경 | Squash commit으로 보존 |

## 5. 핵심 계약

### 5.1 하나의 Goal에는 하나의 활성 PR

새 PR 생성 전 같은 Issue·Goal·작업 Branch의 열린 PR을 검색한다. 범위가 동일하면 기존 PR과 Branch에 커밋을 추가한다. 리뷰 수정, 테스트 실패 수정, 문구 보완, 중단 후 재개는 새 PR 생성 사유가 아니다.

독립 PR은 별도 승인·롤백이 필요한 변경, 병합 순서가 분리되는 변경, 긴급 수정, 정책상 제안·구현 분리가 필요한 변경에 한정한다.

### 5.2 열린 PR WIP 제한

저장소 기본값:

- `status:active`: 최대 1개
- `status:review`: 최대 1개
- `status:blocked` 또는 `status:hold`: 최대 1개
- 전체 열린 PR: 권장 최대 3개

한도를 넘으면 새 PR을 만들기 전에 기존 PR을 병합, 종료, 통합 또는 Issue로 되돌린다. 이미 한도를 넘은 저장소는 기존 항목을 자동 삭제하지 않고 무손실 분류를 먼저 수행한다.

### 5.3 상태와 검색

공용 Label 기본값:

- `status:active`, `status:review`, `status:blocked`, `status:hold`
- `type:planning`, `type:docs`, `type:code`, `type:ci`, `type:data`
- `scope:base`, `scope:project`, `scope:godot`, `scope:tooling`

Label 생성 권한이나 Repository 설정을 확인하지 못하면 정책 문서와 PR 본문 상태를 먼저 적용하고 실제 설정은 `UNVERIFIED_REPOSITORY_SETTING`으로 남긴다.

### 5.4 병합과 Branch 정리

- 기본 병합 방식은 Squash merge다.
- 병합된 PR의 head Branch는 자동 삭제를 권장한다.
- 종료된 미병합 PR은 종료 사유, 보존할 조사 결과, 대체 Issue·PR, 재개 조건, Branch 삭제 가능 여부를 남긴다.
- 기본 Branch와 Release Branch는 삭제 대상이 아니다.

### 5.5 Run·Artifact 보존

기본 보존 목표:

| 항목 | 기본 보존 |
|---|---:|
| 성공한 일반 CI 로그·Run | 14일 |
| 실패한 일반 CI 로그·Run | 30일 |
| 실패 진단 Artifact | 14일 |
| 임시 HTML·스크린샷·테스트 보고서 | 14일 |
| 개발용 빌드 | 7일 |
| Release candidate | 30일 |
| 정식 Release | Actions Artifact가 아니라 GitHub Release에 보존 |

GitHub가 성공·실패 Run의 차등 보존을 직접 지원하지 않거나 더 긴 최소 기간을 강제하면 실제 지원 범위를 기록한다. Run 삭제 전 PR에는 결과, 실패 원인, 수정 내용, 최종 검증, 후속 작업을 남긴다.

### 5.6 오래된 Workflow

사용하지 않는 Workflow는 즉시 삭제하지 않는다.

1. 비활성화 또는 호출 차단
2. 대체 Workflow와 종료 이유 기록
3. 참조·Required Check·최근 사용 여부 확인
4. 고유 정보가 없고 롤백 경로가 있으면 승인 후 삭제

## 6. 적용 구성요소

### 6.1 새 정본

`docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`

Issue·Goal·Branch·PR·Run·Artifact·Release의 책임, WIP, 종료, 보존, 삭제 전 증거, 적용 순서를 관리한다.

### 6.2 문서 라우팅

`docs/DOCUMENTATION_MAP.md`에서 PR·Run·Artifact 누적, 기존 PR 재사용, Branch·증거 삭제 질문을 새 정본으로 연결한다.

### 6.3 PR Template

- Base 실제 PR: `.github/pull_request_template.md`
- 프로젝트 배포용: `templates/pull_request_template.md`

두 Template은 원본 Issue·Goal, 기존 PR 검색, 새 PR 필요 사유, 포함·제외 범위, 검증·미검증, Run·Artifact 보존, Branch 처리, Base·프로젝트 동기화를 기록한다.

Base Template은 프로젝트 전용 `docs/BASE_RULES_VERSION.md`를 요구하지 않는다. 프로젝트 Template은 Base 동기화 추적을 위해 해당 경로를 유지한다. 두 Template 모두 삭제된 `docs/AI_SHARED_WORK_RULES.md`를 요구하지 않는다.

### 6.4 회귀 검증

`tests/test_github_work_item_lifecycle_policy.py`는 정책 용어·WIP·보존 기간·Documentation Map·두 Template의 책임을 검사한다. 기존 Workflow가 이미 실행하는 `tests/test_ci_workflow_cost_policy.py`가 새 TestCase를 import하므로 Workflow 파일을 추가 수정하지 않는다.

### 6.5 변경 기록 보존

`docs/CHANGELOG.md`는 전체 파일을 안전하게 읽고 최소 patch할 수 없는 커넥터 경로에서 강제로 재작성하지 않는다. 구현 중 부분 교체 위험을 발견한 경우 `main`의 원본 blob으로 정확히 복구하고 최종 PR diff에서 제외한다. 이번 정책의 장기 변경 기록은 정책 문서, 설계, 실행 계획, PR과 squash commit이 보존한다.

## 7. 오류·예외 처리

- Repository 설정을 실제 변경하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 기록한다.
- Actions 사용 불가 시 `BLOCKED_BY_GITHUB_ACTIONS`, 판정 `UNVERIFIED`를 유지한다.
- 같은 Goal인지 불명확하면 새 PR을 자동 생성하지 않고 기존 Issue·PR·Branch 연결을 먼저 조사한다.
- 삭제 대상에 고유 정보, 열린 참조, 미해결 실패, Release 증거가 있으면 `KEEP_UNRESOLVED`로 유지한다.
- WIP 초과는 기존 PR 자동 종료 권한이 아니다.

## 8. 완료 기준

- 새 생명주기 정책이 공용 책임 원본으로 추가된다.
- Documentation Map, Base PR Template, 프로젝트 PR Template이 동기화된다.
- 정적 회귀 테스트가 기존 CI 계약 검사에서 실행된다.
- 변경은 별도 Branch와 PR로 제출된다.
- Repository 설정 중 도구로 확인·변경하지 못한 항목은 미검증으로 명시된다.
- 기존 열린 PR은 자동 종료·삭제하지 않는다.
- Changelog와 게임·런타임 파일에는 의도하지 않은 변경이 없다.
