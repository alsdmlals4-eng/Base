# 사람용 Blueprint 프로젝트 작업현황 투영 계약

- Contract ID: `HUMAN_BLUEPRINT_PROJECT_PROGRESS_PROJECTION`
- 상태: `ACTIVE_V4_EXTENSION`
- 상위 발행 계약: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
- 작업 상태 계약: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` §14
- 권한 계약: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`
- 템플릿: `templates/project-operations/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_TEMPLATE.md`
- 검증기: `tools/human_blueprint_progress_projection.py`

## 1. 목적과 산출물 경계

```text
BLUEPRINT_IS_SINGLE_HUMAN_PM_SURFACE
NO_SEPARATE_PM_PDF
NO_HTML_DASHBOARD
NO_SECOND_STATUS_CANON
DERIVED_SNAPSHOT_NOT_STATUS_OWNER
REPOSITORY_OWNER_PLUS_PROJECT_WORK_KANBAN
PROJECT_WORK_KANBAN_DIRECT_SOURCE_NO_STATUS_COPY
```

기존 `HUMAN_MASTER_GDD_PDF` 한 파일에서 게임의 목표·시스템·콘텐츠·구현 원리와 현재 프로젝트 작업 상태를 함께 이해하게 한다. 작업현황을 보여 주기 위한 별도 HTML, 별도 PM PDF, 별도 대시보드, 수동 체크 전용 상태 저장소는 만들지 않는다.

PDF의 작업현황 장은 같은 exact revision에서 다음 source를 읽은 파생 snapshot이다.

1. repository의 기획·Decision·구조화 데이터·코드·Scene·Resource·asset·test·evidence owner
2. `PROJECT_AI_PRODUCTION_SPEC.md` 또는 프로젝트 `AGENTS.md`가 지정한 목표·시스템·케이스 owner
3. 기존 root receipt의 `project_work_kanban`
4. 실제 자동 테스트·runtime·visual·play·human evidence

작업 제목·상태·현재 작업·차단·다음 행동은 `project_work_kanban`을 직접 읽는다. projection에 별도 `work_items`, root `active_work_item_ref`, root `next_action`을 복사해 두 번째 상태 표를 만들지 않는다. `work_item_links`는 기존 `WORK_ITEM_ID`를 목표·시스템·케이스에 연결하는 관계만 소유하며 작업 상태를 소유하지 않는다.

Projection JSON은 생성 과정의 transient input이다. 이를 persistent current-status owner로 등록하지 않는다. PDF 체크 표시나 주석만으로 repository 상태를 바꾸지 않고 기존 owner를 수정·검증한 뒤 PDF를 재생성한다.

## 2. Blueprint 필수 시각 모듈

```text
PROJECT_STATUS_DASHBOARD
CURRENT_WORK_AND_NEXT_ACTION
PROJECT_GOAL_MAP
GOAL_STATUS_CARD
SYSTEM_STATUS_CARD
CASE_VERIFICATION_MATRIX
GOAL_SYSTEM_CASE_WORK_TRACEABILITY
```

### 2.1 `PROJECT_STATUS_DASHBOARD`

첫 3분 읽기 범위에서 다음을 보여 준다.

- 프로젝트 핵심 약속과 현재 승인 Goal/Playable Slice
- `source_commit`, `generated_at`, 포함 범위, approval status, evidence ceiling
- 작업 snapshot source·생성 시각·staleness·진행 계산 기준
- 목표 완료/적용 수
- 시스템 완료/적용 수
- 케이스 완료/적용 수
- 필수 작업 완료/적용 수
- 차단 수와 `USER_DECISION_REQUIRED` 수
- 현재 활성 작업과 다음 안전 작업

단일 전체 퍼센트가 위 상태 축을 대체하지 않는다.

### 2.2 `PROJECT_GOAL_MAP`과 `GOAL_STATUS_CARD`

각 `GOAL_ID`는 플레이어 가치, 현재/목표 성숙도, 연결된 `SYSTEM_ID`·`CASE_ID`·`WORK_ITEM_ID`, 다음 행동과 evidence-backed checklist를 가진다.

```text
GOAL_AND_SYSTEM_EVIDENCE_BACKED_CHECKLISTS
```

목표 체크리스트의 각 항목은 `id`, 사람용 문장, 상태, evidence 또는 N/A reason을 가진다. `PASS`에 evidence가 없으면 완료로 세지 않는다. 목표 완료는 다음을 모두 충족해야 한다.

- 목표 성숙도가 목표 성숙도에 도달
- 적용 가능한 목표 체크리스트가 모두 `PASS`
- 연결 필수 시스템 완료
- 연결 적용 케이스 완료
- 연결 필수 작업 `DONE`

### 2.3 `SYSTEM_STATUS_CARD`

각 `SYSTEM_ID`는 다음을 보여 준다.

- 플레이어 가치와 시스템 책임
- canon owner와 actual consumer
- 입력·출력·상태·데이터·UI·asset·저장·실패·rollback 영향
- 기획·데이터·자산·구현·검증의 evidence-backed checklist
- 연결 목표·케이스·작업과 그 작업의 실제 상태
- 현재/목표 성숙도, 연결 blocker, 다음 행동

시스템 완료는 성숙도와 적용 checklist, 연결 적용 케이스, 연결 필수 작업이 모두 완료됐을 때만 계산한다.

### 2.4 `CASE_VERIFICATION_MATRIX`

각 `CASE_ID`는 실제 사용·플레이 상황 하나다. 실제 consumer·위험·실패 비용에 필요한 유형만 선택한다.

```text
NORMAL | BOUNDARY | FAILURE | CONFLICT | INTERRUPTION
RECOVERY | SAVE_LOAD | UI_STATE | ACCESSIBILITY | PERFORMANCE
```

각 케이스는 `SYSTEM_ID`, 관련 `GOAL_ID`, 관련 `WORK_ITEM_ID`, 적용 여부, 현재/목표 성숙도, 필수 evidence, evidence별 실제 결과와 locator, 다음 행동을 가진다.

적용 가능한 케이스는 최소 하나의 필수 evidence level을 선언해야 한다. 빈 필수 evidence 목록으로 `all([]) == true`와 같은 공집합 완료를 만들지 않는다.

### 2.5 `GOAL_SYSTEM_CASE_WORK_TRACEABILITY`

모든 표시 행은 다음 관계를 양방향으로 추적할 수 있어야 한다.

```text
GOAL_ID ↔ SYSTEM_ID ↔ CASE_ID ↔ WORK_ITEM_ID ↔ EVIDENCE
```

`work_item_links`의 ID 집합은 `project_work_kanban.work_items`의 ID 집합과 정확히 같아야 한다. 한쪽에만 존재하는 참조, 사라진 ID, 다른 source revision의 상태를 정상 표시하지 않는다.

## 3. 상태 축

```text
MATURITY_WORK_EVIDENCE_AXES_SEPARATE
```

### 3.1 기획·구현 성숙도

```text
DOCUMENTED
→ CONFIRMED
→ IMPLEMENTED
→ AUTOMATED_TEST_PASS
→ RUNTIME_VERIFIED
→ UX_VERIFIED
→ RELEASE_READY
```

프로젝트가 `IDEA → RESEARCHED → FEASIBLE → SPECIFIED → ASSET_READY → IMPLEMENTED → MACHINE_VERIFIED → RUNTIME_VERIFIED → USER_APPROVED`처럼 더 세분화된 lifecycle을 이미 정본으로 사용하면 해당 owner의 상태를 별도 행으로 보존한다. 서로 다른 lifecycle을 임의로 자동 승격하거나 동의어로 합치지 않는다.

### 3.2 작업 흐름

```text
BACKLOG | READY | IN_PROGRESS | VERIFY_REVIEW | DONE
BLOCKED_UNVERIFIED | USER_DECISION_REQUIRED | DEFERRED
```

기존 `project_work_kanban`이 유일한 작업 상태 source다. 해당 validator의 ID·의존성·WIP·체크리스트·evidence·readback 규칙을 그대로 통과해야 한다.

### 3.3 Evidence와 ceiling

```text
E0_CONTRACT | E1_STATIC | E2_TEST | E3_RUNTIME
E4_VISUAL | E5_PLAY | E6_HUMAN_PLAYTEST
```

허용 결과:

```text
PASS | FAIL | PARTIAL | NOT_RUN | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

```text
EVIDENCE_CEILING_ENFORCED
```

- `evidence_ceiling`은 위 level 중 하나다.
- 필수 evidence 또는 `PASS` evidence가 ceiling보다 높으면 inconsistency다.
- 적용 가능한 케이스의 필수 evidence는 모두 존재하고 `PASS`여야 완료다.
- 자동 테스트 PASS는 runtime, 화면, UX, human/player, 사용자 승인 또는 release PASS가 아니다.

## 4. 진행률·완료 계산

```text
PASS_ONLY_COUNTS_COMPLETE
NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR
DO_NOT_AVERAGE_CHILD_PERCENTAGES
NO_APPLICABLE_CHECKLIST
```

- 작업 완료: `project_work_kanban`의 `DONE`만 센다.
- 목표·시스템 checklist: 적용 가능한 모든 항목이 evidence-backed `PASS`일 때만 완료 조건 하나를 충족한다.
- 케이스 완료: `APPLICABLE`, 목표 성숙도 도달, 비어 있지 않은 필수 evidence 전체 `PASS`일 때만 센다.
- 시스템·목표 완료: 각각의 성숙도·checklist·연결 적용 케이스·연결 필수 작업 조건을 모두 충족해야 한다.
- `NOT_APPLICABLE`은 구체적인 reason이 있을 때만 분모에서 제외한다.
- future scope나 선택적 polish를 몰래 분모에 넣거나, 미완료 항목을 지워 분모를 줄이지 않는다.
- 자식 퍼센트를 평균내지 않고 목표·시스템·케이스·작업 완료 수를 각각 표시한다.
- 적용 항목이 0이면 `100%` 또는 `0 / 0`이 아니라 `NO_APPLICABLE_CHECKLIST`를 표시한다.

## 5. Source·시간·최신성·안전

```text
SOURCE_SHA_MATCH_REQUIRED
STALE_SNAPSHOT_VISIBLE
PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON
```

Projection/PDF metadata는 다음을 가진다.

```yaml
source_commit:
generated_at:
work_status_snapshot_source:
work_status_snapshot_generated_at:
work_status_snapshot_staleness: CURRENT_AT_SOURCE_SHA | STALE_SNAPSHOT | UNVERIFIED
progress_calculation_basis: INDEPENDENT_GOAL_SYSTEM_CASE_WORK_COUNTS
```

- `source_commit`과 `project_work_kanban.source_main_sha`는 같은 40자 SHA다.
- current publication 검증에서는 trusted expected SHA와 일치하고 staleness가 `CURRENT_AT_SOURCE_SHA`여야 한다.
- 두 생성 시각은 timezone을 포함한 ISO-8601이며 작업 snapshot 시각은 PDF 생성 시각보다 늦을 수 없다.
- history snapshot은 `STALE_SNAPSHOT`을 표시할 수 있지만 current라고 주장하지 않는다.
- source mismatch, unresolved ref, evidence 없는 PASS, reason 없는 N/A, blocker·resume condition 없는 차단은 validation failure다.
- 외부 URL·명령·HTML·Markdown은 데이터로만 취급하며 실행하지 않는다.
- 검증기는 기록 일관성과 계산을 확인할 뿐 evidence 진실성, 사용자 승인, UX 품질을 대신 판정하지 않는다.

## 6. 생성·갱신 Gate

다음 중 하나가 바뀐 의미 있는 시점에 기존 Blueprint PDF를 재생성한다.

- 승인 Goal/Playable Slice
- 목표·시스템·케이스의 현재/목표 상태 또는 checklist
- `project_work_kanban`의 완료·차단·사용자 결정·다음 행동
- 자동 테스트·runtime·visual·play·human evidence
- Codex 인계, Vertical Slice, milestone, Release Candidate

작은 코드 수정마다 PDF를 재발행하지 않는다. 상태 변화가 없으면 repository diff가 일상 검토 수단이다.

## 7. 프로젝트 적용

1. 프로젝트 `AGENTS.md`와 실제 owner를 fresh-read한다.
2. 기존 ID와 owner를 재사용하고 새 ID 체계를 일괄 강제하지 않는다.
3. 현재 승인 범위의 Goal/System/Case와 기존 `project_work_kanban`을 같은 source SHA에서 읽는다.
4. Goal/System checklist는 owner에서 파생하고, Work 상태는 board에서 직접 읽으며 복사본을 만들지 않는다.
5. `tools/human_blueprint_progress_projection.py`로 source·board·참조·evidence·계산을 검증한다.
6. `--render-markdown` 출력을 기존 Blueprint source의 작업현황 장에 포함한다.
7. 기존 PDF 생성·전 페이지 렌더·내부 링크·표 잘림을 확인한다.
8. 실제 project adoption은 프로젝트별 정상 PR과 exact-revision 검증으로 수행한다. Base 병합만으로 전 프로젝트 적용 완료를 주장하지 않는다.

## 8. 완료 증거 상한

이 계약과 검증기는 projection 형식, ID/참조 일관성, direct PM source, source SHA, evidence locator, ceiling, N/A 분모 제외, 독립 완료 수, Markdown 안전 출력을 증명할 수 있다.

다음은 별도 검증이 필요하다.

- 프로젝트 owner에서 모든 목표·시스템·케이스/checklist를 빠짐없이 추출했는지
- 실제 PDF 시각 완성도·페이지 레이아웃·접근성·내부 링크
- Godot runtime·UX·human playtest
- 사용자 최종 Blueprint 승인
- 프로젝트별 adoption·release readiness
