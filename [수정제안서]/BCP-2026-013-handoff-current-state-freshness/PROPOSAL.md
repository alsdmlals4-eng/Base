# BCP-2026-013 — Handoff / Current-State Freshness Gate

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 기준 프로젝트 커밋: `6cd14324a3de1a1b2a9898aaee1e9535c87c8fdc`
- 관련 프로젝트 PR: `#137 · docs: refresh handoff state after SX-DEC-055 deferral`
- 관련 Decision: `SX-DEC-055`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `PATTERN`

## Observation / Problem

프로젝트의 `CURRENT_CONFIRMED_DECISIONS`와 Google Sheet는 최신 `SX-DEC-055`까지 반영됐지만, cold-start 진입점인 `START_HERE.md`, `ACTIVE_CONTEXT.md`, `ROADMAP.md`가 과거 PR #83~100 / SX-DEC-042 전후 상태를 계속 현재 작업처럼 안내했다.

그 결과 새 세션/에이전트가 저장소 최신 정본을 읽더라도, 가장 먼저 보는 handoff/current-state 표면이 stale하면 이미 완료된 작업을 재실행하거나 현재 보류된 작업 대신 과거 Android/기능 작업으로 잘못 라우팅될 수 있었다.

## Evidence

프로젝트 `main` 기준에서 동시에 관찰된 사실:

- `CURRENT_CONFIRMED_DECISIONS.md`: `SX-DEC-055` approved / DoR ready / Godot implementation not started.
- Google Sheet: `SX-DEC-055`가 `IMPLEMENTATION_DOR_READY`.
- `START_HERE.md`: `SX-DEC-027~036`, Android Device Smoke를 현재 gate로 안내.
- `ACTIVE_CONTEXT.md`: 과거 PR #83/#99/#100과 `SX-DEC-041/042 IMPLEMENTATION_PENDING` 상태를 현재처럼 안내.
- `ROADMAP.md`: `M6 ANDROID DEVICE SMOKE · CURRENT`를 즉시 다음 작업으로 유지.

프로젝트 PR #137은 이 drift를 current repository truth에 맞게 교정하고, `SX-DEC-055`를 `USER_DEFERRED_AFTER_DOR`로 보존하면서 재개 시 `Task 1 / Step 1.1 RED`부터 시작하도록 Continuation State를 재구성했다.

## Root Cause

Base에는 이미 `maintaining-project-context-and-handoff`와 project-operations의 `START_HERE / ACTIVE_CONTEXT / HANDOFF` Template이 존재한다. 그러나 현행 계약은 주로 **무엇을 기록할지**와 **새 작업자의 읽기 순서**를 정의하며, 다음과 같은 material drift를 fail-closed로 분류하는 공용 freshness 계약은 충분히 명시되어 있지 않다.

```text
latest decision/canon/merged-main advances
+ START_HERE / ACTIVE_CONTEXT / ROADMAP remains old
→ cold-start route can contradict repository truth
```

즉 문제는 새 Handoff 책임 부재가 아니라, 기존 owner의 **cross-owner freshness / resume-route consistency** 검증 공백이다.

## Existing Base Coverage

현재 Base가 이미 제공하는 것:

- `maintaining-project-context-and-handoff`: current context / handoff / resume 책임.
- `auditing-canonical-reference-freshness`: canonical/reference drift 감사 책임.
- `PROJECT_START_HERE.md`: 새 작업자 읽기 순서와 10분 cold-start 확인.
- `ACTIVE_CONTEXT.md`: 현재 목표·단계·다음 작업·보호 대상·미확정·최소 읽기 순서.
- `HANDOFF.md`: 인수 시점 상태·미완료·다음 첫 행동·읽기 순서.
- `reviewing-and-validating-project-changes`: 실제 변경과 current evidence 검증.

## Existing Solution Verdict

**ABSORB**

새 broad Handoff/Progress Skill을 만들지 않는다. 승인될 경우 기존 owner들에 다음 최소 계약을 흡수하는 것이 적절하다.

1. material checkpoint에서 `START_HERE / ACTIVE_CONTEXT / ROADMAP or equivalent`를 current decision/main/active PR과 대조한다.
2. stale route가 발견되면 handoff를 실행 권위로 사용하지 않고 먼저 `STALE_CONTINUATION_STATE`로 fail-closed한다.
3. resume 시 저장된 SHA/PR/next-step을 current GitHub truth와 비교하고, stale이면 교정 후 다음 작업을 선택한다.
4. duplicate state owner를 만들지 않고 기존 owner를 갱신한다.
5. user-deferred approved work는 승인 자체를 폐기하지 않고 `DEFERRED_WITH_RESUME_TRIGGER`로 보존한다.

## Proposed General Principle

```text
HANDOFF_IS_A_LOCATOR_NOT_TRUTH

current repository truth
→ latest main / active PR / current decision / actual files / current validation
→ compare handoff/current-state surfaces
→ if consistent: RESUME_ALLOWED
→ if stale: STALE_CONTINUATION_STATE
→ repair existing owner
→ re-evaluate next executable step
```

Material checkpoint 예시:

- new Decision approval
- major Task completion
- blocker discovery
- PR open/update
- exact-head validation
- merge
- post-merge verification
- explicit user deferral/resume
- session handoff

## Project-Specific Boundary

Base에 올리지 않는 값:

- `Switchy Express: Cargo Puzzle`의 실제 gameplay 규칙.
- `SX-DEC-055`의 runtime semantic POC 내용.
- 프로젝트 PR 번호/commit SHA를 공용 규칙으로 강제하는 것.
- 73 PNG, Godot 4.7.1, Android/Windows 실제 gate 값.
- 프로젝트 Google Sheet의 실제 row/tab.

이 값들은 출처 증거로만 존재하며 Base 구현 계약에는 들어가면 안 된다.

## Use When

- 장기 작업이 여러 PR/Decision에 걸쳐 이어질 때.
- 새 세션/새 에이전트가 `START_HERE`, `ACTIVE_CONTEXT`, `HANDOFF`, Roadmap을 사용해 재개할 때.
- 사용자가 작업을 명시적으로 보류했다가 나중에 재개할 수 있을 때.
- Canon/Decision/main은 전진했지만 current-state 표면이 독립적으로 유지될 때.
- 여러 owner 사이의 “다음 작업”이 달라질 위험이 있을 때.

## Do Not Use When

- 단일 짧은 작업이며 별도 continuation owner가 존재하지 않을 때.
- archive/historical handoff만 있고 active current-state로 소비되지 않을 때.
- 자동 생성 snapshot이 항상 canonical owner에서 원자적으로 재생성되고 stale 상태가 구조적으로 불가능할 때.
- 프로젝트가 이미 동등한 fail-closed freshness 검사를 가지고 있을 때.

## Counterexamples

1. `HANDOFF.md`가 명시적으로 historical snapshot이고 cold-start route에서 제외된 경우: stale 자체는 오류가 아니다.
2. Roadmap이 장기 제품 milestone만 소유하고 “next executable step”을 소유하지 않는 프로젝트: Roadmap을 강제로 current-state owner로 만들면 안 된다.
3. 저장된 SHA가 과거 기준점으로 의도적으로 보존되는 경우: 값이 오래됐다는 이유만으로 자동 수정하면 안 된다. `observed_at`/`baseline` 의미를 먼저 해석해야 한다.
4. 사용자 보류가 새 범위 취소를 의미하는 경우: approval reuse를 자동 적용하지 말고 실제 사용자 지시의 의미를 따른다.

## Benchmark

### GitHub pull-request review / branch truth

GitHub는 PR에서 base/head와 실제 diff를 기준으로 변경을 검토하고, branch가 뒤처졌거나 변경됐으면 현재 상태를 다시 확인하는 흐름을 제공한다. 이 원리는 handoff에도 그대로 적용할 수 있다: 저장된 설명보다 현재 repository state를 먼저 확인해야 한다.

적용: current main/PR를 handoff보다 우선하는 fail-closed 재개.

비적용: GitHub PR metadata 형식을 project handoff schema로 그대로 복제하지 않는다.

### Google Engineering Practices — small changes / reviewability

Google의 code review guidance는 작은 변경과 명확한 검토 단위를 권장한다. 인수인계 freshness도 거대한 상태 문서 하나를 새로 만드는 대신 기존 current-state owner의 최소 delta를 유지하는 편이 reviewability와 drift 억제에 유리하다.

적용: duplicate owner 대신 bounded update.

비적용: 특정 조직의 changelist 절차를 프로젝트에 강제하지 않는다.

### ADR / decision supersession pattern

ADR 계열 관행은 이전 결정 기록을 삭제하지 않고 superseded/accepted 상태를 명시해 역사와 현재 권위를 분리한다. Handoff에서도 과거 snapshot을 삭제하는 대신 “historical locator”와 “active current state”를 구분하는 것이 안전하다.

적용: stale historical record 보존 + active route 교정.

비적용: 모든 프로젝트에 ADR 파일 형식을 강제하지 않는다.

## Benefits

- 새 세션이 오래된 next-step을 실행할 위험 감소.
- 완료된 작업의 중복 실행/중복 PR 감소.
- 사용자 보류 상태와 승인 재사용 경계 보존.
- cold-start 문서와 current decision/main의 drift 조기 발견.
- 새 broad Skill 없이 기존 owner의 책임 품질 강화.

## Risks

### Complexity

freshness 대조 항목을 너무 많이 강제하면 작은 프로젝트의 handoff 비용이 커질 수 있다. 따라서 material checkpoint와 active consumer에만 적용해야 한다.

### Maintenance

`START_HERE`, `ACTIVE_CONTEXT`, `ROADMAP`, `HANDOFF`를 모두 필수 owner로 강제하면 프로젝트별 구조 차이를 깨뜨릴 수 있다. “or equivalent active current-state owner” 원칙이 필요하다.

### Compatibility

기존 프로젝트의 historical SHA/PR 표기는 stale처럼 보여도 의도된 baseline일 수 있다. 필드 의미를 해석하지 않고 timestamp/숫자 비교만 하는 자동화는 금지해야 한다.

### Security / Cost

추가 외부 서비스나 secret은 필요하지 않는다. 검증은 repository metadata와 프로젝트의 기존 정본으로 수행할 수 있다.

## Affected Consumers — 승인 후 후보

이번 제안 단계에서는 **아래 활성 파일을 수정하지 않는다.** 승인된 별도 구현 단계에서만 검토한다.

- `skills/maintaining-project-context-and-handoff/SKILL.md`
- `skills/auditing-canonical-reference-freshness/SKILL.md`
- `templates/project-operations/PROJECT_START_HERE.md`
- `templates/project-operations/ACTIVE_CONTEXT.md`
- `templates/project-operations/HANDOFF.md`
- 관련 operating-system/reference-freshness regression test

새 ACTIVE Skill은 기본 후보가 아니다.

## Validation Plan

별도 구현 승인 후에만:

1. positive case: current state와 handoff가 일치 → resume allowed.
2. stale decision case: Decision registry가 전진했으나 Active Context가 과거 → fail closed.
3. stale PR case: handoff가 merged/closed PR을 active로 가리킴 → repair required.
4. intentional historical baseline case → false positive 금지.
5. user-deferred approved work → approval preserved, execution deferred.
6. duplicate owner creation 금지.
7. existing cold-start/reference-freshness regression과 통합.

## Regression Plan

- 기존 `maintaining-project-context-and-handoff`의 snapshot/handoff 기능을 제거하지 않는다.
- archive/historical evidence를 active state로 강제 승격하지 않는다.
- 프로젝트별 owner 명칭과 문서 구조를 하드코딩하지 않는다.
- 사용자 Decision 없이 보류 작업을 자동 재개하지 않는다.

## Rollback

이번 proposal-only 단계는 `[수정제안서]/**`만 추가한다. 문제가 있으면 proposal/Registry entry를 revert하면 되며 Base 활성 동작에는 영향이 없다.

향후 별도 구현이 승인되어도 existing owner의 bounded mode/reference/template/test 변화만 후보이며, 독립 rollback 가능한 PR로 수행해야 한다.

## Adversarial Findings

- `MUST_FIX` — BCP ID 012가 이미 다른 proposal로 사용됨: `013`으로 교정.
- `REJECTED_CRITIQUE` — 새 Handoff Skill 필요: existing owner가 명확하므로 중복 책임.
- `REJECTED_CRITIQUE` — 모든 오래된 SHA를 stale로 판정: historical baseline/observed-at 의미가 있으므로 금지.
- `SHOULD_FIX` — Roadmap을 모든 프로젝트에서 mandatory current-state owner로 강제하면 과잉: equivalent active owner 허용.
- `DEFER` — 자동 cross-document freshness checker의 구체 구현: 이번 실행의 Base 활성 구현은 명시적으로 금지되어 별도 후속 단계.

## Knowledge State

`PATTERN`

- 실제 프로젝트에서 stale cold-start route가 재현됨.
- current owner 교정으로 프로젝트 continuity가 개선됨.
- Base 기존 owner와 gap 위치가 확인됨.
- 다른 두 번째 프로젝트 pilot 및 자동화 효과 측정은 `NOT_RUN`.

## 승인과 구현

- 사용자 승인 근거: **제안 저장·proposal-only PR 병합만 허용됨. Base 활성 구현 권한은 이번 단계에서 부여되지 않음.**
- proposal status: `SUBMITTED`
- proposal-only PR: `PENDING`
- Base active implementation: `NOT_STARTED_IN_THIS_STAGE`
- implementation boundary: `SEPARATE_FOLLOWUP_STAGE`
