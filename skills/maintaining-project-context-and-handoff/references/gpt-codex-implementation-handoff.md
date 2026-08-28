# GPT–Codex Godot 제품 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 **실제 게임 프로젝트 Godot 제품 구현 인계** 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
Workspace authority: `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`

## 1. 책임 분리

```text
GPT
= 현재 PLAY_MEANINGFUL_WORK_SLICE의 기획·조사·벤치마킹·적대적 검수·Base·repository canon·문서·표·이미지·Godot Work Instruction·최종 검수

Codex
= 승인된 Slice 범위의 실제 게임 프로젝트 Godot 제품 구현·코딩·runtime/play test

Project repository
= 기획·Decision·structured data·승인 runtime asset·code·Scene·Resource·test·evidence의 REPOSITORY_PRIMARY_CANON

Human Master GDD PDF
= exact source SHA를 가진 HUMAN_GDD_PDF_DERIVED_VIEW

Notion
= 고유 자료가 남은 기존 프로젝트에서만 GPT-owned LEGACY_READ_ONLY migration source
```

Codex는 일반 repository executor가 아니다. Base의 정책·Skill·Registry/generated·CI/test contract와 Notion legacy migration은 GPT가 담당한다.

## 2. 인계 조건

`CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF`는 다음이 실제로 남았을 때만 만든다.

- GDScript / product code
- Scene / Resource / Autoload
- runtime game-data wiring
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- Godot build/export
- Godot implementation/runtime/headless/play tests

repository 기획 정본, PDF, Notion migration, Base maintenance, GDD/표/Flow, 이미지, 조사/검수만 남았다면 인계하지 않는다.

인계 전 GPT는 current Slice에서 다음 Gate를 닫아야 한다.

```text
PLAY_MEANINGFUL_WORK_SLICE
→ TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT
→ GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING
→ EXISTING_SOLUTION_FIRST
→ 필요한 benchmark / adversarial review / IRG
→ PLANNING_CANON_BEFORE_HANDOFF
→ PRE_HANDOFF_GPT_STOP
```

`PLANNING_CANON_BEFORE_HANDOFF`는 승인된 기획 Decision과 구현 계약을 repository 정본에 기록하는 단계다. 구현·runtime·play PASS를 미리 주장하는 단계가 아니다.

## 3. GPT 인계 계약

```yaml
mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
project:
repository:
base_branch:
exact_source_sha:
work_slice_mode: PLAY_MEANINGFUL_WORK_SLICE
work_slice_id:
player_outcome:
player_action_and_choice:
approved_scope: []
explicit_non_scope: []
protected_scope: []
required_data_and_inputs: []
ui_ux_flow: []
asset_audio_dependencies: []
acceptance_criteria: []
review_evidence_expected: []
repository_sources:
  project_agents:
  start_here:
  active_context:
  confirmed_decisions: []
  ai_production_spec:
  current_codex_handoff:
  asset_manifest:
  godot_product_paths: []
  runtime_tests_and_evidence: []
optional_legacy_migration_context:
  status: NOT_APPLICABLE | ALREADY_MIGRATED | GPT_MIGRATION_BLOCKED
  repository_receipt:
required_runtime_or_play_checks: []
forbidden_changes: []
visual_policy:
  generation_by_codex: FORBIDDEN
  approved_repository_path_sha256_and_manifest_only: true
  missing_visual_action: GPT_VISUAL_REQUEST
change_proposal_boundary: []
```

이 명세는 구현 방법을 고정하지 않는다. Codex는 exact project repository와 실제 Godot 구조를 읽고 승인된 결과를 보존하는 기술 구현 방법을 결정한다.

`explicit_non_scope`는 이번 Slice에서 의도적으로 제외한 미래 기능·콘텐츠·시스템을 Codex가 구현 편의상 끌어오지 못하게 하는 범위 계약이다.

## 4. Codex 재수화 Gate

`CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA`

```text
exact game project/repository/base branch/source SHA/worktree
→ Project AGENTS / START_HERE / Active Context
→ current Decision / AI production spec / current handoff
→ latest main + task branch + open independent PR
→ approved Visual repository path / SHA-256 / consumer / ASSET_MANIFEST readback
→ project.godot
→ GDScript / Scene / Resource / runtime data / tests
→ Work Instruction과 current truth 대조
→ authoring/runtime readiness
→ GODOT PRODUCT BUILD
```

과거 대화·stale handoff·로컬 캐시·source SHA 없는 PDF만으로 구현하지 않는다. 재수화는 current Slice와 직접 의존하는 구현 truth를 확인하는 것이며, Codex가 프로젝트 전체를 재기획하는 단계가 아니다.

Notion page/database/attachment는 기본 Codex 입력이 아니다. 고유 자료가 남았다면 GPT가 이관하고 repository receipt를 전달한다.

## 5. Visual Gate

Codex 금지:

- 이미지 신규 생성
- 생성형 이미지 편집
- 임시 AI placeholder 생성
- 미승인 Visual 사용
- Library·PDF·Notion preview를 runtime binary로 직접 사용

허용:

- `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`를 충족한 Visual 소비
- 코드 기반 UI layout / shader / VFX / primitive drawing / animation wiring

별도 이미지가 필요하면:

```yaml
GPT_VISUAL_REQUEST:
  implementation_task:
  why_required:
  target_screen_or_scene:
  asset_type:
  visual_constraints:
  repository_destination:
  manifest_destination:
  acceptance_criteria: []
```

GPT가 제작·검수·사용자 승인 후 원본 binary를 repository에 저장하고 SHA-256·consumer·provenance·상태를 manifest에서 readback한 뒤 새 exact SHA로 Codex를 재개한다.

## 6. 기술 자율성과 `CHANGE_PROPOSAL`

Codex가 자율 결정 가능:

- Node/Scene/Resource 구조
- 함수/클래스/Signal/Autoload
- 구현 순서
- runtime data 연결
- test structure
- 오류 처리
- 성능·안정성 개선
- 동작 보존 리팩터링

GPT로 반환:

- Core Loop / 플레이 규칙
- 주요 UX 의미
- 경제·성장·밸런스 의미
- 서사 정사
- Art Direction
- MVP/기능 범위
- `explicit_non_scope`의 범위 확대
- 제품 호환성을 깨는 중요 결정

## 7. 실행환경 freshness

- exact project/repository/worktree 확인
- base branch / exact source SHA / branch/main/dirty/diverged 확인
- project.godot 확인
- stale PID/session/port/editor를 current truth로 사용하지 않음
- adopted authoring authority를 우회하지 않음
- force push/history rewrite/destructive reset 금지
- other open/draft/ready PR read-only

## 8. 패키지

큰 Godot 구현만 패키지로 나눈다.

좋은 경계:

- 플레이 가능한 독립 결과
- 독립 test/runtime evidence
- rollback 가능
- 같은 Scene/Resource 경쟁 수정 최소화

기본 병렬성은 `SEQUENTIAL`이다.

## 9. 선택적 Codex Godot technical preflight

고위험 Godot 구현에서만 별도 read-only 기술 preflight를 사용할 수 있다.

```yaml
mode: CODEX_GODOT_TECHNICAL_PREFLIGHT
scope: ACTUAL_GODOT_PRODUCT_IMPLEMENTATION_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

이 preflight는 제품 방향을 설계하는 별도 PLAN 단계가 아니다. GPT가 이미 확정한 player outcome·approved scope·protected scope를 바꾸지 않고 실제 Godot 구조·위험·rollback을 읽기 전용으로 확인한다.

preflight를 생략해도 exact repository SHA 재수화와 asset manifest readback은 생략하지 않는다.

## 10. 결과 반환

```yaml
codex_result:
  project:
  repository:
  work_slice_id:
  baseline_exact_source_sha:
  final_commit:
  changed_godot_files_and_reasons: []
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

GPT가 final review owner다. GPT는 구현 결과를 `FIX | TUNE | REDESIGN`으로 분류하고, 필요한 수정 뒤 current Slice와 실제 영향받은 직접 의존성만 재검증한다. 실제 구현·runtime/play PASS 상태는 검증 뒤에만 repository 정본으로 승격한다.

## 11. 잘못된 라우팅

- Base test/Registry/generated/CI를 Codex에 넘김
- repository 기획·PDF·Notion migration 작업을 Codex에 넘김
- 모든 code file을 Codex ownership으로 판단
- 실제 Godot product work를 GPT가 누적 구현
- Codex가 이미지 생성
- current Slice와 무관한 미래 기능을 implementation convenience로 함께 구현
- GPT가 구현 준비 완료 뒤 Node/Scene/함수 수준 구현법을 계속 강제
- Notion을 Codex 구현의 dual canon으로 복원

## Retired compatibility vocabulary

```text
project GitHub+Notion 재수화 = retired dual-canon route
notion_sources = retired handoff field
approved_notion_visuals_consumed = retired result field
```

> 인계 기준은 **코드 파일 존재 여부가 아니라 실제 Godot 제품 구현 필요 여부**다. 인계 범위는 프로젝트 전체가 아니라 승인된 `PLAY_MEANINGFUL_WORK_SLICE`와 그 직접 의존성이다.
