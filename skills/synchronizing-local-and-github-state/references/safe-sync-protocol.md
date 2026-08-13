# 안전한 Git 동기화 프로토콜

이 프로토콜은 Git 상태뿐 아니라 동시에 진행 중인 Branch·PR·Task의 소유권을 첫 write 전에 판정한다. `CONCURRENT_CHANGE_PREFLIGHT`는 협업자가 지키는 **cooperative** 계약이며 GitHub의 강제 mutex나 외부 lock service를 대신하지 않는다.

## 1. 기준과 작업 의도 고정

1. remote·upstream·기본 Branch·현재 Branch·HEAD·working tree·untracked를 기록한다.
2. `fetch --prune` 뒤 기본 Branch의 실제 `current_main_sha`, 현재 Branch의 fork point와 ahead/behind를 판정한다.
3. 조사·분기 기준 `source_main_sha`, 검토·병합 대상 `expected_head_sha`, 이번 작업의 Goal·`intended_paths`·`semantic_resource_locks`를 기록한다.
4. 쓰기 범위가 아직 확정되지 않았으면 읽기·조사만 진행하고 `CLEAR`를 추정하지 않는다.

## 2. 동시작업 증거 수집

5. 같은 저장소의 열린 PR과 같은 Goal의 최근 병합·종료·대체 PR을 조회한다.
6. 열린 PR별 changed paths, source/generator/derivative 관계와 알려진 semantic resource owner를 수집한다.
7. `AGENTS.md`, 보호 Branch 정책, Required Checks, 승인·권한과 `protected_concurrent_paths`를 대조한다.
8. PR 목록·changed paths·현재 main·policy 중 필요한 증거를 읽지 못하면 `UNKNOWN + BLOCKED_UNVERIFIED`다.

## 3. 중첩·중복·stale 분류

```text
NO_OVERLAP      → 경로·의미 자원·Goal 중첩 없음
PATH_OVERLAP    → 하나 이상의 활성 PR과 경로가 겹침
SEMANTIC_OVERLAP→ 파일은 같거나 달라도 같은 정본·Schema·생성물·runtime·Scene·자산 계열을 변경
SAME_GOAL       → 같은 사용자 Goal과 기대 결과를 다른 활성·대체 작업이 소유
UNKNOWN         → 판정 증거 부족
```

9. `source_main_sha != current_main_sha`면 먼저 `STALE_BASE_SHA`로 판정한다. 최신 main에 reconcile하고 영향 검증 뒤 전체 preflight를 다시 수행한다.
10. `SAME_GOAL`이면 `DUPLICATE_WORK`다. 경쟁 PR을 만들지 않고 기존 PR의 검토·보완·대체 관계를 확인한다.
11. 활성 `PATH_OVERLAP` 또는 `SEMANTIC_OVERLAP`이면 기본 disposition은 `WAITING_RESOURCE`다. 단순히 자동 merge 가능해 보인다는 이유로 `CLEAR`로 낮추지 않는다.
12. `PATH_OVERLAP`은 실제 textual merge conflict의 확정 증거가 아니다. 의도한 hunk·소유권·source/derivative 관계를 확인한다. 반대로 다른 파일이어도 `SEMANTIC_OVERLAP`이면 동시 writer를 허용하지 않는다.
13. 필요한 증거가 모두 있고 current main이 기준과 같으며 same-goal·활성 writer 중첩이 없을 때만 `CLEAR`다.

## 4. 충돌 없는 실행 경로

14. **first persistent write** 전에 preflight가 `CLEAR`인지 확인하고, 정확한 `source_main_sha`에서 격리 Branch/Worktree를 사용한다.
15. 다른 PR이 문서·정본을 소유하면 다음 순서로 조정한다.

```text
비중첩 path로 범위 축소
→ 소유 PR에 finding·필요 수정 comment 전달
→ 명시적 handoff 또는 resource release 확인
→ 최신 main/PR 상태 재조회
→ preflight 재실행
```

comment를 남긴 사실만으로 resource가 해제됐다고 간주하지 않는다. `WAITING_RESOURCE`가 유지되면 해당 write를 보류하고 독립된 작업만 진행한다.

16. working tree가 `DIRTY`면 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
17. `REMOTE_AHEAD`는 clean fast-forward일 때만 자동 갱신한다.
18. `LOCAL_AHEAD`는 실제 diff·검증·명시적 파일 범위를 확인한 뒤 push한다.
19. `DIVERGED`는 백업 Branch를 먼저 만들고 merge·rebase·새 Branch 중 선택한 전략을 기록한다. force push·hard reset은 자동 수행하지 않는다.
20. 비밀·대용량 생성물·승인되지 않은 파일과 범위 밖 변경은 commit하지 않는다.

## 5. PR·검토·병합 Gate

21. **PR creation** 직전 최종 `intended_paths`와 semantic resources로 열린 PR·same-goal·current main을 다시 조회한다. 새 중첩이 생기면 PR 생성을 멈추고 disposition을 갱신한다.
22. PR 설명에는 `source_main_sha`, exact `expected_head_sha`, changed paths, protected paths, preflight 결과, 검증·미검증, rollback을 기록한다.
23. Required Checks는 exact `expected_head_sha`에서 실행된 결과만 사용한다. 이전 HEAD 또는 stale merge preview 결과를 현재 증거로 재사용하지 않는다.
24. **merge** 직전 다음을 다시 확인한다.

```text
reviewed HEAD == expected_head_sha
current main freshness
same-goal open/recent PRs
open PR changed paths
path and semantic resource ownership
required checks and unresolved review state
```

main 또는 PR 집합이 바뀌면 `STALE_BASE_SHA`, `WAITING_RESOURCE`, `DUPLICATE_WORK`, `BLOCKED_UNVERIFIED` 중 하나로 재분류하고 reconcile·재검증 전에는 병합하지 않는다.

## 6. 완료·병합 후 검증

25. 병합하지 않은 sync 작업은 최종 local HEAD와 remote HEAD, tree diff, ahead/behind, CI 상태를 대조한다.
26. 병합한 작업은 **post-merge main readback**에서 새 main SHA와 실제 변경 파일·핵심 계약·생성/소비자 상태를 다시 읽는다.
27. 같은 Goal의 열린·최근 PR, stale Branch, 누락 consumer·정본 충돌을 재검사한다. 발견 시 `OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK`로 라우팅하고 완료를 주장하지 않는다.
28. 실행하지 못한 로컬 검사·런타임·렌더·Branch cleanup은 `BLOCKED_UNVERIFIED` 또는 명시적 미검증으로 보고한다.

## 최소 출력

```yaml
source_main_sha:
current_main_sha:
expected_head_sha:
git_state:
overlap_classification:
disposition:
intended_paths: []
semantic_resource_locks: []
same_goal_open_and_recent_prs: []
coordination_action:
validation_evidence:
post_merge_main_sha:
remaining_risk:
```
