# BCP-2026-012 — 연재소설 Canon Migration Debt lifecycle

## 출처와 상태

- Proposal ID: `BCP-2026-012-serial-fiction-canon-migration-debt`
- 출처 프로젝트: `alsdmlals4-eng/Coc-Fiction`
- 출처 프로젝트 기준 main: `c9c4fa647c833470759ada2514e45d1b2abb1e8b`
- 관련 프로젝트 PR: `#13`, `#14`
- 관련 stale recovery: `#9`, `#12`
- 관련 프로젝트 파일:
  - `fiction/CANON_REGISTRY.json`
  - `tools/check_fiction_content.py`
  - `fiction/bible/01_PROJECT_CORE.md`
  - `fiction/bible/02_CANON_AND_CONTINUITY.md`
  - `fiction/bible/03_PART1_STORY_BIBLE.md`
  - `fiction/bible/04_PART2_STORY_BIBLE.md`
  - `docs/coordination/2026-08-10_COC_FICTION_INTEGRATION_ADVERSARIAL_REVIEW.md`
  - `docs/coordination/2026-08-10_CANON_SYNC_ADVERSARIAL_REVIEW.md`
- 제출일: `2026-08-10`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- Knowledge Level: `Pattern`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow를 수정하지 않는다. 승인 전에는 proposal/evidence/registry만 등록한다.

## 관찰과 증거

### Problem

장편 연재 원고에서 **새 사용자 Decision 또는 새 Canon이 승인된 뒤 이미 존재하는 대량 DRAFT가 그 결정과 충돌하는 경우**, 현재 Base의 `CANON_AND_ADAPTATION_BOUNDARY_FIRST`만으로는 “새 결정은 즉시 유효하지만 기존 DRAFT는 어떤 lifecycle로 정리할지”가 충분히 구분되지 않는다.

Coc-Fiction에서 실제로 다음 문제가 발생했다.

1. 과거 설정을 `SUPERSEDED`로 만들고 새 자기통제 규칙을 Canon으로 승격했다.
2. 첫 validator 설계는 폐기 설정명을 곧바로 `forbidden_in_active_manuscript`에 넣었다.
3. exact-head CI가 기존 GitHub DRAFT의 11개 bundle에서 과거 설정 debt를 발견했다.
4. 이 실패를 문자 치환 명령으로 해석하면, 원본 사건 기록·최신 사용자 결정·앞뒤 continuity를 대조해야 하는 `serial-arc-pass`를 우회해 대량 장면 의미를 기계적으로 바꿀 위험이 생겼다.
5. 반대로 기존 DRAFT를 아무 제한 없이 두면 폐기 설정이 새 회차·재퇴고 원고·다른 소비자로 퍼질 수 있다.

### Evidence

프로젝트 TDD/debug lineage:

- 초기 최신 Canon 계약 RED: Coc-Fiction head `43aa73936125fa51d64f36ab685ea804d2d21711`, workflow run `31351462921` → expected `FAILURE`.
- strict-global 시도: head `1224a418...`, run `31351564487` → `FAILURE`; legacy DRAFT debt 11개 bundle + 별도 1개 `블랙킹` bundle 노출.
- root-cause 계약 RED: head `9089b26faf7e3023996e49e791303a6dea0ab5a7`, run `31351678017` → expected `FAILURE`.
- lifecycle 분리 GREEN: head `97c4dff1ba3a26b3b6546bb7780a99884429776d`, run `31351757414` → `SUCCESS`.
- adversarial-review exact head `e2d623bf8c38a3924591b4eefc2c3cc949d710b1`, run `31351829221` → `SUCCESS`.
- PR #14 merge/main `c9c4fa647c833470759ada2514e45d1b2abb1e8b`.
- post-merge main run `31351884525` → `SUCCESS`.

실제 수정에서 다음 lifecycle을 분리했을 때 원고를 기계 수정하지 않고도 fail-closed 검증이 가능했다.

```text
STRICT_NOW
FORBIDDEN_IN_NEW_OR_REVISED
BOUNDED_LEGACY_RECONCILIATION_DEBT
SCOPED_STRICT
```

### Root Cause

문제의 원인은 “Canon Decision의 현재 유효성”과 “그 결정 이전에 생성된 대량 DRAFT의 migration 완료 상태”를 한 상태로 취급한 것이다.

```text
새 Canon 승인
≠ 기존 모든 artifact가 이미 새 Canon 준수
```

Decision과 artifact migration은 서로 연결되지만 별도 lifecycle이다.

### Existing Base Coverage

현행 Base `developing-and-revising-serial-fiction`은 다음을 이미 소유한다.

- `CANON_AND_ADAPTATION_BOUNDARY_FIRST`
- 사용자 결정·원작·기존 정본 우선순위
- protected facts / event results / information timing
- continuity와 revision evidence
- serial POV·pacing·payoff

`auditing-canonical-reference-freshness`는 canonical source 변경 뒤 stale consumer와 untouched consumer를 찾는 공용 책임을 이미 갖는다.

따라서 새 광역 Skill은 필요하지 않다. 부족한 것은 **새 Canon Decision을 대량 기존 DRAFT에 적용하는 migration/debt 상태 분리**다.

### Existing Solution Verdict

`ABSORB`

- owner: `developing-and-revising-serial-fiction: canon-and-continuity`
- supporting owner: `auditing-canonical-reference-freshness`
- 새 ACTIVE Skill: `0`

## 일반화 후보

### Proposed General Rule

장편·연재소설에서 승인된 새 Canon/Decision이 기존 DRAFT와 충돌하면 다음 순서로 처리한다.

```text
NEW_CANON_DECISION
→ old decision = SUPERSEDED / history preserved
→ affected consumers inventory
→ enforcement class per rule/scope
   1. STRICT_NOW
   2. FORBIDDEN_IN_NEW_OR_REVISED
   3. BOUNDED_LEGACY_RECONCILIATION_DEBT
   4. SCOPED_STRICT
→ debt must not grow outside declared consumer set
→ source/canon/continuity reconciliation by bounded batch
→ verified artifact promotion to strict-clean
→ debt ledger reduction
→ post-merge freshness recheck
```

### Enforcement classes

#### `STRICT_NOW`

현재 활성 artifact 전체가 즉시 준수해야 하고, 안전한 기계 수정 또는 이미 완료된 migration 증거가 있는 규칙.

예: 오탈자 표준명, 이미 이전 PR에서 전수 제거된 폐기 ID.

#### `FORBIDDEN_IN_NEW_OR_REVISED`

새로 쓰거나 현재 Decision 이후 실질적으로 재퇴고하는 원고에서는 즉시 금지하지만, 과거 DRAFT 전체를 blind rewrite하지 않는 규칙.

#### `BOUNDED_LEGACY_RECONCILIATION_DEBT`

현재 DRAFT에 남아 있는 legacy 위반을 **정확한 artifact/bundle set**으로 등록한다. 등록된 debt가 새 파일·새 회차로 증가하면 실패한다. 제거는 source/canon/continuity 대조를 거친 bounded revision으로 수행한다.

#### `SCOPED_STRICT`

특정 부·아크·시점·플랫폼·버전에만 적용되는 현재 규칙. 범위를 전역화하지 않는다.

### Debt invariant

```text
actual_legacy_debt_consumers == declared_debt_consumers
```

또는 구현 언어에 따라 동등한 fail-closed 계약을 둔다.

- 새 위치 증가: `FAIL`
- 등록 위치 감소: migration 진척으로 받아들이되 ledger 갱신 필요
- 정확한 집합 일치: `PASS_WITH_KNOWN_DEBT`
- 실제 원고 직접 대조 미실행: clean으로 승격 금지

### Project-Specific Boundary

Base에 올리지 않을 값:

- 특정 작품의 폐기 설정명·인물명
- `1~3 POV` 같은 작품별 production rule
- 실제 bundle 경로·화수
- 실제 Canon ID
- 작품별 원본 PDF/TRPG 우선순위
- 프로젝트별 exact debt set

Base는 lifecycle과 검증 원리만 소유한다.

### Use When

- 장편 DRAFT가 이미 대량 존재한 뒤 Canon/설정/호칭/사건 결과가 승인 변경됐다.
- 단어 치환만으로 의미·인과·관계가 안전하게 보존되는지 확신할 수 없다.
- legacy violation을 당장 모두 고칠 수 없지만 새 원고로 번지는 것은 막아야 한다.
- source/canon/continuity reconciliation을 묶음 단위로 진행한다.

### Do Not Use When

- 기존 artifact가 없거나 migration을 한 번에 안전하게 끝낼 수 있는 greenfield 변경.
- 단순 오탈자처럼 문맥과 무관하게 전체 안전 치환이 검증된 경우.
- old artifact가 명시적으로 archive/reference-only이고 활성 consumer가 아닌 경우.
- 사용자가 기존 Canon 자체를 유지하기로 한 경우.

### Counterexample

프로젝트에 3개 문서만 있고 폐기된 ID `OLD_NAME`이 세 곳 모두 단순 metadata key로만 존재하며 schema migration test가 전체 안전 치환을 보장한다면 `BOUNDED_LEGACY_RECONCILIATION_DEBT`를 만들 필요가 없다. 즉시 migration 후 `STRICT_NOW`만 두는 편이 단순하다.

### Benchmark

상세 비교는 `evidence/INDUSTRY_BENCHMARK_AND_PROJECT_EVIDENCE.md`가 책임진다.

핵심 비교:

- AWS Prescriptive Guidance ADR: 새 Decision이 이전 Decision을 supersede해도 역사 기록을 보존하며, legacy non-compliant code/artifact는 자동 해결되지 않으므로 점진 갱신 또는 technical debt task로 별도 관리한다.
- GitHub Docs: PR three-dot diff는 merge base 이후 해당 branch가 도입한 delta를 중심으로 보여주며, base와 동기화해 충돌·test failure를 사전에 찾도록 권장한다. 이는 stale 전체 history보다 현재 기준 unique delta를 검토하는 Base의 기존 방향과 정합적이다.
- Reedsy multiple POV guidance: 새 POV는 필요성이 있어야 하고 scene/chapter boundary에서 즉시 식별해야 하며 mid-scene head-hopping을 피해야 한다. Coc-Fiction의 POV 교훈은 이미 Base current POV filter 원칙으로 충분해 새 BCP로 승격하지 않는다.

### Benefits

- 새 Canon의 즉시 권위와 기존 DRAFT migration 현실을 동시에 표현한다.
- 대량 blind rewrite를 막는다.
- legacy debt가 새 원고로 퍼지는 것을 fail-closed로 차단한다.
- source/canon/continuity 대조가 필요한 작품에 단계적 정본화 경로를 제공한다.
- 프로젝트가 특정 term/path를 Base에 복사하지 않고 lifecycle만 재사용할 수 있다.

### Risks

- debt ledger가 영구 backlog가 될 수 있다.
- 너무 작은 변경에도 debt 상태를 만들면 운영 복잡도가 증가한다.
- declared set을 느슨한 wildcard로 두면 fail-closed 가치가 사라진다.
- `PASS_WITH_KNOWN_DEBT`를 전체 Canon-clean PASS로 오독할 위험이 있다.
- 프로젝트별 구현이 서로 다른 field 이름을 쓰면 학습 비용이 생길 수 있다.

대응:

- bounded exact consumer set을 선호한다.
- Do Not Use When을 명시한다.
- debt가 0이 되기 전 `CANON_MIGRATION_COMPLETE`를 주장하지 않는다.
- Base는 구체 schema를 먼저 강제하지 않고 reference contract로 시작한다.

## 적용 조건과 비사용 조건

### Existing Solution First 결과

| 후보 | 판정 | 이유 |
|---|---|---|
| stale PR selective recovery | `REUSE / NO_PROMOTION` | Base/GitHub 기존 diff·freshness·adversarial 절차로 충분 |
| post-merge verification | `REUSE / NO_PROMOTION` | Base 운영 규칙에 이미 존재 |
| approval reuse | `REUSE / NO_PROMOTION` | Base intake/continuous-work 계약에 이미 존재 |
| exact-head evidence freshness | `REUSE / NO_PROMOTION` | Base validation/reference freshness가 소유 |
| `serial-arc-pass`의 exact Coc-Fiction consumer 전파 | `SPLIT` | 묶음 원리는 공용, index/override/Scene Registry 경로는 project-only |
| `1~3 POV` | `PROJECT_ONLY / NO_PROMOTION` | 작품별 production value |
| POV switch value + extra/support POV | `REUSE / NO_PROMOTION` | 현행 Base POV filter와 scene boundary 원칙 확장 없이도 충분 |
| Canon migration debt lifecycle | `ABSORB / BASE_CANDIDATE` | 현재 owner는 존재하지만 post-decision legacy-DRAFT lifecycle 명시 부족 |

### 적용 전 조건

- 최신 사용자 Decision과 project Canon authority가 확인되어야 한다.
- affected consumer inventory가 생성되어야 한다.
- old artifact가 active인지 archive/reference-only인지 구분되어야 한다.
- blind rewrite가 안전하지 않은 이유가 기록되어야 한다.

### 비사용 조건

앞의 `Do Not Use When`과 동일하며, 단순 일회성 프로젝트 값이나 fixed POV count를 이 lifecycle의 명분으로 Base에 올리지 않는다.

## 반례와 위험

### Adversarial Findings

#### MUST_FIX — proposal에 fixed term/path schema를 넣지 않는다

Coc-Fiction에서 사용한 field 이름과 exact path는 구현 사례일 뿐 공용 표준이 아니다. Base는 상태 의미와 invariant만 정의한다.

#### MUST_FIX — `PASS_WITH_KNOWN_DEBT`와 `MIGRATION_COMPLETE`를 구분한다

검증기가 debt 확산을 막았다는 것과 기존 debt를 제거했다는 것은 다른 사실이다.

#### SHOULD_FIX — second-project evidence 전에는 `Validated Pattern`으로 승격하지 않는다

현재 실증은 Coc-Fiction 한 프로젝트에서 강하다. AWS ADR의 legacy debt 처리와 구조적으로 일치하지만, 다른 fiction project pilot은 아직 없다. Knowledge Level을 `Pattern`으로 유지한다.

#### REJECTED_CRITIQUE — 새 `managing-fiction-canon-migration` Skill 필요

기각. 독립 trigger/output owner를 만들기보다 기존 `developing-and-revising-serial-fiction: canon-and-continuity`에 mode/reference 계약을 흡수하면 된다.

#### REJECTED_CRITIQUE — Canon 변경 즉시 모든 legacy DRAFT를 자동 rewrite해야 한다

기각. 의미·인과가 얽힌 원고에서는 사용자 Decision과 source evidence를 보존하지 못할 수 있다.

#### REJECTED_CRITIQUE — legacy debt가 있으면 새 Canon을 승인 상태로 둘 수 없다

기각. Decision authority와 artifact migration completion은 별개다. 단, debt 상태를 숨기면 안 된다.

### 유지비

중간. 상태 분류와 debt inventory가 추가되지만 새 Skill·새 광역 Registry는 만들지 않는다.

### 잘못 사용될 가능성

프로젝트가 어려운 정리를 무한 연기하기 위해 debt ledger를 남용할 수 있다. 정확한 consumer set, 다음 reconciliation unit, completion status를 요구해 완화한다.

## 영향 범위와 검증

### Affected Consumers — 승인 후 구현 후보

`ABSORB` 방향의 최소 후보:

1. `skills/developing-and-revising-serial-fiction/SKILL.md`
   - `canon-and-continuity`에 decision-vs-artifact-migration 분리 계약 추가.
2. `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
   - Canon Migration Debt lifecycle reference 추가 또는 기존 Canon section 확장.
3. `skills/auditing-canonical-reference-freshness/SKILL.md`
   - fiction migration debt가 있는 경우 exact affected consumer set을 freshness evidence로 소비할 수 있게 연결 문구 최소 확장.
4. 기존 Skill behavior/contract test
   - strict-now, future-only, bounded-debt, scoped-strict fixture.
5. generated active skill view/learning log는 기존 Base 생성·전파 규칙에 따라 필요할 때만.

새 ACTIVE Skill·광역 프로젝트 Registry·mandatory schema는 기본 구현안이 아니다.

### Validation Plan

1. Base contract fixture에서 새 Canon Decision + 3 legacy DRAFT consumer를 만든다.
2. bounded debt에 등록된 3개가 존재하면 `PASS_WITH_KNOWN_DEBT`, 4번째 새 consumer가 생기면 fail-closed인지 확인한다.
3. 한 consumer를 source/canon reconciliation으로 정리한 뒤 declared debt가 줄지 않으면 stale-ledger fail을 확인한다.
4. `SCOPED_STRICT`가 다른 아크에 과잉 적용되지 않는 반례를 검사한다.
5. greenfield 단순 rename은 debt lifecycle 없이 기존 path로 통과하는지 확인한다.
6. `auditing-canonical-reference-freshness`와 책임 중복이 없는지 registry/owner audit.
7. 실제 두 번째 serial-fiction 프로젝트 pilot 전에는 `Validated Pattern` 또는 human usability PASS를 주장하지 않는다.

### Regression Plan

- 기존 `CANON_AND_ADAPTATION_BOUNDARY_FIRST` 의미 유지.
- 프로젝트별 Canon schema를 Base가 소유하지 않음.
- current `pov-and-character-voice`, pacing/payoff, reader feedback modes 영향 없음.
- archive/reference-only artifact에 active debt 강제 금지.
- 단순 proofreading-only 경로를 무거운 migration workflow로 라우팅하지 않음.
- Base Skill 수 증가 없음.

### Rollback

승인 후 구현이 과도하게 복잡하거나 두 번째 pilot에서 가치가 없으면:

1. reference/mode 확장을 revert한다.
2. 프로젝트별 debt ledger는 project-local 운영 규칙으로 유지할 수 있다.
3. BCP와 evidence는 historical proposal record로 보존한다.
4. 기존 BCP-009 serial-fiction Skill 동작은 그대로 복귀한다.

## 승인과 구현

```yaml
proposal_status: APPROVED_FOR_IMPLEMENTATION
user_approval_for_active_base_implementation: GRANTED_2026_08_10
approval_ref: "[수정제안서]/BCP-2026-012-serial-fiction-canon-migration-debt/PROPOSAL.md#승인과-구현"
active_base_skill_change: NOT_STARTED
project_evidence: PASS
second_project_pilot: NOT_RUN
human_usability: HUMAN_NOT_RUN
knowledge_level: Pattern
recommended_existing_solution_verdict: ABSORB
```

사용자는 2026-08-10 KST 대화에서 `좋아 다 승인할게 [연속작업] 진행해`로 이 제안의 최소 `ABSORB` 구현을 승인했다. 구현은 별도 PR에서 진행하며, 새 ACTIVE Skill·프로젝트 전용 schema·작품별 Canon 값은 제외한다.

다음 상태:

```text
SUBMITTED
→ Proposal Review
→ user approval if accepted
→ APPROVED_FOR_IMPLEMENTATION
→ minimal ABSORB implementation with TDD
→ second-project/fixture validation
→ adversarial review
→ post-merge verification
```
