# 안전한 Git 동기화 프로토콜

이 프로토콜은 Git 상태뿐 아니라 동시에 진행 중인 Branch·PR·Task의 소유권을 첫 write 전에 판정한다. `CONCURRENT_CHANGE_PREFLIGHT`는 협업자가 지키는 **cooperative** 계약이며 GitHub의 강제 mutex나 외부 lock service를 대신하지 않는다.

Base의 기본 충돌 복구 방식은 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`에 따른 **latest-main copy integration**이다. 이미 승인된 작업이 같은 Goal·path·semantic resource와 겹치면 owner PR을 기다리거나 직접 고치지 않고, exact latest completed `main`에서 별도 통합 Branch를 만든 뒤 필요한 material delta만 selective copy/reproduce하고 semantic reconciliation한다.

호환성 주의: 과거 계약의 literal `explicit user authorization`과 `must not merge`는 legacy migration/search token으로만 보존하며 **현재 Gate가 아니다**. 현재 계약은 standing authorization, owner PR read-only, material-delta accounting, exact-head validation으로 대체한다.

## 1. 기준과 작업 의도 고정

1. remote·upstream·기본 Branch·현재 Branch·HEAD·working tree·untracked를 기록한다.
2. `fetch --prune` 뒤 기본 Branch의 실제 `current_main_sha`, 현재 작업 Branch의 exact `write_parent_sha`, fork point와 ahead/behind를 판정한다.
3. 현재 작업을 다른 Task·Branch·PR과 구별할 `current_task_or_pr_identity`를 기록한다.
4. 조사·분기 기준 `source_main_sha`, 이번 작업의 Goal·`intended_paths`·`semantic_resource_locks`를 기록한다.
5. 첫 write 전에는 최종 변경 commit이 없으므로 `expected_head_sha: PENDING_FIRST_WRITE`다. 첫 write가 반환한 commit SHA를 exact `expected_head_sha`로 기록하고, 다음 write 전에는 그 값을 새 `write_parent_sha`로 사용한다.
6. 쓰기 범위가 아직 확정되지 않았으면 읽기·조사만 진행하고 `CLEAR`를 추정하지 않는다.

## 2. 동시작업 증거 수집

7. 같은 저장소의 열린 PR과 같은 Goal의 최근 병합·종료·대체 PR을 조회한다.
8. 비교 목록에서는 **exclude the current task or PR itself**. `current_task_or_pr_identity`가 없거나 현재 PR을 다른 작업과 구별할 수 없으면 `BLOCKED_UNVERIFIED`다.
9. 다른 열린 PR별 changed paths, source/generator/derivative 관계와 알려진 semantic resource owner를 수집한다.
10. `AGENTS.md`, 보호 Branch 정책, Required Checks, 승인·권한과 `protected_concurrent_paths`를 대조한다.
11. PR 목록·changed paths·현재 main·현재 작업 identity·Branch HEAD·policy 중 필요한 증거를 읽지 못하면 `UNKNOWN + BLOCKED_UNVERIFIED`다.

## 3. 중첩·중복·stale 분류

```text
NO_OVERLAP       → 현재 작업 자신을 제외한 경로·의미 자원·Goal 중첩 없음
PATH_OVERLAP     → 다른 활성 PR과 하나 이상의 경로가 겹침
SEMANTIC_OVERLAP → 파일은 같거나 달라도 같은 정본·Schema·생성물·runtime·Scene·자산 계열을 변경
SAME_GOAL        → 같은 사용자 Goal과 기대 결과를 다른 활성·대체 작업이 소유
UNKNOWN          → 판정 증거 부족
```

12. `source_main_sha != current_main_sha`면 먼저 `STALE_BASE_SHA`로 판정한다. 최신 main에 reconcile하고 영향 검증 뒤 전체 preflight를 다시 수행한다.
13. 관찰한 현재 작업 Branch HEAD가 선언한 `write_parent_sha`와 다르면 concurrent branch update다. 내용을 다시 읽고 새 parent를 명시하기 전에는 write하지 않는다.
14. `SAME_GOAL`, `PATH_OVERLAP`, `SEMANTIC_OVERLAP`이 있어도 이미 승인된 작업이면 단순 대기보다 `PROVISIONAL_INTEGRATION`을 기본 recovery로 사용한다. `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`이 replacement/coordination standing authorization이다.
15. standing authorization은 새 제품 범위, 파괴적 마이그레이션, 결제, 계정·보안 권한 확대, direct main, force push, `--admin`, ruleset bypass를 승인하지 않는다. 이런 새 권한이 필요하면 `USER_DECISION_REQUIRED` 또는 해당 고위험 Gate로 분리한다.
16. `PATH_OVERLAP`은 actual textual merge conflict의 확정 증거가 아니다. 필요한 hunk와 source/derivative 관계를 확인한다. 반대로 파일이 달라도 `SEMANTIC_OVERLAP`이면 반드시 reconciliation 대상으로 기록한다.
17. 필요한 증거가 모두 있고 current main과 write parent가 고정 기준에 일치하며 중첩이 없을 때만 `CLEAR`다. 중첩이 있지만 standing copy-integration 경로로 진행하는 작업은 `CLEAR`가 아니라 `PROVISIONAL_INTEGRATION`으로 남긴다.

## 3.1 `PROVISIONAL_INTEGRATION` / copy integration

18. `PROVISIONAL_INTEGRATION`은 waiting 비용을 줄이면서 active owner Branch를 보호하는 Base 기본 조정 상태다. Base standing authorization은 다음 ID로 추적한다.

```text
BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
```

19. 통합 Branch는 **exact latest completed main**에서 만들고 다음을 preflight에 고정한다.

```yaml
copy_integration_policy: DEFAULT_ON_CONFLICT
standing_authorization: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
provisional_integration_authorized: true
owner_pr_head_shas:
  "<pr-number>": "<exact-head-sha>"
provisional_overlap_paths: []
provisional_semantic_resources: []
absorbed_owner_deltas: []
residual_owner_deltas: []
last_reconciled_main_sha:
```

20. **owner PR branches**는 read-only다. 통합 작업은 owner PR Branch에 commit·push·rebase·force-push·test-fix write를 하지 않는다. 필요한 구현은 통합 Branch에 **selective copy**·흡수·재구현한다.
21. copy는 stale whole-file replacement가 아니다. 최신 main에 존재하는 더 새롭거나 강한 계약을 보존하고, owner PR에서 필요한 material delta만 재현한다. owner PR이나 main이 변할 때마다 **semantic reconciliation**을 다시 수행해 stale/provisional duplicate를 제거한다.
22. `absorbed_owner_deltas`에는 통합 Branch에 실제 반영·검증한 owner material delta를 기록한다. `residual_owner_deltas`에는 아직 고유하게 남아 통합 범위에서 보존해야 하는 작업을 기록한다. 둘 다 근거 없이 비어 있다고 추정하지 않는다.

## 4. 충돌 없는 실행 경로

23. **first persistent write** 전에 preflight가 `CLEAR` 또는 standing authorization이 적용된 `PROVISIONAL_INTEGRATION`인지 확인한다. overlap이 있으면 stale owner Branch가 아니라 exact latest completed main에서 격리 Branch/Worktree를 만든다.
24. write 성공 뒤 반환된 commit SHA를 `expected_head_sha`로 기록한다. 후속 write가 있으면 Branch HEAD를 다시 읽고 그 SHA를 다음 `write_parent_sha`로 고정한다.
25. approved work의 same-goal/path/semantic overlap은 다음 순서가 기본이다.

```text
owner PR/head/path/semantic resource read-only snapshot
→ latest completed main exact SHA
→ separate integration branch
→ selective copy / reproduce material delta
→ semantic reconciliation
→ stale duplicate removal
→ affected tests
→ exact-head validation
```

26. 필요한 owner delta를 안전하게 식별할 증거가 없거나 reconciliation이 제품 의미·보안·권한 결정을 새로 요구하면 그 부분만 `WAITING_RESOURCE` 또는 `BLOCKED_UNVERIFIED`로 defer한다. **open PR 존재 자체는 WAITING_RESOURCE 사유가 아니다.**
27. working tree가 `DIRTY`면 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
28. `REMOTE_AHEAD`는 clean fast-forward일 때만 자동 갱신한다.
29. `LOCAL_AHEAD`는 실제 diff·검증·명시적 파일 범위를 확인한 뒤 push한다.
30. `DIVERGED`는 백업 Branch를 먼저 만들고 merge·rebase·새 Branch 중 선택한 전략을 기록한다. force push·hard reset은 자동 수행하지 않는다.
31. 비밀·대용량 생성물·승인되지 않은 파일과 범위 밖 변경은 commit하지 않는다.

## 5. PR·검토·병합 Gate

32. **PR creation** 직전 최종 `intended_paths`와 semantic resources로 열린 PR·same-goal·current main을 다시 조회한다. 현재 PR 자신은 비교 대상에서 제외한다. 새 overlap이 생기면 owner/head/path/resource 목록에 추가하고 latest-main copy integration 범위에서 reconcile한다.
33. PR 설명에는 `current_task_or_pr_identity`, `source_main_sha`, exact `expected_head_sha`, changed paths, protected paths, preflight 결과, 검증·미검증, rollback을 기록한다. `PROVISIONAL_INTEGRATION`이면 standing authorization, `owner_pr_head_shas`, `provisional_overlap_paths`, `provisional_semantic_resources`, `absorbed_owner_deltas`, `residual_owner_deltas`, 마지막 reconciliation 기준 main SHA를 함께 기록한다.
34. Required Checks는 exact `expected_head_sha`에서 실행된 결과만 사용한다. 이전 HEAD 또는 stale merge preview 결과를 현재 증거로 재사용하지 않는다.
35. **merge** 직전 다음을 다시 확인한다.

```text
current PR identity is excluded from duplicate comparison
reviewed HEAD == expected_head_sha
current main freshness
owner PR exact heads and changed paths
path and semantic resource ownership
absorbed_owner_deltas / residual_owner_deltas
required checks and unresolved review state
```

main, 현재 작업 Branch HEAD 또는 owner PR head가 바뀌면 최신 main에 reconcile하고 material delta accounting과 exact-head 검증을 다시 수행한다.

36. owner PR이 **열려 있다는 사실만으로** 통합 PR을 막지 않는다. 다음 조건을 모두 만족하면 standing authorization 아래 병합할 수 있다.

```text
latest main reconciled
→ 필요한 owner material delta 전부 absorbed 또는 근거 있게 제외
→ residual unique work가 있으면 residual_owner_deltas에 보존
→ stale duplicate 0
→ exact-head required checks PASS
→ P0/P1 0
→ unresolved review thread 0
→ expected head pinned
```

37. 병합 뒤 material delta가 전부 흡수되어 owner PR에 고유 작업이 없으면 그 PR에 absorption 근거를 남기고 `superseded`로 정리할 수 있다. `residual_owner_deltas`가 남으면 owner PR을 닫아 완료를 가장하지 않고 남은 고유 범위를 보존한다.

## 6. 완료·병합 후 검증

38. 병합하지 않은 sync 작업은 최종 local HEAD와 remote HEAD, tree diff, ahead/behind, CI 상태를 대조한다.
39. 병합한 작업은 **post-merge main readback**에서 새 main SHA와 실제 변경 파일·핵심 계약·생성/소비자 상태를 다시 읽는다.
40. 현재 완료된 PR 자신을 제외한 같은 Goal의 열린·최근 PR, stale Branch, 누락 consumer·정본 충돌을 재검사한다. 발견 시 `OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK`로 라우팅한다. fully absorbed owner PR은 superseded 후보, residual owner PR은 remaining work로 분리한다.
41. 실행하지 못한 로컬 검사·런타임·렌더·Branch cleanup은 `BLOCKED_UNVERIFIED` 또는 명시적 미검증으로 보고한다.

## 최소 출력

```yaml
current_task_or_pr_identity:
source_main_sha:
current_main_sha:
write_parent_sha:
expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>
git_state:
overlap_classification:
disposition:
copy_integration_policy: DEFAULT_ON_CONFLICT
standing_authorization: BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
provisional_integration_authorized: true | false
owner_pr_head_shas: {}
provisional_overlap_paths: []
provisional_semantic_resources: []
absorbed_owner_deltas: []
residual_owner_deltas: []
last_reconciled_main_sha:
coordination_action:
validation_evidence:
post_merge_main_sha:
remaining_risk:
```
