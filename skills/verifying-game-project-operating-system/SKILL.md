---
name: verifying-game-project-operating-system
description: Use after installing, migrating, or materially changing a game-project operating system, before a major gate or release, or when cold-start, JSON design documents, skill routing, DOCX/PDF publications, images, or automation health is uncertain.
---

# Verifying a Game Project Operating System

## Core principle

파일이 존재하는지만 보지 않는다. **시작 문서 → Registry → JSON 책임 원본 → 선택적 스킬 → 실제 파일 → 검증 → DOCX/PDF·인수인계**가 실제로 이어지는지 증거로 확인한다.

## Use when

- 운영체계를 설치하거나 기존 프로젝트를 마이그레이션함
- 분야·본책·스킬·생성기·자동화 구조를 크게 변경함
- Vertical Slice·Production·Alpha·Beta·Release Candidate 전
- 새 채팅이 필요한 기획서·스킬을 찾지 못함
- JSON·구현·자산·DOCX/PDF·검증 불일치가 의심됨
- 주기적인 Health Review

## Do not use when

- 운영체계와 무관한 L0 수정
- 작은 구현에서 관련 테스트와 분야 검수만으로 충분함
- 저장소 접근 없이 정상 선언
- 런타임 검증 없이 게임 품질까지 통과 판정

## Required inputs

```yaml
target_repository:
base_version:
project_agents:
project_start_here:
documentation_map:
active_context_and_handoff:
development_gates:
design_document_registry:
skill_registry:
project_skill_map_publication:
active_design_document_jsons:
design_document_publication_manifests:
visual_and_asset_manifests:
governance_config:
workflow_runs:
actual_code_data_assets_tests:
```

## Read first

```text
최신 사용자 지시
→ AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ Documentation Map·Active Context·Development Gates
→ DESIGN_DOCUMENT_REGISTRY.json·SKILL_REGISTRY.json
→ 관련 기획서 JSON·분야 스킬
→ 사람용 DOCX/PDF·다이어그램·승인 이미지
→ Governance config·Workflow·검사 결과
→ 실제 코드·데이터·자산·테스트
```

## Verification areas

### 1. Root and entrypoints

- `[기획서]`가 저장소 루트 바로 아래에 있는가?
- 중첩 현행 기획서 폴더가 없는가?
- 사용자와 AI가 같은 시작 문서를 읽는가?
- START_HERE가 Design Document Registry·Skill Registry·현재 상태·다음 작업을 연결하는가?

### 2. Design document responsibility

- `DESIGN_DOCUMENT_REGISTRY.json`이 존재하고 활성 문서 ID가 고유한가?
- 프로젝트 전체와 11개 분야 책임이 `responsibility_coverage`로 보존되는가?
- 각 활성 항목의 JSON·DOCX·PDF·asset dir·Manifest 경로가 존재하는가?
- 활성 `*_기획서.md`, `DISCIPLINE_BIBLE.md`, `PROJECT_MASTER_PLAN.md`가 재생성되지 않았는가?
- 질문마다 현행 JSON 책임 원본이 하나인가?
- 백업·보류·제거 후보가 기본 읽기에서 제외되는가?

### 3. Human publications

각 활성 기획서에서 확인:

- JSON source SHA-256과 Manifest가 일치함
- DOCX가 유효한 ZIP·OOXML 파일임
- PDF가 실제 PDF임
- 생성기·다이어그램 생성기 해시가 현재 파일과 일치함
- 작업 흐름·상태·책임 다이어그램이 존재함
- 승인 이미지·실제 캡처가 존재하고 해시가 일치함
- PDF 전 페이지 렌더가 성공하고 빈 페이지가 없음
- 요구된 경우 사람이 모든 페이지를 시각 검수함
- DOCX·PDF가 독립 책임 원본으로 수정되지 않음

### 4. Skill routing and learning

- `SKILL_REGISTRY.json`의 활성 경로가 존재함
- 각 스킬에 Trigger·사용·비사용 조건·Learning Log·review trigger가 있음
- 각 분야의 진입 스킬이 등록됨
- 전체 스킬이 아니라 최소 집합만 선택됨
- `PROJECT_SKILL_MAP.docx/.pdf/.assets`가 Registry와 동일한 해시 기준으로 생성됨
- `PROJECT_SKILL_MAP.md`가 없음
- 호출 후 성공·실패·예외·피드백이 기록됨

### 5. Development gates and traceability

- Ready·Implementation·Verification·Documentation·Completion Gate가 연결됨
- 현재 제품 단계와 다음 Greenlight 증거가 명확함
- 대표 결정이 다음 경로로 추적됨

```text
결정
→ 기획서 JSON
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ 현재 상태
→ 사람용 PDF
```

### 6. Visuals and assets

- 승인 이미지와 실제 캡처가 구분됨
- 캐노니컬 경로·Asset ID가 중복되지 않음
- 채택·비채택 요소가 JSON에 기록됨
- 기존 승인 이미지를 임의로 교체하지 않음
- 폐기 이미지를 현행 PDF가 기준처럼 보여주지 않음

### 7. Automation and enforcement

- `check_documentation_governance.py`
- `check_skill_routing_governance.py`
- `check_design_document_publications.py`
- 정상·실패 회귀 테스트
- DOCX/PDF 실제 생성 통합 테스트
- GitHub Actions 실제 실행
- Required Status Check·CODEOWNERS·브랜치 보호 실제 활성 상태

파일 존재와 실제 실행·강제를 구분한다.

### 8. Cold start

새 AI가 10분 안에 답해야 한다.

- 프로젝트 목적과 핵심 경험은 무엇인가?
- 현재 단계와 최우선 작업은 무엇인가?
- 무엇을 변경하면 안 되는가?
- 프로젝트 전체·각 분야 JSON 본책은 어디인가?
- 사람이 볼 최신 PDF·DOCX·승인 이미지는 어디인가?
- 각 분야 진입 스킬과 실제 검증은 어디인가?
- 보류·미검증·위험은 어디인가?

## Output contract

```md
# 게임 프로젝트 운영체계 Health Review

## 결론
## 루트·시작 문서
## Design Document Registry·JSON 책임 원본
## 사람용 DOCX/PDF·다이어그램·승인 이미지
## 분야·Foundation 스킬 라우팅
## 스킬 학습·갱신
## 개발 게이트·추적성
## 자동화·GitHub 강제
## 콜드 스타트
## 실패·미검증
## 수정 우선순위
```

각 항목은 `PASS / PARTIAL / FAIL / NOT_RUN`으로 표시하고 증거 경로를 기록한다.

## Definition of Done

- 모든 검수 영역에 상태와 증거가 있음
- 실행하지 않은 검증은 `NOT_RUN` 또는 `[미검증]`
- 구조적 실패와 제품 품질 실패를 구분함
- 수정 우선순위와 책임 분야가 있음
- 반복된 운영 실패를 Learning Log·Skill·Checker·Test에 반영함

## Failure conditions

- 파일 존재만으로 실제 작동·강제를 통과 처리함
- 대상 저장소를 읽지 않고 추정함
- 전체 스킬을 로드해 선택적 호출을 검증하지 않음
- PDF 존재만 보고 JSON·이미지·생성기 최신성을 생략함
- 전 페이지 렌더 없이 시각 검수 통과 선언
- 런타임 테스트 미실행을 숨김
- 문제를 발견했지만 책임 원본·스킬·검사에 피드백하지 않음

## Learning contract

```text
실패 영역
→ 재현 조건
→ 누락된 JSON 계약·생성기·검사
→ 프로젝트 전용 수정
→ 반복 여부 확인
→ Base Method·Skill·Template·Test 후보
```

같은 실패가 반복되면 관련 review trigger를 활성화하고 자동화 가능한 항목은 회귀 테스트로 만든다.
