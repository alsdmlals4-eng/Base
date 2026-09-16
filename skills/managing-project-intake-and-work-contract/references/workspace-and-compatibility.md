# Conditional Workspace and Compatibility

명시된 legacy 이관·외부 workspace 예외·다른 작업 PR과 실제 중첩·구형 alias 해석이 필요할 때만 읽는다. 정상 repository-only 접수에는 필요하지 않다. 다른 PR read-only, 프로젝트 채택 계약 보존과 명시적 흡수 승인은 본문에서도 유지한다.

## Concurrent PR and absorption boundary

명시적인 user-directed 계속 작업에서 `same-goal`의 `in-progress PR`이 이미 있으면 `USER_DIRECTED_PARALLEL_PR`로 라우팅한다. 기존 PR은 read-only overlap evidence로만 확인하고 **do not modify/rebase/update** 하며, **current completed main**에서 **separate branch/PR**을 만든다. ordinary same-workstream coordination에서 허용된 경우 `synchronizing-local-and-github-state`의 concurrent preflight와 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 사용할 수 있다.

그러나 `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 항상 먼저 적용된다. 현재 작업의 더 구체적인 승인 계약이 다른 open/draft/ready PR 또는 다른 workstream을 `read-only / no absorption`으로 지정하면 standing copy-integration보다 우선한다. 그 PR의 material delta를 own 작업으로 가져오려면 **explicit absorption authorization**이 별도로 있어야 하며, 다른 workstream에는 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`을 충족해야 한다. 없으면 overlap 탐지·경로 회피·main의 이미 병합된 결과 재평가만 수행하고 selective copy·재구현·흡수·close·supersede 처리를 하지 않는다.

흡수가 명시적으로 허용된 ordinary coordination에서만 `PROVISIONAL_INTEGRATION`을 사용한다. owner PR branches는 read-only로 보존하고 필요한 material delta만 selective copy·재구현한 뒤 semantic reconciliation과 exact-head 검증을 수행한다. `absorbed_owner_deltas`와 `residual_owner_deltas`로 coverage를 증명한다. `scheduled/periodic` repository-writing automation도 unrelated open PR 존재 자체를 전역 blocker로 사용하지 않고 실제 path/semantic overlap만 국소 조정한다. 상세 경계는 [continuous-work-execution.md](continuous-work-execution.md)와 `synchronizing-local-and-github-state`를 따른다.

## Project workspace handling

현행 machine owner는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`이다. V3 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`은 `V3_COMPATIBILITY_AND_HISTORY_ONLY`로 유지하며 새 작업의 기본 계약으로 사용하지 않는다.

`NO_NEW_NOTION_WRITE_BY_DEFAULT`: Notion/Sheets는 아래 명시적 예외·이관 조건 외 기본 쓰기 대상이 아니다. 승인된 변경은 `REPOSITORY_DERIVED_VIEW_SYNC_DURING_WORK`로 repository owner와 적용되는 사람용 view에 반영한다.

```yaml
workspace_authority: DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE
project_canon: REPOSITORY_PRIMARY_CANON
human_facing_view: HUMAN_GDD_PDF_DERIVED_VIEW
notion: LEGACY_OPTIONAL_READ_ONLY_MIGRATION_SOURCE
google_sheets: MIGRATION_COMPATIBILITY_ONLY
google_sheet_compatibility_source: OPTIONAL_LEGACY_MIGRATION_INPUT
```

- 최신 repository 정본·실제 파일을 현재 계획·결정·구조화·runtime truth로 읽고, 사람용 PDF에는 exact source SHA와 evidence ceiling을 기록한다.
- `CURRENT_CODEX_HANDOFF.md`는 실제 인계가 있을 때만 사용하는 조건부 경로다. 같은 Work의 재개 정보는 기존 Active Context·작업 계약에 유지하며 별도 handoff 문서 생성을 요구하지 않는다.
- Base 채택은 승인된 운영 규칙에 한정한다. 프로젝트의 engine/version·저장 호환성·제품 의미·자산 승인·보안 계약은 최신 Base를 관찰했다는 이유로 조용히 교체하지 않는다.
- Base 자체 작업처럼 project-scoped migration surface가 적용되지 않으면 목적지를 발명하지 않는다.
- 기존 Notion 또는 Google Sheet가 실제 존재하면 고유 사용자 자료를 `UNIQUE / DUPLICATE / OBSOLETE`로 판정한다. `UNIQUE`만 repository 또는 명시적 non-canon 보관소로 이관 → readback/Test → consumer/reference 확인한다.
- Notion과 Sheet는 신규 입력·active Decision sync·완료 판정에 필요하지 않으며 신규 프로젝트에 생성하지 않는다. V4 예외는 explicit user approval, owner, scope, measurable value, revisit/exit 조건이 있을 때만 적용한다.

## State model

```text
RECEIVED
→ ROUTED
→ AWAITING_REUSE_PREFLIGHT | AWAITING_EXISTING_SOLUTION_REVIEW | PROMPT_DRAFTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED | REUSED_APPROVAL
→ CONTRACT_READY
→ EXECUTION_PLAN_READY
→ EXECUTED
→ REPORTED
→ SUPERSEDED | ABANDONED
```

연속작업은 위 상태 머신을 대체하지 않는 직교 실행 flag다.

```text
CONTINUOUS_WORK_INACTIVE
→ (CONTINUATION_INTENT_ALIASES + CONFIRMED/REUSED_APPROVAL)
→ CONTINUOUS_WORK_ACTIVE
→ COMPLETE | STOPPED_USER_DECISION | GLOBAL_TERMINAL_BLOCKER | STOPPED_BY_USER
```

`BLOCKED_UNVERIFIED`, `EVIDENCE_TRANSPORT_INCOMPLETE`, `DEFERRED_EXTERNAL_EXECUTOR`는 개별 task/evidence 상태가 될 수 있으며 자동으로 전역 종료 상태가 되지 않는다.

## Legacy aliases

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `grill-me`, `grillme`, `Grill Me` → `clarify` + [grill-me-protocol.md](grill-me-protocol.md)
- `transforming-requests-into-prompts` → `first-prompt` + `contract` + `clarify`
- `[좋은 프롬프트]`, `좋은 프롬프트`, `퍼스트 프롬프트`, `first prompt` → `first-prompt` + `contract` + `clarify`
- `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행` → 유효한 현재 승인 계약 + [continuous-work-execution.md](continuous-work-execution.md)

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`
