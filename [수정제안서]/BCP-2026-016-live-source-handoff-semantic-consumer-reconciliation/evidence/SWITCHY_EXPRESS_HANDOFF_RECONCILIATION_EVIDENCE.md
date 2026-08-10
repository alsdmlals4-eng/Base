# Switchy Express Handoff Reconciliation Evidence

## Evidence identity

```yaml
project: Switchy Express: Cargo Puzzle
repository: alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
project_decision: SX-DEC-055
source_main_observed: eb07dcc39b9675a54c675694236f507a8e50e78a
project_pr_137: MERGED
project_pr_138: MERGED
base_project_proposal: BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation
active_base_behavior_change: false
```

이 파일은 Base 일반 규칙을 직접 변경하지 않는다. Switchy Express에서 실제로 실행·검증된 handoff/current-state 개선과 검증 ceiling을 project-specific evidence로 보존한다.

## 프로젝트 상황

`SX-DEC-055 Runtime Semantic POC`는 사용자 승인, 설계 Spec, RED-first exact-file DoR까지 완료됐지만 실제 Godot/GDScript 구현은 사용자의 지시로 보류됐다.

따라서 다음 세션이 잘못된 과거 작업으로 진입하지 않으면서도 승인된 `SX-DEC-055`를 그대로 재개할 수 있게 current handoff/cold-start surface를 정리해야 했다.

프로젝트 main의 현재 관측점은 `eb07dcc39b9675a54c675694236f507a8e50e78a`이며, evidence 작성 시 열린 프로젝트 PR은 0이다.

## PR #137 — current-state refresh와 semantic consumer migration

- PR: `Switchy-Express-Cargo-Puzzle #137`
- title: `docs: refresh handoff state after SX-DEC-055 deferral`
- exact head: `7be35adf4fa98bb915616a1e6a89f67dcb19a4ca`
- merge commit: `32a0d6c154188f36bdefdefe96e62bc2a4718565`
- changed files: 5
- runtime/product bytes changed: `false`

### 최초 문제 1 — stale Android immediate-task consumer

새 handoff는 `SX-DEC-055 USER_DEFERRED_AFTER_DOR`를 current authority로 만들고 Android Device Smoke를 별도 `OPEN_NOT_RUN` lane으로 남겼다.

그런데 기존 canonical-freshness regression은 과거 문자열인 `ANDROID DEVICE SMOKE · CURRENT`를 계속 요구했다.

복구 원칙:

```text
DO NOT restore stale product/current-task state just to satisfy a test.
Preserve the still-open validation gate,
but migrate the consumer to the current semantic state.
```

최종 consumer는 다음 의미를 검증하게 됐다.

- `SX-DEC-055`가 current deferred runtime authority다.
- Android device validation은 여전히 `NOT_RUN`이다.
- Android validation이 immediate current task라는 과거 literal은 제거한다.

### 최초 문제 2 — fossilized field spelling

다음 실패에서는 오래된 post-merge regression이 다음 literal shape를 current contract로 요구했다.

```text
branch: main
pull_request_83: MERGED
```

하지만 새 live router의 의미는 다음과 같았다.

```text
default branch is main
current authority is live repository truth
PR #83 remains historical merge evidence
```

프로젝트는 현재 문서를 과거 spelling에 맞춰 되돌리지 않고, regression이 current semantics + historical evidence를 검증하도록 migration했다.

### PR #137 exact-head verification

GitHub Actions exact head `7be35adf4fa98bb915616a1e6a89f67dcb19a4ca`:

| Workflow | Run ID | Result |
|---|---:|---|
| Project Contract | 31354096765 | PASS |
| GUT 9.7.1 Tests | 31354096767 | PASS |
| Godot Tests | 31354096757 | PASS |
| Validate Thin Adapter Migration | 31354096769 | PASS |
| Windows Demo Export | 31354096778 | PASS |

이 PASS는 handoff/canonical-freshness 변경의 repository-level 자동 검증이다. 실제 physical Windows runtime, Android device, connected editor, human comprehension을 증명하지 않는다.

## PR #137 merge 이후 stale edge

PR #137이 merge되자 project main이 `32a0d6c154188f36bdefdefe96e62bc2a4718565`로 이동했다.

PR head에서 정확했던 handoff의 integration metadata는 merge 직후 historical observation이 됐다.

```text
valid_at_exact_head
→ merge changes repository truth
→ stored SHA / PR state becomes historical
```

이 현상은 pre-merge 문서가 틀렸다는 뜻이 아니다. current router와 point-in-time evidence의 수명주기가 다르다는 뜻이다.

## PR #138 — live source와 self-SHA loop 방지

- PR: `Switchy-Express-Cargo-Puzzle #138`
- title: `docs: reconcile post-merge handoff after PR 137`
- exact head: `51dbffef06f274ca319b4d23982d65c8d7753709`
- merge commit: `eb07dcc39b9675a54c675694236f507a8e50e78a`
- changed files: 2 project-hub docs
- runtime/product bytes changed: `false`

PR #138은 live router가 자신의 closure commit SHA를 다시 써야 하고 그 commit 때문에 다시 stale해지는 self-reference loop를 피하도록 current source를 다음처럼 바꿨다.

```yaml
current_main_source: LIVE_GITHUB_DEFAULT_BRANCH
post_merge_main_observed_after_pr_137: 32a0d6c154188f36bdefdefe96e62bc2a4718565
```

원칙:

- current truth는 GitHub default branch/open PR/actual files/configured Sheet에서 fresh-read한다.
- 저장된 SHA는 `last observed` 또는 historical integration evidence로 취급한다.
- current router가 자신의 closure SHA를 무한 추적하지 않는다.

### PR #138 exact-head verification

GitHub Actions exact head `51dbffef06f274ca319b4d23982d65c8d7753709`:

| Workflow | Run ID | Result |
|---|---:|---|
| Project Contract | 31355199653 | PASS |
| GUT 9.7.1 Tests | 31355199646 | PASS |
| Godot Tests | 31355199665 | PASS |
| Validate Thin Adapter Migration | 31355199592 | PASS |

Windows Demo Export workflow는 이 docs-only exact head에 별도 run이 생성되지 않았다. 따라서 Windows Export PASS를 #138의 신규 증거라고 기록하지 않는다.

## 검증된 개선점

### Improvement A — live-source indirection

Before:

```text
current router stores one exact main SHA
→ closure/merge changes main
→ router is stale again
```

After:

```text
current router points to LIVE_GITHUB_DEFAULT_BRANCH
+ stores exact SHA only as historical observation
```

검증: PR #138 exact-head Project Contract/GUT/Godot/Thin PASS + merge readback.

### Improvement B — semantic consumer migration

Before:

```text
machine consumer requires historical literal token
→ valid current state fails CI
```

After:

```text
consumer validates current semantic meaning
+ historical evidence remains historical
```

검증: PR #137에서 두 단계의 canonical-freshness failure가 최종 exact-head GREEN으로 전환됨.

### Improvement C — validation lane preservation

Before risk:

```text
remove obsolete immediate-task wording
→ accidentally imply validation gate completed or irrelevant
```

After:

```text
current task routing changed
AND
Android / physical runtime / human gates remain explicit NOT_RUN
```

검증: PR #137 current-state tests + #138 handoff closure.

### Improvement D — no runtime-scope leakage during handoff closure

PR #137과 #138 모두 product/gameplay/runtime implementation을 시작하지 않았다.

```yaml
sx_dec_055_godot_implementation: NOT_STARTED
runtime_integrated: false
windows_physical_runtime: NOT_RUN
android_landscape_device_smoke: NOT_RUN
connected_physical_editor: NOT_RUN
broader_human_comprehension: NOT_RUN
```

즉 handoff/canonical-freshness 복구가 승인된 runtime implementation scope를 몰래 넘지 않았다.

## Base existing-solution mapping

### BCP-2026-013

이미 소유:

- post-merge continuation-state reconciliation
- live router vs historical snapshot
- merge 후 fresh truth 재관측

Switchy가 강화한 evidence:

- self-SHA loop를 실제 project closeout에서 `LIVE_GITHUB_DEFAULT_BRANCH`로 회피
- exact-head GREEN 후 merge→post-merge closure까지 연속 검증

### BCP-2026-014

이미 소유:

- Handoff/current-state machine consumer inventory
- historical compatibility vs stale consumer
- semantic migration 또는 근거 있는 compatibility 보존

Switchy가 강화한 evidence:

- stale Android immediate-task literal과 fossilized `branch/pull_request` spelling 두 종류를 실제 CI failure에서 분리·수정
- current state를 과거 literal에 맞추지 않고 consumer를 의미 기반으로 migration한 실제 GREEN evidence

### 이번 BCP의 역할

`BCP - Switchy Express: Cargo Puzzle`은 위 두 기존 lifecycle을 대체하는 새 active owner가 아니다.

```yaml
proposal_role: PROJECT_SOURCE_CANONICAL_RECORD
recommended_absorption_targets:
  - BCP-2026-013
  - BCP-2026-014
new_active_owner: false
active_base_implementation_authorized: false
```

## 프로젝트 전용으로 남길 값

다음 값은 Base 일반 규칙으로 복사하지 않는다.

- `SX-DEC-055`
- Switchy rail/LIFO/cargo gameplay 규칙
- 73 semantic product PNG 수량
- Switchy PR #135~#138 번호
- 특정 project-hub/test 파일 경로
- 특정 workflow run ID
- Base release pin `v9.4.3`
- configured Google Sheet ID
- project-specific Android/Windows lane 명칭

## 검증 ceiling

```yaml
project_pr_137_exact_head_ci: PASS
project_pr_138_exact_head_ci: PASS
project_pr_137_merge: VERIFIED
project_pr_138_merge: VERIFIED
project_main_readback: eb07dcc39b9675a54c675694236f507a8e50e78a
sx_dec_055_runtime_implementation: NOT_STARTED
windows_physical_runtime: NOT_RUN
android_device: NOT_RUN
connected_editor: NOT_RUN
human_comprehension: NOT_RUN
base_active_implementation: NOT_AUTHORIZED
```

## Source references

- Project PR #137: handoff refresh + semantic canonical-freshness consumer migration
- Project PR #138: post-merge live-source reconciliation and self-SHA-loop avoidance
- Project main observed: `eb07dcc39b9675a54c675694236f507a8e50e78a`
- Configured Sheet: `SX-DEC-055`, `SX-AUD-035` records preserve the same project verification boundary

이 evidence는 실제 검증 범위를 넘어 성공을 확대하지 않는다. Base proposal 병합은 이 학습을 Registry에 보존하는 단계이며 active Base behavior 변경은 별도 승인 대상이다.
