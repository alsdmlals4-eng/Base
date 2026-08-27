# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. Work Mode

| Work Mode | Owner | 핵심 목적 |
|---|---|---|
| `PLAN` | GPT | 의도·요구·근거·기획·Notion·Visual·Acceptance 확정 |
| `NONCODING_BUILD` | GPT | Base/Notion/문서/정본/표/이미지/운영 교정 |
| `GODOT_PRODUCT_BUILD` | Codex | 실제 게임 프로젝트의 Godot 제품 구현·코딩·runtime 연결 |
| `REVIEW` | GPT | 결과 적대적 검토·증거·회귀·기획 일치 판정 |

`BUILD`라는 단어만으로 Codex를 호출하지 않는다. 먼저 **비코딩/Base/Notion 작업인지, 실제 Godot 제품 구현인지** 분류한다.

```text
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
BASE_GOVERNANCE_BUILD_IS_GPT
NOTION_BUILD_IS_GPT
GODOT_PRODUCT_BUILD_IS_CODEX
```

## 2. 기본 라우팅

공용 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

```text
사용자 Prompt
→ current Project/Base/Notion/GitHub 정본 복원
→ GPT PLAN
→ 재사용 조사·벤치마킹·적대적 검토·IRG
→ 기획/Flow/UI/UX/데이터/Visual/Acceptance 확정
→ 비코딩 교정이 있으면 GPT NONCODING_BUILD
→ 실제 Godot 제품 구현 필요 여부 판정

Godot 제품 구현 없음
→ GPT REVIEW / readback / 종료

Godot 제품 구현 있음
→ GPT가 프로젝트별 Codex 작업지시문 작성
→ CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
→ Codex가 해당 프로젝트 GitHub + Notion 재수화
→ GODOT_PRODUCT_BUILD
→ test/runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ GPT REVIEW
```

## 2A. Owner classification literal

```text
BASE / NOTION / PLANNING / DOC / VISUAL → GPT
ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex
```

이 분류는 파일 확장자가 아니라 제품 책임을 기준으로 한다.

## 2B. Skill / Skill Mode 자동 선택

사용자는 Work Mode·Skill·Skill Mode를 매번 직접 고를 필요가 없다.

```text
사용자 Prompt
→ 의도·현재 단계·위험 파악
→ 주 Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 필요한 최소 Skill 자동 선택
→ 각 Skill의 Skill Mode 자동 선택
→ 실행·검증·필요 시 재라우팅
```

- `load_by_default=false`는 자동 선택 금지가 아니라 trigger가 없을 때 불필요하게 읽지 않는다는 뜻이다.
- 주 책임 Skill은 하나를 우선하고, Foundation·검증·handoff companion은 실제 필요할 때만 추가한다.
- Skill을 읽은 것과 실제 절차를 실행한 것을 구분한다.
- 새 사실·실패·범위·정본 변경이 생기면 자동 선택을 다시 수행한다.
- 파일이 코드 형식이라는 이유로 Base 작업을 Codex Skill로 라우팅하지 않는다.

## 2C. `CLAIM_AND_INTENT_VERIFICATION_GATE`

사용자의 말·기존 보고·handoff에 포함된 **완료 주장과 실제 요청 의도**를 현재 정본·GitHub/Notion 상태·증거로 대조한 뒤 실행한다.

Reference: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`

Continuous Work의 recovery/queue/승인범위 해석은 다음 reference와 함께 사용한다.

Reference: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

```text
CLAIM_AND_INTENT_VERIFICATION_GATE
→ user intent / approved scope 복원
→ completion / implementation claim 분리
→ current GitHub + Notion + evidence readback
→ 사실과 의도 일치 여부 판정
→ 실제 owner로 route
```

handoff summary나 과거 PASS를 current truth로 가정하지 않는다.

## 3. Codex Trigger

Codex는 다음에만 기본 진입한다.

```text
GDScript / product code
Godot Scene / Resource / Autoload
runtime game-data wiring
save/load product implementation
UI runtime wiring
shader/VFX/code-driven feedback
Godot build/export
Godot implementation/runtime/headless/play tests
```

다음은 **Codex Trigger가 아니다**.

```text
Base 정책·Skill·Guide·Template
Base Python contract test / CI policy / Registry / generated governance
Notion 생성·편집·표·Flow·AI Workspace
GDD·기획서·밸런스표·테크트리·병종표
벤치마킹·시장조사·검수
이미지 생성·편집·승인
문제→교훈→Base 승격
GitHub 비제품 문서/정본 교정
```

파일 확장자가 `.py`, `.json`, `.md`인지가 owner를 결정하지 않는다. **게임 제품 runtime을 구현하는가**가 Codex 진입 기준이다.

## 4. 경량 중립성 Gate와 적대적 검토

권장안·판정·설계 선택은 다음 순서로 본다.

```text
평가 기준
→ 대안
→ 반증
→ 이익·비용·위험
→ 되돌리기 난이도
→ 미검증
→ 권장 결론
```

- `동의 편향`을 막되 `반대를 위한 반대`를 요구하지 않는다.
- `L0`: 오탈자·명백한 기계 수정·동일 검사 재실행은 전체 적대 검토 생략 가능.
- **`결정·권장안이 없는 설명형 칭찬·균형 요약`**만 full adversarial exclusion 가능하다.
- **`L1 이상`** 중요한 기능·설계·아키텍처·정책·방향 결정과 중요 권장안은 PLAN 사전판정에서 `running-adversarial-review-and-refinement: attack → validate-critique → decision-report`를 적용한다.
- finding은 먼저 validate한다.
- 승인된 finding은 실제 owner의 BUILD에서 한 번만 구현·수정한다. 비코딩/Base/Notion finding은 GPT가 직접 교정하고, **실제 Godot 제품 finding만** Codex Build로 넘긴다.
- 호환 lifecycle 표현인 **`refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정**은 현재 owner 분류를 따른다. Base/Notion/noncoding은 GPT BUILD, 실제 Godot 제품 구현은 Codex Build다.
- 구현된 finding은 GPT가 다시 중복 구현하지 않고 REVIEW의 `regression-recheck → decision-report`로 이동한다.
- 사용자안과 AI 최초안을 동일 기준으로 평가하며 무조건 동의나 무조건 반대 요청보다 정본·증거를 우선한다.
- 최소 5회의 완전한 전체 개선 루프 후 clean exit까지 계속한다.

## 5. REVIEW finding 분류

```text
review-scope-map
→ attack
→ validate-critique
→ finding
   ├─ BASE_GOVERNANCE_CORRECTION → GPT
   ├─ NOTION_OR_DOCUMENT_CORRECTION → GPT
   ├─ PLANNING_OR_VISUAL_CORRECTION → GPT
   ├─ GODOT_PRODUCT_IMPLEMENTATION_CORRECTION → Codex
   ├─ USER_DECISION_REQUIRED
   ├─ BLOCKED_UNVERIFIED
   └─ NO_CHANGE
→ correction
→ regression-recheck
→ decision-report
→ whole-state re-attack
```

## 6. GPT 권한

GPT는 다음을 직접 수행한다.

- 조사·벤치마킹·기획·Acceptance
- Base/Project 정책·문서·Skill·Guide·Template
- Base Registry/generated/CI/test contract 유지보수
- Notion Home/Domain/AI System 생성·편집
- 사람용 데이터표·Flow·Storyboard
- 이미지 brief·생성·편집·검수·Notion 승인 전달
- 문제/교훈 정리·Base 승격
- GitHub 비제품 정본 교정
- Codex 구현지시문 작성
- Codex 결과 최종 검수

GPT는 실제 게임 프로젝트의 Godot 제품 코드를 기본 구현하지 않는다.

## 6A. Work 직접 Godot 기계검증과 작업 소유 프로세스 정리

GPT Work의 `REVIEW`가 runtime·scene·input·UI·resource 연결·오류 로그·GUT/headless/live-QA 증거를 직접 확인해야 하고 현재 도구로 실행할 수 있으면 Godot을 기계검증에 사용한다. 문서·정적 diff·data schema 검사만으로 Acceptance를 충족할 수 있으면 불필요하게 실행하지 않는다.

```text
REVIEW
→ exact repository/worktree/project identity 확인
→ pre-existing Godot/game/debug/server 상태 기록
→ materially-needed Godot verification 실행
→ evidence와 readback 확보
→ 같은 작업의 추가 검증 필요 여부 판정
→ task-owned process만 정상 종료
→ child process·project lock·session 잔여 확인
→ 검증과 정리를 분리해 보고
```

- 이번 Work가 시작한 Editor, game window, headless/runtime, debug/test runner, HiGodot/MCP/live-QA server만 `task-owned`로 본다.
- 사용자가 작업 전에 열어 둔 instance, 다른 프로젝트·repository·worktree, 다른 승인 workstream의 process는 종료하지 않는다.
- process 소유권을 안전하게 구분할 수 없으면 broad kill을 하지 않고 `PROCESS_OWNERSHIP_UNVERIFIED`와 잔여 위험을 보고한다.
- 같은 bounded verification group에서 재실행이 예정돼 있으면 매 assertion마다 Editor를 닫지 않아도 된다. 필요한 증거를 모두 확보했고 해당 도구가 더 이상 필요하지 않은 시점에 정리한다.
- 이 경로는 검수·기계검증 권한이며 GPT의 persistent Godot 제품 구현 권한을 확장하지 않는다.

공용 세부 계약은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`와 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다.

## 7. Codex 권한

Codex는 실제 게임 프로젝트에서만 다음을 수행한다.

- GDScript/product code
- Scene/Resource/Autoload/runtime config
- runtime game data 연결
- save/load/migration 구현
- UI runtime wiring
- shader/VFX/code-driven feedback
- build/export
- Godot 구현 test/runtime/play evidence
- 승인 범위 내 기술 리팩터링·오류 수정

Codex는 Base repository의 일반 maintenance executor가 아니다.

## 8. Codex 구현지시문

Base Template:

`templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

GPT는 다음을 전달한다.

```yaml
project:
repository:
player_outcome:
approved_scope: []
protected_scope: []
acceptance_criteria: []
github_sources: []
notion_sources: []
approved_visual_records: []
required_runtime_or_play_checks: []
forbidden_changes: []
change_proposal_boundary: []
```

지시문은 구현 방법을 고정하지 않는다. Codex는 프로젝트 GitHub+Notion과 실제 Godot 구조를 읽고 승인된 결과를 보존하는 기술 구현 방법을 결정한다.

## 9. `CHANGE_PROPOSAL`

Codex가 다음을 바꿔야 구현 가능하면 GPT로 반환한다.

- Core Loop / 플레이 규칙
- 주요 UX 의미
- 경제·성장·밸런스 의미
- 서사·세계관·정사
- Art Direction
- 기능 범위/MVP
- 제품 호환성에 영향을 주는 중요 결정

## 10. Visual 반환 경로

```text
Codex 구현 중 새 이미지 필요
→ WAITING_GPT_VISUAL
→ GPT_VISUAL_REQUEST
→ GPT brief·제작·검수
→ Notion current-use Approved + upload/attach/readback
→ Codex fresh-read
→ Godot Product Build 재개
```

Codex는 이미지 생성·생성형 편집·임의 AI placeholder를 만들지 않는다.

## 11. `[연속작업] 진행해`

`CONTINUOUS_WORK_ACTIVE`는 같은 승인 범위를 중간 승인 없이 이어가는 실행 flag다.

```text
ready PLAN/NONCODING task → GPT
ready GODOT_PRODUCT_BUILD → Codex handoff
Codex result → GPT REVIEW
recoverable evidence failure → 재조회/재실행
Codex 경로가 현재 없으면 Godot task만 DEFERRED_EXTERNAL_EXECUTOR
독립 GPT 비코딩 task 계속
```

**`기술적 단일 최소 안전 finding이면 자동 승인`**은 새 제품 결정을 자동 승인한다는 뜻이 아니다. 정본·테스트·표준으로 하나의 최소 안전 교정이 결정되고 기존 승인 범위 안에 있을 때만 적용한다.

- 해당 finding이 **비코딩/Base/Notion**이면 GPT가 같은 승인 범위에서 직접 교정한다.
- 해당 finding이 **실제 Godot 제품 구현**이면 Codex가 구현하고 GPT가 `regression-recheck → decision-report`로 검수한다.
- 진짜 사용자 결정·범위 확대·고위험 외부 행위만 새 승인 대상으로 올린다.

## 12. 동시작업·Git 안전

- 다른 open/draft/ready PR은 기본 read-only.
- current task의 명시된 PR만 수정.
- force push/history rewrite/destructive reset 금지.
- current main/remote HEAD를 fresh-read.
- 병합 전 exact HEAD·required checks·unresolved thread·ruleset 확인.
- 병합 뒤 main readback.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 명시 승인된 동일 범위는 새 차단 finding이 없으면 별도 병합 승인 없이 현재 repository gate를 통과해 병합할 수 있다.

## 13. 완료 보고

GPT 비코딩 작업:

```yaml
result:
  changed_base_or_notion_items: []
  validation: []
  remaining_godot_implementation: []
  godot_verification:
    status: PASS | FAIL | PARTIAL | NOT_RUN
    project_identity:
    scenes_or_behaviors_checked: []
    evidence: []
    unverified: []
  godot_process_cleanup:
    status: PASS | PARTIAL | NOT_RUN | NOT_APPLICABLE
    task_owned_processes_started: []
    task_owned_processes_stopped: []
    preexisting_or_unrelated_preserved: []
    residual_check: PASS | PARTIAL | NOT_RUN | NOT_APPLICABLE
    residual_risk: []
```

Godot을 시작하지 않은 작업은 `godot_verification.status: NOT_RUN`, `godot_process_cleanup.status: NOT_APPLICABLE`로 기록할 수 있다. 실행했지만 종료 또는 잔여 확인 증거가 없으면 cleanup을 PASS로 올리지 않는다.

Codex Godot 구현:

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
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

## 14. 실패 조건

다음은 잘못된 라우팅이다.

- Base test/Registry/generated/CI를 “코드니까 Codex”로 넘김
- Notion 작업을 Codex에 넘김
- 기획·검수·이미지 작업을 Codex에 넘김
- 모든 GitHub file mutation을 Codex Build로 분류
- 실제 Godot 제품 구현을 GPT가 누적 구현
- Codex가 이미지 생성
- Work가 시작하지 않았거나 소유권을 확인하지 못한 Godot·게임·debug/server process를 종료
- Godot 직접 검증 뒤 cleanup 증거 없이 완료를 과장

현재 역할은 다음 한 줄로 요약한다.

> **GPT = 기획·검수·Base·Notion·문서·데이터표·이미지·작업지시문, Codex = 실제 게임 프로젝트의 Godot 구현·코딩·런타임 테스트.**