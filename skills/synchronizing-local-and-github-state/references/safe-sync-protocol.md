# 안전한 Git 동기화 프로토콜

이 프로토콜은 Git 상태뿐 아니라 동시에 진행 중인 Branch·PR·Task의 소유권을 first persistent write 전에 판정한다. `CONCURRENT_CHANGE_PREFLIGHT`는 협업자가 지키는 **cooperative** 계약이며 GitHub의 강제 mutex나 외부 lock service를 대신하지 않는다.

Base의 기본 충돌 복구 방식은 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`에 따른 **latest-main copy integration**이지만 workstream 격리 Gate보다 우선하지 않는다.

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

같은 Goal·path·semantic resource가 겹치더라도 `different workstream`이면 현재 사용자의 명시적 흡수 승인 전에는 owner Branch·path·PR을 수정하거나 material delta를 가져오지 않는다. `same workstream`일 때만 standing authorization이 기본 통합 경로를 제공한다.

## 1. 기준과 작업 의도 고정

작업 시작 시 최소 다음을 기록한다.

```yaml
repository:
current_task_or_pr_identity:
current_workstream_identity:
owner_workstream_identity:
cross_workstream_absorption_authorized: false | true
source_main_sha:
current_main_sha:
current_branch:
current_worktree:
write_parent_sha: PENDING_FIRST_WRITE
expected_head_sha:
intended_paths: []
semantic_resource_locks: []
protected_paths: []
```

- `source_main_sha`: 작업 계약/Branch를 시작할 때 기준이 된 completed main SHA.
- `current_main_sha`: 현재 remote authority를 다시 읽은 SHA.
- `write_parent_sha`: 실제 first persistent write 직전 Branch parent. 아직 쓰지 않았으면 `PENDING_FIRST_WRITE`.
- `expected_head_sha`: 검증·PR·merge에서 기대하는 정확한 head SHA.
- `semantic_resource_locks`: 파일 경로가 달라도 같은 Registry entry, schema, policy decision, tool route처럼 동시에 수정하면 의미가 충돌하는 자원.
- `current_workstream_identity`: 현재 채팅/작업 계약/PR이 소유한 독립 작업 흐름.
- `owner_workstream_identity`: 겹치는 Branch/PR/Task가 속한 독립 작업 흐름.
- `cross_workstream_absorption_authorized`: 현재 사용자가 이 작업에서 다른 workstream의 변경을 실제 흡수·통합하도록 명시 승인했는지 여부.

값을 모르면 추측하지 않는다.

## 2. Workstream identity gate

path/semantic overlap보다 먼저 workstream 경계를 확인한다.

1. 같은 채팅/같은 승인 contract/같은 integration Goal의 소유권이 확인되면 `same workstream`으로 분류한다.
2. 다른 채팅 또는 별도 승인 contract/독립 PR 흐름이면 `different workstream`으로 분류한다.
3. 식별할 근거가 부족하면 `UNKNOWN_WORKSTREAM`이다.
4. `different workstream` + `cross_workstream_absorption_authorized=false`이면 read-only 상태 확인만 허용하고 `WAITING_RESOURCE`로 둔다.
5. `UNKNOWN_WORKSTREAM`에서 cross-workstream absorption authorization도 없으면 `BLOCKED_UNVERIFIED`다.
6. 사용자가 현재 작업에서 다른 채팅/독립 PR의 흡수·통합을 명시 승인하면 `cross_workstream_absorption_authorized=true`를 기록하고 그 승인 범위 안에서만 `PROVISIONAL_INTEGRATION`을 사용할 수 있다.

`same goal`만으로 `same workstream`을 추정하지 않는다.

## 3. CONCURRENT_CHANGE_PREFLIGHT

다음 시점마다 동일한 preflight를 다시 실행한다.

- first persistent write
- PR creation
- merge
- post-merge main readback

현재 task/PR 자신은 overlap 목록에서 **exclude the current task or PR itself** 한다.

확인 항목:

```text
current_task_or_pr_identity
current_workstream_identity
owner_workstream_identity
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

workstream Gate는 위 overlap보다 먼저 적용한다. `SAME_GOAL`이어도 `different workstream`이면 명시 승인 없이는 흡수하지 않는다.

### Preflight outcomes

| 상태 | 의미 | 다음 행동 |
|---|---|---|
| `CLEAR` | 경쟁 owner가 없고 base/head가 최신 | write 가능 |
| `STALE_BASE_SHA` | 기준 SHA가 current authority와 다름 | latest main에서 재기준화 |
| `WAITING_RESOURCE` | 자원을 다른 task/PR/workstream이 소유 | owner surface를 건드리지 않고 해당 task만 보류 |
| `DUPLICATE_WORK` | 같은 material delta가 이미 다른 owner에서 구현·검증 중 | 중복 구현 금지; workstream auth 확인 |
| `BLOCKED_UNVERIFIED` | owner/workstream/SHA/PR/권한을 검증 불가 | 증거 확보 전 write 금지 |
| `PROVISIONAL_INTEGRATION` | same workstream 또는 명시 승인된 cross-workstream delta를 별도 latest-main Branch에서 통합 | selective copy + semantic reconciliation |

## 4. Cooperative ownership

동시 작업 격리는 강제 lock이 아니라 cooperative ownership이다.

- 다른 owner Branch/worktree의 dirty state를 clean/rebase/reset하지 않는다.
- 다른 채팅/독립 workstream의 Branch·path·PR은 기본 보호 대상이다.
- overlap 확인을 위해 read-only diff/head/path 조회는 가능하다.
- owner Branch에 직접 commit하지 않는다.
- `different workstream`은 현재 사용자 명시 승인 전 selective copy도 하지 않는다.
- `same workstream` 통합은 별도 Branch에서 수행한다.
- 같은 파일을 피했더라도 같은 semantic resource면 owner 충돌로 처리한다.
- process/port/temp directory도 소유권이 있으면 임의 종료·재사용하지 않는다.

## 5. BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16

### 5.1 Authorization boundary

standing authorization은 **same workstream**의 승인된 same-goal/path/semantic overlap을 기다리지 않고 latest main에서 통합하기 위한 기술적 권한이다.

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

- `same workstream`: standing authorization을 사용할 수 있다.
- `different workstream`: standing authorization이 `explicit user authorization`을 대신하지 않는다. 사용자가 현재 작업에서 명시적으로 흡수·통합 승인해야 한다.
- `UNKNOWN_WORKSTREAM`: owner identity와 승인 범위가 확인될 때까지 `BLOCKED_UNVERIFIED` 또는 `WAITING_RESOURCE`다.

### 5.2 Read-only owner snapshot

통합 전 owner PR branches를 수정하지 않고 기록한다.

```yaml
owner_pr_head_shas: []
current_workstream_identity:
owner_workstream_identity:
cross_workstream_absorption_authorized:
provisional_overlap_paths: []
provisional_semantic_resources: []
```

최소 확인:

- exact owner PR head SHA
- owner changed paths
- source/base SHA
- latest main SHA
- successor/duplicate PR 존재 여부
- semantic ownership
- workstream identity
- 현재 user absorption authorization 여부

### 5.3 Create a separate PROVISIONAL_INTEGRATION branch

```text
latest completed main
→ separate PROVISIONAL_INTEGRATION branch
→ no owner-branch write
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
- 다른 workstream에서 명시 흡수 승인되지 않은 변경
- unrelated dependency/product work

### 5.5 Semantic reconciliation

bytes 동일성보다 현재 의미를 비교한다.

```text
owner intent
+ owner tests
+ latest main implementation
+ successor merges
+ current canon
+ workstream authorization
→ semantic reconciliation
```

판정:

- `ABSORB_MATERIAL_DELTA`
- `ALREADY_ABSORBED_BY_SUCCESSOR`
- `REJECT_DUPLICATE_AUTHORITY`
- `PRESERVE_RESIDUAL_OWNER`
- `WAITING_RESOURCE`
- `BLOCKED_UNVERIFIED`

### 5.6 Verification and accounting

```yaml
absorbed_owner_deltas: []
residual_owner_deltas: []
rejected_duplicate_authority: []
```

`residual_owner_deltas`가 0이어야 해당 owner가 이 Goal에서 완전히 superseded되었다고 볼 수 있다. 그러나 `different workstream` owner PR의 close/supersede는 사용자의 현재 명시 승인 범위 안에서만 수행한다.

## 6. Write-time preflight

first persistent write 직전:

1. current main을 다시 읽는다.
2. current/owner workstream identity를 다시 확인한다.
3. current task Branch/head를 다시 읽는다.
4. same-goal open/recent PR을 다시 읽는다.
5. current task or PR itself를 overlap 후보에서 제외한다.
6. intended path + semantic resource overlap을 판정한다.
7. `CLEAR` 또는 승인된 `PROVISIONAL_INTEGRATION`일 때만 write한다.

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

- current main/base SHA 재확인
- actual branch head 확인
- changed paths/semantic resources 확인
- current/owner workstream auth 재확인
- same-goal PR/new successor 확인
- owner residual accounting 확인
- tests/evidence ceiling 확인

새로운 overlap이 생기면 PR을 만들기 전에 다시 reconcile한다.

## 8. Merge preflight

merge 직전:

```text
expected_head_sha == actual PR head sha
current main/base acceptable
workstream authorization still valid
required checks == PASS
unresolved threads == 0
required approvals satisfied
P0/P1 == 0
residual owner deltas accounted
NOT_RUN / BLOCKED_* / CANCELLED not promoted to PASS
```

PR metadata나 과거 성공 run만 보고 merge하지 않는다. exact head의 상태를 읽는다.

`different workstream` owner PR을 close/supersede하는 것도 merge와 별개의 mutation이며 현재 사용자 명시 승인 범위가 필요하다.

## 9. Post-merge main readback

병합 뒤:

1. 새 `main` SHA를 읽는다.
2. merge PR의 실제 merged state와 merge SHA를 읽는다.
3. changed canon/registry/policy/runtime file을 main에서 다시 읽는다.
4. same-goal open/recent PR을 다시 조회한다.
5. authorized owner PR의 `absorbed_owner_deltas / residual_owner_deltas`를 다시 확인한다.
6. current operational machine checkpoint가 있으면 읽는다.
7. generated/derived surface가 stale인지 확인한다.
8. postmerge workflow가 있으면 evidence ceiling을 확인한다.

병합 자체는 완료 증거가 아니다.

## 10. Failure recovery

### Missing `gh` / push auth

연결된 GitHub connector가 같은 mutation/read 기능을 제공하면 connector를 우선 사용한다. 사용자가 반복 인증해야 하는 수동 CLI 경로로 회귀하지 않는다.

### Local clone/network unavailable

GitHub connector + repository CI가 acceptance criterion을 권위 있게 증명할 수 있는지 확인한다. 가능하면 그 경로를 사용하고 local run은 `NOT_RUN`으로 남긴다.

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
- current_task_or_pr_identity:
- current_workstream_identity:
- owner_workstream_identity:
- cross_workstream_absorption_authorized:
- source_main_sha:
- current_main_sha:
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
- exact-head checks:
- unresolved threads:
- required approvals:
- merge SHA:
- post-merge main readback:
- NOT_RUN / BLOCKED / CANCELLED:
```

## 12. 금지

- 다른 채팅/독립 workstream을 same-goal이라는 이유만으로 자동 흡수
- explicit cross-workstream authorization 없이 owner Branch/path/PR write/rebase/close/merge/selective-copy
- owner PR branches 직접 수정
- dirty sibling worktree clean/reset
- stale blob/head blind overwrite
- whole old branch를 latest main에 무검토 merge
- same-path만 보고 semantic overlap 무시
- current task 자체를 overlap owner로 잘못 집계
- exact-head가 아닌 과거 CI 성공 재사용
- cancelled/blocked/not-run을 PASS로 보고
- residual material delta가 있는데 source PR을 superseded 처리
