# BCP - Coc-Fiction

## Existing Solution First

```yaml
project: Coc-Fiction
project_repository: alsdmlals4-eng/Coc-Fiction
project_main_observed: e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0
primary_canonical_base_proposal: BCP-2026-012-serial-fiction-canon-migration-debt
supporting_existing_base_proposal: BCP-2026-013-post-merge-continuation-state-reconciliation
existing_solution_verdict: REUSE_EXISTING_BCPS
new_canonical_bcp: false
proposal_registry_change: false
active_base_behavior_change: false
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
human_title: BCP - Coc-Fiction
```

Coc-Fiction에서 이번 연속 작업으로 얻은 공용 교훈은 새로운 광역 BCP를 만들 필요가 있는 독립 Goal이 아니라, 이미 Base에 제출된 BCP-012와 BCP-013을 실제 장편 연재소설 작업에서 추가 검증한 사례다.

따라서 사용자 요청의 `BCP - 프로젝트 이름` 규칙은 **사람이 읽는 프로젝트 증거 이름**으로 적용하고, Base의 validator-compatible canonical proposal ID/path는 기존 BCP-012/013을 유지한다.

이 파일은 Coc-Fiction의 프로젝트 출처형 개선 기록을 한곳에 모으는 roll-up evidence이며, Base 활성 Skill/Method/Test/Workflow 구현 승인을 뜻하지 않는다.

## 이번 프로젝트에서 추가로 검증된 사실

### 1. Canon migration debt는 고정 backlog가 아니라 이동하는 reconciliation frontier다

초기 Canon sync PR #14에서는 새 Canon을 즉시 유효하게 하면서 기존 대량 DRAFT의 충돌 위치를 bounded debt로 고정했다.

그 뒤 외부 최신 1~105화와 GitHub legacy 225화 저장 원고를 실제로 맞추기 시작하면서 단순한 `debt exists / does not exist`보다 더 구체적인 상태가 필요했다.

PR #17에서 외부 최신 제1~5화를 원본 사건·현재 Canon·사용자 Decision에 대조해 승격한 결과:

```yaml
reconciled_prefix_end: 5
legacy_tail_starts_at: 6
boundary_after_chapter: 5
whole_manuscript_continuity: NOT_YET_CLAIMED
next_bundle: 006-010
```

이때 새 제5화는 이미 구 저장 원고보다 사건이 더 진행된 상태였기 때문에, 최신 제5화 뒤에 legacy 제6화를 정상 연속으로 붙이면 사건 되감기가 발생했다. 프로젝트는 이를 억지 연결하지 않고 migration boundary로 명시했다.

이후 PR #19에서 제6~10화 reconciliation이 진행되면서 frontier가 다시 이동했다.

```yaml
reconciled_prefix_end: 10
legacy_tail_starts_at: 11
boundary_after_chapter: 10
next_bundle: 011-015
```

즉 BCP-012의 bounded legacy debt는 단순한 정적 목록이 아니라, **검증된 artifact가 strict-clean 영역으로 승격될 때마다 경계가 앞으로 이동하고 legacy tail이 줄어드는 lifecycle**로도 사용될 수 있음을 실증했다.

### 2. Migration boundary는 false continuity를 생성하지 않아야 한다

Coc-Fiction의 최신 외부 회차 편성과 GitHub legacy 저장 편성은 같은 chapter number를 공유해도 같은 사건 위치를 뜻하지 않았다.

따라서 reconciliation 중인 경계에서는 다음을 금지했다.

- `reconciled chapter → legacy chapter`를 자동으로 정상 next/previous 관계로 생성
- reverse outline 또는 index가 migration boundary를 이야기상 직접 연속으로 오인
- 회차 번호가 같다는 이유만으로 외부 최신본을 legacy bundle에 blind overwrite
- 과거 225화 storage topology를 현재 narrative numbering으로 재선언

프로젝트는 `SCENE_PASS_REGISTRY + composed index/reverse-outline override + migration boundary`를 기존 owner 안에서 사용하고, boundary를 만나면 false `previous/next`를 fail-closed로 끊었다.

이 구현 경로 자체는 Coc-Fiction 전용이지만, **Canon migration 중 파생 소비자가 아직 검증되지 않은 경계를 정상 연속성으로 추론하면 안 된다**는 원리는 BCP-012의 implementation 검토에 유용한 추가 evidence다.

### 3. Duplicate ownership은 guard를 약화하지 않고 한 소유자로 정리해야 한다

PR #17 디버깅에서 한 chapter를 기존 override와 migration-boundary override가 동시에 소유해 reverse-outline composer가 실패한 사례가 있었다.

해결은 duplicate guard를 느슨하게 만드는 것이 아니었다.

```text
duplicate canonical ownership detected
→ FAIL
→ decide one current owner for the chapter/boundary
→ remove overlapping ownership
→ regenerate composed consumer
```

이 패턴은 Coc-Fiction의 구체적인 JSON/file 구조를 Base에 강제할 근거는 아직 부족하다. 다만 BCP-012 구현 시 **migration debt를 허용한다는 이유로 canonical consumer ownership ambiguity까지 허용해서는 안 된다**는 반례 증거로 보존한다.

### 4. Post-merge continuation state는 실제 Coc-Fiction에서도 self-stale했다

Coc-Fiction PR #15는 BCP-012 병합 결과를 `ACTIVE_CONTEXT/HANDOFF`에 정확히 기록해 main으로 들어갔다. 그러나 그 PR이 병합되는 순간 문서가 기록한 `current main SHA` 자체가 과거 값이 되었다.

PR #16에서 이를 다음 의미로 보정했다.

```text
stable default branch = main
+ last_observed_main_sha
+ last integrated PR / merge result
+ actual post-merge CI evidence
+ resume 시 fresh repository truth 재조회
```

이 사례는 이미 Base BCP-013이 소유하는 Goal과 동일하므로 새 제안으로 만들지 않는다.

또한 PR #18처럼 reconciliation milestone 뒤 continuation checkpoint를 남기더라도, 그 checkpoint를 병합 완료 자체로 현재 truth의 영구 보증으로 해석하지 않고 다음 실행에서 fresh GitHub truth를 다시 읽는 경계가 필요함을 재확인했다.

### 5. External artifact의 `최종` 표기는 자동 Canon 승격 권한이 아니다

사용자가 제공한 최신 1~105화 산출물은 현행 프로젝트보다 새 문장과 편성을 포함했지만, GitHub current manuscript에 바로 전부 덮어쓰지 않았다.

각 bounded bundle에서 다음 순서를 사용했다.

```text
external latest artifact
→ current user Decision
→ active project Canon
→ source/original event evidence available for the bundle
→ current manuscript/adjacent-state comparison
→ KEEP / APPLY / REWORK / REJECT
→ only approved delta promotion
→ coupled consumer regeneration
→ exact-head verification
```

이는 Base에 새 Skill을 요구하지 않는다. 기존 `developing-and-revising-serial-fiction`과 BCP-012 lifecycle을 결합해 해결 가능하다.

## Coc-Fiction 개선사항 분류

| 프로젝트에서 얻은 항목 | 판정 | Base 처리 |
|---|---|---|
| 새 Canon 즉시 권위와 legacy DRAFT migration 상태 분리 | `REUSE / CORROBORATE` | BCP-012 |
| reconciled prefix + legacy tail + 이동하는 migration frontier | `REUSE / EXTEND_EVIDENCE` | BCP-012 |
| migration boundary에서 false next/previous continuity 차단 | `REUSE / EXTEND_EVIDENCE` | BCP-012 구현 검토 시 반영 후보 |
| duplicate chapter/consumer ownership fail-closed | `BASE_CANDIDATE_EVIDENCE_ONLY` | 단독 승격 금지, 추가 프로젝트 증거 대기 |
| post-merge live continuation self-stale | `REUSE / CORROBORATE` | BCP-013 |
| stable ref + last_observed_sha 의미 분리 | `REUSE / CORROBORATE` | BCP-013 |
| stale PR 전체 branch 대신 current-main 위 unique delta 재적용 | `REUSE / NO_PROMOTION` | 기존 Git/적대적 검토/freshness 절차로 충분 |
| external final artifact 자동 Canon 승격 금지 | `REUSE / NO_NEW_BCP` | 기존 serial-fiction Canon/source priority + BCP-012 |
| composed index / reverse-outline override / Scene Pass Registry의 Coc-Fiction 파일 구조 | `PROJECT_ONLY` | Base schema로 복제 금지 |
| 5화 단위 reconciliation | `PROJECT_ONLY` | 작품 운영 단위일 뿐 Base 고정값 아님 |
| 한 화 1~3명 POV | `PROJECT_ONLY` | 작품별 production rule |
| 조연·엑스트라 POV 허용 | `REUSE / NO_PROMOTION` | 기존 Base POV 가치/scene-boundary 필터로 충분 |
| POV·후크·캐릭터 QA의 작품별 상세 규칙 | `PROJECT_ONLY` | Coc-Fiction 운영 규칙으로 유지 |

## 공용화할 수 있는 보강 원리

BCP-012 구현을 검토할 때 Coc-Fiction 사례에서 추가로 참고할 수 있는 최소 원리는 다음과 같다.

### A. Reconciliation frontier

```text
VERIFIED_PREFIX + DECLARED_MIGRATION_BOUNDARY + LEGACY_TAIL
```

- prefix는 source/canon/continuity 검증을 통과한 범위다.
- boundary는 아직 정상 narrative continuity를 주장하지 않는 경계다.
- legacy tail은 현재 저장은 되어 있으나 새 Canon/편성과 완전 reconciliation이 끝났다고 주장하지 않는 범위다.
- 다음 bounded pass가 통과하면 boundary는 전진하고 legacy tail은 감소한다.

### B. No false continuity across unresolved migration

```text
IF chapter A is reconciled
AND chapter B is still legacy/unreconciled
AND A→B continuity has not been verified
THEN derived consumers must not invent normal continuity.
```

파생 데이터는 `UNKNOWN / MIGRATION_BOUNDARY / null` 또는 프로젝트가 정의한 동등한 fail-closed 상태를 사용할 수 있다. Base는 Coc-Fiction의 field 이름을 강제하지 않는다.

### C. Debt reduction must preserve unique ownership

```text
migration debt allowed
!= duplicate canonical ownership allowed
```

한 artifact/chapter/consumer의 current authority가 둘 이상이면 fail-closed하고, 먼저 ownership을 해소한 뒤 합성한다.

이 원리는 현재 Coc-Fiction 한 프로젝트에서 강하게 재현됐으므로 구현 참고 evidence로만 기록하고, 별도 공용 Skill/BCP로 승격하지 않는다.

## Base에 올리지 않을 Coc-Fiction 전용 값

다음은 Base 공용 규칙으로 승격하지 않는다.

- 작품 인물명·설정명·금지 설정명
- 특정 1부/2부/외전 회차 편성
- `001-005`, `006-010` 같은 실제 bundle 경로와 5화 고정 크기
- 프로젝트의 `MANUSCRIPT_INDEX_OVERRIDE_*`, `REVERSE_OUTLINE_OVERRIDE_*`, `SCENE_PASS_REGISTRY.json` 경로
- 특정 원본 PDF/스프레드시트의 파일명과 셀 주소
- `1~3 POV` 고정값
- 조연/엑스트라 POV의 작품별 사용 빈도
- 특정 캐릭터의 말투·관계·능력 제한
- Coc-Fiction의 PR/commit/workflow 번호 자체를 Base runtime contract로 강제하는 것

## 반례 / Do Not Use

- 새 Canon과 충돌하는 legacy artifact가 없으면 migration frontier를 만들지 않는다.
- 모든 소비자를 한 번에 안전하게 migration하고 검증할 수 있으면 `STRICT_NOW`로 끝내며 legacy tail을 인위적으로 만들지 않는다.
- 오래된 파일이 명시적으로 archive/reference-only이고 active consumer가 아니면 active migration debt로 세지 않는다.
- chapter 번호와 사건 편성이 이미 동일하고 adjacent continuity도 검증됐다면 boundary를 억지로 끊지 않는다.
- project-specific composed-data schema를 다른 프로젝트에 그대로 복제하지 않는다.

## 검증 시나리오 후보

이 evidence가 향후 BCP-012 구현 검토에 사용될 경우 다음 시나리오가 유용하다.

### Scenario A — frontier advances

Given reconciled prefix 1~5 and legacy tail 6+,
when 6~10 are source/canon/continuity reconciled,
then the strict-clean prefix becomes 1~10 and the migration boundary moves after 10 without restoring a false 5→legacy-6 edge.

### Scenario B — unresolved boundary stays fail-closed

Given a reconciled chapter followed by an unreconciled legacy chapter whose event placement differs,
when reverse-outline/index consumers are generated,
then they do not assert normal `next/previous` continuity across that boundary.

### Scenario C — duplicate owner rejected

Given one chapter is claimed by both a normal override and a migration-boundary override,
when composed consumers are generated,
then validation fails until one current owner remains.

### Scenario D — external artifact is evidence, not authority by label

Given an external artifact labelled `최종`,
when its numbering/event placement differs from project current manuscript,
then it is compared against user Decision, Canon, source evidence, and adjacent state before promotion.

### Scenario E — continuation truth refreshed after integration

Given a live continuation router merged with a PR,
when integration advances main or changes CI/PR state,
then fresh repository truth is observed before the router is used as current authority.

## Evidence lineage

Key Coc-Fiction integration/reconciliation evidence observed during this work:

- PR #13 — current Base integration + stale unique-delta recovery; merged.
- PR #14 — latest approved Canon sync + bounded legacy reconciliation debt; merged.
- PR #15 — persist BCP-012 continuation locator; merged.
- PR #16 — repair post-merge continuation self-stale semantics; merged.
- PR #17 — external latest Ch1~5 reconciliation + first explicit mixed-migration boundary; merged.
- PR #18 — post-001~005 continuation checkpoint; merged.
- PR #19 — external latest Ch6~10 reconciliation; merged.
- observed Coc-Fiction main after PR #19: `e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0`.

BCP-012의 기존 industry benchmark/evidence는 다음 문서가 계속 책임진다.

`[수정제안서]/BCP-2026-012-serial-fiction-canon-migration-debt/evidence/INDUSTRY_BENCHMARK_AND_PROJECT_EVIDENCE.md`

새로운 외부 일반화 주장을 추가하지 않았으므로 이번 프로젝트 roll-up은 기존 benchmark를 재사용하고, 프로젝트에서 실제로 재현된 delta만 추가한다.

## 설계 및 실행 계획

이번 Base 변경은 의도적으로 작다.

```text
current Base main
→ isolated proposal/evidence branch
→ add this one project-named evidence file under existing BCP-012
→ Proposal Registry unchanged
→ active Base files unchanged
→ exact-head Base proposal/contract CI
→ adversarial scope check
→ merge with exact head pinned
→ post-merge readback/CI check
```

### Scope gate

허용 파일:

```text
[수정제안서]/BCP-2026-012-serial-fiction-canon-migration-debt/evidence/BCP-Coc-Fiction.md
```

금지 범위:

- `skills/**`
- `templates/**`
- `tests/**`
- `.github/workflows/**`
- active Base methods/guides
- `START_HERE.md`
- release lock/frozen snapshot
- `[수정제안서]/PROPOSAL_REGISTRY.json`

Registry를 바꾸지 않는 이유는 이 문서가 새 canonical BCP를 등록하는 것이 아니라 기존 BCP-012/013에 프로젝트 증거를 추가하는 것이기 때문이다.

## Scope and lifecycle status

```yaml
evidence_role: PROJECT_NAMED_ROLLUP_EVIDENCE
human_title: BCP - Coc-Fiction
primary_canonical_owner: BCP-2026-012-serial-fiction-canon-migration-debt
supporting_canonical_owner: BCP-2026-013-post-merge-continuation-state-reconciliation
proposal_status_in_base: SUBMITTED
new_registry_record: NONE
active_base_implementation: NOT_AUTHORIZED_BY_THIS_EVIDENCE
active_skill_change: NONE
active_method_change: NONE
active_template_change: NONE
active_test_change: NONE
active_workflow_change: NONE
```

이 evidence의 병합은 Coc-Fiction에서 얻은 개선사항을 Base 수정제안서에 영속화하는 작업이다. BCP-012 또는 BCP-013의 실제 Base 활성 구현은 별도 승인·설계·TDD·구현 PR이 필요하다.
