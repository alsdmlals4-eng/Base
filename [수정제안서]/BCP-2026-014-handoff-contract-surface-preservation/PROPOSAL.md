# BCP-2026-014 — Handoff Contract-Surface Preservation

## 출처와 상태

- Proposal ID: `BCP-2026-014-handoff-contract-surface-preservation`
- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 출처 프로젝트 기준 main: `dc95883873ccd8718f6aa5cb11f936ef39db42c7`
- 관련 프로젝트 PR: `#135`, `#136`
- 관련 현재 owner:
  - `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
  - `[기획서]/00_프로젝트_허브/HANDOFF.md`
- 관련 프로젝트 검증:
  - `tests/check_canonical_combat_docs.py`
  - `tests/test_godot_live_editor_adoption.py`
  - PR Validation / canonical reference freshness 계열
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- Knowledge Level: `PATTERN`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow·Tool을 수정하지 않는다. 이 PR에서 허용되는 쓰기는 `[수정제안서]/**`뿐이며, 실제 Base 동작 변경은 별도 승인·별도 구현 단계다.

## 관찰과 증거

### Problem

Active Context/Handoff를 오래된 장문 정본 복제에서 **압축된 current-state router**로 정리하는 과정에서, 현재 mutable state가 아니어 보이는 문자열을 단순 삭제하면 downstream validator·reference-freshness·다음 작업자의 discovery가 의존하는 **machine-consumed contract surface**까지 함께 사라질 수 있다.

Ten Paces PR #135는 정확히 이 실패를 반복적으로 드러냈다.

1. 기존 `ACTIVE_CONTEXT.md`의 stale/current 상태를 정리하고, 제품 규칙 전문을 책임 원본으로 돌려보내는 압축을 수행했다.
2. 문서의 의미는 더 간결해졌지만, 기존 회귀가 discovery/lineage locator로 소비하던 표식 일부도 함께 제거됐다.
3. exact-head PR Validation이 누락된 current/historical discovery surface를 순차적으로 적발했다.
4. 해결은 과거 상태를 current로 되살리는 것이 아니었다. **현재 상태와 역사·발견용 호환 표식을 분리하고, 필요한 locator만 명시적으로 보존**했다.
5. 최종 exact head `c18d384b537ec3eaf49370d454d23e98c44ba3f4`에서 관련 PR 검증이 GREEN이 되었고 PR #135가 merge commit `69eba09c6d18f5b4a473c0be14361ddd745983a0`으로 병합됐다.
6. 병합 직후 별도 pre-existing workflow 실패를 조사하면서도 같은 원리가 재확인됐다. `project.godot`은 Godot AI + GUT + Hera 공존 상태였지만 legacy pilot test는 Godot AI 단독 배열을 exact-string으로 요구해 이전 main부터 계속 실패했다. PR #136은 consumer의 실제 계약을 “Godot AI 보존”으로 복원하여 exact head GREEN 후 `dc95883873ccd8718f6aa5cb11f936ef39db42c7`에 병합됐다.

두 사례의 공통점은 다음이다.

```text
HUMAN_INTENT
!=
ACCIDENTAL_TEXT_SHAPE

BUT

MACHINE_CONSUMED_CONTRACT_SURFACE
must be inventoried before deletion or compression.
```

### PR #135에서 보존이 필요했던 표식 유형

실제 수정 과정에서 다음 종류의 표식이 회귀 계약에 의해 발견됐다.

- historical lineage locator: 과거 PR/Issue/검토 상태 표식
- canonical owner locator: `docs/02_COMBAT_RULES.md`
- current mutable state token: `latest_combat_planning_runtime: PRODUCT_VALIDATION_AUTOMATED`
- 핵심 규칙 discovery token: `3/3/4`
- 제품·관찰·성장 소비자가 찾아야 하는 권위 표식

중요한 점은 이들을 모두 current state로 유지한 것이 아니라는 것이다.

```text
CURRENT_MUTABLE
CANONICAL_LOCATOR
HISTORICAL_DISCOVERY
COMPATIBILITY_ANCHOR
SAFE_TO_DROP
```

로 책임을 분리한 뒤, current truth와 충돌하지 않는 형태로 필요한 표식만 보존했다.

### Root Cause

원인은 handoff/context 압축을 **문서 요약 문제**로만 취급하고, 해당 문서가 이미 갖고 있던 downstream contract를 inventory하지 않은 것이다.

```text
"이 내용은 현재 상태가 아니다"
→ 삭제 가능
```

은 성립하지 않는다.

더 정확한 판정은 다음이다.

```text
"이 내용은 현재 상태가 아니다"
→ current-state 섹션에서는 제거 가능
→ 그러나 historical/discovery/reference consumer가 있는가?
   ├─ YES → 올바른 책임 섹션/owner locator로 보존 또는 consumer migration
   └─ NO  → SAFE_TO_DROP 후보
```

즉 **semantic compression**과 **contract-surface removal**은 별도 작업이다.

## Existing Base Coverage

현행 Base의 `maintaining-project-context-and-handoff`는 이미 다음을 책임진다.

- Active Context와 Handoff를 장문 정본 복제가 아닌 압축 router로 유지
- runtime truth 재확인
- current / verified / pending / risk / next work 분리
- context-refresh / session-handoff / resume
- actual repo/project state가 stale Handoff보다 우선

`auditing-canonical-reference-freshness`는 canonical source 변경 뒤 stale/untouched consumer를 찾는 공용 책임을 가진다.

또한 `BCP-2026-013-post-merge-continuation-state-reconciliation`은 **integration 뒤 live continuation state가 새 main truth와 즉시 어긋나는 self-invalidating edge**를 제안한다.

### BCP-013과의 경계

두 proposal은 owner가 같지만 trigger가 다르다.

| Proposal | Trigger | Failure |
|---|---|---|
| BCP-013 | merge/integration 이후 | main SHA·PR state·post-merge CI 등 live truth가 바뀌어 current state가 stale |
| BCP-014 | context/handoff rewrite·compression 중 | downstream machine/human consumer가 의존하던 locator/lineage/discovery surface가 삭제됨 |

BCP-013만으로는 BCP-014의 실패를 막지 못한다. PR #135의 문제는 merge 전 exact head에서 이미 발생했기 때문이다.

### Existing Solution Verdict

`ABSORB`

- primary owner: `maintaining-project-context-and-handoff`
- supporting owner: `auditing-canonical-reference-freshness`
- 신규 broad ACTIVE Skill: `0`
- 신규 자동 write workflow: 기본 `0`
- 우선 구현 후보: 기존 owner의 context-refresh/session-handoff 계약 + focused regression/reference test

## 일반화 후보

### Proposed General Rule

Live continuation owner를 압축·재작성하기 전에 **contract-surface inventory**를 수행한다.

```text
READ LIVE OWNER
→ INVENTORY CURRENT + DOWNSTREAM CONSUMERS
→ CLASSIFY SURFACES
   CURRENT_MUTABLE
   CANONICAL_LOCATOR
   HISTORICAL_DISCOVERY
   COMPATIBILITY_ANCHOR
   GENERATED_OR_DERIVED
   SAFE_TO_DROP
→ COMPRESS CURRENT STATE
→ PRESERVE OR MIGRATE REQUIRED NON-CURRENT ANCHORS
→ DO NOT REVIVE STALE STATE AS CURRENT
→ RUN REFERENCE/CONTRACT REGRESSION ON EXACT HEAD
→ MERGE
→ BCP-013 POST-MERGE RECONCILE IF APPLICABLE
```

### Invariant 1 — current truth remains singular

Historical/compatibility 표식을 보존한다고 해서 과거 상태를 current state로 승격하면 안 된다.

```text
CURRENT_MUTABLE
must agree with observed repository truth.
```

예:

- 과거 `active_planning_pr: 92`가 회귀 discovery에 필요하다면 `historical discovery` 섹션에 둘 수 있다.
- current field는 실제 상태인 `active_planning_pr: NONE`을 유지한다.

### Invariant 2 — canonical semantics stay with canonical owner

Handoff는 제품 규칙 전문을 보존하는 장소가 아니다.

규칙 자체의 owner가 별도 존재하면 다음 패턴을 우선한다.

```text
canonical owner path
+ minimal stable locator/token only when a consumer truly requires it
```

따라서 `3/3/4`를 Active Context에 다시 넣는 것은 전투 정본 복제가 아니라, 현재 프로젝트의 machine discovery contract가 실제로 요구한 최소 locator였다. Base는 특정 게임 숫자나 표현을 요구하지 않는다.

### Invariant 3 — consumer migration is preferable to accidental fossilization

필요 표식이 단순 brittle substring test 때문에만 남아 있고 더 안정적인 semantic consumer로 안전하게 바꿀 수 있다면, 영구적으로 문자열을 쌓기보다 consumer를 함께 migration하는 것이 낫다.

PR #136이 예다.

- 잘못된 consumer: editor plugin 배열 전체가 Godot AI 하나뿐이라고 exact-string 비교
- 실제 의도: Godot AI plugin이 여전히 설치·등록돼 있음
- 수정: 공존 가능한 presence assertion으로 계약을 좁힘

즉 BCP-014는 “옛 문자열을 무조건 보존”이 아니라 **실제 contract를 먼저 식별하고 producer 또는 consumer 중 책임이 잘못된 쪽을 최소 수정**하자는 원리다.

## Project-Specific Boundary

Base에 올리지 않을 값:

- `3/3/4`
- Ten Paces 전투 규칙
- PR #7/#65/#92/#135/#136 번호 자체
- `CORE_REVIEW_PENDING`
- Ten Paces의 `ACTIVE_CONTEXT.md` YAML field 이름
- Godot AI/GUT/Hera의 프로젝트별 설치 배열
- `docs/02_COMBAT_RULES.md`라는 특정 프로젝트 경로
- Android/device/human gate 상태

Base는 **continuation owner rewrite 전에 downstream contract를 inventory하고, current truth와 historical/discovery compatibility를 분리하며, safe deletion을 검증하는 lifecycle**만 소유한다.

## 적용 조건과 비사용 조건

### Use When

- `ACTIVE_CONTEXT`, `CURRENT_STATUS`, `HANDOFF`, resume manifest 같은 live router를 크게 압축·재구성한다.
- 문서가 machine test, parser, freshness checker, search-based router 또는 다음 세션 discovery의 입력이다.
- historical lineage를 지우면 후속 작업의 provenance/ownership 탐색이 어려워진다.
- canonical owner 전문을 다른 위치로 이동하면서 locator가 바뀐다.
- 기존 consumer가 literal string에 의존할 가능성이 있다.

### Do Not Use When

- 문서가 current router가 아닌 단순 dated historical report다.
- downstream machine/human consumer가 없고 archive owner가 따로 있다.
- 제거 대상이 실제로 dead surface임을 reference scan/test로 증명했다.
- greenfield owner라서 compatibility surface가 아직 존재하지 않는다.
- 단순 오탈자·포맷팅처럼 contract 의미가 바뀌지 않는 편집이다.

## Counterexamples

### Counterexample A — safe deletion

오래된 `CURRENT_STATUS.md`의 한 문장이 어느 parser/test/link/search route에서도 소비되지 않고, 동일 사실은 canonical owner에 있으며, repository-wide reference scan에서도 소비처가 0이라면 별도 compatibility section으로 보존할 이유가 없다. 삭제가 단순하다.

### Counterexample B — historical snapshot

`docs/reviews/2026-08-10-pre-merge.md`가 당시 SHA와 PR 상태를 기록했다면 이는 current router가 아니다. 내용을 최신 상태로 바꾸면 오히려 역사 증거를 훼손한다.

### Counterexample C — wrong consumer

consumer test가 `enabled=[A]`라는 배열 shape를 요구하지만 실제 계약은 `A가 포함됨`이고 B/C의 공존이 승인됐다면 producer를 과거 singleton 상태로 되돌리지 않는다. consumer를 semantic presence check로 고친다.

## Benchmark

상세 비교와 적용 한계는 `evidence/INDUSTRY_AND_PROJECT_EVIDENCE.md`가 책임진다.

핵심 비교:

- Google Engineering Practices는 하나의 self-contained change와 관련 test를 함께 유지하고 작은 변경으로 review/rollback/bug risk를 낮추는 방향을 권장한다. BCP-014는 handoff compression과 unrelated product rewrite를 분리하고, contract repair를 focused change로 유지하는 근거로 사용한다.
- GitHub Docs는 required checks가 최신 commit SHA에서 성공해야 하며, 이전 commit의 성공을 현재 증거로 재사용할 수 없다고 설명한다. BCP-014의 surface migration도 exact current head에서 regression을 다시 실행해야 한다.
- AWS ADR guidance는 accepted/rejected decision history를 보존하고 새 결정이 기존 것을 supersede할 때 과거 기록을 지우지 않는 방식을 권장한다. 이는 current truth와 historical lineage를 분리하는 원리와 정합적이다.
- Kubernetes deprecation policy는 안정된 API 요소를 소비자 호환성을 고려하지 않고 임의 제거하지 않는 강한 compatibility discipline의 사례다. Handoff의 machine-consumed locator를 API와 동일시하는 것은 아니지만, **소비되는 surface는 생산자 관점의 정리만으로 제거하면 안 된다**는 비교 근거로 제한적으로 사용한다.

외부 방식의 형식을 그대로 Base에 복제하지 않는다. 이 proposal은 문서 field versioning이나 deprecation 기간을 강제하지 않는다.

## Benefits

- context/handoff 압축이 회귀 검증을 무너뜨리는 일을 줄인다.
- 과거 상태를 current로 되살리지 않으면서 lineage/provenance를 보존한다.
- canonical owner를 가리키는 최소 locator를 유지해 다음 세션 탐색 비용을 줄인다.
- brittle consumer를 발견하면 producer fossilization 대신 semantic consumer repair를 선택할 근거를 제공한다.
- BCP-013의 post-merge reconciliation과 결합해 pre-merge rewrite와 post-merge truth 두 시점을 모두 보호한다.

## Risks

### Complexity / document bloat

모든 옛 문자열을 compatibility anchor로 남기면 Active Context가 다시 장문화될 수 있다.

Control:
- consumer inventory가 있는 표식만 보존한다.
- history 전문 대신 owner/locator를 선호한다.
- `SAFE_TO_DROP` 판정을 명시적으로 허용한다.

### Brittle-string institutionalization

literal substring test를 보호한다는 이유로 잘못된 표현을 영구 정본처럼 만들 수 있다.

Control:
- 먼저 semantic intent를 식별한다.
- 가능하면 consumer를 구조적/semantic assertion으로 migration한다.
- current state와 compatibility anchor를 분리한다.

### Hidden consumers

검색만으로 runtime/parser consumer가 모두 발견되지 않을 수 있다.

Control:
- Registry/routing/reference-freshness/test/workflow를 함께 inventory한다.
- exact-head CI를 삭제 증거의 일부로 사용한다.
- 확인 불가 consumer는 `BLOCKED_UNVERIFIED`로 남긴다.

### Maintenance cost

classification vocabulary가 지나치게 무거워질 수 있다.

Control:
- Base 구현 시 고정 schema보다 최소 질문/상태 분리를 우선한다.
- 모든 프로젝트에 동일 field 이름을 강제하지 않는다.

## Affected Consumers — 승인 후 후보

본 proposal 단계에서는 아래를 수정하지 않는다.

- `skills/maintaining-project-context-and-handoff/SKILL.md`
  - context-refresh/session-handoff 전에 contract-surface inventory 단계 후보
- `skills/auditing-canonical-reference-freshness/**`
  - supporting check 연결 후보
- handoff/context Method/reference
  - current vs historical/discovery compatibility 설명 후보
- focused contract tests
  - machine-consumed locator 보존
  - stale current state 부활 금지
  - consumer migration 허용
- generated/Registry consumer
  - 실제 active Skill body가 바뀌는 별도 구현 단계에서만 current Base 규칙에 따라 동기화

신규 broad Skill은 후보가 아니다.

## Validation Plan — 별도 구현 승인 후

### Scenario 1 — compression with machine consumer

Given:
- live Active Context contains current state plus a locator consumed by a regression test
- rewrite removes duplicated prose

Expected:
- locator is preserved or consumer is safely migrated
- exact-head regression passes
- stale historical state is not promoted to current

### Scenario 2 — historical lineage

Given:
- past PR/state token is needed only for provenance discovery

Expected:
- token may move to clearly labeled historical/discovery section
- current field reflects actual repository truth

### Scenario 3 — dead surface

Given:
- repository/registry/test/reference scan finds no consumer

Expected:
- deletion is allowed
- no compatibility anchor is forced

### Scenario 4 — brittle consumer

Given:
- test asserts accidental text shape rather than intended behavior

Expected:
- consumer is migrated to semantic intent
- producer is not reverted to obsolete shape
- focused RED→GREEN evidence exists

### Scenario 5 — post-merge transition

Given:
- context rewrite PR merges successfully

Expected:
- BCP-013 post-merge reconciliation applies independently if live state became stale after integration

## Regression Plan

- Existing context/handoff resume behavior remains intact.
- Historical snapshots remain immutable history unless they are actually live routers.
- Canonical owner continues to hold full domain semantics; Active Context does not become a second canon.
- Projects without machine-consumed handoff surfaces should not gain mandatory compatibility boilerplate.
- Test suites must not be deleted/disabled merely to permit compression.

## Rollback

이 proposal 단계에서는 활성 Base behavior가 바뀌지 않는다.

- proposal이 거절되면 Registry status를 Base lifecycle에 맞게 변경한다.
- proposal/evidence history는 삭제하지 않는다.
- 별도 구현 단계가 나중에 실패하면 구현 PR만 revert할 수 있어야 하며 이 proposal 기록은 근거로 남긴다.

## Adversarial Findings

### MUST_FIX — resolved in proposal

1. **BCP-013 중복 위험**: trigger를 pre-merge rewrite/compression vs post-merge integration stale로 분리했다.
2. **옛 문자열 무한 보존 위험**: `SAFE_TO_DROP`과 consumer migration을 명시했다.
3. **current/historical 상태 혼동**: current truth singular invariant를 명시했다.
4. **프로젝트 값 승격 위험**: Ten Paces 숫자·경로·PR·Godot plugin 배열을 project-specific boundary로 제외했다.

### SHOULD_FIX — future implementation concern

- 가능하면 literal substring test보다 semantic/structured assertion을 선호한다.
- 실제 Base implementation은 BCP-013과 함께 owner 내 lifecycle 충돌이 없는지 한 번 더 설계 검토한다.

### REJECTED_CRITIQUE

- “압축 문서에는 historical token이 하나도 없어야 한다”: 실제 downstream discovery consumer가 있는 경우 현재 상태와 분리해서 보존하는 편이 안전하므로 거부한다.
- “모든 historical token을 자동 archive로 이동하면 된다”: 소비자가 현재 live router를 탐색 entrypoint로 사용하면 archive 이동만으로 깨질 수 있어 일반 규칙으로 채택하지 않는다.

## Knowledge State

`PATTERN`

- 한 프로젝트에서 여러 독립 validation failure와 하나의 pre-existing workflow contract failure가 같은 원리를 반복 노출했다.
- exact-head GREEN과 merge로 프로젝트 수준 해결은 검증됐다.
- 다른 프로젝트의 context compression에 직접 적용한 두 번째 project pilot은 아직 `NOT_RUN`이다.
- 따라서 `VALIDATED_PATTERN`으로 승격하지 않는다.

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

이 proposal-only PR의 Base main 병합은 **제안 기록 저장**만 의미한다. `APPROVED_FOR_IMPLEMENTATION`이 아니며, active Base Skill/Test/Method/Tool/Workflow 변경은 별도 후속 단계에서만 수행한다.