# 프로젝트 작업 카드·체크리스트

> 이 템플릿은 Goal·Playable Slice 또는 독립 작업의 진행 상태를 보여 주는 운영용 receipt다. 프로젝트의 기획·결정·데이터·코드·Scene·Resource·승인 asset·test·runtime evidence는 현재 repository owner가 계속 소유한다.

```text
PROJECT_WORK_KANBAN_CHECKLIST
CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON
PASS_ONLY_COUNTS_COMPLETE
NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR
NO_APPLICABLE_CHECKLIST
PARENT_GOAL_PROGRESS_USES_REQUIRED_CHILD_DONE_COUNT
DO_NOT_AVERAGE_CHILD_PERCENTAGES
TRUSTED_VERIFICATION_TARGET_HEAD
VERIFIED_SUBJECT_HEAD
PREMERGE_CANDIDATE_NOT_CLOSEOUT
FINAL_PR_HEAD_CI_REVIEW_REQUIRED
NORMAL_PROTECTED_MERGE
MERGED_MAIN_POSTMERGE_READBACK
POSTMERGE_READBACK_REQUIRED
POSTMERGE_CLOSEOUT
RECEIPT_ONLY_TAIL_COMMIT
NO_HTML_DASHBOARD
NO_NEW_PAID_PM_TOOL
NO_FLEET_WIDE_EMPTY_ARTIFACT_ROLLOUT
```

## 1. 카드 메타데이터

```yaml
work_item_id:
work_item_type: GOAL_SLICE | INDEPENDENT_TASK
parent_issue_ref:
required_child_work_item_refs: []
project:
goal_or_slice:
title:
category: PLANNING | SYSTEM_DATA | CODE | UI_UX | VISUAL | AUDIO_VFX | BUG | QA | CANON_DOCS | RELEASE
status: BACKLOG | READY | IN_PROGRESS | VERIFY_REVIEW | BLOCKED_UNVERIFIED | USER_DECISION_REQUIRED | DEFERRED | DONE
priority: P0 | P1 | P2 | P3

player_or_user_value:
why_now:
depends_on: []
blocked_by: []

scope: []
out_of_scope: []
protected_scope: []

canon_owner:
actual_consumers: []
source_main_sha:
task_branch_or_pr:

acceptance_criteria: []
required_evidence: []
evidence_ceiling:

progress:
  progress_basis: CHECKLIST_PASS | REQUIRED_CHILD_WORK_ITEM_DONE
  completed_items:
  applicable_items:
  display:
blocker:
next_action:
resume_condition:
last_updated:
```

## 2. Context and authority

- 현재 사용자 지시:
- 현재 Goal·Playable Slice:
- project `AGENTS.md`·Active Context:
- 책임 원본 `canon_owner`:
- 실제 구현·소비처:
- 기준 branch·SHA:
- 같은 Goal의 기존 Issue·PR 검색 결과:
- 이 카드는 위 정본의 **derived operational view**이며 새로운 사실 정본이 아니다.

## 3. Scope and protected behavior

### 포함 범위

- `<포함 항목>`

### 제외 범위

- `<제외 항목>`

### 보호할 의미·동작·경로

- `<보호 항목>`

## 4. Dependencies and blocker

| 구분 | 참조 | 상태 | 영향 | 해제·재개 조건 |
|---|---|---|---|---|
| 선행 작업 |  |  |  |  |
| 공유 자원 |  |  |  |  |
| 차단 항목 |  |  |  |  |
| 사용자 결정 |  |  |  |  |

## 5. Acceptance criteria

완료 기준은 `조건 → 행동 → 관찰 가능한 결과 → 증거`로 작성한다.

- [ ] AC-01 — `<조건 → 행동 → 결과 → 증거>`
- [ ] AC-02 — `<조건 → 행동 → 결과 → 증거>`

## 6. Evidence-backed checklist

`[x]`는 요구 조건과 증거가 확인된 `PASS`에만 사용한다. 상태를 수동으로 바꾸는 것만으로 완료되지 않는다.

- [x] PASS — 완료 항목. evidence: `<command, URL, repository path, capture, run ID, SHA>`
- [ ] IN_PROGRESS — 현재 수행 중인 항목. owner: `<owner>`
- [ ] READY — 선행 조건을 충족한 다음 항목.
- [ ] BLOCKED_UNVERIFIED — blocker: `<missing source, executor, permission, or evidence>`
- [ ] USER_DECISION_REQUIRED — decision: `<meaning-, scope-, cost-, permission-, or release-changing choice>`
- [ ] DEFERRED — resume_condition: `<observable condition>`
- [ ] FAIL — evidence: `<reproduced failure and affected acceptance>`
- [ ] NOT_APPLICABLE — reason: `<why this item does not apply>`

### 진행률 계산

독립 작업 카드는 카드 내부 적용 항목을 사용한다.

```text
applicable_items = all checklist items - NOT_APPLICABLE items
completed_items = PASS items only
progress = completed_items / applicable_items
```

부모 Goal·Playable Slice 카드는 세부 체크 수가 아니라 **현재 Goal 완료에 필수인 자식 work item**을 사용한다.

```text
applicable_items = required child work items in current approved Goal
completed_items = required child work items whose status is DONE
progress = completed_items / applicable_items
```

- 자식 카드의 서로 다른 퍼센트를 평균내지 않는다. 각 자식의 규모·위험·증거 수준이 다르므로 평균은 전체 완료를 왜곡한다.
- future scope, 선택적 polish, 명시적으로 현재 Goal에서 제외된 자식은 분모에 넣지 않는다.
- `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`, `VERIFY_REVIEW`인 필수 자식은 분모에 남고 완료 수에는 포함하지 않는다.
- 독립 작업의 `READY`, `IN_PROGRESS`, `VERIFY_REVIEW`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`, `FAIL`도 완료 수에 포함하지 않는다.
- 적용 가능한 항목이 0개이면 `0/0`, `100%` 또는 `DONE`이 아니라 `NO_APPLICABLE_CHECKLIST`로 표시한다.
- 진행률은 상태 요약일 뿐 Acceptance Criteria와 증거를 대체하지 않는다.

## 7. Verification matrix

전체 검증 절차는 `templates/project-operations/DEVELOPMENT_GATES.md`를 따른다. 이 표는 현재 카드에 필요한 증거와 실제 결과만 연결한다.

| Evidence | 요구 여부 | 상태 | 방법·명령 | exact 대상 | 증거 | 미검증·실패 영향 |
|---|---:|---|---|---|---|---|
| `E0_CONTRACT` 기획·승인 계약 |  | NOT_RUN |  |  |  |  |
| `E1_STATIC` 포맷·문법·정적 검사 |  | NOT_RUN |  |  |  |  |
| `E2_TEST` 자동 테스트 |  | NOT_RUN |  |  |  |  |
| `E3_RUNTIME` 실제 실행 |  | NOT_RUN |  |  |  |  |
| `E4_VISUAL` 실제 화면·렌더 |  | NOT_RUN |  |  |  |  |
| `E5_PLAY` 기계·담당자 플레이 경로 |  | NOT_RUN |  |  |  |  |
| `E6_HUMAN_PLAYTEST` 사용자·플레이어 검수 |  | NOT_RUN |  |  |  |  |

허용 상태:

```text
PASS | FAIL | PARTIAL | NOT_RUN | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

자동 테스트 PASS는 runtime·화면·UX·Human/Player·사용자 승인·출시 PASS를 의미하지 않는다.

## 8. Repository readback

- 변경된 responsibility owner:
- 실제 diff와 승인 범위 대조:
- data·schema·ID·path consumer 확인:
- test·runtime·capture evidence:
- Decision·Active Context·handoff 갱신:
- asset manifest·provenance·SHA-256 갱신:
- exact HEAD 또는 merged main SHA:
- 남은 stale reference·drift:

## 9. Completion and next action

```yaml
acceptance_status: PASS | PARTIAL | FAIL | NOT_RUN
required_evidence_status: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED_UNVERIFIED
must_fix_remaining:
blocked_unverified_remaining:
user_decision_required_remaining:
repository_readback: PASS | PARTIAL | NOT_RUN
work_item_status:
next_action:
resume_condition:
rollback:
```

`DONE`은 다음을 모두 만족할 때만 사용한다.

- 모든 필수 Acceptance Criteria가 증거와 함께 PASS다.
- 이 카드에 요구된 Evidence level이 PASS다.
- 열린 `MUST_FIX`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`가 없다.
- repository owner·actual consumer·handoff의 필요한 readback이 끝났다.
- 변경이 있으면 exact diff·HEAD 또는 merged main·rollback이 연결됐다.

그 외에는 실제 상태에 따라 `VERIFY_REVIEW`, `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED` 또는 `DEFERRED`를 유지한다.

## 10. 실행 가능한 PM receipt와 갱신 Gate

`PM_EXECUTION_GATE_REQUIRED` · `PM_CHECKLIST_VISIBLE_AT_START_TRANSITION_CLOSEOUT`

책임 원본은 `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` §14다. `tools/project_work_tracking.py`는 위 카드의 **검증·Markdown 출력 모듈**이며 별도 PM 상태 저장소가 아니다. 기존 project/Base work-contract JSON receipt에 **root `project_work_kanban`**을 추가한다. 실행용 전체 root 형식은 `WORK_PROJECT_START_CANON_CHECKLIST.md` §12.1이다. `benchmark_preflight_receipt`·`context_configuration_hygiene`와 형제 필드로 둔다.

### 최소 데이터 투영

아래는 형식 설명이다. 꺾쇠 placeholder는 실제 값으로 바꾸며 빈 틀은 실행 Gate를 통과하지 않는다. 별도 receipt 파일을 중복 생성하지 말고 프로젝트가 현재 소유한 receipt를 확장한다.

```json
{
  "project_work_kanban": {
    "goal_or_slice_issue_ref": "<current approved Goal issue or repository locator>",
    "source_main_sha": "<40-character fresh-read source SHA>",
    "work_item_refs": ["TASK-01"],
    "active_work_item_ref": "TASK-01",
    "next_action": "<next safe action within approved scope>",
    "work_items": [{
      "work_item_id": "TASK-01",
      "title": "<observable outcome>",
      "status": "IN_PROGRESS",
      "canon_owner": "<existing canonical path>",
      "actual_consumers": ["<actual consumer>"],
      "depends_on": [],
      "acceptance_criteria": ["AC-01"],
      "required_evidence": ["E2_TEST"],
      "checklist": [{"id": "AC-01", "text": "<condition, action, result>", "status": "NOT_RUN"}],
      "verification": [{"level": "E2_TEST", "status": "NOT_RUN", "evidence": []}],
      "next_action": "<first verification or implementation step>"
    }]
  }
}
```

`work_items`는 **현재 승인 Goal의 필수 독립 작업**이다. `work_item_refs`와 ID 집합이 정확히 일치해야 한다. 선택적 미래 기능을 섞거나 미완료 필수 항목을 지워 분모를 줄이지 않는다. 단일 작업도 전체 적용 checklist를 포함한다. 기존 작업이 있으면 ID·Issue·owner를 재사용하고, 독립 Issue가 필요 없는 작은 단계는 해당 카드 안에 둔다.

`acceptance_criteria`는 checklist의 필수 ID 목록이다. 문장·조건은 해당 checklist의 `text`에 기록한다. 모든 PASS에는 실제 `evidence` locator 목록을 둔다. PASS가 아니어도 evidence가 있으면 text 목록이어야 한다. 선택적 N/A에는 `reason`이 필요하고 필수 AC·필수 evidence는 N/A로 면제할 수 없다. `required_evidence`는 실제 승인 계약에서 선택하며, UI 작업에서 테스트만 넣어 runtime·화면 요구를 지우지 않는다. 모듈은 승인 원문의 완전성이나 증거 진실성을 대신 판단하지 않는다.

DONE 추가 필드: `verified_head_sha`(실제 검증한 40자 HEAD), `repository_readback: PASS`, 비어 있지 않은 `readback_evidence`, `rollback`, 정수 `must_fix_remaining: 0`, `blocked_unverified_remaining: 0`, `user_decision_required_remaining: 0`. 해당 작업의 적용 checklist와 필수 evidence 모두 PASS여야 하며 다른 verification에도 FAIL·BLOCKED_UNVERIFIED가 남아 있으면 DONE과 모순된다. evidence가 외부 Artifact라면 만료 전에 방법·결과·exact 대상·장기 보존 근거를 기존 Issue/PR에 남긴다.

### 실행·재개·마감

```text
project AGENTS / approved owner / actual implementation fresh-read
→ existing Goal issue + required remaining work reconciliation
→ 같은 repository receipt에 현재 ID·scope·evidence·next action 갱신
→ adapter가 승인한 exact Base checkout 확인
→ validate_work_contract_receipt.py --receipt <receipt> --phase start --expected-source-sha <fresh-read-source-sha> --render-markdown
→ 사용자에게 전체 적용 작업 목록·현재 항목·완료/필수 수·차단·다음 행동 표시
→ 한 작업 수행·검증·owner readback
→ 같은 receipt와 기존 Issue/card 갱신
→ 다음 승인 작업을 먼저 선택해 IN_PROGRESS와 active_work_item_ref에 기록
→ 그 작업을 실행하기 전 --phase resume으로 재검사
→ branch에서 검증 가능한 구현·정본·consumer 작업 완료
→ PREMERGE_CANDIDATE_NOT_CLOSEOUT
→ 필요 시 receipt/status metadata만 기록하는 RECEIPT_ONLY_TAIL_COMMIT
→ FINAL_PR_HEAD_CI_REVIEW_REQUIRED
→ NORMAL_PROTECTED_MERGE
→ NORMAL_MERGE_AND_POSTMERGE_READBACK
→ MERGED_MAIN_POSTMERGE_READBACK
→ POSTMERGE_READBACK_REQUIRED
→ 같은 승인 Goal의 merge·postmerge 필수 항목과 모든 evidence를 merged main에서 재검증
→ POSTMERGE_CLOSEOUT_REQUIRED_WHEN_IN_DENOMINATOR
→ POSTMERGE_CLOSEOUT
→ validate_work_contract_receipt.py --receipt <receipt> --phase closeout --expected-source-sha <fresh-read-source-sha> --expected-head-sha <fresh-read-merged-main-sha> --render-markdown
```

`PREMERGE_CANDIDATE_NOT_CLOSEOUT`: branch에서 구현·테스트·정본 readback이 끝났더라도 병합·postmerge가 승인 범위의 필수 항목이면 integration work item은 `VERIFY_REVIEW`로 남기고 최종 `DONE`이나 closeout을 주장하지 않는다. exact PR HEAD의 required checks, 독립 검토와 unresolved thread 0을 확인한 뒤에만 정상 보호 병합한다.

`TRUSTED_VERIFICATION_TARGET_HEAD` · `VERIFIED_SUBJECT_HEAD`: final closeout의 `--expected-head-sha`는 receipt 내부 값이 아니라 신뢰한 caller가 별도로 fresh-read한 **merged main 검증 대상 HEAD**다. 이 HEAD에는 현재 승인 범위의 모든 제품·정본·consumer·검증 evidence 영향 변경과 required merge 결과가 실제로 들어 있어야 한다. receipt 안의 `verified_head_sha`를 기대값으로 다시 복사하면 자기주장 확인에 불과하므로 허용하지 않는다. 모든 필수 DONE 작업의 evidence와 readback은 이 동일한 `VERIFIED_SUBJECT_HEAD`를 대상으로 재확인한다.

`POSTMERGE_READBACK_REQUIRED`: merge commit 또는 squash commit, merged `main`의 exact SHA, changed-path/owner/consumer readback, required check 결과, rollback을 기존 Goal Issue·PR·repository receipt projection에 기록한다. merge·postmerge가 필수 작업이면 closeout 전에 DONE으로 표시하지 않는다. repository 파일에 final receipt metadata를 남겨야 하면 제품·정본·consumer를 바꾸지 않는 bounded receipt-only follow-up을 사용하며, 그 metadata 변경을 이전 제품 검증의 대체 증거로 취급하지 않는다.

`RECEIPT_ONLY_TAIL_COMMIT`: premerge receipt는 자신의 최종 commit SHA를 미리 기록할 수 없으므로 **receipt·상태 metadata만** 기록하는 tail commit을 허용한다. 이 tail은 제품·정본·consumer·검증 evidence를 바꾸지 않아야 한다. 그런 영향 변경이 하나라도 생기면 새 HEAD에서 evidence와 premerge 검토를 다시 실행한다. `FINAL_PR_HEAD_CI_REVIEW_REQUIRED`: receipt-only tail을 포함한 최종 PR HEAD는 exact-head CI·독립 review·changed-path readback을 통과해야 하며 예상하지 않은 tail 경로가 있으면 premerge candidate를 주장하지 않는다. start/resume은 역사적으로 완료된 작업의 이전 HEAD 기록을 보존한다.

기존 CLI의 기본 phase가 `start`이므로 PM을 활성화하는 opt-in flag가 없다. L1+에서 trusted expected source 누락, PM 필드 누락, 잘못된 진행률, 미완료 dependency, WIP 초과, evidence 없는 PASS/DONE은 nonzero exit다. `BLOCKED_UNVERIFIED` benchmark는 올바른 실패 기록일 수 있지만 실행 허가는 아니다. `validate_receipt()` Python API는 **과거 구조 검사 호환용**이고 실행 승인에 사용하지 않는다. 실행 consumer는 CLI 또는 `validate_execution_receipt()`를 쓴다.

오래된 receipt에 PM 필드가 없으면 `PM_RECONCILIATION_REQUIRED`로 현재 승인 작업을 복원하고 receipt bookkeeping만 교정한 뒤 재실행한다. 이 교정은 새로운 제품 기능을 시작하는 권한이 아니다. 완전히 차단된 상태도 Issue와 receipt에 보존한다. `--render-markdown`은 형식이 유효한 차단 목록·진행 수·실제 blocker·재개 조건을 `INFORMATION ONLY; EXECUTION BLOCKED`로 표시하지만 nonzero exit를 유지한다. failed Gate에서는 receipt의 task/board `next_action`을 실행 지시로 재출력하지 않는다. 독립 작업이 준비됐으면 그 작업을 active로 먼저 선택한 뒤 재검사한다.

시작/재개에서는 `active_work_item_ref`가 `IN_PROGRESS` 또는 `VERIFY_REVIEW` 작업 하나를 가리켜야 하며, renderer는 선택된 항목만 `ACTIVE`로 표시한다. 각 상태의 WIP는 최대 1개다. 프로젝트의 명시적 다른 WIP 계약은 별도 adapter 변경·검증 없이 이 기본 모듈에 조용히 주입하지 않는다. 현재 모듈로 표현되지 않는 project exception은 `BLOCKED_UNVERIFIED`로 기록하고 기존 승인 계약에 맞춰 bounded adaptation한다. `--expected-head-sha`는 closeout 판정에만 사용하며 start/resume 화면에서 과거 DONE 항목을 stale로 재분류하지 않는다.

최종 마감은 모든 필수 작업 DONE, active null, `next_action: STOP_APPROVED_SCOPE_COMPLETE`이며 merged-main postmerge 증거가 확인된 뒤에만 가능하다. 승인 범위가 끝났으면 종료하며 다음 Goal을 자동 발명하지 않는다. 완료 항목의 오래된 next_action은 renderer가 지시문으로 출력하지 않는다. 중단 시 `finished / remaining / blocker / resume_condition / why`를 보존하고 같은 지시를 지우지 말고 완료 표시와 근거를 남긴다.

`--render-markdown`은 파생 text-native 출력이다. 별도 HTML·보드·PM 앱을 설치하지 않으며 입력의 URL·명령·HTML을 실행하지 않는다. terminal control·bidi control은 유효한 text로 받지 않는다. `--expected-source-sha`는 L1+에서 필수이며 신뢰한 caller가 fresh-read한 값을 전달한다. 모듈 자체가 GitHub 최신성을 조회하지 않으므로 receipt 자신의 SHA를 기대값으로 복사하거나 형식 검사만으로 freshness를 주장하지 않는다. `progress_summary.display`가 있으면 자동 계산된 완료/필수 수와 일치해야 한다. 기존 project pin은 정상 adoption PR로 검증하기 전까지 유지하고, Base 병합을 모든 프로젝트 설치 완료로 보고하지 않는다.

## 11. 새 세션용 여섯 절 인계 — 기존 정본 재사용

새 파일 `DESIGN.md / STATUS.md / INBOX.md`를 일괄 만들지 않는다. 아래 여섯 절은 기존 handoff의 작은 실행 요약으로 사용하고 분야별 사실은 기존 owner를 가리킨다.

1. **합격 기준:** 한 문장 목표와 관찰 가능한 AC ID·필수 evidence. 목표 문장만으로 완료 판정하지 않는다.
2. **먼저 읽기:** project AGENTS·Active Context·승인 Decision·실제 consumer·현재 PM receipt의 exact revision과 필요한 section/읽기 범위. 범위 밖의 숨은 의존성이 발견되면 필요한 만큼 확장한다.
3. **규칙과 이유:** 기존 Method의 authority·reason·source·adjustment condition·validation을 사용한다. 문구 금지만 늘리지 않는다.
4. **한 바퀴:** fresh-read → 승인된 의미 있는 작업 하나 → 정적/자동 검사 → 필요 시 격리 checkpoint → 실제 runtime/화면/입력 확인 → 교정 → 정본·PM 상태·증거 갱신 → 다음 승인 작업 또는 정상 종료.
5. **커밋 순서:** 복구용 checkpoint는 `IN_PROGRESS / VERIFY_REVIEW`로 남길 수 있으나 DONE·품질 승인·병합을 뜻하지 않는다. checkpoint에 미완료와 다음 검증을 기록한다. 저장된 미커밋 파일이 세션 종료만으로 삭제된다고 주장하지 않는다. 사용자 변경·다른 workstream은 staging하지 않으며 main 직접 push하지 않는다. 완료용 commit과 exact-head PR 검토는 별도 Gate다.
6. **QA와 학습:** 실제 화면·상태·consumer·exact build를 캡처하고 이미지를 직접 읽는다. 캡처 생성과 시각 합격을 분리한다. 같은 지적의 원인을 재현한 뒤 프로젝트 전용/공용을 분류하고 가능한 검사를 만든다. 반복 횟수만으로 Base 강제 규칙을 자동 승격하지 않는다.

`FRESH_SESSION_HANDOFF_NOT_NEW_LOOP` · `CHECKPOINT_IS_NOT_COMPLETION`

각 실행의 기록·예산·중단·복구는 기존 continuous-work/Loop owner를 재사용한다. 제품별 CLI 옵션을 이름만 바꿔 이식하지 않는다. `codex exec` 새 실행과 `--ephemeral`의 세션 파일 비보존은 다른 개념이며, 새 실행에서도 필요한 evidence는 별도 보존한다. Claude의 `--max-turns`를 Codex 옵션으로 가정하지 않는다. 구독 경로 실패를 유료 API로 우회하거나 OS 서비스·스케줄러를 이 문서만으로 활성화하지 않는다.

원출처 비교: 사용자가 제공한 `kIUhkiAecM8` 댓글 텍스트(영상 전체 시청 증거 아님), OpenAI non-interactive Codex 문서 `https://developers.openai.com/codex/noninteractive`, GitHub sub-issue 문서 `https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues`. 새 세션·파일 기억·작은 작업은 ADAPT, 무한 개발·새 정본·자동 정책 승격은 REJECT다. 재사용 교훈은 **문구 존재 검사와 실제 실행 Gate 검사를 반드시 구분한다**는 것이다. 이 개선의 검증 owner는 `tests/test_project_work_tracking.py`이고 실제 현재 작업 적용 기록은 Base Issue #825에 둔다.
