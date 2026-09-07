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

## 8A. 승인 Slice 연속 실행 인계

이 절은 **이미 승인된 `PLAY_MEANINGFUL_WORK_SLICE` 하나**에서 사용자 재전달을 줄이기 위한 기존 인계의 상세 절차다. 역할·승인 정본은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`, 연속 실행·복구 정본은 `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`를 그대로 사용한다. 새 Skill·Work Mode·게임 전체 원큐 제작 계약이 아니다.

### 승인과 기존 consumer

- 이 절의 연속 루프는 유효한 approval reference와 명시적 `CONTINUATION_INTENT_ALIASES`를 기존 실행 계약에 기록하여 `APPROVED_CONTRACT_CONTINUATION` / `CONTINUOUS_WORK_ACTIVE`가 확인된 경우에만 적용한다. Blueprint 승인만 있거나 계속 실행 의도가 없으면 `CONTINUOUS_WORK_INACTIVE`를 유지하고 일반 인계·검토 경계를 따른다. 사용자 중지·검토만 요청은 즉시 우선한다.
- 유효한 approval reference와 해당 범위의 사용자 승인 `BLUEPRINT_PASS_2_FINAL exact revision`을 확인한다. 같은 승인 범위의 기술적 교정에는 routine 재승인을 요구하지 않는다. 새 Goal·범위·비용·권한을 자동 승인하지 않는다.
- `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`의 기존 `approved_scope / explicit_non_scope / acceptance_criteria / repository_sources / asset_audio_dependencies / review_evidence_expected`에 아래 실행 정보를 연결한다. 이 reference의 `required_runtime_or_play_checks`는 Template의 검증 요구에 대응한다. 같은 정보를 새 정본에 복제하지 않고 기존 owner의 경로·ID를 참조하며, 새 필수 Schema나 별도 진행표를 만들지 않는다.
- 필요한 이미지·의미 변경은 각각 `GPT_VISUAL_REQUEST`와 `CHANGE_PROPOSAL`로 분리한다. 승인 자산을 임의 교체하지 않는다. 이에 의존하지 않는 승인 작업만 계속하며, 미승인 대체물로 완료 처리하지 않는다.

### 실행 가능한 인계 준비

| 기존 인계 위치 | 연결할 실제 정보 |
|---|---|
| `repository_sources` | exact revision, working directory, `project.godot`, 채택한 engine/version, 실제 명령 또는 기존 script 경로, 필요한 환경과 authoring authority |
| `acceptance_criteria / ui_ux_flow` | 승인된 시작 → 선택·행동 → 결과 → 다음 행동과 판정 기준. 실패·재시작·저장/불러오기는 해당 Slice에 적용되는 경우만 연결하고, 비적용 이유를 남긴다. |
| `review_evidence_expected / required_runtime_or_play_checks` | 재현 scene/fixture와 필요한 scenario/seed, 입력 → 상태 변화 → 화면·소리 → 결과, assert·로그·캡처 위치, 실제 consumer와 exact revision 연결 |
| 기존 실행 계약·작업 기록 | 현재 계약의 실행 상한·quota·중단 조건, checkpoint 위치, 되돌릴 범위와 보호할 사용자 변경·저장 데이터 |

없는 명령·도구·실행 결과를 만들어 적지 않는다. 저장소에서 복원 가능한 정보는 다시 묻지 않고 읽으며, 새 테스트 진입점이 필요하면 승인 범위의 구현 작업으로 구분한다. 아직 없는 진입점을 이미 검증된 경로처럼 쓰지 않는다. 실행 경로 미확인은 `BLOCKED_UNVERIFIED`로 표시하고 기존 recovery 절차를 적용한다. 새 화면·기능을 검증 명목으로 추가하지 않는다. 재현은 격리 fixture를 우선하여 사용자 저장 데이터를 보호한다.

### 구현·검증·교정 루프

```text
exact project/approval/asset/consumer 재수화
→ 기존 동작의 baseline smoke와 기존 실패 기록
→ 승인 흐름의 최소 end-to-end 구현
→ 자동 검사 + 실제 입력·상태·캡처 확인
→ 실패 재현 → 범위 안 교정 → 영향받는 회귀검사
→ acceptance와 미완료 범위 재대조
→ 요구된 evidence가 준비되면 READY_FOR_GPT_REVIEW
→ GPT 최종 검수 + 기존 사용자 결정·merge/readback Gate
```

- 완료를 위해 acceptance나 테스트의 기대 결과를 낮추지 않는다. 잘못된 테스트는 정본·반례 근거를 남겨 교정하되 승인된 제품 의미를 바꾸지 않는다. 기존 실패와 새 회귀를 구분하고, 기존 실패라고 해서 필수 acceptance를 면제하지 않는다.
- 반복 실패·개선 정체 또는 상한 도달 시 같은 방법을 무한 반복하지 않는다. 기존 계약의 `recover → local defer → independent ready work`로 분류하고, 반복 원인·대안·남은 필수 항목을 기록한다. 최신 사용자 지시·AGENTS가 명시한 전역 중단 조건은 우선한다. 상한 미확인은 무제한 실행 허가가 아니다. 안전한 실행 한도를 기존 owner에서 먼저 복원하며, 해결되지 않은 해당 실행은 보류한다.
- side effect 뒤에는 기존 작업 기록에 checkpoint를 남긴다. 중단 후 commit·PR·외부 쓰기를 무조건 재시도하지 않는다. current SHA·dirty state·PR ownership readback 뒤 완료된 단계는 보호하고 미완료 단계만 재개한다. 다른 open/draft/ready PR은 read-only이며, main 이동 시 현재 계약의 drift·영향 재검증 경계를 따른다.
- 외부 쓰기의 완료 여부는 Git 상태로 판정하지 않는다. 기존 task-recovery owner에 따라 해당 provider의 실제 목적지 상태, request/result identity 또는 idempotency key와 postcondition을 readback한 뒤 이미 적용된 효과를 분류한다. 확인할 수 없으면 `retry_safe: unknown`과 해당 쓰기 차단을 유지하며, 응답 누락만으로 미완료로 간주하지 않는다.
- 필수 검증이 실패했거나 `NOT_RUN`이면 전체 완료가 아니다. 증거가 부족한 항목과 의존 작업만 보류하고 독립 작업은 계속한다. headless 통과를 화면·조작 검증 PASS로 바꾸지 않는다. `codex_result`의 기존 tests/evidence/risks/status로 결과를 반환하며, `READY_FOR_GPT_REVIEW`는 사용자 승인이나 출시 PASS가 아니다.
- 이 절은 `GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED` 경로를 재활성화하거나 도입하지 않는다. 새 daemon·scheduler·유료 API도 추가하지 않는다. 실제로 제공된 승인 실행 환경 안에서만 동작하며, 채팅 종료 후 백그라운드 실행을 보장하지 않는다.

### 시범 적용·학습과 증거 상한

첫 실제 프로젝트 시범 적용에서는 기존 작업 기록에 첫 플레이 가능 결과까지의 시간, 사용자 재전달·재지시 횟수, 검수 결함·회귀·재작업을 관측 가능할 때만 남긴다. 정당한 핵심 결정 요청은 불필요한 재전달과 구분한다. 기록이 없으면 `NOT_MEASURED`이며 0이나 추정 절감률로 바꾸지 않는다. 비교는 같은 범위·엔진·자산·완료 기준에서 수행하고 측정 전 생산성 향상을 단정하지 않는다. 이 자료를 실제 consumer의 다음 인계 개선에 사용하되 프로젝트 고유 사실은 프로젝트에 남긴다.

문서 회귀검사는 agent 실행 강제·프로젝트 채택·Godot runtime의 증거가 아니다. 이 절을 읽거나 Template을 채웠다는 사실만으로 시범 적용 성공·사용자 개입 감소·완성 게임을 주장하지 않는다. 실제 프로젝트 적용은 해당 프로젝트의 최신 `AGENTS.md`와 채택한 Base 계약·drift 분류를 따르며 일괄 교체하지 않는다.

2026-09-07 원출처 비교: [OpenAI Codex app 사례](https://openai.com/index/introducing-the-codex-app/)의 단일 초기 사용자 프롬프트 이후 자율 작업과 실제 플레이 검증, [Anthropic 장기 실행 실험](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)의 작은 기능 단위·진행 기록·end-to-end 검사, [Godot 공식 CLI](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)의 실제 실행 경로를 `ADAPT`한다. 웹 실험의 성과 수치를 Godot에 전이하거나 새 provider·전체 게임 자율 확장·검증 생략을 채택하지 않는다. 공용 교훈은 **승인 입력뿐 아니라 실행·관측·교정 경로까지 기존 인계에 연결해야 한다**는 것이며, 효과 검증은 실제 프로젝트 시범 실행에 남는다.

이번 교정의 사전 비교·실행 상태는 `docs/operations/work-receipts/2026-09-07-approved-slice-continuous-handoff.json`에 기록한다. 최초 PR 작성 시점의 누락된 기록을 소급하여 PASS로 바꾸지 않으며, final exact-head 검사·독립 검토·병합 readback의 현황은 PR #856이 소유한다.

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
