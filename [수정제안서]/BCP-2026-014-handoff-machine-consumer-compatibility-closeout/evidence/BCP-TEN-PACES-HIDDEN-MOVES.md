# BCP - Ten-Paces-Hidden-Moves

## 역할

이 파일은 새 Base Change Proposal을 만들지 않는다.

현재 Base main의 `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`이 이미 같은 공용 문제를 소유하므로, Ten Paces 프로젝트에서 관찰된 독립 근거를 해당 proposal의 보강 증거로 추가한다.

```yaml
source_project: alsdmlals4-eng/Ten-Paces-Hidden-Moves
source_project_main: dc95883873ccd8718f6aa5cb11f936ef39db42c7
related_project_prs:
  - 135
  - 136
existing_solution_verdict: REUSE_BCP_2026_014
new_base_behavior: false
new_broad_skill: false
```

## 프로젝트 관찰 1 — Handoff 압축과 machine-consumed surface

Ten Paces PR #135는 오래된 장문 Active Context/Handoff를 현재 상태 중심의 압축 router로 정리했다.

그 과정에서 사람이 보기에 과거 정보나 중복처럼 보이던 일부 표식이 실제로는 validator·reference-freshness·다음 세션 discovery가 소비하는 계약 표면임이 exact-head CI에서 드러났다.

복구 과정에서는 표식을 다음 책임으로 분리해야 했다.

```text
CURRENT_MUTABLE
CANONICAL_LOCATOR
HISTORICAL_DISCOVERY
COMPATIBILITY_ANCHOR
SAFE_TO_DROP
```

핵심은 stale 값을 current truth로 되살리는 것이 아니었다.

- current mutable state는 실제 repository truth를 유지한다.
- canonical semantics는 해당 canonical owner가 계속 소유한다.
- machine/human consumer가 실제로 필요한 최소 locator나 historical discovery anchor만 비-current 역할로 보존한다.
- consumer가 없는 surface는 제거 후보가 된다.

PR #135 최종 exact head:

```text
c18d384b537ec3eaf49370d454d23e98c44ba3f4
```

병합 commit:

```text
69eba09c6d18f5b4a473c0be14361ddd745983a0
```

최종 exact head에서 관련 PR Validation과 canonical/reference 계열 검증이 GREEN이었고 unresolved review thread는 0이었다.

## 프로젝트 관찰 2 — producer 보존보다 semantic consumer migration이 맞는 경우

PR #135 병합 뒤 `Validate Godot Live-Editor Pilot`의 기존 실패를 조사하면서 같은 문제의 반대편이 확인됐다.

현재 `project.godot`은 승인된 Godot AI + GUT + Hera 공존 상태였지만 legacy test는 Godot AI가 editor plugin 배열의 유일한 값이어야 한다는 과거 literal shape를 검사했다.

실제 계약은 다음이었다.

```text
Godot AI plugin remains installed and registered.
```

따라서 producer를 과거 singleton 배열로 되돌리지 않고 consumer assertion을 semantic presence check로 변경했다.

이 실패는 PR #135 이전 main에서도 이미 존재했다.

```text
prior main: 43841d3cc6667d821c10df75272b239f314f3df0
prior failing run: 31349838418
```

PR #136 exact head:

```text
4b9b12554b236c42ef24fa00d77af0c13c3406f7
```

해당 exact head에서 다음이 모두 성공했다.

- `Validate Godot Live-Editor Pilot`
- `PR Validation`
- `Full Validation`
- active toolchain/product/platform regressions

unresolved review thread는 0이었다.

PR #136 병합 commit:

```text
dc95883873ccd8718f6aa5cb11f936ef39db42c7
```

post-merge main run `31353193715`에서 `adoption-contract`와 reusable `project-pilot` job도 모두 성공했다.

## BCP-2026-014와의 정합성

Urban Legend 기반 기존 BCP-2026-014는 Handoff refresh/closeout 전에 machine consumer inventory를 수행하고, current authority / historical compatibility / stale-remove를 분리한 뒤 exact-head contract validation을 거치는 lifecycle을 제안한다.

Ten Paces의 독립 관찰은 이 원칙과 정합적이다.

```text
HANDOFF OR ACTIVE CONTEXT REWRITE
→ INVENTORY DOWNSTREAM CONSUMERS
→ CLASSIFY SURFACES
→ PRESERVE REQUIRED COMPATIBILITY OR MIGRATE CONSUMER
→ KEEP CURRENT TRUTH CURRENT
→ EXACT-HEAD VALIDATION
→ CLOSEOUT
```

Ten Paces는 추가로 다음 제한을 명확히 보여준다.

> brittle consumer가 accidental text shape를 검사하는 경우에는 compatibility token을 계속 쌓기보다 consumer를 실제 semantic contract로 migration하는 편이 맞을 수 있다.

즉 기존 BCP-2026-014를 새 proposal로 복제하지 않고, 해당 proposal의 검증 근거를 보강하는 것이 적절하다.

## 프로젝트 전용으로 남길 값

Base 공용 규칙으로 승격하지 않는다.

- Ten Paces의 `3/3/4` 전투 수치.
- PR #135 / #136 자체 번호.
- 특정 Active Context field 이름.
- `docs/02_COMBAT_RULES.md` 같은 프로젝트 경로.
- Godot AI/GUT/Hera의 프로젝트별 plugin 배열.
- Android/device/human gate 상태.

## 검증 ceiling

```yaml
ten_paces_failure_mode: OBSERVED
focused_project_fix: EXACT_HEAD_GREEN_AND_MERGED
post_merge_live_editor_pilot: PASS
cross_project_alignment_with_existing_bcp014: CONFIRMED_BY_CURRENT_REVIEW
base_active_implementation: NOT_RUN
human_usability_validation: NOT_RUN
```
