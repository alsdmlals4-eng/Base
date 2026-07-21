---
name: managing-game-project-operating-system
description: Use when installing, auditing, migrating, or verifying the repository operating system that connects project entrypoints, design sources, selective skills, publications, assets, gates, automation, and cold-start handoff.
---

# Managing the Game Project Operating System

## Core principle

신규 설치, 기존 구조 감사·마이그레이션, 운영체계 검수는 같은 구조를 서로 다른 권한으로 다루는 하나의 생명주기다. 모드를 명시하고 읽기 전용 감사와 승인된 쓰기 작업을 혼동하지 않는다.

## Modes

- `install`: 신규 또는 내용이 거의 없는 프로젝트에 운영체계를 설치한다.
- `audit`: 운영 중인 기존 프로젝트를 변경 없이 조사하고 목표 구조·위험·보존표를 제안한다.
- `migrate`: 사용자가 승인한 처리표 범위만 안전하게 재배치한다.
- `verify`: 설치·마이그레이션·대규모 변경 뒤 구조 연결과 자동화를 증거로 검수한다.

기본 모드:

```text
신규·내용 거의 없음 → install
기존 운영 프로젝트 → audit
승인된 처리표 있음 → migrate
설치·마이그레이션·주요 게이트 후 → verify
```

## Required inputs

```yaml
target_repository:
project_mode: new/existing/installed
requested_mode: install/audit/migrate/verify
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
governance_and_workflow_state:
```

## Shared read order

```text
최신 사용자 지시
→ AGENTS·README·START_HERE
→ Active Context·Documentation Map·Roadmap·Development Gates
→ Design Document Registry·Skill Registry
→ 관련 Markdown/JSON 책임 원본·스킬·Learning Log
→ DOCX/PDF·다이어그램·승인 이미지·Manifest
→ 실제 코드·데이터·자산·테스트
→ Issue·Plan·PR·Workflow·최근 변경
```

전체 skills 폴더를 기본 로드하지 않는다. 백업·보류·제거 후보는 감사 대상일 때만 읽는다.

## Shared operating contract

- 활성 `[기획서]`는 신규·승인된 구조에서 저장소 루트에 둔다.
- 한 질문에는 등록된 단일 Markdown 또는 JSON 책임 원본 하나만 둔다.
- PDF는 Registry의 발행 정책에 따라 동기화하고 DOCX·다이어그램은 선언한 경우만 생성한다.
- 전체 스킬이 아니라 trigger가 일치하는 최소 스킬만 호출한다.
- 승인·구현·검증·발행 최신성·사람 검수 상태를 분리한다.
- 기존 승인 결정·수치·자산·실패·보류·참조는 조사와 승인 없이 제거하지 않는다.
- 파일 존재와 실제 실행·강제를 구분한다.
- 새 AI가 과거 대화 없이 현재 상태와 다음 작업을 찾을 수 있어야 한다.

## Mode: install

1. 대상이 신규·빈 프로젝트인지 확인한다. 운영 중인 고유 문서·자산·이력이 있으면 `audit`로 전환한다.
2. 루트 `[기획서]/00_프로젝트_허브/`와 시작 문서·Registry·게이트를 설치한다.
3. 프로젝트가 실제로 선택한 책임 분야만 등록한다. 11개 분야 전체를 강제하지 않는다.
4. 서술 중심은 Markdown, 구조 검증·상태·게임 데이터는 JSON을 선택한다.
5. 발행 생성기·Manifest·선택 파생본 정책을 설치한다.
6. Foundation·분야 Skill Registry와 Learning Log를 설치한다.
7. Visual Source·Asset Manifest와 승인 상태를 연결한다.
8. Governance 검사·Actions·Required Check 준비 상태를 구분해 기록한다.
9. `verify` 모드로 콜드 스타트와 파이프라인을 확인한다.

## Mode: audit

첫 단계에서는 대량 삭제·이동·통합을 수행하지 않는다.

파일·자산·스킬별로 기록한다.

| 현재 경로 | 역할 | 참조 | 고유 정보 | 중복·충돌 | 상태 | 제안 | 위험 | 검증 |
|---|---|---|---|---|---|---|---|---|

산출물:

- 현재 책임 문서·스킬·자산 지도
- 중복·충돌·누락 목록
- 목표 Registry와 책임 원본 구조
- 이동·통합·제거 후보
- 변경 전후 예상 구조
- 보존·참조·롤백 검증 계획
- 사용자가 승인해야 할 처리표

## Mode: migrate

`approved_migration_table`에 있는 항목만 수행한다.

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

삭제는 다음을 모두 만족한 경우만 수행한다.

- 모든 고유 정보·이미지·예외·보류가 승계됨
- 활성·보조·외부 참조가 새 경로로 갱신됨
- 발행본·Manifest가 검증됨
- Git 이력 또는 별도 보존으로 복구 가능함
- 사용자 승인 근거가 있음

## Mode: verify

각 영역을 `PASS / PARTIAL / FAIL / NOT_RUN`과 증거 경로로 기록한다.

1. 루트와 시작 문서
2. Design Document Registry와 단일 책임 원본
3. PDF·선택 DOCX·다이어그램·승인 이미지·Manifest
4. Skill Registry·최소 라우팅·Learning Log
5. Development Gates·Roadmap·결정 추적성
6. Visual Source·Asset Manifest
7. Governance checker·회귀 테스트·GitHub Actions·브랜치 보호
8. 콜드 스타트

추적 경로:

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
## 실행 모드와 권한
## 현재 구조·증거
## 실제 변경
## 제안만 한 변경
## 보존·참조 대조
## Registry·책임 원본·발행본
## Skill·Learning·Routing
## 자동화·GitHub 강제
## 콜드 스타트
## PASS·PARTIAL·FAIL·NOT_RUN
## 미검증·위험·롤백
## 다음 단계와 승인 조건
```

## Definition of Done

- 모드와 쓰기 권한이 명확하다.
- 기존 프로젝트는 `audit`와 사용자 승인 없이 대규모 변경하지 않았다.
- 신규·마이그레이션 결과는 `verify` 증거를 가진다.
- 문서·스킬·발행·자산·실제 파일·검증이 끊김 없이 연결된다.
- 실행하지 않은 검사와 권한은 `NOT_RUN` 또는 `[미검증]`이다.
- 새 작업자가 저장소만으로 방향·상태·다음 작업·보호 범위를 찾는다.

## Failure conditions

- 기존 프로젝트에 신규 설치 구조를 강제함
- 사용자 승인 전 삭제·이동·통합함
- 파일 수 감소를 성공으로 판단함
- 고유 정보·승인 자산·보류·실패 기록을 축약함
- PDF·DOCX를 독립 책임 원본으로 수정함
- 파일 존재만으로 Actions·Required Check·런타임 검증을 통과 처리함
- 전 페이지 렌더 없이 시각 검수 완료를 선언함
- 설치·마이그레이션 뒤 `verify`를 생략함

## Legacy aliases

- `installing-game-project-operating-system` → `install`
- `migrating-existing-game-project-structure` → `audit` 또는 `migrate`
- `verifying-game-project-operating-system` → `verify`

Related methods:

- `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`
