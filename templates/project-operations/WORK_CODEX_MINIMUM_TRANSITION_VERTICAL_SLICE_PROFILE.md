# Work↔Codex 최소 전환 버티컬 슬라이스 실행 프로필

> 이 파일은 `CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`와 Compatibility Appendix가 명시적으로 라우팅하는 **선택형 실행 프로필**이다. Base의 Work/Codex·Visual·Vertical Slice·HiGodot/GUT/Hera owner를 대체하는 새 정본이나 새 Skill이 아니다.

## 0. Activation and authority

```text
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_SLICE_ONLY
WORK_NONPRODUCT_OWNER_PRESERVED
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER_PRESERVED
HUMAN_PLAYER_EVIDENCE_SEPARATION_PRESERVED
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
DEFAULT_IMAGE_CONVERSATION_GATE_PRESERVED_WITHOUT_DELEGATION
NO_AUTOMATIC_SCOPE_EXPANSION
```

이 프로필은 현재 사용자가 다음 의도를 명시한 경우에만 활성화한다.

```text
- routine 권장안을 승인한 것으로 취급
- 중간 승인·중단 최소화
- Work에서 기획·검수·이미지·사운드·UI·데이터 준비를 먼저 닫음
- Codex로 한 번 전환해 실제 제품 구현을 연속 수행
- GUT·Hera 등 machine QA를 우선하고 Human QA는 사용자가 실제 Slice를 플레이할 때까지 보류
- 현재 Slice의 machine-executable required work를 0까지 진행
```

활성화 evidence가 없거나 사용자가 `이미지마다 승인`, `검토만`, `PR만`, `병합하지 마`, `Codex로 넘기지 마`처럼 더 좁은 제한을 주면 기존 default 계약이 우선한다.

이 프로필은 상위 system·developer·host·tool confirmation을 우회하지 않는다. host가 특정 외부 전송·이미지 생성·파일 쓰기·병합에 confirmation을 강제하면 `HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE`로 해당 Gate를 따른다.

## 1. Intended three-stage flow

정상 경로는 한 번의 Work→Codex→Work round trip 뒤 사용자 검증으로 이동한다.

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
→ CODEX_SINGLE_IMPLEMENTATION_WINDOW
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

```text
MINIMIZE_WORK_CODEX_TRANSITIONS
WORK_PRODUCTION_INPUT_BATCH
CONSOLIDATED_RETURN_PACKET
```

### Stage A — Work preparation

```text
Project GitHub·Notion·Base fresh-read
→ current Playable Slice 복원
→ Reuse-First
→ 필요한 benchmark·시장·현업·성공/실패 사례
→ 최소 3개 대안과 권장안
→ 기획·규칙·Flow·데이터·UI/UX 마감
→ actual consumer가 있는 이미지·사운드·VFX 입력 준비
→ provenance·rights·Acceptance·QA scenario 준비
→ 적대적 검토·IRG
→ WORK_PRODUCTION_INPUT_PACKET readback
→ READY_FOR_SINGLE_CODEX_WINDOW
```

### Stage B — Codex implementation

```text
Codex가 Project GitHub·Notion fresh-read
→ WORK_PRODUCTION_INPUT_PACKET 소비
→ 실제 product code·Scene·Resource·runtime wiring 구현
→ 승인 범위 bug fix·reversible refactor 계속
→ adopted GUT deterministic test
→ import/parse/headless/runtime/build checks
→ adopted Hera live QA·screen evidence
→ consolidated missing/change/high-risk packet
→ READY_FOR_GPT_FINAL_REVIEW
```

### Stage C — Work final review and user validation handoff

```text
Work/GPT가 actual diff·test·runtime·Hera evidence 검수
→ valid finding 교정 또는 Codex consolidated correction
→ impact-bounded machine revalidation
→ GitHub structured/runtime canon + Notion human canon sync/readback
→ exact-head PR gate·safe merge·new-main readback
→ scope-bounded remaining-work rescan
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

사용자 실제 플레이 뒤 다음 중 하나를 결정한다.

```text
EXPAND | FIX | TUNE | REDESIGN | HOLD | STOP
```

## 2. Work production-input completion

Codex 전환은 문서가 많아졌을 때가 아니라 **현재 Slice의 실제 구현 입력이 닫혔을 때** 수행한다.

```yaml
WORK_PRODUCTION_INPUT_PACKET:
  project_identity:
  repository:
  slice_id:
  exact_project_baseline:
  player_promise:
  starting_context:
  player_action_or_choice:
  meaningful_tradeoff:
  expected_result:
  failure_and_learning:
  reward_and_feedback:
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

### 2.1 Scope rule

```text
CURRENT_SLICE_ONLY
SCOPE_BY_PLAYER_MEANING_NOT_DOCUMENT_VOLUME
```

- 프로젝트 전체 roadmap을 미리 구현 준비하지 않는다.
- 현재 Slice의 player action·choice·result·feedback에 실제로 필요한 input만 포함한다.
- 미래 캐릭터·전체 캠페인·장기 경제·전체 플랫폼 release asset은 현재 Slice consumer가 아니면 제외한다.
- 전환을 줄이기 위해 여러 Slice를 하나의 거대 batch로 합치지 않는다.

### 2.2 Planning readiness

Work는 최소한 다음을 닫는다.

- 플레이어가 무엇을 보고·듣고·조작하는가
- 선택지·비용·위험·trade-off가 무엇인가
- 성공·실패·보상·다음 행동이 어떻게 나타나는가
- 기존 core/system/data/save/UI 의미 중 무엇을 보호하는가
- UI/UX Flow와 decision-critical information
- data/state/input/output 의미
- edge case와 failure behavior
- actual test/runtime/play acceptance

구현 Node·함수·Scene 내부 구조를 불필요하게 고정하지 않는다. 승인된 player outcome과 보호 의미를 보존하는 기술 방법은 current repository를 읽은 Codex가 결정한다.

## 3. Actual in-game production inputs

```text
PRODUCTION_INFORMATION
!= ACTUAL_GAME_INPUT
```

제작자·AI용 시스템 설명·세계관·체크리스트·관계도는 text/table/DB/Flow owner에 유지한다. Codex packet에 들어가는 이미지·사운드·UI·VFX는 실제 consumer가 있어야 한다.

### 3.1 Visual input

```text
DELEGATED_VISUAL_PRODUCTION_ACTIVE
BOUNDED_VISUAL_PRODUCTION_PACKET_REQUIRED
CURRENT_SLICE_USE_ONLY
```

```yaml
VISUAL_PRODUCTION_PACKET:
  requirement_id:
  actual_consumer:
  consumer_surface:
  game_or_product_slot:
  current_art_direction:
  approved_reference_or_style_anchor:
  required_count:
  independent_briefs: []
  format_and_dimensions:
  alpha_crop_import_requirements:
  protected_identity_and_canon: []
  excluded_scope: []
  objective_acceptance: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

명시적 delegation이 활성이고 packet이 완전하면 current Slice 범위의 생성·선정·revision·Notion delivery를 per-result 사용자 응답 없이 계속할 수 있다.

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
```

단, 다음은 이 자동 위임에서 제외한다.

- project-wide Art Direction master 교체
- 대표 캐릭터 identity master의 얼굴·실루엣·복장·정사 변경
- store capsule·key art처럼 프로젝트 전체 첫인상을 결정하는 장기 대표 이미지
- 권리·라이선스 불명확 asset
- 승인 수량·consumer·Slice를 넘어서는 자동 batch 확장

생성 성공은 승인된 project asset·runtime consumer·Human/Player PASS가 아니다. 승인된 current-Slice use record, upload/attach/readback, import, actual screen consumer, runtime QA가 별도로 필요하다.

### 3.2 Audio input

```text
DELEGATED_AUDIO_PRODUCTION_ACTIVE
BOUNDED_AUDIO_PRODUCTION_PACKET_REQUIRED
```

```yaml
AUDIO_PRODUCTION_PACKET:
  cue_id:
  actual_consumer:
  trigger_and_stop_condition:
  player_information_or_emotion_role:
  existing_approved_asset_or_reuse:
  source_or_generation_route:
  file_or_approved_procedural_spec:
  format_sample_rate_channels:
  loop_and_tail:
  loudness_and_priority:
  variation_count:
  protected_audio_direction:
  excluded_scope: []
  provenance_and_rights:
  notion_destination:
  repository_or_runtime_destination:
  runtime_validation:
```

Work에 실제 audio binary 제작 capability가 없으면 만들었다고 추측하지 않는다. 다음 순서로 해결한다.

```text
approved existing project audio
→ project/Base reusable source
→ rights-verified zero-incremental-cost source
→ approved procedural audio specification when product implementation legitimately generates the cue
→ BLOCKED_UNVERIFIED
```

핵심 feedback이 무음·dummy·권리 미확인 상태면 shipping-intent input ready를 과장하지 않는다.

### 3.3 UI·data·VFX input

각 input은 다음을 가진다.

```text
owner
→ actual consumer
→ approved meaning
→ input/output/state
→ implementation acceptance
→ machine QA scenario
→ evidence ceiling
```

예쁜 목업이 존재한다는 사실만으로 runtime UI wiring이나 input semantics가 완료되지 않는다.

## 4. Delegated routine approval

이 프로필의 핵심은 **모든 위험을 무시하는 자동 승인**이 아니라 current Slice 안에서 안전하게 분류 가능한 routine decision을 미리 위임하는 것이다.

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
```

### 4.1 Auto-approved routine scope

- current approved project identity와 Slice 안의 권장 기획 세부안
- 기존 Art/Audio Direction 안의 bounded asset candidate
- tunable default와 safe test range
- 구현 기술 선택·국소 bug fix·reversible refactor
- 누락 test·consumer·reference·small canon sync
- actual evidence가 하나의 최소 안전안을 가리키는 correction
- current-task branch·commit·PR·exact-head safe merge
- stalled route의 evidence-equivalent fallback

각 항목마다 `진행할까요?`, `권장안으로 할까요?`, `이미지 승인할까요?`, `병합할까요?`를 반복하지 않는다. 실행 후 decision·trade-off·evidence를 최종 보고한다.

### 4.2 High-risk defer and bundle

```text
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
```

다음 literal은 자동 승인하지 않는다.

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

처리 순서:

```text
high-risk finding
→ affected task만 HIGH_RISK_DEFERRED
→ destructive action 실행 금지
→ rollback·evidence·권장안 기록
→ independent ready work 계속
→ 같은 Slice의 high-risk 항목을 한 packet으로 묶음
→ 독립 작업 소진 뒤 사용자에게 한 번만 결정 요청
```

high-risk item이 current Slice acceptance를 실제 차단하면 `AUTOMATED_VERTICAL_SLICE_READY`를 주장하지 않는다.

## 5. Stall detection and fallback

elapsed time 하나를 Base 전역 상수로 고정하지 않는다. 다음과 같은 **진전 부재 evidence**를 stall signal로 사용한다.

```text
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
```

### 5.1 Stall signals

- 같은 command/connector가 같은 root cause로 반복 실패
- bounded retry와 current-state readback 뒤 새 evidence 없음
- external service가 terminal result나 progress identity를 제공하지 않음
- output truncation·transport failure가 같은 evidence path에서 반복
- required executor가 current session에서 callable하지 않음
- 현재 route가 구조적으로 required artifact/upload/readback/runtime result를 만들 수 없음
- stale session·wrong project·wrong head가 계속 탐지됨

### 5.2 Recovery ladder

```text
current state readback
→ root-cause classification
→ bounded safe retry
→ authorized fallback A
→ authorized fallback B
→ evidence-equivalent local/manual route when available
→ blocked task local defer
→ independent ready tasks continue
→ new evidence마다 deferred 재평가
→ global stop last
```

규칙:

- 동일 실패를 무한 재시도하지 않는다.
- fallback은 evidence·보안·권한·비용 수준을 낮추지 않는다.
- 첫 tool이 실패했다는 이유로 current session에 callable한 다른 connector/tool을 무시하지 않는다.
- source가 필수인데 읽을 수 없으면 snippet·memory·추측으로 우회하지 않는다.
- product executor가 없으면 product implementation만 `DEFERRED_EXTERNAL_EXECUTOR`로 두고 Work-owned independent task를 계속한다.

## 6. Codex single implementation window

```text
CODEX_SINGLE_IMPLEMENTATION_WINDOW
MINIMIZE_WORK_CODEX_TRANSITIONS
```

Codex는 current Project GitHub·Notion과 packet을 fresh-read하고, 승인된 Slice 구현과 machine QA를 가능한 한 하나의 연속 window에서 닫는다.

### 6.1 Continue without routine bounce

Codex는 다음을 Work로 즉시 한 건씩 반환하지 않는다.

- 기존 의미를 보존하는 기술 구현 선택
- 승인 범위의 reversible refactor
- local bug fix
- test fixture·runtime scenario 보완
- 비차단 문서/asset locator 누락
- 동일 Slice 안의 작은 acceptance ambiguity가 current canon으로 해소됨

이를 구현하거나 `CONSOLIDATED_RETURN_PACKET`에 기록하면서 독립 작업을 계속한다.

### 6.2 Consolidated return packet

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

Work 재진입 조건:

- packet으로 해결할 수 없는 blocking input batch
- project core identity·major UX·economy/story/Art master replacement
- high-risk category
- 구현·machine QA 완료 뒤 GPT final evidence review

`WAITING_GPT_VISUAL` 같은 반환이 생겨도 Codex는 가능한 독립 구현·test·QA를 먼저 진행하고 missing visual을 batch로 모은다. 단, 잘못된 placeholder로 player-facing acceptance를 꾸미지 않는다.

## 7. Machine QA first; Human QA deferred

현재 사용자 결정:

```text
MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
```

이 결정은 Human QA를 PASS 처리한다는 뜻이 아니다. 자동화 phase에서 machine-executable evidence를 최대한 확보하고, Human/Player evidence는 완성 Slice를 사용자가 직접 검증하는 다음 milestone로 이동한다.

### 7.1 Deterministic tests

```text
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
```

프로젝트가 GUT을 채택했다면 다음을 검증한다.

- domain rule·state transition
- economy/combat/puzzle logic
- save/load and data transformation
- repeatable UI/domain logic
- fixed regression from implementation findings

GUT이 채택되지 않았다면 자동 설치하지 않는다. current project test authority를 사용하고, 필요한 GUT adoption은 Existing Solution First와 exact compatibility Gate를 따른다.

### 7.2 Hera live QA and screen evidence

```text
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HERA_PERSISTENT_AUTHORING_FORBIDDEN
HERA_PHASE_SOURCE_DELTA_NONE
```

프로젝트가 Hera를 채택했다면 다음 범위에서 사용한다.

- exact Editor/game readiness
- normal gameplay run/stop
- player-path input injection·semantic click
- runtime tree/state assertion
- runtime UI inspection
- diagnostics and output
- material screen screenshot capture
- bounded screenshot diff with platform/resolution/renderer identity
- source pre/post snapshot

Hera로 다음을 하지 않는다.

- persistent Scene/Node/Script/Resource/file mutation
- acceptance를 위한 diagnostic state cheating
- screenshot diff를 디자인·가독성·접근성·재미·Human approval PASS로 승격

Hera QA 직전·직후 tracked source delta는 `NONE`이어야 한다. 예상하지 않은 source delta가 생기면 QA PASS가 아니라 root-cause finding이다.

### 7.3 Other machine evidence

필요에 따라 다음을 실제 실행한다.

```text
import/parse
headless smoke
runtime representative flow
build/export
performance sample window
target-platform machine checks
asset import/consumer verification
Notion/repository readback
```

실행할 수 있는데 실행하지 않은 mandatory machine Gate는 `NOT_RUN`이며 automated readiness를 막는다.

### 7.4 Evidence ceiling

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

사용자가 실제 Slice를 플레이하기 전까지 유지한다.

```text
GUT PASS
!= runtime PASS
!= screen semantics PASS
!= Human comprehension PASS
!= Player Experience PASS
```

## 8. Scope-bounded remaining-work zero

```text
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
COMPLETION_CANDIDATE_RESCAN
```

`남은 작업 0`은 현재 approved Slice와 automation phase에만 적용한다. 프로젝트 전체 future roadmap을 자동으로 소비하지 않는다.

### 8.1 Queue

```yaml
ready_tasks: []
deferred_tasks: []
high_risk_deferred: []
completed_tasks: []
```

### 8.2 Loop

```text
ready task 실행
→ verify
→ valid finding correction
→ stall이면 recovery/fallback
→ 해결 불가 task만 local defer
→ independent ready work 계속
→ deferred 재평가
→ remaining machine-executable work 재계산
```

`remaining > 0`이면 계속한다.

`remaining = 0`이면 즉시 완료하지 않고 다음을 수행한다.

```text
COMPLETION_CANDIDATE_RESCAN
→ implementation
→ planning/canon
→ visual/audio/data consumer
→ deterministic tests
→ runtime/Hera/build evidence
→ PR/merge/readback
→ evidence ceiling
→ high-risk blocker
→ valid finding?
   YES: remaining work reopen → correct → reverify
   NO: final-state adversarial review
```

최소 5회 full-scope adversarial loop와 `CLEAN_REVIEW_EXIT`를 유지한다.

### 8.3 What blocks automated readiness

- current Slice required product implementation missing
- actual consumer가 필요한 image/audio/data input missing
- mandatory deterministic/runtime/build QA `NOT_RUN`
- required PR merge or new-main/Notion readback missing
- high-risk deferred item이 current Slice acceptance를 차단
- evidence ceiling overclaim 또는 unresolved P0/P1

### 8.4 What becomes the next milestone

다음은 숨은 미완료가 아니라 명시된 후속 milestone이다.

- `HUMAN_QA_DEFERRED_BY_CURRENT_USER`
- `READY_FOR_USER_VERTICAL_SLICE_VALIDATION`
- current Slice 밖 future improvement
- user validation 결과에 따라 열리는 다음 Slice

따라서 machine-executable required work가 0이고 모든 machine Gate가 닫히면 다음 상태를 허용한다.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
```

이는 전체 제품 완료나 Player Experience PASS가 아니다.

## 9. PR and merge automation

```text
CURRENT_TASK_SAFE_MERGE_STANDING_AUTHORIZATION
```

현재 사용자 delegation과 current-task continuation이 있고 PR이 latest completed main에서 만든 하나의 명확한 current-Slice PR이면 routine merge confirmation을 다시 묻지 않는다.

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
→ new-main SHA readback
→ required GitHub·Notion readback
→ post-merge adversarial review
```

금지:

```text
FORCE_DIRECT_MAIN_ADMIN_BYPASS
```

다른 open/draft/ready PR은 read-only다. 다른 SHA의 PASS를 재사용하지 않는다.

## 10. Incident, fallback, and Base learning

material failure는 다음 packet으로 남긴다.

```yaml
INCIDENT_SOLUTION_LESSON:
  symptom:
  exact_environment_version_sha_tool:
  root_cause:
  attempted_routes: []
  failed_routes: []
  final_solution:
  actual_evidence:
  recurrence_guard:
  project_only_details: []
  reusable_principle:
  non_applicable_conditions: []
  base_promotion_disposition:
  rollback:
```

- project-specific path·asset·value는 Project owner에 둔다.
- 반복 가능하고 project-neutral한 evidence만 Base proposal/case candidate로 올린다.
- `NO_NEW_REUSE_LEARNING` 또는 `NO_BASE_PROMOTION`도 유효한 종료 판정이다.

## 11. Handoff and final report

### 11.1 Work→Codex handoff

Codex work instruction에는 `WORK_PRODUCTION_INPUT_PACKET`의 locator와 다음을 포함한다.

- exact Project and repository
- approved player outcome
- scope/non-scope/protected scope
- actual visual/audio records and durable locators
- data/UI/Flow meanings
- acceptance and machine QA scenarios
- forbidden changes
- consolidated return expectation
- rollback

### 11.2 Codex→Work return

한 건씩 대화로 되돌리는 대신 `CONSOLIDATED_RETURN_PACKET`을 사용한다. Work는 actual diff·tests·runtime evidence를 fresh-read하고 report만 믿지 않는다.

### 11.3 User validation packet

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
  next_decisions:
```

사용자가 실제 플레이하기 전에 `사용자가 검증했다`고 보고하지 않는다.

### 11.4 Final reporting order

```text
작업 전
→ 발견 문제
→ Work 준비 묶음
→ Codex 실제 구현
→ 이미지·사운드·UI·data 실제 consumer
→ GUT/Hera/runtime/build evidence
→ IRG evidence layer
→ valid finding과 correction
→ PR·merge·new-main/Notion readback
→ remaining machine work
→ high-risk deferred packet
→ Human/Player NOT_RUN
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
→ 사용자 실행·검증 방법
```

## 12. Clean-exit checklist

```text
explicit delegation evidence exists
current Slice bounded
Work production inputs actual-consumer complete
routine approvals did not expand scope
high-risk actions not executed
Codex one-window implementation attempted
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
