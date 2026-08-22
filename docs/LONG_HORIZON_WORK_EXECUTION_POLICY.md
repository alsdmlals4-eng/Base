# Base 장기 작업 실행 정책

이 문서는 Base와 Base를 채택한 프로젝트에서 시간보다 기획 의도·정확성·복원성·검증 가능성을 우선하는 L1 이상 장기 작업의 공용 생명주기를 정의한다. 새 Skill이나 Work Mode가 아니라 기존 intake·검증·Git·archive·Loop Engineering 책임을 한 흐름으로 묶는다.

## 1. Machine contract

```text
DIRECTION_FIRST
DEEP_WORK_PREANSWER_GATE
REQUIRED_EVIDENCE_BEFORE_FINAL
NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION
INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION
GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY
REASONING_EFFORT_IS_NOT_WORK_EVIDENCE
REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF
CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY
MINIMUM_VIABLE_ALTERNATIVES: 3
BENCHMARK_SYNTHESIS
CREATIVE_BENCHMARK_FRONTIER
ORIGINALITY_FUN_CREATIVITY_REVIEW
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
BEST_LONG_TERM_EFFICIENT_METHOD
QUALITY_OVER_RESPONSE_SPEED
BENCHMARK_PRACTICE_COMPARISON
EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD
SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
RECOVER_TRY_ALTERNATIVES_RESUME
INDEPENDENT_WORKSTREAM_ISOLATION
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE
FOLLOW_UP_TARGET_IS_MERGED_MAIN
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
ADVERSARIAL_REVIEW_UNTIL_CLEAN
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
POSTMERGE_PROMOTION_AND_SUPERSESSION
POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP
POSTMERGE_CORRECTION_REQUIRED
PROGRESS_READBACK_REQUIRED
RELEASE_NEAR_VERTICAL_SLICE_FIRST
GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE
SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE
TECHNICAL_SPIKE_INTERNAL_ONLY
EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT
SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED
BALANCE_BUDGET
WORLD_STORYLINE_FIT_REQUIRED
REUSABLE_SYSTEM_EXTRACTION
NOTION_DEFAULT_PROJECT_WORKSPACE
PROJECT_RELATION_REQUIRED
WORK_MASTER
ASSET_KNOWLEDGE_MASTER
VISUAL_MAP_DERIVED
PROJECT_VISUALIZATION_NEED_MAP
REPO_NATIVE_STRUCTURED_DATA
GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL
EXTERNAL_HTML_WORKSPACE_RETIRED
TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW
QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW
LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT
REQUIRED_WORK_REMAINING: 0
```

## 2. 기본 흐름

`BEST_LONG_TERM_EFFICIENT_METHOD`가 이 흐름의 목표다. `QUALITY_OVER_RESPONSE_SPEED`에 따라 효율을 빠른 답변·최소 토큰·최소 Tool 호출로 정의하지 않고, 사용자·플레이어 가치, 정확성, 출시 품질, 유지보수성, 재사용성, 되돌리기 가능성, 위험, 수명주기 총비용의 결합으로 판정한다. 중요한 작업은 최고 결과를 위해 더 많은 시간·토큰·조사·검증을 사용할 수 있다. `BENCHMARK_PRACTICE_COMPARISON`은 공식/1차 자료, 벤치마크, 현업 운영 방식, 실무 성공·실패 사례를 최소 3개 실질 대안과 함께 비교하도록 요구한다.

```text
RESEARCH
→ CURRENT STATE / OPEN PR RECONCILIATION
→ DIRECTION / INTENT
→ >= 3 VIABLE ALTERNATIVES
→ BENCHMARK SYNTHESIS + CREATIVE FRONTIER
→ TRADE STUDY
→ PROVISIONAL BEST OPTION
→ EXPECTED EFFECTS / RISKS / MITIGATIONS
→ ONE USER APPROVAL
→ SMALL TESTABLE SLICES
→ TOOL / RUNTIME EXECUTION
→ AT LEAST 5 FULL ADVERSARIAL LOOPS, THEN UNTIL CLEAN
→ LONG-TERM FIT CLOSURE
→ EXACT-HEAD PR GATE
→ MERGE
→ POSTMERGE READBACK
→ LESSON PROMOTION / SUPERSESSION
→ REQUIRED WORK REMAINING = 0
```

### `DEEP_WORK_PREANSWER_GATE`

L1 이상 또는 조사·벤치마킹·검토·구현·검증을 명시한 요청은 `REQUIRED_EVIDENCE_BEFORE_FINAL`이다. 현재 정본과 실제 구현 조사, 필요한 외부 원출처 조사, 최소 3개 실질 대안 비교, 구현 현실성, 요구된 적대적 검토와 검증을 실제로 수행하기 전에 substantive final answer로 종료하지 않는다.

`INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION`: 중간보고를 생략하거나 한 번에 결과를 달라는 요청은 사용자 노출만 줄인다. 도구 호출·조사·검토·테스트·readback을 생략하거나 미래 단계로 미루는 근거가 아니다.

`NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION`: 필수 evidence가 `NOT_RUN`이면 완료가 아니다. 현재 실행할 수 없으면 `BLOCKED_UNVERIFIED`와 해제 조건을 보고하고, 실행 가능한 독립 범위는 계속한다.

`GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY`: GPT-first는 판단·통합 책임의 owner를 정하는 말이지 prose-only 경로가 아니다. `REASONING_EFFORT_IS_NOT_WORK_EVIDENCE`이므로 `매우 높음` 같은 추론 강도도 실제 source readback·Tool 호출·실행·테스트 증거를 대체하지 않는다. `REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF`에 따라 현재 세션 Tool로 필수 evidence를 얻을 수 있으면 실행하며, 별도 Codex 인계의 선택성과 혼동하지 않는다.

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

### `CREATIVE_BENCHMARK_FRONTIER`

게임의 중요한 코어·시스템·콘텐츠·UX·서사 방향은 직접 장르 성공작 한두 개만 보지 않는다. 결정 직전까지 다음 다섯 축에서 현재 문제를 가장 잘 푸는 작품·시스템·실패사례를 찾는다.

```text
DIRECT_GENRE_BEST_IN_CLASS
+ ADJACENT_GENRE_BEST_IN_CLASS
+ DISTINCTIVE_OR_INNOVATIVE_WORK
+ FAILURE_OR_MIXED_CASE
+ PROJECT_INTERNAL_STRENGTH
→ transferable principles
→ recombination candidates
→ project-specific synthesis
```

목표는 “많이 섞기”가 아니라 **서로 다른 강점의 원리를 분리한 뒤 프로젝트의 플레이어 약속·세계관·제작 규모에 맞는 새로운 조합으로 다시 설계**하는 것이다. 유명세·판매량·수상 여부는 후보 발견 신호일 뿐 프로젝트 적합성 증거가 아니다.

### `ORIGINALITY_FUN_CREATIVITY_REVIEW`

권장 기획에는 기능성뿐 아니라 다음을 함께 공격한다.

```yaml
creative_review:
  originality_delta:
  fun_hypothesis:
  creativity_recombination:
  familiar_anchor:
  surprising_or_distinctive_element:
  meaningful_player_decision:
  feedback_and_pacing:
  world_story_fit:
  production_feasibility:
  risks_of_gimmick_or_complexity:
  player_evidence_status:
```

- `originality_delta`: benchmark에서 무엇을 유지·제거·뒤집고·결합·추가했는지 설명한다.
- `fun_hypothesis`: 왜 재미있을 것으로 예상하는지 행동·선택·긴장·보상·피드백으로 설명한다.
- `creativity_recombination`: 여러 원리가 하나의 coherent player experience로 연결되는지 본다.
- 익숙함을 모두 없애 독해 비용을 높이거나, 독창성을 핑계로 핵심 루프를 복잡하게 만들지 않는다.
- **재미 PASS는 실제 player evidence 전에는 주장하지 않는다.** 기획/benchmark 단계는 `FUN_HYPOTHESIS`이며 release-near Slice의 사람 플레이 증거가 있어야 높은 evidence로 승격한다.

`BETTER_ALTERNATIVE_SEARCH`는 최초 권장안을 보호하는 절차가 아니다. 새 테스트·실패·적대적 finding·환경 변화·더 강한 benchmark 후보가 생길 때마다 더 나은 방안이 나타났는지 다시 본다. **장기적으로 더 강한 방안**이 승인된 방향 안에 있으면 근거와 함께 교체한다.

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

이미 승인된 동일 계약에서 `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행`처럼 계속 실행 의도가 명확하면 `CONTINUATION_INTENT_ALIASES`를 `APPROVED_CONTRACT_CONTINUATION`으로 해석한다. 정확한 마법 문구를 다시 요구하지 않되, 승인되지 않은 범위·새 Goal·사용자 결정 Gate는 이 별칭으로 승인하지 않는다.

### `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`

`APPROVED_CONTRACT_CONTINUATION`이 활성이고 현재 승인된 작업 계약이 latest completed `main`에서 직접 만든 **단 하나의 명확한 `current-task PR`**이라면, continuation intent는 그 PR의 latest-main reconciliation, `exact HEAD` 재검증, repository가 요구하는 `required checks`·review·unresolved-thread·ruleset Gate 통과 뒤 merge와 `postmerge readback`까지 포함한다. 같은 작업의 PR 번호를 다시 요구하지 않는다.

이 예외는 `pre-existing`, `unrelated`, `other-workstream`, `draft` PR, 복수의 모호한 PR 후보, 다른 작업의 material-delta takeover에는 적용하지 않는다. `force push`, direct `main` push, `--admin`, `ruleset bypass`는 계속 금지한다. 사용자가 `병합하지 마`, `PR만 열어`, `검토만`처럼 범위를 좁히면 최신 지시가 merge authority를 제거한다.

### `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`

모든 Base/project GitHub 병합 뒤에는 새 main SHA를 다시 가져와 전체 승인 범위를 적대적으로 검토한다. 유효 finding은 `POSTMERGE_CORRECTION_REQUIRED`로 최신 main에서 새 Branch/PR에 교정하고 exact-head 회귀를 재실행한다. 해당 프로젝트에 Notion 사람용 정본이 적용되면 repository 증거가 확정된 뒤에만 현재 상태 블록을 갱신한다. 마지막으로 GitHub와 Notion 목적지를 모두 재조회하고 `PROGRESS_READBACK_REQUIRED`에 따라 완료율, 남은 필수 작업, 선택 backlog, blocker를 다시 계산한다. 열린 다른 PR은 명시적 번호·동작 승인 없이 수정하지 않고, 역사 섹션을 현재 상태로 일괄 치환하지 않는다.

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

`OPEN_PR_READ_ONLY_BY_DEFAULT`

`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`

`FOLLOW_UP_TARGET_IS_MERGED_MAIN`

`open / draft / ready` PR·branch는 실제 동시 작업자 여부와 무관하게 기본 read-only다. current-state reconciliation을 위한 head/diff/check 읽기는 가능하지만 checkout/write/rebase/close/merge/selective-copy/material-delta 흡수는 하지 않는다. 일반 후속 작업은 latest completed `main`에서 새 Branch로 시작하고 main에 실제 유지된 변경만 대상으로 한다.

열린 PR mutation이 필요하면 사용자가 현재 작업에서 PR 번호와 허용 동작을 명시해야 한다. 같은 Goal, owner evidence 부재, 현재 coordinator만 활성이라는 확인, 과거 standing authorization은 예외 권한이 아니다.

단, `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`의 조건을 모두 만족하는 현재 승인 작업의 단일 `current-task PR`은 위 기본 금지의 좁은 예외다. 이 예외는 다른 open PR의 mutation·흡수·종료·supersede 권한으로 확장되지 않는다.

## 8. 게임 작업 계약

### `RELEASE_NEAR_VERTICAL_SLICE_FIRST`

기획·검수를 닫은 뒤 플레이어 재미·몰입·가독성·첫인상·선택의 감정적 효과를 검증하는 첫 인간 플레이 테스트는 짧더라도 **실제 출시 의도에 가까운 완성형 Vertical Slice**를 대상으로 한다. `GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE`이며, `SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED`에 따라 실제 게임 사용 후보인 UI/UX, 이미지·아트, 애니메이션/연출, 음악·효과음, VFX/피드백, 핵심 시스템·데이터·콘텐츠가 한 구간에서 연결되어야 한다. 플레이어가 보는·듣는·조작하는 경로에는 임시 `player-facing placeholder`나 dummy 표현을 남겨 플레이 경험을 왜곡하지 않는다.

`SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`: 시스템만 동작하는 회색 상자·dummy UI·무음/무연출 PoC는 알고리즘·성능·호환성·데이터 흐름 같은 좁은 기술 질문에는 쓸 수 있지만 재미·몰입·판매력·가독성·감정·기억·전체 UX의 PASS 근거가 될 수 없다. 이런 검증은 `TECHNICAL_SPIKE_INTERNAL_ONLY`로 분리하며 공개 데모·Vertical Slice·player-experience evidence로 승격하지 않는다.

`EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`: 완성형 Slice를 만든다는 이유로 모든 자산·UI·사운드·효과를 새로 만들지 않는다. 현재 프로젝트의 승인된 자산·구조·검증된 외부 해법을 먼저 조사하고 `ADOPT / ADAPT / REJECT`로 판정한다. 프로젝트의 세계관·핵심 경험·가독성·일관성에 맞는 기존 해법은 재사용·변형하고, 검증 목적에 실제로 필요한 대표 품질만 구현한다.

가역적 `BALANCE_BUDGET`과 내부 기술 Spike는 완성형 Slice 제작 중 위험을 줄이는 보조 수단이며, 그 자체가 인간 플레이 검증 제품은 아니다. Core Loop를 구성하는 핵심 시스템은 먼저 parameter budget·상대값·cap·dummy-but-coherent test values를 두고 build/test 가능한 상태를 만든 뒤 실제 플레이 증거에 따라 튜닝한다. 프로젝트 고유 예산표 자체는 프로젝트 정본이 소유한다.

### `WORLD_STORYLINE_FIT_REQUIRED`

기능적으로 맞아도 세계관·핵심 스토리·플레이어 판타지를 훼손하면 완료가 아니다. 게임 프로젝트는 최소한 세계 premise, 플레이어 역할, 핵심 갈등/질문, Core Loop와 연결되는 결과·귀결의 backbone을 정의해 시스템·콘텐츠·Visual이 따로 노는 것을 막는다.

### `REUSABLE_SYSTEM_EXTRACTION`

반복해서 필요한 핵심 시스템·미니 시스템은 프로젝트 고유 수치·세계관·콘텐츠와 공용 구조를 분리해 재사용한다. 한 번의 성공만으로 새 공용 Skill이나 universal runtime을 만들지 않고, module contract → project adapter/pilot → 반복 검증 → Base promotion 순서를 따른다.

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

### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`

기존 Google Sheet는 고유 unmigrated material을 한 번 이관하기 위한 migration-only source다. `UNIQUE / DUPLICATE / OBSOLETE` 분류와 destination readback 뒤 unique material이 0이면 활성 검색·라우팅·템플릿에서 제거한다.

### Retired project surfaces

```text
EXTERNAL_HTML_WORKSPACE_RETIRED
FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY
TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW
QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW
```

Figma, 외부 HTML catalog/dashboard, project-management Tool Hub, QA Evidence Studio와 과거 localhost visual management surface는 신규 기본 작업면·필수 preflight·완료 조건이 아니다. 고유 정보·증거 vocabulary·재사용 원리가 있으면 현재 Notion/repository/PowerShell/Loop owner로 한 번 흡수하고 기본 탐색에서 제외한다.

Loop Engineering은 이 폐기 surface와 독립적이다. current operational checkpoint와 프로젝트 Package가 사용을 정당화할 때 직접 사용할 수 있다.

## 10. 시각 자산·Reference·Benchmark

Asset & Knowledge Master는 `ASSET / COMPONENT / SCREEN / REFERENCE / BENCHMARK` Record Type을 사용할 수 있다. 사람 view에는 Preview/Name/Usage/Style/Approved/Reuse처럼 판단에 필요한 정보만 보이고, AI/System view에는 ID, Project, version, Status, Prompt, source provenance, Rights / License, Hash, Implementation Path, Decision 등을 보존할 수 있다.

Reference/Benchmark decision은 필요할 때 `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`를 사용한다. 외부 자료는 요구사항 정본이 아니며 고유 표현을 복제하지 않는다.

### `PROJECT_VISUALIZATION_NEED_MAP`

프로젝트 정본·Core Loop·세계관·UI 흐름·현재 구현을 이해한 뒤, 무엇을 시각화하면 기획 정확성·일관성·구현 인계가 실제로 좋아지는지 먼저 목록화한다.

```yaml
visualization_need:
  project:
  planning_question:
  needed_artifact:
  why_visual_needed:
  exact_project_notion_target:
  source_decisions: []
  implementation_consumer:
  approval_state:
```

이미지·flow·screen mock·diagram이 의사결정을 개선하면 기획 중에도 생성/정리해 exact Project Notion에 배치하고 readback한다. 단 장식 수량 채우기나 “이미지가 있으면 좋아 보인다”는 이유만으로 생성하지 않는다. 생성물은 `DRAFT_VISUAL`/candidate와 승인 자산/runtime evidence를 분리한다.

생성·수정 이미지의 성공 보고는 upload call만으로 끝나지 않는다.

```text
generate / edit
→ correct Project target
→ upload / attach
→ readback
→ approval / rejection
→ version / replacement relation
→ repository handoff
→ runtime validation separately
```

## GPT-first 기획·검수와 선택적 Codex 보조 계약

`GPT_FIRST_PLANNING_AND_REVIEW`가 기본이다. GPT는 프로젝트 GitHub와 Notion의 현재 정본을 읽고 기획·조사·벤치마킹·대안 비교·시스템/데이터 설계·UI/UX 흐름·시각 방향·검수·적대적 검토를 닫는다. Codex는 실제 코드/Scene/Resource/data 변경, 저장소 규모가 큰 기계적 점검, 로컬 실행·테스트 등 **실행 권위가 필요한 경우에만** `OPTIONAL_CODEX_EXECUTOR`로 호출한다.

`GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY`: GPT-primary는 prose-only가 아니다. `REASONING_EFFORT_IS_NOT_WORK_EVIDENCE`이며 추론 강도는 source readback·Tool 호출·runtime·test evidence를 대신하지 않는다. `REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF`에 따라 현재 GPT 세션이 필요한 browser/repository/connector/runtime Tool을 보유하면 직접 실행하고, 별도 Codex handoff만 선택적으로 판단한다.

```text
GPT planning/research/review
→ GitHub + Notion canon reconciliation
→ >=3 alternatives + creative benchmark frontier
→ UI/UX/visual requirement + PROJECT_VISUALIZATION_NEED_MAP
→ when visuals improve decisions: generate/curate candidate visuals
→ attach to exact Project in Notion + readback
→ user/GPT review and approval state
→ implementation-ready package
→ OPTIONAL_CODEX_EXECUTOR when repository/runtime mutation is needed
→ repository implementation/runtime evidence
→ GPT final adversarial review
→ GitHub/Notion sync + readback
```

`RELEASE_NEAR_VERTICAL_SLICE_FIRST`: 기획·검수 뒤 재미·몰입·가독성·첫인상·판매 포인트·감정 곡선을 판단하는 플레이 테스트는 shipping-intent UI/UX·이미지/아트·대표 사운드·VFX/피드백·핵심 시스템/콘텐츠가 연결된 짧은 완성형 Vertical Slice에서 수행한다. 좁은 기술 질문은 `TECHNICAL_SPIKE_INTERNAL_ONLY`로 먼저 풀 수 있지만 `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`에 따라 그 결과만으로 플레이어 경험을 PASS 처리하지 않는다.

`LEGACY_ABSORB_VERIFY_REMOVE`: 더 이상 사용하지 않기로 확정된 Figma, 전용 로컬 시각 Tool/Hub, QA Evidence Studio, 외부 HTML 작업면, Google Sheets 등 구형 surface는 일상 검색·라우팅 대상에서 제거한다. 삭제 전 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`를 분류하고, `UNIQUE`한 규칙·데이터·증거·재사용 원리만 현재 Notion 또는 repository 정본으로 흡수한다. 목적지 readback과 참조 신선도 검증이 끝나면 원본과 활성 참조를 제거한다. `DUPLICATE/OBSOLETE`는 재검토를 반복하지 않는다. 법적·감사·rollback 때문에 보존이 필요한 최소 이력은 명시적 archive manifest만 남기고 기본 탐색에서 제외한다.

Google Sheets는 신규 입력을 받지 않는다. 남은 고유 자료는 Project relation을 확정해 Notion 사람용 정본 또는 repository structured/runtime owner로 이관하고, `MIGRATED_READBACK_VERIFIED`가 되면 활성 호환 surface 자체를 제거 대상으로 전환한다.

`PAID_PLAN_GATE`: 현재 승인된 유료 플랜은 `GPT_PRO` 하나다. Notion은 현재 사용 가능한 무료 범위를 기본으로 하며, 기능 제한이 실제 목표를 막고 무료/기존 대안보다 유료 Notion이 장기 총비용·정확성에서 우월하다는 근거가 있을 때만 `NOTION_PAID_PLAN_PROPOSAL`로 사용자 승인을 요청한다. 승인 전에는 결제·유료 기능 의존을 만들지 않는다.

## 적대적 검토 종료 조건

`ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 **최소 5회 floor + 이후 clean-exit** 계약이다. `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`이며 5회는 최대 quota가 아니다.

```text
FULL_SCOPE_REVIEW #1
→ validate findings → fix approved findings → verification/regression → RE-ATTACK
→ FULL_SCOPE_REVIEW #2
→ FULL_SCOPE_REVIEW #3
→ FULL_SCOPE_REVIEW #4
→ FULL_SCOPE_REVIEW #5
→ if any new valid error/conflict/omission/blocker remains: continue #6..N
→ CLEAN_REVIEW_EXIT only after minimum 5 and verified zero-blocker re-attack
```

`CLEAN_REVIEW_EXIT` 조건은 모두 필요하다.

- 완전한 전체 개선 루프 5회 이상 완료
- 새 유효 `MUST_FIX` 또는 blocking finding 0
- 정본/owner/consumer/reference 충돌 0
- acceptance criterion failure 0
- 기존 수정으로 생긴 회귀 0
- evidence ceiling 위반/미실행을 PASS로 과장한 항목 0
- 더 나은 대안 재탐색과 장기계획 적합성 재검사가 현재 증거에서 추가 변경을 요구하지 않음

1~5회 중 한 회차가 깨끗해도 최소 floor를 충족하기 전에는 종료하지 않는다. **5회 이후에도** 전체 범위를 다시 공격했을 때 새 finding이 나오면 수정·검증 후 추가 전체 루프를 수행한다. 다만 횟수를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않으며, full-scope 검토와 검증을 실제 수행했다면 finding/changes가 0인 clean loop도 유효한 회차다.

## 11. 비용 경계

### `ZERO_INCREMENTAL_COST_REQUIRED`

```text
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
```

현재 기본 유료 플랜은 **GPT Pro** 하나다. Notion은 Free 범위에서 사용하며 paid Notion AI, 별도 API credit, metered storage/automation, marketplace, 신규 유료 runner/compute/storage를 기본 경로에 넣지 않는다. 다른 유료 기능을 도입·실행·결제하려면 **새 사용자 승인**이 필요하다. 비용 상태가 불명확하면 `COST_GATE_BLOCKED`로 둔다.

## 12. 최소 5회 후 오류가 사라질 때까지의 전체 적대적 개선 루프

### `ADVERSARIAL_REVIEW_UNTIL_CLEAN`

적대적 검토를 실제로 실행할 때는 다음 **전체 범위 개선 루프를 최소 5회 수행하고, 5회 이후에는 CLEAN_REVIEW_EXIT가 성립할 때까지** 반복한다.

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_SCOPE_REVIEW
→ finding 검증
→ 개선/보완
→ 실제 검증/회귀
→ 개선된 전체 상태 RE-ATTACK
→ repeat through loop 5 even when an earlier loop is clean
→ after loop 5, continue while any valid blocker exists
→ CLEAN_REVIEW_EXIT
```

각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자산, 실패 복구, 보안, 동시성, 비용, 벤치마크, 장기 유지, 증거와 완료조건을 다시 본다. 회차 N 입력은 원칙적으로 회차 N-1의 검증된 출력 상태다.

각 회차에서 `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_REQUIRED`를 다시 확인한다. **최소 5회의 완전한 전체 개선 루프**를 수행하기 전에는 `CLEAN_REVIEW_EXIT`를 선언하지 않는다. **5회 이후에도** P0/P1, `MUST_FIX`, 정본 충돌, acceptance criterion을 막는 finding 또는 회귀가 남으면 수정·검증 후 추가 전체 루프를 수행한다. 최대 회차 수는 고정하지 않는다.

finding이 없는 의무 회차에서도 전체 범위 attack·검증·대안·장기 적합성 재검사를 실제 수행하고 evidence를 남긴다. 횟수를 채우기 위한 가짜 finding이나 불필요한 변경은 금지한다.

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
