---
name: maintaining-project-context-and-handoff
description: Use when resuming project state, correcting stale Active Context, or transferring approved work across an actual session or capability boundary.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context는 현행 owner·완료/미완료·검증·다음 작업을 연결하는 압축 라우터다. 과거 대화 없이 재개할 수 있게 만들되 같은 내용을 복제하지 않는다.

역할 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`.
Workspace: `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
Machine contract: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`.

`UNIFIED_WORK_EXECUTION` / `CAPABILITY_BASED_EXECUTOR_SELECTION`: 승인된 작업은 현재 Work의 실제 도구로 기획·코딩·검증까지 이어간다. 앱 이름으로 제품 구현을 다른 실행자에게 강제 전달하지 않는다. `CAPABILITY_IS_NOT_AUTHORIZATION`을 유지한다.

## Modes and conditional reads

- `context-refresh`: 실제 변경과 최신 owner에서 현재 상태·다음 작업을 압축한다.
- `resume`: [fresh-read-project-bootstrap.md](references/fresh-read-project-bootstrap.md)의 `FRESH_READ_PROJECT_BOOTSTRAP`으로 Project `AGENTS.md`, main·관련 PR·결정·Active Context·actual consumer를 확인한다.
- `session-handoff`: 실제 세션/담당자 경계에서만 재개 스냅샷을 만든다.
- `codex-godot-implementation-handoff`: 사용자 지정 또는 실제 capability gap으로 Codex 인계가 필요할 때만 [gpt-codex-implementation-handoff.md](references/gpt-codex-implementation-handoff.md)를 읽는다. 이름은 호환용이다.
- `implementation-package-handoff`: 큰 승인 범위의 독립 구현·검증 단위를 연결한다. 패키지는 승인 범위 축소가 아니다.
- `legacy-migration-resume`: 고유 미이관 Notion/Sheet 자료가 실제 있을 때만 해당 상태를 복원한다.
- `post-merge-reconcile`: current-task 병합 후 LIVE_CONTINUATION_STATE를 exact main과 맞춘다.

복구 경로 자체를 평가할 때만 [long-horizon-failure-recovery-pilot.md](references/long-horizon-failure-recovery-pilot.md)와 [case specification](references/long-horizon-failure-recovery-pilot.json)을 사용한다. 이 파일은 결과가 아니며 매 재개 때 실행할 의무가 없다.

## Process

1. 승인 범위·현재 결정·실제 구현·검증 상태를 읽는다. 상태 전달 요청이 없는 단순 문서/이미지 제작에는 이 Skill을 추가하지 않는다.
2. 현재 세션의 repository 읽기/수정, tests, engine, image 도구 능력을 각각 확인한다. 가능한 승인 작업은 계속한다. runtime이 없다는 이유만으로 가능한 코딩까지 전부 멈추지 않는다.
3. current state / changed scope / remaining work / blocker / owner paths / exact revision / first next action만 기존 Active Context에 갱신한다. 과거 진행 일지를 계속 prepend하지 않는다.
4. `HANDOFF_ONLY_FOR_CAPABILITY_GAP_OR_EXPLICIT_REQUEST`일 때 기존 인계 Template을 사용한다. 같은 세션의 단계 전환에는 새 handoff 파일을 만들지 않는다.
5. 실제 검사·runtime·사용자 승인·병합은 따로 판정하고 evidence ceiling을 기록한다. `NOT_RUN`은 PASS가 아니다.
6. 컨텍스트가 길어지거나 작업을 종료·재개할 때는 [프로젝트 인수인계·컨텍스트 설계 방법](../../docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md)의 파일 기반 재개·동기화·가지치기 절차를 따른다. 현재 작업에 필요한 owner와 Blueprint source SHA만 연결하고 전체 대화·모든 Skill을 다시 싣지 않는다. 대체 완료·역참조·복구가 확인된 구형 파일만 삭제하며, 프로젝트 작업에도 동일하게 적용한다.

## Implementation contract

`PLAY_MEANINGFUL_WORK_SLICE`의 work_slice_id, player outcome, approved_scope, explicit_non_scope, protected_scope, actual consumer, data/UI/asset dependencies, Acceptance와 검증 진입점을 기존 owner에서 연결한다.
`PLANNING_CANON_BEFORE_HANDOFF`는 구현 전 승인 의미를 기록하는 안전 조건이다. `PRE_HANDOFF_GPT_STOP`은 기획을 멈추고 구현으로 이동하는 legacy 이름이며 Work 종료가 아니다.

인계할 때만 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF`와 `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`를 사용한다. 받는 실행자는 exact project/repository/worktree, source SHA, dirty/diverged, project.godot, 채택 authoring authority, 실제 tests/runtime을 확인한다. stale PID/session/port를 신뢰하지 않는다.

`CHANGE_PROPOSAL`은 새로운 코어·주요 UX·경제·서사·Art Direction·범위·저장 호환성 결정에 필요하다. 승인 범위의 기술 교정은 routine 재승인 없이 계속한다.

## Visual and safety

- 이미지 도구가 있으면 실제 consumer에 필요한 후보를 현재 세션에서 만들 수 있다. 사용자 승인 전 정본 승격·runtime 확정 금지.
- `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`로 승인 binary·consumer·provenance·상태를 확인한다.
- 이미지 도구/승인이 없으면 `GPT_VISUAL_REQUEST` / `WAITING_GPT_VISUAL`은 호환 상태이며 미완료를 숨기지 않는다.
- 다른 open PR/worktree 보존, force push/history rewrite/destructive reset 금지.
- Notion Project Home/Domain/AI System은 legacy migration source only이며 기본 구현 입력이 아니다.

## Output and failure conditions

현재 상태·owner·exact SHA, 완료/미완료, 실제 검사와 evidence ceiling, blocker/rollback, 다음 행동을 제공한다. `READY_FOR_GPT_REVIEW` 상태만으로 구현·독립 검토 PASS를 선언하지 않는다.

실패: 도구 이름만으로 capability/권한 추정, 가능한 Work 구현을 강제 인계, 이미 승인된 같은 계약 재인터뷰, 미검증 runtime을 PASS 처리, 다른 PR takeover, 오래된 PDF/채팅을 current truth로 사용, 후보 이미지를 승인 자산으로 간주.

## Retired compatibility

`GPT_NONCODING_PROJECT_OWNER`, `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`, `CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`, `GPT_BASE_NOTION_GOVERNANCE_OWNER_RETIRED`는 RETIRED_ROLE_SPLIT_COMPATIBILITY다. Base/Notion/문서/기획/이미지 작업을 Codex에 넘기지 않는다는 과거 일괄 제한도 현행 실행자 선택 규칙이 아니다.
