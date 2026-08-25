# GPT–Codex Godot 제품 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 **실제 게임 프로젝트 Godot 제품 구현 인계** 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 1. 책임 분리

```text
GPT
= 기획·조사·벤치마킹·적대적 검수·Base·Notion·문서·표·이미지·Godot Work Instruction·최종 검수

Codex
= 실제 게임 프로젝트의 Godot 제품 구현·코딩·runtime/play test

GitHub
= 프로젝트 structured/runtime truth

Notion
= 사람용 기획·Flow·시각 정본과 승인 Visual
```

Codex는 일반 repository executor가 아니다. Base의 정책·Skill·Registry/generated·CI/test contract는 GPT가 담당한다.

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

Notion 편집, Base maintenance, GDD/표/Flow, 이미지, 조사/검수만 남았다면 인계하지 않는다.

## 3. GPT 인계 계약

```yaml
mode: CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
project:
repository:
player_outcome:
approved_scope: []
protected_scope: []
acceptance_criteria: []
notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []
github_sources:
  project_agents:
  active_context:
  godot_product_paths: []
  runtime_tests_and_evidence: []
required_runtime_or_play_checks: []
forbidden_changes: []
visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST
change_proposal_boundary: []
```

이 명세는 구현 방법을 고정하지 않는다. Codex는 current project GitHub+Notion과 실제 Godot 구조를 읽고 승인된 결과를 보존하는 기술 구현 방법을 결정한다.

## 4. Codex 재수화 Gate

```text
exact game project/repository/worktree
→ Project AGENTS / START_HERE / Active Context
→ latest main + task branch + open independent PR
→ Notion Project Home / Domain / AI System
→ approved Visual + upload/attach/readback
→ project.godot
→ GDScript / Scene / Resource / runtime data / tests
→ Work Instruction과 current truth 대조
→ authoring/runtime readiness
→ GODOT PRODUCT BUILD
```

과거 대화·stale handoff·로컬 캐시만으로 구현하지 않는다.

## 5. Visual Gate

Codex 금지:

- 이미지 신규 생성
- 생성형 이미지 편집
- 임시 AI placeholder 생성
- 미승인 Visual 사용

허용:

- current-use 승인 + Notion upload/attach/readback된 Visual 소비
- 코드 기반 UI layout / shader / VFX / primitive drawing / animation wiring

별도 이미지가 필요하면:

```yaml
GPT_VISUAL_REQUEST:
  implementation_task:
  why_required:
  target_screen_or_scene:
  asset_type:
  visual_constraints:
  notion_destination:
  acceptance_criteria: []
```

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
- 제품 호환성을 깨는 중요 결정

## 7. 실행환경 freshness

- exact project/repository/worktree 확인
- project.godot 확인
- branch/main/dirty/diverged 확인
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

## 9. 선택적 Codex technical preflight

고위험 Godot 구현에서만 별도 read-only 기술 Plan을 사용할 수 있다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

Plan을 생략해도 project GitHub+Notion 재수화는 생략하지 않는다.

## 10. 결과 반환

```yaml
codex_result:
  project:
  repository:
  baseline_commit:
  final_commit:
  changed_godot_files_and_reasons: []
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

GPT가 final review owner다.

## 11. 잘못된 라우팅

- Base test/Registry/generated/CI를 Codex에 넘김
- Notion 작업을 Codex에 넘김
- 모든 code file을 Codex ownership으로 판단
- 실제 Godot product work를 GPT가 누적 구현
- Codex가 이미지 생성

> 인계 기준은 **코드 파일 존재 여부가 아니라 실제 Godot 제품 구현 필요 여부**다.
