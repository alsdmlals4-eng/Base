# BCP-2026-014 — Handoff Contract-Surface Preservation

## 출처와 상태

- Proposal ID: `BCP-2026-014-handoff-contract-surface-preservation`
- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 출처 프로젝트 기준 main: `dc95883873ccd8718f6aa5cb11f936ef39db42c7`
- 관련 프로젝트 PR: `#135`, `#136`
- 관련 owner: 기존 `maintaining-project-context-and-handoff`
- supporting owner: `auditing-canonical-reference-freshness`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- Knowledge Level: `PATTERN`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 동작을 수정하지 않는다. 쓰기 범위는 `[수정제안서]/**`뿐이며 실제 Skill·Method·Test·Tool·Workflow 구현은 별도 후속 승인 단계다.

## 관찰과 증거

### Problem

Active Context/Handoff를 장문 정본 복제에서 압축된 current-state router로 정리할 때, 현재 상태가 아니거나 중복처럼 보이는 문자열을 단순 삭제하면 validator·reference-freshness·routing·다음 작업자의 discovery가 의존하는 **machine-consumed contract surface**까지 제거될 수 있다.

Ten Paces PR #135에서 실제로 다음이 발생했다.

1. stale/current 상태를 분리하고 제품 규칙 전문을 해당 canonical owner로 돌려보내는 context compression을 수행했다.
2. 의미는 더 간결해졌지만 기존 회귀가 소비하던 일부 locator/lineage/current-state marker도 함께 사라졌다.
3. exact-head PR Validation이 누락 표식을 순차적으로 적발했다.
4. 해결은 과거 상태를 current로 복원하는 것이 아니라 **현재 mutable state와 historical/discovery compatibility anchor를 분리**하고 필요한 locator만 보존하는 것이었다.
5. 최종 exact head `c18d384b537ec3eaf49370d454d23e98c44ba3f4`에서 관련 검증이 GREEN이 되었고 PR #135는 `69eba09c6d18f5b4a473c0be14361ddd745983a0`으로 병합됐다.

발견된 surface 유형은 한 종류가 아니었다.

```text
CURRENT_MUTABLE
CANONICAL_LOCATOR
HISTORICAL_DISCOVERY
COMPATIBILITY_ANCHOR
SAFE_TO_DROP
```

예를 들어 프로젝트의 combat timing locator, 과거 lineage marker, canonical owner locator, 현재 제품 검증 상태 marker 등이 서로 다른 이유로 소비되고 있었다. 이 proposal은 그 프로젝트 고유 문자열 자체를 Base 규칙으로 만들지 않는다.

### Complementary consumer-side evidence

PR #135 병합 뒤 `Validate Godot Live-Editor Pilot`의 기존 실패도 같은 원리의 반대편을 보여줬다.

현재 `project.godot`은 승인된 Godot AI + GUT + Hera 공존 상태였지만 legacy pilot test는 editor plugin 배열 전체가 Godot AI 하나뿐인 과거 표현이어야 한다고 assertion했다. 실제 보존 계약은 “Godot AI가 설치·등록되어 있다”였다.

이 실패는 이전 main `43841d3c...` run `31349838418`에서도 존재했고, PR #135가 만든 회귀가 아니었다.

PR #136은 test 삭제나 product state rollback 없이 consumer assertion을 semantic presence check로 좁혔다.

- exact head: `4b9b12554b236c42ef24fa00d77af0c13c3406f7`
- exact-head PR Validation: `SUCCESS`
- exact-head Full Validation: `SUCCESS`
- exact-head Live-Editor Pilot: `SUCCESS`
- unresolved review threads: `0`
- merge main: `dc95883873ccd8718f6aa5cb11f936ef39db42c7`
- post-merge Live-Editor run `31353193715`: adoption-contract `SUCCESS`, project-pilot `SUCCESS`

즉 producer 문자열을 무조건 보존하는 것도 정답이 아니다. **실제 semantic contract를 먼저 식별한 뒤 producer surface를 보존하거나 consumer를 migration**해야 한다.

### Root Cause

문서 압축을 단순 요약으로 취급하면 다음 잘못된 추론이 생긴다.

```text
"현재 상태가 아니다"
→ 삭제 가능
```

더 안전한 판정은 다음이다.

```text
"현재 상태가 아니다"
→ current-state 섹션에서는 제거 가능
→ downstream consumer 존재?
   ├─ YES → historical/discovery/compatibility role로 보존 또는 consumer migration
   └─ NO  → SAFE_TO_DROP 후보
```

따라서 semantic compression과 contract-surface removal은 별도 판단이다.

## 일반화 후보

### Proposed General Rule

Live continuation owner를 압축·재작성하기 전에 contract-surface inventory를 수행한다.

```text
READ LIVE OWNER
→ INVENTORY DOWNSTREAM CONSUMERS
→ CLASSIFY SURFACES
→ COMPRESS CURRENT STATE
→ PRESERVE OR MIGRATE REQUIRED NON-CURRENT ANCHORS
→ DO NOT REVIVE STALE STATE AS CURRENT
→ RUN REFERENCE/CONTRACT REGRESSION ON EXACT HEAD
→ MERGE
→ BCP-013 POST-MERGE RECONCILE IF APPLICABLE
```

핵심 invariant:

1. `CURRENT_MUTABLE`은 현재 repository truth와 모순되면 안 된다.
2. 제품/도메인 전문은 canonical owner에 남기고 live router에는 필요한 최소 locator만 둔다.
3. consumer가 accidental literal shape를 검사하고 있다면 producer를 fossilize하기보다 semantic consumer migration을 우선 검토한다.
4. consumer가 없고 canonical 책임이 다른 곳에 있으며 reference/test scan이 clean이면 `SAFE_TO_DROP`을 허용한다.

### Existing Base Coverage

현행 `maintaining-project-context-and-handoff`는 이미 context-refresh, session-handoff, resume, runtime truth, compressed router를 책임진다. 따라서 새 broad Skill은 필요 없다.

`auditing-canonical-reference-freshness`는 stale/untouched consumer 탐색을 지원할 수 있다.

### BCP-013과의 경계

`BCP-2026-013-post-merge-continuation-state-reconciliation`은 같은 owner를 사용하지만 trigger가 다르다.

- BCP-013: merge/integration **후** main SHA·PR state·post-merge CI 등 live truth가 변해 state가 stale.
- BCP-014: context/handoff rewrite/compression **중** downstream consumer가 필요로 하는 locator/lineage/semantic contract surface가 사라짐.

PR #135의 failure는 merge 전 exact head에서 이미 발생했으므로 BCP-013만으로 막을 수 없다.

### Project-Specific Boundary

Base에 승격하지 않을 값:

- Ten Paces의 `3/3/4` 및 전투 규칙.
- 특정 PR/Issue 번호와 과거 상태 문자열.
- 프로젝트의 `ACTIVE_CONTEXT.md` field 이름.
- 특정 canonical path.
- Godot AI/GUT/Hera의 프로젝트별 plugin 배열.
- Android/device/human gate 상태.

Base는 consumer inventory, current/history 분리, safe deletion, semantic migration 원리만 소유한다.

## 적용 조건과 비사용 조건

### Use When

- `ACTIVE_CONTEXT`, `CURRENT_STATUS`, `HANDOFF`, resume manifest 같은 live router를 크게 압축·재구성할 때.
- 해당 문서가 machine test, parser, freshness checker, search-based router 또는 다음 세션 discovery 입력일 때.
- canonical owner 전문을 옮기면서 locator나 책임 경로가 달라질 때.
- historical lineage를 삭제하면 provenance/ownership discovery가 약화될 때.
- 기존 consumer가 literal string에 의존할 가능성이 있을 때.

### Do Not Use When

- 문서가 current router가 아니라 시점이 명확한 historical snapshot일 때.
- downstream consumer가 없고 archive/canonical owner가 따로 있을 때.
- repository/reference/test scan으로 dead surface임을 증명했을 때.
- greenfield owner라 compatibility surface가 아직 없을 때.
- 단순 formatting/오탈자처럼 contract 의미가 바뀌지 않을 때.

## 반례와 위험

### Counterexamples

1. **Safe deletion**: 오래된 문장이 어느 parser/test/link/search route에서도 소비되지 않고 동일 사실이 canonical owner에 있으면 별도 compatibility anchor 없이 삭제할 수 있다.
2. **Historical snapshot**: dated pre-merge report가 당시 SHA/PR 상태를 기록했다면 최신 상태로 rewrite하면 오히려 역사 증거를 훼손한다.
3. **Wrong consumer**: test가 `enabled=[A]`라는 accidental shape를 요구하지만 실제 계약은 `A 포함`이고 B/C 공존이 승인됐다면 producer를 singleton으로 되돌리지 않고 consumer를 고친다.

### Risks and controls

- **문서 비대화**: 모든 옛 문자열을 보존하면 router가 다시 장문화된다. → 실제 consumer가 있는 surface만 보존하고 owner locator를 선호한다.
- **brittle-string 제도화**: literal test 때문에 잘못된 표현을 영구화할 수 있다. → semantic intent를 먼저 판정하고 consumer migration을 허용한다.
- **hidden consumer**: 단순 text search만으로 모든 소비자를 찾지 못할 수 있다. → Registry/routing/freshness/test/workflow를 함께 조사하고 exact-head CI를 사용한다.
- **운영 복잡도**: 분류어를 모든 프로젝트에 고정 schema로 강제할 수 있다. → Base 구현 시 필드명보다 질문/책임 분리를 우선한다.
- **BCP-013 중복**: owner가 같아 lifecycle이 겹칠 수 있다. → pre-merge rewrite와 post-merge integration trigger를 분리한다.

## 영향 범위와 검증

### 승인 후 영향 후보

본 proposal 단계에서는 아래를 수정하지 않는다.

- `skills/maintaining-project-context-and-handoff/SKILL.md`: context-refresh/session-handoff 전에 consumer/surface inventory 단계 후보.
- `auditing-canonical-reference-freshness` 관련 surface: supporting reference scan 후보.
- handoff/context Method/reference: current vs historical/discovery compatibility 설명 후보.
- focused regression tests: locator 보존, stale current state 부활 금지, semantic consumer migration 허용.
- Registry/generated consumer: 실제 active Skill body가 바뀌는 별도 구현 단계에서만 현행 Base 규칙에 따라 동기화.

신규 broad Skill은 영향 후보가 아니다.

### Validation Plan — 별도 구현 승인 후

1. **Compression with machine consumer**: 중복 prose를 줄여도 필요한 locator는 보존되거나 consumer가 migration되고 exact-head regression이 통과한다.
2. **Historical lineage**: provenance marker는 historical/discovery role에 둘 수 있지만 current field는 실제 repository truth를 유지한다.
3. **Dead surface**: consumer 0이 확인되면 compatibility boilerplate 없이 삭제 가능하다.
4. **Brittle consumer**: accidental text shape assertion은 semantic intent assertion으로 migration하고 RED→GREEN 증거를 남긴다.
5. **Post-merge transition**: merge 뒤 live truth가 달라진 경우 BCP-013 lifecycle이 별도로 적용된다.

### Regression Plan

- canonical owner가 full domain semantics를 계속 소유한다.
- historical snapshot은 current router와 혼동하지 않는다.
- 프로젝트에 machine-consumed handoff surface가 없으면 불필요한 compatibility section을 강제하지 않는다.
- test 삭제·skip·약화만으로 Green을 만들지 않는다.
- current truth를 historical anchor 때문에 과거 상태로 되돌리지 않는다.

### Benchmark

상세 evidence는 `evidence/INDUSTRY_AND_PROJECT_EVIDENCE.md`가 책임진다.

- Google Engineering Practices: self-contained small change + related test → focused repair/rollback 원리만 `ADOPT`.
- GitHub required status checks: latest required SHA 검증 → contract rewrite 뒤 exact-current-head evidence를 `ADOPT`.
- AWS ADR guidance: history/supersession 보존 → current state와 provenance 분리를 `ADAPT`.
- Kubernetes deprecation policy: consumed surface의 compatibility-aware removal discipline → analogy로만 `ADAPT`; 문서 field에 API version/deprecation 기간은 강제하지 않는다.

### Knowledge ceiling

```yaml
knowledge_state: PATTERN
second_independent_project_pilot: NOT_RUN
human_usability_validation: NOT_RUN
base_active_implementation: NOT_RUN
```

한 프로젝트에서 여러 validation failure가 같은 원리를 반복 노출했고 프로젝트 fix는 exact-head 및 merge로 검증됐지만, 두 번째 프로젝트 pilot이 없어 `VALIDATED_PATTERN`으로 올리지 않는다.

## 승인과 구현

```yaml
proposal_status: SUBMITTED
proposal_storage_merge_authority: GRANTED_BY_CURRENT_SINGLE_FILE_INSTRUCTION
approval_ref: null
implementation_pr: null
active_base_behavior_changed: false
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
implementation_status: NOT_STARTED_IN_THIS_STAGE
implementation_boundary: SEPARATE_FOLLOWUP_STAGE
```

이 proposal-only PR의 Base main 병합은 **제안 기록 저장**만 의미한다. `APPROVED_FOR_IMPLEMENTATION`이 아니며 Base 활성 Skill/Test/Method/Tool/Workflow 변경은 별도 후속 사용자 승인/실행지시문에서만 수행한다.