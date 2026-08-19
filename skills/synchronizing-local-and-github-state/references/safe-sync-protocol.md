# 안전한 Git 동기화 프로토콜

이 프로토콜은 Git 상태뿐 아니라 동시에 진행 중인 Branch·PR·Task의 **현재 활성 소유권**을 first persistent write 전에 판정한다. `CONCURRENT_CHANGE_PREFLIGHT`는 협업자가 지키는 **cooperative** 계약이며 GitHub의 강제 mutex나 외부 lock service를 대신하지 않는다.

Base의 기본 충돌 복구 방식은 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`에 따른 **latest-main copy integration**이지만 실제 활성 owner 보호보다 우선하지 않는다.

```text
OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM
CURRENT_OWNER_EVIDENCE_REQUIRED
ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED_WHEN_ACTUALLY_ACTIVE
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_ACTIVE_OTHER_WORKER_EXCEPTION
```

같은 Goal·path·semantic resource가 겹쳐도 open/draft/ready 상태만으로 active owner를 추정하지 않는다. `ACTIVE_OTHER_WORKER` evidence가 있으면 takeover 승인 전 owner Branch·path·PR을 수정하거나 material delta를 가져오지 않는다. `NO_ACTIVE_OWNER_EVIDENCE` backlog는 current coordinator가 latest main에서 takeover/finish/supersession 여부를 판정할 수 있다.

## 1. 기준과 작업 의도 고정

작업 시작 시 최소 다음을 기록한다.

```yaml
repository:
execution_surface: LOCAL_WORKTREE | GITHUB_CONNECTOR_ONLY | HYBRID
current_task_or_pr_identity:
current_workstream_identity:
owner_workstream_identity:
owner_activity_classification: CURRENT_COORDINATOR | ACTIVE_OTHER_WORKER | NO_ACTIVE_OWNER_EVIDENCE | UNKNOWN_OWNER_ACTIVITY
current_owner_evidence: []
cross_workstream_absorption_authorized: false | true
source_main_sha:
current_main_sha:
current_branch:
current_worktree: <actual path> | NOT_APPLICABLE_CONNECTOR_ONLY
write_parent_sha: PENDING_FIRST_WRITE
expected_head_sha:
intended_paths: []
semantic_resource_locks: []
protected_paths: []
```

- `execution_surface`: 이번 동기화에서 실제로 관찰·수정 가능한 표면. 관찰하지 않은 local/remote 상태를 다른 표면의 증거로 추정하지 않는다.
- `LOCAL_WORKTREE`: 실제 local branch/worktree/dirty state를 읽는다.
- `GITHUB_CONNECTOR_ONLY`: connector의 remote branch/head/diff/PR/check만 증거로 사용한다. local worktree가 관찰되지 않았으면 `current_worktree: NOT_APPLICABLE_CONNECTOR_ONLY`로 기록하고 local test/dirty-state를 추정하지 않는다.
- `HYBRID`: local과 connector 증거의 출처를 각각 구분한다.
- `OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`: open/draft/ready 상태는 owner evidence가 아니다. 실제 current owner evidence가 없고 사용자가 현재 coordinator만 활성이라고 확인했으면 열린 PR을 backlog로 분류해 최신 main에서 takeover/finish/supersession할 수 있다.
- `source_main_sha`: 작업 계약/Branch를 시작할 때 기준이 된 completed main SHA.
- `current_main_sha`: 현재 remote authority를 다시 읽은 SHA.
- `write_parent_sha`: 실제 first persistent write 직전 Branch parent. 아직 쓰지 않았으면 `PENDING_FIRST_WRITE`.
- `expected_head_sha`: 검증·PR·merge에서 기대하는 정확한 head SHA.
- `semantic_resource_locks`: 파일 경로가 달라도 같은 Registry entry, schema, policy decision, tool route처럼 동시에 수정하면 의미가 충돌하는 자원.
- `current_workstream_identity`: 현재 채팅/작업 계약/PR이 소유한 독립 작업 흐름.
- `owner_workstream_identity`: 겹치는 Branch/PR/Task의 목적/계보. 존재만으로 current owner를 의미하지 않는다.
- `owner_activity_classification`: current owner evidence를 바탕으로 `CURRENT_COORDINATOR / ACTIVE_OTHER_WORKER / NO_ACTIVE_OWNER_EVIDENCE / UNKNOWN_OWNER_ACTIVITY`를 기록한다.
- `current_owner_evidence`: 사용자 지시, current session/automation owner, Resource Lock, matching running execution 등 현재 활동 주체를 직접 뒷받침하는 locator.
- `cross_workstream_absorption_authorized`: 실제 `ACTIVE_OTHER_WORKER`를 현재 작업에 takeover/흡수하도록 사용자가 명시 승인했는지 여부.

값을 모르면 추측하지 않는다.

## 2. Workstream identity gate

path/semantic overlap보다 먼저 **현재 active owner evidence**를 확인한다.

1. 같은 채팅/같은 승인 contract/현재 coordinator 소유권이 확인되면 `CURRENT_COORDINATOR`다.
2. open/draft/ready PR·Branch·과거 다른 채팅 기록은 owner identity metadata일 수 있지만 current owner evidence 자체는 아니다.
3. 사용자 지시, current session/automation owner, Resource Lock, matching running execution을 `current_owner_evidence`로 수집한다.
4. 실제 다른 작업자가 현재 활동 중이면 `ACTIVE_OTHER_WORKER`; takeover 승인 전 read-only 상태 확인만 허용하고 `WAITING_RESOURCE`로 둔다.
5. current owner evidence가 없으면 `NO_ACTIVE_OWNER_EVIDENCE`; latest completed main과 Goal을 재검증해 `COORDINATOR_TAKEOVER / READY_TO_FINISH / SUPERSEDED_DUPLICATE / STALE_BACKLOG / BLOCKED_EXTERNAL`로 재분류한다.
6. owner activity 자체를 판정할 근거가 부족하면 `UNKNOWN_OWNER_ACTIVITY`이고 `BLOCKED_UNVERIFIED`다.
7. 사용자가 실제 `ACTIVE_OTHER_WORKER`의 takeover/통합을 명시 승인하면 `cross_workstream_absorption_authorized=true`를 기록하고 승인 범위 안에서만 `PROVISIONAL_INTEGRATION`을 사용한다.

`same goal`만으로 `same workstream`이나 active owner를 추정하지 않는다. 반대로 `different workstream`이라는 역사적 계보만으로 현재 activity를 추정하지도 않는다.

## 3. CONCURRENT_CHANGE_PREFLIGHT

다음 시점마다 동일한 preflight를 다시 실행한다.

- first persistent write
- PR creation
- merge
- post-merge main readback

현재 task/PR 자신은 overlap 목록에서 **exclude the current task or PR itself** 한다.

확인 항목:

```text
execution_surface
current_task_or_pr_identity
current_workstream_identity
owner_workstream_identity
owner_activity_classification
current_owner_evidence
cross_workstream_absorption_authorized
source_main_sha
current_main_sha
write_parent_sha
expected_head_sha
intended_paths
semantic_resource_locks
same_goal_open_and_recent_prs
open_pr_changed_paths
```

### Overlap classes

- `PATH_OVERLAP`: 같은 path 또는 부모/자식 이동·rename 관계.
- `SEMANTIC_OVERLAP`: 다른 path라도 같은 schema, Registry row, policy decision, route identity, canonical question을 수정.
- `SAME_GOAL`: 같은 사용자 Goal의 구현/후속 변경.
- `UNKNOWN`: owner/목적/changed path를 검증할 수 없음.

owner activity Gate는 위 overlap보다 먼저 적용한다. `SAME_GOAL`이어도 실제 `ACTIVE_OTHER_WORKER`이면 takeover 승인 없이는 흡수하지 않는다. 반대로 `different workstream` history만으로 `ACTIVE_OTHER_WORKER`를 추정하지 않는다.

### Preflight outcomes

| 상태 | 의미 | 다음 행동 |
|---|---|---|
| `CLEAR` | 경쟁 active owner가 없고 현재 execution surface에서 base/head가 최신 | write 가능 |
| `STALE_BASE_SHA` | 기준 SHA가 current authority와 다름 | latest main에서 재기준화 |
| `WAITING_RESOURCE` | 실제 `ACTIVE_OTHER_WORKER` 또는 Resource Lock이 자원을 소유하고 takeover 권한이 없음 | owner surface를 건드리지 않고 해당 task만 보류 |
| `DUPLICATE_WORK` | 같은 material delta가 실제 active owner에서 구현 중이거나 completed main에서 이미 충족됨 | 중복 구현 금지; active/completed 상태 확인 |
| `BLOCKED_UNVERIFIED` | owner activity/workstream/SHA/권한 또는 필요한 surface 증거를 검증 불가 | 증거 확보 전 write 금지 |
| `PROVISIONAL_INTEGRATION` | same workstream, `NO_ACTIVE_OWNER_EVIDENCE` takeover, 또는 승인된 `ACTIVE_OTHER_WORKER` delta를 별도 latest-main Branch에서 통합 | selective copy + semantic reconciliation |

## 4. Cooperative ownership

동시 작업 격리는 강제 lock이 아니라 cooperative ownership이다.

- 실제 `ACTIVE_OTHER_WORKER` Branch/worktree의 dirty state를 clean/rebase/reset하지 않는다.
- open/draft/ready PR 상태만으로 보호를 발동하지 않는다. actual current owner evidence가 있는 Branch·path·PR만 active mutation-protected다.
- overlap과 owner activity 확인을 위해 read-only diff/head/path/status 조회는 가능하다.
- `ACTIVE_OTHER_WORKER` owner Branch에 직접 commit하지 않는다.
- `ACTIVE_OTHER_WORKER`는 사용자 takeover 승인 전 selective copy도 하지 않는다.
- `CURRENT_COORDINATOR` / `NO_ACTIVE_OWNER_EVIDENCE` takeover 통합은 latest completed main의 별도 Branch에서 수행한다.
- 같은 파일을 피했더라도 같은 semantic resource면 owner 충돌로 처리한다.
- process/port/temp directory도 실제 소유권 evidence가 있으면 임의 종료·재사용하지 않는다.
- `GITHUB_CONNECTOR_ONLY`에서 local process/worktree/dirty state가 없다고 단정하지 않는다. 그 상태는 `NOT_APPLICABLE_CONNECTOR_ONLY` 또는 `NOT_RUN`이다.

## 5. BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16

### 5.1 Authorization boundary

standing authorization은 latest completed main에서 충돌을 통합하기 위한 기술적 권한이며, 실제 활성 다른 작업자의 takeover 권한을 대신하지 않는다.

```text
OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM
CURRENT_OWNER_EVIDENCE_REQUIRED
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_ACTIVE_OTHER_WORKER_EXCEPTION
```

- `CURRENT_COORDINATOR` / same workstream: standing authorization을 사용할 수 있다.
- `NO_ACTIVE_OWNER_EVIDENCE`: current approval 범위의 `COORDINATOR_TAKEOVER / READY_TO_FINISH / SUPERSEDED_DUPLICATE`는 standing authorization으로 latest-main 통합을 진행할 수 있다.
- `ACTIVE_OTHER_WORKER`: standing authorization이 takeover 승인을 대신하지 않는다. 사용자가 현재 작업에서 명시적으로 takeover/통합 승인해야 한다.
- `UNKNOWN_OWNER_ACTIVITY`: owner activity evidence가 확인될 때까지 `BLOCKED_UNVERIFIED`다.

### 5.2 Read-only owner snapshot

통합 전 실제 active owner PR branches를 수정하지 않고 기록한다.

```yaml
execution_surface:
owner_pr_head_shas: []
current_workstream_identity:
owner_workstream_identity:
owner_activity_classification:
current_owner_evidence: []
cross_workstream_absorption_authorized:
provisional_overlap_paths: []
provisional_semantic_resources: []
```

최소 확인:

- exact owner/backlog PR head SHA
- owner changed paths
- source/base SHA
- latest main SHA
- successor/duplicate PR 존재 여부
- semantic ownership
- workstream identity
- current owner evidence
- 실제 active other worker이면 현재 user takeover authorization 여부

### 5.3 Create a separate PROVISIONAL_INTEGRATION branch

```text
latest completed main
→ separate PROVISIONAL_INTEGRATION branch
→ no active-owner branch write
```

whole stale branch merge를 기본으로 하지 않는다.

### 5.4 Selective copy

`selective copy`는 owner의 모든 commit을 가져오는 것이 아니다.

가져올 후보:

- 아직 main에 없는 실제 material behavior
- 현재 Goal의 acceptance criterion을 충족하는 test/contract
- 현재 main의 successor와 충돌하지 않는 doc/registry delta

가져오지 않을 후보:

- successor merge로 이미 main에 흡수됨
- old base에만 맞는 stale code
- 현재 owner/canon을 약화하는 duplicate authority
- 실제 `ACTIVE_OTHER_WORKER`에서 takeover 승인되지 않은 변경
- unrelated dependency/product work

### 5.5 Semantic reconciliation

bytes 동일성보다 현재 의미를 비교한다.

```text
owner intent
+ current owner evidence
+ owner tests
+ latest main implementation
+ successor merges
+ current canon
+ takeover authorization when actually needed
→ semantic reconciliation
```

판정:

- `ABSORB_MATERIAL_DELTA`
- `ALREADY_ABSORBED_BY_SUCCESSOR`
- `REJECT_DUPLICATE_AUTHORITY`
- `PRESERVE_RESIDUAL_OWNER`
- `COORDINATOR_TAKEOVER`
- `READY_TO_FINISH`
- `SUPERSEDED_DUPLICATE`
- `STALE_BACKLOG`
- `BLOCKED_EXTERNAL`
- `WAITING_RESOURCE`
- `BLOCKED_UNVERIFIED`

### 5.6 Verification and accounting

```yaml
absorbed_owner_deltas: []
residual_owner_deltas: []
rejected_duplicate_authority: []
```

`residual_owner_deltas`가 0이어야 해당 owner/backlog가 이 Goal에서 완전히 superseded되었다고 볼 수 있다. 그러나 실제 `ACTIVE_OTHER_WORKER` PR의 close/supersede는 사용자의 takeover 승인 범위 안에서만 수행한다. `NO_ACTIVE_OWNER_EVIDENCE` backlog는 current coordinator가 승인된 Goal 안에서 supersession을 마무리할 수 있다.

## 6. Write-time preflight

first persistent write 직전:

1. current main을 다시 읽는다.
2. `execution_surface`와 실제 관찰 가능한 증거를 다시 확인한다.
3. current/owner workstream identity와 owner activity evidence를 다시 확인한다.
4. current task Branch/head를 다시 읽는다.
5. same-goal open/recent PR을 다시 읽는다.
6. current task or PR itself를 overlap 후보에서 제외한다.
7. intended path + semantic resource overlap을 판정한다.
8. `CLEAR` 또는 승인된 `PROVISIONAL_INTEGRATION`일 때만 write한다.

GitHub contents API는 stale blob SHA를 거부할 수 있다. 409는 blind retry 신호가 아니다.

```text
HTTP 409 / stale blob
→ read exact current file/blob SHA
→ compare intended delta
→ preserve newly-arrived content
→ apply only missing delta
→ regression test
```

## 7. PR creation preflight

PR creation 직전:

- execution surface 재확인
- current main/base SHA 재확인
- actual branch head 확인
- changed paths/semantic resources 확인
- current/owner workstream + owner activity 재확인
- same-goal PR/new successor 확인
- owner residual accounting 확인
- tests/evidence ceiling 확인

새로운 overlap이나 active-owner evidence가 생기면 PR을 만들기 전에 다시 reconcile한다.

## 8. Merge preflight

merge 직전:

```text
execution_surface evidence is explicit
expected_head_sha == actual PR head sha
current main/base acceptable
owner_activity_classification is current
ACTIVE_OTHER_WORKER takeover authorization is valid when required
required checks == PASS
unresolved threads == 0
required approvals satisfied
P0/P1 == 0
residual owner deltas accounted
NOT_RUN / BLOCKED_* / CANCELLED not promoted to PASS
```

PR metadata나 과거 성공 run만 보고 merge하지 않는다. exact head의 상태를 읽는다.

실제 `ACTIVE_OTHER_WORKER` PR을 close/supersede하는 것도 merge와 별개의 mutation이며 current takeover 승인 범위가 필요하다.

## 9. Post-merge main readback

병합 뒤:

1. 새 `main` SHA를 읽는다.
2. merge PR의 실제 merged state와 merge SHA를 읽는다.
3. changed canon/registry/policy/runtime file을 main에서 다시 읽는다.
4. same-goal open/recent PR을 다시 조회하고 current owner evidence도 갱신한다.
5. authorized active-owner 또는 takeover backlog의 `absorbed_owner_deltas / residual_owner_deltas`를 다시 확인한다.
6. current operational machine checkpoint가 있으면 읽는다.
7. generated/derived surface가 stale인지 확인한다.
8. postmerge workflow가 있으면 evidence ceiling을 확인한다.
9. connector-only 실행이면 local post-merge state를 성공으로 추정하지 않는다.

병합 자체는 완료 증거가 아니다.

## 10. Failure recovery

### Missing `gh` / push auth

연결된 GitHub connector가 같은 mutation/read 기능을 제공하면 connector를 우선 사용한다. 사용자가 반복 인증해야 하는 수동 CLI 경로로 회귀하지 않는다. local worktree가 실제로 관찰되지 않으면 `execution_surface: GITHUB_CONNECTOR_ONLY`, `current_worktree: NOT_APPLICABLE_CONNECTOR_ONLY`로 기록한다.

### Local clone/network unavailable

GitHub connector + repository CI가 acceptance criterion을 권위 있게 증명할 수 있는지 확인한다. 가능하면 `GITHUB_CONNECTOR_ONLY`로 전환하고 local run은 `NOT_RUN`으로 남긴다. repository-native CI가 증명하지 않는 local-only acceptance를 자동 PASS로 만들지 않는다.

### Workflow cancellation

`cancelled`는 PASS가 아니다.

1. 동일 exact head의 더 최신 run 검색
2. superseding run이 있으면 최신 run 사용
3. 없으면 cancelled/failed jobs를 same exact head에서 rerun
4. rerun 동안 불필요한 PR/head mutation 금지
5. final required gate까지 확인

### Main moved

merge 전 main이 이동하면:

```text
new main readback
→ changed-base semantic reconciliation
→ required tests rerun if affected
→ exact-head/base merge gate
```

자동 force update/rebase로 덮지 않는다.

## 11. Report contract

```md
## CONCURRENT_CHANGE_PREFLIGHT
- execution_surface: LOCAL_WORKTREE | GITHUB_CONNECTOR_ONLY | HYBRID
- current_task_or_pr_identity:
- current_workstream_identity:
- owner_workstream_identity:
- owner_activity_classification:
- current_owner_evidence:
- cross_workstream_absorption_authorized:
- source_main_sha:
- current_main_sha:
- current_worktree: <actual path> | NOT_APPLICABLE_CONNECTOR_ONLY
- write_parent_sha:
- expected_head_sha:
- intended_paths:
- semantic_resource_locks:
- same_goal_open_and_recent_prs:
- open_pr_changed_paths:
- result: CLEAR | STALE_BASE_SHA | WAITING_RESOURCE | DUPLICATE_WORK | BLOCKED_UNVERIFIED | PROVISIONAL_INTEGRATION

## Copy integration
- owner_pr_head_shas:
- provisional_overlap_paths:
- provisional_semantic_resources:
- absorbed_owner_deltas:
- residual_owner_deltas:
- rejected_duplicate_authority:

## Verification
- execution-surface evidence:
- exact-head checks:
- unresolved threads:
- required approvals:
- merge SHA:
- post-merge main readback:
- NOT_RUN / BLOCKED / CANCELLED:
```

## 12. 금지

- 존재가 확인되지 않은 local worktree/dirty state/test 결과를 추정
- `GITHUB_CONNECTOR_ONLY`를 local 검증 PASS처럼 표현
- open/draft/ready 상태만으로 다른 작업자를 active owner로 추정
- 실제 `ACTIVE_OTHER_WORKER`를 same-goal이라는 이유만으로 자동 흡수
- active-other-worker takeover authorization 없이 owner Branch/path/PR write/rebase/close/merge/selective-copy
- 실제 active owner PR branches 직접 수정
- dirty sibling worktree clean/reset
- stale blob/head blind overwrite
- whole old branch를 latest main에 무검토 merge
- same-path만 보고 semantic overlap 무시
- current task 자체를 overlap owner로 잘못 집계
- exact-head가 아닌 과거 CI 성공 재사용
- cancelled/blocked/not-run을 PASS로 보고
- residual material delta가 있는데 source PR을 superseded 처리
