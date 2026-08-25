# Codex Godot Product Implementation Work Instruction

> 이 Template은 **GPT가 기획·검수·비코딩 작업을 끝낸 뒤, 실제 게임 프로젝트의 Godot 제품 구현이 남았을 때만 Codex에 전달하는 작업지시문**이다.
>
> Base/Notion/문서/기획/이미지/운영 정본 작업에는 사용하지 않는다. Codex는 일반 repository executor가 아니다.

## 0. Handoff Contract

```yaml
handoff_mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
project:
repository:
target_branch_or_pr:
work_instruction_status: GPT_REVIEWED_GODOT_IMPLEMENTATION_READY
implementation_owner: CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
final_review_owner: GPT_FINAL_IMPLEMENTATION_REVIEW
actual_state_verification_required: true
notion_rehydration_required: true
github_rehydration_required: true
codex_image_generation: FORBIDDEN
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
- Notion 편집
- GDD·기획서·밸런스표·Flow
- 이미지 작업
- 조사·벤치마킹·검수
- 문제→교훈→Base 승격
- GitHub 비제품 문서/정본 교정

## 1. GPT가 전달하는 것

### 목표 / Player Outcome
- 이번 Godot 구현으로 플레이어에게 무엇이 가능해져야 하는가?

### 승인된 구현 범위
- 구현할 기능/시스템:
- 변경 가능한 Godot 영역:
- 제외 범위:

### 보호 범위
- 바꾸면 안 되는 프로젝트 코어:
- 유지해야 할 플레이 동작:
- 저장/Schema/API compatibility:
- 다른 진행 중 workstream:

### Acceptance Criteria
1.
2.
3.

### 검증 요구
- Godot/headless tests:
- runtime/play checks:
- regression checks:
- platform/device checks if applicable:

### Visual 입력
- approved Notion visual records:
- allowed intended use:
- rights/provenance constraints:

Codex는 승인된 Visual만 소비하며 새 이미지를 생성·생성형 편집하지 않는다.

## 2. Codex가 다시 읽을 프로젝트 정본

### GitHub
```yaml
github_sources:
  repository:
  project_agents:
  start_here:
  active_context:
  confirmed_decisions: []
  godot_product_paths: []
  runtime_tests_and_evidence: []
  current_open_prs: true
```

### Notion
```yaml
notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []
```

## 3. Codex 시작 순서

```text
GPT-reviewed Godot Work Instruction 수신
→ project/repository identity 확인
→ latest user decision 확인
→ GitHub current project canon 재수화
→ Notion Project Home / relevant Domain / AI System / approved Visual 재수화
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
- Visual direction / Art Bible
- 저장 호환성을 깨는 제품 결정
- 추가 유료 서비스/권한 확대

필요하면 `CHANGE_PROPOSAL`로 GPT에 반환한다.

## 6. 이미지 규칙

```text
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_GENERATIVE_IMAGE_EDITING_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
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
  notion_destination:
  acceptance_criteria: []
```

GPT가 제작·검수 → Notion current-use 승인 + upload/attach/readback → Codex fresh-read 후 재개한다.

## 7. Git / Concurrent Work

- current main과 target branch/head를 시작 시 재확인한다.
- 다른 open/draft/ready PR은 명시적 authorization 없이는 read-only.
- force push / destructive reset / unrelated work absorption 금지.
- 사용자 기존 변경을 보존한다.
- current main이 움직이면 안전하게 reconcile하고 affected regression 재실행.

## 8. 결과 반환

```yaml
codex_result:
  project:
  repository:
  baseline_main:
  final_head:
  implementation_direction_chosen:
  changed_godot_files_and_reasons: []
  protected_behavior_preserved: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  technical_improvements: []
  change_proposals: []
  remaining_risks: []
  rollback:
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

## 9. 전체 흐름

```text
GPT
기획 → 조사/벤치마킹 → 적대적 검수
→ Base/Notion/문서/Visual 등 비코딩 작업 완료
→ 실제 Godot 제품 구현 필요 판정
→ 프로젝트별 Codex Godot Work Instruction

Codex
해당 프로젝트 GitHub + Notion current truth 재수화
→ Godot 구현 방향 결정
→ 구현·코딩·runtime/play test
→ READY_FOR_GPT_REVIEW

GPT
최종 검수
→ REVISE면 Codex 재작업
→ APPROVED면 merge gate
→ post-merge GitHub + Notion 상태 정리
```

> 현재 역할 한 줄: **GPT는 비코딩·Base·Notion·기획·검수·Visual을 담당하고, Codex는 실제 게임 프로젝트의 Godot 제품 구현·코딩을 담당한다.**
