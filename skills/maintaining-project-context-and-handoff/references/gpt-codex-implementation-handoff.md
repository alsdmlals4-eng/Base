# GPT–Codex 단계별 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 `on-demand-codex-handoff`와 `implementation-package-handoff` Skill Mode 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 1. 책임 분리

```text
GPT
= 평상시 기획·구현 보조·Godot POC + 사용자 요청 시 실행 명세 + 검수·자동 병합 적격성 판정

Codex Plan
= CODEX_PREFLIGHT_OPTIONAL 읽기 전용 재검수와 기술 개선·변경 제안 보고

Codex Build
= 실제 저장소·프로젝트·Godot 상태 재조사 + 지정 패키지 Branch의 구현·테스트·Commit·Push

사용자
= 프로젝트 방향·체감·새 기획 변경 결정

GitHub
= 필수 병합 게이트 충족 후 자동/에이전트 병합
```

## 2. On-demand 인계 준비

`USER_REQUESTED_CODEX_HANDOFF`가 발생하면 `ON_DEMAND_CODEX_HANDOFF`를 만든다.

최소 계약:

```yaml
mode: ON_DEMAND_CODEX_HANDOFF
trigger: USER_REQUESTED_CODEX_HANDOFF
intent_and_current_behavior:
actual_state_verification_required: true
repository_and_project_scope: []
godot_scope: []
known_problems_and_improvement_goals: []
protected_behavior_and_contracts: []
priority_order: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
performance_size_structure_checks: []
forbidden_or_high_risk_changes: []
codex_preflight: CODEX_PREFLIGHT_OPTIONAL
```

명세에는 다음 문장을 고정한다.

> 이 명세는 현재까지의 기획 의도와 예상 상태를 설명한다. 실제 구현 상태는 반드시 현재 GitHub 저장소, 로컬 프로젝트 파일 및 Godot 프로젝트를 직접 조사하여 검증할 것. 명세와 실제 구현이 충돌하면 임의로 덮어쓰지 말고 원인을 분석한 뒤 가장 안전한 개선안을 선택할 것.

작은 국소 변경에는 마스터 계획·상위 Issue·별도 Codex Plan을 형식적으로 강제하지 않는다.

## 3. L2 이상 패키지 준비 게이트

다중 의존성·고위험·Vertical Slice 구현처럼 패키지화가 필요한 경우 다음을 확인한다.

- 프로젝트 코어와 통합 설계가 승인됨
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 마스터 구현계획 존재
- 상위 구현 Issue 존재 또는 생성 계약 존재
- 현재 패키지 결과·포함·제외·수정 금지 범위 존재
- 데이터·저장·ID·Schema 보호 조건 존재
- 패키지 Branch가 최신 기준 Commit에서 준비됨
- 테스트 명령과 rollback 존재
- 사용자 기존 변경·보호 경로 파악
- 저장소 병합 정책과 Required Check 선언

하나라도 차단되면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

## 4. 패키지 경계

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

## 5. `CODEX_PREFLIGHT_OPTIONAL` Plan

별도 Codex Plan은 다음에서만 사용한다.

- 저장·Schema·마이그레이션·플랫폼 설정 같은 고위험 변경
- GPT 명세와 실제 저장소의 drift 가능성이 큼
- 여러 패키지·Scene·공용 Resource가 얽힘
- 구현 전에 기술 대안·`CHANGE_PROPOSAL` 분리가 필요함
- 사용자가 명시적으로 Plan 검토를 요청함

사용할 경우 Codex Plan은 읽기 전용이다.

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

Codex가 제출할 보고서는 `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md`를 따른다. Plan을 생략해도 Build의 실제 저장소 선조사는 필수다.

## 6. Plan 판정

### 기술 개선

플레이어 결과와 승인된 데이터·저장 계약을 유지하면 GPT가 패키지 계약에 반영할 수 있다.

### `CHANGE_PROPOSAL`

프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 호환성 파괴가 필요하면 구현과 분리한다.

### 사용자 결정

조작감, 난이도, 보상 체감, 아트·연출·사운드, 둘 이상의 유효한 UX 선택, Vertical Slice 승인에는 `USER_DECISION_REQUIRED`를 사용한다.

## 7. GPT의 선택적 Plan 반영

Codex Plan을 사용한 경우 Codex가 문서를 수정하지 않는다. GPT가 다음을 수행한다.

1. 최신 저장소 조사 근거 확인
2. 마스터 계약과 대조
3. 기술 개선 승인·기각
4. `CHANGE_PROPOSAL`·사용자 결정 분리
5. 패키지 계약·Issue·체크리스트 갱신
6. `READY_FOR_BUILD` 판정

## 8. Codex Build 지시

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

Build 첫 단계는 최신 `main`, 지정 Branch, 실제 Godot Scene·Script·Resource·project.godot·테스트를 직접 확인하는 것이다. 비-Godot 변경이 필요하면 구현하지 않고 `non_godot_change_request`로 반환한다.

## 9. 구현 결과 검수

GPT는 Push된 Commit과 PR diff에서 확인한다.

- 지정 Branch·Commit·변경 파일
- Commit SHA와 원격 HEAD 일치
- Godot 런타임 파일 외 혼입
- 승인된 패키지 범위
- 기술 개선과 기획 변경 구분
- 데이터·저장 호환성
- 정상·실패·경계·회귀 테스트
- 미실행 검증·위험·롤백

## 10. 패키지 종료 상태

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

`PACKAGE_APPROVED*`만 다음 패키지와 자동 병합 적격성 검토에 진입한다.

## 11. 자동 병합 게이트

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 사용자의 명시적 승인이 완료된 동일 범위는 추가 확인·재승인·병합 승인 요청 없이 검증 후 병합한다.

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
- Repository `Allow auto-merge` 또는 저장소가 허용한 병합 방식
- active Ruleset 또는 동등한 branch protection
- `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL` 없음

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

사용자 최종 병합 클릭은 기본 필수가 아니다. 기존 승인 범위를 벗어난 새 사용자 결정이 필요한 상태에서는 결정을 반영한 뒤 다시 검수한다.

## 12. GitHub 구조

L2 이상 패키지 작업의 기본 구조:

```text
상위 구현 Issue
├─ PKG-00 Branch / PR
├─ PKG-01 Branch / PR
├─ PKG-02 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 도구·자산 파이프라인만 병렬 허용한다.

## 13. 중단·재개

중단 시 Handoff에 다음을 남긴다.

- 마지막 승인 범위와 Commit
- 현재 패키지 상태
- Codex Plan 사용 여부와 결과
- Push된 Commit·테스트
- `CHANGE_PROPOSAL`·사용자 결정
- 자동 병합 상태와 차단 원인
- 다음 첫 행동
- 롤백 경로

재개 시 최신 `main`과 패키지 Branch를 다시 대조하고 오래된 Plan이나 과거 대화만 그대로 사용하지 않는다.
