---
name: maintaining-project-context-and-handoff
description: Use when project state must be resumed, current canon compressed for a new worker, or approved planning is ready for actual Godot product implementation.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context와 Handoff는 현재 상태·읽기 순서·미완료 작업·위험·다음 책임자를 연결하는 압축 라우터다.

현재 역할 경계:

```text
GPT_NONCODING_PROJECT_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

Base/Notion/문서/기획/이미지 작업을 Codex에 넘기지 않는다. Codex handoff는 **실제 게임 프로젝트의 Godot 제품 구현이 남았을 때만** 사용한다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
Godot work-instruction template: `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`
Packaged Godot handoff reference: [gpt-codex-implementation-handoff.md](references/gpt-codex-implementation-handoff.md)
Packaged fresh-read bootstrap reference: [fresh-read-project-bootstrap.md](references/fresh-read-project-bootstrap.md)

현재 Godot 구현 인계는 canonical policy와 packaged handoff reference의 bounded Slice 계약을 얇게 소비한다.

```text
PLAY_MEANINGFUL_WORK_SLICE
→ PLANNING_CANON_BEFORE_HANDOFF
→ PRE_HANDOFF_GPT_STOP
→ ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex
```

위 reference의 이름은 호환성을 위해 유지하지만 current 의미는 **GPT 비코딩 작업 완료 → Codex 실제 Godot 제품 구현 → GPT 최종 검수**에 한정한다. 새 채팅/담당자의 재개는 `fresh-read-project-bootstrap.md`의 `FRESH_READ_PROJECT_BOOTSTRAP`을 사용해 현재 Project GitHub + Notion에서 다시 재구성한다.

## Skill Modes

- `context-refresh`: current state와 다음 작업을 Active Context에 압축한다.
- `session-handoff`: 새 채팅/담당자/브랜치 경계의 재개 스냅샷을 만든다.
- `codex-godot-implementation-handoff`: GPT 기획·검수·비코딩 작업 후 실제 Godot 제품 구현만 Codex로 넘긴다.
- `implementation-package-handoff`: 큰 Godot 구현을 패키지로 나눠 GPT 설계 → Codex 제품 구현 → GPT 검수 흐름으로 관리한다.
- `resume`: `FRESH_READ_PROJECT_BOOTSTRAP`으로 Project GitHub·Notion·branch·commit·Godot runtime/session identity를 fresh-read하고, 과거 대화를 필수 입력으로 요구하지 않은 채 현재 품질·보호 범위·다음 안전 작업·evidence ceiling을 재구성한다.
- `post-merge-reconcile`: merge 뒤 LIVE_CONTINUATION_STATE를 새 main과 재조정한다.

## Use when

- 세션/채팅/담당자 경계에서 현재 상태를 넘겨야 한다.
- Active Context가 current GitHub/Notion과 drift했다.
- 실제 게임 프로젝트에서 GDScript/Scene/Resource/runtime wiring/build/test 구현이 남았다.
- 큰 Godot 구현을 패키지로 나눠야 한다.
- Codex 결과를 GPT가 검수한 뒤 수정/다음 패키지/merge를 결정해야 한다.

## Do not use when

- Base 정책·Skill·Guide·Template·Registry/generated·CI/test contract 교정
- Notion 편집
- GDD·밸런스표·Flow·문서 교정
- 이미지 생성·편집
- 조사·벤치마킹·적대적 검수
- GitHub 비제품 정본 교정
- 문제→교훈→Base 승격

위 작업은 GPT가 직접 끝낸다.

## Required inputs

```yaml
project_agents:
project_start_here:
active_context:
current_stage_and_gate:
validation_results:
remaining_risks:
next_work:

codex_godot_handoff:
  mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
  implementation_ready: true
  work_slice_id:
  player_outcome:
  player_action_and_choice:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  required_data_and_inputs: []
  ui_ux_flow: []
  asset_audio_dependencies: []
  notion_sources:
    project_home:
    relevant_domain_pages: []
    ai_system_detail_pages: []
    approved_visual_records: []
  github_sources:
    repository:
    godot_product_paths: []
    runtime_tests_and_evidence: []
  acceptance_criteria: []
  review_evidence_expected: []
  required_runtime_or_play_checks: []
  forbidden_changes: []
  visual_policy:
    generation_by_codex: FORBIDDEN
    approved_notion_visuals_only: true
    missing_visual_action: GPT_VISUAL_REQUEST
```

## Read first

1. Project `AGENTS.md`
2. `START_HERE.md` / Active Context
3. 관련 Notion Project Home/Domain/AI System
4. 승인 Visual record와 attach/readback
5. 실제 Godot code/Scene/Resource/runtime data/test
6. current main/branch/open workstream
7. `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## Process

### 1. Owner 분류

먼저 작업을 분류한다.

```text
BASE / NOTION / PLANNING / DOC / VISUAL → GPT
ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex
```

파일 형식만으로 Codex를 선택하지 않는다.

### 2. `context-refresh`

- 현재 프로젝트 방향
- 이번 작업에서 바뀐 것
- 구현/검증 상태
- 위험·미확정
- 다음 작업과 선행 조건
- 보호 경로
- 먼저 읽을 정본

만 남긴다.

### 3. `session-handoff`

```text
현재 상태
→ 이번 작업 결과
→ 남은 작업
→ 위험·미검증
→ 다음 작업자의 첫 행동
→ GitHub/Notion 정본
→ 검증·rollback
```

### 4. `codex-godot-implementation-handoff`

실제 Godot 제품 구현이 남았을 때만 `docs/GPT_CODEX_WORKFLOW_POLICY.md`와 `gpt-codex-implementation-handoff.md`를 소비해 다음 경계를 확인한다.

```text
PLAY_MEANINGFUL_WORK_SLICE
→ player outcome / player action and choice
→ approved scope / explicit_non_scope / protected scope
→ required data / UI·UX Flow / asset·audio dependencies
→ Acceptance Criteria / review evidence
→ PLANNING_CANON_BEFORE_HANDOFF
→ PRE_HANDOFF_GPT_STOP
→ GitHub project canon
→ Notion 기획/Flow/Visual
→ 승인 Visual
→ 실제 Godot 구현 대상
→ runtime/play test
→ CHANGE_PROPOSAL boundary
→ GPT_VISUAL_REQUEST boundary
```

`PRE_HANDOFF_GPT_STOP` 이후 GPT는 Node/Scene/함수 수준의 구현 방법을 더 고정하지 않는다. Codex는 handoff를 그대로 기계 구현하지 않고 project GitHub+Notion을 fresh-read해 실제 기술 방향을 결정한다.

### 5. Visual Gate

Codex는 이미지 생성·생성형 편집을 하지 않는다. current-use 승인 + Notion upload/attach/readback된 Visual만 사용한다.

이미지가 없으면 `GPT_VISUAL_REQUEST`로 반환한다.

### 6. `CHANGE_PROPOSAL`

Core Loop·주요 UX·경제/밸런스 의미·서사 정사·Art Direction·MVP 범위 변경이 필요하면 Codex가 임의 변경하지 않고 GPT로 반환한다.

### 7. Godot 실행 freshness

- exact project/repository/worktree
- project.godot
- branch/main/dirty/diverged
- adopted authoring authority
- editor/runtime/addon/test readiness
- stale PID/session/port 불신
- 다른 open PR read-only

을 확인한다.

### 8. 결과 반환

```yaml
codex_result:
  changed_godot_files_and_reasons: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  change_proposals: []
  remaining_risks: []
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

GPT가 final review owner다.

## Concurrent work

다른 open/draft/ready PR은 기본 read-only다. force push/history rewrite/destructive reset 금지. current main이 이동하면 fresh reconcile한다.

## Failure conditions

- Base maintenance를 Codex로 handoff
- Notion 작업을 Codex로 handoff
- 모든 코드 파일을 Codex owner로 간주
- Godot 제품 구현을 GPT가 누적 수행
- Codex가 이미지 생성
- stale handoff를 current truth로 사용

## Output contract

- current state / source-of-truth paths
- GPT-owned remaining noncoding work
- Codex-owned remaining Godot product work
- validation state
- risks / rollback
- next first action

> 현재 한 줄: **GPT는 비코딩·Base·Notion·기획·검수·Visual을 담당하고, Codex는 실제 게임 프로젝트의 Godot 제품 구현을 담당한다.**
