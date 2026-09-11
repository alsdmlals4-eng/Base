# Base 장기 작업 실행 정책

이 문서는 Base와 Base를 채택한 프로젝트에서 시간보다 기획 의도·정확성·복원성·검증 가능성을 우선하는 L1 이상 장기 작업의 공용 생명주기를 정의한다.

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
GPT_NONCODING_PROJECT_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
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
FULL_LOOP_COUNT_MINIMUM: 2
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 2
POSTMERGE_PROMOTION_AND_SUPERSESSION
POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP
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
REPOSITORY_PRIMARY_CANON
HUMAN_GDD_PDF_DERIVED_VIEW
V4_NOTION_EXCEPTION_ONLY
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
REMAINING_WORK_COMPLETION_GATE: REQUIRED
REMAINING_WORK_RECALCULATION_REQUIRED: REQUIRED
IMPLEMENTATION_CORRECTION_RESCAN: REQUIRED
POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED: REQUIRED
FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK: REQUIRED
```

## 2. 역할 경계

장기작업에서도 owner는 파일 확장자가 아니라 **작업의 성격**으로 정한다.

### GPT

- Base 정책·Skill·Guide·Template·Learning
- Base Python test·CI contract·Registry/generated·Manifest·checker
- Notion Home/Domain/AI System
- 기획·GDD·밸런스·데이터표·Flow·Storyboard
- 벤치마킹·시장/현업 조사·최소 3안 비교
- 적대적 검토·IRG
- 이미지 생성·편집·검수·Notion 승인 delivery
- GitHub 비제품 문서/정본
- 문제→교훈→Base 승격
- 실제 Godot 구현 전 Work Instruction
- Codex 구현 결과 최종 검수

### Codex

실제 게임 프로젝트의 **Godot 제품 구현**만 맡는다.

- GDScript/product code
- Scene/Resource/Autoload/runtime wiring
- runtime game data integration
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- build/export
- Godot implementation/runtime/headless/play test

`CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`: Base test·Registry·generated·CI가 코드 형식이어도 Codex 대상이 아니다.

## 3. 기본 흐름

`BEST_LONG_TERM_EFFICIENT_METHOD`는 빠른 답변·최소 Tool 수가 아니라 사용자/플레이어 가치, 정확성, 출시 품질, 유지보수성, 재사용성, 되돌리기 가능성, 위험과 총비용을 함께 본다. `QUALITY_OVER_RESPONSE_SPEED`와 `BENCHMARK_PRACTICE_COMPARISON`을 유지한다.

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
→ GPT NONCODING WORK / NOTION / VISUAL / BASE GOVERNANCE
→ 실제 Godot 제품 구현 필요 여부
   ├─ NO → GPT VERIFY / READBACK
   └─ YES → GPT Work Instruction
             → Codex Project GitHub + Notion Rehydration
             → Godot Product Build / Runtime / Play Evidence
             → GPT Final Review
→ EXACTLY 2 FULL ADVERSARIAL ROUNDS, THEN TARGETED VERIFICATION
→ LONG-TERM FIT CLOSURE
→ EXACT-HEAD PR GATE
→ MERGE
→ POSTMERGE READBACK
→ LESSON PROMOTION / SUPERSESSION
→ REMAINING_WORK_RECALCULATION_REQUIRED
→ REQUIRED WORK REMAINING = 0 ? COMPLETION_CANDIDATE : CONTINUE
→ IMPLEMENTATION_CORRECTION_RESCAN
→ POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ SAME FINAL POST_CHANGE_MONITOR_LOOP
→ CONTINUE same final-state lineage WITH POSTMERGE EVIDENCE UNTIL CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
```

## 4. `DEEP_WORK_PREANSWER_GATE`

L1 이상 또는 조사·벤치마킹·검토·구현·검증을 명시한 요청은 `REQUIRED_EVIDENCE_BEFORE_FINAL`이다. 현재 정본·실제 상태·필요한 외부 원출처·최소 3개 실질 대안·구현 현실성·적대적 검토·검증을 수행하기 전에 substantive final로 종료하지 않는다.

`INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION`: 중간보고 생략은 작업 생략이 아니다.

`NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION`: 필수 evidence가 `NOT_RUN`이면 완료가 아니다. `BLOCKED_UNVERIFIED`와 해제 조건을 기록하고 독립 가능한 작업은 계속한다.

`GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY`: GPT는 prose-only가 아니다. Base/Notion/문서/표/이미지/검증 인프라를 실제 도구로 수정·검증한다. 다만 실제 게임 프로젝트의 Godot 제품 구현 owner는 Codex다.

`REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF`: 현재 GPT 세션의 연결 도구로 수행할 수 있는 **Base/Notion/문서/검증 인프라의 필수 read/write/test/readback**은 실제로 실행한다. Codex가 별도 실행자로 존재하는지와 혼동해 GPT-owned 필수 작업을 `NOT_RUN`으로 미루지 않는다. 실제 Godot 제품 구현만 별도의 Codex handoff 경계를 따른다.

## 5. `DIRECTION_FIRST`

1. 사용자 목표·플레이어 가치·성공 조건·비목표를 복원한다.
2. 최신 main, 같은 Goal의 열린·최근 병합 PR, 현재 정본, 실제 구현, 테스트·실패 증거를 대조한다.
3. 세부 구현 편의가 큰 방향을 역으로 결정하지 못하게 한다.
4. 프로젝트 코어·플레이어 경험·비용·범위를 바꾸는 선택만 사용자 결정으로 올린다.

## 6. 현행 조사·대안·벤치마킹

### `CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`

L1 이상 중요한 결정은 **현행 조사 → 최소 3개 → 벤치마킹 → 동일 기준 비교 → 임시 권장안 → 더 나은 방안 → 전체 적대적 검토 → 장기적으로 최선** 순서다.

`MINIMUM_VIABLE_ALTERNATIVES: 3`은 숫자 채우기가 아니다. 현행 유지, 기존 해법 재사용/흡수, 최소 수정, 구조 개선, 검증된 외부 해법, 신규 구축 중 materially distinct 후보를 확보한다.

비교 기준에는 최소 사용자/플레이어 가치, 정확성, 위험, 수명주기 비용, 유지보수성, 되돌리기 난이도, 재사용성, 증거 강도, 비용 경계를 포함한다.

### `BENCHMARK_SYNTHESIS`

**벤치마킹은 한 성공사례를 모방하는 절차가 아니다.** 실무사례·실패사례를 여러 개 비교한다.

```text
ADOPT / ADAPT / REJECT
```

### `CREATIVE_BENCHMARK_FRONTIER`

```text
DIRECT_GENRE_BEST_IN_CLASS
+ ADJACENT_GENRE_BEST_IN_CLASS
+ DISTINCTIVE_OR_INNOVATIVE_WORK
+ FAILURE_OR_MIXED_CASE
+ PROJECT_INTERNAL_STRENGTH
→ transferable principles
→ project-specific synthesis
```

### `ORIGINALITY_FUN_CREATIVITY_REVIEW`

`FUN_HYPOTHESIS`와 실제 player evidence를 분리한다. 재미 PASS는 실제 사람 플레이 evidence 전에는 주장하지 않는다.

`BETTER_ALTERNATIVE_SEARCH`는 최초 권장안을 보호하지 않는다. 새 증거가 생기면 **장기적으로 더 강한 방안**인지 다시 비교한다. `LONG_TERM_PLAN_FIT_REQUIRED`를 매 중요 checkpoint에서 재확인하고 최종 보고에는 왜 현재 후보 중 **장기적으로 최선**인지와 재검토 조건을 남긴다.

## 7. 구현 전 Gate

### `EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD`

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

Base/Notion/noncoding BUILD는 GPT가 수행한다. 실제 Godot 제품 BUILD만 Codex Work Instruction으로 전환한다.

## 8. 승인 후 연속 실행

### `SINGLE_INITIAL_APPROVAL_THEN_CONTINUE`

완전한 작업 계약을 한 번 승인받은 뒤 같은 범위의 구현·테스트·실패 진단·가역적 수정·PR·exact-head 검사·적대적 검토·회귀·허용 병합·postmerge readback은 routine approval로 멈추지 않는다.

`CONTINUATION_INTENT_ALIASES`: `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행`은 같은 승인 범위의 계속 실행 의도로 해석한다.

- GPT-owned Base/Notion/noncoding 작업은 GPT가 계속한다.
- Godot product task가 되면 Codex handoff를 준비한다.
- 새로운 제품 결정·범위 확대·파괴적 migration·새 비용·권한 확대는 기존 승인으로 덮지 않는다.

### `APPROVED_BLUEPRINT_END_TO_END_DELIVERY`

사용자와 방향·기획·기본 설계를 논의하고 검토·보완한 뒤 구현 승인을 받으면, 승인된 범위 전체를 사용자가 실제 실행·테스트할 수 있는 결과로 인도한다. 단계 전환·상세 설계 완료·한 Slice 완료·담당 인계만을 이유로 다시 “진행할까요?”를 묻거나 종료하지 않는다.

- 기존 Goal·작업 카드에 승인 참조와 블루프린트의 필수 기능·화면·상태·이미지 및 다른 자산·실제 consumer·검증의 대응을 연결한다. 별도 중복 정본은 만들지 않는다. `ALL_APPROVED_REQUIREMENTS_COVERED`: 전체 블루프린트 구현을 승인받았다면 모든 필수 항목을 닫는다. Slice는 실행 단위이지 승인 범위를 임의로 줄이는 수단이 아니다. 미승인·후속·보류 아이디어는 구현 범위에 끼워 넣지 않는다.
- 각 작업의 현재 정본·실제 구현을 읽고 기존 해법과 벤치마크를 재사용하거나 필요한 새 조사를 수행해 `ADOPT / ADAPT / REJECT`를 기록한다. 승인 의미 안의 가역적 권장 선택 → 상세 설계·구현 → 자동 검사·Godot 실행·실제 화면 검증 → 실패 원인 교정 → 영향 범위 재검증을 이어간다. 같은 실패의 맹목 반복이나 무제한 재검토 대신 기존 복구·검토 규칙을 적용한다. 적대적 전체 검토는 동일 후보 계보에서 2회이며 발견 사항의 교정·표적 재검증과 필요한 독립 검토는 구별한다.
- 승인 자산을 먼저 재사용하고 실제 씬·노드·리소스·상태에 연결한다. 이미지 파일 생성이나 문서에 붙이기만으로 구현 완료가 아니다. 구현 승인이 아직 보지 않은 새 후보 이미지의 최종 승인은 아니다. 필요한 시각 결정을 가능한 한 승인 묶음에서 준비하고, 남은 사용자 결정은 근거와 함께 모으며 독립 실행 가능한 승인 작업은 계속한다. 기존 이미지 제작 담당·승인·권리 규칙을 우회하지 않는다.
- `HANDOFF_IS_NOT_DELIVERY`: GPT 기획 종료는 담당 전환이며 전체 구현 작업의 완료가 아니다. 현재 허용되고 사용 가능한 실행 경로로 Codex가 이어받는다. 실행기가 없거나 실제 권한·자료가 차단되면 완료를 주장하지 않고 완료분·미완료분·정확한 blocker·재개 방법을 보고한다. 폐기된 로컬 호출 경로나 새 권한을 임의 복구하지 않는다.
- `USER_TESTABLE_DELIVERY`: 모든 승인 필수 항목의 실제 구현과 자산 연결, 적용 가능한 자동 검사·Godot 실행·화면 증거, 필요한 PR 검토·필수 CI·정상 병합·병합 후 readback까지 확인한다. 사용자에게 실행할 프로젝트 또는 빌드의 정확한 위치·revision, 시작 방법, 핵심 테스트 경로와 알려진 제한을 제공한다. 실행에 필요한 파일을 정리 대상으로 옮기지 않는다. 프로젝트 규칙에 따라 작업 소유 Godot 프로세스는 종료할 수 있으며 실행 가능 상태가 항상 에디터를 켜 두라는 뜻은 아니다.
- 블루프린트의 계획 대비 실제 구현 상태·연결도·인게임 이미지·설명을 갱신한다. 무엇이 바뀌었는가 / 어떤 연결로 작동하는가 / 사용자가 어떻게 확인하는가를 설명하며 기존 학습 자료 owner를 재사용한다. `USER_TESTABLE_NOT_HUMAN_PASS`: 사용자가 테스트할 수 있다는 사실과 사용자 플레이·UX 승인 PASS를 구분한다. 필수 미구현·미검증 항목이 남으면 전체 완료로 쓰지 않는다.
- `RECOVERABLE_DESKTOP_CLEANUP`: 정리 시 `skills/governing-legacy-retention-and-archives/SKILL.md`를 적용한다. 사용자가 요청한 삭제 가능 파일은 참조·consumer·보존 의무·소유권을 확인한 뒤, 현재 Windows의 실제 바탕화면 경로를 조회하여 프로젝트별 정리 폴더에 복구 가능하게 보관한다. 이동 전 절대 대상 경계와 충돌을 확인하고 원래 경로·보관 경로·SHA-256·이유·복원 방법을 기록하며 이동 후 해시와 참조·실행을 재확인한다. 바탕화면은 정본이나 runtime consumer 경로가 아니다. 활성 코드·승인 자산·저장 데이터·필요한 빌드·검증 증거·비밀정보·소유권 불명 파일은 이동하지 않는다. 추적 파일 제거는 같은 변경의 PR·검증에 포함하고 영구 삭제는 별도 권한 없이 하지 않는다. 대상이 없으면 폴더를 만들지 않고 0건으로 보고한다.

새 제품 방향·범위·고위험 변경·비용·보안·권한 결정은 기존 승인으로 덮지 않는다. 기술적 선택이나 담당 전환은 반복 승인의 이유가 아니지만 실제 사용자 결정·도구 차단을 숨기지 않는다.

### `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`

`APPROVED_CONTRACT_CONTINUATION`이고 latest completed `main`에서 만든 단 하나의 current-task PR이면 exact HEAD, required checks, review/thread/ruleset Gate 통과 뒤 merge와 postmerge readback까지 포함한다.

`pre-existing`, `unrelated`, `other-workstream`, `draft` PR, force push, ruleset bypass, 사용자의 `병합하지 마`/`PR만 열어`/`검토만`은 예외다.

## 9. 실패 복구

### `RECOVER_TRY_ALTERNATIVES_RESUME`

```text
failure / interruption
→ side effect 판정
→ authoritative state readback
→ root-cause hypothesis
→ safe route A
→ 필요 시 B/C
→ rollback / containment
→ completed work 보존
→ incomplete work만 resume
→ regression recheck
```

같은 실패 명령을 맹목 반복하지 않는다.

## 10. 독립 workstream 격리

```text
INDEPENDENT_WORKSTREAM_ISOLATION
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
FOLLOW_UP_TARGET_IS_MERGED_MAIN
```

`open / draft / ready` PR·branch는 기본 read-only다. current-state read는 가능하지만 checkout/write/rebase/close/merge/selective-copy/material-delta 흡수는 하지 않는다. 단 current-task PR의 승인된 merge 예외는 `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE`만 따른다.

## 11. 게임 작업 계약

### `RELEASE_NEAR_VERTICAL_SLICE_FIRST`

기획·검수 뒤 첫 인간 플레이 테스트는 짧더라도 실제 출시 의도에 가까운 Vertical Slice를 대상으로 한다. 이 Slice의 UI·이미지·오디오·VFX·시스템은 단순 throwaway mock이 아니라 **실제 게임 사용 후보**를 우선해 전체 경험을 검증한다.

플레이어가 보는·듣는·조작하는 경로에는 임시 `player-facing placeholder`나 dummy 표현을 남겨 플레이 경험을 왜곡하지 않는다.

```text
GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE
SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED
SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE
TECHNICAL_SPIKE_INTERNAL_ONLY
EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT
BALANCE_BUDGET
WORLD_STORYLINE_FIT_REQUIRED
REUSABLE_SYSTEM_EXTRACTION
```

시스템-only PoC는 기술 질문에는 쓸 수 있지만 재미·몰입·판매력·전체 UX PASS 근거가 아니다.

`EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`: 승인 자산·기존 모듈·검증된 외부 해법을 먼저 확인하고 `ADOPT / ADAPT / REJECT`한다.

## 12. 프로젝트 작업면·데이터 권위

### `REPOSITORY_PRIMARY_CANON` + `HUMAN_GDD_PDF_DERIVED_VIEW`

repository는 사람용 프로젝트 개요·Flow·Visual·표·핵심 시스템 이해의 정본이며 exact-SHA `HUMAN_GDD_PDF_DERIVED_VIEW`는 사람이 보는 파생 snapshot이다. `V4_NOTION_EXCEPTION_ONLY` / `NO_NEW_NOTION_WRITE_BY_DEFAULT`: Notion은 explicit exception 또는 legacy migration source일 때만 사용한다. 모든 project record는 `PROJECT_RELATION_REQUIRED`를 지킨다.

```text
WORK_MASTER
ASSET_KNOWLEDGE_MASTER
VISUAL_MAP_DERIVED
```

### `REPO_NATIVE_STRUCTURED_DATA`

실제 게임 runtime code, Scene, Resource, runtime config, tracked product asset, build/test 상태는 repository/runtime evidence가 소유한다.

Base의 정책·Skill·Registry/generated·CI/test contract는 runtime product code가 아니며 GPT governance owner가 유지한다.

### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`

고유 미이관 자료만 migration source로 사용한다.

### Retired project surfaces

```text
EXTERNAL_HTML_WORKSPACE_RETIRED
FIGMA_DEPRECATED_NOT_ACTIVE_AUTHORITY
TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW
QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW
```

## 13. Visual / Codex 경계

`PROJECT_VISUALIZATION_NEED_MAP`으로 필요한 시각화만 선정한다.

```text
GPT generate / edit / review
→ repository candidate path / manifest / exact-SHA derived view
→ readback
→ V4 exception upload/attach only when explicitly approved
→ approval / rejection
→ 실제 Godot 제품 구현 필요?
   ├─ NO → GPT 종료
   └─ YES → Codex Godot Work Instruction
             → approved Visual 소비
             → runtime validation
```

Codex는 이미지 생성·생성형 편집·임의 AI placeholder를 만들지 않는다. 부족하면 `GPT_VISUAL_REQUEST`다.

## 13A. Legacy 흡수·검증·제거

`LEGACY_ABSORB_VERIFY_REMOVE`: 더 이상 사용하지 않는 Figma, 전용 local visual Tool/Hub, QA Evidence Studio, external HTML workspace, Google Sheets 같은 구형 surface는 `UNIQUE / DUPLICATE / OBSOLETE`로 한 번 분류한다. UNIQUE한 규칙·데이터·증거·재사용 원리만 현재 repository owner와 exact-SHA derived view로 흡수하고 destination readback·consumer 확인 뒤 active route에서 retirement한다. V4 exception destination은 실제 적용된 경우에만 별도로 확인한다.

`PAID_PLAN_GATE`: 현재 기본 유료 플랜은 **GPT Pro** 하나다. Notion은 Free 범위를 기본으로 하며 별도 API credit·SaaS·runner·compute/storage는 **새 사용자 승인** 전 도입하지 않는다.

## 14. 적대적 검토 종료 조건

`ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 **정확히 2회 전체 검토 + 필요한 결함별 수정·검증 + clean-exit**다. 회차 상한·계보·재사용·차단의 정본은 `docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md`다.

```text
FULL_LOOP_COUNT_MINIMUM: 2
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 2
FULL_SCOPE_REVIEW
→ finding 검증
→ 개선/보완
→ 실제 검증/회귀
→ 개선된 전체 상태 RE-ATTACK
→ complete exactly two full-scope rounds
→ after round 2, targeted correction/verification only; no automatic third full review
→ CLEAN_REVIEW_EXIT
```

병합 전 검토와 postmerge readback은 서로 다른 완료를 과장하기 위한 중복 cycle이 아니다. 마지막 교정부터 merge/postmerge 증거까지 **same final-state lineage**로 이어지는 동일 상태를 검증한다. 2회 이후에는 영향 범위 교정·검증과 main readback만 하며 전체 적대 검토를 추가하지 않는다.

`CLEAN_REVIEW_EXIT`에는 새 유효 오류·충돌·누락·blocking finding 0, 정본/owner/consumer/reference 충돌 0, acceptance failure 0, 회귀 0, evidence ceiling 위반 0이 필요하다.

## 15. 비용 경계

```text
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
```

Notion은 Free 범위를 기본으로 하고 새 유료 API/SaaS/runner/compute/storage는 사용자 승인 전 도입하지 않는다.

## 16. PR·병합·postmerge

작업은 self-contained slice로 진행한다. 병합 전 exact head, required checks, unresolved thread 0, P0/P1 0, 비용/보안 Gate를 확인한다.

### `POSTMERGE_PROMOTION_AND_SUPERSESSION`

병합 뒤 main을 다시 읽고 replacement pointer와 실제 consumer를 확인한다.

### `POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP`

병합 뒤 새 main, repository primary canon, asset manifest, exact-SHA human projection과 runtime evidence를 readback하고 전체 승인 범위를 재공격한다. 명시된 V4 Notion exception이 있을 때만 해당 destination을 추가 readback한다. 유효 finding은 `POSTMERGE_CORRECTION_REQUIRED`로 처리하고 `PROGRESS_READBACK_REQUIRED`에 따라 남은 작업을 다시 계산한다. 이 검증은 premerge 마지막 교정과 **same final-state lineage**를 유지한다.

## 17. 완료 조건

```yaml
required_work_remaining: 0
remaining_work_recalculation_status: PASS
implementation_correction_rescan_status: PASS
completion_adversarial_review_status: PASS
clean_review_exit_status: PASS
external_blockers: []
optional_backlog: []
```

`REQUIRED_WORK_REMAINING: 0`은 완료 후보일 뿐이다. `REMAINING_WORK_RECALCULATION_REQUIRED` → `IMPLEMENTATION_CORRECTION_RESCAN` → `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED` → `CLEAN_REVIEW_EXIT` 순서를 닫아야 한다.

## 18. 신선도와 교훈 승격

작업 시작 시 latest main SHA, `AGENTS.md`, `START_HERE.md`, Documentation Map, Skill Registry, same-goal open/recent PR, current tool/runtime checkpoint를 다시 찾는다.

`REUSABLE_LESSON_PROMOTION_GATE`:

```text
incident / solution
→ REUSE_EXISTING_OWNER
→ EXTEND_REFERENCE_OR_MODE
→ EXTRACT_MODULE
→ BASE_CHANGE_PROPOSAL
→ NEW_SKILL_LAST
```

한 번의 성공을 즉시 새 Skill·local tool·SaaS 권위로 승격하지 않는다.

## 18A. 사용자 학습형 완료보고

최종 보고는 파일 목록이 아니라 `작업 전 → 개선된 기능 → 실제 사용 예 → 기대효과 → 아직 개선되지 않은 범위`를 사람이 이해할 수 있게 설명한다.

## 19. 현재 한 줄

> **GPT는 Base·Notion·기획·검수·문서·표·이미지·운영 인프라를 담당하고, Codex는 실제 게임 프로젝트의 Godot 제품 구현·코딩·runtime/play test만 담당한다.**
