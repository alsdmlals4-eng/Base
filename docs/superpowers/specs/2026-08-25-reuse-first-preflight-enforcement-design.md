# Reuse-First Preflight Enforcement Design

## Goal

프로젝트/Base의 신규·개정 설계·구현·시각 제작이 시작되기 전에 이미 존재하는 프로젝트 구현, 승인된 Asset/Reference/Benchmark 자료, Base 재사용 모듈과 축적 knowledge/case/reference, 다른 프로젝트의 검증된 패턴, 필요한 외부 벤치마크를 순서대로 먼저 확인하고, 재사용·변형·참고·신규 제작 판정을 남기도록 작업 진입 게이트를 fail-closed로 연결한다.

## User-approved direction

2026-08-25 사용자 승인: 기존 재사용 체계를 새 Skill로 늘리지 않고 `AGENTS → managing-project-intake-and-work-contract → PROJECT_WORK_REUSE_HANDOFF`를 하나의 필수 진입 게이트로 연결하는 B안을 채택한다. 교정 뒤에는 같은 유형의 “문서에는 있으나 실제 진입점에 연결되지 않은 규칙”도 추가 감사한다.

## Root cause

재사용 Registry, adoption profile, opportunity scan, Notion 재사용 모듈/에셋/레퍼런스 surface와 Base knowledge/case/reference는 이미 존재한다. 그러나 최상위 intake의 `FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN`에는 이 자원들을 신규 제작·외부 재조사 전에 반드시 확인하는 명시적 fail-closed 단계가 없다. 따라서 분야별 Skill이 개별적으로 Existing Solution First를 갖고 있어도 실행자가 해당 owner를 로드하지 않으면 신규 제작이나 외부 조사로 바로 진입할 수 있다.

두 번째 누락은 exit feedback이다. `PROJECT_WORK_REUSE_HANDOFF.json`에는 `selected_modules`, `project_only_lessons`, `base_promotion_candidates` 등 종료 필드가 있으나 intake 완료 게이트와 직접 연결되어 있지 않아 프로젝트에서 새로 확인된 재사용 가치가 Base로 되돌아오는 루프가 생략될 수 있다.

## Scope

### Change

- root `AGENTS.md`에 `REUSE_FIRST_PREFLIGHT_REQUIRED`와 `REUSE_LEARNING_HANDOFF_REQUIRED` 불변식을 추가한다.
- intake의 current-state audit 순서를 `현재 프로젝트 → 기존 승인 Asset/Reference/Benchmark → Base reuse state → Base accumulated knowledge/case/reference → 필요한 targeted cross-project evidence → 필요한 외부 benchmark → 대안/IRG`로 연결한다.
- `PROJECT_WORK_REUSE_HANDOFF.json`에 applicability, required source order, fail-closed 조건, targeted scan 경계, exit-learning handoff를 구조화한다.
- `START_HERE.md`에 universal entry route를 짧게 노출한다.
- focused contract test와 CI route를 추가해 향후 문구 삭제/우회가 회귀로 잡히게 한다.
- Notion의 `Base · 작업 시스템 & Skill 지도`와 `Base · 재사용 모듈 라이브러리`에는 사람이 이해할 최소 요약만 동기화한다.

### Protect

- open/draft/ready PR #660, #658, #650 및 다른 open workstream은 read-only다.
- 모든 프로젝트를 매 작업마다 전수 스캔하지 않는다.
- 단순 오탈자, 기계적 문서 정리, 이미 승인되고 재사용 판정이 남아 있는 동일 범위 continuation에는 불필요한 외부 시장조사를 강제하지 않는다.
- 재사용 후보 발견만으로 프로젝트 정본·runtime·Asset 승인 권위를 획득하지 않는다.
- 프로젝트 고유 정체성, 세계관, 게임 규칙을 공용화 때문에 평준화하지 않는다.
- 새 Skill, 새 유료 도구, 새 runtime dependency를 만들지 않는다.

## Gate contract

### `REUSE_FIRST_PREFLIGHT_REQUIRED`

적용 대상은 신규 또는 의미 있게 개정되는 시스템, mechanic, data/content structure, UI/UX, visual/asset, tool/automation, workflow, Skill/eval, QA/test 설계·구현이다.

기본 source order:

1. current project authority와 실제 구현/자산/테스트
2. current project의 승인된 Asset/Reference/Benchmark surface
3. Base `PROJECT_WORK_REUSE_HANDOFF`, adoption profile/matrix, `REUSABLE_MODULE_REGISTRY`
4. 현재 결정과 관련된 기존 Base knowledge/case/reference owner
5. Registry/profile가 가리키거나 현재 병목과 직접 관련 있는 다른 프로젝트의 검증된 구현/패턴만 targeted 확인
6. 현재 결정을 실제로 바꿀 필요가 있을 때 공식/1차 자료와 성공/실패 사례를 포함한 외부 benchmark
7. owner별 disposition과 reuse/no-reuse 근거

적용 대상에서 이 preflight가 `NOT_RUN`이면 신규 설계/제작/`BUILD_NEW` readiness를 주장할 수 없다. 이미 같은 승인 계약에서 유효한 preflight evidence가 있고 범위·consumer·freshness가 변하지 않은 continuation은 `REUSED_EVIDENCE`로 재사용할 수 있다. 순수 기계적 변경은 이유를 기록한 `NOT_APPLICABLE`을 허용한다.

### Targeted cross-project boundary

다른 프로젝트 전수 검색은 기본 동작이 아니다. Base Registry/profile의 출발 프로젝트, 동일 모듈 ID, 동일 병목/consumer가 가리키는 프로젝트만 확인한다. 유사성이 낮거나 권위가 불분명한 프로젝트를 억지로 참고하지 않는다.

### Disposition

새 범용 taxonomy를 별도 정본으로 만들지 않는다. 각 owner의 기존 vocabulary를 그대로 사용한다. 최소한 `selected candidate`, `reuse/adapt/reference/no-reuse decision`, `why`, `consumer`, `validation ceiling`을 남긴다. 신규 제작은 기존 후보가 현재 요구를 충족하지 못한다는 근거가 있어야 한다.

### `REUSE_LEARNING_HANDOFF_REQUIRED`

적용된 작업이 끝날 때 `selected_modules`, `reuse_mode`, `project_paths_changed`, `verification_evidence`, `evidence_ceiling`, `rollback`, `project_only_lessons`, `base_promotion_candidates`를 기존 handoff owner에 맞춰 평가한다. 실제 새 학습이 없으면 `NO_NEW_REUSE_LEARNING`으로 종료하고 억지 Registry churn을 만들지 않는다. Base 승격은 기존 promotion gate를 통과할 때만 수행한다.

## Additional audit findings

- 주기적 Source/AI-game benchmarking 자동화는 2026-08-25 기준 enabled 상태이며 관련 daily/weekly task에 최근 run evidence가 존재한다. 주간 AI-game task는 2026-08-24 09:06 KST경 생성되어 같은 날 09:00 예약을 지난 뒤 만들어졌으므로 첫 정상 실행은 2026-08-31 월요일이다. 이 항목은 교정 대상이 아니다.
- 재사용 체계의 가장 큰 추가 누락은 exit learning handoff의 top-level enforcement 부재다. 이를 이번 변경에 포함한다.
- Notion Asset/Reference/Benchmark surface가 존재하지만 intake current-state audit가 이를 명시적으로 호출하지 않으므로 신규 제작 전에 모아둔 자료가 건너뛰어질 수 있다. 이를 이번 변경에 포함한다.
- Base knowledge/case/reference가 이미 축적되어 있어도 intake에서 외부 benchmark보다 먼저 읽는 순서가 강제되지 않았다. 같은 내용을 외부에서 다시 조사하거나 이미 흡수한 원리를 놓치는 원인이므로 이번 변경에 포함한다.

## Verification

- focused test가 변경 전 main 기준에서 실패하고 변경 후 통과해야 한다.
- v4.7 workflow alignment CI에서 새 focused test를 실행한다.
- Base v9 contract 및 변경으로 트리거되는 required checks를 exact PR head에서 확인한다.
- PR diff가 approved scope와 일치하고 open PR의 변경을 흡수하지 않았는지 재검토한다.
- merge 전 current main freshness, unresolved review thread 0, ruleset/required checks를 재검증한다.
- merge 후 GitHub main 및 두 Notion human surfaces를 readback한다.
