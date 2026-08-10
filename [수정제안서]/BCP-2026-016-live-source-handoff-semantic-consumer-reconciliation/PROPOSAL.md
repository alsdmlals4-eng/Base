# BCP - Switchy Express: Cargo Puzzle

## 출처와 상태

- Proposal ID: `BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation`
- 사용자 표시명: `BCP - Switchy Express: Cargo Puzzle`
- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 출처 프로젝트 기준 main: `eb07dcc39b9675a54c675694236f507a8e50e78a`
- 관련 프로젝트 Decision: `SX-DEC-055`
- 관련 프로젝트 PR: `#137`, `#138`
- 이전 Base evidence PR: `#245`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `PROJECT_VALIDATED_PATTERN`
- Existing Solution Verdict: `ABSORB_EXISTING_OWNERS`
- 관련 기존 proposal: `BCP-2026-013-post-merge-continuation-state-reconciliation`, `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 Switchy Express: Cargo Puzzle에서 실제로 검증된 **live handoff source-of-truth, post-merge continuation reconciliation, machine-consumer semantic migration, validation-ceiling 보존**을 프로젝트 출처형 Base Change Proposal로 등록한다.

이전 Base PR #245에서는 Switchy 학습을 BCP-013의 하위 evidence로만 저장했다. 그러나 사용자의 최신 운영 규칙은 프로젝트별 수정제안서를 `BCP - 프로젝트 이름`으로 별도 등록하고 Registry lifecycle을 갖도록 요구한다. 따라서 본 제안은 기존 BCP-013/014의 proposal 본문과 활성 Base 규칙을 수정하지 않고, Switchy evidence만 별도 canonical proposal로 이동·등록한다.

본 proposal의 병합은 **제안 저장과 Registry 등록만** 의미한다. Base의 활성 Skill·Method·Template·Test·Tool·Workflow를 바꾸지 않으며, 실제 공용 동작 흡수는 별도 승인과 별도 구현 PR이 필요하다.

## 관찰과 증거

Switchy Express의 `SX-DEC-055 Runtime Semantic POC`는 설계와 Definition of Ready까지 승인·병합되었으나, 사용자의 지시로 실제 Godot/GDScript runtime 구현은 보류되었다. 이 상태를 다음 세션이 정확히 재개할 수 있도록 handoff/cold-start 정본을 갱신하는 과정에서 공용화 가치가 있는 실패와 복구가 재현됐다.

### 1. 현재 작업을 과거 literal token이 가로막는 canonical-freshness 실패

프로젝트 PR #137에서 `START_HERE.md`, `ACTIVE_CONTEXT.md`, `ROADMAP.md`를 현재 `SX-DEC-055 USER_DEFERRED_AFTER_DOR` 상태로 갱신하자 기존 regression이 오래된 Android immediate-task 문자열을 요구하며 실패했다.

잘못된 복구는 현재 상태를 다시 과거 문자열에 맞추는 것이다. 실제 복구는 Android Device Smoke를 별도 `OPEN_NOT_RUN` lane으로 유지하면서 테스트가 현재 의미를 검증하도록 수정하는 것이었다.

### 2. literal field spelling과 semantic current-state contract의 충돌

다음 단계에서는 오래된 post-merge consumer가 `branch: main`, `pull_request_83: MERGED` 같은 특정 문자열 모양 자체를 current contract로 강제했다.

프로젝트는 current repository semantics와 historical evidence를 분리하도록 consumer를 migration했다.

```text
fossilized literal consumer
→ current semantic contract + historical evidence preservation
```

PR #137 exact head `7be35adf4fa98bb915616a1e6a89f67dcb19a4ca`에서 다음 GitHub Actions가 모두 PASS했다.

- Project Contract `31354096765`
- GUT 9.7.1 Tests `31354096767`
- Godot Tests `31354096757`
- Validate Thin Adapter Migration `31354096769`
- Windows Demo Export `31354096778`

### 3. merge가 handoff 안의 integration metadata를 즉시 historical로 만드는 stale edge

PR #137이 merge되면서 project main은 `32a0d6c154188f36bdefdefe96e62bc2a4718565`가 되었다. 이때 PR head에서 정확했던 저장된 baseline/PR 관측값은 더 이상 live current truth가 아니었다.

```text
LIVE_STATE_VALID_AT_EXACT_HEAD
+ MERGE
= SAVED_INTEGRATION_METADATA_BECOMES_HISTORICAL
```

### 4. self-SHA loop를 피하는 live-source indirection

후속 프로젝트 PR #138은 current router가 자기 closure commit SHA를 계속 추적하지 않도록 다음 원칙을 적용했다.

```yaml
current_main_source: LIVE_GITHUB_DEFAULT_BRANCH
saved_sha: historical observation only
```

즉 현재 main은 GitHub default branch에서 fresh-read하고, 저장된 SHA는 관측 시점의 증거로만 유지한다.

PR #138 exact head `51dbffef06f274ca319b4d23982d65c8d7753709`에서 다음 workflow가 PASS했다.

- Project Contract `31355199653`
- GUT 9.7.1 Tests `31355199646`
- Godot Tests `31355199665`
- Validate Thin Adapter Migration `31355199592`

#138은 정확히 두 개의 project-hub 문서만 변경했고 runtime/product bytes를 변경하지 않았다. merge 후 project main은 `eb07dcc39b9675a54c675694236f507a8e50e78a`로 관측됐다.

### 5. 자동화 증거 ceiling 보존

Switchy의 handoff 복구는 자동 PASS를 실제 device/runtime/human PASS로 확대하지 않았다.

```yaml
windows_demo_export: PASS_AS_PACKAGING_EVIDENCE
windows_physical_runtime: NOT_RUN
android_landscape_device_smoke: NOT_RUN
connected_physical_editor: NOT_RUN
broader_human_comprehension: NOT_RUN
sx_dec_055_runtime_implementation: NOT_STARTED
runtime_integrated: false
```

상세 project-specific timeline과 검증값은 `evidence/SWITCHY_EXPRESS_HANDOFF_RECONCILIATION_EVIDENCE.md`에 보존한다.

## 일반화 후보

### Live-Source Handoff + Semantic Consumer Reconciliation Contract

현재 상태를 전달하는 Handoff/Active Context를 갱신하거나 병합할 때 다음 lifecycle을 공용 후보로 제안한다.

```text
FRESH_AUTHORITY_READ
→ CLASSIFY_LIVE_ROUTER_VS_HISTORICAL_SNAPSHOT
→ INVENTORY_MACHINE_CONSUMERS
→ UPDATE_CURRENT_ROUTER
→ MIGRATE_LITERAL_CONSUMERS_TO_SEMANTIC_CONTRACT_OR_PRESERVE_EVIDENCED_COMPATIBILITY
→ EXACT_HEAD_VALIDATION
→ MERGE / INTEGRATION
→ RE-OBSERVE_LIVE_REPOSITORY_TRUTH
→ RECONCILE_CONTINUATION_STATE
→ PRESERVE_VALIDATION_CEILINGS
→ CLOSE
```

핵심 invariant는 다음과 같다.

1. **Live router는 저장된 SHA보다 fresh repository truth를 우선한다.**
2. **Historical snapshot은 과거 사실로 보존하며 current router와 역할을 섞지 않는다.**
3. **Machine consumer는 특별한 이유가 없으면 field spelling이 아니라 의미를 검증한다.**
4. **Compatibility token을 유지할 때는 실제 consumer 근거가 있어야 한다.**
5. **merge 이후에는 integration metadata를 다시 관측하기 전 current truth라고 단정하지 않는다.**
6. **자동 export/contract PASS를 physical/device/human PASS로 승격하지 않는다.**
7. **current router가 자신의 closure SHA를 무한 추적하도록 설계하지 않는다.**

### Existing Solution First

이 제안은 새 broad Skill을 요구하지 않는다.

- `BCP-2026-013`은 post-merge continuation-state reconciliation과 live/historical state 분리를 이미 소유한다.
- `BCP-2026-014`는 Handoff/Active Context 변경 시 machine-consumer compatibility inventory와 semantic migration 경계를 이미 다룬다.
- Switchy가 추가로 제공하는 가치는 두 lifecycle이 **동일 실제 프로젝트에서 연속으로 실패→수정→exact-head GREEN→post-merge closure까지 검증된 결합 evidence**다.

따라서 승인 후 구현 방향도 기존 owner에 흡수하는 것을 우선한다.

```yaml
new_broad_skill: false
new_parallel_handoff_owner: false
recommended_future_action: ABSORB_INTO_EXISTING_OWNERS
```

## 적용 조건과 비사용 조건

### Use When

- `ACTIVE_CONTEXT`, `CURRENT_STATUS`, `START_HERE`, resume manifest 등 다음 세션이 current truth로 읽는 live router를 수정한다.
- merge로 main SHA, PR state, active baseline 또는 CI state가 바뀐다.
- 테스트·validator·workflow가 handoff/current-state 문서를 machine-consume한다.
- current semantic truth와 historical compatibility token을 구분해야 한다.
- docs-only closure가 runtime/device/human evidence와 함께 기록된다.

### Do Not Use When

- 문서가 명시적인 point-in-time historical report이고 current router 역할을 하지 않는다.
- machine consumer가 전혀 없는 단순 설명 문서다.
- literal token 자체가 공개 API/파일 포맷/외부 consumer 계약으로 명시적으로 승인된 경우다.
- 외부 시스템이 current-state router를 자동 생성하고 freshness를 보장한다.
- 실제 현재 truth를 확인할 수 없어 추정만 가능한 경우다. 이때는 `UNVERIFIED` 또는 동등 상태로 남긴다.

## 반례와 위험

### Counterexample 1 — historical report

`2026-08-10-pre-merge-review.md`가 당시 `head=abc123`을 기록했다면 이후 main이 바뀌어도 그 값은 유효한 history다. live router처럼 rewrite할 필요가 없다.

### Counterexample 2 — real external schema

외부 도구가 정확히 `branch` 필드를 요구하는 공개 schema를 가진다면 field spelling은 의미 없는 fossil이 아니다. 이 경우 consumer migration보다 호환 보존 또는 명시적 schema migration이 필요하다.

### Risks

- semantic migration이라는 이유로 실제 compatibility contract를 임의 삭제할 수 있다.
- 모든 merge마다 follow-up commit을 만들면 self-SHA churn이 발생한다.
- current source를 live-read로 바꾸면서 historical evidence를 잃을 수 있다.
- CI PASS가 runtime/device/human PASS처럼 보이게 문서가 단순화될 수 있다.
- BCP-013/014와 역할이 중복된 새 active owner를 만들 위험이 있다.

### Controls

- consumer inventory를 먼저 수행한다.
- historical evidence와 live router를 구조적으로 분리한다.
- exact SHA는 필요할 때 `last_observed` evidence로 기록하고 current source는 stable authority로 표현한다.
- evidence ceiling을 상태별로 분리한다.
- 본 proposal 자체는 existing owner absorption만 제안하며 active implementation을 승인하지 않는다.

## 영향 범위와 검증

### 본 proposal PR의 영향 범위

허용 변경은 `[수정제안서]/**`에 한정한다.

- 새 `PROPOSAL.md`
- 새 Switchy project evidence
- Proposal Registry entry
- BCP-013 아래 잘못 배치된 기존 Switchy evidence 제거

변경하지 않는 것:

- Base ACTIVE Skill
- Base Method
- Base Template
- Base Test
- Base Tool
- Base Workflow
- `START_HERE.md`
- `AGENTS.md`
- release lock / frozen snapshot
- Godot/project runtime behavior

### 승인 후 후보 영향 범위

별도 구현 승인이 내려질 경우 우선 검토 대상은 기존 owner다.

- `skills/maintaining-project-context-and-handoff/SKILL.md`
- `skills/auditing-canonical-reference-freshness/SKILL.md`
- 관련 기존 contract regression
- 필요 시 method/learning-log companion

새 Skill이나 자동 writer는 기본값이 아니다.

### Verification scenarios

#### Scenario A — literal consumer is stale

Given current router 의미는 올바르지만 오래된 test가 과거 field spelling만 요구한다.

Expected: 실제 consumer 요구를 확인한 뒤 의미 기반 contract로 migration하거나 evidential compatibility를 유지한다. current state를 과거 상태로 되돌리지 않는다.

#### Scenario B — merged handoff

Given live router가 PR head 기준 current state를 기록하고 PR이 merge된다.

Expected: merge 직후 저장된 integration metadata를 historical observation으로 취급하고 current repository truth를 fresh-read한다.

#### Scenario C — self-SHA loop

Given follow-up closure commit이 main SHA를 또 변경한다.

Expected: current router는 `LIVE_GITHUB_DEFAULT_BRANCH`와 같은 stable source authority를 사용하고 자기 SHA를 영구 추적하지 않는다.

#### Scenario D — evidence ceiling

Given docs/contract/export CI가 PASS한다.

Expected: physical runtime, Android device, connected editor, human comprehension은 실제로 실행하지 않았다면 `NOT_RUN`을 유지한다.

### Compatibility

이 proposal은 기존 BCP-013/014의 의미를 변경하지 않는다. 향후 구현이 승인되더라도 기존 live router가 없는 프로젝트에는 적용을 강제하지 않는다.

### Rollback

제안 단계 롤백은 새 proposal/evidence/Registry entry를 제거하고, 필요하다면 Switchy historical evidence를 이전 위치로 되돌리는 것으로 충분하다. 활성 Base 동작은 변경되지 않는다.

## 승인과 구현

```yaml
proposal_status: APPROVED_FOR_IMPLEMENTATION
proposal_storage_and_merge_authority: USER_DIRECTED_2026_08_10
approval_ref: docs/superpowers/specs/2026-08-10-approved-base-continuity-diagnostics-actions-design.md
implementation_pr: null
active_base_behavior_changed: false
active_base_implementation_authorized: true
```

제안 등록 당시 사용자의 지시는 **프로젝트 출처형 proposal 작성·Registry 등록·proposal-only PR 검증·병합**까지만 승인했다. 현재는 위 `approval_ref`의 별도 승인으로 BCP-014 및 기존 handoff/freshness owner에 흡수하는 실제 구현 PR을 진행할 수 있다. 이 승인 기록 PR 자체는 관련 Skill·Method·Test·Workflow를 변경하지 않는다.
