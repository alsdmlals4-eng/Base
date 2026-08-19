---
contract_name: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT
contract_version: "9.1"
release_line: "Base v9.3"
active_authority: true
status: ACTIVE_EXECUTION_CONTRACT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
usage: "이 파일 하나만 첨부하면 GitHub·exact Project Notion 상태 복원부터 GPT 기획·검수, 필요 시 Codex 보조 구현, 검수·병합·postmerge 동기화까지 현재 작업에 필요한 절차를 실행한다."
execution_model: SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION
legacy_contracts:
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md
  - LEGACY_REFERENCE_INPUT: VERTICAL_SLICE_MASTER_REFERENCE_v6.md
core_policies:
  - APPLICATION_BINDING
  - REPOSITORY_FIRST_INTERVIEW
  - INTEGRATED_DELIVERY_PROFILE
  - RECONCILIATION_PLANNING_PROFILE
  - CONDITIONAL_RECONCILIATION
  - DUPLICATE_OMISSION_CONFLICT_AUDIT
  - LEGACY_REQUIREMENT_TRACEABILITY
  - SOURCE_CONSUMER_PROPAGATION_AUDIT
  - EVIDENCE_BEFORE_COMPLETION
  - INTERMEDIATE_VISUAL_CHECKPOINT
  - NOTION_VISUAL_CHECKPOINT_BEFORE_POC
  - APPROVED_VISUALS_FEED_POC
  - GPT_PRIMARY_PLANNING_REVIEW
  - CODEX_OPTIONAL_SUB_EXECUTOR
  - AGENT_MERGE_REQUIRED
---

# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약 v9

## 0. 역할과 권한

이 계약은 **GPT 기획·검수**를 기본 주 책임으로 두고, 실제 repository/engine mutation이 필요할 때만 Codex를 보조 executor로 연결한다. 이 파일 하나를 첨부했다고 해서 Codex 구현, 제품 범위, 사용자 Decision이 자동 승인되지 않는다.

```text
latest user decision
→ project AGENTS / security / engine / data rules
→ GitHub current canon and actual implementation
→ exact Project Notion human-facing canon
→ project Base adapter / Skill snapshot / router
→ pinned Base release
→ this v9 contract
→ v6-v8 LEGACY_REFERENCE_INPUT
```

과거 Prompt, 예전 HTML, retired local app, Google Sheet, 구형 Skill 이름은 current authority가 아니다. `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`는 `SUPERSEDED_COMPATIBILITY`로 보존한다.

`CORE_POC`, `SLICE_VALIDATION`, `VERTICAL_SLICE_FULL_PROFILE`은 historical/compatibility concept으로 자동 치환하지 않는다. 각 프로젝트에서 `CURRENT`, `LEGACY_REFERENCE_ALLOWED`, `CANON_CONFLICT`, `STALE_REFERENCE`를 판정한다.

## 1. APPLICATION_BINDING

다른 단계보다 먼저 `Baseline Recovery Record`에 다음을 기록한다.

1. `origin/main` 정확한 SHA, 현재 branch/PR, 보호 경로.
2. 프로젝트 `AGENTS.md`, START_HERE, Active Context, Decision Registry, design map.
3. 실제 code/data/Scene/Resource/asset/test와 열린 Issue/PR.
4. exact Project Notion Home과 Project-filtered Work/Asset/Core System/Visual/Reference surfaces.
5. Project relation, relevant Notion revision/readback state.
6. Base `release_commit`, `release_evidence_commit`, Registry/Snapshot/router binding.
7. Google Sheets가 현재 migration scope에 포함되는지. 포함되더라도 `RETIRED_MIGRATION_ONLY`이며 `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`만 허용한다.

어댑터·snapshot·router·actual project path가 맞지 않거나 Base pin을 검증할 수 없으면 추측 실행하지 않고 `BLOCKED_UNVERIFIED`다.

## 2. REPOSITORY_FIRST_INTERVIEW + GitHub/Notion preflight

`REPOSITORY_FIRST_INTERVIEW`는 GitHub만 읽는다는 뜻이 아니다. structured/runtime truth는 repository에서, 사람이 보는 current direction/visual/table/flow는 **exact Project Notion**에서 읽는다.

이미 확정된 질문을 되묻지 않고 현재 요청을 다음으로 분류한다.

```text
AUDIT_ONLY
→ 읽기·감사·visual review·Change Plan

PLAN_OR_DECISION
→ GPT 기획·근거·Approval Bundle·Notion/repository update proposal

IMPLEMENTATION_REQUESTED
→ approved implementation contract
→ OPTIONAL_CODEX_HANDOFF when actually needed
→ implementation / test / runtime verification

SYNC_OR_RELEASE_FOLLOWUP
→ merged main + exact Project Notion readback
→ Gate Close
```

## 3. 실행 프로필

### INTEGRATED_DELIVERY_PROFILE

기획부터 실제 구현까지 승인된 범위에서 연결한다.

```text
허용:
GitHub + Notion current-state audit
→ GPT planning / >=3 alternatives / benchmark / adversarial review
→ representative visual checkpoint when material
→ approval
→ canonical update
→ optional Codex implementation handoff
→ tests / Godot validation
→ GPT final review
→ exact-head PR / merge / postmerge readback

금지:
요청·승인·Issue/Goal 없이 제품 범위를 발명하는 구현
→ protected path bypass
→ retired Sheet/HTML/local app를 current canon으로 복원
→ Notion preview를 runtime proof로 주장
→ 실제 증거 없는 사람/기기/runtime 완료 주장
```

구현 최소 조건:

1. 현재 요청 또는 승인된 Change Plan이 구현을 연다.
2. `APPLICATION_BINDING`, canon recovery, blocking `P0/P1`·`CANON_CONFLICT`가 닫혔다.
3. Goal/Issue, protected behavior, acceptance criteria, rollback, test/runtime evidence가 명시됐다.
4. 시각이 material하면 `NOTION_VISUAL_CHECKPOINT_BEFORE_POC`가 닫혔다.

### RECONCILIATION_PLANNING_PROFILE

`RECONCILIATION_PLANNING_PROFILE`은 모든 첨부의 기본값이 아니라 감사·복원·planning-only 작업에서 선택한다.

```text
허용: canon recovery, comparison, integrity audit, visual simulation, Finding/Change Plan
금지: 게임 코드·Scene·데이터·에셋 수정, approved Decision overwrite, destructive migration, 제품 범위 PR 병합
```

`Google Sheet 쓰기`는 이 프로필에서 금지다. 정상 delivery profile에서도 Sheet는 current workspace가 아니라 one-time migration source일 뿐이다.

필요하면 같은 첨부 계약 안에서 `INTEGRATED_DELIVERY_PROFILE`로 전환하되 새 승인 범위를 발명하지 않는다.

## 4. 통합 실행 루프

```text
1. APPLICATION_BINDING
2. REPOSITORY_FIRST_INTERVIEW
3. PROFILE_SELECTION
4. BASELINE_RECOVERY + DUPLICATE_OMISSION_CONFLICT_AUDIT
5. EVIDENCE_PACK + APPROVAL_BUNDLE
6. GPT_PLANNING_AND_REVIEW
7. INTERMEDIATE_VISUAL_CHECKPOINT when material
8. CANONICAL_UPDATE
9. OPTIONAL_CODEX_HANDOFF when actual implementation needs it
10. CANONICAL_UPDATE_AND_IMPLEMENTATION
11. SOURCE_CONSUMER_PROPAGATION_AUDIT
12. VALIDATION
13. INDEPENDENT_REVIEW + adversarial review
14. MERGE_AND_SYNC
15. POSTMERGE_READBACK
16. USER_LEARNING_COMPLETION_REPORT
```

`PLAN_AND_CODEX_HANDOFF`는 legacy term으로 발견될 수 있으나 current behavior는 `GPT_PLANNING_AND_REVIEW → OPTIONAL_CODEX_HANDOFF`다. Codex를 모든 변경의 의무 단계로 사용하지 않는다.

## 5. CONDITIONAL_RECONCILIATION

기존 프로젝트를 백지에서 재설계하지 않는다. finding은 다음으로 분류한다.

```text
DUPLICATE_WORK
MISSING_CANON
MISSING_CONSUMER
CANON_CONFLICT
IMPLEMENTATION_CONFLICT
STALE_REFERENCE
VISUAL_CANONICAL_CONFLICT
MIGRATION_PENDING
NO_CONFLICT
BLOCKED_UNVERIFIED
```

`LEGACY_REQUIREMENT_TRACEABILITY`는 과거 요구를 자동 복원하는 절차가 아니라, 현재 승인과 비교하여 material requirement의 유지·대체·폐기 근거를 남기는 절차다.

## 6. 시각 checkpoint

`INTERMEDIATE_VISUAL_CHECKPOINT`와 `NOTION_VISUAL_CHECKPOINT_BEFORE_POC`는 tool-specific page가 아니라 project decision gate다.

시각·UI·UX가 플레이 판단에 영향을 주면 최소 한 화면 흐름을 선택해 다음을 만든다.

```text
Screen Brief
→ representative UX/UI state
→ visual candidate
→ GPT visual + UX review
→ exact Project Notion attach
→ destination readback
→ Screen Interpretation Review
→ user approval / rejection
```

상태:

- `MISSING_CANON`
- `DRAFT_VISUAL`
- `VISUAL_CANONICAL_CONFLICT`
- `TECHNICAL_REVIEW_PROPOSAL`
- `PROJECT_ASSET_APPROVED`
- `APPLIED_AND_RUNTIME_VERIFIED`

사용자 Decision 없이는 `DRAFT_VISUAL`을 승인 asset으로 승격하지 않는다. 시각 후보는 **최종 게임 리소스**나 **Godot 구현 완료**를 뜻하지 않는다.

`APPROVED_VISUALS_FEED_POC`: 승인된 이미지·UI가 PoC 판단 근거라면 해당 이미지 또는 provenance가 유지된 implementation derivative를 PoC에 사용한다.

## 7. OPTIONAL_CODEX_HANDOFF

Codex는 `CODEX_OPTIONAL_SUB_EXECUTOR`다.

다음 경우만 사용한다.

- multi-file repository implementation.
- Godot Scene/Resource/GDScript mutation.
- build/runtime bug reproduction.
- GPT가 승인 contract는 확정했지만 current session에 실행 권위가 없음.
- user explicitly asks for Codex implementation/review.

필요할 때 GPT는 fresh PowerShell용 one-copy/paste launcher + complete contract를 제공한다. Codex는 pasted prompt만 믿지 않고 GitHub/current project files를 다시 읽고, 접근 가능한 경우 exact Project Notion도 확인한다.

## 8. CANONICAL_UPDATE_AND_IMPLEMENTATION

승인된 Decision은 repository structured owner와 필요한 Notion human-facing surface에 반영한다.

```text
NOTION_HUMAN_FACING_CANON
↕ SYNC_BEFORE_IMPLEMENTATION
REPOSITORY_STRUCTURED_CANON
→ actual implementation
→ REPOSITORY_RUNTIME_TRUTH
```

Notion 변경이 code/data/Scene/Resource 의미를 바꾸면 repository structured owner를 먼저 동기화한다. implementation-bound image는 provenance/version, repository asset path, runtime consumption evidence를 갖는다.

## 9. SOURCE_CONSUMER_PROPAGATION_AUDIT

변경 후 다음을 다시 본다.

- canonical source.
- exact Project Notion surface.
- active Skill/router/template.
- code/data/Scene/Resource/asset consumer.
- tests / runtime evidence.
- reference freshness.
- retired surface reference.

고유 material이 없는 retired HTML/local/Sheet consumer는 제거한다.

## 10. VALIDATION

```text
static / schema
→ focused tests
→ runtime / render / build when applicable
→ visual / accessibility / performance when applicable
→ regression
→ adversarial review
```

`NOT_RUN`, `BLOCKED_UNVERIFIED`, `DEFERRED_NOT_CONNECTED`는 PASS가 아니다.

## 11. MERGE_AND_SYNC

구현 PR이 main에 병합된 **뒤에만** merged GitHub main SHA와 실제 구현을 다시 읽는다.

```text
exact-head required checks
→ unresolved thread 0
→ P0/P1 0
→ merge
→ GitHub main readback
→ exact Project Notion destination readback
→ Decision / version / implementation status reconciliation
```

`MERGE_AND_SYNC`의 정상 target은 repository + Notion이다. Google Sheets는 active sync destination이 아니다. legacy Sheet에서 고유 material migration이 현재 승인 범위에 포함될 때만 `GOOGLE_SHEETS_MIGRATE_THEN_REMOVE`를 실행하고 destination readback 뒤 Sheet active reference를 제거한다.

## 12. 완료 보고

단순 `완료/테스트 통과`가 아니라 다음을 알려준다.

- 이 slice/part의 역할.
- 핵심 규칙.
- 핵심 Skill·Mode.
- 핵심 모듈과 연결.
- 변경 전 / 변경 후.
- 유지·개선·흡수·제거.
- player/user 효과.
- long-term effect / trade-off / revisit conditions.
- actual test/runtime/visual/Notion readback.
- PR/merge/main SHA.
- unverified / remaining risks / rollback.

`REQUIRED_WORK_REMAINING: 0`은 승인된 필수 criterion이 실제로 닫힌 경우에만 쓴다.
