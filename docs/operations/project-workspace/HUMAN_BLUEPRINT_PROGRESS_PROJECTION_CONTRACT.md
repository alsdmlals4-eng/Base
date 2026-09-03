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
```

사람용 `HUMAN_MASTER_GDD_PDF` 하나에서 게임의 목표·시스템·콘텐츠·구현 원리와 현재 작업 상태를 함께 이해할 수 있게 한다. 프로젝트 작업현황을 보여 주기 위해 별도 HTML, 별도 PM PDF, 별도 대시보드 파일, 수동 체크 전용 상태 저장소를 추가하지 않는다.

PDF 안의 작업현황 장은 다음 source를 같은 exact revision에서 읽은 파생 snapshot이다.

1. repository의 현재 기획·Decision·데이터·코드·Scene·Resource·asset·test·evidence owner
2. `PROJECT_AI_PRODUCTION_SPEC.md` 또는 프로젝트 `AGENTS.md`가 지정한 목표·시스템·케이스 책임 원본
3. 기존 root work receipt의 `project_work_kanban`
4. 실제 자동 테스트·runtime·visual·play·human evidence

PDF의 체크 표시나 사람이 PDF에 남긴 주석만으로 repository 상태를 변경하지 않는다. 수정은 기존 owner에 반영하고 검증한 뒤 PDF를 다시 생성한다.

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
- 목표 완료/적용 수
- 시스템 완료/적용 수
- 케이스 완료/적용 수
- 필수 작업 완료/적용 수
- 차단 수와 `USER_DECISION_REQUIRED` 수
- 현재 활성 작업과 다음 안전 작업

단일 전체 퍼센트가 위 상태 축을 대체하지 않는다.

### 2.2 `PROJECT_GOAL_MAP`과 `GOAL_STATUS_CARD`

각 `GOAL_ID`는 다음을 가진다.

- 플레이어·사용자 가치
- 현재 성숙도와 목표 성숙도
- 연결된 `SYSTEM_ID`, `CASE_ID`, `WORK_ITEM_ID`
- 완료 조건, blocker, 다음 행동
- 목표가 완료로 계산된 근거

목표 완료는 제목이나 문서 작성 여부가 아니라, 목표 성숙도와 연결된 필수 시스템·적용 케이스·작업의 완료 조건을 모두 충족했을 때만 계산한다.

### 2.3 `SYSTEM_STATUS_CARD`

각 `SYSTEM_ID`는 다음을 보여 준다.

- 플레이어 가치와 시스템 책임
- canon owner와 actual consumer
- 입력·출력·상태·데이터·UI·asset·저장·실패·rollback 영향
- 기획·데이터·자산·구현·검증 체크리스트
- 연결 목표·케이스·작업
- 현재 성숙도, 목표 성숙도, blocker와 다음 행동

### 2.4 `CASE_VERIFICATION_MATRIX`

각 `CASE_ID`는 실제 사용·플레이 상황 하나를 표현한다. 적용 가능한 유형은 필요에 따라 선택한다.

```text
NORMAL | BOUNDARY | FAILURE | CONFLICT | INTERRUPTION
RECOVERY | SAVE_LOAD | UI_STATE | ACCESSIBILITY | PERFORMANCE
```

각 케이스는 `SYSTEM_ID`, 관련 `GOAL_ID`, 관련 `WORK_ITEM_ID`, 적용 여부, 성숙도, 필수 evidence, 실제 결과, evidence locator, 다음 행동을 가진다. 모든 시스템에 모든 유형을 기계적으로 복제하지 않고 실제 consumer·위험·실패 비용이 있는 케이스만 둔다.

### 2.5 `GOAL_SYSTEM_CASE_WORK_TRACEABILITY`

모든 표시 행은 다음 관계를 양방향으로 추적할 수 있어야 한다.

```text
GOAL_ID ↔ SYSTEM_ID ↔ CASE_ID ↔ WORK_ITEM_ID ↔ EVIDENCE
```

한쪽에만 존재하는 참조, 사라진 ID, 다른 source revision의 상태를 정상 표시하지 않는다.

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

프로젝트가 더 세분화된 `IDEA → RESEARCHED → FEASIBLE → SPECIFIED → ASSET_READY → IMPLEMENTED → MACHINE_VERIFIED → RUNTIME_VERIFIED → USER_APPROVED` 상태를 이미 정본으로 사용하는 경우, 그 상태를 별도 행으로 보존할 수 있다. 두 상태 모델을 임의로 자동 승격하거나 의미가 같은 것으로 합치지 않는다.

### 3.2 작업 흐름

```text
BACKLOG | READY | IN_PROGRESS | VERIFY_REVIEW | DONE
BLOCKED_UNVERIFIED | USER_DECISION_REQUIRED | DEFERRED
```

이 값은 기존 `project_work_kanban`을 투영한다. PDF가 새 작업 상태 owner가 아니다.

### 3.3 Evidence

```text
E0_CONTRACT | E1_STATIC | E2_TEST | E3_RUNTIME
E4_VISUAL | E5_PLAY | E6_HUMAN_PLAYTEST
```

허용 결과:

```text
PASS | FAIL | PARTIAL | NOT_RUN | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

자동 테스트 PASS는 runtime, 화면, UX, human/player, 사용자 승인 또는 release PASS가 아니다.

## 4. 진행률·완료 계산

```text
PASS_ONLY_COUNTS_COMPLETE
NOT_APPLICABLE_EXCLUDED_FROM_DENOMINATOR
DO_NOT_AVERAGE_CHILD_PERCENTAGES
NO_APPLICABLE_CHECKLIST
```

- 작업 완료: `DONE`만 센다.
- 케이스 완료: `APPLICABLE`이고 목표 성숙도에 도달했으며 모든 필수 evidence가 PASS일 때만 센다.
- 시스템 완료: 목표 성숙도, 적용 케이스, 현재 Goal에 필요한 연결 작업이 모두 완료되어야 한다.
- 목표 완료: 목표 성숙도와 연결 필수 시스템·적용 케이스·필수 작업이 모두 완료되어야 한다.
- `NOT_APPLICABLE`은 구체적인 이유가 있을 때만 분모에서 제외한다.
- future scope, 선택적 polish, 현재 승인 범위 밖 항목을 분모에 몰래 포함하거나 미완료 항목을 지워 분모를 줄이지 않는다.
- 자식 퍼센트를 평균내지 않는다. 목표·시스템·케이스·작업 완료 수를 각각 표시한다.
- 적용 항목이 0이면 `100%`가 아니라 `NO_APPLICABLE_CHECKLIST`로 표시한다.

## 5. Source·최신성·안전

```text
SOURCE_SHA_MATCH_REQUIRED
STALE_SNAPSHOT_VISIBLE
PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON
```

- projection `source_commit`은 PDF metadata와 검증 caller가 fresh-read한 40자 SHA와 일치해야 한다.
- `generated_at`, 포함 범위, approval status, evidence ceiling을 표시한다.
- source mismatch, unresolved reference, evidence 없는 PASS, reason 없는 N/A, blocker·resume condition 없는 차단 상태는 validation failure다.
- PDF 발행 뒤 repository 상태가 바뀌면 기존 PDF는 역사 snapshot이다. 이를 live current 상태라고 표시하지 않는다.
- 외부 URL·명령·HTML·Markdown은 데이터로만 취급하며 실행하지 않는다.
- 검증기는 기록 일관성과 계산을 확인할 뿐 evidence 진실성, 사용자 승인, UX 품질을 대신 판정하지 않는다.

## 6. 생성·갱신 Gate

다음 중 하나가 바뀐 의미 있는 시점에 기존 Blueprint PDF를 재생성한다.

- 승인 Goal/Playable Slice
- 목표·시스템·케이스의 현재 또는 목표 상태
- `project_work_kanban`의 완료·차단·사용자 결정·다음 행동
- 자동 테스트·runtime·visual·play·human evidence
- Codex 인계, Vertical Slice, milestone, Release Candidate

작은 코드 수정마다 PDF를 재발행하지 않는다. 상태 변화가 없는 경우 repository diff가 일상 검토 수단이다.

## 7. 프로젝트 적용

1. 프로젝트 `AGENTS.md`와 실제 owner를 fresh-read한다.
2. 기존 ID와 owner를 재사용한다. 새 ID 체계를 일괄 강제하지 않는다.
3. 현재 승인 범위의 Goal/System/Case/Work만 projection에 넣는다.
4. `tools/human_blueprint_progress_projection.py`로 source·참조·계산을 검증한다.
5. `--render-markdown` 출력을 기존 Blueprint source의 작업현황 장에 포함한다.
6. 기존 PDF 생성·전 페이지 렌더·내부 링크·표 잘림을 확인한다.
7. 실제 project adoption은 프로젝트별 정상 PR과 exact-revision 검증으로 수행한다. Base 병합만으로 전 프로젝트 적용 완료를 주장하지 않는다.

## 8. 완료 증거 상한

이 계약과 검증기는 다음을 증명할 수 있다.

- projection 형식·ID·참조·상태 어휘 일관성
- source SHA 일치
- PASS evidence locator 존재
- N/A 분모 제외
- 완료 수 계산과 Markdown 출력
- Base route와 회귀 테스트

다음을 증명하지 않는다.

- 프로젝트 정본에서 모든 값이 정확히 추출됐는지
- PDF 시각 완성도·페이지 레이아웃·접근성
- Godot runtime·UX·human playtest
- 사용자 최종 Blueprint 승인
- 프로젝트별 adoption·release readiness
