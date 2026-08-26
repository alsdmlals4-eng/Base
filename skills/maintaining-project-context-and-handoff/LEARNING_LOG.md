# Maintaining Project Context and Handoff Learning Log

## 2026-08-26 — Fresh-read bootstrap must be discoverable from the owning Skill

### Context

PR #719 added a narrow fresh-read companion reference so a new chat can reconstruct project identity, current goal, quality/stage, protected scope, next safe action, evidence ceiling and instruction surface from the project's current GitHub + Notion without requiring the prior conversation.

### Finding

The first GREEN attempt created `references/fresh-read-project-bootstrap.md` and routed the project Handoff template to it, but did not link that packaged reference from the owning `SKILL.md`. Base package-integrity correctly failed closed even though the reference itself was valid.

### Decision

- Keep Fresh-Read inside the existing `maintaining-project-context-and-handoff` owner rather than adding a new broad Skill.
- Link every packaged reference from the owning `SKILL.md`; indirect use from a template is not sufficient package discoverability.
- `resume` explicitly consumes `FRESH_READ_PROJECT_BOOTSTRAP` and does not make past conversation history a required input.
- Fresh-read remains a reconstruction/router contract, not a second project canon.

### Reuse boundary

This lesson applies to packaged Skill references/scripts generally: creating a useful companion artifact is incomplete unless its owning Skill makes it directly discoverable. It does not authorize registry expansion or duplicate broad Skills.

### Evidence

- PR #719 first GREEN attempt: exact head `54bdc0702dd5bf3725c12396e65034f2d40080fa`
- Failing regression: `tests.test_skill_package_integrity.SkillPackageIntegrityTests.test_every_packaged_reference_or_script_is_linked_from_its_skill`
- Corrected owner: `skills/maintaining-project-context-and-handoff/SKILL.md`
- Companion: `skills/maintaining-project-context-and-handoff/references/fresh-read-project-bootstrap.md`

### Status

`CURRENT_CORRECTION`

## 2026-08-25 — Correction: product responsibility, not code shape, determines Codex ownership

### Context

PR #674의 첫 역할 migration은 `GPT planning/review/visual → Codex implementation`을 너무 넓게 해석해 Base Python test·Registry/generated·CI contract까지 Codex에 넘기는 방향으로 확장됐다. 사용자가 의도한 경계는 달랐다.

### Finding

- **코드 파일이라는 사실은 Codex ownership 증거가 아니다.**
- Base 정책·Skill·Guide·Template·Registry/generated·CI/test contract는 공용 운영 인프라이므로 GPT가 소유한다.
- Notion/GDD/표/Flow/이미지/조사/검수 역시 GPT가 담당한다.
- Codex는 실제 게임 프로젝트의 Godot 제품 구현, 즉 GDScript·Scene·Resource·runtime wiring·build/export·implementation/runtime/play test에만 기본 진입한다.
- Handoff 문서가 “모든 code/data mutation = Codex”라고 쓰면 Base maintenance와 제품 구현 경계가 붕괴한다.

### Decision

```text
BASE / NOTION / PLAN / DOC / TABLE / VISUAL / GOVERNANCE → GPT
ACTUAL GAME-PROJECT GODOT PRODUCT IMPLEMENTATION → Codex
```

Codex handoff trigger는 파일 확장자나 GitHub write 여부가 아니라 `ACTUAL_GODOT_PRODUCT_IMPLEMENTATION_EXISTS`다.

GPT는 실제 Godot 제품 구현이 남았을 때만 프로젝트별 Work Instruction을 작성한다. Codex는 해당 게임 프로젝트의 GitHub + Notion을 재수화해 기술 구현 방향을 결정한다.

### Safety preserved

- stale PID/session 불신
- exact project/worktree/branch 확인
- rollback
- exact remote HEAD
- open PR read-only
- post-merge readback
- `CHANGE_PROPOSAL`
- `GPT_VISUAL_REQUEST`
- Codex 이미지 생성·생성형 편집 금지

### Reusable lesson

> **Owner migration은 파일 형식이 아니라 제품 책임을 기준으로 해야 한다.** Base maintenance code와 game product code는 같은 “code”라도 다른 owner다.

### Evidence

- `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `skills/maintaining-project-context-and-handoff/SKILL.md`
- `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md`
- `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

### Status

`CURRENT_CORRECTION`; PR #674 Base validation은 GPT가 끝까지 닫는다.

## 2026-08-25 — SUPERSEDED INTERIM: Role migration must classify consumers before rewriting contracts

이 항목의 **consumer classification 원리 자체는 유지**하지만 당시 `CODEX_IMPLEMENTATION_EXECUTOR`를 일반 repository implementation owner로 확장한 결론은 위 CURRENT_CORRECTION이 대체한다.

### Context

GPT와 Codex의 역할을 처음 재정의하는 과정에서 기존 Handoff·local-executor·test 계약에는 실제 안전 capability와 과거 ownership 표현이 같은 문자열 집합에 섞여 있었다.

### Finding

- `OPTIONAL_CODEX_EXECUTOR`, GPT Godot preproduction 같은 ownership literal은 current decision과 충돌했지만, wrong-target 방지·stale PID/session 차단·rollback·exact remote HEAD·continuous recovery·post-merge history 보호는 계속 필요했다.
- 문서를 짧게 만들며 old section을 통째로 제거하면 `동의 편향` 방지, 균형 요약의 좁은 예외, 승인 범위의 기술적 최소 finding 처리 같은 독립 capability까지 같이 사라질 수 있다.
- machine schema/version이나 기존 sync token을 역할 변경과 함께 불필요하게 바꾸면 unrelated compatibility break가 생긴다.
- bootstrap template과 Part Context Pack처럼 목적이 다른 문서를 같은 파일로 덮어쓰면 cold-start contract가 붕괴한다.
- test failure를 모두 stale assertion으로 취급하면 진짜 비퇴행 finding을 놓친다.

### Decision retained

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

- `PRESERVE_SEMANTIC`: 안전성·복구·검증 의미 유지
- `MIGRATE_OWNER`: capability의 실제 owner 변경
- `STALE_EXPECTATION`: superseded assertion 교체
- `HISTORICAL_SNAPSHOT`: 당시 기록 보존

### Superseded boundary

당시의 generic `CODEX_IMPLEMENTATION_EXECUTOR` 결론은 폐기됐다. 현재는 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`만 유효하다.

### Evidence from interim review

- 초기 lightweight contract: 137 tests / 9 failures → non-regression 보강 뒤 5 failures
- whole-core baseline: 2151 tests / 13 failures / 37 skips
- `templates/custom-instructions.codex.md` 오염 발견 및 복원
- Workspace schema v3 / `SYNC_BEFORE_IMPLEMENTATION` compatibility 복원
- canonical-reference freshness가 paired consumer 누락을 fail-closed로 검출

### Reuse boundary

consumer classification 원리는 authority migration에 계속 재사용한다. generic Codex ownership 결론은 재사용하지 않는다.

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

당시 확정된 방식은 GPT에서 기획·조사·구조 설계와 필요한 Godot POC·사전 구현을 오래 진행하고, 사용자가 Codex 전환을 요청하는 시점에 실행 명세를 만드는 구조였다. 이 항목은 역사적 계약이며 2026-08-25 current role correction이 대체한다.

### Finding

- 모든 Codex Build 전에 별도 읽기 전용 Codex Plan을 강제하면 저위험 작업에서도 비용·지연이 증가한다.
- GPT가 만든 명세는 의도 전달 계약이지 실제 구현 사실의 정본이 아니므로, Codex는 current repository/project 상태를 재검증해야 한다.
- 동일 승인 범위에 병합 승인을 반복 요청하면 승인 생명주기가 중복된다.

### Decision at that time

- `on-demand-codex-handoff` mode를 기존 Handoff Skill에 흡수
- `implementation-package-handoff` 유지
- Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`

### Validation evidence

- TDD RED: `32078a5afb886d71245a324529bf90cf33479ea2`
- 당시 GREEN은 Draft PR #215에서 진행

### Current supersession

2026-08-25 현재는 actual Godot product implementation이 있으면 사용자 별도 Codex 전환 요청 없이 project-specific Godot handoff를 만든다. Base/Notion/noncoding 작업은 GPT가 끝낸다.

## 2026-08-08 — Machine routing sync

- Post-merge audit found that the machine Registry still described the then-superseded mandatory Codex Plan flow.
- Registry triggers were updated to the then-current handoff and generated active-skill view rebuilt.
- Current 2026-08-25 routing must now be updated again to the Godot-product-only handoff contract.

## 2026-08-10 — Post-merge live-state reconciliation is conditional

- Sources: BCP-013, BCP-014, BCP-016, BCP-019, and the approved continuity design.
- A merge can stale a live continuation router even when its pre-merge snapshot remains valid history.
- Reuse boundary: run `post-merge-reconcile` only for `LIVE_CONTINUATION_STATE`; retain `PRE_MERGE_SNAPSHOT`, never create automatic writeback or self-SHA loops.
- Validation: `tests/test_gpt_codex_workflow_contract.py` plus the handoff and freshness contract suites.
