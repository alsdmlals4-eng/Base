# Base 장기 작업 실행 정책

이 문서는 Base와 Base를 채택한 프로젝트에서 시간보다 기획 의도·정확성·복원성·검증 가능성을 우선하는 L1 이상 장기 작업의 공용 생명주기를 정의한다. 새 Skill이나 Work Mode가 아니라 기존 intake·검증·Git·archive·Loop Engineering 책임을 한 흐름으로 묶는다.

## 1. Machine contract

```text
DIRECTION_FIRST
CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY
MINIMUM_VIABLE_ALTERNATIVES: 3
BENCHMARK_SYNTHESIS
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD
SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
RECOVER_TRY_ALTERNATIVES_RESUME
INDEPENDENT_WORKSTREAM_ISOLATION
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
POSTMERGE_PROMOTION_AND_SUPERSESSION
CORE_LOOP_DUMMY_BALANCE_BUILD_TEST
BALANCE_BUDGET
WORLD_STORYLINE_FIT_REQUIRED
REUSABLE_SYSTEM_EXTRACTION
NOTION_DEFAULT_PROJECT_WORKSPACE
PROJECT_RELATION_REQUIRED
WORK_MASTER
ASSET_KNOWLEDGE_MASTER
VISUAL_MAP_DERIVED
REPO_NATIVE_STRUCTURED_DATA
GOOGLE_SHEETS_COMPATIBILITY_ONLY
EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE
LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT
REQUIRED_WORK_REMAINING: 0
```

## 2. 기본 흐름

```text
RESEARCH
→ CURRENT STATE / OPEN PR RECONCILIATION
→ DIRECTION / INTENT
→ >= 3 VIABLE ALTERNATIVES
→ BENCHMARK SYNTHESIS
→ TRADE STUDY
→ PROVISIONAL BEST OPTION
→ EXPECTED EFFECTS / RISKS / MITIGATIONS
→ ONE USER APPROVAL
→ SMALL TESTABLE SLICES
→ TOOL / RUNTIME EXECUTION
→ FIVE FULL ADVERSARIAL IMPROVEMENT LOOPS
→ LONG-TERM FIT CLOSURE
→ EXACT-HEAD PR GATE
→ MERGE
→ POSTMERGE READBACK
→ LESSON PROMOTION / SUPERSESSION
→ REQUIRED WORK REMAINING = 0
```

### `DIRECTION_FIRST`

1. 현재 사용자 목표, 플레이어 가치, 성공 조건, 비목표를 먼저 복원한다.
2. 최신 main, 같은 Goal의 열린·최근 병합 PR, 현재 정본, 실제 구현, 테스트·실패 증거를 대조한다.
3. 세부 수치나 구현 편의가 큰 방향을 역으로 결정하지 못하게 한다.
4. 프로젝트 코어·플레이어 경험·비용·범위를 바꾸는 선택만 사용자 결정으로 올리고, 승인된 방향 안의 가역적 기술 세부는 연속 실행한다.

## 3. 현행 조사·대안·벤치마킹

### `CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`

L1 이상 중요한 결정은 한 방법을 먼저 고른 뒤 근거를 끼워 맞추지 않는다. **현행 조사 → 최소 3개 실질 대안 → 벤치마킹 → 동일 기준 비교 → 임시 권장안 → 더 나은 방안 탐색 → 전체 적대적 개선 루프 → 장기적으로 최선인 안 확정** 순서를 따른다.

`MINIMUM_VIABLE_ALTERNATIVES: 3`은 숫자 채우기가 아니다. 현행 유지, 기존 해법 재사용/흡수, 최소 수정, 구조 개선, 검증된 외부 해법 채택, 신규 구축 중 실제로 가능한 materially distinct 후보를 최소 3개 확보한다. 세 후보가 구조적으로 불가능하면 이유와 탈락 증거를 숨기지 않고 `BLOCKED_UNVERIFIED` 또는 Decision evidence로 남긴다.

비교 기준에는 최소한 사용자/플레이어 가치, 정확성·기획 충실도, 위험, 수명주기 비용, 유지보수성, 되돌리기 난이도, 재사용·모듈성, 증거 강도, 현재 비용 경계를 포함한다.

### `BENCHMARK_SYNTHESIS`

**벤치마킹은 한 성공사례를 모방하는 절차가 아니다.** 현업의 실무사례·실패사례를 여러 개 비교하고 작동 원리와 실패 조건을 분리한다.

```text
ADOPT / ADAPT / REJECT
```

- `ADOPT`: 현재 목표·비용·권위·기술 환경에 그대로 맞는다.
- `ADAPT`: 장점의 원리를 가져오되 프로젝트 세계관·핵심 경험·기술 경계에 맞게 재해석한다.
- `REJECT`: 성공 사례라도 현재 환경에서 총비용·권위·플레이어 가치가 맞지 않는다.

`BETTER_ALTERNATIVE_SEARCH`는 최초 권장안을 보호하는 절차가 아니다. 새 테스트·실패·적대적 finding·환경 변화가 생길 때마다 더 나은 방안이 나타났는지 다시 본다. **장기적으로 더 강한 방안**이 승인된 방향 안에 있으면 근거와 함께 교체한다.

`LONG_TERM_PLAN_FIT_REQUIRED`는 최종 선택이 현재 작업뿐 아니라 장기계획에 적합한지 확인한다. 최종 보고에는 왜 현재 후보 중 **장기적으로 최선**인지와 재검토 조건을 함께 기록한다.

## 4. 구현 전 Gate

### `EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD`

L1 이상 BUILD 전에 최소한 다음을 닫는다.

```yaml
expected_effects: []
likely_problems: []
mitigations: []
considered_alternatives: []
rejected_alternatives: []
provisional_best_option:
long_term_fit:
revisit_conditions: []
rollback: []
acceptance_criteria: []
verification_plan: []
```

## 5. 승인 후 연속 실행

### `SINGLE_INITIAL_APPROVAL_THEN_CONTINUE`

완전한 작업 계약을 한 번 승인받은 뒤 같은 범위의 구현, 테스트, 실패 진단, 가역적 수정, PR 생성, exact-head 검사, 적대적 검토, 회귀 검사, 저장소 정책이 허용하는 병합과 postmerge readback은 routine approval로 멈추지 않는다.

새 사용자 승인이 필요한 것은 핵심 게임 방향·플레이어 경험·중요 스토리 의미 변경, 승인 범위 확대, 파괴적 migration/삭제, 새 결제·별도 과금, 계정·보안 권한 확대, 사용자 취향 선택이 필요한 복수 유효안이다.

## 6. 실패 복구

### `RECOVER_TRY_ALTERNATIVES_RESUME`

```text
failure / interruption
→ side effect 가능성 판정
→ authoritative state readback
→ root-cause hypothesis
→ safe route A
→ 필요 시 safe route B/C
→ rollback / partial-state containment
→ completed work 보존
→ incomplete work만 resume
→ regression recheck
```

같은 실패 명령을 맹목적으로 반복하지 않는다. 한 도구나 전송면이 막히면 동일 acceptance criterion을 만족하는 더 단순하고 권위 있는 경로를 먼저 찾는다.

## 7. 독립 workstream 격리

### `INDEPENDENT_WORKSTREAM_ISOLATION`

`OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT`

`EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`

다른 채팅·Branch·PR이 같은 Goal처럼 보여도 기본적으로 별도 workstream으로 취급한다. read-only 충돌 탐지는 가능하지만 checkout/write/rebase/close/merge/material-delta 흡수는 사용자 명시 승인 없이는 수행하지 않는다.

## 8. 게임 작업 계약

### `CORE_LOOP_DUMMY_BALANCE_BUILD_TEST`

게임 작업은 core loop, 핵심 시스템, 세계관/핵심 스토리라인 정합성, 가역적 dummy `BALANCE_BUDGET`, playable build/test와 재사용 가능한 모듈 경계를 함께 본다.

### `WORLD_STORYLINE_FIT_REQUIRED`

기능적으로 맞아도 세계관·핵심 스토리·플레이어 판타지를 훼손하면 완료가 아니다.

### `REUSABLE_SYSTEM_EXTRACTION`

반복해서 필요한 기능은 프로젝트 고유 수치·세계관·콘텐츠와 공용 구조를 분리해 재사용한다. 한 번의 성공만으로 새 공용 Skill이나 플랫폼을 만들지 않는다.

## 9. 프로젝트 작업면과 데이터 권위

### `NOTION_DEFAULT_PROJECT_WORKSPACE`

새 프로젝트와 새 시각/기획 작업의 기본 인간 작업면은 **하나의 Notion workspace**다. 여러 프로젝트를 같은 workspace에 둘 수 있지만 `PROJECT_RELATION_REQUIRED`로 Work, Asset, Component, Screen, Reference, Benchmark를 강하게 구분한다.

```text
00 · PROJECT HUB
→ Project Registry

project page
  01 · PROJECT CONTROL
  → WORK_MASTER filtered by Project

  [large visual separation]

  02 · ASSET / LIBRARY / BENCHMARK
  → ASSET_KNOWLEDGE_MASTER filtered by Project

  [large visual separation]

  03 · VISUAL MAP
  → VISUAL_MAP_DERIVED
  → approved project visuals

90 · SYSTEM MASTERS
→ unfiltered master data sources
```

프로젝트 페이지에 unfiltered cross-project Master view를 기본 노출하지 않는다. 프로젝트가 다른 레코드를 직접 복사해 독립 정본으로 만들지 않는다. 공용 재사용이 필요하면 하나의 source record와 명시적 reuse intent를 유지한다.

`VISUAL_MAP_DERIVED`는 현재 Screen/관계 record와 승인 preview에서 만든 파생 표현이다. 게임은 화면 흐름을, 서사 프로젝트는 canon/character/clue/scene/continuity 관계를 시각화할 수 있다. 그림이 구조화 record와 충돌하면 그림을 수정·재생성한다.

### `REPO_NATIVE_STRUCTURED_DATA`

balance, economy, schema, runtime config, 코드, scene, resource, tracked implementation asset, build/test 상태는 repository-native source와 실제 runtime evidence가 소유한다. Notion의 승인이나 screenshot은 runtime proof가 아니다.

### `GOOGLE_SHEETS_COMPATIBILITY_ONLY`

기존 Google Sheet는 고유 unmigrated material이 남아 있을 때만 compatibility/migration source로 읽는다. 검증된 migration과 readback 뒤에는 새 프로젝트 작업면으로 사용하지 않는다.

### `EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE`

외부 HTML catalog/dashboard는 발견·보조 surface일 뿐 정본이나 실행 증거가 아니다.

## 10. 시각 자산·Reference·Benchmark

Asset & Knowledge Master는 `ASSET / COMPONENT / SCREEN / REFERENCE / BENCHMARK` Record Type을 사용할 수 있다. 사람 view에는 Preview/Name/Usage/Style/Approved/Reuse처럼 판단에 필요한 정보만 보이고, AI/System view에는 ID, Project, version, Status, Prompt, source provenance, Rights / License, Hash, Implementation Path, Decision 등을 보존할 수 있다.

Reference/Benchmark decision은 필요할 때 `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`를 사용한다. 외부 자료는 요구사항 정본이 아니며 고유 표현을 복제하지 않는다.

생성·수정 이미지의 성공 보고는 upload call만으로 끝나지 않는다.

```text
generate / edit
→ correct Project target
→ upload / attach
→ readback
→ approval / rejection
→ version / replacement relation
→ repository handoff
→ runtime QA separately
```

## 11. 비용 경계

### `ZERO_INCREMENTAL_COST_REQUIRED`

```text
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
```

현재 기본 유료 플랜은 **GPT Pro** 하나다. Notion은 Free 범위에서 사용하며 paid Notion AI, 별도 API credit, metered storage/automation, marketplace, 신규 유료 runner/compute/storage를 기본 경로에 넣지 않는다. 다른 유료 기능을 도입·실행·결제하려면 **새 사용자 승인**이 필요하다. 비용 상태가 불명확하면 `COST_GATE_BLOCKED`로 둔다.

## 12. 다섯 번의 전체 적대적 개선 루프

### `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`

적대적 검토를 실제로 실행할 때는 다섯 관점을 한 번씩 보는 것이 아니라 다음 **전체 범위 개선 루프를 최소 5회** 반복한다.

```text
FULL_SCOPE_REVIEW
→ finding 검증
→ 개선/보완
→ 실제 검증/회귀
→ 개선된 전체 상태 RE-ATTACK
```

각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자산, 실패 복구, 보안, 동시성, 비용, 벤치마크, 장기 유지, 증거와 완료조건을 다시 본다. 회차 N 입력은 원칙적으로 회차 N-1의 검증된 출력 상태다.

각 회차에서 `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_REQUIRED`를 다시 확인한다. 5회차 뒤 P0/P1 또는 acceptance criterion을 막는 finding이 남으면 수정·검증 후 추가 전체 루프를 수행한다.

`NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니다.

## 13. PR·병합·postmerge

작업은 작은 self-contained slice로 구현한다. exact current main에서 시작하고 다른 workstream을 건드리지 않는다. 병합 전에 exact head, required checks, unresolved thread 0, P0/P1 0, 비용/보안 Gate를 확인한다.

### `POSTMERGE_PROMOTION_AND_SUPERSESSION`

병합 뒤 main을 다시 읽고 replacement pointer와 실제 소비자를 확인한다. 구형 구현이 새 권위에 완전히 대체되었고 사용자가 제거를 승인한 경우 active surface에서 제거한다. Git history는 복구 가능한 기록으로 남는다.

## 14. 완료 조건

완료 보고는 acceptance criterion별 상태를 분리한다.

```yaml
required_work_remaining: 0
external_blockers: []
optional_backlog: []
```

`REQUIRED_WORK_REMAINING: 0`은 승인된 필수 criterion이 모두 충족됐을 때만 쓴다. 외부 계정/사용자 PC/기기 검증은 external blocker로, 장기 개선 아이디어는 optional backlog로 분리한다.

## 15. 신선도와 교훈 승격

Base는 계속 변하므로 작업 시작 시 latest main SHA, `AGENTS.md`, `START_HERE.md`, `DOCUMENTATION_MAP`, Skill Registry, same-goal open/recent PR, current tool/runtime checkpoint를 다시 찾는다.

`REUSABLE_LESSON_PROMOTION_GATE`는 실패·복구·반복 패턴을 다음 순서로 분류한다.

```text
incident / solution
→ REUSE_EXISTING_OWNER
→ EXTEND_REFERENCE_OR_MODE
→ EXTRACT_MODULE
→ BASE_CHANGE_PROPOSAL
→ NEW_SKILL_LAST
```

한 번의 성공을 즉시 새 Skill·새 local tool·새 SaaS 권위로 승격하지 않는다. 원인, 안전한 해결 경로, 반례/비사용 조건, 재현·검증 증거와 롤백 조건을 함께 남긴다.
