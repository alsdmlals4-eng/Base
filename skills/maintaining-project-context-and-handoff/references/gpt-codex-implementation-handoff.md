# GPT–Codex 단계별 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 `implementation-package-handoff` Skill Mode 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 1. 책임 분리

```text
GPT
= 기획·비-Godot 파일·GitHub 계약·Plan 문서·검수·자동 병합 적격성 판정

Codex Plan
= 최신 저장소 읽기 전용 재검수와 기술 개선·변경 제안 보고

Codex Build
= 지정 패키지 Branch의 Godot 구현·테스트·Commit·Push

사용자
= 프로젝트 방향·체감·기획 변경 결정

GitHub
= 필수 병합 게이트 충족 후 자동 병합
```

## 2. 인계 준비 게이트

다음을 모두 확인한다.

- 프로젝트 코어와 통합 설계가 승인됨
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 마스터 구현계획 존재
- 상위 구현 Issue 존재 또는 생성 계약 존재
- 현재 패키지 결과·포함·제외·수정 금지 범위 존재
- 데이터·저장·ID·Schema 보호 조건 존재
- 패키지 Branch가 최신 기준 Commit에서 준비됨
- Codex Plan 보고 Template과 테스트 명령 존재
- 사용자 기존 변경·보호 경로 파악
- 저장소 병합 정책과 Required Check 선언

하나라도 차단되면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

## 3. 패키지 경계

패키지는 파일 목록이 아니라 독립 결과로 정의한다.

좋은 경계:

- 핵심 상태 모델이 테스트 가능한 상태
- 하나의 플레이 행동이 입력→반응→결과까지 동작
- 실패·복구 루프가 독립 검증됨
- 저장·불러오기 한 주기가 호환성 테스트됨
- Vertical Slice 대표 구간이 플레이 가능

나쁜 경계:

- 스크립트 세 개 작성
- UI 파일 모음
- 여러 의존 시스템을 동시에 변경하지만 독립 결과가 없음
- 같은 Scene·Schema를 여러 패키지가 경쟁 수정

## 4. Codex Plan 요청

Codex Plan에는 다음을 명시한다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
baseline_branch:
baseline_commit:
allowed_branch:
master_plan:
package_contract:
required_reading: []
```

Codex가 제출할 보고서는 `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md`를 따른다.

## 5. Plan 판정

### 기술 개선

플레이어 결과와 승인된 데이터·저장 계약을 유지하면 GPT가 패키지 계약에 반영할 수 있다.

### `CHANGE_PROPOSAL`

프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 호환성 파괴가 필요하면 구현과 분리한다.

### 사용자 결정

조작감, 난이도, 보상 체감, 아트·연출·사운드, 둘 이상의 유효한 UX 선택, Vertical Slice 승인에는 `USER_DECISION_REQUIRED`를 사용한다.

## 6. GPT의 Plan 반영

Codex가 문서를 수정하지 않는다. GPT가 다음을 수행한다.

1. 최신 저장소 조사 근거 확인
2. 마스터 계약과 대조
3. 기술 개선 승인·기각
4. `CHANGE_PROPOSAL`·사용자 결정 분리
5. 패키지 계약·Issue·체크리스트 갱신
6. `READY_FOR_BUILD` 판정

## 7. Codex Build 지시

Codex Build에는 다음을 고정한다.

```yaml
branch:
  create_or_switch: FORBIDDEN
  allowed_branch: <GPT가 지정>
  push_target: ALLOWED_BRANCH_ONLY
commit:
  godot_runtime_files_only: true
  unrelated_changes: FORBIDDEN
  preserve_user_changes: true
  force_push: FORBIDDEN
  amend: FORBIDDEN
  independent_commits: REQUIRED
pull_request:
  create_or_update: FORBIDDEN
  merge: FORBIDDEN
```

비-Godot 변경이 필요하면 구현하지 않고 `non_godot_change_request`로 반환한다.

## 8. 구현 결과 검수

GPT는 Push된 Commit과 PR diff에서 확인한다.

- 지정 Branch·Commit·변경 파일
- Commit SHA와 원격 HEAD 일치
- Godot 런타임 파일 외 혼입
- 승인된 패키지 범위
- 기술 개선과 기획 변경 구분
- 데이터·저장 호환성
- 정상·실패·경계·회귀 테스트
- 미실행 검증·위험·롤백

## 9. 패키지 종료 상태

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

`PACKAGE_APPROVED*`만 다음 패키지 선행 조건과 자동 병합 적격성 검토에 진입한다.

## 10. 자동 병합 게이트

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`다.

```yaml
merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS
reviewed_head_sha:
current_head_sha:
required_check: ci-gate
required_checks_passed:
unresolved_review_threads:
repository_auto_merge:
ruleset:
user_review_required:
change_proposal:
merge_gate:
```

허용 조건:

- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- PR이 Draft가 아님
- HEAD SHA가 검수 뒤 바뀌지 않음
- Required Check 성공
- unresolved review thread 0
- Repository `Allow auto-merge` 활성화
- active Ruleset 또는 동등한 branch protection
- `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL` 없음

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

사용자 최종 병합 클릭은 기본 필수가 아니다. 사용자 결정이 필요한 상태에서는 결정을 반영한 뒤 다시 검수한다.

## 11. GitHub 구조

```text
상위 구현 Issue
├─ PKG-00 Branch / PR
├─ PKG-01 Branch / PR
├─ PKG-02 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 도구·자산 파이프라인만 병렬 허용한다.

## 12. 중단·재개

중단 시 Handoff에 다음을 남긴다.

- 마지막 승인 패키지와 Commit
- 현재 패키지 상태
- Codex Plan 결과
- Push된 Commit·테스트
- `CHANGE_PROPOSAL`·사용자 결정
- 자동 병합 상태와 차단 원인
- 다음 첫 행동
- 롤백 경로

재개 시 최신 `main`과 패키지 Branch를 다시 대조하고 오래된 Plan을 그대로 사용하지 않는다.
