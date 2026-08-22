# Current Workstream Continuation Through Merge Design

## Status

```yaml
status_scope: USER_APPROVED_IMPLEMENTATION_DESIGN
base_goal: reduce repeated merge confirmations within one approved workstream
new_broad_skill: NONE
repository_governance_bypass: FORBIDDEN
foreign_pr_mutation: EXPLICIT_NAMED_AUTHORIZATION_REQUIRED
```

## Goal

사용자가 현재 작업의 방향·범위를 승인한 뒤 `진행해`, `계속 진행해`, `남은 작업 전부 진행해`, `권장안대로 진행해` 또는 동등한 **연속 실행 지시**를 주면, 같은 current workstream이 만든 변경은 구현에서 멈추지 않고 정상 Git 생명주기의 끝인 `PR → exact-head Required Checks → 필요 시 범위 보존 충돌 해소 → merge → postmerge main readback`까지 진행한다.

## Why

현행 `SINGLE_INITIAL_APPROVAL_THEN_CONTINUE`와 장기 작업 흐름은 이미 `ONE USER APPROVAL → ... → MERGE → POSTMERGE READBACK`을 의도하지만, `OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`이 current workstream에도 동일하게 적용되어 PR 생성 뒤 사용자가 PR 번호와 `병합해`를 다시 말해야 한다. 이 중복 승인을 없애되 다른 workstream 보호는 약화하지 않는다.

## Contract

```text
CURRENT_WORKSTREAM_CONTINUE_INCLUDES_MERGE
CURRENT_WORKSTREAM_IDENTITY_REQUIRED
EXACT_HEAD_REQUIRED_CHECKS_PASS
POSTMERGE_READBACK_REQUIRED
FOREIGN_OR_UNKNOWN_WORKSTREAM_REQUIRES_NAMED_AUTHORIZATION
EXPLICIT_STOP_BEFORE_MERGE_OVERRIDES_CONTINUATION
BLOCK_ON_FAILED_OR_PENDING_REQUIRED_CHECKS
NO_FORCE_PUSH_OR_GOVERNANCE_BYPASS
SEMANTIC_CONFLICT_REQUIRES_USER_DECISION
```

Continuation authority applies only when all are true:

1. 현재 채팅/작업 계약/branch/PR이 같은 `current_workstream_identity`로 증명된다.
2. 사용자가 현재 workstream의 방향 또는 실행을 이미 승인했고 이후 연속 실행 지시를 했다.
3. 사용자가 `병합하지 마`, `PR까지만`, `draft로 멈춰`처럼 더 구체적인 stop instruction을 주지 않았다.
4. exact-head Required Checks와 필수 검증이 모두 성공하고 blocking finding/thread가 없다.
5. PR이 mergeable하고 repository rules를 우회하지 않는다.
6. 최신 main과 충돌하면 승인된 current-workstream 의미와 최신 main 양쪽을 보존하는 bounded reconciliation만 한다. 핵심 기획·비용·보안·권한·범위를 바꾸는 semantic conflict는 사용자 결정으로 올린다.

## Non-goals / protected boundaries

- 다른 채팅·다른 작업자·owner 불명 PR을 `진행해`만으로 수정·흡수·종료·병합하지 않는다.
- failed/pending Required Check를 무시하지 않는다.
- force-push, branch protection/ruleset 완화, admin bypass를 하지 않는다.
- 사용자가 명시한 `do not merge`를 standing continuation보다 항상 우선한다.
- 유료 구매·credential/permission 확대·파괴적 삭제 같은 별도 위험 행동은 이 계약이 승인하지 않는다.

## Placement

새 Skill을 만들지 않는다. 기존 owner 네 곳을 함께 보강한다.

- `AGENTS.md`: 항상 적용되는 authority rule.
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`: lifecycle semantics.
- `skills/synchronizing-local-and-github-state/SKILL.md`: PR/workstream routing.
- `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`: merge/conflict/readback 실행 경계.

Regression owner: `tests/test_current_workstream_continue_merge_contract.py`.

## Rollback

새 token과 current-workstream exception 문단을 위 네 owner에서 제거하고 전용 regression test를 제거하면 기존 `PR 번호 + 허용 동작` 방식으로 복귀한다. 다른 PR 보호 규칙과 Required Check 설정은 변경하지 않는다.
