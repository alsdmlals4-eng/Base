# BCP - OMENWARD

## Existing Solution First

```yaml
project: OMENWARD
project_repository: alsdmlals4-eng/omenward
canonical_base_proposal: BCP-2026-013-post-merge-continuation-state-reconciliation
existing_solution_verdict: REUSE_BCP_2026_013
new_canonical_bcp: false
proposal_registry_change: false
active_base_behavior_change: false
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
```

OMENWARD에서 관찰된 continuation-state 문제는 이미 Base의 `BCP-2026-013-post-merge-continuation-state-reconciliation`이 소유하는 공용 Goal과 같다. 따라서 새 일반 BCP를 만들지 않고, 사용자 요청의 `BCP - 프로젝트 이름` 규칙에 따라 이 프로젝트 증거를 `BCP - OMENWARD`로 기존 BCP-013에 연결한다.

## 프로젝트 관찰

OMENWARD의 승인된 runtime 구현은 Draft PR #175에서 exact-head 증거를 보존하면서 진행되었고, 별도 Draft PR #177이 `ACTIVE_CONTEXT`, `HANDOFF_CONTEXT`, `CURRENT_IMPLEMENTATION_STATUS`를 담는 continuation locator 역할을 했다.

2026-08-10 11:57 KST 사용자는 진행 중이던 로컬 HiGodot/runtime 진단을 나중에 재개하고 먼저 인수인계를 수행하도록 요청했다. 당시 handoff snapshot은 그 시점의 저장소·runtime·blocker 사실을 정확히 기록했다.

그 뒤 새 실행이 시작되자 fresh GitHub/Base/Sheet truth를 다시 읽었고 다음 차이가 발생했다.

1. historical handoff snapshot은 당시 사실로서 여전히 유효했다.
2. live `ACTIVE_CONTEXT`는 새 실행 시점의 current truth에 맞게 다시 갱신되어야 했다.
3. runtime PR #175는 이후 non-Godot transition-CI reconciliation을 진행해 exact head가 전진했다.
4. 이전 exact head에서 존재하던 네 CI transition failure는 새 exact head에서 모두 해소되었다.
5. 따라서 live router가 과거 handoff의 SHA·CI 상태를 계속 current truth로 주장했다면 즉시 stale state가 되었을 것이다.

이 관찰은 BCP-013의 핵심 invariant를 재확인한다.

```text
HISTORICAL_HANDOFF_SNAPSHOT = point-in-time evidence
LIVE_CONTINUATION_ROUTER = fresh repository truth dependent
```

## 추가 use-condition: locator 자체의 merge가 active work를 stale하게 만드는 경우

OMENWARD에서는 continuation locator PR #177을 즉시 main에 병합하지 않는 것이 더 안전했다.

그 이유는 locator의 목적이 active runtime exact-head 작업을 보존하고 다음 실행이 재개할 수 있게 하는 것이었는데, locator를 main에 병합하면 main SHA가 전진하고 보존 중인 active runtime PR #175가 불필요하게 behind/stale 상태가 되어 재동기화 비용을 만들 수 있었기 때문이다.

따라서 다음 조건을 BCP-013의 보조 evidence/use-condition으로 제시한다.

```text
IF
  continuation locator merge would itself invalidate, stale, or unnecessarily move
  the baseline of the exact-head implementation work it is preserving
THEN
  the locator may remain REFERENCE_ONLY / DO_NOT_MERGE,
  while the live continuation router is reconciled from fresh repository truth.
```

이 규칙은 "handoff PR은 항상 병합해야 한다"는 뜻이 아니다. 반대로 모든 handoff PR을 미병합 상태로 두라는 뜻도 아니다. integration이 continuation truth를 바꾸는지와 active exact-head work에 실제 복구 비용을 만드는지를 기준으로 판단한다.

## 재현된 transition-state 예시

OMENWARD runtime PR에서 과거 exact head는 GitHub Actions `7 SUCCESS / 4 FAILURE` 상태였다. 이후 같은 승인 범위에서 transition gate를 보수한 새 exact head는 triggered workflow `11 SUCCESS / 0 FAILURE`가 되었다.

이 변화는 dated handoff snapshot을 rewrite해야 한다는 증거가 아니다. 오히려 다음을 보여준다.

- historical snapshot은 과거 상태로 보존한다.
- live `ACTIVE_CONTEXT` 또는 동등한 current router만 새 exact head와 current CI truth를 반영한다.
- 다음 실행은 locator 문서보다 fresh GitHub/Sheet truth를 우선한다.

## 공용화할 수 있는 원리

BCP-013에 추가로 유용한 일반화 후보는 다음과 같다.

1. **Historical snapshot과 live router를 별도 역할로 취급한다.**
2. **Live router는 새 실행 시작 시 fresh repository/integration truth로 다시 reconcile한다.**
3. **Continuation locator 자체를 통합하는 것이 active exact-head work를 stale하게 만들면 reference-only 보존을 허용한다.**
4. **Reference-only locator는 current authority가 아니다. fresh repository truth가 항상 우선한다.**
5. **CI 상태·PR 상태·head SHA가 변하면 과거 PASS/FAIL을 current 상태로 재사용하지 않는다.**

## Base에 올리지 않을 OMENWARD 전용 값

다음 값은 공용 규칙으로 승격하지 않는다.

- OMENWARD의 PR/Issue 번호와 branch 이름
- 특정 commit SHA
- Windows Godot process PID
- WS9500 port/session 관찰값
- HiGodot/GUT/Hera의 OMENWARD별 실행 세부
- 병영 role-output gap 목록
- 전투/기능가치 수치와 provisional PoC numerics
- `BLOCKED_RUNTIME_OUTPUT`을 사용하는 특정 project metric 이름
- OMENWARD Sheet의 tab/cell 주소

공용화 대상은 continuation lifecycle과 fresh-truth reconciliation 원리뿐이다.

## 반례 / Do Not Use

- dated review/handoff가 명시적으로 point-in-time evidence라면 이후 main/head 변경 때문에 rewrite하지 않는다.
- locator merge가 active work baseline에 영향을 주지 않고 정상적인 통합이 필요한 경우에는 `DO_NOT_MERGE`를 기본값으로 적용하지 않는다.
- live router가 외부 시스템에서 자동 생성되고 freshness가 보장되는 프로젝트라면 별도 수동 reconciliation commit을 강제하지 않는다.
- current truth를 검증할 수 없는 경우에는 stale 값을 추정해 갱신하지 않고 `BLOCKED_UNVERIFIED` 또는 동등 상태로 남긴다.

## 검증 기준

이 evidence가 향후 BCP-013 구현 검토에 사용될 경우 다음 시나리오를 포함하면 좋다.

### Scenario A — historical snapshot preserved

Given a dated handoff that accurately records pre-change state,
when the implementation PR later advances,
then the dated handoff remains valid history and is not rewritten solely to match the new head.

### Scenario B — live router refresh

Given a live Active Context that points to an older implementation head,
when fresh GitHub truth reports a newer head/CI state,
then the live router is reconciled before it is used as current continuation authority.

### Scenario C — reference-only locator

Given a handoff/locator PR whose merge would advance main and unnecessarily stale the exact-head implementation PR it preserves,
then the locator may stay unmerged and explicitly `REFERENCE_ONLY / DO_NOT_MERGE`, while fresh repository truth remains authoritative.

### Scenario D — no baseline harm

Given a locator whose merge does not invalidate or stale active work,
then this evidence does not prohibit normal merge/integration.

## Scope and lifecycle status

```yaml
evidence_role: PROJECT_NAMED_CORROBORATING_EVIDENCE
human_title: BCP - OMENWARD
canonical_owner: BCP-2026-013-post-merge-continuation-state-reconciliation
proposal_status_in_base: SUBMITTED
active_base_implementation: NOT_AUTHORIZED_BY_THIS_EVIDENCE
registry_change: NONE
active_skill_change: NONE
active_method_change: NONE
active_template_change: NONE
active_test_change: NONE
active_workflow_change: NONE
```

이 파일의 병합 여부와 무관하게 OMENWARD의 제품/runtime 승인 범위나 Base active behavior는 변경되지 않는다. 실제 BCP-013 구현은 별도의 `APPROVED_FOR_IMPLEMENTATION` 결정과 구현 PR이 있어야 한다.
