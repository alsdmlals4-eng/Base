---
name: managing-game-project-operating-system
description: Use automatically when installing, auditing, reconciling legacy files, migrating, or verifying the repository operating system that connects project entrypoints, design sources, selective skills, publications, assets, gates, automation, and cold-start handoff.
---

# Managing the Game Project Operating System

## Core principle

신규 설치, 기존 구조 감사, 구형 파일 정리, 승인된 마이그레이션과 운영체계 검수는 같은 책임 원본·참조·복구 계약을 공유한다. `Work Mode`와 `Skill Mode`를 구분하며, 읽기 전용 조사와 승인된 쓰기 작업을 혼동하지 않는다.

- `Work Mode`: `PLAN / BUILD / REVIEW`
- 이 문서의 `mode`: 운영체계 Skill 내부의 **Skill Mode**

## Skill Modes

- `install`: 신규 또는 내용이 거의 없는 프로젝트에 운영체계를 설치한다.
- `audit`: 기존 프로젝트를 변경 없이 조사하고 현재 구조·위험·보존표를 만든다.
- `reconcile-legacy`: 구형·중복·버전명 파일과 파생본을 현행 정본에 맞춰 갱신·통합·호환 보존·아카이브·승인 삭제한다.
- `migrate`: 사용자가 승인한 처리표 범위만 새 책임 구조로 재배치한다.
- `verify`: 설치·정리·마이그레이션·대규모 변경 뒤 전체 연결을 증거로 검수한다.

```text
신규·내용 거의 없음 → install
기존 운영 프로젝트 → audit
v2·final·latest·복제본·구형 파생본 존재 → audit → reconcile-legacy
승인된 구조 이동표 있음 → migrate
설치·정리·마이그레이션·주요 게이트 후 → verify
```

`reconcile-legacy`는 별도 신규 Skill이 아니다. 기존 프로젝트의 책임 원본·참조·보존·삭제 권한을 다루는 같은 생명주기이므로 이 Skill의 전문 Skill Mode로 유지한다.

## Required inputs

```yaml
target_repository:
work_mode: PLAN/BUILD/REVIEW
project_mode: new/existing/installed
requested_skill_mode: install/audit/reconcile-legacy/migrate/verify
base_version:
project_agents:
project_start_here:
documentation_map:
active_context:
development_gates:
design_document_registry:
skill_registry:
publications_and_manifests:
visual_and_asset_manifests:
roadmap_issues_plans_prs:
actual_code_data_assets_tests:
protected_paths_decisions_assets:
approved_migration_table:
approved_legacy_reconciliation_table:
known_versioned_duplicates_and_aliases:
governance_and_workflow_state:
rollback_ref:
```

## Shared read order

```text
최신 사용자 지시
→ AGENTS·README·START_HERE
→ Work Mode·Skill 라우팅 계약
→ Active Context·Documentation Map·Roadmap·Development Gates
→ Design Document Registry·Skill Registry
→ 관련 책임 원본·Skill·Learning Log
→ DOCX/PDF·다이어그램·승인 이미지·Manifest
→ 실제 코드·데이터·자산·테스트
→ Issue·Plan·PR·Workflow·최근 변경
```

전체 skills 폴더를 기본 로드하지 않는다. 백업·보류·제거 후보는 감사·정리 대상일 때만 읽는다.

## Shared operating contract

- 한 질문에는 등록된 현행 Markdown 또는 JSON 책임 원본 하나만 둔다.
- PDF·DOCX·다이어그램은 Registry 발행 정책과 Manifest를 따른다.
- trigger가 일치하는 최소 Skill·Skill Mode를 자동 선택한다.
- 승인·구현·검증·발행 최신성·사람 검수 상태를 분리한다.
- 기존 승인 결정·수치·자산·실패·보류·참조는 조사와 승인 없이 제거하지 않는다.
- 파일 존재와 실제 실행·강제를 구분한다.
- 새 AI가 과거 대화 없이 현재 상태와 다음 작업을 찾을 수 있어야 한다.

## Skill Mode: install

1. 신규·빈 프로젝트인지 확인한다. 고유 문서·자산·이력이 있으면 `audit`로 전환한다.
2. 루트 `[기획서]/00_프로젝트_허브/`와 시작 문서·Registry·게이트를 설치한다.
3. 프로젝트가 실제 선택한 책임 분야만 등록한다.
4. 서술은 Markdown, 구조·상태·게임 데이터는 JSON을 선택한다.
5. 발행 생성기·Manifest·선택 파생본 정책을 설치한다.
6. Foundation·분야 Skill Registry와 Learning Log를 설치한다.
7. Visual Source·Asset Manifest와 승인 상태를 연결한다.
8. Governance 검사·Actions·Required Check 준비 상태를 구분한다.
9. `verify`로 콜드 스타트와 파이프라인을 확인한다.

## Skill Mode: audit

첫 단계는 `PLAN` 또는 `REVIEW` Work Mode이며 대량 삭제·이동·통합을 수행하지 않는다.

| 현재 경로 | 역할 | 추정 버전 | 참조 | 고유 정보 | 중복·충돌 | 상태 | 제안 | 위험 | 검증 |
|---|---|---|---|---|---|---|---|---|---|

산출물:

- 현재 책임 문서·Skill·자산·파생본 지도
- 중복·충돌·누락·구형 참조 목록
- 목표 Registry와 책임 원본 구조
- 갱신·통합·호환 보존·아카이브·삭제 후보
- 변경 전후 예상 구조
- 보존·참조·롤백 검증 계획
- 사용자가 승인해야 할 처리표

## Skill Mode: reconcile-legacy

다음 신호가 있으면 자동 선택한다.

- `v2`, `v3`, `final`, `final2`, `latest`, 날짜 접미사 등 활성 복제본
- 같은 책임을 가진 Markdown·JSON·PDF·DOCX 다중 현행본
- 새 경로로 대체됐지만 활성 파일이 계속 참조하는 구형 경로·ID·Schema
- 원본보다 오래된 생성물·Manifest·해시
- 삭제된 Skill·명령·파일을 실행 경로가 참조함

파일별로 하나를 판정한다.

```text
CURRENT
UPDATE_IN_PLACE
MERGE_TO_CANONICAL
COMPATIBILITY_STUB
ARCHIVE_HISTORY
DELETE_APPROVED
KEEP_UNRESOLVED
```

처리 순서:

```text
인벤토리·해시·참조 수집
→ 현행 정본 판정
→ 고유 결정·예외·이미지·보류 승계
→ 충돌·미확정 분리
→ 처리표 승인 확인
→ BUILD Work Mode로 UPDATE·MERGE·STUB·ARCHIVE·DELETE 실행
→ Registry·참조·생성기·테스트·파생본 갱신
→ REVIEW Work Mode로 reference-freshness·회귀·복구 검증
```

승인표가 없으면 `PLAN/REVIEW`에서 판정과 제안까지만 수행한다. 삭제는 다음을 모두 만족해야 한다.

- 모든 고유 정보·이미지·예외·보류가 현행 정본에 승계됨
- 활성·보조·외부 참조가 새 경로로 갱신되거나 호환 stub이 있음
- PDF·DOCX·Manifest·해시·생성기가 검증됨
- Git 이력·태그·백업 등 복구 경로가 있음
- 사용자 지시 또는 승인된 작업 계약의 삭제 근거가 있음
- `auditing-canonical-reference-freshness`에 차단 finding이 없음

템플릿: `templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md`

## Skill Mode: migrate

`approved_migration_table` 항목만 `BUILD` Work Mode에서 수행한다.

```text
고유 문장·표·결정·예외·이미지·보류 추출
→ 충돌 표시
→ 최신 사용자 결정과 실제 구현으로 현행 판정
→ 불확실성은 [확인 필요]
→ 새 책임 원본과 Registry에 승계
→ 승인 이미지·발행 경로 연결
→ 참조 갱신
→ 변경 전후 보존 대조
→ 기존 원본 수명주기 판정
→ verify
```

## Skill Mode: verify

각 영역을 `PASS / PARTIAL / FAIL / NOT_RUN`과 증거 경로로 기록한다.

1. 루트와 시작 문서
2. Work Mode·Skill 자동 라우팅과 실행 보고
3. Design Document Registry와 단일 책임 원본
4. 구형본 처리표·Legacy Alias·활성 stale reference 부재
5. PDF·선택 DOCX·다이어그램·승인 이미지·Manifest
6. Skill Registry·최소 라우팅·Learning Log
7. Development Gates·Roadmap·결정 추적성
8. Visual Source·Asset Manifest
9. Governance checker·회귀 테스트·GitHub Actions·브랜치 보호
10. 콜드 스타트

```text
결정
→ Markdown/JSON 책임 원본
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ Active Context
→ 사람용 발행본
```

## Output contract

```md
# 게임 프로젝트 운영체계 결과
## Work Mode와 Skill Mode
## 자동 선택 이유
## 현재 구조·증거
## 구형 파일·파생본 처리표
## 실제 갱신·통합·아카이브·삭제
## 제안만 한 변경
## 보존·참조·롤백 대조
## Registry·책임 원본·발행본
## Skill·Learning·Routing
## 자동화·GitHub 강제
## 콜드 스타트
## PASS·PARTIAL·FAIL·NOT_RUN
## 얻은 결과·미검증·위험
## 다음 단계와 승인 조건
```

## Definition of Done

- Work Mode와 Skill Mode·쓰기 권한이 명확하다.
- 사용자가 Skill을 선언하지 않아도 trigger로 필요한 Skill Mode를 자동 선택했다.
- 기존 프로젝트는 `audit`와 승인 없이 대규모 변경하지 않았다.
- 구형 파일은 고유 정보·참조·파생본·복구·승인에 따라 판정됐다.
- 삭제·통합 뒤 활성 stale reference와 untouched 소비자가 없다.
- 신규·정리·마이그레이션 결과는 `verify` 증거를 가진다.
- 실행하지 않은 검사와 권한은 `NOT_RUN` 또는 `[미검증]`이다.
- 사용한 Skill Mode의 이유와 얻은 결과를 보고했다.

## Failure conditions

- 기존 프로젝트에 신규 설치 구조를 강제함
- 사용자 승인 전 삭제·이동·통합함
- 파일명에 `old`·`v2`가 있다는 이유만으로 삭제함
- 파일 수 감소를 성공으로 판단함
- 고유 정보·승인 자산·보류·실패 기록을 축약함
- Git 이력만 있다는 이유로 활성 참조·복구 검증 없이 삭제함
- 호환성이 필요한 외부 경로를 stub 없이 제거함
- PDF·DOCX를 독립 책임 원본으로 수정함
- 설치·정리·마이그레이션 뒤 `verify`를 생략함
- 사용한 이유와 결과 없이 Skill 실행만 주장함

## Legacy aliases

- `installing-game-project-operating-system` → `install`
- `migrating-existing-game-project-structure` → `audit`, `reconcile-legacy` 또는 `migrate`
- `verifying-game-project-operating-system` → `verify`

Related:

- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`
