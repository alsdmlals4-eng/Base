# Work 프로젝트 시작 정본 확인·선교정 체크리스트

> 이 파일은 프로젝트 사실을 새로 소유하는 두 번째 정본이 아니다. 현재 Base·Project owner를 찾아 읽고, 작업 시작 상태를 검증하며, 누락·충돌을 먼저 교정하는 **project-specific 실행 receipt의 형식과 Gate**를 정의한다.

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
REUSE_VALID_RECEIPT_UNTIL_MATERIAL_DRIFT
STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED
```

## 1. 목적

새 Work·새 채팅·작업 재개에서 바로 새 기획이나 제작으로 들어가지 않는다.

```text
안전한 read-only authority bootstrap와 Git remote refresh
→ 현재 Project GitHub·Notion·actual implementation·open workstream 확인
→ 핵심 재미·핵심 시스템·SWOT·남은 작업·작업순서 체크리스트 작성
→ 정본 상태 분류
→ 현재 승인 범위의 누락·충돌·stale 상태 선교정
→ GitHub structured canon / Notion human canon destination readback
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
- GitHub↔Notion↔actual implementation drift가 발견된 경우
- 새 test/runtime/player/market evidence가 기존 상태를 바꾼 경우
- major closeout 또는 다음 Playable Slice 진입 전

같은 Stage 안에서 최근 receipt가 유효하고 source identity·scope·material evidence가 바뀌지 않았다면 전체 감사를 매 응답마다 반복하지 않는다. 필요한 owner와 consumer만 targeted recheck한다.

## 3. 필수 source와 권위

현재 owner를 과거 경로로 추측하지 않는다. 다음을 fresh-read한다.

```text
current user instruction
→ Base latest completed main / root AGENTS / current routing owners
→ Project default branch / AGENTS / Active Context / confirmed decisions
→ Project Notion Home / relevant Domain / Flow / Visual / Production
→ actual code·data·Scene·Resource·asset·test·runtime evidence
→ open/draft/ready PR and protected other workstreams
```

material source를 읽지 못하면 snippet·Memory·과거 대화로 대체하지 않는다.

```text
REQUIRED_SOURCE_UNREADABLE
→ BLOCKED_UNVERIFIED
```

## 4. 프로젝트 시작 receipt

```yaml
PROJECT_START_CANON_CHECKLIST:
  identity_and_sources:
    exact_project_identity:
    exact_base_main:
    exact_project_default_branch_and_sha:
    exact_notion_home_and_active_domains:
    actual_implementation_evidence:
    source_locators: []
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
    github_structured_canon_readback:
    notion_human_canon_readback:

  evidence_and_exit:
    human_usability_evidence: NOT_RUN
    player_experience_evidence: NOT_RUN
    deferred_decisions: []
    decision_state: NONE | USER_DECISION_REQUIRED | EXPLICITLY_DEFERRED
    next_safe_action:
    result: READY_AFTER_CORRECTION | BLOCKED_UNVERIFIED
```

## 4.1 사용자에게 보여줄 시작 보고

`STARTUP_CANON_CHECKLIST_USER_REPORT_REQUIRED`

첫 material 작업에서는 내부 YAML만 만들고 숨기지 말고, 사용자에게 다음을 짧은 체크리스트로 보여준다. 이미 유효한 receipt를 재사용할 때는 변경된 항목만 보고한다.

```text
정본 identity와 current stage
→ 핵심 재미·player promise·핵심 시스템
→ SWOT 핵심 변화와 evidence ceiling
→ 실제 구현·test·Visual/Audio 상태
→ 발견한 stale/conflict/missing canon
→ 먼저 교정한 항목과 destination readback
→ 남은 작업과 우선 작업순서
→ 보류된 사용자 결정
→ 다음 안전 작업
```

이 보고는 기획서를 다시 쓰는 절차가 아니다. 작업 시작 시 무엇을 믿고, 무엇을 먼저 고쳤으며, 왜 이 순서로 진행하는지를 확인하는 실행 요약이다.

## 5. 핵심 재미·핵심 시스템 확인

`pointed_fun`은 기능 목록의 요약이 아니다. 다음 연결을 확인한다.

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
→ current canon owner
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

각 항목은 가능한 범위에서 다음을 기록한다.

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

외부 기회·위협이 현재 material decision에 영향을 주면 `MARKET_SUCCESS_FAILURE_COMPARISON`을 실행하고 공식·현업·성공·실패/혼합·player report를 구분한다. L0 기계 수정처럼 시장조사가 불필요한 작업에서는 억지 SWOT 조사를 만들지 말고 `NOT_RUN` 또는 `NOT_APPLICABLE`과 이유를 기록한다.

SWOT은 자동 scope 확장 권한이 아니며, 재미·독창성·시장성을 실제 player/market evidence보다 높게 주장하지 않는다.

## 7. 남은 작업과 작업순서

`remaining_required_work`는 전체 희망 목록이 아니라 현재 Goal과 승인된 Playable Slice를 완료하는 데 필요한 gap이다. 활성 Slice가 아직 없으면 current stage·roadmap_or_milestones·accepted_frontier·blocker를 대조해 `next_playable_slice_candidate`를 복원한 뒤 그 후보의 gap만 우선 계산한다.

먼저 다음을 재계산한다.

```text
confirmed requirement
→ owner
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

서로 독립적인 작업은 병렬화할 수 있지만, 선행 Decision·consumer·asset·schema가 없는 downstream 구현을 먼저 시작하지 않는다.

## 8. 정본 선교정

`STARTUP_CANON_RECONCILIATION_AND_CORRECTION_FIRST`

새 기획·새 에셋 production·Codex mutation 전에 다음을 분류한다.

```text
CURRENT / HISTORICAL / SUPERSEDED / CONFLICT / UNKNOWN_UNVERIFIED
```

현재 승인 범위에서 자동 교정 가능한 것:

- stale stage·status·remaining-work·work-order
- 승인된 Decision이 current owner에 누락된 상태
- 동일 의미의 중복·서로 모순되는 current 문구
- owner·consumer·test·readback locator 누락
- completed/merged 사실과 맞지 않는 handoff·Notion 상태
- 보호된 다른 workstream을 침범하지 않는 bounded canon sync

교정 흐름:

```text
validated finding
→ smallest safe correction
→ GitHub structured canon
→ Notion human canon
→ exact destination readback
→ checklist recalculation
```

기존 검증된 Notion IA는 wholesale remigration하지 않는다. 고유 프로젝트 내용·승인 Visual·Decision을 보존하고 검증된 결함만 bounded correction한다.

다음은 해당 항목을 `USER_DECISION_REQUIRED`로 보류한다.

- core fun·core identity 변경
- core system의 제품 의미 변경
- 주요 UX·경제·보상·서사·Art Direction 변경
- 승인 범위 확대
- 파괴적 migration/delete
- 새 비용·계정·보안 권한·공개 배포

독립적인 안전 교정은 계속할 수 있다. 그러나 unresolved conflict가 현재 Slice 의미·acceptance·consumer를 바꾸면 `NO_NEW_SLICE_WORK_BEFORE_STARTUP_CORRECTION_OR_EXPLICIT_DEFER`를 적용한다.

## 9. 통과 조건

다음을 모두 만족해야 `READY_AFTER_CORRECTION`이다.

```text
exact project/source identity known
AND core fun / player promise / core loop aligned
AND core/supporting systems and consumers mapped
AND SWOT evidence ceiling explicit
AND current stage / roadmap / accepted frontier / blockers known
AND active Slice or next playable Slice candidate identified
AND remaining work and work order recalculated
AND approved-scope stale/conflict/missing canon corrected
AND GitHub structured canon destination readback complete when changed
AND Notion human canon destination readback complete when changed
AND protected other workstreams preserved
AND unresolved product-meaning decisions explicitly deferred
```

체크리스트가 존재한다는 사실만으로 통과하지 않는다. write가 필요 없으면 `NO_CORRECTION_NEEDED`와 근거를 기록한다.

## 10. 이전 지시문 비퇴행 연결

`REVISION_NON_REGRESSION_GATE`

이 체크리스트는 이전 v4.8 r5.4·v4.9의 전체 계약을 대체하지 않고 다음 책임을 current bundle에 연결한다.

| 책임 | 처리 |
|---|---|
| Authority Recovery / Fresh-read / Entry Reconciliation | PRESERVED · 시작 receipt에서 가시화 |
| Whole Project Audit / Requirement Traceability | PRESERVED |
| core fun / player promise / Project Direction | IMPROVED · 작업 시작 필수 확인 |
| core systems / meaningful choice / reward-failure learning | IMPROVED · owner·consumer·evidence 연결 |
| SWOT | NEW · evidence-based decision snapshot |
| remaining required work / completion rescan | IMPROVED · 시작 시 재계산 |
| dependency·player-value work order | NEW/IMPROVED |
| Reuse First / benchmark / 3 alternatives / long-term fit | PRESERVED · current v4.9 owner 사용 |
| Visual Delete Test / actual consumer / image approval / Notion upload | PRESERVED |
| Work↔Codex role / engine adapter / Implementation Ready | PRESERVED |
| automatic safe Git fetch·pull·push / PR·merge readback | PRESERVED |
| project-scoped Godot·computer·browser operation | PRESERVED |
| user-downloadable build / machine QA / Human evidence ceiling | PRESERVED |
| failure recovery / Incident-Solution-Lesson | PRESERVED |
| minimum 5 full adversarial loops / Completion Candidate | PRESERVED |

세부 알고리즘은 다음 current owner를 따른다.

```text
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

이 파일은 `CHECKLIST_IS_ROUTING_RECEIPT_NOT_SECOND_CANON`을 유지한다. durable 사실과 결정은 분야별 GitHub structured canon과 Notion human canon이 소유하며, 이 receipt가 그 사실을 덮어쓰지 않는다.
