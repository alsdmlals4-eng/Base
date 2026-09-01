# Work 프로젝트 시작 정본 확인·선교정 체크리스트

> 이 파일은 프로젝트 사실을 새로 소유하는 두 번째 정본이 아니다. 현재 Base·Project repository owner를 찾아 읽고, 작업 시작 상태를 검증하며, 누락·충돌을 먼저 교정하는 **project-specific 실행 receipt의 형식과 Gate**를 정의한다.

```text
PROJECT_START_CANON_CHECKLIST
STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST
PROJECT_START_CANON_CHECKLIST_REQUIRED
CORRECTION_BEFORE_PRODUCTION
NO_NEW_SLICE_WORK_BEFORE_STARTUP_CORRECTION_OR_EXPLICIT_DEFER
CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON
CORE_FUN_AND_SYSTEM_ALIGNMENT_REQUIRED
SWOT_IS_CURRENT_EVIDENCE_BASED_NOT_GENERIC_MARKETING
REMAINING_WORK_AND_ORDER_DERIVED_FROM_CURRENT_CANON
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
FRESH_READ_BEFORE_PROJECT_WORK_REQUIRED
GENRE_WORLD_VISUAL_BENCHMARK_RECEIPT_REQUIRED
MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT
BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED
LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED
ACTUAL_IMPLEMENTATION_EVIDENCE_NO_SPECULATION
REUSE_VALID_RECEIPT_UNTIL_MATERIAL_DRIFT
STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED
REPOSITORY_PRIMARY_CANON
NO_NEW_NOTION_WRITE_BY_DEFAULT
```

## 1. 목적

새 Work·새 채팅·작업 재개에서 바로 새 기획이나 제작으로 들어가지 않는다.

```text
안전한 read-only authority bootstrap와 Git remote refresh
→ current Project repository exact SHA·actual implementation·open workstream 확인
→ 현재 장르·하위 장르·세계관/setting tone·시각/구도 anchor와 실제 소비처 확인
→ task-appropriate benchmark·역공학을 원출처와 evidence status로 확인하고 `ADOPT / ADAPT / REJECT` 판정
→ 이번 scope의 context·설정·entrypoint·문서·생성물을 hygiene 분류하고 active owner 혼동을 선교정
→ 핵심 재미·핵심 시스템·SWOT·남은 작업·작업순서 체크리스트 작성
→ 정본 상태 분류
→ 현재 승인 범위의 누락·충돌·stale 상태 선교정
→ repository Decision/spec/data/asset manifest/handoff destination readback
→ 필요 Gate에서 source-SHA-bound Human GDD PDF freshness 확인
→ legacy Notion/Sheet 고유 자료가 있을 때만 migration receipt 확인
→ 체크리스트 재평가
→ READY_AFTER_CORRECTION
→ 새 기획·제작·Codex 구현
```

이 순서는 안전한 `fetch`, metadata read, open PR inventory 같은 read-only bootstrap을 막지 않는다. 아직 정본 확인이 끝나지 않았다는 이유로 오래된 local state에서 작업하라는 뜻도 아니다.

## 2. 실행 시점

다음에는 이 Gate를 실행한다.

- 새 Work 또는 새 채팅의 첫 material 프로젝트 작업
- handoff·context gap 이후 작업 재개
- Goal·scope·authority·핵심 Decision이 material하게 바뀐 경우
- repository canon↔actual implementation drift가 발견된 경우
- legacy migration source와 repository receipt가 충돌한 경우
- 새 test/runtime/player/market evidence가 기존 상태를 바꾼 경우
- major closeout 또는 다음 Playable Slice 진입 전

같은 Stage 안에서 최근 receipt가 유효하고 source identity·scope·material evidence가 바뀌지 않았다면 전체 감사를 매 응답마다 반복하지 않는다. 필요한 owner와 consumer만 targeted recheck한다.

## 3. 필수 source와 권위

현재 owner를 과거 경로로 추측하지 않는다. 다음을 fresh-read한다.

```text
current user instruction
→ Base latest completed main / root AGENTS / current routing owners
→ Project default branch / exact SHA / AGENTS / START_HERE / Active Context / confirmed decisions
→ AI production spec / current handoff / ASSET_MANIFEST
→ actual code·data·Scene·Resource·asset·test·runtime evidence
→ open/draft/ready PR and protected other workstreams
→ 필요하면 source-SHA-bound Human GDD PDF
→ actual migration scope이면 legacy Notion/Sheet unique source와 repository receipt
```

material source를 읽지 못하면 snippet·Memory·과거 대화로 대체하지 않는다.

```text
REQUIRED_SOURCE_UNREADABLE
→ BLOCKED_UNVERIFIED
```

Notion을 조회하지 않았다는 이유만으로 block하지 않는다. 고유 unmigrated 자료가 존재한다는 evidence가 있을 때만 해당 migration task를 계산한다.

## 4. 프로젝트 시작 receipt

```yaml
PROJECT_START_CANON_CHECKLIST:
  identity_and_sources:
    exact_project_identity:
    repository:
    exact_base_main:
    exact_project_default_branch_and_sha:
    project_entrypoints: []
    current_decision_and_spec_locators: []
    asset_manifest:
    actual_implementation_evidence:
    source_sha_bound_human_pdf:
    legacy_migration_sources: []
    current_task_branch_or_connector_ref:
    git_sync_evidence:
    open_workstreams_and_prs:
    observed_at:

  authority_reconciliation:
    classification: CURRENT / HISTORICAL / SUPERSEDED / CONFLICT / UNKNOWN_UNVERIFIED
    current: []
    historical: []
    superseded: []
    conflict: []
    unknown_unverified: []

  project_direction:
    project_goal:
    genre_and_subgenre:
    world_and_setting_tone:
    visual_style_and_composition_anchor:
    benchmark_decisions:
      - source_and_evidence:
        observed_pattern:
        project_fit_and_difference:
        decision: ADOPT | ADAPT | REJECT | NOT_APPLICABLE
        owner_or_consumer:
    benchmark_preflight_state: PASS | REUSED_EVIDENCE | NOT_APPLICABLE | BLOCKED_UNVERIFIED
    benchmark_preflight_scope:
    benchmark_preflight_reason_not_applicable:
    player_promise:
    pointed_fun:
    core_loop:
    session_loop:
    progression_or_meta_loop:
    core_systems: []
    supporting_systems: []
    meaningful_choices: []
    reward_and_failure_learning:
    emotional_target:
    first_session_memory:
    sales_points: []
    protected_strengths: []

  swot:
    strengths: []
    weaknesses: []
    opportunities: []
    threats: []
    evidence_and_owner: []
    evidence_status: VERIFIED | PARTIAL | NOT_RUN | NOT_APPLICABLE | BLOCKED_UNVERIFIED

  execution_state:
    current_stage:
    roadmap_or_milestones:
    accepted_frontier:
    active_playable_slice:
    next_playable_slice_candidate:
    actual_implementation_state:
    implementation_and_test_state:
    visual_audio_asset_state:
    blockers_and_dependencies: []
    protected_scope: []

  remaining_and_order:
    remaining_required_work: []
    work_order:
      - priority:
        status: READY | BLOCKED | USER_DECISION_REQUIRED | DEFERRED | DONE
        task:
        why_now:
        dependency:
        player_value:
        risk_or_blocker:
        owner:
        acceptance:
        verification:
        fallback_or_defer:

  correction:
    stale_conflict_missing_canon: []
    corrections_applied: []
    corrections_deferred_with_reason: []
    repository_canon_readback:
    decision_spec_data_readback:
    asset_manifest_readback:
    handoff_readback:
    human_pdf_freshness_readback:

  context_configuration_hygiene:
    scope:
    inventory: []
    classification: ACTIVE_OWNER | COMPATIBILITY | ARCHIVE | OBSOLETE_CANDIDATE | UNKNOWN_UNVERIFIED
    entrypoint_or_token_saving_correction: []
    references_and_consumers_zero_before_removal:
    git_recoverable_removal_and_readback:
    cleanup_result: NO_CHANGE | CORRECTED | REMOVAL_VERIFIED | DEFERRED_UNKNOWN_UNVERIFIED

  legacy_migration:
    notion_unique_canon_count:
    codex_notion_dependency_count:
    active_notion_write_requirement_count:
    repository_receipts: []
    status: NOT_APPLICABLE | IN_PROGRESS | BLOCKED | COMPLETE

  evidence_and_exit:
    human_usability_evidence: NOT_RUN
    player_experience_evidence: NOT_RUN
    deferred_decisions: []
    decision_state: NONE | USER_DECISION_REQUIRED | EXPLICITLY_DEFERRED
    next_safe_action:
    result: READY_AFTER_CORRECTION | BLOCKED_UNVERIFIED
```

### 4.1 필수 benchmark·역공학 receipt

`GENRE_WORLD_VISUAL_BENCHMARK_RECEIPT_REQUIRED` · `MANDATORY_BENCHMARK_REVERSE_ENGINEERING_PREFLIGHT` · `BENCHMARK_PREFLIGHT_BEFORE_WORK_REQUIRED`

모든 L1+ 프로젝트 작업은 fresh-read 뒤 exact repository revision의 같은 책임·실제 consumer를 먼저 비교한다. 기획·시스템·서사·Art Direction·UI/UX·에셋처럼 플레이어가 보는 의미를 material하게 바꾸는 경우에는 `genre_and_subgenre`, `world_and_setting_tone`, `visual_style_and_composition_anchor`도 current owner와 actual consumer에서 복원한다. benchmark는 원출처·관찰 사실·현재 프로젝트와의 차이·`ADOPT / ADAPT / REJECT`만 남기며, 다른 작품의 설정·그림체·구도·고정 버튼 목록을 복사하거나 evidence 없는 추측으로 채우지 않는다. `benchmark_preflight_state`가 `PASS` 또는 freshness가 유지된 `REUSED_EVIDENCE`가 아니면 새 설계·제작·구현으로 들어가지 않는다.

L0 기계 수정이나 이 형식의 판단이 전혀 관련 없는 작업은 `NOT_APPLICABLE`과 이유를 남긴다. 현재 source가 읽히지 않으면 기억·대화·파일명으로 채우지 않고 `BLOCKED_UNVERIFIED`로 둔다.

### 4.1.1 legacy context·configuration hygiene receipt

`LEGACY_CONTEXT_CONFIGURATION_HYGIENE_REQUIRED`

작업 시작 범위 안에서만 context·설정·entrypoint·문서·생성물을 `ACTIVE_OWNER | COMPATIBILITY | ARCHIVE | OBSOLETE_CANDIDATE | UNKNOWN_UNVERIFIED`로 분류한다. `NO_BROAD_SWEEP_WITHOUT_SCOPE`: token 절감 명목의 전체 저장소 대량 재작성은 하지 않는다. `NO_DELETION_BY_AGE_OR_NAME`: 오래된 날짜·구형 이름·파일명은 삭제 근거가 아니다. `OBSOLETE_CANDIDATE`는 `REFERENCES_AND_CONSUMERS_ZERO_BEFORE_REMOVAL`과 `GIT_RECOVERABLE_REMOVAL_AND_READBACK`을 만족한 경우에만 실제 제거하며, 그렇지 않으면 `DEFERRED_UNKNOWN_UNVERIFIED`로 보존하고 active entrypoint·문서 지도에서의 오인만 먼저 교정한다.

## 4.2 사용자에게 보여줄 시작 보고

`STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED`

첫 material 작업에서는 내부 YAML만 만들고 숨기지 말고, 사용자에게 다음을 짧은 체크리스트로 보여준다. 이미 유효한 receipt를 재사용할 때는 변경된 항목만 보고한다.

```text
repository identity와 exact SHA / current stage
→ 핵심 재미·player promise·핵심 시스템
→ SWOT 핵심 변화와 evidence ceiling
→ 실제 구현·test·Visual/Audio 상태
→ 발견한 stale/conflict/missing canon
→ 먼저 교정한 항목과 repository destination readback
→ PDF freshness가 필요한 Gate인지
→ legacy migration counter와 blocker가 있는지
→ 남은 작업과 우선 작업순서
→ 보류된 사용자 결정
→ 다음 안전 작업
```

이 보고는 기획서를 다시 쓰는 절차가 아니다. 작업 시작 시 무엇을 믿고, 무엇을 먼저 고쳤으며, 왜 이 순서로 진행하는지를 확인하는 실행 요약이다.

## 5. 핵심 재미·핵심 시스템 확인

`pointed_fun`은 기능 목록의 요약이 아니다.

```text
player promise
→ 대표 행동
→ 의미 있는 선택·고민
→ 관찰 가능한 결과
→ 보상 또는 실패 학습
→ 감정·기억·다음 동기
```

각 `core_systems`는 최소 다음을 가져야 한다.

```text
핵심 재미에 대한 역할
→ current repository owner
→ actual implementation 또는 planned consumer
→ 현재 evidence
→ 남은 gap
```

지원 시스템이 핵심 재미를 가리거나 유지비만 늘리면 축소·defer·cut 후보로 올린다. 핵심 재미·핵심 시스템·주요 UX·경제·서사·Art Direction의 제품 의미를 바꾸는 교정은 `USER_DECISION_REQUIRED`다.

## 6. 증거 기반 SWOT

`SWOT_IS_CURRENT_EVIDENCE_BASED_NOT_GENERIC_MARKETING`

SWOT은 홍보 문구를 채우는 표가 아니라 현재 의사결정의 위험·기회를 드러내는 시점별 분석이다.

- `strengths`: current canon과 actual test/runtime/player evidence로 확인된 내부 강점
- `weaknesses`: 구현·UX·콘텐츠·생산·유지보수·증거의 내부 약점
- `opportunities`: 프로젝트 정체성과 맞는 외부 시장·플랫폼·기술·플레이어 요구의 기회
- `threats`: 경쟁 혼잡, scope/콘텐츠 비용, 기술·권리·플랫폼·시장 위험

```yaml
SWOT_ITEM:
  statement:
  class: STRENGTH | WEAKNESS | OPPORTUNITY | THREAT
  evidence_and_owner:
  observed_at:
  project_applicability:
  confidence:
  disposition: PROTECT | IMPROVE | TEST | MITIGATE | MONITOR | REJECT
```

외부 기회·위협이 current material decision에 영향을 주면 `MARKET_SUCCESS_FAILURE_COMPARISON`을 실행한다. L0 기계 수정처럼 시장조사가 불필요한 작업에서는 `NOT_RUN` 또는 `NOT_APPLICABLE`과 이유를 기록한다.

SWOT은 자동 scope 확장 권한이 아니며, 재미·독창성·시장성을 실제 player/market evidence보다 높게 주장하지 않는다.

## 7. 남은 작업과 작업순서

`remaining_required_work`는 전체 희망 목록이 아니라 현재 Goal과 승인된 Playable Slice를 완료하는 데 필요한 gap이다. 활성 Slice가 아직 없으면 current stage·roadmap_or_milestones·accepted_frontier·blocker를 대조해 `next_playable_slice_candidate`를 복원한다.

```text
confirmed requirement
→ repository owner
→ current canon/implementation
→ consumer
→ test/readback/runtime/play evidence
→ missing gap
→ remaining work
```

`work_order`는 다음 우선순위로 정렬한다.

1. authority conflict·필수 blocker·dependency 해소
2. 핵심 재미와 player value를 직접 살리는 작업
3. first-session 이해·대표 Slice 실행에 필요한 작업
4. runtime consumer·test·build·readback 누락
5. 재작업·권리·보안·save/schema 위험 완화
6. polish와 후속 확장

각 작업에는 `priority`, `status`, `why_now`, `dependency`, `player_value`, `risk_or_blocker`, `owner`, `acceptance`, `verification`, `fallback_or_defer`가 있어야 한다. 문서량·commit 수가 아니라 playable progress를 기준으로 순서를 정한다.

## 8. 정본 선교정

`STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST`

새 기획·새 에셋 production·Codex mutation 전에 다음을 분류한다.

```text
CURRENT / HISTORICAL / SUPERSEDED / CONFLICT / UNKNOWN_UNVERIFIED
```

현재 승인 범위에서 자동 교정 가능한 것:

- stale stage·status·remaining-work·work-order
- 승인된 Decision이 repository owner에 누락된 상태
- 동일 의미의 중복·서로 모순되는 current 문구
- owner·consumer·test·readback locator 누락
- completed/merged 사실과 맞지 않는 handoff·spec·manifest 상태
- 보호된 다른 workstream을 침범하지 않는 bounded canon sync

교정 흐름:

```text
validated finding
→ smallest safe correction
→ repository Decision/spec/data/manifest/handoff
→ exact destination readback
→ 필요한 경우 source-SHA-bound Human GDD PDF 재생성
→ checklist recalculation
```

legacy Notion/Sheet에서 고유 자료가 발견되면 원본을 파괴하지 않고 provenance와 source relation을 보존해 repository에 이관한다. 신규 Notion 페이지·DB·중간 sync를 만들지 않는다.

다음은 `USER_DECISION_REQUIRED`로 보류한다.

- core fun·core identity 변경
- core system의 제품 의미 변경
- 주요 UX·경제·보상·서사·Art Direction 변경
- 승인 범위 확대
- 파괴적 migration/delete
- 새 비용·계정·보안 권한·공개 배포

독립적인 안전 교정은 계속할 수 있다. unresolved conflict가 현재 Slice 의미·acceptance·consumer를 바꾸면 `NO_NEW_SLICE_WORK_BEFORE_STARTUP_CORRECTION_OR_EXPLICIT_DEFER`를 적용한다.

## 9. 통과 조건

다음을 모두 만족해야 `READY_AFTER_CORRECTION`이다.

```text
exact project/repository/source SHA known
AND core fun / player promise / core loop aligned
AND core/supporting systems and consumers mapped
AND SWOT evidence ceiling explicit
AND current stage / roadmap / accepted frontier / blockers known
AND active Slice or next playable Slice candidate identified
AND remaining work and work order recalculated
AND approved-scope stale/conflict/missing canon corrected
AND repository destination readback complete when changed
AND approved runtime asset path/SHA/manifest recoverable when applicable
AND PDF source SHA current when a human review Gate requires it
AND legacy migration counters explicit when applicable
AND protected other workstreams preserved
AND unresolved product-meaning decisions explicitly deferred
```

체크리스트가 존재한다는 사실만으로 통과하지 않는다. write가 필요 없으면 `NO_CORRECTION_NEEDED`와 근거를 기록한다.

## 10. 이전 지시문 비퇴행 연결

`REVISION_NON_REGRESSION_GATE`

이 체크리스트는 이전 v4.8 r5.4·v4.9의 전체 계약을 대체하지 않고 다음 책임을 current bundle에 연결한다.

| 책임 | 처리 |
|---|---|
| Authority Recovery / Fresh-read / Entry Reconciliation | PRESERVED · repository exact SHA 기반 |
| Whole Project Audit / Requirement Traceability | PRESERVED |
| core fun / player promise / Project Direction | IMPROVED · 작업 시작 필수 확인 |
| core systems / meaningful choice / reward-failure learning | IMPROVED · owner·consumer·evidence 연결 |
| SWOT | PRESERVED · evidence-based decision snapshot |
| remaining required work / completion rescan | IMPROVED · 시작 시 재계산 |
| dependency·player-value work order | PRESERVED |
| Reuse First / benchmark / 3 alternatives / long-term fit | PRESERVED |
| Visual Delete Test / actual consumer / image approval | IMPROVED · repository path/SHA/manifest |
| 사람용 전체 시각 점검 | IMPROVED · exact source SHA의 derived PDF |
| Work↔Codex role / engine adapter / Implementation Ready | IMPROVED · exact repository SHA rehydrate |
| automatic safe Git fetch·pull·push / PR·merge readback | PRESERVED |
| project-scoped Godot·computer operation | PRESERVED |
| user-downloadable build / machine QA / Human evidence ceiling | PRESERVED |
| failure recovery / Incident-Solution-Lesson | PRESERVED |
| minimum 5 full adversarial loops / Completion Candidate | PRESERVED |
| Notion human canon / upload / dual sync | INTENTIONALLY_SUPERSEDED · legacy read-only migration only |

세부 알고리즘은 다음 current owner를 따른다.

```text
docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md
docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

이 파일은 `CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON`을 유지한다. durable 사실과 결정은 project repository의 분야별 structured/runtime canon이 소유하며, 사람용 PDF와 이 receipt가 그 사실을 덮어쓰지 않는다.

## 11. Retired compatibility vocabulary

```text
GitHub structured canon = repository structured/runtime canon
Notion human canon = retired legacy human surface
GitHub structured canon / Notion human canon destination readback = retired dual-write route
```

위 문자열은 역사·구형 test 탐색용이며 active completion condition이 아니다.

## 12. 프로젝트 작업 칸반·체크리스트 연결

`PROJECT_WORK_KANBAN_CHECKLIST_REQUIRED`

프로젝트 시작 receipt의 `remaining_and_order`를 계산한 뒤, 같은 Goal·Playable Slice의 기존 Issue·카드·PR을 먼저 찾고 현재 작업 목록을 `templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md` 형식으로 연결한다.

```text
REUSE_EXISTING_WORK_ITEM_BEFORE_CREATE
NO_ISSUE_EXPLOSION
CHECKLIST_IS_DERIVED_OPERATIONAL_VIEW_NOT_CANON
PROJECTS_DERIVED_VIEW_NOT_CANON
NO_PROJECTS_WRITE_CAPABILITY_IS_NOT_BLOCKER
```

작업 목록은 프로젝트 사실의 새 정본이 아니다. 각 항목은 current repository owner, actual consumer, Acceptance Criteria와 요구 evidence를 가리키며, 충돌하면 owner·실제 구현·검증을 다시 읽고 카드 상태를 교정한다.

### 12.1 Receipt extension

```yaml
PROJECT_START_CANON_CHECKLIST:
  project_work_kanban:
    goal_or_slice_issue_ref:
    work_item_refs: []
    active_work_item_ref:
    board_or_view_ref:
    board_configuration_status: NOT_APPLICABLE | VERIFIED | UNVERIFIED_PROJECTS_CONFIGURATION
    sub_issue_relation_status: NOT_APPLICABLE | VERIFIED | UNVERIFIED_SUB_ISSUE_RELATION
    progress_summary:
      completed_items:
      applicable_items:
      display: NO_APPLICABLE_CHECKLIST | "completed_items / applicable_items"
    blocked_or_decision_items: []
    next_action:
```

GitHub Projects 또는 sub-issue 관계를 실제로 생성·조회·readback할 수 없으면 Issue 본문과 Markdown 카드 참조를 유지하고 각각 `UNVERIFIED_PROJECTS_CONFIGURATION`, `UNVERIFIED_SUB_ISSUE_RELATION`을 기록한다. 설정되지 않은 board·automation·relation을 추측하지 않으며, 해당 capability 부재만으로 project work를 전역 차단하지 않는다.

### 12.2 Materialization order

```text
active_playable_slice 또는 next_playable_slice_candidate
→ 같은 Goal의 기존 Issue·PR·work item 검색
→ remaining_required_work와 work_order fresh-read
→ 별도 owner/PR·독립 blocker·dependency·Acceptance·verification 여부 판정
→ 기존 work item 재사용
→ 필요한 독립 작업만 새 Issue 또는 카드 생성
→ 작은 순차 단계는 부모 카드 내부 체크리스트로 유지
→ READY / IN_PROGRESS / VERIFY_REVIEW / BLOCKED_DECISION / DONE
→ evidence와 repository readback에 따라 진행률·다음 행동 갱신
```

`BLOCKED_DECISION`은 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, `DEFERRED`를 한눈에 보는 파생 View다. 실제 work item 상태는 원래 분류를 유지한다.

### 12.3 GPT PM 갱신 책임

GPT는 현재 승인 범위에서 다음을 연속 수행한다.

1. dependency와 player/user value를 기준으로 `READY` 순서를 정한다.
2. 기본 WIP에 따라 `IN_PROGRESS` 하나와 `VERIFY_REVIEW` 하나를 넘지 않게 한다.
3. 작업·검증·readback 뒤 PASS·FAIL·blocker와 exact evidence를 카드에 반영한다.
4. `[x]`는 evidence-backed `PASS`에만 사용하고 `NOT_APPLICABLE`은 이유와 함께 진행률 분모에서 제외한다.
5. blocker가 생기면 해당 작업만 defer하고 독립 `READY` 작업을 계속한다.
6. 완료 후보에서 remaining-work recalculation, implementation correction rescan과 adversarial review를 실행한다.
7. 사용자에게는 전체 진행률, 현재 작업, 차단·결정 항목, 다음 안전 작업을 요약한다.

카드나 Issue 작성 자체는 구현·runtime·UX·Human/Player·사용자 승인 PASS가 아니다. 모든 기존 프로젝트에 빈 항목을 일괄 생성하지 않고 새 material work, 작업 재개, Goal 변경, major closeout 또는 다음 Slice 진입 시 필요한 범위에서만 적용한다.
