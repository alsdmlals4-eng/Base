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

## 14. 프로젝트 작업 칸반·증거 체크리스트

`PROJECT_WORK_KANBAN_CHECKLIST`

이 절은 프로젝트 작업을 이미지와 같은 카드·체크리스트로 확인하며 진행하기 위한 공용 운영 계약이다. 새 정본이나 독립 PM framework가 아니라 기존 Issue·Goal·PR 생명주기, 프로젝트 시작 receipt, continuous work queue와 개발 검증 Gate를 연결한다.

```text
GOAL_OR_PLAYABLE_SLICE_PARENT_ISSUE
INDEPENDENT_WORK_ITEM
CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON
PROJECTS_DERIVED_VIEW_NOT_CANON
REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE
NO_ISSUE_EXPLOSION
PLAIN_MARKDOWN_TASK_LIST_NOT_RETIRED_TASKLIST_BLOCK
PASS_ONLY_COUNTS_COMPLETE
NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR
NO_APPLICABLE_CHECKLIST
NO_PROJECTS_WRITE_CAPABILITY_IS_NOT_BLOCKER
UNVERIFIED_PROJECTS_CONFIGURATION
UNVERIFIED_SUB_ISSUE_RELATION
NO_HTML_DASHBOARD
NO_NEW_PAID_PM_TOOL
NO_FLEET_WIDE_EMPTY_ARTIFACT_ROLLOUT
IN_PROGRESS_WIP_LIMIT: 1
VERIFY_REVIEW_WIP_LIMIT: 1
```

### 14.1 권한과 작업 계층

| Surface | 책임 | 정본 여부 |
|---|---|---:|
| 프로젝트 repository owner | 기획·Decision·data·code·Scene·Resource·승인 asset·test·runtime evidence | 정본 |
| Goal 또는 Playable Slice 부모 Issue | 승인 Goal의 가치·범위·제외 범위·완료 기준·하위 작업 관계 | 지속 work item |
| 독립 작업 Issue | 별도 실행·차단·검증·재개가 필요한 작업 단위 | 지속 work item |
| `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md` 기반 카드 | owner 상태·진행·증거·다음 행동을 요약한 receipt | derived |
| GitHub Projects | Issue·PR과 field를 board/table/roadmap으로 보여 주는 선택형 View | derived |

충돌 시 최신 사용자 지시 → 프로젝트 `AGENTS.md`와 Active Context → 실제 repository owner·implementation·evidence → 승인 Goal Issue 순으로 다시 읽고 카드와 Projects field를 교정한다. 카드나 보드만 바꿔 프로젝트 Decision·구현·검증 상태를 확정하지 않는다.

```text
Project
└─ Goal 또는 Playable Slice 부모 Issue
   ├─ 독립 작업 Issue
   │  ├─ bounded checklist item
   │  └─ verification item
   └─ 독립 작업 또는 사용자 결정 Issue
```

다음 중 하나가 있을 때만 `INDEPENDENT_WORK_ITEM`으로 분리한다.

- 별도 owner 또는 PR이 있다.
- 독립적으로 block·defer·resume될 수 있다.
- 별도 Acceptance Criteria 또는 검증이 있다.
- 다른 작업이 명시적으로 의존한다.
- reviewer가 해당 작업만 독립적으로 판정할 수 있다.

동일 파일의 작은 순차 수정, 몇 분 단위 확인, 하나의 검증 사이클 안에서 분리 가치가 없는 단계는 카드 내부 Markdown task list로 유지한다. GitHub의 과거 tasklist block 문법을 새로 도입하지 않는다.

### 14.2 상태와 WIP

기본 흐름:

```text
BACKLOG
→ READY
→ IN_PROGRESS
→ VERIFY_REVIEW
→ DONE

BLOCKED_DECISION
```

`BLOCKED_DECISION`은 정상 완료 단계가 아니라 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`를 한눈에 보는 파생 board column이다. blocker가 해제되면 실제 상태와 원래 흐름으로 복귀한다.

| Work item 상태 | 의미 | 완료 수 포함 |
|---|---|---:|
| `BACKLOG` | 승인 범위 후보지만 현재 실행 순서 밖 | 아니오 |
| `READY` | owner·dependency·Acceptance·검증 준비 완료 | 아니오 |
| `IN_PROGRESS` | 현재 수행 중인 active task | 아니오 |
| `VERIFY_REVIEW` | 구현·준비 뒤 증거·검토·readback 대기 | 아니오 |
| `BLOCKED_UNVERIFIED` | 필수 source·executor·permission·evidence 부재 | 아니오 |
| `USER_DECISION_REQUIRED` | 제품 의미·범위·비용·권한·공개 배포 결정 필요 | 아니오 |
| `DEFERRED` | 재개 조건과 함께 현재 실행에서 뒤로 이동 | 아니오 |
| `DONE` | Acceptance와 요구 evidence·readback 충족 | 예 |
| `NOT_APPLICABLE` | 현재 항목에 적용되지 않으며 이유 기록 | 분모 제외 |

1인 개발 기본 WIP는 `IN_PROGRESS_WIP_LIMIT: 1`, `VERIFY_REVIEW_WIP_LIMIT: 1`이다. 차단 작업이 있어도 독립 `READY` 작업이 있으면 continuous work recovery ladder에 따라 계속한다. WIP 초과는 기존 Issue·PR을 자동 종료하거나 작업을 숨길 권한이 아니다.

### 14.3 진행률과 evidence

```text
applicable_items = all checklist items - NOT_APPLICABLE items
completed_items = PASS items only
progress = completed_items / applicable_items
```

사용자 표시식은 `completed_items / applicable_items`다. `[x]`는 실제 evidence가 있는 `PASS`에만 사용한다. `READY`, `IN_PROGRESS`, `VERIFY_REVIEW`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`, `FAIL`은 완료가 아니다. 적용 항목이 0개이면 `0/0` 또는 `100%`가 아니라 `NO_APPLICABLE_CHECKLIST`로 표시한다.

진행률은 상태 요약일 뿐 완료 판정을 대체하지 않는다. 카드 전체 `DONE`에는 최소 다음이 필요하다.

1. 모든 필수 Acceptance Criteria가 evidence와 함께 PASS다.
2. 해당 카드에 요구된 `E0_CONTRACT`부터 `E6_HUMAN_PLAYTEST` 중 필요한 수준이 PASS다.
3. 열린 `MUST_FIX`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`가 없다.
4. repository owner·actual consumer·handoff의 필요한 readback이 끝났다.
5. 실제 변경에는 exact diff·HEAD 또는 merged main·rollback이 연결됐다.

자동 테스트 PASS는 runtime·화면·UX·Human/Player·사용자 승인·release PASS가 아니다.

### 14.4 Continuous work queue 매핑

새 queue schema를 만들지 않고 기존 continuous work 실행 상태를 재사용한다.

```text
READY                  ↔ ready_tasks
IN_PROGRESS            ↔ ready_tasks 중 현재 owner/lease가 잡힌 단일 작업
BLOCKED_UNVERIFIED     ↔ deferred_tasks + blocker와 recovery route
USER_DECISION_REQUIRED ↔ deferred_tasks + decision packet
DEFERRED               ↔ deferred_tasks + resume condition
DONE                   ↔ completed_tasks
```

카드와 queue가 불일치하면 실제 owner·evidence를 다시 읽고 둘을 교정한다. queue 이동만으로 repository 사실이나 Acceptance 결과를 바꾸지 않는다.

### 14.5 선택형 GitHub Projects 파생 View

권장 board columns:

```text
Backlog | Ready | In Progress | Verify/Review | Blocked/Decision | Done
```

권장 fields:

| Field | 값·용도 |
|---|---|
| Status | 위 board column |
| Project | 프로젝트 식별 |
| Goal/Slice | 부모 Goal 또는 Slice |
| Priority | P0 / P1 / P2 / P3 |
| Category | Planning / System-Data / Code / UI-UX / Visual / Audio-VFX / Bug / QA / Canon-Docs / Release |
| Evidence | Not Run / Partial / Pass / Fail / Blocked |
| Next action | 다음 안전 작업 |

Projects API·connector나 account 권한으로 실제 생성·field 설정·readback을 수행하지 못하면 `NO_PROJECTS_WRITE_CAPABILITY_IS_NOT_BLOCKER`를 적용한다. Issue와 `PROJECT_WORK_ITEM_CHECKLIST.md`를 코어로 계속 사용하고 `UNVERIFIED_PROJECTS_CONFIGURATION`을 기록한다. 부모·하위 Issue 관계를 실제로 쓰거나 다시 읽지 못하면 plain Issue reference를 유지하고 `UNVERIFIED_SUB_ISSUE_RELATION`으로 남긴다. 설정하지 않은 board·automation·relation을 완료로 주장하지 않는다.

동일 의미를 repository owner, Issue 본문, Projects field에 각각 별도 사실로 중복 소유하지 않는다. 프로젝트가 이미 같은 목적의 Issue field·label·Project view를 채택했다면 기존 구조를 재사용하고 Base 명칭을 강제 복제하지 않는다.

### 14.6 생성·갱신·적용 순서

```text
프로젝트 fresh-read와 start canon reconciliation
→ 현재 Goal 또는 Playable Slice 복원
→ 같은 Goal의 기존 Issue·PR·work item 검색
→ remaining work를 독립 작업 기준으로 분류
→ 기존 work item 재사용 또는 필요한 최소 Issue 생성
→ READY / BLOCKED / DECISION queue 구성
→ active task 하나를 IN_PROGRESS로 선택
→ 작업·검증·readback 뒤 checklist와 evidence 갱신
→ VERIFY_REVIEW 또는 실제 blocker 상태
→ remaining-work recalculation과 적대적 검토
→ 요구 작업과 blocker 0일 때 DONE
→ 다음 READY 작업
```

모든 기존 프로젝트에 빈 Issue·카드·board를 일괄 생성하지 않는다. 새 material 작업, 재개, Goal 변경, major closeout 또는 다음 Playable Slice 진입에서 현재 프로젝트 규칙에 맞게 적용한다. 첫 pilot의 실제 사용 evidence 전에는 PM 효율·개발 속도·품질 향상을 측정 완료로 주장하지 않는다.
