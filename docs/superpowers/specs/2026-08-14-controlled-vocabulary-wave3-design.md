# Base Controlled Vocabulary Wave 3 Design

## 상태

- Date: 2026-08-14
- Scope approval: 직전 Wave 2 완료 보고에서 제안한 3차 실무 기술 용어군을 사용자가 `진행해`로 승인했다.
- Base baseline: `0701cfb6c3bcbdd81df92a313025c03e4154e574`
- Work Mode: PLAN → BUILD → REVIEW
- Canonical target: `docs/CONTROLLED_VOCABULARY.md`
- New Skill / Work Mode / Schema / Route / Workflow: 없음

## Goal

초보 개발자가 구현·디버깅·배포 과정에서 반복해서 마주치는 용어를 기존 `BASE_SHARED` Controlled Vocabulary 안에서 짧게 찾을 수 있게 하고, 비슷한 표현을 같은 뜻으로 잘못 승격하는 문제를 semantic regression으로 막는다.

## Scope

### 1. 작업·결함·운영 문제

- Issue
- Bug
- Defect
- Incident

핵심 경계:

```text
Issue ≠ Bug
Issue는 Bug·Task·Feature·Feedback 등을 담을 수 있는 tracking container다.
Bug와 Defect는 조직·표준 문맥에 따라 겹치거나 구분될 수 있으므로 Base가 보편적인 완전 동의어/완전 비동의어 규칙을 강제하지 않는다.
Incident ≠ 개별 Bug/Defect
```

Incident는 실제 서비스·운영 영향과 조정된 대응이 필요한 문제 상태로 사용하고, 단일 결함 보고와 자동 동일시하지 않는다.

### 2. 요구·명세·제약

- Requirement
- Specification
- Constraint

핵심 경계:

```text
Requirement ≠ Specification document
Specification은 요구·설계·행동·특성 등을 정밀하게 기술하는 문서/데이터일 수 있다.
Constraint는 허용되는 해법·환경·자원·플랫폼 범위를 제한한다.
Constraint를 Requirement의 하위형으로 다루는 방법론도 있으므로 보편적 상속관계를 강제하지 않는다.
Acceptance Criteria ≠ Requirement 전체
```

### 3. 구조·의존 관계

- Dependency
- Coupling
- Cohesion

핵심 경계:

```text
Dependency 존재 ≠ Tight Coupling 확정
Coupling = 모듈 간 상호의존 정도
Cohesion = 한 모듈 내부 책임들의 논리적 관련성
High Cohesion / Low Coupling은 유용한 설계 휴리스틱이지만 단독 품질 PASS 증거가 아니다.
```

### 4. 인터페이스·호환성·데이터 계약

- API
- ABI
- Protocol
- Schema

핵심 경계:

```text
API ≠ Web API만
API compatibility ≠ ABI compatibility
Protocol ≠ Endpoint 목록
Schema ≠ Protocol
OpenAPI ≠ 모든 종류의 API
JSON Schema ≠ 모든 종류의 Schema
```

API는 프로그램이 사용할 수 있는 인터페이스 계약, ABI는 binary-level calling/data/symbol compatibility, Protocol은 상호작용의 메시지·순서·의미 규칙, Schema는 데이터 구조·타입·제약을 기술/검증하는 계약으로 구분한다.

### 5. 빌드·산출물·배포·출시

- Build
- Package
- Artifact
- Deployment
- Release

핵심 경계:

```text
Build process ≠ Build output
Artifact ≠ Package
Package는 설치·배포·의존성 소비를 위한 구조화된 유통 단위일 수 있지만 모든 Artifact가 Package는 아니다.
Deployment ≠ Release
Release Candidate ≠ Release
Staging Deployment ≠ Public Release
```

기존 운영 표의 `ARTIFACT` Kind는 문서·기록 등을 포함하는 일반 객체 분류다. 이 Wave의 `Artifact`는 build/workflow/test/evidence에서 생성·보존되는 산출물을 설명하는 공용 용어이며, 필요하면 `Build Artifact`, `Workflow Artifact`, `Evidence Artifact`처럼 qualifier를 붙인다.

### 6. 관측·진단

- Telemetry
- Metrics
- Logging / Logs
- Tracing / Traces
- Profiling / Profiles

`Metrics`는 직전 후보 목록에는 빠져 있었지만 OpenTelemetry의 핵심 telemetry signal 중 하나라 같은 축을 올바르게 이해하기 위해 최소 보완으로 포함한다.

핵심 경계:

```text
Telemetry = 상위 관측 데이터 범주
Metrics ≠ Logs
Logs ≠ Traces
Tracing ≠ Profiling
Profile ≠ Trace
관측 signal 존재 ≠ 원인 규명 완료
```

OpenTelemetry 문맥에서는 Traces, Metrics, Logs가 지원 signal이며 Profiles는 2026-08 기준 Alpha 상태다. Base는 OpenTelemetry의 maturity를 모든 profiling 도구의 maturity로 일반화하지 않는다.

## Source classification

| Source | Use | Disposition |
|---|---|---|
| GitHub Docs — About issues | Issue가 bug만이 아니라 idea/feedback/task 등을 추적할 수 있음을 확인 | ADOPT platform context / 일반화는 제한 |
| Google SRE Workbook — Incident Response | incident가 긴급 운영 영향·복구·조정된 대응 문맥임을 확인 | ADAPT SRE practice |
| NASA Systems Engineering Handbook / NPR 7123.1 | Requirement·Specification·Constraint 문맥 비교 | ADAPT; NASA-local equivalence를 보편화하지 않음 |
| Microsoft / Android architecture docs | Dependency·Coupling·Cohesion의 설계 관계 | ADAPT industry guidance |
| OpenAPI Specification | HTTP API interface description의 표준 문맥 | ADOPT only for OpenAPI context |
| Python C API Stability | API compatibility와 ABI compatibility가 동일하지 않음을 확인 | ADAPT binary interface boundary |
| JSON Schema official docs | Schema가 JSON 구조·타입·제약을 기술·검증함을 확인 | ADOPT only for JSON Schema context |
| GitHub Actions Artifacts / Packages / Releases | Artifact·Package·Release가 서로 다른 platform objects임을 확인 | ADAPT platform examples |
| Kubernetes Deployment docs | Deployment가 실행 workload 배치를 관리하는 개념임을 확인 | ADAPT deployment boundary |
| OpenTelemetry Signals / Profiles | Telemetry·Metrics·Logs·Traces·Profiles 관계 | ADOPT only for OpenTelemetry context |

## Approaches considered

### A. 한 개 대형 표에 모두 추가

장점: 검색이 가장 짧다.

기각 이유: 결함/요구/인터페이스/배포/관측성의 비교 축이 달라 `Artifact`, `Issue`, `Release` 같은 다의어가 섞인다.

### B. 기존 한 정본 안에 6개 책임별 섹션 추가 — 채택

장점:

- Wave 1/2의 단일 정본 구조 유지
- 각 용어군 내부에서만 혼동 방지 규칙을 읽을 수 있음
- 새 Skill·문서 정본·라우팅 표면 불필요
- semantic regression을 분야별로 작성 가능

### C. 별도 `TECHNICAL_GLOSSARY.md` 신설

기각 이유: 같은 질문에 두 번째 공용 용어 정본이 생기고 `DOCUMENTATION_MAP`/`START_HERE`를 다시 늘려야 한다.

## Changed-path contract

예상 최종 경로:

```text
docs/CONTROLLED_VOCABULARY.md
docs/CHANGELOG.md
docs/superpowers/specs/2026-08-14-controlled-vocabulary-wave3-design.md
docs/superpowers/plans/2026-08-14-controlled-vocabulary-wave3.md
tests/test_controlled_vocabulary_contract.py
```

보호/비변경:

```text
AGENTS.md
START_HERE.md
docs/DOCUMENTATION_MAP.md
skills/**
skills/SKILL_REGISTRY.json
schemas/**
.github/workflows/**
released/generated artifacts
project product files
```

기존 Controlled Vocabulary가 이미 `START_HERE`와 Documentation Map에 노출되어 있으므로 Wave 3에서 discovery surface를 다시 수정하지 않는다.

## TDD contract

production vocabulary 수정 전에 다음 6개 의미 회귀와 1개 중복/과장 회귀를 추가한다.

1. Issue/Bug/Defect/Incident boundary
2. Requirement/Specification/Constraint boundary
3. Dependency/Coupling/Cohesion boundary
4. API/ABI/Protocol/Schema boundary
5. Build/Package/Artifact/Deployment/Release boundary
6. Telemetry/Metrics/Logs/Traces/Profiles boundary
7. 기존 canonical row 중복·표준성 과장 방지

RED는 기존 Wave 1/2 tests는 PASS하고 Wave 3 신규 tests만 실패해야 한다.

## Adversarial attack lenses

- Issue를 Bug의 동의어로 축약했는가.
- Bug와 Defect의 조직별 차이를 Base가 가짜 보편 표준으로 만들었는가.
- Incident를 모든 결함에 붙여 운영 심각도를 과장했는가.
- Requirement/Specification/Constraint를 동일 계층으로 강제했는가.
- Dependency 한 개만으로 tight coupling을 확정했는가.
- low coupling을 dependency 없음으로 잘못 정의했는가.
- API와 ABI 호환성을 동일시했는가.
- OpenAPI를 모든 API 정의 규격으로 일반화했는가.
- Schema를 Protocol 전체로 승격했는가.
- Artifact와 Package를 동일시했는가.
- Deployment를 곧 Public Release라고 불렀는가.
- Release Candidate가 실제 Release로 중복 정의됐는가.
- Logs/Traces/Metrics/Profiles를 하나의 signal로 뭉갰는가.
- OpenTelemetry Profiles Alpha 상태를 profiling 일반의 미성숙으로 일반화했는가.
- 관측 데이터 존재를 root cause evidence로 과장했는가.

## Completion criteria

- 예상 5개 경로 이외 변경 없음
- Wave 1/2 의미 보존
- Wave 3 RED 증거 존재
- production GREEN 존재
- 적대적 추가 RED가 발견되면 먼저 test로 고정 후 최소 수정
- current-main / open PR path overlap 재확인
- exact-head `ubuntu-contract`, `docs-validation`, `publication-validation`, `base-v9-contract`, `adversarial-gate`, `ci-gate` 성공
- unresolved review thread 0
- expected-head squash merge
- merged main readback
- post-merge push full-matrix 성공

## Rollback

단일 squash merge를 revert한다. Runtime, Registry, Schema, workflow, project data migration은 없다.
