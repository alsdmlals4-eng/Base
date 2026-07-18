---
name: verifying-game-project-operating-system
description: Use after installing, migrating, or materially changing a game-project repository operating system, before a major gate or release, or when cold-start, documentation, skill routing, PDF, or automation health is uncertain.
---

# Verifying a Game Project Operating System

## Core principle

문서가 존재하는지만 보지 않는다. **시작 문서 → 책임 원본 → 선택적 스킬 → 실제 파일 → 검증 → PDF·인수인계**가 실제로 이어지는지 증거로 확인한다.

## Use when

- 운영체계를 새로 설치하거나 기존 프로젝트를 마이그레이션했다.
- 분야·폴더·본책·스킬·자동화 구조를 크게 변경했다.
- Vertical Slice, Production, Alpha, Beta, Release Candidate 등 주요 게이트 전이다.
- 새 채팅이 필요한 문서·스킬을 찾지 못한다.
- 문서·구현·자산·PDF·검증의 불일치가 의심된다.
- 주기적인 운영체계 Health Review를 수행한다.

## Do not use when

- 운영체계와 무관한 L0 수정이다.
- 작은 구현 작업에서 관련 자동 검사와 분야 검수만으로 충분하다.
- 실제 저장소 접근 없이 전체 운영체계가 정상이라고 선언하려는 경우다.
- 런타임 검증을 수행하지 않았는데 게임 품질까지 통과로 판정하려는 경우다.

## Required inputs

```yaml
target_repository:
base_version:
project_agents:
project_start_here:
documentation_map:
active_context_and_handoff:
development_gates:
project_skill_map:
skill_registry:
discipline_bibles:
publication_manifest:
visual_and_asset_manifests:
governance_config:
workflow_runs:
actual_code_data_assets_tests:
```

## Read first

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`
3. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
4. Documentation Map·Active Context·Development Gates
5. Project Skill Map·Skill Registry
6. 관련 분야 본책·스킬
7. Governance config·Workflow·검사 결과
8. 실제 코드·데이터·자산·테스트·PDF

## Verification areas

### 1. Root and entrypoints

- `[기획서]`가 저장소 루트 바로 아래에 있는가?
- `docs/[기획서]` 같은 중첩 복제본이 없는가?
- 사용자와 AI가 같은 시작 문서를 읽는가?
- START_HERE가 현재 상태·다음 작업·분야 본책·스킬·PDF를 연결하는가?

### 2. Responsibility and lifecycle

- 질문마다 현행 책임 원본이 하나인가?
- `[백업]`, `[보류]`, `[제거 후보]`가 기본 읽기에서 제외되는가?
- 승인·구현·검증·미확정이 실제 결과와 일치하는가?
- 이동·통합 후 오래된 참조가 남지 않았는가?

### 3. Skill routing and learning

- `SKILL_REGISTRY.json`의 활성 스킬 경로가 존재하는가?
- 각 활성 스킬에 사용·비사용 조건, trigger tags, Learning Log와 review trigger가 있는가?
- 각 분야의 진입 스킬이 등록됐는가?
- 새 요청에서 전체 스킬이 아니라 최소 skill set만 선택되는가?
- 스킬 사용 후 성공·실패·예외가 기록되는가?
- 반복된 교훈이 프로젝트 스킬 또는 Base 후보로 분류되는가?

### 4. Development gates and traceability

- Definition of Ready·Implementation·Verification·Documentation·Completion Gate가 연결되는가?
- 현재 제품 단계와 다음 Greenlight 증거가 명확한가?
- 샘플 결정 3개 이상이 다음 경로로 추적되는가?

```text
결정
→ 본책
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ 현재 상태
```

### 5. Visuals and publications

- 승인 이미지와 실제 캡처가 구분되는가?
- 캐노니컬 경로·Asset ID가 중복되지 않는가?
- 분야 PDF가 책임 Markdown과 승인 이미지에서 생성되는가?
- Publication Manifest·입력 해시·PDF 헤더·시각 검수가 최신인가?

### 6. Automation and enforcement

- Governance checker의 config 경로가 실제 프로젝트와 일치하는가?
- 정상·실패 회귀 테스트가 있는가?
- GitHub Actions가 실제로 실행됐는가?
- Required Status Check·CODEOWNERS·브랜치 보호의 실제 활성 상태를 파일 존재와 구분하는가?

### 7. Cold start

새 AI가 10분 안에 다음을 답해야 한다.

- 프로젝트 목적과 핵심 경험은 무엇인가?
- 현재 단계와 최우선 작업은 무엇인가?
- 무엇을 변경하면 안 되는가?
- 각 분야 본책과 진입 스킬은 어디인가?
- 실제 파일과 검증은 어디인가?
- 최신 승인 이미지와 PDF는 어디인가?
- 보류·미검증·위험은 어디인가?

## Output contract

```md
# 게임 프로젝트 운영체계 Health Review

## 결론
## 루트·시작 문서
## 책임 원본·수명주기
## 분야·Foundation 스킬 라우팅
## 스킬 학습·갱신 상태
## 개발 게이트·추적성
## 이미지·PDF
## 자동화·GitHub 강제
## 콜드 스타트 결과
## 실패·미검증
## 수정 우선순위
```

각 항목은 `PASS / PARTIAL / FAIL / NOT_RUN`으로 표시하고 증거 경로를 기록한다.

## Definition of Ready

- [ ] 저장소와 기준 브랜치·커밋을 확인했다.
- [ ] 운영체계 핵심 원본과 실제 파일에 접근할 수 있다.
- [ ] 실행할 자동·수동 검증 범위가 정해졌다.

## Definition of Done

- [ ] 모든 검수 영역에 상태와 증거가 있다.
- [ ] 실행하지 않은 검증은 NOT_RUN 또는 미검증이다.
- [ ] 구조적 실패와 제품 품질 실패를 구분했다.
- [ ] 수정 우선순위와 책임 분야가 있다.
- [ ] 반복된 운영 실패를 Learning Log와 관련 스킬에 반영했다.

## Failure conditions

- 파일 존재만으로 실제 작동·강제 상태를 통과 처리함
- 대상 저장소를 읽지 않고 추정함
- 전체 스킬을 로드해 선택적 호출을 검증하지 않음
- PDF 존재만 보고 입력 최신성·이미지·시각 검수를 생략함
- 런타임 테스트 미실행을 숨김
- 문제를 발견했지만 책임 원본·스킬·검사에 피드백하지 않음

## Learning contract

검수 실패는 운영체계 학습 입력이다.

```text
실패 영역
→ 재현 조건
→ 누락된 계약·검사
→ 프로젝트 전용 수정
→ 반복 여부 확인
→ Base Method·Skill·Template·Test 환류 후보
```

같은 실패가 두 번 이상 반복되면 관련 스킬의 review trigger를 활성화하고, 자동화 가능한 항목은 회귀 테스트 후보로 기록한다.
