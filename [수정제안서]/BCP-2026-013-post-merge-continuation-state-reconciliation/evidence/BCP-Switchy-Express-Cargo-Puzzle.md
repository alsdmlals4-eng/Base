# BCP - Switchy Express: Cargo Puzzle

## 역할

이 파일은 새 Base Change Proposal을 만들지 않는다.

Switchy Express: Cargo Puzzle에서 관찰된 handoff 병합 후 live continuation-state stale edge는 현재 Base의 `BCP-2026-013-post-merge-continuation-state-reconciliation`이 이미 소유한다. 따라서 사용자의 최신 **`BCP - 프로젝트 이름`** 명명 규칙에 따라 Switchy 프로젝트 증거를 기존 canonical BCP 아래에 보강하고, 새 Registry 항목이나 중복 공용 규칙은 만들지 않는다.

```yaml
project_evidence_name: "BCP - Switchy Express: Cargo Puzzle"
source_project: alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
source_project_merge_observed: 32a0d6c154188f36bdefdefe96e62bc2a4718565
related_project_decision: SX-DEC-055
related_project_pr: 137
existing_solution_verdict: REUSE_BCP_2026_013
new_base_proposal: false
new_registry_entry: false
new_active_base_behavior: false
```

## 프로젝트 관찰

Switchy Express의 `SX-DEC-055 Runtime Semantic POC`는 결정·설계·Definition of Ready까지 승인·병합되었지만, 사용자의 최신 지시로 실제 Godot/GDScript runtime 구현은 나중으로 보류되었다.

프로젝트의 cold-start/continuation owner를 현재 상태로 맞추는 PR #137을 진행하면서 다음 순서가 실제로 관찰됐다.

1. `START_HERE.md`, `ACTIVE_CONTEXT.md`, `ROADMAP.md`를 당시 main과 승인 상태 기준으로 갱신했다.
2. 첫 exact-head CI가 오래된 Android-immediate canonical-freshness assertion을 실패시켰다.
3. Android Device Smoke를 현재 즉시 작업으로 되돌리지 않고 별도 `OPEN_NOT_RUN` validation lane으로 유지하도록 consumer contract를 수정했다.
4. 다음 exact-head CI는 오래된 post-merge consumer가 `branch: main`, `pull_request_83: MERGED` 같은 과거 literal shape를 강제하는 문제를 드러냈다.
5. current main semantics와 historical PR evidence를 분리해 검증하도록 regression을 수정했다.
6. PR #137 exact head `7be35adf4fa98bb915616a1e6a89f67dcb19a4ca`에서 Project Contract, GUT, Godot, Thin, Windows Demo Export가 모두 PASS했다.
7. PR #137을 squash merge했고 project main이 `32a0d6c154188f36bdefdefe96e62bc2a4718565`로 바뀌었다.
8. merge 직후 live handoff가 보존한 pre-merge 관측점은 historical snapshot이 되었고, 현재 truth는 다시 GitHub main/open PR/CI에서 읽어야 했다.

즉 Switchy 사례에서도 다음 edge가 재현됐다.

```text
LIVE_CONTINUATION_STATE_VALID_AT_PR_HEAD
+ MERGE
= SAVED_INTEGRATION_METADATA_BECOMES_HISTORICAL
```

## Existing Solution First

Verdict: `REUSE_BCP_2026_013`.

Canonical owner:

- `BCP-2026-013-post-merge-continuation-state-reconciliation`
- existing Base owner: `maintaining-project-context-and-handoff`

Switchy에서 새 broad Skill이나 새 canonical BCP를 만들 필요는 없다.

핵심 재사용 원리는 다음이다.

```text
PRE_MERGE_STATE_CAPTURE
→ EXACT_HEAD_VERIFICATION
→ MERGE / INTEGRATION
→ OBSERVE_POST_MERGE_TRUTH
→ RECONCILE_LIVE_CONTINUATION_STATE
→ VERIFY_RECONCILIATION
→ CLOSE_HANDOFF
```

## 추가로 확인된 consumer migration 경계

Switchy 사례에서는 live handoff 문서를 갱신했을 때 오래된 자동 테스트가 **의미가 아니라 특정 문자열 모양**을 current contract로 고정하고 있던 문제가 함께 드러났다.

예:

```text
old literal consumer:
  branch: main
  pull_request_83: MERGED

current semantic contract:
  default branch is main
  live source is current GitHub repository truth
  PR #83 merge remains historical evidence
```

이 경우 안전한 수정은 current state를 오래된 문자열로 되돌리는 것이 아니라, consumer가 실제 의미를 검증하도록 migration하는 것이다.

다만 이 관찰은 새 BCP를 요구하지 않는다. 현재 Base의 BCP-013과 handoff owner가 이미 live/historical state 분리를 소유하고 있으며, machine-consumer compatibility는 기존 Base의 후속 handoff compatibility proposal/discipline과 함께 검토할 수 있다.

## 검증 ceiling 보존

PR #137 exact-head 자동 PASS는 다음을 의미하지 않는다.

```yaml
sx_dec_055_runtime_implementation: NOT_STARTED
runtime_integrated: false
windows_physical_runtime: NOT_RUN
android_landscape_device_smoke: NOT_RUN
connected_physical_editor: NOT_RUN
broader_human_comprehension: NOT_RUN
production_cutover: BLOCKED_DEFERRED
```

Hosted Windows export 성공도 physical Windows runtime·visual·audio·physical input PASS로 확대하지 않는다.

## 프로젝트 전용으로 남길 값

Base 공용 규칙으로 승격하지 않는다.

- `SX-DEC-055`
- Switchy의 rail/LIFO/cargo gameplay 규칙
- 73 semantic product PNG 수량
- PR #135~#137 번호
- 특정 Android/Windows validation lane 명칭과 순서
- Switchy 전용 테스트·문서 경로
- 프로젝트 Base pin `v9.4.3` 자체

## 현재 공용 판정

```yaml
finding_1:
  name: post_merge_live_continuation_state_reconciliation
  verdict: REUSE_BCP_2026_013
finding_2:
  name: historical_snapshot_vs_live_router_separation
  verdict: REUSE_BCP_2026_013
finding_3:
  name: stale_literal_consumer_during_handoff_refresh
  verdict: REUSE_EXISTING_HANDOFF_COMPATIBILITY_DISCIPLINE
new_base_gap_confirmed: false
```

## 병합 의미

이 증거 파일의 병합은 Switchy 프로젝트 학습을 기존 BCP-013에 연결하는 것만 의미한다.

- Proposal Registry 변경 없음
- 새 canonical BCP 없음
- 새 broad Skill 없음
- active Base Skill·Method·Template·Test·Tool·Workflow 변경 없음
- Base active implementation 승인 없음

활성 Base 구현은 기존 proposal lifecycle에 따라 별도 사용자 승인과 별도 구현 PR이 있어야 한다.
