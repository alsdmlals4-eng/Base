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
- `L1+`: 중요한 기능·설계·정책·방향 결정은 `running-adversarial-review-and-refinement` 적용.
- 결정·권장안 없는 설명형 칭찬/균형 요약만 full adversarial exclusion 가능.
- finding은 먼저 validate한다.
- 비코딩/Base/Notion finding은 GPT가 직접 교정한다.
- **실제 Godot 제품 finding만** Codex Build로 넘긴다.
- 구현된 finding은 GPT가 다시 중복 구현하지 않고 `regression-recheck → decision-report`로 검수한다.
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

- 기술적 단일 최소 안전 finding이 **비코딩/Base/Notion**이면 GPT가 같은 승인 범위에서 직접 교정한다.
- 기술적 단일 최소 안전 finding이 **실제 Godot 제품 구현**이면 Codex가 구현하고 GPT가 검수한다.
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
```

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

현재 역할은 다음 한 줄로 요약한다.

> **GPT = 기획·검수·Base·Notion·문서·데이터표·이미지·작업지시문, Codex = 실제 게임 프로젝트의 Godot 구현·코딩·런타임 테스트.**
