# BCP-2026-012 — Handoff Current Router Freshness Guard

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 기준 커밋: `6cd14324a3de1a1b2a9898aaee1e9535c87c8fdc`
- 제출일: `2026-08-10`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `재현된 프로젝트 관찰 + 공용화 가설`

## 관찰과 증거

Switchy Express 인수인계 작업에서 다음 상태가 동시에 존재했다.

1. `CURRENT_CONFIRMED_DECISIONS.md`와 configured Google Sheet는 `SX-DEC-055`까지 현재 상태였다.
2. 프로젝트 `main`도 `SX-DEC-055` decision/spec/DoR closure까지 병합된 상태였다.
3. 그러나 `START_HERE.md`, `ACTIVE_CONTEXT.md`, `ROADMAP.md`는 훨씬 오래된 PR #83~100 / SX-DEC-042 이전 실행 큐와 Android Device Smoke 즉시 실행 상태를 여전히 `현재`로 안내했다.
4. 이 세 파일은 모두 정상 경로의 현행 문서였기 때문에 단순 존재 여부·링크 유효성 검사만으로는 drift를 발견하기 어려웠다.
5. 사용자가 `SX-DEC-055` 구현을 나중으로 미루고 인수인계를 요청하자, 저장소·Sheet·Base를 재조회한 뒤 current-router 문서를 교정해야 새 세션이 잘못된 실행 큐로 진입하지 않게 됐다.

프로젝트 handoff branch `agent/handoff-sx-dec-055-deferred`에서 확인된 최소 수정은 다음 세 owner였다.

- `START_HERE.md`: 현재 결정 범위, 현재 작업 모드, 재개 read order.
- `ACTIVE_CONTEXT.md`: baseline, approval refs, completed/not-started/blocked/superseded, verification, resume trigger, stop conditions.
- `ROADMAP.md`: 즉시 실행 lane과 별도 열려 있는 검증 lane 분리.

이 문제는 프로젝트 고유 규칙이 아니라 **“current로 라우팅하는 문서가 더 권위 있는 현재 상태보다 오래된 경우 handoff가 잘못된 다음 작업을 전달할 수 있다”**는 공용 운영 문제다.

## 일반화 후보

### 1. Current Router Freshness Gate

`maintaining-project-context-and-handoff`의 `context-refresh`, `session-handoff`, `resume`는 handoff 완료 전에 다음을 비교한다.

```text
현재 GitHub default branch / latest commit / open same-goal PR
+ 실제 current owner docs / code / tests
+ project Decision/Registry authority
+ configured external state owner가 있으면 그 current row/state
→ START_HERE / ACTIVE_CONTEXT / ROADMAP / HANDOFF 같은 current router의 주장 비교
```

다음 중 하나라도 발견되면 `STALE_CURRENT_ROUTER`다.

- current router의 결정 범위가 authoritative current registry보다 뒤처짐;
- 이미 merged/closed된 작업을 pending/current로 지시함;
- 사용자 최신 deferral/resume 상태와 next executable task가 충돌함;
- `NOT_RUN` 별도 검증 lane을 즉시 현재 작업으로 잘못 라우팅함;
- 저장된 baseline SHA/branch를 실제 current state보다 우선함.

`STALE_CURRENT_ROUTER`가 있으면 handoff는 완료로 보고하지 않고, owner를 갱신하거나 명시적으로 historical/reference-only로 낮춘다.

### 2. Deferral은 승인 취소가 아니다

승인된 작업이 사용자의 최신 지시로 나중으로 미뤄졌다면 다음 상태를 분리한다.

```yaml
approval: PRESERVED
implementation: NOT_STARTED | PARTIAL
execution: USER_DEFERRED
resume_trigger: explicit user resume or named dependency resolution
next_executable_step: exact approved next step
new_approval_required_for_same_scope: false
```

새 제품/게임플레이/semantic 범위, 승인 범위 확대, P0/P1 blocker가 생기면 별도 사용자 결정이 필요하지만, 같은 승인 범위를 단순 재개할 때 승인 질문을 반복하지 않는다.

### 3. Active Context는 state router다

`ACTIVE_CONTEXT`는 장문 기획 복제가 아니라 다음 최소 continuation contract를 갖는다.

```yaml
baseline:
authority:
progress:
  completed_verified:
  completed_not_merged:
  in_progress:
  ready_next:
  not_started:
  blocked:
  superseded:
verification:
changes:
review:
resume:
  trigger:
  next_executable_step:
  next_read_order:
  stop_conditions:
  user_decision_needed:
```

값이 없는 프로젝트는 필드를 생략할 수 있지만, **다음 실행 지점·중단 조건·검증되지 않은 영역**은 반드시 구분한다.

### 4. START_HERE는 cold-start router다

`START_HERE`는 최소 다음을 보여준다.

- 현재 결정/제품 범위;
- 현재 작업 모드;
- 즉시 실행할 작업이 있는지 없는지;
- 재개 시 첫 작업;
- current main 관측점과 이것이 runtime truth보다 낮은 snapshot임을 명시;
- 새 작업자의 최소 read order;
- 별도 열린 physical/device/human gate가 현재 작업인지 단순 open lane인지.

### 5. ROADMAP은 immediate lane과 open lane을 분리한다

Roadmap에 `CURRENT`라고 적힌 항목이 자동으로 next executable이 되지 않도록 다음을 구분한다.

- `CURRENT_EXECUTION`: 지금 실행할 승인된 lane.
- `OPEN_NOT_RUN`: 유효하지만 지금 실행 지시가 없는 gate.
- `BLOCKED`: 선행 조건이 필요한 lane.
- `USER_DEFERRED`: 승인됐지만 최신 사용자 지시로 보류된 lane.

프로젝트가 기존 다른 용어를 사용하면 동일 의미를 유지하는 매핑으로 적용할 수 있다.

## 프로젝트 전용으로 남길 내용

Base 활성 계약에는 다음 Switchy Express 고유값을 넣지 않는다.

- `SX-DEC-055`, `SX-DEC-053/054`, 각 PR 번호·SHA·Actions run ID.
- 73개 product PNG 수량과 asset 이름.
- Switchy Express의 LIFO, route-end, switch, cargo pickup 규칙.
- 해당 프로젝트 Google Sheet ID와 tab/row 번호.
- Android/Windows/asset-vault 프로젝트 고유 상태.
- 프로젝트의 실제 local path와 Godot 파일 경로.

이 값은 proposal의 출처 증거로만 남긴다.

## 적용 조건과 비사용 조건

적용:

- 세션/작업자/AI/브랜치/마일스톤 경계에서 handoff를 작성할 때.
- 사용자가 승인된 작업을 중단·보류하고 나중에 재개하려 할 때.
- `START_HERE`, `ACTIVE_CONTEXT`, `ROADMAP`, `HANDOFF` 중 둘 이상이 current 상태를 안내할 때.
- Decision/Registry/Sheet/actual main이 진전됐는데 cold-start router가 따라오지 않았을 가능성이 있을 때.
- 과거 대화 없이 새 작업자가 저장소만으로 다음 작업을 판단해야 할 때.

비사용:

- L0 오탈자처럼 다음 작업을 바꾸지 않는 변경.
- current router 자체가 없는 작은 일회성 저장소.
- 과거 archive/historical handoff 문서의 내용을 현재 owner로 승격하지 않는 단순 보존 작업.
- external Sheet/DB가 configured owner가 아닌 프로젝트에 해당 소스를 강제하는 경우.

## 반례와 위험

### 반례 1 — 모든 current 문서의 SHA를 항상 동일하게 강제

실패 이유:
- 한 문서는 기능 검증 SHA, 다른 문서는 documentation closure SHA를 기록할 수 있다.
- 단순 SHA equality는 실제 authority semantics를 표현하지 못한다.

판정: `AVOID`.

대신 각 저장된 SHA는 `snapshot/evidence`임을 명시하고 실제 current main 및 owner semantics와 모순 여부를 본다.

### 반례 2 — START_HERE에 모든 상태를 복제

실패 이유:
- Decision/Registry/Active Context/Roadmap과 이중 정본이 된다.
- handoff마다 대량 동기화 비용이 생긴다.

판정: `AVOID`.

START_HERE는 router와 summary만 소유한다.

### 반례 3 — 승인된 보류 작업을 취소/미승인으로 되돌림

실패 이유:
- 같은 scope 재개 때 불필요한 승인 질문을 반복한다.
- 과거 승인 lineage를 잃는다.

판정: `MUST_NOT`.

### 반례 4 — OPEN_NOT_RUN physical gate를 자동으로 next task로 승격

실패 이유:
- 사용자가 다른 작업을 명시적으로 보류/전환했을 때 latest intent를 무시한다.
- validation lane이 유효하다는 사실과 지금 실행할 작업이라는 사실은 다르다.

판정: `MUST_SEPARATE`.

### 위험

- 너무 엄격한 freshness gate가 작은 프로젝트에 문서 오버헤드를 늘릴 수 있다.
- external source가 configured owner인지 판정하지 않으면 불필요한 Google Sheet/DB 의존성을 강제할 수 있다.
- 날짜만 비교하면 실제 semantic freshness를 잘못 판단할 수 있다.

따라서 implementation은 **필드/문서 존재 강제보다 의미상 current-routing contradiction 탐지와 handoff checklist 보강**에 집중한다.

## 영향 범위와 검증

승인된 최소 구현 후보:

1. `skills/maintaining-project-context-and-handoff/SKILL.md`
   - `current-router-freshness` 하위 계약 추가.
   - `context-refresh/session-handoff/resume` 종료 전에 `STALE_CURRENT_ROUTER` 비교 요구.
   - approved-but-deferred resume semantics 명시.
2. `templates/project-operations/ACTIVE_CONTEXT.md`
   - compact Continuation State 필드 추가.
3. `templates/project-operations/PROJECT_START_HERE.md`
   - current work mode / immediate task / resume first step / snapshot-vs-runtime truth 안내 추가.
4. `templates/project-operations/HANDOFF.md`
   - current-router freshness result, approval preservation, resume trigger/step/stop condition 추가.
5. `templates/project-operations/ROADMAP.md`
   - current execution / open-not-run / blocked / user-deferred lane distinction 예시 추가.
6. `tests/test_game_project_operating_system_structure.py`
   - 위 공용 contract가 template/Skill에서 빠지지 않는 회귀 테스트.
7. Skill body 변경이 canonical freshness 정책상 요구하면 해당 learning evidence를 같이 갱신한다.

제외:

- 새 ACTIVE Skill ID.
- 새 broad Handoff/Progress authority.
- 특정 프로젝트 파일 자동 수정 tool.
- 프로젝트별 Decision/Sheet schema 강제.
- Base release pin/tag 변경.
- open unrelated PR #136/#137 내용 흡수.

검증 시나리오:

1. **기준:** current registry와 routers가 일치 → handoff 정상 완료.
2. **stale decision span:** registry는 N인데 START_HERE가 N-3 → `STALE_CURRENT_ROUTER` repair/block 요구.
3. **stale merged work:** ACTIVE_CONTEXT가 이미 merged된 PR을 pending으로 지시 → superseded repair 요구.
4. **deferred approval:** approved task + user deferral → approval preserved, implementation not started, resume step retained.
5. **open physical lane:** `NOT_RUN` gate는 남되 immediate next task로 자동 승격되지 않음.
6. **no external owner:** configured Sheet/DB가 없으면 외부 소스 조회를 강제하지 않음.
7. existing handoff / one-click-play / on-demand Codex handoff regressions PASS.

## 필요한 도구·파일·권한

- 필요 항목: Base GitHub read/write, existing GitHub Actions.
- 필요한 이유: proposal/implementation 분리, exact-head 회귀 검증, merge.
- 설치·적용 방법: 신규 외부 도구 설치 없음.
- 설치 후 확인 명령: repository contract tests + required GitHub Actions exact-head.
- 최소 권한: Base branch/PR create·push·merge 권한.

## 승인과 구현

- 사용자 승인 근거: `2026-08-10 KST 사용자 직접 지시 — "Base에도 이번 작업에서 얻은 개선점을 별도 수정제안서로 먼저 작성한 뒤 병합까지 진행하면 돼"`
- 승인 해석: proposal과 implementation PR을 분리하되, 위 최소 공용화 범위는 추가 재승인 질문 없이 진행 가능. 새 broad Skill, project-specific 값 승격, release 변경은 승인 범위 밖이다.
- approval_ref: `[수정제안서]/BCP-2026-012-handoff-current-router-freshness/PROPOSAL.md#승인과-구현`
- 구현 PR: `proposal merge 후 별도 생성`
- 롤백: implementation PR의 Skill/template/test/learning 변경만 revert한다. proposal/Registry 이력은 보존한다.
