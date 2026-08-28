# Codex Godot Product Implementation Work Instruction

> 이 Template은 **GPT가 기획·검수·비코딩 작업을 끝낸 뒤, 실제 게임 프로젝트의 Godot 제품 구현이 남았을 때만 Codex에 전달하는 작업지시문**이다.
>
> Base/Notion/문서/기획/이미지/운영 정본 작업에는 사용하지 않는다. 여기서 Notion은 legacy inventory·이관 작업까지 포함한다. Codex는 일반 repository executor가 아니다.

## 0. Handoff Contract

```yaml
handoff_mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
project:
repository:
base_branch:
target_branch_or_pr:
exact_source_sha:
work_slice_mode: PLAY_MEANINGFUL_WORK_SLICE
work_slice_id:
work_instruction_status: GPT_REVIEWED_GODOT_IMPLEMENTATION_READY
planning_stop_gate: PRE_HANDOFF_GPT_STOP
implementation_owner: CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
final_review_owner: GPT_FINAL_IMPLEMENTATION_REVIEW
actual_state_verification_required: true
repository_rehydration_required: true
github_rehydration_required: true
notion_rehydration_required: false
legacy_notion_migration_source_optional: true
codex_image_generation: FORBIDDEN
visual_input_contract: APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
missing_visual_action: GPT_VISUAL_REQUEST
```

### 사용 조건

이 Template은 다음 중 하나가 남았을 때 사용한다.

- GDScript / product code
- Godot Scene / Resource / Autoload
- runtime game-data wiring
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- Godot build/export
- Godot implementation/runtime/headless/play tests

### 사용하지 않는 조건

- Base 정책·Skill·Guide·Template·Registry/generated/CI/test contract
- repository Decision·AI production spec·GDD·기획서·밸런스표·Flow 교정
- 사람용 상세 기획서 PDF 생성·검수
- Notion 편집·legacy inventory·이관
- 이미지 생성·편집·승인 정리
- 조사·벤치마킹·검수
- 문제→교훈→Base 승격
- GitHub 비제품 문서/정본 교정

## 1. GPT가 전달하는 것

### Slice / Player Outcome

```yaml
work_slice_id:
player_outcome:
player_action_and_choice:
expected_feedback_or_reward:
```

현재 지시문은 `PLAY_MEANINGFUL_WORK_SLICE` 하나를 구현·검증하기 위한 계약이다. 프로젝트 전체 장기 기획이나 아직 소비되지 않을 미래 범위를 끌어오지 않는다.

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
```

- `required_data_and_inputs`: 구현에 필요한 데이터·상태·입력/출력의 **의미**를 적는다. Node/함수 설계를 강제하지 않는다.
- `ui_ux_flow`: 플레이어가 보고 조작하는 흐름과 필요한 정보·피드백을 적는다.
- `asset_audio_dependencies`: 실제 게임 소비처가 있는 승인 이미지·UI·VFX·사운드 요구를 적는다.

### Acceptance Criteria

1.
2.
3.

### 검증 요구

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

Codex는 `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`를 충족한 Visual만 소비하며 새 이미지를 생성·생성형 편집하지 않는다.

## 2. Codex가 다시 읽을 프로젝트 정본

```yaml
repository_sources:
  repository:
  base_branch:
  exact_source_sha:
  project_agents:
  start_here:
  active_context:
  confirmed_decisions: []
  ai_production_spec:
  current_codex_handoff:
  asset_manifest:
  godot_product_paths: []
  runtime_tests_and_evidence: []
  current_open_prs: true
```

기존 Notion에만 고유 자료가 남아 있으면 GPT가 별도 migration 작업에서 repository로 옮긴다. Codex 구현 지시문은 Notion page/database/attachment 조회를 필수 재수화 경로로 만들지 않는다.

```yaml
optional_legacy_migration_context:
  status: NOT_APPLICABLE | ALREADY_MIGRATED | GPT_MIGRATION_BLOCKED
  repository_receipt:
```

재수화는 current Slice와 직접 의존하는 구현 사실을 정확히 확인하기 위한 것이다. GPT 지시문에 없는 프로젝트 전체를 임의로 재기획하는 단계가 아니다.

## 3. Codex 시작 순서

```text
GPT-reviewed Godot Work Instruction 수신
→ work_slice_id / approved_scope / explicit_non_scope 확인
→ project/repository identity + exact_source_sha 확인
→ latest user decision 확인
→ repository current project canon 재수화
→ Decision / AI production spec / current handoff 대조
→ approved Visual repository path / SHA-256 / manifest readback
→ 실제 project.godot / code / Scene / Resource / runtime data / test 상태 조사
→ open PR/worktree/branch overlap 확인
→ Work Instruction과 current truth 대조
→ 승인 범위 안에서 구현 방향·기술 방법 결정
→ GODOT PRODUCT IMPLEMENTATION
→ TEST / RUNTIME / PLAY EVIDENCE
→ READY_FOR_GPT_REVIEW
```

지시문과 current truth가 충돌하면 억지 구현하지 않고 drift를 분류한다.

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

필요하면 `CHANGE_PROPOSAL`로 GPT에 반환한다.

## 6. 이미지 규칙

```text
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_GENERATIVE_IMAGE_EDITING_FORBIDDEN
CODEX_VISUAL_INPUT_REPOSITORY_MANIFEST_ONLY
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY_RETIRED
```

이미지가 부족하면:

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

GPT가 제작·검수·사용자 승인 → repository binary 저장 → SHA-256·consumer·provenance·상태 manifest readback → Codex exact SHA fresh-read 후 재개한다.

Library·PDF·Notion preview에 보인다는 사실만으로 구현 입력이 되지 않는다.

## 7. Git / Concurrent Work

- current main과 target branch/head를 시작 시 재확인한다.
- `exact_source_sha`가 stale이면 구현을 계속하지 않고 reconcile한다.
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

Codex는 구현 결과와 evidence를 반환하며 `FIX | TUNE | REDESIGN`의 최종 제품 판정은 GPT final review에서 수행한다.

## 9. 전체 흐름

```text
GPT
현재 PLAY_MEANINGFUL_WORK_SLICE repository 정본 복원
→ 최소 구현 준비 기획
→ Existing Solution First / 필요한 벤치마킹
→ 적대적 검수·IRG
→ approved scope / explicit non-scope / Acceptance 확정
→ repository Decision / AI production spec / asset manifest 등 비코딩 작업 완료
→ 필요 Gate에서 source-SHA-bound 사람용 상세 PDF 점검
→ PRE_HANDOFF_GPT_STOP
→ 실제 Godot 제품 구현 필요 판정
→ 프로젝트별 Codex Godot Work Instruction

Codex
exact repository SHA + project entrypoints + asset manifest 재수화
→ 승인 범위 안에서 Godot 구현 방향·기술 방법 결정
→ 구현·코딩·runtime/play test
→ READY_FOR_GPT_REVIEW

GPT
구현 일치 → runtime → 실제 play/UX/Visual/Audio 최종 검수
→ FIX / TUNE / REDESIGN 분류
→ 필요한 영향 범위만 재검증
→ APPROVED면 merge gate
→ 검증된 결과만 post-merge repository 정본에 반영
→ 필요 시 merged source SHA로 사람용 상세 PDF 재생성
```

> 현재 역할 한 줄: **GPT는 현재 플레이 의미 Slice의 비코딩·기획·검수·Base·repository canon·Visual을 담당하고, Codex는 승인된 Slice 범위의 실제 게임 프로젝트 Godot 제품 구현·코딩을 담당한다.** Notion은 고유 자료가 남은 기존 프로젝트의 GPT-owned legacy migration source일 뿐 Codex의 기본 구현 입력이 아니다.
