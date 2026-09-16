# Conditional Codex Implementation Work Instruction

> 이 Template은 **사용자 요청, 현재 세션의 실제 capability 부족, 또는 근거 있는 격리 실행 때문에 Codex를 선택한 경우**의 조건부 작업지시문이다. 기존 파일명은 호환성을 위해 유지한다.
>
> 기본 경로는 `UNIFIED_WORK_EXECUTION`이다. capable Work는 승인 범위의 기획·상세 설계·구현·검증·검토·통합을 계속한다. 코드가 있다는 이유로 전환하지 않으며, 별도 handoff가 없으면 이 파일을 매 작업 복제하지 않는다. capability는 사용자 승인·repository 권한을 대체하지 않는다.

## 0. Handoff Contract

```yaml
handoff_mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
executor_selection: CAPABILITY_BASED_EXECUTOR_SELECTION
handoff_reason: USER_REQUEST | MISSING_CAPABILITY | ISOLATED_EXECUTION
selected_executor: CODEX
project:
repository:
base_branch:
target_branch_or_pr:
exact_source_sha:
base_observed_head_sha:
base_adopted_contract_sha:
base_execution_sha:
base_drift_classification: NO_RELEVANT_DRIFT | COMPATIBLE_ADOPTION | MIGRATION_REQUIRED | PROJECT_OVERRIDE | BLOCKED_UNVERIFIED
blueprint_pass_1_revision:
blueprint_pass_2_final_revision:
user_final_approval_decision_id:
implementation_authority_revision:
work_slice_mode: PLAY_MEANINGFUL_WORK_SLICE
work_slice_id:
work_instruction_status: APPROVED_IMPLEMENTATION_READY
planning_readiness: APPROVED_CANON_READY
implementation_owner: CURRENT_AUTHORIZED_CAPABLE_EXECUTOR
final_review_owner: CURRENT_REVIEW_OWNER
actual_state_verification_required: true
repository_rehydration_required: true
github_rehydration_required: true
notion_rehydration_required: false
legacy_notion_migration_source_optional: true
image_generation: IMAGE_TOOL_REQUIRED_CANDIDATE_APPROVAL_REQUIRED
visual_input_contract: APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
missing_visual_action: CANDIDATE_PREPARATION_OR_CAPABILITY_REQUEST
```

### Base revision contract

```text
LATEST_BASE_DISCOVERY_REQUIRED
PIN_IS_EVIDENCE_NOT_FRESHNESS_BYPASS
PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED
BASE_DRIFT_CLASSIFICATION_REQUIRED
BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK
NO_PERMANENT_STALE_PIN
NO_FLOATING_EXECUTION
BOUNDARY_FRESH_READ_REQUIRED
```

- `base_observed_head_sha`는 이 구현 인계 경계에서 다시 확인한 최신 completed Base `main`이다.
- `base_adopted_contract_sha`는 프로젝트가 현재 채택한 Base 계약이며 최신 Base가 더 새롭다는 이유만으로 자동 교체하지 않는다.
- `base_execution_sha`는 drift 분류 뒤 이번 bounded 구현 Slice에 적용할 revision이다. 구현 중 이동하는 Base `main`을 매 단계 추종하지 않는다.
- 구현 인계, pre-merge, post-merge, closeout에서 최신 Base와 프로젝트 상태를 다시 읽고 `base_drift_classification`을 갱신한다.
- 관련 Base 변경이면 reconcile·migration·affected test/consumer 재검증 뒤 execution pin을 바꾼다. 무관한 변경이면 기존 pin을 유지하고 영향 없음 근거를 남긴다.
- `implementation_authority_revision`은 사용자 승인된 `BLUEPRINT_PASS_2_FINAL exact revision`과 동일한 package scope를 가리켜야 한다. 1차 구조 Blueprint, candidate 이미지, 내부 review 또는 자동 test만으로 구현 authority를 만들지 않는다.

### 사용 조건

인계 사유가 실제로 성립하고 다음과 같은 승인 작업이 남았을 때 사용한다. 이 목록은 Work의 수행 금지 목록이 아니다.

- GDScript / product code
- Godot Scene / Resource / Autoload
- runtime game-data wiring
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- Godot build/export
- Godot implementation/runtime/headless/play tests

### 인계를 만들지 않는 조건

- 현재 Work가 승인된 작업을 수행할 capability와 권한을 갖고 있으며 별도 격리 이점이 없다.
- 단지 파일이 code/JSON/Python이거나 제품 구현 단계라는 이유만 있다.
- 기획·문서·이미지·Base 운영 작업이라는 이름만으로 실행자를 금지하거나 필수 지정하려 한다.
- runtime 하나가 없다는 이유로 독립 구현·정적 검사 전체를 전환하려 한다. 누락된 검증은 `NOT_RUN`으로 남기고 필요한 부분만 인계한다.

## 1. 현재 Work가 전달하는 것

### Slice / Player Outcome

```yaml
work_slice_id:
player_outcome:
player_action_and_choice:
expected_feedback_or_reward:
```

현재 지시문은 `PLAY_MEANINGFUL_WORK_SLICE` 하나를 구현·검증하기 위한 계약이다. 프로젝트 전체 장기 기획이나 아직 소비되지 않을 미래 범위를 끌어오지 않는다.

### Blueprint authority

```yaml
blueprint_authority:
  pass_1_structural_revision:
  pass_2_final_revision:
  final_approval_decision_id:
  implementation_authority_revision:
```

- pass 1은 Flow·Screen Inventory·대표 wireframe·state/data/system flow·actual/planned consumer를 정한 구조 초안이다.
- pass 2는 필요한 image/material/VFX-source candidate 검수 결과를 통합한 최종 Blueprint다.
- Codex는 `BLUEPRINT_PASS_2_FINAL exact revision`과 동일 scope의 사용자 최종 승인만 구현 authority로 사용한다.
- 두 pass는 기존 사용자용 PDF와 AI Production Spec의 revision이며 별도 세 번째 Blueprint 정본이 아니다.

### 승인된 구현 범위

```yaml
approved_scope: []
explicit_non_scope: []
changeable_godot_areas: []
```

### 보호 범위

- 바꾸면 안 되는 프로젝트 코어:
- 유지해야 할 플레이 동작:
- 저장/Schema/API compatibility:
- 다른 진행 중 workstream:

### 구현 입력 의미

```yaml
required_data_and_inputs: []
ui_ux_flow: []
asset_audio_dependencies: []
vfx_implementation_contract: []
```

- `required_data_and_inputs`: 구현에 필요한 데이터·상태·입력/출력의 **의미**를 적는다. Node/함수 설계를 강제하지 않는다.
- `ui_ux_flow`: 플레이어가 보고 조작하는 흐름과 필요한 정보·피드백을 적는다.
- `asset_audio_dependencies`: 실제 게임 소비처가 있는 승인 이미지·UI·VFX-source·사운드 요구를 적는다.
- `vfx_implementation_contract`: 최종 Blueprint의 VFX 목적·trigger·timing·layer·storyboard·source texture/mask·reduced-motion·budget·fallback을 받아 Particle/Shader/AnimationPlayer/Tween/Signal wiring·중단·재진입·성능과 runtime tuning으로 구현한다.

### Acceptance Criteria

1.
2.
3.

### 검증 요구

연속 실행 인계에 적용할 때는 `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`의 `## 8A. 승인 Slice 연속 실행 인계`를 읽는다. Blueprint 승인만으로 연속 실행을 활성화하지 않고, 기존 실행 계약의 continuation intent와 승인 범위를 먼저 확인한다.

- `repository_sources`: 실제 working directory, project.godot, engine/version, 실행 명령·기존 script 및 환경의 경로를 연결한다.
- 아래 `runtime/play checks`와 `review_evidence_expected`: reference의 `required_runtime_or_play_checks`에 대응한다. scenario/seed, 입력·상태·캡처와 판정 기준을 실제 consumer에 연결한다.
- 기존 실행 계약·작업 기록: checkpoint, 실행 상한·quota·중단 조건과 외부 side effect readback 경로를 연결한다. 별도 Schema나 중복 상태 장부를 만들지 않는다.

```yaml
review_evidence_expected: []
```

- Godot/headless tests:
- runtime/play checks:
- regression checks:
- platform/device checks if applicable:
- GPT final review에서 확인해야 할 player-facing evidence:

### Visual 입력

```yaml
approved_visual_records:
  - asset_id:
    consumer:
    repository_path:
    sha256:
    approval_status: APPROVED
    implementation_status: READY
    provenance:
```

- allowed intended use:
- rights/provenance constraints:

runtime에는 `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`를 충족한 Visual만 소비한다. 필요한 이미지 후보의 생성·생성형 편집은 실제 이미지 도구와 현재 승인 범위에 따라 수행하며, candidate 제작과 runtime 자산 승격을 구분한다.

## 2. Codex가 다시 읽을 프로젝트 정본

```yaml
repository_sources:
  repository:
  base_branch:
  exact_source_sha:
  base_observed_head_sha:
  base_adopted_contract_sha:
  base_execution_sha:
  project_agents:
  start_here:
  active_context:
  confirmed_decisions: []
  ai_production_spec:
  human_blueprint_pdf:
  blueprint_pass_2_final_revision:
  user_final_approval_decision_id:
  current_codex_handoff:
  asset_manifest:
  godot_product_paths: []
  runtime_tests_and_evidence: []
  current_open_prs: true
```

기존 Notion에만 고유 자료가 남아 있으면 승인된 migration scope에서 repository로 옮긴다. 이 구현 지시문은 Notion page/database/attachment 조회를 필수 재수화 경로로 만들지 않는다.

```yaml
optional_legacy_migration_context:
  status: NOT_APPLICABLE | ALREADY_MIGRATED | GPT_MIGRATION_BLOCKED
  repository_receipt:
```

재수화는 current Slice와 직접 의존하는 구현 사실을 정확히 확인하기 위한 것이다. GPT 지시문에 없는 프로젝트 전체를 임의로 재기획하는 단계가 아니다.

## 3. Codex 시작 순서

```text
조건부 Work Instruction과 실제 인계 사유 확인
→ work_slice_id / approved_scope / explicit_non_scope 확인
→ project/repository identity + exact_source_sha 확인
→ latest completed Base main fresh-read
→ adopted Base contract + latest Base drift classification
→ base_execution_sha bounded pin 확인
→ BLUEPRINT_PASS_2_FINAL exact revision + user approval 확인
→ latest user decision 확인
→ repository current project canon 재수화
→ Decision / AI production spec / current handoff 대조
→ approved Visual repository path / SHA-256 / manifest readback
→ 실제 project.godot / code / Scene / Resource / runtime data / test 상태 조사
→ open PR/worktree/branch overlap 확인
→ Work Instruction과 current truth 대조
→ 승인 범위 안에서 구현 방향·기술 방법 결정
→ APPROVED IMPLEMENTATION WITH SELECTED ENGINE ADAPTER
→ TEST / RUNTIME / PLAY EVIDENCE
→ READY_FOR_GPT_REVIEW
```

지시문과 current truth가 충돌하면 억지 구현하지 않고 drift를 분류한다. 관련 최신 Base 변경이 있으면 stale pin을 영구 고집하거나 floating latest로 즉시 전환하지 않고, 영향을 분류해 현재 package의 안전한 reconcile·revalidation 경계를 결정한다.

runtime capability가 없으면 해당 검증은 `NOT_RUN`으로 반환하고 독립적으로 가능한 승인 구현·정적 검사를 계속한다. 필수 검증 증거가 없는 전체 완료 주장은 하지 않는다. repository write 권한이나 사용자 승인이 없다면 영향을 받는 변경은 실행하지 않는다.

## 4. Codex가 자율 결정할 수 있는 기술 구현

승인된 플레이어 결과·기획 의미·데이터 계약을 바꾸지 않는 범위에서:

- Node / Scene / Resource 구조
- GDScript 함수·클래스·Signal·Autoload 구성
- 구현 순서
- 테스트 작성 방식
- runtime data 연결 방법
- 오류 처리와 edge case
- 성능·안정성 리팩터링
- repository convention에 맞는 명명/파일 구조

GPT가 예상 구현 경로를 적었더라도 더 안전하고 단순한 Godot 구현이 있으면 Codex가 승인 결과를 보존한 채 선택할 수 있다.

## 5. Codex가 바꾸면 안 되는 것

- 프로젝트 코어 / player promise
- Core Loop / 주요 플레이 규칙
- 주요 UX 의미
- 경제·성장·난이도 방향
- 서사 정사·캐릭터 의미
- 승인 기능 제거/범위 확대
- `explicit_non_scope`를 승인 없이 구현 범위에 추가
- Visual direction / Art Bible
- 저장 호환성을 깨는 제품 결정
- 추가 유료 서비스/권한 확대
- 프로젝트가 채택한 Base 계약을 최신이라는 이유만으로 자동 교체
- 사용자 승인된 `BLUEPRINT_PASS_2_FINAL`의 의미·scope 변경

필요하면 `CHANGE_PROPOSAL`로 현재 작업 owner와 사용자 결정 경계에 반환한다.

## 6. 이미지 규칙

```text
IMAGE_TOOL_REQUIRED_FOR_GENERATION_AND_EDITING
GENERATED_CANDIDATE_IS_NOT_APPROVED_ASSET
RUNTIME_VISUAL_INPUT_REPOSITORY_MANIFEST_ONLY
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY_RETIRED
```

이미지가 부족하면 consumer·brief·승인 범위와 실제 이미지 도구를 확인한다. 아래 `GPT_VISUAL_REQUEST`는 기존 요청 Schema의 호환 이름이며 GPT로의 필수 전환을 뜻하지 않는다.

```yaml
GPT_VISUAL_REQUEST:
  implementation_task:
  why_required:
  player_or_ui_role:
  asset_type:
  target_screen_or_scene:
  required_dimensions_or_ratio:
  visual_constraints:
  existing_approved_references: []
  repository_destination:
  manifest_destination:
  acceptance_criteria: []
```

실제 이미지 도구로 candidate 제작·검수 → 사용자 자산 승인 → repository binary 저장 → SHA-256·consumer·provenance·상태 manifest readback → current executor exact SHA fresh-read 후 연결한다. 도구나 승인이 없으면 해당 의존 작업만 보류하고 독립 작업은 계속한다.

Library·PDF·Notion preview에 보인다는 사실만으로 구현 입력이 되지 않는다.

## 7. Git / Concurrent Work

- current main과 target branch/head를 시작 시 재확인한다.
- `exact_source_sha`가 stale이면 구현을 계속하지 않고 reconcile한다.
- `base_execution_sha`는 bounded Slice 동안 고정하고, 관련 최신 Base change는 `BASE_DRIFT_CLASSIFICATION_REQUIRED` 뒤에만 채택한다.
- 구현 인계·pre-merge·post-merge·closeout에서 `BOUNDARY_FRESH_READ_REQUIRED`를 수행한다.
- 다른 open/draft/ready PR은 명시적 authorization 없이는 read-only.
- force push / destructive reset / unrelated work absorption 금지.
- 사용자 기존 변경을 보존한다.
- current main이 움직이면 안전하게 reconcile하고 affected regression 재실행.

## 8. 결과 반환

```yaml
codex_result:
  project:
  repository:
  work_slice_id:
  baseline_main:
  baseline_exact_source_sha:
  base_observed_head_sha:
  base_adopted_contract_sha:
  base_execution_sha:
  base_drift_classification:
  blueprint_pass_2_final_revision:
  user_final_approval_decision_id:
  implementation_authority_revision:
  final_head:
  implementation_direction_chosen:
  changed_godot_files_and_reasons: []
  protected_behavior_preserved: []
  explicit_non_scope_preserved: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_repository_visuals_consumed: []
  visual_requests_waiting: []
  technical_improvements: []
  change_proposals: []
  remaining_risks: []
  rollback:
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

Codex는 구현 결과와 evidence를 반환하며 `FIX | TUNE | REDESIGN`의 제품 판정은 current review owner가 실제 정본·diff·검증에 대조해 수행한다. 기존 `READY_FOR_GPT_REVIEW` 결과명은 검토 필요 상태의 호환 표현이며 필수 앱 전환이 아니다.

## 9. 전체 흐름

```text
현재 승인된 Work
latest Base + project current authority fresh-read
→ adopted Base drift comparison + execution SHA pin
→ 현재 PLAY_MEANINGFUL_WORK_SLICE repository 정본 복원
→ 전체 system coverage + 다음 Slice 최소 구현 준비 기획
→ Existing Solution First / 필요한 벤치마킹
→ 1차 구조 Blueprint: Flow / Screen / state / consumer
→ 필요한 image/material/VFX-source preparation
→ 2차 최종 Blueprint + 적대적 검수·IRG
→ approved scope / explicit non-scope / Acceptance 확정
→ repository Decision / AI production spec / asset manifest 준비
→ source-SHA-bound 사람용 상세 PDF 점검
→ exact final Blueprint 사용자 승인
→ IMPLEMENTATION_READY
→ 현재 capability와 권한으로 상세 설계·구현 계속
→ 사용자 요청 / 실제 capability 부족 / 격리 필요 시에만 handoff boundary fresh-read
→ 필요한 경우에만 이 조건부 Codex Work Instruction

현재 executor (인계가 있을 때 Codex)
latest Base drift + pinned base_execution_sha 대조
→ exact repository SHA + final Blueprint + project entrypoints + asset manifest 재수화
→ 승인 범위 안에서 Godot 구현 방향·기술 방법 결정
→ 구현·코딩·runtime/play test
→ READY_FOR_GPT_REVIEW

현재 review owner
구현 일치 → runtime → 실제 play/UX/Visual/Audio 최종 검수
→ FIX / TUNE / REDESIGN 분류
→ 필요한 영향 범위만 재검증
→ pre-merge boundary fresh-read
→ APPROVED면 merge gate
→ post-merge boundary fresh-read와 repository 정본 반영
→ 필요 시 merged source SHA로 사람용 상세 PDF 재생성
→ closeout boundary fresh-read와 남은 작업 재계산
```

> 현재 역할 한 줄: **승인되고 capability를 갖춘 Work가 기획부터 상세 설계·구현·검증·검토·허용된 통합까지 이어가며, 이 Template은 실제 인계가 필요할 때만 사용한다.** `PRE_HANDOFF_GPT_STOP`은 retired compatibility로 기획 준비 완료만 뜻하며 작업 중단이나 Codex 필수 전환이 아니다. Notion은 명시된 V4 exception 또는 고유 자료의 legacy migration source다.
