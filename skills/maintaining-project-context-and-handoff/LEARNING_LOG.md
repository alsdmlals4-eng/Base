# Maintaining Project Context and Handoff Learning Log

## 2026-08-25 — Role migration must classify consumers before rewriting contracts

### Context

GPT와 Codex의 역할을 `GPT planning/review/visual → Codex implementation`으로 바꾸는 과정에서 기존 Handoff·local-executor·test 계약에는 **실제 안전 capability와 과거 ownership 표현이 같은 문자열 집합에 섞여** 있었다.

### Finding

- `OPTIONAL_CODEX_EXECUTOR`, GPT Godot preproduction 같은 ownership literal은 current decision과 충돌하므로 폐기 대상이지만, 그 주변의 wrong-target 방지·stale PID/session 차단·rollback·exact remote HEAD·continuous recovery·post-merge history 보호는 계속 필요했다.
- 문서를 짧게 만들며 old section을 통째로 제거하면 `동의 편향` 방지, 균형 요약의 좁은 예외, 승인 범위의 기술적 최소 finding 처리 같은 독립 capability까지 같이 사라질 수 있다.
- machine schema/version이나 기존 sync token을 역할 변경과 함께 불필요하게 바꾸면 role migration이 unrelated compatibility break를 만든다.
- bootstrap template과 Part Context Pack처럼 목적이 다른 문서를 같은 파일로 잘못 덮어쓰면 이름은 남아 있어도 cold-start contract가 붕괴한다.
- test failure를 모두 stale assertion으로 취급하면 진짜 비퇴행 finding을 놓치고, 반대로 old literal을 전부 되살리면 새 역할 결정이 무효화된다.

### Decision

역할·executor·authority migration은 다음 순서로 수행한다.

```text
current authority / user decision
→ active consumer inventory
→ each consumer = PRESERVE_SEMANTIC | MIGRATE_OWNER | STALE_EXPECTATION | HISTORICAL_SNAPSHOT
→ source contract 최소 교정
→ schema/compatibility unrelated delta 되돌림
→ paired test + Learning Log + Registry/generated migration
→ exact-head regression
→ whole-state adversarial re-attack
```

- `PRESERVE_SEMANTIC`: 안전성·복구·검증 의미는 owner가 바뀌어도 유지한다.
- `MIGRATE_OWNER`: GPT local bootstrap의 wrong-target/session safety처럼 capability는 Codex execution-environment owner로 이동한다.
- `STALE_EXPECTATION`: `OPTIONAL_CODEX_EXECUTOR`, GPT product preproduction 같은 superseded ownership assertion은 새 positive/negative regression으로 교체한다.
- `HISTORICAL_SNAPSHOT`: 날짜/SHA/당시 계약을 설명하는 기록은 현재 문구로 소급 수정하지 않는다.

### Current role boundary learned

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
```

Codex image prohibition은 단순 “이미지 tool을 쓰지 않음”이 아니라 **현재 용도 승인 + Notion upload/attach/readback된 Visual만 구현 input으로 소비**하고 누락 시 `GPT_VISUAL_REQUEST`로 반환한다는 handoff 계약까지 포함한다.

### Evidence

- PR #674 초기 lightweight contract: 137 tests / 9 failures에서 non-regression 보강 뒤 5 failures로 축소.
- whole-core baseline `c59fa9b...`: 2151 tests / 13 failures / 37 skips. 여기서 stale ownership assertion과 실제 neutral-review/one-shot/bootstrap finding을 분리했다.
- `templates/custom-instructions.codex.md`가 P08 Context Pack으로 오염된 것을 independent bootstrap contract가 검출했고 `c322deab...`에서 stable bootstrap으로 복원했다.
- `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`의 불필요한 schema 3→4 및 sync key 변경을 latest main과 대조해 schema v3 / `SYNC_BEFORE_IMPLEMENTATION`으로 복원하고 role fields만 additive로 유지했다.
- canonical-reference freshness는 Handoff Skill 변경에 paired test + local Learning Log + common Skill Learning Log + behavior companion을 요구해 partial migration을 fail-closed로 차단했다.

### Reuse boundary

이 교훈은 역할·executor·authority·workspace owner를 교체하는 migration에 재사용한다. 단순 오탈자나 isolated L0 rename에는 전체 consumer classification을 강제하지 않는다.

`CLEAN_REVIEW_EXIT`는 paired machine consumer migration과 exact-head regression이 닫힐 때까지 주장하지 않는다.

## 2026-08-10 — External runtime session resume needs current evidence

### Context

An external Editor/MCP runtime target can be absent from a session registry while an earlier process or transport observation still exists. A handoff that presents those historical values as current authority can select the wrong target or resume unsafe work.

### Finding

- A past PID, WebSocket connection, or session ID does not prove current target identity, transport ownership, or registry registration.
- A missing target session does not prove process failure and does not authorize a shared-server restart or another project's session selection.
- Recovery of the automation session only reopens approved runtime work; it does not prove product tests, runtime behavior, human QA, release readiness, or production readiness.

### Decision

- Keep full same-snapshot external-session diagnosis in the Godot Live Editor security/recovery authority.
- In a Handoff, label stale PID/session values as historical evidence and require fresh current reads before target selection or mutation.
- Retain `BLOCKED_UNVERIFIED` when process, transport, bounded server logs, and immediate registry evidence cannot be tied to the same observation window.

### Boundary and validation

This does not add an external transport, MCP server, process-control implementation, or project runtime proof. Focused same-snapshot recovery contract tests verify the owner/consumer boundary; actual external runtime reproduction remains `NOT_RUN` until a project provides an isolated harness.

## 2026-08-08 — On-demand Codex handoff and inherited merge authority

### Context

최근 확정된 실제 작업 방식은 GPT에서 기획·조사·구조 설계와 필요한 Godot POC·사전 구현을 오래 진행하고, 사용자가 Codex 전환을 요청하는 시점에만 실행 명세를 만들어 실제 저장소·프로젝트·Godot 상태를 다시 확인시키는 구조다.

### Finding

- 모든 Codex Build 전에 별도 읽기 전용 Codex Plan을 강제하면 명확한 저위험 작업에서도 비용·지연이 증가한다.
- GPT를 비-Godot 작업으로만 제한하면 현재 도구·POC·사전 제작 활용 방식과 충돌한다.
- GPT가 만든 명세는 의도 전달 계약이지 실제 구현 사실의 정본이 아니므로, Codex는 현재 GitHub 저장소·프로젝트 파일·Godot 상태를 직접 재검증해야 한다.
- 사용자가 이미 명시적으로 승인한 동일 범위에 병합 승인까지 반복 요청하면 승인 생명주기가 중복된다. 다만 새 범위·새 기획 결정·`USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·P0/P1은 기존 승인으로 덮으면 안 된다.

### Decision

- 새 광역 Skill을 만들지 않고 기존 `maintaining-project-context-and-handoff`에 `on-demand-codex-handoff` mode를 추가한다.
- `implementation-package-handoff`는 L2 이상·다중 의존성·고위험 작업의 패키지 인계 책임을 유지한다.
- Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`로 바꾸고 위험·불확실성·사용자 요청에 따라 선택한다.
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 적용해 동일 승인 범위의 PR은 새 차단 finding이 없으면 추가 확인·재승인·병합 승인 요청 없이 검증 후 병합한다.

### Validation evidence

- TDD test-only RED: `32078a5afb886d71245a324529bf90cf33479ea2`
- RED에서 새 on-demand/merge-authority 계약 부재로 required validation failure를 확인했다.
- GREEN 구현은 Draft PR `#215`에서 진행 중이며 exact-head contract, reference freshness, adversarial, Required Check를 다시 검증한다.

### Reuse boundary

새 Skill은 독립 입력·산출물·승인 권한이 생기고 기존 Handoff 책임에 넣을 때 경계가 무너지는 경우에만 검토한다. 현재는 같은 인계 생명주기의 mode 차이이므로 기존 Skill 흡수가 더 적합하다.

## 2026-08-08 — Machine routing sync

- Post-merge audit found that the machine Registry still described the superseded mandatory Codex Plan flow.
- Registry triggers now discover on-demand Codex handoff and the generated active-skill view is rebuilt from the same machine source.
- This closes the policy → Skill → Registry → generated-view propagation gap.

## 2026-08-10 — Post-merge live-state reconciliation is conditional

- Sources: BCP-013, BCP-014, BCP-016, BCP-019, and the approved continuity design.
- A merge can stale a live continuation router even when its pre-merge snapshot remains valid history.
- Reuse boundary: run `post-merge-reconcile` only for `LIVE_CONTINUATION_STATE`; retain `PRE_MERGE_SNAPSHOT`, never create automatic writeback or self-SHA loops.
- Validation: `tests/test_gpt_codex_workflow_contract.py` plus the handoff and freshness contract suites.
