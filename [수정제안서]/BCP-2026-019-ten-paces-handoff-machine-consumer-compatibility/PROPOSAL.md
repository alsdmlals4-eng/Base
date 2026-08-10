# BCP - Ten-Paces-Hidden-Moves

## 출처와 상태

- Proposal ID: `BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility`
- 사용자 표시명: `BCP - Ten-Paces-Hidden-Moves`
- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 출처 main: `dc95883873ccd8718f6aa5cb11f936ef39db42c7`
- 관련 프로젝트 PR: `#135`, `#136`
- 제출일: `2026-08-10`
- 상태: `IMPLEMENTED`
- 지식 상태: `관찰 + 기존 공용 제안 보강`
- Existing Solution Verdict: `ABSORB_INTO_BCP_2026_014`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 사용자의 `BCP - 프로젝트 이름` 명명 규칙에 따라 Ten Paces 관찰을 **독립 proposal record**로 저장한다. 다만 같은 공용 문제의 기존 owner는 `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`이므로, 새 broad Skill이나 두 번째 active implementation owner를 만들지 않는다.

기존 보강 증거는 다음 경로에 이미 존재하며 이 proposal의 source evidence로 재사용한다.

`[수정제안서]/BCP-2026-014-handoff-machine-consumer-compatibility-closeout/evidence/BCP-TEN-PACES-HIDDEN-MOVES.md`

이번 단계는 proposal storage만 수행한다. Base 활성 Skill, Method, Template, Test, Tool, Workflow, schema, `AGENTS.md`, `START_HERE.md`, release lock은 변경하지 않는다.

## 관찰과 증거

### 관찰 1 — Handoff 압축은 사람이 보는 문서 편집만이 아니다

Ten Paces PR #135는 오래된 `ACTIVE_CONTEXT.md`와 `HANDOFF.md`를 현재 repository truth 중심으로 압축·정리했다. 이 과정에서 사람이 보기에는 과거 정보나 중복처럼 보이는 일부 문자열이 실제로는 validator, reference-freshness, 다음 세션 discovery가 소비하는 계약 표면이라는 점이 exact-head CI에서 드러났다.

복구 과정에서 필요한 구분은 다음과 같았다.

```text
CURRENT_MUTABLE
CANONICAL_LOCATOR
HISTORICAL_DISCOVERY
COMPATIBILITY_ANCHOR
SAFE_TO_DROP
```

핵심은 stale 값을 current truth로 되살리는 것이 아니었다.

- current mutable state는 현재 repository truth를 유지한다.
- canonical semantics는 canonical owner가 계속 소유한다.
- downstream consumer가 실제로 요구하는 최소 locator/anchor만 비-current 역할로 보존한다.
- consumer가 없는 surface는 제거 후보가 된다.

PR #135 exact head `c18d384b537ec3eaf49370d454d23e98c44ba3f4`는 관련 validation을 통과한 뒤 merge commit `69eba09c6d18f5b4a473c0be14361ddd745983a0`으로 main에 반영됐다.

### 관찰 2 — 과거 literal shape 보존보다 semantic consumer migration이 맞는 경우가 있다

PR #135 병합 뒤 기존 `Validate Godot Live-Editor Pilot` 실패를 조사하면서 반대 방향의 failure mode가 확인됐다.

현재 프로젝트는 승인된 Godot AI + GUT + Hera 공존 상태였지만 legacy test는 Godot AI가 editor plugin 배열의 유일한 값이라는 과거 literal representation을 검사했다. 실제 의미 계약은 `Godot AI plugin remains installed and registered`였다.

따라서 producer를 과거 singleton 배열로 되돌리지 않고 consumer assertion을 semantic presence check로 수정했다. PR #136 exact head `4b9b12554b236c42ef24fa00d77af0c13c3406f7`에서 Live-Editor/PR/Full 관련 검증을 통과했고 merge commit `dc95883873ccd8718f6aa5cb11f936ef39db42c7`으로 반영됐다.

이 사례는 다음 두 행동을 구분해야 함을 보여준다.

```text
PRESERVE_REQUIRED_COMPATIBILITY_ANCHOR
vs
MIGRATE_BRITTLE_CONSUMER_TO_SEMANTIC_CONTRACT
```

둘을 구분하지 않으면 handoff 문서는 계속 과거 token을 쌓아 비대해지거나, 반대로 필요한 discovery surface를 지워 회귀를 만든다.

### 기존 Base 제안과의 관계

`BCP-2026-014-handoff-machine-consumer-compatibility-closeout`은 urban-legend에서 먼저 관찰된 같은 공용 문제를 소유한다. Ten Paces는 독립 프로젝트에서 같은 failure family를 재현했고, 추가로 **accidental literal representation을 검사하는 brittle consumer는 semantic migration 대상이 될 수 있다**는 반례를 제공한다.

따라서 이 proposal은 BCP-014를 대체하지 않고 cross-project corroboration으로 흡수되는 것이 적절하다.

## 일반화 후보

### Handoff / Continuation Machine-Consumer Preservation Contract

handoff 또는 active context를 압축·재작성할 때 다음 순서를 공용 기본값으로 제안한다.

```text
CURRENT REPOSITORY TRUTH FRESH READ
→ DOWNSTREAM CONSUMER INVENTORY
→ SURFACE CLASSIFICATION
→ CURRENT / CANONICAL LOCATOR / HISTORICAL DISCOVERY / COMPATIBILITY / DROP 분리
→ 필요한 compatibility anchor 보존
→ accidental literal-shape consumer는 semantic contract로 migration
→ exact-head consumer validation
→ post-merge continuation-state reconciliation
```

### 최소 공용 계약 후보

1. **Consumer inventory before destructive compression**
   - `ACTIVE_CONTEXT`, `HANDOFF`, Progress/Status 계열 문서의 문자열·링크·상태 필드를 삭제하기 전에 machine/human downstream consumer를 찾는다.
2. **Current truth와 historical compatibility 분리**
   - 과거 locator를 current field에 되살리지 않고 history/compatibility surface로 분리한다.
3. **Semantic contract over accidental serialization**
   - consumer가 의미가 아니라 배열 전체, 특정 문장, 특정 순서 같은 우연한 표현을 검사한다면 안전한 경우 semantic assertion으로 migration한다.
4. **No infinite compatibility fossilization**
   - 모든 과거 token을 영구 보존하지 않는다. owner·consumer·deprecation 조건을 확인한 뒤 제거 가능성을 판정한다.
5. **Exact-head validation**
   - handoff closeout은 문서 lint만이 아니라 실제 reference-freshness, consumer contract, project-specific regression을 exact head에서 통과해야 한다.
6. **Post-merge re-read**
   - merge 후 새 main SHA와 continuation owner를 다시 읽어 pre-merge snapshot을 current truth로 남기지 않는다.

### Existing Solution First 판정

공용 구현이 승인된다면 새 broad Skill을 만들지 않고 기존 `maintaining-project-context-and-handoff` 및 BCP-014 책임 경계에 흡수하는 것을 우선한다.

이 proposal 자체의 존재는 별도 active owner 생성을 의미하지 않는다.

## 적용 조건과 비사용 조건

### 적용 조건

- Handoff/Active Context/Continuation 문서를 대폭 압축·재작성한다.
- CI나 도구가 해당 문서의 token, link, field, locator를 읽는다.
- 과거 state를 current state로 오인하지 않으면서 discovery compatibility를 유지해야 한다.
- 기존 consumer가 literal representation에 결합되어 current authority와 충돌한다.
- post-merge 새 main을 기준으로 다음 세션을 이어가야 한다.

### 비사용 조건

- 순수 오탈자 수정처럼 downstream consumer surface가 변하지 않는다.
- 문서가 machine-consumed contract가 아니며 별도 canonical owner/locator도 없다.
- literal representation 자체가 명시적으로 canonical protocol인 경우.
- 보안·secret·개인정보 제거가 필요한 값을 compatibility 이유로 보존하려는 경우.
- 프로젝트 고유 수치나 특정 PR/SHA를 Base 전역 불변으로 승격하려는 경우.

## 반례와 위험

### MUST_FIX — stale 상태를 compatibility라는 이름으로 current truth에 복원

과거 PR 번호, 오래된 상태 문자열, 과거 SHA를 current mutable field에 다시 넣으면 continuation truth가 오염된다. 필요한 경우 명시적 historical/discovery section에만 보존한다.

### MUST_FIX — 테스트를 통과시키기 위해 의미 없는 token을 무한 누적

consumer가 accidental text shape에 결합되어 있다면 producer 문서에 token을 계속 추가하는 대신 consumer의 실제 의미 계약을 확인하고 migration 여부를 판단한다.

### MUST_FIX — semantic migration이 실제 protocol을 약화

모든 literal assertion이 brittle한 것은 아니다. 순서·정확 문자열·전체 배열이 실제 protocol이면 semantic presence 검사로 약화해서는 안 된다. canonical owner가 무엇을 보장하는지 먼저 확인한다.

### MUST_FIX — project-specific 값의 Base 전역화

Ten Paces의 `3/3/4`, 특정 PR/SHA, 특정 Active Context field, Godot AI/GUT/Hera plugin 배열은 source evidence이지 Base 공용 상수가 아니다.

### SHOULD_FIX — 문서 압축 후 machine consumer만 보고 사람 discovery를 누락

다음 세션 사람이 canonical owner를 찾을 수 있는 locator도 consumer surface다. machine tests만 통과했다고 handoff 품질이 완성됐다고 주장하지 않는다.

### SHOULD_FIX — BCP-013과 책임 중복

`BCP-2026-013-post-merge-continuation-state-reconciliation`은 merge 후 live state를 새 main truth와 재조정하는 책임을 소유한다. 이번 proposal의 핵심은 **압축/재작성 중 consumer surface 보존·migration**이며, post-merge SHA 재조정은 BCP-013에 위임한다.

## 프로젝트 전용으로 남길 내용

다음은 Base 일반 규칙으로 승격하지 않는다.

- Ten Paces 전투의 `3/3/4` 계획 수치
- PR #135 / #136 번호와 개별 commit SHA
- `docs/02_COMBAT_RULES.md` 같은 프로젝트 경로
- 특정 `ACTIVE_CONTEXT.md` field/token
- Godot AI/GUT/Hera의 프로젝트별 plugin 배열
- Android/device/human gate 상태
- Ten Paces 제품 구현 승인 상태

## 영향 범위와 검증

### 이번 proposal 단계 영향

- 새 proposal `BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility`
- `[수정제안서]/PROPOSAL_REGISTRY.json`의 해당 entry

### 이번 proposal 단계 비영향

- 기존 BCP-014 본문과 상태
- Base active Skill/Method/Template/Test/Tool/Workflow
- `skills/SKILL_REGISTRY.json`
- schemas와 release locks
- Ten Paces repository 제품 파일과 현재 gate
- Base PR #247 등 다른 열린 작업

### proposal 단계 검증

- changed files는 `[수정제안서]/**`의 `PROPOSAL.md`와 Registry 두 파일만 허용한다.
- `tools/check_base_change_proposals.py --base-ref <fresh-main>` 통과.
- Registry ID/path/source/status가 본문과 일치.
- same-goal BCP-014를 명시적으로 참조하고 두 번째 active owner를 만들지 않는지 적대 검토.
- exact-head required CI 성공과 unresolved review thread 0 확인.
- merge 직전 최신 Base main과 compatibility 재검사.

### 향후 구현 승인 시 검증 후보

- handoff compression fixture에서 required consumer locator 제거 시 RED.
- current state와 historical compatibility가 분리된 수정 후 GREEN.
- accidental literal-shape consumer를 semantic contract로 migration해도 canonical 의미가 유지되는 회귀 테스트.
- actual protocol literal assertion은 약화되지 않는 negative test.
- post-merge continuation reconciliation은 BCP-013 owner와 연결.

## 필요한 도구·권한

Proposal 저장 단계:

- Base GitHub branch/PR 쓰기
- `[수정제안서]/**` 수정 권한
- Base proposal validator 및 required CI

향후 active 구현 단계에서만:

- `maintaining-project-context-and-handoff` owner 수정 권한
- 관련 consumer regression test/validator 수정 권한
- 별도 `APPROVED_FOR_IMPLEMENTATION`

## 승인과 구현

- `BCP - Ten-Paces-Hidden-Moves` proposal storage: 사용자의 현재 지시로 진행 승인됨
- proposal status: `IMPLEMENTED`
- active Base implementation: BCP-014 및 기존 handoff owner에 흡수됨
- approval_ref: `docs/superpowers/specs/2026-08-10-approved-base-continuity-diagnostics-actions-design.md`
- implementation PR: `https://github.com/alsdmlals4-eng/Base/pull/260`
- implementation merge SHA: `d45a80c6b12a2c790bf1f5ba2338a1a53e5c165e`
- intended implementation owner: `BCP-2026-014` / existing handoff owner reuse

PR #260에서 BCP-014와 함께 handoff machine-consumer compatibility boundary로 흡수했다. Ten Paces의 실제 handoff 값·경로·제품 상태는 공용 규칙으로 올리지 않았다.
