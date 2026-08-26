# Work↔Codex 최소 전환 버티컬 슬라이스 실행 프로필

> 이 파일은 명시적 사용자 위임이 있을 때만 Work v4.9에 결합하는 선택형 실행 adapter다. 세부 절차를 복제 소유하지 않고 current Base owner를 조합한다.

## 0. Authority and owner composition

```text
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_SLICE_ONLY
COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON
CURRENT_OWNER_DETAILS_WIN_ON_DRIFT
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION
NO_AUTOMATIC_SCOPE_EXPANSION
```

Current detailed owners:

- Work continuation/recovery: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Work↔Codex role and handoff: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Visual production/approval: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Default image conversation gate: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- Shipping-intent Slice evidence: `skills/designing-vertical-slices/SKILL.md`
- HiGodot/GUT/Hera authority: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

이 프로필은 위 owner의 두 번째 정본이 아니다. 세부 owner가 바뀌면 current Base owner가 이 adapter의 오래된 문구보다 우선한다.

활성화에는 현재 사용자의 명시적 위임 evidence가 필요하다. 사용자가 routine 권장안 승인, 중간 정지 최소화, Work에서 actual game input 일괄 준비, Codex 단일 구현 window, machine QA 우선, Human QA 후속 보류를 명시해야 한다. evidence가 없거나 사용자가 더 좁은 제한을 주면 default Work v4.9와 default image approval이 유지된다.

상위 system·developer·host·tool이 confirmation을 강제하면 `HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE`를 따른다. 이 profile은 host Gate, repository ruleset, account/security confirmation을 우회하지 않는다.

## 1. Three-stage minimum-transition flow

정상 경로는 Work→Codex→Work final review의 한 round trip 뒤 사용자 검증으로 이동한다.

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
→ CODEX_SINGLE_IMPLEMENTATION_WINDOW
→ WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

```text
WORK_PRODUCTION_INPUT_BATCH
MINIMIZE_WORK_CODEX_TRANSITIONS
CONSOLIDATED_RETURN_PACKET
```

### Stage A — Work preparation

```text
Project GitHub·Notion·Base fresh-read
→ current Playable Slice 복원
→ Reuse-First + decision-relevant benchmark
→ 기획·규칙·UI/UX·data·Flow 검수 마감
→ actual-consumer Visual·Audio·VFX 입력 준비
→ provenance·rights·Acceptance·machine-QA scenario
→ adversarial review + IRG
→ WORK_PRODUCTION_INPUT_PACKET readback
→ READY_FOR_SINGLE_CODEX_WINDOW
```

### Stage B — Codex implementation

```text
Project GitHub·Notion fresh-read
→ packet 소비
→ product code·Scene·Resource·runtime wiring 구현
→ 승인 범위 bug fix·reversible refactor
→ deterministic test + runtime/build QA
→ adopted Hera live QA when applicable
→ CONSOLIDATED_RETURN_PACKET
→ READY_FOR_GPT_FINAL_REVIEW
```

### Stage C — Work final review and user handoff

```text
WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION
→ actual diff·test·runtime evidence 검수
→ valid finding correction
→ impact-bounded revalidation
→ GitHub·Notion canon/readback
→ exact-head PR gate·safe merge·new-main readback
→ scope-bounded remaining-work rescan
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

## 2. Work production-input completion

Codex 전환 기준은 문서량이 아니라 current Slice의 실제 구현 입력 readiness다.

```yaml
WORK_PRODUCTION_INPUT_PACKET:
  project_identity:
  repository:
  slice_id:
  exact_project_baseline:
  player_promise:
  player_action_or_choice:
  meaningful_tradeoff:
  expected_result:
  failure_learning_reward_feedback:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  planning_and_rules:
  ui_ux_flow:
  data_and_state_contract:
  visual_requirements: []
  approved_visual_assets: []
  audio_requirements: []
  approved_audio_assets_or_procedural_specs: []
  vfx_and_feedback_requirements: []
  localization_and_accessibility_requirements: []
  provenance_and_rights_records: []
  implementation_acceptance: []
  deterministic_test_requirements: []
  runtime_qa_scenarios: []
  build_or_export_checks: []
  required_canon_updates: []
  rollback:
  unresolved_nonblocking: []
  blocking_missing_inputs: []
  evidence_ceiling:
  readiness: READY_FOR_SINGLE_CODEX_WINDOW | BLOCKED_UNVERIFIED
```

Rules:

- current player action→choice→result→feedback에 실제 필요한 input만 준비한다.
- 여러 Slice·장기 roadmap·미래 content를 전환 절감 명목으로 합치지 않는다.
- 승인된 player outcome과 보호 의미를 고정하되 Codex의 Node·함수·Scene 내부 기술 구조를 불필요하게 선행 고정하지 않는다.
- blocking input 하나가 있어도 독립 Work 준비는 계속하고 마지막에 blocking batch를 판정한다.

## 3. Actual in-game Visual, Audio, UI, Data, and VFX

```text
PRODUCTION_INFORMATION != ACTUAL_GAME_INPUT
```

제작자·AI용 설명은 text/table/DB/Flow owner에 둔다. Codex packet의 asset/spec은 concrete game/product consumer가 있어야 한다.

### 3.1 Delegated Visual production

```text
DELEGATED_VISUAL_PRODUCTION_ACTIVE
BOUNDED_VISUAL_PRODUCTION_PACKET_REQUIRED
CURRENT_SLICE_USE_ONLY
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
```

```yaml
VISUAL_PRODUCTION_PACKET:
  requirement_id:
  actual_consumer:
  consumer_surface_and_slot:
  current_art_direction:
  approved_reference_or_style_anchor:
  required_count:
  independent_briefs: []
  format_dimensions_alpha_crop_import:
  protected_identity_and_canon: []
  excluded_scope: []
  objective_acceptance: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

명시적 delegation과 완전한 packet이 있으면 current Slice의 생성·선정·revision·Notion delivery를 per-result 질문 없이 진행할 수 있다. 생성 성공은 project asset approval, runtime consumption, Human/Player PASS가 아니다. upload/attach/readback, import, actual consumer, runtime QA가 별도 필요하다.

Art Direction master, 대표 캐릭터 identity master, 장기 store key art, 권리 불명확 자산, 승인 수량·consumer·Slice를 넘는 batch는 자동 위임 범위가 아니다.

### 3.2 Delegated Audio production

```text
DELEGATED_AUDIO_PRODUCTION_ACTIVE
BOUNDED_AUDIO_PRODUCTION_PACKET_REQUIRED
```

```yaml
AUDIO_PRODUCTION_PACKET:
  cue_id:
  actual_consumer:
  trigger_and_stop_condition:
  information_or_emotion_role:
  existing_approved_asset_or_reuse:
  file_or_approved_procedural_spec:
  format_loop_tail_loudness_priority:
  protected_audio_direction:
  excluded_scope: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

Work에 audio binary 제작 capability가 없으면 제작 완료를 추측하지 않는다.

```text
approved project audio
→ reusable rights-verified source
→ zero-incremental-cost rights-verified source
→ approved procedural audio spec legitimately implemented by product code
→ BLOCKED_UNVERIFIED
```

핵심 feedback을 무음·dummy·권리 미확인 자산으로 가린 상태는 shipping-intent readiness가 아니다.

### 3.3 UI·Data·VFX

각 input은 `owner → actual consumer → approved meaning → input/output/state → implementation acceptance → machine QA → evidence ceiling`을 가진다. 목업 존재만으로 runtime UI wiring이나 input semantics를 PASS하지 않는다.

## 4. Delegated routine approval and high-risk deferral

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
BLOCKING_HIGH_RISK_PREVENTS_PHASE_ADVANCE
NO_AUTOMATIC_SCOPE_EXPANSION
```

Auto-approved only inside the current approved Slice:

- existing project identity·Art/Audio Direction 안의 권장 세부안
- tunable default와 safe test range
- bounded actual-consumer Visual/Audio candidate
- 기술 구현 선택·국소 bug fix·reversible refactor
- 누락 test·consumer·reference·small canon sync
- actual evidence가 결정하는 최소 안전 correction
- evidence-equivalent fallback
- current-task branch·PR·exact-head safe merge

다음은 자동 실행하지 않는다.

```text
IRREVERSIBLE_DATA_LOSS
ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION
NEW_PAID_COST
LEGAL_OR_RIGHTS_UNCERTAINTY
PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION
FORCE_DIRECT_MAIN_ADMIN_BYPASS
PROJECT_CORE_IDENTITY_REPLACEMENT
BROAD_ENGINE_OR_SAVE_BREAKING_MIGRATION
```

```text
high-risk finding
→ affected task만 HIGH_RISK_DEFERRED
→ destructive action 금지
→ evidence·rollback·권장안 기록
→ independent ready work 계속
→ 같은 Slice의 high-risk 결정을 한 packet으로 묶음
→ 독립 작업 소진 뒤 사용자에게 한 번만 요청
```

high-risk item이 current Slice acceptance를 차단하면 automated readiness를 주장하지 않는다.

## 5. Stall signal and fallback ladder

시간 숫자 하나가 아니라 진전 부재 evidence를 사용한다.

```text
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
```

Stall signals include repeated same-root-cause failure, no new evidence after bounded retry/readback, non-terminal external state without progress identity, repeated output transport failure, unavailable required executor, structurally incapable route, stale project/session/head.

```text
current-state readback
→ root-cause classification
→ bounded safe retry
→ authorized fallback A
→ authorized fallback B
→ evidence-equivalent local/manual route
→ blocked task local defer
→ independent ready tasks continue
→ deferred re-evaluation on new evidence
→ global stop last
```

No infinite retry, source substitution by snippet/memory, permission bypass, new cost, or evidence downgrade. Product executor absence defers only product work while Work-owned independent tasks continue.

## 6. Codex single implementation window

```text
CODEX_SINGLE_IMPLEMENTATION_WINDOW
MINIMIZE_WORK_CODEX_TRANSITIONS
```

Codex fresh-reads current Project GitHub·Notion and executes the approved Slice continuously. Routine technical choices, reversible refactors, local bug fixes, fixtures, QA scenarios, and canon-resolvable small ambiguity do not bounce one-by-one to Work.

```yaml
CONSOLIDATED_RETURN_PACKET:
  project:
  slice_id:
  exact_baseline:
  exact_head:
  implementation_completed: []
  files_and_reasons: []
  deterministic_tests_completed: []
  runtime_qa_completed: []
  build_or_export_checks: []
  approved_visuals_consumed: []
  approved_audio_consumed: []
  missing_input_batch: []
  change_proposal_batch: []
  high_risk_deferred_batch: []
  independent_work_remaining: []
  tests_failed: []
  tests_not_run: []
  evidence_locations: []
  evidence_ceiling:
  work_reentry: NONE | FINAL_REVIEW | BLOCKING_INPUT_BATCH | HIGH_RISK_DECISION_BATCH
```

Immediate Work re-entry is limited to an actually blocking input batch with no approved alternative, project/core meaning replacement, high-risk action, or final evidence review. Missing Visual/Audio is batched while independent implementation/test work continues; player-facing placeholders cannot fake acceptance.

## 7. Machine QA first; Human QA deferred

```text
MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HERA_PERSISTENT_AUTHORING_FORBIDDEN
HERA_PHASE_SOURCE_DELTA_NONE
EVIDENCE_EQUIVALENT_MACHINE_QA_REQUIRED_WHEN_NOT_ADOPTED
```

Use the project’s adopted current authority:

- deterministic domain/state/save/data/UI logic: adopted GUT or current equivalent
- import/parse/headless/runtime/build/export checks as required
- adopted Hera: normal gameplay run/input, runtime state/UI inspection, diagnostics, screenshot and bounded visual diff
- Hera pre/post tracked source delta: `NONE`

Do not auto-install GUT/Hera merely because this profile exists. Existing Solution First, exact version compatibility, adoption record, rollback, and current owner apply. If GUT or Hera is not adopted, the current project must use an evidence-equivalent deterministic/runtime QA route; absence of an equivalent required route stays `NOT_RUN` and blocks automated readiness.

Hera must not persistently mutate Scene/Node/Script/Resource/files, use diagnostic state cheating as normal-path acceptance, or turn screenshot diff into design/readability/fun approval.

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

until the user actually plays the Slice.

```text
GUT PASS != runtime PASS != screen semantics PASS != Human comprehension PASS != Player Experience PASS
```

## 8. Scope-bounded required work zero

```text
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
COMPLETION_CANDIDATE_RESCAN
```

```yaml
ready_tasks: []
deferred_tasks: []
high_risk_deferred: []
completed_tasks: []
```

```text
ready task execute→verify→correct
→ stall recovery/fallback
→ unresolved task local defer
→ independent work continue
→ deferred re-evaluate
→ remaining machine-executable work recalculate
```

If remaining work is not zero, continue. At zero, re-scan actual implementation, planning/canon, Visual/Audio/Data consumers, deterministic tests, runtime/Hera/build evidence, PR/merge/readback, evidence ceiling, and high-risk blockers. Any valid finding reopens remaining work.

Automated readiness is blocked by missing product implementation, missing required input/consumer, mandatory machine QA `NOT_RUN`, required merge/readback missing, high-risk acceptance blocker, or unresolved P0/P1/evidence overclaim.

After correction, perform at least five full-scope adversarial loops and continue until `CLEAN_REVIEW_EXIT`.

When all machine-executable current-Slice work is zero and only the user’s explicitly deferred play validation remains:

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
```

This is not whole-product completion or Player Experience PASS.

## 9. Safe merge and user validation

A current-task PR may proceed without another routine merge question only after:

```text
latest-main reconciliation
→ exact reviewed HEAD
→ current required checks
→ unresolved thread 0
→ review blocker 0
→ conflict 0
→ protected-scope drift 0
→ high-risk blocker 0
→ repository-supported squash merge
→ new-main readback
→ required GitHub·Notion readback
→ post-merge adversarial review
```

`FORCE_DIRECT_MAIN_ADMIN_BYPASS` remains forbidden. Other open/draft/ready PRs are read-only; another SHA’s PASS is not reusable.

```yaml
USER_VERTICAL_SLICE_VALIDATION_PACKET:
  project:
  slice_id:
  build_or_scene:
  exact_commit_or_build_identity:
  launch_route:
  prerequisites:
  representative_play_window:
  expected_action_choice_result:
  expected_visual_audio_feedback:
  success_markers: []
  known_not_run: []
  evidence_capture:
  feedback_questions: []
  next_decisions: [EXPAND, FIX, TUNE, REDESIGN, HOLD, STOP]
```

Do not claim user validation before the user actually plays.

## 10. Clean-exit contract

```text
explicit delegation evidence exists
current Slice bounded
Work production inputs actual-consumer complete
routine approvals did not expand scope
high-risk actions not executed
Codex one-window implementation completed
all independent work completed before return
stall routes exhausted or locally deferred with evidence
machine-executable required work = 0
GUT/current deterministic tests complete when required
Hera/current live QA complete when required
Hera persistent mutation absent
Hera source delta NONE
runtime/build/readback evidence complete
Human/Player evidence remains NOT_RUN
current-task PR safely merged and read back when applicable
minimum five full adversarial loops complete
blocking finding = 0
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```
